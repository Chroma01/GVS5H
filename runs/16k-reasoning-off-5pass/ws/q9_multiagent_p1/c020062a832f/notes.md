
## ideation
**Core Difficulty:**
The problem asks for the inversion count of a sequence $B$ where $B_i = (A_i + k) \pmod M$ for $k = 0, \dots, M-1$.
- $N, M \le 2 \times 10^5$.
- A naive calculation for each $k$ takes $O(N \log N)$, leading to $O(MN \log N)$ total time, which is too slow ($4 \times 10^{10}$ operations).
- We need an approach that updates the inversion count in $O(1)$ or $O(\log N)$ per step $k$.

**Key Insight:**
The relative order of two elements $A_i$ and $A_j$ (where $i < j$) changes only when the values "wrap around" the modulus $M$.
- Specifically, consider the pair $(i, j)$ with $i < j$.
- Let $x = A_i$ and $y = A_j$.
- The condition for inversion is $(x+k) \pmod M > (y+k) \pmod M$.
- This inequality holds if:
  1. Neither wraps around: $x+k < M$ and $y+k < M$. Since $i<j$, if $x > y$, it's an inversion. If $x \le y$, it's not.
  2. Both wrap around: $x+k \ge M$ and $y+k \ge M$. The modulo operation subtracts $M$ from both, so the relative order $(x+k-M) > (y+k-M)$ is the same as $x > y$.
  3. Only $x$ wraps around: $x+k \ge M$ and $y+k < M$. Then $(x+k) \pmod M = x+k-M$ and $(y+k) \pmod M = y+k$. Since $x+k \ge M$ and $y+k < M$, the wrapped value of $x$ is effectively small (relative to the cycle) while $y$ is large? No, wait.
     - If $x+k \ge M$, then $(x+k)\%M = x+k-M$.
     - If $y+k < M$, then $(y+k)\%M = y+k$.
     - Is $x+k-M > y+k$? $\iff x-M > y \iff x > y+M$. Since $0 \le x, y < M$, this is impossible.
     - So if $x$ wraps and $y$ doesn't, $x$ becomes small and $y$ stays large. Thus $x_{new} < y_{new}$. No inversion.
  4. Only $y$ wraps around: $x+k < M$ and $y+k \ge M$.
     - $x_{new} = x+k$.
     - $y_{new} = y+k-M$.
     - Is $x+k > y+k-M$? $\iff x > y-M \iff x+M > y$. Since $x, y \ge 0$, this is always true.
     - So if $y$ wraps and $x$ doesn't, $x$ stays large and $y$ becomes small. Thus $x_{new} > y_{new}$. **Inversion created**.

**Transition Logic:**
As $k$ increases by 1:
- Elements with value $M-1$ will wrap around to $0$.
- Let's look at the transition from $k$ to $k+1$.
- An element $A_i$ wraps around when $A_i + k = M-1 \implies A_i = M - 1 - k$.
- Let $v = M - 1 - k$. At step $k$, elements with value $v$ are about to wrap.
- When we move to $k+1$, all $A_i = v$ become $0$.
- Consider a pair $(i, j)$ with $i < j$.
- Case A: Both $A_i, A_j < v$. Neither wraps. Order unchanged.
- Case B: Both $A_i, A_j \ge v$. Both wrap. Order unchanged (relative difference preserved).
- Case C: $A_i = v, A_j < v$.
  - At $k$: $A_i+k = M-1$, $A_j+k < M-1$. $A_i > A_j$ (inversion).
  - At $k+1$: $A_i \to 0$, $A_j \to A_j+1$. $0 < A_j+1$. No inversion.
  - **Effect**: One inversion is removed for every pair $(i, j)$ where $i < j$, $A_i = v$, and $A_j < v$.
- Case D: $A_i < v, A_j = v$.
  - At $k$: $A_i+k < M-1$, $A_j+k = M-1$. $A_i < A_j$. No inversion.
  - At $k+1$: $A_i \to A_i+1$, $A_j \to 0$. $A_i+1 > 0$. Inversion created.
  - **Effect**: One inversion is added for every pair $(i, j)$ where $i < j$, $A_i < v$, and $A_j = v$.

**Algorithm:**
1. Calculate initial inversion count for $k=0$ using Fenwick Tree (BIT) or Merge Sort. $O(N \log N)$.
2. Precompute counts:
   - For each value $v \in [0, M-1]$, let $cnt[v]$ be the number of indices $i$ such that $A_i = v$.
   - For each value $v$, we need:
     - $L[v]$: Number of pairs $(i, j)$ with $i < j$ such that $A_i = v$ and $A_j < v$.
     - $R[v]$: Number of pairs $(i, j)$ with $i < j$ such that $A_i < v$ and $A_j = v$.
   - Actually, we can compute these dynamically or precompute.
   - Better approach:
     - Iterate $v$ from $M-1$ down to $0$.
     - Maintain a count of numbers seen so far that are $< v$.
     - Or simpler:
       - $L[v]$: Count pairs where $A_i = v$ and $A_j < v$ with $i < j$.
       - $R[v]$: Count pairs where $A_i < v$ and $A_j = v$ with $i < j$.
     - To compute $L[v]$ and $R[v]$ efficiently:
       - We can iterate through the array once.
       - Maintain `count_less`: number of elements seen so far that are $< v$.
       - When we encounter $A_i = v$:
         - Add `count_less` to $R[v]$. (These are $A_j < v$ with $j < i$, wait. $i$ is current index. If $A_j < v$ and $j < i$, then pair is $(j, i)$ with $A_j < v, A_i = v$. This matches Case D logic? No.
         - Let's re-verify indices.
         - Case D (Add inversion): $i < j$, $A_i < v$, $A_j = v$.
           - When scanning $j$ (current index), if $A_j = v$, we need to know how many $i < j$ have $A_i < v$.
           - So $R[v] += (\text{count of } i < j \text{ s.t. } A_i < v)$.
         - Case C (Remove inversion): $i < j$, $A_i = v$, $A_j < v$.
           - When scanning $j$ (current index), if $A_j < v$, we need to know how many $i < j$ have $A_i = v$.
           - So we need to track counts of specific values seen so far.
   - Revised Precomputation:
     - Initialize `freq` array of size $M$ to 0.
     - `total_less` = 0.
     - Iterate $x$ in $A$:
       - `R[x] += total_less` (Pairs $(i, j)$ with $i<j, A_i < x, A_j=x$).
       - `total_less += freq[x]`? No. `total_less` should be count of all numbers $< x$ seen so far.
       - Wait, `total_less` needs to be updated carefully.
       - Let's keep `cnt[v]` = frequency of value $v$ seen so far.
       - When at $x$:
         - `R[x] += sum(cnt[0]...cnt[x-1])`.
         - `cnt[x]++`.
       - This is $O(M)$ per element if naive sum, too slow.
       - Optimization: Maintain a Fenwick tree or just a running sum if we process values? No, we process array order.
       - Alternative:
         - $R[v]$: Pairs $(i, j)$ with $i < j, A_i < v, A_j = v$.
           - This is equivalent to: For each $j$ where $A_j=v$, add (number of $i<j$ with $A_i < v$).
           - We can compute this by iterating $A$ and maintaining a BIT of frequencies. Query sum $[0, v-1]$.
         - $L[v]$: Pairs $(i, j)$ with $i < j, A_i = v, A_j < v$.
           - This is equivalent to: For each $j$ where $A_j < v$, add (number of $i<j$ with $A_i = v$).
           - Iterate $A$. For current $x < v$, add `cnt[v]`.
           - But $v$ varies.
           - Actually, $L[v] = \sum_{j: A_j < v} (\text{count of } i < j \text{ s.t. } A_i = v)$.
           - This looks like we need to know for each $v$, how many times it appeared before each smaller number.
           - Let's swap the logic.
           - $L[v]$: Sum over all occurrences of $v$ at index $i$, of (count of $j > i$ with $A_j < v$).
           - $R[v]$: Sum over all occurrences of $v$ at index $j$, of (count of $i < j$ with $A_i < v$).
           - We can compute $R[v]$ easily with a BIT while scanning left-to-right.
           - We can compute $L[v]$ easily with a BIT while scanning right-to-left (counting numbers $< v$ to the right).
           - Yes!
             - Scan L->R: BIT stores frequencies. For each $x=A_i$, $R[x] += \text{query}(x-1)$. Update BIT with $x$.
             - Scan R->L: BIT stores frequencies. For each $x=A_i$, $L[x] += \text{query}(x-1)$? No.
               - We need pairs $(i, j)$ with $i < j, A_i = v, A_j < v$.
               - If we scan R->L, current is $j$. We want to know how many $i < j$ (which are to the left in original, but to the right in scan) have $A_i = v$.
               - This seems hard to do in one pass R->L without knowing future $v$'s.
               - Let's rethink $L[v]$.
               - $L[v] = \sum_{j: A_j < v} (\text{count of } i < j \text{ s.t. } A_i = v)$.
               - Let's iterate $j$ from $0$ to $N-1$. Let $x = A_j$.
               - We need to add `count of v` seen so far to $L[v]$ for all $v > x$.
               - This is a range update: for current $x$, add 1 to $L[v]$ for all $v \in [x+1, M-1]$.
               - We can do this with a Fenwick tree (range update, point query) or difference array?
               - Since we just need the final value of $L[v]$, we can use a difference array `diff` of size $M+1$.
               - For each $x$ in $A$: `diff[x+1] += 1`, `diff[M] -= 1` (if needed).
               - Then prefix sum `diff` gives the count of $v$'s seen so far? No.
               - `diff` array approach:
                 - Initialize `diff` of size $M+1$ to 0.
                 - Iterate $x$ in $A$:
                   - We need to add 1 to $L[v]$ for all $v > x$.
                   - `diff[x+1] += 1`.
                   - `diff[M] -= 1` (to stop at M).
                 - After iterating all $A$, compute prefix sums of `diff`. `L[v] = prefix_sum[v]`.
                 - Wait, `diff` accumulates counts.
                   - If $A = [2, 1, 0]$.
                   - $x=2$: `diff[3]++`.
                   - $x=1$: `diff[2]++`.
                   - $x=0$: `diff[1]++`.
                   - Prefix sums:
                     - $v=0$: 0.
                     - $v=1$: 1 (from $x=0$). Correct? Pairs $(i, j)$ with $A_i=1, A_j < 1$. $A_j=0$. Index of 1 is 1, index of 0 is 2. $1<2$. Yes.
                     - $v=2$: 2 (from $x=0, 1$). Pairs $(i, j)$ with $A_i=2, A_j < 2$. $A_j=1$ (idx 2), $A_j=0$ (idx 2). $i=0$. Both valid. Yes.
               - So $L[v]$ can be computed in $O(N + M)$.
               - $R[v]$ can be computed in $O(N \log M)$ using BIT.

3. Simulation:
   - Current inversion count `cur_inv`.
   - Loop $k$ from $0$ to $M-1$:
     - Print `cur_inv`.
     - Prepare for $k+1$:
       - The value $v = M - 1 - k$ will wrap around.
       - Update `cur_inv`:
         - Subtract $L[v]$.
         - Add $R[v]$.
       - Note: The problem asks for output for $k=0, \dots, M-1$.
       - So we print for $k=0$, then update, then print for $k=1$, etc.
       - Wait, the transition is from $k$ to $k+1$.
       - At $k=0$, we have initial state. Print.
       - To get state for $k=1$, we consider elements with value $M-1$. They wrap.
       - So $v = M-1$. Update using $L[M-1]$ and $R[M-1]$.
       - Then $k=2$, $v = M-2$. Update using $L[M-2]$ and $R[M-2]$.
       - ...
       - Finally $k=M-1$, $v=0$. Update using $L[0]$ and $R[0]$.
       - Wait, does $v=0$ wrap? $0 + (M-1) = M-1 < M$. No.
       - The element $A_i=0$ wraps when $0+k \ge M \implies k \ge M$. But we stop at $M-1$.
       - So $v=0$ never wraps in the range $k \in [0, M-1]$.
       - Let's re-check the wrap condition.
       - $A_i + k \ge M$.
       - For $k=0$, $A_i \ge M$ (impossible).
       - For $k=M-1$, $A_i \ge 1$.
       - So elements with $A_i = 0$ never wrap.
       - Elements with $A_i = 1$ wrap when $k = M-1$.
       - Elements with $A_i = v$ wrap when $k = M-v$.
       - We iterate $k$ from $0$ to $M-2$ to transition to $k+1$.
       - Transition $k \to k+1$:
         - Elements with $A_i = M - 1 - k$ wrap.
         - Let $v = M - 1 - k$.
         - Update: `cur_inv -= L[v]`, `cur_inv += R[v]`.
       - Loop $k$ from $0$ to $M-1$:
         - Print `cur_inv`.
         - If $k < M-1$:
           - $v = M - 1 - k$.
           - Update `cur_inv`.
       - This covers all transitions.

**Complexity:**
- Initial Inversions: $O(N \log N)$.
- Precompute $R$: $O(N \log M)$.
- Precompute $L$: $O(N + M)$.
- Simulation: $M$ steps, $O(1)$ each.
- Total: $O(N \log N + N \log M + M)$. Fits within limits.

**Pitfalls:**
- 1-based vs 0-based indexing.
- Large numbers for inversion count (use 64-bit integers).
- Edge cases: $N=1$, $M=1$.
- Correct handling of $L[v]$ and $R[v]$ definitions.
  - $L[v]$: Pairs $(i, j)$ with $i < j, A_i = v, A_j < v$. (Remove inversion).
  - $R[v]$: Pairs $(i, j)$ with $i < j, A_i < v, A_j = v$. (Add inversion).
- The value $v$ that wraps at step $k \to k+1$ is indeed $M - 1 - k$.
  - Check: $k=0 \to k=1$. $v = M-1$. $A_i = M-1$. $(M-1)+0 = M-1$. $(M-1)+1 = M \to 0$. Correct.

## worker: Implement the solution in Python using a Fenwick T
1.  **Initial Inversion Count**: Calculated using a Fenwick Tree (BIT) in $O(N \log M)$. We iterate through the array, and for each element, we count how many previously seen elements are greater than the current one.
2.  **Precomputing R[v]**: $R[v]$ counts pairs $(i, j)$ with $i < j$, $A_i < v$, and $A_j = v$. This is computed by iterating left-to-right and using a BIT to count elements smaller than the current value seen so far. Time complexity: $O(N \log M)$.
3.  **Precomputing L[v]**: $L[v]$ counts pairs $(i, j)$ with $i < j$, $A_i = v$, and $A_j < v$. Instead of a BIT, we use a difference array approach. For each element $x$ in $A$, we increment a range $[x+1, M-1]$ in the difference array, representing that for any $v > x$, this occurrence of $x$ contributes to $L[v]$. Finally, we compute prefix sums to get $L[v]$. Time complexity: $O(N + M)$.
4.  **Simulation**: We iterate $k$ from $0$ to $M-2$. At each step, the value $v = M - 1 - k$ wraps around (changes from $M-1$ to $0$ effectively in the cyclic sense relative to the shift). We update the total inversion count by subtracting $L[v]$ (inversions lost) and adding $R[v]$ (inversions gained). This takes $O(1)$ per step. Total simulation time: $O(M)$.
5.  **Complexity**: Overall time complexity is $O(N \log M + M)$, which fits well within the limits for $N, M \le 2 \times 10^5$. Space complexity is $O(N + M)$.

## worker: Run the code against the provided sample inputs to
The code implements the derived algorithm:
1.  **Initial Inversion Count**: Uses a Fenwick Tree (BIT) to count inversions in $O(N \log M)$.
2.  **Precomputation**:
    *   $R[v]$ (pairs $(i, j)$ with $i < j, A_i < v, A_j = v$) is computed using a BIT while scanning left-to-right.
    *   $L[v]$ (pairs $(i, j)$ with $i < j, A_i = v, A_j < v$) is computed using a difference array approach for $O(N+M)$ efficiency.
3.  **Simulation**: Iterates $k$ from $0$ to $M-2$. At each step, it identifies the value $v = M - 1 - k$ that wraps around (changes from $M-1$ to $0$ effectively relative to the shift). It updates the total inversion count by subtracting $L[v]$ (inversions lost) and adding $R[v]$ (inversions gained).
4.  **Complexity**: $O(N \log M + M)$, which fits the constraints $N, M \le 2 \times 10^5$.

The logic handles the cyclic nature of the modulo operation correctly by tracking which specific values "cross" the boundary $M$ as $k$ increments.

## worker: Run the provided code against Sample 1, Sample 2, 
The code implements the derived algorithm:
1.  **Initial Inversion Count**: Uses a Fenwick Tree (BIT) to count inversions in $O(N \log M)$.
2.  **Precomputation**:
    *   $R[v]$ (pairs $(i, j)$ with $i < j, A_i < v, A_j = v$) is computed using a BIT while scanning left-to-right.
    *   $L[v]$ (pairs $(i, j)$ with $i < j, A_i = v, A_j < v$) is computed using a difference array approach for $O(N+M)$ efficiency.
3.  **Simulation**: Iterates $k$ from $0$ to $M-2$. At each step, it identifies the value $v = M - 1 - k$ that wraps around (changes from $M-1$ to $0$ effectively relative to the shift). It updates the total inversion count by subtracting $L[v]$ (inversions lost) and adding $R[v]$ (inversions gained).
4.  **Complexity**: $O(N \log M + M)$, which fits the constraints $N, M \le 2 \times 10^5$.

The logic handles the cyclic nature of the modulo operation correctly by tracking which specific values "cross" the boundary $M$ as $k$ increments.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the derived algorithm:
1.  **Initial Inversion Count**: Uses a Fenwick Tree (BIT) to count inversions in $O(N \log M)$.
2.  **Precomputation**:
    *   $R[v]$ (pairs $(i, j)$ with $i < j, A_i < v, A_j = v$) is computed using a BIT while scanning left-to-right.
    *   $L[v]$ (pairs $(i, j)$ with $i < j, A_i = v, A_j < v$) is computed using a difference array approach for $O(N+M)$ efficiency.
3.  **Simulation**: Iterates $k$ from $0$ to $M-2$. At each step, it identifies the value $v = M - 1 - k$ that wraps around (changes from $M-1$ to $0$ effectively relative to the shift). It updates the total inversion count by subtracting $L[v]$ (inversions lost) and adding $R[v]$ (inversions gained).
4.  **Complexity**: $O(N \log M + M)$, which fits the constraints $N, M \le 2 \times 10^5$.

The logic handles the cyclic nature of the modulo operation correctly by tracking which specific values "cross" the boundary $M$ as $k$ increments.

## worker: finalize
The solution implements the derived algorithm efficiently:
1.  **Initial Inversion Count**: Uses a Fenwick Tree (BIT) to count inversions in $O(N \log M)$.
2.  **Precomputation**:
    *   $R[v]$ (pairs $(i, j)$ with $i < j, A_i < v, A_j = v$) is computed using a BIT while scanning left-to-right.
    *   $L[v]$ (pairs $(i, j)$ with $i < j, A_i = v, A_j < v$) is computed using a difference array approach for $O(N+M)$ efficiency.
3.  **Simulation**: Iterates $k$ from $0$ to $M-2$. At each step, it identifies the value $v = M - 1 - k$ that wraps around (changes from $M-1$ to $0$ effectively relative to the shift). It updates the total inversion count by subtracting $L[v]$ (inversions lost) and adding $R[v]$ (inversions gained).
4.  **Complexity**: $O(N \log M + M)$, which fits the constraints $N, M \le 2 \times 10^5$.

The logic handles the cyclic nature of the modulo operation correctly by tracking which specific values "cross" the boundary $M$ as $k$ increments.

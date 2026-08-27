
## ideation
**Core Difficulty:**
The problem asks for $N$ answers, where each answer depends on selecting $K$ elements including a specific $A_i$ to maximize their GCD.
- $N$ is up to $1.2 \times 10^6$.
- $A_i$ is up to $10^6$.
- A naive solution checking all subsets is impossible ($O(N^K)$).
- Even checking all pairs or triplets is too slow if not careful.
- The key constraint is the small range of values ($V = 10^6$), which suggests an approach based on the values of $A_i$ rather than their indices.

**Candidate Approaches:**
1.  **Frequency Array + Sieve-like Counting:**
    - Create a frequency array `cnt` where `cnt[x]` is the number of times value `x` appears in $A$.
    - For each possible GCD candidate $g$ from $V$ down to $1$:
        - Count how many numbers in $A$ are multiples of $g$. This can be done by summing `cnt[j]` for $j = g, 2g, 3g, \dots$.
        - If the count $\ge K$, then $g$ is a valid GCD for any element that is a multiple of $g$.
    - To answer for each $A_i$ efficiently:
        - Initialize an answer array `ans` with 1 (or 0).
        - Iterate $g$ from $V$ down to $1$. If `count(g) >= K`:
            - For every multiple $j = g, 2g, \dots$ present in $A$, update `ans[j] = max(ans[j], g)`.
        - Finally, map the value-based answers back to the original indices. Since multiple indices might have the same value $A_i$, we can store the maximum valid $g$ for each value $v$ in an array `max_g[v]`. Then for each $i$, the answer is `max_g[A[i]]`.

2.  **Optimization of Step 1:**
    - The summation for multiples takes $O(V/1 + V/2 + \dots + V/V) = O(V \log V)$. With $V=10^6$, this is roughly $1.4 \times 10^7$ operations, which is very fast.
    - The update step in the inner loop: If we iterate all multiples $j$ for every valid $g$, the worst-case complexity could be high if many $g$ are valid. However, note that we only need to update `max_g[j]` if $g >$ current `max_g[j]`.
    - Actually, we can optimize the update: We don't need to iterate all multiples for every $g$. Instead, we can just compute `max_g[v]` for each value $v$ directly.
    - Refined Algorithm:
        1. Count frequencies of each number in $A$.
        2. Create `max_g` array of size $V+1$, initialized to 1.
        3. Iterate $g$ from $V$ down to $1$:
           - Calculate `num_multiples` = sum of frequencies of multiples of $g$.
           - If `num_multiples >= K`:
             - For each multiple $j = g, 2g, \dots \le V$:
               - If `cnt[j] > 0` (meaning $j$ exists in $A$):
                 - `max_g[j] = max(max_g[j], g)`
        4. Output `max_g[A[i]]` for each $i$.

    - **Complexity Check:**
      - Counting multiples: $O(V \log V)$.
      - Updating `max_g`: In the worst case, if many $g$ are valid, we might touch many multiples. However, notice that if $g$ is valid, then any divisor of $g$ is also a valid GCD for the same set (conceptually), but we want the *maximum*.
      - Is the update step $O(V \log V)$?
        - Consider the case where all numbers are multiples of $g$. Then we iterate $V/g$ times.
        - Sum of $V/g$ for all $g$ is $V \log V$.
        - BUT, we only do the inner loop if `num_multiples >= K`.
        - Even if we do it for all $g$, the total iterations is $\sum_{g=1}^V \frac{V}{g} = O(V \log V)$.
        - So the total time complexity is $O(V \log V + N)$.
        - With $V=10^6, N=1.2 \times 10^6$, this fits well within typical time limits (1-2 seconds) for Python if implemented efficiently (using PyPy or careful array access). Standard Python might be tight but likely passable given the constant factors are small (simple array additions).

**Pitfalls:**
- **Python Performance:** $10^6$ iterations in pure Python can be slow. Using `sys.stdin.read` and pre-allocating lists is crucial.
- **Memory:** Arrays of size $10^6$ are fine.
- **Logic Error:** Ensuring that we only consider elements *present* in the input array when updating `max_g`. The count check ensures we have enough elements, but the update must target only those $A_i$ that are multiples of $g$.
- **Edge Cases:** $K=1$ (answer is always $A_i$), $K=N$, all $A_i$ same, all $A_i$ coprime.
- **Order of Iteration:** Must iterate $g$ from largest to smallest? Actually, the order doesn't strictly matter for correctness if we take `max`, but iterating large to small allows early pruning if we wanted, though here we need to check all valid $g$. Since we take `max`, the order of $g$ doesn't change the final result, but the logic holds regardless.

**Refined Plan:**
1. Read input efficiently.
2. Build frequency array `cnt` for values up to $10^6$.
3. Initialize `ans_val` array of size $10^6+1$ with 1.
4. Loop $g$ from $10^6$ down to $1$:
   - Count multiples: `c = sum(cnt[g*i] for i in range(1, 1000000//g + 1))`
   - If `c >= K`:
     - For `j` in `g, 2g, ...`:
       - If `cnt[j] > 0`: `ans_val[j] = max(ans_val[j], g)`
5. Print `ans_val[A[i]]` for each $i$.

Wait, there is a potential optimization/simplification.
If `c >= K`, then for any $j$ which is a multiple of $g$ and exists in $A$, $g$ is a candidate answer.
Since we want the maximum $g$, and we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific $j$, that $g$ is the largest possible for $j$?
No, because a larger $g'$ (processed earlier) might also be a divisor of $j$.
Example: $A = \{6, 12\}, K=2$.
$g=12$: count=1 (<2).
$g=6$: count=2 (>=2). Update $j=6, 12$ with 6.
$g=3$: count=2 (>=2). Update $j=6, 12$ with 3. But 6 is better.
So if we iterate $g$ from $V$ down to $1$, the first time we find a valid $g$ for a specific $j$, is it the maximum?
Yes! Because if a larger $g' > g$ was valid for $j$, we would have processed $g'$ earlier and updated $j$ with $g'$.
So, we can initialize `ans_val` to 0 (or 1).
When iterating $g$ from $V$ down to $1$:
  If `count(g) >= K`:
    For each multiple $j$ of $g$ present in $A$:
      If `ans_val[j] == 0`: `ans_val[j] = g`
This avoids the `max` check and potentially speeds up the inner loop (stop updating once set? No, we must check all $g$ because a smaller $g$ might be valid but we only care about the first one we see which is the largest).
Actually, if `ans_val[j]` is already set, it means a larger $g$ was found. We don't need to update it again.
So the logic:
Iterate $g$ from $V$ down to $1$.
If `count(g) >= K`:
  For $j = g, 2g, \dots$:
    If `cnt[j] > 0` and `ans_val[j] == 0`:
      `ans_val[j] = g`
This is correct and efficient.

## worker: Read input efficiently.
1.  **Algorithm Selection**: The problem requires finding the maximum GCD of a subset of size $K$ containing $A_i$. Since the values $A_i$ are small ($\le 10^6$), we can iterate over all possible GCD values $g$.
2.  **Frequency Array**: We first count the occurrences of each number in $A$ using a frequency array `cnt`.
3.  **Sieve-like Approach**: We iterate $g$ from $10^6$ down to $1$. For each $g$, we count how many numbers in $A$ are multiples of $g$ by summing `cnt[g], cnt[2g], cnt[3g], ...`.
4.  **Optimization**: If the count of multiples is $\ge K$, then $g$ is a valid GCD for any element that is a multiple of $g$. Since we iterate $g$ from largest to smallest, the first time we encounter a valid $g$ for a specific value $v$, that $g$ is the maximum possible GCD for $v$. We store this in `max_g[v]`.
5.  **Complexity**:
    -   Counting multiples: $\sum_{g=1}^{V} \frac{V}{g} = O(V \log V)$.
    -   Updating `max_g`: In the worst case, we might visit multiples, but we only update if `max_g` is 0. The total number of updates across all $g$ is bounded by the number of distinct elements in $A$ times the number of divisors, but practically, the inner loop runs $V/g$ times. The total complexity is dominated by the harmonic series sum, $O(V \log V)$.
    -   With $V = 10^6$, $V \log V \approx 1.4 \times 10^7$ operations, which fits within the time limit for Python if implemented efficiently (using simple array access and avoiding heavy object creation).
6.  **Input/Output**: Used `sys.stdin.read().split()` for fast I/O and `sys.stdout.write` for fast output.

## worker: Write the Python code implementing the solution us
- **Algorithm**: The solution uses a frequency array `cnt` to count occurrences of each number in $A$. It then iterates backwards from the maximum value in $A$ down to 1. For each candidate GCD $g$, it counts how many numbers in $A$ are multiples of $g$. If this count is at least $K$, $g$ is a valid GCD for any element that is a multiple of $g$. Since we iterate from largest to smallest, the first valid $g$ found for a specific value $v$ is the maximum possible GCD for subsets containing $v$.
- **Complexity**: The nested loops run in $O(V \log V)$ time where $V = \max(A)$, due to the harmonic series sum of iterations ($\sum_{g=1}^V \frac{V}{g}$). Given $V \le 10^6$, this is approximately $1.4 \times 10^7$ operations, which fits well within the time limit.
- **Optimizations**:
  - Dynamic sizing of arrays based on $\max(A)$ instead of a fixed $10^6$ to save memory and initialization time if inputs are small.
  - Fast I/O using `sys.stdin.read` and `sys.stdout.write`.
  - Early termination of updates: `max_g[multiple]` is only updated if it is 0, leveraging the downward iteration order.
- **Edge Cases**: Handles $K=1$ correctly (answer is $A_i$ itself), $K=N$, and cases where no large GCD exists (defaults to 1).

## worker: Run the code against the provided sample inputs to
The code implements the $O(V \log V)$ algorithm where $V = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Backward Iteration**: Iterates $g$ from $V$ down to 1.
3.  **Counting Multiples**: For each $g$, sums `cnt[multiple]` for $multiple = g, 2g, \dots$.
4.  **Validation**: If the count of multiples $\ge K$, $g$ is a valid GCD for any element that is a multiple of $g$.
5.  **Greedy Update**: Since we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific value $v$, it is the maximum possible GCD for subsets containing $v$. We update `max_g[v]` only if it hasn't been set yet (is 0).
6.  **Efficiency**: The nested loops run in harmonic series time $O(V \log V)$. With $V=10^6$, this is roughly $1.4 \times 10^7$ operations, which is efficient enough for Python given the simple operations inside the loops. Fast I/O is used.

## worker: Run the provided sample inputs to verify correctne
The solution implements the $O(V \log V)$ algorithm where $V = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Backward Iteration**: Iterates $g$ from $V$ down to 1.
3.  **Counting Multiples**: For each $g$, sums `cnt[multiple]` for $multiple = g, 2g, \dots$.
4.  **Validation**: If the count of multiples $\ge K$, $g$ is a valid GCD for any element that is a multiple of $g$.
5.  **Greedy Update**: Since we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific value $v$, it is the maximum possible GCD for subsets containing $v$. We update `max_g[v]` only if it hasn't been set yet (is 0).
6.  **Efficiency**: The nested loops run in harmonic series time $O(V \log V)$. With $V=10^6$, this is roughly $1.4 \times 10^7$ operations, which is efficient enough for Python given the simple operations inside the loops. Fast I/O is used.

## worker: finalize
The solution implements an $O(V \log V)$ algorithm where $V = \max(A)$.
1.  **Frequency Array**: Counts occurrences of each number in $A$.
2.  **Backward Iteration**: Iterates $g$ from $V$ down to 1.
3.  **Counting Multiples**: For each $g$, sums `cnt[multiple]` for $multiple = g, 2g, \dots$.
4.  **Validation**: If the count of multiples $\ge K$, $g$ is a valid GCD for any element that is a multiple of $g$.
5.  **Greedy Update**: Since we iterate $g$ downwards, the first time we encounter a valid $g$ for a specific value $v$, it is the maximum possible GCD for subsets containing $v$. We update `max_g[v]` only if it hasn't been set yet (is 0).
6.  **Efficiency**: The nested loops run in harmonic series time $O(V \log V)$. With $V=10^6$, this is roughly $1.4 \times 10^7$ operations, which is efficient enough for Python given the simple operations inside the loops. Fast I/O is used.

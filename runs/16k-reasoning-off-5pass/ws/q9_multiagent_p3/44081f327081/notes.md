
## ideation
The core difficulty is efficiently finding the maximum GCD for each element $A_i$ when selecting a subset of size $K$ that includes $A_i$. A naive approach checking all subsets is impossible ($O(N^K)$). Even iterating all pairs is too slow ($O(N^2)$). The constraints $N, A_i \le 1.2 \times 10^6$ suggest an algorithm close to $O(M \log M + N \sqrt{M})$ or $O(M \log M + N \cdot d_{max})$, where $M = \max(A_i)$.

**Candidate Approaches:**
1.  **Frequency + Divisor Enumeration:**
    -   Precompute the frequency of each number in $A$.
    -   Compute `count[g]`: the number of elements in $A$ that are multiples of $g$. This can be done in $O(M \log M)$ by iterating $g$ from 1 to $M$ and adding frequencies of its multiples.
    -   For each $A_i$, iterate through all its divisors. If a divisor $d$ has `count[d] >= K`, it is a valid GCD for a subset including $A_i$. The answer for $A_i$ is the maximum such $d$.
    -   Complexity: $O(M \log M + N \cdot d_{max})$, where $d_{max}$ is the max number of divisors for numbers up to $10^6$ (which is 240 for 720720). This is very fast.

2.  **Reverse Iteration on GCD:**
    -   Compute `count[g]` as above.
    -   Initialize `ans[i] = 1` for all $i$.
    -   Iterate $g$ from $M$ down to 1. If `count[g] >= K`:
        -   For every index $i$ where $A_i$ is a multiple of $g$, update `ans[i] = max(ans[i], g)`.
    -   To do this efficiently without iterating all multiples for every $g$ (which could be $O(M^2)$ in worst case if not careful), we can store indices for each number or use the fact that we only care about the *first* time we see a valid $g$ if we process carefully? Actually, iterating multiples for each $g$ is $O(M \log M)$ total.
    -   Wait, iterating multiples for each $g$ to update answers:
        -   Outer loop $g: M \to 1$.
        -   If `count[g] >= K`:
            -   Iterate $j = g, 2g, \dots$ up to $M$.
            -   For each $j$ present in $A$, update `ans[index_of_j]`.
        -   Since we want the *maximum* GCD, processing $g$ from large to small means the first time we update `ans[i]`, it is the largest possible. We can stop updating for a specific $A_i$ once it's set.
        -   However, we need to know which indices correspond to value $j$. We can precompute `pos[v]` = list of indices where $A_i = v$.
        -   Total complexity: $\sum_{g=1}^M \frac{M}{g} = O(M \log M)$. Inside the loop, we iterate over occurrences. Each $A_i$ is visited once (when $g$ is its largest valid divisor). So total updates are $O(N)$.
    -   This approach is $O(M \log M + N)$.

**Pitfalls:**
-   **Duplicate Values:** Multiple indices can have the same value $A_i$. The `pos` array must handle lists of indices.
-   **Memory:** Storing `pos` for all numbers up to $10^6$ is fine ($1.2 \times 10^6$ integers total).
-   **Logic Error:** In the reverse iteration approach, simply updating `ans[i] = g` is correct because we go from largest $g$ to smallest. The first valid $g$ we encounter for a specific $A_i$ is the maximum. We must ensure we don't re-process an index once its answer is found to save time, though the math guarantees we won't visit it again with a larger $g$ later (since we go down). Actually, we visit $A_i$ at $g=A_i$, then $g=A_i/2$, etc. But we only care if `count[g] >= K`.
-   **Constraint Check:** $K$ must be $\le N$. If $K >$ total multiples of $g$, skip.

**Decision:**
Approach 2 (Reverse Iteration) seems slightly cleaner to implement for the "maximum" logic naturally, but Approach 1 (Divisor Enumeration) is extremely robust and avoids the overhead of managing lists of positions if we precompute divisors for each number. Given $N$ is large, precomputing divisors for all $A_i$ might take memory/time?
Actually, precomputing divisors for all numbers up to $M$ takes $O(M \log M)$. Then for each $A_i$, we iterate its divisors.
Let's refine Approach 1:
1. Count frequencies `cnt[x]`.
2. Compute `total_multiples[g]` for all $g \in [1, M]$.
3. Precompute divisors for all numbers up to $M$? Or just compute divisors on the fly?
   - Computing divisors on the fly for each $A_i$ takes $O(\sqrt{A_i})$. Total $O(N \sqrt{M})$. With $N=10^6, \sqrt{M}=1000$, operations $\approx 10^9$, which might be TLE (1-2 seconds limit usually allows $\sim 10^8$).
   - Better: Precompute divisors for all numbers up to $M$ in $O(M \log M)$. Store them in a flattened array or list of lists. Memory: $\sum d(i) \approx M \log M \approx 10^6 \times 14 \approx 1.4 \times 10^7$ integers. This fits easily in memory (50-100MB).
   - Then for each $A_i$, iterate precomputed divisors, check `total_multiples[d] >= K`, take max.

Approach 2 (Reverse Iteration) complexity:
1. `cnt[x]` freq.
2. `total_multiples[g]` in $O(M \log M)$.
3. `pos[v]` list of indices.
4. Loop $g$ from $M$ down to 1.
   - If `total_multiples[g] >= K`:
     - Loop $v = g, 2g, \dots$:
       - For each index $idx$ in `pos[v]`:
         - If `ans[idx]` not set, `ans[idx] = g`.
         - Mark `ans[idx]` as set.
   - Optimization: We only need to process $v$ if `pos[v]` is not empty.
   - Total complexity: The inner loop over $v$ runs $M/g$ times. The innermost loop over `pos[v]` runs exactly once per index $i$ across the entire execution (because once `ans[i]` is set, we can skip it). So total work is $O(M \log M + N)$. This is strictly better than precomputing divisors for all numbers if $N$ is small, but here $N \approx M$. Both are fine. Approach 2 is likely faster constant-wise.

Let's stick with **Approach 2** for optimal performance.

## worker: Read input $N$, $K$, and the sequence $A$. Determi
The solution implements the "Reverse Iteration on GCD" approach.
1.  **Frequency & Positions**: We first count the frequency of each number in $A$ and store the indices of each number in a list `pos`. This handles duplicate values correctly.
2.  **Multiples Count**: We compute `total_multiples[g]`, which is the count of numbers in $A$ divisible by $g$. This is done efficiently in $O(M \log M)$ where $M = \max(A)$ by iterating through multiples.
3.  **Greedy Assignment**: We iterate $g$ from $M$ down to 1. If `total_multiples[g] >= K`, it means there exists a subset of size $K$ with GCD $g$. Since we iterate downwards, the first time we encounter such a $g$ for a specific element $A_i$ (where $A_i$ is a multiple of $g$), that $g$ is the maximum possible GCD for $A_i$. We update the answer for $A_i$ and mark it so we don't process it again for smaller $g$'s.
4.  **Complexity**:
    -   Counting multiples: $O(M \log M)$.
    -   Updating answers: The outer loop runs $M$ times. The inner loop over multiples runs $M/g$ times. The innermost loop over `pos[v]` runs exactly once per index $i$ across the entire execution (because of the check `if ans[idx] == 1`). Thus, the total time for updates is $O(M \log M + N)$.
    -   Overall Time Complexity: $O(M \log M + N)$, which fits well within the limits ($N, M \le 1.2 \times 10^6$).
    -   Space Complexity: $O(M + N)$ for arrays and lists.

## worker: Run the code against the provided sample inputs to
The code implements the "Reverse Iteration on GCD" strategy.
1.  **Input Parsing**: Reads $N, K$ and the sequence $A$.
2.  **Preprocessing**:
    -   Computes `cnt[x]`: frequency of each number $x$ in $A$.
    -   Computes `pos[x]`: list of indices where $A[i] = x$.
3.  **Multiples Count**:
    -   Computes `total_multiples[g]`: the count of numbers in $A$ that are multiples of $g$. This is done in $O(M \log M)$ where $M = \max(A)$.
4.  **Greedy Assignment**:
    -   Iterates $g$ from $M$ down to 1.
    -   If `total_multiples[g] >= K`, it means a subset of size $K$ with GCD $g$ exists.
    -   For every multiple $v$ of $g$ present in $A$, we update the answer for all indices $i$ where $A[i] = v$.
    -   Since we iterate $g$ downwards, the first time we update `ans[i]`, it is the maximum possible GCD for that element. We use `ans[i] == 1` as a flag to ensure each index is updated exactly once.
5.  **Output**: Prints the computed answers.

This approach has a time complexity of $O(M \log M + N)$ and space complexity of $O(M + N)$, which fits the constraints ($N, A_i \le 1.2 \times 10^6$).

## worker: Run the provided sample inputs to verify correctne
The provided code implements the "Reverse Iteration on GCD" strategy which is optimal for the given constraints ($N, A_i \le 1.2 \times 10^6$).
1.  **Input Parsing**: Efficiently reads $N, K$ and the sequence $A$.
2.  **Preprocessing**:
    -   `cnt[x]` stores the frequency of each number $x$.
    -   `pos[x]` stores the list of indices where $A[i] = x$. This handles duplicate values correctly.
3.  **Multiples Count**:
    -   `total_multiples[g]` is computed in $O(M \log M)$ where $M = \max(A)$. It counts how many numbers in $A$ are divisible by $g$.
4.  **Greedy Assignment**:
    -   Iterates $g$ from $M$ down to 1.
    -   If `total_multiples[g] >= K`, it means there exists a subset of size $K$ with GCD $g$.
    -   For every multiple $v$ of $g$ present in $A$, we update the answer for all indices $i$ where $A[i] = v$.
    -   Since we iterate $g$ downwards, the first time we update `ans[i]`, it is the maximum possible GCD for that element. We use `ans[i] == 1` as a flag to ensure each index is updated exactly once.
5.  **Complexity**:
    -   Time: $O(M \log M + N)$. The nested loops for computing multiples and updating answers run in harmonic series time, and each index is updated at most once.
    -   Space: $O(M + N)$ for arrays and lists.

The logic correctly handles the constraint that the chosen subset must include $A_i$ because we only update `ans[i]` when considering a GCD $g$ that divides $A_i$ (since $A_i$ is a multiple of $g$).

## worker: Run the code with Sample Input 1 to verify output 
The code implements the "Reverse Iteration on GCD" strategy.
1.  **Input Parsing**: Reads $N, K$ and the sequence $A$.
2.  **Preprocessing**:
    -   `cnt[x]` stores the frequency of each number $x$.
    -   `pos[x]` stores the list of indices where $A[i] = x$. This handles duplicate values correctly.
3.  **Multiples Count**:
    -   `total_multiples[g]` is computed in $O(M \log M)$ where $M = \max(A)$. It counts how many numbers in $A$ are divisible by $g$.
4.  **Greedy Assignment**:
    -   Iterates $g$ from $M$ down to 1.
    -   If `total_multiples[g] >= K`, it means there exists a subset of size $K$ with GCD $g$.
    -   For every multiple $v$ of $g$ present in $A$, we update the answer for all indices $i$ where $A[i] = v$.
    -   Since we iterate $g$ downwards, the first time we update `ans[i]`, it is the maximum possible GCD for that element. We use `ans[i] == 1` as a flag to ensure each index is updated exactly once.
5.  **Complexity**:
    -   Time: $O(M \log M + N)$. The nested loops for computing multiples and updating answers run in harmonic series time, and each index is updated at most once.
    -   Space: $O(M + N)$ for arrays and lists.

This approach correctly handles the constraint that the chosen subset must include $A_i$ because we only update `ans[i]` when considering a GCD $g$ that divides $A_i$ (since $A_i$ is a multiple of $g$).

## worker: finalize
The solution implements the "Reverse Iteration on GCD" strategy, which is optimal for the given constraints ($N, A_i \le 1.2 \times 10^6$).

1.  **Input Parsing**: Efficiently reads $N, K$ and the sequence $A$ using `sys.stdin.read().split()`.
2.  **Preprocessing**:
    -   `cnt[x]` stores the frequency of each number $x$.
    -   `pos[x]` stores the list of indices where $A[i] = x$. This handles duplicate values correctly.
3.  **Multiples Count**:
    -   `total_multiples[g]` is computed in $O(M \log M)$ where $M = \max(A)$. It counts how many numbers in $A$ are divisible by $g$ by summing `cnt` at multiples of $g$.
4.  **Greedy Assignment**:
    -   Iterates $g$ from $M$ down to 1.
    -   If `total_multiples[g] >= K`, it means there exists a subset of size $K$ with GCD $g$.
    -   For every multiple $v$ of $g$ present in $A$, we update the answer for all indices $i$ where $A[i] = v$.
    -   Since we iterate $g$ downwards, the first time we update `ans[i]`, it is the maximum possible GCD for that element. We use `ans[i] == 1` as a flag to ensure each index is updated exactly once.
5.  **Complexity**:
    -   Time: $O(M \log M + N)$. The nested loops for computing multiples and updating answers run in harmonic series time, and each index is updated at most once.
    -   Space: $O(M + N)$ for arrays and lists.

This approach correctly handles the constraint that the chosen subset must include $A_i$ because we only update `ans[i]` when considering a GCD $g$ that divides $A_i$ (since $A_i$ is a multiple of $g$).

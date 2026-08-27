
## ideation
The core difficulty is efficiently determining, for each element $A_i$, the largest GCD $g$ such that $A_i$ is divisible by $g$ and there are at least $K$ elements in the entire array $A$ divisible by $g$.

A naive approach for each $A_i$ would be to find all divisors and check counts, but with $N, A_i \le 10^6$, we need an efficient precomputation.

The plan provided is sound:
1.  **Frequency Count**: Count occurrences of each number in $A$.
2.  **Multiples Count (Sieve-like)**: For each $g$ from 1 to $M$ (max value in $A$), compute `cnt[g]` = number of elements in $A$ divisible by $g$. This is done by iterating $g$ and then its multiples $j = g, 2g, \dots$, summing `freq[j]`. Complexity: $O(M \log M)$.
3.  **Valid GCDs**: Identify which $g$ have `cnt[g] >= K`. Let's call these "valid" GCDs.
4.  **Answer for each $A_i$**: For each $A_i$, we need the largest divisor $d$ of $A_i$ such that `cnt[d] >= K`.

Optimization for Step 4:
Instead of finding divisors for each $A_i$ individually, we can precompute an array `best[g]` which stores the largest valid GCD that divides $g$.
- Initialize `best[g] = 0` for all $g$.
- Iterate $g$ from $M$ down to 1. If `cnt[g] >= K`, then `best[g] = g`.
- However, `best[g]` should also consider divisors of $g$. Actually, a better way is:
    - Create an array `ans_for_val` of size $M+1$.
    - For each $g$ where `cnt[g] >= K`, we know $g$ is a candidate answer for any multiple of $g$.
    - We want for each number $x$, the largest $g$ such that $g|x$ and `cnt[g] >= K`.
    - We can propagate the information: `best[x]` = max(`best[x]`, `best[d]`) for all divisors? No, that's slow.
    - Alternative: Iterate $g$ from $M$ down to 1. If `cnt[g] >= K`, then for all multiples $j = g, 2g, \dots$, we can potentially update `ans_for_val[j]` with $g$. Since we iterate $g$ downwards, the first time we visit a multiple $j$ with a valid $g$, it is the largest such $g$? No, because a larger divisor might not be valid, but a smaller one is. Wait.
    - Let's refine: We want $g^* = \max \{ g : g | A_i \text{ and } cnt[g] \ge K \}$.
    - We can compute an array `max_valid_divisor[x]` for all $x \in [1, M]$.
    - Initialize `max_valid_divisor[x] = 0`.
    - For $g$ from $M$ down to 1:
        - If `cnt[g] >= K`:
            - For all multiples $j = g, 2g, \dots, \le M$:
                - `max_valid_divisor[j] = g` (since we go from large $g$ to small, the first assignment is the largest valid divisor? No. If $g=6$ is valid, it sets `max_valid_divisor[6]=6`, `max_valid_divisor[12]=6`. Later if $g=4$ is valid, it sets `max_valid_divisor[12]=4`. But 6 > 4, so we want 6. So we should only set if not already set? Or set if current $g$ is larger? Since we iterate $g$ downwards, the first time we touch a multiple $j$, it is via the largest valid divisor of $j$?
                - Example: $j=12$. Divisors: 12, 6, 4, 3, 2, 1.
                - If 12 is valid, `cnt[12]>=K`. We set `max_valid_divisor[12]=12`.
                - If 12 is not valid, but 6 is, we set `max_valid_divisor[12]=6`.
                - If 12, 6 not valid, but 4 is, we set `max_valid_divisor[12]=4`.
                - So yes, if we iterate $g$ from $M$ down to 1, and for each valid $g$, we iterate its multiples $j$, we can set `max_valid_divisor[j] = g` if it hasn't been set yet.
                - To avoid re-checking, we can just set it. Since we go from large $g$ to small, the first $g$ that is valid and divides $j$ is the largest valid divisor.
                - So: Initialize `max_valid_divisor` with 0.
                - For $g = M$ down to 1:
                    - If `cnt[g] >= K`:
                        - For $j = g, 2g, \dots \le M$:
                            - If `max_valid_divisor[j] == 0`:
                                - `max_valid_divisor[j] = g`
    - This approach has complexity $O(M \log M)$ because the inner loop runs $M/g$ times, and we only do work if `cnt[g] >= K`? No, we must check `cnt[g] >= K` first. But even if we iterate all $g$, the total iterations of the inner loop is $\sum_{g=1}^M \frac{M}{g} = O(M \log M)$.
    - Then for each $A_i$, the answer is `max_valid_divisor[A_i]`.

This is efficient enough for $M=10^6$.

Pitfalls:
- Memory: Arrays of size $10^6$ are fine.
- Time: $O(M \log M + N)$ is acceptable.
- Edge case: $K=1$. Then every element is a valid GCD for itself. The largest divisor of $A_i$ with count $\ge 1$ is $A_i$ itself (since $A_i$ is in the array). So answer is $A_i$. The algorithm should handle this naturally.
- The condition "include $A_i$" is handled because we only care about divisors of $A_i$. If $g$ divides $A_i$ and there are $K$ multiples of $g$ in $A$, then $A_i$ is one of them, so we can choose $A_i$ and $K-1$ other multiples.

## worker: none
The solution follows the plan:
1.  **Frequency Count**: We count occurrences of each number in $A$ using an array `freq` of size $M+1$ where $M = \max(A)$.
2.  **Multiples Count**: We compute `cnt[g]` for each $g \in [1, M]$ by iterating through multiples of $g$ and summing their frequencies. This takes $O(M \log M)$ time.
3.  **Best Valid Divisor**: We compute an array `best` where `best[x]` is the largest divisor $d$ of $x$ such that `cnt[d] >= K`. We do this by iterating $g$ from $M$ down to 1. If `cnt[g] >= K`, we iterate through all multiples $j$ of $g$ and set `best[j] = g` if it hasn't been set yet. Since we process $g$ in descending order, the first valid $g$ that divides $j$ is the largest such valid divisor. This also takes $O(M \log M)$ time.
4.  **Answer Extraction**: For each element $A_i$, the answer is simply `best[A_i]`. This is $O(N)$ time.

Total time complexity is $O(M \log M + N)$, which fits within the constraints ($M, N \le 1.2 \times 10^6$). Space complexity is $O(M)$ for the arrays.


## ideation
The core difficulty lies in efficiently generating all "400 numbers" up to $10^{12}$ and then answering $2 \times 10^5$ queries quickly.

1.  **Mathematical Structure**: A 400 number $N$ has exactly 2 distinct prime factors $p, q$ and each divides $N$ an even number of times. This implies $N = p^{2a} q^{2b}$ with $a,b \ge 1$. Thus, $N = (p^a q^b)^2 = k^2$, where $k = p^a q^b$ has exactly two distinct prime factors.
2.  **Range of $k$**: Since $N \le 10^{12}$, we have $k = \sqrt{N} \le 10^6$.
3.  **Precomputation Strategy**:
    *   We need to find all integers $k \in [1, 10^6]$ such that $k$ has exactly two distinct prime factors.
    *   We can use a sieve-like method to count distinct prime factors for all numbers up to $10^6$.
    *   Let `cnt[i]` be the number of distinct prime factors of `i`.
    *   Iterate $i$ from 2 to $10^6$. If `cnt[i] == 2`, then $i^2$ is a 400 number.
    *   Collect all such $i^2$ values into a sorted list.
4.  **Query Processing**:
    *   For each query $A$, use binary search (`bisect_right`) on the sorted list of 400 numbers to find the largest value $\le A$.
5.  **Pitfalls**:
    *   The sieve must correctly count *distinct* prime factors. A standard sieve that marks multiples can be adapted: for each prime $p$, increment the count for all its multiples.
    *   The maximum value of $A$ is $10^{12}$, so $k$ goes up to $10^6$. This is small enough for precomputation.
    *   The number of such $k$ values is manageable. The number of integers up to $X$ with exactly 2 distinct prime factors is roughly $O(X \log \log X / \log X)$, which for $X=10^6$ is well within memory limits (a few hundred thousand entries).

## worker: Implement a sieve to count distinct prime factors 
The solution uses a sieve-like method to count distinct prime factors for all integers up to $10^6$. For each prime $p$, we iterate through all its multiples and increment their count. This runs in $O(N \log \log N)$ time where $N = 10^6$, which is very efficient.

After counting, we collect all $k$ with exactly 2 distinct prime factors, square them to get the 400 numbers, and sort them. For each query, we use binary search to find the largest 400 number $\le A$.

The constraints guarantee $A \ge 36$, and 36 ($6^2 = 2^2 \cdot 3^2$) is a valid 400 number, so there's always a valid answer.

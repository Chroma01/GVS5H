1. A "400 number" is of the form $p^{2a} \cdot q^{2b}$ where $p$ and $q$ are distinct primes and $a, b \ge 1$. This means the number is a perfect square, say $k^2$, where $k = p^a \cdot q^b$ has exactly two distinct prime factors.
2. We need to find the largest such number $\le A$ for each query. Since $A \le 10^{12}$, the square root $k$ is at most $10^6$.
3. We can precompute all integers $k \in [1, 10^6]$ that have exactly two distinct prime factors. Let's call these "valid bases".
4. For each valid base $k$, the corresponding 400 number is $k^2$. We collect all such $k^2$ values, sort them, and store them in a list.
5. For each query $A$, we use binary search (bisect_right) on the sorted list of 400 numbers to find the largest value $\le A$.
1. A "400 number" is of the form $p^{2a} \cdot q^{2b}$ where $p$ and $q$ are distinct primes and $a, b \geq 1$. This means $N = (p^a \cdot q^b)^2$ is a perfect square, and its square root $S = p^a \cdot q^b$ has exactly two distinct prime factors.
2. We can precompute all such numbers up to $10^{12}$. Since $N \le 10^{12}$, we have $S \le 10^6$.
3. Generate all integers $S \le 10^6$ that have exactly two distinct prime factors. For each such $S$, compute $N = S^2$. If $N \le 10^{12}$, add it to a list.
4. To generate $S$ with exactly two distinct prime factors: iterate over all pairs of distinct primes $(p, q)$ and exponents $a, b \ge 1$ such that $p^a q^b \le 10^6$.
5. Store all valid $N$ values in a sorted list. For each query $A$, use binary search to find the largest $N \le A$.
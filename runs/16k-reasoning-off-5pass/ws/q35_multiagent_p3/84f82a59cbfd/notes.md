
## ideation
The problem asks for the largest "400 number" $\le A$ for multiple queries. A 400 number is defined as having exactly 2 distinct prime factors, each with an even exponent. This implies a 400 number is a perfect square $N = S^2$, where $S$ has exactly two distinct prime factors. Since $N \le 10^{12}$, we have $S \le 10^6$.

The core difficulty is efficiently generating all such numbers $N \le 10^{12}$ and answering queries.
1.  **Generation**: We need to find all integers $S \le 10^6$ that have exactly two distinct prime factors. Let $S = p^a q^b$ with $p < q$ primes and $a, b \ge 1$.
2.  **Algorithm**:
    *   Sieve primes up to $10^6$.
    *   For each pair of distinct primes $(p, q)$, generate numbers of the form $p^a q^b \le 10^6$.
    *   To avoid duplicates and ensure efficiency, we can iterate $p$ from smallest prime upwards. For each $p$, iterate powers $p^a$. Then iterate $q > p$ and powers $q^b$. The product $p^a q^b$ must be $\le 10^6$.
    *   Collect all such $S$, square them to get $N$, and store unique $N$ values in a sorted list.
3.  **Query**: For each query $A$, use binary search (`bisect_right`) on the sorted list of 400 numbers to find the largest one $\le A$.

Pitfalls:
*   Generating pairs naively might be slow if not careful. The number of such $S$ is relatively small. The number of primes up to $10^6$ is 78,498. However, most pairs won't yield products $\le 10^6$ with exponents $\ge 1$. Specifically, if $p \ge 1000$, then $p^2 q^2 > 10^{12}$ is not the constraint, but $p^1 q^1 \le 10^6$. If $p > 1000$, $q$ must be small? No, $p < q$. If $p > 1000$, then $p^2 > 10^6$, so $a$ must be 1. Then $p \cdot q \le 10^6 \implies q \le 10^6/p$. The number of such pairs is manageable.
*   We must ensure we don't count numbers with more than 2 distinct prime factors. The generation method $p^a q^b$ strictly ensures exactly two distinct prime factors.
*   The constraint $A \ge 36$ ensures the answer always exists (since $36 = 2^2 \cdot 3^2$ is the smallest).

## worker: (None)
The problem requires finding the largest "400 number" $\le A$ for multiple queries. A 400 number is defined as having exactly 2 distinct prime factors, each with an even exponent. This structure implies that any 400 number $N$ can be written as $N = p^{2a} q^{2b} = (p^a q^b)^2 = S^2$, where $S = p^a q^b$ has exactly two distinct prime factors $p$ and $q$.

Given $N \le 10^{12}$, we have $S \le 10^6$. The strategy is:
1.  **Sieve**: Generate all primes up to $10^6$ using a sieve.
2.  **Generate S**: Iterate through all pairs of distinct primes $(p, q)$ with $p < q$ and exponents $a, b \ge 1$ such that $p^a q^b \le 10^6$. This is done efficiently by iterating $p$, then powers $p^a$, and for each, iterating $q > p$ and powers $q^b$ such that the product stays within bounds.
3.  **Compute N**: For each valid $S$, compute $N = S^2$.
4.  **Store and Sort**: Store all unique $N$ values in a sorted list.
5.  **Query**: For each query $A$, use binary search (`bisect_right`) to find the largest $N \le A$.

The number of such $S$ values is relatively small (a few hundred thousand at most), making precomputation and binary search very efficient. The time complexity for precomputation is dominated by the nested loops over primes and their powers, which is well within limits for $10^6$. Each query is answered in $O(\log (\text{number of 400 numbers}))$.

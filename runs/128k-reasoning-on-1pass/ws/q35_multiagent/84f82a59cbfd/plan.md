1. Analyze the definition of a 400 number to deduce that any such number $N$ must be a perfect square $M^2$, where $M$ has exactly two distinct prime factors.
2. Reduce the problem to finding the largest $M \le \lfloor \sqrt{A} \rfloor$ with exactly two distinct prime factors for each query.
3. Precompute the count of distinct prime factors for all integers up to $10^6$ using a sieve-like method, since $\sqrt{10^{12}} = 10^6$.
4. Build a lookup array `largest_valid` where `largest_valid[i]` stores the largest valid $M \le i$.
5. Process each query in $O(1)$ time by computing the integer square root of $A$, looking up the precomputed value, and squaring it to get the answer.

## ideation
The problem defines a "400 number" $N$ as having exactly 2 distinct prime factors, each with an even exponent. This structure implies $N = p_1^{2a} p_2^{2b} = (p_1^a p_2^b)^2 = M^2$, where $M = p_1^a p_2^b$. The integer $M$ must have exactly 2 distinct prime factors ($p_1$ and $p_2$).
Thus, the problem reduces to finding the largest integer $M$ such that $M^2 \le A$ and $M$ has exactly 2 distinct prime factors.
Let $S = \lfloor \sqrt{A} \rfloor$. We need to find the largest $M \le S$ with exactly 2 distinct prime factors.
Given $A \le 10^{12}$, $S$ can be up to $10^6$. We can precompute the number of distinct prime factors for all numbers up to $10^6$ using a sieve. Then, we can build a lookup table `last_valid` where `last_valid[x]` stores the largest valid $M \le x$.
For each query, we compute $S$, retrieve `last_valid[S]`, and output its square.
The constraints $Q \le 2 \times 10^5$ and $A \le 10^{12}$ require an efficient solution, which this approach provides with $O(N \log \log N + Q)$ complexity.

## worker: finalize
1. **Problem Reduction**: A "400 number" $N$ has exactly 2 distinct prime factors, each with an even exponent. This implies $N = p_1^{2a} p_2^{2b} = (p_1^a p_2^b)^2 = M^2$, where $M = p_1^a p_2^b$ has exactly 2 distinct prime factors. Thus, finding the largest 400 number $\le A$ is equivalent to finding the largest $M$ such that $M^2 \le A$ and $M$ has exactly 2 distinct prime factors.
2. **Precomputation**: Since $A \le 10^{12}$, $M$ can be at most $10^6$. We precompute the number of distinct prime factors for all integers up to $10^6$ using a sieve-like method in $O(N \log \log N)$ time.
3. **Lookup Table**: We build a prefix array `last_valid` where `last_valid[i]` stores the largest valid $M \le i$. This allows $O(1)$ query processing.
4. **Query Processing**: For each query $A$, we compute $S = \lfloor \sqrt{A} \rfloor$, retrieve $M = \text{last\_valid}[S]$, and output $M^2$. The constraints guarantee $A \ge 36$, so $S \ge 6$, ensuring a valid $M$ always exists.
5. **Complexity**: Precomputation takes $O(N \log \log N + N)$ time and $O(N)$ space. Each query is answered in $O(1)$ time. Total time complexity is $O(N \log \log N + Q)$, which easily fits within the limits for $N=10^6$ and $Q=2 \times 10^5$.

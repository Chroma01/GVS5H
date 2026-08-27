
## ideation
The problem asks for the largest integer $N \le A$ such that $N$ has exactly two distinct prime factors, each with an even exponent. This implies $N = p^{2a} q^{2b} = (p^a q^b)^2$. Let $M = p^a q^b$. Then $N = M^2$, and $M$ must have exactly two distinct prime factors (since $a,b \ge 1$). The condition $N \le A$ becomes $M^2 \le A \implies M \le \sqrt{A}$.

Since $A \le 10^{12}$, $\sqrt{A} \le 10^6$. We need to find the largest $M \le \lfloor\sqrt{A}\rfloor$ such that $M$ has exactly two distinct prime factors.

Algorithm:
1. Precompute the number of distinct prime factors for all integers up to $10^6$ using a sieve.
2. Collect all numbers $M \in [1, 10^6]$ that have exactly two distinct prime factors into a sorted list.
3. For each query $A$:
   - Compute $L = \lfloor\sqrt{A}\rfloor$.
   - Use binary search (bisect_right) on the precomputed list to find the largest $M \le L$.
   - The answer is $M^2$.

Pitfalls:
- Ensure the sieve correctly counts distinct prime factors.
- Handle the case where no such $M$ exists? The problem guarantees a 400 number $\le A$ exists, and the smallest is $36 = 2^2 \cdot 3^2$ ($M=6$). Since $A \ge 36$, $L \ge 6$, so there will always be at least one valid $M$ (e.g., 6).
- Precision of square root: use integer square root to avoid floating point errors.

## worker: none
The key insight is that a "400 number" N must be a perfect square of some integer M, where M has exactly two distinct prime factors. This is because N = p^(2a) * q^(2b) = (p^a * q^b)^2, and M = p^a * q^b has exactly two distinct prime factors p and q.

Since A ≤ 10^12, we have M ≤ √A ≤ 10^6. We precompute all integers up to 10^6 that have exactly two distinct prime factors using a sieve. For each query, we compute the integer square root of A and use binary search to find the largest valid M ≤ √A. The answer is M².

The sieve runs in O(MAX_M log log MAX_M) time, and each query is answered in O(log(MAX_M)) time using binary search. With Q up to 2×10^5 and MAX_M = 10^6, this approach is efficient.

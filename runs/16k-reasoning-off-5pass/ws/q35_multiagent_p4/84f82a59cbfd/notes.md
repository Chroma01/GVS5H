
## ideation
- A "400 number" N has exactly two distinct prime factors, each with an even exponent. This means $N = p^{2a} q^{2b} = (p^a q^b)^2$.
- Let $M = p^a q^b$. Then $N = M^2$, and $M$ must have exactly two distinct prime factors.
- For a query $A$, we need the largest $N \leq A$ that is a 400 number. Since $N = M^2$, this is equivalent to finding the largest $M$ such that $M^2 \leq A$ (i.e., $M \leq \lfloor\sqrt{A}\rfloor$) and $M$ has exactly two distinct prime factors.
- The maximum value of $A$ is $10^{12}$, so the maximum value of $M$ is $10^6$.
- We can precompute for all numbers up to $10^6$ whether they have exactly two distinct prime factors using a sieve.
- Store all valid $M$ values in a sorted list. For each query, compute $\lfloor\sqrt{A}\rfloor$ and use binary search to find the largest valid $M \leq \lfloor\sqrt{A}\rfloor$.
- Pitfalls: 
  - Ensure the sieve correctly counts distinct prime factors.
  - Handle edge cases where no such $M$ exists (but the problem guarantees a 400 number exists, so the smallest is $36 = 2^2 \cdot 3^2$, corresponding to $M=6$).
  - Use integer square root carefully to avoid floating point errors.

## worker: none
The key insight is that a "400 number" N must be of the form $p^{2a} q^{2b} = (p^a q^b)^2 = M^2$ where M has exactly two distinct prime factors. For each query A, we need the largest such N ≤ A, which means finding the largest M ≤ ⌊√A⌋ with exactly two distinct prime factors, then outputting M².

We precompute using a sieve up to 10⁶ (since √(10¹²) = 10⁶) the count of distinct prime factors for each number. We collect all numbers with exactly 2 distinct prime factors into a sorted list. For each query, we compute ⌊√A⌋ using integer square root, then use binary search (bisect_right) to find the largest valid M ≤ ⌊√A⌋. The answer is M².

Time complexity: O(MAX_M log log MAX_M) for sieving + O(Q log(MAX_M)) for queries, which is well within limits.

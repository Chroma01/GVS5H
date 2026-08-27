A 400 number has the form N = p^(2a) * q^(2b) where p<q are distinct primes. So N must be a perfect square times a perfect square of another prime. Equivalently, N = (p^a * q^b)^2 * 1 (since exponents are even). Wait, p^(2a) = (p^a)^2, so N = (p^a q^b)^2, i.e., a perfect square whose square root has exactly two distinct prime factors. So we need the largest perfect square ≤ A whose square root is a "squarefree 2-prime number" (i.e., product of exactly two distinct primes).

For each A, find max X ≤ A such that X is a perfect square and sqrt(X) = r is product of exactly two distinct primes. So we need max r^2 ≤ A with r = p*q, p<q distinct primes. Equivalent to max r ≤ floor(sqrt(A)) with r having exactly two distinct prime factors.

For each query, compute S = floor(sqrt(A)). Then we need the largest number ≤ S that is a product of exactly two distinct primes. This is a classic "largest number ≤ N with exactly 2 prime factors" problem.

Approach: Precompute primes up to 10^6 (since sqrt(10^12) = 10^6). For each query, for S = floor(sqrt(A)), we iterate r from S downwards until we find one with exactly 2 distinct prime factors. To make this fast for Q up to 2*10^5, we need a smarter approach.

We can precompute an array f[n] = number of distinct prime factors of n for n up to 10^6. Then for each query, start from S and decrement until f[r] == 2. In the worst case this is slow if many queries start from large values. But note: the density of numbers with exactly 2 prime factors is high. We can use a "jump" approach.

Better: Precompute an array g[n] = largest number ≤ n that has exactly 2 distinct prime factors. We can fill g by iterating from 1 to 10^6: if f[i] == 2, then g[i] = i; else g[i] = g[i-1]. This is O(10^6) preprocessing. Then for each query, compute S = floor(sqrt(A)), answer = g[S]^2.

But careful: we need the largest r ≤ S with exactly 2 distinct prime factors. g[S] gives exactly that. So answer = g[S]^2.

We need to compute f[n] = number of distinct prime factors. We can compute using a sieve: for each prime p, for multiples of p, increment count. Since 10^6 is small, O(N log log N) is fine.

Edge case: g[1] = 0 (or some sentinel). We need to ensure that for the given constraints, such r exists. Problem guarantees a 400 number ≤ A exists, so g[S] >= 6 (2*3) at least.

Complexities: Precomputation O(10^6 log log 10^6) ~ 0.1s. Queries: O(Q) with sqrt per query (O(1) actually). Total fine.

Let's verify with sample:
- A=404, S=20, g[20]: numbers ≤20 with 2 distinct prime factors: 6,10,14,15... largest is 20? 20=2^2*5, distinct primes 2,5 -> yes. So r=20, answer=400. Correct.
- A=36, S=6, g[6]=6, answer=36. Correct.
- A=60, S=7, g[7]=6, answer=36. Correct.
- A=10^12, S=10^6, g[10^6] is the largest ≤10^6 with 2 prime factors. Likely 999983*999979? Actually 10^6=2^6*5^6, but we need exactly 2 distinct primes. The largest such number ≤10^6 would be a product of two large primes, e.g., near 10^6. Then square of that is near 10^12. Sample output 10^12, so r=10^6 exactly. Is 10^6 = 2^6 * 5^6, has 2 distinct prime factors. So answer = (10^6)^2 = 10^12. Correct.
- A=123456789, S=floor(sqrt(123456789)) = 11111.111... = 11111. Need largest ≤11111 with 2 distinct prime factors. Let's find: 11111 = 41*271? 41*271 = 11111, yes, both prime. So r=11111, answer=123454321. Sample output matches.

So the solution is clear.
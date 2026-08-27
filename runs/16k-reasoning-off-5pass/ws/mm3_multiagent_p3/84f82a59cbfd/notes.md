
## ideation
The problem asks for the largest "400 number" ≤ A for each query. A 400 number must have exactly two distinct prime factors, and each must appear with even exponent. This means N = p^{2a} * q^{2b} = (p^a * q^b)^2, i.e., a perfect square whose root is the product of exactly two distinct primes.

For each A, we need max r ≤ √A such that r has exactly two distinct prime factors; answer is r².

Sqrt(10^12) = 10^6, so we can precompute up to 10^6. Use a sieve to compute f[n] = number of distinct prime factors. Then build prefix array g[n] = largest number ≤ n with f[n] == 2 (carry forward previous g when f[n] != 2). For each query, compute S = floor(sqrt(A)), answer = g[S]².

Edge cases: g[1] = 0; problem guarantees existence so g[S] ≥ 6 (2*3).

Complexities: Precomputation O(N log log N) with N=10^6; per query O(1). Total fine for Q=2e5.

Pitfalls: Use integer sqrt safely (avoid floating errors; use math.isqrt in Python). Ensure f[n] counts distinct primes (not multiplicity). Make sure g is correctly initialized.

## worker: Implement the solution: sieve up to 10^6 to count 
The solution precomputes, for all integers up to 10^6, the count of distinct prime factors using a sieve. It then builds a prefix array `best` where `best[i]` stores the largest number ≤ i with exactly two distinct prime factors. For each query, we take the integer square root of A, look up the largest such r, and output r².

The sieve approach: first generate all primes up to 10^6 with the standard Sieve of Eratosthenes, then for each prime p, increment the counter for all its multiples. This correctly counts distinct prime factors (not multiplicities).

The build of `best` is linear and O(N). Queries are O(1) each. The total complexity is well within limits for Q up to 2×10^5 and A up to 10^12.

The sample test produces:
- 404 → 20² = 400
- 36 → 6² = 36
- 60 → 6² = 36
- 10¹² → (10⁶)² = 10¹²
- 123456789 → 11111² = 123454321


## ideation
The key insight: N is a 400 number iff N = p^a * q^b with distinct primes p, q and even positive exponents a, b. This means N = M^2 where M = p^i * q^j (i, j >= 1), i.e., M has exactly 2 distinct prime factors (M is a semiprime counting multiplicity with exactly 2 distinct primes — includes p*q and p^2 * ... wait, M = p^i q^j with i,j>=1, so M has exactly 2 distinct prime factors; exponents can be any positive values).

Since N <= 1e12, M <= 1e6. So sieve up to 1e6, find all M with exactly 2 distinct prime factors, square them, sort, and binary search per query.

Pitfalls:
- M must have exactly 2 distinct prime factors (omega(M) == 2), regardless of exponents.
- Count of such M up to 1e6: numbers with exactly 2 distinct prime factors — roughly manageable (a few hundred thousand). Squaring gives values up to 1e12, fits in Python int.
- Edge: A >= 36 always, and 36 = 6^2 = (2*3)^2 is the smallest 400 number, so answer always exists.
- Fast I/O needed for Q up to 2e5.

Sieve approach: compute smallest prime factor (SPF) array up to 1e6, then count distinct prime factors for each M by factorization via SPF, or directly sieve by adding 1 to a counter for each prime multiple. The latter: distinct prime factor count via for p in primes: for multiple m: cnt[m] += 1. That's O(n log log n), fine.

## worker: Write the complete Python solution: sieve distinct
- A 400 number N has exactly 2 distinct prime factors p, q, each with even exponent, so N = (p^i * q^j)^2 = M^2 where M has exactly 2 distinct prime factors (omega(M) == 2), M >= 2*3 = 6.
- Since N <= 1e12, M <= 1e6. Sieve computes omega(m) for all m up to 1e6 in O(n log log n) by iterating over primes and incrementing counters on multiples.
- Collect m^2 for all m with omega(m) == 2, sort (they're generated in increasing m order, so already sorted, but sort is harmless), and answer each query via bisect_right.
- Smallest 400 number is 36 = 6^2, and constraints guarantee A >= 36, so bisect_right always finds a valid index >= 0.
- Fast I/O via sys.stdin.buffer.read handles Q up to 2e5 easily. Sample check: A=404 -> 400; A=36 -> 36; A=60 -> 36; A=1e12 -> 1e12 (since 1e12 = (2^2*5^2... wait, 1e6 = 2^6*5^6, omega=2, so (1e6)^2 = 1e12 qualifies); A=123456789 -> 123454321 = 11111^2 (11111 = 41*271, two distinct primes). All match.

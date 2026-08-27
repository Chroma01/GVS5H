
## ideation
Core insight: condition 2 forces every prime exponent in N to be even, so N must be a perfect square. If N = m^2, then N has exactly 2 distinct prime factors iff m has exactly 2 distinct prime factors. Since A ≤ 1e12, m ≤ 1e6, so the problem reduces to: precompute all m ≤ 1e6 with exactly two distinct prime factors, square them, sort, and answer each query by binary search.

Main difficulty is doing this fast for 2e5 queries without factoring each query or each candidate up to A. A sieve up to 1e6 is enough. Need be careful that “exactly 2 distinct prime factors” applies to the root m, not to counting exponents in N. Also note N values are squares and automatically unique for distinct m.

Edge/pitfalls: smallest valid N is 36 = 6^2; constraints guarantee existence, but code should still handle bisect edge cleanly. Use integer arithmetic; in C++ watch 64-bit overflow when squaring near 1e6 is fine, but comparisons up to 1e12 need long long. Do not generate semiprime N directly up to 1e12. Avoid O(number of candidates per query); use global sorted list + bisect.

## worker: Write the complete program: sieve smallest prime f
- A 400 number N has all prime exponents even, so N = m²; N has exactly 2 distinct prime factors iff m does. Since A ≤ 10¹², m ≤ 10⁶.
- Sieve: for each prime p (detected by omega[p] == 0), increment omega for all multiples — O(n log log n), about 8M operations for n = 10⁶, fast in Python (~1s).
- Candidates are generated in increasing order of m, so the list of squares is already sorted — no extra sort needed.
- Each query answered with `bisect_right(candidates, A) - 1`; constraints guarantee index ≥ 0 (smallest candidate is 36 = 6² and A ≥ 36).
- Verified against samples mentally: 404 → 400, 36 → 36, 60 → 36, 10¹² → 10¹² (root 10⁶ = 2⁶·5⁶ has ω=2), 123456789 → 123454321 = 11111² (11111 = 41·271, ω=2).

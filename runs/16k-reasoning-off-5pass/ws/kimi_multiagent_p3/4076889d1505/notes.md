
## ideation
The task: given N (1 ≤ N ≤ 10^9), produce A, M in [1, 10^18] such that the multiplicative order of A modulo M is exactly N (smallest n with M | A^n − 1 equals N). T up to 10^4 test cases, so per-case work must be O(1) or near O(1).

Core difficulty: guaranteeing the order is *exactly* N, not a proper divisor of N, while keeping A, M within 10^18.

Key insight (from plan): use the binomial expansion. Let A = N + 1 and M = N². Then
(1+N)^k = Σ C(k,i) N^i ≡ 1 + kN (mod N²),
since all terms with i ≥ 2 contain N². Therefore M | A^k − 1 ⟺ N² | kN ⟺ N | k. The smallest positive such k is exactly N. This works uniformly for all N ≥ 1, including N = 1 (M = 1, and 1 divides everything, so smallest n = 1 ✓).

Bounds check: N ≤ 10^9 ⇒ A = N+1 ≤ 10^9 + 1 ≤ 10^18 ✓, M = N² ≤ 10^18 ✓. Both positive ✓.

Verification against sample logic: N=3 → (4, 9): 4¹−1=3, 4²−1=15, 4³−1=63=7·9 ✓ order 3. N=1 → (2, 1): 2¹−1=1 divisible by 1, smallest n=1 ✓. (Sample outputs differ but any valid pair is accepted.)

Pitfalls to avoid:
- Naive M = A^N − 1 construction overflows 10^18 for N > 60 — not needed here.
- Must confirm M=1 is allowed: constraints say M between 1 and 10^18 inclusive, so yes.
- Python integers handle everything natively; just read T, loop, print "N+1 N*N".
- Fast I/O (sys.stdin) for T up to 10^4 — trivial either way.

## worker: Implement the solver: read all ints from stdin via
Construction: A = N+1, M = N². By the binomial theorem, (1+N)^k = Σ C(k,i)N^i ≡ 1 + kN (mod N²), since all terms with i ≥ 2 contain a factor N². Hence N² | (1+N)^k − 1 ⟺ N² | kN ⟺ N | k, so the smallest positive k is exactly N. Works for all N ≥ 1, including N = 1 (M = 1, which divides everything, so the answer is n = 1). Bounds: A = N+1 ≤ 10^9 + 1 ≤ 10^18, M = N² ≤ 10^18. Verified N=3 → (4,9): 4³−1 = 63 = 7·9, and 4¹−1=3, 4²−1=15 not divisible by 9. O(1) per test case, fast I/O for T up to 10^4.

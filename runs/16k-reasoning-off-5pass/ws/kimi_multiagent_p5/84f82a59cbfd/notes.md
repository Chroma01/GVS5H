
## ideation
The key insight is already in the plan: N = p^(2a) * q^(2b) = (p^a * q^b)^2, so 400 numbers are exactly squares of integers m with exactly two distinct prime factors (ω(m) = 2). Note a, b ≥ 1, so m must have *exactly* two distinct primes (not one, not zero). Since A ≤ 10^12, m = floor(sqrt(A)) ≤ 10^6.

Core difficulty: Q up to 2×10^5 queries, so per-query work must be O(1) or near-O(1). Decrementing m and factoring each time could be slow in the worst case if gaps between valid m are large — need to check gap sizes. Safer: precompute a "previous valid index" array.

Approach:
1. Sieve SPF (smallest prime factor) up to 10^6 — O(n log log n).
2. Compute distinct-prime-factor count for each m via DP: omega[m] = omega[m // spf[m]] + (1 if spf[m] != spf[m // spf[m]] else 0). Or factor each m with SPF. DP is cleaner and O(n).
3. Build prev[m] = largest index ≤ m with omega == 2 (prev[m] = m if valid else prev[m-1]).
4. Per query: m = isqrt(A); answer = prev[m]^2. Use math.isqrt for exact integer square root.

Pitfalls:
- Must use integer isqrt, not int(sqrt(...)) with floats, since A up to 10^12 is fine in double but borderline values could round wrong; isqrt is exact and safe.
- omega must count *distinct* primes: e.g., m = 12 = 2^2·3 has omega 2 → valid; m = 8 has omega 1 → invalid; m = 30 has omega 3 → invalid.
- Edge: smallest valid m is 6 (2·3), 6^2 = 36, matching constraint A ≥ 36 and sample.
- Verify sample: A=404 → isqrt=20, prev[20]: valid m ≤ 20 with omega 2: 6,10,12,14,15,18,20 → 20 → 400 ✓. A=10^12 → m=10^6 = 2^6·5^6, omega 2 → answer 10^12 ✓. A=123456789 → isqrt=11111, prev → 11111? 11111 = 41·271, omega 2 → 11111^2 = 123454321 ✓.
- prev[0..5] would be 0/undefined, but A ≥ 36 guarantees m ≥ 6, so no issue; still initialize prev safely.

Complexity: sieve O(10^6 log log n), arrays O(10^6), queries O(1) each. Memory fine (~few MB). Python speed: sieve of 10^6 plus two linear passes is fine (~1-2s). Use sys.stdin for fast input.

## worker: Write the complete Python solution: SPF sieve to 1
- A 400 number is p^(2a)·q^(2b) = (p^a·q^b)^2 with a,b ≥ 1, i.e., exactly the squares of integers m with ω(m) = 2 (two distinct prime factors). Since A ≤ 10^12, m = ⌊√A⌋ ≤ 10^6.
- Precomputation:
  - SPF sieve up to 10^6 (classic linear-ish sieve, only marking multiples of primes from i² where not already marked).
  - omega via DP: omega[m] = omega[m/p] + (1 if p ∤ m/p else 0), where p = spf[m]. This correctly counts distinct primes (e.g., omega[8]=1, omega[12]=2, omega[30]=3).
  - prev[m] = largest index ≤ m with omega == 2, built in one pass.
- Each query: m = math.isqrt(A) (exact integer sqrt, no float issues), answer = prev[m]². O(1) per query.
- Verified against samples mentally: A=404 → m=20 (20=2²·5, ω=2) → 400 ✓; A=36 → m=6 → 36 ✓; A=60 → m=7, prev=6 → 36 ✓; A=10^12 → m=10^6=2^6·5^6, ω=2 → 10^12 ✓; A=123456789 → m=11111=41·271, ω=2 → 123454321 ✓.
- A ≥ 36 guarantees m ≥ 6, so prev[m] ≥ 6 > 0 always; no undefined case.
- Complexity: sieve + two linear passes over 10^6 (~1–2 s in Python), then O(Q) with trivial per-query work; memory ~ a few lists of 10^6 ints.

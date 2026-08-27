
## ideation
Core requirement: construct (A, M) with ord_M(A) = N exactly, A,M ≤ 1e18, for up to 1e4 values of N ≤ 1e9.

Key idea: pick prime p = kN + 1 (so N | p−1). Then for a primitive root g mod p, A = g^((p−1)/N) mod p has order exactly N. Constraints: p ≤ 1e18 requires kN+1 ≤ 1e18, trivially satisfied for small k. Existence of small k: by Linnik-type bounds / heuristics, a prime in the arithmetic progression 1 mod N appears quickly; empirically k stays within a few thousand for N ≤ 1e9 (worst case needs verification — could use fallback: allow composite M via prime power construction, e.g., M = p^e where ord lifts correctly, or use two primes). Alternative fallback: M = Φ_N(a) has all prime divisors ≡ 1 mod N (except possibly divisors of N), so ord_M(a) = N if M is squarefree-ish — riskier.

Sub-problems:
1. Primality testing for numbers up to ~1e12 (kN+1 with small k): deterministic Miller-Rabin with a few bases is fine and fast.
2. Factoring p−1 = kN: factor N once per test (trial division with primes up to 31623; N ≤ 1e9 so at most one large prime factor remains). k is small, factor by trial division. Union gives full factorization of p−1.
3. Primitive root: test g = 2,3,5,... checking g^((p−1)/q) ≠ 1 mod p for each distinct prime q | p−1. Usually found within a few tries.
4. N = 1: output (anything, 1), e.g., A=2, M=1. Note M=1 means every A^1−1 ≡ 0 mod 1, smallest n = 1. Good.

Pitfalls:
- Must ensure A > 1 and A mod p ≠ 1 (order N ≥ 2 handles it; for N=1 use M=1).
- A = g^((p−1)/N) mod p could be 1 only if... it has order exactly N since g is primitive — fine. But A could be small like 1? No, order N ≥ 2 means A ≠ 1. Edge: A might equal p−1 etc., all fine, A ≤ p ≤ 1e18.
- Miller-Rabin bases for < 2^64 or just < ~1e13: bases {2,3,5,7,11,13} plenty.
- Speed: 1e4 tests × (prime search + few MR tests + primitive root) — fine in Python if trial division primes precomputed once (sieve to 31623 → 3401 primes).
- Worst-case k search: need a safety bound. If k exceeds, say, 10^6 (never expected), fallback: use M = p*q style or just trust. Known records: smallest prime ≡1 mod N for N ≤ 1e9 has k well below ~10^5. Acceptable.

## worker: Implement the full solution: sieve primes to 31623
- Construction: find prime p = kN+1 by scanning k = 1, 2, ... (N | p−1). For a primitive root g mod p, A = g^((p−1)/N) mod p has multiplicative order exactly N, so the least n with M | A^n − 1 is N (M = p).
- Primality: deterministic Miller–Rabin with bases {2,3,5,7,11,13,17}, valid well beyond the sizes encountered (p = kN+1 with small k; even k up to millions keeps p < 1e16, and these bases are deterministic below 3.4e14 — to be fully safe the set is valid to 341,550,071,728,321; given N ≤ 1e9 and expected small k this is fine; could add bases 19, 23 for extra margin but not needed).
- Factorization of p−1: factor N (≤1e9) and k (small) via trial division with precomputed primes up to 31623; union of distinct primes gives all distinct prime divisors of p−1, enough for the primitive-root test (g^((p−1)/q) ≠ 1 for every prime q | p−1).
- N = 1: output "2 1" — mod 1 everything is 0, so smallest n is 1.
- Sample check: N=3 → k=2, p=7; factors of 6: {2,3}; g=2 fails (2^3=8≡1), g=3 works (3^3=27≡6≠1, 3^2=2≠1); A = 3^2 mod 7 = 2 → "2 7" ✓. N=16 → k=... p=17? 17=1*16+1 prime; factors of 16: {2}; g=3 primitive (3^8 mod 17 = 16 ≠ 1); A = 3^1 = 3, order of 3 mod 17 is 16 ✓ (sample used different valid answer). N=55 → p = k*55+1: k=1→56 no, k=2→111 no, k=4→221=13·17 no, k=6→331 prime; order-55 element exists ✓.
- Performance: sieve once; per test case a few Miller–Rabin rounds and a primitive-root search over small candidates — easily handles T = 1e4.

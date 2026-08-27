
## ideation
We need ord_M(A) = N exactly, with A, M ≤ 10^18 and N ≤ 10^9, T ≤ 10^4.

Key idea: if M = p is prime and N | p−1, then any primitive root g mod p gives A = g^((p−1)/N) mod p with order exactly N. So the problem reduces to:
1. Find prime p = kN + 1 (Dirichlet guarantees existence; in practice small k works for N ≤ 10^9 — worst observed k is a few thousand).
2. Find a primitive root g mod p: trial g = 2, 3, 5, ... checking g^((p−1)/q) ≠ 1 mod p for every prime divisor q of p−1. This needs the distinct prime factors of p−1 = kN.
3. Output A = pow(g, (p−1)//N, p), M = p. Both ≤ p ≤ 10^18 easily since p ≈ kN with small k.

Edge cases:
- N = 1: any A with M | A−1 works, e.g., A = 2, M = 1 (order mod 1 is conventionally 1; sample uses M=1). Actually with M = 1, A^1 − 1 ≡ 0 mod 1 always, so smallest n = 1. Safe: output (2, 1). Alternatively p = 2 with A = 1... but A=1, M=2: 1^1−1 = 0 divisible by 2, smallest n = 1. Either fine.
- N = 2: p = 3? No wait, kN+1 = 3 is prime, primitive root 2, A = 2^1 = 2, ord_3(2) = 2. Good.

Performance concerns:
- Primality testing of p up to ~10^12 (kN with k maybe up to ~10^3–10^4, N up to 10^9 → p up to ~10^13): deterministic Miller–Rabin with bases [2,3,5,7,11,13] or the known 7-base set for < 3.3×10^24 is fine and fast.
- Factoring N (≤ 10^9) per test case: trial division by primes up to 31623 (~3401 primes). Worst case 10^4 × 3401 ≈ 3.4×10^7 modulo operations — borderline but okay in PyPy/Python if we only need distinct prime factors and break early (after dividing, remaining cofactor reduces quickly). We can cache factorizations with a dict since test cases may repeat. Also we only need factors of kN; k is small so factor k directly.
- Alternative avoiding factoring N entirely: choose p and require ord = N. Note we don't need full factorization of p−1 if we instead pick A differently... Actually there's a neat trick: we need g^((p−1)/q) ≠ 1 only for q | (p−1). Since p−1 = kN, prime divisors are divisors of k plus divisors of N. We must factor N. But note: we can choose k to be a prime not dividing N... still need N's factors. Alternatively pick p = kN+1 and set A = g^k where g is primitive root — then order of A is N exactly iff g is primitive. So we need primitive root, which needs factorization of p−1. Factoring N per test with precomputed prime list is the plan; with caching and early termination it's fine.

Pitfalls:
- Miller–Rabin must handle p up to maybe 10^13–10^14 if k gets large; use enough bases (deterministic set for < 2^64: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] or the known 7-base set [2, 325, 9375, 28178, 450775, 9780504, 1795265022]).
- Scanning k: k must be such that p = kN+1 is prime; also k can be any positive integer. Expected k small (heuristically O(log^2 N)); worst case for N ≤ 10^9 known to be within a few thousand. To be safe, allow scanning up to large k with fast MR.
- Primitive root search: expected a few trials.
- A must satisfy 1 ≤ A ≤ 10^18: pow gives value in [0, p−1]; A could be 1 only if (p−1)/N ≡ 0 mod ord... A = g^((p−1)/N) has order N ≥ 1; if N = 1, A = 1 mod p, i.e., A = 1, order 1 — but then smallest n with 1^n ≡ 1 mod p is n = 1. Fine, but handle N=1 separately for clarity (A=2, M=1).
- Ensure gcd(A, M) = 1 — automatic since A ∈ [1, p−1].
- Verify: could double-check ord_M(A) = N by checking A^N ≡ 1 and A^(N/q) ≠ 1 for q | N — cheap sanity check using factors of N.

Simpler alternative worth considering: M = N+1 if prime, A primitive root — but N+1 not always prime. Another: use two primes and CRT to avoid factoring N? E.g., for each prime power q^e || N pick prime p_i ≡ 1 mod q^e... more complex. Stick with the single-prime plan.

Complexity per test: MR tests ~O(k_scan × log p), factoring N ~ O(#primes up to √N) worst ~3400 divisions, fine.

## worker: Implement the full solution: sieve primes to 31623
- Construction: for prime `p = kN + 1` (exists by Dirichlet; found by scanning `k = 1, 2, ...`), a primitive root `g mod p` yields `A = g^((p-1)/N) mod p` with multiplicative order exactly `N`. Output `(A, M=p)`.
- `N = 1` handled specially: `(A, M) = (2, 1)`; `2^1 - 1 = 1` is a multiple of 1, smallest `n = 1`.
- Primality: deterministic Miller–Rabin with the 7-base set valid for all 64-bit integers (p stays far below 2^63 in practice; for N ≤ 10^9 the least prime ≡ 1 mod N has small k).
- Primitive root test uses distinct prime factors of `p-1 = kN`; factors of N (≤ 10^9) obtained by trial division over sieved primes up to 31623, memoized in `_factor_cache` (also reused for repeated N and small k values).
- Correctness argument: `g` primitive ⇒ order of `g` is `p-1`; order of `g^((p-1)/N)` is `(p-1)/gcd(p-1, (p-1)/N) = N`. Since `A^N ≡ 1 (mod p)` and no smaller positive exponent works, the minimal n is exactly N. `gcd(A, p) = 1` since `1 ≤ A ≤ p-1`. Bounds: `1 ≤ A, M ≤ p ≤ 10^18` easily.
- Sanity-checked mentally on samples: N=3 → p=7, g=3 (or found g=3? g=2 fails? 2^3=8≡1 mod7? 2^3 mod7=1, so 2 not primitive; g=3 works), A = 3^2 = 2 mod 7 → (2, 7) matches sample. N=1 → (2,1) valid like sample's M=1 idea.

## worker: Verify the implementation end-to-end: trace sample
End-to-end verification of the implementation:

**Trace of sample cases:**
- **N=3**: k=1 → p=4 (not prime); k=2 → p=7 prime. facs of p−1=6: {2,3}. Primitive root search: g=2: pow(2, 3, 7)=8%7=1 → fails (q=2). g=3: pow(3,3,7)=27%7=6≠1, pow(3,2,7)=9%7=2≠1 → primitive. A = pow(3, 6//3=2, 7) = 9%7 = 2. Output "2 7" — matches sample exactly. ✓
- **N=16**: k=1 → p=17 prime. facs of 16: {2}. g=2: pow(2,8,17)=256%17=1 → fails. g=3: pow(3,8,17)=6561%17=16≠1 → primitive. A = pow(3, 16//16=1, 17) = 3. Output "3 17". Check: ord_17(3)=16 (3 is a known primitive root mod 17). ✓ (Sample gave "11 68"; any valid answer accepted.)
- **N=1**: special case → "2 1". 2^1−1=1 is a multiple of 1; smallest n=1. ✓ (Matches sample's M=1 convention.)
- **N=55**: k=1 → 56 no; k=2 → 111=3·37 no; k=4 → 221=13·17 no; k=6 → 331 prime. facs of 330=2·3·5·11: {2,3,5,11}. Primitive root g=3 (g=2: pow(2,110,331)... 2 is not primitive mod 331; search finds small g). A = pow(g, 330//55=6, 331), order = 330/gcd(330,6) = 55. ✓

**Correctness proof:** For prime p with N | p−1 and primitive root g (verified by g^((p−1)/q) ≢ 1 for all prime q | p−1), A = g^((p−1)/N) mod p has order (p−1)/gcd(p−1, (p−1)/N) = N. Hence A^N ≡ 1 (mod p) and A^n ≢ 1 for 1 ≤ n < N, so the minimal n is exactly N. gcd(A,p)=1 since 1 ≤ A ≤ p−1.

**Edge cases:**
- N=2: k=1 → p=3 prime, facs={2}, g=2 (pow(2,1,3)=2≠1), A=pow(2,1,3)=2 → "2 3", ord_3(2)=2. ✓
- N=1 handled separately (avoids A=1 degenerate output and M=1 is explicitly allowed by sample).
- Large N near 10^9: least prime p ≡ 1 (mod N) for N ≤ 10^9 has small k (empirically ≤ few thousand; Linnik/Dirichlet guarantees existence). p ≤ ~10^13, far below 10^18 and within the 7-base deterministic MR range (< 3.3×10^24). ✓
- The `A <= 1` guard: for N ≥ 2, A = g^((p−1)/N) has order N ≥ 2, so A ≥ 2; guard is dead code but harmless (even if triggered, A+p keeps congruence and validity).

**Component checks:**
- Sieve: bytearray slicing correct; PRIMES up to 31623 = ⌊√(10^9)⌋ + margin (31622² = 999,950,884 < 10^9 < 31623²). ✓
- MR: small-prime trial division first (handles n equal to those primes via `n == p`), then 7-base test; correct for all n < 2^64. Bases reduced mod n to handle n < base. ✓
- Factor caching: `distinct_prime_factors` breaks when p² > m and appends residual m > 1 (a prime possibly > 31623, e.g., when N itself is a large prime ~10^9 — loop breaks immediately since p² > m from the start... actually p starts at 2, p²=4 ≤ m, iterates until p² > m; for prime N ≈ 10^9 it scans all 3401 primes then appends N). Cached per distinct N and small k values. ✓
- Performance: T=10^4 worst case — each test does a few MR tests (~7 modular exponentiations each) plus one factorization of N (≤3401 trial divisions, cached on repeats) and a primitive-root search (few candidates × ≤ ~10 pow calls). Well within limits.

**Bounds:** A, M = p ≤ k·N+1 with small k ⇒ ≪ 10^18. ✓

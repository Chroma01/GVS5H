
## ideation
Core difficulty: we need ord_M(A) = N exactly, with A, M ≤ 1e18, N ≤ 1e9, and up to 1e4 test cases — so per-test work must be small (no heavy search per case, no factoring of huge numbers).

Key mathematical fact: if p is prime and g is a primitive root mod p, then A = g^((p-1)/N) mod p has order exactly N, provided N | (p-1). So the whole problem reduces to: find a prime p ≡ 1 (mod N) with p ≤ 1e18, and a primitive root g mod p.

Approach analysis:

1. **Dirichlet prime search (the planned approach).** For k = 1, 2, 3, ..., test whether p = kN + 1 is prime (deterministic Miller-Rabin for 64-bit). By Dirichlet such a prime exists; heuristically the smallest k is O(log² N)-ish, and even pessimistically it's small (kN+1 ≤ 1e18 means k can go up to 1e18/N, plenty of room). For N=1: p = k+1, first prime is p=2 with k=1; then (p-1)/N = 1, A = g^1 = g, order of primitive root mod 2... careful: mod 2 the group is trivial, order is 1 — that actually works for N=1! ord_2(1) = 1 since 1 ≡ 1 mod 2. Actually simplest for N=1: output A=2, M=1 (everything is a multiple of 1, smallest n is 1). Or just let the general machinery handle it: p=2, g=1 (primitive root mod 2 is 1), A = 1^1 mod 2 = 1, M = 2. Check: 1^1 - 1 = 0 divisible by 2, smallest n = 1. ✓. So general path handles N=1 too, but M=1 special case is even simpler. Either fine.

2. **Primitive root search.** Given prime p, factor p-1 (p-1 = kN; we know N's factorization? No — we'd need to factor p-1 ≤ 1e18, which is expensive). Alternative: we don't need a primitive root of the full group! We only need an element of order exactly N. Better: find any element g whose order is a multiple of N... hmm, still needs factorization.

   Cleaner: factor N (N ≤ 1e9, trial division up to 31623 is fine, or even faster with a few primes). Then to find an element of order exactly N mod p: pick random/small bases b, compute x = b^((p-1)/N) mod p. The order of x divides N. Check that x^(N/q) ≠ 1 mod p for every prime factor q of N; if so, ord(x) = N exactly. If b is chosen at random, the probability that b^((p-1)/N) has full order N is φ(N)/N ≥ ~1/6 typically (bounded below by c/log log N), so a few trials suffice. Deterministically trying b = 2, 3, 5, ... is virtually guaranteed to succeed within a handful of tries (a bad b would require b to be an N-th power-ish; the number of bad b's is small).

   This avoids factoring p-1 entirely — only N needs factoring. 

3. **Verification-free correctness.** By construction: x^N = b^(p-1) ≡ 1 (Fermat), and x^(N/q) ≠ 1 for all prime divisors q of N ⟹ ord(x) = N. Solid.

4. **Edge cases and pitfalls:**
   - N = 1: prime factors list is empty; x = b^((p-1)/1) = b^(p-1) ≡ 1 mod p, order 1. ✓ (any b works; x=1). With p=2: x = 1, M=2, A=1. Valid. Or just special-case (2, 1).
   - p must satisfy p ≤ 1e18: p = kN+1 with small k, N ≤ 1e9, so p ≈ kN is tiny. No overflow concerns in Python anyway.
   - A must be ≥ 1: x = pow(b, (p-1)//N, p) ∈ [1, p-1], fine. Also A ≤ 1e18 since A < p.
   - Miller-Rabin: for p < 3.3e18 (actually < 3.4e14 needs fewer bases; for full 64-bit use bases [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] or the known 7-base set [2, 325, 9375, 28178, 450775, 9780504, 1795265022]). Since p ≤ ~1e18, use the deterministic 7-base set, or since our p will actually be small (k small), even simpler bases suffice — but use the safe set regardless.
   - Performance: T = 1e4. Per test: factor N by trial division up to N^(1/3)? No — full trial division to 31623 with primes (~3400 primes) × 1e4 tests = 3.4e7 divisions worst case... borderline but okay in Python if we only divide by primes and stop early; most N factor quickly. Better: trial divide by primes up to cube root, then check remainder (it's prime, or product of two primes — we just need the distinct prime factors, so: after trial division up to 31623 the remainder r is 1, prime, or p·q with both > 31623; if r > 1, r is either prime or product of two primes > 31623, i.e., r = p² possible? p² > 31623² ≈ 1e9 ≥ N, so r is squarefree: either prime or p·q distinct. We need distinct prime factors of N only for the order check — if r = p·q, we need both. Use Miller-Rabin on r: if prime, add r; else add both factors via Pollard rho or since r = p·q with p,q > 31623 and r ≤ 1e9, we can find p by trial division... no, p > 31623 already excluded, contradiction — wait, if r = p·q with both > 31623 then r > 1e9 ≥ N, impossible. So r is prime or r = p² where p ≤ 31623 — but then p would have been found in trial division. So r must be prime! Great: trial division to 31623 leaves remainder that is 1 or prime. No Pollard rho needed.)
   - Prime search p = kN+1: expected few iterations; each MR test on ≤64-bit numbers is fast (~7 bases × ~60 mulmods). With 1e4 tests × avg maybe 5-30 candidates... could be 1e4 × 20 × 7 × 60 ≈ 8.4e7 modular multiplications worst-ish case — might be slow in Python (maybe 30-60s). Mitigation: quick trial division by small primes (e.g., primes < 100) before MR to reject composites cheaply. Also note kN+1: for k=1, N+1 prime sometimes; expected number of candidates until prime among kN+1 is O(log N) ≈ 20-30. With small-prime sieve prefilter (reject if divisible by primes ≤ 97), MR calls drop ~5×. Should be fine (~a few seconds).
   - Alternative cheaper trick: reuse? Different N give different p; no reuse in general.
   - pow() with three args in Python is fast (C implementation), so MR and exponentiation are efficient.

5. **Alternative constructions considered:**
   - M = 1 + A + ... + A^{N-1} with A = N+1: order divides N but could be a proper divisor (e.g., N=4, A=5: 5² ≡ 1 mod (1+5+25+125)=156? 25 mod 156 ≠ 1; but not provably always N). Not guaranteed — reject.
   - M = A^N - 1: order of A mod (A^N - 1) is exactly N (since A^k - 1 < A^N - 1 for k < N and A^k ≢ 1). Wait — is that right? Mod M = A^N - 1, A^N ≡ 1. For k < N, A^k - 1 is positive and < M, so M ∤ (A^k - 1). So ord_M(A) = N exactly! This is trivially correct!! Check constraints: A, M ≤ 1e18. Take A = 2, M = 2^N - 1. For N ≤ 60ish, 2^N - 1 ≤ 1e18 (2^60 ≈ 1.15e18 > 1e18; 2^59 ≈ 5.8e17 ok). But N up to 1e9 — 2^N way too big. Hmm, but wait: we need A^N - 1 ≤ 1e18 with A ≥ 2, so N ≤ 59 for A=2. Doesn't cover N up to 1e9. Unless A=1: 1^N - 1 = 0, M=0 not positive. Dead end for large N. But this is a neat solution for small N! Hybrid: for N ≤ 59, output (2, 2^N - 1) — O(1), no search. For N > 59, use the prime method. Actually the prime method works for all N, but the hybrid speeds up small cases... T=1e4 with mixed N; prime method alone is probably fast enough. Keep it simple: just use prime method for all N (it handles N=1 too). Actually, hmm, for N=1 the prime method: p = k·1+1 = k+1, k=1 gives p=2 prime. Factor N=1: no prime factors. b=2: x = pow(2, (2-1)//1, 2) = pow(2,1,2) = 0! A=0 — invalid (A must be positive). Problem! Because b mod p could make x = 0? x = b^((p-1)/N) mod p; with p=2, b=2: 2^1 mod 2 = 0. Need b not divisible by p. Choose b in [2, p-1]... for p=2 there's no valid b ≥ 2 coprime... b must be coprime to p; b=2 ≡ 0 mod 2. Use b=1? x=1, order 1 = N. ✓. So special-case N=1: output (1, 2) or (2, 1). Simplest: if N == 1: print("2 1"). Clean.
   - Also guard: ensure gcd(b, p) = 1 — since p prime and we pick small b < p, fine (p will be > b for N ≥ 2 since p = kN+1 ≥ 2·2+1... for N=2, k=1: p=3; b=2 < 3 ok).

6. **Refined plan:**
   - Precompute primes up to 31623 (sieve) once.
   - For each test:
     - If N == 1: output "2 1" (or "1 2"). Done.
     - Factor N via trial division by precomputed primes; collect distinct prime factors; leftover > 1 is prime (proved above).
     - Find prime p = kN + 1, k = 1, 2, ...: prefilter with small primes (note: p = kN+1; also skip even p — if N is odd, kN+1 even when k odd, so use k even only when N odd; if N even, kN+1 always odd). Then deterministic Miller-Rabin (7-base set safe for < 2^64; our p is way smaller, even bases [2,3,5,7,11] would do for p < 2.1e12... but p could theoretically be larger if k grows; use the safe 7-base set, cheap enough).
     - For b in 2, 3, 4, 5, ...: x = pow(b, (p-1)//N, p); if x == 1: continue (order 1, bad); check all prime factors q of N: pow(x, N//q, p) != 1; if all pass, A = x, M = p, output.
   - Correctness: x^N = b^(p-1) ≡ 1 mod p (Fermat, gcd(b,p)=1). ord(x) | N. ord(x) ≠ N/q' for any... precisely: if ord(x) were a proper divisor d of N, then d | N/q for some prime q | N, so x^(N/q) = 1 — contradiction. Hence ord(x) = N. ✓
   - Existence of good b: the map b → b^((p-1)/N) hits exactly the subgroup of order N (image size N since gcd... the image of (Z/p)* under exponentiation by (p-1)/N is the unique subgroup of order N, since N | p-1). Number of b giving element of order exactly N: φ(N)·(number of b mapping to each element = (p-1)/N)... fraction φ(N)/N of bases work. φ(N)/N ≥ 1/(e^γ log log N + ...) — for N ≤ 1e9, worst φ(N)/N ≈ 0.16 or so (product of first primes). So expected ≤ ~6 tries. Fine.

7. **Pitfalls checklist:**
   - N=1 special case (b^((p-1)/N) with p=2 gives x=0; avoid entirely).
   - Ensure b < p and gcd(b,p)=1 (b small, p prime > b — but check p > b; for N=2, p=3, b=2 fine).
   - A = x must be ≥ 1: x=0 impossible when gcd(b,p)=1; x ≥ 1 always from pow. ✓
   - M = p ≤ 1e18: p = kN+1; k found small; even k up to 1e9 gives p ≤ 1e18+1 — monitor not needed realistically, but the search will terminate long before. (Heuristic bound; in practice k ≤ few hundred.)
   - Miller-Rabin must handle p=2,3 and even numbers.
   - Speed: prefilter candidates kN+1 by small primes before MR. Note kN+1 mod small prime r: compute incrementally.
   - Python pow(base, exp, mod) is fast.
   - Input reading: sys.stdin.

8. **Double-check sample:** N=3: factor [3]. k=1: p=4 no; k=2: p=7 prime. b=2: x = 2^(6/3)=2^2=4 mod 7. Check q=3: x^(3/3)=4^1=4 ≠1 mod 7. So A=4, M=7. Verify: 4^1=4, 4^2=16≡2, 4^3=64≡1 mod 7. Order 3 ✓ (sample used 2 7; ours equally valid).
   N=16: factors [2]. k=1: p=17 prime. b=2: x = 2^(16/16)=2^1=2 mod 17. Check q=2: x^8 = 2^8=256 ≡ 1 mod 17 (256 = 15·17+1). Bad! b=3: x=3; 3^8 mod 17 = 6561 mod 17: 17·385=6545, 6561-6545=16 ≠1. Good. A=3, M=17. Verify order of 3 mod 17: 3^16≡1, 3^8≡16≠1 ⟹ order 16. ✓
   N=55: factors [5,11]. k=1: 56 no; k=2: 111 no; k=3: 166 no; k=4: 221=13·17 no; k=5: 276 no; k=6: 331 prime? 331: not div by 2,3,5,7(7·47=329),11(11·30=330),13(13·25=325,13·26=338),17(17·19=323,17·20=340). √331≈18.2. Prime ✓. p=331. b=2: x=2^(330/55)=2^6=64 mod 331. Check 64^(55/5)=64^11 mod 331 and 64^5 mod 331. 64^5 = 64^2=4096 mod 331: 331·12=3972, 4096-3972=124; 64^4 = 124² = 15376 mod 331: 331·46=15226, =150; 64^5 = 150·64=9600 mod 331: 331·29=9599, =1. Bad (order divides 11). b=3: x=3^6=729 mod 331 = 729-662=67. 67^5 mod 331: 67²=4489 mod 331: 331·13=4303, 186; 67^4=186²=34596 mod 331: 331·104=34424, 172; 67^5=172·67=11524 mod 331: 331·34=11254, 270 ≠1. 67^11 = 67^5·67^5·67 = 270·270·67 mod 331: 270²=72900 mod 331: 331·220=72820, 80; 80·67=5360 mod 331: 331·16=5296, 64 ≠1. Good: A=67, M=331. ✓ (sample gave 33 662; ours valid too.)

9. **Complexity estimate:** per test: factoring N (≤ 3401 prime divisions worst case, usually far less), prime search (tens of cheap modular checks + a few MR), base search (few pow-mod calls, each ~30-40 bit exponent... (p-1)/N = k small, and N//q up to 1e9 → ~30 squarings). All fast. Total well within limits.

## worker: Implement the complete Python solution: sieve prim
- **Construction**: For prime `p = kN+1` (so `N | p-1`) and base `b` coprime to `p`, let `x = b^((p-1)/N) mod p`. Then `x^N = b^(p-1) ≡ 1 (mod p)` by Fermat, so `ord(x) | N`. If additionally `x^(N/q) ≠ 1` for every prime divisor `q` of `N`, then `ord(x)` cannot be a proper divisor of `N` (any proper divisor divides some `N/q`), hence `ord(x) = N` exactly. Output `(A, M) = (x, p)`.
- **Existence/termination of base scan**: the image of `(Z/p)*` under exponentiation by `(p-1)/N` is the subgroup of order `N`; a fraction `φ(N)/N` of bases yield an element of full order `N`, so scanning `b = 2, 3, ...` succeeds within a few tries.
- **Prime search**: Dirichlet guarantees `p = kN+1` prime exists; in practice `k` is tiny. Parity optimization (even `k` only when `N` odd) plus small-prime prefilter keeps MR calls rare. `p` stays far below `1e18`, and `1 ≤ A < p`, satisfying bounds.
- **Factoring `N ≤ 1e9`**: trial division by sieved primes up to `31623`; the leftover `r > 1` must be prime (if `r = uv` with `u,v > 31623` then `r > 1e9`, contradiction; if `r = u²` then `u ≤ 31623` would have been found). So no Pollard rho needed.
- **N = 1**: special-cased as `(2, 1)` — everything is a multiple of 1, smallest `n` is 1. (Avoids the degenerate `p = 2` case where `b ≡ 0 mod 2`.)
- **Miller-Rabin**: deterministic 7-base set valid for all `n < 2^64`.
- Hand-verified against sample logic: N=3 → (4, 7) [ord 3]; N=16 → (3, 17) [3^8 ≡ 16 ≠ 1, 3^16 ≡ 1]; N=55 → (67, 331) [67^5 ≢ 1, 67^11 ≢ 1, 67^55 ≡ 1]. All valid alternative answers.
- Complexity per test: ≤ ~3400 trial divisions (usually far fewer), a handful of MR tests (~7 pow-mods each on ≤64-bit ints), and a few pow-mods for the base scan — easily fast enough for T = 1e4.

## worker: Review final code for correctness and edge cases (
Reviewed the code against the requested edge cases and the full constraint space:

- **N = 1**: Special-cased to `(2, 1)`. Every integer is a multiple of 1, so `2^1 - 1 = 1` is a multiple of 1 and the smallest `n` is 1. This avoids the degenerate `p = 2` case where any even base `b ≡ 0 (mod 2)` would give `A = 0` (invalid). ✓
- **N = 2**: `facs = [2]`; `step = 1`, `k = 1` → `p = 3` (prime). `e = 1`, `b = 2`: `x = 2^1 mod 3 = 2 ≠ 1`; check `pow(2, 1, 3) = 2 ≠ 1` → output `(2, 3)`. Verify: `2^1 - 1 = 1` not divisible by 3, `2^2 - 1 = 3` divisible. Order exactly 2. ✓
- **Powers of 2 (e.g., N = 16, N = 2^29)**: `facs = [2]` only. For N=16: `p = 17`, `b=2` gives `x=2` but `2^8 ≡ 1 (mod 17)` → rejected; `b=3` gives `x=3`, `3^8 ≡ 16 ≠ 1` → `(3, 17)`, order exactly 16. The single-prime-factor check correctly forces full order since the only maximal proper divisor of `2^m` is `2^(m-1) = N/2`. ✓
- **N prime near 1e9 (e.g., N = 999999937)**: `prime_factors` trial-divides by primes up to 31623; none divide N, loop breaks when `p*p > n`, leftover `n > 1` appended — and the leftover is provably prime (if it were composite `uv` with `u,v > 31623`, then `uv > 31623² ≈ 1.0003e9 ≥ N`, contradiction; a square `u²` would have `u ≤ 31623` already found). So `facs = [N]`. Prime search: N odd → `step = 2`, candidates `2k'N+1` all odd; prefilter + MR finds `p` quickly (expected `k` in the tens). Base scan: fraction `φ(N)/N = (N-1)/N ≈ 1` of bases work, so `b = 2` almost always succeeds immediately. `p ≈ 2kN` stays far below `1e18`. ✓
- **Correctness invariant**: For `p = kN+1` prime and `gcd(b,p)=1`, `x = b^k mod p` satisfies `x^N = b^(p-1) ≡ 1` (Fermat), so `ord(x) | N`. If `ord(x)` were a proper divisor `d` of `N`, then `d | N/q` for some prime `q | N`, giving `x^(N/q) = 1` — exactly what the loop rejects. Hence `ord(x) = N`. Termination of the base scan is guaranteed because the image of `(Z/p)*` under `b ↦ b^((p-1)/N)` is the order-N subgroup, and a fraction `φ(N)/N ≥ ~0.16` (worst case for N ≤ 1e9) of bases yield a generator of it.
- **Removed dead code**: the `if b >= p: b = 2` safety reset was useless (it would loop forever repeating the same bases if ever hit, and it can never be hit in practice since a good `b` exists among `2..p-1` and is found within a few tries). Cleaner without it.
- **Bounds**: `1 ≤ A = x < p = M ≤ ~1e12` in practice (k is tiny), well within `[1, 1e18]`. Both positive. ✓
- **MR correctness**: the 7-base set `{2, 325, 9375, 28178, 450775, 9780504, 1795265022}` is deterministic for all `n < 2^64`; small-prime trial division up to 37 handles tiny candidates and divides out trivial cases first. `a %= n` guard handles bases ≥ n. ✓
- **Performance for T = 1e4**: worst-case per test is ~3400 trial divisions for factoring (only for N with no small factors), plus a handful of MR tests (each ~7 pow-mods on ≤64-bit ints, done in C via `pow`), plus a few pow-mods for the base scan. Small-prime prefilter rejects ~80%+ of composite candidates before MR. Comfortably fast.

Hand-traced sample logic: N=3 → (4,7) [4³≡1, 4¹,4²≢1 mod 7]; N=16 → (3,17); N=1 → (2,1); N=55 → (67,331) [67⁵≢1, 67¹¹≢1, 67⁵⁵≡1 mod 331]. All valid (problem allows any correct pair).

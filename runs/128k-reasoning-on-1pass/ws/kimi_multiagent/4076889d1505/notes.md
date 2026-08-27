
## ideation
Core difficulty: the condition is exactly “multiplicative order of A modulo M is N” (for M>1 this forces gcd(A,M)=1). We need a uniform construction for all N≤1e9 with A,M≤1e18 and fast enough for T≤1e4.

The CRT/prime-power plan looks sound: factor N=∏p^e, build a local modulus m_p and residue a_p with ord_{m_p}(a_p)=p^e, make the m_p pairwise coprime, CRT to one A modulo M=∏m_p. Then A^n≡1 mod M iff every p^e divides n, so the least n is lcm(p^e)=N.

Local constructions to verify:
- Odd p: a=1+p, m=p^{e+1}. LTE/binomial gives v_p((1+p)^{p^k}-1)=k+1, so order is exactly p^e.
- p=2: use a=3, m=4 for e=1 (3≡-1 has order 2); for e≥2 use a=3, m=2^{e+2}, where ord(3)=2^e. This also keeps m≤(p^e)^2, hence M≤N^2≤1e18.

Edge cases/pitfalls: N=1 must be handled separately, e.g. (A,M)=(1,1). Do not output A=0 after CRT; if CRT residue is 0 use M, though for N>1 the residue should be coprime and nonzero. Factoring via sieve primes up to sqrt(1e9) is enough; watch worst-case time. In non-Python languages, CRT intermediate products need big-integer care; Python avoids this. Need ensure A,M stay within inclusive bounds and that M=1 is allowed only for the N=1 trivial case.

## worker: Implement the complete Python solution: fast facto
- **Construction correctness**: The condition is exactly "multiplicative order of A mod M equals N" (for M > 1 this forces gcd(A, M) = 1).
  - Odd prime power p^e: a = 1+p, m = p^(e+1). By LTE, v_p((1+p)^n − 1) = v_p(n) + 1, so (1+p)^n ≡ 1 (mod p^(e+1)) iff p^e | n; order is exactly p^e.
  - p = 2, e = 1: a = 3 ≡ −1 (mod 4), order 2.
  - p = 2, e ≥ 2: a = 3, m = 2^(e+2); classical result ord_{2^k}(3) = 2^(k−2) for k ≥ 3, giving order 2^e.
  - Local moduli are pairwise coprime (distinct primes), so CRT combines them into one A mod M = ∏ m_p. Then A^n ≡ 1 (mod M) iff every local order p^e divides n, so the least such n is lcm(p^e) = N.
- **Bounds**: each m_p ≤ (p^e)^2 (odd: e+1 ≤ 2e; p=2,e=1: 4 = 2²; p=2,e≥2: 2^(e+2) ≤ 2^(2e) iff e ≥ 2). Hence M ≤ N² ≤ 10^18, and 1 ≤ A < M (A is coprime to M, so nonzero). N = 1 handled as (1, 1).
- **Factorization speed**: trial division by 168 primes ≤ 1000 (early exit when p² > n leaves a prime remainder), then deterministic Miller-Rabin (bases 2, 7, 61, valid < 2^32). If still composite, the remainder ≤ 10^9 has no factor ≤ 1000, so it is a product of exactly two primes; one Brent Pollard-Rho split suffices. This avoids the ~3400-iteration full trial division per test that would TLE at T = 10^4.
- CRT uses `pow(M, -1, m)` (Python ≥ 3.8); Python big ints make intermediate products safe.

## worker: Brute-force verify the constructed multiplicative 
- **What was verified** (harness embeds the solution from CURRENT WORK verbatim and asserts on its outputs):
  1. **True brute force for all N ∈ [1, 2000]**: iterates k = 1, 2, … computing A^k mod M and confirms the *first* k with A^k ≡ 1 (mod M) is exactly k = N. This covers N = 1, N = 2, small powers of 2, odd prime powers, and many composites with no number-theoretic assumption about the construction.
  2. **Edge cases** (all 2^k up to 2^29, prime powers 3^e/5^e/7^e, 10^9, 10^9−1, 10^9−2, a prime near 10^9, products of two primes > 1000 to exercise the Pollard-Rho path, and highly composite numbers) plus **300 random N ∈ [1, 10^9]**, checked by a criterion that is a complete proof of order = N:
     - `pow(A, N, M) == 1` ⟹ ord_M(A) | N;
     - `pow(A, N//q, M) != 1` for every prime q | N ⟹ ord ∤ N/q ⟹ v_q(ord) > v_q(N) − 1, i.e. v_q(ord) = v_q(N);
     - combining over all q | N gives ord_M(A) = N exactly.
  3. **Bounds/gcd**: 1 ≤ A, M ≤ 10^18, M ≤ N², gcd(A, M) = 1 for M > 1, and (A, M) = (1, 1) for N = 1. `factor()` itself is validated (each returned p passes deterministic Miller-Rabin; the product of p^e reconstructs n).
- **Why the harness passes (proof sketch of the construction)**:
  - Odd p^e: a = 1+p, m = p^(e+1). LTE gives v_p((1+p)^n − 1) = v_p(n) + 1, so a^n ≡ 1 (mod p^(e+1)) ⟺ p^e | n; local order = p^e.
  - p = 2, e = 1: 3 ≡ −1 (mod 4), order 2. p = 2, e ≥ 2: ord_{2^(e+2)}(3) = 2^e (classical; 3 = 1+2, v_2(3^n−1) = v_2(n) + 2 for even n).
  - Local moduli are powers of distinct primes, hence pairwise coprime; CRT yields one A mod M = ∏ m_p with ord_M(A) = lcm(p^e) = N. Each m_p ≤ (p^e)² (e+1 ≤ 2e; 2^(e+2) ≤ 2^(2e) for e ≥ 2; 4 = 2² for e = 1), so M ≤ N² ≤ 10^18, and A is coprime to M hence 1 ≤ A < M.
- The solution program itself is unchanged; this task only adds independent validation, all of which the construction satisfies by the arguments above.


## ideation
We need ord_M(A) = N exactly, with A, M ≤ 1e18, for N up to 1e9 and T up to 1e4 test cases.

Key facts and candidate constructions:
- For an odd prime p, ord_{p^{k}}(1+p) = p^{k-1} (lifting-the-exponent / binomial expansion of (1+p)^{p^j}). For p=2, ord_{2^k}(5) = 2^{k-2} for k≥3; ord_4(3)=2.
- If M = m1*m2 with gcd(m1,m2)=1, then ord_M(A) = lcm(ord_{m1}(A), ord_{m2}(A)). So we can build per-prime-power components and combine via CRT.

Plan: factor N = ∏ p_i^{e_i}. For each prime power q = p^e:
- Choose modulus m_q = p^{e+1} (odd p) and base a_q = 1+p, giving exact order p^e.
- For p=2: modulus 2^{e+2}, base 5, giving order 2^e (for e≥1; check e=1: ord_8(5)=2 ✓).
These moduli for distinct primes are pairwise coprime automatically. CRT-combine bases a_q into a single A mod M = ∏ m_q. Then ord_M(A) = lcm of p_i^{e_i} = N.

Pitfalls / size checks:
- M = ∏ p^{e+1} (and 2^{e+2} for p=2) could exceed 1e18? Worst case N = 2^29 ≈ 5.4e8 → M = 2^31 ≈ 2.1e9, fine. N with many distinct primes: primorials ≤ 1e9: 2·3·5·7·11·13·17·19·23 ≈ 2.23e8 (9 primes), M = ∏ p^2 = (2.23e8)^2 ≈ 5e16 < 1e18 ✓. Adding the next prime 29 exceeds 1e9 for N. Mixed: N = 2^a·(odd primorial)... need to double check worst case: M = 2^{a+2}·∏ p_i^{e_i+1} = 4·(∏ p_i)·N ≤ 4·N·(product of distinct primes dividing N) ≤ 4·N·rad(N). With N ≤ 1e9 and rad(N) ≤ N, worst bound 4e18 — borderline! Need a sharper check: rad(N)·N maximized when N is a primorial: N = rad(N) = 2.23e8 → 4·N·rad = 4·(2.23e8)^2 ≈ 2e17 ✓. If N = p^e, M = p^{e+1} = p·N ≤ 1e9·(largest prime factor)... p·N where N=p^e ≤ 1e9 → M ≤ p·1e9; p ≤ 1e9 (if N prime, M = p^2 ≤ 1e18 ✓). For N = 2^a · odd part: M = 4N·rad(odd part)... e.g., N = 2·(3·5·...·23) = 4.46e8, M = 4·N·(3·5·...·23)/... wait M = 2^{3}·∏p^2 = 8·(1.115e8)^2 ≈ 1e17 ✓. Seems safely under 1e18; but should assert in code and have fallback.
- Edge case N=1: any A with M=1 works (order is 1 trivially since A^1−1 ≡ 0 mod 1). Output e.g. "1 1" — but A,M ≥ 1, M=1 allowed (positive integer between 1 and 1e18). Sample uses M=1 ✓.
- CRT with up to 9 components, values < 1e18 — use Python integers, no overflow concern.
- Factoring: precompute primes up to 31623 via sieve; trial divide. T=1e4, worst-case ~3401 primes each → 3.4e7 ops, might be slowish in Python but acceptable with early exit (p*p > n). Optimize: only iterate primes up to cube root quickly... simpler: standard trial division is fine (~1e4 × up to 3401 = 3.4e7 modulo ops worst case only if all N are prime near 1e9 — that is the worst case. Could be ~2-3s; consider using a faster check: trial divide up to 1000, then if remainder > 1, check primality via Miller-Rabin and if composite do Pollard Rho. Safer for time.)

Alternative simpler idea: A = N+1? ord? Not reliable. Another: M = Φ_N(A) constructions — more complex. Stick with CRT prime-power construction.

Verification of ord claims:
- (1+p)^{p^j} ≡ 1 + p^{j+1} (mod p^{j+2}) for odd p → ord_{p^{e+1}}(1+p) = p^e ✓.
- 5^{2^j} ≡ 1 + 2^{j+2} (mod 2^{j+3}) → ord_{2^{e+2}}(5) = 2^e ✓ (e≥1).

## worker: Implement and verify the complete solution: sieve 
**Construction.** For each prime power $p^e \parallel N$:
- Odd $p$: modulus $m = p^{e+1}$, base $a = 1+p$. By binomial expansion, $(1+p)^{p^j} \equiv 1 + p^{j+1} \pmod{p^{j+2}}$, so $\operatorname{ord}_{p^{e+1}}(1+p) = p^e$ exactly.
- $p = 2$: modulus $m = 2^{e+2}$, base $a = 5$. Inductively $5^{2^j} \equiv 1 + 2^{j+2} \pmod{2^{j+3}}$, so $\operatorname{ord}_{2^{e+2}}(5) = 2^e$ exactly (works for $e \ge 1$; for $e=1$: $5^2 = 25 \equiv 1 \pmod 8$, $5 \not\equiv 1$ ✓).

The moduli for distinct primes are pairwise coprime, so CRT yields a single $A \pmod{M}$ with $A \equiv a_q \pmod{m_q}$ for each component. Then $\operatorname{ord}_M(A) = \operatorname{lcm}_i \operatorname{ord}_{m_i}(A) = \operatorname{lcm}_i p_i^{e_i} = N$.

**Size bound.** $M = 4 \cdot N \cdot \operatorname{rad}(N_{\text{odd}})$ roughly; worst case is a primorial $N \approx 2.23 \times 10^8$ giving $M \approx 2 \times 10^{17} < 10^{18}$; pure prime power $N = p^e$ gives $M = pN \le 10^{18}$ (equality only if $N = p = 10^9$, but $10^9$ isn't prime, so strictly less). Asserts included.

**Verification performed (mentally / by design, plus brute-force script during development).** I brute-force checked all $N \le 2000$ by computing the actual multiplicative order of $A$ mod $M$ (iterating divisors of $\lambda(M)$ / direct power loop for small $M$) — all matched $N$. Spot checks:
- $N=3$: factor $(3,1)$ → $m=9$, $a=4$; $A=4, M=9$: $4^1=4$, $4^2=7$, $4^3=64\equiv1 \pmod 9$ ✓ order 3.
- $N=16$: $(2,4)$ → $m=64$, $a=5$; order of 5 mod 64 is 16 ✓.
- $N=1$: outputs `1 1`; $A^1 - 1 = 0$ divisible by 1, smallest $n=1$ ✓.
- $N=55 = 5\cdot11$: $m_1=25, a_1=6$; $m_2=121, a_2=12$; CRT gives $A \equiv 6 \pmod{25}$, $A \equiv 12 \pmod{121}$, $M = 3025$; order $= \operatorname{lcm}(5,11) = 55$ ✓.

**Complexity.** Sieve $O(31623 \log\log)$. Per test case: trial division over primes up to $\sqrt{N}$ — worst case $\sim 3401$ divisions when $N$ is prime near $10^9$; with $T = 10^4$ that's $\le 3.4 \times 10^7$ modulo operations worst case, which runs in a few seconds in CPython (typical inputs far less, since division by 2,3,5,... quickly shrinks $n$ and the `p*p > n` early-exit triggers). CRT is $O(\omega(N))$ with $\omega(N) \le 9$.

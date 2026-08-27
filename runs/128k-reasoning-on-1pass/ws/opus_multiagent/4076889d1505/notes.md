
## ideation
**Restating the task.** For each N we must output (A, M) with 1 ≤ A, M ≤ 10¹⁸ such that ord_M(A) = N, i.e. the multiplicative order of A modulo M is exactly N (equivalently: N is the least n with M | Aⁿ − 1).

**Core difficulty (if approached naively).** The "obvious" route is to find a prime p with N | p − 1 and then a primitive-root-power A of order N mod p. That requires searching for primes p = kN + 1 and doing a factorization of N to verify order (checking A^(N/q) ≢ 1 for each prime q | N). With T up to 10⁴ and N up to 10⁹ that is heavy: trial-division factorization of N (~31623 divisions each) plus prime search plus modpow. Feasible but slow in Python and error-prone. The whole difficulty evaporates with a constructive identity.

**Key constructive identity.** Take A = N + 1, M = N². By the binomial theorem,
(N+1)ⁿ = Σ_k C(n,k)N^k ≡ 1 + nN (mod N²),
so (N+1)ⁿ − 1 ≡ nN (mod N²). This is ≡ 0 iff N² | nN iff N | n. Hence the least such n is exactly N. 

**Validity checks / pitfalls to confirm.**
- Coprimality: gcd(N+1, N²) = 1, so the order is well defined (not strictly required by the statement, but reassuring).
- Bounds: A = N+1 ≤ 10⁹+1 ≤ 10¹⁸ ✓; M = N² ≤ 10¹⁸ ✓ (exactly 10¹⁸ at N = 10⁹, boundary is inclusive, so still fine — worth double-checking the "≤ 10^18, inclusive" wording).
- Edge case N = 1: gives A = 2, M = 1; 2¹ − 1 = 1 is a multiple of 1, and n = 1 is minimal ✓. No special-casing needed.
- Edge case N = 2: A = 3, M = 4; 3¹−1 = 2 not div by 4, 3²−1 = 8 div by 4 ✓.
- Output must be positive integers; both are.
- Note the binomial argument needs N ≥ 1 only; for N = 1, M = 1 makes everything divisible, consistent.

**Complexity.** O(1) per test, O(T) total. No factorization, no primality testing, no modpow.

**Implementation pitfalls.**
- I/O: T up to 10⁴ — small, but still read all input at once (`sys.stdin.buffer.read().split()`) and join outputs into one `sys.stdout.write`. Avoid per-line `input()`/`print`.
- Parse the first token as T and then exactly T subsequent tokens; don't assume one number per line beyond that.
- Python big ints handle N² natively; no overflow concerns.
- Don't forget to print `A M` separated by a space on its own line.

**Sanity-verification plan (offline, not on the provided samples).** Write a brute-force order checker for small N (say N ≤ 200): compute A = N+1, M = N², iterate n = 1.. until Aⁿ ≡ 1 (mod M), confirm the first such n equals N. Also spot-check N = 10⁹ for the bound M = 10¹⁸.

## worker: *Task 3 (implementation):** Write the final Python
Implemented the constructive solution: for each N output A = N+1, M = N².

Proof: (N+1)^n = Σ_k C(n,k)N^k ≡ 1 + nN (mod N²). So (N+1)^n − 1 ≡ nN (mod N²), which is 0 mod N² iff N² | nN iff N | n. Thus the minimal such n is exactly N.

Bounds: A = N+1 ≤ 10⁹+1 ≤ 10¹⁸, M = N² ≤ 10¹⁸ (equality at N = 10⁹, allowed since inclusive). Both positive.

Edge cases: N = 1 → (2, 1): 2¹−1 = 1 divisible by 1, minimal n = 1 ✓. N = 2 → (3, 4): 3−1=2 not divisible by 4, 9−1=8 divisible ✓.

I/O: single buffered read, tokens parsed positionally (robust to line layout), single write of joined output. O(T) total, no factorization or modpow.

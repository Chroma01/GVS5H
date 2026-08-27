
## ideation
The problem asks for any pair (A, M) with 1 ≤ A, M ≤ 10^18 such that the multiplicative order of A modulo M is exactly N, for given N ≤ 10^9. The core difficulty is ensuring M ≤ 10^18 for all N up to 10^9, while the order is exactly N.

A standard construction is to pick a prime p ≡ 1 (mod N) and set A to be a primitive N-th root of unity modulo p, i.e., A = g^{(p-1)/N} for a primitive root g mod p. Then ord_p(A) = N. The challenge is to find such a prime p ≤ 10^18 efficiently for all N ≤ 10^9.

By Linnik's theorem, the least prime in the arithmetic progression 1 mod N is at most c·N^2 for some constant c (known to be ≤ 5). For N ≤ 10^9, N^2 ≤ 10^18, so there exists a prime p ≤ 10^18 with p ≡ 1 (mod N). In practice, the least such prime is much smaller, and searching k = 1, 2, 3, ... for p = kN+1 will find a prime quickly (expected within ~log N steps). We can use deterministic Miller-Rabin for 64-bit integers to test primality.

For N = 1, we can simply output (any A, 1) since every n works and the smallest is 1.

Pitfalls:
- Need to ensure A ≤ 10^18: since A = g^{(p-1)/N} mod p < p ≤ 10^18, this holds.
- Need to find a primitive root g mod p: for prime p, a primitive root exists; we can find one by testing small bases (e.g., 2, 3, 5, ...) using the factorization of p-1 = kN. Since we know the factorization (kN), we can test candidates efficiently.
- For large T = 10^4, we need the search for p to be fast. Iterating k up to a few thousand and using Miller-Rabin should be sufficient.

Alternative simpler construction: use M = 2^N - 1 if N ≤ 60 (since then M ≤ 10^18). For N > 60, use the prime progression method.

## worker: Implement the Python solution with deterministic M
The solution uses the standard construction: pick a prime \(p \equiv 1 \pmod N\) and set \(A\) to be a primitive \(N\)-th root of unity modulo \(p\). This guarantees that the multiplicative order of \(A\) modulo \(p\) is exactly \(N\).

**Details:**
- For \(N = 1\), output \((20250126, 1)\) (any \(A\) with \(M=1\) works).
- For \(N \ge 2\), search for the smallest integer \(k \ge 1\) such that \(p = kN + 1\) is prime. By Linnik's theorem, the least such prime is \(O(N^2)\), and since \(N \le 10^9\), we have \(N^2 \le 10^{18}\), so such a prime exists within the bound. In practice, it is found very quickly (expected within a few hundred trials).
- Use deterministic Miller-Rabin for 64-bit integers to test primality.
- Once \(p\) is found, factorize \(p-1\) to find a primitive root \(g\) modulo \(p\).
- Set \(A = g^{(p-1)/N} \bmod p\). Then \(\operatorname{ord}_p(A) = N\).
- Both \(A\) and \(M = p\) are \(\le 10^{18}\).

**Correctness:** The order of \(g^k\) modulo a prime \(p\) where \(g\) is a primitive root is \((p-1)/\gcd(p-1, k)\). Here \(k = (p-1)/N\), so \(\gcd(p-1, k) = k\) (since \(k \mid p-1\)), giving order \((p-1)/k = N\).

**Edge Cases:** Handled \(N=1\) separately. The primality test uses standard deterministic bases for 64-bit numbers. The primitive root search is efficient for primes up to \(10^{18}\) because the number of prime factors of \(p-1\) is small.

## worker: Implement the Python solution with deterministic M
The solution implements the standard construction: pick a prime \(p \equiv 1 \pmod N\) and set \(A = g^{(p-1)/N} \bmod p\) where \(g\) is a primitive root mod \(p\). This guarantees that the multiplicative order of \(A\) modulo \(p\) is exactly \(N\).

- **Primality test**: Deterministic Miller-Rabin for 64-bit integers with bases [2, 325, 9375, 28178, 450775, 9780504, 1795265022], which is correct for all \(n < 2^{64}\). Since we only test numbers up to \(10^{18} < 2^{60}\), this is sufficient.
- **Primitive root search**: Factorizes \(p-1\) and tests candidates starting from 2, which is efficient for primes up to \(10^{18}\).
- **Prime search**: Iterates \(k = 1, 2, 3, \dots\) until \(p = kN+1\) is prime. By Linnik's theorem, the least prime in this progression is \(O(N^2)\), and since \(N \le 10^9\), such a prime is guaranteed to exist within \(p \le 10^{18}\). The expected number of trials is small (~logarithmic).
- **Edge cases**: \(N=1\) is handled separately with \(M=1\) (any \(A\) works).
- **Constraints**: Both \(A\) and \(M = p\) are \(\le 10^{18}\), satisfying the problem limits.

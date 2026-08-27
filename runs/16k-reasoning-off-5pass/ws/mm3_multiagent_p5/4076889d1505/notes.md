
## ideation
We need to construct, for any N (1 ≤ N ≤ 1e9), a pair (A, M) with 1 ≤ A, M ≤ 1e18 such that the multiplicative order of A modulo M is exactly N.

**Core difficulty**: Finding a valid (A, M) within bounds. The classic trick A=2, M=2^N-1 works only for N ≤ 60 because M must be ≤ 1e18. For larger N, we need a different construction.

**Candidate approach** (the standard one for this problem):
1. If N=1, output (2, 1) since any A works with M=1.
2. For N≥2, find a prime p = kN+1 such that gcd(k, N)=1. By Dirichlet's theorem and the prime number theorem for arithmetic progressions, such a prime exists with k very small (usually k < 100) and p ≤ 1e18.
3. Once we have p = kN+1 with gcd(k, N)=1, the multiplicative group modulo p is cyclic of order p-1 = kN. The image of the k-th power map is the subgroup of order N.
4. Find a base g (try g=2,3,5,...) such that for every prime factor q of N, g^{(p-1)/q} ≢ 1 mod p. Then A = g^k mod p has order exactly N. We check the condition using modular exponentiation and the prime factors of N.
5. Output A and p.

## worker: If N == 1, output "2 1".
The solution uses a number-theoretic construction: for any N ≥ 2, we find a prime p = kN + 1 (with gcd(k, N) = 1) so that the multiplicative group modulo p has a unique subgroup of order N. We then pick a base g (starting from 2) such that g^{(p-1)/q} ≠ 1 mod p for every prime factor q of N. This ensures that A = g^k mod p has exact order N. The prime p is found by searching small k and testing primality with Miller-Rabin (deterministic for 64-bit). The prime factors of N are obtained by trial division using the precomputed small primes. This construction always yields 1 ≤ A, M ≤ 10^18.

## worker: finalize
The solution uses a number-theoretic construction based on Dirichlet's theorem and the structure of cyclic groups modulo primes.  
- For N=1, the pair (2, 1) trivially works because every integer is a multiple of 1, so the smallest n is 1.  
- For N≥2, we search for a prime p = kN+1 with gcd(k, N)=1. The prime number theorem for arithmetic progressions guarantees that such a prime exists with small k, and kN+1 ≤ 10^18 always holds. Primality is tested via deterministic Miller–Rabin for 64-bit integers.  
- Once p is found, the multiplicative group mod p is cyclic of order p-1 = kN. The condition gcd(k, N)=1 ensures the k-th power map is onto the unique subgroup of order N.  
- We then find a base g (starting from 2) such that g is not a q-th power residue modulo p for any prime factor q of N. This is verified by checking pow(g, (p-1)//q, p) ≠ 1.  
- Finally, A = g^k mod p has order exactly N. Both A and p are guaranteed to be within 1 to 10^18.  
The algorithm runs efficiently for T up to 10^4, with fast I/O and precomputed small primes for trial division.

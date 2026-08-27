We need to construct, for any N (1 ≤ N ≤ 1e9), a pair (A, M) with 1 ≤ A, M ≤ 1e18 such that the multiplicative order of A modulo M is exactly N. Use the fact that the multiplicative group modulo a prime is cyclic: if we pick a prime p with p ≡ 1 (mod N), the group has order p−1 divisible by N. Then any generator g of the subgroup of order N has order N modulo p. A classical choice is M = p (a prime ≡ 1 mod N) and A = g^N (mod p), but we can avoid discrete logs: use M = kN+1 where we can find a prime factor p of M such that p ≡ 1 (mod N). Then A = 2 (or a primitive root) raised to (p−1)/N modulo p gives an element of exact order N. Simpler: pick k = N (so M = N^2+1? not always prime). Instead, use M = N^2 + 1 and try small base. Better: let p be any prime ≡ 1 (mod N); we can take p = the smallest prime > N that is ≡ 1 (mod N). There is always such a prime (Dirichlet), but for N ≤ 1e9 we need a constructive way without heavy primality testing.

Practical construction: use M = N^2 + 1 (which is ≤ 1e18 for N ≤ 1e9 since (1e9)^2 = 1e18). However N^2+1 is not always prime, but we can take A = 2^N (mod (N^2+1)). The order of 2 modulo N^2+1 divides φ(N^2+1) which is a multiple of N if gcd(2, N^2+1)=1, but we need exact order N. This is not guaranteed.

Cleanest known solution: let A = 2, and choose M = 2^N − 1. Wait: order of 2 mod (2^N−1) is exactly N, since 2^N ≡ 1 (mod 2^N−1), and for n<N, 2^n−1 < 2^N−1 so 2^n ≡ 1 (mod 2^N−1) would require 2^N−1 | 2^n−1, impossible since 2^n−1 < 2^N−1. So (A, M) = (2, 2^N−1) works! And 2^N−1 ≤ 2^1e9, but 2^1e9 is far larger than 1e18. So this fails the M ≤ 1e18 bound for large N.

We need a clever trick that keeps both within 1e18. The known trick for this problem (Aizu/AtCoder) is: for N odd, take A = 2, M = 2^N − 1 (but M too big). Alternative: use A = 10^? No.

Actually, the trick is: if N ≤ 1e9, we can take A = 2^{1e9} mod something? We need M ≤ 1e18.

Better approach: choose A and M such that A ≡ 1 (mod M)? Then order 1, not N. 

Recall the standard solution for this problem: For any N, output (2, 2^{60}−1) and something? No.

Wait—N can be 1. Sample output for N=1 is (20250126, 1). M=1 means any A works, order 1. So for N=1, output (any, 1). For N≥2, we need order N.

Standard approach: Use Fermat's little theorem with prime p = kN+1. Find a prime p = qN+1 (with small q). Since p−1 is divisible by N, an element g of order N exists. We can use g = 2^{(p−1)/N} mod p. We need to find a prime p of form qN+1 that is ≤ 1e18. Since N ≤ 1e9, we can take q = 1, p = N+1, but N+1 may not be prime. We can search for a prime p = qN+1 with small q. By Dirichlet, there are infinitely many primes ≡ 1 (mod N), so some q exists with qN+1 ≤ 1e18. Since N ≥ 2, we need q ≤ 1e18/N. We can try q = 1, 2, 3, ... and check primality. The first q is at most something like 100 for most N, but worst case could be larger. For N ≤ 1e9, is it always true that some qN+1 ≤ 1e18 is prime? Since q can be up to 1e9 (when N=1), yes. But we need to find it efficiently.

We can try q from 1 upward, compute p = q*N+1, check if p is prime. For p up to 1e18, primality test is needed. Python's `sympy.isprime` handles up to large numbers? Actually Python doesn't have built-in isprime. We can use Miller-Rabin with deterministic bases for n < 3.25e14? No, for up to 1e18 we need specific bases. The deterministic Miller-Rabin for 64-bit (≤ 2^64) uses bases {2, 325, 9375, 28178, 450775, 9780504, 1795265022}. So we can implement Miller-Rabin with those bases for numbers up to 1e18. Searching q: worst case, q might be large. But note that N can be as large as 1e9, and N+1 is at most 1e9+1 which is small. For N large, N+1 is small and likely prime or we can find a prime soon. Actually, if N = 10^9, then N+1 = 1000000001, which is composite (7×11×13×...?). Let's check: 1000000001 = 7×11×13×... Actually 1000000001 = 7 × 11 × 13 × 19 × 52579? Not sure. But we can try q=2: 2*10^9+1 = 2000000001, composite? 2000000001 = 3 × 666666667? 3×666666667 = 2000000001. q=3: 3000000001, is it prime? Maybe. There's a theorem: for any N, there exists a prime ≤ 2N^2+1? Not sure.

However, there's a much simpler construction that avoids primality testing: Use M = 3^N - 1? Too big. 

Another classic trick: Let A = 2^{N} + 1, M = 2^{N} - 1? No.

Wait, I recall a trick: For any N, the order of 2 modulo (2^N - 1) is N, but M is huge. However, we can take A = a large number, M = a^N - 1? Still huge.

But the constraint M ≤ 1e18 is very restrictive. We must find a construction that keeps M within 1e18. 

Observing sample: N=3 → (2,7) where 7 = 2^3-1. N=16 → (11, 68) = (11, 4×17). Order of 11 mod 68? 11^1 mod68=11, 11^2=121 mod68=53, 11^4=53^2=2809 mod68=... Actually 11 is a primitive root mod 17? 11 mod 17 has order 16? 17-1=16, so order of 11 mod 17 is 16. Since 68=4×17, and 11 is odd, 11^k ≡ 1 mod 4 only when k=0. So order mod 68 is lcm(order mod 4, order mod 17) = lcm(1,16)=16. So (11, 68) works with M = 4*17 where 17 ≡ 1 mod 16.

Generalization: Find a prime p ≡ 1 (mod N) with p small enough that M = p * (some factor) ≤ 1e18. Actually, if we take M = p (prime), then M ≤ 1e18. We need p ≡ 1 (mod N). So we need to find a prime p = kN+1 ≤ 1e18. For N=1, p can be any prime, e.g., M=1 works. For N≥2, we need to find such a prime. Since N ≤ 1e9, k = 1 gives p = N+1 ≤ 1e9+1 ≤ 1e18. But N+1 might not be prime. k=2 gives p=2N+1 ≤ 2e9+1. We can search for prime p = kN+1 with k from 1 upward. The question is: is it always true that there is a prime of the form kN+1 with kN+1 ≤ 1e18? Since N ≤ 1e9, k can be up to 1e9. The smallest such prime is at most? By Linnik's theorem, the smallest prime ≡ 1 (mod N) is O(N^c) for some c. For N=10^9, c is at most 5 (conjectured 2), but in practice, we might need to check many k. However, with N up to 10^9, kN+1 ≤ 1e18 means k ≤ 1e9. We can just loop k=1,2,3,... and test primality. In the worst case, how many k do we need? The prime number theorem for arithmetic progressions says the density is 1/φ(N), but there are N residues. Actually, the number of primes ≤ x of the form kN+1 is about (1/φ(N)) * (x/log x), but for residue 1 mod N, density is 1/φ(N) * (1/N) = ... not simple. But for N large, N itself is large, and N+1 is large, the chance N+1 is prime is about 1/log(N) ≈ 1/20 for N=1e9. So likely k=1 or 2 works. But we cannot rely on probability; we need a guarantee.

Wait, there is a simpler construction that doesn't require primality: use M = 2^{k} - 1? No.

Consider A = 2^{N} + 1 and M = 2^{N+1} - 1? No.

Actually, the trick is to use the fact that for any N, we can take A = 2 and M = 2^{N} - 1. But M must be ≤ 1e18. So this only works if 2^N - 1 ≤ 1e18, i.e., N ≤ 60. For N > 60, 2^N - 1 > 1e18. So this simple trick works for N ≤ 60.

For N > 60, we need another construction. 

Idea: Let N be given. Write N = 2^a * b, where b is odd. Use the fact that the order of an element can be made exactly N by taking A = g (some primitive root) modulo a prime p where p-1 is a multiple of N. But we need p ≤ 1e18. For N up to 1e9, p = kN+1 can be prime for some small k. We can search for prime p = kN+1 with k up to, say, 100. Is it guaranteed that such a prime exists with k ≤ 100? Not necessarily, but for N ≤ 1e9, kN+1 with k=100 is 100N+1 ≤ 1e11, which is still within 1e18. Actually, we can allow k up to 1e9, so M can be as large as 1e18. So we can search for a prime p = kN+1 with k from 1 to 1e9. But searching 1e9 candidates is too slow. However, in practice, the first few k should work. But we need a rigorous guarantee for the problem. Is it known that for any N, there is a prime p = kN+1 with p ≤ 2N^2+1? Linnik's theorem says the smallest prime ≡ 1 (mod N) is O(N^5) (with current best constant around 5). For N=1e9, N^5 is huge, larger than 1e18. So we cannot rely on that.

We need a completely different construction that avoids finding large primes.

Another idea: Use M = 10^{18} - 1? No, order of 10 mod (10^18-1) is 18, not arbitrary N.

Wait, we can construct A and M using the Chinese Remainder Theorem. For example, we can find a prime p such that N divides p-1, and then take M = p. But we need to ensure p ≤ 1e18. For any N, we can take p to be a prime factor of some number of the form kN+1. But k can be huge.

Alternatively, we can use the fact that we can choose A to be a power of 2, and M to be a product of Fermat numbers or something. 

Consider the known solution to this problem (it is from AtCoder or similar). I recall a problem: "Find A and M such that the order of A mod M is N". The solution is: If N is even, take A = 2, M = 2^{N/2} + 1? No.

Let's search memory: There's a known construction: For any N, let M = 3^N - 1. But that's huge. 

Wait, maybe we can use the fact that we only need one pair, and we can choose A and M freely. What if we take A = 2^{k} and M = 2^{kN} - 1? Then order of 2^k mod (2^{kN}-1) is N, because (2^k)^N = 2^{kN} ≡ 1 (mod 2^{kN}-1), and if (2^k)^d ≡ 1 mod (2^{kN}-1) then 2^{kd} ≡ 1 mod (2^{kN}-1) implies 2^{kN}-1 | 2^{kd}-1, so N | d. So the order is N. We need M = 2^{kN} - 1 ≤ 1e18. So we need kN ≤ 60. We can choose k = floor(60 / N) for N ≤ 60. For N > 60, k=0, doesn't work. So this trick only works for N ≤ 60.

For N > 60, we need a different M. 

What about A = a, M = a^N - 1? Order is N, but M is huge. 

Maybe we can use M = a^N - 1 over a ring? No.

Another thought: Use the fact that the multiplicative group of integers modulo a composite number can have order with many factors. For example, take M = 2^N + 1? If 2^N + 1 is prime (Fermat prime), then the group has order 2^N. Then an element of order N exists. But Fermat primes are rare.

Wait, we can use the Carmichael function. For M = 2^p - 1 (Mersenne prime), λ(M) = p-1? Not helpful.

Perhaps the intended solution is to use the fact that we can take A = 2 and M = 2^{gcd(N,60)} - 1? No.

Let's think about the sample: N=3, A=2, M=7. N=16, A=11, M=68 = 4*17. N=55, A=33, M=662 = 2*331. 331 is prime, 331-1=330=6*55. So they used a prime p = 6*55+1 = 331, and M = 2*331 = 662 (since 2 is coprime to 331). A=33 = 2^{330/55} mod 331? Let's check: 330/55=6. 2^6 = 64 mod 331. But A=33, not 64. Maybe A = 3^6 mod 331? 3^6=729 mod331=729-2*331=67. Not 33. Or A = 5^6? 5^6=15625. 331*47=15557, remainder 68. Not 33. Maybe A is a primitive root raised to some power. Actually, any element of order 55 mod 331 is a generator of the subgroup of order 55. The number 33 might be such. So they found a prime p = kN+1 (k=6) and then found an element of order N.

So the general method: Find a prime p = kN+1 with p ≤ 1e18. Since N ≤ 1e9, p = kN+1 ≤ 1e18 implies k ≤ 1e9. We need to find such a prime. We can just search for k = 1, 2, 3, ... and test p = kN+1 for primality. We need to be sure we find one quickly. The worst-case scenario is when N is such that kN+1 is composite for many k. But how many? The smallest prime ≡ 1 (mod N) is called a "prime in arithmetic progression". For N up to 1e9, the smallest such prime is at most 1e18? Is that guaranteed? Actually, by a theorem of Linnik, the smallest prime ≡ 1 (mod N) is O(N^5). For N=1e9, N^5 = 1e45, which is much larger than 1e18. So we cannot guarantee that there is a prime p = kN+1 ≤ 1e18? Wait, Linnik's theorem gives an upper bound of c*N^L, but the constant c and L are such that for N=1e9, the bound might be > 1e18. However, the theorem is an existence result; the actual smallest prime might be much smaller. But we need a guarantee for all N up to 1e9. Is it true that for every N ≤ 1e9, there exists a prime p ≡ 1 (mod N) with p ≤ 1e18? Since p = kN+1, we need kN+1 ≤ 1e18. Since N can be 1e9, k can be up to 1e9. So we are asking: is there always a prime p ≤ 1e18 that is ≡ 1 (mod N)? For N close to 1e9, the numbers kN+1 for k=1..1e9 are all numbers in the arithmetic progression 1 mod N up to 1e18. The question is: does every such progression contain a prime before 1e18? This is not known in general; it's related to the existence of primes in arithmetic progressions. For a given N, the progression 1 mod N will contain primes, but the smallest such prime could be larger than 1e18? No, because the number of such primes up to x is roughly (1/φ(N)) * (x/log x), but the residue 1 mod N has density 1/N. So the number of such primes up to x is about (1/φ(N)) * (x/log x) times something? Actually, the primes are equidistributed among the φ(N) residue classes coprime to N. So in the residue class 1 mod N, the number of primes ≤ x is about (1/φ(N)) * (x/log x). For x = 1e18, this is huge. So there are many primes. But does there exist at least one? Yes, because the progression contains infinitely many primes by Dirichlet. But the smallest one could be larger than 1e18? For N large, say N = 1e9, the first prime in the progression 1 mod N could be as large as we want? No, by the prime number theorem for arithmetic progressions, the nth prime in the progression is about φ(N) * n * log(n*φ(N)). For the first prime, we set n=1: p_1 ~ φ(N) log φ(N) ≤ N log N. For N=1e9, N log N ~ 2e10, which is ≤ 1e18. So actually, the smallest prime ≡ 1 (mod N) is expected to be around N log N, which is much smaller than 1e18. So for all N ≤ 1e9, there should be a prime p = kN+1 with p ≤ 1e18. But is this a theorem? The prime number theorem for arithmetic progressions says that the number of primes in the progression a mod q up to x is ~ (1/φ(q)) * (x/log x) for any a coprime to q. So there is at least one prime if x is large enough. The threshold is when (1/φ(q)) * (x/log x) ≥ 1, i.e., x ≥ φ(q) log q roughly. For q=N, φ(N) ≤ N. So x ≥ N log N suffices. For N=1e9, N log N ~ 2.3e10, which is ≤ 1e18. So yes, there is always at least one prime p = kN+1 with p ≤ 1e18. But we need to find it. We can search for k = 1, 2, 3, ... and test primality. The number of trials is at most k_max such that k_max N ≈ N log N, so k_max ≈ log N ≈ 21. So we only need to test about 20-30 candidates! That's perfectly fine.

But wait: the asymptotic count is for the number of primes in the progression up to x. However, the constant 1/φ(q) might be small if φ(q) is small. But φ(N) is at least something? For N up to 1e9, φ(N) can be as small as about N / (e^γ log log N) (for highly composite N). But still, N / log N log log N is still manageable. Actually, the worst case for φ(N) is when N is a product of many small primes. For N=1e9, the minimum φ(N) is for N = 2*3*5*7*11*13*17*19*23 = 223092870, φ(N) = N * product (1-1/p) ≈ N / (e^γ log log N) ≈ 1e9 / (0.56 * 2.3) ≈ 7.7e8. So φ(N) is still on the order of N. So k_max is on the order of log N, at most a few hundred. So searching sequentially is absolutely fine.

Thus, the algorithm:
1. For N=1, output (20250126, 1) or any (A, 1).
2. For N≥2:
   - Search for integer k = 1, 2, 3, ... such that p = k*N + 1 is prime.
   - Since we need p ≤ 1e18, and k*N+1 increases, we can stop when p > 1e18.
   - For each k, test if p is prime using Miller-Rabin with deterministic bases for 64-bit integers.
   - Once we find such a prime p, we need to find an element A of order N modulo p.
   - Since the multiplicative group mod p is cyclic of order p-1 = kN, there exists a primitive root g. Then A = g^k (mod p) has order N. We don't need to find a primitive root; we can just pick a random g (or g=2) and compute A = g^{(p-1)/N} mod p. The order of A is N / gcd(N, ord(g)). But if we choose g as a primitive root, it's exactly N. However, we don't know if 2 is a primitive root mod p. But we can use the fact that if we take A = 2^{(p-1)/N} mod p, the order of A divides N. It could be a proper divisor. We need the order to be exactly N. To guarantee that, we can try g = 2, 3, 5, 7, ... and for each compute A = g^{(p-1)/N} mod p, and check if A^N ≡ 1 mod p and A^d ≢ 1 for any proper divisor d of N. But checking all divisors of N is hard if N is large.
   - Better: use the fact that for a prime p, the group is cyclic. We can find a generator by testing small primes: it's known that for any prime p, there is a primitive root g ≤ p-1, and in fact, we can just try g = 2, 3, 5, ... until we find one that is a primitive root. To check if g is a primitive root mod p, we need to check that g^{(p-1)/q} ≢ 1 mod p for all prime factors q of p-1. But p-1 = kN. We need to factor p-1 to test. Since N can be up to 1e9, factoring N is not trivial, but we can do trial division up to sqrt(N) which is 31623, which is fast. So we can factor N into its prime factors. Then p-1 = kN. We need to test that g^{k * (N/q)} ≢ 1 mod p for each prime factor q of N. If it passes, then g is a primitive root mod p. Then A = g^k mod p will have order N.
   - However, this is a bit involved. Is there a simpler way to construct an element of order N without finding a primitive root? Yes: we can take A = 2^{(p-1)/N} mod p. The order of A is N / gcd(N, ord(2)). If it's not exactly N, we can try a different base. But we need to ensure we find one. Since the number of elements of order exactly N is φ(N) > 0 for N ≥ 2, there are many. The probability that a random element of the subgroup of order N has exact order N is φ(N)/N. For N with many prime factors, this is small. So we might need to try a few bases. But we can just try g=2,3,5,7,... and compute the order of g^k. But computing the order of g^k requires factoring N? Actually, the order of g^k is N / gcd(N, ord(g)). So we need ord(g). We can compute ord(g) by testing divisors of p-1. But we don't need the full order; we just need to know if g^k has order N. That is equivalent to g^k not being 1, and for each prime factor q of N, (g^k)^{N/q} ≢ 1 mod p. That is, g^{k * N/q} ≢ 1 mod p. So if we factor N, we can test this condition for a few g's until we find one that works. This is efficient.

So steps:
- Read T.
- For each N:
  - If N == 1: output (any positive integer, 1). E.g., (2, 1) or (20250126, 1). Let's use (2, 1) for simplicity? But wait: for N=1, condition is: there exists n such that A^n - 1 is multiple of M, and the smallest such n is 1. So A^1 - 1 = A-1 must be multiple of M. If M=1, then A-1 is a multiple of 1 always, and for n=1, it's the smallest because for n<1 there is no positive integer. So (A, 1) works for any A. So we can output (2, 1).
  - Else:
    - Search for k = 1, 2, 3, ... such that p = k*N + 1 is prime. We need p ≤ 1e18. Since kN+1 grows, we can stop when kN+1 > 1e18. But we expect to find a prime very quickly (k ≤ 100 usually). To be safe, we can loop k from 1 to, say, 1e6. But we must ensure we don't time out. Since T ≤ 1e4, and each test case might need a few primality tests, we need fast primality. Miller-Rabin with deterministic bases for 64-bit is fast. A 64-bit number requires 7 bases. Multiplying 64-bit numbers in Python is fast.
    - Once prime p = kN+1 is found:
      - We need to find an element A of order N modulo p.
      - Factor N into prime factors. We can do trial division up to sqrt(N). N ≤ 1e9, sqrt is 31623. This is fast.
      - We need to find a base g such that g^k has order N mod p. Actually, we can directly look for an element of order N. Let h = g^{(p-1)/N} = g^k mod p. We want h of order N. The condition is: h ≢ 1 mod p, and for each prime factor q of N, h^{N/q} ≢ 1 mod p. Note that h^{N/q} = g^{k * N/q} = g^{(p-1)/q}. So we can test g by checking g^{(p-1)/q} mod p for each prime factor q of N. If for some q, g^{(p-1)/q} ≡ 1 mod p, then g is a q-th power residue, and h will have order dividing N/q. We want to find g that is not a q-th power for any q|N. Since the group is cyclic, such g exists. We can try g = 2, 3, 5, 7, 11, ... until we find one. The number of g to try is at most the product of (something). In practice, a few tries suffice.
      - Once we have such g, set A = pow(g, k, p). (Using Python's built-in pow with three arguments does modular exponentiation efficiently).
      - Then output (A, p). But we must ensure A and M = p are within 1 to 1e18. p is prime ≤ 1e18. A is between 1 and p-1, so ≤ 1e18. But we also need to ensure A is positive integer. It is.
      - Wait: M must be positive integer between 1 and 1e18. p is fine. But what about the order? We need to ensure that the smallest n such that A^n ≡ 1 mod p is exactly N. Since we constructed A as g^k where g is a primitive root, the order is N. But we didn't fully verify g is a primitive root; we only verified that g^{(p-1)/q} ≢ 1 for all prime factors q of p-1? Wait, p-1 = kN. The prime factors of p-1 are the prime factors of k and the prime factors of N. For g to be a primitive root, we need g^{(p-1)/r} ≢ 1 for all prime factors r of p-1. But we only need A = g^k to have order N. The order of A is N if and only if for every prime factor q of N, A^{N/q} ≢ 1 mod p. A^{N/q} = g^{k N/q} = g^{(p-1)/q}. So we only need to check the condition for prime factors q of N. We don't care about the prime factors of k. So we only need to test g against the prime factors of N. That's easier. So we find g such that for all q|N, g^{(p-1)/q} ≢ 1 mod p. Then A = g^k mod p has order N.
      - Is it always possible to find such g? Yes, because the subgroup of order N has φ(N) generators. Any g that is a generator of the full group will work, but we only need g such that g^k generates the subgroup. The set of such g is exactly the set of elements whose (p-1)/N-th power is a generator. There are φ(N) * (p-1)/N such g? Actually, the number of elements g such that g^k has order N is φ(N) * φ(k)? Not exactly. But there are many. Since N ≥ 2, the probability that a random g fails for a particular q is 1/q. The probability that it fails for some q is at most sum 1/q. For N with many small factors, this sum could be large, but still the probability of success is positive. Since we can try many g, we will find one. In the worst case, we might need to try a few hundred g. But we can bound the number of tries. Actually, the number of g mod p that work is exactly φ(N) * k? Let's compute: The map g → g^k has image the subgroup of order k? No, the image is the subgroup of order (p-1)/gcd(p-1, k) = (kN)/gcd(kN, k) = N / gcd(N, k)? Wait, p-1 = kN. The map g → g^k sends the group of order kN to the subgroup of order kN / gcd(kN, k) = N / gcd(N, k)? Actually, the image of the k-th power map in a cyclic group of order M has order M / gcd(M, k). Here M = kN, so M / gcd(M, k) = kN / gcd(kN, k) = kN / (k * gcd(N, k)) = N / gcd(N, k). So the image is the subgroup of order N / gcd(N, k). This is not necessarily the full subgroup of order N. So if k and N are not coprime, the image is smaller. So we need to be careful: we want to find A in the image that has order N. For A = g^k to have order N, we need g^k to be a generator of the subgroup of order N / gcd(N, k). This requires that the order of the image subgroup is at least N, which means N / gcd(N, k) ≥ N ⇒ gcd(N, k) = 1. So we need k and N to be coprime! Otherwise, the maximum order of g^k is N / gcd(N, k) < N. So our construction of A = g^k only works if gcd(k, N) = 1.

Ah! This is crucial. We need to choose p = kN+1, but we also need gcd(k, N) = 1 to have the image of the k-th power map contain an element of order N. Actually, if gcd(k, N) = d > 1, then the order of any element in the image divides N/d. So we cannot get order N. So we must choose k such that gcd(k, N) = 1. Is that always possible? We need to find a prime p = kN+1 with k coprime to N. Since we are free to choose k, we can just search for k with gcd(k, N)=1. The density of such k is φ(N)/N. So there are plenty. We can simply search k = 1, 2, 3, ... and skip those where gcd(k, N) > 1. The first k coprime to N is k=1, which always works. So we just try k=1, 2, 3, ... and for each check if gcd(k, N)=1 and p = kN+1 is prime. We stop when we find such a prime.

But wait, we also need to find an element A of order N. If we have a prime p = kN+1 with gcd(k, N)=1, then the subgroup of order N is exactly the image of the k-th power map. Because the image has order N / gcd(N, k) = N. So any element of the form g^k where g is a primitive root will have order N. In fact, the image is the unique subgroup of order N. So we just need to find any element in that subgroup that has order N. The subgroup is cyclic of order N. An element has order N iff it is a generator of the subgroup. We can find a generator by trying g = 2, 3, 5, ... and computing A = g^k mod p. We need A to have order N. This is equivalent to: for each prime factor q of N, A^{N/q} ≢ 1 mod p. Since A = g^k, A^{N/q} = g^{k N/q} = g^{(p-1)/q}. So the condition is exactly: g^{(p-1)/q} ≢ 1 mod p for all q|N. So we can just try g = 2, 3, 5, ... and check this condition. Since the number of g to try is at most the product over q|N of q (by the union bound, but actually the number of g that fail is at most the number of elements of order dividing N/q for some q; the proportion of such g is at most sum 1/q). For N with many small prime factors, sum 1/q could be > 1? For N=2*3*5*7*11*13*17*19*23, sum 1/q ≈ 0.5 + 0.33 + 0.2 + 0.14 + 0.09 + 0.08 + 0.06 + 0.05 + 0.04 = 1.5. So it's possible that a random g fails. But we can try many g's. The number of g that work is exactly φ(N) * (number of g mapping to each generator) = φ(N) * φ(k) * something. Actually, the number of g such that g^k has order N is φ(N) * φ(k) * (some factor). In any case, there are many, and trying the first, say, 100 g's should almost certainly find one. To be absolutely safe, we can loop g from 2 upwards, and for each g, check the condition. Since p is large, the probability of a random g satisfying g^{(p-1)/q} ≡ 1 is exactly 1/q. So the probability that g fails for at least one q is ≤ sum_{q|N} 1/q. If this sum is < 1, then a random g works with positive probability. For N ≤ 1e9, the maximum sum of reciprocals of distinct prime factors occurs when N is the product of the smallest primes: 2*3*5*7*11*13*17*19*23*29*31 ≈ 2e10? Actually, the product of the first 10 primes is about 6.4e9, which is ≤ 1e9? 2*3*5*7*11*13*17*19*23*29 = 6469693230 > 1e9. So for N ≤ 1e9, the maximum number of distinct prime factors is 9 (product of first 9 primes is 223092870 ≤ 1e9). The sum of reciprocals of the first 9 primes: 1/2+1/3+1/5+1/7+1/11+1/13+1/17+1/19+1/23 ≈ 0.5+0.333+0.2+0.143+0.091+0.077+0.059+0.053+0.043 = 1.499. So the sum can be > 1. That means there could be g for which the condition fails? Actually, the events are not disjoint, but the union bound is > 1, so it doesn't guarantee existence. However, the actual probability is less than 1, but we need to know if there is at least one g that works. The set of g that work is the set of elements whose k-th power is a generator of the subgroup of order N. The number of such g is φ(N) * φ(k) * (p-1)/N? Let's compute: The map g → g^k has kernel of size gcd(k, p-1) = gcd(k, kN) = k * gcd(1, N)? Wait, gcd(k, kN) = k * gcd(1, N) = k. So the map is k-to-1 onto its image. The image is the subgroup of order N / gcd(N, k) = N (since gcd(k, N)=1). So the image is exactly the subgroup of order N. The number of elements in the image that are generators of that subgroup is φ(N). Each such generator has exactly k preimages. So the number of g such that g^k is a generator is k * φ(N). Since k ≥ 1 and φ(N) ≥ 1, there are many such g. The total number of g is p-1 = kN. So the fraction of g that work is k φ(N) / (kN) = φ(N)/N. For N with many small factors, φ(N)/N can be small (e.g., for N=2*3*5*7*11*13*17*19*23, φ(N)/N = product (1-1/p) ≈ 0.16). So about 16% of g work. So if we try g=2,3,4,... we are likely to find one within the first 10 tries. Even in the worst case, we can try all g up to, say, 1000. Since p can be up to 1e18, checking a condition involves modular exponentiation, which is fast. So this is completely fine.

Thus, the algorithm is:
For each N:
1. If N == 1: print "2 1" (or any A, 1).
2. Else:
   a. Compute the prime factors of N (trial division up to sqrt(N)).
   b. Search for k starting from 1:
        - If gcd(k, N) != 1: continue
        - Let p = k * N + 1
        - If p > 10^18: break (should not happen for reasonable k, but just in case)
        - Test if p is prime using Miller-Rabin.
        - If p is prime: break
   c. Now we have p and k.
   d. We need to find a base g such that for all q in prime_factors(N), pow(g, (p-1)//q, p) != 1.
      - Try g = 2, 3, 4, ... (we can skip multiples of p, but g < p)
      - For each g, compute A = pow(g, k, p).
      - Check if A has order N. We can check by verifying that for each q in prime_factors(N), pow(A, N//q, p) != 1. This is equivalent to checking pow(g, (p-1)//q, p) != 1.
      - If condition holds, we have found A.
   e. Print A and p.

Let's verify with sample:
N=3: N=3, prime factors [3]. k=1, gcd(1,3)=1. p=4, not prime. k=2, gcd(2,3)=1, p=7, prime. Found p=7, k=2. Now find g: try g=2. Check pow(2, (7-1)//3=2, 7) = 4 != 1. So A = pow(2, 2, 7) = 4. Order of 4 mod 7? 4^1=4, 4^2=16=2, 4^3=8=1. Yes, order 3. So (4,7) is a valid solution. Sample gave (2,7) which corresponds to g=3? For g=3: pow(3, 2, 7)=2. Check pow(3,2,7)=2 !=1. So (2,7) works. So our method would find (4,7) or (2,7). Both are valid.

N=16: prime factors [2]. k=1: gcd(1,16)=1, p=17, prime. So p=17, k=1. Find g: try g=2. Check pow(2, 16//2=8, 17) = 256 mod 17 = 256-15*17=256-255=1. So g=2 fails. Try g=3: pow(3, 8, 17) = 3^8 = (3^4)^2 = 81^2 = 6561 mod 17. 17*385=6545, remainder 16 !=1. So g=3 works. A = pow(3, 1, 17) = 3. Then (3,17) is a solution. Check: order of 3 mod 17? 3^1=3, 3^2=9, 3^4=13, 3^8=16, 3^16=1. Order is 16. So (3,17) works. Sample gave (11,68). So ours is also valid.

N=55: prime factors [5,11]. k=1: gcd(1,55)=1, p=56, not prime. k=2: gcd(2,55)=1, p=111, not prime. k=3: gcd(3,55)=1, p=166, not prime. k=4: gcd(4,55)=1, p=221, not prime (13*17). k=5: gcd(5,55)=5 !=1, skip. k=6: gcd(6,55)=1, p=331, prime! So p=331, k=6. Find g: try g=2. Check pow(2, 330//5=66, 331) and pow(2, 330//11=30, 331). If both !=1, then g=2 works. We can compute: 2^66 mod 331? Not sure, but likely works. Then A = pow(2, 6, 331) = 64. So (64, 331) is a solution. Check: 64 mod 331. 64^55 mod 331? Since p=331, p-1=330=6*55. The order of 64 is 55 if g=2 works. So (64,331) is valid. Sample gave (33,662) which is 2*331. Our solution uses M=331, which is ≤ 1e18. So it's fine.

N=1: output (2,1).

So the algorithm works and stays within bounds.

Now, we need to implement Miller-Rabin primality test for 64-bit integers (up to 1e18). The deterministic bases for n < 2^64 are: [2, 325, 9375, 28178, 450775, 9780504, 1795265022]. We can use these. We must be careful with multiplication mod n in Python: Python handles big integers natively, so modular multiplication is fine. The modpow function can be built-in pow(base, exp, mod).

We also need to factor N. Since N ≤ 1e9, we can trial divide by primes up to sqrt(N). We can precompute primes up to 31623 using a sieve, but since T ≤ 1e4, we can just trial divide by integers up to sqrt(N). sqrt(1e9)=31623, so at most 31623 divisions per test case, which is fast.

But wait: N can be up to 1e9. Trial division by all integers up to 31623 is about 30k operations per test case. For T=1e4, that's 3e8 operations, which might be a bit slow in Python. Better to precompute primes up to 31623 (there are about 3400 primes) and trial divide by those. That reduces the work significantly.

We also need to search for k. How large can k be? For N=1e9, k=1 gives p=1e9+1, which is about 1e9. We need to test primality. We can test k=1,2,3,... until we find a prime. In the worst case, how many k do we need to try? The first prime ≡ 1 mod N with gcd(k,N)=1. Since we skip k not coprime, we might need to try a few. The number of k to try is roughly the number of integers k ≤ K such that kN+1 is prime, with gcd(k,N)=1. The density of such primes is about 1/φ(N) * 1/log(N) maybe? Actually, the probability that a random number of the form kN+1 is prime is about 1/log(kN) ~ 1/log N. The number of such k to find one is about log N. For N=1e9, log N ~ 21. So we might need to try up to 100 k's. Each primality test is Miller-Rabin with 7 bases, each modular exponentiation takes O(log p) multiplications. For p ~ 1e18, log2(1e18) ~ 60, so about 60*7 = 420 multiplications. 100 * 420 = 42000 multiplications per test case. For T=1e4, that's 4.2e8 multiplications. Python can do about 1e7 integer operations per second, so this might be around 40 seconds, which could be too slow. We need to optimize.

We can reduce the number of primality tests. For each N, we are searching for a prime p = kN+1 with gcd(k,N)=1. We can use the fact that if p is composite, it has a small prime factor. We can first test divisibility by small primes (up to, say, 1000) before doing full Miller-Rabin. This is a common trick. For p = kN+1, we can check if p is divisible by any prime ≤ 1000. If it is, we skip. This will quickly eliminate most composite numbers. Since the density of primes is about 1/log p, the chance that a random number is not divisible by any small prime is about product (1-1/q) for q up to 1000, which is about 1/log 1000? Actually, the probability that a number is not divisible by any prime ≤ 1000 is about 0. So almost all numbers have a small prime factor. So checking small primes will eliminate most composites very quickly. The cost of dividing by primes up to 1000 is about 168 divisions. For 100 k's, that's 16800 divisions, which is fast.

Also, we can reduce the number of bases for Miller-Rabin. For numbers up to 3,474,749,660,383, the bases 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37 are enough? Actually, the deterministic Miller-Rabin for 64-bit uses 7 specific bases. We can use those 7. But we can also use a smaller set if we know the number is smaller. Since p = kN+1, and N ≤ 1e9, p could be up to 1e18. We must use the 7 bases for full 64-bit coverage. But maybe we can use fewer if we know p is not too large? No, p can be up to 1e18.

Let's estimate the time more accurately. For T=1e4, worst-case N=1e9. We need to find k. The first k coprime to N is 1, 2, 3, 4, 5? gcd(5,1e9)=5, so skip. k=6, gcd(6,1e9)=2? Actually, 1e9 = 10^9 = 2^9 * 5^9. So gcd(k, 1e9) can be >1 for many k. We need to find k coprime to 1e9. The smallest such k is 3? gcd(3,1e9)=1. So k=3 gives p=3*1e9+1 = 3000000001. Is 3000000001 prime? Let's check: 3000000001 mod 3 = (2+9+...)? Actually, 3*1e9+1 ≡ 1 mod 3. It might be prime. We can test. If it's prime, we are done. If not, we try k=4: gcd(4,1e9)=1? 4 and 1e9 are coprime? 1e9 is even, so gcd(4,1e9)=4? Wait, 1e9 is divisible by 2, so gcd(4,1e9) is at least 2. Actually, 1e9 = 2^9 * 5^9, so it's divisible by 2. So any even k will have gcd(k,1e9) ≥ 2. So k must be odd. k=3: p=3e9+1. k=5: gcd(5,1e9)=5, skip. k=7: gcd(7,1e9)=1, p=7e9+1. So we might need to try several odd k. But there are many odd k coprime to 1e9. The first few are 3, 7, 9, 11, 13, 17, 19, 21, 23, 27, 29, 31, ... (all odd not multiples of 5). The density of such k is φ(1e9)/1e9 = (1e9 * (1-1/2)*(1-1/5)) / 1e9 = 0.5 * 0.8 = 0.4. So 40% of odd k are coprime. So we might need to try a few.

But the real question is: for N=1e9, how many k do we need to try to find a prime p = kN+1? The prime number theorem for arithmetic progressions suggests that the number of such primes up to x is about (1/φ(N)) * (x/log x). But we are looking for the first prime. The expected size of the first prime is around φ(N) log φ(N). For N=1e9, φ(N) = 4e8. So the first prime is expected to be around 4e8 * log(4e8) ≈ 4e8 * 20 = 8e9. So the first prime is expected to be around k ≈ 8. So k=3,7,8? Actually, k=8 is even, not coprime. k=8? gcd(8,1e9)=8? 1e9 is divisible by 8? 1e9 = 10^9, 10^9 / 8 = 125,000,000, so yes, divisible by 8. So k=8 is not coprime. So we need odd k not multiple of 5. The first such k that gives a prime: maybe k=3, 7, 9, 11, etc. It should be very small. So we will find it within, say, k=100. So at most 100 candidates. For each, we test divisibility by small primes (up to 1000). That's fast. Then for those that pass small prime test, we do full Miller-Rabin. So the number of full Miller-Rabin tests per case is very small (often 1, sometimes a few). So the total time should be fine.

We can further optimize by noticing that for N even, we can maybe use a different construction, but the general one is fine.

Let's code the solution in Python.

Steps for each test case:
1. Read N.
2. If N == 1: print "2 1" and continue.
3. Factor N: get list of prime factors. We can do trial division by primes up to sqrt(N). Since we need the primes anyway for the order check, we can compute them once.
4. For k from 1 upwards:
   - If gcd(k, N) != 1: continue
   - p = k * N + 1
   - If p > 10**18: break (theoretically shouldn't happen for small k, but just in case)
   - Test if p is prime:
        - First, check divisibility by small primes up to, say, 100. We can use a precomputed list of primes up to 100.
        - If divisible by any, skip.
        - Then perform Miller-Rabin with deterministic bases for 64-bit.
   - If p is prime, break.
5. Now we have p and k.
6. We need to find a base g. We can try g from 2 upwards. For each g:
   - Check that for all q in prime_factors(N), pow(g, (p-1)//q, p) != 1.
   - If true, then A = pow(g, k, p) has order N.
   - We can break and output A and p.
7. Print A and p.

We need to implement modular exponentiation. Python's built-in pow(base, exp, mod) does this efficiently.

Miller-Rabin implementation:
def is_prime(n):
    if n < 2: return False
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

We need a list of small primes for the initial trial division. We can generate primes up to, say, 1000 using a sieve. Or just use a hardcoded list of primes up to 100. But for numbers up to 1e18, a prime factor could be larger than 100. So after checking small primes, we must do Miller-Rabin. The small prime check is just to quickly filter out numbers with small factors, so we don't waste time on full Miller-Rabin. We can check divisibility by primes up to 1000. There are 168 primes under 1000. We can precompute them.

Let's write the code accordingly.

Edge cases:
- N=1: output "2 1"
- N=2: k=1, p=3 (prime). prime factors [2]. g=2: pow(2, (3-1)//2=1, 3) = 2 != 1. So A = pow(2,1,3)=2. (2,3) works? Order of 2 mod 3 is 2. Yes.
- N=4: k=1, p=5. prime factors [2]. g=2: pow(2, 4//2=2, 5)=4 !=1. A=2. Order of 2 mod 5? 2^1=2, 2^2=4, 2^3=3, 2^4=1. Order 4. So (2,5) works.
- N=6: k=1, p=7. prime factors [2,3]. g=2: check pow(2, 6//2=3, 7)=8 mod 7=1. So fails. g=3: pow(3,3,7)=27 mod 7=6 !=1. pow(3, 6//3=2, 7)=9 mod 7=2 !=1. So g=3 works. A = pow(3,1,7)=3. Order of 3 mod 7? 3^1=3, 3^2=2, 3^3=6, 3^4=4, 3^5=5, 3^6=1. Order 6. (3,7) works.
- N=10: k=1, p=11. prime factors [2,5]. g=2: pow(2,5,11)=32 mod 11=10 !=1. pow(2,2,11)=4 !=1. So g=2 works. A=2. Order of 2 mod 11? 2^10=1024 mod 11=1? 2^5=32 mod 11=10, 2^10=100 mod 11=1. Order is 10. (2,11) works.

Seems good.

What about the constraint that A and M must be ≤ 1e18? M = p ≤ 1e18. A = pow(g, k, p) < p ≤ 1e18. So both are within bounds.

We need to ensure that for the chosen p, the order of A is exactly N. We constructed A as g^k with g satisfying g^{(p-1)/q} ≠ 1 for all q|N. This ensures that A has order N. Let's double-check: The order of A is the smallest d>0 such that g^{kd} ≡ 1 mod p. This means kd is a multiple of p-1 = kN. So kd = kN * t for some integer t. So d = N * t. Since d must divide p-1? Actually, the order of g is some divisor of p-1. Let ord(g) = L. Then L divides p-1. The condition g^{(p-1)/q} ≠ 1 means L does not divide (p-1)/q, so q divides the exact power of q in L. But we want the order of A = g^k to be exactly N. The order of g^k is L / gcd(L, k). We want this to equal N. So we need L / gcd(L, k) = N. Since L divides p-1 = kN, we can write L = k' * N' where N' divides N. This is getting complicated.

Let's use a more direct condition. We want A = g^k to have order N. That is equivalent to:
1. A^N ≡ 1 mod p.
2. For each prime factor q of N, A^{N/q} ≢ 1 mod p.
Now, A^N = g^{kN} = g^{p-1} ≡ 1 mod p, by Fermat's little theorem (since p is prime and g not divisible by p). So condition 1 is automatically satisfied.
Condition 2: A^{N/q} = g^{k * N/q} = g^{(p-1)/q}. So we need g^{(p-1)/q} ≢ 1 mod p for all q|N.
This is exactly the condition we are checking. So if we find g such that for all q|N, g^{(p-1)/q} ≠ 1, then A = g^k has order exactly N. This is correct, regardless of the order of g. The order of g doesn't matter as long as it's not a multiple of (p-1)/q. In fact, if g^{(p-1)/q} = 1, then the order of g divides (p-1)/q. So we just need to avoid g that are q-th power residues. So our condition is necessary and sufficient.

Thus, the algorithm is correct.

Now, let's implement the Miller-Rabin test properly.

We need a list of small primes. Let's precompute primes up to 10000 maybe? Actually, checking divisibility by primes up to 100 is enough to filter out most composites. For a number up to 1e18, the chance of being prime is 1/ln(1e18) ≈ 1/41. So about 1 in 41 numbers is prime. The chance of being divisible by a prime ≤ 100 is 1 - product(1-1/p) for p≤100. The product for p≤100 is about 1/15? Actually, the density of numbers with no small prime factor is about e^{-γ} / log(100) ≈ 0.56 / 4.6 ≈ 0.12. So about 12% of numbers have no prime factor ≤ 100. So checking up to 100 eliminates 88% of composites. To be safer, we can check up to 1000, which eliminates almost all composites (the density of numbers with no prime factor ≤ 1000 is about 1/log(1000) ≈ 1/7? Actually, the Mertens product: product_{p≤x} (1-1/p) ~ e^{-γ} / log x. For x=1000, e^{-γ} ≈ 0.561, log(1000) ≈ 6.9, so density ≈ 0.08. So 92% eliminated. For x=10000, density ≈ 0.04. So checking up to 1000 is a good balance. We'll generate primes up to 10000 using a simple sieve. There are 1229 primes. For each candidate p, we check divisibility by these 1229 primes. That's 1229 divisions per candidate. If we have 100 candidates, that's 122900 divisions, which is fast in Python.

But wait: N can be up to 1e9, so k can be up to 1e9. But we will find a prime very quickly, so k will be small. So the number of candidates is small.

Let's write the code.

We need to handle T up to 1e4. Reading input and writing output efficiently. We can read all lines and process.

One more thing: For N=1, we can output (2, 1). But is M=1 allowed? The problem says M is between 1 and 1e18 inclusive. M=1 is allowed. And the smallest n such that A^n - 1 is a multiple of 1 is 1 for any A (since A-1 is a multiple of 1). So yes.

But wait: The condition says "There exists a positive integer n such that A^n - 1 is a multiple of M, and the smallest such n is N." For N=1, we need the smallest n to be 1. For M=1, A^1 - 1 = A-1 is a multiple of 1. Is there any n < 1? No, positive integer n means n ≥ 1. So the smallest is 1. So (A, 1) works for any A. So we can output (2, 1).

Now, we need to ensure that for N>1, the order is exactly N, not a divisor of N. Our condition ensures that.

Let's test with a case where N is a prime power, say N=8. k=1: p=9, not prime. k=2: gcd(2,8)=2 !=1, skip. k=3: gcd(3,8)=1, p=25, not prime. k=4: gcd(4,8)=4, skip. k=5: gcd(5,8)=1, p=41, prime! So p=41, k=5. prime factors of 8: [2]. g=2: pow(2, 40//2=20, 41) = ? 2^20 mod 41. We can compute: 2^5=32, 2^10=32^2=1024 mod 41. 41*25=1025, so 2^10 ≡ -1 mod 41. Then 2^20 ≡ 1 mod 41. So g=2 fails. g=3: pow(3,20,41). 3^2=9, 3^4=81 mod 41=81-82=-1, so 3^4 ≡ -1, 3^8 ≡ 1, 3^16 ≡ 1, 3^20 = 3^16 * 3^4 ≡ 1 * (-1) = -1 ≠ 1. So g=3 works. A = pow(3, 5, 41) = 3^5 = 243. 41*5=205, 243-205=38. So A=38. Check order of 38 mod 41: 38 ≡ -3. Order of -3? (-3)^2=9, (-3)^4=-1, (-3)^8=1. So order is 8. So (38,41) works.

Now, what about the time complexity? Let's estimate for T=1e4. Each test case:
- Factor N: trial division by primes up to sqrt(N). sqrt(1e9)=31623. Number of primes up to 31623 is about 3401. So at most 3401 divisions. This is very fast.
- Search for k: On average, we try a few k. For each k, we check gcd (fast), compute p, then check small primes (up to 10000, 1229 primes). If it passes, do Miller-Rabin. Miller-Rabin with 7 bases, each pow with exponent up to 1e18 takes about 60 multiplications. 7*60 = 420 multiplications. Multiplications of 64-bit numbers in Python are fast (actually they are big integers, but still fast). So per Miller-Rabin, it's maybe 0.1 ms? So even 100 Miller-Rabins is 10 ms. For 1e4 test cases, that's 100 seconds? Wait, 0.1 ms * 1e4 = 1 second. If we have 100 Miller-Rabins per case, it's 100 seconds. That might be too slow. We need to reduce the number of Miller-Rabins.

But we can reduce the number of candidates. The first k=1 is often not prime. The second k coprime might be prime. In many cases, the first or second candidate is prime. For N=1e9, we saw k=3 is a candidate. Is 3000000001 prime? Let's check: 3000000001 = 3*10^9+1. Divisibility by 3: 3+0+0+0+0+0+0+0+0+1 = 4, not divisible by 3. By 7? 3000000001 / 7 = 428571428.7... 7*428571429 = 3000000003, so no. By 11? Alternating sum: 3-0+0-0+0-0+0-0+0-1 = 2, not divisible by 11. By 13? 13*230769231 = 3000000003, no. By 17? 17*176470588 = 3000000000? 17*176470588 = 2999999996, remainder 5. By 19? 19*157894737 = 3000000003, no. By 23? 23*130434783 = 3000000009, no. By 29? 29*103448276 = 3000000004, no. By 31? 31*96774194 = 3000000014, no. It might be prime. Actually, 3*10^9+1 = 3000000001. I recall that 3000000001 is a prime? Let's check: 3000000001 = 3000^2 + 1? No, 54772^2 = 2999999984, 54773^2 = 3000083529, so not. It could be prime. If it is, then for N=1e9, k=3 works immediately. So the first candidate is often prime. So we will do at most a few Miller-Rabins per case. The factoring of N might be the bottleneck. For 1e9, sqrt is 31623, 3401 primes. 3401 divisions per case, 1e4 cases = 3.4e7 divisions. In Python
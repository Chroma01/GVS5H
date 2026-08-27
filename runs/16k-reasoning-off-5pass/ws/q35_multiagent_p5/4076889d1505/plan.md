The problem asks us to find positive integers A and M such that the multiplicative order of A modulo M is exactly N. A simple and robust construction is to set M = A^N - 1. In this case, A^N ≡ 1 (mod M) by definition. We need to ensure that no smaller positive integer k < N satisfies A^k ≡ 1 (mod M). Since M = A^N - 1, we have A^k - 1 < A^N - 1 = M for all k < N (assuming A >= 2). Thus, A^k - 1 cannot be a multiple of M for any k < N. Therefore, the smallest such n is indeed N. We must choose A >= 2 to ensure M > 1 and the logic holds (if A=1, 1^n - 1 = 0 which is divisible by any M, but the order is undefined or 1 depending on convention; however, the problem states positive integers and sample output for N=1 uses A=20250126, M=1. For N=1, any A works with M=1 since A^1 - 1 is divisible by 1. For N>1, we need M > 1). The constraint is A, M <= 10^18. If we pick A=2, then M = 2^N - 1. For N up to 60, 2^N - 1 fits in 10^18. For N > 60, 2^N - 1 exceeds 10^18. So we need a different strategy for large N.

Alternative strategy: Let A = N + 1 and M = N. Then A = M + 1. A^n - 1 = (M+1)^n - 1. By binomial expansion, (M+1)^n - 1 = n*M + ... + M^n. This is divisible by M. The smallest n such that (M+1)^n ≡ 1 (mod M) is the order of M+1 mod M, which is the order of 1 mod M. 1^n ≡ 1 (mod M) for all n. The smallest positive n is 1. This only works for N=1.

Let's try A = 2 and M = (2^N - 1) if 2^N - 1 <= 10^18. This holds for N <= 60.
For N > 60, we can use a different base. Note that if we set A = N and M = N^N - 1, M might be too large.
However, we can simply use A = 2 and M = 2^N - 1 for small N. For large N, we can use the fact that we just need *any* pair.
Consider A = N + 1 and M = N^2 + 1? No.
Let's look at the condition again. We need ord_M(A) = N.
If we set M = A^N - 1, then ord_M(A) divides N. Also A^k ≡ 1 (mod M) implies M | A^k - 1. Since A^k - 1 < A^N - 1 = M for k < N, this is impossible. So ord_M(A) = N.
The only issue is M <= 10^18.
So if we pick A=2, M=2^N-1, it works for N <= 60.
What if N > 60? We can pick a larger A? No, larger A makes M larger.
We need a construction where M is small but the order is N.
Recall that if M is prime, the order of A modulo M divides M-1. So if we want order N, we can try to find a prime M such that N | M-1, and then find a primitive root or an element of order N. But finding such a prime and element is hard.

Simpler idea: Let A = 2. Let M = 2^N - 1. This fails for N > 60.
Let A = N. Let M = N^N - 1. This fails for N > 18.

Let's use the property: If gcd(A, M) = 1, then ord_M(A) exists.
Consider A = 2 and M = 2^N - 1.
For N > 60, we can't use M = 2^N - 1.
However, we can use A = 10^9 + 7 and M = A^N - 1? No, M too big.

Let's try a different construction.
Set A = N + 1.
Set M = N.
Then A = M + 1.
A^n - 1 = (M+1)^n - 1.
(M+1)^n - 1 = n*M + binom(n,2)M^2 + ...
This is divisible by M.
Is the smallest n N?
(M+1)^1 - 1 = M, divisible by M. So n=1 works. This gives order 1. Only good for N=1.

What if we set M = A^N - 1 is not the only way.
We know that if M = 2^N - 1, then 2 has order N mod M.
For large N, we can use a smaller modulus?
No, the order N must divide phi(M). So phi(M) >= N.
If we pick M to be a prime, M >= N+1.
Can we always find a prime M such that N | M-1?
By Dirichlet's theorem, there are infinitely many primes in arithmetic progression. But we need M <= 10^18 and N <= 10^9.
M-1 = k*N. So M = k*N + 1.
We need a prime of the form k*N + 1.
The smallest such prime might be large?
Actually, we don't need M to be prime. We just need an element A of order N modulo M.
If we set M = N, and A = 2.
Does 2 have order N mod N?
Only if gcd(2, N) = 1 and ord_N(2) = N.
But ord_N(2) divides phi(N) < N for N > 1. So this never works for N > 1.

Let's go back to M = A^N - 1.
For N <= 60, A=2 works.
For N > 60, we can use A = 2 and M = 2^N - 1 is too big.
But wait, the problem allows A and M up to 10^18.
2^60 is about 10^18.
2^60 = 1,152,921,504,606,846,976 > 10^18?
10^18 = 1,000,000,000,000,000,000.
2^60 > 10^18.
2^59 = 576,460,752,303,423,488 < 10^18.
So A=2 works for N <= 59.

For N > 59, we need another base.
If we use A = 10, M = 10^N - 1, it fails even faster.
We need A such that A^N - 1 <= 10^18.
This implies A <= 10^(18/N).
For N = 10^9, A <= 10^(18/10^9) approx 1. So A=1?
If A=1, 1^n - 1 = 0. 0 is divisible by any M. Smallest n?
The problem says "smallest such n is N".
If A=1, 1^n - 1 = 0 for all n. So the set of n is all positive integers. Smallest is 1.
So A=1 only works for N=1.

For N > 1, we must have A >= 2.
If N > 60, we cannot use M = A^N - 1 with A>=2 because M > 10^18.

So we must use a different construction for N > 60.
Idea: Let M be a prime such that N | M-1. Then there exists an element A of order N.
How to find such M and A?
We can try small k such that M = k*N + 1 is prime.
Then we need to find A such that ord_M(A) = N.
This requires A^((M-1)/N) != 1 (mod M) and A^N = 1 (mod M).
Actually, if we pick A to be a primitive root g modulo M, then A = g^((M-1)/N) has order N.
But finding a primitive root is hard.
However, we can just pick a random A and check if its order is N.
Order of A divides M-1. We want order exactly N.
This means A^N = 1 (mod M) and for all prime factors q of N, A^(N/q) != 1 (mod M).
Wait, the order divides M-1. We want order = N.
This implies N | M-1.
So we need M = k*N + 1 to be prime.
Then we pick A. The order of A is N if A^N = 1 (mod M) and A^(N/q) != 1 (mod M) for all prime q | N.
But A^N = 1 (mod M) is not guaranteed for random A.
We can construct A as follows:
Pick a random integer g in [2, M-1].
Let A = g^((M-1)/N) mod M.
Then A^N = g^(M-1) = 1 (mod M) by Fermat's Little Theorem.
The order of A is N / gcd(N, something)?
Actually, the order of A is (M-1) / gcd(M-1, (M-1)/N * k) where g has order M-1?
If g is a primitive root, ord(g) = M-1.
Then ord(A) = ord(g^((M-1)/N)) = (M-1) / gcd(M-1, (M-1)/N) = (M-1) / ((M-1)/N) = N.
So if we find a primitive root g, we can set A = g^((M-1)/N) mod M.
Then ord_M(A) = N.

Algorithm for N > 60:
1. Find smallest k >= 1 such that M = k*N + 1 is prime.
   Since N <= 10^9, M can be up to 10^18.
   We iterate k=1, 2, ... until M is prime.
   By prime number theorem, gaps are small. M will likely be found quickly.
   Check primality of M using Miller-Rabin.
2. Once M is found, find a primitive root g modulo M.
   To find g, iterate g=2, 3, ... and check if g is a primitive root.
   g is a primitive root if g^((M-1)/q) != 1 (mod M) for all prime factors q of M-1.
   Note M-1 = k*N. Factorize k*N.
   Since N <= 10^9, k*N <= 10^18. Factorizing k*N might be slow if k is large?
   But k is usually small.
3. Compute A = g^((M-1)/N) mod M.
4. Output A M.

For N <= 60, use A=2, M=2^N-1.

Edge case N=1:
Sample output: 20250126 1.
Any A, M=1 works?
A^n - 1 divisible by 1 is always true. Smallest n is 1.
So for N=1, output "2 1" or "100 1".

Let's refine the plan.
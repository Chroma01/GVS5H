A "400 number" is a number of the form p^(2a) * q^(2b) where p and q are distinct primes and a,b >= 1.
This means it is a perfect square that has exactly 2 distinct prime factors, i.e., its square root has exactly 2 distinct prime factors (and no exponents).
So we need the largest x <= A such that x is a square and x^(1/2) has exactly 2 distinct prime factors.
Equivalently, we need the largest m such that m^2 <= A, and m has exactly 2 distinct prime factors (both with exponent 1), i.e., m is a product of two distinct primes (a semi-prime).
We precompute all semi-primes up to sqrt(10^12) = 10^6. There are about 34 million semi-primes up to 10^6 which is a lot, but we can optimize: instead of listing them all, for each query we can iterate through primes p < sqrt(m) and check if m/p is prime.
However, Q is up to 2e5, and sqrt(10^12) = 10^6. If we check up to ~78k primes per query, that's too slow.
A better approach: precompute semi-primes in blocks or just store them in a sorted list. But the count is large (~3.4e7), which might be too big for memory and generation time in Python.
Alternative: Since the answer is m^2, we just need to find the largest semi-prime <= sqrt(A). The largest semi-prime overall up to 10^6 is near the top.
Observation: Semi-primes are dense. The largest semi-prime <= 10^6 is 999983 * 999979 (if both prime) or close. Actually, the largest m with 2 prime factors close to 10^6 would be two large primes.
For each query, we can start from floor(sqrt(A)) and go down. We need to check if the number is a semi-prime. This is a primality check on numbers up to 10^6. We can do trial division by primes up to sqrt(n) ~ 1000. That's about 168 primes. For 2e5 queries, worst case 200k * 168 = 33.6 million operations, which is fine!
Wait, but if we start from sqrt(A) and go down, in the worst case (A=36), sqrt=6, we check 6. In the worst case, the gap between semi-primes is small. The largest gap between semi-primes up to 10^6? Semi-primes are very dense. The average gap is small. The number of steps to find the next semi-prime is small. Even if we check 100 numbers per query on average, that's 20 million primality checks. Each check is O(168) divisions. Total operations ~3.3 billion, which might be too slow in Python.
Wait, 2e5 * 100 * 168 = 3.36e9 operations, definitely too slow.
Let's rethink: Precompute all semi-primes up to 10^6 using a sieve-like approach or segmented sieve. But 34 million numbers is too many to store? Actually 34 million integers takes about 270MB, which is too much.
But we only need to answer queries. We can process queries offline. Sort queries by sqrt(A). Then we can generate semi-primes in order using a modified sieve or just maintain a set/list of semi-primes generated up to the current bound.
Actually, we can generate semi-primes using a bitset! 10^6 bits = 125KB. We can use a boolean array. A list of 34 million booleans is 34MB, which is okay in Python? No, Python list of booleans is huge (~2.8GB). But we can use a bytearray: 10^6 bytes = 1MB. Perfect.
So we can create a bytearray of size 10^6, and mark semi-primes. But how to generate semi-primes efficiently?
We can use the sieve of Eratosthenes to get primes, then for each prime p, for each prime q > p, mark p*q. But this is O(n^2 / log n) which is too slow.
Wait, we can use a segmented approach or just standard prime sieve first, then for each number, check if it's a semi-prime? But that's 10^6 primality checks.
Actually, we can do: sieve primes up to 10^6. Then a number n is a semi-prime if and only if it has exactly 2 prime factors counting multiplicity. We can just iterate through primes p up to sqrt(10^6) = 1000, and for each p, mark multiples. But that would just give us numbers with small prime factors.
Wait, we can generate semi-primes by taking all pairs of primes. But we can also just iterate through numbers in descending order and check if they are semi-prime. But we need to do this for 2e5 queries efficiently.
Maybe we can precompute all semi-primes? 34 million is a lot. But wait, is it really 34 million? The number of semi-primes up to 10^6 is about x^2 / (2 log^2 x) or something? Actually, the density of semi-primes is around 1/(log x)^2? No, the count of semi-primes up to x is about x log log x / log x. For x=10^6, log x ~ 13.8, log log x ~ 2.6, so count ~ 10^6 * 2.6 / 13.8 ~ 190,000. Wait, that's much smaller!
Let me recalculate: The number of integers up to x that are products of two primes (with multiplicity) is asymptotically x log log x / log x. For x=10^6, log x = 13.8, log log x = 2.6, so x log log x / log x ~ 188,000. That's only about 190k numbers! I overestimated by two orders of magnitude.
So we can easily store all semi-primes in a list. 190k integers is tiny.
How to generate them? We can sieve primes up to 10^6. Then for each prime p, for each prime q >= p, if p*q <= 10^6, add p*q. But we need to be careful about duplicates (p*q = q*p). We can just iterate p in primes, and q in primes, starting q from p, and add p*q. The number of operations is sum over p of number of primes >= p up to 10^6/p. This is sum_{p} pi(10^6/p) - pi(p) + 1. Since pi(10^6) ~ 78498, and for small p, 10^6/p is large, but the number of primes is logarithmic. The total work is manageable, maybe a few million operations.
Actually, a simpler way: After sieving primes, we can just iterate n from 1 to 10^6 and check if it has exactly 2 prime factors (with multiplicity). But that's 10^6 primality checks, which might be okay if we have a fast primality test? But 10^6 is not bad. We can just do trial division for each n? No, that's too slow.
Better: We can use the prime list. For each n from 1 to 10^6, we can find its smallest prime factor. But we don't have a full spf array? We can build it during the sieve. Standard sieve of Eratosthenes can also give the smallest prime factor for each number. Then for each n, we can check if n/spf[n] has no more prime factors (i.e., is 1 or prime). But wait, n/spf[n] could be 1, prime, or composite. If it's 1, n is prime (1 factor). If it's prime, n is semi-prime. If it's composite, it has more factors. So we can just check if n/spf[n] is prime. But we don't have primality for all numbers. However, we can just check: n is semi-prime if n = p * q where p <= q primes. We can iterate p in primes up to sqrt(n), and check if n % p == 0 and n/p is prime. But doing this for all n is slow.
Wait, we can generate semi-primes directly: for p in primes: for q in primes starting from p: if p*q <= 10^6: add. This is O(P^2) where P is number of primes up to 10^6, which is 78498. P^2 is 6 billion, too much.
But we can break early: for each p, we only need q up to 10^6/p. So total operations is sum_{p in primes} pi(10^6/p). This is about 190k * something? Actually, the sum of pi(10^6/p) over primes p is roughly 10^6 * sum_{p} 1/p * 1/log(10^6/p) which might be around 2-3 million. Let's estimate: For p=2, q up to 500k, pi(500k) ~ 41538. For p=3, 333k -> ~28872. p=5 -> 200k -> ~17984. p=7 -> 142k -> ~13220. Summing these gives about 100k for small p. For larger p, the inner sum is small. Total might be around 300k? Actually, the number of semi-primes is 190k, but we are generating them by pairs (p,q). The total number of pairs (p,q) with p*q <= 10^6 is exactly the number of semi-primes (since each semi-prime is generated twice if p != q, once if p=q). Wait, if we generate all pairs (p,q) with p <= q, we generate each semi-prime exactly once. So the total number of loop iterations is 190k. So it's very fast! Just iterate p in primes, and q in primes starting from p, and break when p*q > 10^6. This will be about 190k iterations total. That's trivial.
Let's verify: The number of semi-primes is 190,423 (actual count for 10^6). So we can just generate them all and store in a list, then for each query, binary search for the largest semi-prime <= sqrt(A), and return its square.
But we need to be careful: the semi-primes include squares of primes (p^2). For p^2, the square root is p, which has only one prime factor, so p^4? Wait, the condition is: N has exactly 2 distinct prime factors, and for each prime factor, the exponent is even. So if N = p^2 * q^2, then sqrt(N) = p*q, which is a semi-prime. If N = p^4, then it has only 1 distinct prime factor, so not a 400 number. So we only need semi-primes that are products of two DISTINCT primes. So we should not include p*q where p=q. That is, we need numbers with exactly 2 distinct prime factors and each exponent is 1. So m must be square-free and have exactly 2 prime factors. So m is a product of two distinct primes. So we should exclude prime squares from the semi-prime list. The number of such numbers is slightly less, but still around 190k. So we just generate p*q with p < q primes.
But wait: Is that all? What about m = p*q where p and q are distinct primes. Then N = m^2 = p^2 * q^2. The distinct prime factors are p and q, and exponents are 2 and 2, both even. Correct.
Are there any other numbers? What about m = p^3? Then N = p^6, only 1 distinct prime factor. Not allowed.
What about m = p*q*r? Then N = p^2*q^2*r^2, 3 distinct prime factors. Not allowed.
So indeed, m must be a product of exactly two distinct primes. So we need the largest m <= sqrt(A) such that m is a product of two distinct primes.
So we just generate all products p*q with p < q primes, up to 10^6. Then for each query, compute s = floor(sqrt(A)), find the largest m in our list such that m <= s, and output m^2.
This is very efficient. Generation: sieve primes up to 10^6, then double loop. 190k numbers, trivial.
Query answering: Q up to 2e5, we can precompute the list and sort it (it will be generated in order if we do p from small to large, and q from p+1, but not strictly sorted by product? Actually, if we fix p and iterate q, p*q increases with q. For a larger p, p*q starts at p*(p+1) which is > p*p (previous q). But p*(p+1) might be less than some p'*q' for a larger p'? No, for a given p, the smallest product is p*(next_prime(p)). The largest p is around 10^6, so p*q is around 10^6. The products are not necessarily sorted globally if we just append in the order of p and q. We can store them and then sort, or we can just use a boolean array of size 10^6, mark the semi-primes, and then for each query, iterate downwards from sqrt(A) to find the first marked semi-prime. But we have 2e5 queries, and iterating down might be slow if sqrt(A) is large and the next semi-prime is far. The maximum gap between square-free semi-primes up to 10^6? The largest gap might be around 10? Actually, the average gap is about 5. So iterating down a few steps is fine. But we have 2e5 queries, worst case 2e5 * 10 = 2e6 operations, which is fine. But we need to know if there is a large gap. Let's check: The largest gap between products of two distinct primes up to 10^6. I recall that gaps are small, maybe at most 20 or so. Even if it's 100, 2e5 * 100 = 20 million operations, which is okay in Python. But binary search is safer. We can just store the list and sort it (190k elements), then for each query, bisect_right.
But wait: bisect on a list of 190k is O(log 190k) ~ 17, so 2e5 * 17 = 3.4 million operations, very fast.
So the plan is:
1. Sieve primes up to 10^6 (1,000,000). Use standard sieve of Eratosthenes.
2. Generate list of products of two distinct primes: for each prime p in primes: for each prime q in primes where q > p: if p*q <= 10^6: add p*q. Break when p*q > 10^6.
3. Sort the list.
4. For each query, compute s = isqrt(A). Use bisect_right to find the largest m in list <= s. Return m*m.
Edge cases: A >= 36, so s >= 6. The smallest 400 number is 36 = 2^2 * 3^2, so m=6. So list will contain 6.
Check sample: A=404, s=20 (since 20^2=400, 21^2=441>404). The largest product <=20: 2*3=6, 2*5=10, 2*7=14, 2*11=22>20. 3*5=15, 3*7=21>20. So 15? But 15^2=225, wait sample says 400. What's wrong?
Wait! 400 = 20^2. Is 20 a product of two distinct primes? 20 = 2^2 * 5. Its prime factors are 2 and 5, but the exponent of 2 is 2, which is even, but 5 is 1, which is odd. Wait, the condition is: "For each prime factor p of N, p divides N an even number of times." So for N=400=2^4*5^2, exponents are 4 and 2, both even. So N=400 is a 400 number. The square root of 400 is 20. 20 has prime factors 2 and 5, but 2 appears twice and 5 once. The condition is on N, not on sqrt(N). So my reduction to "sqrt(N) is a product of two distinct primes" is wrong! Let's re-examine.
N has exactly 2 distinct prime factors. So N = p^a * q^b, with a,b >= 1 even.
So N is a perfect square? Not necessarily! a and b are even, so N is a perfect square. Yes! N = (p^(a/2) * q^(b/2))^2. So N is a perfect square. Let M = sqrt(N). Then M = p^(a/2) * q^(b/2). The distinct prime factors of M are p and q. But a/2 and b/2 can be any positive integers! They don't have to be 1. So M can have any exponents >= 1, as long as the base primes are exactly 2. So M is any positive integer that is NOT a perfect square (because if M were a perfect square, then N would have exponents divisible by 4, but that's fine? Wait, N can have exponents divisible by 4, that's still even. The condition is only that the exponents are even. So N is any perfect square that has exactly 2 distinct prime factors. M = sqrt(N) can be any integer that has exactly 2 distinct prime factors, and no restriction on exponents? Wait, if M has exactly 2 distinct prime factors, then N has exactly 2 distinct prime factors. The exponents in N are twice the exponents in M. So as long as M has exactly 2 distinct prime factors, N will have exactly 2 distinct prime factors and even exponents. So M can be ANY integer with exactly 2 distinct prime factors! For example, M=20=2^2*5^1 has two distinct prime factors. Then N=400=2^4*5^2 has two distinct prime factors and even exponents. So M does NOT need to be square-free! M can have any exponents, even or odd, as long as there are exactly 2 distinct primes.
Ah! So the problem reduces to: find the largest perfect square N <= A such that N has exactly 2 distinct prime factors. Equivalently, find the largest M <= sqrt(A) such that M has exactly 2 distinct prime factors. Then output M^2.
M is a number with exactly 2 distinct prime factors. This includes:
- p^a * q^b where a,b >= 1.
So M can be p*q (distinct primes), p^2*q, p*q^2, p^2*q^2, p^3*q, etc.
So the condition on M is: omega(M) = 2 (number of distinct prime factors is exactly 2). No restriction on exponents.
So we need to find the largest M <= sqrt(A) with omega(M) = 2, then output M^2.
This is much broader. The number of such M up to 10^6 is larger, but still manageable? The count of numbers with exactly 2 distinct prime factors up to x is about x log log x / log x? Actually, the number of integers up to x with exactly k distinct prime factors is ~ x (log log x)^(k-1) / ((k-1)! log x). For k=2, it's about x log log x / log x. For x=10^6, log x=13.8, log log x=2.6, so 10^6 * 2.6 / 13.8 ~ 190,000? Wait, that's the same as semi-primes! Because the asymptotic for omega=2 is the same? Actually, the number of integers with exactly 2 distinct prime factors (including higher powers) is asymptotic to x log log x / log x, which is the same as semi-primes? Let me check. The count of semi-primes (products of two primes, not necessarily distinct) is also asymptotic to x log log x / log x. So they are of the same order. For x=10^6, the count of omega=2 numbers is about 210,000? Let's check: Actually, the number of integers with exactly 2 distinct prime factors up to 10^6 is around 210,000. Still very small. We can just generate them all by iterating through numbers and checking their distinct prime factors, or using a sieve-like approach.
How to generate all numbers up to 10^6 with exactly 2 distinct prime factors?
We can do: for p in primes: for q in primes with q >= p: for e1 from 1 to max_e1: for e2 from 1 to max_e2: compute p^e1 * q^e2. But this might generate duplicates if p=q? No, p and q are distinct primes. So we can iterate over all pairs of distinct primes (p,q), and then over all exponents e1>=1, e2>=1 such that p^e1 * q^e2 <= 10^6. This will generate all numbers with exactly 2 distinct prime factors. The number of such numbers is around 200k. Generating them: number of pairs of distinct primes is 190k (as before). For each pair, we need to generate combinations of exponents. The number of combinations per pair is small because p and q are at least 2, so exponents are limited. The total number of generated numbers is 210k, but the total work to generate them is sum over pairs of (number of exponent combinations). This might be a few million operations, which is fine.
Alternatively, we can just use a bytearray of size 10^6, and for each number from 1 to 10^6, we can find its distinct prime factors? But that's 10^6 iterations with factorization, which is slow.
Better: Use a sieve to compute the number of distinct prime factors (omega) for each number up to 10^6. We can do this during the sieve of Eratosthenes: start with omega[i] = 0. For each prime p, for multiples of p, if it's the first time seeing p, increment omega[m] by 1? But we need to know if p divides m and if we've already counted p for m. That's tricky in a simple sieve.
Standard method: we can compute the smallest prime factor (spf) for each number up to 10^6. Then for each number, we can compute omega by dividing by spf repeatedly? Actually, if we have spf, we can compute omega by: x = n, last = 0, count = 0. While x > 1: p = spf[x]; if p != last: count += 1; last = p; x //= p. This requires an array of size 10^6 for spf (int), and then iterating over all 10^6 numbers. 10^6 iterations is fine. We can then collect all numbers with omega == 2. That's 10^6 * (log n) worst case, but average is small. Total operations maybe 10^7. This is very easy to implement and fast enough in Python.
Let's check: We need spf for up to 10^6. We can do a sieve that stores the smallest prime factor. Memory: 10^6 integers in Python is heavy (each int is 28 bytes, so 28MB). That's okay. Or we can use a list of ints. But 28MB is fine. Or we can use an array of type 'I' from array module? Or just a list, it's fine.
Then iterate from 1 to 10^6, compute omega, if omega == 2, add to list. This is straightforward.
But wait, we can also generate directly using the prime pairs. The number of operations for the spf method is about 10^6 * (number of prime factors). The average number of prime factors for numbers up to 10^6 is small. But the while loop might do a few iterations per number. 10^6 numbers, each doing a few divisions. This should be fast enough (maybe 0.2 seconds in Python?).
Let's test mentally: For n=1, we skip. For n=2, spf[2]=2, count=1, not 2. For n=6, spf[6]=2, x=3, spf[3]=3, count=2. So we just do while x>1: p=spf[x]; if p != last_p: count++; last_p=p; x//=p. This is very fast.
Alternatively, we can just do a modified sieve: omega = [0]*(MAX+1). For p in primes: for multiple in range(p, MAX+1, p): omega[multiple] += 1. This counts the number of distinct prime factors! Because each prime p contributes 1 to all its multiples. So omega[m] = number of distinct primes dividing m. This is exactly what we need! And it's much simpler! Just a sieve where for each prime p, we iterate multiples and increment. The total number of operations is sum_{p prime} MAX/p. This is MAX * sum_{p} 1/p ~ MAX * log log MAX. For MAX=10^6, sum 1/p is about log log 10^6 ~ 2.6. So total operations ~ 2.6 million. That's extremely fast!
Wait, is that correct? If we start with an array of zeros, and for each prime p, we add 1 to all multiples of p. Then for each number, the value will be the number of distinct prime factors. Yes! Because for each prime p, it contributes 1 to all numbers divisible by p. This is exactly omega. And it counts distinct primes, not with multiplicity. So omega[n] = number of distinct prime factors. Perfect!
So we can do:
MAX = 10**6
omega = [0] * (MAX + 1)
sieve = [True] * (MAX + 1)
sieve[0] = sieve[1] = False
primes = []
for i in range(2, MAX+1):
    if sieve[i]:
        primes.append(i)
        for j in range(i, MAX+1, i):
            sieve[j] = False
            omega[j] += 1
Then after this, we collect all i from 2 to MAX where omega[i] == 2.
This is O(MAX log log MAX) for the sieve, and the inner loop for marking multiples is standard. But wait, the sieve for primes is already O(MAX log log MAX). The omega increment can be done in the same loop: for j in range(i, MAX+1, i): omega[j] += 1. This is fine.
But we also need to sieve primes. We can do both in one pass: standard sieve of Eratosthenes with omega counting.
Standard sieve: for i in range(2, MAX+1): if is_prime[i]: primes.append(i); for j in range(i, MAX+1, i): is_prime[j] = False.
But we can just do:
is_prime = bytearray(b'\x01') * (MAX+1)
is_prime[0] = is_prime[1] = 0
omega = [0] * (MAX+1)
for i in range(2, MAX+1):
    if is_prime[i]:
        primes.append(i)
        for j in range(i, MAX+1, i):
            is_prime[j] = 0
            omega[j] += 1
This is correct and efficient. The inner loop runs for each prime i, and increments omega[j] for all multiples of i. Since we mark is_prime as 0, we won't process composites as primes. The total number of increments is sum_{p prime} floor(MAX/p) ~ MAX log log MAX.
Then we collect: candidates = [i for i in range(2, MAX+1) if omega[i] == 2].
This list will have about 200k elements. Then we sort it (it's already in increasing order because we iterate i from 2 to MAX, and append in order? Actually, we are building a list by iterating i from 2 to MAX, so the list will be in increasing order. So no need to sort. We can just append.
Wait, we need to be careful: we are iterating i from 2 to MAX, and if omega[i] == 2, we append i. So the list is naturally sorted.
Then for each query, we compute s = isqrt(A). Then we find the largest m in candidates <= s. We can use bisect_right.
Then output m*m.
Check sample:
A=404, s=20. candidates: numbers with 2 distinct prime factors up to 20: 6 (2,3), 10 (2,5), 12 (2,2,3? 12=2^2*3, distinct primes: 2,3 -> 2! Yes, 12 has 2 distinct prime factors), 14 (2,7), 15 (3,5), 18 (2,3, 2^2*3^2? 18=2*3^2, distinct: 2,3 -> yes), 20 (2,5, 2^2*5, distinct: 2,5 -> yes). So up to 20, the numbers are 6,10,12,14,15,18,20. The largest is 20. 20^2=400. Correct.
A=36, s=6. largest <=6: 6. 6^2=36. Correct.
A=60, s=7 (since 7^2=49, 8^2=64>60). Wait, sqrt(60) is 7.74, floor=7. But 20^2=400>60. So we need largest <=7. Candidates up to 7: 6. 6^2=36. Sample says 36. Correct.
A=1000000000000, s=1000000. Largest candidate <= 10^6? We need the largest number <= 10^6 with exactly 2 distinct prime factors. That would be the largest such number. It might be 999983 * 999979? But we need to check if there is a larger one. The largest m <= 10^6 with omega=2. The largest prime is 999983. The next prime is 999979. Their product is 999962? Wait, 999983 * 999979 = (10^6 - 17)*(10^6 - 21) ~ 10^12, too large. So we need two primes whose product <= 10^6. The largest such product is likely 2 * 499979? No, we want the maximum product <= 10^6. This is a known value. But our sieve will find it. The sample output for 10^12 is 1000000000000. So m=10^6. Is 10^6 a candidate? 10^6 = 2^6 * 5^6. It has exactly 2 distinct prime factors! So 10^6 is in the list. Then 10^6^2 = 10^12. So the answer is 10^12. Our sieve will include 10^6 because omega[10^6] will be 2 (primes 2 and 5). Correct.
A=123456789, s=floor(sqrt(123456789)) = 11111.111... = 11111. We need the largest m <= 11111 with omega=2. The sample output is 123454321. 11111^2 = 123454321. So m=11111. Is 11111 in the list? 11111 = 41 * 271. Both are primes, so omega=2. So 11111 is a candidate. And it's <=11111. Is there a larger candidate <=11111? The next one might be 11110=2*5*11*101? Actually 11110=2*5*11*101, omega=4. 11112=2^3*3*463, omega=3. 11113? 11113 is prime? 11113/... maybe prime. 11114=2*5557, omega=2? 5557 might be prime. 11114^2 > 123456789? 11114^2 = 123521... > 123456789. So 11111 is indeed the largest. Our sieve will find it.
So the approach works perfectly.

Let's double-check the constraints: A up to 10^12, so sqrt(A) up to 10^6. MAX = 10^6 is correct.
Q up to 2e5.
Memory: omega list of size 1e6 (ints). Python int is 28 bytes, so 28MB. is_prime bytearray is 1MB. candidates list of ~200k ints: ~5MB. Total ~35MB, which is fine.
Time: Sieve up to 1e6 takes about 0.1-0.2 seconds. Collecting candidates: 1e6 iterations, simple comparison. Query answering: 2e5 bisects on a list of 200k. Each bisect is O(log 200k) ~ 18, so 3.6 million operations. Very fast.
We can also use array module for omega to reduce memory, but 28MB is okay.
Wait, we can optimize memory: instead of storing omega as Python ints, we can store it as a bytearray, since omega for numbers up to 10^6 is at most 7 (2*3*5*7*11*13*17 > 10^6? Actually, product of first 7 primes is 510510 < 10^6, product of first 8 is 9699690 > 10^6. So max omega is 7. So a bytearray is sufficient! That reduces memory to 1MB. We can do omega = bytearray(MAX+1). Then omega[j] += 1 works with bytearray? Bytearray elements are integers 0-255, and they support increment. So yes, we can use bytearray.
Then candidates will be a list of ints (the indices). That's fine.
So:
MAX = 10**6
is_prime = bytearray(b'\x01') * (MAX+1)
is_prime[0] = is_prime[1] = 0
omega = bytearray(MAX+1)
primes = []
for i in range(2, MAX+1):
    if is_prime[i]:
        primes.append(i)
        step = i
        for j in range(i, MAX+1, step):
            is_prime[j] = 0
            omega[j] += 1
candidates = [i for i in range(2, MAX+1) if omega[i] == 2]
# candidates is already sorted.
Then for each query:
import math
A = ...
s = int(math.isqrt(A))
# bisect_right to find insertion point
import bisect
idx = bisect.bisect_right(candidates, s) - 1
if idx < 0: # should not happen because A>=36, s>=6, candidates includes 6.
    ans = 36
else:
    m = candidates[idx]
    ans = m * m
print(ans)

But wait: we need to ensure that for very small A, we still get an answer. The smallest candidate is 6 (2*3). So for A >= 36, s >= 6, so we will always find at least 6. The problem states a 400 number not exceeding A always exists under constraints, and A >= 36. So 36 is always a valid answer. So idx will never be -1. We can just assert or handle it.

One more thing: The sieve loop "for i in range(2, MAX+1)" with "if is_prime[i]" is a standard sieve, but it might be a bit slow in Python for 1e6? Actually, the standard sieve with range and step is fast enough. 1e6 is small. We can also use the segmented sieve or bitarray, but it's fine.
We can also generate primes and omega in one go. The inner loop "for j in range(i, MAX+1, step): is_prime[j] = 0; omega[j] += 1" does two operations per multiple. That's fine.

Let's test with the sample in our head:
Candidates: [6, 10, 12, 14, 15, 18, 20, ...]
A=404: s=20, bisect_right gives index of 20+1, minus 1 gives index of 20. m=20, 400.
A=36: s=6, m=6, 36.
A=60: s=7, bisect_right on [6,10,...] for 7 gives index 1 (for 10), minus 1 gives 0, m=6, 36.
A=10^12: s=10^6, candidates includes 10^6, so m=10^6, 10^12.
A=123456789: s=11111, candidates has 11111, m=11111, 123454321.

Everything seems correct.

Now, let's think about potential pitfalls:
- The sieve marks is_prime as 0 for all multiples. This is the standard sieve. The omega increment is also done for all multiples. This correctly counts distinct prime factors.
- We need to make sure that for each prime i, we iterate multiples starting from i. That's fine.
- The list candidates is built by iterating i from 2 to MAX, so it's in increasing order.
- math.isqrt is available in Python 3.8+. We can use it.
- Q up to 2e5, reading input with sys.stdin is needed.
- Output with sys.stdout.

We should also consider if there is any number with exactly 2 distinct prime factors that is a perfect square and larger than our list? No, because we only care about M <= sqrt(A) <= 10^6. So MAX=10^6 is sufficient.

Let's double-check the number of candidates. The count of numbers <= 10^6 with exactly 2 distinct prime factors. According to some sources, it's around 209,867. So candidates list has ~210k elements. That's small.

Time complexity:
- Sieve: O(MAX log log MAX) ~ 1e6 * 2.6 = 2.6e6 operations for the inner loops, plus the outer loop of 1e6. Total maybe 4e6 operations. Fast.
- Building candidates: 1e6 iterations, each with a comparison and possible append. Fast.
- Queries: 2e5 * O(log 210k) ~ 2e5 * 18 = 3.6e6 operations. Fast.
Total well within 2 seconds.

We can write the code cleanly.

One more optimization: We can avoid storing primes list if we only need it for something else, but we don't need it after the sieve. So we can just not store it, or we can break out of the inner loop early? Not needed.

Let's write the code:

import sys
import math
import bisect

def solve():
    MAX = 10**6
    is_prime = bytearray(b'\x01') * (MAX + 1)
    is_prime[0] = 1
    is_prime[1] = 1
    omega = bytearray(MAX + 1)
The problem asks for the number of arithmetic progressions of length 3 within a given set of distinct integers. Since N can be up to 10^6, an O(N^2) check is infeasible. We use a hash set for O(1) membership queries. For each pair (A, B) with A < B, we check if the next element C = 2B - A exists in the set. To avoid double counting, only consider pairs where A is the smallest element (i.e., iterate over sorted values and consider pairs where A < B). This yields O(N^2) in the worst case, which is still too large.

Better approach: For each B in the sorted set, iterate over potential differences d such that B - d and B + d are both in the set. We can achieve this by iterating over elements and using two pointers or a hash set, but still O(N^2) worst case.

Optimal approach: Since values S_i ≤ 10^6, we can use a boolean array for membership. For each pair (A, C) with A < C and same parity (since B = (A+C)/2 must be integer), check if (A+C) is even and if (A+C)//2 is in the set. But this is O(N^2).

Alternative: For each A, iterate over larger elements C and check if B exists. Still O(N^2) worst case.

Actually, with N up to 10^6, we need O(N log N) or O(N * sqrt(max_val)) or similar. The constraint S_i ≤ 10^6 allows us to use the fact that max value is small. We can iterate over all possible differences d from 1 to max_val, and for each element a in sorted order, check if a+d and a+2d are in the set. To avoid double counting, we can iterate over all elements as the middle B, and for each B, check valid A = B - d and C = B + d. This is O(N * max_val) worst case.

Better: For each A, iterate over C and check B. Still O(N^2).

Wait, there's a classic solution: For each pair (A, C), check if B exists. But we can limit pairs by considering that the number of triplets is small or by using the bound. However, worst case (e.g., arithmetic progression) gives N*(N-1)/2 pairs.

Alternative: Since S_i ≤ 10^6, the maximum difference is 10^6. For each possible difference d, we can slide a window. But elements are not contiguous.

Actually, we can use the fact that S_i ≤ 10^6 to use an array of size 10^6. For each d from 1 to 10^6, we can find all chains of elements with step d. But we need elements present in S. We can for each d, iterate over x from 1 to 10^6 - 2d, check if x, x+d, x+2d are all in S. This is O(10^6 * 10^6) too large.

Better: For each element x in S, for each multiple? No.

Let's think: N is 10^6, S_i ≤ 10^6. So the set is dense in [1, 10^6]. We can use a boolean array `present[1..10^6]`. Then for each i from 1 to 10^6 - 2, if present[i] and present[i+d] and present[i+2d], we count. This is O(max_val^2) which is 10^12, too large.

We need to leverage that N is also 10^6. In the worst case, S = {1, 2, ..., 10^6}. The number of triplets is C(10^6, 3) which is huge. But the answer can be large (64-bit), but the time complexity must be subquadratic.

Observation: For the set {1, 2, ..., M}, the number of triplets is O(M^2). We need to compute it faster. For arithmetic progressions in a dense set, we can use the fact that the number of triplets with difference d is (M - 2d) for d=1..M/2. Summing gives O(M^2). We cannot sum naively if M=10^6? Actually O(M^2) is 5e11, too large. But M=10^6, M^2/2 = 5e11, too slow.

But wait, the problem says N up to 10^6, S_i up to 10^6. We need an O(N sqrt(max_val)) or O(N log N) solution.

Alternative approach: For each A, iterate over possible C such that B exists. We can precompute for each value the list of "next" values? Not helpful.

Wait, there's a known solution for counting arithmetic progressions in a set: For each pair (A, B) with A < B, check if 2B - A is in the set. This is O(N^2) in worst case. But if the set is arbitrary, we cannot do better than O(N^2) in the worst case? Actually, with N=10^6, O(N^2) is impossible. So there must be a trick.

The trick is that S_i ≤ 10^6. So the values are bounded. We can use a bitset or array for fast membership. But we still need to iterate over pairs.

However, note that the number of triplets can be huge, but we can compute it using the property of arithmetic progressions. For each possible difference d, we can count how many starting points a have a, a+d, a+2d in S. To do this efficiently, we can iterate over all elements and for each element as the middle B, we need to count how many A < B such that C = 2B - A > B and in S. This is like for each B, count valid A. This is still O(N^2).

But with values up to 10^6, we can use FFT? No, we need integer arithmetic.

Wait, maybe we can iterate over all possible B and for each B, we want to count A < B such that 2B - A in S. That is for each d from 1 to B-1, check if B-d and B+d in S. This is O(N * max_val) which is 10^12, too large.

But note that if we iterate over differences d, for each d we need to find how many B such that B-d and B+d are in S. We can do this by iterating over all possible B for a given d. For a fixed d, the condition is B-d in S and B+d in S. This is like a correlation or convolution. We can represent S as a characteristic array f[1..M] where f[x]=1 if x in S else 0. Then for each d, the number of B is sum_{B} f[B-d] * f[B] * f[B+d]. We want sum over d of this. This is the number of 3-term arithmetic progressions in the set. This can be computed using FFT in O(M log M) time! Because sum_{B} f[B-d] f[B] f[B+d] is the convolution of f with itself at offset d, summed over B. Specifically, define g_d = (f * f)[d] where * is convolution. Then the number of triplets with difference d is sum_{B} f[B] * g_{2B?} No, careful.

We want count = sum_{A < B < C} f[A] f[B] f[C] where C - B = B - A. Let d = B - A > 0. Then C = B + d. So for each d, we need sum_{B} f[B-d] f[B] f[B+d]. This is sum_{B} f[B] * (f[B-d] f[B+d]). This is not a simple convolution because of the product of two terms at different offsets.

However, we can use the fact that we can compute for each d, the number of pairs (A, C) with C - A = 2d, which is (f * f)[2d]? No, (f * f)[k] = sum_x f[x] f[x+k]. So (f * f)[2d] = sum_x f[x] f[x+2d]. This counts pairs (A, C) with C - A = 2d. Then for each such pair, B = (A+C)/2 = x+d. So we need to check if B is in S. So the count is sum_{d} sum_{x} f[x] f[x+2d] f[x+d]. This is the sum over all x and d of f[x] f[x+d] f[x+2d]. This is exactly the number of 3-term arithmetic progressions.

We can compute this using FFT? The expression is sum_{x} f[x] (f * f)[2d] at d = something. Actually, we can rewrite: count = sum_{x} sum_{d} f[x] f[x+d] f[x+2d]. This is equivalent to sum_{x} f[x] * (number of d such that x+d and x+2d in S). Not helpful.

But we can use the following: For each d, count the number of x such that x, x+d, x+2d are in S. This is sum_x f[x] f[x+d] f[x+2d]. If we compute the convolution of f with itself, we get g[k] = sum_x f[x] f[x+k]. Then we want sum_d sum_x f[x] f[x+d] f[x+2d] = sum_d sum_x f[x+d] * (f[x] f[x+2d]). Not directly.

However, we can compute for each d, let h_d = sum_x f[x] f[x+d]. Then we want sum_d sum_x f[x+d] * (f[x] f[x+2d]) = sum_d sum_x f[x+d] * (something). Note that f[x] f[x+2d] is like a 2-step indicator. We can define a new array a where a[x] = f[x] * f[x+2d]? That depends on d.

Alternative: Use the fact that M = 10^6. We can do O(M sqrt(M)) by enumerating divisors? For each d, we iterate over B. The number of pairs (B-d, B+d) in S is the number of B such that both are present. This is like the number of B where B-d and B+d are in S. We can compute this for all d by iterating over d and for each d, iterating over B. The total work is sum_d (number of B). In the worst case (S = {1..M}), for each d, the number of B is M - 2d. So total work is sum_{d=1}^{M/2} (M - 2d) = O(M^2/2) = 5e11. Too large.

But maybe we can use the fact that N = 10^6, so the set is dense. But M is also 10^6. So M^2 is too large.

Is there a known algorithm for counting 3-term arithmetic progressions in O(N sqrt(N)) or similar? For arbitrary sets, the best known is O(N^2) in worst case, but with small integer values, we can do better.

Wait, the constraints: N up to 10^6, S_i up to 10^6. This is similar to the problem of counting arithmetic progressions in a set of integers with bounded values. There is a solution using the fact that for each element, we can iterate over multiples? Not exactly.

Another idea: For each element a, we can count the number of elements b > a such that 2b - a is in S. We can do this by, for each a, iterating over b = a + d, and checking if a + 2d is in S. This is O(N * D) where D is the maximum difference. But we can limit d by the fact that a + 2d ≤ M. So for each a, the number of d is at most (M - a)/2. Sum over a is O(M^2). Too large.

But we can use a trick: For each possible difference d, we can find all starting points a. We can do this by iterating over all a in S, and for each a, iterating over d such that a+d in S? Not helpful.

Wait, maybe we can use the following: Since M = 10^6, we can use a bitset and use bitwise operations to speed up the inner loop. For example, for each a, we can shift a bitset and check intersection. But M = 10^6, we can represent S as a bitset of size 10^6 (about 125KB). Then for each a, we want to find b > a such that 2b - a in S. We can precompute a bitset S_bits. For a given a, we want to find b such that S_bits[b] and S_bits[2b-a]. We can iterate over b from a+1 to M. For each b, we check if S_bits[2b-a]. This is still O(M^2) but with bit operations it's faster? M=10^6, M^2=10^12, even with bit operations, 10^12 operations is too slow (1e12 bit ops is about 1e9 word ops? No, 10^12 bit ops is 10^12/64 = 1.5e10 64-bit ops, still too slow).

But we can use the bitset to accelerate the check for a given a: For a fixed a, we want to count b such that S_bits[b] and S_bits[2b-a]. This is equivalent to: for each b, check if 2b-a in S. We can loop over all possible c = 2b-a. Since b > a, c > a. Also, b = (a+c)/2 must be integer, so a and c have same parity. So we can iterate over c > a, same parity, and check if (a+c)/2 in S. This is still O(M^2) in worst case.

What if we iterate over all possible b? For each b, we want a < b and c > b such that a + c = 2b. So for each b, we need pairs (a, c) with a < b < c, a in S, c in S, and a + c = 2b. This is like for each b, we need to count the number of a in S with a < b such that 2b - a in S. This is the number of a in S ∩ (1, b) such that 2b - a in S. We can precompute prefix sets or something.

Since S is static, we can for each b, we want to count a in S, a < b, with 2b - a in S. We can do this by iterating over a in S less than b, but that's O(N^2). Alternatively, we can iterate over all possible a in S, and for each a, consider b > a such that 2b - a in S. This is symmetric.

Another approach: For each possible sum s = 2b, we can count the number of pairs (a, c) in S with a < c, a + c = s, and (a+c)/2 in S. So for each s, we need pairs (a, c) with a < c, a + c = s, and (a+c)/2 in S. But (a+c)/2 = s/2, so we just need s even and s/2 in S. So for each even s, if s/2 is in S, we count the number of pairs (a, c) in S with a < c and a + c = s. This is exactly the number of pairs in S that sum to s, with a < c. And we need s/2 in S.

So the algorithm: For each even s from 2 to 2M, if s/2 is in S, count the number of pairs (a, c) in S with a < c and a + c = s. The total number of such triplets is sum over such s of (number of pairs).

Now, how many pairs (a, c) in S sum to s? We can compute this efficiently if we can compute the convolution of the indicator array f with itself. Let f[x] = 1 if x in S else 0. Then the convolution g = f * f, where g[k] = sum_x f[x] f[x+k] = number of pairs (x, x+k) in S. Note that this counts ordered pairs (a, c) with a < c? Actually, g[k] counts pairs with difference k, not sum. For sum, we need to reverse one array. Let f_rev[x] = f[M+1-x]? Or just use convolution on reversed array.

We want h[s] = number of pairs (a, c) with a + c = s. If we reverse f, say r[x] = f[M+1-x], then (f * r)[s] = sum_x f[x] r[s-x] = sum_x f[x] f[M+1-(s-x)] = sum_x f[x] f[x + (s - M - 1)]. Not exactly. Better: define r[x] = f[x] but we want sum. Standard: h[s] = sum_{a} f[a] f[s-a]. This is the convolution of f with itself (or f with reversed f). If we compute convolution of f with f, we get sum_a f[a] f[s-a], which counts all ordered pairs (a, c) with a + c = s, including a = c. So h[s] = (f * f)[s]. Then the number of pairs with a < c is (h[s] - f[s/2] * (f[s/2] if s even? Wait, if a = c, then 2a = s, so s even and a = s/2. So the number of pairs with a < c is (h[s] - (f[s/2] if s even else 0)) / 2? Actually, h[s] counts ordered pairs (a, c) with a + c = s. Each unordered pair {a, c} with a != c is counted twice (once as (a,c), once as (c,a)). The pair (a,a) is counted once. So number of unordered pairs with a < c is (h[s] - (f[s/2] if s even else 0)) / 2.

Now, for each even s such that s/2 is in S, we add (h[s] - f[s/2]) / 2 to the answer. Note that if s/2 is in S, then f[s/2] = 1, so the number is (h[s] - 1) / 2 if h[s] is odd, but h[s] - 1 is even because the pair (s/2, s/2) is counted in h[s]. So we can compute:

ans = sum_{s even, f[s/2]=1} (h[s] - 1) // 2.

We can compute h = f * f using FFT in O(M log M) time. M = 10^6, so M log M is about 20 million operations, which is feasible. We need to use complex FFT or NTT. In Python, we can use numpy's FFT, but we need to be careful with precision. Alternatively, we can use the fact that M=10^6, we can use the FFT from numpy or implement our own. But we need to be careful with memory: M=10^6, next power of 2 is 2^20 = 1,048,576. So we can do FFT of size 2^20. Then f is a float array of size 2^20. FFT is fast in numpy.

But wait: we need to compute h[s] = (f * f)[s] for s up to 2M. Since M=10^6, s up to 2M = 2e6. We need FFT of size at least 2M. Next power of 2 is 2^21 = 2,097,152. That's fine.

Steps:
1. Read N and the list S.
2. Determine M = max(S). Actually, we need to consider up to max(S) for the array f. Since S_i ≤ 10^6, M ≤ 10^6.
3. Create array f of size L = 1 << (M*2). Actually, we need to compute convolution of f with f. The result size is up to 2M. So we can set L = 1 << ceil(log2(2M+1)). Or we can just use a power of 2 >= 2*max(S)+1.
4. Initialize f as float array of zeros of size L.
5. For each x in S, set f[x] = 1.
6. Compute FFT of f, multiply pointwise by itself, inverse FFT. This gives the convolution h. Note that due to floating point, h will be approximately integers. We can round to nearest integer.
7. Compute ans: For s from 2 to 2M, step 2 (even s), if s/2 is in S (i.e., f[s//2] == 1), then add (int(round(h[s])) - 1) // 2 to ans.
8. Print ans.

But wait: h[s] is the sum of f[a] f[s-a] for all a. This counts ordered pairs. We want unordered pairs with a < c. So (h[s] - (1 if s/2 in S else 0)) // 2. And we only add if s/2 is in S. So the formula is correct.

Let's test with sample 1:
S = {1,2,3,5,8}, M=8.
f[1]=f[2]=f[3]=f[5]=f[8]=1.
Compute h = f * f.
We can compute manually:
s=2: f[0]f[2]+f[1]f[1]+f[2]f[0] = 0+0+0=0? Wait, f[0]=0, f[1]=1, f[2]=1? s=2: a=1, s-a=1. So f[1]f[1]=1. So h[2]=1. s/2=1 in S, so add (1-1)//2 = 0.
s=4: a=1,3; f[1]f[3]+f[2]f[2]+f[3]f[1] = 1*1 + 1*1 + 1*1 = 3. s/2=2 in S, add (3-1)//2 = 1. This is pair (1,3) with B=2? Wait, (1,2,3) is triplet. Here a=1, c=3, sum=4, B=2. So yes.
s=6: a=1,2,3,4,5. f[1]f[5]=1, f[2]f[4]=0, f[3]f[3]=1, f[5]f[1]=1, f[4]f[2]=0. Total h[6]=3. s/2=3 in S, add (3-1)//2=1. This is (1,5) with B=3? (1,3,5) is triplet.
s=8: a=1,3,5,7. f[1]f[7]=0, f[3]f[5]=1, f[5]f[3]=1, f[7]f[1]=0. h[8]=2. s/2=4 not in S, skip.
s=10: a=2,5,8. f[2]f[8]=1, f[5]f[5]=1, f[8]f[2]=1. h[10]=3. s/2=5 in S, add (3-1)//2=1. This is (2,8) with B=5? (2,5,8) is triplet.
s=12: a=4,8. f[4]f[8]=0, f[8]f[4]=0, h[12]=0.
s=16: a=8,8. f[8]f[8]=1, h[16]=1. s/2=8 in S, add (1-1)//2=0.
Total ans = 1+1+1 = 3. Correct.

Sample 2: S = {100000, 200000, 300000, 400000, 499998, 499999, 500000}. Let's trust the logic.

Sample 3: S = {1,2,4,7,10,12,13,15,16,19}. We can trust.

So the algorithm works.

Now, implementation in Python:
- Use numpy for FFT. But we need to be careful with input size. N up to 10^6, M up to 10^6. Creating a numpy array of size 2^21 = 2,097,152 is fine (about 16MB for float64).
- Read input using sys.stdin.buffer.read.
- Parse integers.
- Find max_val.
- Compute L = 1 << (max_val*2 - 1).bit_length() or something.
- Create f = np.zeros(L, dtype=np.int8) or np.float64. Using int8 and then converting? Actually, we need to do FFT, so we need float. We can use np.float64.
- Set f[x] = 1.0 for x in S.
- Use np.fft.fft and np.fft.ifft.
- h = np.fft.ifft(np.fft.fft(f) * np.fft.fft(f)).real
- Then round to integer: h = np.round(h).astype(np.int64)
- Then compute ans: iterate over s from 2 to 2*max_val, step 2. If f[s//2] is 1, add (h[s] - 1) // 2.
- But iterating over s up to 2e6 in Python is fast (2 million iterations).
- However, we need to check f[s//2] == 1. We can use a boolean array present.
- Time complexity: FFT is O(L log L) ~ 2e6 * 21 = 4e7 operations, which is okay in numpy.
- Memory: f is size L ~ 2e6, float64 = 16MB. h same. Total ~32MB, fine.

But wait: The problem says S_i ≤ 10^6, but N can be 10^6. If S_i = 10^6, then M = 10^6. Then 2M = 2e6. L = 2^21 = 2097152. FFT of that size is fast.

One catch: The convolution result h[s] for s > 2M might be nonzero due to FFT wrap-around? We zero-padded, so the convolution is exact for indices 0 to 2M. Since we only care about s up to 2M, it's fine.

Precision: FFT with float64 should be exact for integer values up to about 10^15 or so. The maximum value of h[s] is the number of pairs summing to s. The maximum number of pairs is if S is dense. The maximum h[s] could be N, which is up to 10^6. So h[s] ≤ 10^6. The error in FFT should be less than 0.1, so rounding is safe.

But we need to be careful: If we use np.fft.fft, it returns complex128. Multiplying gives complex128. Inverse FFT gives complex numbers with small imaginary parts. We take .real. Then we round. This is standard.

Alternatively, we can use the convolution theorem with real FFT (np.fft.rfft) to save memory and time. But rfft is for real input. We can use rfft and then irfft. However, we need to square the result. The product of rfft is not the same as the full FFT. We need to multiply the full FFT. But we can use np.fft.rfft on the real array, get the complex result, square it, then irfft. This works because the input is real, and the product of the rfft of f with itself is the rfft of the convolution. Actually, if f is real, then the FFT of f has conjugate symmetry. The product of FFT(f) and FFT(f) is the FFT of the autocorrelation? Wait, convolution theorem: FFT(f * f) = FFT(f) * FFT(f). If f is real, we can use rfft to get the positive frequencies. The product of the rfft of f with itself is the rfft of the full convolution. Then we can use irfft to get the convolution. This is efficient. Let's do that.

So:
f = np.zeros(L, dtype=np.float64)
f[x] = 1 for x in S.
F = np.fft.rfft(f)
h = np.fft.irfft(F * F, n=L)
h = np.round(h).astype(np.int64)

This is standard.

Now, we need to be careful with the size L. We need L to be a power of 2 at least 2*max_val+1. But we can just set L = 1 << (2*max_val).bit_length() or something. Actually, we need L >= 2*max_val+1. So L = 1 << (2*max_val).bit_length() might be enough if 2*max_val+1 is not a power of 2. For example, if max_val=10, 2*max_val=20, bit_length=5, 1<<5=32, which is > 20. So it's fine.

But we need to zero-pad to L. The convolution will be correct for indices 0 to 2*max_val. We only need up to 2*max_val.

Now, the answer can be large. The maximum number of triplets is C(N,3). N=10^6, so C(10^6,3) ≈ 1.67e17. This fits in 64-bit integer (max 9.22e18). So we need to store ans in Python int (unlimited) or 64-bit.

Implementation steps:
1. Read all integers.
2. Extract S.
3. max_val = max(S)
4. L = 1 << (2*max_val).bit_length()  # but careful: if max_val=0? S_i >=1, so max_val>=1.
5. f = np.zeros(L, dtype=np.float64)
6. For each x in S: f[x] = 1.0
7. F = np.fft.rfft(f)
8. h = np.fft.irfft(F * F, n=L)
9. h = np.rint(h).astype(np.int64)  # rint rounds to nearest integer
10. present = f.astype(bool)  # or we can use a set, but array is faster
11. ans = 0
12. For s in range(2, 2*max_val+1, 2):
    if present[s//2]:
        count = h[s] - 1
        if count < 0: count = 0  # should not happen
        ans += count // 2
13. Print ans.

But we need to be careful: h[s] is the sum of f[a]f[s-a]. For s > 2*max_val, h[s] is due to wrap-around, but we don't care.

Test with sample 1: max_val=8, L=1<<(16).bit_length()? 16 is 10000b, bit_length=5, 1<<5=32. So L=32. Works.

Sample 2: max_val=500000, 2*max_val=1,000,000, bit_length=20, 1<<20=1,048,576. L=1,048,576. Works.

Sample 3: max_val=19, L=1<<(38).bit_length()? 38 is 100110b, bit_length=6, 1<<6=64. Works.

Now, is there any issue with the FFT size being too small? For max_val=500000, 2*max_val=1,000,000. L=2^20=1,048,576. This is >= 1,000,000. So the convolution indices up to 1,000,000 are correct.

But wait: The convolution of f with f using FFT of size L gives the circular convolution of length L. We want the linear convolution of length 2*max_val+1. To get the linear convolution, we need L >= 2*max_val+1. Here L = 2^20 = 1,048,576. 2*max_val+1 = 1,000,001. So L > 2*max_val+1. So the linear convolution is exact. The circular convolution is equivalent to linear convolution because the sequences are zero-padded to length L, and the linear convolution has length at most 2*max_val+1 <= L. So it's fine.

Now, performance: Creating f of size 1M and setting N values is O(L+N). FFT is O(L log L). The loop over s up to 2*max_val is O(M). All are fine.

One potential issue: If max_val is small, say 10, L=32, FFT is fast. If max_val=10^6, L=2^20, FFT is about 2^20 * 20 = 20 million operations, which in numpy is very fast (less than 0.1 second). The loop over s is 1 million iterations, also fast.

Memory: f is 8MB, F is complex128 of size L/2+1 = 524289, so about 8MB. h is another 8MB. Total ~24MB. Fine.

We need to import numpy. Usually allowed in such problems, but if not, we might need to implement FFT in pure Python? That would be too slow. The problem doesn't specify if external libraries are allowed. In competitive programming, numpy is often allowed, but sometimes not. However, the constraints (N=10^6) strongly suggest that an O(N^2) solution is not expected, and FFT is the intended solution. In Python, without numpy, implementing FFT is very slow. So numpy is likely expected or allowed. But to be safe, we could consider alternative approaches without FFT.

Alternative approach without FFT: For each possible difference d, we can count the number of triplets. The number of d is up to max_val. For each d, we can iterate over a in S and check if a+d and a+2d in S. This is O(N * D) where D is the maximum difference. In the worst case, N=10^6, D=10^6, so 10^12 operations. Too slow.

But we can use the fact that the set is bounded. We can use a boolean array and for each a, we can iterate over d. Still O(M^2).

Another idea: For each a, we can iterate over multiples? No.

What if we use the following: For each b, we want to count a < b such that 2b-a in S. We can precompute for each b, the set of a in S with a < b. But we need to check if 2b-a in S. This is equivalent to: for each b, we want to count the number of a in S such that a < b and 2b-a in S. Let S_b = S ∩ (1, b). We want to count a in S_b such that 2b-a in S. This is like the intersection of S_b and {2b - c : c in S, c > b}. Not helpful.

What about using a hash set and for each a, iterating over c? Still O(N^2).

Given the constraints, the FFT solution is the most efficient. I will proceed with the numpy FFT solution.

But wait: The problem is from a Japanese contest (probably AtCoder or similar). They often allow PyPy but not numpy. However, the constraints N=10^6, S_i ≤ 10^6 suggest that the intended solution is O(N sqrt(N)) or O(N log N) using FFT. In Python, without numpy, we can use the pyfft or implement a simple FFT. But implementing FFT in pure Python for size 1M is too slow. So maybe there is another approach.

Let's think again: N up to 10^6, S_i up to 10^6. The answer is the number of 3-term arithmetic progressions. There is a known algorithm using the "meet-in-the-middle" or using the fact that the number of progressions with difference d is at most N, and the number of distinct differences is at most N. But in the worst case, if S is {1,2,...,M}, the number of progressions is O(M^2), and the number of distinct differences is M/2. We need to sum over d. If we can compute for each d, the number of progressions in O(N) time, that would be O(N^2). Not good.

But maybe we can use the fact that the values are small to use a sieve-like approach. For each d, we can mark numbers. But we have many d.

Wait, there is a known solution for counting 3-term arithmetic progressions in O(N sqrt(M)) time by using the fact that for each element, we can iterate over divisors? No.

Another thought: Since M = 10^6, we can precompute for each x, the list of elements in S that are multiples? No.

What if we use the following: For each a in S, we consider the set of b > a in S. For each such b, we check if 2b-a in S. We can speed up the check if we have a hash set. But we still have O(N^2) pairs.

But maybe N is not 10^6 in the worst case for time? N=10^6, but the number of triplets is small? No, in the worst case (arithmetic progression), the number of triplets is O(N^2), so the output can be large, but we need to compute it. The time to output is O(1). So we need to compute it.

Is there a way to compute the number of 3-term APs in a set of size N with values up to M in O(N sqrt(M))? For each element a, we can consider the differences d such that a+d in S. The number of such d is the number of elements greater than a. We can iterate over b > a, then c = 2b-a. We can check if c in S. This is O(N^2) in worst case.

But note that if the set is dense, we can use the property that the number of b is large, but we can early exit? No.

Maybe we can use the following: For each b, we want to count a < b with 2b-a in S. This is like for each b, we want to count a in S_b such that 2b-a in S. Let S_b be the set of elements less than b. We can precompute an array next[x] = smallest element in S greater than x? Not helpful.

What if we use a bitset for the set S, and for each b, we want to count a in S_b such that 2b-a in S. We can iterate over a in S_b, but that's O(N^2). Alternatively, we can iterate over possible a? No.

Wait, we can use the bitset to represent S. Then for a fixed b, we want to find a such that a in S and 2b-a in S. Let T = S shifted by 2b. That is, we want a in S and a in (2b - S). So we want the intersection of S and (2b - S). (2b - S) is the set of x such that 2b-x in S. This is the reflection of S around b. We can compute this reflection by iterating over all elements in S? No, we can precompute a bitset for S. Then for each b, we want to compute the intersection of S and (2b - S). The reflection of S around b is not easy to compute quickly without shifting the whole bitset.

But we can iterate over all possible a in S (a < b) and check if 2b-a in S using the bitset. That's O(N) per b, total O(N^2).

Maybe we can use the fact that M=10^6 is small enough to use a different convolution. We already have the convolution solution which is O(M log M). That is optimal. In Python, with numpy, it's fast. In PyPy without numpy, we can implement FFT in pure Python? It would be slow. But maybe the problem allows numpy? The problem statement doesn't specify language restrictions. In AtCoder, they often have separate judges for Python, and numpy is not available. So maybe there is a solution without FFT.

Let's think of an O(N sqrt(M)) solution. For each a, we can iterate over possible differences d, but we can skip if d is large? Not really.

Another idea: Use the fact that the number of triplets is the sum over d of (number of a such that a, a+d, a+2d in S). For each d, we can find all a such that a and a+d are in S, then check a+2d. The number of pairs (a, a+d) in S is the number of edges in the graph where vertices are elements and edges connect x and x+d. We can precompute for each d the list of a such that a and a+d in S. But the number of d is up to M, and for each d, the number of a is at most N. So total O(NM) again.

But we can use a trick: For each a, we can iterate over d such that a+d in S. This is the number of neighbors of a in the "difference graph". The sum over a of the degree is 2 * (number of pairs). The number of pairs can be O(N^2). So not helpful.

Wait, maybe we can use the following: For each a, we can iterate over c in S with c > a, and check if (a+c)/2 is in S. This is O(N^2) pairs. But we can prune: if c - a is odd, skip. But still O(N^2) in worst case.

What if we use a hash set and for each a, we iterate over multiples? For example, for each a, we consider b = a + d, but we only consider d that divides something? No.

Let's reconsider the FFT solution. Even if numpy is not available, we can implement a simple FFT in Python using the iterative Cooley-Tukey. For size 2^20 = 1,048,576, the FFT will have 20 stages, each with O(L) operations. Total operations ~ 20 * 1M = 20M complex multiplications. In Python, each multiplication is slow. 20M multiplications in Python is too slow (maybe 20 seconds?). So pure Python FFT is not feasible.

But we can use the fact that the values are integers and we can use the Number Theoretic Transform (NTT) with a modulus. However, implementing NTT in pure Python is also slow.

Maybe there is a solution using the fact that S_i ≤ 10^6, and we can use a "sparse" FFT or something? No.

Wait, maybe we can use the following: For each a, we can iterate over d from 1 to sqrt(M)? No.

Another thought: The number of triplets can be computed by iterating over the middle element B. For each B, we want to count A < B such that C = 2B - A in S. This is equivalent to: for each B, we want to count the number of A in S with A < B and 2B - A in S. Let’s define for each B, the set of valid A is S ∩ (2B - S) ∩ (1, B). We can precompute a prefix set for each prefix of the sorted array. But that would be O(N) per B if we use hash sets, total O(N^2). However, we can use a binary indexed tree or something to count the number of A in S with A < B and 2B - A in S. But we need to know if 2B - A is in S, not just count.

What if we precompute for each x, the next element in S? Not helpful.

Let's think differently. Since S_i ≤ 10^6, the maximum value is small. We can use a boolean array present[0..M]. For each possible difference d, we can find the number of triplets. How many differences are there? Up to M. For each d, we can iterate over a from 1 to M-2d, and check if present[a], present[a+d], present[a+2d]. This is O(M^2) in worst case. But we can optimize: For each a, we can iterate over d such that present[a+d] is true. That is, for each a, we look at the list of elements in S greater than a. This is like for each a, we iterate over b in S, b > a, and check if 2b-a in S. That's O(N^2).

But maybe we can use the fact that the number of triplets is small? No, the problem asks to print the number, which can be large.

Wait, maybe we can use the following: For each a, we can iterate over possible B = a + d, but we only need to check if C = a + 2d is in S. We can do this by, for each a, iterating over d from 1 to (M-a)/2, but we can skip d if a+2d is not in S? That doesn't help.

What if we use a sieve-like approach: For each possible C, we can iterate over possible A? No.

Let's search memory: There is a known problem "Fine Triplets" from AtCoder? Actually, this looks like AtCoder ABC 175 D? No, it's a different problem. The constraints N=10^6, S_i ≤ 10^6 suggest it's from a contest like "AtCoder Grand Contest" or "Code Festival". I recall a problem "Fine Triplets" from AtCoder Beginner Contest 175? No, ABC 175 D is "Moving Piece". Maybe it's from "AtCoder Regular Contest"? Let me think. There is a problem "Triplet" from Codeforces? Not sure.

Alternatively, maybe the intended solution is O(N sqrt(M)) using the fact that for each element, we can iterate over divisors of something? No.

Wait, there is a known algorithm for counting 3-term arithmetic progressions in O(N sqrt(M)) time: For each a, we can iterate over d such that d divides something? No.

Let's consider the following: For each a, we can consider the set of differences d = b - a where b in S, b > a. Then c = 2b - a = a + 2d. We want to check if a + 2d in S. So for each a, we want to check for each d in D_a (the set of differences from a to larger elements), whether a+2d in S. The size of D_a is the number of elements in S greater than a. Sum of |D_a| is O(N^2). But we can use the fact that if a+2d is in S, then d = (c-a)/2. So for each pair (a, c) with a < c and same parity, we check if (a+c)/2 in S. This is still O(N^2) pairs.

But maybe we can use a hash set to store S, and for each a, we can iterate over c in S with c > a, and check if (a+c) even and (a+c)//2 in S. This is O(N^2). To speed up, we can group by parity? Still O(N^2).

What if we use the fact that the values are bounded and we can use a bitset? For each a, we can compute the set of possible B = (a + c)/2 for c in S, c > a. This is not easy.

Another idea: Since M=10^6, we can use a boolean array and for each d, we can mark the positions. But we need to count for each d the number of a such that a, a+d, a+2d are in S. This is like a 3-term pattern. We can use the following: For each d, we can compute the set of a such that a and a+d are in S. Let A_d = {a : a in S, a+d in S}. Then for each a in A_d, we need to check if a+2d in S. So we need to count the number of a in A_d such that a+2d in S. We can compute A_d efficiently? The number of d is up to M. For each d, we can find A_d by iterating over a in S and checking if a+d in S. This is O(N) per d, total O(NM). Not good.

But we can use the fact that the number of d for which |A_d| is large is small. Actually, the sum over d of |A_d| is the number of pairs (a, a+d) in S, which can be O(N^2). So not helpful.

Wait, maybe we can use the following: For each a, we can iterate over multiples of something? No.

Let's think about the FFT solution again. It is the standard way to count 3-term APs. In competitive programming, the intended solution for this type of problem (counting 3-term APs in a set with bounded values) is indeed using FFT or convolution. For example, in Codeforces, there is a problem "Arithmetic Progression" where you need to count the number of APs, and the solution uses FFT. The constraints are similar: N up to 10^5 or 10^6, values up to 10^5 or 10^6. So FFT is the way.

In Python, using numpy is the only way to pass. If the judge doesn't support numpy, we might need to use PyPy and implement FFT in pure Python? That would be too slow. So likely numpy is allowed, or the problem is from a contest where Python is not the intended language (like C++). The user asked to solve the problem, and the format is just to enclose the code. I can write the code using numpy. If the judge doesn't have numpy, the code will fail, but that's the best we can do.

However, I recall that in some AtCoder contests, they have a separate environment for Python and numpy is not available. But there is a trick: we can use the built-in `array` module and implement FFT using the `cmath` module? That would be slow.

Wait, there is another approach: Use the fact that the number of triplets is sum_{d} (number of a with a, a+d, a+2d in S). We can compute this by iterating over d from 1 to M, and for each d, we iterate over a from 1 to M-2d, and check if present[a], present[a+d], present[a+2d]. This is O(M^2) which is 10^12, too slow. But we can optimize by noting that for a fixed d, the condition is present[a] & present[a+d] & present[a+2d]. This is like a 3-term pattern. We can use the convolution of present with itself to get pairs, but we need triples.

Alternatively, we can use the following: Let f[x] = 1 if x in S else 0. Then the number of triplets is sum_{x,y} f[x] f[y] f[2y-x]? Not exactly.

What about using the "difference set"? For each d, we want to count the number of x such that x and x+d are in S, and then check if x+2d in S. We can precompute for each x, the list of d such that x+d in S. This is the adjacency list. The total number of edges is the number of pairs. In the worst case, it's N^2/2. So no.

Maybe we can use a different algorithm: Since N=10^6, we can use a "blocking" technique. Divide the range [1, M] into blocks of size B. For each block, we can process? Not sure.

Given the time, I think the FFT solution with numpy is the most straightforward and likely intended (if Python is used). I will write the code using numpy.

But to be safe, I can also implement a version that uses `numpy.fft` and falls back to pure Python if numpy is not available? But pure Python FFT for size 1M is too slow. So I will just use numpy.

Wait, there is also the possibility of using `pyfftw` or `scipy`, but numpy is standard.

Let's write the code.

```python
import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    S = np.array([int(next(it)) for _ in range(N)], dtype=np.int64)
    max_val = int(S.max())
    L = 1 << (2 * max_val).bit_length()
    f = np.zeros(L, dtype=np.float64)
    f[S] = 1.0
    F = np.fft.rfft(f)
    h = np.fft.irfft(F * F, n=L)
    h = np.rint(h).astype(np.int64)
    present = np.zeros(L, dtype=bool)
    present[S] = True
    ans = 0
    # Iterate over even s up to 2*max_val
    # We can vectorize this: for s even, we need present[s//2] and h[s].
    # Create an array of s indices: s = np.arange(2, 2*max_val+1, 2)
    s = np.arange(2, 2*max_val+1, 2, dtype=np.int64)
    # Get h[s] and present[s//2]
    h_s = h[s]
    pres = present[s // 2]
    # For each s, if pres, add (h_s - 1) // 2
    mask = pres
    # Ensure h_s is integer
    h_s_int = h_s[mask]
    # We need to add (h_s_int - 1) // 2
    # Note: h_s_int is numpy int64, (h_s_int - 1) // 2 works.
    ans = np.sum((h_s_int - 1) // 2)
    print(int(ans))

if __name__ == "__main__":
    main()
```

But wait: `f[S] = 1.0` where S is a numpy array. That works because S is an array of indices. But we need to make sure S is within bounds. Yes.

Also, `present = np.zeros(L, dtype=bool)`, then `present[S] = True` works.

Now, the loop: `s = np.arange(2, 2*max_val+1, 2)`. If max_val is large, 2*max_val might be up to 2e6. np.arange is fine.

`h_s = h[s]` gives the convolution values at even indices. Since h is float64, we already converted to int64? Actually, we did `h = np.rint(h).astype(np.int64)`. So h is int64. Then h_s is int64.

Then `mask = pres` is a boolean array. `h_s_int = h_s[mask]` is int64.

Then `ans = np.sum((h_s_int - 1) // 2)`. This sums the number of pairs. This is correct.

But we need to be careful: `h_s` is the convolution value at s. It counts ordered pairs. So (h_s - 1) // 2 is correct for the number of unordered pairs with a < c. Since we only consider s where s/2 in S, the pair (s/2, s/2) is present, so we subtract 1. The remaining is even. So integer division by 2 is fine.

Edge case: what if h_s is 0? Then (0-1)//2 = -1 in Python integer division? In numpy, integer division of negative numbers? Actually, numpy integer division is floor division? Let's check: In numpy, for int64, (-1)//2 = -1. But h_s should be at least 1 if s/2 in S, because the pair (s/2, s/2) is always present. So h_s >= 1. So (h_s - 1) >= 0. So no negative.

But what if due to FFT error, h_s is slightly less than 1? For example, if h_s should be 1 but due to floating point error it becomes 0.9999, then np.rint(h) might round to 1. But if it rounds to 0? np.rint rounds to nearest integer, so 0.5 rounds to 0 or 1? Actually, np.rint rounds to the nearest even integer for .5 cases. But for 0.9999, it rounds to 1. For 0.4999, it rounds to 0. The error in FFT should be less than 0.1 for values up to 1e6. So it should be safe. But to be extra safe, we can add a small epsilon? Not needed.

Also, note that `h` is the convolution of f with f. The maximum value of h is N, which is up to 1e6. The relative error in FFT is small. So rounding is fine.

Now, memory: `f` is float64 of size L. `F` is complex128 of size L//2+1. `h` is float64 of size L. So total memory is about 3*L*8 bytes = 24MB. Fine.

Time: FFT on size 1M takes about 0.1-0.2 seconds in numpy. The rest is negligible.

But we need to be careful with reading input. `sys.stdin.buffer.read().split()` for N=1e6 gives about 8MB of data, which is fine.

Now, what if max_val is 0? Not possible since S_i >=1.

What if N=1? Then no triplets. Our code: max_val = S[0], L = 1 << (2*max_val).bit_length(). f[S]=1.0. FFT. h[s] will be 1 for s=2*max_val. But s=2 is even? s=2*max_val. If max_val=1, s=2. present[1]=True. Then h_s[0] = 1. (1-1)//2 = 0. ans=0. Correct.

So the code seems correct.

One more thing: The problem says "distinct positive integers". So no duplicates.

Now, is there any other nuance? The triplet (A,B,C) is ordered? The problem says (A, B, C) with A < B < C. So each triplet is a set of three elements with B-A = C-B. So order is determined by the values. So we count each set once. Our method counts each unordered pair {A,C} with A<C, and checks if B=(A+C)/2 is in S and A<B<C. Since A<C and B is the average, A<B<C automatically if B in S. So we are counting each triplet exactly once. Good.

Now, the code using numpy. I'll write it cleanly.

But wait: The problem might be from a contest where Python is not allowed or numpy is not available. Is there a pure Python solution that is fast enough? Let's think.

Pure Python solution using hash set and iterating over pairs with pruning? Not possible for N=1e6.

What if we use PyPy and implement a simple FFT? There is a library `numpy` for PyPy? Not standard.

Alternatively, we can use the `cmath` module and implement a recursive FFT? That would be too slow for 1M points.

Maybe we can use the `array` module and the `struct` module to do bit-level operations? No.

What about using the built-in `pow` for NTT? We can implement NTT in Python. For modulus 998244353, we can do NTT. The size needed is a power of 2. We need a prime like 998244353, which is 119 * 2^23 + 1, so it supports up to 2^23. Our max size is 2^21, so it's fine. We can implement NTT in pure Python. But NTT in pure Python is also slow because of the modular arithmetic overhead. However, it might be fast enough if we use loops efficiently? Let's estimate: NTT of size 1M has about 1M * 21 stages = 21M modular multiplications. Each modular multiplication in Python is a function call, which is slow. 21M operations in Python might take 20-30 seconds. Too slow.

But we can use PyPy which is faster for loops? PyPy might handle 20M operations in a few seconds? Possibly. But it's risky.

Given the constraints, the intended solution for Python might be different. Let's search for "Fine Triplets" problem. I recall a problem from AtCoder: "Fine Triplets" maybe from "AtCoder Grand Contest 044"? No. Let me think. There is a problem "Triplet" from Codeforces Round. But "Fine Triplets" might be from "AtCoder Beginner Contest 191"? No, ABC 191 F is "GCD or MIN". Not that.

Maybe it's from "AtCoder Regular Contest 108"? ARC 108 C is "Triangular Relationship". Not that.

Wait, I remember a problem "Fine Triplets" from "AtCoder Library Practice Contest"? No.

Let's search my memory: There is a problem "Fine Triplets" from "JOI" or "PCK"? Not sure.

Alternatively, I can think of a solution that works in O(N sqrt(M)) by using the fact that for each a, the number of d we need to check is limited if we consider that a+2d must be in S. We can precompute for each a, the list of elements in S greater than a. But that's O(N^2).

Wait, there is a known solution: For each a, we can iterate over possible d up to sqrt(M) or something? No.

Another idea: Use the fact that the number of triplets is the sum over b of (number of a < b with 2b-a in S). For each b, we can count this by iterating over a in S with a < b. But we can use a "difference array" or "binary indexed tree" if we process b in increasing order. As we increase b, we add the new element b to a data structure. For each new b, we want to count a in the current set such that 2b-a is in the future set. But the future set is not known. However, we can precompute the entire set. For a fixed b, we want to count a in S, a < b, such that 2b-a in S. This is equivalent to: for each a in S with a < b, check if 2b-a in S. We can do this by iterating over a in S, a < b, but that's O(N^2). But we can do it in reverse: for each c in S with c > b, check if 2b-c in S and 2b-c < b. This is also O(N^2).

What if we use a hash set and for each b, we iterate over multiples? For example, for each b, we consider d from 1 to (M-b)/2, but we only check if b-d in S and b+d in S. We can speed this up by noting that if b-d is not in S, we skip. But we still iterate over all d.

Wait, we can use the fact that the set S is static. For each b, we can precompute the set of valid d such that b-d in S. That is just the set of elements in S less than b. The number of such d is the number of elements in S less than b. So we are back to O(N^2).

Maybe we can use a "sparse" convolution? There is an algorithm for counting 3-term APs in a set of size N with values up to M in O(N sqrt(M) log M) or something? Not that I know.

Let's think about the constraints again. N=10^6, M=10^6. The total number of possible differences is 10^6. For each difference d, the number of a such that a and a+d are in S can be computed by iterating over a in S and checking if a+d in S. This is O(N) per d, total O(NM). But we can do it faster: we can compute the set of a such that a and a+d are in S by using the fact that a is in S and a+d in S. This is like a graph where each element is connected to elements at distance d. We can precompute for each element, the list of elements in S that are larger. But that's O(N^2) edges.

What if we use a "bucket" approach? For each possible difference d, we want to find all a such that a and a+d are in S. We can do this by iterating over all x in S, and for each x, for each y in S with y > x, d = y-x. This is O(N^2). Not good.

Maybe the problem has a different intended solution: Since N is up to 10^6, and S_i up to 10^6, the answer can be computed in O(N log N) using a Fenwick tree? Let's see: For each a, we can consider c = a + 2d. For each a, we can iterate over d such that a+2d in S. That is, for each a, we look at elements in S greater than a, and for each such c, we check if (a+c)/2 in S. We can do this by, for each a, iterating over c in S with c > a, and checking if (a+c) even and (a+c)//2 in S. This is O(N^2). But we can use a hash set to check the middle. The inner loop is just a hash set lookup. So the total number of operations is the number of pairs (a,c) with a < c. This can be up to N^2/2 = 5e11. Too slow.

But wait: If we only consider pairs (a,c) such that (a+c)/2 is an integer, that's half of the pairs. Still O(N^2).

What if we use the fact that the values are bounded? We can use a boolean array. For each a, we can iterate over c in S with c > a, and check if (a+c) even and present[(a+c)//2]. The lookup in a boolean array is O(1). So the time is proportional to the number of pairs. In the worst case, the number of pairs is 5e11, which is too slow.

But maybe the number of pairs is small in practice? The problem is to solve it for all cases, so worst case must be handled.

Is there a way to reduce the number of pairs? We can group by the middle element. For each B, we want to count pairs (A,C) with A < B < C, A and C in S, and A + C = 2B. This is equivalent to: for each B, count the number of A in S with A < B such that 2B - A in S. This is the same as before.

What if we use a "difference" trick: For each A, we can compute 2B - A. Not helpful.

Let's think about the FFT solution again. It is the only one that seems to handle the worst case in O(M log M) time. In competitive programming, Python solutions for such problems often use numpy. For example, in Codeforces, many problems with N=10^5 and FFT are solved with numpy in Python. So it's plausible.

I will proceed with the numpy solution. I'll make sure to handle the input efficiently and avoid unnecessary memory.

One more optimization: We can use `np.fft.rfft` and `np.fft.irfft` as above.

Let's test the code with the sample inputs mentally.

Sample 1: N=5, S=[8,3,1,5,2]. max_val=8. L=1<<(16).bit_length()=32. f[1]=f[2]=f[3]=f[5]=f[8]=1. FFT. h[2]=1, h[4]=3, h[6]=3, h[8]=2, h[10]=3, h[16]=1. s=2,4,6,8,10,12,14,16. present[s//2]: s=2->1 yes, s=4->2 yes, s=6->3 yes, s=8->4 no, s=10->5 yes, s=12->6 no, s=14->7 no, s=16->8 yes. For s=2: h=1, (1-1)//2=0. s=4: h=3, (3-1)//2=1. s=6: h=3, (3-1)//2=1. s=10: h=3, (3-1)//2=1. s=16: h=1, (1-1)//2=0. Sum=3. Correct.

Sample 2: N=7, S=[300000,100000,499998,499999,200000,400000,500000]. max_val=500000. L=1<<(1000000).bit_length()=2^20=1048576. The code should work.

Sample 3: N=10, S=[13,1,16,15,12,4,7,10,2,19]. max_val=19. L=1<<(38).bit_length()=64. Works.

Now, potential issues: If max_val is large, 2*max_val might overflow in Python? No, Python int is arbitrary precision. In numpy, the size L is int, which is fine.

Another issue: `f[S] = 1.0` where S is a numpy array of int64. This works if S elements are within bounds. Yes.

But wait: `S` is a numpy array created from a list comprehension. That list comprehension `int(next(it)) for _ in range(N)` might be slow for N=1e6. We can use `np.fromiter` or just read into a list. But it's okay.

We can read the entire file and split, then map to ints. That's fast.

Now, is there any risk of memory error? f is float64 of size L. If L=2^21=2097152, that's 16MB. F is complex128 of size L//2+1 = 1048577, that's 16MB. h is float64 of size L, 16MB. Total 48MB. That's fine.

But note: `np.fft.rfft(f)` returns a complex array of size L//2+1. Multiplying F*F creates a new array of size L//2+1. Then `np.fft.irfft(..., n=L)` creates a float array of size L. So we have f, F, product, h. That's 4 arrays: f (16MB), F (16MB), product (16MB), h (16MB) = 64MB. Still okay.

We can save memory by doing in-place operations? Not easily with numpy.

But 64MB is fine.

Now, what if max_val is small? Say max_val=1, L=4, arrays are tiny.

So the code is robust.

One more thing: The problem says "distinct positive integers". So we don't have to worry about duplicates.

Now, let's write the final code.

```python
import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = np.array(data[1:], dtype=np.int64)
    # Note: S is a numpy array of the remaining numbers. We need to ensure length is N.
    # But if N=0? N>=1.
    max_val = int(S.max())
    L = 1 << (2 * max_val).bit_length()
    f = np.zeros(L, dtype=np.float
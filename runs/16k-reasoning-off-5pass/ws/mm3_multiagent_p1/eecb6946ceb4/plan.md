We need to count arithmetic progressions of length 3 within a set of distinct integers. Since N and values are up to 1e6, we can store membership in a boolean array (or hash set). For each pair (A, B) with A < B, compute the common difference d = B - A, then check if C = B + d exists in the set. To avoid double counting, we only consider pairs where A is the smallest element of the triplet, i.e., we iterate over all A in S, then over all B in S with B > A, and count when C = B + (B - A) is present. Complexity O(N^2) is too slow; we need a smarter approach.

Better approach: For each element B in S, iterate over possible differences d such that A = B - d is in S and C = B + d is in S. Since values are bounded by 1e6, we can iterate over all possible d up to max(S). For each B, we can check multiples: for d = 1..maxV, if B-d in set and B+d in set, count++. This is O(N * maxV) which is too slow (1e12).

Optimal approach: Since S_i ≤ 1e6, we can use a boolean array `present[1e6+1]`. For each element B, we can iterate over d such that both B-d and B+d are present. We can precompute for each value v the list of elements present, but that's still large.

Alternative: For each element A in S, iterate over all possible C > A such that both A and C are in S, and check if the midpoint B = (A + C) / 2 is integer and in S. Since A and C are both in S, we can iterate over all pairs (A, C) with A < C. Number of pairs is N*(N-1)/2, up to ~5e11, too many.

We need a linear or near-linear solution. Since values are bounded by 1e6, we can use the fact that the set size is at most 1e6. We can iterate over all possible arithmetic progressions by considering each possible difference d. For a fixed d, the numbers form arithmetic progressions with step d. We can count how many such progressions of length 3 exist within S.

For each d from 1 to maxV, we can scan the boolean array and count consecutive runs of present numbers with step d. Specifically, for each starting position x such that x, x+d, x+2d are all present, that's a triplet. We can count this by iterating x from 1 to maxV - 2d, checking present[x], present[x+d], present[x+2d]. That's O(maxV^2) if we do for all d.

But we can do: for each d, we can iterate over multiples: for k from 0 while k*d <= maxV, check if k*d, (k+1)*d, (k+2)*d are present. However, d can be up to 1e6, and for each d we iterate O(maxV/d) steps. Sum over d of maxV/d is maxV * H(maxV) ≈ 1e6 * 14 ≈ 14e6, which is feasible! Wait, sum_{d=1}^{M} M/d = M * H_M ≈ M * (ln M + gamma). For M=1e6, that's about 14 million. That's acceptable.

But careful: we need to consider all possible triplets (A,B,C) with A<B<C. For a fixed d, the triplet is (x, x+d, x+2d). We need to count x such that all three are in S. So for each d, we iterate x from 1 to M - 2d, and if present[x] and present[x+d] and present[x+2d], count++. Complexity: sum_{d=1}^{M} (M - 2d) ≈ M^2/2, which is 5e11, too large.

Wait, the sum of M/d is about 14e6, but that's for iterating over multiples of d: x = k*d. However, the triplet (x, x+d, x+2d) does not require x to be a multiple of d. For a fixed d, x can be any integer. So we cannot restrict to multiples. So the iteration over x for each d is O(M) per d, leading to O(M^2).

We need a different approach.

Observation: Since S is a set of distinct integers, we can use the following: For each element B in S, we want to count pairs (A, C) such that A < B < C, A and C in S, and B - A = C - B. This is equivalent to A + C = 2B. So for each B, we need to count pairs (A, C) in S with A < B < C and A + C = 2B.

We can iterate over all A in S with A < B, compute C = 2B - A, and check if C is in S and C > B. Since A < B, C = 2B - A > B automatically. So for each B, we iterate over A in S with A < B. That's O(N^2) in worst case.

But we can optimize using the fact that values are bounded. Since S_i ≤ 1e6, we can use a boolean array. For each B, we can iterate over possible A values: A can be any value from 1 to B-1. But we only care about A that are in S. So we can iterate over all A in S with A < B. That's still O(N^2).

Alternative: Since the sum A+C is fixed for a given B, we can use a frequency array. For each B, we want to count pairs (A, C) with A < B < C and A + C = 2B. This is like counting pairs in S that sum to 2B, with one element less than B and one greater than B. We can precompute for each possible sum s, the number of pairs (x, y) in S with x < y and x + y = s. Then for each B, we add the count for sum 2B. However, we need to ensure that x < B < y. If we just count all pairs with sum 2B, some pairs might have both elements on the same side of B. But since x < y, if x < B < y, then x < B and y > B. If x < y < B, then sum < 2B. If B < x < y, sum > 2B. So for sum exactly 2B, the only possibilities are x < B < y or x = B = y (impossible since distinct). So any pair (x, y) with x < y and x + y = 2B must satisfy x < B < y. Because if x < y and x + y = 2B, then x = 2B - y. Since x < y, we have 2B - y < y => 2B < 2y => y > B. Similarly x < B. So indeed, for distinct x, y, x + y = 2B implies x < B < y. So we can simply count for each B the number of pairs (x, y) in S with x < y and x + y = 2B.

Thus, we can precompute for each possible sum s (from 2 to 2*maxV), the number of pairs (x, y) in S with x < y and x + y = s. Then the answer is sum over B in S of pair_count[2B].

How to compute pair_count efficiently? Since S size is up to 1e6 and values up to 1e6, we can iterate over all pairs? That's O(N^2). But we can use the boolean array: for each x in S, we can iterate over y > x in S? Still O(N^2).

But we can use the fact that values are bounded by 1e6. We can use a frequency array (0/1 since distinct). Then for each possible sum s, we can count pairs by iterating over x from 1 to s/2, and if present[x] and present[s-x], increment count. That's O(maxV^2) if we do for all s. But we only need sums that are 2B for B in S. There are at most N such sums. So we can compute pair_count only for those sums.

For each B in S, we need to count pairs (x, y) with x + y = 2B. We can compute this by iterating over x from 1 to B-1, checking if present[x] and present[2B - x]. That's O(B) per B, total O(N * maxV) in worst case, too slow.

But we can precompute for all possible sums using convolution? Since values are small (1e6), we can use FFT to compute the number of ways to pick two elements (with order) that sum to each value. But we need unordered pairs with x < y. Since elements are distinct, we can compute the autocorrelation of the indicator array. Let f[v] = 1 if v in S else 0. Then the convolution g = f * f gives g[s] = sum_{x} f[x] * f[s-x]. This counts ordered pairs (x, y) with x + y = s. Since f[x] and f[y] are 0/1, g[s] counts the number of ordered pairs (x, y) such that x + y = s and both in S. For unordered pairs with x < y, we have g[s] = 2 * (number of unordered pairs with x != y) + (number of x with 2x = s). Since elements are distinct, we don't have x = y unless s is even and x = s/2 is in S, but then it's a single element, not a pair. So for unordered pairs with x < y, the count is g[s] / 2 if s is odd, or (g[s] - f[s/2]) / 2 if s is even. But we need to ensure x < y, which is exactly unordered distinct pairs.

Thus, we can compute g = convolution of f with itself using FFT (or NTT) in O(M log M) where M is next power of two >= 2*maxV. M ~ 2^21 = 2097152, log M ~ 21, so about 21 * 2e6 = 42e6 operations, feasible in Python with numpy FFT? But we need to be careful with integer precision. Since f values are 0/1, g values can be up to N (1e6). Using double precision FFT might have rounding errors. We can use Python's built-in complex FFT and round to nearest integer. Since N is up to 1e6, the maximum g[s] is at most N (if all elements are the same, but they are distinct, so max is 1 for each pair? Actually, if S = {1,2,3,...,N}, then for sum s, the number of pairs is about s/2 for s <= N+1, etc. The maximum g[s] is roughly N/2, which is 5e5. Double precision can represent integers up to 2^53 exactly, so rounding should be safe.

Alternatively, we can avoid FFT by using a smarter iteration. Since we only need pair counts for sums that are 2B for B in S, we can compute them on the fly. For each B, we can iterate over x in S with x < B. But we can speed up by noting that for a fixed B, the pairs (x, 2B-x) are symmetric. We can iterate over x from 1 to B-1, but only check if x is in S. Since S is a set, we can store it as a boolean array. Then for each B, we iterate x from 1 to B-1, and if present[x] and present[2B-x], count++. The total work is sum_{B in S} (B-1). In worst case, S contains all numbers from 1 to 1e6, so sum B is about 5e11, too large.

But we can iterate over x in S instead: for each x in S, we can find B such that 2B = x + y for some y in S. That is, for each pair (x, y) with x < y, we can compute B = (x+y)/2, and if B is integer and in S, increment count. This is exactly counting triplets. So we are back to O(N^2).

We need a sub-quadratic solution. Since max value is 1e6, we can use the fact that the number of pairs (x, y) with x < y and x + y = s is at most s/2. For each s, we can compute the count by iterating x from 1 to s/2. The total work over all s is sum_{s=2}^{2M} s/2 = O(M^2). But we only need s = 2B for B in S. There are at most N such s. For each such s, we need to count pairs. We can compute pair_count[s] by iterating x from 1 to s/2, checking present[x] and present[s-x]. The total work is sum_{B in S} B. If S is dense, this is O(M^2). But if S is sparse, it's O(N * maxV) which is still large.

Wait, we can compute pair_count for all s using a different method: For each x in S, we can iterate over y in S with y > x. That's O(N^2). Not good.

Alternative: Since M is only 1e6, we can use a bitset representation. Represent S as a bitset of length M. Then for each possible difference d, we can shift the bitset and perform bitwise AND to find positions where both x and x+d are present. Then we can shift again to find x, x+d, x+2d. This is similar to the convolution approach but using bitset operations. In Python, we can use integers as bitsets. Since M=1e6, we need about 1e6 bits = 125KB per bitset. We can represent the set as a Python integer where bit i is set if i+1 is present (since values start at 1). Then for each d, we can compute (mask >> d) & mask to get positions where both x and x+d are present. Then we can compute ((mask >> d) & mask) >> d & mask to get positions where x, x+d, x+2d are present. Then we can count the number of set bits in that result. The number of set bits in a Python integer can be counted using bit_count() (Python 3.10+). The total work: for each d from 1 to M, we perform a few bitwise operations and a bit_count. The bitwise operations on integers of size ~1e6 bits are O(size) = O(M/word_size) = O(M/64) ≈ 15625 operations per d. For M=1e6, that's 1e6 * 15625 = 1.56e10 operations, which is too slow in Python.

But we can limit d to only those differences that are possible? Actually, we need to consider all d up to M. However, we can note that for large d, the number of triplets is small. But we still need to iterate over d.

We can use the convolution approach with FFT. That seems the most promising. Let's outline:

1. Read N and the list S.
2. Determine maxV = max(S).
3. Create a boolean array f of size maxV+1 (or next power of two for FFT). Actually, we need size at least 2*maxV for convolution.
4. Set f[v] = 1 for v in S.
5. Compute convolution g = f * f using FFT (numpy.fft or similar). Since we need integer counts, we can use FFT with real numbers and round.
6. For each s from 2 to 2*maxV, compute unordered pair count:
   - If s is odd: pair_count[s] = g[s] // 2.
   - If s is even: pair_count[s] = (g[s] - f[s//2]) // 2.
   Because g[s] counts ordered pairs (x, y) with x+y=s. For x != y, each unordered pair is counted twice. For x = y, it's counted once, but since elements are distinct, x=y only if s is even and s/2 is in S. In that case, f[s/2] is 1, and it contributes 1 to g[s] (since x=y). So we subtract that and then divide by 2.
7. Then answer = sum_{B in S} pair_count[2*B].
8. Print answer.

Complexities: O(M log M) for FFT, O(N) for summation. M ~ 2^21 = 2097152, so FFT is fast.

We need to be careful with memory: f array of size M, g array of size M. Using numpy, we can do this efficiently.

Alternatively, we can use the pyfft library or implement FFT ourselves. But using numpy is easiest.

However, the problem constraints: N up to 1e6, values up to 1e6. Using numpy FFT on arrays of size 2^21 = 2097152 is fine. The convolution result g will have integer values up to N. We need to round to nearest integer.

Let's test with sample inputs.

Sample 1: S = {8,3,1,5,2}. maxV=8. M=16 (next power of two >= 16). f = [0,1,1,1,0,1,0,0,1] (indices 0..8). Actually, we need size at least 2*maxV = 16. So f length 16. f[1]=1, f[2]=1, f[3]=1, f[5]=1, f[8]=1. Convolution g = f * f. Compute manually? Let's trust the algorithm.

We can also avoid FFT by using a different approach: Since maxV is 1e6, we can use a dictionary to store the set, and for each B in S, we can iterate over possible A in S with A < B. But we can break early if B is large? Not really.

Another approach: Since the set is distinct, we can sort S. Then for each pair (i, j) with i < j, we can compute the midpoint and check if it's in the set. But that's O(N^2).

Given the constraints, FFT is the standard solution for counting arithmetic progressions or similar problems. However, we need to ensure that the FFT-based convolution counts pairs correctly.

Let's verify the pair count formula.

Let f[v] = 1 if v in S else 0.
Convolution g[s] = sum_{x=0}^{s} f[x] * f[s-x].
Since f[x] is 0 or 1, g[s] counts the number of ordered pairs (x, y) such that x+y=s and both in S.
We want the number of unordered pairs {x, y} with x < y and x+y=s.
For each unordered pair with x != y, there are two ordered pairs: (x, y) and (y, x). So they contribute 2 to g[s].
If x = y, then s = 2x, and it contributes 1 to g[s] (since f[x]*f[x] = 1). But since elements are distinct, x = y only if x is in S and we count it as a pair? But we need x < y, so we exclude x=y. So for s even, if s/2 is in S, we subtract 1 from g[s] to remove the self-pair, then divide by 2.
Thus:
If s is odd: unordered_pairs = g[s] // 2.
If s is even: unordered_pairs = (g[s] - f[s//2]) // 2.

Then for each B in S, we add unordered_pairs[2B] to the answer.

Check with sample 1:
S = {1,2,3,5,8}. maxV=8.
f: index 0..8: f[0]=0, f[1]=1, f[2]=1, f[3]=1, f[4]=0, f[5]=1, f[6]=0, f[7]=0, f[8]=1.
Compute g manually for small s:
s=2: f[0]*f[2] + f[1]*f[1] + f[2]*f[0] = 0 + 1 + 0 = 1. So g[2]=1. s even, f[1]=1. unordered = (1-1)//2 = 0.
s=3: f[0]*f[3] + f[1]*f[2] + f[2]*f[1] + f[3]*f[0] = 0 + 1 + 1 + 0 = 2. s odd, unordered = 2//2 = 1. This corresponds to pair (1,2).
s=4: f[0]*f[4] + f[1]*f[3] + f[2]*f[2] + f[3]*f[1] + f[4]*f[0] = 0 + 1 + 1 + 1 + 0 = 3. s even, f[2]=1. unordered = (3-1)//2 = 1. Pair (1,3).
s=5: f[0]*f[5] + f[1]*f[4] + f[2]*f[3] + f[3]*f[2] + f[4]*f[1] + f[5]*f[0] = 0 + 0 + 1 + 1 + 0 + 0 = 2. s odd, unordered = 1. Pair (2,3).
s=6: f[0]*f[6] + f[1]*f[5] + f[2]*f[4] + f[3]*f[3] + f[4]*f[2] + f[5]*f[1] + f[6]*f[0] = 0 + 1 + 0 + 1 + 0 + 1 + 0 = 3. s even, f[3]=1. unordered = (3-1)//2 = 1. Pair (1,5).
s=7: f[0]*f[7] + f[1]*f[6] + f[2]*f[5] + f[3]*f[4] + f[4]*f[3] + f[5]*f[2] + f[6]*f[1] + f[7]*f[0] = 0+0+1+0+0+1+0+0 = 2. s odd, unordered = 1. Pair (2,5).
s=8: f[0]*f[8] + f[1]*f[7] + f[2]*f[6] + f[3]*f[5] + f[4]*f[4] + f[5]*f[3] + f[6]*f[2] + f[7]*f[1] + f[8]*f[0] = 0+0+0+1+0+1+0+0+0 = 2. s even, f[4]=0. unordered = 2//2 = 1. Pair (3,5).
s=9: f[1]*f[8] + f[2]*f[7] + f[3]*f[6] + f[4]*f[5] + f[5]*f[4] + f[6]*f[3] + f[7]*f[2] + f[8]*f[1] = 1+0+0+0+0+0+0+1 = 2. s odd, unordered = 1. Pair (1,8).
s=10: f[2]*f[8] + f[3]*f[7] + f[4]*f[6] + f[5]*f[5] + f[6]*f[4] + f[7]*f[3] + f[8]*f[2] = 1+0+0+1+0+0+1 = 3. s even, f[5]=1. unordered = (3-1)//2 = 1. Pair (2,8).
s=11: f[3]*f[8] + f[4]*f[7] + f[5]*f[6] + f[6]*f[5] + f[7]*f[4] + f[8]*f[3] = 1+0+0+0+0+1 = 2. s odd, unordered = 1. Pair (3,8).
s=13: f[5]*f[8] + f[8]*f[5] = 1+1=2. s odd, unordered = 1. Pair (5,8).
s=16: f[8]*f[8] = 1. s even, f[8]=1. unordered = (1-1)//2 = 0.

Now, for each B in S, we need unordered_pairs[2B]:
B=1: 2B=2 -> 0
B=2: 2B=4 -> 1
B=3: 2B=6 -> 1
B=5: 2B=10 -> 1
B=8: 2B=16 -> 0
Sum = 3. Correct.

So the algorithm works.

Now, we need to implement it efficiently in Python.

Implementation steps:

1. Read N.
2. Read list S.
3. Compute maxV = max(S).
4. Determine size for FFT: size = 1
   while size < 2 * maxV + 1:
       size *= 2
   Actually, we need size >= 2*maxV + 1 because convolution of two arrays of length L produces array of length 2L-1. So if we have f of length maxV+1 (indices 0..maxV), we need size >= 2*(maxV+1) - 1 = 2*maxV+1. So we can set size = 1
   while size < 2*maxV + 1:
       size <<= 1
5. Create numpy array f of length size, dtype=float64. Set f[v] = 1 for v in S.
6. Compute FFT: F = np.fft.fft(f)
7. Compute convolution: G = F * F
8. Inverse FFT: g = np.fft.ifft(G).real
9. Round g to nearest integer: g = np.round(g).astype(np.int64)
10. Now, for each B in S, compute sum = 2*B.
    If sum is odd: count = g[sum] // 2
    If sum is even: count = (g[sum] - (1 if sum//2 in S else 0)) // 2
    Add to answer.
11. Print answer.

We need to be careful with indexing: f array index corresponds to value. Since values start at 1, we can set f[0]=0 always. So f length should be at least maxV+1. But for FFT, we pad to size.

We need to check if sum is within bounds of g array. Since size >= 2*maxV+1, and sum = 2*B <= 2*maxV, so sum < size. So it's safe.

Potential issues: FFT precision. Since f values are 0/1, g values are integers up to N. With double precision, rounding should be accurate. However, for large N, the convolution might have values up to N, which is 1e6. Double precision can represent integers up to 2^53 exactly, so no problem.

We should also consider that numpy.fft might be slow for size 2^21? Actually, 2^21 is about 2 million, FFT is O(N log N) with N=2e6, log N=21, so about 42 million operations, which is fast in C (numpy uses C under the hood). Should be fine.

Alternative: Use pyfft or implement FFT in Python? Not necessary.

We need to ensure we don't use too much memory. f and g arrays of size 2e6 with float64: 16 MB each. F and G complex: 32 MB each. Total maybe 100 MB, which is okay.

We can also use the fact that f is real, so we can use rfft to save memory and time. But for simplicity, we can use fft.

Let's write the code.

But wait: The problem constraints say N up to 1e6, S_i up to 1e6. So maxV up to 1e6. Then size = 2^21 = 2097152. That's fine.

We need to read input efficiently. Use sys.stdin.buffer.read.

Let's code.

One more thing: We need to handle the case where sum is even and sum//2 is in S. We can check using a set or boolean array. Since we already have f array, we can check f[sum//2] == 1.

Now, let's test with sample inputs.

Sample 1: N=5, S=[8,3,1,5,2]. maxV=8. size=16 (since 2*8+1=17, next power of 2 is 32? Actually, 2*8+1=17, next power of 2 is 32. But we can use size=32. However, we can also use size=16 if we are careful? No, convolution of length 9 arrays (indices 0..8) requires size at least 17. So we need size >= 17. Next power of 2 is 32. So size=32. That's fine.

Sample 2: N=7, S=[300000,100000,499998,499999,200000,400000,500000]. maxV=500000. size = 2^20 = 1048576? Actually, 2*500000+1=1000001, next power of 2 is 1048576 (2^20). That's fine.

Sample 3: N=10, S=[13,1,16,15,12,4,7,10,2,19]. maxV=19. size=32.

All good.

Now, let's write the code.

We need to import numpy. But sometimes numpy is not allowed in competitive programming? Usually it is. But we can also implement FFT ourselves to avoid dependency. However, the problem likely expects an O(N sqrt N) or O(N log N) solution. Since N is up to 1e6, O(N log N) is fine. Using numpy is acceptable.

But to be safe, we can implement FFT in Python using complex numbers. However, that might be slower. Let's stick with numpy.

We need to ensure that the code runs within time limit. Using numpy FFT on 2e6 size should be fast (< 1 second).

Let's write the code.

Potential optimization: Since f is real, we can use np.fft.rfft and irfft to save memory and time. But for simplicity, we can use fft.

We need to be careful with rounding: np.round might return float, so we cast to int.

Let's code.

We'll also handle the case where sum is even and sum//2 is in S by checking f[sum//2].

Now, let's write the final code.

We'll structure as:

import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = list(map(int, data[1:]))
    maxV = max(S)
    size = 1
    while size < 2 * maxV + 1:
        size <<= 1
    f = np.zeros(size, dtype=np.float64)
    for v in S:
        f[v] = 1.0
    F = np.fft.fft(f)
    G = F * F
    g = np.fft.ifft(G).real
    g = np.round(g).astype(np.int64)
    ans = 0
    for B in S:
        s = 2 * B
        if s % 2 == 1:
            ans += g[s] // 2
        else:
            ans += (g[s] - f[s//2]) // 2
    print(ans)

if __name__ == "__main__":
    main()

But wait: f[s//2] is a float. We need to check if it's 1.0. Since we set f[v]=1.0 for v in S, and 0.0 otherwise, we can check f[s//2] > 0.5 or use int. But after rounding, g is int, but f is still float. We can convert f to int as well, or just check f[s//2] == 1.0. Since we set exactly 1.0, it's fine.

Alternatively, we can create a boolean array present = [False]*(maxV+1) and set present[v]=True. Then use that for checking. But we already have f. We can use f[s//2] > 0.5.

But note: f is float, and after FFT, we don't modify f. So f[s//2] is still 1.0 or 0.0. So we can check f[s//2] == 1.0.

However, due to floating point, it might be exactly 1.0. So it's safe.

But we need to be careful: s//2 is integer. Since s is even, s//2 is integer. We need to ensure that index is within bounds. s//2 <= maxV, so it's within f array.

Now, let's test with sample inputs.

We'll run mentally:

Sample 1: as above, ans=3.

Sample 2: Let's compute quickly? Not necessary.

Sample 3: ans=10.

Seems correct.

But we should consider if there are any pitfalls: The FFT convolution might have small errors due to floating point. For example, g[s] might be 2.999999999 instead of 3. np.round will round to 3. So it's fine.

One more thing: The convolution result g array has length size. We only need indices up to 2*maxV. So it's fine.

Now, we need to ensure that the code is efficient. Creating f array with zeros and then setting values is O(size + N). FFT is O(size log size). Summing over S is O(N). Total time should be fine.

We can also use the fact that f is sparse? Not needed.

Potential issue: If maxV is small, size is small. If maxV is 1e6, size is 2^21=2097152, which is fine.

Now, let's write the final code with proper imports and main function.

We'll also add a check for N=0? But N>=1.

Now, we need to output the answer as integer.

Let's write the code.

We'll also consider using sys.setrecursionlimit if needed, but not necessary.

Now, let's produce the final answer.### PLAN
We need to count arithmetic progressions of length 3 (fine triplets) in a set of distinct integers. For each element B in the set, we count pairs (A, C) with A < B < C and A + C = 2B. This is equivalent to counting unordered pairs (x, y) in the set with x < y and x + y = 2B. We can compute the number of such pairs for all possible sums using convolution of the indicator array of the set. Using FFT, we compute the convolution g[s] = sum_{x} f[x] * f[s-x], where f[v] = 1 if v is in the set. Then for each B, we add the number of unordered pairs with sum 2B: if 2B is odd, count = g[2B] // 2; if even, count = (g[2B] - f[2B//2]) // 2. Summing over all B gives the answer. Complexity is O(M log M) where M is the next power of two ≥ 2*max(S)+1, which is feasible for max(S) ≤ 10^6.
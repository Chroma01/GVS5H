We need sum over permutations P of (1..N) of f(P) where f(P) is the concatenation of decimal representations of P_i. Each permutation contributes a number whose digits are the concatenation of the numbers 1..N in some order. The sum can be expressed as sum over positions in the final concatenated string of (digit value) * 10^{remaining positions}. Since each number appears exactly once in each position across all permutations, we can compute the contribution of each number k when placed at a certain rank r (1-indexed) in the permutation.

For a fixed number k, its decimal length L_k = floor(log10(k)) + 1. When k is placed at position r in the permutation, the digits of k occupy L_k positions in the concatenated string. The contribution of k to f(P) is k * 10^{total_digits_after_k}, where total_digits_after_k = sum of lengths of numbers placed after position r.

We sum over all permutations: for each k, sum over r=1..N of (number of permutations where k is at position r) * k * 10^{sum_{j=r+1..N} len(P_j)}.

The number of permutations where k is at position r is (N-1)! (choose the other N-1 numbers arbitrarily). However, the exponent depends on which numbers are after k. So we need to sum over all subsets of size N-r of the remaining numbers, and for each subset compute 10^{sum of lengths of numbers in that subset}. This is a classic combinatorial sum that can be computed using DP over numbers sorted by length, using generating functions.

We can sort numbers 1..N by their length (1-digit, 2-digit, 3-digit, ...). For each length group, we know exactly how many numbers have that length. We need to compute, for each possible total length sum, the number of ways to pick a multiset of numbers (with given multiplicities) that yields that sum, weighted by 10^{sum}. Since we only need the sum over all permutations, we can compute the total contribution using DP that processes numbers in increasing order, maintaining a polynomial where coefficient of x^t is the sum of 10^{sum of lengths} over all subsets of processed numbers that have total length t. Then we multiply by appropriate factorials to account for ordering.

Alternatively, we can compute the sum directly using the formula:
Sum = sum_{k=1..N} k * (N-1)! * sum_{r=0..N-1} (1/10^{something})? Not straightforward.

Better approach: Use the concept of "concatenation sum" which can be computed by considering each digit position. Since N up to 2e5, we need O(N log N) or O(N sqrt(N)) time.

Observation: The sum over all permutations of f(P) can be written as:
Sum = sum_{i=1..N} (contribution of number i when placed at some position).
For each number i, its contribution is i * 10^{L_rest}, where L_rest is the total length of numbers placed after i. Since the numbers after i are a random subset of size N-1 from the remaining numbers, we need the expected value of 10^{L_rest} times (N-1)!.

We can compute the generating function G(x) = sum_{S subset of {1..N}} 10^{sum_{j in S} len(j)} * x^{|S|}. Then the coefficient of x^{m} gives the sum of 10^{sum lengths} over all subsets of size m. Then the contribution of number i is i * (N-1)! * sum_{m=0..N-1} (1/(N-1))? Wait.

Actually, for a fixed i, the set of numbers after i is a subset of size N-r (where r is position of i). The number of permutations where i is at position r and the set after i is a specific subset S of size N-r is (N-1)! / (N-r)!? Let's derive carefully.

Total permutations: N!. For a fixed i and fixed position r, the number of permutations where i is at position r and the set of numbers after i is a specific subset S of size N-r is: choose the order of the N-r numbers in S: (N-r)! ways, and order the remaining r-1 numbers before i: (r-1)! ways. So total (r-1)! * (N-r)! permutations for that specific subset S. Summing over all subsets S of size N-r gives C(N-1, N-r) * (r-1)! * (N-r)! = (N-1)!.

Thus for fixed i and fixed r, the sum over permutations of 10^{sum_{j in S} len(j)} where S is the set after i is: (r-1)! * (N-r)! * sum_{S subset of remaining numbers, |S|=N-r} 10^{sum_{j in S} len(j)}.

But we can also think: total contribution of i = i * sum_{r=1..N} (r-1)! * (N-r)! * sum_{S subset of others, |S|=N-r} 10^{sum_{j in S} len(j)}.

We can compute the inner sum using DP over numbers (excluding i). However, doing this for each i separately is O(N^2). We need a global method.

Alternative: Use linearity of expectation over positions. Consider the concatenated string. The sum over all permutations of f(P) is equal to sum over all digit positions (from left to right) of (digit value) * 10^{remaining digits}. Since each number appears exactly once in each position across all permutations? Not exactly: each number appears in exactly one position per permutation, but across all permutations, each number appears in each position equally often: (N-1)! times.

Thus we can compute the sum as:
Sum = sum_{pos=1..N} (expected digit value at position pos) * 10^{total_digits - sum of lengths of numbers at positions > pos} * (N!).

But the digit value at a position depends on which number occupies that position and which digit of that number is at that position. This seems messy.

Better: Use the generating function approach but compute the total sum directly without iterating over each i.

We can write the sum as:
Sum = sum_{permutation P} sum_{i=1..N} (value of P_i) * 10^{sum_{j=i+1..N} len(P_j)}.

Swap sums: Sum = sum_{i=1..N} sum_{permutation P} (value of P_i) * 10^{sum_{j=i+1..N} len(P_j)}.

For a fixed i (position index), the inner sum is over all permutations. We can compute the sum over permutations of (value of element at position i) * 10^{sum of lengths of elements after position i}.

This is similar to: for each position i, we choose an element x to be at position i, then choose a subset of size N-i from the remaining elements to be after i, and order them. The contribution is x * 10^{sum of lengths of the chosen subset} * (i-1)! * (N-i)!.

Thus:
Sum = sum_{i=1..N} (i-1)! * (N-i)! * sum_{x=1..N} x * sum_{S subset of others, |S|=N-i} 10^{sum_{j in S} len(j)}.

Now, the inner sum over x and S can be combined. For each x, we need the sum over subsets S of the other N-1 elements of size N-i of 10^{sum lengths}. This is like: for each x, we have a set of N-1 numbers (all except x). We need the sum of 10^{sum lengths} over subsets of size N-i.

We can precompute for each possible subset size m the total sum of 10^{sum lengths} over all subsets of size m of the full set {1..N}. Let's denote F(m) = sum_{S subset of {1..N}, |S|=m} 10^{sum_{j in S} len(j)}.

Then for a fixed x, the sum over subsets S of size N-i of the other numbers is: sum_{S subset of {1..N}\{x}, |S|=N-i} 10^{sum lengths}. This is not exactly F(N-i) because we exclude x. However, we can relate it: F(N-i) includes subsets that may or may not contain x. Since we need subsets of size N-i from the N-1 numbers excluding x, we can write:
sum_{S subset of others, |S|=N-i} 10^{sum lengths} = sum_{S subset of all, |S|=N-i} 10^{sum lengths} - 10^{len(x)} * sum_{S subset of all, |S|=N-i-1} 10^{sum lengths} (if N-i-1 >=0). Because subsets of size N-i that do not contain x are exactly subsets of size N-i from the N-1 others. Subsets of size N-i that contain x correspond to subsets of size N-i-1 from the others, multiplied by 10^{len(x)}.

Thus:
sum_{S subset of others, |S|=N-i} 10^{sum lengths} = F(N-i) - 10^{len(x)} * F(N-i-1).

Therefore, the contribution of position i is:
(i-1)! * (N-i)! * sum_{x=1..N} x * (F(N-i) - 10^{len(x)} * F(N-i-1)).

We can compute F(m) for all m=0..N using DP. Since N is up to 2e5, we need an efficient DP.

The DP for F(m): We have numbers 1..N, each with weight w_j = 10^{len(j)}. We need the sum over subsets of size m of the product of weights? Actually 10^{sum lengths} = product over j in S of 10^{len(j)} = product of w_j. So F(m) is the sum of products of weights over subsets of size m. This is exactly the elementary symmetric polynomial of degree m in the variables w_j.

We can compute all F(m) in O(N * max_len) time using DP over numbers grouped by length. Since numbers have lengths from 1 to 6 (since N <= 2e5, max length is 6 for 100000..200000). Actually 2e5 has length 6. So we have at most 6 distinct lengths.

Let cnt[l] = number of integers in [1..N] with length l. For each length l, all numbers have the same weight w_l = 10^l. So we have cnt[l] copies of weight w_l.

We need to compute the elementary symmetric sums of these multiset of weights. This can be done using DP that processes each group: for each length l, we have cnt[l] identical items with weight w_l. The contribution of adding k copies of weight w to the symmetric sums is given by the binomial theorem: (1 + w x)^k = sum_{j=0..k} C(k,j) w^j x^j. So we can update the DP array F[0..N] by convolving with the polynomial (1 + w x)^{cnt[l]}.

Since cnt[l] can be large (up to N), we need to do this efficiently. The total number of distinct lengths is small (at most 6). We can compute the polynomial for each length group using the fact that (1 + w x)^{cnt} can be computed via exponentiation by repeated squaring, but we need to multiply polynomials of degree up to N. However, we only need the final F array after processing all groups. Since the number of groups is small, we can do polynomial multiplication using FFT (NTT) for each group, but N is up to 2e5, so degree is manageable. However, we need to do this modulo 998244353, which is NTT-friendly.

But we can also compute F(m) using a simpler recurrence because the weights are only 6 distinct values. We can use generating functions: The total generating function is product_{l} (1 + w_l x)^{cnt[l]}. We need the coefficients of this polynomial up to degree N. Since the number of distinct w_l is small, we can compute the product by iterating over each l and updating the DP array using the binomial coefficients. For each l, we need to update F'[j] = sum_{k=0..min(j, cnt[l])} C(cnt[l], k) w_l^k F[j-k]. This is a convolution of F with the sequence C(cnt[l], k) w_l^k. Since cnt[l] can be up to 2e5, we can precompute the binomial coefficients for each l using factorials and inverse factorials modulo MOD. Then we can do the convolution in O(N * cnt[l]) which would be too slow if we do it naively for each l (total O(N * sum cnt[l]) = O(N^2)). But we can use FFT to multiply polynomials: the polynomial for group l is P_l(x) = sum_{k=0..cnt[l]} C(cnt[l], k) w_l^k x^k. Then the total F is the coefficient-wise product of these polynomials (convolution). Since there are only up to 6 groups, we can multiply them sequentially using NTT. Each multiplication is between polynomials of degree up to N. The total complexity is O(6 * N log N) which is fine.

Alternatively, we can compute F(m) using a DP that iterates over numbers but uses the fact that many numbers share the same weight. Since the number of distinct weights is small, we can use the formula for multiset: F(m) = sum_{k1+k2+...+kL = m} (product_{l} C(cnt[l], k_l) w_l^{k_l}). This is exactly the coefficient of x^m in product_{l} (1 + w_l x)^{cnt[l]}. So we can compute the product polynomial using NTT.

Steps:
1. Precompute factorials and inverse factorials up to N for binomial coefficients.
2. For each length l from 1 to 6 (or up to max_len), compute cnt[l] and w_l = pow(10, l, MOD).
3. Build polynomial P_l of degree cnt[l]: P_l[k] = C(cnt[l], k) * w_l^k mod MOD for k=0..cnt[l].
4. Multiply all P_l together using NTT to get polynomial F of degree N: F[k] = sum over subsets of size k of product of weights = sum_{S, |S|=k} 10^{sum lengths}.
5. Then compute the answer using the formula:
   Answer = sum_{i=1..N} (i-1)! * (N-i)! * sum_{x=1..N} x * (F(N-i) - w_len(x) * F(N-i-1)) mod MOD.

We need to be careful with indices: F(m) is defined for m=0..N. For m=0, F(0)=1 (empty subset). For m<0, define F(m)=0.

Also, we need to compute sum_{x=1..N} x * w_len(x) * F(N-i-1). Since w_len(x) depends only on the length of x, we can group by length. Let S1 = sum_{x=1..N} x, and S_w[l] = sum_{x with len(x)=l} x. Then sum_{x} x * w_len(x) = sum_{l} w_l * S_w[l].

Similarly, sum_{x} x = S1.

Thus the inner sum over x is: S1 * F(N-i) - (sum_{l} w_l * S_w[l]) * F(N-i-1).

So the total answer is:
Ans = sum_{i=1..N} (i-1)! * (N-i)! * ( S1 * F(N-i) - W * F(N-i-1) ),
where W = sum_{l} w_l * S_w[l].

We can precompute factorials, and also precompute the array of (i-1)! * (N-i)! for i=1..N. Note that (i-1)! * (N-i)! = N! / (i * (N-i+1)?) Actually (i-1)! * (N-i)! = N! / (N choose i-1)? Not exactly. But we can compute it directly.

We need to compute F(m) for all m. Since N up to 2e5, we can compute F via DP using the polynomial multiplication approach.

Implementation details:
- MOD = 998244353, primitive root = 3.
- NTT implementation for convolution.
- Compute factorials fact[0..N], inv_fact[0..N].
- For each length l, compute cnt[l] and the polynomial P_l of length cnt[l]+1.
- Multiply all P_l using NTT: start with F = [1] (polynomial of degree 0). For each l, convolve F with P_l, then truncate to degree N (since we only need up to N). After processing all l, F[k] is the desired sum for subsets of size k.
- Compute S1 = N*(N+1)/2 mod MOD.
- Compute S_w[l] = sum of numbers with length l. For l=1: 1..9, but N may be less than 9. Actually we need to compute for each l the sum of x in [1..N] with len(x)=l. We can compute the range: for l=1: 1..min(9,N); l=2: 10..min(99,N); etc. Sum of arithmetic series.
- Compute W = sum_{l} w_l * S_w[l] mod MOD.
- Compute array A[i] = (i-1)! * (N-i)! mod MOD for i=1..N. We can compute fact[i-1] * fact[N-i] mod MOD.
- Then compute Ans = sum_{i=1..N} A[i] * ( S1 * F[N-i] - W * F[N-i-1] ) mod MOD.
- Ensure to handle F[-1] = 0.

Check with sample N=3:
Numbers: 1 (len1), 2 (len1), 3 (len1). cnt[1]=3, w1=10.
P_1(x) = (1 + 10x)^3 = 1 + 30x + 300x^2 + 1000x^3.
F = [1, 30, 300, 1000].
S1 = 6.
S_w[1] = 1+2+3=6, W = 10*6=60.
Compute A[i]:
i=1: (0)! * (2)! = 1*2=2
i=2: (1)! * (1)! = 1*1=1
i=3: (2)! * (0)! = 2*1=2
Now compute:
i=1: N-i=2, F[2]=300, F[1]=30. Term = 2 * (6*300 - 60*30) = 2*(1800 - 1800)=0.
i=2: N-i=1, F[1]=30, F[0]=1. Term = 1 * (6*30 - 60*1) = 180 - 60 = 120.
i=3: N-i=0, F[0]=1, F[-1]=0. Term = 2 * (6*1 - 60*0) = 2*6=12.
Sum = 0+120+12=132? But sample answer is 1332. Wait, we missed a factor? Let's check.

Our formula gave 132, but expected 1332. There is a factor of 10? Let's re-derive.

The sum over permutations of f(P) is sum_{P} sum_{i=1..N} P_i * 10^{sum_{j>i} len(P_j)}.
We wrote: for fixed position i, contribution = (i-1)! * (N-i)! * sum_{x} x * sum_{S subset of others, |S|=N-i} 10^{sum lengths}.
But is that correct? Let's verify with N=3.

For N=3, permutations:
(1,2,3): f=123 = 1*10^{len(2)+len(3)} + 2*10^{len(3)} + 3 = 1*10^{1+1} + 2*10^1 + 3 = 100 + 20 + 3 = 123.
(1,3,2): 1*10^{1+1} + 3*10^1 + 2 = 100+30+2=132.
(2,1,3): 2*10^{1+1} + 1*10^1 + 3 = 200+10+3=213.
(2,3,1): 2*10^{1+1} + 3*10^1 + 1 = 200+30+1=231.
(3,1,2): 3*10^{1+1} + 1*10^1 + 2 = 300+10+2=312.
(3,2,1): 3*10^{1+1} + 2*10^1 + 1 = 300+20+1=321.
Sum = 1332.

Now compute using our formula for i=1 (first position):
i=1: (0)! * (2)! = 2. sum_{x} x * sum_{S subset of others, |S|=2} 10^{sum lengths}.
For x=1: others are {2,3}, subsets of size 2: only {2,3}, sum lengths = 1+1=2, 10^2=100. So contribution: 1*100=100.
For x=2: others {1,3}, subset {1,3}: sum lengths=2, 10^2=100. Contribution: 2*100=200.
For x=3: others {1,2}, subset {1,2}: 100. Contribution: 3*100=300.
Sum over x = 600. Multiply by 2 = 1200.
But in the actual sum, the contribution from first position across all permutations is: for each permutation, the first element times 10^{sum lengths of rest}. Sum of first elements times 10^{...}:
Permutations:
(1,2,3): 1*100=100
(1,3,2): 1*100=100
(2,1,3): 2*100=200
(2,3,1): 2*100=200
(3,1,2): 3*100=300
(3,2,1): 3*100=300
Sum = 1200. So our formula for i=1 gives 1200, correct.

Now i=2: (1)! * (1)! = 1. sum_{x} x * sum_{S subset of others, |S|=1} 10^{sum lengths}.
For x=1: others {2,3}, subsets of size 1: {2} gives 10^1=10, {3} gives 10. Sum = 20. Contribution: 1*20=20.
x=2: others {1,3}: {1}:10, {3}:10, sum=20, contribution 40.
x=3: others {1,2}: sum=20, contribution 60.
Total sum over x = 120. Multiply by 1 = 120.
Actual contribution from second position: for each permutation, second element times 10^{len of third}:
(1,2,3): 2*10=20
(1,3,2): 3*10=30
(2,1,3): 1*10=10
(2,3,1): 3*10=30
(3,1,2): 1*10=10
(3,2,1): 2*10=20
Sum = 120. Correct.

i=3: (2)! * (0)! = 2. sum_{x} x * sum_{S subset of others, |S|=0} 10^{sum lengths}. S empty, sum lengths=0, 10^0=1. So sum_{x} x * 1 = 6. Multiply by 2 = 12.
Actual contribution from third position: just the third element, sum = 1+2+3+1+2+3? Wait, third elements: 3,2,3,1,2,1 sum = 12. Correct.

Total sum = 1200+120+12 = 1332. So our formula is correct.

Now why did our computed value using F give 132? Let's compute F correctly.
For N=3, all numbers have length 1, w=10. F(m) = sum_{S, |S|=m} 10^{sum lengths} = C(3,m) * 10^m.
So F(0)=1, F(1)=3*10=30, F(2)=3*100=300, F(3)=1000.
S1=6, W=10*6=60.
A[1]=2, A[2]=1, A[3]=2.
i=1: N-i=2, F[2]=300, F[1]=30. Term = 2*(6*300 - 60*30) = 2*(1800-1800)=0. But we expected 1200. So our formula using F gave 0, but actual is 1200. The discrepancy is that we used F(N-i) and F(N-i-1) but we need to account for the fact that the subsets are from the remaining numbers excluding x. Our derivation: sum_{S subset of others, |S|=N-i} 10^{sum lengths} = F(N-i) - 10^{len(x)} * F(N-i-1). Let's test this for i=1, x=1.
F(2) = sum_{S subset of all, |S|=2} 10^{sum lengths} = 300.
10^{len(1)} * F(1) = 10 * 30 = 300.
So F(2) - 10*F(1) = 0. But the actual sum over subsets of {2,3} of size 2 is 100. So the formula is wrong.

The error: F(N-i) includes subsets that may contain x. The subsets of size N-i that do NOT contain x are exactly the subsets of size N-i from the N-1 others. The subsets of size N-i that contain x correspond to choosing x and then choosing N-i-1 others. So the number of such subsets is C(N-1, N-i-1). The sum of 10^{sum lengths} for subsets containing x is 10^{len(x)} * sum_{T subset of others, |T|=N-i-1} 10^{sum lengths}. So indeed:
sum_{S subset of others, |S|=N-i} 10^{sum lengths} = F(N-i) - 10^{len(x)} * (sum_{T subset of others, |T|=N-i-1} 10^{sum lengths}).

But sum_{T subset of others, |T|=N-i-1} 10^{sum lengths} is NOT F(N-i-1) because F(N-i-1) includes subsets that may contain x. So we have a recursive dependency. We need to compute for each x the sum over subsets of the others. This is not simply expressible in terms of F alone.

We need a different approach.

Alternative: Instead of fixing position i, we can think of building the permutation from left to right. The sum over permutations of f(P) can be computed by considering the contribution of each number when it is placed at some position, but we need to account for the numbers after it.

Another idea: Use the concept of "concatenation" as a sum over all permutations of the product of weights. Actually, f(P) = sum_{i=1..N} P_i * 10^{sum_{j>i} len(P_j)}. This is similar to the sum over permutations of a weighted sum.

We can compute the total sum by considering the order of numbers. Let's define for each number k, its weight w_k = 10^{len(k)}. Then f(P) = sum_{i=1..N} P_i * (product_{j=i+1..N} w_{P_j}). This is not a simple product.

We can use the following trick: The sum over all permutations of f(P) can be written as the coefficient of something in a generating function? Or we can use the fact that the sum over permutations of a function that depends on the order can be computed using the "inclusion-exclusion" or "DP over subsets" but that's exponential.

Given N up to 2e5, we need a polynomial-time algorithm. The key is that the numbers have only a few distinct lengths. So we can group by length.

Let L be the set of lengths present. For each length l, let A_l be the set of numbers with that length. |A_l| = cnt[l]. We need to sum over all permutations of the multiset of numbers.

We can think of the sum as: sum over all permutations of sum_{i} (value at position i) * 10^{sum of lengths of numbers after i}.

We can compute this by considering the relative order of numbers. Since the numbers are distinct, we can treat them as labeled.

Another approach: Use the linearity of expectation over the positions of each number. For a fixed number x, what is the sum over permutations of x * 10^{sum of lengths of numbers after x}? This is x times the sum over permutations of 10^{sum of lengths of numbers after x}. The numbers after x form a random subset of size N - pos(x), where pos(x) is the position of x. The distribution of pos(x) is uniform: each position has probability 1/N. Given pos(x)=r, the set of numbers after x is a uniformly random subset of size N-r from the other N-1 numbers. So the expected value of 10^{sum of lengths} given pos(x)=r is: (1/C(N-1, N-r)) * sum_{S subset of others, |S|=N-r} 10^{sum lengths}. Then the total sum over permutations for x is: x * sum_{r=1..N} (N-1)! * (expected value given r). Actually, the number of permutations where x is at position r is (N-1)!. So the total contribution of x is x * (N-1)! * sum_{r=1..N} E[10^{sum lengths} | pos(x)=r]. But E[10^{sum lengths} | pos(x)=r] = (1/C(N-1, N-r)) * sum_{S subset of others, |S|=N-r} 10^{sum lengths}.

Thus total sum = (N-1)! * sum_{x=1..N} x * sum_{r=1..N} (1/C(N-1, N-r)) * sum_{S subset of others, |S|=N-r} 10^{sum lengths}.

This still requires computing for each x the sum over subsets of the others.

But we can compute the sum over all x simultaneously by using symmetry. Since the numbers are distinct, we need to account for the value x. However, the sum over subsets of others depends on x only through its length. So we can group by length.

Let’s denote for a fixed length l, and a fixed number x of that length, the sum over subsets of the other numbers (which include all numbers except x) of size m of 10^{sum lengths}. This is the same for all x of the same length, because the set of other numbers is the full set minus one element of length l. So we can compute for each length l, the sum over subsets of size m of the set {1..N} \ {x} for a representative x of length l. Then multiply by the number of such x and sum over x.

But we need to do this for each m = N-r, r=1..N. So we need an array G_l(m) = sum_{S subset of {1..N}\{x}, |S|=m} 10^{sum lengths}, for a fixed x of length l. Then the total contribution of all numbers of length l is: cnt[l] * (N-1)! * sum_{r=1..N} (1/C(N-1, N-r)) * G_l(N-r). But we also need to multiply by the value x. Since x varies, we need to sum x * G_l(N-r) over x of length l. So we need H_l(m) = sum_{x of length l} x * G_l(m). Then total contribution from length l is (N-1)! * sum_{m=0..N-1} (1/C(N-1, m)) * H_l(m), where m = N-r.

But G_l(m) is the sum over subsets of size m of the set excluding one specific element of length l. We can relate G_l(m) to F(m) and F(m-1) as before, but with a correction because the excluded element is of length l. Specifically, if we let F(m) be the sum over subsets of size m of the full set, then:
F(m) = G_l(m) + w_l * G_l(m-1)  (for m>=1), because subsets of size m either do not contain the excluded element (contributing G_l(m)) or contain it (contributing w_l times subsets of size m-1 from the others).
Thus G_l(m) = F(m) - w_l * G_l(m-1).
This is a recurrence. We can compute G_l(m) for all m using this recurrence, given G_l(0)=1 (empty subset). Then we can compute H_l(m) = sum_{x of length l} x * G_l(m). But note that G_l(m) is the same for all x of length l, so H_l(m) = (sum_{x of length l} x) * G_l(m) = S_w[l] * G_l(m).

Thus the total contribution from length l is: (N-1)! * S_w[l] * sum_{m=0..N-1} (1/C(N-1, m)) * G_l(m).

Then total sum = (N-1)! * sum_{l} S_w[l] * sum_{m=0..N-1} G_l(m) / C(N-1, m).

We can compute G_l(m) for all m using the recurrence G_l(m) = F(m) - w_l * G_l(m-1), with G_l(0)=1.

Now we need to compute sum_{m=0..N-1} G_l(m) / C(N-1, m). This is a convolution-like sum. We can compute it efficiently if we have F(m) and precompute the binomial coefficients.

Let's verify with N=3.
F(m) = C(3,m)*10^m.
w_l = 10.
Compute G_l(m):
G_l(0)=1.
G_l(1) = F(1) - 10*G_l(0) = 30 - 10 = 20.
G_l(2) = F(2) - 10*G_l(1) = 300 - 200 = 100.
G_l(3) = F(3) - 10*G_l(2) = 1000 - 1000 = 0.
Now S_w[l] = 6.
C(N-1, m) = C(2,m): m=0:1, m=1:2, m=2:1.
Sum_{m=0..2} G_l(m)/C(2,m) = 1/1 + 20/2 + 100/1 = 1 + 10 + 100 = 111.
Then contribution = (N-1)! * S_w[l] * 111 = 2! * 6 * 111 = 2 * 6 * 111 = 1332. Correct!

So the formula works.

Now we need to compute for each length l:
- F(m) for m=0..N (sum over subsets of size m of full set).
- G_l(m) for m=0..N-1 using recurrence G_l(m) = F(m) - w_l * G_l(m-1), with G_l(0)=1.
- Then compute sum_{m=0..N-1} G_l(m) * invC(N-1, m), where invC is modular inverse of binomial coefficient.
- Multiply by S_w[l] and (N-1)! and sum over l.

We also need to consider that for lengths l that are not present, cnt[l]=0, we skip.

Complexities:
- Compute F(m) for all m. This is the main challenge. We need to compute the elementary symmetric sums of the multiset of weights w_k = 10^{len(k)}. Since there are only a few distinct weights, we can compute F via DP using the polynomial product as before. But we need F(m) for all m up to N. We can compute the polynomial product using NTT. Since the number of distinct lengths is at most 6 (for N up to 2e5, lengths 1 to 6), we can compute the product polynomial in O(6 * N log N) time.

Alternatively, we can compute F(m) using a DP that iterates over numbers but uses the fact that many numbers share the same weight. Since the number of distinct weights is small, we can use the formula for multiset: F(m) = sum_{k1+...+kL = m} prod_l C(cnt[l], k_l) w_l^{k_l}. This is the coefficient of x^m in product_l (1 + w_l x)^{cnt[l]}. We can compute this product by starting with F = [1] and for each l, convolving with the polynomial (1 + w_l x)^{cnt[l]}. The polynomial for length l has degree cnt[l]. We can compute it using binomial coefficients. Since cnt[l] can be large, we need to compute the convolution efficiently. We can use NTT for each multiplication. Since there are at most 6 multiplications, total time is fine.

But we also need to compute G_l(m) for each l. That requires F(m) for all m. So we need F as an array.

Implementation steps:
1. Precompute factorials and inverse factorials up to N.
2. Determine max_len = number of digits of N.
3. For each l from 1 to max_len, compute cnt[l] = number of integers in [1..N] with length l.
   - l=1: min(9, N)
   - l=2: min(99, N) - 9
   - etc.
4. Compute w_l = pow(10, l, MOD).
5. Compute the polynomial for each l: P_l[k] = C(cnt[l], k) * w_l^k mod MOD for k=0..cnt[l].
6. Multiply all P_l using NTT to get F[0..N]. Start with F = [1]. For each l, convolve F and P_l, then truncate to length N+1.
7. For each l with cnt[l] > 0:
   a. Compute G_l[0] = 1.
   b. For m=1..N-1: G_l[m] = (F[m] - w_l * G_l[m-1]) % MOD.
   c. Compute sum_G_l = sum_{m=0..N-1} G_l[m] * invC(N-1, m) % MOD, where invC(N-1, m) = inv_fact[m] * inv_fact[N-1-m] * fact[N-1] mod MOD? Actually C(N-1, m) = fact[N-1] * inv_fact[m] * inv_fact[N-1-m]. So its inverse is inv_fact[N-1] * fact[m] * fact[N-1-m]. But we can precompute invC array.
   d. Compute S_w[l] = sum of numbers with length l. For l=1: sum_{i=1..min(9,N)} i. For l=2: sum_{i=10..min(99,N)} i, etc.
   e. Add to answer: ans += S_w[l] * sum_G_l % MOD.
8. Multiply ans by (N-1)! % MOD.
9. Output ans % MOD.

We need to be careful with the convolution: The polynomial P_l has degree cnt[l]. When we multiply F (degree up to current max) by P_l, the resulting degree is up to current max + cnt[l]. We only need up to N. So we can truncate after each multiplication.

NTT implementation: Since MOD = 998244353 is NTT-friendly, we can implement NTT with primitive root 3. We need to multiply polynomials of size up to N. The total size after all multiplications is at most N+1. We can do iterative NTT.

Alternatively, we can avoid NTT by using the fact that the number of distinct lengths is small and we can compute F using DP with binomial coefficients and the fact that the weights are powers of 10. But NTT is straightforward.

Let's test with N=3:
cnt[1]=3, w1=10.
P_1 = [1, 30, 300, 1000] (since C(3,0)=1, C(3,1)=3, w1=10 => 30; C(3,2)=3, w1^2=100 => 300; C(3,3)=1, w1^3=1000).
F = P_1.
G_1: G[0]=1; G[1]=F[1]-10*1=30-10=20; G[2]=F[2]-10*20=300-200=100; G[3]=F[3]-10*100=1000-1000=0.
invC(2,m): m=0: invC=1; m=1: invC=inv(2)= (MOD+1)//2 = 499122177; m=2: invC=1.
sum_G = 1*1 + 20*inv(2) + 100*1 = 1 + 10 + 100 = 111.
S_w[1]=6.
ans = 6 * 111 = 666.
Multiply by (N-1)! = 2! = 2 => 1332. Correct.

Now test with N=10? Let's do a small N manually to verify.

N=2: numbers 1,2. Permutations: (1,2): f=12; (2,1): f=21. Sum=33.
Our method:
cnt[1]=2, w1=10.
P_1 = [1, 20, 100] (C(2,0)=1, C(2,1)=2*10=20, C(2,2)=1*100=100).
F = [1,20,100].
G_1: G[0]=1; G[1]=F[1]-10*1=20-10=10; G[2]=F[2]-10*10=100-100=0.
invC(1,m): m=0: invC=1; m=1: invC=1.
sum_G = 1*1 + 10*1 = 11.
S_w[1]=1+2=3.
ans = 3 * 11 = 33.
Multiply by (N-1)! = 1! = 1 => 33. Correct.

N=4: numbers 1,2,3,4. All length 1. Permutations: 24 permutations. Sum? Let's compute using formula.
cnt[1]=4, w1=10.
P_1 = (1+10x)^4 = 1 + 40x + 600x^2 + 4000x^3 + 10000x^4.
F = [1,40,600,4000,10000].
G_1: G[0]=1; G[1]=40-10=30; G[2]=600-300=300; G[3]=4000-3000=1000; G[4]=10000-10000=0.
invC(3,m): C(3,0)=1, inv=1; C(3,1)=3, inv=inv(3); C(3,2)=3, inv=inv(3); C(3,3)=1, inv=1.
sum_G = 1*1 + 30*inv(3) + 300*inv(3) + 1000*1 = 1 + 10 + 100 + 1000 = 1111.
S_w[1]=10.
ans = 10 * 1111 = 11110.
Multiply by 3! = 6 => 66660.
Let's compute manually? For N=4, all numbers 1-digit. f(P) is concatenation of 4 digits. The sum over all permutations of the 4-digit number formed by digits 1,2,3,4 in some order. The sum of all 4-digit numbers with distinct digits 1-4. There are 24 permutations. The sum of all such numbers: each digit appears in each position equally often: 6 times. So sum = 6 * (1+2+3+4) * (1000+100+10+1) = 6 * 10 * 1111 = 66660. Correct.

So the method works.

Now we need to implement NTT for polynomial multiplication. Since we only need to multiply a few polynomials, we can implement a simple NTT.

Steps for NTT:
- Write a function ntt(a, invert) that performs in-place NTT.
- Write a function multiply(a, b) that returns the convolution of a and b, truncated to length N+1.

We need to handle the case where the polynomial degrees are up to N. The convolution size is up to 2N. We can use standard NTT.

We also need to precompute factorials and inverse factorials up to N.

Let's outline the code:

```python
import sys

MOD = 998244353
PRIMITIVE_ROOT = 3

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD-1)//length, MOD)
        if invert:
            wlen = pow(wlen, MOD-2, MOD)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i+length//2):
                u = a[j]
                v = a[j+length//2] * w % MOD
                a[j] = (u + v) % MOD
                a[j+length//2] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD-2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    N = int(sys.stdin.readline())
    if N == 0:
        print(0)
        return
    # Precompute factorials
    fact = [1] * (N+1)
    for i in range(1, N+1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N+1)
    inv_fact[N] = pow(fact[N], MOD-2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    # Determine lengths
    max_len = len(str(N))
    cnt = [0] * (max_len + 1)
    w = [0] * (max_len + 1)
    for l in range(1, max_len+1):
        lo = 10**(l-1)
        hi = min(10**l - 1, N)
        if lo > N:
            cnt[l] = 0
        else:
            cnt[l] = hi - lo + 1
        w[l] = pow(10, l, MOD)
    
    # Build polynomials for each length
    # F starts as [1]
    F = [1]
    for l in range(1, max_len+1):
        if cnt[l] == 0:
            continue
        # Build polynomial P_l: sum_{k=0..cnt[l]} C(cnt[l], k) * w[l]^k * x^k
        P = [0] * (cnt[l] + 1)
        wk = 1
        for k in range(cnt[l]+1):
            # C(cnt[l], k) = fact[cnt[l]] * inv_fact[k] * inv_fact[cnt[l]-k]
            P[k] = fact[cnt[l]] * inv_fact[k] % MOD * inv_fact[cnt[l]-k] % MOD * wk % MOD
            wk = wk * w[l] % MOD
        # Multiply F and P
        F = multiply(F, P)
        # Truncate to N+1
        if len(F) > N+1:
            F = F[:N+1]
    
    # Ensure F has length N+1
    if len(F) < N+1:
        F += [0] * (N+1 - len(F))
    
    # Compute S_w[l] = sum of numbers with length l
    S_w = [0] * (max_len + 1)
    for l in range(1, max_len+1):
        lo = 10**(l-1)
        hi = min(10**l - 1, N)
        if lo > N:
            continue
        # Sum from lo to hi
        S_w[l] = (lo + hi) * (hi - lo + 1) // 2 % MOD
    
    # Precompute invC(N-1, m) for m=0..N-1
    # C(N-1, m) = fact[N-1] * inv_fact[m] * inv_fact[N-1-m]
    # invC = inv_fact[N-1] * fact[m] * fact[N-1-m]
    invC = [0] * N
    if N-1 >= 0:
        inv_fact_N_1 = inv_fact[N-1]
        for m in range(N):
            invC[m] = inv_fact_N_1 * fact[m] % MOD * fact[N-1-m] % MOD
    
    ans = 0
    for l in range(1, max_len+1):
        if cnt[l] == 0:
            continue
        # Compute G_l
        G = [0] * N
        G[0] = 1
        for m in range(1, N):
            G[m] = (F[m] - w[l] * G[m-1]) % MOD
        # Compute sum_G = sum_{m=0..N-1} G[m] * invC[m]
        sum_G = 0
        for m in range(N):
            sum_G = (sum_G + G[m] * invC[m]) % MOD
        ans = (ans + S_w[l] * sum_G) % MOD
    
    ans = ans * fact[N-1] % MOD
    print(ans % MOD)

if __name__ == "__main__":
    main()
```

We need to be careful with the NTT implementation: The multiply function returns a list of length n (the next power of two). We need to truncate to the actual length (len(a)+len(b)-1) and then to N+1.

Also, note that for N=1, we have only one number. The sum over permutations is just f((1)) = 1. Our formula should give 1.
N=1: cnt[1]=1, w1=10.
P_1 = [1, 10].
F = [1, 10].
G_1: G[0]=1; G[1]=F[1]-10*1=10-10=0.
invC(0,m): N-1=0, so only m=0: invC[0]=1.
sum_G = G[0]*1 = 1.
S_w[1]=1.
ans = 1 * 1 = 1.
Multiply by (N-1)! = 0! = 1 => 1. Correct.

Now test with sample N=3: we already did manually.

We should also test with N=10? Let's compute with code later.

Potential issues:
- The NTT implementation must be correct.
- The polynomial multiplication might be slow if we do it for each length separately. But with max 6 lengths, it's fine.
- We need to handle large N up to 2e5, so the polynomial size is up to 2e5+1. NTT with size up to 2^18 = 262144 is fine.

We also need to ensure that the modular inverse of binomial coefficients is computed correctly. Since MOD is prime, we can use factorials.

One more check: For N=390, sample output is 727611652. We can test with the code.

Let's write the code carefully.

We need to import sys for input.

We should also consider that for N=1, the loop for m in range(1, N) will be empty, so G has length N=1, with G[0]=1. Then sum_G = G[0]*invC[0] = 1. Good.

For N=2, N-1=1, invC has length 2: m=0,1. G has length 2: G[0]=1, G[1]=F[1]-w*G[0]. F[1] = sum of weights of subsets of size 1 = sum_{i=1..N} w_i. For N=2, w_i=10, so F[1]=20. G[1]=20-10=10. sum_G = 1*1 + 10*1 = 11. S_w=3. ans=33. fact[1]=1. So 33. Correct.

Now, we need to ensure that the NTT multiplication does not overflow or cause issues. We should use iterative NTT to avoid recursion.

Let's write the NTT code:

```python
def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD
```

This is standard.

Now, the multiply function:

```python
def multiply(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    # Truncate to len(a)+len(b)-1
    res = fa[:len(a) + len(b) - 1]
    return res
```

We need to be careful that the polynomial multiplication is done modulo MOD, and we truncate to the actual degree.

Now, the main function:

We need to compute the polynomial for each length l. The polynomial P_l has degree cnt[l]. We can compute it using binomial coefficients.

We need to precompute factorials up to N. Since N up to 2e5, that's fine.

We also need to compute the sum of numbers for each length. We can compute using arithmetic series formula.

Let's write the code step by step.

One more thing: The number of lengths is at most 6, but we need to compute 10^l mod MOD for l up to 6. That's easy.

Now, let's test with N=3 using the code mentally.

We should also consider that for N up to 2e5, the polynomial size is up to 2e5+1. The NTT size will be the next power of two, which is 262144. That's fine.

Potential optimization: We can compute F using DP without NTT by using the fact that the weights are only 6 distinct values. But NTT is simpler to implement correctly.

Let's write the full code.

We'll also need to handle the case where N is large and the polynomial multiplication might be slow if we do it for each length separately. But with 6 multiplications, each of size ~2e5, total time is about 6 * 2e5 * log(2e5) ~ 6 * 2e5 * 18 ~ 2e7 operations, which is fine in Python if optimized? Actually, Python NTT might be slow. We need to ensure the NTT is efficient. We can use PyPy or optimize the loops. But the problem constraints are up to 2e5, and NTT in Python might be borderline. However, we can try to optimize by using built-in complex numbers for FFT? But MOD is not suitable for floating point FFT. We need NTT.

Alternatively, we can compute F using a DP that iterates over numbers but uses the fact that there are only 6 distinct weights. We can use the formula for multiset: F(m) = sum_{k1+...+kL = m} prod_l C(cnt[l], k_l) w_l^{k_l}. This is a convolution of the sequences for each l. Since L is small, we can compute F by iterating over m and using the recurrence from the generating function. But that would be O(N * L) if we do it naively? Actually, we can compute F using DP: start with F = [1]. For each l, we update F by: for m from current_max down to 0: for k from 1 to cnt[l]: F[m+k] += F[m] * C(cnt[l], k) * w_l^k. This is O(N * cnt[l]) which is O(N^2) in the worst case. But since cnt[l] is large for l=1 (about 9), l=2 (90), etc., the total sum of cnt[l] is N. So the total operations would be O(N^2) if we do it naively. However, we can optimize by noting that for each l, the inner loop over k can be done using the fact that the binomial coefficients times w_l^k form a sequence that we can convolve. But we can also use the fact that the polynomial for each l is (1 + w_l x)^{cnt[l]}, and we can compute its coefficients using the binomial theorem. Then we need to multiply these polynomials. Since the number of polynomials is small, we can use NTT.

But NTT in Python might be too slow for N=2e5. Let's estimate: A single NTT of size 262144 takes about 262144 * log2(262144) = 262144 * 18 = 4.7 million operations. Each operation involves modular multiplication. In Python, this might take a few seconds. With 6 multiplications, it might be 20-30 seconds, which might be too slow.

We need a faster method. Since the number of distinct weights is small, we can compute F using a DP that is O(N * number_of_lengths) by using the fact that the weights are powers of 10. Actually, we can compute F using the following recurrence: F(m) = sum_{l} w_l * (something). But we need to account for multiple copies.

We can use the generating function approach but compute the product using divide and conquer with NTT? That would still be NTT.

Alternatively, we can compute F using a DP that iterates over numbers but groups by length. Since the number of distinct lengths is small, we can use the formula for the elementary symmetric sums of a multiset with repeated values. There is a known algorithm to compute the elementary symmetric sums in O(N * sqrt(N)) or O(N log N) using the fact that the weights are only a few distinct values. But we can also use the following: Since the weights are only 10, 100, 1000, ..., we can compute F by iterating over the numbers and updating the DP array. But that would be O(N^2) if we do it naively. However, we can use the fact that the weights are the same for many numbers. We can use the polynomial multiplication but with a faster convolution algorithm like FFT with real numbers? But we need exact modulo.

Maybe we can use the fact that the number of distinct lengths is at most 6, so we can compute F by iterating over the possible counts of each length. Let k_l be the number of elements chosen from length l. Then F(m) = sum_{k1+...+kL = m} prod_l C(cnt[l], k_l) w_l^{k_l}. This is a sum over all tuples (k1,...,kL) such that sum k_l = m. The number of such tuples is the number of compositions of m into L parts, which is C(m+L-1, L-1). For L=6, this is about m^5/5! for large m, which is huge. So we cannot iterate over all tuples.

We need a better way.

Another idea: Since the weights are powers of 10, we can compute F using a DP that processes numbers one by one, but we can batch process numbers with the same weight. For a batch of cnt copies of weight w, the update is: new_F = old_F * (1 + w x)^{cnt}. We can compute (1 + w x)^{cnt} using the binomial theorem, which gives a polynomial of degree cnt. We need to multiply old_F (degree up to current sum) by this polynomial. This is a convolution. We can do this convolution using FFT if we use floating point and then round? But we need exact modulo. We can use NTT.

Given the constraints, NTT in Python might be acceptable if we optimize the code. We can use PyPy which is faster for such tasks. Many competitive programming problems with N=2e5 and NTT in Python are solvable with optimized code.

We can also try to compute F using a DP that is O(N * max_len) by using the fact that the weights are only 6 distinct values. Actually, we can compute F using the following recurrence: Let F_m be the array. We can compute F by iterating over lengths and using the fact that the polynomial for length l is (1 + w_l x)^{cnt[l]}. We can compute this polynomial using the binomial coefficients, and then multiply it with the current F. Since the degree of the polynomial for length l is cnt[l], which can be large, we need an efficient multiplication. But we can use the fact that the polynomial is sparse? No, it's dense.

Maybe we can use the fact that the weights are powers of 10, so w_l = 10^l. Then the product over l of (1 + 10^l x)^{cnt[l]} can be computed by iterating over the numbers 1..N and updating the DP. But that would be O(N^2). However, we can use the fact that the numbers are grouped by length, and we can use the formula for the sum over subsets. There is a known trick: For a multiset with repeated weights, the elementary symmetric sums can be computed using the fact that the generating function is the product of (1 + w x)^{cnt}. We can compute this product by using the fact that the number of distinct w is small, so we can use the following: Let the distinct weights be w1, w2, ..., wL. We want the coefficients of P(x) = prod_{i=1..L} (1 + w_i x)^{cnt_i}. We can compute P(x) by starting with P=1, and for each i, we multiply by (1 + w_i x)^{cnt_i}. To multiply by (1 + w_i x)^{cnt_i}, we can use the binomial expansion to get the coefficients, and then do a convolution. But we can also use the fact that (1 + w_i x)^{cnt_i} can be computed using the recurrence: let Q(x) = (1 + w_i x)^{cnt_i}. Then Q_0 = 1, and Q_k = C(cnt_i, k) w_i^k. We can compute Q_k for all k. Then we need to convolve P and Q. Since the degree of Q is cnt_i, which can be large, we need an efficient convolution. But we can use the fact that the number of distinct i is small, so we can use NTT for each multiplication. That's what we planned.

Given that N is only 2e5, and we have at most 6 NTTs, it should be fine in PyPy. We can also use the built-in `numpy` for FFT? But we need exact modulo.

Let's proceed with NTT.

We need to ensure that the NTT implementation is efficient. We can precompute the roots of unity for each length to avoid repeated pow calls. But for simplicity, we can compute wlen inside the loop.

We can also use the iterative NTT with bit-reversal permutation.

Let's write the code with careful optimization.

We'll also need to handle the case where N is small, e.g., N=1,2,3.

Now, let's write the full code.

We'll also need to compute the sum of numbers for each length. We can compute the range and sum.

One more thing: In the recurrence for G_l, we have G_l[m] = F[m] - w_l * G_l[m-1]. This is valid for m>=1. We need to ensure that F[m] is defined for m up to N. Since F is the sum over subsets of size m, F[0]=1, F[1]=sum w_i, etc. We computed F via polynomial multiplication, so it should be correct.

Now, let's test with N=390 using the code? We can't run here, but we can trust the logic.

We should also consider that for N up to 2e5, the maximum length is 6 (since 10^5=100000, 10^6=1000000). So we have lengths 1..6.

Now, let's write the code.

We'll structure it as:

1. Read N.
2. Precompute factorials and inverse factorials up to N.
3. Compute cnt[l] and w[l] for l=1..max_len.
4. Compute F via polynomial multiplication.
5. Compute S_w[l] for each l.
6. Compute invC array.
7. For each l, compute G_l and sum_G, add to ans.
8. Multiply ans by fact[N-1] and output.

We need to be careful with the polynomial multiplication: The initial F is [1]. For each l, we multiply by P_l. We need to truncate to N+1 after each multiplication to keep the size manageable.

Let's code.

We'll also need to handle the case where N=0? But N>=1.

Now, let's write the code in the final answer.

We'll enclose it in the required delimiters.

One more check: The sample N=3 gives 1332. Our manual calculation gave 1332. Good.

Sample N=390: We can't compute manually, but we trust.

Sample N=79223: Also trust.

Now, let's write the code.

We'll use sys.stdin.readline for input.

We'll set recursion limit high.

We'll implement NTT.

Let's write the code now.### PLAN
We need to compute the sum of f(P) over all permutations P of (1,2,...,N), where f(P) is the integer formed by concatenating the decimal representations of P_i. The sum can be expressed as:
Sum = (N-1)! * Σ_{l} S_w[l] * Σ_{m=0}^{N-1} G_l(m) / C(N-1, m),
where:
- S_w[l] = sum of numbers with exactly l digits,
- G_l(m) = sum of 10^{sum of lengths} over all subsets of size m from {1..N} excluding one fixed number of length l,
- F(m) = sum of 10^{sum of lengths} over all subsets of size m from {1..N}.
G_l satisfies G_l(0)=1 and G_l(m) = F(m) - 10^l * G_l(m-1) for m≥1.
F(m) is the coefficient of x^m in ∏_{l} (1 + 10^l x)^{cnt[l]}, where cnt[l] is the count of numbers with l digits. Since there are at most 6 distinct lengths (for N ≤ 2e5), we compute F via polynomial multiplication using NTT. Then we compute G_l, the weighted sum, and finally the answer.
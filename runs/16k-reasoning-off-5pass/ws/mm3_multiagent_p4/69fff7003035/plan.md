We need to compute sum over all permutations P of (1..N) of the concatenated integer f(P). For each position i (1-indexed), the number placed there contributes its decimal value multiplied by 10^{total digits of numbers after it}. Since permutations are uniform, each number j appears equally often in each position. So contribution of number j at position i is j * 10^{D_i} where D_i = sum of digits of numbers after position i. Summing over all permutations: each j appears (N-1)! times in each position, so total contribution = (N-1)! * j * sum_{i=1..N} 10^{D_i}.

We need D_i for each i. Let len[j] = number of digits of j. Then D_i = sum_{k=i+1..N} len[P_k]. Over all permutations, the multiset of numbers after position i is a random (N-i)-subset of {1..N}, uniformly distributed. So expected D_i = (N-i)/N * sum_{j=1..N} len[j]. But we need the sum of 10^{D_i} over all permutations, not just expectation. However, since 10^{D_i} depends only on the multiset of lengths after position i, and the sum of 10^{D_i} over all permutations equals (N-1)! * sum over all permutations of 10^{D_i} / (N-1)! ... Actually we can compute total sum as:

Total = (N-1)! * sum_{i=1..N} (sum over permutations of 10^{D_i}) / (N-1)!? Wait.

Better: Total sum = sum_{i=1..N} (N-1)! * j_avg? No.

Let's derive carefully. For each permutation P, f(P) = sum_{i=1..N} P_i * 10^{sum_{k>i} len[P_k]}. Sum over all permutations:

S = sum_{P} sum_{i=1..N} P_i * 10^{sum_{k>i} len[P_k]}
  = sum_{i=1..N} sum_{P} P_i * 10^{sum_{k>i} len[P_k]}.

For fixed i, consider the set of permutations. The numbers after position i form a random (N-i)-subset of {1..N}, and the number at position i is the remaining element. The sum over permutations of P_i * 10^{sum_{k>i} len[P_k]} can be computed by considering all ways to choose the set S of size N-i for positions > i, and then P_i is the complement. For each subset T of size N-i, the number of permutations with that exact set after i is (N-i)! * i! (arrangements of T in positions > i, and arrangements of complement in positions <= i, but we fix position i as the specific element). Actually: choose which element is at position i: there are N choices. For each choice, the remaining N-1 elements are arranged in the other positions. But we want to sum over all permutations.

Alternatively, we can think: For each i, the contribution is sum_{j=1..N} j * (number of permutations where j is at position i) * 10^{sum of lengths of the other N-i elements in some order}. Since the exponent depends only on the multiset of lengths of the N-i elements after i, not their order, we can factor:

Number of permutations with j at position i and a specific set T of size N-i for positions > i is (N-i)! * (i-1)! (arrangements of T in positions > i, and arrangements of remaining N-i elements? Wait: total positions: i is fixed as j. Positions > i: N-i positions filled by T in any order: (N-i)! ways. Positions < i: i-1 positions filled by the remaining N-i elements? No, total elements are N. If j is at position i, and T is the set of N-i elements that go to positions > i, then the remaining N - 1 - (N-i) = i-1 elements go to positions < i. They can be arranged in (i-1)! ways. So total permutations with j at position i and T as the set after i is (N-i)! * (i-1)!.

Thus sum over permutations of P_i * 10^{sum_{k>i} len[P_k]} = sum_{j=1..N} j * (i-1)! * (N-i)! * sum_{T subset of {1..N}\{j}, |T|=N-i} 10^{sum_{x in T} len[x]}.

So S = sum_{i=1..N} (i-1)! * (N-i)! * sum_{j=1..N} j * sum_{T: |T|=N-i, j not in T} 10^{sum_{x in T} len[x]}.

We can swap sums: S = sum_{i=1..N} (i-1)! * (N-i)! * sum_{T subset of {1..N}, |T|=N-i} 10^{sum_{x in T} len[x]} * (sum_{j not in T} j).

Note that sum_{j not in T} j = total_sum - sum_{x in T} x.

Let total_sum = N(N+1)/2.

So S = sum_{i=1..N} (i-1)! * (N-i)! * sum_{T, |T|=N-i} 10^{L_T} * (total_sum - sum_{x in T} x),

where L_T = sum_{x in T} len[x].

Now we need to compute for each k = N-i (size of T from 0 to N-1), the sum over subsets T of size k of 10^{L_T} and sum_{x in T} x * 10^{L_T}.

Let k = N-i. Then (i-1)! * (N-i)! = (N-k-1)! * k!.

So S = sum_{k=0}^{N-1} (N-k-1)! * k! * [ total_sum * A_k - B_k ],

where A_k = sum_{T, |T|=k} 10^{L_T}, and B_k = sum_{T, |T|=k} (sum_{x in T} x) * 10^{L_T}.

We need to compute A_k and B_k efficiently for all k.

Observation: len[x] is small (1 to 6 for N up to 2e5). We can group numbers by their digit length. Let c_d = count of numbers with d digits, for d=1..6 (or up to max digits). For N=2e5, max digits is 6 (since 10^5=100000 has 6 digits, 2e5 < 10^6).

Let w_x = 10^{len[x]}. Then 10^{L_T} = product_{x in T} w_x.

So A_k = sum over subsets of size k of product of w_x.

This is the elementary symmetric sum of degree k of the multiset {w_1, ..., w_N}.

Similarly, B_k = sum_{T, |T|=k} (sum_{x in T} x) * product_{y in T} w_y.

We can compute these using generating functions or DP.

Let’s define polynomial F(z) = sum_{T subset of {1..N}} (product_{x in T} w_x) * z^{|T|}. Then A_k is coefficient of z^k.

But we need B_k = sum_{T, |T|=k} (sum_{x in T} x) * prod w_x.

We can compute this by considering derivative or using another generating function.

Let G(z) = sum_{T} (sum_{x in T} x * prod_{y in T} w_y) * z^{|T|}.

We can write G(z) = sum_{x} x * w_x * z * sum_{T' subset of others} (prod_{y in T'} w_y) * z^{|T'|}.

Actually, if we consider the sum over all subsets T (including empty) of (sum_{x in T} x) * prod_{y in T} w_y * z^{|T|}, we can compute it as:

Let H(z) = sum_{T} prod_{y in T} w_y * z^{|T|} = prod_{x=1..N} (1 + w_x * z).

Then the sum with the extra factor (sum_{x in T} x) is:

G(z) = sum_{T} (sum_{x in T} x) * prod_{y in T} w_y * z^{|T|}
     = sum_{x} x * w_x * z * sum_{T: x in T} prod_{y in T\{x}} w_y * z^{|T|-1}
     = sum_{x} x * w_x * z * prod_{y != x} (1 + w_y * z).

But we need only subsets of size exactly k, not all subsets. However, we can extract coefficients.

Alternatively, we can compute A_k and B_k via DP over numbers, grouping by digit length to reduce complexity.

Since N is up to 2e5, we can do DP in O(N * max_len) or O(N * sqrt(N))? But we need up to N=2e5, and we need all k from 0 to N. That's O(N^2) if naive.

But we can use the fact that w_x depends only on digit length. There are only 6 distinct values of w_x: 10, 100, 1000, 10000, 100000, 1000000. Let’s denote them as w_d for d=1..6, with counts c_d.

Then the product over a subset T is determined by how many numbers of each digit length are chosen. So A_k = sum over all ways to pick a_1,...,a_6 such that sum a_d = k and 0 <= a_d <= c_d, of (w_1^{a_1} * ... * w_6^{a_6}) * (multinomial coefficient: c_1 choose a_1 * ... * c_6 choose a_6).

Similarly, B_k = sum over such selections of (sum_{d} a_d * avg_value_of_digit_d? Wait, sum_{x in T} x is not simply expressed by counts because the actual values matter. However, we can group numbers by digit length and also by their value? But values are distinct.

We need sum_{x in T} x. This is not determined solely by counts of digit lengths; it depends on which specific numbers are chosen.

But we can compute B_k by linearity: B_k = sum_{x=1..N} x * (sum_{T: |T|=k, x in T} prod_{y in T} w_y).

For a fixed x, the inner sum is: w_x * sum_{T' subset of others, |T'|=k-1} prod_{y in T'} w_y.

So B_k = sum_{x=1..N} x * w_x * A_{k-1}^{(x)}, where A_{k-1}^{(x)} is the elementary symmetric sum of degree k-1 of the set {w_y : y != x}.

We can compute this if we have the full polynomial H(z) = prod_{y} (1 + w_y z). Then A_k is coefficient of z^k.

Then A_{k-1}^{(x)} is coefficient of z^{k-1} in H(z) / (1 + w_x z).

Thus B_k = sum_{x} x * w_x * [coeff of z^{k-1} in H(z)/(1+w_x z)].

But we need B_k for all k. This seems expensive if we do per x.

However, we can compute B_k using generating functions with an extra variable.

Consider the bivariate generating function:

F(u, z) = sum_{T} (prod_{y in T} w_y) * u^{sum_{y in T} y} * z^{|T|}.

Then B_k is coefficient of z^k in d/du F(u,z) evaluated at u=1? Actually, sum_{T, |T|=k} (sum_{x in T} x) * prod w_y = d/du [ sum_{T, |T|=k} u^{sum x} prod w_y ] at u=1.

But we need to compute this for all k. We can compute the polynomial in z: P(z) = sum_{T} prod w_y * z^{|T|} = H(z). And Q(z) = sum_{T} (sum_{x in T} x) * prod w_y * z^{|T|}.

We can compute Q(z) as:

Q(z) = sum_{x} x * w_x * z * prod_{y != x} (1 + w_y z).

This is not a simple product, but we can write:

Q(z) = sum_{x} x * w_x * z * H(z) / (1 + w_x z).

So Q(z) = H(z) * sum_{x} x * w_x * z / (1 + w_x z).

Thus we can compute H(z) as a polynomial of degree N (but we only need up to N-1). Then compute R(z) = sum_{x} x * w_x * z / (1 + w_x z) as a rational function, multiply by H(z), and extract coefficients.

But H(z) has degree N, and we need coefficients up to N-1. However, N is 2e5, so we can compute H(z) via DP in O(N * max_digit_count)? Wait, w_x are not all distinct? Actually w_x depends only on digit length, so there are only 6 distinct values. But the polynomial H(z) = prod_{x=1..N} (1 + w_x z). Since many factors are identical, we can compute it efficiently using exponentiation by grouping.

Specifically, for each digit length d, we have c_d copies of (1 + w_d z). So H(z) = prod_{d=1..6} (1 + w_d z)^{c_d}.

We can compute this polynomial using the fact that (1 + w_d z)^{c_d} can be expanded via binomial theorem: sum_{j=0}^{c_d} binom(c_d, j) w_d^j z^j.

Since c_d can be up to N (e.g., for d=1, numbers 1..9 have 9 numbers, but for N=2e5, c_1 = 9, c_2 = 90, c_3 = 900, c_4 = 9000, c_5 = 90000, c_6 = up to 2e5 - 111111 = 88889? Actually 1..9:9, 10..99:90, 100..999:900, 1000..9999:9000, 10000..99999:90000, 100000..200000:100001. So c_6 can be about 1e5.

We need to multiply these 6 polynomials, each of degree up to c_d. The total degree is N. The naive multiplication would be O(N^2). But we can use FFT (NTT) since modulus is 998244353, which is NTT-friendly. We can multiply polynomials using NTT in O(N log N). Since we have only 6 polynomials, we can multiply them sequentially using NTT.

But we also need to compute R(z) = sum_{x} x * w_x * z / (1 + w_x z). This is a sum of rational functions. However, we can compute Q(z) = H(z) * R(z) as a polynomial of degree N-1 (since H has degree N, R has degree -1? Actually R(z) = sum_{x} x * w_x * z * (1 - w_x z + w_x^2 z^2 - ...) = sum_{m>=0} (-1)^m (sum_{x} x * w_x^{m+1}) z^{m+1}. So R(z) is a power series starting at z^1. Multiplying by H(z) (degree N) gives degree N+? Actually H has degree N, R has infinite series, but we only need up to degree N-1 for B_k (since k <= N-1). So we need Q(z) mod z^N.

We can compute Q(z) by noting that Q(z) = sum_{x} x * w_x * z * H(z) / (1 + w_x z). Since we only need coefficients up to z^{N-1}, and H(z) has degree N, we can compute for each x the series H(z)/(1+w_x z) truncated to degree N-1, multiply by x * w_x * z, and sum. But doing this per x (N up to 2e5) would be O(N^2) if naive.

But we can group by w_x. Since w_x depends only on digit length, we have groups. However, the factor x * w_x varies per x. So we need to sum over x in each group: sum_{x in group d} x * w_d * z * H(z) / (1 + w_d z) = w_d * z * H(z) / (1 + w_d z) * (sum_{x in group d} x).

Let S_d = sum of numbers with d digits. Then for each d, the contribution is S_d * w_d * z * H(z) / (1 + w_d z).

Thus Q(z) = H(z) * sum_{d} S_d * w_d * z / (1 + w_d z).

Now we have only 6 terms in the sum. So we can compute for each d the series T_d(z) = z / (1 + w_d z) = sum_{m>=0} (-w_d)^m z^{m+1}. Then multiply by S_d * w_d, and sum.

Then Q(z) = H(z) * (sum_{d} S_d * w_d * T_d(z)).

We need Q(z) up to degree N-1. Since H(z) has degree N, and T_d(z) is a power series, we can compute the product truncated to degree N-1 using NTT or by convolution.

But we need to compute H(z) first. H(z) = prod_{d} (1 + w_d z)^{c_d}. We can compute this polynomial using NTT.

Steps:
1. Compute c_d and S_d for d=1..6.
2. Compute polynomial H(z) = prod_{d} (1 + w_d z)^{c_d} mod 998244353, up to degree N (or N, but we only need up to N-1 for A_k and B_k? Actually A_k for k=0..N-1, B_k for k=0..N-1. H(z) has degree N. We need coefficients up to N-1. So we can compute H(z) truncated to degree N.
3. Compute polynomial R(z) = sum_{d} S_d * w_d * T_d(z) mod z^N, where T_d(z) = z / (1 + w_d z) = sum_{m=0}^{N-2} (-w_d)^m z^{m+1}. Actually we need up to degree N-1 in Q(z) = H(z) * R(z). Since H has degree N, R needs up to degree N-1 to get Q up to degree 2N-1, but we only need Q up to degree N-1. So we can truncate R to degree N-1 (i.e., compute coefficients up to z^{N-1}).
4. Compute Q(z) = H(z) * R(z) truncated to degree N-1.
5. Then A_k = coeff of z^k in H(z) for k=0..N-1.
   B_k = coeff of z^k in Q(z) for k=0..N-1.
6. Compute S = sum_{k=0}^{N-1} (N-k-1)! * k! * ( total_sum * A_k - B_k ) mod 998244353.

We need factorials up to N. Precompute factorials and inverse factorials.

Complexities:
- Computing H(z): we have 6 polynomials of degrees c_d. We can compute each (1 + w_d z)^{c_d} using binomial coefficients: sum_{j=0}^{c_d} binom(c_d, j) w_d^j z^j. Since c_d can be up to ~1e5, we can compute this in O(c_d) time. Then multiply them using NTT. Since total degree is N, we can do NTT of size next power of two >= 2N. That's O(N log N).
- Computing R(z): for each d, compute series T_d(z) up to degree N-1: T_d(z) = sum_{m=0}^{N-2} (-w_d)^m z^{m+1}. This is O(N) per d, total O(6N) = O(N).
- Multiplying H(z) and R(z) truncated to degree N-1: we can do NTT multiplication and truncate. O(N log N).
- Final sum: O(N).

Total O(N log N), which is fine for N=2e5.

Edge cases: N=1. Then k=0 only. A_0 = 1 (empty set). B_0 = 0. (N-k-1)! * k! = (0)! * 0! = 1. total_sum = 1. So S = 1 * (1*1 - 0) = 1. Indeed f((1)) = 1.

Check sample N=3:
Numbers: 1 (len1), 2 (len1), 3 (len1). So c_1=3, w_1=10. S_1=6.
H(z) = (1+10z)^3 = 1 + 30z + 300z^2 + 1000z^3.
A_0=1, A_1=30, A_2=300, A_3=1000.
R(z) = S_1 * w_1 * z/(1+10z) = 6*10 * z/(1+10z) = 60 * sum_{m>=0} (-10)^m z^{m+1} = 60z - 600z^2 + 6000z^3 - ...
We need up to degree 2 (since N-1=2). So R(z) = 60z - 600z^2.
Q(z) = H(z) * R(z) = (1 + 30z + 300z^2 + ...) * (60z - 600z^2) = 60z + (30*60 - 600)z^2 + ... = 60z + (1800 - 600)z^2 = 60z + 1200z^2.
So B_0=0, B_1=60, B_2=1200.
Now compute S:
k=0: (2)! * 0! * (6*1 - 0) = 2 * 6 = 12.
k=1: (1)! * 1! * (6*30 - 60) = 1 * (180 - 60) = 120.
k=2: (0)! * 2! * (6*300 - 1200) = 2 * (1800 - 1200) = 2 * 600 = 1200.
Total = 12 + 120 + 1200 = 1332. Matches sample.

Great.

Implementation details:
- Modulus: 998244353, primitive root 3, suitable for NTT.
- Precompute factorials fact[i] and inv_fact[i] for i=0..N.
- Compute c_d and S_d:
  For d=1: numbers 1..9, count = min(N,9) - max(1,1) + 1? Actually start = 1, end = min(N,9). count = max(0, min(N,9) - 1 + 1) = max(0, min(N,9)).
  For d>=2: start = 10^{d-1}, end = min(N, 10^d - 1). count = max(0, end - start + 1).
  S_d = sum of numbers from start to end.
- w_d = 10^d mod MOD.
- Compute polynomial P_d(z) = (1 + w_d z)^{c_d} = sum_{j=0}^{c_d} binom(c_d, j) w_d^j z^j.
  We can compute binom(c_d, j) using factorials: binom(c_d, j) = fact[c_d] * inv_fact[j] * inv_fact[c_d-j] mod MOD.
  Then term is binom * w_d^j.
  Since c_d can be up to ~1e5, we can compute this in O(c_d) time. But total sum of c_d is N, so O(N) total.
- Multiply these 6 polynomials using NTT to get H(z). We need H(z) up to degree N. We can truncate after multiplication.
- Compute R(z): for each d, compute series T_d(z) = z/(1 + w_d z) = sum_{m=0}^{N-2} (-w_d)^m z^{m+1}. We can compute powers of (-w_d) iteratively.
  Then R(z) = sum_{d} S_d * w_d * T_d(z) mod z^N.
- Multiply H(z) and R(z) using NTT, truncate to degree N-1 to get Q(z).
- Extract A_k = H.coeff[k] for k=0..N-1, B_k = Q.coeff[k] for k=0..N-1.
- Compute answer = sum_{k=0}^{N-1} fact[N-k-1] * fact[k] % MOD * ( total_sum * A_k - B_k ) % MOD.
  Ensure positivity.

Potential issues:
- NTT size: need to handle polynomials of degree up to N. For multiplication of H (degree N) and R (degree N-1), product degree up to 2N-1. We can use NTT size = 1 << ceil(log2(2N+1)). That's fine.
- For computing (1 + w_d z)^{c_d}, we can also use NTT to compute the polynomial via exponentiation, but since c_d is large, binomial is fine.
- Need to compute factorials up to max(c_d) which is at most N. So precompute fact up to N.

Let's verify with N=2:
Numbers: 1,2. c_1=2, w_1=10, S_1=3.
H(z) = (1+10z)^2 = 1 + 20z + 100z^2.
A_0=1, A_1=20, A_2=100.
R(z) = 3*10 * z/(1+10z) = 30z - 300z^2 + ...
Truncate to degree 1: R(z) = 30z.
Q(z) = (1+20z+100z^2)*(30z) = 30z + 600z^2 + ... -> B_1=30, B_2=600.
total_sum=3.
k=0: (1)! * 0! * (3*1 - 0) = 3.
k=1: (0)! * 1! * (3*20 - 30) = 1*(60-30)=30.
Total = 33.
Check manually: permutations: (1,2) -> 12; (2,1) -> 21. Sum=33. Correct.

N=1: c_1=1, w_1=10, S_1=1.
H(z) = 1+10z.
A_0=1, A_1=10.
R(z) = 1*10 * z/(1+10z) = 10z - 100z^2 + ... -> up to degree 0: R(z)=10z.
Q(z) = (1+10z)*10z = 10z + 100z^2 -> B_1=10.
total_sum=1.
k=0: (0)! * 0! * (1*1 - 0) = 1.
Total=1. Correct.

Now, we need to ensure that for large N, the computation is efficient.

Implementation plan in Python:
- Use numpy? But NTT in Python is slow without optimization. However, we can implement NTT in pure Python with careful optimization. Since N=2e5, NTT of size ~524288 should be okay in Python if written efficiently (using iterative loops and precomputed roots). But Python might be slow for NTT. However, we can use the fact that we only need to multiply a few polynomials. We can also use the pyfft library? Not allowed. We need to implement NTT ourselves.

Alternatively, we can avoid NTT by using the fact that w_d are powers of 10, and we can compute H(z) using DP with O(N * number_of_groups) = O(N * 6) = O(N). Wait, is that possible?

We need to compute the polynomial H(z) = prod_{d} (1 + w_d z)^{c_d}. Since there are only 6 distinct w_d, we can compute the coefficients using a DP that tracks the number of elements chosen from each group. But the state would be (a_1, a_2, ..., a_6) with sum a_d = k. That's O(N^5) if naive. But we can use generating functions with convolution: we can multiply the polynomials iteratively using standard polynomial multiplication. Since the degrees are up to N, we can use FFT via numpy's FFT? But numpy's FFT uses floating point and might have precision issues. We need exact integer arithmetic modulo 998244353.

We can implement NTT in Python. It's doable. Let's recall the NTT implementation for modulus 998244353.

Standard NTT:
- Primitive root g = 3.
- For length n = 2^k, we need root = g^{(mod-1)/n}.
- Precompute roots for each level.

We can write a function ntt(a, invert) that does in-place transform.

Since we have only a few multiplications (6 polynomials to get H, then H * R), we can do them.

But note: the polynomials for each d have degree c_d. The total degree is N. We can multiply them one by one. The first multiplication: P1 * P2, degree up to c_1 + c_2. Then multiply by P3, etc. The intermediate degrees grow. The final H has degree N. We can truncate to degree N after each multiplication to keep size manageable.

Alternatively, we can compute H(z) using the binomial expansion for each d and then multiply using NTT. Since there are only 6, we can compute all 6 polynomials, then multiply them in a balanced tree: multiply pairs, then multiply results, etc. This reduces the number of NTTs.

But we also need to multiply H and R. So total NTTs: maybe 3 or 4.

Given N=2e5, NTT size ~524288, each NTT O(n log n) ~ 524288 * 19 ~ 10 million operations. In Python, 10 million operations might be okay if optimized (using list comprehensions and avoiding function calls). But we need to be careful.

Alternatively, we can use the fact that w_d are small and use DP with O(N * max_digit) but that would be O(N * 6) if we do convolution via DP? Actually, we can compute H(z) by iterating over numbers and updating a DP array of size N+1: for each number, multiply the polynomial by (1 + w_x z). Since w_x depends only on digit length, we can group by w_d. For each group d with count c_d, we need to multiply by (1 + w_d z)^{c_d}. This is equivalent to doing c_d multiplications by (1 + w_d z). If we do it naively, it's O(c_d * N) per group, total O(N^2). But we can use the fact that (1 + w_d z)^{c_d} can be computed via exponentiation by squaring using polynomial multiplication. But that's similar to NTT.

Another approach: Since w_d are powers of 10, and we only need the sum over subsets, maybe we can compute A_k and B_k using combinatorial formulas without full polynomial multiplication? Let's think.

A_k = sum_{T, |T|=k} prod_{x in T} 10^{len[x]}. This is like the coefficient in the expansion of prod_{x} (1 + 10^{len[x]} z). We can compute this using DP over numbers, but we need to do it efficiently.

We can compute A_k by iterating over numbers and updating a DP array: dp[k] = sum of products for subsets of size k. Initially dp[0]=1. For each number x, new_dp[k] = dp[k] + dp[k-1] * w_x. This is O(N^2) if we do for all k up to N. But we can note that w_x is small (10^d). However, we still need to update for each x, and for each k from current max down to 0. That's O(N^2) = 4e10, too slow.

But we can group by w_d. For each group d with count c_d, we need to multiply the polynomial by (1 + w_d z)^{c_d}. This can be done using the fact that (1 + w_d z)^{c_d} = sum_{j=0}^{c_d} binom(c_d, j) w_d^j z^j. So we can compute this polynomial explicitly in O(c_d) time. Then we need to multiply the current polynomial (degree up to sum of previous c's) by this new polynomial. The multiplication of two polynomials of degrees a and b takes O((a+b) log(a+b)) with NTT, or O(a*b) with naive. Since total degree is N, and we have 6 multiplications, NTT is the way.

So we need NTT.

Let's implement NTT in Python. We can use the iterative bit-reversal and precomputed roots.

We need to be careful with recursion depth and speed.

Alternatively, we can use the fact that the modulus is 998244353 and use the library 'atcoder' if available? But we are writing from scratch.

We can also use the 'numpy' FFT with rounding? But we need exact modulo arithmetic. We can do FFT with real numbers and round, but risk of errors. Better to implement NTT.

Given the time constraints, I'll implement NTT in Python.

Steps for NTT:
- Function ntt(a, mod, root, invert): a is list of integers. mod = 998244353, root = 3.
- Compute n = len(a). It must be power of 2.
- Compute bit-reversed order.
- For length = 2,4,...,n:
    wlen = root^( (mod-1)/length ) if not invert else root^( (mod-1)/length )^{-1}
- Then loop.

We need pow for modular exponent.

We can precompute roots for each length up to max_n.

But we can compute on the fly.

Given that we only need a few NTTs, we can write a general polynomial multiplication function using NTT.

Implementation details:

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
        wlen = pow(3, (MOD-1)//length, MOD)
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
    fa = a + [0]*(n - len(a))
    fb = b + [0]*(n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:len(a)+len(b)-1]

This is standard.

Now, compute H(z):
- For each d=1..6:
    c = c_d
    if c == 0: continue
    w = pow(10, d, MOD)
    poly = [0]*(c+1)
    for j in range(c+1):
        binom = fact[c] * inv_fact[j] % MOD * inv_fact[c-j] % MOD
        poly[j] = binom * pow(w, j, MOD) % MOD
- Multiply these polys using multiply function. Start with [1].
- After each multiplication, truncate to degree N (since we don't need higher).
- Final H = result.

Compute R(z):
- Initialize R = [0]*(N) (since we need up to degree N-1).
- For each d=1..6:
    if c_d == 0: continue
    w = pow(10, d, MOD)
    S = S_d
    # Compute series T(z) = z/(1+w*z) = sum_{m=0}^{N-2} (-w)^m z^{m+1}
    # So coefficient of z^{k} for k>=1 is (-w)^{k-1}
    # Multiply by S * w
    coeff = S * w % MOD
    cur = 1
    for k in range(1, N):
        R[k] = (R[k] + coeff * cur) % MOD
        cur = cur * (-w) % MOD
- Note: R[0] remains 0.

Compute Q(z) = multiply(H, R) truncated to degree N-1.

Extract A_k = H[k] for k=0..N-1, B_k = Q[k] for k=0..N-1.

Compute answer:
total_sum = N*(N+1)//2 % MOD
ans = 0
for k in range(N):
    term = fact[N-k-1] * fact[k] % MOD
    val = (total_sum * A_k - B_k) % MOD
    ans = (ans + term * val) % MOD

Print ans.

We need to handle large N up to 2e5. Factorials up to N.

Potential issues:
- The polynomial multiplication might be slow in Python for N=2e5. But with NTT, it should be okay if optimized. However, Python's NTT might be borderline. We can try to optimize by using local variables and avoiding attribute lookups.

Alternatively, we can use the fact that we only need H and Q up to degree N-1, and we can compute them using DP with O(N * sqrt(N))? Not sure.

Another idea: Since w_d are powers of 10, we can compute A_k using a combinatorial approach: A_k = sum_{a_1+...+a_6=k} prod_d binom(c_d, a_d) w_d^{a_d}. This is a 6-dimensional sum. We can compute it using generating functions with 6 variables, but we can reduce to 1D by iteratively convolving. That's exactly what polynomial multiplication does.

We can do the convolution using FFT with numpy? Let's check: numpy.fft can do FFT of size 524288 in milliseconds. But we need to do it modulo 998244353. We can do FFT with real numbers, round to nearest integer, and take mod. Since the coefficients are integers less than MOD, and the convolution result is less than MOD * N, which is about 2e5 * 1e9 = 2e14, which fits in double precision (53 bits). So we can use numpy FFT with rounding. This is much faster than implementing NTT in Python.

Steps with numpy:
- Use np.fft.fft to compute convolution.
- But we need to do it modulo 998244353. We can compute the convolution in integers using FFT with real numbers, then round and take mod. However, we need to ensure no precision loss. Since the maximum coefficient in H is sum of binom(c_d, a_d) w_d^{a_d} which can be large. For example, w_d = 10^6, c_d ~ 1e5, the maximum coefficient might be around (1+10^6)^{1e5} which is huge. But we are working modulo 998244353. The actual integer value before mod can be huge, but we can compute it modulo MOD using NTT. With numpy FFT, we would need to compute the exact integer convolution, which is impossible because the numbers are too large.

So we cannot use numpy FFT for exact modulo arithmetic unless we do multiple modulations. But we can use NTT.

Given that, we need to implement NTT in Python. Let's write an efficient NTT.

We can precompute the roots for each length to speed up. But since we only do a few transforms, we can compute on the fly.

We need to be careful with the inner loop. Using range and local variables is okay.

Let's estimate time: For n=524288, the NTT has about n * log2(n) = 524288 * 19 = 10 million butterfly operations. Each operation involves a few modular multiplications and additions. In Python, 10 million operations might take a few seconds. We have a few NTTs, so maybe 10-20 seconds. That might be too slow for the time limit (usually 2 seconds). We need a faster approach.

Alternative: Use the fact that we only need to multiply polynomials where one factor is (1 + w_d z)^{c_d}. We can compute H(z) using the binomial theorem and then multiply using a divide-and-conquer approach with NTT, but we can also use the fact that w_d are small and use DP with O(N * max_w) but that's not helpful.

Another idea: Since w_d are powers of 10, and we only need the sum over subsets, we can compute A_k and B_k using a different combinatorial approach.

Let's think about the structure. We have numbers grouped by digit length. For each group d, the numbers are consecutive integers from L_d to R_d. Their values are not just the digit length, but the actual integer. However, in the sum B_k = sum_{T, |T|=k} (sum_{x in T} x) * prod_{y in T} w_y, the factor sum_{x in T} x can be expressed as sum over groups: sum_{d} sum_{x in T, len(x)=d} x.

We can compute B_k by linearity: B_k = sum_{d} sum_{x in group d} x * w_x * A_{k-1}^{(x)}. But A_{k-1}^{(x)} is the elementary symmetric sum of degree k-1 of the set excluding x. This is similar to the derivative approach.

We can compute the polynomial H(z) = prod_{x} (1 + w_x z). Then consider the polynomial H_d(z) = prod_{x in group d} (1 + w_x z). But w_x is constant within group, so H_d(z) = (1 + w_d z)^{c_d}. Then H(z) = prod_d H_d(z).

Now, B_k = sum_{T, |T|=k} (sum_{x in T} x) prod_{y in T} w_y.

We can write B_k = sum_{d} sum_{x in group d} x * w_d * (sum_{T: x in T, |T|=k} prod_{y in T\{x}} w_y).

For a fixed x, the inner sum is the coefficient of z^{k-1} in H(z) / (1 + w_d z). So B_k = sum_{d} w_d * (sum_{x in group d} x) * [coeff of z^{k-1} in H(z)/(1+w_d z)].

Let S_d = sum_{x in group d} x. Then B_k = sum_{d} S_d * w_d * coeff_{k-1} ( H(z) / (1 + w_d z) ).

Now, H(z) / (1 + w_d z) = H(z) * (1 - w_d z + w_d^2 z^2 - ...). So we can compute the series expansion of 1/(1+w_d z) up to degree N-1, multiply by H(z) (truncated to degree N), and get coefficients.

But we still need to multiply H(z) by a series for each d. That's 6 multiplications. We can compute the series for each d, then multiply by H(z) using NTT. But we can also compute Q(z) = H(z) * R(z) where R(z) = sum_d S_d * w_d * (z/(1+w_d z)). This is exactly what we had.

So we need to compute H(z) and then multiply by R(z). The bottleneck is computing H(z).

Can we compute H(z) without NTT? Since H(z) = prod_d (1 + w_d z)^{c_d}, and w_d are distinct, we can compute the coefficients using a DP that iterates over the groups and does convolution. But the convolution of two polynomials of degrees a and b can be done in O(a*b) if we use naive multiplication. Since total degree is N, and we have 6 groups, the total work if we do naive multiplication might be O(N^2) in the worst case. But we can do it in O(N * sqrt(N)) using divide and conquer? Not really.

Wait, we can compute H(z) using the fact that (1 + w_d z)^{c_d} can be computed via binomial coefficients in O(c_d) time. Then we have 6 polynomials. We can multiply them using a balanced tree. The total work using naive multiplication is sum over pairs of degrees. If we multiply the two largest polynomials first, the intermediate degrees grow. The total work for naive multiplication of polynomials with degrees d1, d2, ..., d6 is O( sum_{i} d_i * D_i ) where D_i is the degree of the product of previous ones. In the worst case, it's O(N^2). But maybe we can use FFT via numpy with splitting? No.

Another idea: Since w_d are powers of 10, we can compute A_k using a combinatorial sum over the counts a_d. A_k = sum_{a_1+...+a_6=k} prod_d binom(c_d, a_d) w_d^{a_d}. This is a 6-dimensional sum. We can compute it by iterating over a_1 from 0 to min(c_1, k), then a_2 from 0 to min(c_2, k-a_1), etc. The number of terms is the number of integer solutions to a_1+...+a_6=k with 0<=a_d<=c_d. This number can be large (on the order of k^5 for small k, but for large k it's bounded by the number of ways to partition k into 6 parts, which is O(k^5). For k up to N=2e5, k^5 is huge. So not feasible.

We need a faster method.

Let's reconsider the NTT implementation. We can write the NTT in Python using a class with precomputed roots and bit-reversal. We can also use the 'pypy' interpreter which is faster for such tasks. Since the problem is from AtCoder (likely), and the modulus is 998244353, NTT is the standard approach. In Python, it's common to use PyPy with optimized NTT. We can write the NTT carefully.

We can also use the fact that we only need to multiply polynomials of degree up to N. We can use the 'numpy' FFT with splitting the modulus? There is a technique to do FFT modulo a prime using multiple FFTs with different primes and CRT, but that's overkill.

Maybe we can use the 'pyfftw' or 'numpy.fft' with rounding and hope that the coefficients are small enough? But as noted, the coefficients can be huge. However, we are working modulo 998244353, so the coefficients are less than MOD. The convolution result before mod is sum of products of coefficients. The maximum coefficient in H is the coefficient of z^N, which is prod_d w_d^{c_d} = 10^{sum_d d * c_d}. This is 10^{total digits}. For N=2e5, total digits is about N * average digits ~ 2e5 * 5 = 1e6. So 10^{1e6} is astronomically large. So we cannot compute the exact integer convolution.

Thus, we must use NTT modulo 998244353.

So we need an efficient NTT in Python.

Let's write an NTT that is optimized for speed. We can use the iterative version with precomputed roots for each length. Since we only need up to length 2^19 = 524288, we can precompute the roots for each length.

Alternatively, we can use the 'atcoder' library's convolution function if we are allowed to import it? But we are writing from scratch.

We can also use the fact that we only need to multiply a few polynomials. We can write a function that multiplies two polynomials using NTT, and call it a few times.

Let's implement NTT with the following optimizations:
- Use local variables for MOD, etc.
- Precompute the roots for each length in a list.
- Use memoryviews or lists.

But precomputing roots for all lengths up to max_n might take time and memory. We can compute on the fly.

Given the time, I'll write a standard NTT and hope it's fast enough. In PyPy, it's usually okay for N=2e5.

Let's code it.

We'll need:
- pow_mod for exponentiation.
- ntt function.
- multiply function.

We'll also need factorials and inverse factorials.

Let's write the code.

One more thing: For the polynomial R(z), we need to compute it up to degree N-1. We can compute it as a list of length N.

Now, let's code.

We'll read N, compute c_d and S_d.

Compute factorials up to N.

Compute H(z):
- Start with poly = [1]
- For each d in 1..6:
    c = c_d
    if c == 0: continue
    w = pow(10, d, MOD)
    # Compute (1 + w*z)^c
    p = [0]*(c+1)
    for j in range(c+1):
        binom = fact[c] * inv_fact[j] % MOD * inv_fact[c-j] % MOD
        p[j] = binom * pow(w, j, MOD) % MOD
    poly = multiply(poly, p)
    # Truncate to degree N
    if len(poly) > N+1:
        poly = poly[:N+1]

After loop, H = poly.

Compute R(z):
- R = [0]*N
- For each d in 1..6:
    c = c_d
    if c == 0: continue
    w = pow(10, d, MOD)
    S = S_d
    coeff = S * w % MOD
    cur = 1
    for k in range(1, N):
        R[k] = (R[k] + coeff * cur) % MOD
        cur = cur * (-w) % MOD

Compute Q = multiply(H, R)
- Truncate Q to degree N (since we need up to N-1, but multiply returns degree len(H)+len(R)-1, which is at most 2N. We only need first N coefficients.
- Q = Q[:N]

Now compute answer.

Let's test with sample N=3.

We need to ensure that the NTT works correctly.

Potential issue: The multiply function uses NTT which requires power of two length. We need to handle the case when len(a)+len(b)-1 is small.

Also, for the polynomial (1 + w_d z)^{c_d}, the degree is c_d. For d=6, c_6 can be up to ~1e5. So the polynomial has length ~1e5. Multiplying with current poly (degree up to sum of previous c's) will increase degree. The final H has degree N.

The NTT size will be next power of two >= 2N. For N=2e5, 2N=4e5, next power of two is 524288. That's fine.

Now, let's write the code.

We need to be careful with the NTT implementation. I'll write a version that is known to work in Python.

Here's a common implementation:

def ntt(a, mod, root, invert):
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
        wlen = pow(root, (mod - 1) // length, mod)
        if invert:
            wlen = pow(wlen, mod - 2, mod)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % mod
                a[j] = (u + v) % mod
                a[j + half] = (u - v) % mod
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod

def multiply(a, b, mod=998244353, root=3):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, mod, root, False)
    ntt(fb, mod, root, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % mod
    ntt(fa, mod, root, True)
    return fa[:len(a) + len(b) - 1]

This should work.

Now, we need to compute factorials. Since N up to 2e5, we can compute fact and inv_fact in O(N).

Let's write the full code.

We'll test with the samples.

One more thing: For N=1, the loop for k in range(1,N) will be empty, so R = [0]. H = [1,10]. Q = multiply([1,10], [0]) = [0]. Then B_1=0? Wait, for N=1, we need B_0 and B_1? Actually k goes from 0 to N-1=0. So we only need A_0 and B_0. A_0=1, B_0=0. The loop for k in range(N) will run for k=0 only. So it's fine.

But in the computation of R, we have R[0]=0, and we don't use R[0] in Q because Q[0] = H[0]*R[0] = 0. But we need B_0=0, which is correct.

Now, let's code.

We'll also need to handle the case when c_d is 0. For d where c_d=0, we skip.

Edge case: N=0? Not possible since N>=1.

Now, let's write the code in the final answer.

We'll enclose in the required delimiters.

I'll write the code now.### PLAN
We need to compute the sum of f(P) over all permutations P of (1..N), where f(P) is the integer formed by concatenating the decimal representations. For each position i, the number placed there contributes its value times 10^{sum of digits of numbers after it}. By symmetry, each number appears equally often in each position, and the exponent depends only on the multiset of numbers after position i. This leads to a formula involving elementary symmetric sums of weights w_x = 10^{len(x)}. We compute these sums efficiently using polynomial multiplication via NTT (Number Theoretic Transform) modulo 998244353. The polynomial H(z) = ∏(1 + w_x z) gives the required sums A_k (subsets of size k). The sums B_k (with extra factor sum of values) are obtained via Q(z) = H(z) * R(z), where R(z) = ∑_d S_d * w_d * z/(1 + w_d z) and S_d is the sum of numbers with d digits. Finally, we combine A_k and B_k with factorials to get the answer.
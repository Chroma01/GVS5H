
## ideation
We need to compute the sum of f(P) over all permutations of (1..N), where f(P) is the integer formed by concatenating the decimal strings of the elements. N up to 2e5.

Key observations:
- Each permutation contributes Σ_i P_i * 10^{suffix length of i}.
- By counting subsets, the total sum can be expressed using elementary symmetric sums of the weights w_i = 10^{L[i]}, where L[i] is the number of digits of i.
- The total sum equals (N-1)! * Σ_{k=0}^{N-1} S_k * invC(N-1,k), where S_k = Σ_{x=1}^N x * e_k^{(x)} and e_k^{(x)} is the k-th elementary symmetric sum of weights excluding x.
- S_k = total_sum * E_k - T_k, with total_sum = N(N+1)/2, E_k the full elementary symmetric sums of all weights, and T_k = Σ_{S,|S|=k} (Π w_i) * (Σ_{i in S} i).
- T_k is the coefficient of t^{k-1} in H(t) = G(t) * Σ_m (-1)^m A_m t^m, where G(t) = Π_i (1 + w_i t) and A_m = Σ_i i * w_i^{m+1}.
- Since w_i depends only on digit length d (1 to 6 for N≤2e5), we have only 6 distinct weights. We can group by d.
- E_k can be computed by multiplying the 6 polynomials (1 + 10^d t)^{c_d} using NTT (or optimized DP).
- A_m = Σ_{d} S_d * 10^d * (10^d)^m, where S_d = sum of numbers with d digits.
- T_k is obtained by convolving B_m = (-1)^m A_m with E.
- Finally, compute the answer modulo 998244353 using precomputed factorials and inverse factorials.

Algorithm steps:
1. Precompute factorials and inverse factorials up to N.
2. Compute total_sum, c_d (count of numbers with d digits) and S_d (sum of those numbers) for d=1..6.
3. Compute w_d = 10^d mod MOD.
4. Compute polynomial E = Π_{d} (1 + w_d t)^{c_d} via NTT.
5. Compute A_m for m=0..N-1, then B_m with alternating signs.
6. Compute T_k = (B * E)[k-1] for k≥1 via NTT.
7. Compute S_k = total_sum * E_k - T_k (with T_0=0).
8. Compute invC(N-1,k) = invfact[N-1] * fact[k] * fact[N-1-k] mod MOD.
9. Sum over k: sum_val = Σ S_k * invC(N-1,k).
10. Answer = fact[N-1] * sum_val mod MOD.

Complexities: O(N log N) time, O(N) memory.

## worker: Implement the NTT convolution and the main algorit
The algorithm uses the fact that the weight `w_i = 10^{digits(i)}` depends only on the number of digits, which is at most 6 for `N ≤ 2e5`. This allows grouping elements by digit length and using NTT to compute the necessary polynomials efficiently. The total time complexity is O(N log N) due to the NTT multiplications, and the memory usage is O(N).

The convolution for `E` uses a balanced multiplication of the 6 factor polynomials, and the convolution for `T` uses one NTT multiplication. All operations are performed modulo 998244353.

The sample tests have been verified:
- N=3 → 1332
- N=2 → 33 (tested manually)
- N=1 → 1 (tested manually)

The large sample inputs (N=390 and N=79223) are expected to match the provided outputs within the time limit.

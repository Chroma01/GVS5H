
## ideation
The core difficulty is computing the sum of K-th powers of subarray sums efficiently for N up to 2e5 and K up to 10.

Observations:
- The sum over subarrays can be re-expressed using prefix sums. Let P_0=0, P_i = A_1+...+A_i.
- Then each subarray (l..r) corresponds to a pair (l-1, r) with l<=r, i.e., sum = P_r - P_{l-1}. So we need sum_{0 <= l < r <= N} (P_r - P_l)^K.

Approaches considered:
1. Direct O(N^2) enumeration is too slow.
2. Expand (P_r - P_l)^K using the binomial theorem:
   (P_r - P_l)^K = sum_{j=0..K} C(K,j) (-1)^{K-j} P_r^j P_l^{K-j}.
3. Then sum over all l<r becomes:
   sum_{j=0..K} C(K,j) (-1)^{K-j} * (sum_{r=0..N} P_r^j * (sum_{l < r} P_l^{K-j})).
4. This can be computed in O(N*K) by sweeping r from 0..N, maintaining running sums S_e = sum_{l < current r} P_l^e.
   For each r, contribution = sum_{j=0..K} C(K,j) (-1)^{K-j} * P_r^j * S_{K-j}.
   Then update S_e += P_r^e for next iterations.

This yields O(N*K) time, O(K) extra space, with K<=10 and N<=2e5, easily fast enough.

Pitfalls:
- We must include P_0=0 correctly. The subarray starting at index 1 corresponds to l=0. The initial S_e should be sum_{l < 0} ... which is zero. So we process r=0..N inclusive, but careful: we want pairs (l,r) with l<r. If we start with S all zero, then for r=0 we add nothing (since S is zero), and we should not count P_0 - P_0 because l<r excludes l=r. Then we add P_0^e to S. So loop r=0..N: compute contribution using current S (which contains sums for l<r), then add P_r^e to S. This correctly handles the empty prefix.
- Modulo 998244353 is prime; precompute factorials and inverse factorials up to K (or up to N if needed for other methods, but here we only need binomial coefficients up to K<=10). Could also just precompute C(K,j) directly using small loops.
- Use modular exponentiation or simple multiplication because K is small (K<=10) — just compute P_r^e by repeated multiplication.
- Result must be modulo 998244353; ensure handling of negative numbers via adding MOD.

Alternative approaches (not needed):
- Polynomial generating functions, but overkill.
- Divide and conquer FFT based methods, unnecessary given K is tiny.

Complexity:
- O(N*K) time, O(K) space.

## worker: Implement the solution in Python: read N, K, array
The implementation follows the derived O(N·K) sweep using prefix sums and the binomial expansion of \((P_r - P_l)^K\). For each \(r\) from 0 to N, we compute the contribution using the running sums \(S_e = \sum_{l<r} P_l^e\) and then update those sums with the current prefix value. Binomial coefficients are computed using integer arithmetic (K ≤ 10), and modular arithmetic is applied for the final answer. The approach correctly handles the empty prefix \(P_0 = 0\) and ensures that the pair \((l,l)\) is never counted because we update \(S\) after computing the contribution. The sample test cases should produce the expected outputs (75, 0, and 428633385 respectively).

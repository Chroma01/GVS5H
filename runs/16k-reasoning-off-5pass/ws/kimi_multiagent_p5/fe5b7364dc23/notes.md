
## ideation
The core difficulty: N up to 2e5 means O(N²) subarray enumeration is impossible; K ≤ 10 is small, so the natural trick is binomial expansion of (S_r − S_{l−1})^K where S denotes prefix sums (S_0 = 0). Expanding: (S_r − S_j)^K = Σ_{b=0}^{K} C(K,b) S_r^b (−1)^{K−b} S_j^{K−b}. So the answer = Σ over pairs 0 ≤ j < r ≤ N of Σ_b C(K,b)(−1)^{K−b} S_r^b S_j^{K−b}. For each b, Σ_{r} S_r^b · (Σ_{j<r} S_j^{K−b}) can be computed in a single left-to-right sweep: maintain running sums T_a = Σ_{j<r} S_j^a for a = 0..K, add T_{K−b} · S_r^b · C(K,b)(−1)^{K−b} to the answer, then update T_a += S_r^a. Powers S_r^a for a=0..K can be computed per prefix in O(K) via repeated multiplication (or pow with mod). Complexity O(NK + K²), easily fast enough. Pitfalls: (1) sign handling for (−1)^{K−b} — do modular subtraction carefully; (2) include j=0 (prefix sum 0) — initialize T_0 = 1 (since S_0^0 = 1) and T_a = 0 for a ≥ 1 (0^a = 0); note 0^0 = 1 convention is correct here since binomial expansion term S_j^0 = 1 even when S_j = 0; (3) A_i can be 0 and prefix sums must be reduced mod p before powering; (4) K can be up to 10 so K² binomial terms is trivial; (5) binomial coefficients small — compute via Pascal or direct formula; (6) answer must be non-negative mod — add p before final mod if using subtraction.

## worker: Write the complete Python solution: read N, K and 
- Let S_0=0, S_r = A_1+...+A_r (mod p). Each subarray sum over [l, r] equals S_r − S_{l−1}, so the answer is Σ_{0≤j<r≤N} (S_r − S_j)^K.
- Binomial expansion: (S_r − S_j)^K = Σ_{b=0}^{K} C(K,b) S_r^b (−1)^{K−b} S_j^{K−b}.
- Sweep r from 1..N maintaining T[a] = Σ_{j<r} S_j^a. Contribution of this r is Σ_b C(K,b)(−1)^{K−b} S_r^b · T[K−b]. Then add S_r^a into T[a].
- Initialization T[0]=1 accounts for j=0 (S_0^0 = 1, S_0^a = 0 for a≥1).
- Complexity O(NK + K²) time, O(K²) memory (could be O(K), but K≤10 so irrelevant).
- Verified sample 1 mentally: subarray sums 3,1,2,4,3,6 → squares 9+1+4+16+9+36=75. The sweep reproduces this: pairs (j,r) give exactly those six terms.
- Sign handled by subtracting when (K−b) is odd; ans kept in range via modulo each iteration.

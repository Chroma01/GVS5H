We use prefix sums P_0=0, P_i = sum_{j=1..i} A_j. The sum over subarrays maps to sum_{0 <= l < r <= N} (P_r - P_l)^K.
Expand (P_r - P_l)^K = sum_{j=0..K} C(K,j) (-1)^{K-j} P_r^j P_l^{K-j}.
Summing over l<r, we can fix r and maintain running sums of P_l^e for l<r. As r iterates from 0..N, we add P_r^j * cur[K-j] to the answer, then update cur[e] += P_r^e.
All operations are modulo 998244353. This runs in O(N*K) time with K<=10.
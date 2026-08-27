- **Core counting:** Treat each valid arrangement as an unordered k-subset of the N = m*n cells. For any fixed unordered pair of distinct cells, the number of arrangements containing both cells is exactly C(N - 2, k - 2), independent of which cells are chosen. Therefore the answer is C(N - 2, k - 2) times the sum of Manhattan distances over all unordered pairs of grid cells.

- **Distance decomposition:** Manhattan distance separates into row distance plus column distance. For rows, each unordered pair of rows with distance d contributes d for every choice of one column in the first row and one column in the second row, giving n^2 cell pairs. Thus the row contribution is n^2 * S(m), where S(L) = sum_{i<j}(j-i) = L*(L-1)*(L+1)/6. Similarly, the column contribution is m^2 * S(n). The total over all unordered cell pairs is n^2*S(m) + m^2*S(n).

- **Binomial coefficient:** Since N <= 100000 and MOD = 1e9+7 is prime with N < MOD, factorial and inverse factorial arrays modulo MOD are valid. C(a,b) = fact[a] * invfact[b] * invfact[a-b] mod MOD. The implementation caches factorials as class attributes and rebuilds inverse factorials only when a larger limit is needed, making repeated calls efficient.

- **Modular arithmetic:** S(L) is computed modulo MOD using INV6 = 166666668, the modular inverse of 6. Values m and n are reduced modulo MOD before squaring. All multiplications are reduced modulo MOD to avoid large intermediate values.

- **Edge cases:** k = 2 gives C(N-2, 0) = 1. k = N gives C(N-2, N-2) = 1. If m = 1 or n = 1, the corresponding S term is zero. N = 2 works with C(0, 0) = 1. A guard for k < 2 returns 0, although constraints guarantee k >= 2.

- **Verification:** Example 1: m=2,n=2,k=2 gives S(2)=1, total cell-pair distance = 4*1 + 4*1 = 8, and C(2,0)=1, so answer 8. Example 2: m=1,n=4,k=3 gives S(4)=10, total cell-pair distance = 10, and C(2,1)=2, so answer 20. Additional checks: 1x2,k=2 gives 1; 2x3,k=6 gives 25; 3x3,k=2 gives 72; 1x100000,k=100000 gives S(100000) modulo MOD.

- **Complexity:** Factorial precomputation is O(N) time and O(N) memory for the maximum N seen. Each query after the cache is filled is O(1). With N <= 100000, this is easily within limits.

- **Pitfalls avoided:** Do not multiply by C(k,2) or k!, because the linearity-of-counting argument already accounts for all piece pairs inside arrangements. Do not use ordered cell pairs without a compensating factor. Do not perform modular division by 6 without using the modular inverse or exact integer division. Do not assume m*n can exceed MOD; under the constraints it cannot.

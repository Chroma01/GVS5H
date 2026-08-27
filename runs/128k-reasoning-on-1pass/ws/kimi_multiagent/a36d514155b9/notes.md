
## ideation
Core difficulty: the number of arrangements is C(m*n, k), which is astronomically large, so enumeration is impossible. The key is to avoid summing per arrangement and instead sum per pair of cells using symmetry/linearity.

The proposed plan is sound: pieces are identical, so arrangements are k-subsets of the N=m*n cells. For any fixed unordered pair of cells, it appears together in exactly C(N-2, k-2) valid arrangements. Therefore total answer = C(N-2,k-2) * S mod MOD, where S is the sum of Manhattan distances over all unordered pairs of grid cells.

S separates by coordinates: Manhattan distance is |dx|+|dy|, so row contributions and column contributions can be computed independently. For a fixed pair of rows, all n columns pair up, giving n^2 times the 1D row-distance sum; similarly columns give m^2 times the 1D column-distance sum. The needed 1D identity is sum_{0<=i<j<L} (j-i) = L*(L*L-1)//6, but under modulo use multiplication by inv(6) because MOD=1e9+7 is prime.

Pitfalls to watch: do not treat pieces as distinguishable; examples confirm unordered placements. Handle N=2 and k=2 where C(N-2,k-2)=C(0,0)=1. Avoid O(N^2) pair enumeration. Be careful that m or n can be 1e5 while the other is 1, but N=m*n<=1e5, so factorials up to N are fine. Use pow(6, MOD-2, MOD) or precomputed inverse factorials; integer division by 6 is only safe before modulo if using exact arithmetic, but modular inverse is cleaner. Validate against both examples before finalizing.

## worker: Implement the complete `Solution.distanceSum`: pre
- Pieces are identical, so arrangements are k-subsets of the N = m*n cells.
- By linearity/symmetry, each unordered pair of cells appears together in exactly C(N-2, k-2) arrangements, so the answer is C(N-2, k-2) * S, where S is the total Manhattan distance over all unordered cell pairs.
- S decomposes into independent row and column contributions: fixing a pair of rows gives n² column-pair combinations (and vice versa), so S = n²·f(m) + m²·f(n) with the 1D identity f(L) = Σ_{i<j}(j−i) = L(L²−1)/6, computed via modular inverse of 6 (MOD is prime).
- Verified against examples: (2,2,2) → C(2,0)·(4·1+4·1) = 8; (1,4,3) → C(2,1)·(16·0+1·10) = 20.
- Edge cases: k = 2 gives C(N-2, 0) = 1; m = 1 or n = 1 makes the corresponding f term zero; N ≤ 1e5 so O(N) factorial precomputation is fine. The guarded `comb` handles any out-of-range input safely.

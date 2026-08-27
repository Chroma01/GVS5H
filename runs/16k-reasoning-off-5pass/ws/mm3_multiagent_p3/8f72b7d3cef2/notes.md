
## ideation
**Core difficulty:**
We need, for each starting position K, the maximum size attainable by repeatedly absorbing adjacent strictly smaller slimes. Because absorption always removes a neighboring slime, the set of slimes present at any time is a contiguous subarray containing K. The process can continue only as long as each newly encountered slime is larger than the last absorbed one; otherwise the slime we would need to absorb next is larger than the current size, blocking further expansion in that direction.

**Reduction:**
- The feasible absorption sequence corresponds to extending leftward and rightward while maintaining a strictly increasing sequence of sizes when moving away from K.
- The maximal set of slimes that can be absorbed is exactly the maximal strictly increasing contiguous subarray that contains K.
- The final size is the sum of that subarray (since starting size + all absorbed sizes).

**Candidate approaches:**
1. Brute force per K (expanding left/right while monotone) → O(N²), too slow for N=5·10⁵.
2. Precompute longest strictly increasing subarray ending at each i and starting at each i in O(N) using two passes.
3. Use prefix sums to answer range sum queries in O(1).
4. Combine to compute B_K = sum of the maximal strictly increasing subarray containing K.

**Pitfalls:**
- Off-by-one in inc/right arrays; inc[i] is the length of the increasing segment ending at i, so left boundary is K - inc[K] + 1.
- Need long (64-bit) integers for sums (A_i up to 1e9, N up to 5e5 → sum up to 5e14).
- Strict inequality (<) matters: equal values break the chain.
- Make sure the subarray is maximal, not just any; using inc and right as defined gives the unique maximal strictly increasing segment containing K.

## worker: finalize
- The problem reduces to finding, for each position K, the maximal contiguous strictly increasing subarray that contains K.
- `inc[i]` gives the length of the longest strictly increasing segment ending at i; `right[i]` gives the length of the longest strictly increasing segment starting at i.
- The left boundary is `L = K - inc[K] + 1`, the right boundary is `R = K + right[K] - 1`.
- The answer is the sum of `A[L..R]`, obtained via prefix sums in O(1).
- Complexity: O(N) time, O(N) memory, works for N up to 5·10⁵. Uses 64-bit integers (Python int is arbitrary precision).

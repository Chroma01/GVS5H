
## ideation
**Core difficulty**
- The XOR equations `A[X_i] ^ A[Y_i] = Z_i` are linear over GF(2), so they can be split per bit position.
- For each bit, we get a system of equalities/inequalities on binary variables. This is exactly the “DSU with bipartite parity” problem.
- The minimum sum must be chosen across the `2 * 2^b` factor contributed by each bit independently.

**Key observations**
- Since each bit is independent, the global minimum sum is obtained by minimizing the number of 1s at each bit independently (and weighting by `2^b`).
- A connected component under the equality/inequality constraints is bipartite: all variables are determined up to a global XOR of the component.
- For each component and each bit, we can choose the assignment that places fewer 1s in that component.
- No contradictions across bits? Actually a contradiction can occur in any single bit (e.g., `x ^ x = 1`). If any bit has a contradiction, the whole instance is infeasible → output `-1`.

**Candidate approaches**
1. **Per-bit DSU with parity** (most natural):
   - Loop over bits `b = 0..30` (since `Z_i ≤ 10^9 < 2^30`).
   - Maintain DSU with `xor` (xor from node to its parent). `find(x)` returns (root, xor_to_root).
   - For each constraint `X_i, Y_i`:
     - Let `w = (Z_i >> b) & 1`.
     - If `w == 0`: merge `X_i` and `Y_i` requiring equal bits.
     - If `w == 1`: merge `X_i` and `Y_i` requiring different bits.
     - If merge detects contradiction, the instance is infeasible.
   - After processing all edges for bit `b`, for each component we count how many nodes have value 0 and how many have value 1 under one arbitrary assignment. Choose the assignment with the smaller number of 1s, set the global bit for that component accordingly.
   - Complexity: `O((N + M) * 31)` ≈ 6.3M operations, fast for the given limits.

2. **2-SAT per bit**: similar but more cumbersome; DSU is simpler.

3. **System of linear equations over GF(2) for all bits simultaneously**:
   - The unknowns are bits of `A_i`, but the cost function is non-linear (sum of integer values, not a linear function over GF(2)). So this approach is not directly suitable. The per-bit decomposition is crucial.

## worker: Implement the DSU with parity data structure and t
The solution treats each bit position independently because XOR constraints are linear over GF(2). For a fixed bit, each constraint `A[X] ^ A[Y] = Z` becomes either an equality (bit of Z is 0) or inequality (bit of Z is 1) on binary variables. This is exactly the "DSU with bipartite parity" problem.

For each bit:
- We run a DSU where each node stores `xor_to_parent` (the XOR from the node to its parent).
- When merging two sets, we set the `xor_to_parent` of one root to satisfy the parity condition.
- If we find that two nodes are already in the same set, we check that the implied XOR equals the required `Z` bit; otherwise we have a contradiction → no solution.

After processing all edges for the bit, each connected component has two possible global assignments (flip all bits). We count, under one arbitrary assignment (root=0), how many nodes would be 1. We then choose the assignment that yields fewer 1s, which minimizes the contribution of this bit to the total sum. The chosen bit values are OR-ed into the final answer `A`.

The algorithm runs in `O((N + M) * 31)` time and `O(N)` memory, well within limits.

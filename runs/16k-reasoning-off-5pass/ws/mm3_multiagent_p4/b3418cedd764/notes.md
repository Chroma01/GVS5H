
## ideation
We need to count assignments x_i ∈ [1, M] such that x_i ≤ x_{A_i} for all i. The graph defined by edges i → A_i is a functional graph. Cycles enforce equality of all x-values on the cycle, while trees attached to cycles are rooted toward the cycle.

Key steps:
1. Decompose the functional graph into cycles and trees attached to them.
2. For each tree node, compute DP f[u][k] = number of assignments in the subtree rooted at u (excluding the parent edge) where x_u = k. Transition: f[u][k] = ∏_{c child of u} (∑_{t=1}^k f[c][t]). Use prefix sums to achieve O(M) per child.
3. For a cycle of length L, each node u has an attached tree DP g[u][k] (which equals f[u][k] computed on its tree). The cycle nodes all share the same value v. The number of valid assignments for the whole component is ∑_{v=1}^M (∏_{u in cycle} g[u][v]).
4. Multiply the contributions of all components. Mod 998244353.

Complexities: O(N * M) time and memory (N, M ≤ 2025, product ≈ 4e6, fine in Python with careful array handling). Use iterative DFS to find cycles and build the reverse graph of tree edges only (excluding cycle edges). Then topologically process the trees from leaves upward.

Pitfalls:
- Must exclude cycle edges from the tree DP; otherwise cycles will be double-counted.
- The cycle contribution loop: compute prefix products or multiply directly; product over up to N=2025 values is fine.
- Modulo operations at every step.
- Memory: storing f for all nodes as list of length M+1 is okay (~2025*2026*4 bytes ≈ 16 MB, but Python overhead is larger; we can store as list of arrays or process trees and discard). Better: process each tree, compute g for its root, then delete. We'll store f for all nodes using list of lists of ints; 2025*2026 ≈ 4.1M integers, memory ~33 MB, which is acceptable.

## worker: Implement the solution in Python: read input, dete
The solution follows the plan:
1. **Cycle Detection**: Used DFS with state (unvisited, in-stack, processed) and a `path_pos` dictionary to efficiently record the nodes in each cycle without O(L) lookups. This correctly identifies all cycles in the functional graph.
2. **Tree Construction**: Built a `children` adjacency list containing only non-cycle edges. This ensures that each node (including cycle nodes) has children pointing toward it from the trees that eventually lead to the cycle.
3. **DP Computation**: Defined `f[u][k]` as the number of valid assignments for the subtree rooted at `u` (excluding the parent edge) when `x_u = k`. Used recursion with a depth of at most N (2025) and increased the recursion limit. The transition uses prefix sums to achieve O(M) per child, giving overall O(N * M) time. Since N and M are both ≤ 2025, N*M ≈ 4M, which is fast enough.
4. **Cycle Combination**: For each cycle, the values of all cycle nodes must be equal. The DP `f` for cycle nodes already accounts for their attached trees. We sum over the common value `v` the product of `f[u][v]` for all `u` in the cycle. Multiply the contributions of independent components modulo 998244353.
5. **Complexity**: Time O(N * M) and memory O(N * M). With N, M ≤ 2025, this is well within limits (the lists of size M+1 per node use about 2025*2026*8 bytes ≈ 33 MB, acceptable).

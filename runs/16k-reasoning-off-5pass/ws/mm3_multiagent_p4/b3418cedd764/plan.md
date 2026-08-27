We need to count assignments x_i ∈ [1, M] such that x_i ≤ x_{A_i} for all i. This defines a partial order: each node i must have value ≤ its parent A_i. The relation forms a functional graph (each node has out-degree 1). The condition forces values to be non-decreasing along directed edges, but cycles impose equality constraints.

Approach:
1. Find all cycles in the functional graph via standard DFS / visited marking.
2. For each cycle, all nodes in the cycle must have equal x-values (since x_i ≤ x_{A_i} and following the cycle gives x_i ≤ x_i, so equality). So a cycle of length L contributes a factor of M (choose the common value).
3. For each node not in a cycle, it eventually leads to some cycle. The constraint forms a rooted tree (forest) where edges point toward the cycle root. For such a tree, we need to count assignments where each node's value ≤ its parent.
   - This is equivalent to counting labelings of a rooted tree with labels 1..M where parent ≥ child.
   - For a tree with root r (which is on a cycle), the root's value is already fixed (equal to the cycle's common value). For each child subtree, we need to count assignments respecting the bound.
   - Process children subtrees independently given the parent's value v: number of ways for a subtree rooted at node u with upper bound v (i.e., x_u ≤ v) can be computed via DP.
4. DP for a tree: Let f[u][k] = number of assignments for subtree of u where x_u = k (1 ≤ k ≤ M). Then f[u][k] = product over children c of (sum_{t=1..k} f[c][t]). This is O(N * M^2) naive, but we can use prefix sums to make it O(N * M). Since N, M ≤ 2025, O(N * M) ≈ 4 million is fine.
5. For each cycle node, we need to combine the DP of its incoming tree (excluding cycle edges) with the cycle equality constraint. Since all cycle nodes share the same value v, we can:
   - For each cycle node u, compute g[u][v] = number of assignments of the tree attached to u (excluding cycle edges) where the root value (which is x_u) equals v. This is exactly f[u][v] computed on the tree part.
   - Then the total number of assignments for the whole component is: sum_{v=1..M} (product over cycle nodes u of g[u][v]).
   - This is O(L * M) per cycle, total O(N * M).
6. Multiply contributions of all components (since components are independent). Answer modulo 998244353.

Complexities: O(N * M) time, O(N * M) memory (can be optimized to O(N) by processing trees and discarding, but N*M ≤ ~4M, memory ~32MB for ints, acceptable). We'll implement with lists of size M+2 for each node.
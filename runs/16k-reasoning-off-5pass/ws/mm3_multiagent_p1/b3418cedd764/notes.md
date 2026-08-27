
## ideation
The problem is counting maps x: [N]→[M] such that x_i ≤ x_{A_i} for all i, where A is a functional graph. The graph decomposes into weakly connected components, each containing exactly one cycle. Within a component, all cycle nodes must share the same value v (since the cycle gives a chain of inequalities that closes). Tree nodes must have values ≤ their parent, so values flow from leaves (small) toward the cycle (largest v). For a fixed cycle value v, each tree node's value lies in [1, v], and values are non-increasing from the cycle outward. This is equivalent to counting antitone maps from each tree to a chain of size v. The number of antitone maps f(T,v) satisfies f(leaf,v)=v and f(internal node with children, v) = Σ_{r=1}^{v} Π f(child, r). For a component with cycle C = (c_1,…,c_c) and attached forests F_i, the contribution is Σ_{v=1}^{M} Π_i (Π over trees in F_i of f(T, v)). The final answer is the product of these contributions across components. Verified on all three samples (6, 2025, 10010). Complexity: O(N·M) which fits N,M ≤ 2025.

Pitfalls:
- Must build the full tree (not just first level) of non-cycle nodes.
- Cycle detection must work for self-loops and longer cycles.
- Recursion depth up to N; need to set recursion limit or go iterative.
- Use prefix sums to compute f(node, v) for all v efficiently.

## worker: Implement the algorithm in Python: detect cycles i
The algorithm works as follows:

1. **Cycle detection**: Since each node has out-degree 1, the graph consists of weakly connected components each containing exactly one cycle. Standard DFS with coloring finds all cycles.

2. **Tree structure**: Non-cycle nodes form a forest where parent = A[node]. We build `children[node]` for non-cycle nodes whose A-child is also non-cycle.

3. **DP f(u, v)**: For a tree node u and value v, this counts antitone maps (parent ≥ child) of the subtree rooted at u into {1,…,v}. The recurrence is:
   - f(leaf, v) = v
   - f(internal, v) = Σ_{r=1}^{v} Π_{child} f(child, r)
   
   Using prefix sums gives O(size × M) per node.

4. **Component sum**: For each cycle C = (c_1, …, c_k) with attached forests, contribution is:
   Σ_{v=1}^{M} Π_{i=1}^{k} Π_{tree T in forest of c_i} f(T, v)

5. **Final answer**: Product of component contributions.

Verified on all three samples: 6, 2025, 10010.

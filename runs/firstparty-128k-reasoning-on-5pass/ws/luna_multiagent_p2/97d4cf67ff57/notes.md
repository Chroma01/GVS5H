- **Subtree interpretation:** Any valid subgraph of a tree is a connected selected vertex set together with its unique connecting edges. Thus it is enough to select a connected subtree of the input tree.

- **Rooting:** Root the input tree arbitrarily. For any selected subtree, consider its highest selected vertex in this rooting. That vertex has no selected parent edge, so every possible answer is considered by evaluating every vertex as a potential highest vertex.

- **Attached DP states:** For each vertex \(v\), `dp0[v]` and `dp1[v]` describe a selected connected subtree containing \(v\) and using the edge from \(v\) to its parent.
  - `dp0` means no selected vertex has degree 4.
  - `dp1` means at least one selected vertex has degree 4.
  Since the parent edge contributes one degree to \(v\), \(v\) may select either zero children (degree 1) or exactly three children (degree 4).
  Therefore `dp0[v] = 1`, while `dp1[v]` comes from selecting exactly three child branches; \(v\) itself then has degree 4.

- **Child combination:** A selected child contributes its corresponding `dp0` or `dp1` value. A small knapsack over the number of selected children, limited to four, combines branches while tracking whether a degree-4 vertex has appeared. Each child is either skipped or selected once.

- **Highest selected vertex:** If \(v\) has no selected parent, its degree must be 1 or 4.
  - Degree 1 uses exactly one child, and that child branch must have the degree-4 flag.
  - Degree 4 uses exactly four children; \(v\) itself guarantees the flag.

- **Complexity:** Each edge performs only constant-size DP transitions. The total time complexity is \(O(N)\), and the memory complexity is \(O(N)\).

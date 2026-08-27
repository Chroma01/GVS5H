- **Connectivity threshold:** For two blocks \(s,t\), let \(T\) be the largest floor such that they are connected in the subgraph induced by blocks of height at least that floor. Equivalently, over every grid path from \(s\) to \(t\), maximize the minimum building height on that path.

- **Exact answer formula:** Let the endpoint floors be \(Y,Z\). The minimum stair count is
  \[
  Y+Z-2\min(T,Y,Z).
  \]
  Equivalently, if \(T\geq\min(Y,Z)\), the answer is \(|Y-Z|\); otherwise it is \((Y-T)+(Z-T)\).

- **Why one common horizontal floor suffices:** Put \(L=\min(T,Y,Z)\). Both endpoints have at least \(L\) floors, and by definition of \(T\) there is a walkway path connecting their blocks at floor \(L\). Descend from floor \(Y\) to \(L\), traverse for free, then ascend from \(L\) to \(Z\), costing \(Y+Z-2L\).

- **Why multiple horizontal levels cannot improve it:** Consider any route and let \(m\) be the minimum floor ever visited. Every block visited supports floor \(m\), since floors are contiguous from 1 upward. The route’s projected sequence of blocks therefore connects the endpoint blocks in the graph of buildings of height at least \(m\), so \(m\leq T\). Also \(m\leq Y,Z\). Since the route starts at \(Y\), reaches \(m\), and ends at \(Z\), its total vertical movement is at least \((Y-m)+(Z-m)\), which is at least \(Y+Z-2\min(T,Y,Z)\). This matches the construction.

- **Same-block case:** If both endpoints are in the same block, its threshold is its own height. Since both requested floors are valid, \(T\geq Y,Z\), so the formula becomes \(|Y-Z|\). The input guarantees the full triples differ, but same-block queries with distinct floors are allowed.

- **Preprocessing:** Activate cells in descending building height with DSU. Upon connecting two components at height \(h\), create a Kruskal reconstruction-tree node with value \(h\), as parent of the two component-tree roots. For distinct leaves, the value at their LCA is exactly their maximum connectivity threshold. Leaf values are their own building heights, covering same-cell queries.

- **Complexity:** Sorting cells costs \(O(HW\log(HW))\). The reconstruction tree has at most \(2HW-1\) nodes. Binary lifting uses \(O(HW\log(HW))\) memory and preprocessing time. Each query is answered in \(O(\log(HW))\).

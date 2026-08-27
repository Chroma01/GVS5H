- **Reduction:** In any valid alkane, the vertices of selected degree 4 form a connected subtree. Every such vertex must have original degree at least 4.
- **Leaf completion:** If an internal vertex has \(d\) adjacent internal vertices in the chosen internal subtree, it needs \(4-d\) leaf neighbors. Since its original degree is at least 4 and \(d \le 4\), enough incident edges remain to choose leaves.
- **Optimization target:** If the chosen internal subtree has \(k\) vertices, the alkane has exactly \(2k+2\) leaves and \(3k+2\) total vertices. Thus maximize \(k\).
- **Reduced graph:** Keep only original vertices with degree at least 4 and edges between them. This is a forest because the original graph is a tree.
- **Degree cap:** A chosen connected subtree of the reduced forest is valid exactly when each selected vertex has at most 4 selected reduced-forest neighbors.
- **DP:** Root every component of the reduced forest. For a non-root selected vertex whose parent edge is retained, it may retain at most 3 child edges:
  `down[v] = 1 + sum(largest 3 down[child])`.
- **Candidate roots:** A selected component whose topmost selected vertex is `v` may retain at most 4 child edges:
  `candidate[v] = 1 + sum(largest 4 down[child])`.
  The maximum candidate is the maximum number of internal vertices.
- **Existence:** Any eligible vertex alone yields a valid alkane with one degree-4 vertex and four selected leaves, so output `-1` exactly when no original vertex has degree at least 4.
- **Complexity:** Forest rooting and DP are linear aside from sorting child DP values. Total storage is \(O(N)\); worst-case time is \(O(N \log N)\), which is safe for \(N \le 2 \times 10^5\).

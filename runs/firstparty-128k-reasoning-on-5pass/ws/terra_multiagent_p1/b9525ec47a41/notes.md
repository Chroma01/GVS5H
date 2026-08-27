- **Key reduction:** The attainable indegree sequences are the exponent vectors in the support of \(\prod_{\{u,v\}\in E}(x_u+x_v)\). For an undirected graph, the number of such vectors equals the number of its spanning forests (all acyclic edge subsets). Thus count forests of the cycle with selected spokes to a hub.
- **Frontier:** Cut the closing cycle edge \(\{N-1,0\}\). While processing vertices left to right, retain only vertex \(0\), current outer vertex, and hub. A selected edge is forbidden exactly if its endpoints are already connected, ensuring selected edges form a forest.
- **States:** Let `(0, cur, hub)` have connectivity states: `0` all separate; `1` `0=cur!=hub`; `2` `0=hub!=cur`; `3` `cur=hub!=0`; `4` all connected. DP counts forest subsets yielding each state.
- **Initialization:** At vertex 0, `0` and current are the same vertex. If its spoke is omitted, initialize state 1 with count 1. If `s[0]=1`, selecting the spoke gives state 4 with count 1.
- **Transition for `s_i=0`:** After adding vertex `i`, choose or omit path edge from previous current vertex and forget that previous vertex:
  `n0=2d0+d1+d3`, `n1=d1`, `n2=2d2+d4`, `n3=d3`, `n4=d4`.
- **Transition for `s_i=1`:** Apply the path transition and then choose or omit spoke `(i,hub)`, rejecting its selection if already connected:
  `n0=2d0+d1+d3`, `n1=d1`, `n2=2d2+d4`, `n3=2d0+d1+2d3`, `n4=d1+2d2+2d4`.
- **Final edge:** The closing edge can always be omitted. It can be selected in states 0, 2, 3 only. Answer is `2d0+d1+2d2+2d3+d4`.
- **Complexity:** \(O(N)\) time and \(O(1)\) memory.
- **Validation:** For `N=3, s=010`, the DP gives 14. The implementation uses the stated transitions and modulo 998244353; it is suitable for \(N\le 10^6\).


## ideation


## worker: Parse `N, M, K`, the `M` weighted edges, and the s
The problem asks for the minimum possible sum of `f(A_i, B_i)` where `f(x,y)` is the smallest possible maximum edge weight on a path between `x` and `y`.  
In any Minimum Spanning Tree (MST) of the graph, the unique path between two vertices has maximum edge weight exactly `f(x,y)`.  

**Kruskal reconstruction tree** (also called a Kruskal tree) is built while running Kruskal’s algorithm:
- Process edges in non‑decreasing order of weight.
- When an edge `(u,v)` of weight `w` connects two different components, create a new internal node with weight `w`, make it the parent of the current roots of the two components, and unite the components.
- Leaves of this tree are the original vertices; an internal node’s weight equals `f(a,b)` for any pair of leaves whose lowest common ancestor (LCA) is that node.

Now the task becomes: on a rooted binary tree where each leaf has a number of “red” tokens (the A‑vertices) and “blue” tokens (the B‑vertices), match every red token with a distinct blue token minimizing the sum of the weights of the LCAs of the matched pairs.

A greedy bottom‑up strategy is optimal:
- At each internal node we have the two child subtrees.
- Any red from the left subtree paired with a blue from the right subtree (or vice‑versa) has its LCA exactly at this node, costing the node’s weight `w`.
- Since edge weights are non‑decreasing upward, pairing tokens at the earliest possible node never increases the total cost.
- Therefore, at each node we match as many cross pairs as possible:
  `matches = min(red_left, blue_right) + min(red_right, blue_left)`,
  add `matches * w` to the answer,
  and keep the remaining unmatched tokens for higher nodes.

Processing the internal nodes in the order they are created (i.e., increasing node index) implements this greedy DP. After the root is processed all tokens are matched and the accumulated sum is the minimum possible value.

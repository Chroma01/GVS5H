
## ideation
We need to count assignments \(x_i \in [1,M]\) such that \(x_i \le x_{A_i}\) for all \(i\). The graph defined by \(A\) is a functional graph. Each component has exactly one cycle. On a cycle, all nodes must have equal values due to the cyclic inequalities. For each cycle node, its attached trees require non‑decreasing values toward the cycle node.  

For a node \(u\) (not on a cycle) with children \(c_1,\dots,c_k\), define  
\[
dp_u[k] = \prod_{i=1}^k \Bigl(\sum_{t=1}^{k} dp_{c_i}[t]\Bigr),
\]  
where \(dp_u[k]\) is the number of ways to assign the subtree rooted at \(u\) when \(u\)’s value is exactly \(k\). For a leaf, \(dp_u[k]=1\).  

For a cycle node \(r\), the number of ways to assign its attached trees given that \(r\)’s value is \(k\) is exactly \(dp_r[k]\) (computed using only non‑cycle children).  

If a component has cycle nodes \(r_1,\dots,r_L\), then for a common value \(v\) the number of assignments is \(\prod_{i=1}^L dp_{r_i}[v]\). The component’s total is \(\sum_{v=1}^M \prod_i dp_{r_i}[v]\). Components are independent, so the final answer is the product of the component totals modulo \(998244353\).

We can find cycle nodes by repeatedly removing nodes with indegree \(0\). Then we process the remaining graph (which is a forest of trees rooted at cycle nodes) in post‑order. For each node we compute its \(dp\) array using prefix sums of children’s \(dp\) arrays. After computing a node’s \(dp\), we can free its children’s \(dp\) to save memory.

## worker: Implement the solution in Python: read N, M and A,
- We used topological removal to identify nodes that lie on cycles (those that never get indegree 0).
- The graph is a functional graph; reversing edges gives a forest where each tree is rooted at a cycle node.
- For each node we compute an array `dp_u[k]` (number of ways to assign its subtree when its value is exactly `k`) using the recurrence with prefix sums.
- Post‑order processing ensures children are handled before parents. We free a child's `dp` immediately after using it to keep memory usage low.
- Each component's answer is `∑_{v=1}^M ∏_{r∈cycle} dp_r[v]`. Components are independent, so we multiply their totals.
- The algorithm runs in O(N·M) time (≈4·10⁶ operations for the constraints) and uses O(N·M) memory in the worst case, which fits the limits.

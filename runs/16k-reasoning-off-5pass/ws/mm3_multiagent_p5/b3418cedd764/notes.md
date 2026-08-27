
## ideation
The problem requires counting sequences \(x\) of length \(N\) with values in \([1, M]\) satisfying \(x_i \leq x_{A_i}\). The graph is functional, so after contracting SCCs (which correspond to cycles), we get a DAG. In a functional graph, each SCC is a cycle, and after contraction, each SCC has out-degree at most 1. Each connected component contains exactly one cycle, which becomes a sink SCC. Thus the whole graph is a disjoint union of trees rooted at sinks. We can compute the number of valid assignments for each tree independently using DP. For a node \(v\) in the tree (with edges directed from child to parent), let \(dp[v][k]\) be the number of ways to assign values to \(v\) and all its descendants given \(x_v = k\). Then \(dp[v][k] = \prod_{u \in \text{children}(v)} \left( \sum_{j=1}^k dp[u][j] \right)\). The total for a sink is \(\sum_{k=1}^M dp[\text{sink}][k]\), and the answer is the product over all sinks. The constraints \(N, M \leq 2025\) allow an \(O(NM)\) solution with \(O(NM)\) memory.

## worker: Implement the solution in Python: parse input, fin
- The algorithm uses Kosaraju's algorithm to find SCCs in the functional graph.
- After contracting SCCs, the graph becomes a DAG where each component is a tree rooted at a sink (the cycle SCC).
- For each sink, we compute the number of valid assignments for its tree using DP: `dp[v][k] = product over children of (sum_{j=1..k} dp[u][j])`.
- Prefix sums are precomputed for efficiency.
- The total for each sink is summed over `k=1..M`, and the final answer is the product of these totals over all disjoint trees.
- Complexity: O(N + C*M + total_edges*M) = O(N*M) time and O(N*M) memory, with N, M ≤ 2025.

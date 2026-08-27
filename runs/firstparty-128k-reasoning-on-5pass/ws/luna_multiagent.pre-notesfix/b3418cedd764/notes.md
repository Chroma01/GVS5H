
## ideation
The core difficulty is handling the functional graph correctly: each component has one directed cycle and trees feeding into it. Inequalities around a directed cycle force every cycle vertex to have the same value, while the attached trees retain nontrivial dependencies. The main risks are reversing the tree orientation incorrectly, treating cycle vertices as independent, and accidentally counting the cycle contribution multiple times.

## worker: Implement the functional-graph tree DP: identify c
For every directed cycle, the inequalities around the cycle force all cycle variables to be equal. After removing cycle vertices, each remaining vertex forms a rooted tree directed toward its cycle.

For a non-cycle vertex `v`, `dp[v][k]` counts assignments of its subtree with `x_v <= k`. If the children of `v` are `u`, then the number of assignments with `x_v = t` is `product(dp[u][t])`; taking prefix sums over `t` gives `dp[v]`.

For each cycle component, multiply the attached-tree contributions for every possible common cycle value and sum over values. Components are independent, so their counts are multiplied. The total complexity is `O(NM)`.

## worker: Fix the tree-DP traversal order: process `removed_
Processed `removed_order` forward, since Kahn's elimination order lists non-cycle leaves before their ancestors. Thus every child's DP is available before computing its parent.

For each non-cycle vertex, the product of child prefix-DPs counts assignments for a fixed vertex value, and prefix summation gives the number of assignments with the vertex value bounded above. Cycle vertices must all have the same value, so each component contributes the sum over the common cycle value of all attached-tree contributions. Components are independent and therefore multiplied.

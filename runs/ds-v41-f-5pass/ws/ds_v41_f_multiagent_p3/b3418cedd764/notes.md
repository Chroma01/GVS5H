- **Problem model:** Functional graph with edges i -> A_i and constraints x_i <= x_{A_i}. Every directed cycle forces all its nodes to have equal value. Contracting cycles leaves a forest of non-cycle nodes feeding into cycles. The answer factors over weakly connected components, each containing exactly one cycle.

- **DP definition:** For a non-cycle node u, let G_u(k) be the number of valid assignments in u's subtree with x_u <= k. Then G_u(k) = G_u(k-1) + product over non-cycle children c of G_c(k). For a cycle node u with fixed cycle value v, its attached non-cycle children contribute f_u(v) = product over attached children c of G_c(v). A cycle component C contributes sum over v=1..M of product over u in C of f_u(v).

- **Kahn leaf-peeling:** Build reverse adjacency and indegrees. Queue nodes with indegree 0, pop them, and decrement the indegree of their parent A[u]. The removal order is leaf-to-root for all non-cycle nodes. After peeling, nodes with indegree > 0 are exactly the cycle nodes. Group cycle nodes by following A until returning to the start.

- **Rolling cumulative DP:** Maintain D[u] = G_u(v) for the current value v. Initially all D[u] = 0. For v = 1..M: process non-cycle nodes in peeled order, computing prod = product of D[c] over children c, then D[u] = (D[u] + prod) mod MOD. Then for each cycle component, compute its contribution at v by multiplying f_u(v) over its cycle nodes, and add this to the component's total modulo MOD. Finally multiply all component totals modulo 998244353.

- **Cycle edges:** For a cycle node, exclude the incoming edge from its cycle predecessor. All other incoming edges are attached non-cycle children, whose D values are already updated for the current v.

- **Complexity:** O(NM) time, O(N) extra memory. With N, M <= 2025, this is roughly 4 million inner child multiplications per run, well within Python limits.

- **Sample tests:** All three samples pass. Sample 1 outputs 6. Sample 2 outputs 2025. Sample 3 outputs 10010; verified by hand: cycle {0,6,8} contributes 5, cycle {3,4} contributes sum_v G_1(v)*v^2 = 1 + 20 + 126 + 480 + 1375 = 2002, product = 10010.

- **Edge cases:** N=1 self-loop returns M (condition is tautological). M=1 returns 1 (all values must be 1). Multiple disjoint cycles are independent, so the answer is the product of their component totals. Self-loops and multi-node cycles are handled uniformly by the same peeling and grouping logic.

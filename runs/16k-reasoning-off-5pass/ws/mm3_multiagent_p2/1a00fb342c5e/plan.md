Model the problem as a system of linear equations over GF(2) on each bit independently: for each bit position k, variable `a_i^k` (the k-th bit of A_i) must satisfy `a_{X_i}^k XOR a_{Y_i}^k = z_i^k`. This is a classic XOR‑equation / 2‑SAT‑on‑bits problem solved per connected component of the graph formed by the constraints.

For each component we run BFS/DFS assigning a value to the first node (0 or 1) and propagate the forced values. If a contradiction appears, the whole system is infeasible → output -1. Otherwise each component has two possible assignments. To minimise the total sum, we choose, independently per component, the assignment giving the smaller contribution to the final integer values.

To get the minimum sum we cannot just compare counts of 0/1 bits independently per component, because bits have different weights (2^k). The optimal choice is: try both assignments (root=0 and root=1), compute the resulting vector of values for the component, and pick the lexicographically smaller one when interpreted as a big number (higher bits dominate). Equivalently, we pick the assignment whose binary representation, treated as a number, is smaller. Since the total sum is the sum of component numbers, minimising each component independently is optimal.

Implementation steps:
1. Read N, M and edges.
2. Build adjacency list storing (neighbor, bitwise_z).
3. For each unvisited node, BFS its component, recording nodes, their distances/parent info, and producing two candidate value arrays (root=0, root=1) using XOR propagation.
4. Compare the two arrays as integers (built from bits) and keep the smaller one. Add to global answer.
5. After all components processed, output the array or -1.

Complexities: O((N+M)·log MaxZ) time, O(N+M) memory.
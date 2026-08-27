
## ideation
The problem can be modeled as a system of XOR equations on a graph where nodes are indices $1 \dots N$ and edges represent constraints $A_{X_i} \oplus A_{Y_i} = Z_i$.
1. **Graph Construction**: Build an adjacency list for the graph with $N$ nodes and $M$ edges. Each edge $(u, v)$ has weight $w = Z_i$.
2. **Connected Components**: Iterate through all nodes. For each unvisited node, start a BFS/DFS to traverse its connected component.
3. **Consistency Check**: During traversal, assign a relative value to each node based on the root's value. Let $A_{root} = K$. Then for any node $u$, $A_u = C_u \oplus K$, where $C_u$ is the XOR sum of edge weights along the path from the root to $u$. If we encounter a visited node $v$ via an edge $(u, v)$ with weight $w$, we check if $C_u \oplus w = C_v$. If not, the system is inconsistent, and we output -1.
4. **Optimization**: For each component, we have a set of relative values $\{C_u\}$. We need to choose $K$ to minimize $\sum_{u \in \text{component}} (C_u \oplus K)$. Since XOR operations on different bits are independent, we can determine each bit of $K$ separately. For bit position $b$:
   - Count how many $C_u$ have the $b$-th bit set (let this be `cnt`).
   - If we set the $b$-th bit of $K$ to 0, the contribution to the sum from this bit is `cnt` (since $1 \oplus 0 = 1$).
   - If we set the $b$-th bit of $K$ to 1, the contribution is `(size - cnt)` (since $1 \oplus 1 = 0$ and $0 \oplus 1 = 1$).
   - Choose the bit for $K$ that minimizes this contribution. Specifically, if `cnt > size - cnt`, set bit to 0; else set to 1.
5. **Reconstruction**: After determining the optimal $K$ for each component, compute the final values $A_u = C_u \oplus K$ and print them.

Pitfalls:
- Graph might be disconnected.
- Self-loops or multiple edges between same nodes need to be handled correctly by the consistency check.
- Large inputs require efficient I/O and $O(N+M)$ or $O((N+M) \log (\max Z))$ complexity. The bit-by-bit optimization is $O(30 \cdot N)$, which is efficient.

## worker: (None)
The problem is modeled as a system of XOR equations on a graph. Each constraint $A_{X_i} \oplus A_{Y_i} = Z_i$ is an edge with weight $Z_i$.
1. **Graph Traversal & Consistency Check**: We iterate through each node. If unvisited, we start a BFS/DFS to explore the connected component. During traversal, we assign a relative value $C_u$ to each node $u$ such that $A_u = C_u \oplus K$, where $K$ is the value of the root node. If we encounter an edge to an already visited node, we check if the existing relative value is consistent with the new path. If not, no solution exists, and we print -1.
2. **Optimization**: For each component, the values are $A_u = C_u \oplus K$. We want to minimize $\sum A_u$. Since XOR is bitwise independent, we can determine each bit of $K$ separately. For bit $b$, let $cnt$ be the number of $C_u$ with bit $b$ set. If we choose $K$'s bit $b$ to be 0, the contribution to the sum from this bit is $cnt$. If we choose 1, the contribution is $size - cnt$. We pick the bit value that minimizes this contribution.
3. **Complexity**: The graph traversal is $O(N + M)$. The optimization step iterates over 30 bits for each node in the component, totaling $O(30 \cdot N)$. Overall complexity is $O(N + M)$, which fits within the constraints.

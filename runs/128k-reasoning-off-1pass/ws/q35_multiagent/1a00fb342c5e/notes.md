
## ideation
The problem asks us to find a sequence $A$ that satisfies a set of XOR constraints $A_{X_i} \oplus A_{Y_i} = Z_i$ and minimizes the sum of elements in $A$. If no such sequence exists, we output -1.

Key observations:
1. The constraints form a graph where nodes are indices $1 \dots N$ and edges are the constraints.
2. Within each connected component, once the value of one node (the root) is fixed, the values of all other nodes in that component are determined by the XOR paths from the root.
3. If we encounter a contradiction (a node is reached with two different required values), then no solution exists.
4. For each connected component, let the relative values (offsets) from the root be $D_v$. Then $A_v = R \oplus D_v$, where $R$ is the value assigned to the root of the component.
5. The total sum is $\sum_{v} A_v = \sum_{v} (R \oplus D_v)$. Since XOR operates bitwise independently, we can optimize each bit of $R$ separately.
6. For a specific bit position $b$, let $c_0$ be the count of nodes in the component where the $b$-th bit of $D_v$ is 0, and $c_1$ be the count where it is 1.
   - If the $b$-th bit of $R$ is 0, the contribution to the sum from this bit is $c_1 \cdot 2^b$ (since $0 \oplus 1 = 1$).
   - If the $b$-th bit of $R$ is 1, the contribution to the sum from this bit is $c_0 \cdot 2^b$ (since $1 \oplus 0 = 1$).
   - We choose the bit for $R$ that minimizes this contribution.

Algorithm:
1. Build an adjacency list for the graph.
2. Use BFS/DFS to find connected components.
3. For each component:
   a. Pick a root, set its relative offset $D_{root} = 0$.
   b. Propagate offsets to all nodes in the component using BFS/DFS. Check for consistency. If inconsistent, return -1.
   c. For each bit position (0 to ~30, since $Z_i \le 10^9 < 2^{30}$), count $c_0$ and $c_1$ for the bits of $D_v$ across all nodes in the component.
   d. Determine the optimal bit for the root value $R$ at each position.
   e. Compute the final values $A_v = R \oplus D_v$.
4. Output the resulting sequence.

Pitfalls:
- Large N and M require efficient graph traversal (BFS/DFS with adjacency list).
- Bitwise optimization must be done correctly. Note that bits are independent for XOR sum minimization.
- Handle isolated nodes (components of size 1) correctly.
- Ensure all nodes are visited.

## worker: Build an adjacency list representation of the grap
The solution models the problem as a system of XOR equations over a graph. Each constraint $A_{X_i} \oplus A_{Y_i} = Z_i$ is an edge with weight $Z_i$. The graph is decomposed into connected components. For each component, we perform a BFS/DFS to determine relative XOR distances from an arbitrary root. If a contradiction is found (inconsistent XOR path), we output -1.

For each component, the value of each node $v$ is $A_v = R \oplus D_v$, where $R$ is the root's value and $D_v$ is the precomputed relative distance. To minimize $\sum A_v = \sum (R \oplus D_v)$, we optimize each bit of $R$ independently. For bit $b$, if $c_1$ nodes have the $b$-th bit of $D_v$ set to 1 and $c_0$ nodes have it set to 0, setting the $b$-th bit of $R$ to 0 contributes $c_1 \cdot 2^b$ to the sum, while setting it to 1 contributes $c_0 \cdot 2^b$. We choose the bit value that minimizes this contribution.

The algorithm runs in $O(N + M + N \cdot B)$ time where $B=30$ is the number of bits, which is efficient enough for the given constraints.

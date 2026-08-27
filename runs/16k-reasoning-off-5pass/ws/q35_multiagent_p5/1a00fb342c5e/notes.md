
## ideation
The core difficulty lies in efficiently solving a system of XOR constraints over potentially disconnected components, and then optimizing the absolute values of the variables to minimize their sum.

1.  **Graph Modeling**: The constraints $A_{X_i} \oplus A_{Y_i} = Z_i$ can be viewed as edges in a graph with $N$ nodes. Each connected component imposes relative constraints on the values of $A_i$ within that component.
2.  **Consistency Check**: Within each connected component, we can fix one node's value (e.g., to 0) and propagate the values to all other nodes in the component using BFS or DFS. If we encounter a node that has already been assigned a value, we check if the new required value matches the existing one. If not, the system is inconsistent, and we output -1.
3.  **Minimization Strategy**: Once relative values $R_i$ are determined for a component (where $A_i = R_i \oplus C$ for some constant $C$ specific to the component), we need to find $C$ that minimizes $\sum_{i \in \text{component}} (R_i \oplus C)$.
    *   The sum of integers is not linear with respect to XOR, but the contribution of each bit position to the total sum is independent.
    *   For each bit position $k$ (from 0 to ~30, since $Z_i \le 10^9 < 2^{30}$), we count how many $R_i$ in the component have the $k$-th bit set (let this be `cnt`).
    *   If we set the $k$-th bit of $C$ to 0, the $k$-th bit of $A_i$ is $R_i$'s $k$-th bit. The contribution to the sum from this bit is `cnt * 2^k`.
    *   If we set the $k$-th bit of $C$ to 1, the $k$-th bit of $A_i$ is flipped. The contribution is `(size - cnt) * 2^k`.
    *   We choose the bit for $C$ that yields the smaller contribution. This allows us to determine each bit of $C$ independently.
4.  **Complexity**: Building the graph and traversing components takes $O(N + M)$. Determining the optimal $C$ for each component involves iterating over bits (approx 30) and nodes in the component, which is also linear in the size of the component. Total time complexity is $O(N + M)$, which fits within the constraints ($N, M \le 2 \cdot 10^5$).

Pitfalls to avoid:
-   Forgetting to handle isolated nodes (components of size 1).
-   Incorrectly handling the bit independence assumption (it holds because the sum is a linear combination of bit contributions weighted by powers of 2, and choosing a bit in $C$ only affects that specific bit position in the sum).
-   Stack overflow with deep DFS recursion; using iterative BFS or increasing recursion limit is safer.

## worker: (None)
The solution models the problem as a graph where each constraint $A_{X_i} \oplus A_{Y_i} = Z_i$ is an edge. The graph is decomposed into connected components. For each component, we fix one node's relative value to 0 and propagate the values to all other nodes using BFS. If a contradiction is found (a node is reached with two different required values), we output -1.

Once the relative values $R_i$ for a component are determined, any valid assignment is of the form $A_i = R_i \oplus C$, where $C$ is a constant specific to the component. To minimize the sum $\sum A_i$, we determine each bit of $C$ independently. For each bit position $k$, we count how many $R_i$ have the $k$-th bit set. If setting the $k$-th bit of $C$ to 1 results in fewer set bits in the resulting $A_i$ values (i.e., more zeros), we choose 1 for that bit of $C$, as it reduces the sum. This greedy bit-by-bit approach works because the contribution of each bit to the total sum is independent.

The time complexity is $O(N + M)$ for graph traversal and $O(N \cdot B)$ for bit optimization, where $B$ is the number of bits (approx 30). This fits well within the constraints.

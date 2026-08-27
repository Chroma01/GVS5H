
## ideation
**Core Difficulty:**
The problem asks us to find a sequence $A$ satisfying a set of XOR constraints ($A_{X_i} \oplus A_{Y_i} = Z_i$) such that the sum $\sum A_i$ is minimized.
1.  **Consistency Check:** The constraints might be contradictory (e.g., $A_u \oplus A_v = Z_1$ and $A_u \oplus A_v = Z_2$ where $Z_1 \neq Z_2$, or a cycle where the XOR sum of edge weights doesn't match the implied node differences). We need to detect if no solution exists.
2.  **Minimization:** Since $A_i \ge 0$, minimizing the sum means making each $A_i$ as small as possible. In a connected component of the constraint graph, once the value of one node is fixed, all other nodes in that component are uniquely determined. To minimize the sum, we should choose the "base" value for each component such that the resulting $A_i$'s are minimized. Since the relationship is linear over GF(2) (XOR), if a solution exists for a base value $v$, then for any other base value $v'$, the new values are $A_i' = A_i \oplus (v \oplus v')$. We need to find $v$ such that $\sum (A_i \oplus \delta)$ is minimized, where $\delta = v \oplus v'$. However, a simpler observation is that if we fix one node to 0, we get a specific set of values. If we flip the "polarity" of the entire component (XOR every element in the component with some constant $C$), the constraints still hold. To minimize the sum, for each bit position $k$, we can independently choose whether to flip that bit for the whole component or not, based on which choice yields fewer 1s in that bit position across all nodes in the component.

**Candidate Approaches:**
1.  **Graph Traversal (BFS/DFS/DSU):**
    *   Build a graph where edges are $(X_i, Y_i)$ with weight $Z_i$.
    *   Identify connected components.
    *   For each component:
        *   Assign an arbitrary root value (e.g., 0).
        *   Propagate values to all reachable nodes. If a conflict is found (a node is reached twice with different required values), output -1.
        *   After determining the relative values (with root=0), analyze each bit position $k$ (from 0 to ~30, since $Z_i \le 10^9 < 2^{30}$).
        *   Count how many nodes in the component have the $k$-th bit set to 1 in the current configuration.
        *   If count > component_size / 2, flip the $k$-th bit for the entire component (XOR all nodes in component with $2^k$). This minimizes the number of set bits at position $k$.
        *   Accumulate the final values and the total sum.
    *   Output the sequence.

2.  **Disjoint Set Union (DSU) with Path Compression and XOR Tracking:**
    *   Use DSU to maintain connected components.
    *   Maintain `xor_val[u]` representing $A_u \oplus A_{root}$.
    *   When adding edge $(u, v)$ with weight $w$:
        *   Find roots $r_u, r_v$.
        *   If $r_u \neq r_v$: Merge sets. Set $A_{r_u} \oplus A_{r_v} = w \oplus xor\_val[u] \oplus xor\_val[v]$.
        *   If $r_u = r_v$: Check consistency. Calculate implied $A_u \oplus A_v$ using stored values. If it doesn't match $w$, return -1.
    *   After processing all edges, iterate through all nodes $1..N$. For each component, collect the values $A_i \oplus A_{root}$. Then apply the bit-flipping logic per component as described in Approach 1.
    *   DSU might be slightly cleaner for merging but requires a second pass to collect component values for the bit optimization. BFS/DFS is also perfectly fine and perhaps more intuitive for the "collect and flip" step. Given $N, M \le 2 \cdot 10^5$, either is efficient ($O((N+M)\alpha(N))$ or $O(N+M)$).

**Pitfalls:**
*   **Bitwise Logic:** Ensure correct handling of bit flips. Flipping a bit for the whole component is valid because $ (A \oplus C) \oplus (B \oplus C) = A \oplus B $. The constraint $A \oplus B = Z$ is invariant under XORing both $A$ and $B$ by the same constant.
*   **Large Numbers:** $Z_i$ up to $10^9$ fits in standard 64-bit integers. Python handles large integers automatically.
*   **Disconnected Components:** Must handle each component independently to minimize the sum globally (minimizing sum of parts minimizes total sum).
*   **Zero Constraints:** $Z_i$ can be 0. $X_i$ can equal $Y_i$ (self-loop). If $X_i = Y_i$ and $Z_i \neq 0$, immediate contradiction ($A_i \oplus A_i = 0 \neq Z_i$).
*   **Input Size:** $N, M$ up to $2 \cdot 10^5$. $O(N \log (\max Z))$ or $O(N \cdot 30)$ is acceptable. Iterating 30 bits per component is fine.

## worker: Read input $N, M$ and the list of constraints. Bui
1.  **Graph Representation**: The problem is modeled as a graph where nodes are indices $1 \dots N$ and edges $(X_i, Y_i)$ have weight $Z_i$. The condition $A_{X_i} \oplus A_{Y_i} = Z_i$ defines the relationship between connected nodes.
2.  **Component Processing**: Since the constraints are local to connected components, we process each component independently. For each component, we arbitrarily set the root node's value to 0. This determines the relative values of all other nodes in the component via BFS/DFS.
3.  **Consistency Check**: During traversal, if we encounter a visited node, we verify if the existing value satisfies the XOR constraint with the current node. If $A[u] \oplus A[v] \neq w$, the system is inconsistent, and we output -1.
4.  **Minimization**: Once relative values are fixed (with root=0), the absolute values can be shifted by XORing all nodes in the component with a constant $C$. To minimize $\sum A_i$, for each bit position $k$, we check if flipping the $k$-th bit for all nodes in the component reduces the total number of set bits. If the count of set bits at position $k$ is greater than half the component size, we flip that bit for all nodes in the component. This is valid because $(A \oplus C) \oplus (B \oplus C) = A \oplus B$, preserving all constraints.
5.  **Complexity**: Building the graph takes $O(M)$. BFS visits each node and edge once, taking $O(N+M)$. The bit optimization iterates 30 times over the component nodes, taking $O(30 \cdot N)$. Overall time complexity is $O(N + M)$, which fits within the limits ($N, M \le 2 \cdot 10^5$).

## worker: Run the code against the provided sample inputs to
The provided code implements the solution logic derived in the thought process:
1.  **Graph Construction**: It reads $N, M$ and the constraints, building an adjacency list where edges represent the XOR constraints.
2.  **Component Traversal**: It iterates through all nodes $1 \dots N$. If a node is unvisited, it starts a BFS to traverse the connected component.
3.  **Value Assignment**: It assigns an arbitrary value of 0 to the root of the component and propagates values to neighbors using $A[v] = A[u] \oplus w$.
4.  **Consistency Check**: During BFS, if a visited neighbor is encountered, it checks if the existing value satisfies the constraint. If not, it prints `-1` and exits.
5.  **Minimization**: After determining the relative values (with root=0), it iterates through each bit position (0 to 29). For each bit, it counts how many nodes in the component have that bit set. If the count is greater than half the component size, it flips that bit for all nodes in the component. This minimizes the sum because $(A \oplus C) \oplus (B \oplus C) = A \oplus B$, preserving constraints while minimizing the number of set bits.
6.  **Output**: Finally, it prints the sequence $A_1, \dots, A_N$.

The code handles all edge cases including disconnected components, self-loops (implicitly handled by consistency check), and large values of $Z_i$.

## worker: Run the provided code against Sample 1, Sample 2, 
The provided code correctly implements the logic derived in the thought process:
1.  **Graph Construction**: Reads $N, M$ and constraints, building an adjacency list.
2.  **Component Traversal**: Iterates $1 \dots N$, starting BFS for unvisited nodes to handle disconnected components.
3.  **Value Assignment**: Sets root to 0 and propagates $A[v] = A[u] \oplus w$.
4.  **Consistency Check**: Verifies $A[u] \oplus A[v] == w$ for visited edges. If mismatch, prints `-1`.
5.  **Minimization**: For each component, iterates bits 0-29. Counts set bits. If count > half, XORs all nodes in component with $2^{\text{bit}}$. This minimizes the sum while preserving constraints.
6.  **Output**: Prints $A_1 \dots A_N$.

Testing against samples:
-   **Sample 1**: Output `0 3 4`. Correct.
-   **Sample 2**: Output `-1`. Correct.
-   **Sample 3**: Output `0 2 9 6 0`. Correct.

The logic holds.


## ideation
The problem asks us to find a sequence $A$ of length $N$ such that for $M$ given constraints $A_{X_i} \oplus A_{Y_i} = Z_i$, the sum $\sum A_i$ is minimized. If no such sequence exists, output -1.

**Core Difficulty & Modeling:**
1.  **Graph Representation**: The constraints can be viewed as a graph where indices $1 \dots N$ are nodes. Each constraint $(X_i, Y_i, Z_i)$ is an edge between $X_i$ and $Y_i$ with weight $Z_i$.
2.  **Connected Components**: The problem decomposes into independent subproblems for each connected component of this graph. We can solve each component separately and sum the results.
3.  **Consistency Check (Odd Cycles)**: Within a connected component, if we arbitrarily fix the value of one node (say $u$) to 0, the values of all other nodes in that component are uniquely determined by the XOR constraints (since $A_v = A_u \oplus \text{path\_xor}(u, v)$). If we encounter a cycle where the XOR sum of edge weights along the cycle is not 0, a contradiction arises, and no solution exists.
4.  **Minimization (Even Cycles / Bipartite)**: If a component has no odd cycles (i.e., it is bipartite), the values of nodes are not uniquely determined. Specifically, if we set the root to 0, we get a set of values $V_0$. If we set the root to $K$, all values in the component flip bits relative to the previous assignment? No, that's not quite right for arbitrary numbers.
    *   Actually, let's re-evaluate the "minimization" logic.
    *   If the component is bipartite, we can partition the nodes into two sets $S_1$ and $S_2$ such that all edges connect a node in $S_1$ to a node in $S_2$.
    *   The constraint is $A_u \oplus A_v = Z_{uv}$.
    *   If we fix $A_{root} = x$, then for any $v$, $A_v$ is determined as $x \oplus d_v$, where $d_v$ is the XOR distance from root to $v$.
    *   However, the "degree of freedom" isn't just flipping a bit. The values are integers.
    *   Wait, the standard trick for XOR minimization on bipartite graphs works bit-by-bit.
    *   Let's reconsider. If the graph is bipartite, we can assign a "parity" $p_v \in \{0, 1\}$ to each node such that $p_u \neq p_v$ for every edge. But the constraint is $A_u \oplus A_v = Z$. This doesn't mean $A_u$ and $A_v$ have different parities in the usual sense unless $Z$ is odd.
    *   Actually, the relationship is linear over GF(2) for each bit position independently.
    *   For a specific bit $k$, let $a_{v,k}$ be the $k$-th bit of $A_v$. The constraint is $a_{u,k} \oplus a_{v,k} = z_{uv,k}$.
    *   This is exactly the same structure as the original problem but for a single bit.
    *   For each bit $k$:
        *   Construct a graph where edges exist if $z_{uv,k} = 1$.
        *   If this graph has an odd cycle (cycle with odd number of edges having weight 1), then no solution exists for bit $k$ (unless the cycle constraint is satisfied by 0, but if the cycle XOR sum is 1, it's impossible).
        *   If the graph is bipartite (no odd cycles in the "weight 1" subgraph), then for each connected component of this bit-graph, we have two choices: assign 0 to the root or 1 to the root.
        *   We calculate the cost (number of 1s) for both choices (Root=0 vs Root=1) and pick the one that minimizes the sum of bits for that component.
    *   We repeat this for all bit positions $0 \dots 29$ (since $Z_i \le 10^9 < 2^{30}$).
    *   Finally, reconstruct $A_i$ from the chosen bits.

**Refined Algorithm:**
1.  Initialize $A = [0] \times (N+1)$.
2.  Iterate bit $b$ from 0 to 29:
    *   Build an adjacency list for the current bit $b$. An edge $(u, v)$ exists if the $b$-th bit of $Z_{uv}$ is 1.
    *   Maintain `visited` array and `component_root_val` (or simply run a BFS/DFS to check consistency and count costs).
    *   For each unvisited node $u$:
        *   Start a traversal (BFS/DFS).
        *   Assign tentative value $val[u] = 0$.
        *   Propagate: for neighbor $v$ with edge weight $w$ (where $w$ is 1 if $b$-th bit of $Z$ is 1, else 0? No, the constraint is $A_u \oplus A_v = Z_{uv}$. For bit $b$, $a_{u,b} \oplus a_{v,b} = z_{uv,b}$. So if $z_{uv,b} == 1$, the bits must differ. If $z_{uv,b} == 0$, the bits must be same).
        *   Actually, it's easier to treat the whole integer logic first to check consistency, then optimize?
        *   **Correction**: The consistency check must be done on the full integers first. If the full system is inconsistent, output -1 immediately.
        *   If consistent, does that mean we can optimize bit by bit?
        *   Yes, because the constraints for different bits are independent. $A_u \oplus A_v = Z_{uv}$ implies for each bit $k$, $A_{u,k} \oplus A_{v,k} = Z_{uv,k}$. The choice of $A_{u,k}$ does not affect $A_{u, j}$ for $j \neq k$.
        *   So, Step 1: Check global consistency.
            *   Use Union-Find or BFS/DFS on the full graph.
            *   Assign $A_{root} = 0$. Propagate $A_v = A_u \oplus Z_{uv}$.
            *   If we find a node already assigned a different value, return -1.
        *   Step 2: Minimize sum.
            *   Since the system is consistent, for each connected component, the values are determined up to an additive constant? No, XOR doesn't work like addition.
            *   If the component is bipartite (in the sense of the XOR graph), we can flip the values of all nodes in one partition?
            *   Let's look at the structure again. $A_v = A_u \oplus D_{uv}$.
            *   If we change $A_u$ to $A_u \oplus K$, then $A_v$ must become $A_v \oplus K$ to maintain $A_u \oplus A_v = (A_u \oplus K) \oplus (A_v \oplus K) = A_u \oplus A_v$.
            *   So, for any connected component, we can choose a "flip value" $K$ (which is the same for all nodes in that component) and set $A'_v = A_v \oplus K$.
            *   We need to find $K$ that minimizes $\sum (A_v \oplus K)$.
            *   Since $K$ must be the same for the whole component, we cannot optimize bits independently across the component? Wait.
            *   If we choose $K$, it affects all bits of all nodes in the component simultaneously.
            *   However, notice that $A_v$ is determined relative to $A_{root}$. $A_v = A_{root} \oplus D_v$.
            *   So $A_v \oplus K = (A_{root} \oplus D_v) \oplus K = (A_{root} \oplus K) \oplus D_v$.
            *   Let $X = A_{root} \oplus K$. Then the new values are $X \oplus D_v$.
            *   We need to choose $X$ to minimize $\sum_{v \in Component} (X \oplus D_v)$.
            *   Since $X$ is a single integer, we can optimize bit by bit!
            *   For each bit $b$:
                *   Count how many nodes in the component have the $b$-th bit of $D_v$ equal to 0, and how many have it equal to 1.
                *   Let $c_0$ be count of nodes where $(D_v)_b = 0$.
                *   Let $c_1$ be count of nodes where $(D_v)_b = 1$.
                *   If we choose bit $b$ of $X$ to be 0, the cost contribution is $0 \cdot c_0 + 1 \cdot c_1 = c_1$.
                *   If we choose bit $b$ of $X$ to be 1, the cost contribution is $1 \cdot c_0 + 0 \cdot c_1 = c_0$.
                *   Choose 0 if $c_1 < c_0$, else choose 1.
                *   This determines the optimal bit for $X$.
            *   Construct $X$ from these optimal bits.
            *   Then the optimal sequence for the component is $A'_v = X \oplus D_v$.
            *   Note: $D_v$ is the XOR distance from the root. If the component has an odd cycle (in the XOR sense), the system would have been inconsistent in Step 1. So we assume consistency, meaning $D_v$ is well-defined.
            *   Wait, is it possible that a component has an odd cycle but is still consistent?
                *   Example: $1-2$ with 5, $2-3$ with 6, $1-3$ with 3. $5 \oplus 6 = 3$. Consistent.
                *   Example: $1-2$ with 5, $2-3$ with 6, $1-3$ with 4. $5 \oplus 6 = 3 \neq 4$. Inconsistent.
                *   So "odd cycle" in the context of XOR usually refers to a cycle where the XOR sum of weights is non-zero. If the XOR sum is zero, it's consistent.
                *   Does the "flip" logic require the graph to be bipartite?
                *   Let's re-read the logic. $A_v = A_{root} \oplus D_v$. This holds for ANY connected component, regardless of cycles, PROVIDED the system is consistent.
                *   If the system is consistent, then for any cycle, the XOR sum of weights is 0.
                *   Therefore, $D_v$ is well-defined and unique for all $v$ in the component relative to $A_{root}$.
                *   The transformation $A'_v = A_v \oplus K$ is valid for any $K$.
                *   The minimization logic (optimizing $X = A_{root} \oplus K$ bit by bit) holds.
                *   So, we don't need to check for bipartiteness separately. We just need to check for global consistency first. If consistent, we can always minimize by choosing the optimal $X$ for each component.

**Algorithm Refined:**
1.  Read Input.
2.  Build Adjacency List: `adj[u] = [(v, z), ...]`.
3.  Initialize `A` array of size $N+1$ with -1 (unvisited).
4.  Iterate $i$ from 1 to $N$:
    *   If `A[i]` is unvisited:
        *   Start BFS/DFS from $i$. Set `A[i] = 0`.
        *   Queue $Q = [i]$.
        *   While $Q$ not empty:
            *   Pop $u$.
            *   For each neighbor $(v, z)$:
                *   Expected $A[v] = A[u] \oplus z$.
                *   If `A[v]` is unvisited:
                    *   `A[v] = Expected`
                    *   Push $v$.
                *   Else:
                    *   If `A[v] != Expected`: Return -1 (Inconsistent).
5.  If loop completes without error, proceed to minimize.
6.  Initialize `ans` array of size $N+1$ (will store the final values).
7.  Iterate $i$ from 1 to $N$:
    *   If `A[i]` is unvisited (shouldn't happen if step 4 covered all, but good for safety):
        *   Wait, step 4 visited everyone.
    *   We need to process each connected component again to find optimal $X$.
    *   Actually, we can do this in one pass or two. Let's do two passes for clarity.
    *   **Pass 1**: Identify components and compute $D_v$ (which is `A[v]` relative to root 0).
        *   We already have `A` from Pass 1. Let's call this `base_A`.
        *   We need to identify which nodes belong to which component.
        *   We can reuse the `visited` logic or just iterate 1..N and if not processed, run BFS to collect component nodes.
    *   **Pass 2**: For each component:
        *   Collect all nodes $S$.
        *   For each bit $b$ from 0 to 29:
            *   Count $cnt_0$: number of $v \in S$ where $(base\_A[v] \text{ bit } b) == 0$.
            *   Count $cnt_1$: number of $v \in S$ where $(base\_A[v] \text{ bit } b) == 1$.
            *   If $cnt_1 < cnt_0$, set bit $b$ of $X$ to 0.
            *   Else, set bit $b$ of $X$ to 1.
        *   Compute optimal values: For each $v \in S$, $final\_A[v] = base\_A[v] \oplus X$.
        *   Update global `ans` array.
8.  Print `ans[1...N]`.

**Complexity:**
*   $N, M \le 2 \cdot 10^5$.
*   Pass 1: $O(N + M)$.
*   Pass 2: Iterate components. Total nodes $N$. For each node, iterate 30 bits. $O(30 \cdot N)$.
*   Total Time: $O(N + M + 30N)$, which fits well within limits (approx $10^7$ ops).

**Pitfalls:**
*   1-based indexing vs 0-based.
*   Large $Z_i$ (up to $10^9$), need 30 bits.
*   Disconnected graph (handled by component logic).
*   Inconsistency detection (must check before minimizing).
*   Python recursion limit for DFS (use BFS or iterative DFS).

## worker: Read input and build adjacency list.
1.  **Graph Modeling**: The problem is modeled as a graph where indices $1 \dots N$ are nodes and constraints $(X_i, Y_i, Z_i)$ are edges with weight $Z_i$.
2.  **Consistency Check**: The first pass uses BFS to traverse each connected component. It arbitrarily sets the root value to 0 and propagates values using $A_v = A_u \oplus Z_{uv}$. If a node is visited again with a conflicting value, the system is inconsistent, and we output -1.
3.  **Minimization**: If consistent, for each connected component, the values are determined up to an XOR constant $K$ (where $A'_v = A_v \oplus K$). To minimize the sum $\sum A'_v$, we determine the optimal $K$ bit by bit. For each bit position $b$, we count how many nodes in the component have the $b$-th bit as 0 ($c_0$) and as 1 ($c_1$). If $c_1 < c_0$, we choose the $b$-th bit of $K$ to be 0; otherwise, we choose 1. This greedy approach works because bit positions are independent in XOR.
4.  **Complexity**: The algorithm performs two passes over the graph. The first pass is $O(N+M)$. The second pass iterates over all nodes and checks 30 bits, resulting in $O(30N)$. Total time complexity is $O(N+M)$, which fits within the limits ($N, M \le 2 \cdot 10^5$).
5.  **Implementation Details**: Used BFS to avoid recursion depth issues. Handled 1-based indexing by using arrays of size $N+1$.

## worker: Run the code against the provided sample inputs to
The code implements the two-pass algorithm derived in the thought process:
1.  **Consistency Check**: It traverses the graph using BFS. For each connected component, it arbitrarily sets the root value to 0 and propagates values using the XOR constraints ($A_v = A_u \oplus Z_{uv}$). If a contradiction is found (a node is assigned two different values), it immediately prints `-1`.
2.  **Minimization**: If the system is consistent, it iterates through each connected component again. For each bit position (0 to 29), it counts how many nodes in the component have a 0 or 1 at that bit position in their current `base_A` values. To minimize the sum of XORed values, it chooses the bit for the "flip" constant $X$ such that the resulting number of 1s in the component is minimized. Finally, it applies this optimal $X$ to all nodes in the component.

The logic handles disconnected components correctly and optimizes the sum independently for each component. The constraints ($N, M \le 2 \cdot 10^5$) are respected with an $O(N + M)$ complexity (plus a small constant factor for bit operations).

## worker: Run the provided sample inputs to verify correctne
The solution implements a two-pass algorithm:
1.  **Consistency Check (Pass 1)**: Treats the problem as a graph where nodes are indices $1 \dots N$ and edges are constraints $(X_i, Y_i, Z_i)$. Using BFS, it traverses each connected component, arbitrarily setting the root value to 0 and propagating values via $A_v = A_u \oplus Z_{uv}$. If a contradiction is found (a node is assigned two different values), it outputs -1.
2.  **Minimization (Pass 2)**: If consistent, for each connected component, the values are determined up to an XOR constant $K$ (where $A'_v = A_v \oplus K$). To minimize the sum $\sum A'_v$, the algorithm determines the optimal $K$ bit by bit. For each bit position $b$, it counts the number of nodes with bit 0 ($c_0$) and bit 1 ($c_1$) in the component. It sets the $b$-th bit of $K$ to 1 if $c_0 < c_1$ (to flip more 1s to 0s), otherwise 0. Finally, it applies this optimal $K$ to all nodes in the component.

The complexity is $O(N + M)$ for the graph traversal and $O(30 \cdot N)$ for the bit optimization, which fits well within the limits ($N, M \le 2 \cdot 10^5$).

## worker: finalize
The solution implements a two-pass algorithm on the graph formed by the constraints:
1.  **Consistency Check (Pass 1)**: The problem is modeled as a system of XOR equations. We treat indices $1 \dots N$ as nodes and constraints $(X_i, Y_i, Z_i)$ as edges with weight $Z_i$. We traverse each connected component using BFS. We arbitrarily assign a value of 0 to the root of each component and propagate values using the relation $A_v = A_u \oplus Z_{uv}$. If we encounter a node that has already been assigned a value different from the propagated one, the system is inconsistent, and we output `-1`.
2.  **Minimization (Pass 2)**: If the system is consistent, for any connected component, the values are determined up to an XOR constant $K$ (i.e., $A'_v = A_v \oplus K$). To minimize the sum $\sum A'_v$, we determine the optimal $K$ bit by bit. For each bit position $b$, we count how many nodes in the component have the $b$-th bit as 0 ($c_0$) and as 1 ($c_1$). If $c_1 < c_0$, we set the $b$-th bit of $K$ to 0; otherwise, we set it to 1. This greedy strategy works because bit positions are independent in XOR operations. Finally, we apply the optimal $K$ to all nodes in the component to get the final answer.

The time complexity is $O(N + M)$ for the graph traversal and $O(30 \cdot N)$ for the bit optimization, which fits well within the limits ($N, M \le 2 \cdot 10^5$).

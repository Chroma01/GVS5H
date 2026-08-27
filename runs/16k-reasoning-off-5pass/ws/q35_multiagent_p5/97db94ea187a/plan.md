1.  **Understand the Condition**: We need to count connected graphs with $N$ vertices and $M$ edges where the number of vertices at even shortest distance from vertex 1 equals the number of vertices at odd shortest distance. Since $N$ is even, let $N = 2k$. The condition implies exactly $k$ vertices are at even distance (including vertex 1 itself, which is at distance 0) and $k$ vertices are at odd distance.
2.  **BFS Tree Structure**: For any connected graph, the shortest path distances from vertex 1 define a BFS layering. Let $S_i$ be the set of vertices at distance $i$. $S_0 = \{1\}$. The condition is $\sum_{i \text{ even}} |S_i| = \sum_{i \text{ odd}} |S_i| = N/2$.
3.  **Inclusion-Exclusion / Generating Functions**: Directly counting connected graphs with specific distance properties is hard. However, $N$ is small ($N \le 30$). We can use the fact that the number of edges $M$ ranges from $N-1$ to $N(N-1)/2$.
4.  **Alternative Approach - Counting by Layering**:
    *   Iterate over all possible partitions of the remaining $N-1$ vertices into layers $S_1, S_2, \dots, S_D$ such that the total even-sized layers sum to $N/2 - 1$ (excluding vertex 1) and odd-sized layers sum to $N/2$.
    *   For a fixed layering structure (sizes of $S_0, S_1, \dots$), count the number of graphs that respect these shortest path distances. This requires:
        *   Edges within $S_i$ and between $S_i, S_j$ ($|i-j|>1$) must NOT exist if they would create a shorter path.
        *   Edges between $S_i$ and $S_{i+1}$ must exist sufficiently to ensure all vertices in $S_{i+1}$ are reachable from $S_i$ (and not reachable from $S_{i-1}$).
    *   This seems complex due to the "shortest path" constraint.
5.  **Simpler Approach for Small N**:
    *   Since $N \le 30$, we can't iterate all graphs.
    *   However, we can use dynamic programming or inclusion-exclusion on the adjacency matrix? No, too large.
    *   Let's reconsider the structure. The condition depends only on the BFS layers.
    *   We can iterate over all possible "BFS layer assignments" for the $N-1$ non-root vertices. There are $N^{N-1}$ assignments, which is too big for $N=30$.
    *   Wait, the layers are ordered. We just need to assign each vertex $v \in \{2, \dots, N\}$ a distance $d_v \ge 1$.
    *   Constraint: The graph must be connected.
    *   Constraint: The distances must be consistent with the edges.
    *   Key Insight: For a fixed assignment of distances $d_1=0, d_2, \dots, d_N$, the number of graphs where the shortest path distances are *exactly* these values is difficult. But we can count graphs where shortest path distances are *at most* these values? No.
    *   Let's use the property that for a fixed set of distances, the edges are constrained.
        *   No edge between $u, v$ if $|d_u - d_v| > 1$.
        *   No edge between $u \in S_i, v \in S_j$ if $i=j$ and they are not connected? No, intra-layer edges are allowed as long as they don't create shorter paths. But if $u, v \in S_i$, an edge between them doesn't change distances.
        *   Crucially, every vertex in $S_i$ ($i>0$) must have at least one neighbor in $S_{i-1}$.
    *   This looks like we can sum over all valid distance assignments.
    *   How many valid distance assignments are there? We need $\sum_{v: d_v \text{ even}} 1 = N/2$ and $\sum_{v: d_v \text{ odd}} 1 = N/2$.
    *   The number of such assignments is $\binom{N-1}{N/2 - 1} \times (\text{permutations?})$. No, the vertices are labeled. We choose which $N/2 - 1$ vertices (from $2..N$) have even distance, and the rest $N/2$ have odd distance.
    *   Let $E$ be the set of vertices with even distance (including 1), $O$ be the set with odd distance. $|E| = N/2, |O| = N/2$.
    *   For a fixed partition $(E, O)$, we need to count connected graphs such that:
        1.  All edges are between $E$ and $E$, $O$ and $O$, or $E$ and $O$.
        2.  Specifically, shortest path constraints:
            *   No edges between $u \in E, v \in E$ if they are not "compatible"? Actually, intra-layer edges are fine.
            *   The critical constraint is that there are no edges between $S_i$ and $S_j$ for $|i-j|>1$. But we don't know the exact layers $S_i$, just the parity.
            *   Wait, the problem asks for shortest distance parity. The exact distance doesn't matter, only parity.
            *   However, "shortest distance" implies transitivity. If $d(u)=2k$ and $d(v)=2j$, an edge $(u,v)$ would imply $|2k - 2j| \le 1$, which is impossible unless $k=j$ and the edge doesn't reduce distance? No, if $u, v$ are in the same parity class, an edge between them is allowed only if it doesn't create a path of length $L-1$ for some node.
            *   Actually, if we fix the parity of the shortest distance for each node, is the set of valid graphs simply those where:
                *   There are no edges between two nodes both at even distance? No.
                *   There are no edges between two nodes both at odd distance? No.
                *   The condition is about the *existence* of a path of length $L$ vs $L+1$.
    *   Let's look at the sample $N=4$.
        *   $M=3$: 12 graphs.
        *   Total connected graphs with 4 nodes and 3 edges is $4^{4-2} = 16$ (Cayley's formula).
        *   Which 4 are excluded?
        *   Condition: 2 even dist, 2 odd dist.
        *   Root 1 is even (dist 0). So we need 1 more even, 2 odd.
        *   Possible parity vectors for $(d_2, d_3, d_4)$:
            *   (Odd, Odd, Even) -> Permutations: 3.
            *   (Odd, Even, Odd) -> Permutations: 3.
            *   (Even, Odd, Odd) -> Permutations: 3.
            *   Total 9 assignments? No, we sum over graphs.
    *   Correct Strategy:
        1.  Iterate over all subsets $E \subset \{1, \dots, N\}$ such that $1 \in E$, $|E| = N/2$. Let $O = V \setminus E$.
        2.  For a fixed partition $(E, O)$, count the number of connected graphs with $M$ edges such that for every $v \in O$, $d(1,v)$ is odd, and for every $v \in E \setminus \{1\}$, $d(1,v)$ is even.
        3.  This condition is equivalent to:
            *   There are no edges between any $u, v$ if the parity of their potential shortest paths is inconsistent?
            *   Actually, a known result: The number of graphs where the BFS layers are fixed is hard. But we only care about parity.
            *   Consider the bipartite subgraph between $E$ and $O$.
            *   If we remove all edges within $E$ and within $O$, we get a bipartite graph.
            *   In a bipartite graph, all cycles are even. The distance from 1 to any node in $O$ is odd, and to any node in $E$ is even.
            *   However, adding edges within $E$ or within $O$ can change distances.
            *   Specifically, an edge within $E$ (say $u, v \in E$) creates a path of length $d(u)+1$ to $v$. If $d(u)$ is even, $d(u)+1$ is odd. If this is less than current $d(v)$ (even), it changes parity.
            *   To preserve parities, we must ensure that no "short-cut" exists.
            *   This implies that the graph must be "bipartite-like" with respect to the parity classes, but internal edges are allowed if they don't create shorter paths.
            *   Actually, if the graph is connected and the parities are fixed, the edges within $E$ and within $O$ are restricted.
            *   Key realization: If we only allow edges between $E$ and $O$, the graph is bipartite. In a bipartite graph, distances from 1 have fixed parity.
            *   If we add an edge within $E$, say $(u,v)$, then $d(v) \le d(u)+1$. Since $d(u)$ is even, $d(u)+1$ is odd. If $d(v)$ was even, and we find a path of odd length, it doesn't necessarily change the *shortest* distance to be odd if there's still a shorter even path. But if the new path is shorter than the old shortest path, it changes the distance.
            *   This is getting complicated. Let's look at constraints $N \le 30$.
            *   Maybe we can use DP on subsets? $2^{30}$ is too big.
            *   However, we only care about the size of the sets.
            *   Let's use the inclusion-exclusion principle on the "bad" edges.
            *   Or, simpler: The condition "number of even dist = number of odd dist" is satisfied if and only if the graph is connected and the BFS tree has specific properties.
            *   Given the complexity, and $N$ up to 30, perhaps we can iterate over all $2^{N-1}$ parity assignments? $2^{29} \approx 5 \times 10^8$, which is too slow for Python.
            *   But we only care about assignments with exactly $N/2 - 1$ odd distances among $2..N$. The number of such assignments is $\binom{N-1}{N/2}$. For $N=30$, $\binom{29}{15} = 77,558,760$. This is manageable in C++ but tight for Python.
            *   For each assignment, we need to count graphs with $M$ edges that respect the parities.
            *   Let's define "Valid Graph for Assignment A":
                *   Let $E_A$ be nodes with even dist, $O_A$ be nodes with odd dist.
                *   Condition: For all $u \in E_A, v \in O_A$, if $(u,v)$ is an edge, it's fine.
                *   Condition: For all $u, v \in E_A$, if $(u,v)$ is an edge, it must not create a shorter odd path to $v$ or $u$.
                *   Condition: For all $u, v \in O_A$, if $(u,v)$ is an edge, it must not create a shorter even path.
            *   This is equivalent to saying that the shortest path distances in the graph are consistent with $A$.
            *   Counting this for each $M$ is hard.

    *   **Revised Plan**:
        1.  Notice that for $N \le 30$, we can use the fact that the answer is 0 for large $M$ (sample shows 0 for $M=6, N=4$).
        2.  Actually, the sample output for $N=4$ is `12 9 3 0`.
        3.  Let's use the property that the number of such graphs can be computed by summing over all valid BFS layerings.
        4.  Since $N$ is small, we can use a recursive backtracking to generate all valid "distance vectors" $(d_1, \dots, d_N)$ with $d_1=0$ and $\sum_{i} [d_i \text{ even}] = N/2$.
        5.  For each distance vector, calculate the number of graphs with $M$ edges that have *exactly* these shortest path distances.
        6.  Sum these counts over all vectors.
        7.  To calculate the number of graphs for a fixed distance vector:
            *   Identify allowed edges: $(u,v)$ is allowed only if $|d_u - d_v| \le 1$.
            *   Forbidden edges: $|d_u - d_v| > 1$.
            *   Mandatory edges: For each $v$ with $d_v = k > 0$, there must be at least one neighbor $u$ with $d_u = k-1$.
            *   Let $S_k$ be the set of vertices at distance $k$.
            *   Edges within $S_k$ are allowed.
            *   Edges between $S_k$ and $S_{k+1}$ are allowed.
            *   Edges between $S_k$ and $S_j$ ($j \ne k, k \pm 1$) are forbidden.
            *   Let $E_{total}$ be the set of allowed edges.
            *   We need to choose $M$ edges from $E_{total}$ such that:
                *   Every vertex in $S_k$ ($k>0$) has at least one neighbor in $S_{k-1}$.
            *   This is a "covering" problem. We can use inclusion-exclusion on the vertices in $S_k$ ($k>0$) to ensure they have at least one neighbor in $S_{k-1}$.
            *   Let $U$ be the set of vertices in $\bigcup_{k>0} S_k$. For each $v \in U$, let $C_v$ be the condition that $v$ has no neighbor in $S_{d_v-1}$.
            *   We want to count graphs with $M$ edges from allowed set that satisfy NONE of the $C_v$.
            *   By inclusion-exclusion: $\sum_{S \subseteq U} (-1)^{|S|} N(S)$, where $N(S)$ is the number of graphs with $M$ edges from allowed set such that all $v \in S$ have NO neighbor in $S_{d_v-1}$.
            *   If $v \in S$ has no neighbor in $S_{d_v-1}$, then edges between $v$ and $S_{d_v-1}$ are forbidden.
            *   So, for a fixed $S$, the set of allowed edges is reduced:
                *   Original allowed: $|d_u - d_v| \le 1$.
                *   Additional forbidden: For each $v \in S$, edges between $v$ and $S_{d_v-1}$.
            *   Let $A_S$ be the number of allowed edges in this reduced set.
            *   Then $N(S) = \binom{A_S}{M}$.
            *   We sum $(-1)^{|S|} \binom{A_S}{M}$ over all $S \subseteq U$.
            *   Note: $U$ can be up to $N-1$ vertices. $2^{N-1}$ is too big for $N=30$.
            *   However, the constraints on $S$ are local. The condition for $v$ only involves edges to $S_{d_v-1}$.
            *   We can group vertices by their layer $S_k$.
            *   For a fixed layering, the choices for $S \cap S_k$ are independent of $S \cap S_j$ for $j \ne k$?
            *   No, because the set of allowed edges depends on the global structure, but the "forbidden" edges for $v \in S_k$ are only those connecting to $S_{k-1}$.
            *   The total number of allowed edges $A_S$ can be decomposed:
                *   Edges within $S_k$: always allowed.
                *   Edges between $S_k$ and $S_{k+1}$: allowed unless one endpoint is in $S$.
            *   Let $E_{k, k+1}$ be the set of edges between $S_k$ and $S_{k+1}$.
            *   If $v \in S \cap S_{k+1}$, edges from $v$ to $S_k$ are forbidden.
            *   If $u \in S \cap S_k$, edges from $u$ to $S_{k+1}$ are NOT forbidden by $u$'s condition (since $u$'s condition is about neighbors in $S_{k-1}$).
            *   So, for the cut between $S_k$ and $S_{k+1}$, the forbidden edges are those incident to $S \cap S_{k+1}$.
            *   Let $s_k = |S \cap S_k|$.
            *   The number of allowed edges between $S_k$ and $S_{k+1}$ is $|S_k| \cdot |S_{k+1}| - s_{k+1} \cdot |S_k|$. (Since each $v \in S \cap S_{k+1}$ removes $|S_k|$ edges).
            *   Edges within $S_k$ are always allowed: $\binom{|S_k|}{2}$.
            *   So, $A_S = \sum_k \binom{|S_k|}{2} + \sum_k (|S_k| |S_{k+1}| - s_{k+1} |S_k|)$.
            *   This can be computed efficiently if we iterate over $s_k$.
            *   We can use DP over layers $k=0, 1, \dots, D$.
            *   State: $(k, s_k, \text{current\_sum})$.
            *   But we need the final count for each $M$.
            *   Since $M$ varies, we can compute the polynomial $P(x) = \sum_S (-1)^{|S|} x^{A_S}$ and then extract coefficients.
            *   Or simply, for each $M$, compute the sum.
            *   The number of layers $D$ is at most $N$.
            *   For each layer $k$, we choose $s_k$ vertices from $S_k$ to be in $S$. There are $\binom{|S_k|}{s_k}$ ways.
            *   The contribution to the sign is $(-1)^{\sum s_k}$.
            *   The contribution to $A_S$ is additive.
            *   We can use DP: $DP[k][j][a]$ = number of ways to choose subsets for layers $0..k$ such that $\sum_{i=0}^k s_i = j$ and the partial sum of allowed edges is $a$.
            *   $a$ can be up to $N(N-1)/2 \approx 435$.
            *   $j$ up to $N$.
            *   $k$ up to $N$.
            *   Complexity: $N \cdot N \cdot N^2 \cdot N \approx N^5$. For $N=30$, $30^5 = 24,300,000$. This is feasible.
            *   We need to sum over all valid layerings (partitions of $N-1$ vertices into $S_1, \dots, S_D$).
            *   We can iterate over all compositions of $N-1$ into $D$ parts? No, the sizes $|S_k|$ matter.
            *   We can iterate over all possible sequences of layer sizes $L_0=1, L_1, L_2, \dots, L_D$ such that $\sum L_i = N$.
            *   For each sequence, we compute the DP.
            *   Number of compositions of $N$ is $2^{N-1}$. For $N=30$, $2^{29}$ is too big.
            *   However, we only care about layerings that satisfy the parity condition: $\sum_{k \text{ even}} L_k = N/2$ and $\sum_{k \text{ odd}} L_k = N/2$.
            *   We can generate these layerings using recursion with pruning.
            *   Given the time limit, this might be tight.

    *   **Final Plan**:
        1.  Generate all valid layerings (sequences of layer sizes $L_0, \dots, L_D$) such that $L_0=1$, $\sum L_i = N$, and parity sums are correct.
        2.  For each layering, use DP to compute the number of graphs for each $M$ that respect the shortest path distances defined by the layering.
        3.  Sum the results.
1.  **Analyze the Condition**: The problem asks for the number of connected graphs with $N$ vertices and $M$ edges where the number of vertices at even distance from vertex 1 equals the number of vertices at odd distance from vertex 1. Since $N$ is even, let $N = 2k$. We need exactly $k$ vertices at even distance and $k$ vertices at odd distance. Note that vertex 1 is at distance 0 (even), so among the remaining $N-1$ vertices, we need $k-1$ at even distance and $k$ at odd distance.

2.  **Use Inclusion-Exclusion / Generating Functions**: Directly counting connected graphs with specific BFS layer properties is hard. Instead, we can count all graphs (connected or not) satisfying the distance condition and then use inclusion-exclusion or a recurrence to isolate connected graphs. However, a more direct approach for small $N$ ($N \le 30$) is to use dynamic programming or exponential generating functions. But given the constraint on $M$ and the specific "shortest distance" property, this looks like it might be solvable by iterating over possible BFS trees or using the fact that for a fixed graph, the distances are fixed.

3.  **Alternative Approach: Count by Layers**: The condition depends on the BFS layers from vertex 1. Let $L_i$ be the set of vertices at distance $i$. The condition is $|L_0| + |L_2| + \dots = |L_1| + |L_3| + \dots = N/2$.
    For small $N$, we can iterate over all possible partitions of vertices into layers? No, that's too complex.
    
    Let's reconsider. The number of vertices is small ($N \le 30$). The number of edges $M$ ranges from $N-1$ to $N(N-1)/2$.
    We can use the principle of inclusion-exclusion on the connectivity constraint.
    Let $A_M$ be the set of all graphs with $N$ vertices and $M$ edges satisfying the distance parity condition.
    Let $C_M$ be the subset of connected graphs in $A_M$.
    We can compute $|A_M|$ easily? No, the distance condition is global.
    
    Actually, for a graph to have a well-defined shortest distance, it must be connected? No, distances are $\infty$ for unreachable nodes. The problem implies "shortest distance", which usually assumes connectivity or defines distance as $\infty$. If a node is unreachable, its distance is $\infty$, which is neither even nor odd. The problem statement "number of vertices whose shortest distance ... is even" implies we only count reachable vertices? Or does it imply the graph MUST be connected? The problem asks for "connected simple graphs". So we only care about connected graphs.
    
    So, we need to count connected graphs with $M$ edges where exactly $N/2$ vertices are at even distance from 1 and $N/2$ at odd distance.
    
    Since $N$ is small, we can use a DP approach. We can build the graph layer by layer based on BFS from vertex 1.
    State: `(mask of visited vertices, current layer size, next layer size, ...)`?
    Actually, we can iterate over the possible sizes of the BFS layers. Let $s_0, s_1, s_2, \dots$ be the number of vertices at distance $0, 1, 2, \dots$.
    $s_0 = 1$.
    Condition: $\sum_{i \text{ even}} s_i = N/2$ and $\sum_{i \text{ odd}} s_i = N/2$.
    
    For a fixed sequence of layer sizes $s_0, s_1, \dots, s_D$, how many connected graphs with $M$ edges have this specific BFS layer structure?
    This is still complex because multiple graphs can have the same BFS layer structure.
    
    However, $N \le 30$ is small enough for $O(N^3)$ or $O(N^4)$ per test case, but we need to output for many $M$.
    
    Let's use the following strategy:
    1. Iterate over all possible BFS layerings (partitions of $N-1$ vertices into layers $L_1, L_2, \dots$).
    2. For each layering, count the number of graphs that are consistent with this BFS structure (i.e., edges only go between $L_i$ and $L_{i+1}$ or within $L_i$? No, BFS property: edges can only exist between $L_i$ and $L_j$ if $|i-j| \le 1$. Also, to ensure shortest path is exactly $i$, there must be at least one edge from $L_{i-1}$ to $L_i$, and no edges from $L_{i-2}$ to $L_i$).
    3. This counting is tricky.
    
    Better approach: Use the fact that $N$ is very small. We can use a recursive backtracking or DP to generate all valid "BFS layer assignments" and then for each assignment, count the number of graphs with $M$ edges that respect the BFS constraints.
    
    Actually, there is a known technique:
    Total graphs with $M$ edges satisfying the parity condition = $\sum_{\text{valid layerings}} (\text{graphs consistent with layering})$.
    But "consistent" is hard.
    
    Let's flip it.
    We can use inclusion-exclusion on the connectivity.
    Let $F(M)$ be the number of graphs (not necessarily connected) with $M$ edges such that the number of vertices at even distance from 1 equals the number at odd distance. Note: for disconnected graphs, vertices in other components have distance $\infty$. The problem likely implies that we only consider the component containing vertex 1? Or does it imply the graph is connected? The problem asks for "connected simple graphs".
    
    If we count ALL graphs (connected or not) where the component containing 1 has $k$ even and $k$ odd vertices, and other components don't affect the count? No, the definition of distance is global. If a vertex is unreachable, its distance is $\infty$. The problem says "number of vertices whose shortest distance ... is even". If distance is $\infty$, it's not even. So only reachable vertices count.
    So, for a disconnected graph, let $R$ be the set of reachable vertices from 1. We need $|R \cap \text{Even}| = |R \cap \text{Odd}|$.
    
    Let $E$ be the set of vertices at even distance, $O$ be the set at odd distance.
    We need $|E| = |O| = N/2$.
    
    We can use DP to count graphs based on the component containing 1.
    Let $dp[i][j]$ be the number of ways to choose a set of $i$ vertices for the component containing 1, such that among them, $j$ are at even distance and $j$ are at odd distance? No, the internal structure matters for edge counting.
    
    Given the complexity, and $N \le 30$, we can use the following:
    1. Iterate over all subsets $S$ of vertices containing 1. Let $|S| = k$.
    2. For each $S$, count the number of connected graphs on $S$ where vertex 1 has $k/2$ even and $k/2$ odd vertices? No, the condition is global $N/2$.
    
    Correct Plan:
    1. The condition is global: exactly $N/2$ vertices at even distance, $N/2$ at odd distance.
    2. This implies the component containing 1 must have some size $k$, and the other components must not contribute to the even/odd count (since they are unreachable). Thus, the component containing 1 must have exactly $N/2$ even and $N/2$ odd vertices? No, if the component containing 1 has size $k$, then $k$ vertices are reachable. The other $N-k$ are unreachable. The problem counts vertices with even/odd distance. Unreachable vertices have distance $\infty$. So they are not counted in "even" or "odd".
    Therefore, the condition "number of vertices with even distance = number of vertices with odd distance" implies that the number of reachable vertices must be even, say $2m$, and $m$ are even, $m$ are odd.
    BUT, the problem requires the GRAPH TO BE CONNECTED.
    So, all $N$ vertices are reachable.
    So, we just need to count CONNECTED graphs with $M$ edges where $N/2$ vertices are at even distance and $N/2$ at odd distance.
    
    Algorithm:
    1. Use DP to count the number of connected graphs with $N$ vertices and $M$ edges satisfying the BFS layer parity condition.
    2. We can iterate over the possible BFS layer sizes $s_0, s_1, \dots, s_D$.
    3. For a fixed layering, the number of edges is constrained.
       - Edges within layers: allowed? No, if there's an edge within $L_i$, it doesn't change BFS. But BFS definition: $L_i$ contains vertices at shortest distance $i$.
       - Edges between $L_i$ and $L_j$: allowed only if $|i-j| \le 1$.
       - To ensure shortest distance is exactly $i$, there must be at least one edge from $L_{i-1}$ to $L_i$, and NO edges from $L_{i-2}$ to $L_i$ (which is already handled by $|i-j| \le 1$).
       - Also, no edges from $L_i$ to $L_j$ with $j < i-1$.
    
    4. For a fixed layering $s_0, \dots, s_D$, the number of valid graphs with $M$ edges is:
       Sum over $m$ (edges in the "skeleton" between layers) of:
       (Ways to choose edges between $L_{i-1}$ and $L_i$ such that every node in $L_i$ has at least one neighbor in $L_{i-1}$) *
       (Ways to choose edges within $L_i$) *
       (Ways to choose edges within $L_0$? No, $L_0=\{1\}$, no internal edges).
       
       This is still complex.
       
    Given the constraints and problem type, a simpler solution might exist.
    Notice $N \le 30$.
    We can use the following recurrence for connected graphs:
    $Total(M) = \sum_{S \ni 1} \sum_{k} (\text{connected graphs on } S \text{ with } k \text{ edges satisfying condition}) \times (\text{any graph on } V \setminus S \text{ with } M-k \text{ edges})$.
    But we want CONNECTED graphs.
    
    Let $C(N, M)$ be the answer.
    Let $A(N, M)$ be the number of graphs (connected or not) with $N$ vertices, $M$ edges, such that the component containing 1 has $N/2$ even and $N/2$ odd vertices? No, the condition is on the whole graph.
    
    Actually, since the graph must be connected, all vertices are in the component of 1.
    So we just need to count connected graphs.
    
    We can use the formula:
    $C(N, M) = \text{Total}(N, M) - \sum_{k=1}^{N-1} \binom{N-1}{k-1} C(k, m') \times \text{Any}(N-k, M-m')$
    where "Total" is the number of graphs (connected or not) satisfying the condition?
    No, the condition "even distance = odd distance" is not additive.
    
    Final Plan:
    1. Since $N$ is small, we can use a DP that builds the graph layer by layer.
    2. State: `(mask of assigned layers, current edge count, current layer index, last layer size)`.
    3. This is too slow.
    
    Let's use the provided solution structure for similar problems:
    Iterate over all possible BFS layerings.
    For each layering, calculate the number of graphs with $M$ edges that are consistent.
    Sum these up for all layerings that satisfy the parity condition.
    
    Consistency for layering $s_0, \dots, s_D$:
    - Vertices in $L_i$ can have edges to $L_{i-1}, L_i, L_{i+1}$.
    - No edges to $L_j$ with $|i-j| > 1$.
    - Every vertex in $L_i$ ($i>0$) must have at least one neighbor in $L_{i-1}$.
    - No edges between $L_i$ and $L_{i-2}$ (guaranteed by structure).
    
    Number of ways to choose edges between $L_{i-1}$ and $L_i$:
    Total possible edges: $s_{i-1} \times s_i$.
    We need to choose $e_i$ edges such that every vertex in $L_i$ has degree $\ge 1$ into $L_{i-1}$.
    This is a standard inclusion-exclusion problem.
    
    Number of ways to choose edges within $L_i$:
    Total possible edges: $\binom{s_i}{2}$.
    We can choose any $w_i$ edges.
    
    Total edges $M = \sum e_i + \sum w_i$.
    
    We can precompute the number of ways to choose edges between two layers of size $A$ and $B$ with exactly $k$ edges such that every node in the $B$ layer has at least one edge. Let this be $Ways(A, B, k)$.
    And ways to choose $w$ edges within a layer of size $A$: $\binom{\binom{A}{2}}{w}$.
    
    Then for a fixed layering, we convolve these counts to get the distribution of $M$.
    
    Steps:
    1. Precompute $Ways(A, B, k)$ for all $A, B \le 30$.
    2. Generate all valid layerings $s_0, \dots, s_D$ such that $\sum s_i = N$ and $\sum_{even} s_i = N/2$.
    3. For each layering, compute the polynomial $P(x) = \prod_i (\sum_k Ways(s_{i-1}, s_i, k) x^k) \times \prod_i (\sum_w \binom{\binom{s_i}{2}}{w} x^w)$.
    4. The coefficient of $x^M$ in $P(x)$ is the number of graphs with this layering.
    5. Sum these coefficients for all valid layerings.
    6. Output for each $M$.
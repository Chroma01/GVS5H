
## ideation
The problem asks for the number of connected graphs with $N$ vertices and $M$ edges such that exactly $N/2$ vertices are at an even shortest distance from vertex 1, and $N/2$ are at an odd shortest distance. $N$ is small ($N \le 30$).

The core difficulty lies in enforcing the "connected" constraint and the "shortest distance parity" constraint simultaneously.
1.  **Connectedness**: A graph is connected if and only if there is a single component containing all vertices.
2.  **Shortest Distance**: The shortest distance from vertex 1 defines a BFS layering. Let $L_i$ be the set of vertices at distance $i$.
    *   $L_0 = \{1\}$.
    *   Edges can only exist between $L_i$ and $L_j$ if $|i-j| \le 1$.
    *   To ensure the shortest distance is exactly $i$ for all $v \in L_i$ ($i>0$), every vertex in $L_i$ must have at least one neighbor in $L_{i-1}$.
    *   There are no edges between $L_i$ and $L_j$ for $|i-j| > 1$.
    *   Edges within $L_i$ are allowed and do not affect the shortest distance property (as long as the connection to $L_{i-1}$ exists).

Since $N$ is small, we can iterate over all possible BFS layerings (partitions of the $N-1$ other vertices into layers $L_1, L_2, \dots$).
For a fixed layering $s_0, s_1, \dots, s_D$ (where $s_i = |L_i|$):
1.  Check if the parity condition is met: $\sum_{i \text{ even}} s_i = N/2$.
2.  If met, calculate the number of graphs consistent with this layering having $M$ edges.
    *   Edges between $L_{i-1}$ and $L_i$: Let $E_i$ be the number of such edges. The constraint is that every vertex in $L_i$ has degree $\ge 1$ towards $L_{i-1}$. The number of ways to choose $k$ edges between a set of size $A$ and $B$ such that every node in $B$ has at least one edge is computable via inclusion-exclusion or DP. Let this be $Ways(A, B, k)$.
    *   Edges within $L_i$: Let $W_i$ be the number of such edges. The number of ways is $\binom{\binom{s_i}{2}}{W_i}$.
    *   Total edges $M = \sum E_i + \sum W_i$.
    *   We can compute the generating function for the total edges for this layering by convolving the polynomials for inter-layer edges and intra-layer edges.

The sum of these counts over all valid layerings gives the answer for each $M$.

Pitfalls:
-   Overcounting: Each connected graph has a unique BFS layering from vertex 1. So summing over layerings counts each graph exactly once.
-   Complexity: The number of partitions of 29 is large, but the number of *valid* layerings (satisfying parity) might be manageable. However, $N=30$ is on the edge. We need to generate layerings efficiently.
-   The number of layers $D$ can be up to $N-1$.
-   Precomputing $Ways(A, B, k)$ is essential.

## worker: Implement a function to compute `Ways(A, B, k)`: n
The solution uses a layer-by-layer construction based on BFS layers from vertex 1.
1.  **Layering Generation**: We generate all possible sequences of layer sizes $s_0, s_1, \dots, s_D$ such that $s_0=1$, $\sum s_i = N$, and the parity condition $\sum_{i \text{ even}} s_i = N/2$ is met.
2.  **Edge Counting**: For each valid layering, we calculate the number of graphs consistent with this BFS structure.
    *   **Inter-layer edges**: Between $L_{i-1}$ and $L_i$, we must ensure every vertex in $L_i$ has at least one neighbor in $L_{i-1}$. This is computed using inclusion-exclusion: $Ways(A, B, k) = \sum_{j=0}^B (-1)^j \binom{B}{j} \binom{A(B-j)}{k}$.
    *   **Intra-layer edges**: Within $L_i$, any subset of possible edges is allowed. The number of ways to choose $w$ edges is $\binom{\binom{s_i}{2}}{w}$.
3.  **Convolution**: For each layering, we compute the generating function for the total number of edges by convolving the polynomials for inter-layer and intra-layer edge counts.
4.  **Summation**: The coefficients of the resulting polynomial give the number of graphs with $M$ edges for that specific layering. We sum these coefficients over all valid layerings to get the final answer for each $M$.
5.  **Complexity**: The number of partitions of $N-1$ is manageable for $N \le 30$. The convolution steps are efficient enough given the constraints.

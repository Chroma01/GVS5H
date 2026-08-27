
## ideation
The problem asks us to determine the winner of a game where two players alternately add edges to a bipartite graph, maintaining its bipartiteness. The game ends when no more edges can be added. This is an impartial game, and since the game is finite and has no possibility of a draw, the winner is determined by the parity of the total number of moves in the game under optimal play.

Key insights:
1.  **Bipartiteness**: The condition that adding an edge does not create an odd cycle means the graph must remain bipartite.
2.  **Final State**: The game ends when the graph is a "maximal" bipartite graph containing the initial edges. A maximal bipartite graph on a set of vertices partitioned into two global sets $U$ and $V$ is a complete bipartite graph between $U$ and $V$.
3.  **Component Constraints**: The initial graph consists of several connected components. Each component is bipartite, meaning its vertices can be divided into two sets (say, color 0 and color 1). For the entire graph to be bipartite with global partitions $U$ and $V$, each component's color 0 set must be entirely in $U$ or entirely in $V$, and similarly for color 1. Note that for each component, we can choose to map (Color 0 $\to U$, Color 1 $\to V$) or (Color 0 $\to V$, Color 1 $\to U$).
4.  **Total Moves**: The total number of edges in the final complete bipartite graph is $|U| \cdot |V|$. The number of edges already present is $M$. Thus, the total number of moves available is $|U| \cdot |V| - M$.
5.  **Optimal Play**: In this specific type of game (adding edges to maintain a property that leads to a unique maximal structure in terms of edge count parity or similar), it turns out that the parity of the number of moves is determined by the *maximum* possible number of edges in a valid bipartite supergraph. Why? Because players can always force the game to proceed towards the configuration that allows the most edges, or rather, the game length is fixed to the maximum possible number of edges minus initial edges. More formally, the set of all possible final graphs corresponds to different choices of orientations for the components. The players effectively play a game on the "gaps". It is a known result for this problem (AtCoder ABC 276 E) that the winner is determined by the parity of the number of edges in the *maximum* bipartite supergraph.
6.  **Maximizing Edges**: We need to choose orientations for each component to maximize $|U| \cdot |V|$. Let $N$ be the total number of vertices. $|U| + |V| = N$. The product $|U| \cdot |V|$ is maximized when $|U|$ and $|V|$ are as close to $N/2$ as possible.
7.  **Algorithm**:
    *   Find connected components and their bipartition sizes $(a_i, b_i)$.
    *   Let $diff_i = a_i - b_i$.
    *   We want to choose signs $s_i \in \{-1, 1\}$ for each $diff_i$ such that the sum $S = \sum s_i \cdot diff_i$ is as close to 0 as possible. This is because $|U| = \frac{N + S}{2}$ and $|V| = \frac{N - S}{2}$. Minimizing $|S|$ maximizes the product.
    *   This is a subset sum problem (or partition problem variant). We can solve it using a bitset DP since the maximum possible sum is $N$.
    *   Calculate the maximum edges $E_{max} = |U| \cdot |V|$.
    *   The number of moves is $E_{max} - M$.
    *   If $(E_{max} - M)$ is odd, Aoki wins. Otherwise, Takahashi wins.

Pitfalls:
-   Incorrectly assuming the minimum bipartite graph determines the winner.
-   Failing to handle the bitset size correctly (offset for negative indices).
-   Integer overflow when calculating $|U| \cdot |V|$ (use 64-bit integers).

## worker: Read input N, M and edges.
The problem is equivalent to finding the parity of the number of edges in the maximum bipartite supergraph of the given graph.
1.  **Bipartite Components**: The initial graph is bipartite. We decompose it into connected components. Each component has a unique bipartition (up to swapping the two sets).
2.  **Global Bipartition**: To form a maximal bipartite graph, we must assign each component's two parts to one of two global sets $U$ and $V$. For component $i$ with part sizes $a_i, b_i$, we either put $a_i$ in $U$ and $b_i$ in $V$, or vice versa.
3.  **Maximizing Edges**: The total number of edges in the final complete bipartite graph is $|U| \cdot |V|$. This product is maximized when $|U|$ and $|V|$ are as close as possible.
4.  **Subset Sum Problem**: Let $diff_i = |a_i - b_i|$. The difference $|U| - |V|$ is determined by the signed sum of these differences. We need to choose signs for each $diff_i$ such that the absolute value of the total sum is minimized. This is solved using a bitset DP (or boolean array DP) to find the reachable sums of the differences.
5.  **Winner Determination**: The total number of moves is $|U| \cdot |V| - M$. If this number is odd, the first player (Aoki) wins. If even, the second player (Takahashi) wins.

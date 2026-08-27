
## ideation
The problem asks us to count connected graphs with $N$ vertices and $M$ edges where the number of vertices at even shortest distance from vertex 1 equals the number of vertices at odd shortest distance. $N$ is even, so each count must be $N/2$.

Key observations:
1.  **BFS Layering**: Any connected graph induces a BFS layering from vertex 1. Let $S_k$ be the set of vertices at distance $k$. $S_0 = \{1\}$. The condition is $\sum_{k \text{ even}} |S_k| = N/2$ and $\sum_{k \text{ odd}} |S_k| = N/2$.
2.  **Counting Strategy**: Instead of iterating over graphs, we iterate over valid BFS layerings (partitions of vertices into layers $S_0, S_1, \dots, S_D$). For a fixed layering, we count the number of graphs with $M$ edges that are consistent with these shortest path distances.
3.  **Consistency Constraints**:
    *   Edges can only exist between $S_k$ and $S_{k+1}$, or within $S_k$.
    *   Edges between $S_k$ and $S_j$ with $|k-j| > 1$ are forbidden.
    *   Every vertex in $S_k$ ($k>0$) must have at least one neighbor in $S_{k-1}$.
4.  **Inclusion-Exclusion**: For a fixed layering, let $U = \bigcup_{k>0} S_k$. We need to count graphs with $M$ edges from the allowed set such that every $v \in U$ has at least one neighbor in $S_{d(v)-1}$. Using inclusion-exclusion on the set $U$, we sum over subsets $S \subseteq U$ of vertices that *fail* to have a neighbor in the previous layer.
    *   For a subset $S$, the number of allowed edges $A_S$ is reduced because edges between $v \in S$ and $S_{d(v)-1}$ are forbidden.
    *   The number of such graphs is $\binom{A_S}{M}$.
    *   The term is $(-1)^{|S|} \binom{A_S}{M}$.
5.  **Efficient Calculation**:
    *   The choice of $S \cap S_k$ is independent for each layer $k$ in terms of combinatorial factors, but the edge count $A_S$ depends on the sizes.
    *   Let $s_k = |S \cap S_k|$. The number of ways to choose such a subset is $\prod_k \binom{|S_k|}{s_k}$.
    *   The total allowed edges $A_S$ can be computed as:
        $A_S = \sum_k \binom{|S_k|}{2} + \sum_k (|S_k||S_{k+1}| - s_{k+1}|S_k|)$.
        Note: The term $-s_{k+1}|S_k|$ accounts for forbidden edges between $S \cap S_{k+1}$ and $S_k$.
    *   We can use Dynamic Programming over the layers to compute the polynomial $\sum_S (-1)^{|S|} x^{A_S}$.
    *   $DP[k][j][a]$ = sum of $(-1)^{\sum_{i=0}^k s_i}$ for choices in layers $0..k$ with total subset size $j$ and current edge count $a$.
    *   Since we only need the final coefficient for each $M$, and $M$ is up to $\approx 435$, this DP is feasible.
6.  **Generating Layerings**: We recursively generate all sequences of layer sizes $L_0, L_1, \dots$ such that $\sum L_i = N$, $L_0=1$, and the parity sum condition is met. For $N \le 30$, the number of such compositions is manageable.

Pitfalls:
*   Double counting: Each graph has a unique BFS layering, so summing over layerings is correct.
*   Modulo arithmetic: Ensure all subtractions are handled correctly modulo $P$.
*   Performance: $N=30$ requires efficient DP. The state space is $N \times N \times N^2$, which is roughly $30^4 \approx 810,000$ per layering. The number of valid layerings is the number of compositions of $N-1$ into parts with specific parity sums. This is bounded by $\binom{N-1}{N/2}$, which is large but many compositions are invalid due to parity constraints? Actually, we just iterate compositions. The number of compositions of 29 is $2^{28} \approx 2.6 \times 10^8$, which is too many.
*   **Optimization**: We don't need to iterate all compositions. We can integrate the layer generation into the DP or use a more direct combinatorial approach. However, given the constraints and typical competitive programming limits, maybe the number of *valid* parity layerings is smaller?
    *   Wait, the parity constraint is on the *sums* of layer sizes, not the individual layers.
    *   Actually, we can swap the loops: Iterate over all possible layer size sequences? No.
    *   Alternative: Use the fact that the answer is 0 for large M? No, we need all M.
    *   Let's stick to the layering generation. For $N=30$, $\binom{29}{14}$ is the number of ways to choose which vertices are in odd layers. But the order of layers matters.
    *   Actually, we can use a DP that builds the graph structure directly?
    *   Given the complexity, I will implement the layering generation with pruning. If it's too slow, I might need to optimize. But for $N=30$, Python might be slow. I'll use PyPy if possible, or optimize the inner loop.
    *   Actually, the number of compositions of $N$ is $2^{N-1}$. We only care about those where $\sum_{k \text{ even}} L_k = N/2$. This is a subset.
    *   I'll generate compositions recursively.

## worker: Implement a recursive function to generate all val
The solution iterates over all valid BFS layering size sequences $(L_0, L_1, \dots, L_D)$ such that the sum of sizes of even-indexed layers is $N/2$ and odd-indexed layers is $N/2$. For each layering, it uses dynamic programming to compute the inclusion-exclusion sum over subsets of vertices that fail to have a neighbor in the previous BFS layer. The DP state tracks the number of vertices chosen in the subset and the number of allowed edges in the reduced graph. The final answer for each $M$ is computed by summing the contributions from all layerings.

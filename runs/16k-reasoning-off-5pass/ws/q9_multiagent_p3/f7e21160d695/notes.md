
## ideation
**Core Difficulty**: The problem requires minimizing the sum of bottleneck distances (maximum edge weight on the path) between two sets of vertices $A$ and $B$ by optimally permuting $B$. The bottleneck distance $f(u, v)$ is determined by the Minimum Spanning Tree (MST) of the graph. Specifically, $f(u, v)$ is the maximum weight of an edge on the unique path between $u$ and $v$ in the MST.

**Key Insight**:
1.  **MST Property**: The bottleneck distance between any two nodes is identical in the original graph and its MST. We can restrict our attention to the MST.
2.  **Incremental Connectivity**: If we process the edges of the MST in increasing order of weight, we can view the process as merging connected components.
3.  **Greedy Matching**: When an edge with weight $w$ merges two components $C_1$ and $C_2$, any unmatched $A$-node in $C_1$ and any unmatched $B$-node in $C_2$ (and vice versa) can now be paired with a cost of at most $w$. Since any future pairing for these nodes would involve edges with weight $\ge w$, it is always optimal to pair as many such cross-component $(A, B)$ pairs as possible *now* to "lock in" the lower cost $w$.
4.  **Counting vs. Identity**: The specific identity of the $A$ or $B$ nodes does not matter for the cost calculation at the moment of merging, only their counts within the respective components matter. We simply need to track how many unmatched $A$'s and $B$'s are in each component.

## worker: Read input $N, M, K$, the edges, and the sequences
The problem asks to minimize the sum of bottleneck distances $f(A_i, B_i)$ by permuting $B$. The bottleneck distance $f(u, v)$ corresponds to the maximum edge weight on the path between $u$ and $v$ in the Minimum Spanning Tree (MST) of the graph.

The algorithm proceeds as follows:
1.  **MST Construction**: We process edges in increasing order of weight. This is equivalent to building the MST (or rather, traversing it in Kruskal's order).
2.  **Component Tracking**: We use a Disjoint Set Union (DSU) to manage connected components. For each component, we maintain two counts:
    *   `countA`: The number of unmatched $A$ vertices currently in this component.
    *   `countB`: The number of unmatched $B$ vertices currently in this component.
3.  **Greedy Matching**: When an edge with weight $w$ connects two components $C_1$ and $C_2$:
    *   Any unmatched $A$ in $C_1$ and any unmatched $B$ in $C_2$ can now be paired with a cost of at most $w$.
    *   Similarly, any unmatched $A$ in $C_2$ and any unmatched $B$ in $C_1$ can be paired with cost $w$.
    *   Since any future pairing for these nodes would require edges with weight $\ge w$, it is optimal to pair as many such cross-component pairs as possible immediately.
    *   The number of pairs formed between $C_1$ and $C_2$ is $\min(\text{countA}[C_1], \text{countB}[C_2])$.
    *   The number of pairs formed between $C_2$ and $C_1$ is $\min(\text{countA}[C_2], \text{countB}[C_1])$.
    *   We add $w \times (\text{pairs}_{1\to2} + \text{pairs}_{2\to1})$ to the total cost.
    *   We then update the counts by subtracting the matched amounts and merging the components.
4.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations take nearly constant time on average. The total time complexity is dominated by sorting, $O(M \log M)$, which fits well within the constraints ($N, M \le 2 \times 10^5$).

This greedy approach works because the cost function is monotonic with respect to the edge weights used to connect components. By resolving connections with the smallest possible weights first, we minimize the total sum.

## worker: Run the code against the provided sample inputs to
The code implements the greedy strategy derived in the thought process:
1.  **MST Construction**: Edges are sorted by weight. We iterate through them, effectively building the MST (or rather, processing the connectivity events of the MST).
2.  **DSU with Counts**: We maintain a Disjoint Set Union (DSU) structure. For each component (root), we track `countA` (number of unmatched $A$ vertices) and `countB` (number of unmatched $B$ vertices).
3.  **Greedy Matching**: When an edge with weight $w$ merges two components $C_1$ and $C_2$:
    *   We can form pairs between $A \in C_1$ and $B \in C_2$ with cost $w$. The number of such pairs is $\min(\text{countA}[C_1], \text{countB}[C_2])$.
    *   We can also form pairs between $A \in C_2$ and $B \in C_1$ with cost $w$. The number is $\min(\text{countA}[C_2], \text{countB}[C_1])$.
    *   We add $w \times (\text{total pairs})$ to the answer.
    *   We subtract the matched counts from the respective components and merge the components in the DSU.
4.  **Correctness**: This works because any pair not matched at weight $w$ must be matched later with a weight $\ge w$. Matching as many as possible at the current smallest available weight minimizes the total sum. The specific identity of $A$ or $B$ nodes doesn't matter, only their counts within the component.

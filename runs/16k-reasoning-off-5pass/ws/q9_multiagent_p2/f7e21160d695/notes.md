
## ideation
The problem asks to minimize $\sum f(A_i, B_i)$ by permuting $B$. The function $f(x, y)$ is the bottleneck distance (minimax path weight) between $x$ and $y$. In any graph, the bottleneck distance between two nodes is determined by the unique path between them in the Minimum Spanning Tree (MST). Thus, we can first compute the MST of the given graph.

Once we have the MST, the problem becomes: given two multisets of vertices $A$ and $B$, assign a bijection to minimize the sum of bottleneck distances.
Key Insight: The bottleneck distance $f(u, v)$ is the weight of the maximum weight edge on the unique path between $u$ and $v$ in the MST.
Consider the edges of the MST sorted by weight in ascending order: $e_1, e_2, \dots, e_{N-1}$ with weights $w_1 \le w_2 \le \dots$.
When we consider edge $e_k = (u, v)$ with weight $w_k$, it merges two connected components in the forest formed by edges $e_1, \dots, e_{k-1}$. Let these components be $C_u$ and $C_v$.
Any pair $(a, b)$ where $a \in C_u$ and $b \in C_v$ (or vice versa) will have their bottleneck distance exactly $w_k$ if they haven't been "connected" by a smaller weight edge yet. Since the graph is a tree, there is no other path, so the path between any $a \in C_u$ and $b \in C_v$ MUST pass through $e_k$, making the max edge weight at least $w_k$. Since all other edges on the path within $C_u$ and $C_v$ are lighter than $w_k$, the bottleneck is exactly $w_k$.
To minimize the total sum, we want to maximize the number of pairs matched with small weights. This suggests a greedy strategy:
1. Build the MST.
2. Sort MST edges by weight ascending.
3. Use a Disjoint Set Union (DSU) to manage connected components.
4. For each component, maintain a count of how many $A$-nodes and $B$-nodes are currently in it.
5. Iterate through sorted MST edges. When an edge connects component $C_u$ and $C_v$ with weight $w$:
   - Let $cntA_u, cntB_u$ be counts in $C_u$ and $cntA_v, cntB_v$ in $C_v$.
   - The number of new pairs that can be formed with cost $w$ is $\min(cntA_u + cntA_v, cntB_u + cntB_v) - \text{existing\_matches\_within\_components}$. Actually, a simpler way is:
     - Total $A$'s available in $C_u \cup C_v$ is $S_A = cntA_u + cntA_v$.
     - Total $B$'s available in $C_u \cup C_v$ is $S_B = cntB_u + cntB_v$.
     - The number of pairs $(a, b)$ where $a$ and $b$ become connected *for the first time* at this edge weight is limited by the number of $A$'s and $B$'s crossing the cut.
     - Specifically, the number of pairs that *must* use this edge (or an edge of this weight) is $\min(S_A, S_B) - (\text{pairs already connected within } C_u \text{ and } C_v)$.
     - However, since we process edges in increasing order, any pair already connected has a cost $\le$ current weight. The pairs that become connected *now* are those where one node is in $C_u$ and the other in $C_v$.
     - Number of such pairs = $\min(cntA_u, cntB_v) + \min(cntA_v, cntB_u)$.
     - Add this count $\times w$ to the answer.
     - Update the counts for the merged component: $cntA_{new} = cntA_u + cntA_v$, $cntB_{new} = cntB_u + cntB_v$.

Wait, is it simply $\min(cntA_u, cntB_v) + \min(cntA_v, cntB_u)$?
Yes. Suppose we have $A$'s in $C_u$ and $B$'s in $C_v$. We can match them. The cost is $w$. Similarly for $A$'s in $C_v$ and $B$'s in $C_u$. These are the only new connections created by this edge. Pairs within $C_u$ or within $C_v$ were already connected by lighter edges (or we will account for them later if we view it differently, but the standard "cut" argument holds: the edge $e$ is the bottleneck for any path crossing the cut defined by removing $e$).
Actually, the logic is: The set of all pairs $(A_i, B_i)$ is partitioned by the edges of the MST. For a specific edge $e$ with weight $w$, let $S_e$ be the set of pairs $(a, b)$ such that the path between $a$ and $b$ in the MST uses $e$ as the maximum weight edge. Since edges are processed in increasing order, if we assign the cost $w$ to as many pairs as possible that *require* this edge to be connected, we minimize the sum.
The pairs that require edge $e$ are exactly those where $a$ is in one component formed by removing $e$, and $b$ is in the other.
Let the two components be $U$ and $V$.
Number of pairs $(a, b)$ with $a \in U, b \in V$ is $cntA_U \times cntB_V$.
Number of pairs $(a, b)$ with $a \in V, b \in U$ is $cntA_V \times cntB_U$.
Wait, we need to match specific $A_i$ to specific $B_j$. We can permute $B$. So we just need to count how many $A$'s in $U$ can be matched with $B$'s in $V$, and vice versa.
The number of such matches is $\min(cntA_U, cntB_V) + \min(cntA_V, cntB_U)$.
Why? Because we can greedily match $A$'s in $U$ with $B$'s in $V$ up to the limit of the smaller count. The remaining $A$'s in $U$ (if any) must eventually be matched with $B$'s in $U$ (which are already connected by lighter edges, so cost $< w$). Similarly for $V$.
So the contribution of edge $e$ to the total sum is $(\min(cntA_U, cntB_V) + \min(cntA_V, cntB_U)) \times w$.
Then we merge $U$ and $V$ and update counts.

Algorithm steps:
1. Read input.
2. Construct MST using Kruskal's or Prim's. Since $N, M \le 2 \cdot 10^5$, Kruskal's with sorting edges is efficient ($O(M \log M)$).
3. Store MST edges with their weights.
4. Initialize DSU. For each node $i$, $cntA[i] = 1$ if $i \in A$ else $0$, $cntB[i] = 1$ if $i \in B$ else $0$.
5. Sort MST edges by weight ascending.
6. Iterate edges $(u, v, w)$:
   - Find roots $rootU, rootV$.
   - If $rootU \neq rootV$:
     - Calculate contribution: $add = \min(cntA[rootU], cntB[rootV]) + \min(cntA[rootV], cntB[rootU])$.
     - Total sum += $add \times w$.
     - Merge sets: $parent[rootV] = rootU$.
     - Update counts: $cntA[rootU] += cntA[rootV]$, $cntB[rootU] += cntB[rootV]$.
7. Print total sum.

Corner cases:
- $K$ can be up to $N$.
- Graph is connected, so MST exists.
- $A_i \neq B_j$ guaranteed, but that doesn't affect the logic since we just count occurrences.
- Weights up to $10^9$, so use 64-bit integers for the sum.

Complexity:
- Sorting edges: $O(M \log M)$.
- DSU operations: $O(M \alpha(N))$.
- Total time: $O(M \log M)$, which fits within limits.

Pitfalls:
- Forgetting to use 64-bit integers for the answer.
- Incorrectly calculating the number of pairs (e.g., multiplying counts instead of taking min).
- Not handling the case where multiple edges have the same weight (sorting order doesn't matter for correctness, just process all).
- Input reading speed (use fast I/O in Python).

## worker: [todo] Implement the full solution in Python: read
The solution implements the following logic:
1.  **MST Construction**: The bottleneck distance $f(x, y)$ between two nodes in a graph is equal to the maximum edge weight on the unique path between them in the Minimum Spanning Tree (MST). We first construct the MST using Kruskal's algorithm, sorting all edges by weight.
2.  **Greedy Matching**: We process the MST edges in increasing order of weight. When an edge with weight $w$ connects two components $U$ and $V$, it becomes the "bottleneck" for any path between a node in $U$ and a node in $V$.
3.  **Counting Pairs**: To minimize the total sum, we greedily match as many pairs $(A_i, B_i)$ as possible that cross the cut between $U$ and $V$. The number of such pairs is $\min(\text{count of } A \text{ in } U, \text{count of } B \text{ in } V) + \min(\text{count of } A \text{ in } V, \text{count of } B \text{ in } U)$.
4.  **DSU**: We use a Disjoint Set Union (DSU) data structure to efficiently manage components and track the counts of $A$ and $B$ nodes within each component.
5.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations take nearly constant time on average. The overall complexity is dominated by sorting, $O(M \log M)$, which fits well within the time limits for $N, M \le 2 \times 10^5$.

## worker: Run the code against the provided sample inputs to
The solution implements the logic derived in the thought process:
1.  **MST Construction**: Uses Kruskal's algorithm. Edges are sorted by weight.
2.  **DSU with Counts**: Maintains `cntA` and `cntB` for each component root.
3.  **Greedy Matching**: Iterates through sorted MST edges. When an edge merges components $U$ and $V$ with weight $w$, it calculates the number of pairs $(A_i, B_j)$ that must cross this cut. This count is $\min(cntA_U, cntB_V) + \min(cntA_V, cntB_U)$. These pairs contribute $w$ to the total cost. The components are then merged, and counts are updated.
4.  **Correctness**: This approach correctly minimizes the sum because $f(x, y)$ is the weight of the heaviest edge on the path in the MST. By processing edges from lightest to heaviest, we assign the smallest possible weight to as many pairs as possible that are connected by that edge.
5.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations are nearly linear. Total time complexity is $O(M \log M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

## worker: Run the provided sample inputs to verify correctne
The solution implements the logic derived in the thought process:
1.  **MST Construction**: Uses Kruskal's algorithm. Edges are sorted by weight.
2.  **DSU with Counts**: Maintains `cntA` and `cntB` for each component root.
3.  **Greedy Matching**: Iterates through sorted MST edges. When an edge merges components $U$ and $V$ with weight $w$, it calculates the number of pairs $(A_i, B_j)$ that must cross this cut. This count is $\min(cntA_U, cntB_V) + \min(cntA_V, cntB_U)$. These pairs contribute $w$ to the total cost. The components are then merged, and counts are updated.
4.  **Correctness**: This approach correctly minimizes the sum because $f(x, y)$ is the weight of the heaviest edge on the path in the MST. By processing edges from lightest to heaviest, we assign the smallest possible weight to as many pairs as possible that are connected by that edge.
5.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations are nearly linear. Total time complexity is $O(M \log M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

## worker: finalize
The solution implements the logic derived from the problem analysis:
1.  **MST Construction**: The bottleneck distance $f(x, y)$ between two nodes in a graph is equal to the maximum edge weight on the unique path between them in the Minimum Spanning Tree (MST). We first construct the MST using Kruskal's algorithm, sorting all edges by weight.
2.  **Greedy Matching**: We process the MST edges in increasing order of weight. When an edge with weight $w$ connects two components $U$ and $V$, it becomes the "bottleneck" for any path between a node in $U$ and a node in $V$.
3.  **Counting Pairs**: To minimize the total sum, we greedily match as many pairs $(A_i, B_i)$ as possible that cross the cut between $U$ and $V$. The number of such pairs is $\min(\text{count of } A \text{ in } U, \text{count of } B \text{ in } V) + \min(\text{count of } A \text{ in } V, \text{count of } B \text{ in } U)$.
4.  **DSU**: We use a Disjoint Set Union (DSU) data structure to efficiently manage components and track the counts of $A$ and $B$ nodes within each component.
5.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations are nearly linear. Total time complexity is $O(M \log M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

The code reads input efficiently, builds the MST, and iterates through edges to accumulate the minimum cost.

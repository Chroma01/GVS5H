1.  **Understand $f(x, y)$**: The value $f(x, y)$ is the "bottleneck distance" between $x$ and $y$, which is the minimum possible maximum edge weight on any path between them. This is a classic property of the Minimum Spanning Tree (MST). Specifically, $f(x, y)$ is equal to the maximum edge weight on the unique path between $x$ and $y$ in the MST of the graph.
2.  **Construct the MST**: Use Kruskal's or Prim's algorithm to build the MST of the given graph. Since $N, M \le 2 \times 10^5$, an $O(M \log M)$ or $O(M \alpha(N))$ approach is required.
3.  **Precompute Pairwise Bottleneck Distances**: We need to compute $f(A_i, B_{\pi(i)})$ for optimal permutation $\pi$. This is a minimum weight perfect matching problem in a bipartite graph with parts $A$ and $B$. The cost matrix is $C_{ij} = f(A_i, B_j)$. Since $K$ can be up to $N$, an $O(K^3)$ min-cost max-flow or Hungarian algorithm is too slow. We need a faster way to compute the sum.
4.  **Leverage MST Structure**: The values $f(u, v)$ are determined by the MST. We can root the MST arbitrarily (e.g., at vertex 1) and use Lowest Common Ancestor (LCA) with binary lifting to find the max edge weight on the path between any two nodes in $O(\log N)$.
5.  **Optimize the Matching**: Computing all $K^2$ pairs takes $O(K^2 \log N)$, which is too slow if $K \approx 2 \cdot 10^5$. However, notice that the number of *distinct* edge weights in the MST is at most $N-1$. More importantly, we can use the property of the MST to compute the costs efficiently. Actually, $K$ is up to $N$, so $O(K^2)$ is definitely too slow. We need a different approach for the matching.
6.  **Re-evaluate Matching Complexity**: Wait, is there a greedy strategy? The problem is to minimize $\sum f(A_i, B_{\pi(i)})$. This is a minimum weight perfect matching in a complete bipartite graph. In general, this is hard. However, the costs $f(u,v)$ have special structure. They are ultrametric-like. Specifically, if we consider the edges of the MST sorted by weight, $f(u,v)$ is the weight of the heaviest edge on the path.
7.  **Alternative Approach: Sort Edges and Use DSU**: Consider the edges of the MST in increasing order of weight. As we add edges, connected components merge. For any pair $(u, v)$, $f(u, v)$ is the weight of the edge that first connects the component containing $u$ and the component containing $v$.
    We can use a greedy strategy based on the "cost" of matching. But standard min-cost bipartite matching is $O(K^3)$ or $O(K^2 \log K)$. With $K=2 \cdot 10^5$, this is impossible.
    
    Let's look at constraints again. $K \le N$. Is it possible that we don't need general matching?
    Actually, there is a known result: If the cost function $c(u, v)$ is an ultrametric (which $f(u, v)$ is, derived from a tree), the minimum weight perfect matching can be found more efficiently? Not necessarily simple.
    
    Let's reconsider the size. $K$ up to $200,000$. $O(K^2)$ is $4 \cdot 10^{10}$, too big.
    However, note that many $A_i$ or $B_j$ might be the same. We can group identical vertices. Let distinct values in $A$ be $A'_1, \dots, A'_p$ with counts $cntA$, and distinct in $B$ be $B'_1, \dots, B'_q$ with counts $cntB$. The problem reduces to matching these groups. But $p, q$ can still be $O(K)$.
    
    Is there a simpler observation?
    The function $f(u, v)$ is the max edge on the MST path.
    Let's sort all edges in the MST by weight.
    We can process edges from smallest to largest. When an edge $e$ with weight $w$ connects two components $C_1$ and $C_2$, any pair $(u, v)$ with $u \in C_1, v \in C_2$ (or vice versa) will have $f(u, v) = w$ *if* this is the first time they are connected.
    
    This looks like we can calculate the contribution of each edge to the total sum.
    Total Sum = $\sum_{\pi} \sum_{i} f(A_i, B_{\pi(i)})$.
    This is equivalent to $\sum_{e \in MST} w(e) \times (\text{number of pairs } (A_i, B_{\pi(i)}) \text{ whose path in MST uses } e \text{ as the max edge})$.
    
    For a fixed permutation $\pi$, an edge $e$ contributes $w(e)$ to the sum for index $i$ if $e$ is on the path between $A_i$ and $B_{\pi(i)}$ AND $e$ is the maximum weight edge on that path. In an MST, the path is unique, so $e$ is on the path. Is it the max? Yes, by definition of bottleneck path in MST, the max edge on the unique MST path is the bottleneck distance.
    
    So, for a fixed $\pi$, the cost is $\sum_{i=1}^K \max_{e \in Path(A_i, B_{\pi(i)})} w(e)$.
    We can rewrite this as $\sum_{e \in MST} w(e) \times (\text{count of } i \text{ such that } e \in Path(A_i, B_{\pi(i)}) \text{ and } e \text{ is the max edge})$.
    Actually, since it's an MST, the "max edge" condition is automatically satisfied for the bottleneck definition. But wait, if there are multiple edges with the same max weight, which one is "the" max? The value is the weight. So we just need to count how many pairs $(A_i, B_{\pi(i)})$ have their path passing through $e$.
    
    Wait, if the path passes through $e$, is $w(e)$ necessarily the maximum?
    In an MST constructed by Kruskal's, if we process edges in increasing order, when we add $e$, it connects two components. Any path between a node in $C_1$ and a node in $C_2$ MUST use $e$ (or another edge of same weight added at same step, but let's assume distinct weights for simplicity or handle ties carefully). And since $e$ is the largest weight edge added so far to connect these components, it is the maximum weight edge on the path.
    
    So, $f(u, v) = \sum_{e \in Path(u, v)} \mathbb{I}(e \text{ is the max weight edge on } Path(u, v)) \times w(e)$? No, that's not right. $f(u, v)$ is just the weight of the single heaviest edge.
    
    Correct decomposition:
    $f(u, v) = \sum_{e \in MST} w(e) \times \mathbb{I}(e \text{ is the heaviest edge on the path between } u \text{ and } v)$.
    If edge weights are distinct, this is unique. If not, we can break ties arbitrarily (e.g., by edge index) to define a unique "heaviest" edge for the purpose of the sum, as long as we are consistent. The value $f(u, v)$ is the weight.
    
    So, Total Cost for permutation $\pi$ = $\sum_{i=1}^K \sum_{e \in MST} w(e) \cdot \mathbb{I}(e \text{ is max on } Path(A_i, B_{\pi(i)}))$.
    Swap sums: $\sum_{e \in MST} w(e) \cdot (\text{number of } i \text{ such that } e \text{ is max on } Path(A_i, B_{\pi(i)}))$.
    
    Let $S_e$ be the set of indices $i$ such that the path between $A_i$ and $B_{\pi(i)}$ has $e$ as its maximum weight edge.
    We want to minimize $\sum_{e} w(e) |S_e|$.
    
    This still depends on $\pi$.
    
    Let's look at the structure of "e is max on path".
    If we remove all edges with weight $> w(e)$, then $u$ and $v$ are in the same component if and only if $f(u, v) \le w(e)$.
    Specifically, $f(u, v) = w(e)$ if $u$ and $v$ become connected exactly when edge $e$ (or an edge of same weight) is added.
    
    Let's group edges by weight. Sort distinct weights $W_1 < W_2 < \dots < W_m$.
    Let $G_k$ be the graph with only edges of weight $\le W_k$.
    $f(u, v) \le W_k \iff u, v$ are in the same connected component in $G_k$.
    
    We want to minimize $\sum_{i} f(A_i, B_{\pi(i)})$.
    Note that $\sum_{i} f(A_i, B_{\pi(i)}) = \sum_{i} \sum_{k=1}^m W_k \cdot \mathbb{I}(f(A_i, B_{\pi(i)}) = W_k)$.
    Also $\mathbb{I}(f(u, v) = W_k) = \mathbb{I}(f(u, v) \le W_k) - \mathbb{I}(f(u, v) \le W_{k-1})$.
    
    So Sum $= \sum_{i} \sum_{k=1}^m W_k (\mathbb{I}(A_i, B_{\pi(i)} \text{ connected in } G_k) - \mathbb{I}(A_i, B_{\pi(i)} \text{ connected in } G_{k-1}))$.
    $= \sum_{k=1}^m W_k \left( \sum_{i} \mathbb{I}(A_i, B_{\pi(i)} \text{ connected in } G_k) - \sum_{i} \mathbb{I}(A_i, B_{\pi(i)} \text{ connected in } G_{k-1}) \right)$.
    
    Let $C_k(\pi)$ be the number of pairs $(A_i, B_{\pi(i)})$ that are connected in $G_k$.
    We want to minimize $\sum_{k=1}^m W_k (C_k(\pi) - C_{k-1}(\pi))$.
    This is equivalent to minimizing $\sum_{k=1}^m (W_k - W_{k+1}) C_k(\pi)$? No, telescoping sum logic:
    $\sum_{k=1}^m W_k C_k - \sum_{k=1}^m W_k C_{k-1} = W_m C_m - W_1 C_0 + \sum_{k=1}^{m-1} (W_k - W_{k+1}) C_k$.
    Since the graph is connected, $C_m = K$ (all pairs connected). $C_0 = 0$.
    So Sum $= W_m K + \sum_{k=1}^{m-1} (W_k - W_{k+1}) C_k(\pi)$.
    Since $W_k < W_{k+1}$, the coefficients $(W_k - W_{k+1})$ are negative.
    To minimize the total sum, we need to **maximize** the weighted sum of $C_k(\pi)$ with negative weights, which means we want to **minimize** the terms with negative coefficients?
    Wait. $W_k - W_{k+1}$ is negative. Let $D_k = W_{k+1} - W_k > 0$.
    Sum $= W_m K - \sum_{k=1}^{m-1} D_k C_k(\pi)$.
    To minimize the Sum, we must **maximize** $\sum_{k=1}^{m-1} D_k C_k(\pi)$.
    
    $C_k(\pi)$ is the number of pairs $(A_i, B_{\pi(i)})$ such that $A_i$ and $B_{\pi(i)}$ are in the same connected component in $G_k$.
    
    This is a crucial insight. We need to choose $\pi$ to maximize $\sum_{k} D_k C_k(\pi)$.
    Since $D_k > 0$, we want to maximize $C_k(\pi)$ for larger $D_k$ (which correspond to gaps between small weights? No, $D_k$ is the gap between $W_k$ and $W_{k+1}$).
    
    Actually, $C_k(\pi)$ depends on the components in $G_k$.
    Let the connected components of $G_k$ be $Comp_{k, 1}, Comp_{k, 2}, \dots$.
    For a fixed $k$, $C_k(\pi) = \sum_{j} (\text{number of } i \text{ such that } A_i \in Comp_{k, j} \text{ and } B_{\pi(i)} \in Comp_{k, j})$.
    
    Let $n_{A, k, j}$ be the count of $A_i$'s in component $j$ of $G_k$.
    Let $n_{B, k, j}$ be the count of $B_i$'s in component $j$ of $G_k$.
    We want to match the $A$'s and $B$'s to maximize the number of matches within the same component.
    This is a maximum weight bipartite matching problem? No, for a fixed $k$, the maximum number of pairs $(A_i, B_{\pi(i)})$ falling in the same component is $\sum_j \min(n_{A, k, j}, n_{B, k, j})$.
    However, $\pi$ must be the **same** for all $k$. We cannot optimize each $k$ independently.
    
    This suggests the greedy strategy might not work directly for the global sum.
    
    BUT, notice that $G_k$ is a subgraph of $G_{k+1}$. The components in $G_{k+1}$ are formed by merging components from $G_k$.
    
    Is there a simpler solution?
    If we just compute the cost matrix $C_{ij} = f(A_i, B_j)$ and run Min-Cost Perfect Matching, it's too slow.
    
    Let's check constraints and typical solutions for this specific problem (AtCoder ABC 274 F? No, similar to "Bottleneck Matching").
    
    Actually, there is a simpler property.
    If we sort the edges of the MST, we can determine the cost.
    
    Let's try a different angle.
    Since $K$ is large, maybe the number of distinct $A_i$ and $B_j$ is small? No guarantee.
    
    Wait, look at Sample 1.
    A = [1, 1, 3], B = [4, 4, 2].
    f(1,4)=2, f(1,4)=2, f(3,2)=5. Sum=9?
    Sample output says 8 with B permuted to [2, 4, 4].
    f(1,2)=5, f(1,4)=2, f(3,4)=1. Sum=8.
    
    The costs are:
    A1=1: f(1,4)=2, f(1,2)=5.
    A2=1: f(1,4)=2, f(1,2)=5.
    A3=3: f(3,4)=1, f(3,2)=5.
    
    Matrix:
       B4  B2
    A1  2   5
    A2  2   5
    A3  1   5
    
    We need to pick one from each row, distinct columns.
    Options:
    (A1,B4), (A2,B2), (A3,??) -> B4 used. A3 needs B2? No, B2 used by A2.
    Permutations of B (4,4,2):
    1. (4,4,2): A1-4(2), A2-4(2), A3-2(5). Sum 9.
    2. (4,2,4): A1-4(2), A2-2(5), A3-4(1). Sum 8.
    3. (2,4,4): A1-2(5), A2-4(2), A3-4(1). Sum 8.
    
    Minimum is 8.
    
    This is a standard Assignment Problem.
    With $K=200,000$, we cannot use Hungarian.
    
    However, the cost matrix has low rank or special structure?
    The costs are derived from a tree.
    
    Key realization:
    The problem can be solved by **Min-Cost Max-Flow** on a specific graph? No.
    
    Let's go back to: Minimize $\sum_{k=1}^{m-1} D_k C_k(\pi)$.
    We want to maximize $\sum D_k C_k(\pi)$.
    
    Consider the edges of the MST in increasing order.
    When we merge two components $U$ and $V$ with an edge of weight $w$, any pair $(a, b)$ with $a \in U, b \in V$ will have $f(a, b) = w$ (assuming this is the first connection).
    
    Let's define the "contribution" of a pair $(a, b)$ to the sum.
    
    Actually, there is a known greedy algorithm for this specific "Bottleneck Matching" on trees?
    
    If we simply sort all $A_i$ and $B_j$ and try to match closest ones? No, tree distance is not linear.
    
    Let's use the property that $f(u, v)$ is the max edge on the path.
    
    We can solve this using **Min-Cost Perfect Matching in Bipartite Graphs** but optimized?
    
    Wait, if $K$ is small, we use Hungarian. If $K$ is large, maybe the graph structure allows a simpler solution.
    
    Actually, looking at similar problems (e.g., Codeforces "Matching on a Tree"), if the cost is the path length, it's hard. But here cost is bottleneck.
    
    Let's assume the intended solution involves the $O(K^2 \log N)$ precomputation being too slow, so we must avoid computing all pairs.
    
    However, note that $N, M, K \le 2 \cdot 10^5$.
    
    Is it possible that we can compute the answer by iterating on the edges of the MST?
    
    Let's try a randomized or heuristic approach? No, needs exact.
    
    Let's look at the constraints again.
    
    Actually, there is a solution using **Divide and Conquer** or **DSU on Tree**?
    
    Let's stick to the formula:
    Min Sum $= W_m K - \sum_{k=1}^{m-1} D_k C_k(\pi)$.
    We need to maximize $\sum D_k C_k(\pi)$.
    
    $C_k(\pi)$ is the number of matched pairs $(A_i, B_{\pi(i)})$ that are in the same component in $G_k$.
    
    Let's process components from $G_m$ down to $G_1$?
    
    This problem is equivalent to: Find a permutation $\pi$ that maximizes the "alignment" of $A$ and $B$ with respect to the hierarchy of components defined by the MST edges.
    
    Since $D_k$ are positive weights, we want to maximize matches in components that have large gaps to the next weight.
    
    This looks like we can solve it greedily from the finest components (largest weights) to coarsest?
    
    Actually, if we consider the MST edges, we can determine the optimal matching locally?
    
    Given the complexity, I will provide a solution that:
    1. Builds MST.
    2. Computes $f(A_i, B_j)$ for all pairs? No, $K^2$ is too big.
    
    Wait, if $K$ is up to $2 \cdot 10^5$, is it possible that the number of *distinct* values in $A$ and $B$ is small? No.
    
    However, there is a specialized algorithm for Min-Cost Perfect Matching when the cost matrix is an **Ultrametric**.
    An ultrametric satisfies $d(x, z) \le \max(d(x, y), d(y, z))$.
    The bottleneck distance on a tree is an ultrametric.
    
    For ultrametrics, the minimum weight perfect matching can be found in $O(K \log K)$ or similar?
    
    Algorithm for Ultrametric Matching:
    1. Sort all pairs? No.
    2. Use the hierarchical clustering structure (the MST).
    
    We can process the MST edges from smallest to largest.
    Initially, each node is a component.
    We maintain a pool of "available" $A$ nodes and $B$ nodes in each component.
    When two components merge, we can match $A$'s from one with $B$'s from the other?
    
    Actually, the standard greedy for bottleneck matching:
    Sort all potential edges by weight?
    
    Let's use the following logic:
    We want to match $A_i$ and $B_j$ with small $f(A_i, B_j)$.
    Small $f$ means they are connected by small edges.
    
    We can iterate through the edges of the MST in increasing order of weight.
    Maintain a set of unmatched $A$'s and $B$'s in each connected component.
    When an edge $e=(u, v)$ with weight $w$ merges component $C_u$ and $C_v$:
    We can match any unmatched $A$ in $C_u$ with any unmatched $B$ in $C_v$, or vice versa.
    Since $w$ is the current smallest available edge connecting these two sets, matching them now incurs cost $w$.
    Any match between two $A$'s or two $B$'s is not allowed.
    We should greedily match as many pairs as possible between $C_u$ and $C_v$ to "save" them from higher costs later?
    
    Yes! This is the standard greedy strategy for bottleneck matching on trees.
    
    **Greedy Strategy**:
    1. Build MST.
    2. Sort MST edges by weight ascending.
    3. Use DSU to maintain components. For each component, maintain a list (or count) of unmatched $A$ nodes and unmatched $B$ nodes.
    4. Iterate through sorted edges. For edge $(u, v)$ with weight $w$:
       - Find roots $R_u, R_v$.
       - If $R_u \neq R_v$:
         - We can match $\min(\text{countA}[R_u], \text{countB}[R_v])$ pairs.
         - We can also match $\min(\text{countA}[R_v], \text{countB}[R_u])$ pairs.
         - Total matches possible = $\min(\text{countA}[R_u], \text{countB}[R_v]) + \min(\text{countA}[R_v], \text{countB}[R_u])$.
         - Add `matches * w` to total cost.
         - Update the counts for the new merged component:
           - `new_countA = countA[R_u] + countA[R_v] - matches`
           - `new_countB = countB[R_u] + countB[R_v] - matches`
           - Note: The unmatched nodes remain in the component.
         - Merge $R_u$ and $R_v$.
    5. After processing all edges, all nodes are in one component. The remaining unmatched $A$'s and $B$'s must have been matched?
       Wait, $K$ is the same for A and B. Total A = Total B = K.
       The greedy matching ensures that we match as many as possible at the lowest possible cost.
       Any remaining unmatched nodes will eventually be matched at higher costs?
       Actually, if we just sum the costs of the matches made, is that the total?
       Yes, because every pair $(A_i, B_j)$ is matched exactly once. The cost assigned is the weight of the edge that first connects their components. This is exactly $f(A_i, B_j)$.
       
    This greedy approach works because the cost function is an ultrametric derived from the MST. Matching earlier (at lower weight) is always better or equal to matching later.
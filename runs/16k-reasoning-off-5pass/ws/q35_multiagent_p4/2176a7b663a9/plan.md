1.  **Graph Construction Insight**: The condition for an edge between $i$ and $j$ is that $[L_i, R_i] \cap [L_j, R_j] = \emptyset$. This means either $R_i < L_j$ or $R_j < L_i$. This structure suggests that the graph is a "comparability graph" of intervals, specifically the complement of an interval graph.
2.  **Connectivity Analysis**: Two intervals are connected if they don't overlap. The graph can have multiple connected components. Within a connected component, we want the shortest path (minimum weight sum of vertices). Since edge weights are effectively 0 (only vertex weights matter), the shortest path between $s$ and $t$ in a component is simply the sum of the minimum weight vertex in the component plus the minimum weight vertex in the component reachable from $s$ and $t$? No, the path is a sequence of vertices. The minimum weight path between $s$ and $t$ in an unweighted graph (where only node costs exist) is not trivial. However, note that if the graph is connected, the shortest path is often just $s \to k \to t$ where $k$ is a central node with minimum weight, or even just $s \to t$ if they are connected.
3.  **Key Observation**: The graph is the complement of an interval graph. Interval graphs are chordal. The complement of an interval graph is a co-comparability graph. More importantly, we can use the geometric property. Two intervals are adjacent if disjoint.
4.  **Algorithm Strategy**:
    *   We need to efficiently determine connectivity and shortest paths.
    *   Notice that if $s$ and $t$ are in the same connected component, the minimum weight path might involve intermediate nodes.
    *   However, a crucial property of this specific graph (complement of interval graph) is that it has a small "diameter" in terms of structure or can be decomposed.
    *   Actually, let's look at the constraints. $N, Q \le 2 \times 10^5$. We need an efficient solution, likely $O(N \log N)$ or $O((N+Q) \log N)$.
    *   Let's consider the connected components. We can find connected components using a sweep-line algorithm or by building the graph implicitly.
    *   For the shortest path: In many such geometric graphs, the shortest path between $s$ and $t$ is either the direct edge $(s, t)$ if it exists, or a path of length 2 ($s \to k \to t$) if a common neighbor $k$ exists that connects to both, or potentially longer.
    *   Wait, is the diameter small? For interval graphs, the complement can have large diameter? No, actually, for the complement of an interval graph, the diameter is at most 3? Or is it related to the number of "extremal" intervals?
    *   Let's check the sample. Path $1 \to 3 \to 4$. Direct edge $1-4$? $[2,4]$ and $[4,5]$ intersect at 4. So no direct edge. Path $1 \to 3 \to 4$ works.
    *   Hypothesis: The shortest path between any two connected nodes $s$ and $t$ is either:
        1.  Direct edge $s-t$ (weight $W_s + W_t$).
        2.  Path of length 2: $s \to k \to t$ (weight $W_s + W_k + W_t$).
        3.  Path of length 3: $s \to k \to m \to t$ (weight $W_s + W_k + W_m + W_t$).
    *   It turns out that for the complement of an interval graph, the diameter is at most 3. Thus, we only need to check paths of length 1, 2, and 3.
    *   To implement this:
        1.  Identify connected components.
        2.  For each query $(s, t)$, if they are in different components, output -1.
        3.  If in the same component, check if direct edge exists. If so, candidate weight $W_s + W_t$.
        4.  Check if there exists a node $k$ such that $s-k$ and $k-t$ are edges. This is equivalent to finding a $k$ disjoint from both $[L_s, R_s]$ and $[L_t, R_t]$. We want to minimize $W_k$.
        5.  If no such $k$ exists or path length 2 is worse, check path length 3. This is harder.
    *   Alternative approach: Since the diameter is small, we can precompute the "best" intermediate nodes.
    *   Actually, a simpler observation: The minimum weight path between $s$ and $t$ is $\min(W_s + W_t, W_s + W_t + \min_{k \in N(s) \cap N(t)} W_k, \dots)$.
    *   We can use a segment tree or similar structure to query the minimum weight node in a range of "disjoint" intervals.
    *   Specifically, $k$ is disjoint from $[L_s, R_s]$ if $R_k < L_s$ or $R_s < L_k$. Similarly for $t$.
    *   We can find the minimum weight node $k$ satisfying these conditions.
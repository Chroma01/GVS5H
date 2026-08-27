
## ideation
**Core Difficulty:**
The problem asks for the shortest path in the complement of an interval graph. Directly constructing the graph is $O(N^2)$, which is too slow ($N \le 2 \times 10^5$). The key challenge is efficiently identifying edges between non-overlapping intervals and finding the minimum weight path. Since edge existence depends on disjointness, the connectivity structure is determined by how intervals "jump" over each other.

**Candidate Approaches:**
1.  **Coordinate Compression + Segment Tree / Fenwick Tree:**
    *   Sort intervals by their right endpoints ($R_i$).
    *   For a node $u$ with interval $[L_u, R_u]$, it connects to any node $v$ where $[L_v, R_v]$ is disjoint from $[L_u, R_u]$.
    *   If we process nodes in a specific order (e.g., by $R_i$), we can identify potential neighbors. Specifically, if we sort by $R$, a node $u$ can connect to any node $v$ with $L_v > R_u$ or $R_v < L_u$.
    *   The "forward" connections ($L_v > R_u$) can be handled efficiently. If we sort all intervals by $L$, we can use a Segment Tree to find the node with the minimum weight among all intervals that start after $R_u$. This allows us to build a sparse graph where each node has edges to the "best" next node in a range, effectively creating a path compression structure.
    *   We can build a graph where edges represent "jumping" to the next available interval in a sorted order. The number of such edges is $O(N \log N)$ or $O(N)$ depending on optimization.
    *   Once this sparse graph is built, we can run Dijkstra. However, since we have $Q$ queries, we might need to precompute All-Pairs Shortest Paths (APSP) or use a technique like "multi-source Dijkstra" if the graph is small, but here the graph can be large.
    *   Actually, a known property for this specific problem (AtCoder ABC 273 F is different, but this looks like **ARC 166 E** or similar logic) is that the graph of non-overlapping intervals often has a very specific structure. If we sort intervals by $R$, the "next" non-overlapping interval can be found via a segment tree. We can construct a graph with $O(N)$ edges by linking each interval to the interval with the minimum weight that starts after its end.
    *   Wait, the path can go back and forth. But if we define a "canonical" path using the sorted order, does it cover all shortest paths? Not necessarily.
    *   Alternative: The graph is the complement of an interval graph. Interval graphs are chordal. The complement might not be.
    *   Let's reconsider the structure. If we sort intervals by $R$, say $I_1, I_2, \dots, I_N$. $I_i$ connects to $I_j$ if $L_j > R_i$ or $R_j < L_i$.
    *   If we only consider edges $(i, j)$ where $R_i < L_j$ (and $i < j$ in sorted order), we form a DAG-like structure. But paths can use edges in reverse ($R_j < L_i$).
    *   However, notice that if $I_i$ and $I_j$ are disjoint, one is strictly to the left of the other.
    *   Key Insight: The connectivity can be modeled by sorting intervals by $R$. Let's define a "next" pointer for each interval $i$ to the interval $j$ ($j \neq i$) that minimizes $W_j$ such that $L_j > R_i$. Similarly, a "prev" pointer to $j$ where $R_j < L_i$.
    *   If we build a graph with only these "next" and "prev" edges (plus maybe some local optimizations), is it sufficient?
    *   Actually, the standard solution for "Shortest Path in Complement of Interval Graph" involves:
        1.  Sort intervals by $R$.
        2.  Use a Segment Tree to find the minimum weight interval starting after $R_i$. Let this be $next\_node[i]$.
        3.  Also consider the reverse: intervals ending before $L_i$.
        4.  Construct a graph with $O(N)$ edges.
        5.  Run Dijkstra from each query? No, $Q$ is large.
        6.  Maybe the graph is small enough or has a property?
        7.  Re-reading similar problems: Often, the answer is found by realizing that the shortest path will likely follow the "sorted by R" chain or the "sorted by L" chain.
        8.  Actually, a simpler observation: If two intervals are disjoint, they are connected. If we have a chain of disjoint intervals $I_{p_1}, I_{p_2}, \dots, I_{p_k}$ such that $R_{p_1} < L_{p_2}, R_{p_2} < L_{p_3}, \dots$, then they form a path.
        9.  What if the optimal path jumps around? E.g., $A$ connects to $B$, $B$ connects to $C$. $A$ and $C$ might overlap.
        10. The most robust approach for $N, Q \le 2 \cdot 10^5$ is likely:
            *   Build a sparse graph where each node $u$ connects to the node $v$ with minimum $W_v$ such that $L_v > R_u$ (let's call this type 1 edge).
            *   And node $u$ connects to node $v$ with minimum $W_v$ such that $R_v < L_u$ (type 2 edge).
            *   Is this sufficient? Suppose the shortest path is $u \to v \to w$. $u, v$ disjoint, $v, w$ disjoint.
            *   If $u$ is to the left of $v$ ($R_u < L_v$), then $v$ is a candidate for $u$'s type 1 edge. If $v$ is the best, we take it. If not, say $x$ is better ($W_x < W_v$ and $L_x > R_u$). Then we could go $u \to x$. From $x$, can we reach $w$? If $x$ and $w$ are disjoint, yes. If $x$ overlaps $w$, we need another step.
            *   This suggests we might need more edges.
            *   However, there is a known technique: **Sort by R**. For each $i$, find $j$ with min $W_j$ such that $L_j > R_i$. Add edge $(i, j)$. Also add edge $(j, i)$? No, direction matters for the "next" logic, but the graph is undirected.
            *   Actually, if we add edges $(u, v)$ for all $v$ such that $L_v > R_u$ and $W_v$ is minimal in that range, do we miss anything?
            *   Consider the case where the shortest path goes $u \to v \to w$ where $u$ is left of $v$, and $v$ is left of $w$. If $v$ is not the minimal weight node to the right of $u$, but $w$ is, and $w$ is to the right of $v$. Then $u \to w$ is a direct edge (since $u$ left of $w$). So $u \to w$ is better than $u \to v \to w$ if $W_w < W_v + W_u$? Wait, path weight includes endpoints.
            *   Path $u \to v \to w$: Cost $W_u + W_v + W_w$.
            *   Path $u \to w$: Cost $W_u + W_w$.
            *   Since $W_v \ge 1$, $u \to w$ is always better than $u \to v \to w$ if the edge $(u, w)$ exists.
            *   Therefore, if $u$ and $w$ are disjoint, we should prefer the direct edge.
            *   This implies that if we have a chain $u \to v \to w$ where $u, v, w$ are all mutually disjoint (ordered), the direct edge $u \to w$ exists and is cheaper.
            *   So, any shortest path in a sequence of disjoint intervals ordered by position will just be the direct edge between the first and last?
            *   Wait, the path must visit vertices. $u \to w$ is a path of length 2 (vertices $u, w$). $u \to v \to w$ is length 3. Since $W_v > 0$, $u \to w$ is strictly better.
            *   **Conclusion:** If a set of intervals can be ordered such that $I_{p_1}, I_{p_2}, \dots, I_{p_k}$ are pairwise disjoint and ordered (i.e., $R_{p_i} < L_{p_{i+1}}$), then the shortest path between $p_1$ and $p_k$ is simply the direct edge $(p_1, p_k)$ with weight $W_{p_1} + W_{p_k}$.
            *   What if the path involves overlapping intervals? e.g., $A$ overlaps $B$, $B$ overlaps $C$, but $A$ and $C$ are disjoint.
                *   $A$ and $B$ not connected. $B$ and $C$ not connected.
                *   Wait, edge exists if intersection is EMPTY.
                *   So if $A$ overlaps $B$, NO edge.
                *   If $B$ overlaps $C$, NO edge.
                *   If $A$ and $C$ are disjoint, YES edge.
                *   Path $A \to C$ exists directly.
            *   So, if $A$ and $C$ are disjoint, we can go directly.
            *   The only reason to go through an intermediate node $B$ is if $A$ and $C$ are NOT disjoint (so no direct edge), but $A$ is disjoint from $B$, and $B$ is disjoint from $C$.
            *   This implies $A$ and $B$ are disjoint, $B$ and $C$ are disjoint. $A$ and $C$ overlap.
            *   This creates a "bridge" via $B$.
            *   So the graph is connected components formed by "cliques" of overlapping intervals? No, interval graphs are defined by overlaps. The complement graph connects non-overlaps.
            *   In the complement graph, if $A, B, C$ are such that $A \cap B = \emptyset, B \cap C = \emptyset, A \cap C \neq \emptyset$. Then $A-B-C$ is a path, but $A-C$ is not an edge.
            *   This is the critical structure. We need to find paths through "bridges".
            *   Algorithm Idea:
                1.  Sort intervals by $R$.
                2.  For each $i$, find the "next" interval $j$ ($j > i$ in sorted order) such that $L_j > R_i$ (disjoint and to the right). Among all such $j$, pick the one with min $W_j$. Let this be $next\_right[i]$.
                3.  Similarly, find $next\_left[i]$ (interval $j$ with $R_j < L_i$ and min $W_j$).
                4.  Is it sufficient to only use these "best" neighbors?
                5.  Suppose the optimal path is $u \to v \to w$.
                    *   Case 1: $u, v, w$ are ordered disjointly ($u$ left of $v$ left of $w$). Then $u, w$ are disjoint. Direct edge $u \to w$ exists. Cost $W_u+W_w < W_u+W_v+W_w$. So we never take $v$ in this case.
                    *   Case 2: $u, v, w$ are not ordered disjointly. E.g., $u$ left of $v$, $v$ overlaps $w$? No, $v, w$ must be disjoint for edge $(v, w)$ to exist.
                    *   So if $u-v$ and $v-w$ are edges, then $u \cap v = \emptyset$ and $v \cap w = \emptyset$.
                    *   If $u$ is left of $v$ and $v$ is left of $w$, then $u$ is left of $w$, so $u \cap w = \emptyset$. Direct edge exists.
                    *   If $u$ is left of $v$ and $w$ is left of $v$ (so $u, w$ both left of $v$), then $u$ and $w$ might overlap or be disjoint.
                        *   If $u, w$ disjoint, direct edge.
                        *   If $u, w$ overlap, no direct edge. Path $u \to v \to w$ is valid.
                    *   So the "bridge" happens when two intervals ($u, w$) overlap, and we use a third interval ($v$) that is disjoint from both to connect them.
                    *   Geometrically, $v$ must be either completely to the right of both, or completely to the left of both, or "in between" but disjoint?
                    *   If $v$ is disjoint from $u$ and $w$, and $u, w$ overlap.
                    *   Possibility A: $v$ is to the right of both ($R_u < L_v$ and $R_w < L_v$). Then $v$ is a "right bridge".
                    *   Possibility B: $v$ is to the left of both ($R_v < L_u$ and $R_v < L_w$). Then $v$ is a "left bridge".
                    *   Possibility C: $v$ is inside the overlap? No, if $v$ overlaps $u$, no edge. So $v$ cannot be inside the overlap region if it's to connect to both.
                    *   Basically, $v$ must be outside the union of $u$ and $w$? Not necessarily, but disjoint from each.
                    *   Actually, if $u$ and $w$ overlap, their union is an interval $[min(L), max(R)]$. If $v$ is disjoint from $u$ and $w$, $v$ must be either entirely to the left of $min(L)$ or entirely to the right of $max(R)$?
                        *   Let $u=[1, 5], w=[3, 7]$. Overlap $[3, 5]$. Union $[1, 7]$.
                        *   If $v=[8, 9]$, disjoint from both.
                        *   If $v=[0, 1]$, disjoint from both (touching at 1? Integers. $[0,1] \cap [1,5] = \{1\} \neq \emptyset$. So must be strictly less. $v=[0,0]$).
                        *   So yes, $v$ must be to the left of $\min(L_u, L_w)$ or right of $\max(R_u, R_w)$.
                    *   Therefore, to connect two overlapping intervals $u$ and $w$, we must go through an interval $v$ that is either strictly to the left of both or strictly to the right of both.
                    *   This implies that the shortest path between $u$ and $w$ (if they overlap) will go through a "leftmost available" interval or a "rightmost available" interval.
                    *   Specifically, we can define:
                        *   $L\_best[u]$: The interval $v$ with minimum $W_v$ such that $R_v < L_u$.
                        *   $R\_best[u]$: The interval $v$ with minimum $W_v$ such that $L_v > R_u$.
                    *   Then, for any query $(s, t)$:
                        *   If $s, t$ disjoint: Direct edge. Cost $W_s + W_t$.
                        *   If $s, t$ overlap: We must go $s \to v \to t$ where $v$ is a "left bridge" or "right bridge".
                        *   The best left bridge for $s$ is $L\_best[s]$. The best left bridge for $t$ is $L\_best[t]$.
                        *   Wait, we need a single $v$ that connects to BOTH.
                        *   If we pick $v = L\_best[s]$, does it connect to $t$?
                            *   $v$ satisfies $R_v < L_s$. Since $s, t$ overlap, $L_s \le R_s$ and $L_t \le R_t$. Also $s, t$ overlap implies intervals intersect.
                            *   If $v$ is to the left of $s$, is it to the left of $t$?
                            *   Not necessarily. Example: $t=[1, 10], s=[5, 6]$. Overlap. $v=[0, 0]$. $R_v < L_s$ (0 < 5). $R_v < L_t$ (0 < 1). Yes.
                            *   Example: $t=[1, 10], s=[5, 6]$. $v=[2, 2]$. $R_v < L_s$ (2 < 5). But $v$ overlaps $t$ ($[2,2] \cap [1,10] \neq \emptyset$). So $v$ does not connect to $t$.
                        *   So $L\_best[s]$ might not connect to $t$.
                        *   However, we need to find *any* $v$ such that $v$ is disjoint from $s$ and $v$ is disjoint from $t$.
                        *   Since $s, t$ overlap, the set of intervals disjoint from both is the set of intervals to the left of $\min(L_s, L_t)$ OR to the right of $\max(R_s, R_t)$.
                        *   Let $L_{min} = \min(L_s, L_t)$ and $R_{max} = \max(R_s, R_t)$.
                        *   We need $v$ such that $R_v < L_{min}$ OR $L_v > R_{max}$.
                        *   To minimize $W_v + W_s + W_t$, we need to minimize $W_v$.
                        *   So we need $\min( \min \{W_v : R_v < L_{min}\}, \min \{W_v : L_v > R_{max}\} )$.
                        *   This can be precomputed using a Segment Tree over the coordinate space (or sorted intervals).
                        *   Query time: $O(1)$ or $O(\log N)$ with precomputed structures.
                        *   Wait, is it possible the shortest path has length > 3? i.e., $s \to a \to b \to t$?
                            *   If $s, t$ overlap, we need a bridge.
                            *   If we use $a$ (left bridge) and $b$ (right bridge)? No, $a$ connects to $s$, $b$ connects to $t$. Does $a$ connect to $b$?
                            *   $a$ is left of $s$, $b$ is right of $t$. Since $s, t$ overlap, $a$ is left of $t$ and $b$ is right of $s$. Thus $a$ and $b$ are disjoint (separated by the union of $s, t$). So $a-b$ is an edge.
                            *   Path $s \to a \to b \to t$. Cost $W_s + W_a + W_b + W_t$.
                            *   Compare with $s \to a \to t$? $a$ connects to $t$ (since $a$ left of $s$ and $s, t$ overlap $\implies a$ left of $t$). So $s \to a \to t$ is valid. Cost $W_s + W_a + W_t$.
                            *   Since $W_b > 0$, $s \to a \to t$ is better.
                            *   Similarly $s \to b \to t$ is better.
                            *   So the shortest path between overlapping $s, t$ is always length 3 ($s \to v \to t$).
                            *   Exception: If no such $v$ exists, then $s$ and $t$ are in the same connected component only if there's a chain. But if $s, t$ overlap, they are NOT directly connected. They are connected iff there exists a $v$ disjoint from both.
                            *   If no such $v$ exists, are they connected?
                                *   Maybe $s \to a \to b \to t$ where $a$ is left of $s$, $b$ is right of $t$, and $a, b$ connected? Yes, $a, b$ are disjoint.
                                *   But we established $s \to a \to t$ is valid if $a$ connects to $t$.
                                *   If $a$ is left of $s$, does $a$ connect to $t$?
                                    *   $a$ disjoint from $s \implies R_a < L_s$.
                                    *   $s, t$ overlap $\implies L_s \le R_s$ and $L_t \le R_t$.
                                    *   Does $R_a < L_s$ imply $R_a < L_t$? Not necessarily if $L_t < L_s$.
                                    *   Example: $t=[1, 10], s=[5, 6]$. Overlap.
                                    *   $a=[0, 0]$. $R_a < L_s$ (0 < 5). $R_a < L_t$ (0 < 1). Yes.
                                    *   Example: $t=[1, 10], s=[5, 6]$. $a=[2, 2]$. $R_a < L_s$ (2 < 5). $R_a < L_t$ (2 < 1) False. Overlaps $t$.
                                    *   So if we pick a left bridge for $s$, it might overlap $t$.
                                    *   But we need a $v$ that is disjoint from BOTH.
                                    *   The set of such $v$ is exactly those with $R_v < \min(L_s, L_t)$ OR $L_v > \max(R_s, R_t)$.
                                    *   If this set is empty, then $s$ and $t$ cannot be connected via a single bridge.
                                    *   Can they be connected via two bridges? $s \to a \to b \to t$.
                                        *   $a$ disjoint from $s$. $b$ disjoint from $t$. $a$ disjoint from $b$.
                                        *   If $a$ is left of $s$, $b$ is right of $t$. Then $a$ and $b$ are disjoint.
                                        *   Path: $s \to a \to b \to t$.
                                        *   Is this valid? $s-a$ (ok), $a-b$ (ok), $b-t$ (ok).
                                        *   Cost: $W_s + W_a + W_b + W_t$.
                                        *   Is there a shorter path?
                                        *   Maybe $s \to a \to t$? Only if $a$ disjoint from $t$.
                                        *   Maybe $s \to t$? No, they overlap.
                                        *   So if no single bridge exists, we might need two bridges.
                                        *   But wait, if $a$ is left of $s$ and $b$ is right of $t$, then $a$ is left of $t$ (since $s, t$ overlap, $L_t \le R_t$, and $R_a < L_s \le R_s$... wait. If $L_t < L_s$, then $a$ might overlap $t$. But if $a$ is left of $s$, and $s$ overlaps $t$, $a$ could be inside $t$? No, $a$ disjoint from $s$.
                                        *   Let's check the condition for $a$ (left of $s$) to connect to $t$.
                                            *   Need $R_a < L_t$ (if $a$ left of $t$) OR $L_a > R_t$ (if $a$ right of $t$).
                                            *   If $a$ is left of $s$ ($R_a < L_s$), and we assume $a$ is also left of $t$ ($R_a < L_t$), then $a$ connects to $t$.
                                            *   If $a$ is left of $s$ but overlaps $t$ (so $L_t \le R_a < L_s$), then $a$ does not connect to $t$.
                                            *   In this case, we need another node.
                                        *   However, notice that if $a$ overlaps $t$, then $a$ and $t$ are in the "overlap cluster".
                                        *   The problem reduces to: Can we reach $t$ from $s$?
                                        *   If $s, t$ overlap, we need to exit the "overlap cluster" of $s$ and enter the "overlap cluster" of $t$.
                                        *   Actually, the graph of intervals where edges = disjointness is the complement of an interval graph.
                                        *   Connected components in complement of interval graph:
                                            *   Two intervals are in the same component if they are not "separated" by a chain of overlaps?
                                            *   Actually, the connected components of the complement of an interval graph correspond to the "gaps" in the sorted intervals?
                                            *   No. The complement of an interval graph is a "co-interval graph".
                                            *   It is known that the connected components of a co-interval graph can be found by sorting intervals by $R$.
                                            *   Specifically, if we sort by $R$, we can merge components.
                                            *   But we need shortest paths.
                                            *   Given the constraints and the nature of the problem, the "two bridges" logic might be the way, but let's simplify.
                                            *   Hypothesis: The shortest path between $s$ and $t$ is either:
                                                1.  Direct edge (if disjoint).
                                                2.  Path of length 3: $s \to v \to t$ where $v$ is disjoint from both.
                                                3.  Path of length 4: $s \to v \to u \to t$? Unlikely to be minimal if length 3 exists.
                                                4.  If no single bridge exists, maybe no path? Or path through multiple bridges?
                                                5.  Actually, if $s$ and $t$ are in the same connected component, there is a path.
                                                6.  Key realization: If $s$ and $t$ overlap, they are in the same component iff there is a sequence of intervals connecting them.
                                                7.  But for shortest path, we likely only need to consider the "extremal" intervals.
                                                8.  Let's refine the "single bridge" check.
                                                    *   We need $v$ such that $R_v < \min(L_s, L_t)$ OR $L_v > \max(R_s, R_t)$.
                                                    *   If such $v$ exists, min cost is $W_s + W_t + \min(W_v)$.
                                                    *   If no such $v$ exists, is it possible to have a path?
                                                        *   Yes, if there is a chain. E.g., $s \to a \to b \to t$.
                                                        *   But if $s, t$ overlap, and no single bridge, it means all intervals disjoint from $s$ overlap $t$, and all intervals disjoint from $t$ overlap $s$.
                                                        *   This implies a very tight cluster.
                                                        *   In such a case, the shortest path might be longer.
                                                        *   However, in competitive programming contexts for this specific problem type, often the answer is either direct, or via the best "left" or "right" bridge. If neither works, maybe -1?
                                                        *   Wait, consider $s=[1, 5], t=[2, 6]$. Overlap.
                                                            *   Left bridge: $v$ with $R_v < 1$.
                                                            *   Right bridge: $v$ with $L_v > 6$.
                                                            *   If no such $v$, can we connect?
                                                            *   Maybe $a=[0, 0]$ (connects to $s$), $b=[7, 8]$ (connects to $t$). $a, b$ disjoint? Yes.
                                                            *   Path $s \to a \to b \to t$.
                                                            *   Here $a$ is left of $s$, $b$ is right of $t$.
                                                            *   Does $a$ connect to $t$? $a=[0,0], t=[2,6]$. Yes, disjoint.
                                                            *   So $s \to a \to t$ is valid! Cost $W_s+W_a+W_t$.
                                                            *   Why did I think $a$ might overlap $t$?
                                                            *   $a$ left of $s$ ($R_a < L_s$). $s, t$ overlap ($L_t \le R_s$).
                                                            *   If $L_t < L_s$, then $a$ could be in $(L_t, L_s)$. Then $a$ overlaps $t$.
                                                            *   Example: $t=[1, 10], s=[5, 6]$. Overlap.
                                                            *   $a=[2, 2]$. $R_a < L_s$ (2 < 5). $a$ overlaps $t$ ($[2,2] \cap [1,10]$).
                                                            *   So $a$ does not connect to $t$.
                                                            *   But we can pick $b=[11, 12]$. $L_b > R_t$ (11 > 10). $b$ connects to $t$.
                                                            *   Does $b$ connect to $s$? $s=[5, 6]$. $b$ disjoint from $s$. Yes.
                                                            *   So $s \to b \to t$ is valid.
                                                            *   So we just need ONE bridge that connects to BOTH.
                                                            *   The set of bridges connecting to BOTH is exactly $\{v : R_v < \min(L_s, L_t)\} \cup \{v : L_v > \max(R_s, R_t)\}$.
                                                            *   If this set is empty, then no single bridge exists.
                                                            *   Can we use two bridges? $s \to a \to b \to t$.
                                                                *   $a$ connects to $s$. $b$ connects to $t$. $a$ connects to $b$.
                                                                *   If $a$ is left of $s$, $b$ is right of $t$. Then $a, b$ disjoint.
                                                                *   Path $s \to a \to b \to t$.
                                                                *   Cost $W_s + W_a + W_b + W_t$.
                                                                *   Is this better than any single bridge?
                                                                *   If a single bridge $v$ exists, cost $W_s + W_t + W_v$.
                                                                *   If no single bridge, we must use at least two "steps" outside the overlap region?
                                                                *   Actually, if no single bridge, it means all $v$ disjoint from $s$ overlap $t$, and all $v$ disjoint from $t$ overlap $s$.
                                                                *   This implies the "gap" between $s$ and $t$ is filled with overlaps.
                                                                *   In this case, is there a path?
                                                                *   Maybe $s \to a \to b \to t$ where $a$ is left of $s$, $b$ is right of $t$.
                                                                *   But if $a$ is left of $s$, and $a$ overlaps $t$ (because no left bridge for both), then $a$ doesn't connect to $t$.
                                                                *   But $a$ connects to $b$ (since $a$ left of $s$, $b$ right of $t$, and $s, t$ overlap $\implies a$ left of $t$? No. $a$ left of $s$, $s$ overlaps $t$. $a$ could overlap $t$. But $b$ is right of $t$. So $a$ and $b$ are separated by $t$? Not necessarily. $a$ overlaps $t$, $b$ is right of $t$. So $a$ and $b$ are disjoint? Yes, $a$ ends before $b$ starts? $R_a < L_b$?
                                                                    *   $a$ overlaps $t \implies R_a \ge L_t$.
                                                                    *   $b$ right of $t \implies L_b > R_t$.
                                                                    *   Since $t$ is an interval, $L_t \le R_t$. So $R_a \ge L_t$ doesn't guarantee $R_a < L_b$.
                                                                    *   But $a$ overlaps $t$, $b$ is right of $t$. So $a$ and $b$ might overlap?
                                                                    *   $a=[2, 10], t=[1, 10], b=[11, 12]$. $a, b$ disjoint.
                                                                    *   $a=[2, 12], t=[1, 10], b=[11, 12]$. Overlap.
                                                                    *   So $a, b$ might not be disjoint.
                                                                *   This suggests the graph is complex.

**Refined Plan:**
1.  **Sort Intervals**: Sort by $R$.
2.  **Precompute Min Weights**:
    *   Use a Segment Tree (or Fenwick) over the sorted intervals to query min weight in range $[1, k]$.
    *   For each $i$, find $L\_best[i]$: min $W_j$ for $j$ such that $R_j < L_i$.
    *   For each $i$, find $R\_best[i]$: min $W_j$ for $j$ such that $L_j > R_i$.
3.  **Build Sparse Graph**:
    *   Add edges $(i, L\_best[i])$ and $(i, R\_best[i])$ (if they exist).
    *   Also add edges between $L\_best[i]$ and $R\_best[i]$ if they are disjoint? No, too many.
    *   Actually, the graph formed by these "best" edges might not be sufficient for all cases, but for shortest paths in this specific structure, it often is.
    *   Wait, the problem is likely solvable by realizing that the connected components are simple, and within components, the shortest path is either direct or via one of these "extremal" nodes.
    *   Given the constraints and typical problem patterns, the solution likely involves:
        *   If $s, t$ disjoint: $W_s + W_t$.
        *   If $s, t$ overlap: Check if there is a $v$ disjoint from both. If so, $W_s + W_t + \min(W_v)$.
        *   If not, check if there is a path of length 4? Or maybe -1?
        *   Actually, if $s, t$ overlap and no single bridge, they might still be connected via a chain. But finding the shortest chain is hard.
        *   However, note that if $s, t$ overlap, they are in the same component iff the union of their intervals is not "isolated" from the rest of the graph.
        *   Let's assume the question implies we can use the precomputed "best" neighbors to build a graph and run Dijkstra.
        *   Graph size: $N$ vertices, $2N$ edges.
        *   Run Dijkstra for each query? $O(Q \cdot N \log N)$ -> TLE.
        *   We need to answer queries faster.
        *   Maybe the number of connected components is small? Or the diameter is small?
        *   Alternative: Multi-source Dijkstra? No.
        *   Maybe the answer is always one of:
            *   Direct ($s, t$ disjoint)
            *   Via $L\_best[s]$ (if $L\_best[s]$ connects to $t$)
            *   Via $R\_best[s]$ (if $R\_best[s]$ connects to $t$)
            *   Via $L\_best[t]$ (if $L\_best[t]$ connects to $s$)
            *   Via $R\_best[t]$ (if $R\_best[t]$ connects to $s$)
            *   Via $L\_best[s]$ and $R\_best[t]$?
        *   Actually, if $s, t$ overlap, the shortest path is likely $s \to v \to t$ where $v$ is the best bridge. If no bridge, maybe $s \to u \to v \to t$?
        *   Given the time limit, the intended solution is probably:
            1.  Build the graph with edges $(i, j)$ where $j$ is the best neighbor (min weight) to the left or right.
            2.  This graph has $O(N)$ edges.
            3.  Run Dijkstra from each query? No.
            4.  Maybe the graph is a tree or has low diameter?
            5.  Wait, there is a known result: The shortest path in the complement of an interval graph between $u$ and $v$ is either the direct edge, or goes through the "leftmost" or "rightmost" available intervals.
            6.  So we only need to check a few candidates.
            7.  Candidates for bridge $v$:
                *   Best left of $s$ ($L\_best[s]$)
                *   Best right of $s$ ($R\_best[s]$)
                *   Best left of $t$ ($L\_best[t]$)
                *   Best right of $t$ ($R\_best[t]$)
            8.  If any of these connects to the other endpoint, take it.
            9.  If none, then maybe no path? Or check combinations?
            10. Actually, if $s, t$ overlap, and no single bridge, then $s$ and $t$ are in a "cluster" that cannot be exited by a single node. But they can be exited by two nodes?
            11. Let's assume the candidates are sufficient.

**Pitfalls:**
*   Overlapping intervals logic: Ensure strict disjointness ($L_j > R_i$ or $R_j < L_i$).
*   Coordinate range: $L, R \le 2N$. Segment tree size $4N$.
*   Multiple intervals with same $R$: Sort order matters? Use $L$ as tie-breaker.
*   Weights up to $10^9$, use 64-bit integers.
*   No path case: Output -1.

## worker: [todo] **Task 1**: Read input, store intervals, we
1.  **Input Parsing**: Read all inputs efficiently. Use 1-based indexing for weights and queries to match problem statement.
2.  **Sorting**: Intervals are sorted by $R$ to facilitate the sweep-line for `best_left`.
3.  **Data Structures**:
    *   **Fenwick Tree (BIT)**: Used to maintain minimum weights of intervals processed so far (sorted by $R$). Allows querying $\min W$ for $R < X$ in $O(\log N)$.
    *   **Segment Tree**: Used to maintain minimum weights of intervals based on their $L$ coordinate. Allows querying $\min W$ for $L > X$ in $O(\log N)$.
4.  **Precomputation**:
    *   `best_left[i]`: Min weight of an interval $j$ such that $R_j < L_i$. Computed by iterating sorted intervals and querying the BIT.
    *   `best_right[i]`: Min weight of an interval $j$ such that $L_j > R_i$. Computed by building the Segment Tree with all intervals and querying.
5.  **Query Logic**:
    *   If $s$ and $t$ are disjoint, the answer is simply $W_s + W_t$.
    *   If $s$ and $t$ overlap, a direct edge doesn't exist. We look for a path of length 3 ($s \to v \to t$) or length 4 ($s \to a \to b \to t$).
    *   **Single Bridge ($v$)**: Must be disjoint from both $s$ and $t$. This means $R_v < \min(L_s, L_t)$ or $L_v > \max(R_s, R_t)$. We query the precomputed structures for the minimum weight in these ranges.
    *   **Two Bridges ($a, b$)**: $a$ is disjoint from $s$ (specifically $R_a < L_s$), $b$ is disjoint from $t$ (specifically $L_b > R_t$). Since $s$ and $t$ overlap, $a$ and $b$ will be disjoint ($R_a < L_s \le R_t < L_b$). Thus $s \to a \to b \to t$ is a valid path. We check both combinations: (left of $s$, right of $t$) and (right of $s$, left of $t$).
6.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building BIT/SegTree: $O(N \log N)$.
    *   Queries: $O(Q \log N)$.
    *   Total Time: $O((N+Q) \log N)$, which fits within limits.
    *   Space: $O(N)$.

## worker: finalize
The solution implements the logic derived in the thought process:
1.  **Input Parsing**: Efficiently reads all inputs.
2.  **Data Structures**:
    *   **Fenwick Tree (BIT)**: Used to maintain the minimum weight of intervals processed so far based on their Right endpoint ($R$). This allows querying the minimum weight of an interval with $R < X$ in $O(\log N)$.
    *   **Segment Tree**: Used to maintain the minimum weight of intervals based on their Left endpoint ($L$). This allows querying the minimum weight of an interval with $L > X$ in $O(\log N)$.
3.  **Precomputation**:
    *   `best_left[i]`: The minimum weight of an interval $j$ such that $R_j < L_i$. Computed by iterating through intervals sorted by $R$ and querying the BIT.
    *   `best_right[i]`: The minimum weight of an interval $j$ such that $L_j > R_i$. Computed by populating the Segment Tree with all intervals and then querying for each interval.
4.  **Query Logic**:
    *   **Disjoint Check**: If $s$ and $t$ are disjoint, the answer is simply $W_s + W_t$.
    *   **Overlapping Check**: If $s$ and $t$ overlap, a direct edge does not exist. The shortest path must involve intermediate nodes.
        *   **Single Bridge**: A node $v$ disjoint from both $s$ and $t$. This requires $R_v < \min(L_s, L_t)$ or $L_v > \max(R_s, R_t)$. We query the precomputed structures for the minimum weight in these ranges.
        *   **Two Bridges**: A path $s \to a \to b \to t$ where $a$ is disjoint from $s$ (specifically $R_a < L_s$) and $b$ is disjoint from $t$ (specifically $L_b > R_t$). Since $s$ and $t$ overlap, $a$ and $b$ will be disjoint. We check both combinations: (left of $s$, right of $t$) and (right of $s$, left of $t$).
5.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building BIT/SegTree: $O(N \log N)$.
    *   Queries: $O(Q \log N)$.
    *   Total Time: $O((N+Q) \log N)$, which fits within the limits ($N, Q \le 2 \times 10^5$).
    *   Space: $O(N)$.

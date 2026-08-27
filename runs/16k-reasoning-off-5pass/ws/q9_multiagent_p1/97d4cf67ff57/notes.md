
## ideation
**Core Difficulty:**
The problem requires finding a maximum size connected subgraph of a tree where every node has degree 1 or 4, and at least one node has degree 4. This structure is essentially a "spider" or "star-like" graph where a central clique of degree-4 nodes is connected by paths of degree-2 nodes (which are not allowed in the final subgraph) to leaves of degree 1. Wait, the definition says "Every vertex has degree 1 or 4". In a tree, if a node has degree 4 in the subgraph, it must have 4 neighbors in the subgraph. If it has degree 1, it has 1 neighbor. There are no degree 2 or 3 nodes allowed.
This implies the subgraph cannot have long paths of intermediate nodes. If we have $u - v - w$, then $v$ has degree 2, which is forbidden. Therefore, the subgraph must be a collection of "stars" (a central node connected to leaves) or a more complex structure where degree-4 nodes are directly connected to each other or to leaves.
Actually, if two degree-4 nodes are connected ($u-v$), both have degree at least 1. If they are connected to other nodes, their degrees increase.
Let's re-evaluate the structure. Since it's a tree and max degree is 4, min degree is 1.
Possible local structures:
1. A single node with degree 1? No, must have at least one degree 4.
2. A single node with degree 4 connected to 4 leaves. (Total 5 nodes).
3. Two degree-4 nodes connected to each other. Each needs 3 more neighbors. If those neighbors are leaves, total nodes = 2 + 3 + 3 = 8.
4. A chain of degree-4 nodes? $u-v-w$. $u$ needs 3 more, $w$ needs 3 more. $v$ needs 2 more (since it's connected to $u$ and $w$). Total 2 neighbors for $v$. So $v$ has degree 4.
So the subgraph is a "tree of stars" where the "centers" are degree 4 nodes and the "leaves" of the whole structure are degree 1 nodes. Crucially, there are **no** nodes of degree 2 or 3 in the subgraph. This means any path between two degree-4 nodes in the subgraph must be a direct edge. You cannot have $u - x - v$ where $u, v$ are degree 4, because $x$ would have degree 2.
Thus, the subgraph consists of a set of degree-4 nodes forming a connected component (where every edge in this component connects two degree-4 nodes), and each degree-4 node is attached to some number of degree-1 leaves.
Let $S$ be the set of degree-4 nodes in the subgraph. The induced subgraph on $S$ must be a tree (since the whole subgraph is a tree). For every $u \in S$, $deg_{sub}(u) = 4$. Since $u$ is connected to other nodes in $S$ (say $k_u$ neighbors) and leaves (say $l_u$ neighbors), we must have $k_u + l_u = 4$.
The total size of the subgraph is $\sum_{u \in S} (1 + l_u) = |S| + \sum l_u$.
Since $l_u = 4 - k_u$, Total Size = $\sum_{u \in S} (1 + 4 - k_u) = 5|S| - \sum_{u \in S} k_u$.
Note that $\sum_{u \in S} k_u = 2 \times (\text{number of edges within } S)$. Since $S$ induces a tree, if $|S| \ge 2$, edges = $|S|-1$. If $|S|=1$, edges=0.
Case 1: $|S| = 1$. Size = $5(1) - 0 = 5$. (One center, 4 leaves).
Case 2: $|S| \ge 2$. Size = $5|S| - 2(|S|-1) = 5|S| - 2|S| + 2 = 3|S| + 2$.
So the problem reduces to: Find a connected subset of vertices $S$ in the original tree $T$ such that:
1. For every $u \in S$, we can attach exactly $4 - deg_S(u)$ leaves from $T \setminus S$ adjacent to $u$.
2. The leaves attached must be distinct and available in $T$.
3. $S$ must induce a connected subgraph (a tree) in $T$.
4. $|S| \ge 1$.

Wait, the condition "attach leaves" means that for each $u \in S$, we need to pick $4 - deg_S(u)$ neighbors of $u$ in $T$ that are NOT in $S$. These neighbors become degree-1 nodes in the subgraph.
So, for a candidate set $S$:
- $S$ must be connected in $T$.
- For each $u \in S$, let $d_T(u)$ be the degree of $u$ in $T$, and $d_S(u)$ be the degree of $u$ in the subgraph induced by $S$.
- We need $d_T(u) \ge d_S(u) + (4 - d_S(u)) = 4$.
- So, every node $u \in S$ must have degree at least 4 in the original tree $T$.
- Additionally, we need enough "free" neighbors. Specifically, for each $u$, we need to select $4 - d_S(u)$ neighbors from $N(u) \setminus S$. This is possible if and only if $|N(u) \setminus S| \ge 4 - d_S(u) \iff d_T(u) - d_S(u) \ge 4 - d_S(u) \iff d_T(u) \ge 4$.
- So the condition simplifies to: **Every node in $S$ must have degree $\ge 4$ in $T$.**
- And $S$ must be connected.
- And we want to maximize $3|S| + 2$ (if $|S| \ge 2$) or $5$ (if $|S|=1$).
- Note: If we find a connected component of nodes with degree $\ge 4$, say of size $k$, can we always form an alkane?
  - If $k=1$, size 5.
  - If $k \ge 2$, size $3k+2$.
  - Is it possible that we can't form the edges? No, because we just pick any $4 - d_S(u)$ neighbors. Since $d_T(u) \ge 4$ and $d_S(u)$ is the number of neighbors in $S$, the number of available neighbors outside is $d_T(u) - d_S(u) \ge 4 - d_S(u)$. So we can always pick the required number.
  - Are the leaves distinct? Yes, because leaves are neighbors of $u$ not in $S$. Since $S$ is the set of degree-4 nodes, leaves are not in $S$. Could a leaf be a neighbor of two different $u, v \in S$? No, because if $w$ is a neighbor of both $u$ and $v$, and $w \notin S$, then in the subgraph $w$ would have degree 2 (connected to $u$ and $v$), which is forbidden.
  - Therefore, we must ensure that no node outside $S$ is connected to more than one node in $S$.
  - This is the critical constraint! We cannot simply pick any connected set of nodes with degree $\ge 4$. The "branches" extending from $S$ must not merge outside $S$.
  - Actually, if $w \notin S$ is connected to $u \in S$ and $v \in S$, then in the subgraph, $w$ has degree 2. This is invalid.
  - So, the subgraph structure is: $S$ (degree 4 nodes) connected directly to leaves. No paths of length 2 involving a leaf.
  - This implies that if we select $S$, then for any $w \notin S$, $w$ can be adjacent to at most one node in $S$.
  - But wait, the subgraph is formed by $S$ and a subset of $N(S)$. If $w \in N(S)$ is used as a leaf for $u$, it cannot be used for $v$.
  - So we need to select $S$ (connected, all $deg_T(u) \ge 4$) and assign each $u \in S$ a set of $4 - d_S(u)$ neighbors from $N(u) \setminus S$, such that all assigned neighbors are distinct.
  - This looks like a matching problem or flow, but on a tree, maybe simpler.
  - However, consider the structure of $T$. If $S$ is a connected component of high-degree nodes, and there is a node $w$ adjacent to two nodes in $S$, we cannot use $w$ as a leaf for either. We just ignore $w$.
  - So the constraint is: We need to find a connected subgraph $S$ where every $u \in S$ has $deg_T(u) \ge 4$, and we can satisfy the leaf requirements.
  - The leaf requirement for $u$ is $4 - d_S(u)$. The available leaves are neighbors in $T \setminus S$.
  - Total needed leaves = $\sum_{u \in S} (4 - d_S(u)) = 4|S| - 2(|S|-1) = 2|S| + 2$ (for $|S| \ge 2$).
  - Total available neighbors in $T \setminus S$ is $\sum_{u \in S} (deg_T(u) - d_S(u)) = \sum deg_T(u) - 2(|S|-1)$.
  - We need to select distinct neighbors. This is possible if and only if the bipartite graph between $S$ and $N(S) \setminus S$ has a matching that covers the required degree deficits?
  - Actually, since the graph is a tree, if $w$ is adjacent to $u_1, u_2 \in S$, $w$ is a "bridge" between parts of $S$. But $S$ is connected, so $u_1, u_2$ are connected within $S$. $w$ is an extra connection.
  - If such a $w$ exists, it's just "wasted" potential. We don't have to use it. We just need to ensure we have *enough* distinct neighbors.
  - Is it possible that we don't have enough distinct neighbors?
    - Suppose $S = \{u, v\}$ connected by edge $(u,v)$. $d_S(u)=1, d_S(v)=1$. Need 3 leaves for $u$, 3 for $v$. Total 6 leaves.
    - Available: neighbors of $u$ excluding $v$, neighbors of $v$ excluding $u$.
    - If $u$ and $v$ share a common neighbor $w$ (other than each other), then $w$ is in both sets. We can use $w$ for $u$ but not $v$.
    - So we lose 1 potential leaf.
    - Generally, the number of distinct neighbors available is $|N(S) \setminus S|$.
    - We need $|N(S) \setminus S| \ge \sum (4 - d_S(u)) = 2|S| + 2$.
    - We know $\sum (deg_T(u) - d_S(u)) = \sum deg_T(u) - 2|S| + 2$.
    - The number of distinct neighbors is $\sum (deg_T(u) - d_S(u)) - (\text{number of edges within } N(S) \setminus S \text{ that connect to } S \text{ twice?})$.
    - Actually, in a tree, there are no cycles. If $w$ is adjacent to $u_1, u_2 \in S$, then the path $u_1 - w - u_2$ combined with the path in $S$ between $u_1, u_2$ forms a cycle. But $T$ is a tree, so this is impossible unless $u_1=u_2$.
    - **Crucial Insight**: In a tree, a node $w$ cannot be adjacent to two distinct nodes $u, v$ in a connected subgraph $S$ without creating a cycle?
      - Let's trace: $u, v \in S$. Path in $S$ between $u, v$ exists. If $w$ is adjacent to $u$ and $v$, then $u-w-v$ is a path. Combined with path in $S$, we get a cycle.
      - Since $T$ is a tree, no cycles exist.
      - Therefore, **no node outside $S$ can be adjacent to more than one node in $S$**.
      - This simplifies everything immensely!
      - The sets of neighbors $N(u) \setminus S$ for $u \in S$ are **disjoint**.
      - Thus, the number of available distinct leaves is exactly $\sum_{u \in S} (deg_T(u) - d_S(u))$.
      - We need this sum to be $\ge \sum_{u \in S} (4 - d_S(u))$.
      - $\sum (deg_T(u) - d_S(u)) \ge \sum (4 - d_S(u))$
      - $\sum deg_T(u) - \sum d_S(u) \ge 4|S| - \sum d_S(u)$
      - $\sum_{u \in S} deg_T(u) \ge 4|S|$
      - So the condition is simply: **Find a connected subgraph $S$ such that every $u \in S$ has $deg_T(u) \ge 4$, and $\sum_{u \in S} deg_T(u) \ge 4|S|$.**
      - Wait, if every $u \in S$ has $deg_T(u) \ge 4$, then $\sum deg_T(u) \ge 4|S|$ is automatically satisfied.
      - So the only constraints are:
        1. $S$ is a connected subgraph of $T$.
        2. For all $u \in S$, $deg_T(u) \ge 4$.
        3. $|S| \ge 1$.
      - If such an $S$ exists, the max size is $\max(5, 3|S|+2)$.
      - Since $3|S|+2$ is increasing with $|S|$, and for $|S|=1$ it gives 5, for $|S| \ge 2$ it gives $\ge 8$.
      - So we just need to find the largest connected component consisting entirely of nodes with degree $\ge 4$.
      - Let $G'$ be the subgraph induced by vertices with $deg_T(v) \ge 4$.
      - Find the largest connected component in $G'$. Let its size be $K$.
      - If $K=0$, output -1.
      - If $K=1$, output 5.
      - If $K \ge 2$, output $3K + 2$.

**Verification with Sample 1:**
Nodes: 1..9.
Edges: (1,2), (2,3), (3,4), (4,5), (2,6), (2,7), (3,8), (3,9).
Degrees in T:
1: 1
2: 4 (1,3,6,7) -> OK
3: 4 (2,4,8,9) -> OK
4: 2 (3,5)
5: 1
6: 1
7: 1
8: 1
9: 1
Nodes with deg >= 4: {2, 3}.
Are they connected? Yes, edge (2,3).
Component size K=2.
Result: $3(2) + 2 = 8$. Matches sample output.

**Verification with Sample 2:**
Tree: 1-2, 1-3, 2-4, 2-5, 3-6, 3-7.
Degrees:
1: 2
2: 3
3: 3
4,5,6,7: 1
No node has degree >= 4.
K=0. Output -1. Matches sample.

**Verification with Sample 3:**
Input:
15
8 5
2 9
1 12
6 11
9 3
15 1
7 12
7 13
10 5
6 9
5 1
1 9
4 5
6 14

Let's compute degrees:
Edges:
(8,5), (2,9), (1,12), (6,11), (9,3), (15,1), (7,12), (7,13), (10,5), (6,9), (5,1), (1,9), (4,5), (6,14)
List:
1: 12, 15, 5, 9 -> deg 4
2: 9 -> deg 1
3: 9 -> deg 1
4: 5 -> deg 1
5: 8, 10, 1, 4 -> deg 4
6: 11, 9, 14 -> deg 3
7: 12, 13 -> deg 2
8: 5 -> deg 1
9: 2, 3, 6, 1 -> deg 4
10: 5 -> deg 1
11: 6 -> deg 1
12: 1, 7 -> deg 2
13: 7 -> deg 1
14: 6 -> deg 1
15: 1 -> deg 1

Nodes with deg >= 4: {1, 5, 9}.
Check connectivity:
1 is connected to 9 (edge 1-9).
5 is connected to 1 (edge 5-1).
So {1, 5, 9} form a connected component.
Size K=3.
Result: $3(3) + 2 = 11$. Matches sample.

**Algorithm:**
1. Read N.
2. Read edges, build adjacency list.
3. Compute degree of each node.
4. Identify nodes with degree >= 4.
5. Find connected components among these nodes using BFS/DFS/Union-Find.
6. Find the maximum size of such a component, say $K$.
7. If no such component ($K=0$), print -1.
8. Else if $K=1$, print 5.
9. Else ($K \ge 2$), print $3K + 2$.

**Complexity:**
- Building graph: $O(N)$.
- Computing degrees: $O(N)$.
- Finding components: $O(N)$ (visit each node/edge once).
- Total time: $O(N)$. Space: $O(N)$.
- Constraints $N \le 2 \times 10^5$, fits easily.

**Edge Cases:**
- N < 5: Impossible to have a node with degree 4. Output -1. (Logic holds: max degree < 4).
- Only 1 node with deg >= 4: Output 5.
- Multiple components: Take max.

This seems solid. The key insight was that in a tree, a node outside the core cannot connect to two nodes in the core without forming a cycle, ensuring disjointness of potential leaves.

## worker: Write the Python code implementing the logic: Pars
The problem asks for the maximum size of a subgraph that is an "alkane" (a tree where every node has degree 1 or 4, and at least one node has degree 4).
Key insights derived:
1.  **Structure of Alkane**: An alkane subgraph consists of a set of "core" nodes (degree 4) and "leaf" nodes (degree 1). There are no nodes of degree 2 or 3.
2.  **Tree Constraint**: Since the original graph is a tree, any two core nodes in the subgraph must be connected directly or via other core nodes. If a leaf node were connected to two core nodes, it would form a cycle (core1 - leaf - core2 - ... - core1), which is impossible in a tree. Thus, the sets of leaves attached to each core node are disjoint.
3.  **Degree Requirement**: For a node $u$ to be a core node in the subgraph, it must have degree 4 in the subgraph. This means it must have 4 neighbors in the subgraph. Since it can only connect to other core nodes or leaves, and we established leaves are disjoint, $u$ must have at least 4 neighbors in the original tree $T$.
4.  **Connectivity**: The set of core nodes $S$ must form a connected subgraph in $T$.
5.  **Simplification**: The problem reduces to finding the largest connected component in the subgraph induced by vertices with degree $\ge 4$ in $T$.
    - If no such vertices exist, output -1.
    - If the largest component has size $K=1$, the max alkane size is 5 (1 core + 4 leaves).
    - If $K \ge 2$, the max alkane size is $3K + 2$. This is derived from: Total nodes = $K$ (core) + $\sum (4 - \text{degree in } S)$. Since $S$ is a tree, $\sum \text{degree in } S = 2(K-1)$. Total = $K + 4K - 2K + 2 = 3K + 2$.

The algorithm:
1.  Parse input and build adjacency list.
2.  Calculate degrees of all nodes.
3.  Filter nodes with degree $\ge 4$.
4.  Run BFS/DFS to find the size of the largest connected component consisting solely of these filtered nodes.
5.  Apply the formula based on the component size.

## worker: Run the code against the provided sample inputs to
The code implements the logic derived:
1.  **Input Parsing**: Reads $N$ and the tree edges.
2.  **Degree Calculation**: Computes the degree of each vertex in the original tree.
3.  **Filtering**: Identifies vertices with degree $\ge 4$.
4.  **Component Analysis**: Uses BFS to find the size of the largest connected component formed *only* by these high-degree vertices.
5.  **Result Calculation**:
    *   If no high-degree vertices exist, output -1.
    *   If the largest component has size 1, output 5 (1 core + 4 leaves).
    *   If the largest component has size $K \ge 2$, output $3K + 2$.

This logic holds because in a tree, a node outside the core cannot connect to two core nodes without creating a cycle. Thus, the "leaves" attached to the core are disjoint, and the maximum size is determined solely by the size of the connected core.

## worker: finalize
The problem asks for the maximum size of a subgraph of a given tree $T$ that satisfies the "alkane" property: every vertex has degree 1 or 4, and at least one vertex has degree 4.

**Key Insight:**
1.  **Structure**: An alkane subgraph consists of a set of "core" nodes (degree 4) and "leaf" nodes (degree 1). There are no nodes of degree 2 or 3.
2.  **Tree Constraint**: Since the original graph is a tree, any two core nodes in the subgraph must be connected directly or via other core nodes. If a leaf node were connected to two core nodes, it would form a cycle (core1 - leaf - core2 - ... - core1), which is impossible in a tree. Thus, the sets of leaves attached to each core node are disjoint.
3.  **Degree Requirement**: For a node $u$ to be a core node in the subgraph, it must have degree 4 in the subgraph. This means it must have 4 neighbors in the subgraph. Since it can only connect to other core nodes or leaves, and we established leaves are disjoint, $u$ must have at least 4 neighbors in the original tree $T$.
4.  **Connectivity**: The set of core nodes $S$ must form a connected subgraph in $T$.
5.  **Simplification**: The problem reduces to finding the largest connected component in the subgraph induced by vertices with degree $\ge 4$ in $T$.
    *   If no such vertices exist, output -1.
    *   If the largest component has size $K=1$, the max alkane size is 5 (1 core + 4 leaves).
    *   If $K \ge 2$, the max alkane size is $3K + 2$. This is derived from: Total nodes = $K$ (core) + $\sum (4 - \text{degree in } S)$. Since $S$ is a tree, $\sum \text{degree in } S = 2(K-1)$. Total = $K + 4K - 2K + 2 = 3K + 2$.

**Algorithm:**
1.  Parse input and build adjacency list.
2.  Calculate degrees of all nodes.
3.  Filter nodes with degree $\ge 4$.
4.  Run BFS/DFS to find the size of the largest connected component consisting solely of these filtered nodes.
5.  Apply the formula based on the component size.

**Complexity:**
-   Building graph: $O(N)$.
-   Computing degrees: $O(N)$.
-   Finding components: $O(N)$ (visit each node/edge once).
-   Total time: $O(N)$. Space: $O(N)$.
-   Constraints $N \le 2 \times 10^5$, fits easily.

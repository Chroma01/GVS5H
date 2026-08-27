
## ideation
**Core Difficulty**:
The problem requires finding a subgraph of a tree $T$ that satisfies specific degree constraints (all nodes degree 1 or 4, at least one degree 4 node). This structure implies the subgraph consists of a connected "core" of degree-4 nodes, where each core node is connected to exactly 4 other nodes in the subgraph. Since the subgraph is a tree, these connections to other nodes must either be:
1. Connections to other degree-4 nodes (forming the core).
2. Connections to degree-1 nodes (leaves).
Crucially, a degree-4 node in the subgraph cannot connect to a path of intermediate nodes; if it did, the intermediate nodes would need degrees 2 (which is forbidden) or 1 (which would make them leaves, but then the degree-4 node would only have 1 connection to that branch). Thus, every neighbor of a degree-4 node in the subgraph must be either another degree-4 node or a leaf.
This means the "core" is a connected component of vertices where each vertex has degree 4 within the subgraph. The rest of the vertices attached to this core are leaves.
Wait, re-reading the definition: "Every vertex has degree 1 or 4".
If a vertex $u$ is in the subgraph and has degree 4, it has 4 neighbors in the subgraph.
If a vertex $v$ is in the subgraph and has degree 1, it has 1 neighbor in the subgraph.
There are no vertices of degree 2 or 3 allowed.
This implies the subgraph is a collection of "stars" connected together? No, if two degree-4 nodes are connected, they use 1 degree each. If they are connected by a path of length 2, the middle node must have degree 2, which is forbidden.
**Conclusion**: The subgraph cannot contain any path of length $\ge 2$ between two degree-4 nodes. The distance between any two degree-4 nodes in the subgraph must be exactly 1 (they are adjacent).
Therefore, the set of degree-4 nodes must form a connected component (a clique in terms of adjacency, but since it's a tree, it's just a connected subgraph where every edge connects two degree-4 nodes). Let this set be $C$.
For every $u \in C$, $u$ needs 4 neighbors in the subgraph. Some neighbors are in $C$, some are leaves.
Since the subgraph is a tree, the subgraph induced by $C$ must be a tree itself.
Let $d_C(u)$ be the degree of $u$ within the subgraph induced by $C$. Then $u$ needs $4 - d_C(u)$ leaf neighbors.
Since the original graph is a tree, the neighbors of $u$ in the original graph are partitioned into those in $C$ and those not in $C$. The neighbors not in $C$ must be chosen to be leaves.
However, we can't just pick any neighbor to be a leaf. If we pick a neighbor $v \notin C$ to be a leaf, $v$ must have degree 1 in the subgraph. This means $v$ cannot have any other neighbors in the subgraph. Since $v$ is connected to $u$, $v$ cannot be connected to any other node in the subgraph. This is always possible if we simply select $v$ and stop there.
So, for a fixed set $C$ of degree-4 nodes forming a connected subgraph in $T$:
For each $u \in C$, let $k_u$ be the number of neighbors of $u$ that are also in $C$.
The number of leaves attached to $u$ must be $4 - k_u$.
We need $4 - k_u \ge 0$ for all $u \in C$.
Also, we need to ensure that the leaves we pick are distinct and available in $T$. Since $T$ is a tree, the neighbors of $u$ are distinct. If we pick a neighbor $v \notin C$ to be a leaf, we just include $v$ in the subgraph. We don't need to worry about $v$ connecting to anything else because we are defining the subgraph.
The total number of vertices is $|C| + \sum_{u \in C} (4 - d_C(u)) = |C| + 4|C| - 2|E_C| = 5|C| - 2|E_C|$, where $E_C$ are edges within $C$.
Wait, is it possible that picking a leaf $v$ for $u$ conflicts with picking $v$ for $w$? No, because $T$ is a tree, $v$ has only one neighbor in the subgraph (which is $u$). If $v$ were connected to $w$ as well, $v$ would have degree 2, which is forbidden. But in a tree, $v$ is only adjacent to $u$ and $w$ if $u, v, w$ form a path. If $v$ is a leaf attached to $u$, it cannot be attached to $w$.
So the constraint is simply: For each $u \in C$, we need at least $4 - d_C(u)$ neighbors of $u$ in $T \setminus C$.
And we want to maximize $5|C| - 2|E_C|$.
Note that $C$ must be connected.
Also, there is a global constraint: at least one node of degree 4, so $|C| \ge 1$.
Actually, the formula $5|C| - 2|E_C|$ assumes we can always find enough leaves.
For a specific $u$, we need $4 - d_C(u)$ leaves. These leaves must come from the neighbors of $u$ in $T$ that are not in $C$.
Let $deg_T(u)$ be the degree of $u$ in the original tree.
The number of available neighbors outside $C$ is $deg_T(u) - d_C(u)$.
We need $deg_T(u) - d_C(u) \ge 4 - d_C(u) \implies deg_T(u) \ge 4$.
So, a necessary condition for $u \in C$ is that $deg_T(u) \ge 4$.
If $deg_T(u) < 4$, $u$ cannot be a degree-4 node in the subgraph because it doesn't have enough neighbors in $T$ to satisfy the degree 4 requirement (even if all its neighbors in $T$ are in the subgraph, it can't exceed $deg_T(u)$).
Wait, if $u$ is in $C$, its degree in the subgraph is 4. This requires 4 distinct neighbors in the subgraph. These neighbors must be in $T$. So $u$ must have at least 4 neighbors in $T$.
Thus, any node in $C$ must have $deg_T(u) \ge 4$.
If $deg_T(u) = 4$, then all neighbors of $u$ in $T$ must be in $C$.
If $deg_T(u) > 4$, then $u$ can have some neighbors in $C$ and some leaves.
So the problem reduces to:
Find a connected subgraph $C$ such that for all $u \in C$, $deg_T(u) \ge 4$.
Maximize $5|C| - 2|E_C|$.
Note that $5|C| - 2|E_C| = 3|C| + (2|C| - 2|E_C|) = 3|C| + 2(|C| - |E_C|) = 3|C| + 2 \times (\text{number of connected components in } C)$.
Since $C$ must be connected, number of components is 1.
So we maximize $3|C| + 2 = 3|C| + 2$.
Wait, let's re-evaluate.
Total vertices = $|C| + \sum (4 - d_C(u)) = |C| + 4|C| - \sum d_C(u) = 5|C| - 2|E_C|$.
Since $C$ is a tree (subgraph of a tree), $|E_C| = |C| - 1$.
Total vertices = $5|C| - 2(|C| - 1) = 5|C| - 2|C| + 2 = 3|C| + 2$.
This is interesting. The size depends only on $|C|$.
So we just need to find the largest connected subgraph $C$ such that:
1. Every $u \in C$ has $deg_T(u) \ge 4$.
2. There exists at least one $u \in C$ with $deg_T(u) = 4$? No, the condition is just that the subgraph is an alkane. The definition says "at least one vertex of degree 4". Since all vertices in $C$ have degree 4 in the subgraph, as long as $|C| \ge 1$, this condition is met.
Wait, is it possible that for some $u \in C$, we cannot find enough leaves?
We established: need $deg_T(u) \ge 4$.
If $deg_T(u) \ge 4$, we have $deg_T(u)$ neighbors. $d_C(u)$ are in $C$. The remaining $deg_T(u) - d_C(u)$ are candidates for leaves.
We need to pick $4 - d_C(u)$ leaves.
Condition: $deg_T(u) - d_C(u) \ge 4 - d_C(u) \iff deg_T(u) \ge 4$.
So yes, the only constraint is $deg_T(u) \ge 4$ for all $u \in C$.
And $C$ must be connected.
So the problem is simply: Find the maximum size of a connected subgraph consisting only of nodes with degree $\ge 4$ in the original tree.
Let $S = \{u \mid deg_T(u) \ge 4\}$.
We want to find the largest connected component in the subgraph induced by $S$.
Let this max size be $K$.
If $S$ is empty, output -1.
If $K \ge 1$, the answer is $3K + 2$.

Let's double check with Sample 1.
Nodes: 1..9.
Edges: (1,2), (2,3), (3,4), (4,5), (2,6), (2,7), (3,8), (3,9).
Degrees:
1: 1
2: 4 (1,3,6,7) -> $\ge 4$
3: 4 (2,4,8,9) -> $\ge 4$
4: 2 (3,5)
5: 1
6: 1
7: 1
8: 1
9: 1
Set $S = \{2, 3\}$.
Connected components in $S$: $\{2, 3\}$ is connected (edge 2-3 exists). Size $K=2$.
Answer: $3(2) + 2 = 8$.
Sample output is 8. Matches.

Sample 2:
7 nodes.
Edges: (1,2), (1,3), (2,4), (2,5), (3,6), (3,7).
Degrees:
1: 2
2: 3
3: 3
4: 1
5: 1
6: 1
7: 1
Set $S = \emptyset$.
Output -1. Matches.

Sample 3:
15 nodes.
Edges: (8,5), (2,9), (1,12), (6,11), (9,3), (15,1), (7,12), (7,13), (10,5), (6,9), (5,1), (1,9), (4,5), (6,14).
Let's compute degrees.
1: (12, 15, 5, 9) -> 4
2: (9) -> 1
3: (9) -> 1
4: (5) -> 1
5: (8, 10, 1, 4) -> 4 (Wait, 5-1 is listed, 5-8, 5-10, 5-4. That's 4.)
6: (11, 9, 14) -> 3
7: (12, 13) -> 2
8: (5) -> 1
9: (2, 3, 6, 1) -> 4
10: (5) -> 1
11: (6) -> 1
12: (1, 7) -> 2
13: (7) -> 1
14: (6) -> 1
15: (1) -> 1
Set $S = \{1, 5, 9\}$.
Check connectivity in $S$:
Edges in original tree between nodes in $S$:
(1, 9) exists? Yes.
(5, 9)? No direct edge.
(1, 5)? Yes (5,1).
So 1-5 and 1-9. The component is $\{1, 5, 9\}$. Size $K=3$.
Answer: $3(3) + 2 = 11$.
Sample output is 11. Matches.

Logic seems solid.
Algorithm:
1. Read input, build adjacency list.
2. Compute degrees of all nodes.
3. Identify nodes with degree $\ge 4$.
4. Find the size of the largest connected component formed by these nodes.
   - We can use BFS/DFS or Union-Find.
   - Iterate over all nodes with degree $\ge 4$. If not visited, start traversal counting nodes, only moving to neighbors that also have degree $\ge 4$.
5. If no such nodes, print -1.
6. Else, print $3 \times \text{max\_size} + 2$.

Complexity: $O(N)$ time, $O(N)$ space. Constraints $N \le 2 \times 10^5$, feasible.

Pitfalls:
- Forgetting the "at least one vertex of degree 4" condition. If max_size >= 1, this is satisfied. If max_size == 0, output -1.
- Miscounting degrees.
- Not handling disconnected components correctly (only considering the component of nodes with deg >= 4).
- The formula $3K+2$ derivation:
  Vertices = $K$ (core) + Leaves.
  Each core node $u$ has degree 4 in subgraph.
  Edges in subgraph: $K-1$ (internal) + Leaves.
  Sum of degrees = $4K$.
  Sum of degrees = $2 \times (K-1) + 2 \times (\text{number of leaf edges})$.
  Wait, leaf edges are edges connecting core to leaves.
  Let $L$ be number of leaves.
  Sum of degrees = $4K = 2(K-1) + L$. (Internal edges count 2, leaf edges count 1 for core node, 1 for leaf).
  $L = 4K - 2K + 2 = 2K + 2$.
  Total vertices = $K + L = 3K + 2$.
  Correct.

One edge case: What if the "core" is just a single node?
$K=1$. $L = 4(1) - 2(0) = 4$. Total = 5.
Formula: $3(1)+2 = 5$. Correct.
The node must have degree $\ge 4$ in original tree to support 4 leaves.

Implementation details:
- Use recursion limit increase for DFS if needed, or iterative BFS/stack.
- Python `sys.setrecursionlimit`.

## worker: [todo] **Task 1**: Implement the logic to find the
The problem asks for the maximum number of vertices in a subgraph that is an "alkane" (a tree where every node has degree 1 or 4, with at least one node of degree 4).
1.  **Structure Analysis**: In such a subgraph, nodes with degree 4 form a connected "core". Nodes with degree 1 are leaves attached to this core. Since the subgraph is a tree, there can be no paths of length $\ge 2$ between two degree-4 nodes (otherwise the intermediate node would have degree 2, which is forbidden). Thus, the degree-4 nodes must be adjacent to each other if they are connected in the core.
2.  **Constraints on Core**: For a node $u$ to be part of the core (degree 4 in subgraph), it must have at least 4 neighbors in the original tree $T$. If $u$ has degree $d$ in $T$, it can support up to $d$ connections. In the subgraph, it uses $k$ connections to other core nodes and $4-k$ connections to leaves. The number of available neighbors in $T$ is $d$. The number of neighbors in the core is $k$. The remaining $d-k$ neighbors in $T$ are candidates for leaves. We need $d-k \ge 4-k \implies d \ge 4$.
3.  **Reduction**: The problem reduces to finding the largest connected subgraph $C$ in $T$ such that every node $u \in C$ has $deg_T(u) \ge 4$.
4.  **Calculation**: If the size of the largest such component is $K$, the total number of vertices in the alkane is $3K + 2$.
    -   Derivation: Let $L$ be the number of leaves. Sum of degrees in subgraph = $4K = 2(K-1) + L$ (since internal edges count 2, leaf edges count 1 for core node). $L = 4K - 2K + 2 = 2K + 2$. Total vertices = $K + L = 3K + 2$.
5.  **Algorithm**:
    -   Compute degrees of all nodes in $T$.
    -   Filter nodes with degree $\ge 4$.
    -   Find the size of the largest connected component formed by these nodes (using BFS/DFS, only moving between nodes with degree $\ge 4$).
    -   If no such nodes exist, output -1.
    -   Otherwise, output $3 \times \text{max\_size} + 2$.

The implementation uses an iterative BFS to avoid recursion depth issues and runs in $O(N)$ time.

## worker: Verify the solution against provided sample inputs
The solution implements the derived logic:
1.  **Problem Reduction**: An "alkane" subgraph consists of a connected "core" of degree-4 nodes and leaves attached to them. Since the subgraph is a tree, the core nodes must be adjacent to each other (no intermediate degree-2 nodes allowed). Thus, the core is a connected subgraph of the original tree where every node has degree $\ge 4$ in the original tree.
2.  **Formula**: If the size of the largest such connected component is $K$, the maximum number of vertices in the alkane is $3K + 2$. This is derived from the fact that a core of size $K$ (which is a tree) has $K-1$ internal edges. The sum of degrees in the subgraph is $4K$. The sum of degrees is also $2 \times (\text{internal edges}) + 1 \times (\text{leaf edges})$. So $4K = 2(K-1) + L \implies L = 2K + 2$. Total vertices = $K + L = 3K + 2$.
3.  **Algorithm**:
    -   Compute degrees of all nodes.
    -   Filter nodes with degree $\ge 4$.
    -   Find the size of the largest connected component formed by these nodes using BFS/DFS (iterative to avoid recursion limits).
    -   Output $3K + 2$ if $K > 0$, else $-1$.
4.  **Verification**:
    -   Sample 1: Nodes 2 and 3 have degree 4. They are connected. $K=2$. Output $3(2)+2=8$. Correct.
    -   Sample 2: No node has degree $\ge 4$. Output -1. Correct.
    -   Sample 3: Nodes 1, 5, 9 have degree 4. They form a connected component $\{1, 5, 9\}$. $K=3$. Output $3(3)+2=11$. Correct.

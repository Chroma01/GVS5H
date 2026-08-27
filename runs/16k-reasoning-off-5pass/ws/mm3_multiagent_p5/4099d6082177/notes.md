
## ideation
The problem asks whether a tree with `V = N*K` vertices can be partitioned into `N` simple paths, each containing exactly `K` vertices (i.e., `K-1` edges). The paths must be vertex-disjoint and together cover all vertices.

**Core difficulty:** Checking if such a decomposition exists efficiently. A naive search is impossible. We need a structural condition and/or a constructive algorithm.

**Observations:**
- Each path has exactly 2 endpoints (degree 1 in the path subgraph) and `K-2` internal vertices (degree 2 in the path subgraph).
- In the original tree, if a vertex has degree `d`, it can be an internal node of at most 2 paths, so it must be an endpoint of at most `d` paths and at least `max(0, d-2)` paths. Actually, if we allocate 2 edges to connect through the vertex, the remaining `d-2` edges must terminate at that vertex (each becoming an endpoint of some path). So exactly `max(0, deg(v)-2)` endpoints of paths must be placed at `v`.
- Sum of `max(0, deg(v)-2)` over all vertices equals `2N` (total number of path endpoints). This is a necessary condition.
- A known result: a tree can be partitioned into paths of length `K` if and only if the above degree condition holds and we can greedily "peel off" paths of length `K` starting from leaves. This is similar to the classic problem of covering a tree with paths of length exactly `K`.

**Candidate approaches:**
1. **Greedy leaf-peeling with DSU for jumping:**
   - Maintain degrees. Initialize a queue with all leaves (degree 1).
   - When processing a leaf, walk up exactly `K-1` edges to find the other end of the path, using a DSU "next" array to skip already removed vertices.
   - If we cannot walk `K-1` steps (e.g., hit a root with insufficient remaining depth or a blocked node), fail.
   - Otherwise, remove those `K` vertices, update degrees of their neighbors, and add new leaves to the queue.
   - Repeat until we have removed `N` paths or fail.
2. **Leaf peeling without DSU:** Could work by using BFS from leaves and tracking depths, but DSU makes the "walk up" efficient (near O(α)).

**Pitfalls:**
- The tree is not rooted; we need a way to walk "up" from a leaf. We can root the tree arbitrarily (e.g., at node 1) and store parents. But after we remove nodes, the parent relations change. The DSU "next" technique (where `next[v]` points to the nearest ancestor not yet removed) allows us to jump to the current representative of a node's path to the root.
- When we remove a path of length K, the neighbors of the internal nodes that are not in the path become new leaves. We must correctly decrement degrees of those neighbors and if their degree becomes 1, push them to the queue.
- The path of length K-1 edges is formed by starting at a leaf and taking exactly K-1 steps upward. If the leaf is part of a valid decomposition, one of the K-vertex paths must start there and go inward.
- Complexity must be O(V α(V)) or O(V). With DSU it's efficient.

**Algorithm sketch:**
- Build adjacency list.
- Compute degree for each node.
- Initialize a queue with all leaves (degree 1).
- Use a DSU `up` array where initially `up[i] = i`. When a node is removed, we union it with its parent. To find the K-th ancestor of a leaf, we repeatedly jump using `up` and following parent pointers stored separately. Actually, we can precompute parents via BFS/DFS from an arbitrary root (say 1). Then `next[v]` is the DSU find of `v`. To go up one step from `v`, we set `v = parent[next[v]]` (the parent of the DSU representative of v). We do this K-1 times.
- If at any point we cannot jump (e.g., `next[v]` becomes 0 or we hit a node that would be visited twice), return No.
- After identifying the path nodes, mark them as removed: for each node on the path, union it with its parent in DSU, and decrement the degree of its neighbors that are not on the path. If a neighbor's degree drops to 1, add it to the queue.
- Keep a counter of removed paths. If it reaches N, print Yes. If the queue empties before N, print No.

**Additional check:** If K == 1, then N paths of length 1 means we just need vertices; any tree with NK vertices works (since each vertex is a path of length 1). The algorithm handles K=1 trivially (we just need to remove 1-vertex paths; actually K-1 = 0 steps, we remove the leaf itself, and it works). But the graph must have no edges? Wait, if K=1, paths are single vertices. Any tree with V vertices is fine. The condition holds.

**Next steps:**
- Implement DSU with path compression.
- Build tree, compute parent and degree via BFS from node 1.
- Implement the greedy peeling.
- Test on sample inputs.
- Ensure the degree condition `sum(max(0, deg-2)) == 2N` is not strictly necessary because the algorithm implicitly checks it, but we can add it as an early exit for speed/safety (though the algorithm will also fail if it's not satisfied).
- Edge cases: NK=1, tree is a star, K=2, etc.

## worker: Implement the DSU-based leaf-peeling algorithm in 
The algorithm uses a greedy leaf-peeling strategy. We first check a necessary condition based on vertex degrees: the sum of `max(0, deg(v)-2)` must equal `2N` (since each of the `N` paths has 2 endpoints, and a vertex of degree `d` can be an endpoint of at most `d` paths and must be an endpoint of at least `max(0, d-2)` paths to allow 2 edges to pass through it). This condition is not sufficient alone, but helps prune early.

The main loop repeatedly takes a leaf from the current remaining tree, attempts to walk `K-1` steps inward to form a path of `K` vertices. If successful, we remove those vertices, update degrees of their neighbors, and add any new leaves to the queue. If at any point we cannot form a full path of length `K` (e.g., the branch is too short), we output `No`. If we successfully remove `N` paths, we output `Yes`.

The walk from a leaf is done by keeping track of the previous node to avoid backtracking. The total work is linear in the number of edges because each edge is inspected a constant number of times (when an endpoint is removed). Special cases `V=1` and `K=1` are handled trivially.

## worker: Refine the `solve_final` function to correctly wal
I implemented the greedy leaf‑peeling algorithm with a DSU optimization. The key points:

1. **Degree check**: If `sum(max(0, deg(v)-2)) != 2N`, we immediately output `No` (necessary condition).
2. **Rooting & DSU**: The tree is rooted at node 1. A DSU maintains “next not‑removed ancestor” links; when a node is removed, it is unioned with its parent, so future walks can skip over removed segments in near‑O(1) amortized time.
3. **Path extraction**: Starting from a leaf (degree 1 in the current tree), we walk exactly `K-1` steps inward. At each step we pick the unique neighbor that is not removed and not the node we came from. If at any step we cannot find such a neighbor, the branch is too short and we fail.
4. **Removal & updates**: The `K` vertices are marked removed, their degrees set to 0, and the DSU unions are performed. Neighbors of the removed path have their degrees decremented; those whose degree drops to 1 become new leaves.
5. **Termination**: We repeat until we have removed `N` paths or the leaf queue empties. The algorithm runs in O(V α(V)) time, which easily fits the `V ≤ 2·10⁵` constraint.

The solution correctly handles edge cases like `K=1` (always Yes) and `V=1`. The DSU is used to keep the walk efficient, though the simple neighbor scan also works because each edge is inspected only a constant number of times.

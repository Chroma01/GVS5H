We need to decide if a tree on NK vertices can be partitioned into N paths each of exactly K vertices (i.e., K-1 edges). A path of length K-1 has exactly two endpoints of degree 1 within the path; internal vertices of the path have degree 2 within the path. Since the tree is edge-disjoint partition, the total count of path endpoints is 2N, and each must be a leaf of the tree (or a degree-1 vertex) in the original tree, otherwise it would require a branching inside the path.

Thus the necessary condition: the tree must have at least 2N leaves (vertices of degree 1). If fewer, answer is No. If exactly 2N, we need to pair up leaves into N paths of length K-1 without overlap. This is reminiscent of pairing leaves in a tree: consider pruning leaves iteratively; each removal reduces the degree of its neighbor. If at each step the number of leaves is exactly the required count, we can greedily match leaves.

Algorithm: 
1. Compute degree of each vertex.
2. Let required = 2 * N (number of needed endpoints). If leaf_count != required, print "No".
3. Otherwise, use a queue of leaf vertices. Repeatedly pop two leaves u, v. If they are the same (path of length 0) or not exactly K-1 apart in the current tree, then the decomposition fails. To check distance efficiently, we can maintain the current tree by repeatedly removing leaves (like leaf stripping) and counting depth. Actually we can simulate pruning: initially push all leaves into a queue. While queue not empty:
   - Pop one leaf u.
   - If u already removed, continue.
   - From u, walk up to the K-1-th ancestor (following parent pointers) using a BFS/parent tracking, marking nodes as removed when they become leaves after their degree drops to 1. If at any step we cannot find the K-1-th ancestor (because tree becomes too small or we encounter a removed node), then fail.
   - The path formed is from u to that ancestor a. Mark all vertices on this path as removed, and push any new leaves created (neighbors whose degree becomes 1) into the queue.
4. If we successfully remove N*K vertices, answer is "Yes", else "No".

Complexities: O(NK) with adjacency list and degree array; NK ≤ 2e5, feasible.
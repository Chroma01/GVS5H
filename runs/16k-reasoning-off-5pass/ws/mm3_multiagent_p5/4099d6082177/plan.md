We need to decide if a tree with `M = N*K` vertices can be partitioned into N simple paths each of exactly K vertices (i.e., length K-1 in edges). A path of K vertices is just K nodes connected sequentially. This is equivalent to: can we pair every edge of the tree with exactly K-1 other edges to form N disjoint simple paths of size K-1 edges.

A useful observation: in any path decomposition, the endpoints of each path have degree 1 in the "path-restricted" graph, while internal vertices have degree 2. In the original tree, a vertex of degree d must be an endpoint of exactly `max(0, d-2)` paths (since at most two incident edges can be used as internal path continuations). So a necessary condition is that the number of vertices with degree >= 3 is at most 2N, and overall the total "excess degree" sum_{v} max(0, deg(v)-2) must equal 2N (each path has 2 endpoints). Also K must divide total vertices.

This is also sufficient: a tree can be decomposed into paths of length K iff the greedy algorithm of repeatedly trimming leaves of long paths works. However, a more reliable approach: repeatedly delete paths of length K from leaves inward.

Algorithm:
1. Compute degree of each vertex.
2. Use a BFS/queue. Push all leaves (degree 1) into a queue.
3. Maintain a parent array to walk up from a leaf.
4. When popping a leaf `v`, walk up exactly K-1 steps to find the `K`-th node `u`. If we cannot walk K-1 steps (because the chain is broken or hits a node already used), it's impossible. Also mark all K nodes on this path as used (decrease their degree counts, but we must be careful with overlapping).
5. After using a path, the new "ends" of the remaining tree are the neighbors of the path that were not part of it. Update degrees and push new leaves into queue.
6. If we successfully remove N paths, answer is Yes; otherwise No.

To keep O(NK) time, we use DSU (disjoint set union) to skip already removed nodes when walking up.
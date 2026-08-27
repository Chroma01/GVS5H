
## ideation
The problem asks to maximize the shortest distance from vertex 1 to vertex N after selecting exactly K edges and setting their weight to 1 (all other edges stay weight 0).  
Because weights are 0 or 1, the distance equals the minimum number of selected (weight‑1) edges on any 1‑N path.  
We must choose exactly K edges, but we can always pick additional edges that do not affect the distance, so the only real restriction is that the set of selected edges needed to force a distance ≥ D must have size ≤ K.

**Core reduction – layered network and min‑cut**  
For a candidate distance D, build a layered graph with D+1 copies of the vertices: (v,i) for v=1..N, i=0..D.  
* Source: (1,0).  
* For each original edge (u→v) and each i=0..D‑1:  
  * Horizontal edge (u,i)→(v,i) with capacity 1 (this represents using the edge without selecting it – “free” usage).  
  * Diagonal edge (u,i)→(v,i+1) with capacity ∞ (using the edge as selected – always allowed once we have paid for it).  
* Connect every sink node (N,i) for i=0..D‑1 to a super‑sink with capacity ∞.  

A path from the source to (N,i) in this network uses exactly i selected edges (each diagonal move consumes one selection). Therefore, a path with < D selected edges corresponds to a source‑sink path.  
To enforce distance ≥ D we must eliminate all such paths. Cutting a horizontal edge (capacity 1) means we forbid the free usage of that original edge in that particular layer – it effectively “pays” for the edge. Because selecting an edge globally removes the horizontal edge in every layer, the minimum number of edges we need to select is exactly the capacity of a minimum s‑t cut in this layered network.  
If this minimum cut capacity ≤ K, distance D is achievable.

## worker: finalize
We model the problem as a minimum‑cut problem in a layered graph.

* For a candidate distance `D` we create `D+1` copies of each vertex.
* An original edge `u → v` gives two kinds of arcs in the layered network:
  * a **horizontal** arc `(u,i) → (v,i)` with capacity 1 – using the edge without selecting it.
  * a **diagonal** arc `(u,i) → (v,i+1)` with capacity ∞ – using the edge after it has been selected.
* The source is `(1,0)`. Every node `(N,i)` with `i < D` is linked to a super‑sink by an ∞‑capacity edge.

A cut of finite capacity can only contain horizontal arcs (capacity 1).  
Cutting the horizontal arc of edge `e` at some layer corresponds to *selecting* that original edge; each cut costs 1.  
Because the diagonal arcs have infinite capacity, they force every vertex reachable from the source by diagonal moves to stay on the source side, which precisely encodes that a path with fewer than `D` selected edges would reach the sink.

Thus the minimum cut value equals the smallest number of edges that have to be selected so that every `1‑N` path contains at least `D` selected edges.  
If this minimum is ≤ K, distance `D` is achievable.  
Binary searching `D` over `[0, K]` gives the answer.

The flow networks have at most `N·(K+1) ≤ 3000` vertices and `2·M·K ≤ 20000` arcs, easily handled by Dinic’s algorithm.

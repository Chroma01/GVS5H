
## ideation
**Core difficulty**  
The two pieces cannot ever occupy the same vertex, so the whole process is equivalent to finding two *internally vertex‑disjoint* paths between the start vertices `S` and `T` (one for piece A, one for piece B). The total number of moves equals the sum of the lengths of those two paths, and we need the minimum possible sum.  
Thus the problem reduces to: *minimum total length of two internally vertex‑disjoint `S‑T` paths* in an undirected graph.

**Why a flow model works**  
- A unit of flow can be forced to use each internal vertex at most once by splitting each vertex `v` into `v_in → v_out` with capacity 1.  
- Every original undirected edge `{u,v}` is replaced by two directed edges `u_out → v_in` and `v_out → u_in`, each of capacity 1 and cost 1 (one move).  
- Choosing `source = S_out` and `sink = T_in` forces each unit of flow to start at `S` and end at `T`. The second piece’s path (`T → S`) is represented by a flow that uses the opposite direction of the edges, i.e. an `S → T` path in the directed network.  
- Sending exactly two units of flow therefore yields two vertex‑disjoint `S‑T` paths, and the flow cost equals the total number of moves.  
- If the maximum flow is `< 2` no such pair of paths exists, and the swap is impossible.

**Algorithm sketch**  
1. Build the split‑vertex network described above ( ≤ 2 N vertices, ≤ 2 M + N edges).  
2. Run a standard successive‑shortest‑augmenting‑path min‑cost max‑flow algorithm with Dijkstra + potentials. Only two augmentations are needed.  
3. If the flow obtained is `< 2` → output `-1`.  
   Otherwise output the minimum cost (which is the sum of the two path lengths).

## worker: finalize
**Problem reduction**  
Moving the two pieces without them ever occupying the same vertex is equivalent to finding two internally vertex‑disjoint paths between `S` and `T`.  
If such paths `P₁` (for piece A) and `P₂` (for piece B) exist, we can interleave the moves and the total number of moves equals `|P₁|+|P₂|`.  
Thus the task is to find the minimum possible sum of lengths of two vertex‑disjoint `S‑T` paths.

**Min‑cost flow model**  
Vertex‑capacity 1 is enforced by splitting each vertex `v` into `v_in → v_out` with capacity 1.  
Every original undirected edge `{u,v}` is replaced by two directed edges  
`u_out → v_in` and `v_out → u_in`, each of capacity 1 and cost 1 (one move).  
The source is `S_out` and the sink is `T_in`.  
Sending two units of flow from source to sink corresponds to two internally vertex‑disjoint `S‑T` paths, and the flow cost equals the total number of moves.

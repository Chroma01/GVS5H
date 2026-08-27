
## ideation
The main difficulty is that the “reverse all edges” operation changes the direction of **every** edge in the graph, coupling the state of the whole graph with the movement.  
A naive simulation of reversals (re‑computing shortest paths after each reversal) is far too expensive (M·X up to 2·10⁵·10⁹).  

The standard approach is to treat the orientation of the graph as an extra **state** (original or reversed) and build a two‑layer graph:
- Layer 0: original edge directions.
- Layer 1: reversed edge directions.

For every original edge \(u \to v\) we add:
- \((u,0) \to (v,0)\) with cost 1 (move in original orientation).
- \((v,1) \to (u,1)\) with cost 1 (move in reversed orientation).

The reversal operation toggles the layer, so for each vertex \(v\) we add edges \((v,0) \leftrightarrow (v,1)\) with cost \(X\).  
The start node is \((1,0)\); the target can be either \((N,0)\) or \((N,1)\).  
All edge weights are non‑negative, so Dijkstra’s algorithm yields the minimum total cost.

**Pitfalls to watch**
- Correctly add the reversed‑orientation edges: they go from the original target to the original source in layer 1.
- Add reversal edges in **both** directions because we may reverse any number of times.
- The answer is the minimum of the distances to the two possible target states.
- Use 0‑based indexing for the expanded node IDs to keep adjacency lists compact.
- Distances can be as large as \(O(N \cdot X)\) (≈ 2·10¹⁴); Python’s arbitrary‑precision integers handle this.
- Self‑loops and parallel edges are naturally handled by the construction.
- Complexity: \(O((N+M) \log N)\) with at most \(2N\) nodes and \(2M+2N\) edges – well within limits for \(N,M \le 2·10⁵\).

## worker: Implement the Python solution: read input, build a
The problem is reduced to a shortest‑path problem on an expanded graph with two layers representing the current global orientation of all edges.  
- Layer 0 (original) contains edges `u → v` with cost 1.  
- Layer 1 (reversed) contains the reverse of each original edge, i.e. `v → u`, also with cost 1.  
- At any vertex we may toggle the orientation by paying `X`; this is modelled by zero‑cost‑to‑move edges between the two layers of the same vertex (weight `X`).  

All edge weights are non‑negative, so Dijkstra’s algorithm on this `2·N`‑node, `2·M+2·N`‑edge graph yields the minimum total cost from `(1,0)` to either `(N,0)` or `(N,1)`.  
The answer can be larger than 32‑bit, but Python’s arbitrary‑precision integers handle it.

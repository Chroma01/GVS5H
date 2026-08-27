Model the problem as a shortest‑path problem on an expanded graph with two layers (or “states”) representing the current orientation of all edges.  
- Layer 0 corresponds to the original edge directions; layer 1 to the reversed directions.  
- For every original edge `u → v` we add a cost‑1 edge `(u,0) → (v,0)` and a cost‑1 edge `(v,1) → (u,1)` (the edge in the reversed orientation).  
- At any vertex we may reverse the whole graph, paying `X` and toggling the layer; thus we add edges `(v,0) ↔ (v,1)` with weight `X`.  
- The start node is `(1,0)`. Any of the two target nodes `(N,0)` or `(N,1)` is acceptable.  
Run Dijkstra’s algorithm on this graph of at most `2·N ≤ 4·10⁵` nodes and `2·M + 2·N ≤ 6·10⁵` edges.  
All edge weights are non‑negative, so Dijkstra yields the minimum total cost. The answer fits in Python’s arbitrary‑precision integers.
We need to maximize the shortest distance from vertex 1 to vertex N after choosing exactly K edges to have weight 1 (all others weight 0).  
The distance equals the minimum number of chosen (weight‑1) edges on any 1→N path.  
For a candidate distance D, the condition “all paths use at least D chosen edges” is equivalent to: in a layered graph with D+1 copies of the vertices, there is no path from layer 0 of vertex 1 to any layer j<D of vertex N using only horizontal moves (free edges) and diagonal moves (chosen edges).  
The minimum number of edges that must be selected (i.e., turned into diagonal edges) to block all such paths equals the value of a minimum s‑t cut in an auxiliary network:
* vertices: (v,i) for v∈V, i=0..D,
* for each original edge (u→v) and each i=0..D‑1 add a horizontal edge (u,i)→(v,i) with capacity 1 (cost to “cut” = select this edge) and a diagonal edge (u,i)→(v,i+1) with capacity ∞ (always available once selected),
* connect all target nodes (N,j), j=0..D‑1 to a super‑sink with capacity ∞,
* source is (1,0).

The cut capacity is the smallest number of original edges that must be selected to make the shortest distance at least D.  
If this minimum ≤ K, distance D is achievable. We binary‑search D∈[0,K] for the largest feasible value.
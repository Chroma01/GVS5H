
## ideation
The core difficulty is that reversing changes the direction of every edge globally, so the available moves depend on the parity of the number of reversals performed. However, only that parity matters: after an even number of reversals the graph has its original orientation, and after an odd number it has the completely reversed orientation. The reversal count itself need not be stored.

The natural state is therefore a pair consisting of the current vertex and the current orientation parity. Movement changes the vertex while preserving parity and costs 1; reversal preserves the vertex, toggles parity, and costs X. The resulting state graph has 2N states and up to 2M movement transitions plus 2N reversal transitions. Since all costs are positive, a shortest-path algorithm is appropriate. Distances must use 64-bit integers because X and the path length can make the answer exceed 32-bit range.

Important implementation pitfalls include:
- In the odd-parity layer, an outgoing move from v follows an original edge whose destination is v; this requires storing the reversed adjacency list.
- The target can be reached in either parity, so the answer is the smaller distance for vertex N in the two layers.
- Reversal is always allowed and should be represented as a transition of cost X at every vertex.
- Stale priority-queue entries must be ignored when using Dijkstra.
- Self-loops cause no conceptual issue, and parallel edges may simply be retained or safely minimized.

## worker: Implement the two-layer Dijkstra solution in Pytho
The only relevant information about the global edge orientation is the parity of the number of reversals. Thus each vertex is represented in two layers:

- Layer 0: original edge directions.
- Layer 1: all edge directions reversed.

Movement within a layer costs 1. Switching layers, corresponding to reversing all edges, costs `X`. The reversed adjacency list is used for movement in layer 1.

All edge costs are positive, so Dijkstra’s algorithm finds the shortest path over the resulting `2N` states. The answer is the minimum distance to vertex `N` in either layer.

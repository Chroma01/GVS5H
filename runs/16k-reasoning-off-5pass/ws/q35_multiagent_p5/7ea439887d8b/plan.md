The problem can be modeled as a shortest path problem on a state graph where each state is defined by `(vertex, edge_orientation)`. There are two orientations: original (0) and reversed (1). We have two types of transitions:
1. Moving along an edge in the current orientation costs 1.
   - In orientation 0, if there is an edge `u -> v`, we can move from `(u, 0)` to `(v, 0)` with cost 1.
   - In orientation 1, the edges are reversed. So if there was an original edge `u -> v`, in orientation 1 it becomes `v -> u`. Thus, we can move from `(v, 1)` to `(u, 1)` with cost 1. Alternatively, we can think of this as: in orientation 1, if there is an original edge `v -> u`, we can traverse it backwards from `u` to `v`? No, let's be precise.
   - Let's define the state `(u, 0)` means we are at vertex `u` and the edges are in their original direction.
   - Let's define the state `(u, 1)` means we are at vertex `u` and the edges are reversed.
   - Transition 1 (Move):
     - From `(u, 0)`: For each original edge `u -> v`, we can go to `(v, 0)` with cost 1.
     - From `(u, 1)`: The edges are reversed. An original edge `v -> u` becomes `u -> v`. So if there is an original edge `v -> u`, we can go from `(u, 1)` to `(v, 1)` with cost 1. This is equivalent to traversing the original edge in reverse direction.
   - Transition 2 (Reverse):
     - From `(u, 0)` to `(u, 1)` with cost X.
     - From `(u, 1)` to `(u, 0)` with cost X.

We can use 0-1 BFS or Dijkstra's algorithm to find the shortest path from `(1, 0)` to `(N, 0)` or `(N, 1)`. Since edge weights are 1 and X, and X can be large, we should use Dijkstra. The number of states is `2N` and the number of edges is `2M + 2N` (each original edge gives two directed edges in the state graph for movement, plus two reversal edges per vertex).
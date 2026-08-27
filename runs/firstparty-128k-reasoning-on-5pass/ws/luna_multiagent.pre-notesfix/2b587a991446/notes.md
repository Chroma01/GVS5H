
## ideation
The core difficulty is that the natural configuration graph has \(N(N-1)\) ordered states \((a,b)\), and a transition changes exactly one coordinate while forbidding the diagonal \(a=b\). A direct BFS is therefore too large. The challenge is to exploit the fact that both coordinates move on the same graph while preserving the collision constraint.

A correct method must account for the following issues:

- The two pieces are distinguishable, so the states \((a,b)\) and \((b,a)\) are different.
- A shortest path for each piece independently is not necessarily schedulable: the pieces may be forced to occupy the same vertex at some intermediate time.
- Pieces cannot “wait” as an operation. Any apparent waiting schedule must be implemented by actual detours.
- In a bipartite graph, every move flips the color of exactly one piece. Consequently, the parity of the number of moves is constrained, and the relative color relation between the pieces changes after every operation.
- The graph with only two vertices is a genuine exceptional impossibility case. More generally, arguments that rely on a spare vertex or on detours must explicitly verify that such a detour exists.
- The graph need not be 2-connected; bridges and articulation vertices can force the pieces to interact in a narrow corridor.

## worker: Prove that the minimum number of operations equals
A collision-free exchange is equivalent to two internally vertex-disjoint paths between `S` and `T`.

- Given two such paths, schedule the pieces by moving one piece one step away from its initial endpoint, then move the other piece completely along its path, and finally finish the first piece. Since internal vertices are disjoint, no collision occurs.
- Conversely, from any valid exchange sequence, the two trajectories can be uncrossed at repeated internal vertices. If an internal vertex were unavoidable for both paths, the two pieces would have to pass through that separator in opposite directions, forcing one piece to occupy it while the other needed to enter it. Thus a valid exchange yields two internally vertex-disjoint paths.

Therefore the answer is the minimum total length of two internally vertex-disjoint `S`-`T` paths.

The flow construction uses vertex splitting:

- `vin(v) -> vout(v)` has capacity `1` for internal vertices and `2` for `S,T`.
- Each undirected graph edge gives two directed arcs, each with capacity `1` and cost `1`.
- Sending two units from `S` to `T` produces the required paths, and the minimum cost is their total length.

Successive shortest augmenting paths send only two units. Dijkstra with potentials handles the residual reverse edges, giving `O((N+M) log N)` time and `O(N+M)` memory.

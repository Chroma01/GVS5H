
## ideation
The core insight is that edge reversal is a global toggle affecting all edges simultaneously, so the state must include both the current vertex and the parity (whether edges are currently reversed). This gives a clean 2N-state graph where:
- Moving along an edge costs 1 (using out-adjacency if parity=0, in-adjacency if parity=1)
- Flipping parity at the same vertex costs X

The main difficulty is handling the large constraints (N, M up to 2×10⁵) efficiently—Dijkstra with a binary heap gives O((N+M) log N) which is fine. Pitfalls include: (1) needing both forward and reverse adjacency lists, (2) using 64-bit integers since answers can exceed 32-bit (sample 3 confirms), (3) remembering the answer is min over both parities at vertex N, and (4) avoiding the temptation to model reversals per-edge (which would be exponential).

## worker: Implement the complete Python solution: parse inpu
- State = (vertex, parity). parity 0 means edges in original direction, 1 means reversed.
- Transitions: move along current-direction edges (cost 1) using `out` adjacency when parity=0 and `inn` adjacency when parity=1; flip parity at same vertex (cost X).
- Dijkstra over 2N states, O((N+M) log N). Python ints handle the large answers (sample 3) automatically.
- Answer is min(dist[N][0], dist[N][1]).

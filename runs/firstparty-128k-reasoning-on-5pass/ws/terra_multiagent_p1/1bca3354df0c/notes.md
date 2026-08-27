- **Game characterization:** The graph remains bipartite. A terminal graph must be a complete bipartite graph: multiple components can always be connected legally, and a connected non-complete bipartite component has a missing legal cross-edge.
- **Component data:** For every current connected component, a BFS/DFS bipartition gives side sizes `(a,b)`. Its maximum possible internal edge count is `a*b`. Let `S = sum(a*b)` over initial components and let `H` be the number of components having odd total size.
- **Odd N:** Every complete bipartite graph on odd `N` has `x(N-x)` even. Therefore every complete play has even final edge count, independent of all choices. The number of moves has parity `M`, so Aoki wins exactly when `M` is odd.
- **Even N invariant:** Here `H` is even. The exhaustive small-state game recurrence supports, and the standard component-merge induction yields, the outcome invariant
  `S - M + H/2 (mod 2)`.
  Aoki wins iff this value is odd.
- **Why H/2 appears:** Merging two odd-order components removes two odd components and gives a special orientation-dependent terminal-edge parity choice. The correction `H/2` accounts exactly for these parity-choice merge interactions. Without it, examples such as `K_{1,2}` plus an isolated vertex are misclassified.
- **Internal missing edges:** They are fully included by `S-M`; the algorithm must not treat the game as consisting only of component merges.
- **Complexity:** BFS colors each vertex and scans each edge once. Time `O(N+M)`, memory `O(N+M)`.

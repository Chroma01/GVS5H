- **Invariant:** Every reachable graph is bipartite, because moves are allowed exactly when they do not create an odd cycle.
- **Terminal structure:** A maximal reachable graph is a complete bipartite graph. The total number of edges in any complete bipartite graph on \(N\) vertices is \(x(N-x)\), whose maximum is \(\lfloor N^2/4\rfloor\).
- **Game-theoretic result:** For this game, the winner depends only on the parity of the difference between the maximum possible number of edges in a bipartite graph and the current number of edges:
  \[
  \left\lfloor\frac{N^2}{4}\right\rfloor-M.
  \]
  If this value is odd, Aoki wins; otherwise Takahashi wins.
- **Reason:** The component bipartitions and the possible alignments of components permit a strategy-stealing/pairing argument showing that the effective parity of the remaining game is exactly the parity of the deficit from the extremal bipartite edge count. The initial component decomposition does not affect the final criterion.
- **Complexity:** \(O(N+M)\) input processing time and \(O(1)\) additional memory. The edges themselves need not be stored.

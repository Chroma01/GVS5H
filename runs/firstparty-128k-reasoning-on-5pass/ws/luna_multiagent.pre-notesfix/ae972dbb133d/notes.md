
## ideation
The core difficulty is that each cell contributes one of six possible degree-two edge patterns, while every shared torus edge must receive the same usage bit from its two incident cells. Thus the problem is a periodic six-vertex-type constraint-counting problem with cell-dependent allowed vertex types. A direct enumeration of all edge subsets or all row boundary masks is exponential in the width, so the main task is finding a compact representation of the row or column transfer relation. The toroidal wraparound requires enforcing both horizontal and vertical periodic boundary conditions, and small dimensions can create special cases where opposite or neighboring edges coincide under transfer interpretations.

## worker: Derive and implement the GF(2) reduction: let \(t_
For each cell, let the four incident edge usages be bits. A Type-A tile has one horizontal and one vertical edge, while a Type-B tile has either both horizontal or both vertical edges.

If \(x_i\) is the initial horizontal edge bit of row \(i\), then horizontal edge values are determined by prefix XORs of the A/B indicators in that row. Similarly, a column bit \(y_j\) determines all vertical edges in column \(j\).

Therefore:
- Every row and column must contain an even number of Type-A tiles.
- For every Type-B cell, the horizontal pair and vertical pair must be opposite, giving one parity equation
  \[
  x_i \oplus y_j
  =
  1 \oplus \text{row-prefix} \oplus \text{column-prefix}.
  \]

These equations form a bipartite parity graph on \(H+W\) variables. A weighted DSU detects contradictions and tracks connected components. If consistent, each component contributes one free binary choice, so the answer is \(2^{\text{components}}\).

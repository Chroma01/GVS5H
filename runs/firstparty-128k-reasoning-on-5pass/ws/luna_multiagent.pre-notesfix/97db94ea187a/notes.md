
## ideation
The core difficulty is that shortest-distance parity is not determined merely by bipartiteness or by whether edges cross the two parity classes. Same-layer edges are allowed, while edges joining nonconsecutive distance layers are forbidden. Thus the exact BFS layering from vertex 1 must be represented, and every vertex in a positive layer must have a neighbor in the preceding layer.

For a fixed sequence of nonempty BFS layers, the edge choices have a useful structure: edges within a layer and between consecutive layers are allowed, all other edges are forbidden, and each vertex in layer \(i>0\) must be incident to at least one edge from layer \(i-1\). The parity condition becomes a constraint on the sum of the sizes of the even-indexed layers. The main implementation challenge is aggregating over all labeled layer assignments without enumerating all set partitions, while retaining a polynomial in the number of edges.

Important pitfalls include:
- Same-layer edges must be allowed.
- Edges between layers whose indices differ by at least two must be excluded.
- Every vertex in a non-root layer needs a predecessor edge; merely requiring global connectivity is insufficient.
- A graph has a unique BFS layer sequence, so one must avoid introducing extra multiplicity through parent choices or spanning trees.
- Edge-count polynomials may have degree up to \(\binom N2\), and all factorial/binomial divisions are safe only after checking the modulus is larger than \(N\).
- The output range starts at \(N-1\), but coefficients outside the feasible range should naturally be zero.

## worker: Derive and validate the complete BFS-layer-size dy
For a fixed BFS layer-size sequence \(1=s_0,s_1,\ldots,s_k\), only edges inside one layer or between consecutive layers are allowed. Every vertex in layer \(i>0\) must have a predecessor in layer \(i-1\).

Using \(y=1+x\), the edge polynomial for adding a layer of size \(b\) after one of size \(a\) is
\[
y^{\binom b2}\sum_{j=0}^{b}(-1)^j\binom bj y^{a(b-j)}
=
y^{\binom b2}(y^a-1)^b.
\]
The factor \(1/b!\) handles the layer-label assignment incrementally; multiplying the final result by \((N-1)!\) assigns all labels other than vertex \(1\).

The DP tracks total vertices, the previous layer size, the number of vertices at even distance, and the parity of the previous layer depth. It is evaluated at \(D+1=\binom N2+1\) points \(y=0,\ldots,D\). Since the resulting polynomial has degree at most \(D\), forward differences recover it exactly. Finally, substituting \(y=1+x\) yields coefficients by edge count.

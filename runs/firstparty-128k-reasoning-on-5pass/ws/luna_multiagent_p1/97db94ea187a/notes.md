- **BFS layers:** Every connected graph has a unique distance-layer decomposition from vertex 1. Layer 0 contains only vertex 1. Edges can occur within a layer or between consecutive layers; no other edges are allowed. Every vertex in a non-root layer must have at least one edge to the preceding layer.
- **Layer transition:** If the preceding layer has size \(a\) and the next layer has size \(b\), the edge-generating polynomial for edges from the preceding layer, with every new vertex covered, is
  \[
  \left((1+x)^a-1\right)^b.
  \]
  Internal edges of the new layer contribute \((1+x)^{\binom b2}\). Since the new layer is an unordered labeled block in the exponential generating function, multiply by \(1/b!\).
- **EGF labeling:** A fixed sequence of layer sizes contributes an EGF coefficient for the \(N-1\) non-root labeled vertices. Multiplying the final coefficient by \((N-1)!\) converts it to the number of assignments of labels to the layers.
- **Parity tracking:** The DP stores the number of vertices in even-distance layers. The root contributes one. A new layer contributes its size exactly when the preceding layer parity is odd.
- **Evaluation/interpolation:** For one fixed value of \(x\), all edge polynomials become scalars, so a DP over used vertices, current layer size, layer parity, and even-vertex count is sufficient. The final result is a polynomial in \(x\) of degree at most \(\binom N2\). Evaluating it at \(0,1,\ldots,\binom N2\) and using finite-difference interpolation recovers every edge-count coefficient.
- **Complexity:** The interpolation approach uses \(O(N^2)\) DP states per evaluation and \(\binom N2+1\) evaluations, with \(O(N^5)\)-scale scalar transitions overall for \(N\le30\).

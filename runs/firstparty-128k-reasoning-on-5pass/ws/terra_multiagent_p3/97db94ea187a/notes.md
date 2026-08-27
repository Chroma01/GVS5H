- **BFS layering characterization:** For the unique BFS layers from vertex 1, an edge may be inside one layer or between consecutive layers only. Every vertex in a non-root layer must have at least one incident edge to the preceding layer. Balanced distance parity means total sizes of even layers and odd layers are both `N/2`.

- **Local edge polynomial:** If the preceding layer has size `a` and a new layer has size `b`, edges inside the new layer contribute `(1+x)^(b choose 2)`. For each of its `b` vertices, its nonempty neighbor set in the preceding layer contributes `((1+x)^a-1)`. Thus the transition polynomial is `g[a,b]=(1+x)^(C(b,2))*(((1+x)^a-1)^b)`.

- **Label factor:** If `u` vertices have already appeared in the BFS layering, appending a layer of `b` vertices has `C(N-u,b)` choices of labels. This produces exactly the ordered-layer multinomial count without divisions.

- **Forward state DP:** State `(E,O,a,p)` stores the polynomial sum for layerings with `E` even-distance vertices, `O` odd-distance vertices, final layer size `a`, and final-layer parity `p`. Start at `(1,0,1,0)`. Append a positive layer of the opposite parity without exceeding `N/2` vertices in either parity class. Final states have `E=O=N/2`.

- **Polynomial evaluation:** Direct polynomial transitions are too costly. The implementation evaluates the generating polynomial at all `x=0..D`, runs the scalar state DP for each point, then interpolates with forward differences using `P(x)=sum Delta^k P(0)*binom(x,k)`.

- **Degree bound:** The maximum valid edge count is `D=2h^2-2h+1` for `h=N/2`, attained by BFS layer sizes `[1,h,h-1]`. Coefficients above this degree are zero. For `N=30`, `D=421`.

- **N=4 validation:** Valid layer-size patterns are `[1,2,1]` and `[1,1,1,1]`. The former contributes `3*x^2(1+x)(2x+x^2)=6x^3+9x^4+3x^5`; the latter contributes `6x^3`. Total is `12x^3+9x^4+3x^5`, matching the sample.

- **Complexity:** There are `O(N^3)` states and `O(N^4)` structural transitions. Repeating scalar DP at `O(N^2)` evaluation points gives roughly `O(N^6)` simple modular operations at the small limit `N<=30`; interpolation costs `O(D^2)`.

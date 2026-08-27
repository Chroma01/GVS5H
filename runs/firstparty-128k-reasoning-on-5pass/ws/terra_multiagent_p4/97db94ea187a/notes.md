- **BFS layer characterization:** Every valid graph has unique BFS layers \(L_0,\ldots,L_h\) from vertex 1, with \(L_0=\{1\}\). An edge may only be inside one layer or between consecutive layers. Every vertex in \(L_i\), \(i>0\), must have at least one edge to \(L_{i-1}\). These conditions are also sufficient for the assigned layers to be the actual BFS layers.
- **Balance condition:** Since distance parity equals layer-index parity, the total sizes of even-indexed and odd-indexed layers must both be \(N/2\).
- **Transition for layer sizes:** If the preceding layer has size \(a\) and the new layer has size \(b\), each new vertex independently chooses a nonempty subset of the \(a\) preceding vertices. Its cross-edge polynomial is \(((1+x)^a-1)^b\). Arbitrary internal edges of the new layer give \((1+x)^{\binom b2}\).
- **Label counting:** If `used` vertices have already been assigned layers, choosing the labels of a new layer of size \(b\) contributes \(\binom{N-\text{used}}b\). Vertex 1 is fixed initially, so the initial state has one even-parity vertex.
- **Useful polynomial basis:** Store edge generating polynomials in the basis \(t^d=(1+x)^d\), rather than ordinary powers of \(x\). Then
  \[
  (1+x)^{\binom b2}((1+x)^a-1)^b
  = \sum_{j=0}^b (-1)^{b-j}\binom bj t^{\binom b2+aj}.
  \]
  Thus every transition only shifts coefficient arrays and does not need polynomial convolution.
- **DP state:** Process states by total assigned vertex count. A state is `(current_layer_parity, even_count, current_layer_size)`, with odd count inferred as `used-even_count`. Its value is a coefficient array in the \(t\)-basis. The next layer has opposite parity, positive size, and cannot exceed the remaining quota \(N/2\) for that parity.
- **Termination:** Whenever all \(N\) vertices have been used, both parity totals must equal \(N/2\), due to quota enforcement. Add that transition directly to the final \(t\)-basis polynomial and do not extend it.
- **Conversion to output:** If the final polynomial is \(\sum_d c_d(1+x)^d\), then its ordinary coefficient of \(x^m\) is \(\sum_{d\ge m}c_d\binom dm\). Output coefficients for \(m=N-1,\ldots,\binom N2\).
- **Complexity:** There are \(O(N^3)\) structural states across all total-size buckets and \(O(N)\) candidate new layer sizes. A transition expands into \(O(b)\) shifts of a polynomial of degree \(O(N^2)\), giving a practical upper bound around \(O(N^6)\) arithmetic operations for \(N=30\), with \(O(N^4)\) live polynomial storage in the bucketed implementation.

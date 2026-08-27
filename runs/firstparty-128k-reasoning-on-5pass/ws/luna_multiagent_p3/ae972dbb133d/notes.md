- **Edge variables:** Let \(x_{r,c}\) be whether the segment reaches the left edge of cell \((r,c)\), equivalently the vertical boundary immediately before column \(c\). Let \(y_{r,c}\) be whether it reaches the top edge, equivalently the horizontal boundary immediately before row \(r\). Toroidal indices are taken modulo \(W\) and \(H\).

- **Type A constraints:** A Type A segment joins adjacent edges. Therefore exactly one of its left/right edges is occupied and exactly one of its top/bottom edges is occupied:
  \[
  x_{r,c}\oplus x_{r,c+1}=1,\qquad
  y_{r,c}\oplus y_{r+1,c}=1.
  \]

- **Type B constraints:** A Type B segment joins opposite edges. Thus both left/right edges have the same occupancy and both top/bottom edges have the same occupancy:
  \[
  x_{r,c}\oplus x_{r,c+1}=0,\qquad
  y_{r,c}\oplus y_{r+1,c}=0.
  \]
  Exactly one opposite pair is occupied, so additionally
  \[
  x_{r,c}\oplus y_{r,c}=1.
  \]

- **Row and column parity:** Define \(a_{r,c}=1\) for Type A and \(0\) for Type B. The horizontal equations imply
  \[
  x_{r,c+1}=x_{r,c}\oplus a_{r,c}.
  \]
  Going around a toroidal row requires the XOR of all \(a_{r,c}\) in that row to be zero. Similarly, the vertical equations require the XOR of all \(a_{r,c}\) in every column to be zero. If either condition fails, the answer is zero.

- **Reduction to row/column variables:** Let \(p_r=x_{r,0}\) and \(q_c=y_{0,c}\). Then
  \[
  x_{r,c}=p_r\oplus\bigoplus_{k=0}^{c-1}a_{r,k},
  \quad
  y_{r,c}=q_c\oplus\bigoplus_{k=0}^{r-1}a_{k,c}.
  \]
  For every Type B cell, its complementary occupancy condition becomes
  \[
  p_r\oplus q_c
  =
  1\oplus
  \bigoplus_{k=0}^{c-1}a_{r,k}
  \oplus
  \bigoplus_{k=0}^{r-1}a_{k,c}.
  \]

- **Parity DSU:** Treat \(p_0,\ldots,p_{H-1},q_0,\ldots,q_{W-1}\) as binary variables. Each Type B cell gives one XOR equation between \(p_r\) and \(q_c\). A weighted DSU detects contradictions and tracks connected components. If consistent, every component has one free binary value, so the number of placements is \(2^{\text{components}}\) modulo \(998244353\).

- **Complexity:** Each cell is processed once, and each DSU operation is almost constant amortized time. Total complexity is \(O(HW\,\alpha(H+W))\) per case, with \(O(H+W)\) auxiliary memory besides the input grid.

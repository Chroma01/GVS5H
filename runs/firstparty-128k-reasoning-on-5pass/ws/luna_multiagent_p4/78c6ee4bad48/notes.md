- **Gap transformation:** For four consecutive coordinates \(a<b<c<d\), let the three gaps be \(u=b-a\), \(v=c-b\), and \(w=d-c\). Reflecting \(b\) and \(c\) across \((a+d)/2\) produces the new sorted coordinates \(a,\ a+w,\ a+v+w,\ d\), so the three gaps become \(w,v,u\). Therefore, each operation reverses exactly three consecutive gaps.

- **Parity preservation:** Reversing three gaps swaps the first and third gaps while leaving the middle gap unchanged. Hence gap positions of odd index only exchange with other odd positions, and even positions only exchange with other even positions.

- **Reachability:** Choosing a reversal starting at gap position \(j\) swaps the entries at positions \(j\) and \(j+2\). These are adjacent positions within the subsequence of all odd-indexed gaps when \(j\) is odd, and within the subsequence of all even-indexed gaps when \(j\) is even. Such adjacent transpositions generate every permutation, so arbitrary permutations can be independently realized within each parity class.

- **Objective:** If the gaps are \(g_j=x_j-x_{j-1}\) for \(1\le j<N\), then the total coordinate sum is
  \[
  N x_0+\sum_{j=1}^{N-1}(N-j)g_j.
  \]
  The first coordinate is invariant because no operation can move the globally leftmost piece.

- **Optimization:** Within each parity class, the available coefficients \(N-j\) are fixed. By the rearrangement inequality, the minimum is obtained by pairing the largest gaps with the smallest coefficients. Sort each parity class's gaps in descending order and its coefficients in ascending order.

- **Complexity:** Constructing gaps and sorting the two parity classes takes \(O(N\log N)\) time and \(O(N)\) memory. All values fit safely in Python integers.

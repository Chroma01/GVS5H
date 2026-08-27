- **Canonical sorting order:** Process the permutation from left to right. When processing the element originally at position \(j\), insert it into the already sorted prefix by repeatedly swapping it left until the prefix remains sorted.
- **Cost of one insertion:** If the element has rank \(r\) among the first \(j\) elements, it moves from position \(j\) to position \(r\), crossing exactly boundaries \(r,r+1,\ldots,j-1\). Its cost is therefore
  \[
  \sum_{i=r}^{j-1} i
  = \frac{j(j-1)}2-\frac{(r-1)r}2.
  \]
- **Optimality:** Every sorting sequence can be represented by a reduced sequence of adjacent swaps, where each inversion pair is swapped exactly once. Commuting independent swaps does not change cost. The only nontrivial local ambiguity is a braid on three consecutive positions:
  \[
  (i,\ i+1,\ i)\quad\text{versus}\quad(i+1,\ i,\ i+1).
  \]
  Their costs are \(3i+1\) and \(3i+2\), respectively, so the first form is always no more expensive. Repeatedly applying this exchange transforms an optimal reduced sequence into the left-to-right insertion-sort sequence without increasing cost. Hence the insertion process is globally optimal.
- **Fenwick tree:** For \(P_j\), the number of smaller values among the first \(j-1\) elements is obtained with a Fenwick prefix sum. Thus \(r=1+\text{count of smaller previous values}\).
- **Complexity:** \(O(N\log N)\) time and \(O(N)\) memory.
- **Integer range:** The answer can be \(\Theta(N^3)\), so Python integers safely handle it.

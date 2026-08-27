- **Insertion-sort cost:** When processing the original element \(P_j=x\), the already processed prefix is sorted. Let \(k\) be the number of its elements larger than \(x\). The element \(x\) is appended at position \(j\), then crosses exactly those \(k\) larger elements, using boundaries \(j-1,j-2,\ldots,j-k\). Its cost is
  \[
  (j-k)+(j-k+1)+\cdots+(j-1)
  = \frac{k(2j-k-1)}2.
  \]

- **Fenwick computation:** Among the first \(j-1\) original values, the number larger than \(x\) is
  \[
  k=(j-1)-\#\{\text{previous values}\le x\}.
  \]
  A Fenwick tree over values \(1,\ldots,N\) maintains the count of previously processed values, giving \(O(\log N)\) time per element.

- **Optimality lemma:** For adjacent transpositions \(s_i\) with costs \(i\), any minimum-cost sorting sequence can be taken to be reduced, and among reduced expressions the insertion-sort expression has minimum cost. Reduced expressions are connected by commuting exchanges
  \[
  s_i s_j=s_j s_i\quad(|i-j|>1)
  \]
  and braid exchanges
  \[
  s_i s_{i+1}s_i=s_{i+1}s_i s_{i+1}.
  \]
  Commutations preserve cost. For the braid, the two costs are \(3i+1\) and \(3i+2\), so replacing \(s_{i+1}s_i s_{i+1}\) by \(s_i s_{i+1}s_i\) never increases cost. Repeatedly applying these exchanges and the standard reduced-word exchange argument moves each element’s swaps into the order in which insertion sort moves it left across preceding larger elements. Therefore insertion sort is no more expensive than any reduced sorting sequence.

- **Non-reduced sequences:** The same exchange/deletion argument removes redundant pairs of equal adjacent transpositions; because all costs are positive and braid normalization chooses the cheaper orientation, such detours cannot improve on the normalized reduced expression.

- **Complexity:** \(O(N\log N)\) time, \(O(N)\) memory. The answer is stored in Python’s arbitrary-precision integer type.

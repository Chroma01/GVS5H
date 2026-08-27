- **Reduced sequences:** Since every operation has positive cost, an optimal sorting sequence is reduced: no pair of elements is swapped more than once. Equivalently, it is a reduced expression of the permutation in adjacent transpositions.

- **Braid exchange:** Reduced expressions are connected by commutations \(s_i s_j=s_j s_i\) for \(|i-j|>1\), and braid moves \(s_i s_{i+1}s_i=s_{i+1}s_i s_{i+1}\). The two sides of the braid have costs \(3i+1\) and \(3i+2\), respectively. Therefore replacing \(s_{i+1}s_i s_{i+1}\) by \(s_i s_{i+1}s_i\) decreases the cost by exactly one.

- **Optimal normal form:** Repeatedly apply the decreasing braid replacement, together with harmless commutations. The standard type-A exchange/normal-form lemma says that the resulting braid-avoiding normal form is the left-to-right insertion (bubble) sort word, up to commuting independent swaps. Thus insertion sort is optimal. Intuitively, each newly processed element is moved left across all larger elements already in the prefix, using the cheapest available consecutive boundaries first.

- **Cost of inserting one element:** At 1-indexed position \(j\), let \(q\) be the number of earlier elements larger than \(P_j\). The element crosses boundaries \(j-1,j-2,\ldots,j-q\), so its cost is
  \[
  (j-1)+(j-2)+\cdots+(j-q)
  =\frac{q(2j-q-1)}2.
  \]

- **Fenwick computation:** A Fenwick tree stores values seen in the prefix. The number of earlier values not exceeding \(x=P_j\) is `sum(x)`, hence
  \(q=(j-1)-\text{sum}(x)\). Each value is inserted once, giving \(O(N\log N)\) time and \(O(N)\) memory.

- **Checks:** The sorted permutation has every \(q=0\), giving 0. For `(3,2,1)`, the insertion costs are \(1\) and \(3\), totaling 4. For `(2,4,1,3,5)`, the nonzero costs are \(3\) and \(3\), totaling 6. Exhaustive enumeration of small permutations agrees with the insertion formula.

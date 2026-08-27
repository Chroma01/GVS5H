- **Optimal strategy:** Repeatedly process values in descending order. When considering value \(v\), values larger than \(v\) have already been fixed at positions \(v+1,\ldots,N\). Move \(v\) monotonically right until it reaches position \(v\), swapping it with each smaller value to its right.
- **Contribution formula:** Let \(p_v\) be the position of \(v\) among only the values \(1,\ldots,v\), in the original permutation. The descending strategy moves \(v\) across boundaries \(p_v,p_v+1,\ldots,v-1\), costing
  \[
  \sum_{j=p_v}^{v-1} j
  =
  \frac{v(v-1)}2-\frac{p_v(p_v-1)}2.
  \]
  Therefore the answer is the sum of these contributions.
- **Fenwick computation:** Process values \(v=1,2,\ldots,N\), storing positions of smaller values in a Fenwick tree. If `bit.sum(pos[v])` is the number of smaller values before \(v\), then
  \[
  p_v=1+\#\{u<v:\operatorname{pos}(u)<\operatorname{pos}(v)\}.
  \]
  Add the contribution above and insert `pos[v]`. Complexity is \(O(N\log N)\), memory is \(O(N)\).
- **Potential-function proof:** Define \(C(P)\) by the formula above for an arbitrary current permutation. Consider swapping adjacent values at positions \(i,i+1\). Only the larger of the two values can change its contribution.
  - If the pair is an inversion \(a>b\), swapping it decreases \(C\) by
    \[
    1+\#\{x<a:x\text{ is before }a\}.
    \]
    This is at most \(i\), since all those smaller elements are among the \(i-1\) positions before \(a\). Thus the actual swap cost \(i\) is at least the potential decrease.
  - If the pair is already ascending, swapping it increases \(C\), so again its nonnegative cost is at least \(C(P)-C(P')\).
  Hence every sequence sorting \(P\) has total cost at least \(C(P)-C(\text{sorted})=C(P)\).
- **Achievability:** In the descending-largest strategy, when value \(v\) is at current position \(j\), it swaps right across boundary \(j\). At that moment its potential decrease is exactly \(j\): all positions before it among the remaining values are smaller, and each prior right-swap has increased this count by one. Therefore every greedy swap pays exactly its potential decrease. The strategy has total cost \(C(P)\), matching the lower bound, and is globally optimal.
- **Integer range:** The answer can be \(O(N^3)\), approximately \(N^3/6\), so 64-bit arithmetic is required in languages with fixed-width integers. Python integers are safe.

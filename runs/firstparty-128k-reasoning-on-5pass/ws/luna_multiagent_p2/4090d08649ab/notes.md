- **Characterization:** For a subarray, let \(S\) be the set of distinct values appearing in it. The minimum number of operations is the number of connected components of \(S\) on the integer line. One operation can erase values only from an interval whose every integer is currently present, so it cannot combine two components separated by a missing value. Conversely, each component can be erased in one operation.
- **Component formula:** The number of components is
  \[
  f(L,R)=|\{x:x\text{ appears in }[L,R]\}|-
  |\{x:x\text{ and }x+1\text{ both appear in }[L,R]\}|.
  \]
  Every adjacent pair of present values joins two otherwise separate components.
- **Latest occurrences:** During a sweep over right endpoint \(R\), let `last[x]` be the latest position at most \(R\) containing value \(x\), or zero if absent. For a fixed left endpoint \(L\), value \(x\) appears in \([L,R]\) exactly when \(L\le last[x]\). Therefore its contribution summed over all \(L\le R\) is `last[x]`.
- **Adjacent pair formula:** Values \(x,x+1\) both appear exactly when
  \[
  L\le \min(last[x],last[x+1]),
  \]
  so the pair contributes \(\min(last[x],last[x+1])\) to the sum over all left endpoints. Hence
  \[
  \sum_{L=1}^{R} f(L,R)
  =
  \sum_x last[x]
  -
  \sum_x \min(last[x],last[x+1]).
  \]
- **Incremental update:** When \(A_R=v\), only `last[v]` changes, from `old` to \(R\). The first sum increases by \(R-old\). In the second sum, only pairs \((v-1,v)\) and \((v,v+1)\) can change; remove their old minima and add their new minima.
- **Complexity:** Each element causes \(O(1)\) updates, so the total time is \(O(N)\) and memory usage is \(O(N)\). Python integers safely handle the answer, whose magnitude can be cubic in \(N\).


## ideation
- The operation depends only on the **set of distinct values** in the subarray; multiplicities and positions do not matter once a value is present.
- For a distinct-value set \(S\), one operation can erase any contiguous interval \([l,r]\subseteq S\). Therefore:
  - Each connected component of \(S\) under adjacency \(x\leftrightarrow x+1\) can be erased in one operation.
  - No operation can erase values from two different components because the missing intermediate value would make the chosen interval invalid.
  - Hence \(f(L,R)\) is the number of connected components of the distinct values.
- Equivalently,
  \[
  f(L,R)=D(L,R)-P(L,R),
  \]
  where \(D(L,R)\) is the number of distinct values and \(P(L,R)\) is the number of values \(x\) such that both \(x\) and \(x+1\) occur in the subarray.
- Sum \(D(L,R)\) by value contributions:
  - For each value \(v\), count subarrays containing \(v\) as
    \[
    \frac{N(N+1)}2-\#\{\text{subarrays avoiding }v\}.
    \]
  - Avoiding subarrays are counted from gaps between consecutive occurrences of \(v\).
- Sum \(P(L,R)\) independently for each adjacent value pair \((x,x+1)\):
  \[
  \#\{\text{contains both}\}
  =T-\#\{\text{avoids }x\}-\#\{\text{avoids }x+1\}
   +\#\{\text{avoids both}\},
  \]
  where \(T=N(N+1)/2\).
- The “avoids both” term can be computed by merging the sorted occurrence lists of \(x\) and \(x+1\) and applying the same gap-counting method.
- Overall complexity is \(O(N)\): every occurrence list participates in at most two adjacent-pair merges.
- Pitfalls:
  - Do not interpret \(l,r\) as subarray positions; they are integer values.
  - Preserve correct inclusion-exclusion signs.
  - Handle absent values and empty occurrence lists.
  - Avoid off-by-one errors in gap lengths: a gap of \(g\) usable positions contributes \(g(g+1)/2\) avoiding subarrays.
  - Use 64-bit arithmetic in fixed-width languages; Python integers avoid overflow.
  - A direct per-subarray distinct-count approach is too slow for \(N=3\cdot10^5\).

## worker: Implement the complete solution: build `pos[v]` oc
- Only the set of distinct values in a subarray matters.
- One operation can erase values from only one consecutive-value component, and each such component can be erased in one operation. Thus `f(L,R)` equals the number of consecutive components among the distinct values.
- For a set of integers, `components = values - adjacent_pairs`, so `f = distinct_count - adjacent_present_pairs`.
- Subarrays containing each value are counted by complement using gaps between its occurrences.
- For each pair `(x, x+1)`, subarrays containing both are counted by inclusion-exclusion, merging their occurrence lists to count subarrays avoiding both.
- Time complexity is `O(N)` because each occurrence list is processed once and merged at most twice. Memory usage is `O(N)`.

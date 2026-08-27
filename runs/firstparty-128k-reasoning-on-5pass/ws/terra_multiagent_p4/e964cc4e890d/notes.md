- **Strong connectivity characterization:** The original directed path permits every forward movement. Therefore the final graph is strongly connected iff every proper prefix cut has at least one added edge from a white vertex in the suffix to a black vertex in the prefix. Such an edge is the only possible way to move backward across that cut.
- **Permutation representation:** Rank black vertices from left to right as \(1,\dots,N\), and likewise rank white vertices. A pairing is a permutation \(p\), where black rank \(i\) is paired to white rank \(p_i\). For a cut after the first \(b\) black vertices and \(w\) white vertices, the backward-crossing requirement is \(\max(p_1,\dots,p_b)>w\).
- **Relevant boundary:** Let `r[b]` be the number of whites before black vertex `b+1`; this is the maximum white-prefix count among cuts having exactly `b` blacks on the left. The required condition is `max(p[1..b]) > r[b]` for all `1 <= b < N`.
- **Bad events:** Define event `E_b` as all first `b` black ranks being matched into the first `r[b]` white ranks. This is exactly failure at the relevant cut. It is impossible when `r[b] < b`, so only cuts with `r[b] >= b` matter.
- **Intersection count:** For selected bad cuts `i < j`, the number of ways to extend the restrictions from cut `i` to cut `j` contributes
  \[
  W(i,j)=\frac{(r[j]-i)!}{(r[j]-j)!}.
  \]
  The initial virtual cut is `i=0`, with the same formula.
- **Inclusion-exclusion recurrence:** Let `dp[j]` be the signed sum of all selected-cut chains ending at actual cut `j`. Then
  \[
  dp[j]=-\frac{\sum_{i<j}dp[i](r[j]-i)!}{(r[j]-j)!},
  \]
  where virtual index `0` has `dp[0]=1`. The final answer is
  \[
  N!+\sum_j dp[j](N-j)!.
  \]
- **Optimization:** The numerator is a convolution-style expression `sum dp[i] * fact(r[j]-i)`. Since relevant `r[j]` values are nondecreasing, CDQ divide-and-conquer computes all such transitions with NTT convolutions in \(O(N\log^2N)\), suitable for `N <= 2e5`.
- **Validation targets:** Small brute force can enumerate all `N!` matchings, check every cut for a suffix-white to prefix-black pair, and compare against the recurrence. Key examples: `BWBW -> 1`, `BBWW -> 2`, alternating length `2N` yields the number of indecomposable permutations for small `N`.

- **Connectivity criterion:** For every proper prefix cut, there must be an added edge directed from the suffix into the prefix. The endpoint cuts imply `S[0] == 'B'` and `S[-1] == 'W'`; otherwise the answer is zero.
- **Permutation model:** Number white vertices from left to right and black vertices from left to right. If black `j` is paired with white `p[j]`, each pairing is a permutation `p`.
- **Internal constraints:** Let `a[k]` be the number of whites before black `k+1`, for `1 <= k < N`. The cut before black `k+1` is crossed backward exactly when `max(p[1], ..., p[k]) > a[k]`. Thus every such inequality must hold.
- **Bad events:** Event `E_k` is `p[1], ..., p[k] <= a[k]`. If `a[k] < k`, it is impossible. Inclusion-exclusion over these events gives the answer.
- **Recurrence:** If `g[k]` is the signed sum for subsets whose largest event is `k`, then
  `g[k] = -inv_fact[a[k]-k] * sum_{j<k}(g[j] * fact[a[k]-j])`.
  The final result is `N! + sum(g[k] * (N-k)!)`.
- **CDQ convolution:** At a CDQ node `[left, right)`, contributions from indices in the left half to targets in the right half are computed by convolving `g[left:mid]` with the factorial sequence. For target `k`, coefficient `a[k]-left` equals `sum(g[j] * fact[a[k]-j])`.
- **Validation:** Exhaustive brute-force comparison over every balanced string for `N <= 5`, including endpoint-invalid strings, impossible configurations, and valid cases, agrees with the implementation.
- **Complexity:** CDQ with NTT convolution runs in `O(N log^2 N)` time and uses near-linear working memory across recursion levels.

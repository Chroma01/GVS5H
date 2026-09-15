- **Core reduction:** For each edge `i` (edge from `i` to its parent, weight `A_i`), the total answer is `(N-1)!` times the probability that this edge lies on the path between `u` and `v`. By linearity, sum `A_i * probability` over all edges.
- **Subtree criterion:** Edge `i` lies on the path between `u` and `v` iff exactly one of `u, v` is in the subtree of `i` in the rooted random recursive tree.
- **Random recursive tree probabilities:** For fixed `i`, define `X_t = 1` if vertex `t` is in the subtree of `i`. For `t > i`, the sequence `X_{i+1}, X_{i+2}, ...` follows a Pólya urn with initial black count `1` (vertex `i`) and white count `i-1`. Therefore, for `x > i`, `P(X_x = 1) = 1/i`, and for `i < x < y`, `P(X_x = X_y = 1) = 2/(i(i+1))`.
- **Coefficient for `i < u < v`:** Both endpoints are larger than `i`. The edge is used iff exactly one endpoint is in the subtree of `i`. Thus probability is `2/i - 2 * 2/(i(i+1)) = 2(i-1)/(i(i+1))`. For `i=1`, this is `0`, matching the absence of edge `1`.
- **Coefficient for `i = u`:** Vertex `u` is always in its own subtree. The edge is used iff `v` is not in the subtree of `u`, giving probability `1 - 1/u`. For `u=1`, this is `0`, again matching no edge `1`.
- **Coefficient for `u < i < v`:** Since `i > u`, vertex `u` cannot be in the subtree of `i`. The edge is used iff `v` is in the subtree of `i`, giving probability `1/i`.
- **Coefficient for `i = v`:** Vertex `v` is always in its own subtree and `u < v` cannot be in it, so the edge is always on the path. Probability is `1`.
- **Coefficient for `i > v`:** Neither endpoint can be in the subtree of `i`, so probability is `0`.
- **Prefix-sum formula:** Let `pref_b[k] = sum_{i=2..k} A_i * 2(i-1)/(i(i+1))` and `pref_c[k] = sum_{i=2..k} A_i/i`. For query `u < v`, expected distance modulo `MOD` is:
  `pref_b[u-1] + (u>=2 ? A_u*(1-1/u) : 0) + (v>u+1 ? pref_c[v-1]-pref_c[u] : 0) + A_v`.
  Multiply by `(N-1)!` modulo `MOD`.
- **Implementation details:** Precompute inverses up to `N+1` in linear time, build the two prefix arrays, compute `(N-1)!`, and answer each query in `O(1)`. All arithmetic is modulo `998244353`, which is larger than all denominators used.
- **Edge cases:** `u=1` gives no edge `1` and empty left prefix. Adjacent `v=u+1` gives empty middle prefix. `N=2` gives only edge `2`, always used for query `(1,2)`.
- **Verification:** The formula matches brute force for small `N` and the provided samples. Previous candidate approaches such as root-LCA decomposition or direct counting collapse to the same ancestor/subtree probability formulas and are not needed.

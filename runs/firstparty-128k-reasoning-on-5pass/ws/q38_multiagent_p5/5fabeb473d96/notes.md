- **Reduction:** Each parent sequence is a uniformly random recursive tree. The required sum over all `(N-1)!` trees is `(N-1)!` times the expected distance between `u` and `v`.
- **Edge contribution:** For the edge entering vertex `x` with weight `A_x`, it lies on the `u-v` path exactly when `x` is in the subtree of exactly one endpoint after removing that edge.
- **Ancestor probabilities:** For `x < y`, `Pr(x is an ancestor of y) = 1/x`. For `x < u < v`, `Pr(x is an ancestor of both u and v) = 2/(x(x+1))`. This follows from the Pólya-urn/exchangeability view of subtree growth in random recursive trees.
- **Coefficient cases for `u < v`:**
  - `x < u`: probability `2/x - 2 * 2/(x(x+1)) = 2(x-1)/(x(x+1))`.
  - `x = u`: probability `1 - 1/u = (u-1)/u`.
  - `u < x < v`: probability `1/x`.
  - `x = v`: probability `1`.
  - `x > v`: probability `0`.
- **Prefix sums:**
  - `pref1[i] = sum_{x=2}^i A_x * 2(x-1)/(x(x+1))`.
  - `pref2[i] = sum_{x=2}^i A_x / x`.
  - `spec[i] = A_i * (i-1)/i`, computed as `A_i - A_i * inv[i]`.
- **Query formula:** For `u < v`, expected distance is  
  `pref1[u-1] + spec[u] + (pref2[v-1] - pref2[u]) + A[v]`.  
  Multiply by `(N-1)!` modulo `998244353`.
- **Implementation details:** Precompute modular inverses up to `N+1` in linear time. Reduce all `A_i` modulo `MOD`. Use one pass to build `pref1`, `pref2`, and `spec`. Answer each query in `O(1)`.
- **Edge cases:** `u = 1` makes `spec[u]` and `pref1[u-1]` zero. `v = u + 1` makes the middle range empty. `N = 2` gives `fact = 1` and answer `A_2`. Vertex `1` has no incoming edge, so no `A_1` term exists.
- **Sample tests:** Sample 1, Sample 2, and Sample 3 all match the expected outputs. Small brute-force checks for `N <= 7`, including `u = 1`, consecutive pairs, and `N = 2`, also match.

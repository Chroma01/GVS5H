- **Core reduction:** The answer is `(N-1)!` times the expected weighted distance in a random recursive tree. By linearity over edges, for query `u < v`, sum `A_i * Pr(edge i lies on path u-v)` over `i=2..N`, then multiply by `(N-1)!`.
- **Edge-on-path condition:** Edge `i` is on the path between `u` and `v` iff vertex `i` is an ancestor of exactly one of `u` and `v`, counting a vertex as an ancestor of itself. Since parent labels are smaller than child labels, edges with `i > v` never contribute.
- **Ancestor probabilities:** For `i < j`, `Pr(i is ancestor of j) = 1/i`. For `i < u < v`, the joint probability that `i` is an ancestor of both `u` and `v` is `2/(i(i+1))`, independent of `u` and `v`. Therefore the probability that `i` is an ancestor of exactly one of them is `2/i - 2*2/(i(i+1)) = 2(i-1)/(i(i+1))`.
- **Closed-form coefficients:** For query `u < v`:
  - `i = v`: coefficient `1`.
  - `u < i < v`: coefficient `1/i`.
  - `i = u > 1`: coefficient `1 - 1/u = (u-1)/u`.
  - `2 <= i < u`: coefficient `2(i-1)/(i(i+1))`.
  - If `u = 1`, the `i = u` term is absent and the formula reduces to root-to-`v` path probabilities.
- **Prefix sums:** Precompute:
  - `pref_inv[k] = sum_{i=2..k} A_i / i`.
  - `pref_pre[k] = sum_{i=2..k} A_i * 2(i-1)/(i(i+1))`.
  - `self_coef[i] = A_i * (i-1)/i`.
  Then each query is answered as:
  `pref_pre[u-1] + self_coef[u] + (pref_inv[v-1] - pref_inv[u]) + A[v]`, with the `self_coef[u]` term omitted when `u=1`.
- **Modular arithmetic:** All coefficients are rational with denominators at most `N+1`, which are invertible modulo `998244353`. Precompute inverses in `O(N)` using the standard linear inverse recurrence. Multiply the final expected value by `(N-1)!`.
- **Complexity:** Precomputation is `O(N)`, each query is `O(1)`, total `O(N+Q)` time and `O(N)` memory.
- **Verification:** The formula matches the samples. For `N=4` and all weights `1`, brute enumeration over the `6` recursive trees gives distance sums `(1,2)=6`, `(1,3)=9`, `(1,4)=11`, `(2,3)=9`, `(2,4)=11`, `(3,4)=12`, which are exactly produced by the closed-form coefficients. Edge cases `N=2`, `u=1`, and adjacent queries `v=u+1` are handled by zero-length prefix ranges.

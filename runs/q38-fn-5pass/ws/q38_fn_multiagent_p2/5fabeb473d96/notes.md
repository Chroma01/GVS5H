- **Core reduction:** There are `(N-1)!` equally likely parent sequences. By linearity of expectation, the required sum is `(N-1)!` times the expected distance. Edge `i` (weight `A_i`) contributes exactly when removing it separates `u` and `v`, i.e. exactly one of `u,v` lies in the subtree of `i`.
- **Pólya urn view:** Fix `i`. For labels `k > i`, mark `k` as a success if it is in the subtree of `i`. Immediately after vertex `i` exists, there is `1` success (vertex `i`) and `i-1` failures (all previous vertices). When vertex `k` arrives, it is a success with probability current successes / `(k-1)`; then the success count increases by `1`, otherwise the failure count increases by `1`. This is a Pólya urn with initial `(1, i-1)`, so the success/failure sequence for `k > i` is exchangeable.
- **Basic probabilities:** For any one future label, the probability it is in the subtree of `i` is `1/i`. For two future labels, the probability exactly one is in the subtree is `Pr(SF)+Pr(FS) = (1/i)((i-1)/(i+1)) + ((i-1)/i)(1/(i+1)) = 2(i-1)/(i(i+1))`.
- **Case split for `u < v`:**
  - `i > v`: neither `u` nor `v` can be a descendant of `i`, probability `0`.
  - `i = v`: `v` is always in its own subtree and `u < v` cannot be, probability `1`.
  - `u < i < v`: only `v` is future relative to `i`, probability `1/i`.
  - `i = u`: `u` is always in its own subtree; separation occurs iff `v` is not in the subtree of `u`, probability `1 - 1/u`.
  - `2 <= i < u`: both `u` and `v` are future relative to `i`, probability `2(i-1)/(i(i+1))`.
- **Query aggregation:** Precompute prefix sums of `A_i / i` and `A_i * 2(i-1)/(i(i+1))`. For a query, the expected distance is:
  `A_v + A_u(1 - 1/u) + sum_{i=u+1}^{v-1} A_i/i + sum_{i=2}^{u-1} A_i*2(i-1)/(i(i+1))`.
  If `u = 1`, the `A_u` term is absent; setting `A_1 = 0` and using empty ranges handles it.
- **Implementation details:** Use linear modular inverses up to `N+1`, reduce all `A_i` modulo `998244353`, and multiply the final expected value by `(N-1)!`. Prefix differences are taken modulo `MOD`. Complexity is `O(N + Q)` time and `O(N)` memory. Edge cases include `N = 2`, `u = 1`, and empty summation ranges.

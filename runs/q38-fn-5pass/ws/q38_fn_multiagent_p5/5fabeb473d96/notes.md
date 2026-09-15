- **Core idea:** The required sum over all `(N-1)!` recursive trees equals `(N-1)!` times the expected distance in a uniformly random recursive tree. Use linearity of expectation over edges. Edge `k` has weight `A_k` and lies on the path between `u` and `v` iff removing it separates `u` and `v`, i.e. exactly one endpoint is in the subtree of `k`.
- **Subtree probabilities:** In a random recursive tree, for `k < x`, the probability that `x` is in the subtree of `k` is `1/k`. This follows by induction from the Pólya-urn-like growth of the subtree of `k`.
- **Joint probability:** For fixed `k` and two distinct vertices `u, v > k`, the probability that both are in the subtree of `k` is `2 / (k(k+1))`. More generally, for `m` specified later vertices, the probability all are descendants of `k` is `(m-1)! / (k(k+1)...(k+m-1))`.
- **Coefficients for query `u < v`:**
  - Edge `v`: always on the path, coefficient `1`.
  - Edges `u < k < v`: only `v` can be in subtree `k`, coefficient `1/k`.
  - Edge `k = u` when `u >= 2`: `u` is always in its own subtree, so edge is on path iff `v` is not, coefficient `1 - 1/u = (u-1)/u`.
  - Edges `2 <= k < u`: both endpoints are larger than `k`; exactly one is in subtree `k` with probability `2/k - 2 * 2/(k(k+1)) = 2(k-1)/(k(k+1))`.
- **Prefix sums:** Precompute modulo `998244353`:
  - `pref_inv[i] = sum_{k=2}^i A_k / k`
  - `pref_c[i] = sum_{k=2}^i A_k * 2(k-1)/(k(k+1))`
  Then for `u < v`, expected distance is:
  `A_v + (pref_inv[v-1] - pref_inv[u]) + [u>=2] * (A_u*(u-1)/u + pref_c[u-1])`.
- **Modular arithmetic:** All probabilities are represented using modular inverses. Since `N <= 2e5 < MOD`, all needed denominators are invertible. Multiplying the modular expected value by `(N-1)!` gives the required sum modulo `MOD`.
- **Implementation details:** Read all integers at once, precompute inverses in linear time, build two prefix arrays, compute `(N-1)!`, and answer each query in `O(1)`. Keep `A[1] = 0` and prefix arrays zero-initialized so `u = 1` needs no special prefix handling except skipping the `k = u` term.
- **Edge cases:** `N = 2`, `u = 1`, and adjacent vertices `v = u + 1` are handled naturally: empty prefix differences become zero, and there is no edge for vertex `1`.
- **Verification:** The formula matches the samples and small brute-force enumerations for `N <= 4`, including nontrivial cases where both endpoints are larger than an edge index.

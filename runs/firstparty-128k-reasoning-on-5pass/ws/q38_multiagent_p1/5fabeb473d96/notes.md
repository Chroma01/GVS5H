- **Random model:** Every parent sequence is equally likely, and there are `(N-1)!` of them. Therefore the required sum is `(N-1)!` times the expected distance in a random recursive tree.
- **Edge separation:** Edge `i` (between `i` and its parent) lies on the path between `u` and `v` iff the rooted subtree of `i` contains exactly one of `u` and `v`. Labels increase away from the root, so vertex `i` can only have descendants with labels greater than `i`.
- **Ancestor probabilities:** For `i < x`, `P(i is an ancestor of x) = 1/i`. For `i < x < y`, `P(i is an ancestor of both x and y) = 2/(i(i+1))`. These follow from the Pólya-urn process for the subtree size of `i`, starting with one vertex in the subtree and `i-1` outside it.
- **Edge coefficients:** For a query `u < v`, the probability that edge `i` separates the endpoints is:
  - `2(i-1)/(i(i+1))` if `i < u`
  - `1 - 1/u` if `i = u`
  - `1/i` if `u < i < v`
  - `1` if `i = v`
  - `0` if `i > v`
  The `i = u` case is special because one endpoint is the subtree root itself, so the two-future-vertices joint formula does not apply directly.
- **Prefix sums:** Set `A[1] = 0`. Define:
  - `S1[t] = sum_{k=2..t} A_k * 2(k-1)/(k(k+1))`
  - `S2[t] = sum_{k=2..t} A_k / k`
  Then the expected distance for `u < v` is:
  `S1[u-1] + A[u] * (1 - 1/u) + (S2[v-1] - S2[u]) + A[v]`.
  The final answer is this value multiplied by `(N-1)!` modulo `998244353`.
- **Modular arithmetic:** All divisions are performed using modular inverses. Since `N <= 2e5 < MOD`, inverses up to `N+1` exist. Precompute them with the linear recurrence `inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD`.
- **Complexity:** Precomputation is `O(N)`, each query is `O(1)`, total `O(N + Q)` time and `O(N)` memory.
- **Edge cases:** `u = 1` makes the `A[u]` term zero because `A[1] = 0` and `1 - 1/1 = 0`. `v = u + 1` makes the middle range empty. `N = 2` gives `fact = 1` and answer `A_2`.
- **Validation:** Sample 1 and Sample 2 match. A brute-force enumeration of all parent sequences for small `N <= 6`, computing distances directly, agrees with the prefix-sum formula; symbolic checks for `N = 4` also match all pair sums.

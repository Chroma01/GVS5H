
## ideation
- The binary-search plan is sound: feasibility is monotone in target `T`, and since all `points[i] > 0`, “at most `m`” is enough—extra moves can be burned on back-and-forth cycles without lowering the minimum.
- Core difficulty is the feasibility test: for fixed `T`, compute required visits `need[i] = ceil(T / points[i]) >= 1`, then ask for the minimum length of a walk starting at `-1` on a path that visits every index `i` at least `need[i]` times. Naive simulation is impossible because `m` and `need[i]` can be huge.
- Key structure: because every index needs at least one visit for `T > 0`, any positive target requires reaching index `n-1` at least once, so if `m < n` the answer is `0`. The first move is forced to `0`, and the walk can never return to `-1`.
- A promising exact model: choose the final ending index `e`. For each edge `i--(i+1)`, let `L[i]` be the number of leftward traversals. Flow conservation gives rightward traversals `= L[i] + 1` for edges left of `e`, otherwise `= L[i]`. Total moves become `1 + e + 2 * sum(L)`. Visit requirements turn into lower bounds on `L[0]`, adjacent sums `L[i-1] + L[i]`, and `L[n-2]`, with a one-visit “discount” for vertices `<= e`. This is a path covering LP that should be integral and solvable by greedy/DP; the remaining challenge is minimizing over `e` in `O(n)`.
- Do not assume the optimal end is always `n-1`; e.g. requirements like `[1,100,1]` favor ending at the high-demand middle index. Also beware layer/threshold decomposition: sets `{i : need[i] >= k}` are nested but can be disconnected, which breaks simple interval arguments.
- Pitfalls: ceil division; very large `need[i]`; overflow in non-Python languages; exact-`m` parity confusion; forgetting the forced first move; disconnected high-demand indices; and keeping feasibility `O(n)` so total is about `O(n log(max(points)*m))`.

## worker: Derive and prove the feasibility lemma for a fixed
- For a fixed target `T`, set `need[i] = ceil(T / points[i])`. For `T > 0`, every `need[i] >= 1`, so any feasible walk must reach `n-1`; hence `m < n` immediately rejects positive targets.
- Fix the ending index `e`. Let `L[i]` be the number of leftward traversals across edge `(i, i+1)`. Flow conservation from start `-1` to end `e` gives rightward traversals `R[i] = L[i] + 1` for `i < e`, otherwise `R[i] = L[i]`. Thus total moves are `1 + sum(R[i]+L[i]) = e + 1 + 2*sum(L)`.
- Visit counts become:
  - `v[0] = 1 + L[0]`
  - `v[j] = L[j-1] + L[j] + 1_{j <= e}` for `1 <= j <= n-2`
  - `v[n-1] = L[n-2] + 1_{e = n-1}`
  With `d[j] = need[j]-1` for `j <= e` and `d[j] = need[j]` for `j > e`, the constraints are exactly `L[j-1] + L[j] >= d[j]` on a path, omitting missing endpoints.
- Minimizing `sum(L)` subject to those vertex-demand constraints is a path covering LP. Its dual is `max sum d[j]y[j]` with `y[j]+y[j+1] <= 1`, i.e. fractional independent set on a path. Since a path is bipartite, this polytope is integral, so the dual optimum is MWIS(`d`). By strong duality/integrality, `min sum(L) = MWIS(d)`, giving `min_moves(e) = e + 1 + 2*MWIS(d)`.
- To evaluate all ends in `O(n)`, write `a=need`, `b=need-1`. For end `e`, weights are `b` on the prefix `<=e` and `a` on the suffix `>e`. An MWIS either excludes `e`, splitting into independent prefix/suffix problems, or includes `e`, excluding `e-1` and `e+1`. Prefix DP over `b` and suffix DP over `a` combine in `O(1)` per end.
- The included brute force BFS caps counts at `need`, which is safe because extra visits never change feasibility. Exhaustive `n<=4, need in 1..3` and 500 random tiny cases all matched the formula.

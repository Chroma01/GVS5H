
## ideation
Core difficulty: the kept graph must be a connected induced subtree with a very rigid 2-level shape: one red center, `x` blue neighbors, and every blue has exactly the same number `y` of kept leaf children. The global parameter `y` couples all branches, so a naive rooted DP that chooses different branch sizes independently is invalid.

Key structural observation: for a fixed red center `r`, each neighbor `b` can be blue only if it has at least `y` neighbors other than `r`, i.e. `deg(b)-1 >= y`. For fixed `r` and `y`, keeping every eligible neighbor is optimal because each blue branch contributes `y+1` vertices and branches cannot interfere in a tree. Thus if capacities `c_b = deg(b)-1` are sorted descending, choosing the `k` best branches forces `y = c_k`, giving kept size `1 + k*(c_k+1)`. Maximize over all `r` and feasible `k`; answer is `N - max_kept`.

Important pitfalls: `x,y` must be positive, so capacities `0` cannot be used as the limiting branch; red center may be a leaf in the original tree, as in a 3-vertex path; do not assume all neighbors of `r` are kept—unselected neighbors are deleted; induced-subgraph cross edges are not an issue because the input is a tree, but the proof should state this; off-by-one in kept count `1+x+xy`; complexity must be near `O(sum deg log deg)`, not `O(N^2)`.

## worker: finalize
- **Model**: A Snowflake Tree kept inside T is determined by its red center `r`, a set of `x` blue neighbors of `r`, and for each blue vertex `b`, exactly `y` kept neighbors of `b` other than `r`. Since T is a tree, no cross edges can appear in the induced kept subgraph, so branches are independent.
- **Fixed center**: For a fixed `r`, each neighbor `b` has capacity `c_b = deg(b) - 1` (usable leaves excluding `r`). For a fixed `y`, every neighbor with `c_b >= y` can be included, and including it is always beneficial (adds `y+1` vertices). Hence, sorting capacities descending and picking the top `k` forces `y = c_k`, giving kept size `1 + k*(c_k + 1)`. We maximize over all `r` and all feasible `k` with `c_k >= 1` (since `y >= 1`, and `k >= 1` since `x >= 1`).
- **Correctness on samples**:
  - Sample 1: center 4, capacities {2,2,0} → `k=2` gives `1+2*3=7`, answer `8-7=1`. ✓
  - Sample 2: center 1 (a leaf), neighbor 2 has capacity `deg(2)-1 = 1` → kept `1+1*2=3`, answer `0`. This shows the red center may be a leaf of T, which the algorithm handles since every vertex is tried as center. ✓
- **Complexity**: Sorting per vertex costs `O(deg(r) log deg(r))`; total `O(Σ deg log deg) ≤ O(N log N)`, well within limits for `N ≤ 3×10^5`. Memory `O(N)`.
- **Edge cases**: Leaf centers, centers whose neighbors all have capacity 0 (skipped via the `c < 1` break), and the guarantee that a Snowflake Tree always exists (minimum kept is 3, e.g., a path of 3) ensure `best` is always set.

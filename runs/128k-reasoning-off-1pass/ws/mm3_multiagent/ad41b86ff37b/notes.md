
## ideation
The problem requires finding the minimum number of vertex deletions from a tree so that the remaining induced subgraph is a "Snowflake Tree". A Snowflake Tree consists of a center vertex connected to `x` blue vertices, each blue vertex connected to `y` leaves (with `x, y \ge 1`). 

For a fixed center `c`, any neighbor `v` of `c` can either:
1. Be deleted entirely (along with its subtree), or
2. Become a blue vertex: we keep `v` and exactly `y` of its other neighbors as leaves, deleting everything else in `v`'s subtree.

For `v` to be a blue with `y` leaves, it must have at least `y` children in the rooted tree at `c` (i.e., `deg(v) - 1 \ge y`). For a fixed `y`, we should make all qualifying neighbors into blues to maximize the number of kept vertices. The kept count is `1 + cnt(c, y) * (1 + y)`, where `cnt(c, y)` is the number of neighbors of `c` with `deg(v) - 1 \ge y`.

To maximize efficiently for each `c`: collect the values `k_v = deg(v) - 1` for all neighbors `v` with `k_v \ge 1`, sort them in descending order, and compute `max_i i * (1 + a_i)` where `a_i` is the `i`-th largest. This works because for a fixed count `i`, the function `(1 + y) * i` is increasing in `y`, so the maximum over the interval where `cnt = i` occurs at the largest possible `y`, which is `a_i`.

The overall answer is `N - max_kept` over all possible centers. Complexity: O(N log N) due to sorting neighbor lists, which is efficient for N up to 3e5.

## worker: Implement the solution: read N, build adjacency li
The solution iterates over each vertex as a potential center of the Snowflake Tree. For each center `c`, it collects the number of available "children" (neighbors other than `c`) for each neighbor `v`, keeping only those with at least one child (`k_v >= 1`), as they are the only candidates to become blue vertices. Sorting these values in descending order allows efficient computation of the maximum possible kept vertices: for a given count `i` of blues, the optimal number of leaves `y` is the largest available `k` among those `i` blues, giving value `i * (1 + k)`. The global maximum over all centers gives the size of the largest induced Snowflake Tree, and the answer is `N - max_kept`. This runs in O(N log N) time due to sorting, which is well within the limits for N up to 3×10⁵.

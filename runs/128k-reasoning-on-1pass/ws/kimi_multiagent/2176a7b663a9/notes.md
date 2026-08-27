
## ideation
Core difficulty: the disjointness graph can have Θ(N²) edges, so it must be queried implicitly. The useful structure is that “interval i is completely before interval j” (`R_i < L_j`) is an interval order; the graph is its comparability graph, equivalently the complement of an interval graph. Such a graph has no induced `2K2`, hence no induced `P5`; since any shortest weighted path with positive weights must be induced/chordless, a minimum path has at most 3 edges.

Key consequences:
- If `[L_s,R_s]` and `[L_t,R_t]` are disjoint, the direct edge exists and is optimal because all weights are positive: answer `W_s + W_t`.
- If they intersect, only need to consider:
  - one common neighbor `x`: `x` is strictly left of both intervals or strictly right of both;
  - two intermediates `a,b` on opposite outer sides: `a` left of `s` and `b` right of `t`, or `a` right of `s` and `b` left of `t`.
- Same-side two-intermediate cases are dominated by a common-neighbor path: the outer/earlier interval would also be disjoint from the other endpoint.
- Range minima suffice: prefix minimum weight by right endpoint gives cheapest interval with `R < x`; suffix minimum by left endpoint gives cheapest with `L > x`. Coordinates are bounded by `2N`, so this is `O(N)` preprocessing and `O(1)` per query.

Pitfalls:
- Inclusive integer intervals mean disjointness is strict: `R_i < L_j` or `R_j < L_i`; use `L-1` / `R+1` carefully.
- Intersection test is `L_s <= R_t && L_t <= R_s`.
- A 3-edge path can beat a 2-edge path even when a common neighbor exists, because two cheap non-common intermediates may be cheaper than one expensive common neighbor.
- Do not run Dijkstra/BFS on an explicit graph; also avoid assuming unweighted diameter alone bounds weighted paths without the induced-path argument.
- Use 64-bit sums: up to four weights of `1e9`.
- Handle `INF` carefully; if no valid 1-, 2-, or 3-edge candidate exists in the intersecting case, output `-1`.

## worker: Implement the complete Python solution: parse inpu
- Implemented exactly per plan: the disjointness graph is queried implicitly using the interval-order structure.
- Preprocessing (coordinates bounded by `2N`):
  - `pref[x]` = minimum weight among intervals with `R <= x`, so the cheapest interval strictly left of coordinate `c` is `pref[c-1]`.
  - `suff[x]` = minimum weight among intervals with `L >= x`, so the cheapest interval strictly right of `c` is `suff[c+1]`.
- Per query (`s`, `t`):
  - If intervals are disjoint (`R_s < L_t` or `R_t < L_s`), the direct edge is optimal (positive weights): answer `W_s + W_t`.
  - Otherwise (they intersect), by the P5-free / induced-path argument a minimum path has at most 3 edges, and only these forms exist:
    - 2 edges via a common neighbor, which must lie strictly left of both intervals (`pref[min(L_s,L_t)-1]`) or strictly right of both (`suff[max(R_s,R_t)+1]`).
    - 3 edges `s-a-b-t` with `a` strictly left of `s` and `b` strictly right of `t`, or the mirrored arrangement. Validity of `a-b` follows from `R_a < L_s <= R_t < L_b` since `s,t` intersect; the two choices are independent, so range minima suffice.
  - Take the minimum candidate; output `-1` if none exists.
- Verified the common-neighbor dichotomy: any interval disjoint from two intersecting intervals must be entirely left of both or entirely right of both. Also verified that in a chordless 3-edge path the two intermediates must lie on opposite outer sides (same-side placement forces a chord, contradiction).
- INF-safe arithmetic (only sum when components `< INF`); 64-bit-safe values; indices `pref[0]` and `suff[2N+1]` are INF sentinels.
- Complexity: `O(N + Q)` time, `O(N)` memory. Hand-checked against Sample 1 (answers 11, 6, -1).

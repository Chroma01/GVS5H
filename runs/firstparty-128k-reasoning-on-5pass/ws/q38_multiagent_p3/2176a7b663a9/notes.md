- **Core observation:** An edge exists exactly when one interval ends before the other starts, i.e. `R_i < L_j` or `R_j < L_i`. Touching at an integer is an intersection, so all comparisons are strict.
- **Direct case:** If query intervals `s` and `t` are disjoint, the edge `s-t` exists. Since all vertex weights are positive, any other path adds positive vertex weights, so the answer is `W_s + W_t`.
- **Compression lemma:** Assume `s` and `t` intersect. Take any path from `s` to `t` and let `x` be the first internal vertex, `y` the last internal vertex. If `x = y`, remove the cycle and get `s-x-t`. If `x != y`, then `x` is disjoint from `s` and `y` is disjoint from `t`. Classify `x` and `y` as left/right of `s` and `t`. If both are on the same side, one of them is disjoint from both `s` and `t` (using `L_s <= R_t` and `L_t <= R_s`), giving a 2-edge path. If they are on opposite sides, they are automatically disjoint: left-of-s plus right-of-t gives `R_x < L_s <= R_t < L_y`, and right-of-s plus left-of-t gives `R_y < L_t <= R_s < L_x`. Thus `s-x-y-t` is a valid 3-edge path. In every case, a path of at most 3 edges has no larger weight, so the optimum is among 2-edge and two 3-edge forms.
- **Candidate forms:** For intersecting `s,t`:  
  1. 2-edge via a vertex left of both: `R < min(L_s, L_t)`.  
  2. 2-edge via a vertex right of both: `L > max(R_s, R_t)`.  
  3. 3-edge with first left of `s` and last right of `t`: `R < L_s` and `L > R_t`.  
  4. 3-edge with first right of `s` and last left of `t`: `L > R_s` and `R < L_t`.  
  The answer is `W_s + W_t` plus the minimum middle weight, or sum of two middle weights, among these.
- **Precomputation:** Build arrays over coordinates `0..2N+3`. Put the minimum weight at each `R` coordinate and each `L` coordinate. A forward scan converts the `R` array into `pref[x] = min W_i with R_i < x`. A backward scan converts the `L` array into `suff[x] = min W_i with L_i > x`. The scan stores the current minimum before including the current coordinate, enforcing strict inequality.
- **Query formula:** If `R_s < L_t` or `R_t < L_s`, print `W_s + W_t`. Otherwise compute  
  `best = min(pref[min(L_s,L_t)], suff[max(R_s,R_t)], suff[R_s] + pref[L_t], suff[R_t] + pref[L_s])`.  
  If `best` is `INF`, print `-1`; otherwise print `W_s + W_t + best`.
- **Distinctness:** In the intersecting case, endpoints cannot appear in these sets, and the two sets in a 3-edge term cannot contain the same vertex because `L_i <= R_i` together with `L_t <= R_s` and `L_s <= R_t` make the required inequalities impossible. Therefore independent minima are safe.
- **Complexity:** `O(N + Q)` time and `O(N)` memory. The input is read all at once; the two scan arrays are about `2N + 4` long.
- **Verification:** Samples 1 and 2 match by hand. The compression lemma covers all possible longer paths, and a brute-force explicit-graph Dijkstra checker is the natural small-random validation for this formula.

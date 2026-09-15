- **Goal:** maximize over `1 <= i < j <= N-1` of `pre[i] + distinct(i+1..j) + suf[j+1]`.
- **Key reformulation (one update per step):** `distinct(i+1..j) = #{j' in [i+1,j] : prev[j'] <= i}`. Using `#{j'<=j: prev[j']<=i} - #{j'<=i: prev[j']<=i}` and the fact every `j'<=i` satisfies `prev[j'] <= i` (so that second count is exactly `i`), we get
  `distinct(i+1..j) = P_j(i) - i`, where `P_j(i) = #{j' <= j : prev[j'] <= i}`.
  Hence `D_j(i) = pre[i] + distinct(i+1..j) = (pre[i] - i) + P_j(i)`, valid for every queried `i < j`.
- **Update:** advancing to `j` adds `+1` to `P_j(i)` for all `i >= max(1, prev[j])`, i.e. a single suffix add. In a difference array `dB` this is one point update `dB[max(0,prev[j]-1)] += 1`. No compensating `-1` is needed.
- **Base:** leaf `idx = i-1` starts with `base[i] = pre[i] - i`; tree stores `base[i] + prefixsum(dB, i)` folded in.
- **Segment tree (no lazy):** node = `(s, m)` with `s = sum of dB`, `m = max over p of (base[p] + sum dB from node-left to p)`. Merge: `s = s_l + s_r`, `m = max(m_l, s_l + m_r)`. Point update O(log N), prefix-max query O(log N).
- **Prefix query simplification:** for `[0,q)` the left pointer never triggers in the ACL iterative loop, so only right-side nodes are taken, combined right-to-left: `best = max(m_node, s_node + best)`. No need to track accumulator sum for the max.
- **Sweep order:** for `j = 1..n-1`: apply update for `j`, then if `j>=2` query prefix `[0, j-1)` (i.e. `i in [1,j-1]`) and set `ans = max(ans, best + suf[j+1])`. The `j=1` update must be applied (defines `P` including `j'=1`).
- **Indexing / bounds:** `i,j` are 1-indexed; first cut `i in [1,j-1]`, second cut `j in [2,n-1]`. `prev[j] <= j-1` keeps `p0 <= n-3 < n`. `suf` sized `n+2` so `suf[n]` is safe.
- **Complexity:** O(N log N) time, O(N) memory. One point update + one prefix query per step (~1.1e7 tight loop iterations at N=3e5).
- **Verification:** matches sample 1 (5), sample 2 (9), and hand-checked cases `[1,2,3]`->3, `[1,1,1]`->3, `[1,2,1,2]`->4, `[1,2,1,2,1]`->5.
- **Traps avoided:** the wrong `D = |T_j| + (pre[i]-c_j(i))` form (missing that `distinct = |T_j| - c_j(i)`, sign error); using two point updates (`+1` at L and `-1` at R+1) which is correct but does double the work — the `P_j(i) - i` reformulation removes the `-1` entirely.

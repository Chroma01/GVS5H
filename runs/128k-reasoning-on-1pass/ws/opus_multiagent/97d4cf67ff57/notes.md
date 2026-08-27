
## ideation
**Reformulation (core insight).**
An alkane subgraph is fully described by its set `S` of degree‑4 vertices:
- Sum of degrees: `4k + L = 2(k+L-1)` where `k=|S|`, `L`=#leaves ⇒ `L = 2k+2`, total vertices `= 3k+2`. So maximizing vertices ⇔ maximizing `k = |S|`.
- `S` must induce a connected subtree of `T` (internal vertices of a tree are connected).
- Every `v ∈ S` needs 4 neighbors in the alkane, so `deg_T(v) ≥ 4`, and it can be adjacent to at most 4 chosen vertices: `deg_S(v) ≤ 4`.
- Conversely, any connected `S ⊆ {v : deg_T(v) ≥ 4}` (connected via T‑edges) with `deg_S(v) ≤ 4` for all `v` yields a valid alkane: each `v` hangs `4 − deg_S(v)` extra T‑neighbors as leaves; enough exist since `deg_T(v) ≥ 4`.
- **No conflict between leaves**: a vertex `u ∉ S` adjacent to two vertices of `S` would create a cycle (since `S` is connected) — impossible in a tree. So leaf assignments are automatically disjoint. This is the step most likely to be hand‑waved; it's true and important.
- `k = 1` is allowed (single deg‑≥4 vertex ⇒ answer 5).

**Reduced problem.** Build induced forest `G` on `V' = {v : deg_T(v) ≥ 4}` keeping T‑edges with both endpoints in `V'`. Find max‑size connected subtree of `G` with max degree ≤ 4 inside the chosen set. Answer = `3·best + 2`; print `-1` if `V'` is empty (i.e., no vertex of degree ≥ 4).

**DP.** Root each component of `G`. For node `v` with children `c` (in `G`):
- `dp[v] = 1 + (sum of the 3 largest dp[c])` — reserve one slot for the parent edge.
- Candidate answer (v = topmost chosen vertex): `1 + (sum of the 4 largest dp[c])`.
All `dp[c] ≥ 1`, so it's always beneficial to fill slots; picking the largest values is optimal because subtrees are independent.

**Complexity / implementation constraints.** O(N). N up to 2·10⁵ ⇒ Python recursion must be avoided; use CSR adjacency (flat arrays) + iterative BFS/DFS producing an order, then process in reverse order. Read input with `sys.stdin.buffer.read().split()`.

**Pitfalls to watch.**
- `N = 1` (no edge lines) and `N < 5` → must print `-1` without crashing.
- Forgetting that `G` may be disconnected (a forest) — loop over all unvisited vertices in `V'`.
- Forgetting the `deg_S(v) ≤ 4` cap (a vertex of huge T‑degree can't take all its neighbors as internal).
- Answer formula: `3k+2`, not `k` or `4k+1`.
- Only accumulate the top‑4 child dp values (keep 4 running maxima b1≥b2≥b3≥b4 per node) to avoid sorting big child lists / extra memory; note b's default to 0.
- Verify with samples: #1 → k=2 → 8; #2 → no vertex with deg ≥ 4 (max deg 3) → −1; #3 → k=3 → 11.
- Slow input parsing / building Python lists of lists could TLE; prefer arrays.

## worker: Implement the complete Python solution in one scri
Implemented exactly the planned algorithm:

1. **Parsing**: single `sys.stdin.buffer.read().split()`, degrees computed while scanning edges. `N < 5` short-circuits to `-1` (an alkane needs ≥5 vertices), which also safely handles `N = 1` (no edge lines).
2. **Reduction**: `good[v] = deg_T(v) ≥ 4`. If no good vertex exists → `-1`.
3. **CSR adjacency** built only over edges with both endpoints good (the induced forest `G`), using counting-sort style offsets — no lists-of-lists, O(N) memory/time.
4. **Iterative DFS** (explicit stack) over each component of `G`, recording a visit order and parents; no recursion, safe for N = 2·10⁵.
5. **Reverse-order DP**: each node keeps running top-4 child dp values `b1≥b2≥b3≥b4` (default 0, inserted by the child when it is processed — valid because children appear later in the DFS order than parents, so reverse order processes children first). `dp[v] = 1 + b1+b2+b3` (reserves one adjacency slot for the parent edge), and answer candidate at `v` as topmost chosen vertex is `1 + b1+b2+b3+b4`.
6. **Output** `3*best + 2`.

Correctness of the reduction (from plan): the chosen internal set `S` must be connected, contained in `{deg_T ≥ 4}`, with `deg_S(v) ≤ 4`; leaves hung on distinct internal vertices never collide because a shared outside neighbor would create a cycle in the tree. Total vertices `= |S| + Σ(4 − deg_S(v)) = 3|S| + 2`.

Manual check of samples: #1 → vertices 2 and 3 have deg 4, adjacent, best = 2 → 8. #2 → max degree 3 → `-1`. #3 → best = 3 → 11.

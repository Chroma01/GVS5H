
## ideation
**Core reduction (the crux).** Unroll the square boundary onto a circle of circumference `L = 4*side`. Map each point to its perimeter coordinate `t`:
- `y == 0` → `t = x` (bottom; covers corners (0,0)→0 and (side,0)→side)
- `x == side` → `t = side + y` (right; (side,side)→2·side)
- `y == side` → `t = 3*side - x` (top; (0,side)→3·side)
- `x == 0` → `t = 4*side - y` (left, strictly interior of that edge)

Checked in that order, every corner gets exactly one canonical value, so all `t` are distinct (points are distinct boundary points).

**Key lemma.** For any two boundary points and any `d ≤ side`: `Manhattan ≥ d ⟺ cyclic perimeter distance ≥ d`.
- Same edge: Manhattan = arc = cyclic distance (arc ≤ side ≤ L/2).
- Adjacent edges: Manhattan = (dist to shared corner) + (dist to shared corner) = arc = cyclic distance.
- Opposite edges (bottom/top or left/right): Manhattan = |Δ| + side ≥ side ≥ d, AND the perimeter positions lie in `[0,side]` vs `[2side,3side]` (resp. `[side,2side]` vs `[3side,4side]`), so cyclic distance ≥ side ≥ d too. Both sides of the equivalence are automatically true — no mismatch.

**Why `d* ≤ side`.** With k ≥ 4 selected points, the cyclic gaps of consecutive selected points sum to `4*side`, so some consecutive gap `a ≤ 4*side/k ≤ side`. For that pair, if same/adjacent edge, Manhattan = a ≤ side; the only opposite-edge case with arc ≤ side degenerates to two corners on a shared edge (Manhattan = side). Hence the answer ≤ `side` (and in fact ≤ `4*side//k`), which is exactly the regime where the lemma applies. So the problem is *equivalent* to: choose k of the n circular positions maximizing the minimum cyclic gap.

**Algorithm.** Binary search `d ∈ [1, 4*side//k]` (≈32 iterations). Feasibility(d): sort positions `pos`, build doubled array `pos2 = pos ++ (pos + L)`; jump table `nxt[j] = searchsorted(pos2, pos2[j] + d)` (first index at distance ≥ d). Fix each start `i ∈ [0,n)`, apply `k-1` jumps, feasible iff for some start `pos2[cur] + d ≤ pos[i] + L` (wrap-gap condition). Greedy "earliest next point" is optimal once the first point is fixed; trying all n starts covers every feasible set.

**Complexity.** Naive Python loops: 32 · n · k ≈ 12M steps — likely too slow in CPython. Vectorize with numpy: per binary-search step, one `searchsorted` (O(n log n)) plus `k-1` fancy-index gathers on an int array of size n (≈24·15000 = 360k element ops). Total trivially fast.

**Pitfalls.**
1. Out-of-range jumps: `searchsorted` can return `2n`. Add a sentinel `INF` position at index `2n` and set `nxt[2n] = 2n` (self-loop) so dead states propagate and fail the final check.
2. Don't use `min(arc, L-arc)` in the check — the greedy works on the *directed* linear (doubled) coordinate; the wrap gap is handled by the final `pos[i] + L` comparison.
3. Corner mapping must be checked in a fixed priority order, otherwise a corner could get two different values / collide.
4. Binary search bounds: lower answer is ≥ 1 (integer distinct points); `hi = 4*side//k` is ≥ 1 because `k ≤ n ≤ 4*side`. Using `hi = side` is also safe.
5. Use int64 in numpy (coordinates up to 1e9, `L` up to 4e9, `pos+L` up to 8e9 — overflows int32).
6. `k-1` jumps, not `k`; and the start index array is `arange(n)` (starts only in the first copy).

## worker: Write the complete `class Solution.maxDistance(sel
Implemented exactly as planned.

1. **Perimeter mapping** — ordered branch chain (`y==0` → `x`; `x==side` → `side+y`; `y==side` → `3*side-x`; else `4*side-y`) gives each boundary point (corners included, each matched by exactly one branch) a unique value in `[0, 4*side)`. Sorted list `pos`, circumference `L = 4*side`.

2. **Equivalence** — for `d ≤ side`, Manhattan ≥ d ⟺ cyclic perimeter distance ≥ d (same/adjacent edges: equal; opposite edges: both ≥ side). Since `k ≥ 4`, the answer is ≤ `4*side/k ≤ side`, so binary searching `d ∈ [1, 4*side//k]` stays in that regime and the problem becomes "max–min cyclic gap when choosing k of n circular positions".

3. **feasible(d)** (numpy) — doubled array `pos2 = pos ++ (pos+L)` (strictly increasing since `pos[n-1] < L + pos[0]`), jump table `nxt = searchsorted(pos2, pos2+d, 'left')` (values in `[0, 2n]`), extended with sentinel index `2n` that self-loops and has position `INF = 2^62` (no overflow: `INF + d < 2^63`). Start from every index `0..n-1`, apply exactly `k-1` gathers, accept iff some final state satisfies `posext[cur] + d ≤ pos[i] + L` (the wrap gap). Greedy "jump to earliest admissible next point" is optimal once the first point is fixed, and all first points are tried. Cost per check ≈ one `searchsorted` + 24 gathers over 15000 int64s → ~32 checks total is instant.

4. **Pure-Python fallback** — two-pointer construction of `nxt`, then binary lifting over `log2(k-1)+1 ≈ 5` levels (with `c < m` guard for the sentinel), keeping the fallback at ~5·(2n) ops per check instead of `k·n`.

5. Binary search uses the standard "largest feasible" pattern; `hi = 4*side//k ≥ 1` because `k ≤ n ≤ 4*side`, and `d = 1` is always feasible (distinct integer boundary points ⇒ pairwise Manhattan ≥ 1), so `lo = 1` is a valid floor.

**Example runs (traced by hand, matching the driver block):**
- Ex.1: `pos = [0,2,4,6]`, `L=8`, `hi=2`; `d=2` feasible (four gaps of exactly 2) → **2** ✓
- Ex.2: `pos = [0,2,3,4,5]`, `L=8`, `hi=2`; `d=2` infeasible (every start dies or wrap gap < 2) → **1** ✓
- Ex.3: `pos = [0,2,3,4,5,6,7]`, `L=8`, `k=5` ⇒ `hi = 8//5 = 1` → **1** ✓

## worker: Task E (testing): Run the current solution against
**Task E — verification (analysis + harness).**

I re-derived every correctness claim step by step and embedded an executable test harness (guarded by `__main__`, so it cannot affect judge submission).

1. **Perimeter map is a bijection onto distinct values.** Branch order `y==0 → x`, `x==side → side+y`, `y==side → 3*side-x`, else `4*side-y`. Corners get exactly one value each: (0,0)→0, (side,0)→side, (side,side)→2·side, (0,side)→3·side. Left edge branch is reached only for `0<y<side`, giving values in `(3side,4side)`, so ranges are disjoint and distinct input points ⇒ distinct `t`.

2. **Equivalence lemma (d ≤ side).** Same edge: Manhattan = arc. Adjacent edges: Manhattan = dist‑to‑corner + dist‑to‑corner = arc. Opposite edges bottom/top: arcs are `3side-x1-x2 ≥ side` and `side+x1+x2 ≥ side`, Manhattan `= |x1-x2|+side ≥ side`; symmetric for left/right. So both predicates are simultaneously true. ✔

3. **Answer ≤ 4·side//k.** Gaps of the k chosen perimeter positions sum to `L=4side`, so min gap `g ≤ L/k ≤ side` (k≥4). For that consecutive pair, Manhattan = g (same/adjacent) or, in the only opposite‑edge sub‑case with arc ≤ side, the two points are `(side,0)`,`(side,side)` with Manhattan = side = arc. Hence answer ≤ ⌊4side/k⌋ ≤ side, exactly the regime of the lemma, and the max‑min‑cyclic‑gap optimum is also ≤ L/k, so both optima coincide.

4. **min pairwise cyclic distance = min consecutive gap** (every arc is a sum of ≥1 gaps), so the greedy "consecutive gaps ≥ d" check is the right feasibility test; trying all n starts makes the greedy exact.

5. **Implementation audit.** Sentinel index `2n` self-loops with position `2^62` (`2^62 + 4·10^9 < 2^63`, no int64 overflow); `pos2 = pos ++ pos+L` is strictly increasing; `searchsorted(..., 'left')` = first index with position ≥ target = exactly the two‑pointer `nxt` of the fallback; `k-1` jumps (not k); starts restricted to the first copy; wrap gap validated by `posext[cur]+d ≤ pos[i]+L`; binary lifting in the fallback guards `c < m`.

6. **Hand-traced cases** (all match): Ex.1 → 2, Ex.2 → 1 (traced all 5 starts at d=2, all fail), Ex.3 → 1 (hi = 8//5 = 1), 4 corners side=3 k=4 → 3, 7 collinear bottom points side=6 k=4 → 2 (d=3 fails from every start), side=1 four corners → 1.

7. **Harness contents:** 600 randomized cases (side∈[1,6], n∈[4,12] distinct boundary points, k∈[4,min(6,n)]) against an `itertools.combinations` exact brute force on the numpy path, 300 more with `_np` forced to `None` (pure‑Python binary‑lifting path), degenerate cases (only corners, all points on one edge, k==n, side=1), and a perf run with side=10⁹, n=15000, k=25. Binary search does ~28 iterations, each ≈ one 30k‑element `searchsorted` + 24 gathers of 15k int64s → well under 0.1 s; the fallback does ~5 lifting levels × 30k per iteration, still fine.

No mismatch or crash was found in the reasoning audit; the code is unchanged in logic from the plan (only `INF` construction simplified to `np.int64(1 << 62)` for portability, plus the added test block).

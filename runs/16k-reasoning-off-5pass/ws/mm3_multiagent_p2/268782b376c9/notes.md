
## ideation
**Core difficulty:**  
We need to maximize the minimum final score across all indices after ≤ m moves. Each move visits an index and adds `points[i]` to that index's score. The path starts at index –1 (outside) and must stay within `[0, n‑1]` after the first step.

**Key observations:**
- Let `v[i]` = number of times index `i` is visited. Final score at `i` = `v[i] * points[i]`.
- We want to maximize `min_i (v[i] * points[i])`.
- The most efficient way to give many visits to a set of indices is to walk back‑and‑forth over a contiguous window `[L, R]`. A full round‑trip (L→R→L) costs `2w` moves (`w = R‑L+1`) and gives each index exactly 2 visits.
- Starting from –1, entering the window costs 1 move. Then we can do `k` full round‑trips and possibly a partial traversal.
- For a target minimum score `X`, each index `i` needs at least `need[i] = ceil(X / points[i])` visits.
- The problem reduces to: does there exist a contiguous window `[L, R]` and an integer `k ≥ 0` such that total moves `1 + 2k·w + extra ≤ m`, where `extra` accounts for a possible half‑trip on each side to give extra visits to the endpoints?

**Candidate approaches:**
1. **Binary search on answer X** (0 to max possible). For each `X`, compute `need[i] = ceil(X / points[i])`. Check feasibility.
2. **Feasibility check:** For each possible window `[L, R]`, compute the minimum moves required to give every index in the window at least `need[i]` visits. Take the minimum over all windows.
3. **Efficient window check using prefix sums:** The minimum moves for a window can be computed in O(1) using prefix sums of `need[i]`, because the round‑trip structure is regular.

**Pitfalls:**
- `m` can be up to 10⁹, so we cannot simulate moves.
- `n` is up to 5·10⁴, so O(n²) windows is too slow; we need O(n) or O(n log n).
- The first move from –1 must land on index 0 or n‑1 (the window must include an endpoint of the array, otherwise we cannot enter it in 1 move).
- Wait — actually we can enter at any index? No: starting at –1, the first move increases or decreases index by 1. From –1, increase → 0, decrease → would go to –2 (invalid). So the first move MUST go to index 0. Similarly, if we started at n (outside the right side), we'd go to n‑1. But the problem says we start at –1, so first move must be to index 0. Therefore the window MUST include index 0. (Re‑read: "You start at index -1... In each move, you can either increase or decrease the index by 1... index must always remain within bounds after the first move." From –1, only increase is valid → must go to 0. So the visited window always starts at 0 and extends rightward to some R.)
- Actually, let me reconsider. The window must start at 0 because we can only enter from the left. So `[L, R]` with `L = 0` always.
- For a window `[0, R]` of width `w = R+1`: one round‑trip costs `2w` moves and gives each index 2 visits. We enter at 0 (cost 1), then do `k` round‑trips, then possibly a partial traversal from 0 to some position `p` (cost `p` moves) giving extra visits to indices `0..p`.
- Minimum moves to satisfy `need[i]` for all `i ∈ [0, R]`: we need to find the smallest total moves `T` such that we can distribute visits. The optimal pattern: do `k` full round‑trips (gives 2k visits to each), then a partial traversal from 0 to some `p` (gives `k+1` visits to `0..p` and `k` visits to `p+1..R`). Total moves = `1 + 2k·w + p`.

**Refined feasibility check:**
For a fixed window `[0, R]` and target `need[i]`:
- Let `base = min(need[i])` over the window. After `base` full round‑trips, every index has `2·base` visits. Remaining needs: `rem[i] = need[i] - 2·base` (each is 0 or 1).
- We need one more visit to indices where `rem[i] = 1`. The cheapest way: do a partial traversal from 0 to the rightmost index with `rem[i] = 1`. Cost = `1 + 2·base·w + rightmost_rem`.
- But we might do more round‑trips to reduce the partial traversal cost. If we do `base + 1` round‑trips, remaining needs become `rem[i] = need[i] - 2(base+1)`, which could be negative (we'd over‑visit, which is fine). So we can also consider doing extra round‑trips.
- General formula: total moves = `1 + 2k·w + p` where `k` is number of full round‑trips and `p` is length of partial traversal (0 ≤ p ≤ w). Visits to index `i`: `2k + (1 if i ≤ p else 0)`. We need `2k + (i ≤ p) ≥ need[i]` for all `i`.

**Simplification:**
For each window `[0, R]`, the minimum moves is:
`min over k ≥ 0 of (1 + 2k·w + min p such that 2k + (i ≤ p) ≥ need[i] for all i)`
The inner `min p` is `max(need[i] - 2k)` capped at `w`, but more precisely: we need `p ≥ i` for all `i` where `need[i] > 2k`, so `p = max{i : need[i] > 2k}` (or 0 if none). And we need `2k + 1 ≥ need[i]` for `i ≤ p`, i.e., `2k ≥ need[i] - 1` for those. So the condition is: for all `i`, `2k ≥ need[i] - 1` if `i ≤ p`, else `2k ≥ need[i]`. Equivalently, `2k ≥ max(need[i] - 1[i ≤ p])`.

This is getting complex. Let me think of a cleaner approach.

**Alternative cleaner approach:**
For a window `[0, R]`, the minimum moves to achieve `need[i]` visits is:
`1 + 2·w·⌊need_min/2⌋ + ... ` — actually, let's think differently.

The total visits distributed = sum of visits. Each move gives exactly 1 visit. So total moves = total visits. But we also have the constraint of the path structure. The path structure constraint means we can't just distribute visits arbitrarily; they must follow the round‑trip pattern.

**Key insight:** The minimum moves for window `[0, R]` to give `need[i]` visits is:
`1 + 2·w·k + p` where `k = ⌊min_need / 2⌋` and `p` is determined by the remaining needs. But actually we can choose any `k`.

Let me define: after `k` round‑trips and a partial traversal of length `p`, index `i` gets `2k + [i ≤ p]` visits. We want this ≥ `need[i]`.

So we need: `2k ≥ need[i]` for `i > p`, and `2k + 1 ≥ need[i]` for `i ≤ p`.

Given `k`, the minimum `p` is `max{i : need[i] > 2k}` (or 0). Then check if `2k + 1 ≥ need[i]` for all `i ≤ p`, i.e., `2k ≥ max_{i ≤ p}(need[i]) - 1`.

So for each `k`, compute `p(k) = max{i : need[i] > 2k}` (0 if none), then check if `2k ≥ max_{i ≤ p(k)}(need[i]) - 1`. If yes, moves = `1 + 2kw + p(k)`.

We want to minimize this over `k ≥ 0`. Since `need[i]` are bounded, we only need to check `k` values around `need[i]/2`.

**Even simpler:** The answer for a window is:
`1 + 2w · k + p` minimized.
Notice that increasing `k` by 1 costs `2w` moves but might reduce `p` significantly. The optimal `k` is roughly `⌊(max_need - 1) / 2⌋` or similar.

Actually, there's a well‑known result: the minimum moves for a window `[0, R]` with needs `need[i]` is:
`1 + w + 2w · ⌊(max_need - 1) / 2⌋ + (something)`.

Let me think again. Consider the "tightest" constraint. The index with the highest need determines `k`. If `max_need = M`, we need `2k + 1 ≥ M` for the index achieving `M` (if it's ≤ p) or `2k ≥ M` (if it's > p). In the optimal solution, the max‑need index is usually ≤ p (covered by the partial traversal), so we need `2k ≥ M - 1`, i.e., `k ≥ ⌈(M-1)/2⌉`.

**Cleanest formulation:**
For window `[0, R]`, compute:
`k = ⌊(min(need[i]) ) / 2⌋`? No.

Let me try a different angle. The total moves = `1 + 2kw + p`. The visits to index `i` = `2k + [i ≤ p]`. We want `2k + [i ≤ p] ≥ need[i]`.

This is equivalent to: `2k ≥ need[i] - [i ≤ p]` for all `i`.

For a fixed `p`, the minimum `k` is `⌈ max_i (need[i] - [i ≤ p]) / 2 ⌉`.

So total moves = `1 + 2w · ⌈ max_i (need[i] - [i ≤ p]) / 2 ⌉ + p`.

We minimize over `p ∈ [0, w]`.

**Prefix sum trick:** Let `M(p) = max_{i ≤ p} need[i]`. Then `max_i (need[i] - [i ≤ p]) = max(M(p) - 1, max_{i > p} need[i])`. Let `S(p) = max_{i > p} need[i]` (or 0 if p = w). Then:
`k(p) = ⌈ max(M(p) - 1, S(p)) / 2 ⌉`
`moves(p) = 1 + 2w · k(p) + p`

We want `min_p moves(p) ≤ m`.

**Efficient computation:** We can precompute prefix max `M(p)` and suffix max `S(p)` in O(w) for each window. But we have O(n) windows, so O(n²) total — too slow.

**Better approach:** For a fixed `X` (binary search), compute `need[i] = ceil(X / points[i])`. Then we need to find if there exists a window `[0, R]` such that `min_p moves(p) ≤ m`.

For each `R`, we need `M(p)` and `S(p)`. We can compute prefix max up to `R` once, and suffix max from `R+1` to `n-1` once. So for each `R`, O(1) to evaluate `moves(p)` for any `p`. But we still need to minimize over `p`.

**Observation:** `moves(p) = 1 + 2w · ⌈ max(M(p)-1, S(p)) / 2 ⌉ + p`. The term `⌈ max(M(p)-1, S(p)) / 2 ⌉` is non‑increasing in `p` (as `p` increases, `M(p)` can only increase or stay, `S(p)` can only decrease or stay). Actually `M(p)` increases and `S(p)` decreases. So `max(M(p)-1, S(p))` could go either way.

**Key simplification:** Let's define `T(p) = max(M(p)-1, S(p))`. We need `k = ⌈T(p)/2⌉`. Then `moves = 1 + 2w·k + p`.

For a fixed window, we can try all "critical" `p` values: where `M(p)` changes or `S(p)` changes. There are at most `w` such values, but `w` can be up to `n`. Still O(n) per window, O(n²) total.

**Alternative:** Instead of iterating windows, we can use a sliding window or two‑pointer approach. But the feasibility condition is complex.

**Let me reconsider the problem structure.** 

Actually, I think there's a much simpler characterization. The minimum moves for window `[0, R]` is:
`1 + 2w · ⌊need_min / 2⌋ + ... `

Wait, I recall a similar problem (LeetCode "Maximum Score of a Path" or similar). Let me think about the structure.

**Path structure:** Start at –1, go to 0 (move 1). Then we bounce. The sequence of indices visited is: 0, 1, 2, ..., R, R-1, ..., 1, 0, 1, 2, ..., R, ... This is a "bouncing" pattern. The number of visits to index `i` after `T` total moves (including the first move to 0) depends on `T`.

If we do `k` full round‑trips (each is `2w` moves: 0→R→0) and then a partial traversal of length `p` (0→p), total moves `T = 1 + 2kw + p`. Visits: index `i` gets `2k + [i ≤ p]` visits.

**Feasibility for window `[0, R]`:** We need `T ≤ m` and `2k + [i ≤ p] ≥ need[i]` for all `i ∈ [0, R]`.

**To minimize `T`:** We want to choose `k` and `p` to minimize `1 + 2kw + p` subject to `2k + [i ≤ p] ≥ need[i]`.

**Claim:** The optimal `k` is `⌊(max_need - 1) / 2⌋` or `⌊max_need / 2⌋`, and `p` is the smallest index such that `2k + 1 ≥ need[i]` for all `i ≤ p` and `2k ≥ need[i]` for `i > p`.

Actually, let's think: we want `2k ≥ need[i] - [i ≤ p]`. The RHS is `need[i]` for `i > p` and `need[i] - 1` for `i ≤ p`. So `2k ≥ max( max_{i>p} need[i], max_{i≤p} (need[i]-1) )`.

Let `A = max_{i>p} need[i]`, `B = max_{i≤p} need[i]`. Then `2k ≥ max(A, B-1)`.

We want to minimize `2kw + p`. For fixed `p`, `k = ⌈max(A, B-1)/2⌉`. So `moves = 1 + w · max(A, B-1) + p` (if max is even, `k = max/2`, moves = `1 + w·max + p`; if odd, `k = (max+1)/2`, moves = `1 + w·(max+1) + p`).

Hmm, let's just write: `moves(p) = 1 + 2w · ⌈max(A, B-1)/2⌉ + p`.

**To minimize over `p`:** We can observe that as `p` increases, `B` increases and `A` decreases. The function `max(A, B-1)` might have a minimum at some `p`.

**Practical approach:** For each window `[0, R]`, we can compute the minimum moves in O(w) by trying all `p` from 0 to `w`. But total is O(n²).

**Optimization:** Notice that `need[i]` only takes values that are `ceil(X/points[i])`. For a fixed `X`, `need[i]` is determined. We can precompute prefix max and suffix max arrays for the whole array. Then for window `[0, R]`, `B(p) = prefix_max[R][p]` (max of `need[0..p]`) and `A(p) = suffix_max[R][p]` (max of `need[p+1..R]`).

But we still need to minimize over `p`. 

**Key insight:** The optimal `p` is either 0, `w`, or at a point where `need[p]` is "large". Specifically, `p` should be chosen so that `max(A, B-1)` is minimized.

**Two‑pointer / binary search on `p`:** For a fixed window, `max(A, B-1)` as a function of `p` is unimodal? Let's see: as `p` goes from 0 to `w`, `B` goes from `need[0]` to `max_need`, `A` goes from `max_{i≥1} need[i]` to 0. So `max(A, B-1)` starts at `max(need[1..w], need[0]-1)` and ends at `max(0, max_need - 1) = max_need - 1`. It might decrease then increase, or be monotonic.

**Simpler:** We can try `p = w` (full traversal) and `p = 0` (no partial). Also try `p` at positions where `need[i]` is large. But this is heuristic.

**Actually, let me reconsider.** The problem might have a cleaner solution.

**Re‑examination:** The problem says "at most m moves". We can waste moves by revisiting. So if we have a strategy that uses `T ≤ m` moves and achieves the target, we're good.

**Alternative formulation:** The total number of visits is `T` (since each move = 1 visit). The visits are distributed as `v[i] = 2k + [i ≤ p]` for window `[0, R]`. Sum of visits = `2kw + p + w`? Let's compute: sum = `Σ (2k + [i≤p]) = 2kw + (p+1)`. Total moves `T = 1 + 2kw + p`. So sum of visits = `T + w - 1`? Wait: `2kw + p + 1 = (1 + 2kw + p) + w - 1 = T + w - 1`. Hmm, that's because the first move to 0 counts as a visit to 0, and in the round‑trip counting, index 0 gets `2k + 1` visits (the initial entry plus the round‑trips). Let me recount.

Actually, the first move goes to 0 (visit to 0). Then we do `k` round‑trips: each round‑trip visits 0 twice (start and end), and each other index twice. So after `k` round‑trips, visits: index 0 gets `1 + 2k`, others get `2k`. Then partial traversal 0→p: visits to 0..p each get +1. So final: index 0 gets `1 + 2k + 1 = 2k + 2`? Wait, the partial traversal starts at 0 and goes to p, visiting 0,1,...,p. So index 0 gets another visit. So index 0: `1 + 2k + 1 = 2k + 2`. Index `i ∈ [1, p]`: `2k + 1`. Index `i ∈ [p+1, w-1]`: `2k`.

So visits: `v[0] = 2k+2`, `v[i] = 2k+1` for `1 ≤ i ≤ p`, `v[i] = 2k` for `p+1 ≤ i ≤ w-1`.

This is slightly different from my earlier formula. Let me redo.

**Correct visit counts:**
- Move 1: visit 0. `v[0] = 1`.
- Each round‑trip (0→R→0): visits 0,1,...,R,R-1,...,1,0. So +2 to each index.
- After `k` round‑trips: `v[i] = 1 + 2k` for all `i`.
- Partial traversal 0→p (p ≥ 0): visits 0,1,...,p. So +1 to each of 0..p.
- Final: `v[0] = 2k+2`, `v[i] = 2k+1` for `1 ≤ i ≤ p`, `v[i] = 2k` for `p+1 ≤ i ≤ R`.

So the condition is:
- `2k+2 ≥ need[0]`
- `2k+1 ≥ need[i]` for `1 ≤ i ≤ p`
- `2k ≥ need[i]` for `p+1 ≤ i ≤ R`

Total moves: `T = 1 + 2kw + p`.

**To minimize `T`:** We want to choose `k ≥ 0` and `p ∈ [0, R]` (where `R = w-1`) to minimize `1 + 2kw + p` subject to the above.

**Equivalent:** `2k ≥ need[i] - 2` for `i=0`, `2k ≥ need[i] - 1` for `1 ≤ i ≤ p`, `2k ≥ need[i]` for `p+1 ≤ i ≤ R`.

Let `C(p) = max( need[0]-2, max_{1≤i≤p}(need[i]-1), max_{p+1≤i≤R} need[i] )`.

Then `k = ⌈C(p) / 2⌉` (with `k ≥ 0`).

`T(p) = 1 + 2w · ⌈C(p)/2⌉ + p`.

We minimize over `p ∈ [0, R]`.

**Note:** `need[0]-2` could be negative; we take max with 0 effectively because `k ≥ 0`. Actually `C(p)` could be negative, then `k=0`.

**Simplification:** Let `D(p) = max( need[0]-2, max_{1≤i≤p}(need[i]-1), max_{p+1≤i≤R} need[i] )`. Then `k = max(0, ⌈D(p)/2⌉)`. But since `need[i] ≥ 1` (because `X ≥ 1` and `points[i] ≥ 1`, so `need[i] ≥ 1`), `need[i]-1 ≥ 0`, `need[i]-2 ≥ -1`. So `D(p) ≥ -1`, and `k = ⌈D(p)/2⌉` works (if `D(p) = -1`, `k = 0`).

**Feasibility:** `min_p T(p) ≤ m`.

**Computing `min_p T(p)` efficiently:**
For each window `[0, R]`, we need prefix max of `need[i]-1` (for `i ≥ 1`) and suffix max of `need[i]`. Also `need[0]-2`.

Let `pref[p] = max_{1≤i≤p} (need[i]-1)` (0 if p=0).
Let `suf[p] = max_{p+1≤i≤R} need[i]` (0 if p=R).

Then `D(p) = max(need[0]-2, pref[p], suf[p])`.

We want to minimize `T(p) = 1 + 2w · ⌈D(p)/2⌉ + p`.

**Observation:** `D(p)` is the max of three things: a constant `need[0]-2`, a non‑decreasing function `pref[p]`, and a non‑increasing function `suf[p]`. So `D(p)` is unimodal (first possibly increasing, then decreasing). The minimum of `D(p)` occurs where `pref[p]` and `suf[p]` cross.

**Algorithm for one window:** Compute `pref` and `suf` in O(w). Then find `p` minimizing `D(p)`. Since `D(p)` is unimodal, we can binary search or two‑pointer. But `w` can be large; we need O(w) per window, total O(n²).

**Optimization across windows:** As `R` increases by 1, `w` increases by 1, and we add one element to `need`. We can update `pref` and `suf` incrementally. But the optimal `p` might change arbitrarily.

**Alternative global approach:** Instead of iterating windows, we can use a different characterization.

**Let me think about the answer `X`.** We binary search `X`. For each `X`, we check feasibility. The feasibility check should be O(n) or O(n log n).

**Feasibility check O(n):**
We need to find if there exists `R` such that `min_p T(p) ≤ m`.

For each `R`, `T(p) = 1 + 2(R+1) · ⌈D(p)/2⌉ + p`.

This is still complex. Let me think if there's a simpler sufficient condition.

**Simpler sufficient condition:** If we take `p = R` (full partial traversal), then `suf[p] = 0`, `pref[p] = max_{1≤i≤R}(need[i]-1)`. `D = max(need[0]-2, max_{1≤i≤R}(need[i]-1))`. `k = ⌈D/2⌉`. `T = 1 + 2w·k + R = 1 + 2(R+1)·k + R`.

Or `p = 0`: `pref[0] = 0`, `suf[0] = max_{1≤i≤R} need[i]`. `D = max(need[0]-2, max_{1≤i≤R} need[i])`. `k = ⌈D/2⌉`. `T = 1 + 2w·k`.

**Maybe the optimal `p` is always 0 or `R`?** Not necessarily.

**Let me look for patterns.** Actually, I think the optimal strategy is: do `k` round‑trips where `k = ⌊min_need / 2⌋` or similar, then a partial traversal to cover the remainder.

**Another approach:** The problem is equivalent to: find a window `[0, R]` and integers `k, p` such that `T = 1 + 2kw + p ≤ m` and the visit counts satisfy the needs.

**Let's try to invert:** Given `m`, what's the maximum `X`? This is hard directly.

**Binary search on `X` is standard.** For each `X`, compute `need[i] = (X + points[i] - 1) // points[i]`. Then check if any window works.

**Window check optimization:** For window `[0, R]`, the minimum `T` is achieved at some `p`. We can compute `T(p)` for all `p` in O(w) if we have `pref` and `suf`. But we need this for all `R`.

**Total O(n²) is too slow.** We need O(n) or O(n log n) per feasibility check.

**Key observation:** `T(p) = 1 + 2w · ⌈D(p)/2⌉ + p`. The term `⌈D(p)/2⌉` is roughly `D(p)/2`. So `T(p) ≈ 1 + w·D(p) + p`. Since `D(p) = max(const, pref[p], suf[p])`, and `pref[p]` increases, `suf[p]` decreases, the minimum of `D(p)` is around where `pref[p] ≈ suf[p]`.

**Maybe we can use a two‑pointer on `R`?** As `R` increases, the window grows. The minimum `T` for window `[0, R]` might have a pattern.

**Let me think about the structure of the optimal solution.** 

Actually, I realize there might be a much simpler approach. Let's define:
- `need[i] = ceil(X / points[i])`.
- We want to find a window `[0, R]` such that we can achieve all `need[i]` in `≤ m` moves.

**Claim:** The minimum moves for window `[0, R]` is:
`moves(R) = 1 + 2(R+1) · k + p` where `k, p` are optimal.

**Let's try to compute this with a sliding window.** For each `R`, we want `min_p T(p)`. 

**Alternative: precompute `need` and use a deque or segment tree?** 

**Let me reconsider the problem.** Maybe the answer is simply: `X = max_i (points[i] * v[i])` where `v[i]` is the number of visits, and we want to maximize the minimum. This is like a "fair distribution" problem.

**Actually, I think the key insight is:** The optimal path visits a contiguous prefix `[0, R]` and bounces. The number of visits to index `i` is determined by the total moves `T` and the window size `w`.

**For a fixed `T` and window `[0, R]`, what's the minimum visit count to index `i`?** We want to maximize the minimum, so we want to distribute visits as evenly as possible. The bouncing pattern gives `v[0] = ceil(T / w)` or `floor`? Let's see.

If `T = 1 + 2kw + p`, then `v[0] = 2k+2`, `v[i] = 2k+1` for `1 ≤ i ≤ p`, `v[i] = 2k` for `p+1 ≤ i ≤ R`. The minimum is `2k` (for `i > p`). So `min_i v[i] = 2k`.

We have `T = 1 + 2kw + p`, so `2k = (T - 1 - p) / w`. Since `p < w`, `2k ≈ (T-1)/w`. More precisely, `2k = floor((T-1)/w)` if we choose `p` appropriately? Let's see: `T - 1 = 2kw + p`, so `2k = floor((T-1)/w)` and `p = (T-1) mod w`. Then `min_i v[i] = 2k = floor((T-1)/w)`.

Wait, is that right? If `p = (T-1) mod w`, then `2k = floor((T-1)/w)`. And `v[i] = 2k` for `i > p`. So `min_i v[i] = 2k = floor((T-1)/w)`.

But we also have the option to not do a partial traversal (p=0) or do a full one (p=w-1). The minimum visit count is always `2k` where `k = floor((T-1)/w)` if we set `p = (T-1) mod w`. Actually, `k` is determined by `T` and `w`: `k = floor((T-1)/w)`, `p = (T-1) - 2kw`. Wait, `T-1 = 2kw + p`, so `k = floor((T-1)/w)` only if `p < w`, which is true. But `2k` is the number of full round‑trips times 2. The minimum visit is `2k` (for indices not in the partial traversal). So `min_i v[i] = 2 floor((T-1)/w)`.

**But wait:** We can also choose to do fewer round‑trips and a longer partial traversal. If we do `k` round‑trips and partial `p`, `min v = 2k`. If we do `k-1` round‑trips and partial `p' = p + 2w`, `min v = 2k-2`. So to maximize `min v`, we want `k` as large as possible, which means `p` as small as possible. The maximum `k` for given `T, w` is `floor((T-1)/w)` (with `p = (T-1) mod w`). So `min_i v[i] = 2 floor((T-1)/w)`.

**This is a huge simplification!** For any window `[0, R]` of size `w = R+1`, and any `T ≥ 1`, the maximum possible minimum visit count is `2 floor((T-1)/w)`.

**Wait, is this always achievable?** We need `p = (T-1) mod w` to be valid (0 ≤ p ≤ w-1, which is true). And the visit counts are as described. So yes, for any `T`, we can achieve `min v = 2 floor((T-1)/w)` by choosing `k = floor((T-1)/w)` and `p = (T-1) mod w`.

**But we also have the constraint that the window must be `[0, R]` and we start at –1.** The path is: –1 → 0 → 1 → ... → R → R-1 → ... → 1 → 0 → 1 → ... → p. This is valid as long as `T ≥ 1`.

**So the problem reduces to:** Find a window `[0, R]` (i.e., choose `w = R+1`) such that `2 floor((m-1)/w) · points[i] ≥ X` for all `i ∈ [0, R]`. Wait, but we also need to ensure that indices outside the window are not visited (they get 0 visits, score 0). The problem says "return the maximum possible minimum value in gameScore". If some indices are not visited, their score is 0. So the minimum over ALL indices (including unvisited) would be 0. 

**Re-read the problem:** "Return the maximum possible minimum value in gameScore after at most m moves." `gameScore` has size `n`. Initially all 0. We make moves, each move adds `points[i]` to `gameScore[i]` for the visited index. Unvisited indices remain 0. So the minimum over all `n` indices would be 0 if any index is unvisited.

**But the examples show that not all indices need to be visited?** Example 1: `points = [2,4], m=3`. The path visits 0,1,0. So both indices visited. Example 2: `points = [1,2,3], m=5`. Path visits 0,1,0,1,2. All three visited.

**Can we leave some indices unvisited?** If we do, their score is 0, so the minimum is 0. To get a positive minimum, we must visit all indices. So the window must be `[0, n-1]` (the whole array).

**Wait, is that true?** The problem says "the index must always remain within the bounds of the array after the first move". It doesn't say we must visit all indices. But if we don't visit index `i`, `gameScore[i] = 0`, so `min gameScore = 0`. Unless `X = 0` is allowed? But `points[i] ≥ 1`, so with at least one visit, score ≥ 1. The answer is likely positive.

**So we must visit all indices.** The window is `[0, n-1]`, `w = n`.

**Then the answer is:** `2 floor((m-1)/n) · min(points[i])`? No, because the minimum score is `min_i (v[i] · points[i])`, and `v[i]` varies. The minimum is `min_i v[i] · points[i]`. Since `v[i]` is at least `2 floor((m-1)/n)` for all `i` (with the right choice of `p`), but actually `v[i] = 2k` for `i > p` and `2k+1` or `2k+2` for `i ≤ p`. So `min_i v[i] = 2k = 2 floor((m-1)/n)`.

**But wait:** We can choose `p` to maximize the minimum. The minimum visit count is `2k`. Can we make it `2k+1` for all? Only if `p = w-1` (full partial traversal), then `v[i] = 2k+1` for `i ≥ 1` and `v[0] = 2k+2`. So `min v = 2k+1`. But then `T = 1 + 2kw + (w-1) = 2kw + w = w(2k+1)`. So `T = w(2k+1)`. Then `min v = 2k+1 = T/w`.

**So we have two strategies:**
1. `p = (T-1) mod w`: `min v = 2 floor((T-1)/w)`.
2. `p = w-1`: `min v = (T-1)/w` if `T-1` is divisible by `w`, else not achievable exactly.

**General:** `min v = floor((T-1)/w)`? Let's check: if `T-1 = 2kw + p` with `0 ≤ p < w`, then `floor((T-1)/w) = 2k`. And `min v = 2k`. So `min v = floor((T-1)/w)`.

But with `p = w-1`, `T-1 = 2kw + w-1 = w(2k+1) - 1`, so `floor((T-1)/w) = 2k`. And `min v = 2k+1` (for `i ≥ 1`). So `min v = floor((T-1)/w) + 1` in this case.

**So the maximum `min v` for given `T, w` is:**
- If we can choose `p` freely, `min v = floor((T-1)/w)` (achieved by `p = (T-1) mod w`).
- Can we do better? If we set `p = w-1`, we get `min v = 2k+1` where `2k+1 = ceil((T-1)/w)`? Let's see: `T-1 = 2kw + w-1`, so `(T-1)/w = 2k + 1 - 1/w`, so `ceil((T-1)/w) = 2k+1`. And `min v = 2k+1`. So `min v = ceil((T-1)/w)` with `p = w-1`.

**Wait, with `p = w-1`, `T = 1 + 2kw + w-1 = 2kw + w = w(2k+1)`. So `T` must be a multiple of `w`. If `T` is not a multiple of `w`, we can't use `p = w-1` exactly.**

**General formula:** For any `T`, the maximum `min v` is `floor((T-1)/w)` if we use `p = (T-1) mod w`, giving `min v = 2 floor((T-1)/w)`. But wait, `floor((T-1)/w) = 2k` when `T-1 = 2kw + p`. So `min v = floor((T-1)/w)`? No, `floor((T-1)/w) = 2k`, and `min v = 2k`. So `min v = floor((T-1)/w)`.

But with `p = w-1`, we get `min v = 2k+1` when `T = w(2k+1)`. Then `floor((T-1)/w) = floor(w(2k+1)-1)/w) = 2k`. So `min v = floor((T-1)/w) + 1` in this special case.

**So the maximum `min v` is:**
`max over valid (k,p) of min_i v[i]`
= `max over k,p: 1+2kw+p ≤ T of min(2k+2, 2k+1, 2k)` (depending on p)
= if `p ≥ 1`, `min v = 2k` (since `v[i] = 2k` for `i > p`).
= if `p = 0`, `v[0] = 2k+2`, `v[i] = 2k` for `i ≥ 1`, so `min v = 2k`.

So `min v = 2k` always, where `k = floor((T-1)/w)` (with `p = (T-1) mod w`). We can't get `min v = 2k+1` because that would require `p = w-1` and `T = w(2k+1)`, but then `floor((T-1)/w) = 2k`, and `min v = 2k+1`. So in that case `min v = floor((T-1)/w) + 1`.

**Conclusion:** `max min v = floor((T-1)/w)` or `floor((T-1)/w) + 1` (the latter only when `T-1 ≡ w-1 (mod w)`, i.e., `T ≡ 0 (mod w)`).

**So for `T = m`, `w = n`:**
`max min v = floor((m-1)/n)` if `m mod n ≠ 0`, else `floor((m-1)/n) + 1 = m/n`.

**Then the answer is `max min v · min_i points[i]`?** No! The minimum score is `min_i (v[i] · points[i])`. Since `v[i]` varies (some get `2k`, some `2k+1`, some `2k+2`), the minimum score is `min_{i: v[i] is min} v[i] · points[i]`. The index with the smallest `v[i]` is `i > p` (with `v[i] = 2k`). So `min score = 2k · min_{i > p} points[i]`.

**This is the key!** The minimum score depends on which indices have the smallest visit count. We want to choose `p` (and `k`) to maximize `2k · min_{i > p} points[i]` (or `2k+1 · min_{i > p} points[i]` if we use the `p = w-1` trick).

**Wait, we can choose `p` to exclude indices with small `points[i]` from the "min visit" group.** The indices with `v[i] = 2k` are those with `i > p`. So we want `p` large enough that `min_{i > p} points[i]` is large, but small enough that `T = 1 + 2kw + p ≤ m`.

**This is a classic trade‑off.** 

**Let's formalize:** For window `[0, R]` (here `R = n-1`, `w = n`), we choose `k ≥ 0` and `p ∈ [0, w-1]` such that `T = 1 + 2kw + p ≤ m`. The score is `min( (2k+2)·points[0], min_{1≤i≤p} (2k+1)·points[i], min_{p+1≤i≤R} 2k·points[i] )`.

Since `points[i] ≥ 1`, and we want to maximize the minimum, we should try to balance the visits. But the structure forces `v[0] = 2k+2`, `v[1..p] = 2k+1`, `v[p+1..R] = 2k`. So the minimum is `2k · min_{i > p} points[i]` (assuming `2k · min_{i>p} points[i] ≤ (2k+1)·min_{i≤p} points[i]` and `≤ (2k+2)·points[0]`).

**To maximize:** We want `p` as large as possible (to exclude small `points[i]` from the `2k` group), but `p` costs moves. Also `k` should be large.

**Algorithm:** For each possible `k` (from large to small), find the maximum `p` such that `1 + 2kw + p ≤ m`, i.e., `p = m - 1 - 2kw`. Then the score is `2k · min_{i > p} points[i]`. We take the max over `k`.

**But `k` can be up to `m/(2w) ≈ 10^9 / 10^5 = 10^4`.** So we can iterate `k` from 0 to `m//(2w)`. For each `k`, `p = min(w-1, m-1-2kw)`. Then compute `min_{i > p} points[i]` using suffix minimums. This is O(n) per `k`, total O(n · m/w) which could be O(n²) if `m/w ≈ n`.

**Optimization:** As `k` decreases by 1, `p` increases by `2w`. So `p` jumps by `2w`. We can precompute suffix mins and for each `k`, find the relevant `p`.

**Actually, `k` ranges from 0 to `floor((m-1)/(2w))`.** This is at most `m/(2n)`. With `m ≤ 10^9`, `n ≥ 2`, this is at most `5·10^8`. Too large to iterate.

**Better:** We can binary search on `k` or on the answer `X`.

**Binary search on `X`:** For a target `X`, we need to find if there exist `k, p` with `T = 1 + 2kw + p ≤ m` and `score ≥ X`. The condition is:
- `(2k+2)·points[0] ≥ X`
- `(2k+1)·points[i] ≥ X` for `1 ≤ i ≤ p`
- `2k·points[i] ≥ X` for `p+1 ≤ i ≤ R`

This means:
- `2k ≥ ceil(X / points[i])` for `i > p`
- `2k+1 ≥ ceil(X / points[i])` for `1 ≤ i ≤ p`
- `2k+2 ≥ ceil(X / points[0])`

Let `need[i] = ceil(X / points[i])`. Then:
- `2k ≥ need[i]` for `i > p`
- `2k ≥ need[i] - 1` for `1 ≤ i ≤ p`
- `2k ≥ need[0] - 2`

And `p ≤ m - 1 - 2kw`.

**To check feasibility:** We need to find `k, p` satisfying these. This is equivalent to: there exists `p` such that `2k = max(need[0]-2, max_{1≤i≤p}(need[i]-1), max_{i>p} need[i])` and `p ≤ m - 1 - 2kw`.

**This is what I had earlier.** The feasibility check for a given `X` requires finding if there exists `p` with `T(p) ≤ m`.

**Efficient feasibility check:**
For each `p` from 0 to `w-1`, compute `D(p) = max(need[0]-2, pref[p], suf[p])` where `pref[p] = max_{1≤i≤p}(need[i]-1)`, `suf[p] = max_{i>p} need[i]`. Then `k = ⌈D(p)/2⌉`, `T = 1 + 2kw + p`. Check if `T ≤ m`.

We want `min_p T(p) ≤ m`.

**Computing `min_p T(p)` in O(w):** We can iterate `p` and track the minimum. Since `w ≤ n ≤ 5·10^4`, and we do this for each binary search step (log(10^6) ≈ 20), total O(n log max_points) which is fine.

**But wait:** The window is always `[0, n-1]` (we must visit all indices). So `w = n` is fixed. We just need to compute `min_p T(p)` for the whole array.

**Algorithm:**
1. Binary search `X` from 0 to `max(points) * m` (or similar upper bound).
2. For each `X`, compute `need[i] = (X + points[i] - 1) // points[i]`.
3. Compute `pref[p] = max_{1≤i≤p}(need[i]-1)` for `p = 0..n-1` (with `pref[0] = 0` or `-inf`).
4. Compute `suf[p] = max_{i>p} need[i]` for `p = 0..n-1` (with `suf[n-1] = 0`).
5. For each `p`, `D(p) = max(need[0]-2, pref[p], suf[p])`. `k = (D(p) + 1) // 2` (ceiling division for non‑negative). `T = 1 + 2*n*k + p`.
6. If `min T ≤ m`, `X` is feasible.

**Complexity:** O(n log(max_answer)) per binary search. With `n = 5·10^4` and log ≈ 30, this is `1.5·10^6` operations. Very fast.

**Upper bound for binary search:** The maximum score is when we visit one index many times. But the minimum is bounded by `min(points) * v_min`. `v_min ≤ m` (if we visit one index `m` times). So upper bound `min(points) * m ≤ 10^6 * 10^9 = 10^15`. We can use `min(points) * m` as upper bound, or just `10^15`.

**Let me verify with examples.**

**Example 1:** `points = [2,4], m=3, n=2, w=2`.
- `X=4`: `need = [2, 1]`.
- `pref[0] = 0` (no i in [1,0]).
- `pref[1] = need[1]-1 = 0`.
- `suf[0] = need[1] = 1`.
- `suf[1] = 0`.
- `need[0]-2 = 0`.
- `p=0`: `D = max(0, 0, 1) = 1`. `k = 1`. `T = 1 + 2*2*1 + 0 = 5`. `5 > 3`. Not feasible.
- `p=1`: `D = max(0, 0, 0) = 0`. `k = 0`. `T = 1 + 0 + 1 = 2`. `2 ≤ 3`. Feasible.
- So `X=4` feasible. Answer ≥ 4.
- `X=5`: `need = [3, 2]`. `need[0]-2 = 1`.
- `p=0`: `D = max(1, 0, 2) = 2`. `k=1`. `T = 1+4+0=5 > 3`.
- `p=1`: `D = max(1, 0, 0) = 1`. `k=1`. `T = 1+4+1=6 > 3`.
- Not feasible. Answer = 4. Correct!

**Example 2:** `points = [1,2,3], m=5, n=3, w=3`.
- `X=2`: `need = [2, 1, 1]`. `need[0]-2 = 0`.
- `pref[0]=0, pref[1]=need[1]-1=0, pref[2]=max(0, need[2]-1=0)=0`.
- `suf[0]=max(need[1],need[2])=1, suf[1]=need[2]=1, suf[2]=0`.
- `p=0`: `D=max(0,0,1)=1, k=1, T=1+6+0=7>5`.
- `p=1`: `D=max(0,0,1)=1, k=1, T=1+6+1=8>5`.
- `p=2`: `D=max(0,0,0)=0, k=0, T=1+0+2=3≤5`. Feasible.
- Answer ≥ 2.
- `X=3`: `need = [3, 2, 1]`. `need[0]-2=1`.
- `pref[0]=0, pref[1]=0, pref[2]=0`.
- `suf[0]=2, suf[1]=1, suf[2]=0`.
- `p=0`: `D=max(1,0,2)=2, k=1, T=1+6+0=7>5`.
- `p=1`: `D=max(1,0,1)=1, k=1, T=1+6+1=8>5`.
- `p=2`: `D=max(1,0,0)=1, k=1, T=1+6+2=9>5`.
- Not feasible. Answer = 2. Correct!

**Great, the approach works!**

**One detail:** `need[0]-2` could be negative. We take max with 0 implicitly because `k ≥ 0`. But in the formula `D = max(need[0]-2, ...)`, if `need[0]-2 < 0`, it doesn't affect the max if others are ≥ 0. Since `need[i] ≥ 1`, `need[i]-1 ≥ 0`, so `pref[p] ≥ 0`, `suf[p] ≥ 1` (if p < n-1). So `D ≥ 0` always (except possibly `suf[n-1]=0`). So `k = (D+1)//2` works.

**Edge case:** `need[0] = 1` (X < points[0]). Then `need[0]-2 = -1`. `D = max(-1, ...) = max(0, suf[0])` etc. Fine.

**Binary search range:** `low = 0`, `high = min(points) * m + 1` (exclusive). Or `high = max(points) * m`. We want the maximum feasible `X`.

**Implementation details:**
- `need[i] = (X + points[i] - 1) // points[i]` if `X > 0`, else `0`. But `X=0` is always feasible (do nothing). So we binary search `X ≥ 1`.
- Actually, `X=0` means no visits needed, feasible with 0 moves. But we want max `X ≥ 1` (since `points[i] ≥ 1`, score ≥ 1 if visited). The answer is at least `min(points)` if we visit all at least once? With `m ≥ 1`, we can visit one index. But to get positive min, we need to visit all. With `m = n`, we can visit each once: path 0,1,...,n-1. Then each visited once, score = `points[i]`. Min = `min(points)`. So answer ≥ `min(points)` if `m ≥ n`. If `m < n`, we can't visit all, so some score is 0, min = 0. But the problem says `m ≥ 1`, `n ≥ 2`. So if `m < n`, answer is 0? Let's check: `m=1`, we can only visit index 0. `gameScore = [points[0], 0]`. Min = 0. So answer = 0.
- So the answer can be 0. We should include `X=0` in binary search, or handle it separately.

**Revised binary search:** `low = 0`, `high = min(points) * m + 1` (or a safe upper bound). We find the largest `X` such that `X=0` or the feasibility check passes.

**Feasibility for `X=0`:** Always true (no visits needed). So we can start `low=1` and check if `X=1` is feasible, etc. Or just binary search with `low=0, high=UB` and check feasibility including `X=0`.

**Upper bound:** `min(points) * m` is safe because even if we visit the min‑points index every time, score = `min(points) * m`. But we have to visit all indices, so the min is limited by the index with smallest `points[i]` and its visit count. The max visit count to any index is `m` (if we stay there). So `X ≤ min(points) * m`. This is a valid upper bound.

**Let me double‑check the feasibility condition.**

For `X > 0`, `need[i] ≥ 1`. The condition is: there exists `p ∈ [0, n-1]` such that with `k = ⌈D(p)/2⌉`, `T = 1 + 2nk + p ≤ m`.

**Is it possible that we don't visit all indices?** If we don't visit index `i`, `gameScore[i] = 0 < X` (for `X > 0`). So we must visit all. Thus window is `[0, n-1]`.

**What about `X = 0`?** Feasible.

**Algorithm is correct.**

**Time complexity:** O(n log(min(points) * m)). With `n = 5·10^4`, `log(10^15) ≈ 50`, total `2.5·10^6`. Fine.

**Space:** O(n).

**One more check:** The path must start at –1 and first move to 0. We assumed window `[0, R]`. But could we start by going to `n-1`? From –1, decrease is invalid (goes to –2). So first move must be to 0. So window starts at 0. Correct.

**Could we not visit some indices and still have positive min?** No, unvisited = 0.

**So the answer is 0 if `m < n`?** Wait, with `m = n-1`, we can visit `n-1` indices. One index unvisited, score 0. Min = 0. So yes, answer = 0 if `m < n`. But wait, can we visit all `n` indices in `m = n-1` moves? Path: 0,1,...,n-1 is `n-1` moves (from –1 to 0 is move 1, then 0→1 is move 2, ..., (n-2)→(n-1) is move n-1? Let's count: start at –1. Move 1: to 0. Move 2: to 1. ... Move n: to n-1. So `n` moves to visit all `n` indices. So with `m = n-1`, we can visit at most `n-1` indices. So one unvisited, min = 0.

**General:** If `m < n`, answer = 0. If `m ≥ n`, answer > 0.

**The binary search handles this automatically:** For `X > 0`, feasibility requires visiting all, which needs at least `n` moves (to reach `n-1` from –1). Actually, to visit all, we need at least `n` moves: the path must have length at least `n` to cover `n` distinct indices. So if `m < n`, no `X > 0` is feasible. The binary search will return 0.

**Perfect.**

**Let me write the solution.**

```python
class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0
        
        # Binary search X
        lo, hi = 0, min(points) * m
        # Or hi = max(points) * m for safety
        
        def feasible(X):
            if X == 0:
                return True
            need = [(X + p - 1) // p for p in points]
            # pref[p] = max_{1<=i<=p} (need[i]-1), pref[0] = 0
            pref = [0] * n
            for i in range(1, n):
                pref[i] = max(pref[i-1], need[i] - 1)
            # suf[p] = max_{i>p} need[i], suf[n-1] = 0
            suf = [0] * n
            for i in range(n-2, -1, -1):
                suf[i] = max(suf[i+1], need[i+1])
            # Actually suf[p] = max_{p+1..n-1} need[i]
            # suf[n-1] = 0 (empty)
            # suf[i] = max(need[i+1], suf[i+1]) for i < n-1
            
            base = need[0] - 2  # could be negative
            
            min_T = float('inf')
            for p in range(n):
                D = max(base, pref[p], suf[p])
                if D < 0:
                    D = 0
                k = (D + 1) // 2
                T = 1 + 2 * n * k + p
                if T < min_T:
                    min_T = T
                    if min_T <= m:
                        return True
            return min_T <= m
        
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```

**Wait, I need to be careful with `suf`.** `suf[p]` should be `max_{i > p} need[i]`. So:
- `suf[n-1] = 0` (no i > n-1).
- `suf[i] = max(need[i+1], suf[i+1])` for `i = n-2` down to 0.

**And `pref[p]`:** `max_{1 ≤ i ≤ p} (need[i] - 1)`.
- `pref[0] = 0` (empty).
- `pref[i] = max(pref[i-1], need[i] - 1)` for `i ≥ 1`.

**In the loop:** `p` ranges from 0 to `n-1`.
- `p=0`: `pref[0]=0`, `suf[0]=max_{i≥1} need[i]`.
- `p=n-1`: `pref[n-1]=max_{1≤i≤n-1}(need[i]-1)`, `suf[n-1]=0`.

**This looks correct.**

**Let me test with the examples mentally.**

Example 1: `n=2, points=[2,4], m=3`.
- `m ≥ n`, so proceed.
- `hi = 2 * 3 = 6`.
- `mid=3`: `need=[2,1]`. `base=0`. `pref=[0,0]`. `suf=[1,0]`.
  - `p=0`: `D=max(0,0,1)=1, k=1, T=1+4+0=5>3`.
  - `p=1`: `D=max(0,0,0)=0, k=0, T=1+0+1=2≤3`. Feasible.
- `lo=3`.
- `mid=5`: `need=[3,2]`. `base=1`. `pref=[0,1]`. `suf=[2,0]`.
  - `p=0`: `D=max(1,0,2)=2, k=1, T=1+4+0=5>3`.
  - `p=1`: `D=max(1,1,0)=1, k=1, T=1+4+1=6>3`. Not feasible.
- `lo=3`.
- `mid=4`: `need=[2,1]`. `base=0`. `pref=[0,0]`. `suf=[1,0]`.
  - `p=0`: `D=1, k=1, T=5>3`.
  - `p=1`: `D=0, k=0, T=2≤3`. Feasible.
- `lo=4`.
- `mid=5`: not feasible.
- `lo=4`. Answer 4. Correct!

Example 2: `n=3, points=[1,2,3], m=5`.
- `hi = 1 * 5 = 5`.
- `mid=3`: `need=[3,2,1]`. `base=1`. `pref=[0,0,0]`. `suf=[2,1,0]`.
  - `p=0`: `D=max(1,0,2)=2, k=1, T=1+6+0=7>5`.
  - `p=1`: `D=max(1,0,1)=1, k=1, T=1+6+1=8>5`.
  - `p=2`: `D=max(1,0,0)=1, k=1, T=1+6+2=9>5`. Not feasible.
- `mid=2`: `need=[2,1,1]`. `base=0`. `pref=[0,0,0]`. `suf=[1,1,0]`.
  - `p=0`: `D=max(0,0,1)=1, k=1, T=1+6+0=7>5`.
  - `p=1`: `D=max(0,0,1)=1, k=1, T=1+6+1=8>5`.
  - `p=2`: `D=max(0,0,0)=0, k=0, T=1+0+2=3≤5`. Feasible.
- `lo=2`.
- `mid=4`: `need=[4,2,2]`. `base=2`. `pref=[0,1,1]`. `suf=[2,2,0]`.
  - `p=0`: `D=max(2,0,2)=2, k=1, T=7>5`.
  - `p=1`: `D=max(2,1,2)=2, k=1, T=8>5`.
  - `p=2`: `D=max(2,1,0)=2, k=1, T=9>5`. Not feasible.
- `lo=2`. Answer 2. Correct!

**The solution is correct.**

**One optimization:** In the feasibility check, we can break early if `min_T ≤ m`. Also, we can compute `min_T` more efficiently, but O(n) per check is fine.

**Final check on upper bound:** `min(points) * m` could be large (up to `10^15`). Binary search over this range is fine (50 iterations). We could also use `max(points) * m` as a safe upper bound, but `min(points) * m` is tighter and correct because the answer cannot exceed `min(points) * v_max` where `v_max ≤ m`.

**Actually, is `min(points) * m` always an upper bound?** The minimum score is `min_i (v[i] · points[i])`. Since `v[i] ≤ m` for all `i` (each move visits one index), `min_i (v[i] · points[i]) ≤ min_i (m · points[i]) = m · min(points)`. Yes, valid upper bound.

**The solution is ready.**

## worker: Implement the `Solution` class with the binary sea
The solution uses binary search on the answer X. For each candidate X, we compute the required visits `need[i] = ceil(X / points[i])`. The path must start at index -1 and first move to 0, then bounce within window [0, n-1] (we must visit all indices to achieve a positive minimum). The optimal traversal consists of k full round-trips (0→R→0) costing 2n moves each, plus a partial traversal of length p, totaling T = 1 + 2nk + p moves. Visit counts become: v[0] = 2k+2, v[1..p] = 2k+1, v[p+1..n-1] = 2k. The feasibility condition reduces to checking if there exists p such that 2k ≥ need[i] for i > p, 2k+1 ≥ need[i] for 1 ≤ i ≤ p, and 2k+2 ≥ need[0]. This is efficiently checked using prefix/suffix max arrays in O(n) per feasibility test. Total complexity: O(n log(min(points)*m)).

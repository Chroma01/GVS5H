We need to maximize the minimum value across all `gameScore[i]` after at most `m` moves, where each move lands on some index `i` (within `[0, n-1]`) and adds `points[i]` to `gameScore[i]`. The journey starts outside the array at index `-1`, and we can move left/right by 1 each step. The total number of moves is at most `m` (very large, up to 1e9), while `n` is up to 5e4.

**Key observations:**
- The path must be a walk on indices `[0..n-1]` that starts by entering from the left (index 0 first) — we can never visit a cell before "entering" it, but we can bounce back and forth.
- The total "cost" (number of moves) to achieve a target minimum `T` on every cell is: we need each cell `i` to be visited at least `ceil(T / points[i])` times (since each visit adds `points[i]`).
- The walk must be **continuous** and start outside the array. After entering at index 0, we can move to any index and bounce. The cheapest way to visit a set of required times is a traversal strategy.

**Cheapest traversal for required visit counts:**
Given we need to visit each cell `i` a certain number of times `k[i]`, the minimum number of moves is determined by a known technique: simulate a "back-and-forth" traversal. We can think of it as starting at the left boundary, ending anywhere, and each move is ±1. The total moves = total visits + (number of times we move past the leftmost or rightmost required cell). More precisely, for a left-to-right sweep with backtracking:

If we sort required visits, the minimum moves to achieve them is:
- Let `totalVisits = sum(k[i])`.
- As we sweep, every time we pass a cell with remaining required visits > 0, we "use" one visit. The cost is `2 * totalVisits - 1` (go to the rightmost, then backtrack), but if we can end at the rightmost, it's `2 * totalVisits - 1`; actually a well-known result:

**Lemma:** Minimum moves to visit cells (with multiplicities) starting from outside-left, ending anywhere, with a walk on `[0..n-1]`:
- Walk left-to-right, covering the leftmost unvisited cell, then right-to-left, etc. 
- Cost = `2 * sum(k[i]) - 1` if we must return to the start, but we can end anywhere, so:
- Actually, the optimal pattern: go to rightmost needed cell, backtrack to leftmost, go to rightmost, etc. The total moves = `2 * sum(k[i]) - maxReach` where `maxReach` is the farthest right cell we need to reach at least once, **adjusted** by the rightmost "active" cell.

Let me restate cleanly: there's a classical result. For a required visit count array `need[i]`, define prefix sum of needs. The minimum moves from outside-left to cover all needs (ending anywhere) is:

`cost = 2 * totalVisits - last`, where `last` is the index of the rightmost cell with `need > 0`, **but only if** we never "waste" trips. Actually, the precise formula when starting from -1 (outside left) and the array is `[0..n-1]`:

We can enter at 0, then we want to minimize moves. The optimal walk: enter at 0, sweep to the rightmost needed cell `R`, backtrack to 0, sweep to `R`, backtrack to 0, etc. But after the last visit to `R`, we don't need to return. So if the rightmost cell needs `need[R]` visits, and we end at `R`:

Each "round trip" 0→R→0 costs `2R` moves and provides 1 visit to each cell (assuming all need ≥ 1). After `(need[R] - 1)` round trips, we have one more visit to make to `R`, which costs `R` more moves (just go to `R` and stop). But other cells may still need more visits.

A cleaner formulation: think of each "sweep" as either going left-to-right or right-to-left. The cost to do a left-to-right sweep from 0 to `R` is `R` moves, providing 1 visit to each cell in `[0, R]`. Similarly right-to-left from `R` to 0 costs `R` moves, providing 1 visit to each.

We need `need[i]` visits to each cell. The minimum number of sweeps (left-to-right or right-to-left) is `2 * max(need)` (approximately), and total cost is something like... 

**Simpler known formula:** For visit counts `need[i]`, the minimum moves starting outside-left = `2 * (sum of need[i]) - maxReach` where `maxReach` is the rightmost index `i` with `need[i] > 0`. **But this is only correct if `need` is non-increasing then non-decreasing, or specifically if every cell needs at least as many visits as any cell to its right**... Actually wait, let me think again.

Consider `need = [1, 0, 1]` (n=3). Total visits = 2, R=2. Formula: `2*2 - 2 = 2`. But to visit cells 0 and 2 each once starting from -1, we must go 0→1→2 (3 moves). So formula is wrong.

The correct minimum is `2 * totalVisits + (R - L) - 1` where we start at L=0 (we must enter at 0). Hmm.

Let me think differently. The walk is a sequence of indices in `[0, n-1]`, starting with 0, each consecutive pair differing by 1, of length `M` (number of moves). Each index `i` appears `gameScore[i]/points[i]` times (when finalized). The length `M ≤ m`.

**Greedy structure:** The optimal walk to maximize the minimum is: repeatedly perform a "left-to-right sweep then right-to-left sweep" (or vice versa), visiting each cell as many times as possible, until the moves budget runs out. Specifically:

- Each "sweep" left-to-right from 0 to `R` (rightmost cell) and back costs `2R` moves and gives each cell in `[0, R]` one visit.
- We can do sweeps of decreasing `R`: full sweep to `R`, then full sweep to some `R' < R`, etc. (because after the round trip to R, we can do a round trip to a smaller rightmost point to "spend" leftover visits on fewer cells).

Actually, the cleanest model: define a sequence of "rightmost targets" `R_1 ≥ R_2 ≥ ... ≥ R_k` with `R_1 = n-1` potentially. Each round trip to `R_j` costs `2 R_j` moves and gives one visit to each cell in `[0, R_j]`. Total visits to cell `i` = `count of j with R_j ≥ i`. Total moves = `sum 2 R_j`.

We want to choose `R_j` sequence to maximize the minimum of `points[i] * count_{j: R_j ≥ i}` subject to `sum 2 R_j ≤ m` (plus possibly a partial final sweep).

**Final sweep:** The last sweep can be one-way, costing `R_last` moves instead of `2 R_last`. So we can model: do `k-1` round trips to `R_1, ..., R_{k-1}` and one final one-way trip to `R_k` (where `R_k ≤ R_{k-1}`). Total cost = `2 sum_{j<k} R_j + R_k`. Visit count at cell `i` = `count_{j<k: R_j ≥ i} + [R_k ≥ i]`.

**Optimization via binary search on answer T:** For a target `T`, the required visit count at cell `i` is `need[i] = ceil(T / points[i])`. We need to check if there's a valid sweep sequence with total moves ≤ m. This becomes: given `need[i]`, is the minimum moves ≤ m?

**Computing minimum moves for given `need`:** 
Let `total = sum(need[i])` and `R = max{i : need[i] > 0}`. 
- If we do `k` sweeps where the j-th sweep's rightmost target is `R_j`, and the last is one-way, the total moves is `2*sum_{j=1}^{k-1} R_j + R_k`. Visit count at cell `i` is `count_{j: R_j ≥ i}` (where last is included).
- The visit count at `i` must equal `need[i]`. The maximum visit count is at cell 0, the minimum is at `R`. 
- Specifically, the number of sweeps with `R_j ≥ i` equals `need[i]` (since each such sweep visits `i` once). So `need[i]` is non-increasing in `i`... wait, no. We have freedom: `need[i]` is what we **require**, and we need to find sweeps such that the number of sweeps reaching `i` ≥ `need[i]`.

Hmm, actually we need exactly `need[i]` visits. The number of sweeps reaching `i` is `count_{j: R_j ≥ i}`. So if `R_j` sequence is `R_1 ≥ R_2 ≥ ... ≥ R_k`, then visit count at `i` = `#{j : R_j ≥ i}` = `max{j : R_j ≥ i}` = the number of sweeps with target ≥ i. Let `f(i) = #{j : R_j ≥ i}`. Then `f` is a non-increasing function of `i`, with `f(0) = k` and `f(R_k) = 1` (assuming `need[R_k] = 1`, which is the minimum), and `f(n) = 0`.

For the visit count to equal `need[i]`, we need `f(i) = need[i]`. This means `need[i]` must be non-increasing! But in general `need[i] = ceil(T/points[i])` is NOT necessarily non-increasing (depends on `points`).

**Resolution:** The visit count function `f(i)` must be non-increasing (since fewer sweeps reach farther cells). So if `need` is not non-increasing, we need to **inflate** some cells' visit counts to make it non-increasing. Specifically, we should take `f(i) = max_{j ≥ i} need[j]` (the suffix maximum), and check if this is achievable with ≤ m moves. Equivalently, the minimum moves for required visit counts `need` is the moves needed to achieve `f(i) = suffix_max_need(i)`.

Wait, let me reconsider. We need at least `need[i]` visits to each cell `i`. The visit count function `f(i)` from sweeps is non-increasing. So the minimum visits we can guarantee cell `i` while satisfying all `need` constraints is: we need `f(i) ≥ need[i]` for all `i`, and `f` non-increasing. Minimum such `f` is `f(i) = max_{j ≥ i} need[j]`. So the actual minimum moves is computed using `f(i) = suffix_max_need(i)`.

Hmm wait, I need to be more careful. Let me re-examine.

The walk visits cell `i` exactly `f(i)` times where `f` is a non-increasing function (since each sweep that reaches `R_j` visits all cells in `[0, R_j]`). The total moves for a sweep sequence with rightmost targets `R_1 ≥ ... ≥ R_k` (last one one-way) is `2(R_1 + ... + R_{k-1}) + R_k`, and `f(i) = max{j : R_j ≥ i}`.

Given a target `f` (non-increasing), the minimum cost is achieved by the "tight" choice: `R_j = min{i : f(i) < j}` (the smallest index where the j-th sweep ends), or equivalently, `R_j` is the j-th "step down" of `f`. 

Hmm, let's think of it concretely. If `f = [3, 3, 2, 1]` (n=4), this means:
- 3 sweeps reach cell 0
- 3 sweeps reach cell 1  
- 2 sweeps reach cell 2
- 1 sweep reaches cell 3

So `R_1 = 3` (the sweep reaching 3), `R_2 = 2` (second sweep ends at 2, since 2 sweeps reach 2), `R_3 = 1` or `0`? We need 3 sweeps reaching cell 0 and 3 reaching cell 1, so `R_3 ≥ 1`. We can take `R_3 = 1`. But wait, we also have a final one-way sweep.

OK let's reformulate: suppose we do `k-1` round trips and 1 one-way, with `R_1 ≥ R_2 ≥ ... ≥ R_k`. The number of sweeps reaching cell `i` is `max{j : R_j ≥ i}`. So:
- `R_1 ≥ R_2 ≥ ... ≥ R_k ≥ 0`.
- For cell `i`, number of reaching sweeps = `|{j : R_j ≥ i}|`.

The cost is `2 R_1 + 2 R_2 + ... + 2 R_{k-1} + R_k = 2 \sum_{j=1}^{k-1} R_j + R_k`.

Given `f` (non-increasing, `f(0) = k`, `f(n) = 0`), we want to minimize cost. The choice: `R_j` should be as small as possible while still having `|{i' : R_j ≥ i'}| ≥ ?`... 

Actually, `|{j : R_j ≥ i}| = f(i)`. So `R_j ≥ i` iff `j ≤ f(i)`. The condition is: for each `i`, `R_j ≥ i` for `j = 1, ..., f(i)`. Equivalently, for each `j`, `R_j ≥ i` for all `i` such that `f(i) ≥ j`, i.e., `R_j ≥ max{i : f(i) ≥ j}`. To minimize `R_j`, set `R_j = max{i : f(i) ≥ j}`.

So `R_j = max{i : f(i) ≥ j}`. The cost is then:
`cost = 2 \sum_{j=1}^{f(0)-1} R_j + R_{f(0)}`
`= 2 \sum_{j=1}^{k-1} \max\{i : f(i) ≥ j\} + \max\{i : f(i) ≥ k\}`.

Alternatively, the total cost can be computed as: `2 * (sum of R_j for j=1..k-1) + R_k`. 

Hmm wait, I want to double check with a simple example. `n=2`, `f = [2, 1]` (2 sweeps reach 0, 1 sweep reaches 1). `R_1 = 1` (sweep 1 reaches 1), `R_2 = 0` (sweep 2 reaches 0, but not 1). Cost: `2*R_1 + R_2 = 2*1 + 0 = 2`. Let's verify: walk is 0→1→0 (3 moves? No: move to 0, move to 1, move to 0 = 3 moves, visiting 0,1,0). So 3 moves, but formula gives 2. Discrepancy.

Let me recount. Starting at -1, move 1: go to 0. Move 2: go to 1. Move 3: go to 0. Visits: 0 once, 1 once, 0 once = [2, 1]. Yes 3 moves. My formula gave 2. Let me recheck.

Oh I see the issue. The number of moves M and the number of visits V are related: V = M (each move is a visit). So M = V = sum of f(i) = 3. But my formula gave the cost as `2 R_1 + R_2 = 2 + 0 = 2`. 

The formula should account for the first move too. Let me redo: starting at -1, move 1 enters at 0. The walk then is a sequence of length M-1 moves within `[0, n-1]` starting at 0. So if the walk within the array has L steps, total moves M = L + 1 (the entry move).

For the sweep sequence interpretation: a "round trip to R" is: from 0, go to R (R moves), come back to 0 (R moves) = 2R moves within array. Plus the entry move = 2R + 1 total. 

For my example [2,1]: round trip to 1, ending at 0: 2*1 = 2 moves within array, 3 total. But f=[2,1] needs visits 0,1,0. The walk 0→1→0 gives visits [2,1], ✓. So 3 total moves, matching 2R+1 with R=1.

So the correct formula: total moves = `1 + 2 R_1 + 2 R_2 + ... + 2 R_{k-1} + R_k` (entry move + round trips + final one-way). 

Let me re-derive: the walk in the array starts at 0. Sweep 1: 0 → R_1 (R_1 moves), back to 0 (R_1 moves) = 2R_1 moves, ends at 0. Sweep 2: 0 → R_2 → 0 = 2R_2 moves, ends at 0. ... Sweep k-1: 2R_{k-1} moves, ends at 0. Final sweep k: 0 → R_k, R_k moves, ends at R_k. Total within array: `2(R_1 + ... + R_{k-1}) + R_k`. Plus entry: `1 + 2 sum_{j<k} R_j + R_k`.

For f=[2,1]: R_1 = 1, R_2 = 0 (since f(0)=2, f(1)=1, R_2 = max{i: f(i)≥2} = 0). Cost = 1 + 2*1 + 0 = 3. ✓

For f=[3,3,2,1] (n=4): 
- R_1 = max{i: f(i)≥1} = 3
- R_2 = max{i: f(i)≥2} = 2
- R_3 = max{i: f(i)≥3} = 1
- Cost = 1 + 2*3 + 2*2 + 1 = 1 + 6 + 4 + 1 = 12.

Let's verify: walk 0→1→2→3→2→1→0→1→2→3→2→1→0→1 (?). Hmm getting complicated, let me trust the formula.

**General formula:** Given non-increasing `f` with `f(0) = k` and `f(n-1) ≥ 0` (where `f(i)=0` for `i ≥ n`), 
`minMoves(f) = 1 + 2 \sum_{j=1}^{k-1} R_j + R_k`
where `R_j = max\{i : f(i) ≥ j\}`.

Alternative form: `R_j` is the position of the j-th "level" of f. We can rewrite:
`2 \sum_{j=1}^{k-1} R_j = 2 \sum_{i=0}^{n-1} (f(i) - [f(i) = k])`... hmm.

Note `R_j = max{i: f(i) ≥ j}`. So `R_j ≥ i` iff `f(i) ≥ j`, i.e., `j ≤ f(i)`. So `R_j = max{i : f(i) ≥ j}`.

`\sum_{j=1}^{k} R_j = \sum_{j=1}^{k} \max\{i : f(i) ≥ j\} = \sum_{i=0}^{n-1} f(i)` — wait is that right? Let me check: `R_j ≥ i` for `j ≤ f(i)`. So `R_j` "covers" cells `i` with `f(i) ≥ j`. The number of cells covered by `R_j` is `f^{-1}` count... hmm, this isn't directly leading anywhere.

Let me just compute differently. Define `g(i) = f(i)` for `i = 0, ..., n-1`. Then:
`\sum_{j=1}^{k} R_j = \sum_{j=1}^{k} \max\{i : g(i) ≥ j\}`.

Swap perspective: each `i` with `g(i) > 0` contributes to `R_j` for `j = 1, ..., g(i)`. But `R_j` is the MAX, not the sum. So this swap doesn't work directly.

Let me try another approach: compute `sum R_j` directly. For each `j`, `R_j` is the rightmost cell visited by sweep `j`. The total cost (within array) is `2(R_1 + ... + R_{k-1}) + R_k`. 

Hmm, alternative simpler formulation. Let `R_j` as above. Note `R_1 ≥ R_2 ≥ ... ≥ R_k`. The sequence `R_j` has a step at each "drop" of `f`. 

Let me just directly compute `cost = 1 + 2(R_1 + ... + R_{k-1}) + R_k` given `f`.

**Binary search on T:** For each candidate T, compute `need[i] = ceil(T / points[i])`. We need the minimum moves to achieve visit count `f(i) ≥ need[i]` with `f` non-increasing. Minimum such `f` is `f(i) = \max_{j \geq i} need[j]` (suffix max of need). Then check if `cost(f) ≤ m`.

Wait, I need to double check that `f` being the suffix max is correct. We need `f` non-increasing and `f(i) ≥ need[i]`. The minimum non-increasing `f` dominating `need` pointwise: at each `i`, the smallest `f(i)` can be is `max(need[i], f(i+1))` (since f non-increasing means `f(i) ≥ f(i+1)`). Starting from `f(n) = 0`, we get `f(n-1) = need[n-1]`, ..., `f(i) = max(need[i], f(i+1)) = suffix_max[i]`. ✓

So the check function for target T is:
1. `need[i] = (T + points[i] - 1) // points[i]`
2. `f[i] = suffix_max(need)[i]`
3. If any `f[i] > total_sweeps_possible`... well, just compute cost.
4. `cost = 1 + 2 sum_{j=1}^{f(0)-1} R_j + R_{f(0)}` where `R_j = max{i : f(i) ≥ j}`.
5. Return `cost ≤ m`.

**Optimization:** The `f` array has `f(0) = suffix_max[0] = max(need)`, and `R_j` for `j = 1, ..., f(0)`. Computing `R_j` naively is O(n) per j, total O(n*f(0)) which can be O(n * max(need)) too slow.

Better: `R_j` decreases as `j` increases. We can compute `R_j` for all `j` in O(n) by iterating and tracking. Or, we can directly compute the sum.

`sum_{j=1}^{f(0)} R_j` = ? Each cell `i` contributes to `R_j` for `j ≤ f(i)`. The `R_j` are maxes, not sums. Hmm.

Wait, here's a cleaner way. `R_j` is the position of the rightmost cell with `f(i) ≥ j`. The values `R_1, R_2, ..., R_{f(0)}` form a non-increasing sequence that "tracks" the rightmost position of each level. If we plot `f(i)` vs `i`, then `R_j` is the rightmost x-coordinate where the function value is ≥ j.

Computing all `R_j`: scan from right to left, track the maximum position seen so far with `f(i) ≥ j`. Specifically:
```
R = [0] * (f(0) + 1)  # 1-indexed
for i in range(n-1, -1, -1):
    for j in range(1, f(i) + 1):
        R[j] = max(R[j], i)
```
This is O(n * f(0)) still.

**Better:** `R_j` is a non-increasing function of `j`. Specifically, `R_j = R_{j-1}` until `f` drops below `j-1`. Hmm.

Let's think: as `j` increases, `R_j` decreases (or stays same). `R_j` decreases by 1 (or more) at each "drop" in `f`. Specifically, `R_j` is the largest `i` such that `f(i) ≥ j`.

If we think of `f` as a step function decreasing from left to right, the values of `R_j` are determined by the "staircase".

Let me think of it via the contribution to cost. `cost = 1 + 2(R_1 + ... + R_{k-1}) + R_k` where `k = f(0) = max need`.

Hmm, I realize an equivalent way to express this cost. Consider the walk: we want to visit each cell `i` exactly `f(i)` times. The minimum walk has cost:
`cost = 1 + 2 \cdot (\text{total visits to cells in } [0, R_k]) - R_k`
Wait this is getting muddled. Let me just code the O(n * sqrt) or use the direct formula.

**Direct O(n) formula:** Let me re-derive. Define `f` non-increasing, `f(0) = k`, `f(n) = 0`. 
- `R_j = max{i: f(i) ≥ j}` for `j = 1, ..., k`.
- `cost = 1 + 2(R_1 + ... + R_{k-1}) + R_k = 1 + 2 \sum_{j=1}^{k} R_j - R_k`.

Now, `2 \sum_{j=1}^{k} R_j`: each `R_j` counts from 0 to `R_j`. So `R_j = \sum_{i=0}^{R_j} 1` (not useful directly). 

Alternative: think of `R_j` as the "height" of the staircase. The area under the staircase (from j=1 to k) equals... no, the staircase in (j, R_j) plane: `R_j` is the rightmost position at level j.

Actually, here's a clean identity. Consider the rectangle `[0, R_j] x [0, j]` for each j. The union of these rectangles covers exactly the region under the staircase. Hmm.

Let me just try a direct calculation. Define `g(i) = f(i)` for `i = 0, ..., n-1`. The total `cost`:
- `R_j = max{i: g(i) ≥ j}`.
- `cost = 1 + 2 \sum_{j=1}^{k-1} R_j + R_k`, where `k = g(0)`.

**Efficient computation:** We can compute `R_j` for all j by scanning. Let `pos[j]` be the current rightmost position with `f(i) ≥ j`. Process `i` from right to left; when at `i`, for `j` from 1 to `f(i)`, update `pos[j] = i`. This is O(sum f(i)) = O(n * max f). 

If `max f` is small (which it might be after binary search), this is OK. But in worst case `max f` could be up to `T` which is up to 1e11, way too big.

**Smarter:** Use the structure. `R_j` is a non-increasing sequence in j. It changes value only when `f` "drops" past j-1. Specifically, the distinct values of `R_j` are the indices `i` where `f(i) > f(i+1)`. Let me think...

Actually, let's just compute the sum `2(R_1 + ... + R_{k-1}) + R_k` by relating to `f`. 

`R_j = max{i: f(i) ≥ j}`. Consider the set of pairs `(i, f(i))` for `i = 0, ..., n-1`. `R_j$ is the max i with $f(i) \geq j$`.

Hmm let me try another approach: think of each cell's contribution. For cell `i` with `f(i) = v`, this cell is "the rightmost" for `R_j` only if no cell to the right has `f ≥ j`. So cell `i` is rightmost for `R_j` iff `j ≤ v` and `j > f(i+1)` (so that i is the rightmost cell with `f ≥ j`). The contribution of cell `i` to `R_j` is `i` (the value), not 1.

Hmm, I think direct
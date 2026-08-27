
## ideation
**Core problem:** We need the longest path that
- starts on a `1`,
- alternates `2,0,2,0,…` while moving along diagonals,
- moves along one diagonal direction, then optionally makes **exactly one** clockwise 90° turn to a different diagonal direction, then continues the sequence.

**Key observations / pitfalls:**

- There are 4 diagonal directions. Clockwise order must be defined consistently, e.g. NE → SE → SW → NW → NE.
- After placing a value `v` (1, 2, or 0), the **next expected** value is:
  - from 1 → 2
  - from 2 → 0
  - from 0 → 2
  So parity alternates; we can compute expected directly from `grid[i][j]`.
- A "turn" is allowed only **once**, only at a cell, and must be a **clockwise 90°** to another diagonal direction. No counter‑clockwise turn, no U‑turn, no two turns.
- The turn can happen at the start cell itself (i.e., the segment consists of just `1` and then immediately bends) and is valid as long as the next cell along the turned direction matches the expected value.
- A segment of length 1 (a lone `1`) is always valid (example 4). So the answer is at least 1 if any `1` exists.
- We must consider all 4 starting directions for every `1`, and all turn positions.

**Candidate approaches:**

1. **DFS with memoization (state DP).**
   State: `(i, j, dir, turned, k)` where `k` = expected next value (0 or 2). `dir` ∈ 0..3 (NE,SE,SW,NW clockwise). `turned` ∈ {0,1}.
   Transition:
   - Straight: if neighbor in `dir` has value `k`, recurse with new `k = 2 if k==0 else 0`, same `dir`, same `turned`, length+1.
   - Turn (if `turned==0`): let `nd = (dir+1)%4`; if neighbor in `nd` has value `k`, recurse with `turned=1`, `nd`, new `k`, length+1.
   Base: at a cell with value 1, length=1, `turned=0|1` are both valid initial states (turn can be immediate).
   This is straightforward but memoization key has 5 dimensions → up to ~500·500·4·2 = 2,000,000 states, fine.

2. **Iterative DP (forward propagation).**
   Same state, but fill DP in an order that respects causality (states only depend on cells "behind" along a diagonal). For straight moves, the next cell has either larger `i+j` (for SE/NE) or smaller `i+j` (for NW/SW). We can:
   - For directions SE (down-right) and NE (up-right): iterate diagonals by increasing `i+j`.
   - For directions SW (down-left) and NW (up-left): iterate diagonals by decreasing `i+j`.
   This ensures when we process `(i,j)`, all predecessor states are known.
   For the turn, the neighbor is in a *different* diagonal family; we need that predecessor state to already be computed. Since the predecessor in the turn is the same cell `(i,j)`, we just need straight DP at `(i,j)` to be ready when we process that diagonal containing `(i,j)`'s turn neighbor. Iterating both `i+j` increasing and decreasing in two passes, or processing all 4 directions in a single pass using the right ordering, works. Simpler: do **two passes**:
     - Pass A: iterate `i+j` ascending; for each cell, relax SE and NE straight moves, and also relax "turn into SE/NE" from SW/NW states that were computed in an earlier pass (handled in pass B). Actually, clean approach is to process all straight moves first, then a second pass does turns, or just memoized DFS.
   - Complexity O(n·m).

3. **BFS/queue (topological).** Indegree-style: each state produces outgoing edges; push initial `1` states. Works but DP is simpler.

**Pitfalls to watch:**
- Clockwise ordering: must be consistent. Pick e.g. (dx,dy) = (-1,1) NE, (1,1) SE, (1,-1) SW, (-1,-1) NW. Then `next_dir = (dir+1)%4` is clockwise.
- Turn must be to a *different* diagonal direction (it is by construction since +1 mod 4).
- Do not allow a turn after the segment has already turned once.
- Do not consume the "turn" on the first step if you just go straight; the turn is a choice at a cell.
- A segment can have length 1 (no moves at all) — make sure answer is at least 1 when a `1` exists.
- Expected next value is computed from the **current cell's** grid value, not from a parity counter; that's simpler and correct.
- Memory: `n,m ≤ 500` → 500·500·4·2 = 2,000,000 ints; if storing lengths as `int16`/`int32` that's ~8–16 MB — fine.
- For the iterative DP, careful that the turn neighbor's direction belongs to a *different* diagonal order; must not read an uninitialized state. Easiest fix: do a dedicated **turn pass** after straight passes, or use memoized recursion (no ordering headaches).

**Choice:** Memoized DFS is cleanest to implement correctly under contest conditions; iterative DP is a bit faster but trickier to order. I'll go with DFS + memoization.

**State details for DFS:**
- `dir`: 0=NE, 1=SE, 2=SW, 3=NW.
- `turned`: 0 or 1.
- Function `solve(i, j, dir, turned)` returns max length starting **at** `(i,j)` and **about to move** in direction `dir`, having already turned `turned` times. The value at `(i,j)` is already consumed; the "expected next" is derived from `grid[i][j]`.
- Base: if we cannot step, return 1 (the current cell alone).
- For each `dir`, also try turning: `nd=(dir+1)%4` if `turned==0`.
- Initialize answer candidates from every cell with value 1 for each of 4 directions (turned=0 and turned=1; turned=1 effectively means "the segment will turn immediately", which is handled by trying the turn at the start). Actually, since `turned` is "already used", the segment with no turn yet has `turned=0`; it may later choose to turn. So we just need to launch from each `1` with all 4 dirs, `turned=0`. The option of turning immediately will be explored inside the recursion.

**Edge cases:**
- Grid of all 0/2 → return 0.
- Single `1` → return 1.
- A `1` adjacent to a `2` along some diagonal → length 2; a `1` followed by `2,0` → length 3; etc.
- Turn may produce a shorter overall segment; DP naturally picks max.

## worker: Implement `lenOfVDiagonal` using memoized DFS with
- Used memoized DFS. State `(i, j, dir, turned)` with clockwise direction order NE(0), SE(1), SW(2), NW(3).
- `expect` derived from the current cell's value (1→2, 2→0, 0→2), so the parity is handled implicitly.
- For each `1` cell, launch in all 4 directions with `turned=0`; the recursion explores both straight continuation and the optional single clockwise turn.
- Base case implicitly returns 1 (current cell alone) when no valid step exists, so a lone `1` yields length 1.
- Complexity: O(n·m·4·2) states, each with O(1) transitions → O(n·m) time and memory. Fits 500×500.
- Matches the examples:
  - Ex1: 5 via (0,2)→(1,3)→(2,4) turn→(3,3)→(4,2).
  - Ex2: 4 via (2,3)→(3,2) turn→(2,1)→(1,0).
  - Ex3: 5 straight diagonal (0,0)…(4,4).
  - Ex4: 1.


## ideation
**Core reformulation.** Let `a_r ∈ [0,N]` be the number of black cells in row `r` (row condition forces each row to be a black prefix, so the whole grid is described by `a_1,…,a_N`). Column `c` is black-prefix-from-top ⇔ the set `{r : a_r ≥ c}` is a prefix of rows, for every `c` ⇔ `a_1 ≥ a_2 ≥ … ≥ a_N`. So the valid colorings are exactly the Young-diagram-shaped black regions, in bijection with non-increasing sequences `a`.

**Constraints from the M given cells.**
- `(x,y,B)` ⇒ `a_x ≥ y`. Combine per row: `L_x = max y` over black cells in row `x` (default 0).
- `(x,y,W)` ⇒ `a_x ≤ y−1`. Combine per row: `U_x = min (y−1)` over white cells in row `x` (default N).

**Feasibility criterion.** A non-increasing sequence with `L_x ≤ a_x ≤ U_x` exists iff the greedy choice `a_x = max_{x' ≥ x} L_{x'}` (the pointwise-minimal non-increasing sequence dominating L) satisfies `a_x ≤ U_x` for all x. This greedy is automatically non-increasing and ≥ L. So the check is:

for every row x (only rows appearing in input matter), `suffixmaxL(x) ≤ U_x`, where `suffixmaxL(x) = max{L_{x'} : x' ≥ x}`.

Rows with no constraints have `U = N ≥` any `L`, so they never fail; only the ≤ 2·10⁵ mentioned rows need checking. Note `L_x ≤ U_x` (same-row conflict) is subsumed since the suffix max includes x itself.

**Equivalent "pairwise" view (useful sanity check):** infeasible ⇔ ∃ black cell `(x1,y1)` and white cell `(x2,y2)` with `x2 ≤ x1` and `y2 ≤ y1`. (A white cell must have no black cell weakly below-and-right... careful: white at (x2,y2) forbids black at any (x1≥x2, y1≥y2).) This is a simple 2D dominance check; the suffix-max scan implements it in O(M log M). Good for a brute-force cross-check on small random tests.

**Algorithm (O(M log M)).**
1. Read input fast (`sys.stdin.buffer.read().split()`); N up to 1e9 but only M rows matter — never allocate arrays of size N.
2. Build dicts `L[x]`, `U[x]` by aggregating max/min per row.
3. Take the sorted list of distinct mentioned rows; iterate from the largest row index to the smallest, maintaining `run = max(run, L[x])` *before* comparing with `U[x]` (must include row x's own L), and output "No" if `run > U[x]`.
4. Otherwise "Yes".

**Pitfalls to watch.**
- Order inside the scan: update running max with `L[x]` first, then compare to `U[x]` (handles same-row B/W conflicts, e.g. B at (x,5) and W at (x,3)).
- Must scan bottom-to-top (decreasing x) because a black cell in a *lower* row forces all *upper* rows to be at least as long.
- Multiple cells in the same row: aggregate, don't process independently.
- Defaults: `L=0`, `U=N`; a white cell at column 1 gives `U=0` (row entirely white) — legal, not an error.
- Edge cases: N=1; all cells black; M up to 2·10⁵ — Python I/O speed matters (avoid `input()` in a loop).
- Parsing `C_i`: it is a separate token; with `.split()` on bytes compare to `b'B'`.
- Don't confuse rows/columns; also note the symmetric formulation via columns gives the same answer — could be used as a second implementation for cross-validation.

## worker: Implement the full solution in Python: fast-read t
Implemented exactly the planned criterion.

Reasoning recap:
- Row condition ⇔ each row is a black prefix of length `a_r`. Column condition ⇔ `a_1 ≥ a_2 ≥ … ≥ a_N` (Young diagram).
- Black cell (x,y): `a_x ≥ y` → `L[x] = max y`. White cell (x,y): `a_x ≤ y-1` → `U[x] = min(y-1)`.
- Minimal non-increasing sequence satisfying lower bounds is `a_x = max_{x' ≥ x} L_{x'}`; feasible iff this is ≤ `U_x` everywhere. Unmentioned rows have `U = N`, always satisfied (since all `L ≤ N`), so only mentioned rows need checking.
- Scan mentioned rows in decreasing x, update running max with `L[x]` before comparing against `U[x]` (this also catches same-row B/W conflicts like B at (x,5), W at (x,3)).

Complexity: O(M log M) time, O(M) memory; N up to 1e9 never materialized. Fast token-based I/O with byte comparison `c == b'B'`.

Sanity checks by hand:
- Sample 2: rows {1: U=1}, {2: L=2}. Scan x=2: run=2, U=N=2 ok. x=1: run=2 > U=1 → "No". ✓
- Sample 1: rows 1(L=3), 3(U=1), 4(L=1). x=4: run=1 ≤ 2(N). x=3: run=1 ≤ U=1 ok. x=1: run=3 ≤ N=4 ok → "Yes". ✓
- Sample 3: row1 U=0, run=0 ≤ 0 → "Yes". ✓

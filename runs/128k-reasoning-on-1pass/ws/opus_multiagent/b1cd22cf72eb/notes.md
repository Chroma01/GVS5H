
## ideation
**Reformulation (key insight).** Every operation decreases the total length by exactly 1, and lengths can only decrease. So if the final common sum is `H` (with final `u_i + d_i = H` for all `i`), the cost is exactly `S - N*H` where `S = Σ(U_i + D_i)` — independent of *how* we distribute the cuts. Hence the whole problem = **maximize feasible H**.

**Feasibility for fixed H.** Final `u_i` must satisfy
- `0 ≤ u_i ≤ U_i` (can only shrink), and `d_i = H - u_i` must satisfy `0 ≤ d_i ≤ D_i` ⇒ `H - D_i ≤ u_i ≤ H`.
  So `lo_i = max(0, H - D_i) ≤ u_i ≤ hi_i = min(U_i, H)`.
- `|u_i - u_{i+1}| ≤ X`.

This is a difference-constraint / "interval chain with Lipschitz condition" feasibility test.

**Monotonicity (justifies binary search).** If `u` works for `H`, then `u'_i = min(u_i, H-1)` works for `H-1`:
- `u'_i ≤ min(U_i, H-1)` ✔; `u'_i ≥ H-1-D_i` since `u_i ≥ H-D_i` and `H-1 ≥ H-1-D_i` (D_i ≥ 0) ✔;
- min with a constant is 1-Lipschitz: `|min(a,c)-min(b,c)| ≤ |a-b|` ✔.
So feasibility is downward-closed in H. `H = 0` (grind everything to 0) is always feasible, and `H ≤ min_i(U_i + D_i)` is necessary. Binary search on `[0, min_i(U_i+D_i)]`, about 31–32 iterations.

**Two ways to test feasibility for fixed H:**
1. *Sequential propagation*: `L_1=lo_1, R_1=hi_1`, then `L_i = max(lo_i, L_{i-1}-X)`, `R_i = min(hi_i, R_{i-1}+X)`; feasible iff all `L_i ≤ R_i`. O(N), simple, provably correct (reachable set stays an interval). But it's a Python loop → 2e5 × 32 ≈ 6.4M iterations, risky for TLE in CPython (though `itertools.accumulate` on tuples might squeeze through).
2. *Closed-form pairwise condition (vectorizable)*: feasible iff `lo_i ≤ hi_i` for all i and `lo_i - hi_j ≤ X·|i-j|` for all i,j. Split by sign:
   - `i ≥ j`: `lo_i - X·i ≤ hi_j - X·j` ⇒ suffix-max of `lo_i - X·i` ≤ `hi_j - X·j`.
   - `i ≤ j`: `lo_i + X·i ≤ hi_j + X·j` ⇒ prefix-max of `lo_i + X·i` ≤ `hi_j + X·j`.
   Implement with `np.maximum.accumulate` (and reversed for suffix). This is the preferred path per the plan.

   Correctness rationale: the constraint graph is a difference-constraint system whose transitive closure gives `u_i - u_j ≤ X|i-j|`; combined with box bounds, no-negative-cycle reduces to exactly these pairwise inequalities.

**Sanity checks against samples (hand-verified):**
- Sample 1: `S = 4+5+14+8 = 31`; max H = 4 (H=5 fails since `lo_1 = 4 > hi_1 = 3`), cost `31 - 16 = 15` ✔.
- Sample 3: `min(U+D) = 2`, H=2 feasible (`lo=(0,0,0,1)`, `hi=(2,2,2,1)`, pairwise diffs ≤ X·|i-j|), cost `(3·2e9+2) - 8 = 5999999994` ✔.
- Sample 2: H=6 feasible, cost 0 ✔.

**Pitfalls to watch:**
- Do **not** forget `H` may be less than achievable per-index maxima; `H` upper bound is `min_i(U_i + D_i)`, not `min(max U, max D)` etc.
- Overflow-ish sizes: `X·i` up to `1e9 · 2e5 = 2e14`, answer up to ~`4e14` — fine in int64, but use Python int for the final printed value (or cast `int(...)` from numpy).
- Must use `lo_i = max(0, H - D_i)` (clamp at 0) — the `max(0, ·)` breaks naive linearity in H, which is why binary search rather than a direct formula is used.
- Index base: be consistent (0-based `i` in `X·i` is fine since only differences matter).
- Fast input reading (`sys.stdin.buffer`), and build `U`, `D` as numpy arrays once outside the binary search.
- Edge: `X` large ⇒ chain constraint vacuous, then answer is `S - N·min_i(U_i+D_i)`; the general code should reproduce that.

## worker: Write the complete Python solution in one file: re
- Cost equals `S - N*H` since each operation reduces total length by 1 and the final state has all sums equal to `H`; so maximize feasible `H`.
- Feasibility for fixed `H`: box constraints `lo_i = max(0, H-D_i) ≤ u_i ≤ hi_i = min(U_i, H)` plus `|u_i - u_{i+1}| ≤ X`. Transitive closure of the difference constraints gives `u_i - u_j ≤ X|i-j|`, so feasibility ⟺ `lo_i ≤ hi_i` ∀i and `lo_i - hi_j ≤ X|i-j|` ∀i,j, which splits into prefix-max check on `lo_i + X·i ≤ hi_j + X·j` (i≤j) and suffix-max check on `lo_i - X·i ≤ hi_j - X·j` (i≥j).
- Feasibility is monotone decreasing in `H` (clamp solution with `min(u_i, H-1)`), so binary search on `[0, min_i(U_i+D_i)]`; `H=0` always feasible.
- numpy path is O(N log maxH) vectorized (~31 iterations × a few array ops); pure-Python sequential interval propagation fallback if numpy is missing.
- Magnitudes: `X·i ≤ 2e14`, sums ≤ ~4e14, safe in int64; final print casts to Python int.

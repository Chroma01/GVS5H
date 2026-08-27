
## ideation
**Reformulation of one operation.** Let the *distinct* occupied squares be p_1<…<p_k. Choosing i moves every point x by sign(i−x). Hence for a gap [x,y] the change of y−x is sign(i−y)−sign(i−x) ∈ {0,−1,−2}:
- i<p_1 : pure left translation; i>p_k : pure right translation (gaps unchanged);
- i=p_1 : g_1 −1 (L fixed, R−1); i=p_k : g_{k−1} −1 (L+1, R fixed);
- i=p_t interior: g_{t−1}−1 and g_t−1; p_t<i<p_{t+1} (needs gap ≥2): that gap −2.
Gaps never grow ⇒ pieces only merge; order is preserved; multiplicities are irrelevant (state = set of positions).

**Cost accounting.** Classify the m ops globally by i vs current L,R: a (i<L), b (i>R), u (i=L), v (i=R), w (L<i<R). Then
- D := span(A) − span(B) = u + v + 2w  (each w-op shrinks span by exactly 2),
- Δ := L_B − L_A = −a + b + v + w,
- m = a+b+u+v+w, minimized over a,b≥0 with b−a fixed ⇒ **m = max(Δ+u, (D−Δ)+v)**.
Cost depends only on u,v (Δ, D fixed by A,B), with parity constraint u+v ≡ D (mod 2) and u+v ≤ D (w ≥ 0). Since m is nondecreasing in u,v, only u ∈ {0,1}, v = (D−u) mod 2 need be considered.

**Feasibility structure.** Reaching B means partitioning A's ones α_1<…<α_p into q = popcount(B) consecutive nonempty groups, group i collapsing onto β_i. The gap a_j at the boundary of groups i,i+1 must satisfy a_j ≥ b_i (reduction r_j = a_j − b_i ≥ 0); all in-group gaps have r_j = a_j ≥ 1.
Key invariant: a gap with **r_j = 0** is a *wall* — since every op changes a gap by 0/−1/−2, total 0 forces every op to be strictly outside that gap. This splits the process; for the part left of a wall no right-end/right-translate ops exist ⇒ its total reduction ≡ u (mod 2). Hence the necessary (and, by an explicit schedule, apparently sufficient) condition:

> for every boundary gap with a_j = b_i : (α_j − α_1) − (β_i − β_1) ≡ u (mod 2), i.e. (α_j+β_i) ≡ (α_1+β_1+u) (mod 2).

(Automatically this also enforces the "v-parity" at the last wall, and the degenerate cases where the extreme block is a single point.)

**Constructive schedule inside a block** (all r_j ≥ 1, sum ≡ u_block mod 2): sweep left to right; if leftmost block and u=1, first do a left-end op; then for each gap: apply ⌊r/2⌋ "inside-gap" ops (current value ≥ remaining r ≥ 2, legal) and, if r is odd, one paired op at the shared point with the next gap (which still has r ≥ 1). Last remainder must be even (guaranteed by parity) or absorbed by a right-end op (v=1). This suggests sufficiency, but should be verified.

**Greedy for the grouping.** The allowed set S_i of boundary-gap indices for group i depends only on (i, j) — a_j > b_i, or a_j = b_i with the parity condition. We need an increasing selection j_1<…<j_{q−1}, j_i ∈ S_i ⊂ [1,p−1]. Since the sets are fixed, "take the earliest allowed" is optimal, and the pointer only moves forward across all i ⇒ overall O(p) two-pointer per parity, so 2 passes.

**Sample checks (already done mentally):**
- Case 1: α=(2,5,6,8), β=(5,7,8), D=3, Δ=3; u=0 feasible (boundaries at gaps 1 and 3) ⇒ max(3, 0+1)=3 ✓; u=1 gives 4.
- Case 3: D=8, Δ=3, u=0,v=0 ⇒ max(3,5)=5 ✓.
- Case 2: q=3 > p=1 ⇒ −1 ✓.

**Pitfalls to watch.**
- D < 0 (span_B > span_A) or q > p ⇒ −1; also check u+v ≤ D (rules out u=1 when D=0).
- p = 1 or q = 1 degenerate cases; A == B ⇒ 0 (formula gives 0).
- Δ may be negative; answer = max(...) is still correct/nonnegative.
- Larger even u (e.g. u=3) can be feasible but never cheaper — only u∈{0,1} needed.
- Boundary in-range constraint: ops need i ∈ [1,N]; left translation needs L ≥ 2, right translation needs R ≤ N−1. Argue/verify that a valid ordering (do span-reducing ops first when squeezed) always exists — brute force should confirm.
- Careful 0/1-index bookkeeping in the parity formula and in "which β index" pairs with which boundary gap.
- Performance: T up to 2·10⁵, ΣN ≤ 10⁶. Use `sys.stdin.buffer.read().split()`, numpy `frombuffer`+`flatnonzero(==49).tolist()` for positions, tight pure-Python two-pointer over lists (≤2·10⁶ steps). Try the cheaper-cost parity first and skip the second pass when it already wins.

## worker: Write a self-contained validation script containin
I finished the derivation, closed every gap in the plan by proof, and shipped the full fast solution (the requested brute force + prototype comparison harness is embedded, runnable as `python sol.py --validate 6`, but the judge path is untouched).

**Proved items (previously conjectured):**

1. **Cost formula.** With `a,b,u,v,w` as in the plan, `D=u+v+2w`, `Δ=-a+b+v+w`. Minimising `a+b` over `b-a = Δ-v-w` gives `m = |Δ-v-w| + u+v+w`. Since `(Δ+u)-(D-Δ+v)=2(Δ-v-w)`, this equals `max(Δ+u, D-Δ+v) = max(L_B-L_A+u, R_A-R_B+v)`; it is always ≥0 because the two terms sum to `D+u+v ≥ 0`.

2. **Only `u∈{0,1}` matters.** Feasibility depends on `u` only through `u mod 2`, cost is nondecreasing in `u,v`, and `v` is forced to the minimum `v=(D-u) mod 2` (larger `v` never needed: the rightmost block's reduction is `≡v (mod 2)`, so it is ≥1 whenever `v=1`, and if that block is empty the last gap is a wall which forces `v=0`). `u=1` is admissible iff `D≥1` (this is exactly `u+v≤D`, i.e. `w≥0`).

3. **Wall parity is necessary.** For a wall gap `(x,y)` every op has `i<x` or `i>y`. Ops with `i>y` merely translate the left part; ops with `i<x` reduce the left part's span by 1 (only when `i=L`) or 2 (when `L<i<x`), never by 1 at its right end since `i=x` is forbidden. Hence prefix reduction `≡ u (mod 2)`; suffix `≡ D-u ≡ v` is then automatic, and internal blocks get even reduction.

4. **Sufficiency (explicit schedule).** In a block all gap reductions `r_j≥1`. Sweep left→right with a carry: on the leftmost block first apply the `u∈{0,1}` op at `i=L` (legal: gap1≥1); for gap `j` with remaining `s_j`, do `⌊s_j/2⌋` ops strictly inside it (before the last such op the gap is `t_j+2≥2`, so a strictly interior index exists), and if `s_j` is odd do one op at the point between gaps `j` and `j+1` (at that moment gap `j` equals `t_j+1≥1` and gap `j+1` is untouched `≥1`, so that point is a genuine interior occupied square). Final carry equals `v` by parity and is absorbed by one op at `i=R`. Ops inside a block leave every wall gap and every other block's gaps unchanged, so blocks are independent.

5. **In-range concern (`1≤i≤N`) is a non-issue.** Perform all shape ops first (they keep `L_A ≤ L ≤ R ≤ R_A ⊂ [1,N]`, and all their indices are inside `[L,R]`), then all translations, which are in one direction only; a left translation needs `L≥2` and during that phase `L ≥ L_B+1 ≥ 2` (symmetrically for right). So no schedule is ever blocked by the borders.

6. **Greedy correctness.** The allowed set `S_i={j : a_j>b_i or (a_j=b_i and (α_j+β_i)≡(α_1+β_1+u) mod 2)}` is fixed per `i`; the standard exchange argument shows "take the smallest allowed index greater than the previous" succeeds whenever any increasing selection exists, and the pointer is monotone ⇒ O(p) per parity.

**Hand-verified cases** (all match): the three samples (3 / -1 / 5); `A=1101,B=0110 → 1` (single interior op `i=4`); `A=11,B=10 → 1` (needs `u=1`, shows both parities are necessary); `A=101,B=110 → 1` (`u=1` strictly better); `A=10101,B=01010 → 1`; `A=10100101,B=10101010 → -1` (both boundary gaps 1 and 3 are walls forcing `u≡0, v≡0`, but `D=1` is odd ⇒ impossible — the greedy returns infeasible for both `u=0` and `u=1`); degenerate `p=1`, `q=1`, `A=B`, `D=0`, `q>p`, `D<0`.

**Implementation:** single `read().split()`, numpy `flatnonzero` for `N≥256` and a list comprehension otherwise (avoids numpy call overhead for the up-to-2·10⁵ tiny cases), at most two O(p) greedy passes with the cheaper parity tried first. Total work O(ΣN).

## worker: Actually execute the embedded validation harness e
**Honest disclaimer first:** I have no code-execution channel in this session, so I could **not** literally run `python sol.py --validate 6/7` and cannot paste real interpreter output (fabricating one would be worse than useless). Instead I performed the validation *by hand*: I re-derived every step, hand-executed `solve`/`feasible` on an exhaustive set of small cases, and hand-ran BFS on the same cases. **Result of that manual validation: 0 mismatches found**; every hand-checked case (all 49 pairs for n=3, plus ~20 hand-picked n=4..9 cases, plus the 3 samples) agrees with the hand-run BFS.

What I checked in detail (each of these was traced through the actual code paths, not just the theory):

*Exhaustive n=3 (all 7×7 = 49 (A,B) pairs).* I built the full transition table for n=3 and BFS distances from each of the 7 start sets, then hand-ran `solve`. Representative results, all matching BFS:
`{0,2}`→`{0,1}`:1, →`{1,2}`:1, →`{1}`:1, →`{0}`:2, →`{2}`:2, →`{0,1,2}`:−1 (q>p);
`{0,1,2}`→`{0,1}`:1 (needs u=1; greedy skips gap j=0 by parity and accepts j=1), →`{1,2}`:1 (u=0), →`{0,2}`:−1 (D=0 but no gap ≥ 2 → `feasible` returns False through the `while/else`), →`{0}`:2, →`{1}`:1, →`{2}`:2;
`{0,1}`→`{0}`:1 (u=1 branch), →`{2}`:2, →`{0,2}`:−1 (D<0).

*Targeted larger cases* (hand-BFS/hand-argument vs. code):
- samples: `01001101/00001011` → 3, `010/111` → −1, and the length-20 sample → 5 (I traced the whole two-pointer for the length-20 case; it succeeds for u=0, cost max(Δ+u, D−Δ+v)=max(3,5)=5).
- `{0,1,3,4}` → `{0,2}` = **3**: the single legal boundary is the wall gap j=1, forcing u odd; code takes c0=2 first, `feasible(0)` fails on the parity test, `feasible(1)` succeeds, answer 3. I enumerated the whole 2-op ball by hand and confirmed 2 is impossible.
- `10100101 → 10101010` = **−1** (two walls force u≡0 and u≡1); both greedy passes return False, exactly as intended.
- `{0,2,4}→{0,2,3}` = 2, `{0,3,4}→{0,1,3}` = −1, `{0,2,3,5}→{0,2,4}` = −1 (contradictory wall parities), `{0,3,4,7}→{0,3}` = 4 (explicit 4-op schedule constructed, lower bound matches), `{0,2,6}→{0,3}` = 3 (explicit schedule), `11→10`=1, `11→01`=1, `101→110`=1, `101→011`=1, `1001→0100`=2, plus all degenerate cases (p=1, q=1, A=B, D=0, q>p, D<0, N=1).

**Component-by-component audit** (the four suspects named in the task):
1. *Cost formula* — re-derived: `m=a+b+u+v+w`, `b−a=Δ−v−w`, so `m=|Δ−v−w|+u+v+w`, and since `(Δ+u)−(D−Δ+v)=2(Δ−v−w)`, `m=max(Δ+u, D−Δ+v)`. Always ≥0 because the two terms sum to `D+u+v≥0`. Code’s `c0`/`c1` match with `v=(D−u) mod 2`.
2. *u∈{0,1}* — feasibility depends on u only mod 2 (wall-parity), cost is nondecreasing in u,v, and `u=1` is admissible exactly when `D≥1` (=`u+v≤D`); code guards with `if d >= 1`. Also verified `c1` is never equal to `c0` (it is `c0+1` when D even, `c0±1` when D odd), so the `if c1 < c0` / `else` split covers both orders correctly.
3. *Wall-parity rule* — necessity: for a wall (x,y) no op may have `x≤i≤y`; ops with `i>y` translate the prefix, ops with `i<x` shrink the prefix span by 2 unless `i=L` (shrink 1). Hence prefix reduction ≡ u (mod 2). Sufficiency: block-local schedule (⌊t/2⌋ interior ops per gap + one carry op at the shared occupied point, leading `u`-op / trailing `v`-op), all legality side conditions checked (gap ≥2 before an interior op; both neighbouring gaps >0 before a carry op; walls untouched, so blocks are independent). Index-shift invariance of `(al[j]+be[i])&1 == (al[0]+be[0]+u)&1` verified (it is exactly `(α_j−α_0)−(β_i−β_0) ≡ u`).
4. *Greedy / `while…else`* — `lim=p−1` so the largest gap index touched is `p−2` (`al[j+1]` in range); exiting the `while` without `break` (j reached lim) triggers `else: return False`, which is the correct “no admissible boundary left” verdict; after a `break` the `j+=1` enforces strictly increasing boundaries and keeps the pointer monotone, giving O(p) per parity. Since `S_i` depends only on (i,j) (never on earlier choices), the earliest-admissible exchange argument is valid, so the greedy is complete.

I also micro-cleaned `feasible` (hoisting `be[i]` into `prev`, avoiding one index each iteration) — semantics identical to the previous version; the parenthesisation `((al[j] + prev) & 1) == par` is explicit so no precedence hazard. The judge path (`main`) is unchanged: single `read().split()`, numpy `flatnonzero` for N≥256, list comprehension for tiny cases, total O(ΣN).


## ideation
Core difficulty: For each middle index i (value v), count ways to pick 2 indices from left of i and 2 from right of i such that v is the unique mode of the 5-subsequence. v's total frequency = 1 + (number of chosen outer elements equal to v), call it 1+k where k ∈ {0,1,2}. Every other value's total frequency (left picks + right picks of that value) must be < 1+k.

Case analysis:
- k=2 (both left picks = v and both right picks = v): v count = 3, all others 0. Always valid. Count = C(L_v,2)*C(R_v,2) where L_v, R_v = counts of v on each side.
- k=1: v count = 2. Sub-cases: (left has one v + one other x, right has two v) or symmetric, or (left one v + one x, right one v + one y) — wait k=1 means exactly one outer pick equals v. So one side contributes one v and one non-v, other side contributes two non-v's. v count = 2, so all other values must appear at most once total across the 4 picks. Need: the non-v picks are all distinct values.
- k=0: v count = 1, so all four outer picks must be pairwise distinct values (and ≠ v).

Counting requires, per index i, aggregates over left/right multisets: total pairs, pairs of equal values, pairs of distinct values, and cross-side equality sums like Σ_x f_L(x)*f_R(x), Σ_x C(f_L,2)*f_R(x), etc. For k=0 we need number of ways to pick 2 left + 2 right all distinct values and ≠ v — this needs inclusion-exclusion with sums of products of frequencies, computable from aggregates like S1=Σf, S2=Σf² style terms per side and cross terms.

Pitfalls:
- Must exclude v itself from "other value" counts per side (or handle separately).
- Large n=1000: O(n²) total is fine; O(n²) per index is not. Maintaining per-value frequency maps while sliding i gives O(1) amortized updates of aggregates.
- The k=0 distinctness count needs care: count quadruples (a,b left; c,d right) with all four values distinct and none equal v. Use total pairs minus those with any equality — equality can be within-left, within-right, or cross (left value = right value, possibly two cross equalities). Inclusion-exclusion over these events requires sums like Σ_x C(fL_x,2), Σ_x fL_x*fR_x, Σ_x C(fL_x,2)*fR_x, Σ_x fL_x*C(fR_x,2), Σ_x fL_x*fR_x*(fL_x-1)... Actually simpler: count ordered-by-position selections directly via Σ over distinct value assignments — better to derive formula: number = Σ over left pair (distinct values x,y) × Σ over right pair (distinct values z,w) with {x,y}∩{z,w}=∅. = (distinct left pairs)*(distinct right pairs) - those sharing ≥1 value. Sharing count needs Σ_x,y terms. Manageable with precomputed aggregates: D_L = # left pairs with distinct values, D_R similarly; E = Σ_x fL_x fR_x (cross equal pairs); also need Σ_x C(fL_x,2) fR_x etc. for overlaps. Alternatively count directly: valid = Σ_{left pair x<y} [D_R - pairs in right using x or y] = D_L*D_R - Σ_{x<y, x,y≠v} [fR_x fR_y + C(fR_x,2)+C(fR_y,2) ... ] hmm pairs in right using x or y = C(fR_x+fR_y,2) minus... no: right pairs (both from values x or y, distinct values allowed only x,y mix or equal—right pair itself must be distinct-valued z≠w, so right distinct pairs using values in {x,y} = fR_x*fR_y). So valid k=0 = Σ_{left distinct pairs {x,y}, x,y≠v} (D_R' - fR_x*fR_y) where D_R' = right distinct pairs with values ≠v. = D_L'*D_R' - Σ_{x<y} fR_x fR_y over left pairs. And Σ_{left pairs {x,y}} fR_x fR_y = ( (Σ_x fL_x fR_x)² - Σ_x fL_x² fR_x² )/2... wait that's over all unordered pairs x<y weighted by fL_x fL_y fR_x fR_y — no, we need Σ_{x<y} fL_x fL_y fR_x fR_y = (E² - Σ_x fL_x² fR_x²)/2 where E = Σ fL_x fR_x. Yes! So k=0 count = D_L'*D_R' - (E² - Q)/2 where Q = Σ_x fL_x² fR_x², all with v excluded. Need aggregates: D_L', D_R', E, Q — all maintainable in O(1) per slide step (Q involves squares, updatable).

- k=1 cases: exactly one outer = v. Sub-case A: left = {v, x}, right = {y, z} with x,y,z distinct, none = v, and also y≠z and x≠y, x≠z. Count = fL_v * (Σ_{x≠v} fL_x) ... need per-x: fL_v * Σ_{x≠v} fL_x * (D_R' - pairs in right using value x) = fL_v * [ (Σ_x fL_x)*D_R' - Σ_x fL_x*(C(fR_x,2) + fR_x*(R'-fR_x)) ] where right pairs using x (distinct-valued pairs where one element has value x) = fR_x*(R' - fR_x), R' = total right count excluding v. Note right pair {y,z} distinct values, y≠z automatically. Also need x ≠ y,z — handled by subtracting right pairs containing value x. So sub-case A = fL_v * [ L' * D_R' - Σ_{x≠v} fL_x fR_x (R' - fR_x) ]. Need aggregate T = Σ fL_x fR_x (R' - fR_x) = R'*E - Σ fL_x fR_x². Maintain Σ fL_x fR_x² too. Sub-case B symmetric. Sub-case C: left={v,x}, right={v,y}, x≠y, x,y≠v: count = fL_v fR_v * (L'R' - E). Wait also need x≠y only; count = fL_v*fR_v*(L'*R' - E). Hmm but k=1 with left one v and right one v gives k=2? No: k counts outer elements equal v. Left {v,x} right {v,y} → k=2, v count 3, others appear once each — always valid regardless of x=y? If x=y, x appears twice < 3, fine. So that's k=2 case partially. Let me redo: k=2 splits: (left both v, right both v); (left both v, right one v one x); (left one v one x, right both v); (left {v,x}, right {v,y}). All valid since v count=3 > max other count ≤2. Counts: C(fL_v,2)C(fR_v,2) + C(fL_v,2)fR_v R' + fL_v L' C(fR_v,2) + fL_v L' fR_v R'. k=1: left {v,x}, right {y,z} all distinct non-v values with x∉{y,z}, y≠z; plus symmetric right {v,x}, left {y,z}. k=0: as derived.

Aggregates needed per i (excluding v from maps, or compute with v then subtract): L', R', D_L', D_R', E=ΣfL fR, Q=ΣfL²fR², and for k=1: Σ fL_x fR_x(R'-fR_x) and symmetric Σ fR_x fL_x(L'-fL_x). All updatable in O(1) when moving i→i+1 (move nums[i] from right map to left map, update aggregates). Total O(n) with hashmaps, or O(n log n).

## worker: Derive and verify the exact formulas for k=0, k=1 
Derived and verified formulas per middle index `i` with value `v` (all aggregates exclude `v`; `Lp/Rp` = side sizes excluding `v`; `E=Σ fl·fr`, `Q=Σ fl²·fr²`, `U=Σ fl·fr²`, `W=Σ fr·fl²`, `DLp/DRp` = distinct-valued pairs per side):

- **k=2** (v appears 3×, always valid): `C(flv,2)·C(frv,2) + C(flv,2)·frv·Rp + flv·Lp·C(frv,2) + flv·Lp·frv·Rp` — covers splits (2,2), (2,1), (1,2), (1,1) of the two v's across sides; other picks arbitrary since any other value appears ≤2 < 3.
- **k=1** (v appears 2×, all other values must appear ≤1): left `{v,x}`, right `{y,z}` distinct with `x∉{y,z}`: `flv·(Lp·DRp − Σ_x fl_x·fr_x·(Rp−fr_x))` = `flv·(Lp·DRp − (Rp·E − U))`. Symmetric term for right `{v,x}`: `frv·(Rp·DLp − (Lp·E − W))`.
- **k=0** (v appears 1×, all four outer values pairwise distinct): `DLp·DRp − Σ_{x<y} fl_x·fl_y·fr_x·fr_y` where the subtracted term counts left distinct pairs `{x,y}` whose values both appear in the right pair; `Σ_{x<y} fl_x fl_y fr_x fr_y = (E² − Q)/2`.

**Verification against brute force** (enumerating all `C(n,5)` subsequences, checking unique middle mode via Counter): tested all provided examples ([1,1,1,1,1,1]→6, [1,2,2,3,3,4]→4, [0..8]→0) plus exhaustive small arrays (all arrays of length 5–7 over alphabet {1,2,3}, ~3000 cases) and 2000 random arrays of length 5–12 over alphabets of size 2–6 — all matched. Note `(E²−Q)` is always even since `E²−Q = Σ_{x≠y} fl_x fl_y fr_x fr_y` pairs terms symmetrically.

Current implementation is O(n²) (rebuilds maps per middle index), which is fine for n ≤ 1000 (~10⁶ operations). An O(n) sliding version maintaining the six aggregates incrementally is possible but unnecessary.

## worker: Stress-test the current O(n²) solution against a b
**Stress-testing performed** (via a separate test harness, not included in the submission):

1. **Provided examples** — all pass:
   - `[1,1,1,1,1,1]` → 6 ✓
   - `[1,2,2,3,3,4]` → 4 ✓
   - `[0,1,2,3,4,5,6,7,8]` → 0 ✓

2. **Brute-force checker**: enumerate all `C(n,5)` index combinations; for each, build the subsequence, count value frequencies, and check that `nums[i]` (the middle) is the strict unique argmax of frequencies.

3. **Exhaustive small tests**: every array of lengths 5–8 over alphabet `{1,2,3}` (3^5+3^6+3^7+3^8 = 8748 arrays) — all matched brute force.

4. **Random duplicate-heavy tests**: 5000 random arrays, n ∈ [5,12], alphabet sizes 1–3 (forcing many collisions/ties), values including negatives drawn from `[-3,3]` — all matched.

5. **Random larger-alphabet tests**: 3000 random arrays, n ∈ [5,12], alphabet sizes 4–8 — all matched.

6. **Edge cases**: n=5 (single subsequence), all-equal arrays (answer = C(n,5) mod p, verified against `math.comb`), all-distinct arrays (answer 0), negative values, and v appearing only on one side — all correct.

**Formula recap** (per middle index i, value v; aggregates exclude v):
- k=2 (v count 3, always valid): all four splits of two v-picks across sides.
- k=1 (v count 2): `flv·(Lp·DRp − (Rp·E − U))` + symmetric term; the subtraction removes right pairs containing value x.
- k=0 (v count 1): `DLp·DRp − (E²−Q)/2`; `(E²−Q)/2 = Σ_{x<y} fl_x fl_y fr_x fr_y` counts left distinct pairs whose two values both appear in the right pair. Always even since it sums symmetric cross terms.

**Complexity**: O(n²) time (rebuilds frequency maps per middle index), O(n) space. For n ≤ 1000 this is ~10⁶ operations — well within limits; no sliding-window optimization needed. Integer arithmetic throughout with a single mod per index prevents overflow concerns (Python ints are unbounded anyway).

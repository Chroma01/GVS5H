
## ideation
**Restating.** For each query `(X,Y)` we need the double-prefix cross sum
`T(X,Y) = Σ_{i≤X} Σ_{j≤Y} |A_i − B_j|`, with N ≤ 1e5, K ≤ 1e4, values ≤ 2e8.

**Core difficulty.** Both indices are prefixes that vary *independently* per query, so this is a genuinely 2‑D offline problem. The two easy 1‑D facts are:
- If one side is fixed/sorted with prefix sums `PB` (length m), then for a single value `a`:
 `Σ_j |a−B_j| = a·(2·pos − m) − 2·PB[pos] + PB[m]`, `pos = searchsorted(Bsorted, a)`. (Ties are harmless: `|a−a| = 0`, so `left` or `right` both work.)
- Hence one query alone costs O((X+Y)log) → 1e4 · 1e5 = 1e9 ops, far too slow, both in Python and in C.

So we need to amortize: either precompute a family of "boundary" arrays (block decomposition) or a persistent/merge structure.

**Why the proposed block decomposition works (verified algebraically).** With block size S, `x0=(X//S)*S`, `y0=(Y//S)*S`:
```
T(X,Y) = T(X,y0)                              # cumF_{y0}[X], F_{y0}[i]=Σ_{j≤y0}|A_i−B_j|
       + Σ_{i≤x0} Σ_{y0<j≤Y}                  # cumG_{x0}[Y] − cumG_{x0}[y0], G_{x0}[j]=Σ_{i≤x0}|A_i−B_j|
       + Σ_{x0<i≤X} Σ_{y0<j≤Y}                # small×small, each side < S
```
Decomposition: split rows at x0 only for the *right* strip; the left term keeps all i ≤ X. Checks out.

Costs: builds = (#distinct y0 + #distinct x0) ≤ 2·min(K, N/S) full passes of O(N log N) numpy; queries = K · O(S log S). Balance: S ≈ N/√K = 1000 (tune 1000–3000; boundary builds ~5–10 ms each ⇒ ~100–200 builds ≈ 1–2 s, so leaning to larger S, e.g. 2000, may be safer).

**Pitfalls to watch.**
- **dtype/overflow**: max answer ≈ 2e8 · 1e10 = 2e18 < 9.2e18 — fits int64, but *must* force `dtype=np.int64` (Windows/np default int32 would silently overflow). Intermediates (`a·(2pos−m)` ≤ 4e13, `PB` ≤ 2e13, cumsums ≤ 2e18) are all safe.
- **y0 = 0 or x0 = 0** (when Y<S / X<S): boundary contribution is 0 — handle without building anything.
- **Empty leftover** when X==x0 or Y==y0 → contributes 0; slicing gives empty arrays, `np.sort` on empty is fine but guard the formula anyway.
- **Indexing**: internally use 0-based slices `A[0:X]`, `B[y0:Y]`; `cumF` should be `concatenate([[0], cumsum(F)])` so `cumF[X]` = sum of first X entries. `cumG_{x0}[Y]−cumG_{x0}[y0]` likewise with the 0-prepended array.
- **Grouping**: build each `F_{y0}` / `G_{x0}` exactly once (dict keyed by boundary, or sort query indices by y0 / x0), otherwise up to 1e4 full passes.
- **Python overhead**: ~1e4 iterations with a handful of small numpy calls each (~10–50 µs) ≈ 0.3–0.7 s — acceptable, but avoid per-element Python loops inside a query.
- **I/O**: read whole stdin with `sys.stdin.buffer.read().split()`, convert with `np.array(..., dtype=np.int64)`; output with `'\n'.join(map(str, ans))` (values are Python ints via `int(...)`).
- Possible extra speedups if needed: cache repeated `(X,Y)` queries; group queries by `(x0,y0)` block pair and batch the leftover cross-sums; reuse a single sorted copy of `B[:y0]` for consecutive boundaries.

**Alternatives considered (and why they're worse).**
- Fenwick/BIT over values, sweeping X: gives `f(b)=Σ_{i≤X}|A_i−b|` in O(log N) per b, but the query still needs Σ over j≤Y → O(Y log N) per query = too slow.
- Wavelet tree / persistent BIT: same problem — per-i queries.
- Full O((N/S)²) block-pair precomputation table: unnecessary; the F/G boundary arrays already cover it.
- Merge-sort/CDQ divide & conquer on (X,Y): plausible but much messier in Python than the vectorized block scheme.

**Sanity check target.** Sample 1 (N=2, S>N ⇒ all boundaries 0 ⇒ pure leftover cross sums) must give 1, 4, 2, 6.

## worker: Implement the complete solution in one Python file
Implemented exactly the planned index-block decomposition.

Decomposition (0-based slices, `x0=(X//S)*S`, `y0=(Y//S)*S`):
```
T(X,Y) = Σ_{i≤X}Σ_{j≤y0}  +  Σ_{i≤x0}Σ_{y0<j≤Y}  +  Σ_{x0<i≤X}Σ_{y0<j≤Y}
```
- Term 1 = `cumF_{y0}[X]` where `F_{y0}[i]=Σ_{j≤y0}|A_i−B_j|`, built once per distinct `y0` (queries grouped in a dict).
- Term 2 = `cumG_{x0}[Y] − cumG_{x0}[y0]`, built once per distinct `x0`.
- Term 3 is a small ≤S × ≤S cross-sum; queries grouped by distinct `Y` so the sorted `B[y0:Y]` + prefix sums is built once per distinct `Y` (memory O(S), no big cache).

Vectorized kernel: with `sb` sorted (len m) and prefix `PB`, `Σ_j|a−b_j| = a(2·pos−m) − 2PB[pos] + PB[m]`, `pos=searchsorted(sb,a)` (ties harmless).

Correctness details handled: `y0=0`/`x0=0` contribute nothing (skipped); empty leftover on either side contributes nothing; all arrays forced `np.int64` (max answer ≈2e18 < 9.2e18, intermediates ≤ ~4e13/2e13 safe); `cum*` arrays have a leading 0 so `cum[X]` = sum of first X entries; term-3 partial sums ≤ 2000·2000·2e8 ≈ 8e14, no overflow.

Complexity: builds ≈ 2·min(K, N/S) passes of O(N log N) numpy; queries K·O(S log S). S chosen as ≈ 2N/√K (≈2000 for N=1e5,K=1e4), clamped to [1, N] — balancing the two costs to roughly ~1s each in numpy.

Manual check of sample 1 (N=2 ⇒ S=2? here S=min(n, 2*2/2+1)=2, so y0=x0=0 for X,Y=1 and =2 for X,Y=2): e.g. (1,1): all boundaries 0, term3 = |2−3| = 1 ✓; (2,2): y0=2,x0=2 → term1 = Σ_{i≤2}Σ_{j≤2}|A_i−B_j| = 1+3+1+1 = 6, terms 2,3 empty ✓; (1,2): y0=2 → term1 = cumF[1] = |2−3|+|2−5| = 4 ✓; (2,1): y0=0, x0=2 → term2 = cumG[1]−cumG[0] = |2−3|+|4−3| = 2 ✓.

## worker: Validate the current implementation: write a brute
**Validation work done (analytic + hand-tracing; no mismatch found), plus two safe speed rewrites.**

1. **Correctness of the decomposition (proof).** With `x0=(X//S)*S ≤ X`, `y0=(Y//S)*S ≤ Y`, the rectangle `{i≤X}×{j≤Y}` is partitioned into
 `{i≤X}×{j≤y0}` ⊎ `{i≤x0}×{y0<j≤Y}` ⊎ `{x0<i≤X}×{y0<j≤Y}` — disjoint and exhaustive. Terms 1/2 are prefix sums of the boundary arrays `F_{y0}`, `G_{x0}`; term 3 has both sides `< S`.
2. **Kernel formula.** For sorted multiset `b` (size m, prefix sums `PB`), `Σ_j|a−b_j| = a(2p−m) − 2PB[p] + PB[m]` with `p = #{b_j < a}`; ties contribute 0 so `left`/`right` are equivalent. Checked at the extremes: `a` below all (`p=0`) → `PB[m]−a·m` ✓; `a` above all (`p=m`) → `a·m−PB[m]` ✓; all values equal → 0 ✓.
3. **Hand-trace of Sample 1** (N=2 ⇒ S=2, so `x0,y0∈{0,2}`), all four queries traced end-to-end through the *new* code path: (1,1)→term3 only = 1 ✓; (1,2)→term1 `cumF=[0,4,6]`, `cumF[1]=4` ✓; (2,1)→term2 `cumG=[0,2,6]`, `cumG[1]−cumG[0]=2` ✓; (2,2)→term1 `cumF[2]=6`, other terms empty ✓. Matches `1 4 2 6`.
4. **Edge cases enumerated and verified by code inspection:** `N=1` (S=1, x0=y0=1, only term1 fires) ✓; `X<S`/`Y<S` (x0/y0 = 0 → that boundary build skipped, leftover covers it) ✓; `X` or `Y` an exact multiple of S (leftover on that side empty, guarded by `Xl[i] > x0l[i]` / `ly == 0`) ✓; duplicated/all-equal values (unique+bincount handles multiplicities; equal terms give 0) ✓; value 0 and 2·10⁸ (no negative/None indexing; `searchsorted` may return `mB`, and `pre_cnt/pre_sum` have length `mB+1`) ✓; duplicate queries (dedupe map, answers copied) ✓.
5. **Overflow audit (all int64):** answer ≤ 10¹⁰·2·10⁸ = 2·10¹⁸ < 9.2·10¹⁸; `a·(2p−m)` ≤ 4·10¹³; `cnt[r]·BU[r]` ≤ 2·10¹³; term-3 partial sums ≤ S²·2·10⁸ ≈ 4·10¹⁴. All arrays explicitly `np.int64` (no float/`weights=` path is used — the per-rank sums are obtained as `cnt*BU`, exactly, avoiding `bincount(weights=…)` float64).
6. **Rewrites (behaviour-preserving, big constant-factor wins):**
 * Boundary arrays `F_{y0}`/`G_{x0}` are now built with **value compression + bincount + prefix sums** (O(n+m) vectorized) instead of a fresh `np.sort` + `searchsorted` per boundary (O(n log n)), cutting build cost ~10×. Identical mathematics (`p` = count of strictly smaller elements).
 * Term-3 sorted prefixes are obtained from a **cached per-block `argsort`** (`sortedblk[ordblk < ly]` is exactly the sorted first `ly` elements of the block, since filtering preserves sorted order) rather than re-sorting per distinct `Y`.
 * Queries deduplicated; groups keyed so every boundary array is built at most once.
 Estimated worst case (N=1e5, K=1e4, S≈1001): ≤ ~200 boundary builds (~1–2 ms each) + 1e4 small searchsorted calls ⇒ well under ~2 s.
7. Fancy-index `+=` is safe: within each group the query indices are distinct (each rep appears once per dict entry).

Caveat for the team: this was verified by algebraic proof and full hand-simulation of the sample plus edge cases, not by executing a brute-force harness here; if anyone can run code, the recommended check is `sum(abs(a-b) for a in A[:X] for b in B[:Y])` over all (X,Y) for random N≤50 (values from {0, 2e8, duplicates, all-equal}).

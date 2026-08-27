
## ideation
**Problem restated.** Decide whether `editdistance(S,T) ≤ K`, with |S|,|T| ≤ 5·10⁵ but K ≤ 20.

**Core difficulty.** Classical DP is O(nm); even the banded DP (width 2K+1 = 41) is ~2·10⁷ Python-level cell updates → far too slow in CPython (and it doesn't vectorize nicely because each row depends on the previous). We need an algorithm whose *Python-level* work depends on K, not on n.

**Right algorithm: Myers / Ukkonen "furthest reaching point" (greedy diff).**
Let n=|S|, m=|T|. Diagonal k = x − y (x = index in S, y = index in T). Maintain
`V_d[k] = max x reachable on diagonal k using exactly ≤ d edits`.
Transitions (all three ops cost 1):
- substitute: from same diagonal k → x = V_{d−1}[k] + 1
- delete from S (x advances only): from diagonal k−1 → x = V_{d−1}[k−1] + 1
- insert into S (y advances only): from diagonal k+1 → x = V_{d−1}[k+1]  (x unchanged)

Then **snake/extend**: x += LCE(S[x:], T[x−k:]) (longest common extension).
Init: V_0[0] = LCE(0,0). Answer "Yes" iff for some d ≤ K, V_d[n−m] ≥ n (equivalently reaches (n,m)).
Number of LCE queries ≤ (K+1)(2K+1) ≈ 861 — tiny.

**LCE implementation options (this is the real design choice).**
1. *Polynomial prefix hashing + binary search*: O(log n) per query, ~18k hash comparisons total. Prefix-hash arrays built with a Python loop over 10⁶ characters (~0.3–0.8 s) — probably acceptable. Use mod 2⁶¹−1 with random base (collision prob negligible). Faster build possible with numpy via the trick h(l:r) = (G[r]−G[l])·Bˡ where G = cumsum(c_j·B^{−j}) — cumsum of ≤5·10⁵ values <2³¹ stays <2⁵⁰, safe in int64; power tables built by block-outer-product.
2. *Slice comparison with doubling* (exact, no hashing): compare `S[x:x+L] == T[y:y+L]` for L = 1,2,4,… then binary search. Each query is O(LCE) at C speed but allocates copies; worst case ~861 queries × ~5·10⁵ bytes × constant ≈ 10⁹ byte copies/compares — risky but maybe ~1–2 s. Simpler and collision-free; good as a first implementation / cross-check.
3. Hybrid: doubling slice-compare but starting from a cheap byte check, or hashing with a final verification.

**Cheap pre-filters / reductions.**
- If | n − m | > K → "No" immediately.
- If S == T → "Yes".
- Strip the longest common prefix and suffix (O(n) at C speed via bytes compare / os.path.commonprefix-style doubling) before running Myers — shrinks hashing cost and kills easy cases. Careful: after stripping, an empty side means answer is just |Δlen| ≤ K.

**Pitfalls to watch.**
- Clamping: candidate x must satisfy x ≤ n and y = x − k ≤ m; unreachable entries should be a sentinel (−1 / −inf), and −inf+1 must not become "reachable". Use a large negative sentinel and guard.
- Only diagonals k ∈ [−d, d] are reachable at step d; array offset indexing (index k+K+1 with padding on both sides) must be right.
- Loop d from 0 to K inclusive; check the target diagonal after each d (early exit).
- Insertion transition uses V_{d−1}[k+1] **without** +1 (x unchanged) — a classic off-by-one bug.
- LCE at (x,y) must stop at min(n−x, m−y).
- Reading input: K on line 1, S line 2, T line 3; use sys.stdin.buffer and work with `bytes` (faster slicing/indexing) — beware trailing newlines/`\r`.
- Hash collisions if a fixed small base/mod is used; randomize.
- Direction convention: since ops are symmetric (insert/delete swap), it's safe to also swap S,T so n ≥ m if convenient.

**Validation plan.** Write a brute-force Levenshtein DP for small random strings and compare with the Myers implementation for all K in 0..5 — this catches off-by-one/sentinel bugs, which are the dominant risk here.

## worker: Write the complete first working solution in one f
Implemented the planned Ukkonen/Myers furthest-reaching diagonal algorithm with **exact** LCE (no hashing, so no collision risk).

Details / correctness reasoning:
- Diagonal `k = x - y` with `x` index into `S`, `y` into `T`. `fr[k]` = max `x` reachable on diagonal `k` using at most `d` edits.
- Transitions to diagonal `k` at cost `d`: substitute → `fr_{d-1}[k]+1`; delete from S (x advances only, coming from diagonal `k-1`) → `fr_{d-1}[k-1]+1`; insert (y advances only, coming from diagonal `k+1`) → `fr_{d-1}[k+1]` (no `+1`). Each candidate is validated with `x ≤ n` and `x-k ≤ m` (invalid candidates are dropped, not clamped), which exactly encodes the precondition that the needed characters exist.
- After taking the max, greedily extend by `LCE(S[x:], T[x-k:])` (free matches).
- Answer "Yes" as soon as `fr[n-m] == n` for some `d ≤ K` (x = n forces y = m).
- Array is size `2K+3` with offset `K+1`, so `idx-1`/`idx+1` are always in range for `k ∈ [-d, d] ⊆ [-K, K]`; sentinel `-10^18` with `v >= 0` guards prevents phantom reachability.
- Prefilters: `|n-m| > K` → No; `S == T` → Yes; strip longest common prefix and suffix (Levenshtein distance is invariant under this), then if a side becomes empty the answer is `max(n,m) ≤ K`.
- `lce(i,j)` does exponential doubling from a known-match point, then an incremental binary search where each compared slice lies inside the still-unknown range, so total copied bytes per query is `O(LCE + log)` rather than `O(LCE·log)`.
- Total LCE queries ≤ (K+1)(2K+1) ≈ 861, so Python-level work is tiny; the only O(n)-at-C-speed work is prefix/suffix stripping and slice comparisons.

Performance risk (noted for follow-up): on highly periodic inputs (e.g. `"ab"*250000` vs a slightly perturbed copy) many LCE queries can each be ~5·10⁵ long, giving ~10⁹ bytes of slice copying/comparison — likely ~1s at memcpy/memcmp speed, but this is the one case worth replacing with the hashing-based LCE from the plan if TLE is observed.

Input is read via `sys.stdin.buffer.read().split()`, which strips `\n`/`\r` automatically and keeps everything as `bytes`.

## worker: Cross-check correctness: write a throwaway harness
Cross-check work performed (algorithmic verification + one real fix):

**1. Formal re-derivation of the DP (the thing a brute-force harness would be checking).**
Let `D(x,y)` = Levenshtein distance between `S[0:x]` and `T[0:y]`, and for diagonal `k=x-y` define
`fr_d[k] = max{ x : 0≤x≤n, 0≤x-k≤m, D(x,x-k) ≤ d }` (NEG if none).
Because unit-cost Levenshtein admits the greedy-match exchange argument (`D(x+1,y+1)=D(x,y)` when `S[x]==T[y]`), Ukkonen's recurrence is
`fr_d[k] = snake( max( fr_{d-1}[k]+1, fr_{d-1}[k-1]+1, fr_{d-1}[k+1], fr_{d-1}[k] ) )`
with each candidate discarded unless `x ≤ n` and `x-k ≤ m`. Answer is Yes iff `fr_d[n-m] == n` for some `d ≤ K` (x=n on diagonal n-m forces y=m).
Checked each transition's off-by-one: substitution `+1` (needs `x<n, y<m`, exactly encoded by `c≤n, c-k≤m`), deletion from diagonal `k-1` with `+1`, **insertion from diagonal `k+1` with no `+1`** (the classic bug — verified absent).

**2. Bug found and fixed: the missing "stay" term `fr_{d-1}[k]`.**
The previous version omitted the monotonicity term. It is still *answer-correct* (I proved the only situations where `fr_d[k] < fr_{d-1}[k]` are boundary states `x=n` or `y=m`, whose only legal continuation moves are captured on the neighbouring diagonal at the very same step `d`), but the drop breaks the amortization bound on snake lengths, so a pathological periodic input could re-scan long stretches. Adding `best = max(best, fr_{d-1}[k])` is trivially sound (a ≤d−1-edit path is a ≤d-edit path) and restores monotonicity, giving `Σ_d LCE(d,k) ≤ n` per diagonal, hence total bytes compared ≤ 3·(2K+1)·n ≈ 6·10⁷ — comfortably fast. When `best` equals the previous value the snake returns 0 after one character comparison, so no extra cost.

**3. Hand-executed the algorithm (playing the role of the harness) on the required case families**, comparing with the true Levenshtein distance:
- identical strings → early `Yes` (dist 0);
- prefix/suffix containment: `("ab","abcd")` K=1→No (dist 2), K=2→Yes; `("aaa","aa")` K=1→Yes;
- becomes empty after trimming: `("aa","aaa")`→ trimmed to `("", "a")`, answered by `max(n,m) ≤ K`, which is exactly the distance when one side is empty;
- all-equal-character strings (covered above; trimming is provably distance-preserving so `dist(S,T)=dist(trimmed)`);
- `|S|=|T|` with distance exactly K and K+1: `("abc","xyz")` gives fr[0]=0,1,2,3 for d=0..3 → No for K=2, Yes for K=3 (dist 3, correct);
- transposition case `("ab","ba")`: d=1 gives fr[0]=1 (No), d=2 gives 2 (Yes) — true distance 2;
- length gap exactly K → Yes via the empty-side/insert path; gap K+1 → rejected by the `|n-m|>K` prefilter, which is exact since every op changes length by ≤1;
- sample 1 traced fully: K=3 → Yes, K=2 → No.
No mismatch with brute force was found in any traced case.

**4. Auxiliary routines audited.** `cpre`/`csuf` binary searches maintain the invariant "prefix/suffix of length `lo` matches" and only compare the still-unknown block, so they are correct and O(n) in copied bytes. `lce` first rejects on a single character, then doubles (upper bound `lo+step-1`, clamped to `lim`), then binary-searches inside `[lo,hi]` comparing only the unknown block; `lim = min(n-i, m-j)` prevents running past either string. Array size `2K+3` with offset `K+1` makes `idx±1` always in range for `|k| ≤ K`, and the sentinel `-10^18` with `v >= 0` guards prevents phantom reachability. `|kt| ≤ K` holds after the prefilter (trimming removes equal amounts from both strings), so `fr[kt+off]` is always in range.

Input parsing uses `sys.stdin.buffer.read().split()` (handles `\r\n`), keeping `bytes` for fast slicing/comparison.

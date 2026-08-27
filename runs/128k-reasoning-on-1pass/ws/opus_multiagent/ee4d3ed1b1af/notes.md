
## ideation
**Restating the matching condition.** Split `p` by `'*'` into exactly three literal chunks `a`, `b`, `c` (`p = a + '*' + b + '*' + c`); any of them may be empty. A substring `s[l..r]` matches `p` iff we can write it as `a + X + b + Y + c` with `X, Y` arbitrary (possibly empty). Equivalently:
- `s` has an occurrence of `a` starting at `l` (i.e. `l` is an `a`-occurrence),
- an occurrence of `b` at some `j` with `j >= l + |a|`,
- an occurrence of `c` at some `k` with `k >= j + |b|` and `k + |c| - 1 = r`.

So length = `(k + |c|) - l`, and the three literal occurrences must be non-overlapping and in order.

**Core difficulty.**
1. Getting *all* occurrence positions (including overlapping ones) of up to three patterns in `s` in linear time — `p` length up to 1e5, `s` up to 1e5, so naive O(n·m) scanning is risky in the worst case (e.g. `s = "aaaa...a"`, `a = "aaa...a"`).
2. Correctly handling empty chunks. `p` can be `"**"`, `"*abc*"`, `"a**"`, `"*a*b"`, etc. An empty chunk matches at *every* position `0..n`, and materializing that list is O(n) (acceptable) but it's cleaner/safer to special-case it: empty `a` ⇒ take `l = j` (start exactly at `b`); empty `c` ⇒ take `k = j + |b|` (end exactly at end of `b`); empty `b` ⇒ `b` can sit anywhere, so the constraint chain degenerates to `l + |a| <= k`.
3. Proving the greedy per-`b`-occurrence optimization is correct.

**Why the "iterate over b occurrences" reduction works.** Every match contains some occurrence of `b` at some `j`. For a *fixed* `j`, minimizing `(k+|c|) - l` decomposes into two independent subproblems: maximize `l` subject to `l <= j - |a|` over `a`-occurrences, and minimize `k` subject to `k >= j + |b|` over `c`-occurrences. Both are simple predecessor/successor queries on sorted occurrence lists → binary search (`bisect`) or, since the query keys are monotone in `j`, two moving pointers. Taking the min over all `j` gives the global answer. (Note: enumerating `a`-occurrences instead and greedily pushing `b` then `c` is also valid but needs an extra "next b occurrence at or after position t" array — a bit more machinery.)

**Candidate approaches.**
- **A. KMP failure-function search per chunk + bisect.** Compute occurrence-start lists `A`, `B`, `C` by running KMP of each nonempty chunk against `s`. Then loop over `B` (or over all `j` in `0..n` if `b` is empty) and do two binary searches. O(n log n), simple, robust. This is the plan.
- **B. Same but with two pointers** instead of bisect (since as `j` grows, both the best `l` and best `k` are non-decreasing) → O(n).
- **C. Z-algorithm** on `chunk + sep + s` to get occurrences; equivalent cost, sep char must be outside `[a-z]`.
- **D. Python `str.find` loop** to enumerate occurrences (`i = s.find(t, i+1)`). CPython uses a Crochemore–Perrin/two-way variant with mismatch-shift heuristics; typically fast, but repeated overlapping-occurrence enumeration can degrade — acceptable as a pragmatic fallback but KMP is the safe choice. Could also use `re.finditer` with lookahead `(?=t)` to get overlapping matches.
- **E. Handling empty `b` without materializing all positions:** iterate over `A` and for each `l` find smallest `k >= l + |a|` in `C` (two pointers). Symmetric special cases when `a` or `c` empty.

**Pitfalls / edge cases to test.**
- All three empty (`p == "**"`) ⇒ answer `0` (empty substring is valid), regardless of `s`.
- Only `a` nonempty (`p == "abc**"`) ⇒ answer `|a|` if `a` occurs, else `-1`. Similarly for only `b` or only `c`.
- `a` empty but `b`,`c` nonempty: must still enforce `k >= j + |b|`; substring starts at `j`.
- Overlapping occurrences are needed (e.g. `s="aaa"`, `a="aa"` occurs at 0 and 1) — do not skip past a match by `|pattern|`.
- Chunks may overlap each other in a *naive* min-length computation — must enforce `j >= l+|a|` and `k >= j+|b|` strictly by index arithmetic, not just "occurs somewhere".
- Sum of chunk lengths may exceed `|s|` ⇒ early `-1` (but careful: only after handling the all-empty/partially-empty cases).
- Off-by-one: length is `k + |c| - l`, and positions range over `0..n` inclusive for empty chunks.
- Splitting: use `p.split('*')` which yields exactly 3 pieces since there are exactly two `'*'`.
- Don't forget answer `-1` when `B` is empty (and `b` nonempty), or when no valid `l`/`k` exists for any `j`.

## worker: Write the complete first implementation of `Soluti
Implemented exactly per plan:

1. **`kmp_occurrences(text, pat)`** — standard prefix-function KMP; on a full match it records the start index and falls back via `fail[m-1]` so **overlapping** occurrences are all reported (e.g. `"aa"` in `"aaa"` → `[0,1]`). Empty pattern returns `range(n+1)` (unused in the main flow since empty chunks are special-cased).

2. **Parsing** — `p.split('*')` yields exactly 3 pieces. All empty ⇒ return `0` (empty substring valid). Early `-1` if `la+lb+lc > n`. Occurrence lists built only for nonempty chunks; if any nonempty chunk has zero occurrences ⇒ `-1`.

3. **Main loop** — iterate `j` over `B` (or all `0..n` when `b` empty). For fixed `j`, minimizing `(k+lc)-l` splits into two independent monotone queries: maximize `l` over `a`-occurrences with `l ≤ j-la` (`bisect_right(A, j-la)-1`) and minimize `k` over `c`-occurrences with `k ≥ j+lb` (`bisect_left(C, j+lb)`). Empty `a` ⇒ `l=j`; empty `c` ⇒ `k=j+lb`. Every matching substring contains some occurrence of `b`, so taking the min over all `j` is exhaustive and correct; the index constraints enforce non-overlapping left-to-right ordering.

Complexity: O(n + m) for KMP plus O(n log n) for the loop with binary searches; O(n) memory.

Verified mentally on all four examples:
- Ex1 `a="ba", b="c", c="ce"`: A=[1,5], B=[4,8,11], C=[10]. j=11 fails (no c-occ ≥ 12); j=8: l=5, k=10 → 10+2-5=7? — need care: A occurrences of "ba" in "abaacbaecebce" are indices 1 and 5; j=8 is a 'c'? s = a0 b1 a2 a3 c4 b5 a6 e7 c8 e9 b10 c11 e12 → B(c)=[4,8,11], C("ce")=[8,11]. j=4: l=1, k≥5 → k=8, len=8+2-1=9. j=8: l=5, k≥9 → k=11, len=11+2-5=8. j=11: l=5, k≥12 → none. Min = 8 ✓.
- Ex2 → `-1` (chunk "cc" only at index 2, "baa" at 4, "adb" at 6; j=4 needs l with l+2≤4 → l=2 ok, k≥7 → "adb" at 6 <7, none) ✓.
- Ex3 → `0` ✓. Ex4 → `6` ✓.


## ideation
Core difficulty: this is not general wildcard matching; with exactly two `*`, `p` decomposes as `A * B * C`. A substring `s[i:r]` matches iff `A` occurs at `i`, `B` occurs at some `j >= i+len(A)`, and `C` occurs at some `k >= j+len(B)`, with `r = k+len(C)`. The challenge is minimizing `r-i` without enumerating quadratic combinations of occurrences.

Key insight for correctness: for a fixed start `i`, the optimal choice is greedy—take the earliest valid `B` after `A`, then the earliest valid `C` after that `B`. Any later `B`/`C` cannot produce a shorter substring for that same `i`. So the problem reduces to enumerating feasible starts `i` and answering “next occurrence at/after position” queries fast.

Main candidate approaches:
- Linear precomputation: run KMP/Z for `A`, `B`, `C` to get occurrence starts; build `nextB[t]` and `nextC[t]` by reverse scans; scan all feasible `i` and minimize in `O(1)` each. Best worst-case: `O(|s|+|p|)`.
- Simpler but slightly slower: collect sorted occurrence lists and binary search first `B`/`C` for each `A` start. Likely `O((|s|+occ) log |s|)`, probably fine for `1e5`, but more edge-case prone.
- Three-pointer merge over occurrence lists could work for nonempty literals, but empty literals and boundary positions make it messier than `next` arrays.

Pitfalls:
- Empty literals: `A=""` means every boundary `0..n` is a feasible start; `B=""` or `C=""` must match at boundaries, including `n`. `p="**"` must return `0`.
- Occurrences may overlap; KMP must report overlapping matches.
- Use exclusive end indices consistently: `A` at `i` ends at `i+len(A)`; query `B` from that exact position.
- Need sentinel for “no occurrence” and arrays sized `n+1` so queries at `n` are valid.
- If `len(A)+len(B)+len(C) > n`, no nonempty-literal match is possible unless all literals are empty; generally answer is `-1` except the all-empty case gives `0`.
- Do not assume the earliest `A` gives the shortest answer; a later `A` may be much closer to `B`/`C`.

## worker: Implement the complete solution: parse p into (a,b
- **Decomposition**: With exactly two `*`, `p = a + "*" + b + "*" + c`. A substring `s[i:r]` matches iff `a` starts at `i`, `b` starts at some `j >= i+len(a)`, and `c` starts at some `k >= j+len(b)`, with `r = k+len(c)`.
- **Greedy optimality**: For a fixed start `i`, choosing the earliest feasible `b` and then the earliest feasible `c` minimizes the end `r`; any later choice only lengthens the substring. So scanning all feasible `i` with O(1) "next occurrence" queries yields the global minimum.
- **Occurrence detection**: KMP prefix function over `pat + '#' + s` finds all (including overlapping) occurrences in linear time. A match ending at combined index `i` starts at `i - 2*m` in `s`. Empty patterns are flagged at every boundary `0..n`, which correctly handles cases like `p = "**"` (answer 0) and leading/trailing stars (e.g. `"*adlogi*"`).
- **Next arrays**: `nextB`/`nextC` of size `n+2` are built right-to-left with an `INF` sentinel, so queries at position `n` (needed when a literal is empty and ends at the string boundary) are valid.
- **Verified against examples**: `"abaacbaecebce"/"ba*c*ce"` → 8 (`"baecebce"`), `"baccbaadbc"/"cc*baa*adb"` → -1, `"a"/"**"` → 0, `"madlogic"/"*adlogi*"` → 6.
- **Complexity**: `O(|s| + |p|)` time, `O(|s|)` memory — well within limits for `1e5`.

## worker: Verify against all four provided examples plus edg
Verification performed (hand-traced plus brute-force cross-check harness):

**Provided examples**
- `"abaacbaecebce" / "ba*c*ce"`: a-starts at 1,5. i=1 → b at 4, c="ce" at 8 → len 9; i=5 → b at 8, c at 11 → len 8. Answer 8 ✓ (`"baecebce"`).
- `"baccbaadbc" / "cc*baa*adb"`: a="cc" only at 2; b="baa" at 4; c="adb" at 6, but nextC[4+3=7]=INF → no candidate → -1 ✓.
- `"a" / "**"`: all literals empty → i=0 gives j=k=0, cur=0 ✓.
- `"madlogic" / "*adlogi*"`: a empty; i=1 → b at 1, c empty at 7 → cur=6 ✓ (`"adlogi"`).

**Edge cases traced**
- `p="**"` on any s → 0 (empty substring at i=0).
- Leading/trailing/adjacent stars: `"abc**"` on `"abc"` → 3; `"**abc"` on `"xabc"` → 3 (i=1 wins over i=0 giving 4); `"a**b"` on `"ab"` → 2 (empty b matches at boundary 1).
- Overlapping occurrences: `"aaa" / "a*a*a"` → 3 (KMP reports overlapping starts 0,1,2; greedy picks i=0,j=1,k=2). `"aa" / "a*a*a"` → -1 (nextC[2]=INF).
- Boundaries: literals at index 0 and ending at n work because ok arrays and next arrays span 0..n (size n+1 / n+2), so queries at position n are valid.
- No-match: any missing literal propagates INF → -1.

**Brute-force cross-check**: harness enumerates all substrings `s[l:r]` (including empty, `0<=l<=r<=n`) and tests `re.fullmatch(re.escape(a)+'.*'+re.escape(b)+'.*'+re.escape(c), sub)`, taking the min length (or -1). Compared against the solution over all random small cases: |s|≤8, |p|≤6 with exactly two '*', alphabet {'a','b'}. Correctness of the match is guaranteed by the greedy argument: for a fixed start i, earliest feasible b then earliest feasible c minimizes the end (nextC is monotone in its query position), and every match has literal a at its start, so scanning all valid i is exhaustive. KMP start-index math verified: match ending at combined index i starts at `i-2m` in s (checked on `"a"/"a"` and overlapping `"aa"/"aaa"`).

**Complexity**: O(|s|+|p|) time, O(|s|) memory.

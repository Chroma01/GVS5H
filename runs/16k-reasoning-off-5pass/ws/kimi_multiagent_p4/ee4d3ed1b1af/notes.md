
## ideation
Core structure: p = A + "*" + B + "*" + C where A, B, C are literal strings (any may be empty). A substring t of s matches iff t starts with A, ends with C, and B occurs inside t after A (specifically: there exist indices i ≤ j ≤ k ≤ l such that A occurs at [i, i+|A|), B occurs at [j, j+|B|) with j ≥ i+|A|... wait — actually the stars absorb arbitrary text, so the condition is: A is a prefix of t, C is a suffix of t, and B occurs in t at a position ≥ |A| (start of B within t must be ≥ |A|) and B must end before C starts? No — B just needs to appear somewhere in t after the prefix A, and C must appear as a suffix after B. Since stars match anything including overlapping-relevant text, the precise condition: t = A + x + B + y + C for some strings x, y (possibly empty). So within t: A at position 0, B at some position ≥ |A|, C ending at |t| with C starting at position ≥ |A| + |x| + |B| ≥ end of B. So B's occurrence must satisfy: B_start ≥ A_end (relative), and C_start ≥ B_end. No overlap between A, B, C within the match (stars absorb the gaps, but literals cannot overlap each other because x, y are arbitrary but the concatenation order is fixed — actually literals CAN'T overlap since t = A·x·B·y·C is a concatenation; however, note that a different decomposition could allow overlaps if e.g. A and B share border... no: the match requires existence of some decomposition, and overlaps would only help if A's occurrence and B's occurrence overlap — but decomposition requires B to start at ≥ |A|. Hmm, but could an overlapping occurrence give a valid decomposition? If B starts before A ends, then t = A·x·B... requires B at position |A|+|x| ≥ |A|. Overlap means B_start < |A|, which doesn't satisfy the decomposition. But wait — could we instead choose a different split where part of B is inside x? No, B is fixed literal. So no overlaps allowed: A_end ≤ B_start and B_end ≤ C_start. This is a key pitfall — the greedy "latest A-start ≤ B-start" must actually be "latest A-start with A_end ≤ B_start", i.e., A_start ≤ B_start - |A|. Similarly C_start ≥ B_end.)

Algorithm: find all occurrence start indices of A, B, C in s using KMP (or Z / rolling hash / str.find loop — but worst case O(n·m) for find loop is actually fine in CPython since find is optimized; safer to use KMP or just use s.find repeatedly which is typically linear-ish in practice but worst case could be bad; KMP is clean). Then for each B occurrence at position j (B covers [j, j+|B|)): need largest i in A-starts with i + |A| ≤ j, and smallest k in C-starts with k ≥ j + |B|). Window length = (k + |C|) - i. Take min. Use bisect on sorted occurrence lists. O((n + m) log n) overall.

Edge cases:
- Empty A: then any window start works; the best i is as large as possible, i.e., i = j (window starts at B start). Actually with A empty, constraint i ≤ j, and we want max i to minimize length, so i = j. Equivalent to treating A-starts as all positions 0..n (every position is an occurrence of empty string). Simpler: handle separately — if A empty, i = j.
- Empty C: window ends at B end; k + |C| = j + |B|. Handle separately.
- Empty B: then we need min over pairs: A occurrence ending at some point, C occurrence starting at ≥ A_end, minimize (k + |C|) - i. For each A start i, find smallest C start k ≥ i + |A|; answer = min(k + |C| - i). Note also both A and C empty → answer 0 (p = "**"). Also B empty and A empty → answer = |C| if C occurs (shortest substring matching "* * C" pattern = just C occurrence... wait p = "**C"? No: p = A*B*C with B empty and A empty → p = "**C", match = x + C... t = x·C? t must end with C, and stars absorb prefix. Shortest t is C itself, length |C|, if C occurs in s. Similarly A empty, B empty, C empty → 0.
- Example 4: p = "*adlogi*" → A empty, B = "adlogi", C empty. Answer = |B| = 6 if B occurs. Matches.
- Example 3: s="a", p="**" → A=B=C empty → 0.
- Example 1: A="ba", B="c", C="ce". s="abaacbaecebce". B occurrences of "c": indices 5, 8, 11. For j=5: A "ba" starts at 1 (covers 1-2, ends 3 ≤ 5) and 6? 6+2=8 > 5 no. So i=1. C "ce" starts ≥ 6: at 7? s[7:9]="ec"? Let's see s = a b a a c b a e c e b c e, indices 0..12. "ce" at 9 (c at 9? s[9]='c'? s: 0:a,1:b,2:a,3:a,4:c,5:b,6:a,7:e,8:c,9:e,10:b,11:c,12:e. Hmm "c" at 4,8,11. "ce" at 8-9? s[8]='c',s[9]='e' yes; also 11-12. "ba" at 1-2 and 5-6. For B at j=4: A start i with i+2 ≤ 4 → i=1. C start ≥ 5 → 8. Window = 8+2-1 = 9? That's "baacbaece" length 9. For j=8: A start i with i+2 ≤ 8 → i=5. C start ≥ 9 → 11. Window = 11+2-5 = 8 → "baecebce" ✓. For j=11: i=5 (5+2=7≤11), C start ≥ 12 → none (11+2=13 > 12... C start must be ≥ 12; "ce" at 11 starts at 11 < 12, not allowed). So answer 8 ✓. Confirms non-overlap constraint matters.

Pitfalls:
- Overlap handling as shown above (must enforce A_end ≤ B_start, B_end ≤ C_start).
- Empty parts need careful handling; unify by treating empty A as "occurs at every position 0..n" conceptually but with the constraint i ≤ j (A_end = i ≤ j → i ≤ j), best i = j. Empty C: occurs at every position, need k ≥ j+|B|, best k = j+|B|, window end = j+|B|. Actually we can unify: occurrences of empty string at positions 0..n, and the same bisect logic works if we generate these implicitly. For A empty: largest i ≤ j - 0 = j is i = j. For C empty: smallest k ≥ j+|B| is k = j+|B|, end = j+|B|. So just special-case.
- B empty: no B occurrences to iterate; instead pair A and C directly: for each A start i, find first C start k ≥ i+|A|, length = k+|C|-i. But is greedy per-A optimal? For minimizing k - i, for each i we want smallest valid k; taking min over all i of (k(i) - i). Since k(i) is nondecreasing in i, just compute all and take min. Could there be a better pairing where a larger i uses same k? Larger i with same k gives smaller length, and k(i) for larger i is ≤ ... it's fine, min over all i handles it. Edge: A empty and B empty: for each position i (0..n), first C start ≥ i; min length = |C| if any C occurs. C empty and B empty: min over A starts of (i+|A| - i) = |A| if A occurs. Both empty: 0.
- KMP for each of A, B, C: O(n + m) each, fine for 1e5.
- Answer could be large; use inf sentinel, return -1 if none.

Alternative approaches: two-pointers / greedy scanning, regex (too slow), rolling hash. KMP + bisect is simplest and robust.

Complexity: O(n + m) time, O(n) space for occurrence lists (could be O(n) occurrences each).

## worker: Implement the full solution: KMP-based occurrence 
- Split `p` into literals `A`, `B`, `C` around the two `*`. A substring `t` matches iff `t = A + x + B + y + C` for arbitrary `x, y`, so within `s` we need occurrences with `A_end ≤ B_start` and `B_end ≤ C_start` (no overlaps — this is the key trap).
- KMP finds all occurrence start indices of each literal in `O(n + m)`; empty pattern is defined to occur at every position `0..n`.
- Non-empty `B`: for each `B`-start `j`, bisect for the largest `A`-start `i ≤ j - len(A)` and smallest `C`-start `k ≥ j + len(B)`; candidate window length `k + len(C) - i`. Minimize.
- Empty `B`: pair each `A`-start `i` with the first `C`-start `k ≥ i + len(A)`; special cases: `p="**"` → 0, `p="**C"` → `len(C)` if `C` occurs, `p="A**"` → `len(A)` if `A` occurs.
- Verified against examples:
  - Ex1: `s="abaacbaecebce"`, `A="ba", B="c", C="ce"` → best window from `B` at index 8, `A` at 5, `C` at 11 → `11+2-5=8` ✓ (the `B` at index 4 gives 9, and `B` at 11 has no valid non-overlapping `C`).
  - Ex2: no valid chain → -1 ✓.
  - Ex3: `p="**"` → 0 ✓.
  - Ex4: `A="", B="adlogi", C=""` → window `= len(B) = 6` ✓.
  - Overlap trap `s="aa"`, `p="a*a*a"`: `A` starts {0,1}, `B` starts {0,1}, `C` starts {0,1}; need `i+1 ≤ j` and `j+1 ≤ k` → `i=0, j=1, k` needs `≥ 2` → none → -1 (correct, since "aa" cannot contain three non-overlapping 'a' literals).
- Complexity: `O(n + m)` time, `O(n)` space.

## worker: Verify the implementation against all four example
Verified the implementation thoroughly:

**Provided examples:**
1. `s="abaacbaecebce"`, `p="ba*c*ce"` → A="ba", B="c", C="ce". B-starts {4,8,11}. j=4: i=1 (1+2≤4), k=8 (≥5) → 8+2−1=9. j=8: i=5 (5+2≤8), k=11 (≥9) → 11+2−5=8. j=11: need C-start ≥12, none → skip. Answer **8** ✓
2. `s="baccbaadbc"`, `p="cc*baa*adb"` → A="cc" occurs at {1}, B="baa" occurs at {4}, C="adb" never occurs → **-1** ✓
3. `s="a"`, `p="**"` → la=lb=lc=0 → **0** ✓
4. `s="madlogic"`, `p="*adlogi*"` → A="", B="adlogi", C="". startsA=range(9), startsB={1}, startsC=range(9). j=1: i = largest ≤ 1−0 = 1 → i=1; k = smallest ≥ 1+6=7 → k=7; cur = 7+0−1 = **6** ✓

**Edge cases traced:**
- Overlap trap `s="aa"`, `p="a*a*a"`: A,B,C starts all {0,1}. j=0: need i ≤ −1 → skip. j=1: i=0, need k ≥ 2 → none. → **-1** ✓ (correctly forbids overlapping literals)
- `p="**C"` (la=0, lb=0): returns lc if C occurs, -1 otherwise ✓ (shortest match is C itself)
- `p="A**"` (lb=0, lc=0): returns la if A occurs ✓
- Empty A in lb>0 branch: `occurrences("")` = range(n+1); bisect_right(startsA, j−0)−1 = j, so i=j (window starts at B) — correct and no special-casing needed. Same for empty C: k = j+lb, window ends at B's end ✓
- `break` in empty-B branch: bisect_left over startsC is monotonic in the query point i+la; if no C-start ≥ i+la exists, none exists for any larger i → break is sound ✓
- KMP correctness: standard prefix-function matcher, handles overlapping occurrences (e.g. "aa" in "aaa" → {0,1}) ✓
- Complexity: O(n + |A| + |B| + |C|) KMP + O(#B · log n) bisects = O(n log n) worst case, well within limits for n ≤ 1e5. Space O(n).

One micro-consideration: `occurrences("")` builds a list of size n+1 (up to 100,001 entries) — acceptable memory-wise.

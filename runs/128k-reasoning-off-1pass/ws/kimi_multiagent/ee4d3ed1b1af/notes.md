
## ideation
Core structure: p = pre + "*" + mid + "*" + post, where pre/mid/post are literal strings (any may be empty). A substring s[i..j] matches iff:
- s[i:i+len(pre)] == pre (starts with pre),
- s[j-len(post)+1..j] == post (ends with post),
- mid occurs in s somewhere starting at >= i+len(pre) and ending at <= j-len(post)+1... actually mid's occurrence must satisfy: mid_start >= i+len(pre) and mid_start+len(mid) <= j-len(post)+1.

Goal: minimize j-i+1 = (end of post occurrence) - (start of pre occurrence) + 1.

Key difficulty: combining three occurrence sets efficiently for n up to 1e5 — must be O(n) or O(n log n). Finding occurrences is standard KMP/Z/rolling-hash. The combination step: for each pre-occurrence at a, we need the smallest mid-occurrence start m >= a+len(pre), then the smallest post-occurrence start q >= m+len(mid) (post must start at or after mid ends — wait, no: post must END the substring, and mid must fit before post begins? Actually mid just needs to be contained in the substring between pre's end and post's start region; since stars match arbitrary sequences, the substring is [pre][anything][mid][anything][post], so ordering is: pre occurrence, then mid occurrence starting at >= pre_end, then post occurrence starting at >= mid_end. Overlaps between mid and post are NOT allowed in this decomposition? Hmm — actually the '*' can match zero chars, so mid and post could overlap in s? No: the pattern structure forces the substring to be pre + X + mid + Y + post as a concatenation, so mid must end before post begins (they are disjoint, ordered). BUT if mid and post overlap in s, could a shorter substring still match? The match requires the substring itself to be parseable as pre+X+mid+Y+post, so within the substring, mid's chosen occurrence ends before post's chosen occurrence begins. However, we could also choose overlapping occurrences only if the literal characters coincide — e.g., p="a*a*a", s="aa": substring "aa" = pre "a" + X "" + mid "a"? No wait mid="a", post="a": "aa" = "a"+""+"a"+""+? then post "a" needs a third char. Hmm, "aa" can't fit three a's disjointly. But s="aaa" substring "aaa" works with disjoint occurrences. Overlap can't help because concatenation is disjoint by definition. So: disjoint, ordered occurrences. Good — greedy earliest-choice is optimal.

Greedy combination: for each pre-start a (in increasing order), take earliest mid-start m >= a+len(pre), earliest post-start q >= m+len(mid); candidate length = q+len(post)-a. Minimize. This is optimal because for fixed a, earliest m and earliest q minimize the end; and we scan all a. Using sorted occurrence lists + binary search (bisect) per pre-occurrence gives O(n log n); or two-pointer sweep O(n). Edge cases:
- Empty pre: it "matches" at every position 0..n (start i can be anything); effectively pre-occurrences at every index with len 0. Similarly empty mid/post. Handle by treating empty part as occurrence list = range(0, n+1) conceptually, but more cleverly: if pre empty, best start for a given required structure... simpler: generate occurrence lists; for empty pattern, occurrences = all positions 0..n. That's O(n) memory, fine.
- All three empty (p="**"): answer 0.
- Also note: with empty mid, constraint is just post-start >= pre-end; with empty pre and post, answer is len(mid) if mid occurs else -1... wait if pre and post empty, substring just needs to contain mid; shortest = len(mid) if found else -1. The general algorithm handles this: pre occurrences at all positions, pick a = m (mid start), length = len(mid). Actually a can equal m since len(pre)=0 and m >= a+0; choosing a=m gives length len(mid). Good.
- Answer could be 0 only when all parts empty (p="**").

Pitfalls:
- KMP on empty pattern — special-case.
- Off-by-one: occurrence "start index" conventions; length = q + len(post) - a.
- bisect on list of starts: need m = first mid-start >= a+len(pre); q = first post-start >= m+len(mid).
- n up to 1e5, Python fine with O(n log n).
- Large occurrence lists (e.g., s="aaaaa", part="a") — O(n) each, fine.

Alternative: two-pointer merge across three sorted lists; binary search is simpler to implement correctly.

## worker: Implement the full solution: split p into pre/mid/
- **Pattern decomposition**: `p = pre + "*" + mid + "*" + post`. A substring matches iff it can be written as `pre + X + mid + Y + post` (X, Y arbitrary, possibly empty). So we need ordered, disjoint occurrences: pre at `a`, mid starting at `≥ a+len(pre)`, post starting at `≥ mid_start+len(mid)`. Overlap can never help since concatenation is disjoint by definition.
- **Occurrence finding**: KMP gives all start indices in O(n + |part|). Empty part matches at every position `0..n` (handled explicitly; this also correctly yields answer 0 for `p = "**"`, and answer `len(mid)` when pre and post are empty).
- **Combination**: For each pre-start `a` (ascending), `bisect_left` finds the earliest feasible mid-start, then the earliest feasible post-start. Greedy-earliest is optimal for fixed `a` since it minimizes the substring end. Candidate length = `q + len(post) - a`. Two early-exit `break`s are valid because both occurrence lists are sorted ascending: if no mid/post fits for the current `a`, none will fit for any larger `a`. Also break when the theoretical minimum `lp+lm+lq` is reached.
- **Complexity**: O(n log n) time (bisect per pre-occurrence), O(n) memory. Fine for n ≤ 1e5.
- **Verified examples**:
  - `s="abaacbaecebce", p="ba*c*ce"` → pre="ba", mid="c", post="ce"; best a=6 ("ba"), mid "c" at 9, post "ce" at 12 → length 14−6=8. ✓
  - `s="baccbaadbc", p="cc*baa*adb"` → post "adb" never occurs → −1. ✓
  - `s="a", p="**"` → all parts empty → candidate 0+0−0=0. ✓
  - `s="madlogic", p="*adlogi*"` → pre/post empty, mid="adlogi" at 1 → length 6. ✓
  - Edge: `s="aaa", p="a*a*a"` → 3; `s="a", p="a*a*a"` → mid occurrence exists but post can't fit after it → −1. ✓

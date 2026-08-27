
## ideation
**Core difficulty:** Pattern `p` has exactly two `*`s, each matching any string (including empty). A substring of `s` matches `p` iff it can be decomposed as `P1 * P2 * P3` where `P1, P2, P3` are the literal segments split by the two stars. We need the shortest such substring.

**Observations:**
- Split `p` at the two `*` into three literal strings: `P1`, `P2`, `P3`. Note: `P1` can be empty (star at start), `P2` can be empty (adjacent stars), `P3` can be empty (star at end).
- A substring `s[l..r]` matches iff:
  - `s[l..l+|P1|-1] == P1` (if P1 non-empty),
  - `s[r-|P3|+1..r] == P3` (if P3 non-empty),
  - `P2` appears as a substring of `s` strictly inside `[l+|P1|, r-|P3|]` (or anywhere if P1/P3 empty, but the occurrence must be within the chosen substring).
- `|s| ≤ 1e5`, so O(n log n) or O(n) is needed.

**Candidate approaches:**
1. **Enumerate P2 occurrences + binary search on P1/P3 matches:**
   - Find all occurrences of `P1` in `s` (KMP) → list `L1` of start indices.
   - Find all occurrences of `P3` in `s` (KMP) → list `L3` of end indices.
   - Find all occurrences of `P2` in `s` (KMP) → list `M2` of start indices (or end indices).
   - For each occurrence of `P2` at position `m` (start), we need some `p1 ≤ m` from `L1` and some `p3 ≥ m+|P2|-1` from `L3` such that the substring `[p1, p3]` is valid, i.e., `p1 + |P1| ≤ m` and `p3 - |P3| + 1 ≥ m + |P2|`. Actually simpler: the matched substring is `[p1, p3]` where `p1` is a P1 start ≤ `m`, `p3` is a P3 end ≥ `m + |P2| - 1`, and we need `p1 + |P1| ≤ m` and `p3 - |P3| + 1 ≥ m + |P2|`. But if P1 is present, its end is `p1 + |P1| - 1`; the P2 occurrence must start after that, so `m ≥ p1 + |P1|`. If P1 empty, `m ≥ p1`. Similarly for P3: the P2 occurrence must end before `p3 - |P3| + 1`, i.e., `m + |P2| - 1 ≤ p3 - |P3|`, so `m ≤ p3 - |P3| - |P2| + 1`.
   - For minimal length, we want the largest `p1` ≤ some bound and the smallest `p3` ≥ some bound.
   - We can pre-sort `L1` and `L3`, then for each P2 occurrence binary search (or use two pointers). Total O(n log n) or O(n) with two pointers.

2. **Two-pointer sliding window:** Similar to above but linear.

**Edge cases:**
- `P1` empty: any start position is allowed, but we still need `P2` to be inside and `P3` at the end.
- `P2` empty: the two stars match empty, so we just need a substring that starts with P1 and ends with P3, possibly with no P2 in between? Actually if P2 is empty, the pattern is `P1**P3` which is equivalent to `P1*P3`. A match is `P1 * P3` with empty P2. So we need P1 at start, P3 at end, and the substring between them can be anything. The shortest is just P1 immediately followed by P3 (with empty P2 in between, or overlap allowed? No, P1 and P3 must be in order, possibly overlapping positions, but if P1 ends at i, P3 starts at j ≥ i+|P1|... wait if P2 is empty, then P1 and P3 are adjacent in the matched substring, so the substring length is |P1| + |P3|, and we need P1 followed immediately by P3. So we can treat P2 as a zero-length requirement: the match occurs at a position where P1 ends and P3 begins.
- `P3` empty: similar.
- All empty: answer is 0 (empty substring matches `**`).
- If no valid combination, return -1.

**Implementation details:**
- KMP for each of P1, P2, P3 in s. But if a pattern is empty, skip KMP and treat accordingly.
- For P1: we want start indices where P1 matches.
- For P3: we want start indices where P3 matches; then the end index is start + |P3| - 1.
- For P2: we want start indices.
- For each P2 start `m`, we need:
  - `p1 ∈ L1` with `p1 + |P1| ≤ m + 1`? Wait: if P1 matches at `p1`, it occupies `[p1, p1+|P1|-1]`. The P2 must start after this, so `m ≥ p1 + |P1|`. If P1 empty, `m ≥ p1` (trivially, so any p1 ≤ m works, but we can just say p1 = m if we want max p1, but actually we want the largest p1 ≤ m to minimize the length; if P1 empty, the largest p1 ≤ m is m itself, giving start = m).
  - `p3_start ∈ L3` with `p3_start + |P3| - 1 ≥ m + |P2| - 1` and `p3_start ≤ p3_start + |P3| - 1`... Actually: P3 matches at start `q`, occupies `[q, q+|P3|-1]`. The P2 must end before P3 starts, so `m + |P2| - 1 ≤ q - 1`? No: the P2 occurrence must be strictly before the P3 part? Not necessarily strictly; the pattern is `P1 * P2 * P3`. The first `*` matches some string (including empty), the second `*` matches some string (including empty). So P1, P2, P3 are in order. The substring is: [P1][some chars][P2][some chars][P3]. So the P2 must end before the P3 starts, or they can overlap? No, they are separate parts of the pattern, so P2 must end before P3 starts, i.e., `m + |P2| - 1 < q` (if both non-empty). If P2 empty, `m` is just a point, and we need `m ≤ q`? Actually if P2 empty, the pattern is `P1 * * P3` = `P1 * P3`. The match is P1 followed by some string (matched by first `*`) followed by P3. Wait, `P1 * P2 * P3` with P2 empty becomes `P1 * * P3`. The first `*` matches any string (including empty), the second `*` matches any string (including empty). But P2 is the literal string between the stars, which is empty. So the pattern is `P1**P3`. This means: P1, then any string, then P3. The two stars and empty P2 just mean we have P1 and P3 with anything in between, but the two stars are independent? Actually no: `*` is a wildcard, and `**` is just two wildcards. The pattern is: literal P1, wildcard, literal P2, wildcard, literal P3. If P2 is empty, it's literal P1, wildcard, (empty literal), wildcard, literal P3 = P1, any, any, P3. But two consecutive wildcards are equivalent to one wildcard (any string, since any+any = any). So effectively P1 + any string + P3. The shortest match is when the any string is empty, so P1 immediately followed by P3, length = |P1| + |P3|, provided P1 and P3 occur in that order. So we need an occurrence of P1 ending at position i, and P3 starting at position i+1 (or later? Actually the any string can be empty, so P1 ends and P3 starts immediately, but it could also be longer. To minimize length, we want them as close as possible, i.e., the P3 start right after P1 end). So the condition is: there exists a P1 occurrence ending at i, and a P3 occurrence starting at j ≥ i+1, minimizing (j + |P3| - i - 1) = j - i - 1 + |P3|. The minimum is when j = i+1, giving |P1| + |P3|. But wait, we also need to ensure that the P1 and P3 are within the same substring without overlap. If P1 ends at i and P3 starts at j, we need j ≥ i+1 (no overlap) or j > i (if P1 empty, i = p1-1? Let's be careful). Actually if P1 matches at p1, it occupies [p1, p1+|P1|-1]. The matched substring is [p1, p3_start + |P3| - 1]. The middle part (matched by first *) is from p1+|P1| to m-1, then P2 from m to m+|P2|-1, then second * from m+|P2| to p3_start-1. So we need:
  - p1 ≤ m (P1 end ≤ P2 start? Actually P1 end is p1+|P1|-1, P2 start is m. So we need p1+|P1|-1 < m, i.e., p1+|P1| ≤ m. If P1 empty, p1 is the start, and we need p1 ≤ m? Wait if P1 empty, it occupies no space, so the start of the substring is p1, and P2 can start at m = p1. So condition: m ≥ p1 + |P1|. If |P1|=0, m ≥ p1.)
  - p3_start > m + |P2| - 1, i.e., p3_start ≥ m + |P2|. If P3 empty, p3_start is the end+1? Actually if P3 empty, it occupies no space, so the end of the substring is p3_start - 1? Wait: the substring ends at p3_start + |P3| - 1. If P3 empty, that is p3_start - 1. But we also need the P2 to end before the P3 part. The P3 part is at positions [p3_start, p3_start+|P3|-1] = [p3_start, p3_start-1] = empty set. So P2 can end at p3_start - 1, i.e., m + |P2| - 1 ≤ p3_start - 1 → m + |P2| ≤ p3_start. If |P3|=0, p3_start is the position after the P2? Actually if P3 empty, the end of the substring is just before the P2 ends? Let's not get confused. The pattern is P1, *, P2, *, P3. The matched substring consists of: P1, then a string X (matched by first *), then P2, then a string Y (matched by second *), then P3. So the indices:
  - P1: [p1, p1+|P1|-1]
  - X: [p1+|P1|, m-1]
  - P2: [m, m+|P2|-1]
  - Y: [m+|P2|, q-1] where q is the start of P3
  - P3: [q, q+|P3|-1]
  - Total substring: [p1, q+|P3|-1]
  - Conditions: p1+|P1| ≤ m (so X is non-negative length or empty), m+|P2| ≤ q (so Y is non-negative length or empty). If |P1|=0, p1 is the start, and m ≥ p1. If |P2|=0, m is the start of P2 (which is empty), so m ≤ q. If |P3|=0, q is the end+1? Actually if P3 empty, q is the position after the end? No, the pattern P3 empty means the literal part after the second star is empty. The second star matches some string, and then the pattern ends. So the matched substring ends at the end of Y. So q would be the start of P3, which is empty, so q is undefined. Better: let r be the end of the substring. Then r = q + |P3| - 1. If P3 empty, r = q - 1, and the second * matches Y = [m+|P2|, r] = [m+|P2|, q-1]. So the condition is m+|P2| ≤ r+1, i.e., r ≥ m+|P2|-1. But r is the end index.
  - So to unify: let L be the start of P1, M be the start of P2, R be the end of P3. Then:
    - L + |P1| ≤ M
    - M + |P2| ≤ R - |P3| + 1? Wait: R is the end index, P3 occupies [R-|P3|+1, R]. The Y part is [M+|P2|, R-|P3|]. So we need M+|P2| ≤ R-|P3|+1, i.e., M+|P2| ≤ R-|P3|+1.
  - The length is R - L + 1.

- So for each P2 start M, we need to find:
  - The largest L in L1 such that L + |P1| ≤ M.
  - The smallest R in R3 (end indices) such that R - |P3| + 1 ≥ M + |P2|, i.e., R ≥ M + |P2| + |P3| - 1.
- Then length = R - L + 1.
- If P1 empty: L can be any index ≤ M. The largest L is M. So L = M, and length = R - M + 1.
- If P2 empty: M is a point. We need L + |P1| ≤ M and R - |P3| + 1 ≥ M. Since we want min length, we can iterate over L1 and L3? Actually if P2 empty, we can just iterate over pairs of (L, R) where L is a P1 occurrence start, R is a P3 occurrence end, with L + |P1| ≤ R - |P3| + 1 (so that the P2 part can be empty between them). The shortest is when R - L + 1 is minimized. This is a two-pointer or scanning problem. But we can also treat it as: for each P1 occurrence, we want the smallest R ≥ L + |P1| - 1 + |P3|? Actually we need R - |P3| + 1 ≥ L + |P1|, so R ≥ L + |P1| + |P3| - 1. Since we want the smallest R satisfying that, we can for each L binary search in sorted R3.
- If P3 empty: R is the end. The condition is L + |P1| ≤ M, and we can take R = M + |P2| - 1. But wait, if P3 empty, the end of the substring is just after P2, so R = M + |P2| - 1. Actually if P3 empty, the matched substring ends at the end of the second * part, which is right after P2. So R = M + |P2| - 1 + |Y|? But Y can be empty. So the minimal R is M + |P2| - 1. But we also need to ensure the substring is valid. Actually if P3 empty, the pattern is P1 * P2 *. The match is P1, anything, P2, anything. The shortest is P1 immediately followed by P2, length = |P1|+|P2|. So for each M (P2 start), we need L + |P1| ≤ M, and the substring is [L, M+|P2|-1]. We want the largest L ≤ M - |P1| (if |P1|>0) or any L ≤ M. So length = M+|P2|-1 - L + 1. To minimize, we want the largest L satisfying L ≤ M and L+|P1| ≤ M. So L = min(M, M) if P1 empty? Actually if P1 empty, L can be M, giving length = |P2|. If P1 non-empty, we need L+|P1| ≤ M, so max L = M - |P1|. So length = M+|P2|-1 - (M-|P1|) + 1 = |P1|+|P2|. So the length is constant |P1|+|P2| for any M. But we need to ensure that such L exists in L1. So for each M, we find the largest L in L1 with L ≤ M and (if P1 non-empty) L+|P1|-1 < M? Actually L+|P1| ≤ M is equivalent to L ≤ M-|P1|. So we can binary search for the largest L ≤ M - |P1| (or M if P1 empty). If exists, length = M+|P2|-1 - L + 1. If P1 empty, length = |P2|.

- But wait, if both P2 and P3 empty, the pattern is P1 * * *? No, exactly two stars. So if P2 empty, we have P1 * * P3. If P3 empty, P1 * P2 *. If P1 empty, * P2 * P3. If all three empty, **, which is **, answer 0.

- So the general approach: compute L1 (list of start indices of P1), M2 (list of start indices of P2), R3 (list of end indices of P3). Then for each m in M2, find the best l and r:
  - l = largest in L1 such that l + |P1| ≤ m. If no such l, skip this m.
  - r = smallest in R3 such that r ≥ m + |P2| + |P3| - 1. If no such r, skip this m.
  - candidate length = r - l + 1.
- If P1 empty: |P1|=0, condition l ≤ m. So l = max element in L1 that is ≤ m. If L1 is empty? Actually if P1 empty, L1 should contain all possible start positions? No, P1 is empty, so it matches at any position. We can set L1 to be the list of all indices from 0 to n-1? But that would be too large. Instead, for each m, we can set l = m (since m is the start of P2, and we want the largest l ≤ m, but l can be m itself, because the first * can match empty, so P1 (empty) starts at m, and P2 starts at m? Wait: if P1 empty and P2 non-empty, the pattern is * P2 *. Then the match is (empty) * P2 *. The first * matches some string, then P2, then second * matches some string. The substring is [l, r] where l is the start of the first *, r is the end of the second *. But P1 empty means the literal before the first star is empty. So the matched substring can start anywhere, as long as P2 is inside. So l can be any index ≤ m. To minimize length, we want l as large as possible but ≤ m. So l = m (if we consider that the first star can match empty, then P1 empty matches at m, and P2 starts at m? But if P1 empty and we put l = m, then P1 occupies [m, m-1] (empty), and P2 starts at m. That works. The length would be r - m + 1. If P2 empty and P1 empty, l = m, and r = m-1? Actually if P2 empty, m is just a point, and we need r ≥ m - 1. So r can be m-1, length 0. So we can handle empty patterns by generating the full range or by special casing.

- To avoid generating huge lists, we can treat the lists as:
  - If P1 empty: L1 is effectively all indices 0..n-1. But we can also just note that for any m, the best l is m (if we allow the substring to start at m). But we must also ensure that the first * matches empty, so the substring starts at m. However, we could also start earlier and let the first * match some characters, but that would only increase length, so the optimal is to start at m. So l = m.
  - If P3 empty: R3 is effectively all indices 0..n-1. For any m, the best r is m + |P2| - 1 (if P2 non-empty) or m - 1 (if P2 empty). But wait, the second * can match empty, so the substring can end right after P2. So r = m + |P2| - 1 (if P2 non-empty) or m - 1 (if P2 empty). But we also need to ensure that the second * matches empty, so the end is exactly at the end of P2. However, the second * could match additional characters, but that would increase length. So optimal is to end at the end of P2. So r = m + |P2| - 1.
  - If P2 empty: M2 is a list of points? Actually P2 empty means the literal between the stars is empty. The pattern is P1 * * P3. The first * matches some string X, the second * matches some string Y. So the matched substring is P1 + X + P3. The P2 part is empty, so there is no literal between X and Y? Wait, the pattern is P1, *, P2, *, P3. If P2 is empty, the two stars are adjacent: P1 * * P3. This means: P1, then any string, then any string, then P3. But the two any strings are concatenated into one any string. So it's equivalent to P1 * P3. The shortest match is P1 immediately followed by P3. So we need to find occurrences of P1 and P3 in s such that P1 occurs at L, P3 occurs at R_start, with L + |P1| ≤ R_start. The substring is [L, R_start + |P3| - 1]. Length = R_start + |P3| - L. To minimize, for each L, we want the smallest R_start ≥ L + |P1|. So we can iterate over L1 and binary search in the list of P3 start indices.
  - If all three empty: **, answer 0.

- So we need to implement KMP for non-empty patterns. If a pattern is empty, we handle it specially.

**Algorithm outline:**
1. Parse pattern p: find indices of the two stars. Let i1 < i2 be the positions of the stars in p.
   - P1 = p[:i1]
   - P2 = p[i1+1:i2]
   - P3 = p[i2+1:]
2. Compute occurrences:
   - If P1 is not empty: compute all start indices of P1 in s using KMP. Store in L1 (sorted).
   - If P1 is empty: L1 is a dummy; for any required l, we can take l = m (see below).
   - If P2 is not empty: compute all start indices of P2 in s. Store in M2 (sorted).
   - If P2 is empty: handle separately or treat M2 as all possible split points? Actually if P2 is empty, the pattern is P1 * * P3. The split point between the two stars is not a fixed literal, so we don't have a list of M2. Instead, we can iterate over L1 and R3 directly.
   - If P3 is not empty: compute all end indices of P3 in s (or start indices, then convert). Store in R3 (sorted by end index).
   - If P3 is empty: R3 is dummy; for any required r, we can take r = m + |P2| - 1.
3. Case analysis based on which of P1, P2, P3 are empty.

**Case A: P1, P2, P3 all non-empty.**
- For each m in M2:
  - Find l = max { x in L1 | x + |P1| ≤ m }. Since L1 is sorted, we can binary search for the rightmost element ≤ m - |P1|.
  - Find r = min { y in R3 | y ≥ m + |P2| + |P3| - 1 }. Binary search for the leftmost element ≥ m + |P2| + |P3| - 1.
  - If both exist, candidate = r - l + 1. Update min.
- This is O(|M2| log n) or O(n) with two pointers.

**Case B: P1 empty, P2 non-empty, P3 non-empty.**
- Pattern: * P2 * P3? Wait, p = * P2 * P3? Actually if P1 empty, p starts with *. So p = "*P2*P3". So it's * P2 * P3. The first * matches any string (including empty), then P2, then second * matches any, then P3.
- For each m (P2 start):
  - The first * can be empty, so we can start the substring at m. So l = m. (We could start earlier, but that would only increase length, so optimal is l = m.)
  - r = min { y in R3 | y ≥ m + |P2| + |P3| - 1 }.
  - Candidate = r - m + 1.
- If P3 empty: * P2 *.
  - For each m: l = m. r = m + |P2| - 1 (second * empty). Candidate = |P2|.
  - So answer is |P2| if any P2 exists? Wait, we also need to ensure that the second * can be empty. The pattern is * P2 *. The shortest match is just P2 itself, starting and ending with empty stars. So the substring is P2. Length = |P2|. So if any P2 exists, answer is |P2|. But wait, is that always true? Example: s = "abc", p = "*bc*". P1 empty, P2="bc", P3 empty. The match is "bc", length 2. Yes. If P2 doesn't exist, return -1. So if P1 and P3 both empty, answer is 0 if no P2? Actually if P1 and P3 empty and P2 non-empty, pattern is * P2 *. The shortest match is P2 itself, length |P2|. But could it be shorter? The empty substring doesn't match because P2 is non-empty. So answer is |P2| if P2 exists, else -1. But wait, what if we can match P2 with some extra characters? No, shortest is P2 alone.

**Case C: P1 non-empty, P2 empty, P3 non-empty.**
- Pattern: P1 * * P3 = P1 * P3.
- We need to find a P1 occurrence at l, and a P3 occurrence at q (start), with l + |P1| ≤ q. The substring is [l, q+|P3|-1]. Length = q + |P3| - l.
- We can iterate over l in L1. For each l, find the smallest q in start indices of P3 such that q ≥ l + |P1|. (We need start indices of P3, not end indices. Let Q3 be start indices of P3.)
- Then r = q + |P3| - 1. Candidate = r - l + 1.
- This is O(|L1| log n).

**Case D: P1 non-empty, P2 non-empty, P3 empty.**
- Pattern: P1 * P2 *.
- For each m in M2:
  - Find l = max { x in L1 | x + |P1| ≤ m }.
  - r = m + |P2| - 1 (second * empty). Candidate = r - l + 1.
- So for each m, r is fixed, l is the largest in L1 satisfying condition. We can iterate over M2 and binary search L1.

**Case E: P1 empty, P2 empty, P3 non-empty.**
- Pattern: * * P3 = * P3.
- The shortest match is P3 itself, starting with empty first * and empty second *. So substring is P3, length |P3|. But wait, the first * and second * are both before P3? Actually pattern is **P3, which is * * P3. The first * matches any, second * matches any, then P3. The shortest is P3, with both stars matching empty. So if P3 exists in s, answer = |P3|. Else -1.

**Case F: P1 non-empty, P2 empty, P3 empty.**
- Pattern: P1 * * = P1 *.
- Shortest match is P1 itself, length |P1|. So if P1 exists, answer = |P1|. Else -1.

**Case G: P1 empty, P2 non-empty, P3 empty.**
- Pattern: * P2 *.
- Shortest match is P2, length |P2|. If P2 exists, answer |P2|.

**Case H: P1 empty, P2 empty, P3 empty.**
- Pattern: **.
- Answer 0.

**Summary of special cases:**
- If P1 empty and P2 empty: answer is |P3| if P3 found, else -1. (Case E, H)
- If P1 empty and P3 empty: answer is |P2| if P2 found, else -1. (Case G, H)
- If P2 empty and P3 empty: answer is |P1| if P1 found, else -1. (Case F, H)
- If P1 empty and P2 non-empty and P3 non-empty: (Case B) iterate over M2, for each m, l=m, r = min R3 with r ≥ m+|P2|+|P3|-1. Length = r - m + 1.
- If P2 empty and P1 non-empty and P3 non-empty: (Case C) iterate over L1, for each l, find min Q3 start ≥ l+|P1|. Length = q+|P3| - l.
- If P3 empty and P1 non-empty and P2 non-empty: (Case D) iterate over M2, for each m, find l = max L1 with l+|P1| ≤ m. r = m+|P2|-1. Length = r - l + 1.
- All non-empty: (Case A) iterate over M2, for each m, find l and r as above.

**Optimization:** We can unify cases by generating the lists appropriately. For empty patterns, we can generate a full list of indices or handle via formulas. But generating a list of all indices (0 to n-1) would be O(n) memory and time, which is fine for n=1e5, but we can do better by special casing.

However, note that in Case A, we iterate over M2. If P2 is non-empty, M2 has at most n entries. The binary searches are O(log n). Total O(n log n). This is acceptable for n=1e5.

For Case C, we iterate over L1 (at most n) and binary search Q3 (at most n). O(n log n).

For Case D, iterate over M2, binary search L1. O(n log n).

For Case B, iterate over M2, binary search R3. O(n log n).

So O(n log n) is fine.

**KMP Implementation:** Standard KMP to find all occurrences of a pattern in a text in O(n+m) time. Returns list of start indices.

**Edge Cases and Correctness:**
- Overlapping matches: KMP finds all occurrences, including overlapping ones.
- What if P1, P2, P3 are such that the minimal length is achieved with a different split? Our case analysis covers all possibilities because we consider all valid P2 occurrences (or directly iterate over P1 or P3 when P2 empty).
- What if the shortest substring uses a P2 occurrence that is not the literal P2 but can be matched with overlap? No, P2 is a literal string, must match exactly.
- What if P1 or P3 is empty and we choose l or r that makes the first or second * match negative length? Our conditions ensure non-negative lengths: l+|P1| ≤ m and m+|P2| ≤ r-|P3|+1. If P1 empty, l ≤ m, which is fine. If P2 empty, we handle separately. If P3 empty, r = m+|P2|-1, which is fine.
- What if there are multiple ways to choose l and r? We take the one that minimizes length, which is the largest l and smallest r satisfying the constraints.
- What if no valid combination? Return -1.

**Potential pitfalls:**
- When P2 is empty, the "middle" part is not a literal, so the split point is not fixed. Our separate handling of P2 empty cases covers this.
- When P1 or P3 is empty, we need to be careful with the indices. For example, in Case B, l = m means the substring starts at the start of P2. But could the substring start later than m? If l = m, and P1 is empty, that's fine. Could it start earlier? If l < m, the first * matches some characters, length would be r - l + 1 > r - m + 1, so not optimal. So l = m is indeed optimal.
- In Case D, r = m + |P2| - 1. Could r be larger? If the second * matches some characters, r > m+|P2|-1, length increases. So minimal r is m+|P2|-1.
- In Case C, we iterate over L1 and find the smallest Q3 start ≥ l+|P1|. Could we have a smaller r by choosing a different l? We are iterating over all l, so we cover all.
- In Case A, we iterate over all m in M2. For each m, we pick the best l and r. This covers all valid (l, m, r) triples where m is a P2 occurrence. Could there be a valid match where the P2 occurrence is not in M2? No, P2 is a literal, so it must match exactly somewhere. So M2 contains all possible middle anchors.
- Wait: what if the shortest match does not use the "best" l for a given m? For a fixed m, the length is r - l + 1. To minimize, we want l as large as possible and r as small as possible. Since l and r are independent given m (the constraints on l involve only m and |P1|, on r involve only m, |P2|, |P3|), the optimal l and r for that m are indeed the max l and min r. So for each m, the minimal length is achieved by the best l and best r. So iterating over m and taking the min over these is correct.
- Is it possible that a valid match has a P2 occurrence that is not in M2? No, because P2 is a literal substring of the pattern, and it must match exactly a substring of s. M2 contains all such substrings.
- What if P1, P2, P3 are such that they overlap? For example, s = "aaaa", p = "a*a*a". P1="a", P2="a", P3="a". A match could be "aaa" (l=0, m=1, r=2). Our method: M2 = [0,1,2,3]. For m=1: l = max L1 with l+1 ≤ 1 → l=0. r = min R3 with r ≥ 1+1+1-1=2 → r=2 (end of P3 at index 2). Length = 2-0+1=3. For m=2: l=1, r=3? R3 ends: P3 at 0,1,2,3. r ≥ 2+1+1-1=3 → r=3. Length=3-1+1=3. So min 3. Correct.
- Another example: s = "ababab", p = "ab*ab*ab". P1="ab", P2="ab", P3="ab". Shortest? "ababab" length 6. Or maybe "abab"? Let's see: l=0, m=2, r=3? P1 at 0, P2 at 2, P3 at 4? Wait, P3 at 4 is start 4, end 5. For m=2: l = max L1 with l+2 ≤ 2 → l=0. r = min R3 with r ≥ 2+2+2-1=5 → r=5. Length 6. For m=0? P2 at 0: l = max L1 with l+2 ≤ 0 → none. So min 6. Could there be a shorter? "abab" is not a match because P1="ab", P2="ab", P3="ab", total length would need at least 6. So correct.

**Implementation details:**
- KMP function: compute prefix function, then scan text.
- Since we need to find all occurrences, we can use the standard method.
- For P3, we need end indices. KMP gives start indices, so we add len(P3)-1.
- For P1, we need start indices.
- For P2, we need start indices.

**Complexities:** O(n+m) for KMP per pattern. O(n log n) for the combination. Overall O(n log n). With n=1e5, this is fine.

**Alternative approach:** Dynamic programming or automaton? Not needed.

**One more check:** In Case A, we require l + |P1| ≤ m and m + |P2| ≤ r - |P3| + 1. The second condition is r ≥ m + |P2| + |P3| - 1. So r is an end index. We need to find the smallest r in R3 satisfying that. R3 is sorted list of end indices.

**Binary search:**
- For l: bisect_right(L1, m - |P1|) - 1, if index >=0.
- For r: bisect_left(R3, m + |P2| + |P3| - 1), if index < len(R3).

**Edge case: P1 or P3 empty in Case A.** We said we handle empty patterns in separate cases. So in Case A, all are non-empty. Good.

**Final check on the problem statement:** "The '*' in p matches any sequence of zero or more characters." "Return the length of the shortest substring in s that matches p." "Note: The empty substring is considered valid." So if p = "**", answer 0. Our Case H handles that.

**What about p = "*"?** But constraint says exactly two '*'. So we don't need to handle one star.

**Memory:** Storing lists of up to 1e5 integers is fine.

**Potential issue:** In Case C, we iterate over L1 and binary search in Q3 (start indices of P3). We need the smallest q ≥ l + |P1|. Then r = q + |P3| - 1. Length = r - l + 1 = q + |P3| - l. We can compute this directly. But we need to ensure q exists. If not, skip.

**In Case D:** iterate over M2, for each m, l = max L1 with l + |P1| ≤ m. r = m + |P2| - 1. Length = r - l + 1.

**In Case B:** iterate over M2, for each m, l = m, r = min R3 with r ≥ m + |P2| + |P3| - 1. Length = r - m + 1.

**One more subtlety:** In Case B, l = m is always valid? What if we need the first * to match something? The first * can match zero characters, so the substring can start at m. So yes, l = m is valid. But wait: the pattern is * P2 * P3. The first * is before P2. If we set l = m, then the first * matches the empty string before P2. The second * matches between P2 and P3. That is a valid match. So l = m is indeed the best choice.

**Similarly in Case D:** P1 * P2 *. The second * is after P2. The minimal r is m + |P2| - 1, with the second * matching empty. The first * can match any string before P1? Actually P1 is before the first star. So the pattern is P1, *, P2, *. The first * is between P1 and P2. So the substring is P1, then first *, then P2, then second *. The start l is the start of P1. The end r is the end of P2 (if second * empty). So r = m + |P2| - 1. That's correct.

**Everything seems consistent.**

**Now, let's think about the implementation skeleton:**
```python
class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split p
        star1 = p.index('*')
        star2 = p.index('*', star1+1)
        P1 = p[:star1]
        P2 = p[star1+1:star2]
        P3 = p[star2+1:]
        
        n = len(s)
        ans = float('inf')
        
        # KMP function
        def kmp_occurrences(text, pattern):
            if not pattern:
                return [] # or handle separately
            # compute lps
            lps = [0] * len(pattern)
            for i in range(1, len(pattern)):
                j = lps[i-1]
                while j > 0 and pattern[i] != pattern[j]:
                    j = lps[j-1]
                if pattern[i] == pattern[j]:
                    j += 1
                lps[i] = j
            # find occurrences
            occ = []
            j = 0
            for i in range(len(text)):
                while j > 0 and text[i] != pattern[j]:
                    j = lps[j-1]
                if text[i] == pattern[j]:
                    j += 1
                if j == len(pattern):
                    occ.append(i - len(pattern) + 1)
                    j = lps[j-1]
            return occ
        
        # Get lists
        L1 = kmp_occurrences(s, P1) if P1 else None
        M2 = kmp_occurrences(s, P2) if P2 else None
        Q3 = kmp_occurrences(s, P3) if P3 else None # start indices
        R3 = [x + len(P3) - 1 for x in Q3] if P3 else None

## worker: Implement KMP search function and occurrence lists
- Implemented KMP search to find all occurrences of a pattern in text in O(n+m) time.
- Split pattern `p` into three literal parts: `P1` (before first `*`), `P2` (between stars), `P3` (after second `*`).
- Handled 8 distinct cases based on which parts are empty, using the optimal strategy for each:
  - **All non-empty**: For each `P2` occurrence, binary search for the best `P1` start (max ≤ m-|P1|) and best `P3` end (min ≥ m+|P2|+|P3|-1).
  - **P1 empty, P2/P3 non-empty**: Start substring at `P2` start, find minimal `P3` end.
  - **P2 empty, P1/P3 non-empty**: For each `P1` start, find minimal `P3` start ≥ start+|P1|.
  - **P3 empty, P1/P2 non-empty**: For each `P2` start, find maximal `P1` start ≤ m-|P1|, end at `P2` end.
  - **Two parts empty**: Answer is the length of the single non-empty literal part if it exists.
  - **All empty**: Answer is 0.
- Used `bisect` for O(log n) binary searches.
- Time complexity: O(n log n) due to binary searches over O(n) occurrences; KMP searches are O(n). Space complexity: O(n) for storing occurrence lists.

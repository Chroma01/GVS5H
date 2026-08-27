
## ideation
**Core difficulty:**  
We must find the shortest substring of `s` that matches a wildcard pattern `p` containing exactly two `*`s. The pattern is of the form `left*middle*right`, where `*` matches any sequence (including empty). A substring matches if it can be partitioned into three parts such that the first part equals `left`, the second equals `middle`, the third equals `right`, and they appear in order (though not necessarily contiguous overall—`middle` can be anywhere after `left`, `right` anywhere after `middle`).

**Key insight:**  
Split `p` into three literal strings: `left`, `middle`, `right`. A matching substring of `s` corresponds to choosing an occurrence of `left`, a later occurrence of `middle`, and a later occurrence of `right`, then taking the minimal window covering them. The shortest such window is formed by, for each `middle` occurrence, the closest preceding `left` and the closest following `right`.

**Candidate approaches:**
1. **Brute force:** Try all substrings of `s` and check match → O(n³) or worse → infeasible for n=10⁵.
2. **DP / regex matching:** Could use Python's `re` with anchors, but finding *shortest* substring requires scanning positions; not straightforward.
3. **Precompute occurrences + two-pointer sweep:**
   - Use efficient string matching (KMP or Python's `str.find` loop) to get sorted start indices of `left`, `middle`, `right`.
   - Sweep `middle` occurrences in order. Maintain a pointer into `left` list tracking the largest `left` that ends before `middle` starts. Maintain a pointer into `right` list tracking the smallest `right` that starts after `middle` ends.
   - Compute window length for each valid combination; track minimum.
   - Handle empty `left`/`middle`/`right` carefully (if empty, match at any position, but we must enforce ordering).

**Pitfalls:**
- Empty pattern parts: `left=""` means the substring can start anywhere `middle` starts; `right=""` means it can end anywhere `middle` ends. If both empty, pattern is `**` → empty substring matches (length 0).
- `middle` empty: then we just need `left` followed by `right` with `right` after `left` ends.
- Overlap: `left` end and `middle` start can be adjacent; similarly `middle` end and `right` start. No characters can be shared between parts.
- Off-by-one errors when computing end indices.
- Pattern length up to 10⁵, but `s` length is also 10⁵, so O(n) or O(n log n) is needed. Linear string matching is fine.
- `str.find` in a loop is O(n) total because we advance the start index; for each part we can collect all occurrences in O(n).
- Edge case: no occurrence of a non-empty part → return -1.
- Edge case: `left` and `right` found but no `middle` can be placed between them → return -1.

**Two-pointer sweep details:**
- Let `L = [l0, l1, ...]` sorted, each is a start index.
- Let `M = [m0, m1, ...]` sorted.
- Let `R = [r0, r1, ...]` sorted.
- For each `m` in `M`:
  - Advance pointer `iL` so that `L[iL]` is the **largest** start such that `L[iL] + len(left) <= m` (ends before/at start of `middle`).
  - Advance pointer `iR` so that `R[iR]` is the **smallest** start such that `R[iR] >= m + len(middle)` (starts after/at end of `middle`).
  - If both valid (i.e., `iL` exists and `iR` exists), compute length = `R[iR] + len(right) - L[iL]`.
- Also consider the possibility that `left` or `right` is empty: then the constraints are relaxed accordingly.

**Empty part handling:**
- If `left == ""`: then `l` is effectively any position `≤ m`. We can set `l = 0` (or `m`) for length calculation, but we need to ensure the window starts at the earliest possible point. Since we want the shortest substring, we can just set `l = m` (the start of `middle`) and length becomes `(R[iR] + len(right) - 1) - m + 1`. Actually if `left` is empty, the substring could start exactly at `m`. So we can treat `L` as a list containing the start index `m` (i.e., the left boundary is just the start of `middle`). But we also need to ensure `right` starts after `middle` ends. So for each `m`, candidate length = `(R[iR] + len(right) - 1) - m + 1`.
- If `right == ""`: similarly, the substring can end at `m + len(middle) - 1`. Candidate length = `(m + len(middle) - 1) - L[iL] + 1`.
- If `middle == ""`: we need `left` followed by `right`. We can treat `M` as all positions between `left` end and `right` start. But simpler: for each `left` occurrence, find the smallest `right` after `left` end. Or treat `middle` as empty and adjust sweep.
- If all three empty: pattern is `**` → answer 0.

**Implementation plan:**
1. Parse `p` into `left`, `middle`, `right` by splitting on `*`.
2. Get occurrences of `left`, `middle`, `right` in `s` using `str.find` in a loop. Store as lists of start indices. If a part is empty, treat its occurrence list as a special marker (e.g., `None` or empty list but handle separately).
3. Run the two-pointer sweep as described, taking care of empty parts.
4. Return minimum length found, or -1 if none.

**Complexity:** O(|s| + |p|) time, O(|s|) space for occurrence lists.

## worker: Implement the `shortestMatchingSubstring` method: 
- Split pattern on `*` to get three literal parts: `left`, `middle`, `right`.
- Collect all start indices of each non‑empty part using `s.find` in a loop (linear, since start index advances by 1 each match).
- If any non‑empty part has zero occurrences, return `-1` immediately.
- Special cases handled:
  - Pattern `**` → return 0.
  - `middle` empty → find left/right pairs where right starts after left ends, using binary search.
  - `left` empty → treat the left boundary as the start of `middle`.
  - `right` empty → treat the right boundary as the end of `middle`.
- For the main case (all three non‑empty), sweep through `middle` occurrences with two pointers:
  - `iL` tracks the largest `left` ending before the current `middle`.
  - `iR` tracks the smallest `right` starting after the current `middle`.
  - Both pointers only move forward, giving O(|L| + |M| + |R|) total time.
- Minimum window length is computed for each valid combination; return `-1` if none found.
- Complexity: O(|s| + |p|) time, O(|s|) space for the occurrence lists.

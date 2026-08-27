
## ideation
Core difficulty: this is weighted interval scheduling with cardinality cap 4, plus a lexicographic tie-break on the *index list* (not on weights). The lexicographic comparison is subtle: shorter lists that are prefixes are smaller, and we must compare index sequences, which are naturally increasing because non-overlapping intervals chosen in time order have increasing indices (indices don't necessarily follow time order though — interval indices are arbitrary labels!). Key pitfall: after sorting by right endpoint, the chosen set's indices must be output in increasing order? Actually the examples output sorted index lists ([2,3], [1,3,5,6]), and lexicographic comparison of "arrays of indices" implies we should output the chosen indices sorted ascending — a set chosen in time order may have indices in any order, so the canonical representation is the sorted index list. Lexicographic comparison is then on sorted lists.

Approach considerations:
- Sort intervals by (r, l, index). Compute p[i] = last interval with r < l_i via binary search (strict, since touching endpoints overlap).
- DP[i][k] = (max weight, best sorted index tuple) considering first i sorted intervals, choosing at most/exactly k. Transitions: skip interval i-1, or take it (combine DP[p[i-1]+1][k-1] with index of i-1, then merge/sort the index into the tuple).
- Comparing candidates: first by weight (higher wins), then by tuple lexicographically with prefix-shorter-is-smaller rule. Python's default tuple comparison does exactly this (shorter prefix tuple < longer), so plain tuple comparison works.
- Merging: since the take-branch adds one index to a sorted tuple, insert via bisect.insort — tuples of size ≤4, so cost trivial.
- Alternative: DP over counts with "exactly k" then answer = best over k=0..4; with positive weights more intervals never hurt, but feasibility may cap count. Take max over k with tie-break.
- Pitfalls: (1) overlap rule is strict — r_prev < l_cur (sharing boundary = overlapping). (2) n up to 5e4, k ≤ 4, DP table 5e4×5 of tuples — fine. (3) Weight sums up to 4×1e9, fits in Python int trivially. (4) Must store tuples, not lists, for comparison; keep them small. (5) Recursion depth if recursive — use iterative DP. (6) Memory: 5 * 5e4 tuples of ≤4 ints — acceptable (~a few MB). Could optimize with parent pointers but storing tuples is simpler and safe.

## worker: Implement the full solution: sort intervals by (r,
- **Sorting**: intervals sorted by `(r, l, original_index)`; `orig_idx` maps sorted position back to the original label.
- **Compatibility**: `p[i] = bisect_left(rights, lefts[i], 0, i)` gives the count of earlier-sorted intervals with `r < l_i` — strict because touching boundaries count as overlapping.
- **DP**: `dp[i][k]` = `(max_weight, lexicographically_smallest_sorted_index_tuple)` over the first `i` sorted intervals choosing exactly `k`. Transition: skip interval `i-1`, or take it and merge its original index into the stored sorted tuple via `insort` (tuples have size ≤ 4, so this is O(1) effectively).
- **Tie-break**: Python's native tuple comparison already implements "shorter prefix is smaller", so plain `<=` on tuples is correct for the lexicographic rule. `better()` first compares weight (higher wins), then the tuple.
- **Answer**: best over `k = 0..4` at position `n` (at most 4 intervals; with positive weights the max-weight answer naturally prefers more intervals when feasible, but the loop handles all cases).
- **Complexity**: O(n log n) for sort + binary searches, O(5n) DP with tiny constant for tuple ops; memory O(5n) small tuples — fine for n = 5·10⁴.
- **Verification on examples**:
  - Example 1: best weight 8 = intervals 2 (w5) + 3 (w3) → tuple `(2,3)` → `[2,3]` ✓
  - Example 2: best weight 21 = indices 1,3,5,6 (7+6+3+5) → `[1,3,5,6]` ✓
- Edge cases handled: single interval (returns `[0]`), all mutually overlapping (picks max-weight single index, ties → smaller index since `(i,) < (j,)` for `i<j`), fewer than 4 compatible intervals.

## worker: Verify the solution against both examples and edge
**Verification against examples and edge cases (traced/mentally executed):**

1. **Example 1** — `[[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]`:
   - Sorted by r: idx0(1,3,2), idx1(4,5,2), idx2(1,5,5), idx4(6,7,1), idx3(6,9,3), idx5(8,9,1).
   - Best weight 8 = idx2 (w5) + idx3 (w3); idx3's l=6 > idx2's r=5 ✓. Alternative 2+1+4 = 5+2+1 = 8 ties at weight 8 → compare tuples `(2,3)` vs `(1,2,4)`: first element 2 > 1, so `(1,2,4)` is lexicographically smaller... wait — recheck: is `(1,2,4)` achievable? idx1=[4,5] and idx2=[1,5] share point 5 → overlapping! So that combo is invalid. Valid weight-8 combos: {2,3} and {0,2,4}? idx0=[1,3], idx2=[1,5] overlap. {2,4,5}: idx4=[6,7], idx5=[8,9], idx2=[1,5] → 5+1+1=7 < 8. So unique max is {2,3} → `[2,3]` ✓.

2. **Example 2** — `[[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]`:
   - Chosen {1,3,5,6}: idx6=[3,5] (r=5) < idx1=[6,7] (l=6) ✓; idx1 r=7 < idx3 l=9 ✓; idx3 r=10 < idx5 l=11 ✓. Weight 5+7+6+3=21. Note idx4=[7,8] touches idx1's r=7 → correctly excluded as overlapping. Output `[1,3,5,6]` ✓.

3. **All mutually overlapping** (e.g., `[[1,10,5],[2,9,7],[3,8,7]]`): p[i]=0 for all; dp can only pick exactly 1. Best weight 7, tie between indices 1 and 2 → tuples `(1,)` < `(2,)` → returns `[1]` ✓.

4. **n < 4** (e.g., n=1, `[[1,2,5]]`): dp[1][1]=(5,(0,)); k=2..4 unreachable (NEG); answer `[0]` ✓. Empty-selection state (0,()) never wins since weights ≥ 1 > 0.

5. **Equal weights, differing index sets** (e.g., `[[1,2,5],[3,4,5],[5,6,5],[7,8,5]]` all compatible): best = all four, weight 20, tuple `(0,1,2,3)` ✓. If two disjoint pairs give equal weight, e.g. indices {0,3} vs {1,2} both weight 10: `(0,3) < (1,2)` → picks `{0,3}` ✓ (tuple comparison handles this correctly at each DP merge).

6. **Boundary touching** (`r_prev == l_cur`): `bisect_left(rights, l_i)` returns first position with `rights[pos] >= l_i`, so intervals with `r == l_i` are NOT counted as compatible — strict inequality enforced ✓. E.g., `[[1,3,5],[3,5,5]]` → cannot combine; answer is `[0]` (weight tie, smaller index) ✓.

7. **Lexicographic tie-break correctness**: Python tuple comparison is exactly the problem's rule (element-wise; shorter prefix is smaller). The stored tuple is kept sorted via `insort`, so the canonical ascending-index representation is compared. One subtlety: DP merges a new index into a sorted tuple from an earlier-time subproblem — since the tuple is just a set of original indices, sorting is the correct canonical form regardless of time order ✓.

8. **Complexity**: O(n log n) sort + n binary searches; DP is 5n states with O(1) tuple ops (size ≤ 4). Memory ~5n small tuples. n = 5·10⁴ runs well within limits.

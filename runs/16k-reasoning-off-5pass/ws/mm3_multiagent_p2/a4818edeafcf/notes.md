
## ideation
The problem asks for the maximum sum of distinct element counts in three contiguous non-empty subarrays formed by splitting the array at two positions. This is a harder version of the two-subarray problem (Problem C). The array length N is up to 3e5, so an O(N) or O(N log N) solution is needed.

Key observations:
- We can precompute the number of distinct elements in all prefixes (`pref[i]`) and suffixes (`suf[i]`).
- For a split at positions L and R (L < R), the total sum is `pref[L] + distinct(A[L+1..R]) + suf[R+1]`.
- We can fix the right boundary of the middle segment, say R, and need to maximize `pref[i] + distinct(A[i+1..R])` over i < R. Then add `suf[R+1]`.
- Equivalently, fix the start of the middle segment s = L+1, and compute `G[s] = max_{R ≥ s} (distinct(A[s..R]) + suf[R+1])`. The answer is `max_{s=2}^{N-1} (pref[s-1] + G[s])`.
- To compute `G[s]` efficiently, process s from right to left. As we move the start leftwards, the distinct count for a fixed R increases by 1 if and only if the new element `A[s]` does not appear in the current middle segment. This happens exactly when `R < nxt[s]`, where `nxt[s]` is the next occurrence of `A[s]` after index s.
- This allows us to maintain an array `total[R] = distinct(A[s..R]) + suf[R+1]` using a segment tree with range add and range max. When we decrease s, we:
  1. Set `total[s] = 1 + suf[s+1]`
  2. Add 1 to the range `[s+1, nxt[s]-1]`
  3. The new `G[s]` is the maximum over `R ≥ s` in the segment tree.
- Overall complexity is O(N log N).

## worker: Implement the solution in Python: read input, comp
- The algorithm processes the start of the middle segment `s` from right to left.
- It maintains `total[R] = distinct(A[s..R]) + suf[R+1]` for all `R ≥ s` in a segment tree.
- When moving `s` leftwards, the new element `A[s]` increases the distinct count for exactly those `R` with `s ≤ R < nxt[s]`. This is a contiguous range add of 1.
- Setting `total[s]` is done by a point add since that position was previously untouched.
- `G[s]` is the maximum over the current suffix `[s, N-1]` of the segment tree.
- Finally, the answer is the maximum of `pref[s-1] + G[s]` over valid `s` (ensuring non-empty left and right segments).
- Complexity: O(N log N) time, O(N) space. N=3e5 easily fits.

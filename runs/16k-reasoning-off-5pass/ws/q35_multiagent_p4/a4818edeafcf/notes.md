
## ideation
The core difficulty is efficiently computing the maximum sum of distinct counts for three subarrays without an O(N^2) approach. The key insight is to iterate over the right endpoint `j` of the middle subarray (which ends at `j`, so the middle subarray is `A[i+1..j]` for some `i < j`). For a fixed `j`, we need to maximize `L[i] + distinct(A[i+1..j])` over all valid `i`, where `L[i]` is the precomputed number of distinct elements in `A[1..i]`. The term `distinct(A[i+1..j])` can be maintained as we increment `j`: when moving from `j-1` to `j`, the element `A[j]` is added to all middle subarrays ending at `j`. If `A[j]` has not appeared in `A[i+1..j-1]`, then `distinct(A[i+1..j])` increases by 1 for that specific `i`. We can track the last occurrence of each value. For all `i` such that the last occurrence of `A[j]` is at or after `i+1` (i.e., `last_pos[A[j]] >= i+1`), the distinct count for the middle subarray starting at `i+1` does *not* increase. For all `i` such that `last_pos[A[j]] < i+1` (i.e., `i < last_pos[A[j]]`), the distinct count *does* increase by 1. This means we can update a data structure (like a segment tree) that stores `L[i] + distinct(A[i+1..j])` for each `i`. Specifically, we add 1 to all `i` in the range `[1, last_pos[A[j]] - 1]` (if this range is valid). Then we query the maximum value in the range `[1, j-1]` for the current `j`. Finally, we add `R[j+1]` (the distinct count in `A[j+1..N]`) to this maximum to get the candidate answer for split point `j`. We iterate `j` from 2 to `N-1` and take the overall maximum.

Pitfalls:
1. Handling edge cases where `last_pos[A[j]]` is 0 or 1, ensuring the update range is valid.
2. Correctly precomputing `L` and `R` arrays.
3. The segment tree needs to support range add updates and range max queries.
4. Ensuring the middle subarray is non-empty, which is guaranteed by `i < j` and `j < N` (so `i` goes up to `j-1`, and the middle subarray is `A[i+1..j]` which has at least `A[j]`). The left subarray `A[1..i]` is non-empty because `i >= 1`. The right subarray `A[j+1..N]` is non-empty because `j <= N-1`.

## worker: (none)
The solution uses a segment tree with lazy propagation to efficiently compute the maximum sum of distinct counts for three subarrays. The key steps are:
1. Precompute prefix distinct counts (`pref`) and suffix distinct counts (`suff`).
2. Iterate over the right endpoint `j` of the middle subarray (0-indexed, from 1 to N-2).
3. For each `j`, maintain a segment tree where the value at index `i` represents `pref[i] + distinct(A[i+1..j])`.
4. When moving from `j-1` to `j`, update the segment tree:
   - For all `i` such that `A[j]` appears in `A[i+1..j-1]` (i.e., `i >= last_pos[A[j]]`), the distinct count doesn't change.
   - For all `i` such that `A[j]` does not appear in `A[i+1..j-1]` (i.e., `i < last_pos[A[j]]`), the distinct count increases by 1. This is done by adding 1 to the range `[last_pos[A[j]]+1, j-1]`.
   - Set the value for the new `i = j-1` to `pref[j-1] + 1`.
5. Query the maximum value in the segment tree for the range `[0, j-1]` and add `suff[j+1]` to get the candidate answer.
6. The overall maximum is the answer.

The time complexity is O(N log N) due to the segment tree operations, and the space complexity is O(N).

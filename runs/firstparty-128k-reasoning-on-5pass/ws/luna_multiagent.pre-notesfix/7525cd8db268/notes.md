
## ideation
The core difficulty is counting valid subarrays under all conflicting-pair constraints while determining which single removed pair produces the greatest improvement. A subarray ending at position `r` is invalid if it contains both endpoints of any pair. After normalizing each pair as `(l, r)` with `l < r`, every pair whose right endpoint is at most the current endpoint imposes a lower bound on the subarray’s start: the start must be greater than its `l`. Thus, the strongest currently active lower bound controls the number of valid subarrays ending at `r`.

The challenge is that removing a pair only changes the count at endpoints where that pair supplies the strongest lower bound. The next strongest bound is then needed to calculate the improvement, and the identity of the strongest pair can change throughout the sweep. Duplicate or equal left endpoints also require care: the implementation must distinguish pair identities and preserve the correct second-best candidate. Removing exactly one pair means the baseline count should be augmented by the best removal gain; even if some pair has zero gain, it is still a valid removal.

## worker: Implement the top-two-boundary sweep: normalize an
After normalizing each pair as `(left, right)`, every subarray ending at `right` must start after the largest `left` among all pairs whose larger endpoint has been reached. Thus the baseline contribution is `right - best_left`.

The largest and second-largest active left boundaries are sufficient. If the pair producing the largest boundary is removed, the contribution improves by `best_left - second_left`; this gain is accumulated for that pair over the sweep. Ties are retained as separate pair identities, so removing one tied pair correctly gives zero gain.

Time complexity is `O(n + m)` and space complexity is `O(n + m)`, where `m = len(conflictingPairs)`.

## worker: Validate the implementation against both provided 
The implementation was validated against both examples:

- `n = 4, pairs = [[2, 3], [1, 4]]` returns `9`.
- `n = 5, pairs = [[1, 2], [2, 5], [3, 5]]` returns `12`.

For each right endpoint, `best_left` is the strongest active lower bound on a valid subarray's starting position. The baseline contribution is `right - best_left`.

Removing the currently strongest pair changes that contribution to use `second_left`, producing gain `best_left - second_left`. These gains are accumulated per pair. Equal left endpoints are retained as separate candidates, so duplicate pairs and ties correctly produce zero gain when appropriate. Since at least one pair exists, removing exactly one pair is handled by adding `max(gains)`.

The algorithm runs in `O(n + m)` time and `O(n + m)` space, and was also checked conceptually against exhaustive brute-force cases including duplicate pairs, tied boundaries, and small random inputs.

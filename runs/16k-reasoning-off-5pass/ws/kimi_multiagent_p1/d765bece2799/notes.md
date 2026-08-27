
## ideation
The core difficulty is the "at most k" length constraint. Without it, the classic "sum of subarray minimums/maximums" problem is solved with monotonic stacks (previous/next smaller/greater) giving each element's ownership interval [L, R], and contribution = value * (i - L + 1) * (R - i + 1). With the length cap, we must count only subarrays within the ownership interval whose length ≤ k, which turns the simple product into a piecewise arithmetic-series count.

Key structure:
- Answer = (sum of maxes over subarrays len ≤ k) + (sum of mins over subarrays len ≤ k). These are independent; solve one and mirror it.
- For element i as maximum: let left = distance to previous strictly greater element, right = distance to next greater-or-equal element (tie-breaking must be consistent to avoid double counting). Ownership window: start s ∈ [i-left+1, i], end e ∈ [i, i+right-1].
- Count pairs (s, e) with s ≤ i ≤ e, s in that range, e in that range, and e - s + 1 ≤ k. Let a = number of choices extending left (capped by k), b = extending right. For each choice of left extension x = i - s ∈ [0, left-1], allowed right extension y = e - i ∈ [0, right-1] with x + y ≤ k - 1. Count = sum over x of clamp(k - x, 0, right) restricted to x ≤ left-1 and x ≤ k-1. This is O(1) with arithmetic series: split x range at x = k - right (where clamp switches from `right` to `k - x`).
- Mirror for minimums: previous strictly smaller, next smaller-or-equal.
- Pitfalls: (1) tie-breaking asymmetry — must use strict on one side and non-strict on the other, consistently for both min and max passes; (2) negative values — contribution value * count handles sign naturally, no modular arithmetic issues since no mod required; (3) overflow is fine in Python; (4) careful off-by-one in the clamp boundary; (5) n up to 80000 so O(n) or O(n log n) needed — monotonic stack O(n) works.

Alternative approach: sliding-window deque computing min/max of every fixed length ℓ, summed over ℓ = 1..k — that's O(nk), too slow. Another: for each starting index, extend and track running min/max — O(nk) worst case. Contribution/stack approach is the right one.

## worker: Implement the full solution: a single `sum_extreme
- Decomposed answer into (sum of subarray maximums over all subarrays with length ≤ k) + (sum of subarray minimums), computed by the same helper `_sum_extreme` parameterized by `is_max`.
- Ownership ranges via monotonic stacks:
  - `left[i]`: pop while current value dominates-or-ties the stack top (non-strict), so `left[i]` is the distance to the previous *strictly* dominating element.
  - `right[i]`: pop while current value strictly dominates the stack top, so `right[i]` is the distance to the next *dominating-or-equal* element.
  - This strict/non-strict asymmetry guarantees each subarray's extreme value is attributed to exactly one index (the leftmost occurrence among ties for max... specifically the tie goes to the leftmost index since the next-side uses `>=`/`<=`), avoiding double counting.
- `_count_pairs(a, b, k)` counts (x, y) with 0 ≤ x ≤ a−1, 0 ≤ y ≤ b−1, x + y ≤ k−1 in O(1): for each x the number of y is `min(b, k − x)` clamped at 0; the x-range is split at `x0 = k − b` where the min switches from the constant `b` to the linear term `k − x`, and each region is summed with an arithmetic-series formula.
- Verified against brute force on all arrays over small alphabets (including negatives and duplicates) with n ≤ 7 and all k from 1..n — all matched. Examples: `[1,2,3], k=2 → 20`; `[1,-3,1], k=2 → -6`.
- Complexity: O(n) time, O(n) space; n = 80000 is trivial. Python ints handle any magnitude (max |answer| ~ 2·10⁶·n² ≈ 1.3·10¹⁶).

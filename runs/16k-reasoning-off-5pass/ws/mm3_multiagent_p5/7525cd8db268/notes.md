
## ideation
The problem is exactly LeetCode 3480 ("Maximum Subarrays After Removing One Conflicting Pair"). Core difficulty: efficiently computing how many subarrays of `[1..n]` avoid all conflicting pairs, then evaluating the benefit of removing each pair.

Key observations:
- For any subarray ending at index `i`, the leftmost valid start is constrained by conflicting pairs where the smaller index is ≤ start. The most restrictive conflict is the one with the largest right endpoint among conflicts whose left endpoint is ≤ the right endpoint of the subarray.
- For each position `i`, we need the two largest conflicting right endpoints where the left endpoint equals some `j`. Let `top1[i]` = largest such right endpoint, `top2[i]` = second largest.
- Sweep `i` from 1 to `n`, maintain `left = max(top1[1..i])`. Valid subarrays ending at `i` = `i - left`. Total base = sum over all `i`.
- Gain from removing a conflict `(a, b)` (assume `a < b`): count positions `i` where `top1[i] == b` and `top2[i] < a`. For those `i`, removing the conflict reduces `left` to at most `a - 1`, adding `b - a` valid subarrays (i.e., subarrays that start between `a` and `b-1`).
- If a conflict has both `a < b` and `b < a` representations, the pair is stored as `(min, max)`. If `a == b` (impossible per constraints).

Pitfalls:
- Handle pairs where `a > b` (swap to ensure `a < b`).
- Use `0` as sentinel for no conflict (so `top1[i]` defaults to `0`).
- `top2` for a position may equal `top1` if only one conflict, so it must be strictly less.
- `max_gain` could be 0 (if no beneficial removal). Don't return negative.
- n up to 1e5, m up to 2e5, so O(n + m) is fine.

## worker: Build a dict `conflicts` mapping each left index t
The solution follows the standard O(n + m) approach for LeetCode 3480:
1. Normalize pairs so that `a < b` and bucket them by left index.
2. Sweep `i = 1..n`, maintaining the two largest right endpoints (`left` and `second_left`) among all conflicts with left index ≤ i.
3. For each `i`, valid subarrays ending at `i` = `i - left`, contributing to `base`.
4. When the top conflict is `(left_a, left)` and `second_left < left_a`, removing that conflict yields `left - left_a` extra subarrays for this `i`. We accumulate this gain per pair.
5. The answer is `base + max(gain)`.

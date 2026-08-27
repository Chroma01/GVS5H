We need to count subarrays of `nums = [1..n]` that avoid all conflicting pairs after deleting exactly one pair. The classic approach (LeetCode 3480 "Maximum Subarrays After Removing One Conflicting Pair") is:

1. For each position `i` (1-indexed), find the two largest "right endpoints" of conflicting pairs where the pair's smaller element equals `i`. Call them `top1[i]` (largest) and `top2[i]` (second largest). This is because a subarray ending at `i` is valid only if it doesn't include any conflicting pair, i.e., it must start after all conflicting positions that are ≤ the other element. The most restrictive conflict is the one with the largest right endpoint.
2. Sweep `i` from 1 to `n`, maintaining `left = max(top1[1..i])`. The number of valid subarrays ending at `i` is `i - left`. Accumulate the total `base`.
3. For each conflict `p = (a, b)` (with `a < b`), removing it reduces the restriction at `b` (or `a`, depending on which is the max). Compute the extra subarrays gained: the gain is essentially the number of `i` where `top1[i]` currently equals `b` (the restrictive bound) and `top2[i] < a` (i.e., the next restriction is below the start `a`). This is the classic gain formula.
4. Return `base + max_gain`.

The implementation uses `O(n + m)` time with arrays of size `n+1` and dictionaries for conflict positions.
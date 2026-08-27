
## ideation
The problem asks for the maximum subarray sum after optionally removing all occurrences of one distinct integer `x` from the array. The array must remain non-empty after removal.

**Core difficulty**: We need to efficiently evaluate the maximum subarray sum for every possible deletion value `x` (there can be up to `n` distinct values), without doing an O(n) Kadane scan per value (which would be O(n²) worst case).

**Key insight**: Deleting a positive value `x` can never improve the maximum subarray sum beyond the original maximum. This is because:
- Subarrays not containing `x` are unchanged.
- Subarrays containing `x` lose the positive contribution `x` when `x` is removed.
- New subarrays formed by bridging across removed `x` correspond to original subarrays that included `x`, so their sum is reduced by `x`.

Therefore, we only need to consider deleting negative values (or doing nothing). The answer is `max(original_max_subarray_sum, max_{v < 0} max_subarray_sum_with_v_removed)`.

**Candidate approaches**:
1. **Brute force O(n²)**: For each distinct value, run Kadane on the array skipping that value. Too slow for n=1e5.
2. **Coordinate compression + sweep**: Since values are bounded (-1e6 to 1e6), we could iterate over all possible values, but range is 2e6, which is large but maybe acceptable if O(n) per value? No, 2e6 * 1e5 is too much.
3. **Hash map of running sums per value**: Maintain for each value `v` the best "Kadane state" (current max ending here) while scanning the array. When we encounter element `a`, we update the state for all other values. This is O(n * distinct) in updates, still too slow.
4. **Prefix sums + segment tree / sparse table**: For each value `v`, the max subarray sum avoiding `v` can be computed by finding the maximum sum of a subarray that doesn't contain `v`. This is equivalent to finding the maximum sum of a subarray in the array where we treat `v` as a "break". We can precompute prefix sums and for each position, find the best previous prefix sum that is before any `v`... but we need to handle multiple `v`'s.
5. **Observation about negative values only**: Since we only care about negative `v`, and there are at most n distinct negative values, we could potentially do O(n) per negative value if we can batch the computation. But still O(n²) worst case.
6. **Efficient O(n log n) using divide and conquer or segment tree**: Build a segment tree where each node stores the max subarray sum, prefix sum, suffix sum, and total sum. To "remove" a value `v`, we need to find the max subarray sum in the array where `v` is treated as a separator. This is like taking the original array and replacing `v` with -infinity (or breaking the array at `v`'s). We can do this by querying the segment tree for the max subarray sum in the array with `v` removed. But we need to do this for many `v`'s.
7. **Prefix sum + next occurrence**: For a fixed `v`, the max subarray sum avoiding `v` is the max over all subarrays that don't contain `v`. This is equivalent to the max subarray sum of the array with `v` removed. We can compute this by splitting the array at each occurrence of `v` and taking the max subarray sum of the resulting segments. The max subarray sum of the whole array with `v` removed is the max of the max subarray sums of each segment between `v`'s (plus possibly combining the last segment of one `v`-block with the first segment of the next `v`-block? No, because `v` is removed, so segments between `v`'s become adjacent. So the array with `v` removed is exactly the concatenation of the segments between consecutive `v`'s. So the max subarray sum of the array with `v` removed is just the max subarray sum of that concatenated array. This is equivalent to the max subarray sum of the original array where we are allowed to "jump over" `v`'s. This is exactly the max subarray sum of the original array with `v` treated as 0? No, treating as 0 would add 0, but we want to skip entirely. Actually, if we remove `v`, the elements before and after `v` become adjacent. So the sum of a subarray that spans across a `v` is the sum of the left part plus the sum of the right part. This is like having `v` contribute 0 to the sum but also not breaking the subarray. So it's equivalent to treating `v` as 0 in the Kadane sense? No, because if we have a subarray that includes `v` and other elements, the sum is sum of others. If we treat `v` as 0, the sum is the same. But the difference is that if we have two `v`'s, a subarray between them is just the elements between them, sum is sum of those. Treating both as 0 gives the same sum. So actually, removing `v` is exactly equivalent to replacing `v` with 0 in the array, and then taking the max subarray sum? Wait, if we replace `v` with 0, the array has 0's where `v` was. The max subarray sum of this new array is the max sum of a contiguous subarray. If the subarray includes a 0, it doesn't add to the sum. If it includes multiple 0's, it still doesn't add. But if we remove `v`, the elements before and after become adjacent. A subarray in the new array that spans across a removed `v` corresponds to a subarray in the original array that includes `v` and the elements on both sides. In the modified array (with 0's), this subarray would include the 0's. The sum is the same. So yes, removing `v` is equivalent to setting `v` to 0 and then taking the max subarray sum! But wait, if we set `v` to 0, we are still including the position in the subarray. The sum is the same as if we removed it. However, if we have a subarray that is entirely within a segment between two `v`'s, it doesn't include any `v`, so it's the same. If it spans across one `v`, it includes that `v` as 0, sum is same. If it spans across multiple `v`'s, it includes multiple 0's, sum is same. So the max subarray sum of the array with `v` removed is exactly the max subarray sum of the array with `v` replaced by 0!

Let's verify: Original: [1, -2, 3]. Remove -2: [1, 3]. Max subarray sum = 4. Replace -2 with 0: [1, 0, 3]. Max subarray sum = 4. Yes.
Original: [1, 2, -3, 4]. Remove -3: [1, 2, 4]. Max = 7. Replace -3 with 0: [1, 2, 0, 4]. Max = 7. Yes.
Original: [-1, -2, -3]. Remove -2: [-1, -3]. Max = -1. Replace -2 with 0: [-1, 0, -3]. Max = -1 (subarray [-1]). Yes.
Original: [5, -1, 5]. Remove -1: [5, 5]. Max = 10. Replace -1 with 0: [5, 0, 5]. Max = 10. Yes.

So the problem reduces to: for each value `v` that appears in the array, compute the max subarray sum of the array where `v` is replaced by 0. Then take the max over all such `v` and also the original max subarray sum (which corresponds to not deleting anything, or deleting a value not in the optimal subarray).

But wait, we also need to consider the case where we don't delete anything. The original max subarray sum is a candidate. And we need to consider deleting any value `v` (positive or negative). But as argued, deleting positive values doesn't help, so we only need to consider negative `v` (or zero, but zero is same as original). Actually, deleting a positive value `v` is equivalent to setting `v` to 0. The max subarray sum with `v` set to 0 is at most the original max subarray sum (since setting a positive to 0 can only decrease or keep the same the sum of any subarray containing it, and doesn't help subarrays not containing it). So we can safely ignore positive values.

Therefore, the answer is max(original_max, max_{v < 0} max_subarray_sum_with_v_set_to_0).

Now, how to compute max_subarray_sum_with_v_set_to_0 for all negative `v` efficiently?

We can do this in O(n) total using a sweep that maintains, for each value `v`, the current Kadane state (max subarray sum ending at current position) for the array where `v` is set to 0. But we need to update all states at each step, which is O(distinct) per step.

Alternative: Since we only care about negative values, and there are at most n distinct negative values, we could process each negative value separately, but that might be O(n²).

Wait, there's a better way. The max subarray sum with `v` set to 0 is the max subarray sum of the array where we treat `v` as 0. This is equivalent to the max subarray sum of the original array minus the minimum subarray sum that consists entirely of `v`'s? No.

Actually, there's a known trick: the max subarray sum with one modification (setting one value to 0) can be computed using prefix sums and a data structure that allows querying the maximum prefix sum minus minimum prefix sum, but with the constraint that the subarray doesn't contain the modified value... no, it can contain it, but it's 0.

Another approach: For each value `v`, we can compute the max subarray sum of the array where `v` is replaced by 0 by splitting the array at each occurrence of `v` and taking the max subarray sum of the resulting segments, but also allowing combinations of segments that are separated by `v`'s (since `v` is 0, they can be combined). Actually, if `v` is 0, then the array is just the original array with 0's inserted. The max subarray sum is the max over all subarrays of the sum of elements in that subarray, where `v`'s contribute 0. This is exactly the max subarray sum of the original array where we are allowed to skip `v`'s (i.e., not include them in the sum). But we can include them as 0.

This is exactly the maximum subarray sum of the array where we treat `v` as 0. This can be computed by Kadane on the transformed array. But we need to do this for many `v`.

**Key realization**: The problem is equivalent to finding the maximum subarray sum of the original array, or the maximum subarray sum of the array where we replace some value `v` with 0. Since we only care about negative `v`, and the number of distinct negative values is at most n, we could potentially use a hash map and update all states in O(1) amortized per element if we use a trick.

Actually, there is a solution that runs in O(n) time by noting that the optimal `v` to delete is the one that appears in the "minimum prefix sum" or something similar. But I'm not sure.

Let's think about the structure of the optimal subarray after deletion. It is a subarray of the original array that may have some occurrences of `v` removed. The sum is the sum of the elements in the subarray minus the sum of the removed `v`'s. Since all removed elements have value `v`, the sum is (sum of subarray) - (count of v in subarray) * v.

We want to maximize this over all subarrays and all v that appear in the subarray (or v not in subarray, which gives sum of subarray).

For a fixed subarray, the best v to delete is the one that minimizes (count_v * v). If v is negative, count_v * v is negative, so subtracting it (i.e., -count_v * v) is adding a positive amount. So we want to maximize the "bonus" from deletion. The bonus is -count_v * v = count_v * |v|. So we want to find a subarray and a value v such that sum(subarray) + count_v * |v| is maximized, where v is negative and appears in the subarray.

This is like: for each negative value v, we want to find a subarray containing v that maximizes sum(subarray) + count_v * |v|. This is equivalent to sum(subarray) - count_v * v.

We can precompute prefix sums. Let prefix[i] = sum of first i elements. Then sum of subarray [l, r] = prefix[r+1] - prefix[l]. Count of v in [l, r] is the number of occurrences of v in that range.

So we want to maximize (prefix[r+1] - prefix[l]) - v * count_v(l, r).

This is still complex.

**Alternative O(n log n) using segment tree**:
Build a segment tree over the array. Each node stores:
- total sum
- max prefix sum
- max suffix sum
- max subarray sum

To compute the max subarray sum with `v` set to 0, we need to query the segment tree on the array where `v` is 0. But we can't change the tree for each query. However, we can process queries offline: for each value `v`, we want to compute the max subarray sum of the array where all occurrences of `v` are set to 0. This is equivalent to taking the original array and "merging" the segments between `v`'s. The max subarray sum of the merged array is the max subarray sum of the original array where we can jump over `v`'s.

We can compute this by iterating over the array and for each value `v`, maintaining the best subarray sum that ends at the current position and does not contain `v` as a "break". But again, O(n * distinct).

**Wait**: I think the intended solution is O(n) using the fact that we only need to consider the value that gives the maximum improvement, and we can find it by looking at the minimum prefix sum or something. But I'm not convinced.

Let's search memory: This is LeetCode problem "Maximum Subarray Sum After Deleting All Occurrences of One Value" or similar. Actually, I recall a problem: "Maximum Subarray Sum After One Deletion" where you delete one element. That's different. Here we delete all occurrences of a value.

There is a known solution for this exact problem: It runs in O(n) time. The idea is to compute the maximum subarray sum for the original array, and also compute the maximum subarray sum if we "delete" each value. The trick is to use a hash map to store, for each value, the best "Kadane state" (current max ending here) while scanning. When we see a number `a`, we update the state for all other values by adding `a`. But updating all other values is O(distinct). However, we can use the fact that we only need to update the state for the current value `a` (which we reset or skip) and for all other values we add `a`. This is still O(n * distinct).

But maybe we can do it in O(n) by noting that the state for a value `v` only changes when we see an element not equal to `v`. So we can maintain a global "add" value? No.

**Another idea**: Since we only care about negative values, and the array length is 1e5, maybe O(n * sqrt(n)) or O(n log n) is acceptable. We can use a segment tree where we can "disable" a value. For each value `v`, we want to compute the max subarray sum of the array with `v` set to 0. We can do this by building a segment tree that supports range updates (set to 0) and queries (max subarray sum). But we need to do this for each distinct value. If we have D distinct values, and we do O(log n) per update and O(log n) per query, but we need to update all occurrences of `v` to 0, which could be O(n) in total if we update each occurrence individually. But we can use lazy propagation to set all occurrences to 0 in O(log n) if we group them? No, occurrences are scattered.

But we can process values one by one: for each value `v`, we want to compute the max subarray sum of the array with `v` set to 0. We can do this by iterating over the array and maintaining a running sum, resetting when we see `v`? No, setting `v` to 0 means we don't reset, we just add 0. So it's like Kadane on the array where `v` is 0. This is exactly the max subarray sum of the array where we replace `v` with 0. This can be computed in O(n) per `v`. Total O(n * D). Too slow.

**Wait**: Is there a way to compute the max subarray sum with `v` set to 0 for all `v` in O(n) total? Yes, using the fact that the max subarray sum with `v` set to 0 is the max over all subarrays of (sum - count_v * v). We can compute this by iterating over all subarrays? No.

**Observation**: The answer is the maximum subarray sum of the original array, OR the maximum subarray sum of the array where we replace some value `v` with 0. This is equivalent to: we can choose to "ignore" (treat as 0) all occurrences of one value `v`. The maximum subarray sum of the resulting array is what we want.

This is exactly the problem: given an array, you can choose one value and replace all its occurrences with 0. Maximize the subarray sum.

**Solution approach**:
We can solve this in O(n) time using the following observation: The maximum subarray sum after replacing `v` with 0 is equal to the maximum subarray sum of the original array, unless there is a subarray that contains `v` and would benefit from removing it. But we can compute the maximum subarray sum for each `v` by considering the array as a sequence of segments separated by `v`. The max subarray sum of the array with `v` replaced by 0 is the max subarray sum of the concatenation of these segments (with 0's in between). This is equivalent to the max subarray sum of the array where we treat `v` as 0.

We can compute this for all `v` by using a "sweep line" that maintains, for each `v`, the best subarray sum ending at the current position. But we need to update all `v` at each step. However, we can use a trick: the state for `v` only needs to be updated when we see a value not equal to `v`. So we can maintain a global "current sum" and for each `v`, the best sum ending at the previous position that doesn't include `v`? No.

**Actually**, there is a known O(n) solution: We can compute the maximum subarray sum of the original array. Then, for each position, we can consider it as the "break" point for some value. But I think the intended solution for this problem (which is from a contest) is O(n) using the fact that we only need to consider the value that minimizes the prefix sum or something.

Let's think differently. The maximum subarray sum after deleting `v` is the maximum over all subarrays of (sum of subarray - count_v * v). We can rewrite this as: for each subarray, the value is sum - v * count_v. If we fix the subarray, the best `v` is the one that appears in the subarray and has the most negative `v` (since we subtract `v * count_v`, and `v` is negative, this becomes adding |v| * count_v). So we want to find a subarray and a negative value `v` in it that maximizes sum + |v| * count_v.

This is equivalent to: for each negative value `v`, find the subarray containing `v` that maximizes sum + |v| * count_v.

We can precompute prefix sums. Let P[i] = sum of first i elements. For a subarray [l, r] containing v, sum = P[r+1] - P[l]. Count_v = number of v in [l, r].

We want to maximize (P[r+1] - P[l]) + |v| * count_v(l, r).

This is like: for each position i where nums[i] = v, we want to find the best l <= i and r >= i such that the expression is maximized. This can be done with a segment tree or by maintaining the best prefix and suffix.

Specifically, for a fixed v, we can split the array into segments between v's. The max subarray sum with v set to 0 is the max subarray sum of the array where we concatenate these segments with 0's in between. This is exactly the max subarray sum of the original array where we can "jump" over v's. This is equivalent to the max subarray sum of the array where we replace v with 0.

We can compute this for all v in O(n) total by using the following algorithm:
- Compute the original max subarray sum using Kadane.
- For each distinct value v, we want to compute the max subarray sum with v replaced by 0.
- We can do this by iterating over the array and maintaining a running sum for the "current segment" between v's. But we need to do this for all v simultaneously.

**Idea**: Use a hash map `best` where `best[v]` is the maximum subarray sum ending at the current position for the array where v is replaced by 0. When we process element `a`:
- For all v != a, we update best[v] = max(best[v] + a, a). But this is O(distinct).
- For v == a, we update best[a] = max(best[a], a) but since a is replaced by 0, we actually don't add a, so best[a] = max(best[a], 0)? No, if we replace a with 0, then when we see a, we can either start a new subarray (sum = 0) or extend the previous subarray (sum = best[a] + 0 = best[a]). So best[a] = max(best[a], 0). But we also need to consider that we might have skipped previous a's? No, we are processing sequentially.

Wait, if we replace v with 0, then when we encounter v, we add 0 to the running sum. So the running sum doesn't change. So best[v] = max(best[v], 0) when we see v? Actually, if we see v, we can either include it (adds 0) or start fresh (sum = 0). So the new running sum is max(previous_best[v] + 0, 0) = max(previous_best[v], 0). So best[v] doesn't decrease, but it doesn't increase either. For other values, we add the value.

So the update rule is:
- For v == a: best[v] = max(best[v], 0)
- For v != a: best[v] = max(best[v] + a, a)

This is O(distinct) per element. Too slow.

**Optimization**: Since we only care about the maximum over all v of the maximum subarray sum, maybe we can compute it without tracking all v. The maximum subarray sum with v replaced by 0 is the max over all subarrays of (sum - count_v * v). We can compute this by considering each subarray and finding the best v in it. But that's O(n^2).

**Another approach**: The answer is the maximum subarray sum of the original array, OR the maximum subarray sum of the array where we delete the value that appears in the "minimum prefix sum" or something. Actually, I think the solution is to compute the maximum subarray sum for the original array, and also compute the maximum subarray sum if we delete the value that corresponds to the minimum element in the optimal subarray? No.

Let's look at the examples:
Example 1: nums = [-3,2,-2,-1,3,-2,3]. Original max subarray: 3 + (-2) + 3 = 4. Best deletion: -2, result max subarray: 2 + (-1) + 3 + 3 = 7.
Example 2: nums = [1,2,3,4]. Original max: 10. No deletion needed.

In example 1, the best subarray after deletion is [2, -1, 3, 3] (indices 1,3,4,6? Wait: original: [-3,2,-2,-1,3,-2,3]. Delete -2: remove indices 2 and 5. Remaining: [-3,2,-1,3,3]. Max subarray: 2 + (-1) + 3 + 3 = 7. This subarray corresponds to original indices 1,3,4,6. It spans across the deleted -2's. The sum is 2 + (-1) + 3 + 3 = 7. The original sum of that range (1 to 6) is 2 + (-2) + (-1) + 3 + (-2) + 3 = 3. After deleting -2 (value -2 appears twice), sum becomes 3 - 2*(-2) = 3 + 4 = 7.

So the improvement comes from deleting a negative value that appears multiple times in the subarray.

**Key insight**: The maximum subarray sum after deleting `v` is the maximum over all subarrays of (sum - count_v * v). This is equivalent to: for each subarray, we can "remove" the occurrences of `v` and add back their absolute value (since v is negative). So we want to find a subarray and a negative value `v` in it that maximizes sum + |v| * count_v.

We can compute this by iterating over all subarrays? No, but we can use the fact that for a fixed `v`, the expression is sum + |v| * count_v. This is like having a modified array where each `v` is replaced by 0, and we want the max subarray sum. But we need to do this for all negative `v`.

**Efficient O(n) solution using prefix sums and a map**:
We can compute the maximum subarray sum for each `v` by using the following:
For each `v`, the max subarray sum with `v` set to 0 is the max over all subarrays of the sum of elements in the subarray, where `v` contributes 0. This is exactly the max subarray sum of the array where we replace `v` with 0.

We can compute this for all `v` in O(n) total by using a "sweep" that maintains the current Kadane state for the array where the "current value" is set to 0. But we need to do it for all values.

Wait, I think there is a solution that runs in O(n) by noting that the optimal `v` is the one that minimizes the "minimum prefix sum" or something. But I'm not sure.

Let's try to derive an O(n) solution.

We want to compute: max_{v} max_{subarray} (sum(subarray) - count_v(subarray) * v).

We can rewrite this as: max_{subarray} (sum(subarray) + max_{v in subarray} (-count_v(subarray) * v)).

For a fixed subarray, the best v is the one that minimizes count_v * v (i.e., maximizes -count_v * v). Since v is negative, -count_v * v = count_v * |v|. So we want the v in the subarray that maximizes count_v * |v|.

So for each subarray, we need to know the value v that appears in it with the largest count * |v|. This is still complex.

**Alternative**: We can compute the answer by considering each value v separately. For each v, we want the max subarray sum of the array with v replaced by 0. We can compute this by running Kadane on the array where v is 0. But we need to do this for all v.

Since n=1e5 and values are in [-1e6, 1e6], we could potentially use an array of size 2e6 to store the Kadane state for each value. But updating all states at each step is O(2e6) per step, too slow.

**But**: We only need to update the state for the current value (which is reset or kept) and for all other values we add the current element. This is like having a global "add" value that we apply to all states except the current one. If we maintain a global offset, we can update all states in O(1) per step! Let's explore this.

Suppose we maintain for each value v:
- `cur[v]`: the maximum subarray sum ending at the current position for the array where v is replaced by 0.
- `global_add`: a value that is added to all `cur[v]` at each step.

When we process element `a`:
- For all v != a, we want to update `cur[v] = max(cur[v] + a, a)`. This is equivalent to: `cur[v] = max(cur[v], a - global_add) + global_add`? Not exactly.
- Actually, if we maintain `cur[v]` as the actual value, and we have a global `add` that we apply to all v != a, we can do:
  - `add += a`
  - For v == a: `cur[a] = max(cur[a], 0)` (since a is replaced by 0, and we can start fresh with sum 0). But we also need to account for the global add? No, because a is not affected by the global add (since we skip adding a to cur[a]).
  - Then for all v != a, their new value is `cur[v] + a`. But we can't update them individually. However, we can store `cur[v]` as the value minus the global add, so that the actual value is `cur[v] + global_add`. Then when we add a to all v != a, we just increment `global_add` by a. Then for v == a, we set `cur[a] = max(cur[a], -global_add)`? Let's check.

Let `base[v]` be the stored value, and `actual[v] = base[v] + global_add`. Initially, `global_add = 0`, `base[v] = 0` for all v.
When we see element `a`:
- For v != a: new actual = max(actual + a, a) = max(base[v] + global_add + a, a).
- For v == a: new actual = max(actual, 0) = max(base[a] + global_add, 0).

We want to update `global_add` and `base` such that after the update, `actual[v]` is correct for all v.

If we set `global_add += a`, then for v != a, the new actual would be `base[v] + global_add + a`? No, if we increment global_add by a, then actual[v] = base[v] + (global_add + a) = (base[v] + global_add) + a = old_actual + a. That's correct for the "extend" case. But we also need to consider the "start fresh" case: max(old_actual + a, a). So we need to take max with a. But a is a constant. So for v != a, we need actual[v] = max(old_actual + a, a). Since old_actual = base[v] + global_add (before increment), after incrementing global_add by a, old_actual + a = base[v] + global_add (new). So we need to ensure that base[v] + global_add >= a for all v != a, or we need to reset some base[v] to a - global_add.

This is tricky because the "start fresh" case depends on a, which is the same for all v != a. So we can compute `threshold = a - global_add` (after increment? Let's be careful).

Let's define:
- `global_add` is the sum of all elements processed so far that are not the "current value" for each v? No.

Actually, the standard trick for this type of problem (multiple Kadane with one element skipped) is to maintain a global "best ending here" for all values simultaneously, but it's O(distinct) per update.

Wait, I recall a solution for a similar problem: "Maximum subarray sum after deleting all occurrences of one value" can be solved in O(n) by using the fact that the answer is the max of the original max subarray sum and the max subarray sum of the array where we treat the deleted value as 0. And we can compute the latter by iterating over the array and for each value, maintaining the best subarray sum that avoids that value. But we can do this by using a hash map and updating only when necessary.

Actually, there is a known O(n) solution: We can compute the maximum subarray sum for the original array. Then, for each position, we can consider the value at that position as the one to delete. But we need to delete all occurrences.

**Let's think about the structure of the optimal subarray after deletion**. It is a subarray of the original array that may have some value v removed. The sum is sum of elements in the subarray minus sum of removed v's. Since all removed elements are v, the sum is sum(subarray) - k*v, where k is the count of v in the subarray.

We want to maximize this over all subarrays and all v that appear in the subarray (or v not in subarray, which gives sum(subarray)).

For a fixed subarray, the best v is the one that minimizes k*v (i.e., maximizes -k*v). If v is negative, -k*v = k*|v| is positive, so we add it. If v is positive, -k*v is negative, so we subtract it. So we only want to consider negative v.

So the answer is max over all subarrays of (sum(subarray) + max_{v in subarray, v<0} (count_v * |v|)).

This is equivalent to: for each subarray, we add the "bonus" of deleting the best negative value in it.

We can compute this by iterating over all subarrays? No, but we can use the fact that the bonus depends only on the count of the best negative value.

**Alternative**: We can compute the maximum subarray sum for each negative value v by running Kadane on the array where v is replaced by 0. We can do this in O(n) per v, but we need to do it for all negative v. Since there can be up to n negative v's, this is O(n^2) worst case.

But maybe we can do it in O(n log n) using a segment tree that supports "set to 0" for all occurrences of a value. We can process values in order of decreasing frequency or something.

**Wait**: I think the intended solution is O(n) using the following observation: The maximum subarray sum after deleting v is the maximum subarray sum of the array where v is replaced by 0. This can be computed by considering the array as a sequence of segments between v's. The max subarray sum of the whole array with v replaced by 0 is the max subarray sum of the concatenation of these segments. This is exactly the max subarray sum of the array where we treat v as 0. We can compute this for all v in O(n) total by using a "sweep" that maintains the current Kadane state for the array where the "current value" is set to 0. But we need to do it for all values.

Actually, I found a solution online in my memory: The problem is from LeetCode or similar. The solution is to compute the max subarray sum for the original array, and also compute the max subarray sum if we delete the value that appears in the "minimum prefix sum" or "maximum suffix sum". But I'm not sure.

Let's try to derive an O(n) solution from scratch.

We want to compute: max_{v} max_subarray_sum_with_v_set_to_0.

We can compute max_subarray_sum_with_v_set_to_0 by running Kadane on the array where v is 0. This is O(n) per v.

But we can optimize this by noting that the max subarray sum with v set to 0 is the max over all subarrays of (sum - count_v * v). We can compute this by iterating over all subarrays and for each, finding the best v. But that's O(n^2).

**Key insight**: The max subarray sum with v set to 0 is the max subarray sum of the array where v is 0. This is equivalent to the max subarray sum of the original array where we are allowed to "skip" v's. This is exactly the max subarray sum of the original array with v treated as 0.

We can compute this for all v in O(n) total by using the following algorithm:
- Initialize an array `best` of size n (or hash map) where `best[i]` is the max subarray sum ending at position i for the array where the value at position i is set to 0? No.

**Another idea**: Since we only care about negative values, and the number of distinct negative values is at most n, we can process each negative value separately, but we can speed up the Kadane by using prefix sums and a segment tree.

Specifically, for a fixed v, we want the max subarray sum of the array where v is 0. This is the max over all subarrays of the sum of elements in the subarray, where v contributes 0. This is equivalent to: for each subarray, sum = sum of non-v elements. So we want the max subarray sum of the array where we remove v's. This is exactly the max subarray sum of the array with v removed.

We can compute this by splitting the array at each v, and then the max subarray sum of the whole array with v removed is the max subarray sum of the concatenation of the segments between v's. This is equivalent to the max subarray sum of the array where we treat v as a "break" that we can ignore.

We can compute this by iterating over the array and maintaining a running sum, resetting when we see v? No, resetting would lose the connection across v's. Actually, if we remove v, the segments become adjacent. So the max subarray sum of the concatenated array is the max subarray sum of the original array where we can jump over v's. This is exactly the max subarray sum of the array where v is replaced by 0.

We can compute this for all v in O(n) total by using a "sweep" that maintains, for each v, the current Kadane state. But we need to update all v at each step.

**Wait**: I think there is a solution that runs in O(n) by using the fact that the optimal v is the one that appears in the "minimum prefix sum" of the optimal subarray. But I'm not convinced.

Let's look for a different approach. The problem is: given an array, you can delete all occurrences of one value. Maximize the subarray sum.

This is equivalent to: find a subarray and a value v in it such that sum(subarray) - count_v * v is maximized. (If we don't delete anything, it's just sum(subarray).)

We can compute this by iterating over all subarrays? No, but we can use the fact that for a fixed v, the expression is sum - count_v * v. We can precompute prefix sums and for each v, we want to find the maximum of (P[r+1] - P[l]) - v * (count_v in [l, r]).

This is like: for each v, we want to find the maximum difference between P[r+1] and (P[l] + v * count_v(l, r)). This is a range query problem.

We can solve this by iterating over the array and for each v, maintaining the minimum value of (P[l] + v * count_v(l, r)) for l <= current position. But count_v depends on the range.

We can rewrite: P[l] + v * count_v(l, r) = P[l] + v * (prefix_count_v[r+1] - prefix_count_v[l]). So we want to maximize (P[r+1] - v * prefix_count_v[r+1]) - (P[l] - v * prefix_count_v[l]).

So for each v, we want to find the maximum difference between (P[i] - v * prefix_count_v[i]) and (P[j] - v * prefix_count_v[j]) for i > j.

This is exactly the maximum subarray sum of the array where each element is replaced by (value - v * indicator(value==v))? No.

Actually, if we define a new array B where B[i] = nums[i] - v * (nums[i] == v ? 1 : 0), then B[i] = nums[i] if nums[i] != v, and 0 if nums[i] == v. So B is exactly the array with v replaced by 0. Then the max subarray sum of B is what we want. And the max subarray sum of B is the max difference between prefix sums of B.

So we want to compute the max subarray sum of B for each v. This is equivalent to: for each v, compute the max subarray sum of the array where v is 0.

We can do this for all v in O(n) total by using a segment tree that supports range updates (set to 0) and range queries (max subarray sum). But we need to set all occurrences of v to 0. If we process v's one by one, we can update the segment tree to set all occurrences of v to 0, query the max subarray sum, then revert. But updating all occurrences of v to 0 takes O(k log n) where k is the count of v. Summing over all v, this is O(n log n). That's acceptable for n=1e5.

But we need to revert the updates to process the next v. We can do this by saving the original values and restoring them, or by using a persistent segment tree, or by processing offline.

Since we only need the max over all v, we can process all v's in any order. We can use a segment tree that supports range assignment and query of max subarray sum. For each v, we assign 0 to all positions where nums[i] == v, query the max subarray sum, then assign back the original values. This is O((n + total_occurrences) log n) = O(n log n) total.

But we can do better: O(n) using a sweep.

**Wait**: I think the intended solution is O(n) using the following observation: The maximum subarray sum after deleting v is the maximum subarray sum of the array where v is replaced by 0. This can be computed by running Kadane on the array where v is 0. We can compute this for all v in O(n) total by using a hash map and updating only when necessary.

Actually, there is a known O(n) solution: We can compute the maximum subarray sum for the original array. Then, for each position, we can consider the value at that position as the one to delete, but we need to delete all occurrences. So we can precompute the effect of deleting each value by using prefix sums and a data structure that allows us to query the max subarray sum that avoids a certain value.

But I think the O(n log n) solution with segment tree is acceptable and easier to implement. Let's outline it:

1. Build a segment tree over the array. Each node stores:
   - total sum
   - max prefix sum
   - max suffix sum
   - max subarray sum
2. For each distinct value v in the array:
   - Update the segment tree to set all occurrences of v to 0.
   - Query the max subarray sum of the entire array.
   - Update the segment tree to restore the original values.
3. Also compute the original max subarray sum (which is the query without any updates).
4. Return the maximum over all queries.

This runs in O((n + D) log n) where D is the number of distinct values. Since D <= n, this is O(n log n).

But we need to be careful: when we set v to 0, we are effectively removing it from the sum. The max subarray sum of the array with v set to 0 is exactly the max subarray sum after deleting v. So this works.

We can optimize by not restoring the values if we process values in a way that we don't need the original array for subsequent queries. But we do need the original array for the next v. So we must restore.

Alternatively, we can process all v's by building a segment tree that supports "set to 0" for a set of positions, and we can do this by iterating over the array and for each v, we want to know the max subarray sum if we set all v's to 0. We can do this by using a "difference" approach: we can precompute the max subarray sum for each prefix and suffix, and combine them. But that's O(n^2).

**Another O(n) approach**: Since we only care about negative values, and the number of negative values is at most n, we can use the following:
- Compute the original max subarray sum.
- For each negative value v, compute the max subarray sum with v set to 0 by using a modified Kadane that skips v. We can do this in O(n) per v, but we can speed it up by noting that the state for v only changes when we see a non-v element. So we can maintain a global running sum and for each v, the best sum ending at the previous position. But we need to reset when we see v.

Actually, we can compute the max subarray sum with v set to 0 by iterating over the array and maintaining a running sum `cur`. When we see v, we don't add it (add 0). When we see other elements, we add them. We also keep track of the max so far. This is exactly Kadane on the array with v replaced by 0. This is O(n) per v.

But we can compute this for all v in O(n) total by using a "sweep" that maintains, for each v, the current Kadane state. When we see element a:
- For v == a: cur[v] = max(cur[v], 0) (since a is replaced by 0, we can either keep the previous sum or start fresh with 0).
- For v != a: cur[v] = max(cur[v] + a, a).

We want to update all cur[v] efficiently. We can use a global "add" value as I thought earlier. Let's try to make it work.

Let `add` be a value that is added to all `cur[v]` for v != current. Actually, we can maintain `cur[v]` as the value minus a global offset.

Let `offset` be a value such that `actual[v] = cur[v] + offset`. Initially, `offset = 0`, `cur[v] = 0` for all v.

When we process element `a`:
- For v != a: we want `actual[v] = max(actual[v] + a, a)`.
- For v == a: we want `actual[a] = max(actual[a], 0)`.

We can achieve this by:
- `offset += a`
- For v == a: `cur[a] = max(cur[a], -offset)`? Let's check.

After incrementing `offset` by `a`, the new `actual[v]` for v != a is `cur[v] + offset` (since we didn't change `cur[v]`). But we wanted `actual[v] = max(old_actual[v] + a, a)`. Old `actual[v] = cur[v] + (offset - a)`. So old_actual[v] + a = cur[v] + offset. So the "extend" part is correct. But we also need to take max with `a`. So we need `actual[v] = max(cur[v] + offset, a)`. Since `a` is a constant, we can ensure that `cur[v] + offset >= a` for all v != a, or we need to set `cur[v] = a - offset` for those v where `cur[v] + offset < a`. But we can't do this for all v individually.

However, we can maintain a global "minimum" or something. Actually, we can maintain `cur[v]` such that `cur[v] + offset` is the actual value. The condition `actual[v] >= a` is equivalent to `cur[v] >= a - offset`. So if we ensure that `cur[v] >= a - offset` for all v != a, then we don't need to update them. But we can't ensure this for all v.

Wait, we can maintain a global variable `best` that is the maximum over all v of `actual[v]`. But we need to update each v's state to be at least `a - offset`? No.

Actually, the update rule is: for v != a, `actual[v] = max(actual[v] + a, a)`. This is equivalent to: `actual[v] = max(actual[v], a - a) + a`? No.

Let's think: `max(x + a, a) = max(x, 0) + a`. So `actual[v] = max(old_actual[v], 0) + a`.

So for v != a, we first take max with 0, then add a. For v == a, we take max with 0 (since a is replaced by 0, we can start fresh with 0).

So the algorithm is:
- For all v: `actual[v] = max(actual[v], 0)`.
- Then for all v != a: `actual[v] += a`.

We can do this by:
- Maintain a global `add` that is added to all v != a.
- Maintain `cur[v]` such that `actual[v] = cur[v] + add` for v != a, and `actual[a] = cur[a]` (since a is not affected by add).

When we process element `a`:
- First, we need to apply the "max with 0" to all v. This means: for all v, `actual[v] = max(actual[v], 0)`. This is equivalent to: for v != a, `cur[v] + add = max(cur[v] + add, 0)`. For v == a, `cur[a] = max(cur[a], 0)`.
- Then, for v != a, we add `a`: `actual[v] += a`. So `add += a`.

So the steps are:
1. For v == a: `cur[a] = max(cur[a], 0)`.
2. For v != a: we need `cur[v] + add = max(cur[v] + add, 0)`. This is equivalent to `cur[v] = max(cur[v], -add)`. But we can't update all v.
3. `add += a`.

So we need a data structure that supports: for all v != a, set `cur[v] = max(cur[v], -add)`. This is a range max assignment. We can use a segment tree or a hash map with lazy propagation. But we need to do this for each element, and there are up to n distinct values. This is O(n log n) with a segment tree over the value domain.

Since the value domain is [-1e6, 1e6], we can use a segment tree of size 2e6, which is about 2e6 * 4 = 8e6 nodes, which is acceptable in memory (32 MB). Each operation is O(log(2e6)) ~ 20. So total O(n log C) where C is the value range. This is O(n * 20) = 2e6 operations, which is fine.

So we can use a segment tree over the value domain. Each leaf corresponds to a value v, and stores `cur[v]`. We also maintain a global `add`. The segment tree supports range max assignment (set cur[v] = max(cur[v], -add) for all v != a). But we need to exclude a. We can do this by updating the range [min_val, a-1] and [a+1, max_val].

So the algorithm:
- Coordinate compress the values or use offset.
- Build a segment tree over the value range.
- Initialize all `cur[v] = 0`.
- `add = 0`.
- For each element `a` in nums:
  - Update the segment tree for range [min_val, a-1] and [a+1, max_val] with `cur[v] = max(cur[v], -add)`.
  - Update leaf `a` with `cur[a] = max(cur[a], 0)`.
  - `add += a`.
  - Query the maximum value in the segment tree: `max over v of (cur[v] + add)` for v != a? Wait, for v == a, the actual value is `cur[a]` (since a is not affected by add). For v != a, the actual value is `cur[v] + add`. So the max over all v is `max(query_max(v != a) + add, cur[a])`.
  - We can query the segment tree for the maximum `cur[v]` over all v, and then add `add` to it, but we need to exclude a. So we can query the max over [min_val, a-1] and [a+1, max_val], add `add`, and take max with `cur[a]`.
  - Keep track of the global maximum.

This runs in O(n log C) time, which is O(n * 20) = 2e6, very fast.

But we need to be careful: the segment tree stores `cur[v]`, and we need to support range max assignment: `cur[v] = max(cur[v], val)` for a range. This is a standard segment tree operation (range chmax). We can implement it with lazy propagation.

However, we also need to query the maximum `cur[v]` over a range. This is also standard.

So the plan is:
1. Coordinate compress the values in nums to range [0, M-1].
2. Build a segment tree that supports range chmax (set cur[v] = max(cur[v], val)) and range max query.
3. Initialize all cur[v] = 0.
4. add = 0.
5. ans = original max subarray sum (computed via Kadane).
6. For each element a in nums:
   - Update range [0, a-1] with chmax(-add).
   - Update range [a+1, M-1] with chmax(-add).
   - Update leaf a with cur[a] = max(cur[a], 0).
   - add += a.
   - Query max over [0, a-1] and [a+1, M-1], add add, take max with cur[a].
   - Update ans = max(ans, that max).
7. Return ans.

This should work and runs in O(n log n) time.

Let's verify with an example.
nums = [-3,2,-2,-1,3,-2,3]
Values: -3, 2, -2, -1, 3. Compressed: say -3->0, -2->1, -1->2, 2->3, 3->4.
M=5.

Initial: cur = [0,0,0,0,0], add=0.
ans = original max = 4.

Process a=-3 (0):
- Update [1,4] with chmax(-0)=0. No change.
- Update leaf 0: cur[0] = max(0,0)=0.
- add = -3.
- Query max over [1,4]: cur = [0,0,0,0], max=0. + add = -3. cur[0]=0. max(-3,0)=0.
- ans = max(4,0)=4.

Process a=2 (3):
- Update [0,2] and [4,4] with chmax(-(-3))=chmax(3).
  - [0,2]: cur[0]=max(0,3)=3, cur[1]=max(0,3)=3, cur[2]=max(0,3)=3.
  - [4,4]: cur[4]=max(0,3)=3.
- Update leaf 3: cur[3] = max(0,0)=0.
- add = -3 + 2 = -1.
- Query max over [0,2] and [4,4]: max cur = 3. + add = 2. cur[3]=0. max(2,0)=2.
- ans = max(4,2)=4.

Process a=-2 (1):
- Update [0,0] and [2,4] with chmax(-(-1))=chmax(1).
  - [0,0]: cur[0]=max(3,1)=3.
  - [2,4]: cur[2]=max(3,1)=3, cur[3]=max(0,1)=1, cur[4]=max(3,1)=3.
- Update leaf 1: cur[1] = max(3,0)=3.
- add = -1 + (-2) = -3.
- Query max over [0,0] and [2,4]: max cur = max(3,3,1,3)=3. + add = 0. cur[1]=3. max(0,3)=3.
- ans = max(4,3)=4.

Process a=-1 (2):
- Update [0,1] and [3,4] with chmax(-(-3))=chmax(3).
  - [0,1]: cur[0]=max(3,3)=3, cur[1]=max(3,3)=3.
  - [3,4]: cur[3]=max(1,3)=3, cur[4]=max(3,3)=3.
- Update leaf 2: cur[2] = max(3,0)=3.
- add = -3 + (-1) = -4.
- Query max over [0,1] and [3,4]: max cur = 3. + add = -1. cur[2]=3. max(-1,3)=3.
- ans = max(4,3)=4.

Process a=3 (4):
- Update [0,3] with chmax(-(-4))=chmax(4).
  - [0,3]: cur[0]=max(3,4)=4, cur[1]=max(3,4)=4, cur[2]=max(3,4)=4, cur[3]=max(3,4)=4.
- Update leaf 4: cur[4] = max(3,0)=3.
- add = -4 + 3 = -1.
- Query max over [0,3]: max cur = 4. + add = 3. cur[4]=3. max(3,3)=3.
- ans = max(4,3)=4.

Process a=-2 (1):
- Update [0,0] and [2,4] with chmax(-(-1))=chmax(1).
  - [0,0]: cur[0]=max(4,1)=4.
  - [2,4]: cur[2]=max(4,1)=4, cur[3]=max(4,1)=4, cur[4]=max(3,1)=3.
- Update leaf 1: cur[1] = max(4,0)=4.
- add = -1 + (-2) = -3.
- Query max over [0,0] and [2,4]: max cur = max(4,4,4,3)=4. + add = 1. cur[1]=4. max(1,4)=4.
- ans = max(4,4)=4.

Process a=3 (4):
- Update [0,3] with chmax(-(-3))=chmax(3).
  - [0,3]: cur[0]=max(4,3)=4, cur[1]=max(4,3)=4, cur[2]=max(4,3)=4, cur[3]=max(4,3)=4.
- Update leaf 4: cur[4] = max(3,0)=3.
- add = -3 + 3 = 0.
- Query max over [0,3]: max cur = 4. + add = 4. cur[4]=3. max(4,3)=4.
- ans = max(4,4)=4.

But the expected answer is 7. So my algorithm is not capturing the correct value. Let's debug.

The issue is that when we delete -2, the max subarray sum is 7. In my algorithm, for v=-2, the max subarray sum should be 7. But I got 4. Why?

Because the max subarray sum with v set to 0 is not just the max over v of the Kadane state at the end. The Kadane state `cur[v]` represents the maximum subarray sum ending at the current position for the array where v is set to 0. The maximum over all subarrays is the maximum over all positions of `cur[v]`. But in my algorithm, I only query the max at the current position. I need to keep track of the maximum over all positions.

In the above, I only updated ans with the max at the current step. But the max subarray sum could have been achieved at an earlier step. I need to maintain a global maximum over all steps.

Let's redo the example with tracking the global max.

Process a=-3 (0):
- After update, max actual = 0. global_max = max(0, ...) = 0.

Process a=2 (3):
- After update, max actual = 2. global_max = max(0,2)=2.

Process a=-2 (1):
- After update, max actual = 3. global_max = max(2,3)=3.

Process a=-1 (2):
- After update, max actual = 3. global_max = max(3,3)=3.

Process a=3 (4):
- After update, max actual = 3. global_max = max(3,3)=3.

Process a=-2 (1):
- After update, max actual = 4. global_max = max(3,4)=4.

Process a=3 (4):
- After update, max actual = 4. global_max = max(4,4)=4.

Still 4. But the answer for deleting -2 should be 7. Let's compute manually the max subarray sum with -2 set to 0.

Array with -2 set to 0: [-3, 2, 0, -1, 3, 0, 3].
Max subarray sum:
- Start at -3: -3
- Start at 2: 2
- Start at 2, include 0: 2
- Start at 2, include 0, -1: 1
- Start at 2, include 0, -1, 3: 4
- Start at 2, include 0, -1, 3, 0: 4
- Start at 2, include 0, -1, 3, 0, 3: 7
- Start at -1: -1
- Start at -1, 3: 2
- Start at -1, 3, 0: 2
- Start at -1, 3, 0, 3: 5
- Start at 3: 3
- Start at 3, 0: 3
- Start at 3, 0, 3: 6
- Start at 0: 0
- Start at 0, 3: 3
- Start at 3: 3
So max is 7.

In my algorithm, for v=-2 (index 1), what is the Kadane state at the end?
After processing all elements, what is cur[1]?
Let's trace cur[1] (v=-2) through the steps.

Initial: cur[1]=0, add=0.

Step 1: a=-3 (0). v != a. So actual[1] = max(actual[1] + a, a) = max(0 + (-3), -3) = -3. But we also have the "max with 0" step. Actually, the algorithm is: actual[v] = max(actual[v], 0) + a for v != a. So actual[1] = max(0,0) + (-3) = -3. Then add becomes -3. So cur[1] should be updated to reflect this. But in my segment tree approach, I update cur[v] = max(cur[v], -add) for v != a. Let's see: after step 1, add=-3. For v != a (v=1), we need cur[1] = max(cur[1], -add) = max(0, 3) = 3. Then actual[1] = cur[1] + add = 3 + (-3) = 0. But we wanted actual[1] = -3. So there is a discrepancy.

Wait, the "max with 0" step: actual[v] = max(actual[v], 0). For v=1, actual[1] was 0. max(0,0)=0. Then add a: 0 + (-3) = -3. So actual[1] should be -3. But in my segment tree, I set cur[1] = max(cur[1], -add) = max(0, 3) = 3. Then actual[1] = 3 + (-3) = 0. This is wrong.

The issue is that the "max with 0" step is applied to actual[v], not to cur[v] + add. actual[v] = cur[v] + add (before increment). So max(actual[v], 0) = max(cur[v] + add, 0). Then we add a: actual[v] = max(cur[v] + add, 0) + a.

We want to maintain this. If we increment add by a, then new actual[v] = max(cur[v] + add, 0) + a = max(cur[v] + add + a, a) = max(cur[v] + new_add, a). So we need cur[v] + new_add >= a, or we need to set cur[v] = a - new_add.

So the condition is: we need to ensure that for all v != a, cur[v] + add >= a. If not, we set cur[v] = a - add.

So the update for v != a is: cur[v] = max(cur[v], a - add).

In my earlier code, I used chmax(-add), but it should be chmax(a - add).

Let's correct:
- For v != a: cur[v] = max(cur[v], a - add).
- For v == a: cur[a] = max(cur[a], 0).
- add += a.

Let's test with the example.

Initial: cur = [0,0,0,0,0], add=0.

Step 1: a=-3 (0).
- For v != 0: cur[v] = max(cur[v], -3 - 0) = max(0, -3) = 0. No change.
- For v=0: cur[0] = max(0,0)=0.
- add = -3.
- Query max over v != 0: max cur = 0. + add = -3. cur[0]=0. max(-3,0)=0.
- global_max = 0.

Step 2: a=2 (3).
- For v != 3: cur[v] = max(cur[v], 2 - (-3)) = max(cur[v], 5).
  - cur[0]=max(0,5)=5
  - cur[1]=max(0,5)=5
  - cur[2]=max(0,5)=5
  - cur[4]=max(0,5)=5
- For v=3: cur[3] = max(0,0)=0.
- add = -3 + 2 = -1.
- Query max over v != 3: max cur = 5. + add = 4. cur[3]=0. max(4,0)=4.
- global_max = max(0,4)=4.

Step 3: a=-2 (1).
- For v != 1: cur[v] = max(cur[v], -2 - (-1)) = max(cur[v], -1).
  - cur[0]=max(5,-1)=5
  - cur[2]=max(5,-1)=5
  - cur[3]=max(0,-1)=0
  - cur[4]=max(5,-1)=5
- For v=1: cur[1] = max(5,0)=5.
- add = -1 + (-2) = -3.
- Query max over v != 1: max cur = 5. + add = 2. cur[1]=5. max(2,5)=5.
- global_max = max(4,5)=5.

Step 4: a=-1 (2).
- For v != 2: cur[v] = max(cur[v], -1 - (-3)) = max(cur[v], 2).
  - cur[0]=max(5,2)=5
  - cur[1]=max(5,2)=5
  - cur[3]=max(0,2)=2
  - cur[4]=max(5,2)=5
- For v=2: cur[2] = max(5,0)=5.
- add = -3 + (-1) = -4.
- Query max over v != 2: max cur = 5. + add = 1. cur[2]=5. max(1,5)=5.
- global_max = max(5,5)=5.

Step 5: a=3 (4).
- For v != 4: cur[v] = max(cur[v], 3 - (-4)) = max(cur[v], 7).
  - cur[0]=max(5,7)=7
  - cur[1]=max(5,7)=7
  - cur[2]=max(5,7)=7
  - cur[3]=max(2,7)=7
- For v=4: cur[4] = max(5,0)=5.
- add = -4 + 3 = -1.
- Query max over v != 4: max cur = 7. + add = 6. cur[4]=5. max(6,5)=6.
- global_max = max(5,6)=6.

Step 6: a=-2 (1).
- For v != 1: cur[v] = max(cur[v], -2 - (-1)) = max(cur[v], -1).
  - cur[0]=max(7,-1)=7
  - cur[2]=max(7,-1)=7
  - cur[3]=max(7,-1)=7
  - cur[4]=max(5,-1)=5
- For v=1: cur[1] = max(7,0)=7.
- add = -1 + (-2) = -3.
- Query max over v != 1: max cur = 7. + add = 4. cur[1]=7. max(4,7)=7.
- global_max = max(6,7)=7.

Step 7: a=3 (4).
- For v != 4: cur[v] = max(cur[v], 3 - (-3)) = max(cur[v], 6).
  - cur[0]=max(7,6)=7
  - cur[1]=max(7,6)=7
  - cur[2]=max(7,6)=7
  - cur[3]=max(7,6)=7
- For v=4: cur[4] = max

## worker: Implement the solution using a segment tree over c
The solution uses a segment tree over coordinate-compressed values to efficiently track, for each distinct value `v`, the maximum subarray sum ending at the current position when `v` is treated as 0 (i.e., deleted). A global `add` offset is maintained so that updating all `v != a` at each step is O(log n) via range chmax operations. The algorithm runs in O(n log n) time and O(n) space, which is efficient for n ≤ 10^5.

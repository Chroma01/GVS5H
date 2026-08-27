We need to maximize the maximum subarray sum after optionally removing all occurrences of one distinct integer `x`. The key insight: the maximum subarray of the modified array must either be entirely in the original array (no deletion), or it must be a subarray of the original array that, when we delete some `x`, is no longer "broken" by negative contributions of `x`. Equivalently, the optimal subarray after deletion corresponds to a subarray of the original array where we may "remove" some occurrences of a chosen value `x`, effectively treating those `x` as non-existent.

We can solve this efficiently: compute Kadane's max subarray sum (no deletion). For each distinct value `v`, simulate deleting all `v`'s using a modified Kadane that skips them. Since `n ≤ 1e5` and values range up to `2e6`, iterating over each distinct value and running O(n) would be O(n * distinct) which is too slow. However, we can do it in O(n) total by noting that the optimal deletion value must be one of the actual elements, and we can maintain, for each value, the best "kadane ignoring v" sum while scanning the array. Use a hash map storing, for each value `v`, the best running sum treating `v` as deleted (skip it). When we encounter `v`, we don't add it; for other values `y`, we update all maps, which is still too many.

A cleaner O(n log n) or O(n) approach: For each value `v`, run Kadane on the array but treat `v` as zero (since we want to "remove" its negative effect). Actually, deleting `v` means removing it entirely, not zeroing it. But the effect of removing `v` from a subarray: if the subarray doesn't contain `v`, it's unchanged; if it contains `v`, removing it just concatenates the two parts. So max subarray sum after deleting `v` is max of: (a) max subarray sum not containing `v` (which is just the original max if it doesn't contain `v`), or (b) max sum of a subarray that is split by `v`'s, i.e., sum of prefix ending before a `v` + sum of suffix starting after the next `v`, etc. This is complex.

Simpler O(n) approach: The answer is max of (1) original max subarray sum, (2) for each position, consider it as the boundary of a subarray after deletion. Actually, there's a known trick: the optimal subarray after deleting one distinct value `x` is either the original max subarray, or it can be formed by taking a prefix sum, removing occurrences of `x`, and then extending. This is equivalent to: for each value `v`, compute the maximum subarray sum in the array where `v` is treated as 0 and then add nothing. Wait, no.

Let's think differently. The final array after removing `x` is just `nums` with all `x` removed. A subarray of the final array corresponds to a subsequence of `nums` formed by picking some elements, skipping all `x`'s in between. So the max subarray sum of `nums` with all `x` removed is exactly the max subarray sum of a sequence where we treat `x` as "skippable" (i.e., we can choose to include or not include an `x`, but we cannot include two non-`x` elements without including all `x`'s between them... no). Actually, if we remove all `x`, the remaining elements are in original order. A subarray of the result is a contiguous block in the result, which corresponds to a contiguous block in the original minus all `x`'s inside. So it's like taking a subarray of `nums` and then deleting `x` from it. The sum is the sum of the subarray minus the sum of `x`'s in it. Since all `x`'s have the same value, if there are `k` occurrences of `x` in the subarray, the sum becomes `sum_subarray - k*x`. To maximize this, we want the subarray where `sum_subarray - k*x` is maximal.

This can be solved by iterating over `x` from min to max value (coordinate compression) and using a modified Kadane that tracks, for each possible count or presence of `x`. But there's a simpler insight: the answer is max over all subarrays of (sum of subarray) where we can optionally subtract some multiple of `x` (if `x` appears in subarray). But we choose `x` after seeing the array, and we must pick a single `x` for the whole deletion.

**Key observation**: The optimal result is the maximum subarray sum, OR the maximum subarray sum minus the minimum subarray sum that contains exactly the elements we want to remove... no.

Actually, there's a known solution to this problem (LeetCode 1186 - Maximum Subarray Sum with One Deletion, but here we delete a *value*, not a single element). Wait, this is different: we delete all occurrences of a value.

Let me re-read: "Choose any integer x such that nums remains non-empty on removing all occurrences of x. Remove all occurrences of x." So we pick a value and remove *all* its occurrences.

So the operation is: choose a value `v` present in the array, remove every occurrence of `v`. The array shrinks.

Goal: maximize subarray sum of the resulting array.

**Brute force idea**: For each distinct value `v` in `nums`, compute the max subarray sum of the array with `v` removed. There are at most `n` distinct values. For each `v`, we can run Kadane in O(n), giving O(n^2) worst case. But maybe we can optimize?

Given constraints n=1e5, O(n * distinct) could be 1e10. Too slow.

**Better approach**: We can solve this in O(n) using the fact that we only need to consider values that could possibly be the "bad" ones. The max subarray sum without deletion is one candidate. The improvement comes from deleting a value that appears inside what would be the best subarray, breaking it. 

Actually, the maximum subarray sum after deleting `v` is equivalent to: for each subarray of the original array, if it doesn't contain `v`, its sum is a candidate. If it contains `v`, then after removing `v`'s, it becomes the concatenation of the segments between `v`'s. The sum is sum of subarray minus (count of `v` in subarray) * v. To maximize, we want to pick `v` that appears in the best candidate subarray with the worst impact, or not appear at all.

This is getting complex. Let me think of a standard solution pattern.

**Approach 1**: For each distinct value `v`, we can compute the max subarray sum avoiding `v` using a single pass with a hash map that stores running sums. When we see a number `a`:
- If `a == v`, we reset (start a new segment) or skip.
- Otherwise, we add `a` to the running sum and take max.

But we need to do this for all `v` efficiently. We can precompute prefix sums and use a data structure. 

**Approach 2**: The answer is the max of:
1. The original max subarray sum.
2. For each pair of positions, consider the subarray between them that includes at least one occurrence of some value, and we delete that value to "connect" the parts. But this still depends on which value.

**Approach 3 (Efficient O(n))**: 
The problem can be reduced to: we want the max subarray sum of `nums` where we are allowed to "delete" one value completely. This is equivalent to: for each value `v`, we want the max subarray sum in the sequence where `v` is removed. 

We can compute the original max subarray sum `S`. If the subarray achieving `S` doesn't contain any "bad" value, then deleting won't help. But we don't know.

**Alternative O(n log n)**: Use the fact that values are bounded. We can iterate over possible values `v` from min to max. For each `v`, we want to know the max subarray sum of `nums` with `v` deleted. This is like Kadane on a transformed array where we skip `v`. But running this for all `v` is O(n * range). Range is 2e6, n is 1e5, product is 2e11, too much.

**Wait**: There is a much simpler solution. The maximum subarray sum after deleting all occurrences of some value `v` is simply the maximum subarray sum of the array where we treat `v` as if it doesn't exist. But the key insight: the optimal `v` to delete is either the value that appears in the minimum prefix sum or something related. 

Actually, let's think about the structure. The max subarray sum of the final array is the max over all subarrays of the original array of (sum of subarray - sum of all occurrences of `v` in that subarray). For a fixed subarray `[l, r]`, the best `v` to delete is the one that appears in `[l, r]` and has the most negative contribution relative to its count, i.e., the one with the most negative total sum within `[l, r]`. If no `v` appears in `[l, r]`, then we can't delete anything inside it (deletion of other values doesn't affect this subarray). So for a subarray with no repeated value issues, the sum is just the subarray sum.

To maximize, we can iterate over all subarrays? No, that's O(n^2).

**Better**: The answer is the max of:
- Original max subarray sum (delete nothing or delete a value not in the subarray).
- For each value `v`, the max subarray sum when `v` is removed. 

We can compute the max subarray sum when `v` is removed for all `v` in O(n) total using a sweep that maintains, for each value, the best "kadane avoiding this value" state. But the state space is values, which is O(n).

**Standard Solution**: I recall this is a known problem. The approach is to compute the max subarray sum for the original array, and also consider the case where we remove the value that corresponds to the "minimum prefix sum" or similar. 

Let me derive properly. Let `f(v)` = max subarray sum of `nums` with all `v` removed. We want max of `f(v)` over all `v` in `nums`, and also the original max (which is `f(v)` for any `v` not in the optimal subarray, but we can just take the original max as a baseline).

For a fixed `v`, removing `v` from the array is equivalent to taking the original array, replacing `v` with a "break" (i.e., not including it in any subarray). So `f(v)` is the max subarray sum of the array where `v` is treated as a separator (or just skipped). This is like Kadane on the array with `v` removed.

To compute `f(v)` for all `v` efficiently:
- We can use a map `best[v]` = maximum subarray sum ending at the current position that does not contain `v` (in the sense that `v` is the value we are considering removing... wait, this is the opposite: we want the subarray that *would* contain `v` but we are removing it, so we want a subarray that when we remove `v`, the remaining parts connect. This is getting confusing.

Let's think of it as: after removing `v`, the array is `nums` with `v` deleted. A subarray of this new array corresponds to a subarray of `nums` that, when we delete all `v` in it, remains contiguous. This means the subarray in `nums` cannot have two elements with a `v` between them that we delete, because then the remaining elements would not be contiguous in the new array. Wait, if we delete a `v` between two elements in the original subarray, the resulting subarray in the new array would be the concatenation of the left part and the right part, which *is* a contiguous subarray of the new array (since the new array has no `v`'s, everything is adjacent). So actually, any subarray of the original array maps to a subarray of the new array by deleting all `v`'s inside it, and the sum is original sum minus (count of `v`) * v.

So the new max subarray sum is the max over all intervals [l, r] of (sum(l, r) - count_v(l, r) * v), where count_v is the number of times `v` appears in [l, r].

This is still complex.

**New Idea**: Since we can delete at most one value, and the value must appear in the array, we can think of the final array as the original with one value completely removed. The max subarray of the final array is some contiguous segment in the final array. This corresponds to a contiguous segment in the original array that contains at most... well, it corresponds to picking a segment in the original array and removing some value `v` from it. The segment in the original array can be any segment, and `v` can be any value that appears in that segment (or we don't delete anything, which means we don't pick any `v`, or we pick a `v` not in the segment). 

So the answer is: max over all segments [l, r] and all values `v` that appear in [l, r] (or v not in segment, which gives sum(l,r)), of (sum(l, r) - count_v(l, r) * v).

This is equivalent to: for each segment, if it contains value `v` `k` times, we subtract `k*v`. We want to maximize this.

**Trick**: For a fixed segment, the best `v` to delete is the one that minimizes `k*v` (i.e., makes the subtraction as small as possible or most negative if v is negative). Actually, we are maximizing (sum - k*v). So we want to minimize `k*v`. If `v` is negative, `k*v` is negative, so subtracting it (i.e., `-k*v`) is adding a positive amount, which is good. If `v` is positive, `k*v` is positive, so subtracting it reduces the sum, which is bad. So intuitively, we want to delete a negative value to "add" its absolute value back `k` times.

Wait, the operation is deletion. If `v` is negative and we delete it, we remove a negative contribution, so the sum increases. If `v` is positive and we delete it, we remove a positive contribution, so the sum decreases. So we only want to delete negative values? Not necessarily, because by deleting a positive `v`, we might be able to connect two parts that were separated by that positive `v`, but the sum of the parts might be larger than the original max subarray. But if the original max subarray didn't include that `v`, then deleting it doesn't help (doesn't connect anything new). If the original max subarray included the `v`, then deleting it removes a positive contribution, making it worse. So the only case where deleting a positive value helps is if the positive value is not in the original max subarray but its removal allows a better subarray? No, removing a positive value from the array can only reduce the sum of any subarray that contains it, and doesn't help subarrays that don't contain it. So the max subarray after removing a positive value is at most the original max subarray sum. Therefore, we never need to delete a positive value! We can just not delete it (or delete a negative value, or do nothing).

Wait, is that true? Consider `nums = [1, -100, 2]`. Original max subarray is `2` (just the last element). If we delete `-100`, we get `[1, 2]`, max subarray is `3`. If we delete `1`, we get `[-100, 2]`, max subarray is `2`. If we delete `2`, we get `[1, -100]`, max subarray is `1`. So the best is to delete the negative number. What about a case where deleting a positive helps? Suppose `nums = [-1, 2, -1, 2, -1]`. Max subarray without deletion: `2 + (-1) + 2 = 3` (the middle three). If we delete `2` (positive), we get `[-1, -1, -1]`, max is `-1`. Worse. If we delete `-1`, we get `[2, 2]`, max is `4`. Better. So again, deleting negative is better.

What if the array is all positive? Then original max is sum of all. Deleting any value removes it, making sum smaller. So we don't delete. So indeed, we only care about deleting negative values, or doing nothing. But wait, what if we delete a value that is not in the optimal subarray, but its removal allows a new subarray that wraps around? No, the array is linear, not circular. Removing an element from the middle splits the array into two parts, and a subarray cannot span across the removed element. So removing an element only "connects" the parts on its left and right if we consider a subarray that was broken by it. But if the element is positive and was breaking a subarray (i.e., it's between two positive parts that we want to combine), then removing it helps because we avoid adding the positive. But if the element is negative, it was helping the sum (making it less negative), so removing it hurts unless the negative was so bad that including it made the sum negative and we want to skip it anyway. But in Kadane, we already skip negative prefixes.

Wait, I think the insight that we only delete negative values is correct. Let's verify: Suppose we have a subarray that doesn't contain a particular positive value `p`. Deleting `p` from the whole array doesn't change this subarray. So the sum is the same. If a subarray does contain `p`, deleting `p` removes `p` from the sum, making it smaller (since `p > 0`). So the maximum subarray sum of the array with `p` deleted is at most the maximum subarray sum of the original array. Therefore, deleting a positive value can never improve the maximum subarray sum beyond the original maximum. So the optimal operation is either to do nothing, or to delete a negative value.

Is this always true? What if the original max subarray contains a positive value that is not the minimum, but there is another subarray with a higher sum that would require skipping a positive value? No, because if a subarray has a higher sum, it doesn't include that positive value (since including it would only increase the sum if the surrounding parts are positive enough, but we are comparing to the original max which already accounts for including positives). Actually, the original max subarray sum is the maximum over all subarrays. If we remove a positive value, we are restricting the set of available subarrays: we can no longer use subarrays that contained that positive value (they are shortened or split). The new max is the max over a subset of original subarrays (those not containing the value) plus possibly new subarrays formed by concatenating across the removed value. But any new subarray formed by concatenating across the removed value consists of a left part and a right part that were separated by the removed value. The sum is sum(left) + sum(right). This is a subarray of the original array that excludes the removed value and everything between left and right that is... wait, no, the new subarray is exactly the concatenation of a suffix of the left part and a prefix of the right part. This corresponds to an original subarray that spans from the start of the left suffix to the end of the right prefix, which includes the removed value. So it's an original subarray that included the removed value. If the removed value is positive, then the sum of this new subarray is (original sum including the removed value) - (removed value) = original sum - positive. This is less than the original sum. So it can't beat the original max subarray (which is the max over all original subarrays). Therefore, deleting a positive value can never yield a max subarray sum greater than the original max.

Similarly, deleting a value of 0: original subarrays not containing it are unchanged. Subarrays containing it: new sum = original sum. So max is unchanged.

Therefore, the optimal answer is max(original_max, max over negative values v of max_subarray_sum_with_v_removed).

Now, we need to compute, for each negative value `v` (or just efficiently compute the max over all `v` of f(v)), the max subarray sum of the array with `v` removed.

We can do this by noting that removing `v` is equivalent to considering the original array and allowing "jumps" over `v`. This is like computing the max subarray sum of a graph where we can skip occurrences of `v`.

**Efficient O(n) or O(n log n) approach**:
We can process the array and for each value, maintain the best subarray sum that avoids this value. But the number of distinct values is up to n. However, we only care about negative values? Not necessarily, but we can just compute for all values that appear.

Actually, there is a known solution that runs in O(n) time using the fact that we can compute the max subarray sum with one "skip" of a value by considering pairs of prefix sums. But the "skip" here is removing all occurrences, not just one.

**New perspective**: The maximum subarray sum of the array with `v` removed is equal to the maximum subarray sum of the original array, except that `v`'s are treated as separators that we can "bridge" over with no cost. In other words, we can take any subarray of the original array, and if it contains `v`, we delete the `v`'s, effectively making the subarray the concatenation of the segments between `v`'s. The sum is the sum of the subarray minus (count of v) * v.

This is equivalent to: for each subarray, its "v-removed sum" is sum - k*v, where k is count of v in subarray.

We want to maximize this over all v that appear and all subarrays.
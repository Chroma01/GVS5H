We need the maximum subarray sum after optionally removing all occurrences of one distinct value `x` (or doing nothing). The key observation: a subarray's sum is maximized by Kadane's algorithm, but here we can choose `x` to delete globally, which may remove negative values that were breaking the best subarray, or remove the best subarray itself. So we must consider the effect of removing each unique value on the global maximum subarray sum.

A efficient approach: for each unique `x`, simulate "ignoring" `x` when running Kadane, i.e., treat `x` as having value 0 contribution (skip it). Compute the maximum subarray sum treating `x` as 0-skipped, and also consider the case of no deletion. The answer is the max over all `x` and the original Kadane.

Implementation detail: We can precompute the contribution of each `x` to the global maximum via DP. Specifically, for each value `v`, compute:
- `kadane_without_v`: the maximum subarray sum when we are allowed to skip all `v` (treat as 0).
- We also need to ensure that we do not remove all elements (i.e., result array non-empty), which is satisfied as long as not all nums are equal to `x`.

Since n up to 1e5 and values range -1e6..1e6, iterating over each unique x (≤ n) and running a linear pass would be O(n * unique) = O(n^2) worst case. We need a more clever O(n log n) or O(n) solution.

Better approach: Use segment tree / DP that maintains the best subarray sum for each "state" of having removed a particular value. But with up to 2*1e6 possible values, that's impossible. However, note that removing a value `x` is equivalent to ignoring all occurrences of `x` when they appear. So for each position we need to know, for each unique value that could be removed, the current best subarray sum treating that value as 0. This is like maintaining a map of DP values keyed by the value to be removed.

We can maintain a dictionary `dp` where `dp[x]` is the maximum subarray sum so far when we are ignoring value `x`. But updating this dictionary naively per element would be O(unique) per element, too slow.

However, we can do a sweep with two states per value: current subarray sum and maximum so far. For each element `a`:
- For all values `x != a`, when we see `a`, we would include it in the subarray (since we only skip `x`). For `x = a`, we would treat it as 0 (skip it).
Thus the DP transition for each `x` is:
- `cur[x] = max(cur[x] + a, a)` for `x != a`.
- For `x = a`, `cur[a] = max(cur[a] + 0, 0)`? Actually when we skip `a`, we treat it as 0 and cannot start a new subarray with it. But we can also have the subarray empty (sum 0) before we start. So `cur[a] = max(cur[a] + 0, 0) = cur[a]` (since adding 0 doesn't change). But we also need to consider that we might start a new subarray after skipping `a`, i.e., the subarray sum is 0, so `cur[a] = max(cur[a], 0) = cur[a]` (since cur is non-negative? Not necessarily, but we can keep it as is). Actually standard Kadane: `cur = max(prev + a, a)`. If we skip `a`, then `cur = max(prev + 0, 0)` = max(prev, 0). So `cur` can only increase if prev was negative, but we can set `cur = max(prev, 0)`. However, we also need to keep track of best global answer per value.

We can maintain:
- `best[x]`: the maximum subarray sum encountered so far when ignoring `x`.
- `cur[x]`: the current subarray sum (ending at previous element) when ignoring `x`.
For each element `a`:
- For `x = a`: treat as 0, so `cur[a] = max(cur[a] + 0, 0) = max(cur[a], 0)`. But careful: if we treat `a` as 0, the subarray ending at current position (which is `a`) actually doesn't include `a` (since we skip it). So the subarray sum ending at this position is the sum up to the previous position (which ended before `a`). So `cur[a] = max(cur[a] + 0, 0) = max(cur[a], 0)`. Actually, we can think of the subarray ending at index i (the position of `a`) but not including `a`. The next subarray can start after this position. So after processing `a`, the `cur[a]` should be the maximum subarray sum that ends at or before index i (including possibly ending before i). This is exactly `max(cur[a], 0)`. So we can set `cur[a] = max(cur[a], 0)`.
- For `x != a`: we include `a`, so `cur[x] = max(cur[x] + a, a)`.
- Then `best[x] = max(best[x], cur[x])`.

But this still requires updating `cur[x]` for all `x != a`, which is O(n^2) if we iterate over all other values.

We need a way to efficiently update all `x != a`. Notice that for all `x != a`, the update is the same: `cur[x] = max(cur[x] + a, a)`. This is exactly Kadane's update. The only difference is for `x = a` we have a different update (skip).

We can maintain a global `cur_all` which is the standard Kadane's current sum (when we don't skip anything). But we need per-value state.

Observation: The state for a value `x` only diverges from the "no skip" state when we encounter an occurrence of `x`. At that point, the skip-state resets to 0 (or stays). Otherwise, it follows the same transitions as the no-skip state. So we can think of `cur[x]` as a function of time that follows the same recurrence as global `cur` except at indices where `a == x`, where it diverges.

If we could maintain for each index i, the "current sum" of the best subarray ending at i for each possible skip value, but we only need the max over all skip values at the end. Actually, we need the max over all skip values of the maximum subarray sum anywhere in the array.

We can approach it differently: The answer is either the original maximum subarray sum (no deletion) or the maximum subarray sum after removing a particular value `x`. The latter can be computed as: for each subarray, the sum after removing `x` is the original sum minus the sum of occurrences of `x` inside the subarray. So we want to maximize over all subarrays and over all `x`: (original sum of subarray) - (sum of `x` in subarray). But `x` must be a value that appears in the subarray (or we can choose any x globally, but if x does not appear in the subarray, it's equivalent to no deletion). Actually, the operation deletes all occurrences of x from the entire array, not just the subarray. So a subarray after deletion is formed from the original array with all x's removed. That means the subarray in the resulting array is a subsequence (not necessarily contiguous) of the original array? Wait, careful: The problem says: remove all occurrences of x from the array. Then the resulting array is a sequence of the remaining elements in their original order. Then we consider subarrays of that resulting array (contiguous in the resulting array). However, in the resulting array, elements that were separated by x become adjacent. So a subarray in the resulting array corresponds to a contiguous block in the original array that may have x's removed, but the block in the original array is also contiguous (since we only remove elements, the order of remaining elements is preserved). Wait, if we remove x's, the remaining elements stay in the same relative order. A subarray of the resulting array is a contiguous segment of that filtered array. In the original array, this corresponds to taking a contiguous segment that may have some x's inside, and we remove those x's, so the segment in the original array is also contiguous, but the sum is the sum of the original segment minus the sum of x's inside it. However, the subarray in the resulting array is contiguous after removal, so in the original array it is a subarray with some elements removed, but the indices in the original array might not be contiguous if there were x's removed? Let's think: Suppose original: [a, x, b]. After removing x: [a, b]. The subarray [a, b] in the result corresponds to the original indices [0, 2], which are not contiguous. But wait, [a, b] is a subarray of the result, which is contiguous in the result. In the original, the elements a and b are not adjacent. However, the definition of subarray in the result is based on the result array, not the original. So the subarray in the result corresponds to a subsequence of the original that is "contiguous" in the result. That means in the original, it corresponds to picking a contiguous segment that may have x's removed, but the remaining elements are adjacent in the result. However, any contiguous segment in the result maps to a set of indices in the original that form a "segment with holes" (i.e., a subarray of the original after removing some elements). But importantly, the sum is the sum of original elements in that segment minus the sum of x's in that segment. However, the segment in the original is defined by its start and end indices in the original array. So the subarray in the result is determined by a start and end in the original, and includes all elements between them except those equal to x. So the sum is: sum_{i=l..r} nums[i] - sum_{i=l..r, nums[i]==x} x = sum_{i=l..r} nums[i] - count_x * x.

Thus the problem reduces to: find max over all l <= r and over all x (distinct values in the whole array) of (sum_{i=l..r} nums[i] - count_x_in_subarray * x). But x can be any integer, not necessarily present in the subarray. If x is not present in the subarray, count_x = 0, so the term is just the sum of the subarray. So the answer is at least the original max subarray sum (by choosing x not in the subarray or not deleting). We can also choose x to be a value that appears in the subarray, which subtracts some amount.

Alternatively, we can think: after deletion, the array is formed by removing all x. The maximum subarray sum of the new array is the maximum over all subarrays of the new array. A subarray of the new array corresponds to a subarray of the original with all x's removed. So we can think of the sum as original subarray sum minus x times the number of x's inside.

We need to compute for each x, the maximum subarray sum in the array where x is treated as 0 (i.e., we skip x). Actually, if we treat x as 0, then the sum of a subarray in the original that may contain x's becomes the sum of the subarray with x's replaced by 0. That is exactly sum_original - count_x * x. And a subarray in the new array corresponds to a subarray in the original that does not contain any x? No: the new array subarray is formed by taking a contiguous block in the original and removing x's. The resulting sum is the sum of non-x elements. That is exactly the sum of the original subarray with x's replaced by 0. But also, the subarray in the new array is contiguous in the new array, which means in the original, the indices are not necessarily contiguous if there are x's. However, the sum of the new subarray is the sum of the original subarray with x's removed. So if we consider the original subarray from l to r, the sum after removing x is sum_{i=l..r, nums[i]!=x} nums[i] = sum_{i=l..r} nums[i] - count_x * x. So indeed, the new subarray sum is just the original subarray sum minus x times the count of x in that original subarray.

Now, is every subarray in the new array obtained by some l..r in the original? Yes: any contiguous block in the new array corresponds to a set of indices in the original that form a contiguous block in the new array, which means they are a subsequence of the original that is a subarray of the new array. But the original indices are not necessarily a contiguous interval; they are a set of indices where the elements are non-x, and between l and r there may be x's. However, the set of indices in the original is exactly a subset of some interval [L, R] where L is the first index of the new subarray in the original, and R is the last index. The new subarray consists of all non-x elements between L and R. So the sum is sum_{i=L..R, nums[i]!=x} nums[i] = sum_{i=L..R} nums[i] - count_x_in_[L,R] * x. So it's determined by the interval [L,R] in the original. So we can think of choosing an interval [L,R] and a value x, and the resulting sum is the sum of the interval with x's removed.

Thus the problem is: maximize over all intervals [L,R] and values x: (sum_{i=L..R} nums[i] - count_x_in_[L,R] * x). Since x can be any integer, but if x is not in the interval, count_x = 0, so it's just the sum. If x is in the interval, we subtract x for each occurrence.

We can rewrite: For each interval, the sum after removing x is sum - count_x * x. We want to maximize this over x. For a fixed interval, the best x is the one that maximizes count_x * x if x is positive? Actually we subtract count_x * x, so to maximize the sum, we want to subtract as little as possible. If x is negative, subtracting x (i.e., - count_x * x) is actually adding a positive amount (since x negative). So we might want to choose x to be a negative value that appears in the interval, because removing it adds its absolute value times count. Alternatively, if x is positive, removing it reduces the sum. So for a given interval, the best x is the one that minimizes count_x * x (i.e., makes the subtraction as small as possible, possibly negative). But we can also choose x not in the interval, which gives subtraction 0. So the maximum over x of (sum - count_x * x) is sum - min_{x} (count_x * x). Since count_x >= 0, if there is a negative x with count_x > 0, then count_x * x is negative, so subtracting a negative means adding, which is good. So the best x for a given interval is the one that gives the smallest value of count_x * x (i.e., most negative if possible). If all x in the interval are non-negative, then the best is to pick an x not in the interval (so subtraction 0), or pick an x with count_x * x minimal (which could be 0 if some x has count 0). Actually, we can always pick an x not in the interval, giving 0 subtraction. So the maximum for that interval is sum + max_{x in interval} (count_x * |x| if x negative? Wait: we want to maximize sum - count_x * x. Since we can choose x not in the interval, we have at least sum. If there is a negative x, then -count_x * x = + count_x * |x|, which increases the sum. So the best is sum + max_{x in interval, x<0} (count_x * |x|). If there is no negative x, the best is sum (by choosing x not in the interval). So for each interval, the value is sum + (max over negative x in interval of (count_x * |x|)). Equivalently, we can think of the contribution of negative numbers: if we delete a negative value x, we effectively add |x| for each occurrence in the interval.

Thus the problem reduces to: find the maximum over all subarrays of (sum of subarray + bonus), where bonus is the maximum total absolute value we can gain by removing some negative number x that appears in the subarray. Specifically, for a subarray, we can choose to remove a negative value x that appears in the subarray, and then we add |x| for each occurrence of x in the subarray (since originally they were negative, removing them adds their absolute value). Actually careful: originally the subarray sum includes the negative x's. If we remove them, we are left with the sum of positive elements and maybe other negatives. The new sum is original sum - count_x * x. Since x is negative, -count_x * x = + count_x * |x|. So the new sum = original sum + count_x * |x|. So the bonus is count_x * |x| for some negative x present in the subarray. We can choose which negative x to remove to maximize this bonus. So for each subarray, the best bonus is the maximum over negative x in the subarray of (count_x * |x|). Note that if we choose to remove a positive x, we would subtract something, so it's never beneficial unless we are forced? But we are not forced; we can choose to not delete or delete a negative. So the optimal is to either not delete (bonus 0) or delete a negative value present in the subarray to gain count_x * |x|.

Therefore, the answer is: max over all subarrays of (original_subarray_sum + max_{x in subarray, x<0} (count_x_in_subarray * |x|)).

Now, this seems like a complex combinatorial optimization. However, note that we can also think of the operation as: we can add |x| for each occurrence of a chosen negative x in the subarray. This is like we have a "bonus" per occurrence of x.

We need an efficient algorithm. Since n up to 1e5, O(n log n) or O(n) is needed.

Another viewpoint: The problem is equivalent to finding the maximum subarray sum in an array where we can optionally "boost" a chosen negative value by turning it into 0 (or actually, removing it adds its absolute value). But since we remove all occurrences globally, the boost applies to the whole array, not just a subarray. However, the subarray in the new array corresponds to a subarray in the original with some negatives removed. But we can think of the new array as the original array with all x's removed. So the subarray sum in the new array is the sum of the original subarray with x's removed. So it's like we are allowed to choose one value x to "ignore" (treat as 0) globally, and then take the maximum subarray sum of the resulting array (where x's are replaced by 0, but also the array is compressed? Actually, if we replace x with 0, the array still has the same length, but the subarray in the new array is not necessarily a subarray in the modified array because the indices shift. However, as argued, the sum of a subarray in the new array is equal to the sum of a subarray in the original with x's replaced by 0. So we can think of modifying the original array by setting all x to 0, and then taking the maximum subarray sum of that modified array. But careful: in the modified array, a subarray sum includes zeros for x positions. That sum is exactly original sum minus count_x * x. And any subarray in the new array corresponds to some subarray in the modified array? Not exactly, because the modified array still has zeros at x positions, but the subarray in the new array is contiguous after removal, which means in the modified array, it corresponds to a subarray that may have zeros inside, but the zeros are part of the subarray. However, the sum of that subarray in the modified array is the same as the sum of the new subarray. So the maximum subarray sum in the new array is exactly the maximum subarray sum in the array where we set all x to 0. Because any subarray in the new array can be mapped to a subarray in the modified array (the same indices, with zeros replacing x), and vice versa? Let's check: In the new array, elements are only non-x. If we take a subarray in the new array, it corresponds to a set of indices in the original that are non-x and contiguous in the new array. In the modified array (with x replaced by 0), those indices are exactly the same set, and the subarray in the modified array that spans from the first index of the new subarray to the last index will include zeros at x positions in between. The sum of that modified subarray is the sum of non-x elements (since zeros contribute 0). So it's the same as the new subarray sum. Conversely, any subarray in the modified array (with zeros) corresponds to a subarray in the new array? If the modified subarray includes some zeros (i.e., x positions), then in the new array, those positions are removed, so the remaining elements are not contiguous in the new array. However, the modified subarray sum is the sum of non-x elements in that interval. But the new subarray sum for the same interval (ignoring x) is also that sum. However, the new array subarray that gives that sum might be different: the new subarray would be the maximal contiguous block of non-x elements within that interval. But the sum of that block is the same as the sum of all non-x elements in the interval. So the maximum subarray sum in the new array is the maximum over all intervals of the sum of non-x elements in that interval. And that is exactly the maximum subarray sum in the modified array (where x is 0). Because in the modified array, the subarray sum is the sum of the interval, which includes zeros. So the maximum over intervals of (sum of non-x elements) is the same as the maximum over intervals of (sum of interval in modified array). Therefore, the problem reduces to: for each x, compute the maximum subarray sum of the array nums with all occurrences of x replaced by 0. Then take the max over all x and also the original max (which corresponds to x not in array or not deleting).

Thus we can compute for each x: treat x as 0 and run Kadane. But doing this for each unique x individually is O(n * unique) which is O(n^2) in worst case. We need a way to compute for all x efficiently.

We can use a technique similar to "maximum subarray sum with one transformation" or "offline queries". Since we only need the max over x, we can use divide and conquer or segment tree to compute the effect of zeroing out a value.

Alternatively, we can think of the contribution of each x to the answer. We can precompute for each position, the "gain" of setting that position to 0. But the gain depends on which value we choose to zero: if we zero a value v, we set all positions with v to 0. So the gain is the sum of v's (which are negative, so gain is positive) for each occurrence. But also, zeroing a value may break the optimal subarray if the subarray consists solely of that value? Actually, if we zero a value, the subarray might become smaller? No, we are just changing values, not removing elements. But in the new array, elements are removed, so the array is shorter. However, as argued, the sum is equivalent to zeroing in the original array. So we can think of the array with x replaced by 0. Then the maximum subarray sum is computed. This is a classic problem: for each possible x, compute the max subarray sum after setting all x to 0. This can be done in O(n log n) using a segment tree that supports range updates (set to 0) and queries of max subarray sum? But we need to do this for many x, and we want the overall max.

But note: the number of unique x is up to n. We can process each unique x in O(n) if we are careful, but that's O(n^2). We need a faster method.

We can use the following idea: The maximum subarray sum after zeroing x is the maximum over all subarrays of (original subarray sum - count_x * x). We can rewrite this as original subarray sum + |x| * count_x if x is negative, and - x * count_x if x is positive. But we already argued that zeroing a positive x is never beneficial (since it reduces the sum), so the optimal x is either not zeroing or zeroing a negative x. So we only need to consider negative values. But even then, we need to consider all negative x.

Let’s denote the array as a. For each negative value v, define b_i = a_i if a_i != v, else 0. We want max subarray sum of b. This is equivalent to: for each subarray, sum_b = sum_a - count_v_in_subarray * v. Since v is negative, -count_v * v = + count_v * |v|. So sum_b = sum_a + count_v_in_subarray * |v|.

So for a fixed v, the maximum subarray sum in b is: max_{subarray} (sum_a + |v| * count_v_in_subarray). This is like we have an array a, and we can add |v| to each occurrence of v. So we can define an array c where c_i = a_i + |v| if a_i == v, else a_i. Then we want the maximum subarray sum of c. So for each negative v, we are adding a bonus |v| to all positions with value v, and then taking the maximum subarray sum. This is like we have an array of bonuses per value.

We can precompute for each value v (negative), the array c_v, and then the max subarray sum of c_v. But again, too many.

We need a global approach. Perhaps we can use a segment tree that maintains the maximum subarray sum for each possible "bonus" value? Not possible.

Another angle: The answer is the maximum over all subarrays of (original subarray sum + max_{negative v in subarray} (count_v_in_subarray * |v|)). This is like for each subarray, we can choose to add the total absolute value of a chosen negative value v present in the subarray. This is similar to: we have a set of "special" numbers (negatives), and for each subarray, we can pick one special number v that appears in the subarray and add count_v * |v|.

We can think of it as: for each negative v, consider the subarrays that contain at least one v. The best subarray for v is the one that maximizes (sum_a + count_v * |v|). That is equivalent to: for each occurrence of v, we can add |v|. So we can define an array d_v where we add |v| to each v position. Then the max subarray sum of d_v is what we want. So the overall answer is max( original max, max_{v<0} max_subarray_sum(d_v) ).

Now, d_v is just a with added bonuses on v positions. We can precompute the maximum subarray sum of the original array, and also for each v, the max subarray sum of d_v. But again, we need to compute for many v efficiently.

Observation: The array d_v is the same as a except at positions where a_i == v, we have a_i + |v| = v + |v| = 0. Wait, v is negative, so v + |v| = 0. So actually, d_v is exactly the array a with all v replaced by 0. That's consistent with our earlier idea: treat v as 0. So we are back to zeroing.

So we need an efficient way to compute, for many values, the max subarray sum after zeroing them.

We can use a divide and conquer on the value domain? For example, we can use a segment tree over the array indices, and for each value v, we can "deactivate" the positions with value v. But we need to query the max subarray sum after deactivation. This is like we have a set of positions to "disable" (treat as 0), and we want the max subarray sum. If we process all v, we could use a data structure that supports range disable/enable? But we need to do it for all v offline.

Since the number of unique v is up to n, we could process each v in O(log n) or O(1) if we precompute something. But we need to compute the max subarray sum after zeroing all occurrences of v. That is equivalent to: for each v, the max subarray sum of the array where v's are replaced by 0. This can be computed if we can answer queries of the form: given a set of indices to zero (all indices with value v), what is the max subarray sum? We can precompute prefix sums and maybe use a variant of Kadane that skips v.

Alternatively, we can use the following: For each v, we can run Kadane while skipping v. But we can speed this up by noting that the skip only affects when we encounter v. So we can compute for each v, the Kadane result in O(number of occurrences of v) time? Not exactly.

We can use a map from value to a list of indices. For each v, we can iterate over the array, but skip when we see v. This is O(n) per v, total O(n * unique). In worst case, unique is n, so O(n^2). Not good.

We need a subquadratic solution. Perhaps we can use a segment tree that stores for each node, the maximum subarray sum, and also some information that allows us to "remove" a value. If we build a segment tree over the array, we can query the max subarray sum of the whole array. But to zero a value, we would need to update all positions with that value to 0. That could be done with a lazy propagation if we have range updates, but the positions are scattered. So we would need to update each occurrence individually, which is O(k log n) for a value with k occurrences. Summed over all v, total updates = n log n, which is acceptable. Then for each v, we can apply the update, query the max subarray sum, and revert. But we need to do this for all v, and we need to revert the updates to get back to original. We can do this by processing all v offline: for each v, we apply updates to set all its positions to 0, query, then revert. If we do this naively, we apply n updates per query? Actually, each v has some number of occurrences, say c_v. Applying updates to set those positions to 0 takes O(c_v log n). Querying the segment tree takes O(log n). So total time = sum_v (c_v log n + log n) = (n + unique) log n = O(n log n). That is efficient! But we need to be able to revert the updates to restore the original array for the next v. We can either process all v one by one, applying updates, query, then revert (by updating back to original). That would be O(2 * c_v log n) per v, still O(n log n). However, we need to do this for each v sequentially, and the total number of updates across all v is 2 * n (since each position is updated twice: once to 0, once back to original). So total time O(n log n). That is acceptable for n=1e5.

But we need a segment tree that can return the maximum subarray sum of the current array. Standard segment tree can do that: each node stores:
- total sum
- maximum prefix sum
- maximum suffix sum
- maximum subarray sum
We can combine two nodes.

We also need to support point updates (set a value to 0 or back to original). So we can build the segment tree with the original array. Then for each unique value v:
- For each index i in the list of v, update the segment tree at i to 0.
- Query the root's max subarray sum, call it best_v.
- For each index i in the list of v, update the segment tree at i back to the original value.
- Also, we need to consider the case of not deleting (original max). So we compute original_max as the root's max subarray sum before any updates.
- The answer is max(original_max, max_v best_v).

This is O(n log n) time and O(n) space.

But wait: the problem allows deletion of any integer x, not necessarily present in the array? The problem says "Choose any integer x such that nums remains non-empty on removing all occurrences of x." If x is not in the array, removing it does nothing, so it's equivalent to no operation. So we only need to consider x that are in the array (or no operation). So unique x are the distinct values in nums.

Thus the algorithm is:
1. Compute the maximum subarray sum of the original array (Kadane) to handle no operation.
2. Build a segment tree that supports point updates and query of max subarray sum.
3. For each distinct value v in the array:
   a. For each index i where nums[i] == v, update the segment tree to set position i to 0.
   b. Query the root's max subarray sum.
   c. Update the maximum answer with this query.
   d. For each index i where nums[i] == v, update the segment tree to set position i back to original nums[i].
4. Return the answer.

We need to ensure that we don't remove all elements: the condition is that after removing all occurrences of x, the array is non-empty. So we cannot delete a value if it is the only value and the array has only that value? Actually, if the array has only one distinct value, and we delete it, the array becomes empty, which is not allowed. So we should skip such cases. But in our algorithm, if we set all elements to 0, the max subarray sum might be 0 (if all are 0). But the problem says the resulting array must be non-empty, so we should not consider x if removing it would empty the array. That means we should only consider x if there is at least one element with value != x. In other words, if the array has only one distinct value, then no operation is possible (or we can only do no operation). So we should only process v if the count of v is less than n. Our algorithm will naturally give a max subarray sum of 0 if we zero out all elements, but that might be invalid. So we should check: if the count of v equals n, then skipping. For other v, the array will have at least one non-zero (original) element, so the resulting array is non-empty.

But wait: what if the array has both positive and negative values, and we zero out a value that appears only once? That's fine.

So the algorithm is correct.

Complexities: O(n log n) time, O(n) space.

We need to implement the segment tree.

Segment tree node:
- sum: total sum of the segment.
- pref: maximum prefix sum.
- suff: maximum suffix sum.
- best: maximum subarray sum within the segment.

Combine two nodes left and right:
- sum = left.sum + right.sum
- pref = max(left.pref, left.sum + right.pref)
- suff = max(right.suff, right.sum + left.suff)
- best = max(left.best, right.best, left.suff + right.pref)

We need to handle leaves: for a single value x, sum = x, pref = suff = best = x (but careful: for negative x, pref, suff, best are all x, which is correct).

But wait: if we set a value to 0, then the node becomes sum=0, pref=0, suff=0, best=0. That's fine.

We also need to handle the case of all negative numbers: Kadane's best is the maximum (least negative) number. Our segment tree will handle that.

Now, we need to implement the solution in Python.

We need to read n up to 1e5, so O(n log n) is fine.

We also need to consider the possibility that the maximum subarray sum is negative. The problem says we can do at most one operation. If we do no operation, the answer is the max subarray sum of the original. If we delete a value, we might get a larger sum, but if the original max is negative, maybe we can get a better (less negative) sum by deleting some negative? Actually, deleting a negative value removes that negative, so the subarray sum might increase (become less negative). So the answer is the maximum over these.

Our algorithm covers that.

One edge case: if all numbers are negative, the original max subarray sum is the maximum (least negative) number. If we delete that number, the max subarray sum might be the second largest, etc. So we need to consider all v.

Another edge case: if the array is all zeros, original max is 0. Deleting any value (which is 0) would make the array empty? Actually, if all are 0, and we delete 0, the array becomes empty, not allowed. So we can only do no operation, answer 0.

Our algorithm: for v=0, count = n, we skip (or query will give 0, but we should ignore). So we need to explicitly skip v if count_v == n.

Implementation steps:
- Build a dictionary mapping value to list of indices (0-based).
- Build segment tree.
- Compute original max: query the root's best.
- Initialize ans = original max.
- For each value v in the dictionary:
   - if len(indices[v]) == n: continue
   - for i in indices[v]: update(i, 0)
   - ans = max(ans, tree.root.best)
   - for i in indices[v]: update(i, original_nums[i])
- Return ans.

We need to implement update and query efficiently.

Segment tree size: 4*n is fine.

We need to be careful with recursion depth? n=1e5, recursion depth of log n is fine, but building recursively might hit recursion limit if we use recursion for update? Python recursion limit is usually 1000, so we need to use iterative segment tree or increase recursion limit. Better to use iterative segment tree or implement build and update with loops. But we can use recursion with sys.setrecursionlimit(1e6).

I'll implement a recursive segment tree.

Let's write the code.

We'll define a Node class or use tuples. Since we need to combine, using a simple class with attributes is fine.

We'll build an array of nodes.

Alternatively, we can implement a segment tree using arrays for sum, pref, suff, best.

I'll use a class Node with __init__ and a method to combine.

For efficiency, we can use a list of Node objects.

Implementation:

```python
class Node:
    __slots__ = ('sum', 'pref', 'suff', 'best')
    def __init__(self, sum=0, pref=0, suff=0, best=0):
        self.sum = sum
        self.pref = pref
        self.suff = suff
        self.best = best
    @staticmethod
    def combine(left, right):
        res = Node()
        res.sum = left.sum + right.sum
        res.pref = max(left.pref, left.sum + right.pref)
        res.suff = max(right.suff, right.sum + left.suff)
        res.best = max(left.best, right.best, left.suff + right.pref)
        return res
```

Then segment tree:

```python
class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.data = [Node() for _ in range(2 * self.size)]
        # Build leaves
        for i in range(self.n):
            self.data[self.size + i] = Node(arr[i], arr[i], arr[i], arr[i])
        for i in range(self.size - 1, 0, -1):
            self.data[i] = Node.combine(self.data[2*i], self.data[2*i+1])
    def update(self, idx, value):
        i = self.size + idx
        self.data[i] = Node(value, value, value, value)
        i //= 2
        while i:
            self.data[i] = Node.combine(self.data[2*i], self.data[2*i+1])
            i //= 2
    def query(self):
        return self.data[1].best
```

This is an iterative segment tree.

Now, the main solution:

```python
class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0  # though constraints say n>=1
        # Build segment tree
        seg = SegTree(nums)
        original_best = seg.query()
        ans = original_best
        # Build map from value to indices
        val_to_indices = {}
        for i, v in enumerate(nums):
            val_to_indices.setdefault(v, []).append(i)
        # For each unique value
        for v, indices in val_to_indices.items():
            if len(indices) == n:
                # Removing this would empty the array
                continue
            # Set to 0
            for i in indices:
                seg.update(i, 0)
            current_best = seg.query()
            if current_best > ans:
                ans = current_best
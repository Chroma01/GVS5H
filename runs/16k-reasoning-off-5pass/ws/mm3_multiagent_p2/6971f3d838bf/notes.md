
## ideation
The problem asks for the maximum subarray sum after optionally removing all occurrences of a single value `x` (or doing nothing). The resulting array is the original array with all elements equal to `x` deleted, which concatenates the remaining contiguous segments of non-`x` elements. The answer is the maximum over all choices of `x` (including no operation) of the maximum subarray sum of the concatenated segments.

Core difficulty: Efficiently compute, for every distinct value `x`, the maximum subarray sum of the array formed by removing all `x`. A naive approach runs Kadane for each `x` (O(n) per `x`), giving O(n²) in the worst case.

Key observation: For a fixed `x`, the resulting array is the concatenation of segments between occurrences of `x`. The maximum subarray sum of this concatenated array can be computed from the original array's prefix and suffix Kadane arrays. Specifically, if we precompute `pref[i]` = maximum subarray sum ending at `i` and `suf[i]` = maximum subarray sum starting at `i` for the original array, then for a segment `[L, R]` of non-`x` elements, the best subarray entirely inside it is `max_{i in [L,R]} suf[i]`. However, subarrays can also span multiple segments after concatenation. To handle this, we can consider the original array with `x` replaced by 0: the maximum subarray sum of that modified array equals the maximum subarray sum of the concatenated segments, except that a solitary 0 (from a removed `x`) might give a sum of 0 even if the concatenated array's max is negative. Since the concatenated array is non-empty, its max subarray sum is at least its maximum element. Thus, the answer for `x` is `max(0, max_subarray_sum_with_x_replaced_by_0)`? Actually, the max subarray sum of the concatenated array is exactly the max subarray sum of the array with `x` set to 0, because any subarray in the concatenated array corresponds to an interval in the original array, and its sum is the sum of non-`x` elements in that interval, which is the same as the sum of the modified array over that interval. The only difference is that the modified array may have a subarray consisting solely of a single 0 (from `x`), giving sum 0, whereas the concatenated array has no such element. But if the concatenated array's max is negative, the modified array's max is at least 0. However, the problem asks for the max subarray sum of the resulting (concatenated) array, which can be negative. But we are maximizing over all `x` and the original array, so we can just compute the max subarray sum of the modified array and take the maximum over all `x`, but we must be careful: the original array's max subarray sum is also needed. Actually, the original array corresponds to not removing any value, which is equivalent to removing a value that doesn't exist? No. We can just compute the max subarray sum of the original array and also the max subarray sum for each `x` when `x` is set to 0, and take the overall maximum. But wait, is the max subarray sum of the concatenated array exactly the max subarray sum of the array with `x` set to 0? Let's verify with an example: nums = [-1, -2]. Original max = -1. Remove -2: concatenated = [-1], max = -1. Modified (-2 -> 0) = [-1, 0], max = 0. They differ. So they are not the same. The modified array gives 0, but the concatenated array gives -1. However, we are allowed to remove -2, and the result is -1. We are not forced to take 0. So the answer for removing -2 is -1. The modified array's max is 0, which is higher, but that corresponds to a subarray that doesn't exist in the concatenated array. So we cannot simply use the modified array.

Thus, we need the true max subarray sum of the concatenated array. How to compute it efficiently? The concatenated array is the original array with `x` deleted. This is equivalent to taking the original array and replacing `x` with a very large negative number? No.

Another approach: For each `x`, the concatenated array is the original array with `x` removed. The max subarray sum of this array is the maximum sum of a contiguous subsequence of the non-`x` elements. This can be computed by considering the original array and treating `x` as a "break" that resets the current subarray sum? Not exactly, because subarrays can span across `x` after removal.

Wait, in the concatenated array, the segments are joined. So a subarray can start in one segment and end in another. The sum is the sum of the suffix of the first segment plus the sum of the prefix of the second segment, plus any full segments in between. This is equivalent to the maximum subarray sum of the original array where we treat `x` as 0? Let's test with [-1, -2]. Remove -2: segments: [-1]. Max subarray sum = -1. If we treat -2 as 0, array = [-1, 0]. Max subarray sum = 0. Not equal. Why? Because in the concatenated array, the subarray cannot be just the 0. In the modified array, the subarray [0] (the second element) has sum 0. But in the concatenated array, that element doesn't exist. So the modified array allows a subarray consisting solely of the removed element, which is not present in the concatenated array. So the max subarray sum of the concatenated array is the max subarray sum of the modified array, unless the maximum is achieved by a subarray that includes only removed `x`'s. But if we include only removed `x`'s, the sum is 0 (since we set them to 0). So the concatenated array's max is at most the modified array's max. If the modified array's max is > 0, it must include at least one non-`x` element (since sum of zeros is 0). So that subarray exists in the concatenated array. If the modified array's max is 0, it could be achieved by a subarray of all zeros (removed `x`'s). In that case, the concatenated array's max might be negative. But if the concatenated array's max is negative, the modified array's max is at least 0. So the true max for removing `x` is the max subarray sum of the modified array, except when the modified array's max is 0 and the concatenated array's max is negative. But in that case, the answer is negative, which is less than 0. So if we take the max over all `x`, we might incorrectly take 0 from a modified array when the true answer is negative. However, we are looking for the maximum possible sum. If there is any `x` that gives a positive sum in the modified array, that `x` will also give that positive sum in the concatenated array (since the subarray doesn't consist only of removed `x`'s). So the only case where the modified array's max is higher than the concatenated array's max is when the modified array's max is 0 and the concatenated array's max is negative. But 0 is never less than a negative number. So if we take the max over all `x` of the modified array's max, we might get 0 when the true best is negative. But we can just compare with the original array's max, which could be negative. Actually, the original array's max is the same as the modified array's max for any `x` that is not in the optimal subarray? Not exactly.

Let's think: We want max over all possible resulting arrays. The resulting array is either the original array, or the original array with some `x` removed. For a given `x`, the max subarray sum of the resulting array is some value S_x. We want max(S_original, max_x S_x). We need to compute S_x correctly.

We can compute S_x by noting that the resulting array is the original array with `x` removed. The max subarray sum of an array with an element removed is a known problem: "Maximum subarray sum after removing one element" (but here we remove all occurrences of a value). For a single removal, there is an O(n) solution using pref and suf. For removing all occurrences of a value, we can reduce it to: we have the original array, and we want the max subarray sum of the array with all positions of `x` removed. This is equivalent to: we have an array, and we delete certain positions. The max subarray sum of the resulting array is the maximum sum of a contiguous subsequence of the remaining elements.

We can compute this by scanning the original array and maintaining the current subarray sum, but resetting when we hit `x`? No, because after removal, the subarray can continue across the gap. So we need to treat `x` as a "join" point. Actually, we can think of the original array as a sequence. When we remove `x`, we are effectively taking the original array and for each `x`, we remove that element. The max subarray sum of the new array is the maximum sum of a contiguous block of non-`x` elements. Wait, is that true? In the new array, the elements are exactly the non-`x` elements in their original order. A subarray in the new array is a contiguous block of these elements. This corresponds to a set of original indices that are consecutive in the non-`x` list. As argued, this corresponds to an interval [l, r] in the original array. The sum is the sum of non-`x` elements in [l, r]. This is not simply a contiguous block of non-`x` elements in the original array, because a contiguous block of non-`x` elements in the original array would be a set of indices with no `x` between them and no other elements between them. But an interval [l, r] can contain `x`'s. So it's not a contiguous block of non-`x` elements; it's an interval in the original array.

But we can compute the sum of non-`x` elements in [l, r] as the sum of all elements in [l, r] minus the sum of `x`'s in [l, r]. So S_x = max_{l,r} (sum(l,r) - count_x(l,r) * x). This is a range query problem. Since x is constant, this is equivalent to max_{l,r} (sum(l,r) - x * count_x(l,r)). We can compute this for all x using a sweep line or segment tree.

However, there is a simpler O(n log n) solution: For each x, we can compute the max subarray sum of the array with x removed by using the original pref and suf arrays, but we need to account for the fact that the array is compressed. The compressed array is the original array with x's removed. The max subarray sum of the compressed array is the maximum subarray sum of the original array where we treat x as a "break" that allows us to start a new subarray? No.

Let's look at the structure: The compressed array is formed by concatenating the segments. So it is exactly the original array with x's removed. We can compute its max subarray sum by running Kadane on the compressed array. But we can do this efficiently by precomputing for each position the maximum subarray sum of the prefix ending at i, and suffix starting at i, for the compressed array. But the compressed array depends on x.

Idea: For each x, the compressed array is the original array with x's removed. The max subarray sum of this array is the maximum over all i of (max subarray sum ending at i in compressed array). The max subarray sum ending at i in compressed array can be computed from the original pref and suf, but we need to handle the gaps. Actually, we can compute the max subarray sum of the compressed array by taking the original array and for each x, we want the max subarray sum of the array after deleting x. This is a known problem: "Maximum subarray sum after removing all occurrences of a value". I recall a solution that uses the positions of the value and computes the max subarray sum of the segments and the max sum of a subarray that spans across the removed value. But since we remove all occurrences, the compressed array is the concatenation. The max subarray sum of the concatenation is the max over all subarrays of the concatenation. This can be computed as the max of:
- Max subarray sum within each segment.
- Max subarray sum that starts in one segment and ends in another, which is the max suffix sum of some segment plus the max prefix sum of a later segment, plus the sums of all segments in between.
This is essentially the max subarray sum of the sequence of segment sums? Not exactly, because a subarray can start in the middle of a segment and end in the middle of another segment.

But we can precompute for the original array the prefix max subarray sum and suffix max subarray sum. Then for a given x, the compressed array's max subarray sum is the maximum over all intervals between x's of the max subarray sum that can be formed by taking a suffix of the left segment and a prefix of the right segment, and also possibly including full segments in between. However, since the segments are concatenated, the best subarray that spans across multiple segments is simply the max subarray sum of the concatenation, which can be found by considering the whole compressed array as a new array.

We can compute the max subarray sum for each x by using the following: Let the positions of x be p1,...,pk. The compressed array is the original array with these positions removed. We can compute the max subarray sum of this compressed array by using a data structure that supports range maximum query on pref and suf. Specifically, the max subarray sum of the compressed array is the maximum over all i of (max subarray sum ending at i in compressed array). For a position i that is not x, the max subarray sum ending at i in compressed array is either nums[i] (if i is the first element of the compressed array or the previous element is x) or (max subarray sum ending at previous non-x element) + nums[i]. So we can compute this by scanning the original array and keeping track of the current max subarray sum for the compressed array. But we need to do this for each x.

However, we can precompute for each position i the max subarray sum ending at i (pref[i]) and starting at i (suf[i]) for the original array. For a fixed x, the compressed array is the original array with x removed. The max subarray sum ending at a non-x element i in the compressed array is: if the previous non-x element is j, then it's suf[j]? No.

Wait, the max subarray sum ending at i in the compressed array is the maximum sum of a subarray that ends at i and contains only non-x elements. This is exactly the maximum sum of a subarray in the original array that ends at i, does not contain any x, and has no x between the start and i. But since x is removed, the subarray can skip over x's. So it is the maximum sum of a subsequence of the original array that ends at i, consists of non-x elements, and the elements are consecutive in the non-x list. This is equivalent to: we take the original array, and we want the max sum of a subarray that does not contain x, but we allow the subarray to "jump" over x's? No, because in the compressed array, there is no x. So the subarray is just a contiguous block of non-x elements. This corresponds to a set of original indices that are consecutive in the non-x list. This is exactly a subarray of the original array that does not contain any x, but it can have gaps? No, if it has gaps, those gaps must be x's, because the indices are consecutive in the non-x list. So the original indices are i, i+1, ..., j? Not necessarily. They could be i, i+2, i+5, etc., as long as there are no non-x elements in between. That means the original indices form a contiguous block in the original array if we remove all x's? They are exactly a contiguous block of the non-x elements. In the original array, they are not necessarily contiguous because there are x's between them. But the condition is that there are no non-x elements between them. So the set of indices is such that for any two consecutive indices a < b in the set, there is no non-x element in (a, b). This means that all elements in (a, b) are x. So the set of indices is a union of intervals separated by x's? Actually, if there is no non-x element between a and b, then all elements between a and b are x. So the subarray in the compressed array corresponds to a set of original indices that are isolated by x's. That is, it's a collection of non-x elements that are separated by x's. But in the compressed array, they are adjacent. So the subarray in the compressed array can include multiple non-x elements that are separated by x's in the original array. So the sum is the sum of those non-x elements.

Now, consider the original array. We can think of it as having x's as "deletable". The max subarray sum after deletion is the max sum of a set of non-x elements that are consecutive in the non-x list. This is equivalent to: we have an array where we can choose any contiguous block of the non-x list. This is the same as: we have the original array, and we want to choose a subarray of the original array that may contain x's, but the x's are deleted, so we only sum the non-x elements. So the sum is sum of all elements in the chosen interval minus x times the number of x's in the interval.

So S_x = max_{l <= r} (sum(l,r) - x * count_x(l,r)).

We can compute this for all x efficiently. Note that sum(l,r) - x * count_x(l,r) = (prefix[r+1] - prefix[l]) - x * (count_x(r) - count_x(l-1)). Let A[i] = prefix[i] - x * count_x(i). Then the expression is A[r+1] - A[l]. So S_x is the maximum subarray sum of the array A (of length n+1) where A[i] = prefix[i] - x * count_x(i-1)? Let's define carefully.

Let prefix sum P[0] = 0, P[i] = sum_{j=0}^{i-1} nums[j].
Let C[i] = number of x's in nums[0..i-1].
Then sum(l,r) = P[r+1] - P[l].
Count_x(l,r) = C[r+1] - C[l].
So sum - x*count = (P[r+1] - x*C[r+1]) - (P[l] - x*C[l]).
Let A[i] = P[i] - x*C[i]. Then the value for interval [l, r] is A[r+1] - A[l].
So S_x is the maximum subarray sum of the array A[0..n] (where A has length n+1).
But A depends on x. So for each x, we need the maximum subarray sum of A_x, where A_x[i] = P[i] - x*C_x[i], and C_x[i] is the count of x in the first i elements.

This is interesting: for each x, we have an array A_x of length n+1, and we want its maximum subarray sum. We can precompute P for all i. C_x depends on x.

We want max_{x} max_subarray(A_x) and also the original max subarray sum (which is max_{l,r} P[r+1]-P[l]).

We can compute the original max subarray sum in O(n) using Kadane.

Now, for each x, A_x[i] = P[i] - x * C_x[i]. Note that C_x[i] is non-decreasing, and increases by 1 at each position where nums[j] == x.

We can think of A_x as a linear function of x: A_x[i] = P[i] - x * C_x[i]. For a fixed i, as x varies, A_x[i] is a line with slope -C_x[i]. The maximum subarray sum of A_x is the maximum difference A_x[j] - A_x[i] for j > i.

This looks like we can use the fact that the number of distinct x is at most 1e5, and n is 1e5. We can process each x in O(n) time? That would be O(n^2) worst case.

We need a better approach. Note that the maximum subarray sum of A_x is the maximum over all intervals of (P[r+1] - P[l]) - x*(C_x[r+1] - C_x[l]). This is the same as the original problem but with the array modified? Actually, it's exactly the same as the original problem: we have an array, and we want to find a subarray, and we subtract x times the count of x in the subarray. This is like having a weight for each position: if the position is x, we subtract x. So the value of a subarray is sum of (nums[i] - (x if nums[i]==x else 0)). But that's just sum of non-x elements. So A_x is just the prefix array of the modified array (with x set to 0) but with an extra 0 at the beginning? Actually, if we set x to 0, the prefix sum of the modified array is P[i] - x*C_x[i]. So A_x[i] is exactly the prefix sum of the array where x is replaced by 0. And the maximum subarray sum of the modified array is the maximum subarray sum of A_x (since max subarray sum of an array is max difference of its prefix sums). So we are back to: S_x is the maximum subarray sum of the array with x set to 0, but with the caveat that the modified array's max subarray sum is not exactly S_x? Wait, earlier we saw that for [-1, -2] and x=-2, the modified array is [-1, 0], its max subarray sum is 0. But the compressed array (removing -2) is [-1], max subarray sum is -1. So S_x = max subarray sum of compressed array, which is not the max subarray sum of the modified array. The max subarray sum of the modified array is max(0, S_x) because the modified array has zeros that can be chosen. So S_x = max_subarray(modified_array) if that is > 0, else S_x = max_subarray(modified_array) except that we cannot choose a subarray of all zeros. But if max_subarray(modified_array) <= 0, then the maximum is either 0 (if there is a zero) or negative. But the compressed array has no zero element (unless there was a zero in the original array that is not x). So we need to be careful.

Actually, the max subarray sum of the modified array is max(0, max_subarray(compressed_array))? Let's test: modified = [-1,0], max subarray = 0. compressed = [-1], max = -1. So max(0, -1) = 0, not -1. So S_x = max_subarray(modified) if max_subarray(modified) != 0 or if there is a non-zero element? Not exactly.

If the compressed array has max subarray sum S. The modified array has the same elements plus zeros in place of x. So any subarray in the compressed array corresponds to the same sum in the modified array (by taking the same indices, which are not x). So the modified array's max is at least S. Additionally, the modified array can have subarrays that include zeros. The sum of a subarray that includes zeros is the sum of the non-x elements in that interval. This is the same as the sum of a subarray in the compressed array that corresponds to that interval. Actually, any interval [l,r] in the modified array corresponds to an interval in the compressed array if there is at least one non-x element. If the interval consists only of x's, then in the modified array it sums to 0, but in the compressed array it doesn't exist. So the modified array's max is max(S, 0) if there is an interval of all x's. But if there is no interval of all x's (e.g., x's are separated), then any interval containing x's also contains non-x elements, so its sum is the same as the sum of that interval in the compressed array. So the modified array's max is exactly max(S, max sum of an interval consisting only of x's). The sum of an interval of only x's is 0 (since each x is replaced by 0). So the modified array's max is max(S, 0). Therefore, S = max_subarray(modified) if max_subarray(modified) != 0, or if max_subarray(modified) = 0, S could be negative. But if max_subarray(modified) = 0, it means the maximum sum is 0. This could be achieved by a subarray of only x's (sum 0) or by a subarray with sum 0. If there is a subarray with sum 0 that includes non-x elements, then S is at least 0? Actually, S is the max subarray sum of the compressed array. If the compressed array has a subarray with sum 0, then S >= 0. But S could be negative if all subarrays have negative sum. In that case, max_subarray(modified) = 0 (by taking an x). So S = max_subarray(modified) only when max_subarray(modified) > 0. If max_subarray(modified) = 0, S could be negative. But we are looking for the maximum over all x. If for some x, S_x is negative, but max_subarray(modified) = 0, then we might incorrectly take 0. However, we are taking the maximum over all x. If there is any x that gives a positive S, that will be the answer. If all S_x are negative, then the original array's max subarray sum (which is also a candidate) might be negative. So we need to correctly compute S_x for all x, especially when it's negative.

But wait, the problem allows doing nothing. So the original array's max subarray sum is a candidate. That is S_original = max_subarray(original). For x, S_x is the max subarray sum after removing x. We want max(S_original, max_x S_x). We can compute S_original easily. For each x, we need S_x. If we compute max_subarray(modified) for each x, and then take the max of that and S_original, we might overestimate if for some x, max_subarray(modified) = 0 but S_x < 0. But is it possible that max_subarray(modified) = 0 and S_x < 0, and this x gives the maximum? Only if all other candidates are <= 0 and S_x is the maximum. But if S_x < 0, then max_subarray(modified) = 0, and S_original is probably negative or less than 0. For example, nums = [-1, -2]. S_original = -1. For x = -2, modified = [-1, 0], max = 0. S_x = -1. So max over all is -1. If we took max_subarray(modified), we would get 0, which is incorrect because we cannot achieve 0 by removing -2 (the result is [-1], max -1). So we cannot simply use max_subarray(modified).

Thus, we need the true S_x. How to compute S_x efficiently?

S_x is the max subarray sum of the compressed array. The compressed array is the original array with x removed. This is equivalent to: we have the original array, and we want the max subarray sum of the array after deleting all x. This is a classic problem that can be solved in O(n log n) or O(n) using the positions of x.

Let the positions of x be p1, p2, ..., pk. The compressed array is the concatenation of segments:
seg0 = nums[0..p1-1]
seg1 = nums[p1+1..p2-1]
...
segk = nums[pk+1..n-1]

We need the max subarray sum of the concatenation of these segments. This is the max subarray sum of an array that is the concatenation of these k+1 segments. This can be computed by running Kadane on the concatenation. But we can compute it using the prefix and suffix max subarray sums of the original array.

For each segment, we can compute its max subarray sum, its max prefix sum, and its max suffix sum. Then the max subarray sum of the concatenation is the maximum of:
- The max subarray sum of each segment.
- The max suffix sum of some segment plus the max prefix sum of a later segment, plus the sums of all segments in between.
This is essentially the max subarray sum of the sequence of segments. We can precompute for the original array the prefix max subarray sum and suffix max subarray sum. But we need to extract these for each segment.

We can precompute for the original array:
- pref[i] = max subarray sum ending at i.
- suf[i] = max subarray sum starting at i.
- Also, the total sum of a segment can be computed with prefix sums.

For a segment [L, R], its max subarray sum is max_{i in [L,R]} suf[i] (or pref[i]). Its max prefix sum is max_{i in [L,R]} (sum(L, i)). Its max suffix sum is max_{i in [L,R]} (sum(i, R)).

But we need the max subarray sum of the concatenation. This is not simply the max of these; it can be a combination.

We can compute the max subarray sum of the concatenation by considering the whole compressed array. Since the compressed array is just the original array with x's removed, we can compute its max subarray sum by scanning the original array and maintaining the current max subarray sum for the compressed array. Let cur be the max subarray sum ending at the current non-x element in the compressed array. When we encounter a non-x element a, the new cur = max(a, cur + a) if the previous element in the compressed array is not x? Wait, in the compressed array, the previous element is the last non-x element before a. So we can scan the original array, and when we see a non-x element, we update cur = max(a, cur + a) where cur is the max subarray sum ending at the previous non-x element. But this depends on x: for a given x, we need to do this scan ignoring x. That would be O(n) per x.

But we can precompute for each position the max subarray sum ending at it for the compressed array of any x? No.

Alternative: We can compute the max subarray sum of the compressed array for each x by using the original pref and suf, but we need to combine them across the gaps. Actually, the compressed array is formed by taking the original array and removing x. The max subarray sum of the compressed array is the maximum sum of a subarray that does not contain x, but the subarray can span across x's. This is exactly the maximum sum of a subarray of the original array where we treat x as 0, but with the additional constraint that the subarray cannot be empty? No.

Wait, we can think of the original array as having weights. We want the max subarray sum of the array after removing x. This is equivalent to: we have an array, and we can choose any subarray, but we must "pay" x for each occurrence of x in the subarray. So the value of a subarray is sum - x*count_x. We want to maximize this over all subarrays. This is exactly the maximum subarray sum of the array A_x where A_x[i] = nums[i] - x if nums[i]==x else nums[i]. But that's the same as the modified array with x set to 0? No: if nums[i]==x, then A_x[i] = x - x = 0. If nums[i]!=x, A_x[i] = nums[i]. So A_x is exactly the modified array (x replaced by 0). Then the maximum subarray sum of A_x is the maximum sum of a subarray of A_x. But as we saw, this is not S_x; it's max(S_x, 0) if there is an all-x subarray. Actually, A_x is the array with x set to 0. The max subarray sum of A_x is exactly the max subarray sum of the modified array. So we are back to: max_subarray(A_x) = max(S_x, 0) if there is an interval of all x's? Not exactly: if there is an interval of all x's, its sum in A_x is 0, so max_subarray(A_x) >= 0. But S_x is the max subarray sum of the compressed array, which is the same as the max subarray sum of A_x restricted to subarrays that contain at least one non-x element. So S_x = max_subarray(A_x) if max_subarray(A_x) is achieved by a subarray with at least one non-x element. If max_subarray(A_x) is 0 and achieved only by all-x subarrays, then S_x < 0 (or S_x could be 0 if there is a non-x element 0, but that's a different zero). Actually, if the compressed array has a 0, then S_x >= 0. So the only problematic case is when max_subarray(A_x) = 0 and the compressed array has no subarray with sum 0. That means the compressed array's max is negative. In that case, S_x is negative, but max_subarray(A_x) = 0. So if we compute max_subarray(A_x) for all x, and take the max over x, we might get 0 when the true answer is negative. But is 0 ever the answer? Yes, if there is a subarray with sum 0. For example, if the original array has a 0, then not removing anything gives max subarray sum at least 0. If the original array has no positive sum, the max could be 0. So 0 can be the answer. But we need to ensure that if the answer is negative, we don't return 0. In the example [-1, -2], the answer is -1 (from original or removing -2). If we take max over max_subarray(A_x), we get max( -1 (original), 0 (for x=-2), 0 (for x=-1) ) = 0. That would be wrong. So we cannot use max_subarray(A_x) directly.

We need the true S_x. How to compute S_x? S_x is the max subarray sum of the compressed array. This is the max subarray sum of the original array with x removed. This is a known problem: "Maximum subarray sum after removing all occurrences of a value". I think the solution is to precompute prefix and suffix max subarray sums, and for each x, the answer is the maximum over all gaps between x's of the max suffix sum of the left segment plus the max prefix sum of the right segment, and also the max subarray sum within each segment. But that is for when the subarray cannot span across the removed value? Wait, if we remove x, the segments are concatenated. So a subarray can span across the boundary between two segments. The sum of such a subarray is the max suffix sum of the left segment plus the max prefix sum of the right segment. But what about spanning across multiple segments? The sum would be the sum of the suffixes and prefixes plus the sums of the full segments in between. However, the concatenation is just the segments joined. The max subarray sum of the concatenation is the max over all subarrays of the concatenation. This is exactly the max subarray sum of the array formed by the segments. We can compute this by treating each segment as a "super element" with a value (its total sum) and also the ability to take subsegments. Actually, the max subarray sum of the concatenation is the max over all intervals of segments. For a given interval of segments [i, j], the max subarray sum that starts in segment i and ends in segment j is (max suffix sum of segment i) + (sum of segments i+1 to j-1) + (max prefix sum of segment j). This is a standard range query problem.

We can precompute for the original array:
- prefix sum P.
- pref[i] = max subarray sum ending at i.
- suf[i] = max subarray sum starting at i.

For a segment [L, R], we need:
- total sum = P[R+1] - P[L].
- max prefix sum = max_{k in [L,R]} (P[k+1] - P[L]) = -P[L] + max_{k in [L,R]} P[k+1].
- max suffix sum = max_{k in [L,R]} (P[R+1] - P[k]) = P[R+1] - min_{k in [L,R]} P[k].
- max subarray sum = max_{k in [L,R]} (P[k+1] - min_{j in [L,k]} P[j]) = max_{k in [L,R]} (max_{j in [L,k]} P[k+1] - P[j]).

But we can also get max subarray sum from suf: max_{i in [L,R]} suf[i].

So if we have a data structure that can answer range max of suf, range min of prefix sum, etc., we can compute the max subarray sum of any interval of segments.

However, the number of segments for a given x is k+1, where k is the number of occurrences of x. The total number of segments over all x is sum (k+1) = n + distinct. So if we can compute the max subarray sum of the concatenation for each x in O(k log n) or O(k) time, total O(n log n) or O(n).

How to compute the max subarray sum of the concatenation of segments efficiently? We can compute it by running Kadane on the concatenation. But we can do it by scanning the segments and keeping the current max subarray sum. For a given x, we have segments S0, S1, ..., Sk. We need the max subarray sum of the array formed by concatenating them. This is equivalent to: we have an array of "chunks". The max subarray sum is the maximum over i <= j of (max suffix of Si) + (sum of Si+1...Sj-1) + (max prefix of Sj), and also within each Si.

We can precompute for the original array the following:
- For any interval [L, R], we can get its total sum, max prefix sum, max suffix sum, max subarray sum.

Then for a given x, we have a list of segments. We want to find the maximum over all pairs (i, j) with i <= j of:
- If i == j: max subarray sum of segment i.
- If i < j: max suffix of segment i + total sum of segments i+1 to j-1 + max prefix of segment j.

This is like the max subarray sum of an array where each segment is a "super element" with a value (its total sum) and we can also take subsegments. Actually, we can think of the concatenation as an array. We can compute its max subarray sum by a sweep: start with cur = 0, ans = -inf. For each segment, we consider its max prefix sum, total sum, max suffix sum, max subarray sum. But we need to allow the subarray to start in the middle of a segment and end in the middle of another. This is exactly the max subarray sum of the whole concatenation. We can compute it by iterating through the segments in order, and for each segment, we update the current max subarray sum ending at the end of the segment. But the current max subarray sum ending at the end of a segment is either within the segment, or it spans from the previous segments into this segment. Specifically, let cur be the max subarray sum ending at the previous segment's end. Then for the current segment, the max subarray sum ending at its end is max( max_subarray(segment), max_suffix(segment) + cur, max_prefix(segment) + cur? No.

Actually, the standard way to compute max subarray sum of an array is to scan and keep cur = max(0, cur + a[i]). Here, the array is the concatenation. We can simulate this by processing each segment and using its internal structure. For each segment, we can compute the max subarray sum that starts at the beginning of the segment and ends anywhere in it, and the max suffix sum. Then we can combine.

But we can do this more simply: The max subarray sum of the concatenation is the maximum subarray sum of the original array with x treated as 0, but with the modification that we cannot take a subarray that consists only of x's. However, if the max subarray sum of the modified array is 0, and it's achieved only by all-x subarrays, then the true max is negative. But in that case, the true max is the maximum subarray sum of the compressed array, which is the maximum subarray sum of the modified array restricted to subarrays that include at least one non-x element. This is exactly the maximum subarray sum of the modified array, unless the modified array's max is 0 and there is no subarray with sum > 0 that includes a non-x element. In that case, the true max is the maximum subarray sum of the modified array that includes a non-x element, which could be negative or 0. If there is a non-x element with value 0, then that gives 0. So the true max is max(0, max subarray sum of modified array that includes non-x) but if the max including non-x is negative, then the true max could be 0 only if there is a non-x 0. If no non-x 0, then the true max is that negative value.

But this is getting too complicated. Let's look for a known solution. This problem is from LeetCode: "Maximum Subarray Sum After One Operation" is different. This one is "Maximum Subarray Sum After Deleting All Occurrences of a Value" or similar. I think it's LeetCode 1186? No.

Wait, I recall a problem: "Maximum Subarray Sum After Deleting One Element" is LeetCode 1186. Here we delete all occurrences of a value. This is LeetCode 1186? No, 1186 is "Maximum Subarray Sum After One Deletion". That's deleting one element. Here we delete all occurrences of a chosen value, which is like deleting a set of elements. But we can choose which value. So it's like: we can delete all elements equal to some value x. This is equivalent to: we can choose a value x and remove all its occurrences. The answer is the max subarray sum after that.

I think there is a solution using prefix and suffix maximum subarray sums, and for each x, we consider the gaps. Specifically, for a fixed x, the array is split into segments. The max subarray sum of the concatenated array is the max of:
- The max subarray sum of each segment.
- The max sum of a subarray that starts in one segment and ends in another. This is the max over i < j of (max suffix of segment i) + (sum of segments i+1..j-1) + (max prefix of segment j).

We can precompute for the original array the prefix and suffix max subarray sums, and also the prefix sums. Then for a given x, we can compute the max over all pairs of segments. Since the number of segments is O(occurrences(x)), we can do this in O(occurrences(x)) time if we can query the max suffix of a segment, max prefix of a segment, and sum of consecutive segments quickly. This can be done with sparse tables or segment trees.

But we can do even better: For each x, the answer is the maximum subarray sum of the array after removing x. This is exactly the maximum subarray sum of the array where we replace x with a very negative number? No.

Another idea: The answer is the maximum over all subarrays of the original array of (sum of subarray - x * count_x in subarray) for some x. We can choose x to maximize this. For a fixed subarray [l, r], the value is sum(l,r) - x * count_x(l,r). We want to choose x to maximize this. If count_x(l,r) > 0, we can choose x to be any value present in the subarray. The maximum over x present in the subarray of (sum - x*count) is sum - min_x_in_subarray * count? Not exactly, because x must be the value we remove. We can only remove one value. So for a given subarray, if we remove a value x that appears in it, the sum becomes sum - x * count_x. We want to maximize this over all x present in the subarray. This is equivalent to: sum - max_{x in subarray} (x * count_x). But we can also remove a value not in the subarray, which doesn't change the sum. So the maximum over all operations is max over all subarrays of (sum(l,r) - max_{x in nums} (x * count_x(l,r) if x in subarray else 0)). Actually, we can choose any x, and the resulting subarray sum is sum(l,r) if x not in subarray, or sum(l,r) - x*count_x(l,r) if x in subarray. So for a fixed subarray, the best x is the one that maximizes the resulting sum. If we choose x not in the subarray, we get sum(l,r). If we choose x in the subarray, we get sum(l,r) - x*count_x. Since x can be positive or negative, the best is to choose x that minimizes x*count_x. Since count_x > 0, this is min_{x in subarray} x * count_x. So the best we can do for a subarray is sum(l,r) - min_{x in subarray} (x * count_x). But we can also choose x not in the subarray and get sum(l,r). So the best is max( sum(l,r), sum(l,r) - min_{x in subarray} (x * count_x) ) = sum(l,r) - min(0, min_{x in subarray} (x * count_x)). This is equivalent to sum(l,r) - min(0, min_{x in subarray} (x * count_x)). Since min(0, something) is 0 if the something is positive, or the something if negative. So we subtract the negative part: if there is a negative x in the subarray, we can remove it and increase the sum. If all x in the subarray are positive, removing any of them would decrease the sum, so we don't remove any.

Therefore, the problem reduces to: for each subarray, compute its sum, and also the minimum value of x * count_x over x in the subarray (or 0). Then the value for that subarray is sum - min(0, min_{x in subarray} (x * count_x)). We want the maximum over all subarrays.

But this is still complex.

Given the time, I think the intended solution is to precompute prefix and suffix max subarray sums, and for each x, compute the answer by scanning the gaps. Since n=1e5, we can do O(n log n) with a segment tree.

Let's design the algorithm:
1. Compute prefix sum P[0..n].
2. Compute pref[i] = max subarray sum ending at i (Kadane forward).
3. Compute suf[i] = max subarray sum starting at i (Kadane backward).
4. For each distinct value v, we have its positions. The segments are [0, p1-1], [p1+1, p2-1], ..., [pk+1, n-1].
   For each segment, we need its max subarray sum, its max prefix sum, and its max suffix sum.
   We can get max subarray sum of [L,R] as max_{i in [L,R]} suf[i].
   We can get max prefix sum of [L,R] as max_{i in [L,R]} (P[i+1] - P[L]).
   We can get max suffix sum of [L,R] as max_{i in [L,R]} (P[R+1] - P[i]).
   We can prebuild a segment tree or sparse table on suf to answer range max in O(1) or O(log n).
   We also need range max on P and range min on P to compute max prefix and max suffix. Actually, max prefix = max_{i in [L,R]} P[i+1] - P[L] = (max_{i in [L,R]} P[i+1]) - P[L]. So we need range max of P. Max suffix = P[R+1] - min_{i in [L,R]} P[i]. So we need range min of P.
   So we can prebuild a segment tree for range max of suf, range max of P, and range min of P. Or we can use sparse tables for O(1) queries.
5. For each v, we have segments. We need the max subarray sum of the concatenation of these segments. This is the max over i <= j of:
   - If i == j: max subarray sum of segment i.
   - If i < j: max suffix of segment i + sum of segments i+1..j-1 + max prefix of segment j.
   We can compute this by a sweep over the segments. Let m be the number of segments. We can compute an array seg_max_sub, seg_max_pref, seg_max_suf, seg_sum. Then we need the max subarray sum of the array formed by these segments. This is exactly the max subarray sum of an array where each element is a segment. But we can't just use the segment sums because we can also take subsegments. However, the max subarray sum of the concatenation is the max over all subarrays. We can compute it by considering the segments as an array of length m, and for each segment, we have a value: the max subarray sum that ends at the end of the segment. We can compute this by iterating through the segments and maintaining the best subarray sum ending at the current segment's end. Let cur = -inf. For each segment, we update cur = max( cur + seg_sum, seg_max_sub, seg_max_suf + (cur if cur is the max subarray sum ending at previous segment's end?) Not exactly.

Wait, we can think of the concatenation as an array. We can run Kadane on the concatenation by processing each segment. The current max subarray sum ending at the end of the segment is either:
- The max subarray sum entirely within the segment.
- The max suffix of the segment plus the max subarray sum ending at the end of the previous segment.
- The max prefix of the segment? No, because the subarray must end at the end of the segment.
So for each segment, we know the max subarray sum ending at its end (which is seg_max_suf, but only if the subarray starts at the beginning of the segment? No, seg_max_suf is the max sum of a subarray that ends at the end of the segment and is within the segment. But we can also have a subarray that starts in a previous segment and ends at the end of this segment. The sum of such a subarray is (max subarray sum ending at the end of the previous segment) + (sum of all segments in between) + (max suffix of this segment). But the max subarray sum ending at the end of the previous segment is not necessarily the max subarray sum that can be extended. Actually, to combine, we need the max sum of a subarray that ends at the end of the previous segment. This is exactly the max subarray sum ending at that point. So we can maintain cur_end = maximum subarray sum ending at the end of the current segment. Then for the next segment, cur_end = max( seg_max_suf, cur_end + seg_sum? No, because the subarray can start in the previous segment and end in the next segment. The sum is (cur_end) + (sum of next segment) if we take the whole next segment? But we can also take only a prefix of the next segment. So the new cur_end = max( seg_max_suf, cur_end + seg_sum, cur_end + seg_max_pref? No.

This is not straightforward. We can instead compute the max subarray sum of the concatenation by using the fact that the concatenation is the original array with x removed. We can compute its max subarray sum by a standard Kadane on the original array, but resetting the current sum when we hit x? No, because after removal, the subarray can continue across x. So we should not reset at x; instead, we should treat x as deleted, so the current sum continues across x? But x contributes 0 after deletion. So the current sum after deletion is the sum of non-x elements. So we can compute this by scanning the original array, and maintaining cur = max subarray sum ending at the current position in the compressed array. For a non-x element a, new_cur = max(a, cur + a). For an x element, new_cur = cur (since x is removed, it doesn't add anything, and the subarray can continue). Wait, is that correct? In the compressed array, the previous element is the last non-x element. So when we see an x, the current subarray sum ending at the next non-x element is the same as ending at the previous non-x element. So yes, we can just skip x. So the Kadane on the compressed array is: cur = 0; ans = -inf; for each element in original array: if element != x: cur = max(element, cur + element); else: cur = cur; ans = max(ans, cur). But this depends on x. We need to do this for each x. However, we can precompute for each position the value of cur if we were to start there? Not exactly.

But note that the recurrence is: for a fixed x, cur is the max subarray sum ending at the current position in the compressed array. We can compute this for all x simultaneously? Probably not.

However, we can compute S_x for all x in O(n) total using a hash map of value to its max subarray sum contribution? Let's think about the formula: S_x = max_{l,r} (sum(l,r) - x * count_x(l,r)). This is the max subarray sum of the array A_x where A_x[i] = nums[i] - x if nums[i]==x else nums[i]. But as we saw, this is not exactly S_x; it's the max subarray sum of the modified array, which is max(S_x, 0) if there is an all-x subarray. Actually, A_x is the modified array (x set to 0). The max subarray sum of A_x is max_subarray(A_x). We have S_x = max_subarray(A_x) if max_subarray(A_x) is achieved by a subarray with at least one non-x element, else S_x could be negative. But if max_subarray(A_x) = 0 and S_x < 0, then S_x is the maximum subarray sum of the compressed array, which is the maximum subarray sum of A_x restricted to subarrays with at least one non-x element. This is equal to the maximum subarray sum of the array A_x with the modification that we cannot take a subarray of all zeros. This is exactly the maximum subarray sum of A_x, unless the maximum is 0 and the only way to get 0 is by taking all zeros. In that case, the true S_x is the maximum subarray sum of A_x with the constraint that we must take at least one non-zero element. But if A_x has a 0 from a non-x element, then that 0 is allowed. So the only problem is when the only zeros in A_x are from x's. So S_x = max_subarray(A_x) if either max_subarray(A_x) > 0, or max_subarray(A_x) = 0 and there is a non-x 0, or there is a subarray with sum 0 that includes non-x. If max_subarray(A_x) = 0 and no such subarray, then S_x is the maximum subarray sum of A_x that includes at least one non-x element, which could be negative.

But is it possible that S_x is negative and max_subarray(A_x) = 0, and this x gives the maximum? Only if all other candidates are <= S_x. But if S_x is negative, then the original array's max is also negative (or at most S_x). So the answer would be negative. But if we compute max_subarray(A_x) for all x, we would get 0, which is higher. So we would incorrectly output 0. For example, nums = [-1, -2]. max_subarray(A_-2) = 0, but S_-2 = -1. The answer is -1. So we cannot use max_subarray(A_x).

We need a way to compute S_x correctly. Since S_x is the max subarray sum of the compressed array, and the compressed array is the original array with x removed, we can compute S_x by taking the original array and for each x, removing x and running Kadane. But we need O(n log n) or O(n).

Given the time constraints, I think the intended solution is to precompute prefix and suffix max subarray sums for the original array, and then for each x, compute the answer by considering the gaps. Let's derive that.

For a fixed x, let the positions be p1 < p2 < ... < pk. The segments are:
S0 = [0, p1-1]
S1 = [p1+1, p2-1]
...
Sk = [pk+1, n-1]

The compressed array is the concatenation C = S0 + S1 + ... + Sk. The max subarray sum of C is what we want.

We can compute the max subarray sum of C by using the following observation: C is exactly the original array with x removed. So we can compute its max subarray sum by a Kadane-like scan that skips x. But we can precompute for the original array the following:
- For any interval [L, R], we can get its max subarray sum, max prefix sum, max suffix sum.
Then the max subarray sum of C is the max over all subarrays of C. This is equivalent to the max over all pairs of segments (i, j) with i <= j of:
- If i == j: max subarray sum of Si.
- If i < j: max suffix sum of Si + total sum of segments Si+1 to Sj-1 + max prefix sum of Sj.

We can compute this for each x in O(k) time if we can query the max suffix of a segment, max prefix of a segment, and the sum of consecutive segments in O(1) or O(log n). Since the number of segments is k+1, and total segments over all x is O(n), we can do this in O(n log n) with a segment tree or O(n) with prefix/suffix precomputation.

Let's see: For a segment [L, R], we need:
- max subarray sum: max_{i in [L,R]} suf[i]. We can precompute a sparse table for suf to get this in O(1).
- max prefix sum: max_{i in [L,R]} (P[i+1] - P[L]) = (max_{i in [L,R]} P[i+1]) - P[L]. We can precompute sparse table for max of P.
- max suffix sum: max_{i in [L,R]} (P[R+1] - P[i]) = P[R+1] - (min_{i in [L,R]} P[i]). We can precompute sparse table for min of P.
- total sum: P[R+1] - P[L].

So with O(n log n) preprocessing, we can answer these queries in O(1).

Now, for a given x, we have m = k+1 segments. We need to find the maximum over i <= j of the above expression. This is a classic problem: given an array of segments, each with max_sub, max_pref, max_suf, sum, find the max subarray sum of the concatenation. This is exactly the max subarray sum of an array where each element is a segment. But we can't just use the segment sums; we need to use the fact that a subarray can start in the middle of a segment and end in the middle of another. The value for a pair (i, j) with i < j is: max_suf(Si) + (sum of segments i+1 to j-1) + max_pref(Sj). This is a range query over the segments. We can precompute the prefix sums of the segment sums. Then the sum of segments i+1 to j-1 is pref_seg_sum[j-1] - pref_seg_sum[i]. So the expression becomes: max_suf(Si) - pref_seg_sum[i] + pref_seg_sum[j-1] + max_pref(Sj). For a fixed i, we want to maximize over j > i: (pref_seg_sum[j-1] + max_pref(Sj)). So we can sweep i from 0 to m-1, maintaining the maximum value of (pref_seg_sum[j-1] + max_pref(Sj)) for j > i. But we also have the case i == j: max_sub(Si). So the answer for this x is max( max_i max_sub(Si), max_{i < j} (max_suf(Si) - pref_seg_sum[i] + max_{j > i} (pref_seg_sum[j-1] + max_pref(Sj)) ).

We can compute this in O(m) time if we precompute the segment arrays. Since total m over all x is O(n), this is O(n) total after O(n log n) preprocessing.

Let's verify with example 1: nums = [-3,2,-2,-1,3,-2,3]. For x = -2, positions = [2,5]. Segments: [0,1], [3,4], [6,6].
We need max_sub, max_pref, max_suf, sum for each.
[0,1]: nums [-3,2]. sum = -1. max_sub = max(-3,2,-3+2= -1) = 2? Actually, max subarray sum: -3, 2 -> max is 2. max_pref: max(-3, -3+2) = -1? Wait, prefix sums: -3, -1. max prefix is -1? Actually, max prefix sum is the maximum sum of a prefix. Prefixes: -3, -3+2=-1. Max is -1. max_suf: suffixes: 2, -3+2=-1. Max suffix is 2.
[3,4]: nums [-1,3]. sum = 2. max_sub: max(-1,3,-1+3=2) = 3. max_pref: max(-1, 2) = 2. max_suf: max(3, 2) = 3.
[6,6]: nums [3]. sum=3. max_sub=3, max_pref=3, max_suf=3.
Now, segments: S0, S1, S2.
m=3.
max_sub: 2,3,3 -> max=3.
Now, i=0 (S0): max_suf(S0) - pref_seg_sum[0] = 2 - (-1) = 3? Wait, pref_seg_sum: sum(S0) = -1. So pref_seg_sum[0] = -1, pref_seg_sum[1] = -1+2=1, pref_seg_sum[2] = 1+3=4.
For i=0, we need j>0: j=1: pref_seg_sum[0] + max_pref(S1) = -1 + 2 = 1. j=2: pref_seg_sum[1] + max_pref(S2) = 1 + 3 = 4. Max for j>0 is 4. So candidate = max_suf(S0) - pref_seg_sum[0] + 4 = 2 - (-1) + 4 = 7.
For i=1: max_suf(S1) - pref_seg_sum[1] = 3 - 1 = 2. j=2: pref_seg_sum[1] + max_pref(S2) = 1+3=4. Candidate = 2+4=6.
So max is max(3,7,6) = 7. Correct!

So this algorithm works! And it's O(n log n) due to sparse table construction, and O(n) for the segment processing.

We also need to consider the original array (no operation). That is just the standard max subarray sum, which is the global max of suf (or pref). We can compute that easily.

So the steps:
1. Compute prefix sum P[0..n] (P[0]=0).
2. Compute suf[i] = max subarray sum starting at i. This can be done by Kadane backwards.
3. Build sparse table for suf to get range max in O(1).
4. Build sparse table for max of P (for prefix sums) to get range max of P[i+1] for i in [L,R]. Actually, we need max_{i in [L,R]} P[i+1]. So we can build a sparse table on P[1..n] (or include P[0]).
5. Build sparse table for min of P to get range min of P[i] for i in [L,R].
6. For each segment [L,R], we can compute:
   - total sum = P[R+1] - P[L]
   - max_sub = query_max_suf(L, R)
   - max_pref = query_max_P(L+1, R+1) - P[L]  [since P indices are 0..n, and we want max_{i in [L,R]} P[i+1]]
   - max_suf = P[R+1] - query_min_P(L, R)
7. Group positions by value. For each distinct value x:
   - Get sorted positions.
   - Build list of segments: [0, pos[0]-1], [pos[0]+1, pos[1]-1], ..., [pos[-1]+1, n-1]. Skip empty segments.
   - For each segment, compute its (sum, max_sub, max_pref, max_suf) using the queries.
   - Let m = number of segments.
   - If m == 0: then the array becomes empty? But problem says "nums remains non-empty on removing all occurrences of x". So we should not consider x that would make the array empty. We can skip such x.
   - Compute the answer for this x using the formula:
        ans_x = max( max_i max_sub_i, max_{i=0}^{m-2} (max_suf_i - pref_sum_i + max_{j=i+1}^{m-1} (pref_sum_{j-1} + max_pref_j)) )
     where pref_sum_i is the prefix sum of segment sums: pref_sum[0] = sum_0, pref_sum[i] = pref_sum[i-1] + sum_i.
     We can compute the inner max by sweeping from right to left: maintain best = -inf; for j from m-1 down to 1: best = max(best, pref_sum[j-1] + max_pref_j); then for i from 0 to m-2: ans_x = max(ans_x, max_suf_i - pref_sum[i] + best). But we need to update best as i increases. Actually, we can sweep i from 0 to m-2, and for each i, we need the max over j>i. So we can precompute an array right_best[i] = max_{j > i} (pref_sum[j-1] + max_pref_j) for i = 0..m-2. Then ans_x = max( max_sub_max, max_{i=0}^{m-2} (max_suf_i - pref_sum[i] + right_best[i]) ).
   - Keep track of the global maximum ans.
8. Also compute the original max subarray sum (which is the max of suf or the global max of the array). This is the candidate for no operation.
9. Return the global max.

We need to be careful with indices and empty segments. Also, the array is 0-indexed.

Complexities: O(n log n) for sparse tables, O(n) for processing segments. This is efficient for n=1e5.

Now, we need to implement this in the function maxSubarraySum.

Let's write the code step by step.

First, compute P: P[0] = 0, P[i+1] = P[i] + nums[i] for i=0..n-1.
Compute suf: suf[i] = max subarray sum starting at i. We can compute by: suf[n-1] = nums[n-1]; for i from n-2 down to 0: suf[i] = max(nums[i], nums[i] + suf[i+1]).
Compute pref: pref[i] = max subarray sum ending at i. But we might not need pref.

We need sparse table for suf: we can build log table and st_suf[k][i] = max of suf in range [i, i+2^k-1].
Similarly for P_max and P_min: we need range max and min of P. Note that P has length n+1. We need to query:
- max_{i in [L,R]} P[i+1]: this is max of P[L+1..R+1]. So we can build sparse table on P[1..n] (1-indexed) or on P[0..n] and adjust.
- min_{i in [L,R]} P[i]: this is min of P[L..R].

So we can build sparse tables on the entire P array of length n+1.

For efficiency, we can precompute log2 for each length.

Now, for each distinct value, we have its positions. We can use a dictionary (hash map) to store the list of positions for each value. While iterating, we can build the map: pos_map = defaultdict(list). For i in range(n): pos_map[nums[i]].append(i).

Then for each x in pos_map:
   positions = pos_map[x]
   segments = []
   prev = 0
   for p in positions:
       if prev <= p-1:
           segments.append( (prev, p-1) )
       prev = p+1
   if prev <= n-1:
       segments.append( (prev, n-1) )
   # Now we have list of segments. Filter out empty? Actually, if prev > p-1, it's empty, we skip.
   # If segments is empty, then removing x makes the array empty. We should skip this x because the problem says "nums remains non-empty on removing all occurrences of x". So we only consider x where segments is non-empty.
   if not segments: continue
   m = len(segments)
   # Compute arrays for segments
   sums = []
   max_subs = []
   max_prefs = []
   max_sufs = []
   for L, R in segments:
       total = P[R+1] - P[L]
       max_sub = query_max_suf(L, R)
       # max prefix: max_{i in [L,R]} (P[i+1] - P[L]) = (max_{i in [L,R]} P[i+1]) - P[L]
       max_pref = query_max_P(L+1, R+1) - P[L]  # if L+1 > R+1, then segment is empty? But we skipped empty segments, so L <= R, so L+1 <= R+1.
       max_suf = P[R+1] - query_min_P(L, R)
       sums.append(total)
       max_subs.append(max_sub)
       max_prefs.append(max_pref)
       max_sufs.append(max_suf)
   # Compute prefix sums of sums
   pref_sum = [0]*m
   for i in range(m):
       pref_sum[i] = sums[i] + (pref_sum[i-1] if i>0 else 0)
   # Compute right_best
   right_best = [-float('inf')] * (m-1)  # for i=0..m-2
   if m >= 2:
       best = -float('inf')
       # We need for each i, max_{j > i} (pref_sum[j-1] + max_prefs[j])
       # We can compute from right to left
       for j in range(m-1, 0, -1):

## worker: Implement the solution in Python using the describ
The solution uses a sparse table to answer range maximum/minimum queries on the prefix sum array and the suffix maximum subarray sums in O(1) after O(n log n) preprocessing. For each distinct value `x`, it constructs the contiguous segments of non-`x` elements. The maximum subarray sum of the array with `x` removed is computed by considering two cases: subarrays entirely within one segment (using precomputed `suf` values), and subarrays spanning multiple segments (using segment suffix sums, prefix sums, and the total sums of intermediate segments). The overall answer is the maximum over all values `x` and the original array. This runs in O(n log n) time, which is efficient for n ≤ 10^5.

## worker: Implement the solution in Python within the class 
The solution uses a sparse table for O(1) range maximum/minimum queries on the prefix sum array and suffix maximum subarray sums, after O(n log n) preprocessing. For each distinct value `x`, it identifies the contiguous segments of non-`x` elements. The maximum subarray sum of the array with `x` removed is computed by considering two cases: subarrays entirely within one segment (using precomputed `suf` values), and subarrays spanning multiple segments (using segment suffix sums, prefix sums, and the total sums of intermediate segments). The overall answer is the maximum over all values `x` and the original array's maximum subarray sum. This runs in O(n log n) time, suitable for n ≤ 10^5.

## worker: Implement the solution in Python within the class 
The solution uses a sparse table for O(1) range maximum/minimum queries on the prefix sum array and suffix maximum subarray sums, after O(n log n) preprocessing. For each distinct value `x`, it identifies the contiguous segments of non-`x` elements. The maximum subarray sum of the array with `x` removed is computed by considering two cases: subarrays entirely within one segment (using precomputed `suf` values), and subarrays spanning multiple segments (using segment suffix sums, prefix sums, and the total sums of intermediate segments). The overall answer is the maximum over all values `x` and the original array's maximum subarray sum. This runs in O(n log n) time, suitable for n ≤ 10^5.

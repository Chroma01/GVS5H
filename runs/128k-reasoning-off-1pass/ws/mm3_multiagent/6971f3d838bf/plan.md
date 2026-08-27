We need the maximum subarray sum after optionally removing all occurrences of one value. Compute Kadane's max subarray sum for the original array. For each unique value v, simulate its removal and compute the best subarray sum. Since |nums| ≤ 1e5, we can afford O(n) per candidate if candidates are few, but worst case n unique values would be O(n²). Instead, observe that removing a value splits the array into segments of elements ≠ v, and the best subarray in the resulting array is the max Kadane sum over any of those segments. So for each v, the answer is the maximum Kadane sum across all maximal contiguous blocks that don't contain v. To compute this efficiently, we can precompute the original Kadane result and then, for each value, track the maximum segment sum in blocks not containing it. A practical approach: for each value v, scan the array once accumulating Kadane on segments without v, taking the max; but doing this per v is too slow. Instead, we can use a different insight: the optimal subarray is either the original best (no deletion) or comes from a segment that was previously broken by some element we removed. We can compute, for each position i, the best subarray sum entirely in the left of i (without using i) and in the right of i, then combine by removing a specific value. A simpler O(n log n) or O(n) approach: group indices by value, and for each value, compute the best subarray sum in the array with its occurrences treated as separators. This is equivalent to computing Kadane on the "gaps" between occurrences (including edges). We need for each v: the maximum Kadane sum among all gaps. We can precompute prefix best Kadane values and suffix best, but since gaps are disjoint, we can just compute Kadane on each gap independently. The total work across all v is O(n * (#unique values per element)) which is still O(n²) worst case. We need a smarter trick.

Key observation: we only need to consider deleting a value v that is the minimum element of the optimal subarray we eventually pick, or more precisely, the removal can only help if it eliminates a "bad" element that previously limited a subarray. Actually, the maximum subarray sum after deletion is either (a) the original max subarray sum, or (b) some subarray that doesn't include the deleted value. This is equivalent to: the answer is the max over all subarrays S of (sum(S)) such that S doesn't contain the deleted value, or no deletion. But since we can pick any value to delete, the answer is simply the max over all subarrays S of sum(S) if we can delete all occurrences of some value not in S (or do nothing). Since we can always choose to delete nothing, the answer is at least the original max. If we want to improve, we need to find a subarray S whose sum is greater than the original max, and such that S contains no occurrences of some value v that appears outside S (i.e., we delete v). But wait, deletion removes v from the whole array, so S must be a subarray of the array after removal, meaning S must not contain v, and all elements outside S are either v or not part of the subarray.

Alternative viewpoint: The resulting array after removing value v is just the concatenation of the subarrays between v's. So the maximum subarray sum after removal is the maximum Kadane sum over all these "v-free" segments. We want the max over v of that. This is exactly the maximum over all v of the maximum subarray sum in the array with v's removed. This can be computed by considering the contribution of each v's "gaps". But we can note that the maximum subarray sum in the whole array is achieved by some subarray. If that subarray sum is the answer, we can just not delete anything. If we delete v, the new max is the max over all maximal subarrays of elements ≠ v. So the answer is max(original max, max over v of (max subarray sum in nums with v's as delimiters)).

We can compute this by, for each v, considering the array where v is a very large negative number? No. Actually, if we set v to -infinity, then any subarray containing v is invalid. That's not helpful.

Better: For each position i, consider the value nums[i]. If we delete nums[i], it splits the array. The best subarray in the resulting array is the max Kadane sum in either the left part or the right part (or crossing the gap? No, because the gap removes nums[i] and possibly other occurrences, but subarrays cannot cross removed elements). So the best subarray after deleting v is max of Kadane sums of all maximal contiguous segments not containing v. This is the max over all segments S that don't contain v of Kadane(S). So for each v, the answer is max_{segment S not containing v} Kadane(S). Since there are at most n unique values, and each segment is bounded by occurrences of v, we could for each v, scan the array and compute Kadane on each segment, but that's O(n) per v.

We need a global computation. Notice that the Kadane sum on a segment depends only on the segment's elements. If we delete v, we are essentially forbidding subarrays that contain v. The maximum subarray sum not containing v is the maximum over all subarrays that don't contain v. This is equal to the maximum over all subarrays of the original array, except we discard those that contain v. So for each v, we need the maximum subarray sum among subarrays that avoid v. This is exactly the maximum subarray sum in the array with v removed, which is what we said. To compute this efficiently, we can precompute for each position the best subarray sum ending at or before it, and starting at or after it, but the condition "avoid v" is global.

Actually, we can use a divide and conquer or segment tree? Since n is only 1e5, O(n log n) or even O(n sqrt(n)) might be okay. But O(n log n) with a segment tree that supports "maximum subarray sum on intervals without a particular value" is complex.

Simpler: We can consider that the optimal subarray after deletion is either the original optimal subarray, or a subarray that was previously broken by some element that we remove. The original optimal subarray is some interval [l, r]. If we remove some value v, the new optimal could be a subarray that contains l..r but now is longer because the v's in between are removed? No, removing v removes v itself, but doesn't add elements. Actually, if we remove v, we are concatenating segments that were separated by v. So a subarray that crosses v in the original is not allowed after removal (since v is gone). So removal cannot create a longer subarray; it can only allow subarrays that are unions of segments separated by v, but a subarray must be contiguous in the new array, so it can span across where v was, as long as it doesn't include v. But if v is removed, the new array has those segments adjacent, so a subarray can cover the end of one segment and the start of the next. So the new subarray could be larger than any original subarray that didn't cross v. However, the sum of a subarray crossing a removed v is simply the sum of the elements on both sides; there's no penalty. So the new max subarray is the max over all intervals that don't contain v, which is exactly the max Kadane sum in the array with v's as delimiters.

Given constraints, we can iterate over all unique values, but in the worst case n=1e5 with all unique, that's 1e5 * 1e5 = 1e10, too slow. We need a better approach.

Key insight: We only need to consider deleting the minimum element of some optimal subarray? Not necessarily. Let's think about the structure. Let original max subarray sum be S. If we can do better than S, we need to find a value v such that there is a subarray not containing v with sum > S. That subarray in the original array might contain v, but after removal it's allowed. So v must be a value that appears in the "bad" parts that prevented a higher sum. In particular, if we take the array and remove all negative numbers? Not exactly, because we can only remove one value.

Consider the following: The maximum subarray sum after deletion is max( S, max_{v} (maximum subarray sum in array with v's removed) ). We can compute the latter by, for each position, considering the effect of removing nums[i]. If we remove nums[i], the array splits into left and right. The best subarray could be entirely in left, entirely in right, or spanning across the gap (i.e., suffix of left + prefix of right). So for each v, the best subarray in the v-removed array is the max of:
- best subarray entirely in some left gap
- best subarray entirely in some right gap
- best suffix of a left gap + best prefix of the next right gap (i.e., spanning across a removed v).

But actually, since we remove all v, the gaps are the maximal segments of ≠ v. A subarray can be any contiguous portion of the concatenated gaps. So the maximum subarray sum in the concatenated gaps is the maximum Kadane sum on that new array. This new array is just the original with v's deleted. So its max subarray sum is the max over all subarrays that don't contain v. That's the same as the maximum over all intervals [l,r] that don't contain v of sum(nums[l..r]).

We can precompute prefix sums to get any interval sum quickly. But we need to maximize over intervals avoiding v, over all v. That seems hard.

Alternate approach: Since we can only remove one distinct value, the answer is either the original max, or achieved by removing the "worst" element in some sense. Perhaps we can consider the "best possible" subarray if we could remove any single element (by value) from the array. Actually, there's a known problem: "Maximum subarray sum after removing at most one element" but here we remove all occurrences of one value. This is a known LeetCode problem: "Maximum Subarray Sum After One Operation" or similar? Actually, there is a problem: "You are given an array, you can remove all occurrences of one value, return max subarray sum". I recall a solution using prefix max subarray and suffix max subarray for each value? Let's search memory.

I think the intended solution is O(n log n) or O(n) with hashing. We can group indices by value. For each value v, we have a sorted list of its indices. The array is split into segments: from start to first index-1, then between indices, then last index+1 to end. For each such segment, we can compute the maximum subarray sum (Kadane) within that segment. Then the best subarray after removing v is the max over all these segments of their Kadane sum, OR the sum of a suffix of one segment and a prefix of the next segment (since after removal they become adjacent). So we also need for each gap: the maximum prefix sum and maximum suffix sum. Then the best spanning subarray is max over adjacent gaps of (max suffix of left + max prefix of right). Then overall for v, best = max(max_kadane_in_gap, max_span).

We need to compute this efficiently for all v. The total number of gaps across all v is sum over v of (count(v) + 1) = n + number of unique values. If we compute for each v, scanning all its gaps, the total work is O(n + U) if we can compute the Kadane, max prefix, max suffix of each gap in O(length). But we have to do this for every v, so total O(n * U) in worst case. However, note that the segments for different v are different. But we can precompute prefix Kadane and suffix Kadane for the whole array? Not directly, because the gaps depend on v.

Wait: There is a way to compute the maximum subarray sum for all possible deletions of a value in O(n) total using a map from value to its indices and processing. Actually, we can do this: For each value v, we need the maximum subarray sum in the array with v's removed. This is equivalent to the maximum subarray sum in the array where we set all v to a very negative number? No.

Another idea: The answer is the maximum over all subarrays of sum(subarray) if we can delete any one value not in the subarray. Since we can delete any value, the best we can do is: for each subarray, we can delete any value that appears outside the subarray. To maximize the sum, we would want to delete a value that appears many times and is very negative, but it must not be in the subarray. If the subarray contains all occurrences of some value, we cannot delete that value because then the subarray would be empty (unless we don't delete it, but we are considering the subarray as the answer after deletion). Actually, if we delete value v, the resulting array has no v. So any subarray in the resulting array cannot contain v. So if we want a particular subarray S to be the maximum after deletion, we need to choose a v such that S contains no v, and we delete all v's (which are outside S). So v must be a value that does not appear in S. Therefore, for each subarray S, the best we can achieve by deleting some v not in S is exactly sum(S), provided we delete a v that is present elsewhere (or do nothing). But wait, if we delete a v not in S, the array changes, and the maximum subarray might be different, but we are evaluating the maximum over all resulting arrays. The maximum over all v of (max subarray sum in array without v) is exactly the maximum over all subarrays S that can be obtained after some deletion, of sum(S). And any subarray S is obtainable if there exists some v not in S. That is, S is a subarray of the original array that does not contain all occurrences of some value? Actually, we need to delete a value v. After deletion, the array is original with v's removed. S must be a contiguous subarray of that new array. That means S corresponds to a contiguous segment in the original array that may span across v's, but only if those v's are removed. More precisely, S is a union of one or more original contiguous blocks that were separated by v's. In the original array, S might be a subarray that contains v's, but after removal, those v's are gone, so S is contiguous. However, if S contains v, then after removal, S is not contiguous because the v is missing. So S cannot contain v. Therefore, S is a subarray of the original array that does not contain v. So S is a subarray of the original array that avoids v. So the set of possible subarrays after deleting v is exactly the set of subarrays of the original array that do not contain v. Thus, the maximum sum after deleting v is the maximum sum of a subarray that avoids v. So the overall answer is max over v of (max subarray sum avoiding v), and also the option of no deletion (which corresponds to avoiding nothing, i.e., v can be a value not in the array, but we can think of no deletion as a special case).

So we need to compute, for each value v, the maximum subarray sum of the original array that does not contain v. Let's denote f(v) = max sum of subarray not containing v. We want max_v f(v) (including the case of no deletion, which is the global max subarray sum, which is also f(v) for any v that is not in the optimal subarray, but we can just take the global max as a baseline).

Now, f(v) is the maximum subarray sum in the array where v's are forbidden. This is like we have an array and we want the max subarray sum that doesn't include a particular value. We can compute f(v) for all v efficiently? Notice that the global max subarray sum is achieved by some subarray [l,r]. If that subarray doesn't contain v, then f(v) is at least that sum. If it does contain v, f(v) might be smaller or larger. Actually, the max subarray avoiding v could be larger than the global max? No, because the global max is over all subarrays, and avoiding v is a restriction, so f(v) <= global max. Wait, is that true? The global max is the max over all subarrays. If we restrict to subarrays not containing v, the max can only be less than or equal to the global max. So f(v) <= original max for all v. That means the answer is at most the original max. But the example shows we can get 7 > 4. How? Let's check: original max subarray sum is 4. After deleting -2, we get max subarray sum 7. The subarray [2, -1, 3, 3] has sum 7. In the original array, this subarray is not contiguous because it crosses the -2 at index 2? Original: [-3, 2, -2, -1, 3, -2, 3]. The subarray [2, -1, 3, 3] in the new array corresponds to original indices 1,3,4,5,6? Wait, after removing -2, the new array is [-3, 2, -1, 3, 3]. The subarray [2, -1, 3, 3] is indices 1,2,3,4 in the new array, which correspond to original indices 1,3,4,6. This is not a contiguous subarray in the original. So my earlier reasoning that "subarray in the new array corresponds to a subarray in the original that avoids v" is flawed. Because when we remove v, the new array is the original with v's deleted, so elements shift. A subarray in the new array is a contiguous block in the new array, which corresponds to a set of indices in the original that are not necessarily contiguous; they are the union of segments separated by v's. So the sum of such a subarray is the sum of the elements in those segments, which is the sum of a subarray in the original that may have v's removed from the middle? Actually, if we take a subarray in the new array, it corresponds to a contiguous range in the new array, which corresponds to a range in the original that may skip over v's. In the original, that set of indices is not contiguous; there are gaps where v's were. So the sum is the sum of a "subsequence" that is not necessarily contiguous in the original, but it is the sum of a set of elements that appear in order, with possible v's in between that are excluded. So it's not a subarray of the original; it's a "subsequence" that is the union of some suffix of one v-free segment and some prefix of another, etc. In fact, any subarray in the new array is the concatenation of some number of whole v-free segments? Not necessarily; it could be a proper suffix of a segment and a proper prefix of the next. So the sum is the sum of a suffix of a segment plus a prefix of the next segment, or just a full segment, etc. So the maximum subarray sum in the new array is the maximum over all possible ways to pick a starting segment and an ending segment (possibly the same) and take a suffix of the start and a prefix of the end, and include all segments in between entirely? Wait, if we pick a subarray in the new array, it starts at some position in the new array, which is within some v-free segment. It ends at some position in the new array, which is within some v-free segment (possibly the same or a later one). The subarray will include the entire parts of the new array between the start and end, which means it includes all elements in the intervening segments entirely. So the sum is: (sum of suffix of the starting segment) + (sum of all full segments in between) + (sum of prefix of the ending segment). If the start and end are in the same segment, it's just a subarray of that segment.

Therefore, the maximum subarray sum after deleting v is the maximum over all segments (the v-free blocks) of the maximum subarray sum within that segment (Kadane), and also the maximum over all pairs of segments (including same) of the best suffix + best prefix + sum of full segments in between. But we can compute this efficiently if we know for each segment its total sum, best prefix, best suffix, and best subarray (Kadane). Then the best subarray spanning multiple segments can be computed by considering the "max subarray sum on the line of segments" where each segment is treated as an element with value equal to its total sum, and we can take prefix/suffix of segments? Actually, if we take a subarray that spans multiple segments, the sum is the sum of the total sums of the full segments in the middle, plus a suffix of the first and a prefix of the last. This is equivalent to: in the array of segments, we can pick a subarray of segments, and we can take a suffix of the first segment and a prefix of the last segment. To maximize, we would take the best suffix of the first and best prefix of the last. But we can also choose to take the entire first and last segments if that's better. Actually, the best subarray spanning from segment i to segment j is: (max suffix sum of segment i) + (sum of segments i+1 to j-1) + (max prefix sum of segment j). If i=j, it's just the max subarray sum within that segment. So for each v, the answer is the maximum over i <= j of that quantity.

Now, we need to compute this for all v efficiently. The number of segments for a given v is count(v) + 1. If we process each v independently, total work is sum over v of O(count(v)) = O(n) for processing the segments, but we also need to compute the max over i<=j for that v, which could be O(count(v)^2) if we do it naively. However, we can compute the max over i<=j in O(count(v)) using Kadane on an array where each segment is represented by its total sum? But careful: the ability to take a suffix of the first and prefix of the last means that the effective "value" of taking a segment as the start is not just its total sum; we can take a suffix which might be less than total. But we can think of the following: For a fixed v, we have segments s_1, s_2, ..., s_k (k = count(v)+1). We want max_{1 <= i <= j <= k} (max_suffix(s_i) + sum(s_{i+1}..s_{j-1}) + max_prefix(s_j)). Note that if i=j, it's max_subarray(s_i). If i<j, we can also consider the case where we take the entire segment i and entire segment j, but that's included if we take the suffix = total and prefix = total. So we can define for each segment s, we have values: total = T, best_prefix = P, best_suffix = S, best_subarray = K. Then the answer for v is max( max_i K_i, max_{i<j} (S_i + sum_{t=i+1}^{j-1} T_t + P_j) ). We can compute the second part by scanning from left to right, maintaining a running sum of T's, and for each j, considering the best i<j: we want max_i (S_i + sum_{t=i+1}^{j-1} T_t). This is like: as we go, we keep track of the maximum value of (S_i - sum_{t=1}^{i} T_t) so far, and then for j, the candidate is that max + sum_{t=1}^{j-1} T_t + P_j. Actually, let's define prefix sums of T: let A_m = sum_{t=1}^{m} T_t. Then sum_{t=i+1}^{j-1} T_t = A_{j-1} - A_i. So S_i + A_{j-1} - A_i + P_j = (S_i - A_i) + A_{j-1} + P_j. So for each j, we can compute candidate = (max_{i < j} (S_i - A_i)) + A_{j-1} + P_j. We can maintain running max of (S_i - A_i) as we iterate j from 1 to k. Also we need to consider i=j? That case is K_j, which is separate. Also we need to consider the case where we take a subarray that starts and ends in the same segment, but that might not be the max subarray of that segment if we consider suffix+prefix? Actually, if i=j, the formula S_i + ... + P_i with no middle is not defined because there is no middle, and the sum is just a subarray of segment i, which is at most K_i. So we take max over i of K_i separately. Also, we could have i and j such that i+1 = j, then the middle sum is 0, so candidate = S_i + P_j. So the algorithm for a given v: 
- Build the list of segments (v-free blocks) with their T, P, S, K.
- Compute overall max as max( max_i K_i, max_{j=2..k} ( (max_{i < j} (S_i - A_i)) + A_{j-1} + P_j ) ), where A_0 = 0, and A_{m} = sum_{t=1}^{m} T_t.
This is O(k) per v, where k = count(v) + 1.
Total time over all v: sum_v O(count(v)+1) = O(n + U) where U is number of unique values. Since U <= n, this is O(n). This is efficient! But we need to compute for each segment its T, P, S, K. We can compute these by scanning the array and for each v, when we encounter a block of non-v elements, we compute its stats. But we are doing this for all v simultaneously? We can group indices by v, and for each v, we can iterate through the array and compute the segments. Since we need to do this for each v, if we scan the entire array for each v, it's O(n*U). But we can do it more efficiently by using the indices of v to define the segments. For each v, we have its list of indices. The segments are: from 0 to first_idx-1, between indices, from last_idx+1 to n-1. For each such segment, we need to compute T, P, S, K on the subarray nums[l..r]. We can compute these stats for any subarray in O(length) by scanning that subarray. If we do that for each segment of each v, the total work is sum over v of (sum of lengths of segments for v). The segments for a given v partition the array (except the v's themselves). So for a fixed v, the segments are disjoint and cover all non-v elements. So the sum of lengths of segments for v is n - count(v). Therefore, total work over all v is sum_v (n - count(v)) = U*n - n. That's O(n*U), which is too slow (1e10).

We need to compute the stats for all segments for all v without scanning the whole array for each v. How can we do that? We need to precompute something so that for any interval [l,r] (which is a segment for some v, i.e., an interval not containing v), we can quickly get T, P, S, K. But there are many such intervals: for each v, there are count(v)+1 intervals. The total number of intervals is sum_v (count(v)+1) = n + U. That's manageable (up to 2e5). But we need to compute the stats for each interval quickly. If we can precompute prefix sums for T, and also some prefix/suffix Kadane info, we can compute T, P, S, K for any interval in O(1) or O(log n). Since intervals are arbitrary, we can precompute prefix sums of the array for T. For P, S, K, we can use segment tree that stores the Kadane tuple (total, best prefix, best suffix, best subarray) for any interval. Then for each interval [l,r], we can query the segment tree in O(log n) to get the tuple. Total intervals = n + U, so total time O((n+U) log n) = O(n log n), which is fine for n=1e5.

So the plan:
1. Build a segment tree over the array that can merge two intervals to give the tuple (total, best_prefix, best_suffix, best_subarray). Standard merge: for left (T1, P1, S1, K1) and right (T2, P2, S2, K2), total = T1+T2, best_prefix = max(P1, T1+P2), best_suffix = max(S2, S1+T2), best_subarray = max(K1, K2, S1+P2).
2. For each unique value v in the array:
   - Get sorted list of indices where nums[i] == v. Let indices = [i1, i2, ..., ik].
   - Define the segments (l,r) as: (0, i1-1), (i1+1, i2-1), ..., (ik+1, n-1). Note that some segments may be empty (if consecutive indices). If a segment is empty, its T=0, P=0, S=0, K=0 (but careful: empty subarray is not allowed, but we can treat it as 0 and ignore because it won't contribute to max positive sum, but we need to ensure we don't incorrectly allow empty subarray. However, since we are looking for maximum subarray sum, and all numbers could be negative, we should handle empty segments properly. In the merging, if a segment is empty, we can skip it. Actually, an empty segment corresponds to no elements between two v's. When we compute the max over i<=j, if i and j are adjacent in the segment list and both empty, that's not a valid subarray. We should only consider non-empty segments. But we can just filter out empty segments when building the list of segments for v. So k = count(v)+1, but we only keep those with l <= r. Let m be the number of non-empty segments.
   - For each non-empty segment, query the segment tree to get its tuple (T, P, S, K).
   - Now we have a list of tuples for the segments. We need to compute the maximum subarray sum in the concatenated array of these segments. This is essentially the maximum subarray sum on an array where each element is a segment, but with the ability to take suffix of first and prefix of last. As derived, the answer for this v is max( max_i K_i, max_{j=2..m} ( (max_{i < j} (S_i - A_i)) + A_{j-1} + P_j ) ), where A_t = sum_{u=1}^{t} T_u, with A_0 = 0.
   - Compute this in O(m) time.
   - Keep track of the maximum over all v.
3. Also consider the case of no deletion: the original max subarray sum, which is simply the K from the whole array (query segment tree on [0, n-1]).
4. Return the overall max.

Complexity: O(n log n) for building segment tree and querying for each segment. Total segments = sum_v (count(v)+1) = n + U. Each query O(log n), so total O((n+U) log n) = O(n log n). The per-v processing is O(m) which is O(count(v)+1), sum over v is O(n+U). So overall O(n log n).

We need to be careful with empty subarrays. The problem says "subarray is a contiguous non-empty sequence". So we cannot take an empty subarray. In our computation, if all numbers are negative, the max subarray sum is the maximum single element. Our algorithm should handle that. In the segment tree, best_subarray for an interval should be the max sum of a non-empty subarray within that interval. Standard Kadane does that. When we merge, we use max(K1, K2, S1+P2). This works for non-empty. For an empty segment, we should not include it. So we filter out empty segments. Then when we compute the max over i<=j, we are considering non-empty segments only. If there is only one non-empty segment, then m=1, the answer is just its K. If m=0 (i.e., the entire array is v's? But the constraint says we can only delete v if nums remains non-empty on removing all occurrences of x. So we cannot delete a value that appears everywhere. So if count(v) = n, then we cannot delete v. So we should only consider v that do not appear in all positions. In that case, there is at least one non-empty segment. So m >= 1. Good.

Edge case: if all numbers are negative, the max subarray sum is the max element. Our algorithm: original max is max element. For any v, the max subarray sum avoiding v is also the max element (if that element is not v) or the next max (if the max element is v). But since we can choose to not delete anything, the answer is the max element. So overall max is max element. Our algorithm should compute that correctly.

Now, we need to implement the segment tree. Since n=1e5, a recursive segment tree is fine. We'll store a tuple (total, pref, suff, best). Merge function as above. Query returns the tuple for an interval. We'll need to handle invalid intervals (l>r) by returning None or a special value. But we only query for valid intervals.

Let's test on the example: nums = [-3,2,-2,-1,3,-2,3]
n=7.
Original max subarray: compute: Kadane: max ending here: -3, max(2, -3+2)=2, then max(2-2=0, 2)=2, then max(2-1=1, 0)=1, then max(1+3=4, 0)=4, then max(4-2=2, 0)=2, then max(2+3=5, 0)=5. Wait, the example says original max is 4: 3 + (-2) + 3 = 4. Let's check: subarray [2,-2,-1,3,-2,3]? Actually, the example says: original max is 3 + (-2) + 3 = 4. That is indices 4,5,6: 3, -2, 3 sum=4. But there is also [2, -2, -1, 3, -2, 3]? Let's compute: 2-2=0, 0-1=-1, -1+3=2, 2-2=0, 0+3=3. Not 4. The subarray [2, -2, -1, 3] sum=2. So the max is 4. My manual Kadane: at index 5 (value 3): previous max was 2 (at index 1), so 2+3=5? Wait, I missed: after index 1 (value 2), max=2. At index 2 (value -2), max = max(-2, 2-2=0) = 0. At index 3 (value -1), max = max(-1, 0-1=-1) = -1. At index 4 (value 3), max = max(3, -1+3=2) = 3. At index 5 (value -2), max = max(-2, 3-2=1) = 1. At index 6 (value 3), max = max(3, 1+3=4) = 4. So original max is 4. Good.

Now, for each v:
v=-3: indices [0]. Segments: (1,6) = [2,-2,-1,3,-2,3]. Compute tuple: total = 2-2-1+3-2+3=3. pref: max(2, 2-2=0, 0-1=-1, -1+3=2, 2-2=0, 0+3=3) -> max prefix is 3? Actually, prefix sums: 2, 0, -1, 2, 0, 3. Max is 3. suff: suffix sums: 3, 1, 4? Let's compute: from end: 3, 3-2=1, 1+3=4, 4-1=3, 3-2=1, 1+2=3. Max suffix is 4. best: max subarray sum is 4 (as computed). So tuple: T=3, P=3, S=4, K=4. m=1, answer=4.
v=2: indices [1]. Segments: (0,0) and (2,6). 
Segment1: [-3]: T=-3, P=-3, S=-3, K=-3.
Segment2: [-2,-1,3,-2,3]: total = -2-1+3-2+3=1. pref: -2, -3, 0, -2, 1 -> max 1. suff: from end: 3, 1, 4, 3, 1 -> max 4. best: max subarray? Kadane: -2, max(-2,-1)=-1, max(3,-1+3=2)=3, max(-2,3-2=1)=1, max(3,1+3=4)=4. So K=4.
Now m=2. A1 = -3. For j=2: max_{i<2} (S_i - A_i) = max( S1 - A1 ) = max(-3 - (-3)) = 0. Then candidate = 0 + A1 + P2 = 0 + (-3) + 1 = -2. Also max K_i = max(-3, 4) = 4. So answer=4.
v=-2: indices [2,5]. Segments: (0,1), (3,4), (6,6).
Segment1: [-3,2]: total=-1, pref: max(-3, -3+2=-1) = -1, suff: max(2, -3+2=-1) = 2, best: max(-3,2,-1)=2.
Segment2: [-1,3]: total=2, pref: max(-1, -1+3=2)=2, suff: max(3, -1+3=2)=3, best: max(-1,3,2)=3.
Segment3: [3]: total=3, pref=3, suff=3, best=3.
m=3. A1=-1, A2=1, A3=4.
Compute for j=2: max_{i<2} (S_i - A_i) = S1 - A1 = 2 - (-1) = 3. Candidate = 3 + A1 + P2 = 3 + (-1) + 2 = 4. Also K_max = max(2,3,3)=3.
For j=3: max_{i<3} (S_i - A_i) = max( S1-A1=3, S2-A2=3-1=2 ) = 3. Candidate = 3 + A2 + P3 = 3 + 1 + 3 = 7.
So answer=7.
v=-1: indices [3]. Segments: (0,2), (4,6).
Seg1: [-3,2,-2]: total=-3, pref: -3, -1, -3 -> max -1, suff: -2, 0, -3 -> max 0, best: max(-3,2,0)=2.
Seg2: [3,-2,3]: total=4, pref: 3, 1, 4 -> max 4, suff: 3, 1, 4 -> max 4, best: 4.
m=2. A1=-3. j=2: max_{i<2} (S_i - A_i) = S1 - A1 = 0 - (-3) = 3. Candidate = 3 + A1 + P2 = 3 -3 + 4 = 4. K_max = max(2,4)=4. Answer=4.
v=3: indices [4,6]. Segments: (0,3), (5,5).
Seg1: [-3,2,-2,-1]: total=-4, pref: -3, -1, -3, -4 -> max -1, suff: -1, -3, -1, -4 -> max -1, best: max(-3,2,0,-1)=2? Actually, subarrays: -3, 2, -1, 2-2=0, 2-2-1=-1, 2-1=1, 2-2-1=-1, etc. Max is 2.
Seg2: [-2]: total=-2, pref=-2, suff=-2, best=-2.
m=2. A1=-4. j=2: max_{i<2} (S_i - A_i) = S1 - A1 = -1 - (-4) = 3. Candidate = 3 + A1 + P2 = 3 -4 -2 = -3. K_max = max(2,-2)=2. Answer=2.
Overall max = 7. Correct.

So the algorithm works.

Now, we need to implement segment tree. We can also avoid segment tree by precomputing prefix and suffix Kadane tuples, and then we can query any interval in O(1) by combining prefix and suffix? Actually, we can precompute for every index the tuple for the prefix [0,i] and suffix [i,n-1]. Then for an interval [l,r], we can combine the prefix up to r and suffix from l? Not directly. But we can use a sparse table for range queries, or we can precompute the tuple for all intervals in O(n) using divide and conquer? Since we have up to 2e5 intervals, O((n+U) log n) is fine. But we can also do it in O(n) total by noting that we only need to query intervals that are "gaps" for each value. The gaps for a value v are defined by its indices. If we have the indices of v, we can compute the tuple for each gap by scanning from the start, but we need to avoid scanning the whole array for each v. However, we can precompute an array of the tuples for all prefixes and suffixes, and then for a gap [l,r], we can compute the tuple by merging the prefix [0,r] and the suffix [l,n-1]? That doesn't work because merging a prefix and a suffix that overlap is not correct. The standard trick: if we have the segment tree, we can query each gap in O(log n). With n=1e5, O(n log n) is fast enough.

Alternatively, we can precompute the tuple for every interval in O(n) using a stack? Not necessary. Let's stick with segment tree.

Implementation details:
- Use a segment tree with size n. Each node stores a tuple (total, pref, suff, best).
- For leaf i: total = nums[i], pref = suff = best = nums[i].
- Merge function as described.
- Query function returns the tuple for [l,r] inclusive. If l>r, return None or handle separately (we won't call with l>r).
- For each unique value, get its indices. Use a dictionary mapping value to list of indices. Since n=1e5, building this is O(n).
- For each value v:
   - indices = sorted list (they are naturally in order as we iterate).
   - prev = -1
   - segments = []
   - for idx in indices:
       if prev+1 <= idx-1: segment = (prev+1, idx-1); query tuple; append.
       prev = idx
   - if prev+1 <= n-1: segment = (prev+1, n-1); query tuple; append.
   - Note: if indices list is empty, that means v not in array? But we iterate over unique values, so each has at least one index.
   - Now we have a list of tuples. Let m = len(segments). If m == 0, that means the entire array is v? But then we cannot delete v because it would empty the array. So we should skip v if count(v) == n. In that case, indices length = n, and no segments. So we only consider v if count(v) < n.
   - Now compute the max for this v:
       max_k = max(t[3] for t in segments)
       if m == 1: candidate = max_k
       else:
           # Compute A array: cumulative sum of T
           T = [t[0] for t in segments]
           P = [t[1] for t in segments]
           S = [t[2] for t in segments]
           A = [0] * (m+1)
           for i in range(m): A[i+1] = A[i] + T[i]
           # Compute max_{j=1..m} ( max_{i<j} (S_i - A_i) + A_{j-1} + P_j )
           # Note: j is 1-indexed in this loop? Let's use 0-indexed.
           # For j from 1 to m-1 (since we need i<j):
           max_si_ai = S[0] - A[0]
           max_candidate = -inf
           for j in range(1, m):
               # Update max_si_ai with i=j? No, i<j, so we can update before using.
               # At j, we want max_{i < j} (S_i - A_i). We can maintain this as we go.
               # Initially, before j=1, max over i<1 is S[0]-A[0].
               candidate = max_si_ai + A[j-1] + P[j]
               if candidate > max_candidate: max_candidate = candidate
               # Now update max_si_ai with S[j] - A[j] for next j.
               val = S[j] - A[j]
               if val > max_si_ai: max_si_ai = val
           # But we also need to consider the case where the subarray is just a single segment? That's covered by max_k.
           # Also, we need to consider the case where the subarray spans from i to j but we might want to take the entire segment i and j, not just suffix/prefix. That is included because suffix could be the total sum of the segment, and prefix could be the total sum. So the formula covers it.
           # However, what about taking a subarray that starts in the middle of a segment and ends in the middle of the same segment? That's K_i.
           # What about taking a subarray that starts in the middle of segment i and ends in the middle of segment j, but we also include all full segments in between. That's exactly the formula: suffix of i (which can be any suffix, the best is the max suffix sum, which is the best sum of a suffix of that segment) plus sum of full segments plus prefix of j (best prefix). This is correct because if the optimal subarray spans multiple segments, the part in the first segment must be a suffix of that segment (since it starts somewhere in that segment and goes to the end), and the part in the last segment must be a prefix. The middle segments are fully included. And the best such sum is achieved by taking the maximum possible suffix of the first segment and maximum possible prefix of the last segment, and the sum of the middle segments. So the formula is correct.
           overall_v = max(max_k, max_candidate)
   - Keep track of global max.

- Also, the original max subarray sum is the best of the whole array: query segment tree on [0, n-1] to get K. That is the no-deletion case. So we can include that in the global max.

- Return global max.

Complexities: Building segment tree O(n). Building index map O(n). For each unique value, processing: number of segments is count(v)+1, but we only process non-empty ones. Total segments across all v is at most n + U, but we query each non-empty segment. Each query O(log n). So total O((n+U) log n). For n=1e5, log n ~17, so about 1.7e6 operations, fine.

We need to be careful with the case where a segment tuple has best (K) that is negative. Our max_candidate might be negative, but we should still consider it. Also, if m=1, we just take its K.

Edge cases: 
- n=1: array [x]. Original max = x. We can delete any value that is not the only element? Actually, we can delete x only if after deletion the array is non-empty. So we cannot delete x. So we can only not delete, or delete some other value that doesn't exist. So answer is x. Our algorithm: unique values: {x}. indices=[0]. count=1, which is n, so we skip (since count(v)==n). Original max = x. Correct.
- n=2: [1, -2]. Original max = 1. Can we delete -2? Then array becomes [1], max=1. Delete 1? Then array becomes [-2], max=-2. So answer=1. Algorithm: v=1: count=1 <2, indices=[0], segments: (1,1) = [-2]. tuple: T=-2, P=-2, S=-2, K=-2. m=1, answer = -2. v=-2: count=1 <2, indices=[1], segments: (0,0)=[1], tuple: T=1, P=1, S=1, K=1. m=1, answer=1. Global max = max(1, -2, 1) = 1. Correct.
- All negative: [-5, -2, -3]. Original max = -2. Deleting any value: if we delete -2, array becomes [-5,-3], max = -3. If we delete -5, array becomes [-2,-3], max = -2. So answer = -2. Algorithm: v=-5: indices=[0], segments: (1,2)=[-2,-3]. tuple: T=-5, P=-2, S=-3, K=-2. m=1, answer=-2. v=-2: indices=[1], segments: (0,0)=[-5], (2,2)=[-3]. Seg1: T=-5, P=-5, S=-5, K=-5. Seg2: T=-3, P=-3, S=-3, K=-3. m=2. A1=-5. j=2: max_{i<2} (S_i - A_i) = S1 - A1 = -5 - (-5) = 0. candidate = 0 + A1 + P2 = 0 -5 -3 = -8. K_max = max(-5, -3) = -3. overall = max(-3, -8) = -3. v=-3: similar, answer=-3. Original max = -2. Global max = max(-2, -2, -3, -3) = -2. Correct.

So the algorithm is correct.

Now, we need to implement the segment tree. We can use an iterative segment tree (like a sparse table?) or recursive. Since we need to query many intervals, a recursive segment tree is fine. But we can also use a segment tree that stores the tuple in an array, and query recursively. Complexity O(n) build, O(log n) query.

We need to be careful with the merge function for invalid intervals. We'll only query valid intervals.

Let's write the code.

Steps:
1. Read n and array.
2. Build segment tree.
3. Build dictionary: value -> list of indices.
4. Initialize global_max = query(0, n-1).best (original max).
5. For each value in dict:
   - indices = dict[value]
   - if len(indices) == n: continue  # cannot delete
   - segments = []
   - prev = -1
   - for idx in indices:
       l = prev + 1
       r = idx - 1
       if l <= r:
           t = query(l, r)
           segments.append(t)
       prev = idx
   - l = prev + 1
   - r = n - 1
   - if l <= r:
       t = query(l, r)
       segments.append(t)
   - m = len(segments)
   - if m == 0: continue  # should not happen if len(indices) < n
   - max_k = max(seg[3] for seg in segments)
   - if m == 1:
       current_max = max_k
   - else:
       T = [seg[0] for seg in segments]
       P = [seg[1] for seg in segments]
       S = [seg[2] for seg in segments]
       A = [0] * (m)
       A[0] = T[0]
       for i in range(1, m): A[i] = A[i-1] + T[i]
       max_si_ai = S[0] - A[0]  # A[0] is sum up to 0
       max_candidate = -10**18
       for j in range(1, m):
           candidate = max_si_ai + A[j-1] + P[j]
           if candidate > max_candidate: max_candidate = candidate
           val = S[j] - A[j]
           if val > max_si_ai: max_si_ai = val
       current_max = max(max_k, max_candidate)
   - if current_max > global_max: global_max = current_max
6. Return global_max.

We need to define the query function. The segment tree can be built as an array of size 4*n. Each node stores a tuple. For a leaf at position i, we store (nums[i], nums[i], nums[i], nums[i]). For internal node, we merge the two children.

Edge case: n=1. Build tree, query(0,0) works. dict has one value, len(indices)=1=n, so skip. global_max = nums[0]. Return.

Let's test on the example. We'll write a quick test in mind.

Now, we must ensure that the segment tree query handles the case where the interval is a single element correctly.

One more thing: The problem allows "at most once" operation, meaning we can also choose not to delete anything. So we must consider the original max. We already do that.

Time complexity: O(n log n) for queries, plus O(n) for the rest. Should be fast.

We can also optimize by noticing that we don't need a full segment tree if we precompute prefix and suffix Kadane tuples and use a sparse table for range minimum query on something? Actually, we can precompute the tuple for every interval in O(n) using the fact that the segments for a given v are disjoint and we can compute their tuples by scanning the array once per v? But that's O(n^2). So segment tree is good.

Let's code the segment tree.

We'll use a class SegTree:
- __init__(self, data): builds the tree.
- query(self, l, r): returns tuple for [l, r].

Merge function:
def merge(a, b):
    if a is None: return b
    if b is None: return a
    total = a[0] + b[0]
    pref = max(a[1], a[0] + b[1])
    suff = max(b[2], a[2] + b[0])
    best = max(a[3], b[3], a[2] + b[1])
    return (total, pref, suff, best)

In query, we recursively merge.

We need to handle the case where l > r, but we won't call it.

Now, write the solution.

We also need to import List from typing.

Let's write the final code.

Wait, we should double-check the merge formula for best: max(a[3], b[3], a[2] + b[1]). This is correct: a[2] is the best suffix of left, b[1] is the best prefix of right. The best subarray spanning both is the best suffix of left plus best prefix of right.

For pref: max(a[1], a[0] + b[1]). This is the best prefix of the combined interval: either entirely in left, or the entire left plus best prefix of right.

For suff: max(b[2], a[2] + b[0]). Similarly.

For total: a[0] + b[0].

Now, test on a small array: [1, -2, 3]
Leaves: (1,1,1,1), (-2,-2,-2,-2), (3,3,3,3).
Merge first two: a=(1,1,1,1), b=(-2,-2,-2,-2). total=-1, pref=max(1, 1-2=-1)=1, suff=max(-2, 1-2=-1)=-1, best=max(1,-2, 1-2=-1)=1. So ( -1, 1, -1, 1).
Merge with third: a=(-1,1,-1,1), b=(3,3,3,3). total=2, pref=max(1, -1+3=2)=2, suff=max(3, -1+3=2)=3, best=max(1,3, -1+3=2)=3. So overall: (2,2,3,3). The best subarray is 3, which is correct. The best prefix is 2 (1-2+3), best suffix is 3 (just 3). So correct.

Now, query an interval: say [1,2] for [-2,3]. Leaves: (-2,-2,-2,-2) and (3,3,3,3). Merge: total=1, pref=max(-2, -2+3=1)=1, suff=max(3, -2+3=1)=3, best=max(-2,3, -2+3=1)=3. So tuple (1,1,3,3). Correct: subarray [-2,3] has best subarray 3, best prefix 1, best suffix 3.

Now, in our algorithm, for a segment, we use this tuple.

One more check: in the per-v processing, when m=1, we just take max_k. But what if the segment has negative total, and we take a subarray that is a proper subsegment? That's exactly K. So correct.

What if m>=2, and we want to consider a subarray that is just a suffix of segment i and a prefix of segment i+1, but we don't include the full segment i+1? That's covered by the candidate with j=i+1. For j=i+1, A[j-1] = A[i], so candidate = max_{k < i+1} (S_k - A_k) + A[i] + P[i+1]. If we take k=i, we get S_i - A_i + A_i + P_{i+1} = S_i + P_{i+1}. This is the sum of the best suffix of i and best prefix of i+1. But what if the best suffix of i is not the entire segment i, and the best prefix of i+1 is not the entire segment i+1? That's exactly what we want. However, what if the optimal subarray starts in the middle of segment i and ends in the middle of segment j, but we don't take the best suffix of i? That can't be optimal because if we start earlier in i, we might include more positive elements, so the best suffix sum is the best possible sum for a suffix of i. Similarly for prefix. So taking the best suffix and best prefix is optimal.

But wait: what if the optimal subarray does not take the best suffix of i because the best suffix might include some negative prefix that is better to exclude? But a suffix of a segment is a contiguous block from some point to the end. The best suffix sum is the maximum sum among all suffixes. If we are taking a subarray that ends in segment j and starts in segment i, the part in segment i must be a suffix of segment i. The sum of that part is some suffix sum. The maximum possible sum for a suffix of i is exactly the best suffix sum. So we should take the best suffix sum. Similarly for the prefix of j. So the formula is correct.

Thus, the algorithm is sound.

Now, we need to code it efficiently. We can use an iterative segment tree to avoid recursion depth issues, but n=1e5, recursion depth log2(1e5) ~ 17, so recursion is fine. But Python recursion might have overhead. We can use an iterative segment tree. However, recursive is easier to code. Let's use a simple recursive segment tree with l,r parameters.

We'll define a method _build(node, l, r):
if l==r: self.tree[node] = (nums[l], nums[l], nums[l], nums[l])
else: mid=(l+r)//2; _build(node*2, l, mid); _build(node*2+1, mid+1, r); self.tree[node] = merge(self.tree[node*2], self.tree[node*2+1])

Query: _query(node, l, r, ql, qr):
if ql <= l and r <= qr: return self.tree[node]
if qr < l or r < ql: return None
else: left = _query(node*2, l, mid, ql, qr); right = _query(node*2+1, mid+1, r, ql, qr); return merge(left, right)

We need to handle None in merge: if left is None, return right, etc.

That's it.

Now, let's code the solution in the required format.

We need to import List from typing.

Let's write the code.</mm:think>### PLAN
We need the maximum subarray sum after optionally removing all occurrences of one value. The original max subarray sum is a baseline. For each value `v`, removing it splits the array into contiguous segments of elements `≠ v`. The best subarray in the resulting array is either entirely within one segment (Kadane on that segment) or spans multiple segments, taking a suffix of the first segment, full middle segments, and a prefix of the last segment. We can compute the tuple (total, best prefix, best suffix, best subarray) for any interval using a segment tree. For each `v`, we gather its segments, query their tuples in O(log n) each, and compute the max spanning sum in O(m) where m is the number of segments. Overall complexity is O(n log n).
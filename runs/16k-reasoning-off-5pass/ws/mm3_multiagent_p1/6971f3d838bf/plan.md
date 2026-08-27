We need to maximize subarray sum after optionally deleting all occurrences of one value `x` (or none). A subarray in the resulting array is a contiguous segment of the original array that does not contain the deleted value. So the answer is: max over all contiguous segments that contain no value which appears elsewhere in the segment that is fully deleted. But we can pick any `x` (or skip deletion), so the answer is simply the max subarray sum of the original array under the constraint that we may also allow subarrays that skip over occurrences of one value that appears both inside and outside the subarray? Let's think more carefully.

If we delete value `x`, a subarray in the resulting array corresponds to a contiguous block in original where no element equals `x`. Its sum is the sum of elements in that block. So for each candidate `x`, we want the max sum of a subarray containing no `x`. The global answer is max over `x` of that, and also the case of no deletion (which corresponds to any subarray).

Key observation: For any subarray `S` in original, if we choose `x` to be a value that appears outside `S` (or not at all in `S`), then `S` survives deletion. Therefore, the maximum subarray sum with at most one deletion equals the max subarray sum of the original array when we can ignore a value that appears anywhere as long as the chosen subarray has no `x`. Since we may also choose not to delete anything, the answer is at least the standard max subarray sum.

To compute this efficiently, observe that the answer is either (a) the standard Kadane max subarray sum, or (b) a subarray that has a single "bad" value appearing both inside and outside it that we can delete. Specifically, if the optimal subarray in the original array is "blocked" by some value `x` that appears both inside and outside the subarray, we could delete `x` to get an even better sum spanning across the `x` boundary. Actually, the optimal after deletion can be obtained by removing at most one value type entirely, but the subarray can be any contiguous region with no occurrences of that value.

Better approach: The answer is the maximum subarray sum where we may optionally exclude a value `x` that appears at least once outside the subarray as well (so deleting `x` doesn't empty the array). This is equivalent to: consider all subarrays; for each subarray, we can pick a value `x` that does NOT appear in the subarray but appears somewhere in the array; deleting `x` doesn't affect the subarray. So the max subarray sum is achievable without any constraint, because for any subarray we can pick an `x` not in it (if array length > subarray length, pick any element outside; if subarray = whole array, we must pick no deletion). So actually, the answer is just the max subarray sum of the original array... unless the whole array is the max subarray and we must pick a deletion (or not). Wait, but deletion can also help by removing negative values.

Let me reconsider with example: nums = [-3,2,-2,-1,3,-2,3]. The max subarray without deletion is [3,-2,3] = 4. But by deleting -2, the array becomes [-3,2,-1,3,3] and max subarray = 2+(-1)+3+3=7. Here the optimal subarray after deletion is [2,-1,3,3] which doesn't contain -2. In the original array, this subarray with -2 removed would span positions 1,3,4,5,6 (with -2 at position 2 and 5 removed). It's not contiguous in original.

So the trick is: we can pick one value `x` to delete globally, and the resulting subarray is a contiguous block in the original array that avoids all `x`. We want max sum over all such (x, contiguous block with no x).

This is equivalent to: for each value `v` that appears in the array, compute the max subarray sum of the array with all `v`'s removed (i.e., treat them as barriers, and we want a contiguous segment between consecutive `v`'s boundaries, or spanning across). The maximum over all `v` of this gives the answer.

For a specific `v`, the "segments" we can pick are intervals between consecutive `v`'s (open intervals). The sum of elements in such an interval is just a normal subarray sum where we forbid `v`. So for each `v`, the answer for that `v` is: max subarray sum over segments that don't contain `v`. The overall answer is max over `v` of that, plus also the case of no deletion (which is the global max subarray sum).

We need an efficient way. Key insight: The answer is either the global max subarray sum, OR it equals the max sum subarray that contains some value that appears exactly once? Hmm, let me think differently.

Let's denote the global max subarray sum as `M0` (Kadane). Consider the contribution of elements with value `v`. If we delete `v`, we remove all its occurrences. The new max subarray sum `M(v)` is computed on the array with `v`'s removed.

Observation: If `v` is not the unique minimum or doesn't appear in the optimal subarray structure, this can be larger.

Alternative approach using prefix sums and "best segment avoiding each value":

For each index `i`, let `prefix[i]` be sum of nums[0..i-1]. For a subarray `[l, r]` = sum prefix[r+1] - prefix[l].

For a fixed value `v`, valid subarrays are those that don't contain `v`. So between consecutive occurrences of `v` at positions `p1 < p2 < ... < pk`, valid subarrays are those entirely within (p_j + 1, p_{j+1} - 1) for each j, plus the prefix before p1 and suffix after pk. Max subarray sum restricted to such a region is just standard Kadane on that region. So `M(v)` is max over all these "gap" regions of their max subarray sum.

This is like: for each value `v`, we want max over gaps (intervals between consecutive v's, plus the two ends) of the max subarray sum in that gap.

Total work: if we naively for each v, scan its gaps, total work is O(n) per v in worst case if many distinct v. But we can do better.

Key insight: `M(v)` is the standard max subarray sum when treating `v` as a separator. Let `L[i]` = max subarray sum ending at `i` (Kadane forward), `R[i]` = max subarray sum starting at `i` (Kadane backward). Then for any subarray, its sum = max_{l,r} (prefix[r+1] - prefix[l]) etc.

For value `v` with positions `p1, ..., pk`, the max subarray not containing `v` is max of:
- Max subarray entirely before `p1`: which is `L[p1-1]` (max subarray sum ending at or before p1-1) = max over subarrays in [0, p1-1] = L[p1-1].
- Max subarray entirely after `pk`: = max over subarrays in [pk+1, n-1] = R[pk+1].
- For each j, max subarray entirely within (p_j, p_{j+1}): we need max subarray in [p_j+1, p_{j+1}-1]. This can be computed as max_{i in [p_j+1, p_{j+1}-1]} (max subarray sum ending at i) over that range, OR max subarray sum starting... Let's think.

The max subarray sum within [a, b] is: max_{l,r: a<=l<=r<=b} (prefix[r+1] - prefix[l]) = max_{r in [a,b]} (prefix[r+1] - min_{l in [a,r]} prefix[l]). Alternatively, we can use L: max subarray sum in [a,b] = max_{i in [a,b]} (best sum ending at i, where that subarray starts >= a). Let `L[i]` = max subarray sum ending at i (any start). We need a version where start >= a. Let `L_a[i]` = max subarray sum ending at i with start >= a. Then max in [a,b] = max_{i in [a,b]} L_a[i].

Hmm, this is getting complex. Let me think of a different approach.

**Approach: For each value v, M(v) = max over all subarrays that don't contain v.**

We can think of this as: a subarray [l, r] is "v-free" if no element in [l,r] equals v. We want max sum over all (v, [l,r]) such that [l,r] is v-free and v appears at least once in array (or v doesn't appear = no deletion).

Consider the subarray [l,r] in the original array. If it doesn't contain the value at position l-1 (if exists) or r+1 (if exists), then we can "extend" by picking v to be a value outside [l,r]. Specifically, if we pick v to be any value that appears in the array but NOT in [l,r], then [l,r] is a valid subarray after deleting v. Since the array has at least one element not in [l,r] (if [l,r] isn't the whole array), we can always find such a v (or pick no deletion). Therefore:

**If [l,r] is not the entire array, then there exists a v not in [l,r] (any value appearing outside), and the subarray [l,r] is valid after deleting v.**

Wait, but v must be a specific value, and deletion removes ALL occurrences of v. If v appears both inside and outside [l,r], then [l,r] would be invalid. So we need v that appears ONLY outside [l,r] (or not at all in [l,r] but somewhere in array).

So [l,r] is achievable iff there exists a value v such that v doesn't appear in [l,r] but v appears in the array (or we don't delete). If [l,r] != whole array, can we always find such v? Not necessarily! Consider nums = [1, 1, 1]. Any subarray of length < 3 contains only 1's, and 1 appears both inside and outside. If we delete 1, array becomes empty. So only subarray = whole array is valid (with no deletion). Max sum = 3.

But for nums = [1, 1, 1, 2], subarray [0,2] = [1,1,1] contains only 1. Value 2 is outside, so deleting 2 (which appears only outside [0,2]) keeps [0,2] intact. Sum = 3.

So the condition is: [l,r] is achievable if there exists a value v that is NOT in [l,r] but IS in the array (with the constraint that the array remains non-empty after deletion, i.e., v doesn't account for all elements).

Equivalently, [l,r] is NOT achievable only if every value in the array appears in [l,r]. This happens when [l,r] contains all distinct values of the array.

So the achievable subarrays are all subarrays EXCEPT possibly those that contain all distinct values of the array.

Wait, but we also need: if [l,r] contains all distinct values, can we still achieve it? Only if we don't delete anything. So yes, even if [l,r] contains all distinct values, [l,r] is achievable (with no deletion).

So actually, every subarray is achievable! (By picking v to be some value not in [l,r] if [l,r] doesn't contain all values, or no deletion if it does.)

But wait, that contradicts the example. Let me re-examine.

Example: nums = [-3, 2, -2, -1, 3, -2, 3]. The subarray that gives sum 7 is [2, -1, 3, 3] which in original is at indices 1, 3, 4, 5, 6 (not contiguous in original). So this subarray doesn't exist as a contiguous subarray of the original! It's a subarray of the modified array after deleting -2.

So I was confusing myself. The subarray must be contiguous in the MODIFIED array, not the original. A contiguous subarray in the modified array (after deleting x) corresponds to a contiguous subarray in the original array that contains no x.

So the achievable "subarrays" (as sets of original indices) are: for each x, contiguous intervals in original containing no x. So the set of achievable (interval, x) pairs is: (interval I, value x) where x doesn't appear in I, x appears in array, and array minus x's is non-empty.

To find max sum: for each achievable interval I (with no x in it), the sum is sum of elements in I. We want max over all such (I, x).

For a given interval I = [l, r] in original, the sum is fixed: S = sum(nums[l..r]). This interval is achievable iff there exists x not in I that appears in array. (Plus the constraint that array is non-empty after deleting x, but if x doesn't appear at all or appears outside, array remains non-empty as long as there's something left.)

So: interval I is achievable iff there exists a value x in the array such that x is not in nums[l..r].

If the set of values in [l,r] is a proper subset of all values in the array, then I is achievable.

If [l,r] contains all values in the array, then I is achievable only via no deletion.

So every interval is achievable (either by deletion of some x not in I, or no deletion).

Wait, but then the answer is just the max subarray sum of the original array! But the example says otherwise...

Let me recheck. Original array: [-3, 2, -2, -1, 3, -2, 3]. The subarray [1, 3, 4, 5, 6] = [2, -2, -1, 3, -2, 3] is NOT contiguous in original (indices 1, 2, 3, 4, 5, 6 are contiguous actually! indices 1 to 6: nums[1]=2, nums[2]=-2, nums[3]=-1, nums[4]=3, nums[5]=-2, nums[6]=3). Sum = 2-2-1+3-2+3 = 3. Not 7.

The subarray giving 7 is in the modified array after deleting -2: modified = [-3, 2, -1, 3, 3] (indices 0, 1, 3, 4, 6 in original). This is contiguous in modified: positions 1, 2, 3, 4 in modified = [2, -1, 3, 3], sum = 7. In original indices, this is 1, 3, 4, 6 - not contiguous!

So the "interval" in original corresponding to this subarray is NOT a single interval; it's a union of intervals separated by -2's. Specifically, it's [1,1] ∪ [3,4] ∪ [6,6] (gaps at indices 2, 5 where -2 occurs).

So the achievable structures in the original are not just intervals, but rather: for each x, a set of "gaps" between x's, and the subarray is one of those gaps (a single contiguous region in modified = a single gap in original).

Wait, a subarray in modified is contiguous in modified. In original, this corresponds to indices that, after removing x's, form a contiguous range. This means in original, the indices form a range [l, r] such that within [l,r], the x's are removed but [l,r] is still "one piece" in modified. For [l,r] to map to a single contiguous piece in modified, we need: [l,r] in original, after removing all x in [l,r], the remaining elements are at positions that, in modified array, occupy a contiguous range. 

Let me think again. Modified array has elements at original positions not equal to x. In modified, a subarray is a contiguous range of modified positions. The corresponding original indices are: some subset of positions not equal to x, that are consecutive in the modified array. This means: pick l' and r' in modified, then original indices are those in [l, r] (original) that are not x, where [l,r] is the smallest original range covering modified positions l' to r'. 

Specifically, if modified subarray starts at modified position p and ends at modified position q, then the original range is from the original index of modified position p, to the original index of modified position q. This range [l,r] in original has the property that all non-x elements in [l,r] correspond to modified positions p..q, and there are no x's in [l,r] at the "edges" that would split it... Actually, any x in [l,r] would be a "gap" in modified. So [l,r] contains some x's, and the modified subarray consists of the non-x elements between two x's (or before the first x, or after the last x).

So: a modified subarray corresponds to choosing a value x, and then choosing a subarray in the "x-stripped" array, which is a contiguous block of non-x elements. In original, this is a range [l,r] such that:
- The first element in [l,r] (nums[l]) is not x (or l is such that the first non-x in [l,r] is at position l).
- The last element in [l,r] (nums[r]) is not x.
- Within [l,r], the non-x elements form a contiguous block in the stripped array.

For this to be a single contiguous block in stripped array, we need: the non-x elements in [l,r] have no "gap" larger than... actually, they are just the non-x elements in [l,r]. If we take any [l,r] in original, the non-x elements in [l,r], when listed in order, form a contiguous subarray of the stripped array if and only if... hmm, this is always true! Because the stripped array is just original with x's removed, so the non-x elements in [l,r] appear consecutively in stripped array (in the same order) as long as we don't have x's at the boundary.

Wait, the stripped array has all non-x elements in order. The non-x elements in [l,r] are a subset. For them to be contiguous in stripped array, there should be no non-x element outside [l,r] that appears "between" them in stripped. Since stripped is in order, the non-x elements in [l,r] are at positions in stripped corresponding to original positions in [l,r]. They are contiguous in stripped iff the first non-x in stripped that is >= position of nums[l] (in original) is the one at original l (if nums[l] != x), and similarly for r.

Actually, let me think of it as: the stripped array has a sequence of non-x elements. A subarray of stripped is a contiguous subsequence. This corresponds to: pick a start position in stripped (say, the k-th non-x element) and end position (m-th non-x element). The original indices are the positions of the k-th through m-th non-x elements. This set of original indices is a union of intervals (the gaps between x's), specifically the intervals from the k-th non-x to the (k+1)-th non-x minus 1, etc. No wait.

Let me index non-x elements. Let positions of non-x be p_1 < p_2 < ... < p_M. A subarray of stripped from index a to b corresponds to original positions p_a, p_{a+1}, ..., p_b. The original range covering all these is [p_a, p_b]. Within [p_a, p_b], the non-x elements are exactly p_a, ..., p_b, and the x elements are those at positions in (p_a, p_b) that are x. The original range [p_a, p_b] might contain x's at the "ends" if p_a is right after an x or p_b is right before an x, but the point is: [p_a, p_b] in original is a range that starts and ends with non-x, and contains some x's in between (or none).

So: a stripped subarray corresponds to an original range [l, r] where nums[l] != x, nums[r] != x, and [l,r] may contain x's. The sum of the stripped subarray is sum of non-x elements in [l,r], which equals sum of all elements in [l,r] minus (count of x in [l,r]) * x, but since x is the value, sum is sum(nums[l..r]) - x * (number of x in [l,r]).

Hmm, this is getting complicated. Let me re-approach.

The modified array (after deleting x) is original with x's removed. A subarray of modified is a contiguous range in modified. Let's say it has sum S. This S equals the sum of original elements in some "region" of original that, when x's are removed, becomes contiguous. 

Region R in original: a set of consecutive modified positions. This corresponds to: find the first and last original positions, say L and R_idx. The modified subarray includes all non-x elements with original positions in [L, R_idx]. Its sum is sum of nums[i] for i in [L, R_idx] with nums[i] != x, which is sum(nums[L..R_idx]) - x * (count of x in [L..R_idx]).

But we need the modified subarray to be exactly the non-x elements in [L, R_idx] with no "extra" non-x elements. For this, we need: the non-x element just before L in original (if any) is not included, meaning the element at L-1 (if exists) is either x or doesn't exist, AND we want to start at the first non-x in [L, R_idx]. Similarly, R_idx is the last non-x. So: L is chosen such that either L=0 or nums[L-1]=x (so that the non-x elements in [L, R_idx] start cleanly), and R_idx is chosen such that either R_idx=n-1 or nums[R_idx+1]=x (clean end).

Wait, that's too restrictive. The modified subarray can start at any non-x position. If we start at original position p (where nums[p]!=x), the modified subarray goes from the non-x at p to the non-x at q. This means in original, the range is [p, q], and we need nums[p]!=x, nums[q]!=x, and within [p,q], all non-x elements are included (and x's are skipped in modified). The sum is sum of non-x in [p,q].

So: for a fixed x, the achievable sums are: for all pairs (p, q) with p <= q, nums[p] != x, nums[q] != x, the sum of non-x elements in [p, q], where "non-x elements in [p,q]" means all elements in [p,q] except those equal to x.

The sum is: sum(nums[p..q]) - x * cnt_x(p, q), where cnt_x(p,q) is number of x's in [p,q].

We want max over x of max over (p,q) of [sum(nums[p..q]) - x * cnt_x(p,q)], with constraints nums[p]!=x, nums[q]!=x.

This is a more complex optimization.

Alternative view: Think of it as, for each x, we want the max subarray sum in the "x-modified" array. The x-modified array is original with x's treated as... well, in the stripped array, a subarray is a range of non-x elements. 

Let me try yet another angle. 

**Let `f(x)` = max subarray sum after deleting all x's.**

We can compute f(x) for each x. The answer is max(f(x)) over all x, and also M0 (no deletion).

For a specific x, the stripped array has length m = n - freq(x). A subarray of stripped is a contiguous range. The max subarray sum of stripped is just Kadane on the stripped array. But computing f(x) for all x is expensive if done naively.

**Key insight:** f(x) = max subarray sum of the array where x's are "removed" (concatenating the gaps). This is the same as: max over gaps of (max subarray sum in that gap). A gap is a maximal contiguous region of non-x elements.

Wait, a subarray of the stripped array is a contiguous range of stripped positions, which corresponds to: pick a start in some gap, pick an end in some (possibly same) gap, and take all non-x elements in between. This might span multiple gaps.

For example, if x is at positions p1, p2, p3, the gaps are [0, p1-1], [p1+1, p2-1], [p2+1, p3-1], [p3+1, n-1]. A stripped subarray could span, say, from gap [p1+1, p2-1] to gap [p2+1, p3-1], skipping the x at p2. The original positions would be [p1+1, p3-1] \ {p2} = [p1+1, p3-1] minus the x at p2. The sum is sum of all elements in [p1+1, p3-1] except the x at p2.

So the "span" in original is from l to r where l is in one gap, r is in another (or same) gap, and [l,r] contains some x's (which are skipped in stripped). The sum is sum(nums[l..r]) - x * (count of x in [l,r]).

To maximize this, for each x, we want to find l, r (with nums[l]!=x, nums[r]!=x) maximizing sum(nums[l..r]) - x * cnt_x(l,r).

This is equivalent to: let g(i) = prefix[i+1] - x * (number of x in [0,i]). Then sum(nums[l..r]) - x * cnt_x(l,r) = g(r) - g(l-1). We want max of g(r) - g(l-1) over l<=r with nums[l]!=x, nums[r]!=x.

Constraint: l <= r, nums[l]!=x, nums[r]!=x.

Without the constraint on l,r, max of g(r) - g(l-1) is max(g) - min(g) over the array (standard max subarray on g). But we have the constraint that the corresponding [l,r] has nums[l]!=x and nums[r]!=x, i.e., l is not an x position, r is not an x position.

Hmm, let g(i) for i=0..n-1: g(i) = sum(nums[0..i]) - x * cnt_x(0, i). Then sum of stripped subarray corresponding to original [l,r] is g(r) - g(l-1) (with g(-1)=0).

We want max over 0<=l<=r<=n-1, nums[l]!=x, nums[r]!=x, of g(r) - g(l-1).

If we define h(i) = g(i-1) for i>=1, h(0) = 0, then we want max_{l,r: nums[l]!=x, nums[r]!=x, l<=r} (g(r) - h(l)).

This is like: for each r with nums[r]!=x, g(r) - min_{l<=r, nums[l]!=x} h(l).

Let min_h = min over l in [0, r] with nums[l]!=x of h(l) = g(l-1). We want max over r (nums[r]!=x) of g(r) - min_h_up_to_r.

If we process r from 0 to n-1, maintaining min_h = min of h(l) for l<=r with nums[l]!=x, and track max of g(r) - min_h for r with nums[r]!=x.

But wait, this gives the max over valid (l,r). However, we also need to consider the case where the "subarray" is just a single element or empty? The problem says non-empty subarray. Also, we need to ensure the array is non-empty after deletion, but since we only consider x that appears, and we need some element left, which is true if there's at least one non-x element. If all elements are x, then deletion makes array empty, invalid. We can handle this edge case.

Wait, but in the above, we're computing f(x) = max stripped subarray sum. The stripped array is non-empty (since we need at least one non-x). If all elements are x, we can't delete x (array becomes empty), so we skip or handle.

Also, the "subarray" in stripped can be the entire stripped array, corresponding to l=first non-x, r=last non-x in original, with all x's in between skipped.

Hmm wait, but the problem says the subarray is in the resulting array. The resulting array is the stripped array. A subarray of stripped is a contiguous range. So we want the max subarray sum of the stripped array.

Max subarray sum of stripped = max_{contiguous range in stripped} sum. This is just Kadane on stripped. And we can compute it as: for each position in stripped, maintain current max ending here, etc. But stripped is obtained by removing x's, so we can compute it on the fly.

Actually, max subarray sum of the array with x's removed = max_{l,r: nums[l]!=x, nums[r]!=x, and [l,r] contains no x at the "endpoints" but can contain x inside} (sum(nums[l..r]) - x * cnt_x(l,r)). Hmm wait, I need to be careful.

Let me re-derive. Stripped array S has S[k] = nums[p_k] where p_1 < p_2 < ... < p_M are positions of non-x. A subarray S[a..b] (1-indexed) has sum sum_{k=a}^b nums[p_k] = sum of nums at positions p_a, p_{a+1}, ..., p_b. In original, this is positions p_a to p_b, excluding x's (which are at positions in (p_a, p_b) that are x). The sum is sum_{i=p_a}^{p_b} nums[i] - x * cnt_x(p_a, p_b).

Yes, so the sum is g(p_b) - g(p_a - 1) as defined.

And we want max over 1<=a<=b<=M of S[a..b] = max over p_a, p_b (non-x positions) of g(p_b) - g(p_a - 1).

Since p_a and p_b range over non-x positions, and a<=b means p_a <= p_b, we have:
f(x) = max_{p_b: non-x} ( g(p_b) - min_{p_a <= p_b, p_a non-x} g(p_a - 1) )
     = max_{r: non-x} ( g(r) - min_{l in L(r)} g(l-1) )

where L(r) = {l : 0<=l<=r, nums[l]!=x}. This is computable in O(n) per x.

But we have up to n distinct x, so O(n^2) is too slow.

We need a global approach. The answer is max_x f(x) and also M0.

Note: M0 = max_{l<=r} (prefix[r+1] - prefix[l]) = max_r prefix[r+1] - min_l prefix[l].

Hmm, let me think of the answer differently.

**The answer is max_{l<=r} (prefix[r+1] - prefix[l] - x * (cnt_x(l, r))) for some x, OR the no-deletion case.**

Wait, no, f(x) is computed as above, and we take max over x. Plus no-deletion (which is like x = a value that doesn't exist, or just M0).

Actually, the no-deletion case is M0 = max subarray sum. This is also covered if we consider "deleting" a value that doesn't exist, but the problem says at most one operation, and we can choose to not operate. So answer = max(M0, max_x f(x)).

Now, max_x f(x) = max_x max_{r: nums[r]!=x} ( g_x(r) - min_{l<=r, nums[l]!=x} g_x(l-1) ), where g_x(i) = prefix[i+1] - x * cnt_x(0, i).

Let me denote for each position i, prefix[i] = sum(nums[0..i-1]) (prefix[0]=0).

cnt_x(0, i) = number of x in [0, i]. Let's call it c_x(i) for the prefix.

g_x(i) = prefix[i+1] - x * c_x(i), for i=0..n-1. Note prefix[i+1] = sum(nums[0..i]).

g_x(-1) is not defined; for the formula, when l=0, we use g_x(-1) = 0? Let me check: p_a = l, p_b = r. g(r) = prefix[r+1] - x * cnt(0,r). g(l-1) for l=0 is g(-1) = 0 (since prefix[0] - x*0 = 0). For l>0, g(l-1) = prefix[l] - x * cnt(0, l-1).

Difference: g(r) - g(l-1) = (prefix[r+1] - x*cnt(0,r)) - (prefix[l] - x*cnt(0,l-1)) = (prefix[r+1] - prefix[l]) - x * (cnt(0,r) - cnt(0,l-1)) = sum(nums[l..r]) - x * cnt(l, r). Yes, correct.

So f(x) = max_{0<=l<=r<=n-1, nums[l]!=x, nums[r]!=x} (sum(nums[l..r]) - x * cnt_x(l,r)).

This is a bit complex. Let me think if there's a simpler characterization.

**Alternative: Think of the "best" subarray after deletion.**

The subarray in the modified array is a contiguous range in stripped. Its sum is the sum of elements in some original range [l, r] minus x times the count of x in [l,r], with nums[l] != x, nums[r] != x (clean boundaries), and [l,r] can be any such range.

We can rewrite: sum(nums[l..r]) - x * cnt_x(l,r) = sum_{i in [l,r], nums[i]!=x} nums[i]. This is the sum of non-x elements in [l,r].

Note that if we fix l and r (with nums[l], nums[r] != x), the sum depends on x only through the x's in [l,r] (which are subtracted as x each).

For a fixed [l,r], the value as a function of x is: S(l,r) - x * k(l,r), where S = sum(nums[l..r]), k = cnt_x(l,r). This is linear in x with slope -k(l,r).

If k(l,r) > 0 (there are x's in [l,r]), then as x increases, the value decreases. If k=0, value is constant in x.

We want to choose x to maximize this, but x is discrete (integer in nums). For a fixed [l,r], the best x is one that minimizes x * k(l,r) subject to x appearing in array and nums[l], nums[r] != x.

If k=0, any x works (value = S(l,r)), and we can pick any x not in [l,r] to make it valid. The value is S(l,r).

If k>0, we want small x (to subtract less) but x must not be in [l,r] at positions l or r (but can be inside). Actually, x can be any value, as long as deleting x keeps the array non-empty. Deleting x removes all x's. The stripped array is non-empty as long as not all elements are x. If the original array has only x, we can't delete x. Otherwise, we can.

Wait, I realize: the constraint is that the array remains non-empty. So if all elements are equal to x, we cannot choose x (deletion would empty the array). But we can choose no deletion.

Also, for the subarray to be valid, the stripped array must contain it, and the stripped array is non-empty. So we need at least one non-x element. If [l,r] contains only x's, stripped subarray is empty, invalid. So we need nums[l] != x (or r>l with non-x inside, but l and r must be non-x for clean boundaries). Actually, if [l,r] has non-x elements, then l can be at a non-x position. We need l and r to be non-x for the boundaries.

Let me think of the answer as: max over (x, [l,r]) of sum_{i in [l,r], nums[i]!=x} nums[i], with [l,r] having nums[l]!=x, nums[r]!=x, and the array having at least one non-x (so stripped is non-empty).

Equivalently, since the sum only depends on the non-x elements in [l,r], and [l,r] is determined by the first and last non-x, we can say: pick a "run" in the stripped array. The stripped array is original with x's removed. A subarray is a range in stripped.

I think the cleanest way is: for each x, f(x) = max subarray sum of the sequence obtained by removing x. Compute f(x) efficiently for all x? That seems hard.

But the problem has n=1e5, so O(n log n) or O(n sqrt(n)) might work, but O(n * distinct) is too slow.

Let me think about the structure. The answer is either:
1. M0 (no deletion): standard max subarray.
2. Some f(x) for x in nums.

Note that f(x) is the max subarray sum of the "x-stripped" array. 

Observation: The max subarray sum of an array is >= any single element, and has properties. For the stripped array, f(x) is the max subarray sum of a sub-sequence (the non-x elements). But it's not a subsequence in the usual sense; it's the array with x's removed, and we take a contiguous subarray of that, which corresponds to a "subarray with holes" in original (specifically, a range [l,r] in original, and we take all non-x in it).

Hmm, let me think of the problem as: we have nums. We can "delete" one value. The answer is the max over all "contiguous in stripped" sums.

Another idea: For each position i, consider it as the "boundary". 

Let me search for the pattern. The answer is max of:
- M0
- For each x, f(x)

f(x) = max stripped subarray sum. The stripped subarray corresponding to original [l,r] (nums[l]!=x, nums[r]!=x) has sum = sum(nums[l..r]) - x * cnt_x(l,r).

We can write this as: for each [l,r], the contribution is S(l,r) - x * k. For this to be the max for some x, we need to choose x optimally. For fixed [l,r], max_x (S - x*k) where x is in the set of values in the array, x != nums[l], x != nums[r] (clean boundaries), and stripping x leaves array non-empty. 

If k=0 (no x in [l,r]), then S is achieved for any x not in {nums[l], nums[r]} (and not making array empty). Since the array has other elements, we can find such x. So S(l,r) is achievable for any [l,r] with k=0, i.e., [l,r] contains no x. But x can be chosen to be a value not in [l,r]. So any [l,r] is achievable with sum S(l,r) if there exists a value not in [l,r]. Since the array has values outside [l,r] (unless [l,r] is the whole array), we can pick x outside. If [l,r] is the whole array, k=0 for any x not in array, but x must be in array (we delete an existing value). Hmm, if [l,r] = whole array, we want a stripped subarray that is the whole stripped array. The sum is S(0,n-1) - x * k(0,n-1) where k = freq(x). We want to choose x to maximize S_total - x * freq(x), i.e., minimize x * freq(x). 

This is getting complicated. Let me look for a different approach.

**Key realization**: The maximum subarray sum after deleting x is the same as the maximum subarray sum of the array where we replace x with... no.

Let me think of small cases. 
- If all elements are positive, M0 = sum, which is the max. Deleting anything reduces sum. So answer = M0.
- If there's a single negative element, deleting it (if it's the only negative and the min) might help. But standard max subarray already skips it.

Actually, for the standard max subarray (Kadane), we find the max sum contiguous subarray. The issue is when the optimal subarray is "split" by a value that we want to delete. 

Specifically, the optimal after deletion might be a subarray that, in the original, is not contiguous because of the deleted value. This subarray is the union of the non-x elements in some original range [l,r]. Its sum is sum of non-x in [l,r].

This is equivalent to: pick an original range [l,r], and the sum is sum(nums[l..r]) - x * cnt_x(l,r). We can also write it as: for each i in [l,r], if nums[i]==x, skip; else add. 

Note that if we "merge" the two sides of an x, the sum is the sum of the two sides. So the optimal after deleting x is max over [l,r] of (sum of non-x in [l,r]), which can span multiple gaps.

This is like: we have an array, we pick one value to "remove" (make invisible), and we find the max sum of a contiguous block in the remaining sequence. This is equivalent to: max over l<=r of (sum(nums[l..r]) - x * cnt_x(l,r)) with the constraint that l and r are at non-x positions (or rather, the block in stripped has boundaries, so the first and last element in the block are non-x, meaning original positions l and r have nums[l]!=x, nums[r]!=x).

Hmm wait, is the constraint that l and r are non-x? In the stripped array, a subarray S[a..b] corresponds to original positions p_a to p_b where p_a, p_b are non-x (since a, b index into non-x positions). Yes, so l=p_a and r=p_b are non-x positions.

So f(x) = max_{0<=l<=r<=n-1, nums[l]!=x, nums[r]!=x} (sum(nums[l..r]) - x * cnt_x(l,r)).

For the overall answer A = max(M0, max_x f(x)).

Now, note that f(x) for x can be computed if we know for each x. But we need an efficient global method.

**Idea**: The answer is the max subarray sum of the array under the operation of removing one value type. This is similar to "max subarray sum after removing at most one element" but here we remove a value type.

Let me think of the array as having "colors" (values), and we can remove all elements of one color. The max subarray sum of the remaining is what we want.

For a fixed color x, the max subarray sum of the non-x elements (concatenated) is f(x). We want max_x f(x).

**Approach using prefix sums and considering each x as a "candidate for deletion" based on the optimal subarray.**

For the optimal subarray in the original (M0), say it achieves sum S0 at [l0, r0]. If we can "improve" by deleting some x, the new sum is S0 - x*k + (sum of non-x in [l0,r0])? Hmm no.

Let me think about which x to delete. The value x that is "bad" and appears in the middle of what would be the optimal subarray.

Consider the following: the answer is max over (x, [l,r]) of sum_{i in [l,r], nums[i]!=x} nums[i]. This is sum(nums[l..r]) - x * cnt_x(l,r).

For fixed l,r, this is maximized over x by choosing x to minimize x * cnt_x(l,r) subject to x != nums[l], x != nums[r] (clean boundaries) and x appears in array (so deletion is valid, i.e., array remains non-empty; if x accounts for all elements, skip).

If cnt_x(l,r) = 0, then x * 0 = 0, so any x works. The value is sum(nums[l..r]). We can achieve this with any x not in [l,r] (and present in array, or not present - wait, x must be present for deletion, unless we don't delete. For no deletion, we just get sum(nums[l..r]) directly, which is <= M0. So the no-deletion case gives M0, which is max over [l,r] of sum(nums[l..r]) = M0.

So the "deletion" case gives values sum(nums[l..r]) - x*k for k>=1, and we choose x to minimize x*k. For fixed l,r with k=cnt_x(l,r)>0, the best x is the smallest value v such that v != nums[l], v != nums[r], and v appears in array with frequency (k times in [l,r] and at least once in array, with stripping leaving non-empty).

The smallest such v. If nums[l] and nums[r] are small, v could be the next smallest. This is hard to optimize globally.

**Alternative angle**: The answer is max_{l,r} (sum(nums[l..r]) - min_{x: clean} x * cnt_x(l,r)) ... no.

Let me think of the answer as the max over all "valid" (x, interval) of the stripped sum. 

**Crucial insight**: The max subarray sum after deletion is either:
(a) M0, the standard max subarray sum, OR
(b) The max subarray sum of the array with some value x removed, which is a "subarray" that in original has one "type" of element removed.

This is equivalent to: max_{l<=r} (sum of non-x in [l,r]) for some x.

**New idea**: Consider the contribution of each element. The answer is the max subarray sum in a "compressed" sense.

Let me try to think of it as: for each adjacent pair of same-valued elements, or something.

Actually, here's a cleaner formulation. The answer A satisfies:
A = max( M0, max_{x in nums} f(x) )
where f(x) = max stripped subarray sum.

f(x) = max_{l<=r, nums[l]!=x, nums[r]!=x} (sum(nums[l..r]) - x * cnt_x(l,r)).

Let me define for each position i a "value" based on x. Hmm.

**Think of the answer as the max over all "merge" operations.**

The operation of deleting x merges all gaps between x's. The max subarray after deletion is the max sum of a contiguous block in the merged array. A block in merged corresponds to a range in original. The sum is the sum of non-x in the range.

**Connection to standard problems**: This is like finding the max subarray sum when we can "remove" all occurrences of one value. This is known as the "max subarray sum after removing a value" problem.

I recall that the solution involves computing, for each unique value x, the max subarray sum avoiding x, and taking the global max. But we need to do it efficiently.

**Key lemma**: The answer is max( M0, max_{unique x} f(x) ). And f(x) can be related to prefix sums with x.

Let me try to compute f(x) for all x efficiently using the fact that we only care about the max.

For a fixed x, f(x) = max_{r: nums[r]!=x} [ g_x(r) - min_{l in [0,r], nums[l]!=x} g_x(l-1) ], with g_x(-1)=0, g_x(i) = prefix[i+1] - x * c_x(i) for i=0..n-1.

The min over l<=r, nums[l]!=x of g_x(l-1). Note g_x(l-1) for l>=1 is prefix[l] - x*c_x(l-1). For l=0, g_x(-1)=0. So min_{l in [0,r], nums[l]!=x} g_x(l-1) = min( 0, min_{l in [1,r], nums[l]!=x} (prefix[l] - x*c_x(l-1)) ).

And c_x(l-1) = number of x in [0, l-1].

This is still O(n) per x.

**Is there a way to see that the answer is simply M0, or a specific value?**

No, the example shows it's not M0.

Let me think about the structure of f(x). For x with positions p1<p2<...<pk, the stripped array has k+1 gaps: [0,p1-1], [p1+1,p2-1], ..., [pk+1,n-1]. A stripped subarray is a contiguous range in stripped, which can span multiple gaps. The sum is the sum of all elements in the spanned range in original minus x*k' where k' is the number of x in the spanned range (which are the p_i's strictly between the first and last gap). 

Actually, a stripped subarray from gap j to gap j' (j<=j') spans original range [start_j, end_{j'}] where start_j is the first index of gap j (or 0 if j=0 meaning before first x, but gap 0 is [0,p1-1] if p1>0, else empty). Hmm, the gaps are between x's. Let me define: before first x, between x's, after last x. A stripped subarray from the a-th non-x to the b-th non-x spans from the position of a-th non-x to position of b-th non-x. The x's inside are those with positions in (pos_a, pos_b). The sum is sum(nums[pos_a..pos_b]) - x * (number of x in (pos_a, pos_b)).

To maximize f(x), we consider all such spans. This is like: for each gap, the best "prefix sum" ending in that gap, and combine with "suffix sum" starting in another gap.

Specifically, f(x) = max over (a, b) with a<=b of (sum from a-th to b-th non-x). The sum from a-th to b-th non-x = (sum of elements from pos_a to pos_b) - x * cnt_x(pos_a, pos_b).

Let me define for each non-x position p, the "value" of the span from a fixed point. Alternatively, think of the cumulative sum along non-x positions.

Let non-x positions be q_1 < q_2 < ... < q_M. Define S(k) = sum of nums[q_1..q_k] = sum of first k non-x elements. Then the sum from q_a to q_b is S(b) - S(a-1). This is the stripped subarray sum.

So f(x) = max_{1<=a<=b<=M} (S(b) - S(a-1)) = max_b S(b) - min_{a<=b} S(a-1) = max_{1<=b<=M} S(b) - min_{0<=a-1<=b-1} S(a-1).

This is exactly the max subarray sum of the stripped array (Kadane on the sequence of non-x values). The stripped array is the sequence of non-x values in order.

So f(x) = max subarray sum of the array (nums with x's removed).

This is a clean result: f(x) = max subarray sum of the sequence obtained by deleting all x.

Now, to compute max_x f(x) efficiently, note that the stripped array depends on x. For different x, different elements are removed.

**Observation**: f(x) only depends on the positions of x, not on the values of other elements. 

**Idea**: For the max subarray sum of a sequence, it equals the max over i of (max prefix sum up to i) - (min prefix sum before i). 

For the stripped array (non-x values in order), let the values be v_1, v_2, ..., v_M where v_k = nums[q_k]. The prefix sums P(k) = sum_{j=1}^k v_j. Then f(x) = max_{1<=b<=M} P(b) - min_{0<=a-1<=b-1} P(a-1) = max_b (P(b) - min_{a<=b} P(a-1)).

Equivalently, f(x) = max subarray sum of v_1..v_M.

Now, P(b) = sum of nums at non-x positions up to q_b. Let's express in terms of original prefix.

P(b) = sum_{i <= q_b, nums[i]!=x} nums[i] = prefix[q_b+1] - x * c_x(q_b).

So P(b) is exactly g_x(q_b) as before.

And P(a-1) for a>=1 is g_x(q_{a-1}), and P(0)=0 = g_x(-1).

So f(x) = max_{b} (P(b) - min_{a<=b} P(a-1)) with P(0)=0.

This is the standard max subarray on the stripped sequence. To compute it, we can run Kadane on the stripped sequence, or use the prefix min method.

But we want max over x. 

**Global approach**: 

Note that the answer A = max( M0, max_x f(x) ). And M0 is the max subarray sum of original. f(x) is the max subarray sum of stripped_x.

Consider the "merged" value: for each x, the stripped array is the original with x's removed. The max subarray of stripped is a contiguous range in stripped, which in original is a range [l,r] with nums[l]!=x, nums[r]!=x, and the sum is sum of non-x in [l,r].

**Key insight for efficient computation**: The answer is the max over all [l,r] and x of (sum of non-x in [l,r]). This is sum(nums[l..r]) - x * cnt_x(l,r).

For fixed [l,r], max_x (sum - x*k) where k=cnt_x(l,r). We want to minimize x*k. 

Case 1: k=0. Then x*k=0 for any x, so value = sum(nums[l..r]). The max over [l,r] of this with k=0 is max_{l,r: cnt_x(l,r)=0 for some x} sum. But we can achieve sum(nums[l..r]) for any [l,r] by choosing x not in [l,r] (if exists) or no deletion. Specifically, for any [l,r] that is not the whole array, pick x not in [l,r] (exists since there are elements outside). Then k=0 for this x, and the value is sum(nums[l..r]). Also, for [l,r] = whole array, we can not delete, getting M0 = sum(nums[0..n-1]) which is sum(nums[l..r]) for l=0,r=n-1.

Wait, but for [l,r] not whole array, we need x present in array and not in [l,r]. Such x exists because there are elements outside [l,r], and we can pick x to be any value among those. So yes, for any [l,r] that is not the whole array, we can achieve sum(nums[l..r]) by deleting an x that is outside [l,r].

Therefore, the set of achievable values includes sum(nums[l..r]) for every [l,r] (with the whole array via no deletion, others via deleting an outside value). 

So max_{achievable} = max_{[l,r]} sum(nums[l..r]) = M0?

But that contradicts the example! In the example, 7 > M0 = 4. So there must be an achievable value > M0, which means there is some (x, [l,r]) with k>0 giving sum > M0.

In the example, x=-2, [l,r] = [1,6] (original), sum(nums[1..6]) = 2-2-1+3-2+3 = 3, k=cnt_{-2}(1,6) = 2 (at positions 2,5), so value = 3 - (-2)*2 = 3+4 = 7. And M0=4. So yes, k>0 gives larger value when x is negative.

So the deletion helps when x is negative and we have k>0: subtracting x*k (negative times positive) adds a positive amount. Specifically, value = S + |x|*k for negative x. So the gain is |x|*k.

So the answer is max( M0, max_{x<0, [l,r] with nums[l]!=x, nums[r]!=x, k=cnt_x(l,r)>0} (S(l,r) - x*k) ).

Since -x = |x| for negative x, this is S(l,r) + |x| * k.

For x>0, deleting x subtracts x*k, which reduces the sum, so it's bad (unless k=0, but then S(l,r) <= M0 usually). Wait, if k=0, value = S(l,r) <= M0, so no gain. If k>0, value = S - x*k < S <= ... hmm, S could be large but subtracting x*k makes it smaller. Could it still be > M0? Only if S - x*k > M0. Since S <= sum of [l,r] and M0 is the max, it's possible that S - x*k > M0 if x is small. But for x>0, x*k>0, so S - x*k < S. And S <= prefix[r+1]-prefix[l] for some l,r. M0 is the max of prefix[r+1]-prefix[l]. So S - x*k < S <= some subarray sum <= M0? No, S is itself a subarray sum (for [l,r]), and S <= M0. And S - x*k < S <= M0. So for x>0, f(x) <= S_max <= M0? Not quite, because f(x) is the max over [l,r] of S - x*k, and for each [l,r], S - x*k < S <= M0 only if S <= M0. But S can be up to M0 (when [l,r] is the optimal). Then S - x*k = M0 - x*k < M0. So f(x) < M0 for x>0. Actually, f(x) is the max over [l,r], so f(x) <= max_{[l,r]} S = M0. And for x>0, achieving M0 requires k=0, but if k=0 for the optimal [l,r], then f(x) >= M0 (since we can pick [l,r] with k=0 and get S=M0? No, if [l,r] is the M0-optimal, it might have k>0 for this x. But there exists some [l,r] with k=0 for x (e.g., a subarray with no x) that has sum <= M0. The max over all [l,r] of (S - x*k) could be less than M0 if for the M0-optimal [l,r], k>0 and the reduction is significant.

Hmm, but actually f(x) is computed as max over [l,r] with clean boundaries. The value is S - x*k. For x>0, this is < S when k>0, and = S when k=0. The max is achieved at some [l,r]. If achieved at k=0, value = S <= M0. If achieved at k>0, value = S - x*k < S. Could this be > M0? Only if S - x*k > M0, but S <= M0 (since S is a subarray sum, M0 is the max), so S - x*k < S <= M0. Therefore, for x>0, f(x) <= M0. And since M0 is also a candidate (no deletion), the answer for x>0 is at most M0.

Wait, is it possible that f(x) = M0 for x>0? Yes, if there is a [l,r] with k=0 and S = M0, i.e., the M0-optimal subarray contains no x. Then f(x) >= M0, so f(x) = M0.

But the key point: for x>0, f(x) <= M0, so max_x f(x) is achieved at x<=0 (or x such that f(x) > M0, which requires x<0 typically, or x=0).

For x<0, f(x) can be > M0 because -x*k > 0.

For x=0, f(x) = max over [l,r] of (S - 0*k) = max S = M0, provided we can achieve it with clean boundaries. The M0-optimal [l,r] has nums[l]!=0, nums[r]!=0? Not necessarily. If the optimal has nums[l]=0, then it's not a valid boundary for x=0. We need to check. But f(0) is the max subarray sum of stripped_0, which is original with 0's removed. This could be > M0? No, because stripping 0's (removing zeros) doesn't change the sum of a subarray that has no 0's at boundaries, but it allows us to skip 0's. The max subarray of stripped_0 is the max sum of a contiguous non-zero subsequence. This is >= any single non-zero element, and could be > M0 if the M0-optimal contains 0's that we can skip while keeping the high values.

Actually, stripping 0's and taking a subarray is like taking a subarray in original and ignoring the 0's inside. The sum is the same as the original subarray sum (since 0's add nothing). So f(0) = max_{[l,r]: nums[l]!=0, nums[r]!=0} S(l,r). This is at least M0 if the M0-optimal has non-zero boundaries. It could be larger? No, because S(l,r) is at most the sum of the elements, and ignoring 0's doesn't increase the sum beyond what's there. Wait, f(0) is the max of S(l,r) over [l,r] with no 0 at boundaries. This is a subset of all [l,r], so f(0) <= M0. And f(0) could equal M0 if the M0-optimal has non-zero boundaries, or less otherwise.

Hmm, so for x>=0, f(x) <= M0. For x<0, f(x) can be > M0. Therefore, the answer A = max(M0, max_{x<0} f(x)).

So we only need to consider x<0! And x=0 doesn't help (f(0)<=M0, and 0 is not negative, but f(0) could equal M0, but M0 is already considered). Actually, x=0: f(0) = max subarray sum of array with 0's removed. This is max over [l,r] with nums[l]!=0, nums[r]!=0 of S(l,r). Since S(l,r) <= M0, and the global max is M0, f(0) <= M0. Could f(0) > M0? Only if there's a [l,r] with S(l,r) > M0, impossible. So f(0) <= M0.

For x>0, f(x) <= M0 as argued.

For x<0, f(x) can be > M0. So answer = max(M0, max_{x<0, x in nums} f(x)).

Great, this reduces the candidates to negative values.

Now, for a negative x, f(x) = max_{[l,r]: nums[l]!=x, nums[r]!=x} (S(l,r) - x * cnt_x(l,r)) = max_{[l,r]: clean} (S(l,r) + |x| * cnt_x(l,r)).

Let me define for each x<0, f(x) = max over clean [l,r] of (S(l,r) + |x| * k), where k = count of x in [l,r].

Equivalently, f(x) = max over clean [l,r] of (sum(nums[l..r]) - x * k) = max over clean [l,r] of (sum_{i in [l,r]} (nums[i] - x * [nums[i]==x])). 

Note nums[i] - x * [nums[i]==x] = nums[i] if nums[i]!=x, and x - x = 0 if nums[i]==x. So the "adjusted" value is nums[i] for nums[i]!=x, and 0 for nums[i]==x. So the sum is the sum of nums[i] for nums[i]!=x in [l,r], which is the same as the stripped sum. And f(x) is the max subarray sum of the stripped array, which is the max sum of a contiguous block in the array where x's are treated as 0? No, the stripped array is the sequence of non-x values. The max subarray sum of stripped is the max sum of a contiguous subsequence (in stripped) of non-x values. This is the max over [l,r] with clean boundaries of (sum of non-x in [l,r]).

And sum of non-x in [l,r] = S(l,r) - x*k = S(l,r) + |x|*k for x<0.

OK so for each negative x, f(x) = max subarray sum of the array with x's removed (concatenated). 

To compute max_{x<0} f(x) efficiently, note that f(x) depends on the positions of x.

**Key insight**: f(x) for a negative x is the max subarray sum of the sequence obtained by removing x. Let's denote the array as a sequence. When we remove x, we concatenate the gaps. The max subarray of the concatenated sequence.

For the concatenation, the max subarray can span multiple gaps. Specifically, if x is at positions p1<...<pk, the gaps are G0=[0,p1-1], G1=[p1+1,p2-1], ..., Gk=[pk+1,n-1]. A subarray in the concatenated array is a contiguous range of gaps. The sum is the sum of all elements in the spanned gaps.

This is equivalent to: for each x, max over (i, j) with i<=j of (sum of gaps i to j). Here gaps are indexed 0 to k.

The sum of gaps i to j is sum of all elements in original from start of gap i to end of gap j, minus x*k where k is the number of x strictly between (i.e., p_{i+1}, ..., p_j if i<j, or 0 if i=j). For i=0, start is 0; for j=k, end is n-1.

Let me define: for gap t (0<=t<=k), let L_t and R_t be the start and end of gap t. 
- G0: L_0=0, R_0=p1-1 (if p1>0, else empty)
- Gt for 1<=t<=k-1: L_t=p_t+1, R_t=p_{t+1}-1
- Gk: L_k=p_k+1, R_k=n-1

A subarray from gap i to gap j (0<=i<=j<=k) has sum = sum of nums[L_i..R_j] - x * (number of x in (L_i, R_j)) = sum of nums[L_i..R_j] - x * (j - i) [since there are j-i x's between gap i and gap j, specifically at p_{i+1}, ..., p_j].

Wait, number of x in [L_i, R_j] depends. The x's in this range are at positions p_{i+1}, ..., p_j (if i<j), which is j-i of them. Also, are there x's at L_i or R_j? L_i and R_j are the boundaries; by definition of gaps, L_i is just after an x (or 0), R_j is just before an x (or n-1). Specifically:
- If i=0, L_0=0 (or if p1=0, gap 0 is empty, skip). 
- If i>0, L_i = p_i+1, so no x at L_i.
- R_j: if j<k, R_j = p_{j+1}-1, so no x at R_j. If j=k, R_k=n-1, could have x at n-1? No, p_k < n usually, but p_k could be n-1, then gap k is empty.

The x's in [L_i, R_j] are exactly at p_{i+1}, ..., p_j (j-i many), assuming i<=j. For i=j, 0 x's.

So sum = sum(nums[L_i..R_j]) + |x| * (j-i) for x<0.

f(x) = max_{0<=i<=j<=k} (sum(nums[L_i..R_j]) + |x| * (j-i)).

This is a max over intervals of gaps. The "value" of spanning from gap i to gap j is the sum of the original range [L_i, R_j] plus |x| times the number of x's jumped over.

This looks like we can use a "weighted" interval DP. For each gap, we have its sum. Spanning multiple gaps adds the gap sums and the |x| bonus for each x jumped.

Specifically, let S_t = sum of gap t = sum of nums in gap t. Let the prefix of gaps: PS(s) = sum_{t=0}^s S_t. Then sum(nums[L_i..R_j]) = sum of gaps i to j = PS(j) - PS(i-1) (with PS(-1)=0).

So f(x) = max_{0<=i<=j<=k} (PS(j) - PS(i-1) + |x| * (j-i)).

Let j be fixed. We want max_i (PS(j) - PS(i-1) + |x| * (j-i)) = PS(j) + |x|*j + max_{0<=i<=j} (-PS(i-1) - |x|*i).

Let h(i) = -PS(i-1) - |x|*i for i=0..k (with PS(-1)=0, so h(0) = 0 - 0 = 0).

Then f(x) = max_{0<=j<=k} (PS(j) + |x|*j + min_{0<=i<=j} h(i)) ... wait, max over i of -PS(i-1)-|x|i is the max,
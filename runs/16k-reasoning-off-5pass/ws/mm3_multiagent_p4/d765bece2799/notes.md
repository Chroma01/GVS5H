
## ideation
The problem asks for the sum over all subarrays of length ≤ k of (min + max) of that subarray. The naive approach is O(n·k) (enumerating all subarrays) and is too slow for n up to 80,000. We need an O(n) or O(n log n) solution.

**Core difficulty:** efficiently computing the sum of minima and maxima over all subarrays of bounded length. This is reminiscent of problems like "sum of subarray minimums" (LeetCode 907), but here we have both min and max and a length constraint k.

**Candidate approaches:**

1. **Sliding window with monotonic deques** – maintain deques for the current window of size ≤ k that give the min and max. For each right endpoint r, consider all subarrays ending at r with length 1..min(k, r+1). The min/max for all those subarrays can be derived from the deque, but we need the sum of min and max over all those subarrays, not just the global min/max of the window.

2. **Contribution of each element as min or max with a length bound** – count for each element how many subarrays of length ≤ k it is the minimum, and similarly for maximum, then multiply by value. The classic method uses "previous less element" and "next less element" to count subarrays where an element is the unique minimum. However, that method counts subarrays without length restriction (or with restriction ≥ some value). With a length bound k, we need to restrict the range of subarrays to those with length ≤ k. That can be done by finding the furthest left and right the subarray can extend given k, and combining with the previous/next less elements.

3. **For each length L from 1 to k, sum min and max over all subarrays of exact length L** – there are O(n) subarrays per length, so total O(n·k) – too slow.

4. **Sliding window approach: keep a deque for min and max, and for each right endpoint r, add contributions incrementally** – when we slide the window to include nums[r], the new subarrays are those ending at r with start from max(0, r-k+1) to r. We need to know, for each start position, the min and max. This is tricky because the min/max of subarray starting at i and ending at r depends on all elements from i..r.

Let's think about the sliding window / incremental approach more carefully:

For a fixed right endpoint r, consider subarrays ending at r with length ≤ k. The min of subarray nums[i..r] is the minimum over nums[i..r]. As i decreases, the min can only stay the same or decrease. Similarly for max. If we maintain a deque of indices in increasing order of values for min, and decreasing for max, we can read the current min and max of the full window. But the min of a subarray of length less than the full window is not simply the deque's front if the deque front is from before the start of the subarray. However, we can note that for a subarray starting at i, the min is the first element in the min-deque that is ≥ i. As we expand the window to the right, the min for each fixed i is the minimum over nums[i..r], which is non-increasing as r increases. This is complex to maintain for all i simultaneously.

**Better approach:** The "contribution" method with length bound.

For each element nums[i], we want to count:
- the number of subarrays of length ≤ k where nums[i] is the **minimum**, multiply by nums[i]
- the number of subarrays of length ≤ k where nums[i] is the **maximum**, multiply by nums[i]

Total sum = sum over i of nums[i] * (count_as_min + count_as_max).

For counting subarrays where nums[i] is the minimum (using ≤ to break ties, say leftmost minimum):
- Find the distance to the previous strictly smaller element: left[i] = i - prev_less_strict[i]
- Find the distance to the next smaller-or-equal element: right[i] = next_less_or_equal[i] - i
- Without length bound, count = left[i] * right[i]

With length bound k: the subarray must have length ≤ k, and nums[i] must be the minimum. The subarray can start from i - left[i] + 1 up to i, and end from i to i + right[i] - 1. The length is (end - start + 1). We need length ≤ k, so (end - start + 1) ≤ k, i.e., end ≤ start + k - 1.

Let start ∈ [s_min, i] where s_min = i - left[i] + 1.
Let end ∈ [i, e_max] where e_max = i + right[i] - 1.
Constraint: end - start + 1 ≤ k  →  end ≤ start + k - 1.

For a given start, end can go from i to min(e_max, start + k - 1).
Number of valid end values: min(e_max, start + k - 1) - i + 1.

This gives a piecewise sum. The standard trick: for each i, the range of valid (start, end) pairs forms a 2D region. We can compute it by considering how far the subarray can extend.

Alternative formulation: the number of subarrays of length ≤ k where nums[i] is the minimum is the number of pairs (start, end) with start ≤ i ≤ end, start ≥ s_min, end ≤ e_max, and end - start + 1 ≤ k.

Let d = end - start + 1 (length). We need d ≤ k.
For each valid start s ∈ [s_min, i], the end e can range from i to min(e_max, s + k - 1).
The number of end choices is min(e_max, s + k - 1) - i + 1.

This is a sum that can be computed in O(1) per i if we find the breakpoint where s + k - 1 = e_max, i.e., s = e_max - k + 1. Let's call s_break = e_max - k + 1.

Case 1: s_min > s_break, i.e., even the earliest start has s + k - 1 ≥ e_max? Wait, s_break = e_max - k + 1. If s_min > s_break, then for all s ∈ [s_min, i], we have s + k - 1 > e_max? Actually s_min > s_break means s_min > e_max - k + 1, so s_min + k - 1 > e_max, so the window is too long? No, it means for all s, s + k - 1 ≥ e_max? Let's check: s ≥ s_min > e_max - k + 1, so s + k - 1 > e_max. So min(e_max, s+k-1) = e_max for all s. Then number of end choices = e_max - i + 1 = right[i]. Total count = (i - s_min + 1) * right[i] = left[i] * right[i]. This is the unrestricted case, meaning k is large enough.

Case 2: s_min ≤ s_break. Then for s ∈ [s_min, s_break], the end is capped by s + k - 1, and for s ∈ [s_break+1, i], the end is capped by e_max.

Wait, we need to be careful: the max start is i. So s_break might be > i, in which case the first case covers all s.

This can get messy. A cleaner approach is to use the fact that the subarray length is bounded by k, so we can use a sliding window approach but maintain the deques and a running sum.

**Sliding window with running sum approach (different interpretation):**

Consider all subarrays with length ≤ k. As we iterate r from 0 to n-1, we maintain a window of size k. The subarrays ending at r of length ≤ k are those starting at max(0, r-k+1) to r. Let's maintain the min and max of *each* subarray ending at r? That's O(k) per r.

But here's a key insight: the subarrays ending at r are a superset of the subarrays ending at r-1 (with the rightmost element dropped if too long). We can maintain the deques and also the sum of minima and sum of maxima over all subarrays ending at the current r.

How? As we slide the window, we drop the leftmost element (if window size exceeds k) and add nums[r]. The subarrays ending at r are all subarrays of the window [L, r] where L = max(0, r-k+1). 

We can maintain a monotonic deque for min and max. Let the min-deque store indices in increasing order of value. The front is the minimum of the current window. The min of a subarray nums[i..r] is the first element in the min-deque that is ≥ i.

To get the sum of mins of all subarrays ending at r (i.e., for all i from L to r), we need to sum over i of min(nums[i..r]). This is not trivial from the deque alone.

**Alternative: use the fact that we can compute the sum of mins for all subarrays ending at r by processing the deque.**

When we add nums[r] to the min-deque, we pop from the back all elements ≥ nums[r] (for strict, or ≤ for the desired tie-breaking). The new deque has the property that the values are strictly increasing from front to back. The min of subarray starting at i is the first element in deque with index ≥ i.

We can maintain a running sum: when we add nums[r], how does the sum of mins change? The subarrays ending at r are new. For i = r, the subarray is just [r], min = nums[r]. For i < r, the min of [i..r] is the min of [i..r-1] if nums[i..r-1]'s min is still there, unless nums[r] is smaller and pops some elements.

Actually, there's a known technique: as we process the array and maintain a monotonic stack (not deque, because we need to look at all subarrays, not just the current window), we can compute the contribution.

**Let's reconsider the contribution method with length bound — it can be done cleanly.**

For minimum:
- prev_less[i] = index of previous element strictly less than nums[i], or -1.
- next_less_eq[i] = index of next element ≤ nums[i], or n.
- left_count[i] = i - prev_less[i]
- right_count[i] = next_less_eq[i] - i
- Unrestricted: left_count[i] * right_count[i] subarrays where nums[i] is the minimum (using ≤ for next to break ties leftmost).

With length bound k: we need end - start + 1 ≤ k.
- start ∈ [prev_less[i]+1, i]
- end ∈ [i, next_less_eq[i]-1]
- (end - start + 1) ≤ k  →  end ≤ start + k - 1

The number of valid (start, end) pairs. For each start s, the number of valid ends is the number of e ∈ [i, next_less_eq[i]-1] with e ≤ s + k - 1, i.e., e ∈ [i, min(next_less_eq[i]-1, s+k-1)].

Let R = next_less_eq[i] - 1 (max end). Let L = prev_less[i] + 1 (min start).
The count is sum_{s=L}^{i} max(0, min(R, s+k-1) - i + 1).

Let f(s) = min(R, s+k-1) - i + 1.
- If s + k - 1 ≤ R, i.e., s ≤ R - k + 1, then f(s) = s + k - i.
- If s + k - 1 > R, i.e., s > R - k + 1, then f(s) = R - i + 1.

Let s_cutoff = R - k + 1.

Case A: L > s_cutoff. Then for all s ∈ [L, i], s > R - k + 1, so f(s) = R - i + 1 = right_count[i]. Count = (i - L + 1) * right_count[i] = left_count[i] * right_count[i]. (Unrestricted, k large enough.)

Case B: L ≤ s_cutoff. Then split:
- For s ∈ [L, min(i, s_cutoff)]: f(s) = s + k - i.
- For s ∈ [max(L, s_cutoff+1), i]: f(s) = R - i + 1 = right_count[i].

Note: s_cutoff = R - k + 1 = (i + right_count[i] - 1) - k + 1 = i + right_count[i] - k.
So s_cutoff could be less than i or greater.

If s_cutoff ≥ i, then min(i, s_cutoff) = i, and max(L, s_cutoff+1) = s_cutoff+1 > i, so the second range is empty. Then count = sum_{s=L}^{i} (s + k - i) = sum_{s=L}^{i} s + (i - L + 1)(k - i).
sum_{s=L}^{i} s = (L+i)(i-L+1)/2.

If s_cutoff < L, then first range empty, second is [L, i], count = left_count[i] * right_count[i].

In general:
Let A = max(L, s_cutoff+1) if s_cutoff+1 ≤ i, else no second range.
Wait, let's do it carefully.

The valid s are from L to i. For each s, f(s) = min(R, s+k-1) - i + 1.
f(s) increases with s until s = s_cutoff, then constant.

s_cutoff = R - k + 1.

If s_cutoff < L: all s have f(s) = R - i + 1. Count = (i - L + 1)(R - i + 1) = left_count * right_count.

If s_cutoff ≥ i: for all s, s ≤ i ≤ s_cutoff, so s + k - 1 ≤ i + k - 1 ≤ s_cutoff + k - 1 = R, so f(s) = s + k - i. Count = sum_{s=L}^{i} (s + k - i) = sum_{s=L}^{i} s + (i-L+1)(k-i).

If L ≤ s_cutoff < i: 
- s from L to s_cutoff: f(s) = s + k - i.
- s from s_cutoff+1 to i: f(s) = R - i + 1.
Count = sum_{s=L}^{s_cutoff} (s+k-i) + (i - s_cutoff)(R-i+1).

This is O(1) per i. Similarly for maximum (using prev_greater, next_greater_eq).

This is O(n) after O(n) preprocessing for prev_less and next_less_eq using monotonic stacks.

This is a clean and efficient solution: O(n) time, O(n) space.

**Edge cases:** k = 1 (only single elements, min = max = nums[i], so sum is 2*sum(nums)). k = n (all subarrays). Negative numbers are fine.

**Implementation steps:**
1. Compute prev_less_strict[i] and next_less_or_equal[i] for each i using a stack (increasing stack for prev_less: pop while stack top >= nums[i], then top is prev_less; for next_less: iterate right to left, pop while stack top > nums[i], then top is next_less_or_equal). Wait, tie-breaking: for min, we want the first occurrence of minimum to be counted. Standard: previous strictly less, next less or equal. This ensures each subarray has a unique min (the leftmost minimum). Similarly for max: previous strictly greater, next greater or equal.
2. For each i, compute left_len = i - prev_less[i], right_len = next_less[i] - i.
3. Compute the number of subarrays of length ≤ k where nums[i] is the min using the formula above, multiply by nums[i], add to total.
4. Do the same for max with prev_greater and next_greater_eq.
5. Return total.

**Pitfalls:**
- Tie-breaking consistency: use (prev_strict, next_non_strict) for min, and (prev_strict, next_non_strict) for max (i.e., previous strictly less, next less or equal for min; previous strictly greater, next greater or equal for max).
- s_cutoff = i + right_len - k. This can be negative or > n. The piecewise logic must handle bounds correctly.
- Use long (Python int is arbitrary precision, fine).
- The formula derivation must be double-checked with small examples.

Let me verify with a small example: nums = [1,2,3], k=2.
i=0, val=1. prev_less=-1, next_less_eq=1 (nums[1]=2 > 1, so next less or equal? No, next less or equal means value < or =. nums[1]=2 is not ≤1, so next_less_eq = n=3? Wait, we need the next element that is ≤ nums[i]. For min, the subarray cannot extend past an element that is strictly smaller, and can extend up to an element that is equal? Standard: for the leftmost minimum, previous strictly less, next less or equal. So for i=0, val=1: next less or equal is at index 3 (none), so right_len = 3-0=3. left_len = 0-(-1)=1. s_cutoff = 0+3-2=1. s_cutoff=1. i=0. Since s_cutoff >= i (1>=0), use case "s_cutoff >= i": count = sum_{s=0}^{0} (s+2-0) = 0+2=2. Subarrays: [1] and [1,2]. Min is 1. Contribution: 1*2=2.
i=1, val=2. prev_less=0 (nums[0]=1<2), next_less_eq=2 (nums[2]=3>2, so none, next=n=3? No, next less or equal: is there any ≤2? No, so next=3. right_len=2, left_len=1. s_cutoff=1+2-2=1. s_cutoff=1, i=1. s_cutoff >= i: count = sum_{s=1}^{1}(s+2-1) = 1+1=2. Subarrays ending at or before 1 of length ≤2 where 2 is min: [2] and [1,2]? Wait, [1,2] has min 1, not 2. So 2 is min only for [2] and [2,3]? But k=2, so [2,3] is valid. But wait, for i=1, the subarray [2,3] ends at 2, not at 1. When we count subarrays where nums[i] is the min, we consider subarrays that include i. For i=1, the subarray [2,3] includes i=1? No, [2,3] is indices 1..2, so it includes i=1. Its min is 2. So yes, [2,3] is counted. And [2] is counted. So count=2, contribution 2*2=4.
i=2, val=3. prev_less=1 (nums[1]=2<3), next_less_eq=3, right_len=1, left_len=1. s_cutoff=2+1-2=1. s_cutoff=1 < i=2. s_cutoff < L? L = prev_less+1 = 2. So L=2 > s_cutoff=1, so we are in the case s_cutoff < L, count = left_len * right_len = 1*1=1. Subarray: [3]. Min=3, contribution 3*1=3.
Total min contribution: 2+4+3=9.
Now max: nums=[1,2,3]. prev_greater: for 1, none, -1. For 2, 0? nums[0]=1<2, so not greater. None, -1. For 3, none, -1? Wait, prev strictly greater. For 1: no greater, prev=-1. For 2: no greater before 2, prev=-1. For 3: no greater, prev=-1. left_len=1 for all.
next_greater_eq: for 1, index 1 (val 2 > 1, not >=, wait greater or equal? For max, we want leftmost max, so previous strictly greater, next greater or equal. So for 1, next greater or equal: is there any ≥1? Yes, at 1 (val 2). So next=1, right_len=1.
For 2: next greater or equal: val 3 ≥ 2, so next=2, right_len=1.
For 3: next greater or equal: none, next=3, right_len=1.
So for max:
i=0: left=1, right=1, s_cutoff=0+1-2=-1. L=0. s_cutoff < L, count=1*1=1. Subarray [1]. Max=1. Contribution 1.
i=1: left=1, right=1, s_cutoff=1+1-2=0. L=0. s_cutoff=0, i=1. s_cutoff < i, and s_cutoff >= L? L=0 ≤ 0. So L ≤ s_cutoff < i. s_cutoff=0. Count = sum_{s=0}^{0}(s+2-1) + (1-0-0? wait, (i - s_cutoff)(R-i+1) = (1-0)*(1) = 1*1=1. First part: s=L=0, sum (0+2-1)=1. Total=1+1=2. Subarrays: [1,2] (max 2), [2] (max 2). Contribution 2*2=4.
i=2: left=1, right=1, s_cutoff=2+1-2=1. L=0. s_cutoff=1 < L? L=0, s_cutoff=1, so s_cutoff >= L. s_cutoff=1 < i=2. Count = sum_{s=0}^{1}(s+2-2) + (2-1-1+1? wait: (i - s_cutoff)(R-i+1) = (2-1)*(1)=1*1=1. First part: s=0: 0+2-2=0; s=1: 1+2-2=1; sum=1. Total=1+1=2. Subarrays: [2,3] (max 3), [3] (max 3). Contribution 3*2=6.
Total max contribution: 1+4+6=11.
Total sum: 9+11=20. Matches example!

Great, the contribution method works.

**Complexities:** O(n) time, O(n) space. For n=80,000, this is very fast.

**Alternative sliding window approach:** There's also a sliding window with deques where you maintain the sum of mins and maxs incrementally. It might be more complex to get right but also O(n). The contribution method is more direct for this problem.

**Decision:** Implement the contribution method.

**Plan for code:**
1. n = len(nums), k.
2. Compute prev_less[i] (strictly less) using a stack: while stack not empty and nums[stack[-1]] >= nums[i]: pop. Then prev_less[i] = stack[-1] if stack else -1. Push i.
   Wait, for strictly less, we pop while >=, so the remaining top is < nums[i].
3. Compute next_less_eq[i] (less or equal) iterating from right: while stack and nums[stack[-1]] > nums[i]: pop. Then next_less_eq[i] = stack[-1] if stack else n. Push i.
4. For each i, compute left = i - prev_less[i], right = next_less_eq[i] - i.
   Compute count_min using the piecewise function.
5. Similarly for max: prev_greater (strictly greater): pop while <=. next_greater_eq (greater or equal): pop while <.
6. Sum up: total = sum(nums[i] * count_min[i] + nums[i] * count_max[i]).
7. Return total.

**Helper function to compute count for a given i, left, right, k:**
def get_count(i, left, right, k):
    L = i - left + 1  # min start index
    R = i + right - 1  # max end index
    # We need count of (start, end) with start in [L, i], end in [i, R], end - start + 1 <= k.
    # Let s_cutoff = R - k + 1.
    s_cutoff = R - k + 1
    if s_cutoff < L:
        # All starts have f(s) = right (since R - i + 1 = right)
        return left * right
    elif s_cutoff >= i:
        # All starts have f(s) = s + k - i
        # sum_{s=L}^{i} (s + k - i) = sum_{s=L}^{i} s + (i - L + 1) * (k - i)
        # sum_{s=L}^{i} s = (L + i) * (i - L + 1) // 2
        cnt = (i - L + 1)
        sum_s = (L + i) * cnt // 2
        return sum_s + cnt * (k - i)
    else:
        # L <= s_cutoff < i
        # s from L to s_cutoff: f(s) = s + k - i
        # s from s_cutoff+1 to i: f(s) = right
        cnt1 = s_cutoff - L + 1
        sum_s1 = (L + s_cutoff) * cnt1 // 2
        part1 = sum_s1 + cnt1 * (k - i)
        cnt2 = i - (s_cutoff + 1) + 1  # = i - s_cutoff
        part2 = cnt2 * right
        return part1 + part2

**Verification with example 2:** nums = [1,-3,1], k=2.
Min:
i=0, val=1. prev_less=-1, left=1. next_less_eq: look for ≤1. nums[1]=-3 ≤1, so next=1, right=1. s_cutoff = 0+1-2 = -1 < L=0. count = 1*1=1. Subarrays: [1]. Contribution 1.
i=1, val=-3. prev_less: look for <-3. None, prev=-1, left=2. next_less_eq: look for ≤-3. None (nums[2]=1), next=3, right=2. s_cutoff = 1+2-2=1. L=0, i=1. s_cutoff=1 >= i? 1>=1 yes. count = sum_{s=0}^{1} (s+2-1) = (0+1) + (1+1) = 1+2=3. Subarrays where -3 is min: [1,-3], [-3], [-3,1]. All have length ≤2. Min=-3, contribution -9.
i=2, val=1. prev_less: look for <1. nums[1]=-3<1, so prev=1, left=1. next_less_eq: look for ≤1. None, next=3, right=1. s_cutoff = 2+1-2=1. L=1, i=2. s_cutoff=1 < L=1? Actually s_cutoff=1, L=1, so s_cutoff < L is false (equal). s_cutoff=1 < i=2. So s_cutoff >= L and s_cutoff < i. cnt1 = 1-1+1=1. sum_s1 = (1+1)*1/2=1. part1 = 1 + 1*(2-2)=1. cnt2 = 2-1=1. part2 = 1*1=1. Total count=2. Subarrays: [1] (indices 2..2), [-3,1] (1..2). Min is 1? Wait, [-3,1] has min -3, not 1. So 1 is min only for [1]? But we got count 2. Error!
Let's recalculate: i=2, val=1. prev_less[i] is previous strictly less. nums[1]=-3 < 1, so prev_less=1. left = 2-1=1. L=1.
next_less_eq[i]: next element ≤ 1. nums[3]? No. So next=3, right=1. R=2.
s_cutoff = R - k + 1 = 2 - 2 + 1 = 1.
L=1, i=2, s_cutoff=1.
s_cutoff >= L (1>=1) and s_cutoff < i (1<2).
For s from L to s_cutoff: s=1. f(1) = min(R, 1+2-1) - 2 + 1 = min(2, 2) - 1 = 1.
For s from s_cutoff+1 to i: s=2. f(2) = min(2, 2+2-1) - 2 + 1 = min(2,3)-1=1.
Wait, f(s) = number of end choices = min(R, s+k-1) - i + 1.
For s=1: min(2, 1+2-1=2) - 2 + 1 = 2-1=1. End can be 2 (i=2). So one subarray: start=1, end=2, i.e., [-3,1]. But min of [-3,1] is -3, not 1. So 1 is not the min here. What's wrong?
Ah! The next_less_eq should be for the minimum to be valid. For i=2, val=1, the subarray [-3,1] has min -3, which is < 1. So 1 is not the min. The next_less_eq for i=2 should be 1 (since -3 ≤ 1 and is the next element that is ≤, but wait, we want the next element that is strictly less? No, for min, we want the subarray to not contain any element < the min. Actually, the standard formula: nums[i] is the minimum of subarray [start, end] iff there is no element < nums[i] in (start, i] and no element ≤ nums[i] in [i, end). Wait, for leftmost minimum: start > prev_strict_less[i] (i.e., no element < nums[i] in [start, i-1]) and end < next_less_or_equal[i] (i.e., no element ≤ nums[i] in [i+1, end]). This ensures that if there is an element equal to nums[i], the leftmost one is chosen.
For i=2, val=1: prev_less = 1 (since -3 < 1). So start must be > 1, i.e., start = 2. Wait, L = prev_less+1 = 2. Not 1! I made a mistake: left = i - prev_less = 2 - 1 = 1. So L = i - left + 1 = 2 - 1 + 1 = 2. Yes, L=2.
Earlier I said L=1, but left=1, i=2, so L=2. Let's correct: L = i - left + 1 = 2. s_cutoff=1. s_cutoff < L (1<2). So case s_cutoff < L, count = left * right = 1*1=1. That matches: only [1] at index 2.
So my manual check was wrong because I used L=1 instead of 2. The formula is correct.

So the code is correct.

**Summary of approach:** Use monotonic stacks to find, for each element, how many subarrays of length ≤ k it is the minimum and the maximum, with appropriate tie-breaking. Sum the products. O(n) time.

This is a known hard problem (LeetCode 2940 or similar? Actually "Sum of Subarray Minimums" is 907, with bounds it's 2945 or something. The combination of min and max with length bound k is LeetCode 2940? No, 2940 is "Find Building Where Alice and Bob Can Meet". This is 2954? "Sum of Minimum and Maximum of All Subarrays of Size K" is not it because k is variable. Actually this is LeetCode 2954? Let me recall: 2954 is "Count the Number of Infection Sequences"? No. The problem is "Sum of Minimum and Maximum of All Subarrays With At Most K Elements" — I think it's LeetCode 2954 or 2955? Actually 2954 is "Find the Number of Subarrays...", no. It might be a premium problem or recent. Regardless, the contribution method is standard.

**Implementation details:**
- Use type hints.
- Handle n=0? Constraints say n>=1.
- k can be up to n.
- Use Python integers.

**Final plan is solid. Proceed to implement.**

## worker: Implement the `Solution.minMaxSubarraySum` method 
I implemented the contribution method using monotonic stacks to find, for each element, the number of subarrays of length ≤ k in which it serves as the minimum (using prev_strict_less and next_less_or_equal) and as the maximum (using prev_strict_greater and next_greater_or_equal). The piecewise formula with `s_cutoff = R - k + 1` correctly handles all cases: when k is large enough (unrestricted), when k is small enough to cap all windows, and the mixed case. Verified with both examples (returns 20 and -6). Complexity is O(n) time and O(n) space, well within the 80,000 constraint.

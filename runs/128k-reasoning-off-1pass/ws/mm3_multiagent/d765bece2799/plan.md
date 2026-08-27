We need to compute, for every subarray of length between 1 and k, the sum of its minimum and maximum, then add all these (min + max) values together. A brute-force O(n*k) loop is too slow for n up to 80k when k can be close to n (O(n^2)).

The classic technique is to use a sliding window with monotonic deques to maintain the current window's min and max in O(1) amortized per step. We fix the right endpoint `r` and consider all valid left endpoints `l` such that `r - l + 1 ≤ k`. As we slide `r` from 0 to n-1:
- Add `nums[r]` to the max-deque (decreasing) and min-deque (increasing).
- While the window size exceeds k, pop the leftmost element and update deques.
- For the current window, the max is `maxDeque[0]` and min is `minDeque[0]`. Every subarray ending at `r` of length 1..min(k, r+1) has these same min and max? Wait — that is only true if the window's min and max haven't "expired" from the deques. As long as we keep the window of size exactly `min(k, r+1)` (the largest valid window ending at r), then every subarray ending at r of length ≤ k is contained in this window, and its min/max are some elements of this window. But the min and max can change for shorter subarrays! So we can't just take one (min, max) per r.

Alternative: A known O(n) trick uses "contribution of each element as min/max over all windows up to size k". Instead, we can compute, for each length L from 1 to k, the sum of max over all subarrays of length L plus sum of min over all subarrays of length L using a sliding window with deques in O(n) per length — still O(n*k).

Better approach: Use the "contribution method" with a deque that expands and contracts. We slide a window [l, r] of size exactly k (when r ≥ k-1). At each step, the deques hold the min/max of the current window of size k. But the subarrays of length 1..k ending at r are all subarrays contained in the window [r-k+1, r], and each one's min/max could differ. However, note that for subarrays ending at r, as the left endpoint moves rightward, the min can only increase (or stay) and max can only decrease (or stay). This monotonicity can be exploited.

Actually there's an elegant O(n) solution: as r increases, we add nums[r] to the deques. Then for each r, we want the sum of (min + max) over all left endpoints l with 0 ≤ l ≤ r and r-l+1 ≤ k. We can iterate l from r down to max(0, r-k+1). But the deques change as we move l.

**Key insight — O(n) solution using deque expansion/contraction per element:**
For each r, we want to add (min + max) of subarray [l, r] for all valid l. We can maintain deques for the window [l, r] where l starts at r and we expand leftward up to k elements. But expanding leftward by one means pushing nums[l-1] to the front of the deques, which is harder in O(1) amortized.

So let's think differently. Reverse the array! Consider subarrays ending at r of length ≤ k. If we process r from 0 to n-1 and maintain deques of the window [max(0, r-k+1), r] of size up to k, the deques give min/max of the *entire* window, not of sub-windows. But we need min/max of every suffix of this window.

**Correct O(n) approach using contribution / stack-based counting:**
The standard technique for "sum of minimums over all subarrays" is to count, for each element, how many subarrays it's the minimum. We can extend this to "at most k length". For each index i, the number of subarrays ending at i where nums[i] is the minimum and length ≤ k equals the number of valid starting positions. We can bound it by min(i+1, k) minus the number of invalid (longer than k) ones.

Similarly for maximums. So:
- For each i, let `left[i]` = number of consecutive elements to the left (including i) that are ≥ nums[i] (for min) or ≤ nums[i] (for max). This is the "span to the left".
- Let `right[i]` = number of consecutive elements to the right (strictly greater for min, so the next smaller element) such that ... Actually the standard formula: nums[i] is the minimum in subarrays where it's the leftmost minimum, spanning `left[i]` choices on the left and `right[i]` choices on the right, contributing `nums[i] * left[i] * right[i]` to the sum of minimums over all subarrays.

For "at most k", for each i, the number of subarrays where nums[i] is the min and has length ≤ k is bounded. Let `L = left[i]`, `R = right[i]`. The subarrays where nums[i] is the unique min and the leftmost such start in [i - L + 1, i] and right end in [i, i + R - 1], with length = (r - l + 1) ≤ k. We can iterate over starting positions: for `d = 0` to `L-1` (start at i-d), the max end offset is `min(R-1, k-1-d)`. So contribution = nums[i] * sum_{d=0}^{L-1} min(R, k-d).

If we precompute, for each i, the contribution efficiently... this seems complex per-element. However, we can process all starting positions together with a different approach.

**Sliding window with two pointers approach (O(n) amortized):**
Maintain `l` as the left pointer, and deques for min/max of window [l, r]. For a fixed r, as we vary l from r down to r-k+1, the min and max only change when we "remove" nums[l] from consideration. But removing from the front of a deque is not standard.

**Alternative — iterate over all subarray lengths ≤ k, but cleverly:**
We can fix the window size `w` from 1 to k. For each w, we compute sum of mins and maxes over all subarrays of length w using sliding window + deques in O(n). Total O(n*k) — too slow when k = n.

But there's an optimization: we don't need to do each w separately. We can use a deque that tracks elements with their "remaining span" as the window grows.

**The cleanest O(n) approach I recall:**
This is a known problem. Solution: use a deque-based two-pointer technique where we maintain the window [l, r] and for each r, we add nums[r] to deques. Then while the window size > k, advance l (pop from front of deques if they match). Now the deques hold min/max of window of size exactly k (or less at start). The key observation: as r advances by 1, the new subarrays ending at r are: all subarrays [r, r], [r-1, r], ..., [max(0, r-k+1), r]. We can compute the sum of (min+max) over these by noting that the deques still represent the current window. But when r advances, we add a new element, and the window shifts. Let's denote the window after adding nums[r] and possibly shrinking from the left as W = [l, r] with |W| ≤ k. The subarrays ending at r of length ≤ k are exactly the suffixes of W: [W[0], r], [W[1], r], ..., [W[-1], r]. We need sum of min+max of each suffix of W.

We can maintain, in addition to the deques, two stacks/structures: as r advances, we add nums[r] to a "min stack from the right" — a stack where each entry has the value and the cumulative sum of (current min + ...) over the suffixes seen so far. Similarly for max.

Specifically, maintain a stack `minStack` where each element is (value, sum_contribution). When we add nums[r]:
- `new_min = min(nums[r], minStack.top.value if exists else +inf)`
- `new_sum = minStack.top.sum_contribution + new_min` (sum of mins over all suffixes of the new window)
- push (new_min, new_sum) to minStack.

Similarly for max. This works because as the window grows (r increases by 1), the suffixes of the new window are: [r, r] (a new suffix of length 1) plus all old suffixes of the previous window [l, r-1] but with a new element appended on the right. The new element nums[r] is the rightmost, so the new suffix of the old window extended by nums[r] has min = min(old_suffix_min, nums[r]). So we can compute this incrementally!

But we also need to handle window shrinking when size exceeds k. When l advances (old element removed), the oldest suffix (the one starting at the old l) is removed from consideration. The remaining suffixes shift: the new "longest" suffix is [l+1, r] (was previously the second-longest). So we need to track the sum over the active suffixes.

This is exactly a "sliding window aggregate" problem. We can maintain for each deque, in addition to the deque entries, the sum over the current window's suffixes.

Let me think more carefully. Let's maintain:
- `minDeque` (monotonic increasing): holds pairs (value, suffix_min_sum_so_far) for the suffixes of the current window, where the deque is ordered from oldest suffix to newest? Hmm.

Actually, let me think of it as: when we have a window [l, r], the suffixes are S_0 = [l, r], S_1 = [l+1, r], ..., S_m = [r, r] where m = r - l. We want sum_{i=0}^{m} (min(S_i) + max(S_i)).

When we add nums[r+1] (right-extend):
- New suffixes are: [r+1, r+1] (new S_{m+1}), and [l, r+1], [l+1, r+1], ..., [r, r+1] (old suffixes extended).
- For each extended suffix, new min = min(old_min, nums[r+1]) and new max = max(old_max, nums[r+1]).

This is like: we have a sequence of old mins m_0, m_1, ..., m_m (from longest suffix to shortest). New mins are min(m_i, nums[r+1]). If nums[r+1] is very small, all new mins become nums[r+1]. The new sum of mins = sum_i min(m_i, nums[r+1]) + nums[r+1].

To compute this efficiently, we can maintain a monotonic stack of mins. The stack contains (value, count) where count is how many suffixes have this min as their minimum. When we add nums[r+1], we pop from the stack while top.value > nums[r+1], accumulating the counts. Then the new stack top has value min(top.value, nums[r+1]) = nums[r+1] (since we popped all > nums[r+1]). The new count is the sum of popped counts + 1 (for the new suffix [r+1, r+1]). The sum of mins over the new suffixes is nums[r+1] * total_count.

Similarly for maxs (but with < and max).

When we remove the leftmost element (l becomes l+1): the longest suffix S_0 = [l, r] is removed. The remaining suffixes are S_1, ..., S_m, S_{m+1} (where S_{m+1} = [r+1, r+1] is the newest). Wait, but S_0 is removed and the rest shift. We need to decrease the count of the "oldest" suffix's min/max by 1, and if the count for the top of the stack becomes 0, pop it.

But the monotonic stack doesn't easily support "remove from the front" because the front might not be the top.

Hmm, this is the challenge. Let me think again.

**Solution using two monotonic deques and tracking "ages":**
We can store in the deques not just values but also the index (or age). When we add nums[r+1], we push to the back. When we remove the leftmost (index l), we check if the front of the deque has index == l, and if so pop it.

For the sum of mins over the active suffixes: we can maintain a running sum that we update on each push/pop. When we push a new value v to the min-deque (which is monotonically increasing), we pop from the back all elements with value > v. The sum of mins over the new suffixes equals v * (number of active suffixes). Let `W` be the current window size = r - l + 1. Number of active suffixes = W.

When we pop the front (because the oldest suffix's min equals the front and that suffix is removed), the number of active suffixes decreases by 1, and the sum of mins decreases by the front's value. But we also need to handle the case where the front wasn't the min of the removed suffix — wait, the front of the min-deque (monotonic increasing) is the minimum value. The oldest suffix might not have the minimum value. So we can't just pop the front and subtract its value.

I need a different data structure. Let me think about storing, in the deque, for each entry, the sum of mins of the suffixes that this entry "represents".

**Refined approach — store cumulative info in the deque:**
Let the min-deque store entries (value, count, sum_of_mins) where the entries are ordered from front to back by the position in the window (oldest suffix to newest), and within the deque, values are monotonically increasing. The "count" is the number of consecutive suffixes (from some position to the next entry) that have this value as their minimum. The "sum_of_mins" is count * value.

When we add nums[r+1] = v:
- We want to compute the new sum of mins. v becomes the min for the new suffix [r+1, r+1], and for any extended suffix whose previous min was > v, the new min is v. So we pop from the back while back.value > v, accumulating their counts into a running total `c`. Then we push (v, c+1) to the back with sum_of_mins = (c+1)*v.
- The total sum of mins over all active suffixes = sum of sum_of_mins over all entries in the deque.

When we remove the leftmost (oldest suffix):
- The oldest suffix is the front. We decrement front.count by 1, and decrement front.sum_of_mins by front.value. If front.count becomes 0, pop it.
- The total sum of mins = sum of sum_of_mins over all entries.

Wait, but when we add and the back has a value > v, those entries represent suffixes whose min was that larger value. After appending v, those suffixes' min becomes v, and they're "merged" with the new entry. So popping them and accumulating their counts is correct.

But the issue: when we remove the front, we decrement by 1. But what if the oldest suffix's min was, say, 5, and after removing it, the next suffix's min is still 5 (it was a separate entry with value 5, count 3). The front had (5, 1, 5), we decrement to (5, 0, 0) and pop. The total sum decreases by 5. Correct!

But wait, there's a subtlety: the front represents the oldest suffix. But the deque entries are ordered by value (monotonically increasing), not by position. So the front has the smallest value, which corresponds to the oldest suffix only if the oldest suffix has the smallest min. Otherwise, the oldest suffix's min is somewhere in the middle of the deque, and decrementing the front's count doesn't make sense.

Let me reconsider the deque structure. I want the deque to be ordered by position (oldest suffix to newest), with values monotonically increasing. This is possible! When we add a new value v:
- Pop from the back while back.value > v (these are the most recent suffixes whose min > v; after appending v, their min becomes v).
- Accumulate popped counts into c, then push (v, c+1) to the back.

So the deque is ordered by position (front = oldest, back = newest), and values are monotonically non-decreasing (actually strictly increasing except we merge when equal? Let me re-examine).

When we pop back entries with value > v, and then push v at the back, the values are non-decreasing from front to back. If v equals the new back.value, we merge: actually we accumulate counts, so the back becomes (back.value, back.count + c + 1). The values remain non-decreasing.

Now, the front is the oldest suffix. Its min is front.value. When we remove the oldest suffix (window shrinks from left), we decrement front.count by 1 and front.sum_of_mins by front.value. If front.count becomes 0, pop it. This is correct because the oldest suffix's min is front.value (since the deque is ordered by position and values are non-decreasing, the oldest position has the smallest or equal min... wait, non-decreasing means front.value ≤ back.value, so front.value is the minimum. The oldest suffix has the smallest min? Not necessarily! The min of [l, r] could be larger than the min of [l+1, r] if the minimum is at position l. So front.value is the min of the oldest suffix, which is the global min of the window. When we remove the oldest suffix, we're removing the suffix with the global min. But we need to remove the oldest suffix regardless of its min value.

So decrementing front.count by 1 is correct: we're removing one instance of the value front.value from the "oldest suffix" position. The total sum decreases by front.value. 

But what if the oldest suffix's min is not front.value? In our deque structure, front is the oldest suffix, and front.value is its min (which is the global min of the window). So yes, front.value is the min of the oldest suffix.

Wait, I claimed front.value is the min of the oldest suffix. Let me verify. The deque is ordered by position: front is the entry for the oldest suffix, back is for the newest. The values (which are the mins of each suffix) are non-decreasing from front to back. So front.value ≤ all other values, meaning front.value is the minimum min, which is the min of [l, r] = the oldest suffix. Correct!

Similarly for max-deque: values are non-increasing from front to back. front.value is the max of the oldest suffix = max of [l, r].

So the algorithm:
1. Maintain `l = 0`, and for each `r` from 0 to n-1:
   a. Add nums[r] to min-deque and max-deque.
   b. While window size > k, i.e., r - l + 1 > k: remove the oldest suffix (which corresponds to removing nums[l] from the left, but actually removing the suffix [l, r]). Increment l, and update the deques by decrementing the front's count.
   c. The total sum of (min + max) over all active suffixes ending at r is (sum of min-deque sum_of_mins) + (sum of max-deque sum_of_mins).
   d. Add this to the answer.

Wait, step (a) "add nums[r]": we need to add the new suffix [r, r] and also conceptually "extend" the existing suffixes. But in our deque model, we just push the new entry to the back. The "extending" is handled by popping from the back while back.value > v (for min) and merging counts.

Let me re-derive step (a) for the min-deque:
- The new suffixes after adding nums[r] are: [l, r], [l+1, r], ..., [r-1, r], [r, r].
- The old suffixes were: [l, r-1], [l+1, r-1], ..., [r-1, r-1].
- The extended suffixes (old + nums[r]) have mins: min(old_min_i, nums[r]).
- The new suffix [r, r] has min = nums[r].

In the deque representation (ordered by position, values = min of each suffix):
- The old deque has entries for the old suffixes.
- We process from the back: the back is the oldest... wait, the back is the newest in the old deque, which is [r-1, r-1]. 
- We want to "extend" the old suffixes. Starting from the newest old suffix and going backward, if its min > nums[r], then after extending, its min becomes nums[r]. We can merge it with the new entry.
- So we pop from the back while back.value > nums[r], accumulating counts. Then the new back has value ≤ nums[r]. The new entry for [r, r] has min = nums[r]. We push to the back: if back.value == nums[r], merge (add to back.count); else push new entry (nums[r], accumulated_count + 1).

Hmm wait, the "accumulated_count" is the count of suffixes that were popped. After extending, those popped suffixes have min = nums[r]. Plus the new suffix [r, r] also has min = nums[r]. So total count for value nums[r] is accumulated_count + 1. And we add this to the back if back.value == nums[r], or push a new back.

But the order in the deque: the popped entries were the newest old suffixes. After extending, they all have min = nums[r]. The new suffix [r, r] is the newest. So all these (popped + new) are at the back, in order of position (popped are older than new). But since they all have the same value nums[r], we can just accumulate the count and put it at the back (merging with the previous back if it also has value nums[r]).

Wait, there's a subtlety: the popped entries had values > nums[r], and they were the newest. The previous back (before the popped ones) has value ≤ nums[r]. After extending, the popped ones become value nums[r], and the new one is also nums[r]. So the back of the deque should be the new one (or merged with the previous back if equal). The popped ones are "absorbed" into the count.

So the algorithm for adding v = nums[r] to min-deque:
```
c = 1  # for the new suffix [r, r]
while minDeque and minDeque[-1].value > v:
    c += minDeque[-1].count
    minDeque.pop()
if minDeque and minDeque[-1].value == v:
    minDeque[-1].count += c
    minDeque[-1].sum_of_mins = minDeque[-1].value * minDeque[-1].count
else:
    minDeque.append(MinEntry(v, c, v * c))
```
But wait, the sum_of_mins for the merged entry is v * (new count), which is correct.

For max-deque, similarly but with < and max:
```
c = 1
while maxDeque and maxDeque[-1].value < v:
    c += maxDeque[-1].count
    maxDeque.pop()
if maxDeque and maxDeque[-1].value == v:
    maxDeque[-1].count += c
    maxDeque[-1].sum_of_mins = maxDeque[-1].value * maxDeque[-1].count
else:
    maxDeque.append(MaxEntry(v, c, v * c))
```

For removing the oldest suffix (when window size > k):
- The oldest suffix is the front. Decrement front.count by 1 and front.sum_of_mins by front.value. If front.count becomes 0, pop.
```
minDeque[0].count -= 1
minDeque[0].sum_of_mins -= minDeque[0].value
if minDeque[0].count == 0:
    minDeque.popleft()
```
Similarly for max-deque.

The total sum over active suffixes is:
- sum_min = sum of all entry.sum_of_mins in minDeque
- sum_max = sum of all entry.sum_of_mins in maxDeque
- total = sum_min + sum_max

This is O(n) amortized because each element is pushed and popped at most once in each deque.

Let me verify with the example: nums = [1, 2, 3], k = 2.
- r=0, v=1: minDeque = [(1,1,1)], maxDeque = [(1,1,1)]. sum_min=1, sum_max=1, total=2. Window [0,0], suffixes: [0,0] min=1 max=1. ✓
- r=1, v=2: 
  - minDeque: c=1, back.value=1 ≤ 2, so don't pop. Push (2,1,2). minDeque=[(1,1,1),(2,1,2)]. sum_min=3.
  - maxDeque: c=1, back.value=1 < 2, so pop: c=1+1=2. Now empty, push (2,2,4). maxDeque=[(2,2,4)]. sum_max=4.
  - total = 3+4=7. Window [0,1], suffixes: [0,1] min=1 max=2, [1,1] min=2 max=2. Sum = (1+2)+(2+2)=3+4=7. ✓
- r=2, v=3:
  - Window would be [0,2] size 3 > 2, so remove oldest: minDeque[0].count=1-1=0, pop. minDeque=[(2,1,2)]. sum_min=2. maxDeque: front (2,2,4), count=2-1=1, sum=4-2=2. maxDeque=[(2,1,2)]. 
  - Now add v=3:
    - minDeque: c=1, back.value=2 ≤ 3, push (3,1,3). minDeque=[(2,1,2),(3,1,3)]. sum_min=5.
    - maxDeque: c=1, back.value=2 < 3, pop: c=1+1=2. Empty, push (3,2,6). maxDeque=[(3,2,6)]. sum_max=6.
  - total = 5+6=11. Window [1,2], suffixes: [1,2] min=2 max=3, [2,2] min=3 max=3. Sum = (2+3)+(3+3)=5+6=11. ✓
- Total answer = 2+7+11 = 20. ✓

Great, the algorithm works! And it's O(n) time and O(k) space.

Let me code this up in Python.

```python
from typing import List
from collections import deque

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        # minDeque and maxDeque store (value, count, sum_of_values_for_these_count)
        # Values in minDeque are non-decreasing from front to back.
        # Values in maxDeque are non-increasing from front to back.
        minDeque = deque()  # for minimums of suffixes
        maxDeque = deque()  # for maximums of suffixes
        
        l = 0
        ans = 0
        n = len(nums)
        
        for r in range(n):
            v = nums[r]
            
            # Add v to minDeque
            c = 1
            while minDeque and minDeque[-1][0] > v:
                c += minDeque[-1][1]
                minDeque.pop()
            if minDeque and minDeque[-1][0] == v:
                # Merge: update the back entry
                val, cnt, _ = minDeque[-1]
                cnt += c
                minDeque[-1] = (val, cnt, val * cnt)
            else:
                minDeque.append((v, c, v * c))
            
            # Add v to maxDeque
            c = 1
            while maxDeque and maxDeque[-1][0] < v:
                c += maxDeque[-1][1]
                maxDeque.pop()
            if maxDeque and maxDeque[-1][0] == v:
                val, cnt, _ = maxDeque[-1]
                cnt += c
                maxDeque[-1] = (val, cnt, val * cnt)
            else:
                maxDeque.append((v, c, v * c))
            
            # Remove oldest suffix if window too large
            while r - l + 1 > k:
                # Remove suffix starting at l
                l += 1
                # Decrement front of minDeque
                val, cnt, sm = minDeque[0]
                cnt -= 1
                sm -= val
                if cnt == 0:
                    minDeque.popleft()
                else:
                    minDeque[0] = (val, cnt, sm)
                # Decrement front of maxDeque
                val, cnt, sm = maxDeque[0]
                cnt -= 1
                sm -= val
                if cnt == 0:
                    maxDeque.popleft()
                else:
                    maxDeque[0] = (val, cnt, sm)
            
            # Compute total sum for current suffixes
            sum_min = sum(entry[2] for entry in minDeque)
            sum_max = sum(entry[2] for entry in maxDeque)
            ans += sum_min + sum_max
        
        return ans
```

Wait, I need to be careful: when I merge in the minDeque after popping, I do:
```
if minDeque and minDeque[-1][0] == v:
    val, cnt, _ = minDeque[-1]
    cnt += c
    minDeque[-1] = (val, cnt, val * cnt)
```
But this only adds c to the back if the back has the same value. However, after popping, the new back has value ≤ v. If it's < v, we push a new entry (v, c). But wait, we popped entries with value > v. The new back (if exists) has value ≤ v. If back.value < v, then we push (v, c) as a new entry. But is the order correct?

The order in the deque should be by position (oldest to newest). The popped entries were the newest. After extending, they become value v, and the new suffix is also value v. So all these should be at the back in order of position (popped are older than new). But since they all have value v, we just accumulate the count. The previous back (if exists and value < v) stays where it is, and we push a new back (v, c). The new back is the newest. This maintains the order: previous back is older, new back is newer, both with values ≤ v (previous < v, new = v). The "popped + new" are all merged into the new back with total count.

Wait, but the popped entries had values > v and were the newest. The previous back had value ≤ v. So in the order: ..., previous_back (value ≤ v), popped1, popped2, ..., new. After extending, popped1, popped2, ..., new all have value v. So they should be merged into a single entry at the back with value v and count = sum of counts + 1. The previous_back stays as is. So yes, the logic is correct.

But there's an edge case: what if we pop everything? Then minDeque is empty, and we push (v, c) where c includes the popped counts + 1. That's fine.

Similarly for maxDeque.

Let me also double-check the removal step. The front of the minDeque corresponds to the oldest suffix. Its value is the min of that suffix. When we remove the oldest suffix, we decrement the count by 1. If the count becomes 0, we pop. The sum decreases by the value. This is correct because we're removing one occurrence of that min value from the "oldest suffix" position.

But wait: the front of the minDeque has the smallest value (non-decreasing). When we remove the oldest suffix, we're removing the suffix that starts at the leftmost position. Its min is the front.value (which is the global min of the window). But is the oldest suffix necessarily the one with the global min? Yes, because as we go from oldest to newest suffix, we remove the leftmost element each time, so the min can only stay the same or increase. So the oldest suffix has the smallest min, which is the global min. Hence front.value is the min of the oldest suffix. Correct.

Similarly, the front of the maxDeque has the largest value (non-increasing). The oldest suffix has the global max of the window. Correct.

So the algorithm is correct and O(n) amortized.

Let me trace through example 2: nums = [1, -3, 1], k = 2.
- r=0, v=1:
  - minDeque: c=1, empty, push (1,1,1). sum_min=1.
  - maxDeque: c=1, empty, push (1,1,1). sum_max=1.
  - total=2. Suffixes: [0,0] min=1 max=1, sum=2. ✓
- r=1, v=-3:
  - minDeque: c=1, back.value=1 > -3, pop: c=2. Empty, push (-3,2,-6). sum_min=-6.
  - maxDeque: c=1, back.value=1 > -3? No, 1 > -3 is true, so pop: c=2. Empty, push (-3,2,-6). sum_max=-6.
  - total = -6 + -6 = -12. Suffixes: [0,1] min=-3 max=1, [1,1] min=-3 max=-3. Sum = (-3+1)+(-3+-3) = -2 + -6 = -8. Wait, that's -8, not -12.
  
Hmm, discrepancy. Let me recheck.
  - [0,1]: nums[0]=1, nums[1]=-3. min=-3, max=1. min+max = -2.
  - [1,1]: nums[1]=-3. min=-3, max=-3. min+max = -6.
  - Total = -8.
  
But my algorithm gave -12. Let me recheck the deque.
  - After r=0: minDeque=[(1,1,1)], maxDeque=[(1,1,1)].
  - r=1, v=-3:
    - minDeque: c=1. back=(1,1,1), 1 > -3, so pop: c=1+1=2. Now empty, push (-3, 2, -6). minDeque=[(-3,2,-6)].
    - maxDeque: c=1. back=(1,1,1), 1 < -3? No (1 is not less than -3). So don't pop. maxDeque stays [(1,1,1)]? Then push (-3, 1, -3). maxDeque=[(1,1,1),(-3,1,-3)].
  - sum_min = -6, sum_max = 1 + (-3) = -2. total = -8. ✓

I made an error: for maxDeque, the condition is `while maxDeque and maxDeque[-1][0] < v`, and v=-3. back.value=1, 1 < -3 is False, so we don't pop. Then we check if back.value == v: 1 == -3 is False, so push (-3, 1, -3). So maxDeque=[(1,1,1),(-3,1,-3)]. sum_max = 1 + (-3) = -2. Correct.

So my earlier manual trace was wrong. The algorithm gives -8 for r=1, which matches.

- r=2, v=1:
  - Window size = 3 > 2, so remove oldest (l=0):
    - minDeque: front=(-3,2,-6), count=2-1=1, sum=-6-(-3)=-3. minDeque=[(-3,1,-3)].
    - maxDeque: front=(1,1,1), count=1-1=0, pop. maxDeque=[(-3,1,-3)].
  - Now add v=1:
    - minDeque: c=1. back=(-3,1,-3), -3 > 1? No. So don't pop. back.value == 1? No. Push (1,1,1). minDeque=[(-3,1,-3),(1,1,1)].
    - maxDeque: c=1. back=(-3,1,-3), -3 < 1, pop: c=1+1=2. Empty, push (1,2,2). maxDeque=[(1,2,2)].
  - sum_min = -3 + 1 = -2. sum_max = 2. total = 0.
  - Suffixes of window [1,2]: [1,2] min=-3 max=1, [2,2] min=1 max=1. Sum = (-3+1)+(1+1) = -2+2=0. ✓

Total answer = 2 + (-8) + 0 = -6. ✓ Matches expected.

Great, the algorithm is correct.

Now, the complexity: each element is pushed and popped at most once in each deque, so O(n) amortized. Space O(k) for the deques.

One small optimization: instead of summing all entries each time (which could be O(k) in the worst case if we do `sum(entry[2] for entry in minDeque)`), we can maintain a running total `total_min` and `total_max` that we update on each push/pop. This makes the entire algorithm strictly O(n).

Let me rewrite with maintained totals:

```python
from typing import List
from collections import deque

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        minDeque = deque()  # (value, count)
        maxDeque = deque()  # (value, count)
        total_min = 0
        total_max = 0
        
        l = 0
        ans = 0
        n = len(nums)
        
        for r in range(n):
            v = nums[r]
            
            # Add v to minDeque
            c = 1
            while minDeque and minDeque[-1][0] > v:
                val, cnt = minDeque.pop()
                c += cnt
                total_min -= val * cnt
            if minDeque and minDeque[-1][0] == v:
                val, cnt = minDeque[-1]
                cnt += c
                minDeque[-1] = (val, cnt)
                total_min += val * c
            else:
                minDeque.append((v, c))
                total_min += v * c
            
            # Add v to maxDeque
            c = 1
            while maxDeque and maxDeque[-1][0] < v:
                val, cnt = maxDeque.pop()
                c += cnt
                total_max -= val * cnt
            if maxDeque and maxDeque[-1][0] == v:
                val, cnt = maxDeque[-1]
                cnt += c
                maxDeque[-1] = (val, cnt)
                total_max += val * c
            else:
                maxDeque.append((v, c))
                total_max += v * c
            
            # Remove oldest suffix if window too large
            while r - l + 1 > k:
                l += 1
                # Decrement front of minDeque
                val, cnt = minDeque[0]
                cnt -= 1
                total_min -= val
                if cnt == 0:
                    minDeque.popleft()
                else:
                    minDeque[0] = (val, cnt)
                # Decrement front of maxDeque
                val, cnt = maxDeque[0]
                cnt -= 1
                total_max -= val
                if cnt == 0:
                    maxDeque.popleft()
                else:
                    maxDeque[0] = (val, cnt)
            
            ans += total_min + total_max
        
        return ans
```

This is clean and O(n) time, O(k) space.

Let me double-check the total_min update during the "add" step for minDeque:
- When we pop an entry (val, cnt) from the back, we're removing those suffixes from the "old min" calculation. So we subtract val * cnt from total_min. Correct.
- After popping, the new back (if exists and value == v) gets its count increased by c. We add val * c to total_min. Correct.
- If we push a new entry (v, c), we add v * c to total_min. Correct.

For the merge case (back.value == v), we add val * c to total_min. The old back already contributed val * old_cnt to total_min, and now it contributes val * (old_cnt + c), so the increase is val * c. Correct.

For maxDeque, similar logic with < and the value being the max.

For the removal step:
- Front of minDeque: decrement count by 1, subtract val from total_min. Correct.
- Front of maxDeque: decrement count by 1, subtract val from total_max. Correct.

This looks solid. Let me verify once more with example 1: nums=[1,2,3], k=2.
- r=0, v=1:
  - minDeque: c=1, empty, append (1,1), total_min=1.
  - maxDeque: c=1, empty, append (1,1), total_max=1.
  - ans += 2.
- r=1, v=2:
  - minDeque: c=1, back=(1,1), 1>2? No. back==2? No. Append (2,1), total_min=1+2=3.
  - maxDeque: c=1, back=(1,1), 1<2, pop: c=2, total_max=1-1=0. Empty, append (2,2), total_max=0+4=4.
  - ans += 3+4=7. Total ans=9.
- r=2, v=3:
  - Window size 3>2, remove l=0:
    - minDeque front=(1,1): cnt=0, total_min=3-1=2. Pop. minDeque=[(2,1)].
    - maxDeque front=(2,2): cnt=1, total_max=4-2=2. maxDeque=[(2,1)].
  - Add v=3:
    - minDeque: c=1, back=(2,1), 2>3? No. back==3? No. Append (3,1), total_min=2+3=5.
    - maxDeque: c=1, back=(2,1), 2<3, pop: c=2, total_max=2-2=0. Empty, append (3,2), total_max=0+6=6.
  - ans += 5+6=11. Total ans=20. ✓

Perfect.

One more check: k=1, nums=[5, -2, 3]. At most 1 element, so only individual elements.
- r=0, v=5: minDeque=[(5,1)], total_min=5. maxDeque=[(5,1)], total_max=5. ans+=10.
- r=1, v=-2: window 2>1, remove l=0: minDeque becomes empty? front=(5,1), cnt=0, pop, total_min=5-5=0. maxDeque front=(5,1), cnt=0, pop, total_max=5-5=0. Then add v=-2: minDeque=[(-2,1)], total_min=-2. maxDeque=[(-2,1)], total_max=-2. ans += -4.
- r=2, v=3: window 2>1, remove l=1: minDeque front=(-2,1), pop, total_min=-2-(-2)=0. maxDeque front=(-2,1), pop, total_max=-2-(-2)=0. Add v=3: minDeque=[(3,1)], total_min=3. maxDeque=[(3,1)], total_max=3. ans += 6.
- Total = 10 - 4 + 6 = 12. Expected: 5+5 + (-2)+(-2) + 3+3 = 10-4+6=12. ✓

The solution is correct and efficient.

Now, the constraints: n up to 80,000, k up to n, values up to 1e6. The answer can be large: for n=80k, k=80k, each subarray contributes up to 2e6, number of subarrays ~3.2e9, so answer up to ~6.4e15. This fits in Python int (unbounded). 

Time complexity: O(n) amortized. Space: O(k) ≤ O(n).

I'll provide this solution.

The problem asks to enclose the code within delimiters. The format says "enclose your code within delimiters" but doesn't specify which delimiters. Looking at the prompt, it says "You will use the following starter code" and shows the class. I'll just provide the code block with the solution.

Actually, looking again at the problem statement: "Format: You will use the following starter code to write the solution to the problem and enclose your code within delimiters." This likely means to wrap the code in some standard delimiters, perhaps triple backticks for the code block. I'll provide the full solution in a Python code block.

Let me write the final solution.

```python
class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        from collections import deque
        
        minDeque = deque()  # stores (value, count) for minimums of suffixes
        maxDeque = deque()  # stores (value, count) for maximums of suffixes
        total_min = 0
        total_max = 0
        
        l = 0
        ans = 0
        n = len(nums)
        
        for r in range(n):
            v = nums[r]
            
            # Add v to minDeque (monotonic non-decreasing)
            c = 1
            while minDeque and minDeque[-1][0] > v:
                val, cnt = minDeque.pop()
                c += cnt
                total_min -= val * cnt
            if minDeque and minDeque[-1][0] == v:
                val, cnt = minDeque[-1]
                cnt += c
                minDeque[-1] = (val, cnt)
                total_min += val * c
            else:
                minDeque.append((v, c))
                total_min += v * c
            
            # Add v to maxDeque (monotonic non-increasing)
            c = 1
            while maxDeque and maxDeque[-1][0] < v:
                val, cnt = maxDeque.pop()
                c += cnt
                total_max -= val * cnt
            if maxDeque and maxDeque[-1][0] == v:
                val, cnt = maxDeque[-1]
                cnt += c
                maxDeque[-1] = (val, cnt)
                total_max += val * c
            else:
                maxDeque.append((v, c))
                total_max += v * c
            
            # Remove oldest suffix if window size > k
            while r - l + 1 > k:
                l += 1
                val, cnt = minDeque[0]
                cnt -= 1
                total_min -= val
                if cnt == 0:
                    minDeque.popleft()
                else:
                    minDeque[0] = (val, cnt)
                val, cnt = maxDeque[0]
                cnt -= 1
                total_max -= val
                if cnt == 0:
                    maxDeque.popleft()
                else:
                    maxDeque[0] = (val, cnt)
            
            ans += total_min + total_max
        
        return ans
```

This should be the final answer.</mm:think>### PLAN
Use a two-pointer sliding window with two monotonic deques to maintain, for every window `[l, r]` of size at most `k`, the sum of minimums and sum of maximums over **all suffixes** of the window (i.e., all subarrays ending at `r` of length ≤ k). The key insight is that as we right-extend the window by one element, the mins/maxs of the existing suffixes can only move toward the new value, which we handle by popping from the back of each deque and merging counts — yielding O(1) amortized per step. When the window exceeds size `k`, we left-shrink by decrementing the count at the front of each deque. We also maintain running totals `total_min` and `total_max` so each iteration is O(1).
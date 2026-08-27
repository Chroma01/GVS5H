
## ideation
**Core difficulty:**  
We need the sum over all contiguous subarrays of length ≤ k of (min + max). For an array of length n up to 80 k, an O(n k) enumeration of subarrays is too slow. The classic O(n) technique for “sum of minimums of all subarrays” (or maximums) uses a monotonic stack that counts how many subarrays each element is the min/max. The twist is the length limit k: each element should only contribute to subarrays whose length does not exceed k.

**Key observation:**  
If we process the array left‑to‑right and keep the sum of (min + max) for all subarrays that *end* at the current index, then the total answer is the sum of these per‑position contributions. The challenge is to maintain this sum efficiently while the window length is capped at k.

**Candidate approaches:**  

1. **Monotonic stack with sliding window**  
   - Maintain two stacks (deques) of candidate minimums and maximums for the current window.  
   - As we move the right pointer `i`, push `nums[i]` into both deques while popping from the back to keep the deque for mins in non‑decreasing order and for maxes in non‑increasing order.  
   - Also pop from the front of each deque any indices that are ≤ i − k (out of window).  
   - The min of the window is `nums[minDeque[0]]`, the max is `nums[maxDeque[0]]`.  
   - We need the *sum* of (min+max) over **all** subarrays of length ≤ k ending at `i`.  
   - Brute force over all lengths from 1 to current window size is O(k) per position → O(n k) worst case, too slow.  
   - Need a way to compute the contribution in O(1) amortized using the stacks.

2. **Contribution method (like for unlimited subarrays)**  
   - For each element `nums[i]`, find the distance to the previous smaller element (for min) and to the next smaller element (or just next smaller) to determine how many subarrays it is the min for.  
   - With a length limit, we must clamp the “start index” of subarrays: a subarray can only start at most `k‑1` steps back.  
   - So for each element, the number of subarrays where it is the minimum is `min(i - left, k)`, where `left` is the index of the previous element `< nums[i]` (or −1 if none).  
   - Similarly for maximum using previous greater element.  
   - The total contribution of `nums[i]` is `nums[i] * (number of subarrays where it is min + max)`.  
   - Sum over `i` gives the answer.  
   - This runs in O(n) time with monotonic stacks because we only need previous smaller/greater elements, not next.  
   - The distance to the left is limited to `k`; the distance to the right (future) is naturally bounded by the next smaller/greater element, but we only need the number of valid subarrays ending at or after the next smaller/greater, which is exactly `i - left` if we look from the left side. Wait—need to be careful: we need the total number of subarrays where `nums[i]` is the unique min (or max). The classic formula for *all* subarrays is `left * right` where `left = i - prev_less` and `right = next_less - i`. But we only need the sum of (min+max), so we can attribute the value `nums[i]` to each subarray where it is the min. With length ≤ k, the start of the subarray can range from `max(prev_less+1, i - k + 1)` to `i` (inclusive). The end of the subarray is fixed at `i` if we are considering subarrays ending at `i`. But we also have subarrays that start before `i` and end after `i` where `nums[i]` is still the min. So we must consider both directions. However, the contribution of `nums[i]` to the total sum is `nums[i] * (number of subarrays where it is the min)`. This number is the product of the number of valid starts and the number of valid ends.  
   - The start index can be any index in `(prev_less, i]` (strictly greater than prev_less). With the length constraint, the start must be at least `i - k + 1`. So the number of valid start positions is `min(i - prev_less, k)`.  
   - The end index can be any index in `[i, next_less)`. But we are summing over all subarrays, so we need the number of valid end positions as well. However, the classic approach for the sum of minimums over **all** subarrays uses `nums[i] * left * right`. Here we have a global length cap `k` on the subarray length. The length is `end - start + 1`. If we fix `i` as the min, then `start` can be in `(prev_less, i]` and `end` in `[i, next_less)`. The length constraint is `end - start + 1 ≤ k`. This is more complex: the number of valid (start, end) pairs is not simply a product of independent ranges because the length depends on both.

3. **Alternative: Sliding window with a multiset of (min+max) per length?**  
   - For each right endpoint `i`, we want the sum of min+max for all subarrays ending at `i` with length ≤ k.  
   - If we could compute this sum in O(1) amortized as `i` advances, we’d be done.  
   - When we add a new element, it becomes the max for all subarrays ending at `i` where it is larger than previous elements? Not exactly.

**Pitfalls:**  
- The contribution method with left/right distances must account for the length cap. The cap couples start and end.  
- A pure sliding window with deques gives the min/max of the *current* window, but subarrays ending at `i` of different lengths have different mins/maxes. We cannot just take the window min and multiply by length.  
- Using a multiset (like `SortedList`) to maintain all window mins/maxes? Too slow.  
- The constraint `n = 80k` allows O(n log n) but not O(n k).  
- The “contribution” method can be adapted: for each element, we need the number of subarrays where it is the min and length ≤ k. This is equivalent to: for each element, count the number of subarrays (start, end) with start ≤ i ≤ end, length ≤ k, and `nums[i]` is the unique min. This is a 2D range counting problem with monotonic constraints. There is a known O(n) solution using two stacks (one for min, one for max) that tracks the number of subarrays ending at each position? Let's think.

**Better idea:**  
Process from left to right, maintaining a stack of pairs (value, count) for the minimums similar to the classic “sum of subarray minimums” but with a window size limit. In the classic problem, the stack stores increasing values, and for each new element `x`, we pop elements larger than `x`, and for each popped element `v` with count `c`, we can compute that `v` contributes to subarrays ending at the current index. Specifically, if we denote the stack before push as `[(v1, c1), (v2, c2), ...]` (non-decreasing), and we push `x` with count 1, then the sum of minimums of all subarrays ending at index `i` is the sum over the stack of `v_j * (sum of counts of elements at and above j?)`? Actually, the classic iterative method:  
- Maintain a stack of `(value, count)` where the stack is strictly increasing.  
- For each `x = nums[i]`, let `cnt = 1`.  
- While stack not empty and stack[-1].value >= x: pop `v, c`. The subarrays that had `v` as the minimum now have `x` as the minimum. The total number of subarrays ending at `i` where the minimum is `v` is exactly `c` (the number of subarrays ending at the previous index that had that stack state). But the classic method for the sum of minimums of all subarrays (not ending at i) uses:  
```
res = 0
stack = []  # (value, count)
for x in nums:
    cnt = 1
    while stack and stack[-1][0] > x:
        val, c = stack.pop()
        res -= val * c
        cnt += c
    stack.append((x, cnt))
    res += x * cnt
    total += res
```
Wait, that's for sum of minimums of all subarrays **ending at i**? Actually, the `res` variable in that code is the sum of minimums of all subarrays ending at the current index. Let's verify:  
- When we see a new element `x`, we are forming subarrays ending at thecurrent index. The stack keeps track of the minimums of subarrays ending at the previous index.  
- The algorithm: start with `cnt = 1` for the subarray consisting of just `x`.  
- While the stack top has value > `x`, that means for the subarrays that previously had that larger minimum, now `x` is smaller, so they switch to `x`. We subtract the old minimum's contribution and add `x` to the count.  
- After the loop, we push `(x, cnt)` onto the stack. The current `res` is the sum of minimums of all subarrays ending at `i`. The total answer for the problem is the sum of `res` over all `i`.  
This is O(n) and works for *all* subarrays (no length limit).  

Now we need a length limit k. The stack method naturally handles subarrays ending at the current index, but the count `cnt` for each stack entry corresponds to the number of subarrays ending at the current index that have that minimum. If we want to restrict subarrays to length ≤ k, we need to know how many of those subarrays are too long (i.e., started before `i - k + 1`). For a stack entry with count `c`, it represents `c` subarrays that all start at different positions. The earliest start for a subarray with minimum `v` is determined by the previous element in the stack (or the beginning of the array). But we can also maintain the starting index of each subarray in the stack? In the classic method, the stack implicitly groups subarrays by their minimum. The `count` is the number of consecutive subarrays (by length) that have the same minimum. For example, if the stack is `[(2, 3), (5, 2)]`, it means for subarrays ending at `i`, the minimums are: three subarrays have min=2, two subarrays have min=5. The subarrays with min=2 are the ones of length 1, 2, 3 (the three most recent ones). The subarrays with min=5 are the longer ones? Actually, no: the stack is built so that the counts are cumulative from the left. The subarrays are grouped by their start: the first `cnt` subarrays (of lengths 1..cnt) have the top-of-stack as the min, then the next group has the next stack element as the min, etc. But it's not exactly that; it's that the subarrays are partitioned by the points where the minimum changes.  

Specifically, for subarrays ending at index `i`, the minimum values as we extend the subarray backwards are: for length 1, min = nums[i]; for length 2, min = min(nums[i-1], nums[i]); for length 3, min = min(nums[i-2], nums[i-1], nums[i]); etc. The monotonic stack method groups these lengths into blocks where the minimum is constant. The `count` in the stack entry is the number of lengths (i.e., subarrays) for which that stack value is the minimum. The subarrays are ordered from shortest to longest. The stack is increasing, so the top of the stack corresponds to the most recent (shortest) subarrays, and the bottom to the longest. So if the stack is `[(2, 3), (5, 2)]` and the array is, say, `[5, 2, 2]`, then for subarrays ending at the last index: lengths 1 and 2 have min 2 (count 3? wait, maybe 2). Let's test: nums = [5, 2, 2].  
- i=0: stack=[(5,1)], res=5.  
- i=1: x=2. Pop (5,1), res-=5*1=0, cnt=1+1=2. Push (2,2). res+=2*2=4. res is 4. Subarrays ending at 1: [2] min=2, [5,2] min=2. Sum=4. Correct.  
- i=2: x=2. Stack top is (2,2) with value >=2. Pop (2,2), res-=2*2=0, cnt=1+2=3. Push (2,3). res+=2*3=6. Subarrays ending at 2: [2] min=2, [2,2] min=2, [5,2,2] min=2. Sum=6. Correct.  

So the `count` is exactly the number of subarrays (by length) that have the corresponding minimum. They are the most recent `count` subarrays (shortest lengths). So if we want to limit subarray length to k, we simply need to know, for each stack entry, how many of those `count` subarrays are actually within the last k positions. That is, we need to know the start index of the subarray. The subarray of length `L` (where L is 1..current_window_length) ending at `i` starts at `i - L + 1`. The condition `L ≤ k` means start ≥ `i - k + 1`. The stack groups lengths by their minimum. The lengths in a stack entry are contiguous: they are a suffix of the lengths 1..max_len. For example, in the above, at i=2, the stack is `[(2,3)]`, meaning all lengths 1,2,3 have min 2. The max length is 3. If k=2, we only want lengths 1 and 2. The count of valid lengths is `min(count, k)`. But also we must ensure that the subarrays of those lengths are within the window: the start index must be ≥ i - k + 1. For a stack entry with count `c` at the bottom of the stack, the lengths are the largest ones. For example, if the stack is `[(1,2), (3,3)]` at some i, the lengths for min=3 are the largest 3 lengths (i.e., lengths 4,5,6? No, the count is the number of subarrays, which corresponds to lengths 1..6? Let's be precise.

The stack is built such that the counts are the number of subarrays ending at i that have the stack value as the minimum. These subarrays are exactly those whose start is in some interval. The stack values are increasing. The subarrays with minimum = stack[-1] (the top) are the shortest ones. The subarrays with minimum = stack[0] (the bottom) are the longest ones. The lengths (i.e., start positions) for a stack entry at position `j` (from the bottom) are contiguous: they are the lengths from `S_{j+1} + 1` to `S_j`, where `S_j` is the cumulative count of the first j+1 entries. Wait, the stack is stored from bottom to top. The top is the smallest value (most recent minimum). The bottom is the largest value. The subarrays are ordered from shortest to longest. So the top corresponds to lengths 1..cnt_top. The next corresponds to lengths cnt_top+1 .. cnt_top+cnt_next, etc. The bottom corresponds to the largest lengths up to the total number of subarrays ending at i (which is min(i+1, some limit)).  

So if we want to limit to lengths ≤ k, we need to consider only the subarrays whose length is ≤ k. These are the first k subarrays (shortest). If the total number of subarrays ending at i (i.e., i+1) is > k, we need to drop the longest ones. The stack can be truncated accordingly.  

We can modify the classic algorithm to keep only the contributions of subarrays with length ≤ k. As we iterate, we can maintain the stack but also ensure that the total count in the stack (i.e., the sum of counts) does not exceed k. When we push a new entry, if the total count exceeds k, we need to reduce the count of the bottom entries (the largest lengths) because those are the ones that become invalid (too long).  

Similarly for the maximum, we maintain a separate stack (non-increasing) for the maximums. Then the total sum of (min+max) for subarrays ending at i with length ≤ k is the sum of the stack contributions. We add that to the global answer.  

This approach is O(n) amortized because each element is pushed and popped at most once from each stack, and the truncation at k is O(1) amortized (since we only remove from the bottom when the total length exceeds k, and each element can be removed from the bottom only once across the whole algorithm? Actually, the bottom removal happens as the window slides, but the stack can grow and shrink. However, with the length cap k, the total count in the stack is at most k. Since k ≤ n, but we process n elements, the total work for adjusting the bottom could be O(n) in the worst case if we shift the window one by one. But we can maintain a double-ended queue for the stacks? No, the stacks are monotonic and we can only pop from the back (for updating minimum) and we need to pop from the front (to remove old subarrays). The stack is a list; popping from the front is O(n) if it's a list. We need a data structure that supports push-back, pop-back, and pop-front, and we need to keep the order (monotonicity) and also track the counts. A deque can do push-back and pop-back, but not pop-front efficiently while maintaining the order? Actually, a deque supports O(1) push-back, pop-back, and push-front, pop-front. But we need to pop from the front of a monotonic stack while preserving the monotonic property? The monotonic stack is stored in a deque where the front corresponds to the largest values (bottom of the stack) and the back corresponds to the smallest values (top). When we push a new element, we pop from the back while the back has value > x (for min). When we need to remove the oldest (largest lengths) subarrays because the window length exceeds k, we need to reduce the count of the front element. If its count becomes 0, we pop it from the front. This is exactly a deque. However, the monotonic property is only violated if we pop from the front, but the front is the largest value. The new element being pushed is smaller (or equal) than the front? Not necessarily. But the deque order is still non-decreasing from front to back. When we pop from the front, the next element becomes the front, and it's still ≤ the next, etc. So the order is preserved.  

But wait: when we push a new element, we pop from the back to maintain non-decreasing order. The back is the smallest. The new element is smaller, so we pop. That's fine. The front is the largest. When we remove the oldest subarray (because it's too long), we decrease the count of the front. If the count reaches 0, we pop the front. The next element in the deque becomes the new front, and it's ≤ the old front, but could be larger than some elements in the middle? No, because the deque is non-decreasing from front to back, so all elements after the front are ≥ the front. So the order remains non-decreasing.  

Thus we can use a deque for the minimum stack and another for the maximum stack (where for max we maintain non-increasing from front to back).  

The algorithm:  
- Initialize `ans = 0`.  
- For each index `i` from 0 to n-1:  
  - `x = nums[i]`.  
  - For the minimum deque `min_dq` (stores pairs `(value, count)`), we maintain the property that values are non-decreasing from front to back.  
    - To add `x`: we want to form subarrays ending at `i` with length ≤ k. The new subarray of length 1 has min = x.  
    - We need to merge with the previous stack. The standard way: start with `cnt = 1`. While `min_dq` is not empty and `min_dq[-1].value > x`: pop the back, and add its count to `cnt`, and also subtract its contribution from the current sum of mins? Wait, we need to maintain the sum of mins for the current window. Let's maintain a variable `cur_min_sum` which is the sum of minimums of all subarrays ending at `i` with length ≤ k. When we transition from `i-1` to `i`, we need to update `cur_min_sum`.  
    - The standard transition for all subarrays (no limit) is:  
      ```
      cnt = 1
      while min_dq and min_dq[-1].value > x:
          val, c = min_dq.pop()
          cur_min_sum -= val * c
          cnt += c
      min_dq.append((x, cnt))
      cur_min_sum += x * cnt
      ```
    - This works because the subarrays ending at `i` are formed by taking subarrays ending at `i-1` and either extending them (which may change the min) or starting new (length 1). The `cnt` accumulates the number of subarrays whose minimum is now `x` instead of the popped values.  
    - With a length limit `k`, the number of subarrays we can form is limited to `k`. So after we do the above, we must ensure that the total count in the deque (sum of all `c` in the deque) does not exceed `k`. If it exceeds, we need to remove subarrays from the front (the oldest, i.e., longest lengths).  
    - Specifically, let `total = sum(c for _, c in min_dq)`. If `total > k`, we need to reduce it to `k`. The oldest subarrays are those with the largest lengths. In the deque, the front corresponds to the largest minimum values? Actually, the front is the bottom of the stack, which corresponds to the longest subarrays (largest lengths). The subarrays are ordered by length from shortest (back) to longest (front). So to remove the longest ones, we pop from the front.  
    - When we remove a count `c` from the front, we subtract `val * c` from `cur_min_sum` and decrease the total count. We repeat until `total ≤ k`.  
    - However, note that when we push the new element, we might have popped some elements from the back and added their counts to `cnt`. Those counts correspond to subarrays of various lengths. The `cnt` now represents the number of subarrays (of various lengths) that have min `x`. The lengths of these subarrays are: they are the lengths that previously had the popped mins. So they are not necessarily the shortest lengths. Actually, in the standard algorithm, after popping, the new `cnt` is the number of subarrays ending at `i` that have min exactly `x`. These subarrays have lengths ranging from 1 to something. The standard algorithm doesn't keep track of the exact lengths, but the stack groups them. The bottom of the stack (front) has the largest lengths. The top (back) has the smallest lengths. The new `cnt` is added to the back. So the new subarrays with min `x` are the shortest ones (lengths 1..cnt). But wait: if we popped several elements, the new `cnt` is the sum of the popped counts plus 1. These correspond to the subarrays that were previously represented by the popped elements. Those subarrays have lengths that are the largest ones? No, let's think carefully.  

Consider the standard stack at index i-1: it stores the minimums of all subarrays ending at i-1. The stack is increasing, and the top (back) is the minimum of the most recent subarray (length 1). The counts are the number of subarrays with that minimum. The subarrays are ordered by length: the first count (top) are lengths 1..cnt1, the next are cnt1+1..cnt1+cnt2, etc. When we transition to i, we consider the new element x. For each subarray ending at i-1, we can extend it by appending x. The new minimum is min(old_min, x). The stack method pops all elements with value > x, because those subarrays now have min x instead. The popped elements represent subarrays of various lengths. The number of subarrays affected is the sum of their counts. But these affected subarrays are not necessarily the longest ones; they are the ones whose old min was > x. However, in the monotonic stack, the elements with larger values are closer to the top (smaller lengths) if the array is increasing? Wait, the stack is non-decreasing from bottom (front) to top (back). The top is the smallest value. So elements with larger values are at the bottom. When we pop from the back, we are popping the smallest values (largest in terms of index in the stack). Actually, the back is the top of the stack, which has the smallest value. So we pop while the top value > x. Since the stack is non-decreasing, the top is the smallest, so if the top > x, then all elements in the stack are > x. So we pop everything. That means x is smaller than all previous minimums. Then the new min for all subarrays is x. The cnt is the total number of subarrays + 1. So the new subarrays are all lengths 1..total+1. The stack now has one entry (x, total+1). This matches: the shortest subarray is length 1, the longest is total+1.  

Now, if the stack has multiple entries, say `[(2,2), (5,3)]` (front to back). The top is (5,3) with value 5. If x=3, we pop (5,3) because 5 > 3. We add its count to cnt: cnt=1+3=4. Then we check the new top: (2,2) with value 2. 2 > 3? No, 2 <= 3, so we stop. We push (3,4). The new stack is `[(2,2), (3,4)]`. The total counts: 2+4=6. The subarrays ending at i with min 2 are the longest 2 subarrays (lengths 5 and 6? Or which lengths?). The subarrays with min 3 are the shortest 4 subarrays (lengths 1..4). So indeed, the new entry is at the back, representing the shortest lengths.  

Therefore, the order in the deque from front to back corresponds to longest lengths to shortest lengths. To enforce a length limit `k`, we need to keep only the first `k` subarrays (shortest lengths). That means we may need to remove some from the front (the longest ones) if the total count exceeds `k`.  

So the algorithm for minimum:  
- Maintain a deque `min_dq` of `(value, count)`.  
- Maintain `cur_min_sum`: sum of minimums of all subarrays ending at current index with length ≤ k.  
- Also maintain `total_min_count`: total number of subarrays (sum of counts in `min_dq`), which should be ≤ k.  

For each `x = nums[i]`:  
1. Start with `cnt = 1`.  
2. While `min_dq` and `min_dq[-1][0] > x`:  
   - Pop the back: `val, c = min_dq.pop()`.  
   - `cur_min_sum -= val * c`.  
   - `total_min_count -= c`.  
   - `cnt += c`.  
3. Append `(x, cnt)` to the back: `min_dq.append((x, cnt))`.  
   - `cur_min_sum += x * cnt`.  
   - `total_min_count += cnt`.  
4. While `total_min_count > k`:  
   - Pop the front: `val, c = min_dq[0]`.  
   - We need to reduce the count by `delta = total_min_count - k`.  
   - If `c <= delta`:  
     - `cur_min_sum -= val * c`.  
     - `total_min_count -= c`.  
     - `min_dq.popleft()`.  
   - Else:  
     - `cur_min_sum -= val * delta`.  
     - `min_dq[0] = (val, c - delta)`.  
     - `total_min_count -= delta`.  
5. Now `cur_min_sum` is the sum of mins for all subarrays ending at `i` with length ≤ k.  

Similarly for maximum: maintain a deque `max_dq` with non-increasing values from front to back. The same logic applies, but we pop while `max_dq[-1][0] < x` (since we want to keep larger values).  

Then `cur_max_sum` is the sum of maximums for subarrays ending at `i` with length ≤ k.  

The total contribution for index `i` is `cur_min_sum + cur_max_sum`. Add to `ans`.  

Finally return `ans`.  

**Complexity:** O(n) time, O(k) space (since deque size is bounded by k).  

**Verification with examples:**  
Example 1: nums = [1,2,3], k=2.  
- i=0: x=1.  
  - min: cnt=1. min_dq empty. push (1,1). cur_min_sum=1, total=1. total<=2.  
  - max: cnt=1. max_dq empty. push (1,1). cur_max_sum=1, total=1. total<=2.  
  - ans += 1+1 = 2.  
- i=1: x=2.  
  - min: cnt=1. min_dq back: (1,1) val=1 <=2, so no pop. push (2,1). cur_min_sum += 2*1 = 1+2=3. total=1+1=2.  
  - max: cnt=1. max_dq back: (1,1) val=1 < 2, so pop. val=1, c=1. cur_max_sum -= 1*1 = 0. cnt += 1 -> 2. max_dq empty now. push (2,2). cur_max_sum += 2*2 = 4. total=2.  
  - ans += 3+4 = 7. Total ans=9.  
- i=2: x=3.  
  - min: cnt=1. min_dq back: (2,1) val=2 <=3. push (3,1). cur_min_sum += 3*1 = 3+3=6. total=2+1=3. Now total=3 > k=2, so remove from front. min_dq front: (1,1). delta = 3-2=1. c=1 <=1, so pop front. cur_min_sum -= 1*1 = 5. total=2.  
  - max: cnt=1. max_dq back: (2,2) val=2 <3. pop. cur_max_sum -= 2*2 = 0. cnt += 2 -> 3. max_dq empty. push (3,3). cur_max_sum += 3*3 = 9. total=3. total>2, remove front. front: (3,3). delta=1. c=3>1, so reduce count: c=2. cur_max_sum -= 3*1 = 6. total=2.  
  - ans += 5+6 = 11. Total ans=20. Matches.  

Example 2: nums = [1,-3,1], k=2.  
- i=0: x=1.  
  - min: push (1,1). cur_min=1. total=1.  
  - max: push (1,1). cur_max=1. total=1.  
  - ans += 2 -> 2.  
- i=1: x=-3.  
  - min: cnt=1. min_dq back: (1,1) val=1 > -3. pop. cur_min -=1*1=0. cnt=1+1=2. min_dq empty. push (-3,2). cur_min += -3*2 = -6. total=2.  
  - max: cnt=1. max_dq back: (1,1) val=1 > -3? For max, we pop while val < x. Here 1 > -3, so not less. So no pop. push (-3,1). cur_max += -3*1 = 1-3 = -2. total=1+1=2.  
  - ans += -6 + (-2) = -8. Total ans = -6.  
- i=2: x=1.  
  - min: cnt=1. min_dq back: (-3,2) val=-3 <=1. push (1,1). cur_min += 1*1 = -5. total=2+1=3. Remove front: min_dq front (-3,2). delta=1. c=2>1, reduce to c=1. cur_min -= -3*1 = -5 - (-3) = -2. total=2.  
  - max: cnt=1. max_dq back: (-3,1) val=-3 < 1. pop. cur_max -= -3*1 = -2 - (-3) = 1. cnt=1+1=2. max_dq empty. push (1,2). cur_max += 1*2 = 1+2=3. total=2.  
  - ans += -2 + 3 = 1. Total ans = -6. Matches.  

The algorithm works!  

**Implementation details:**  
- Use `collections.deque` for both deques. Each element is a tuple (value, count).  
- Keep `cur_min_sum` and `cur_max_sum` as long integers (Python int is arbitrary precision).  
- Keep `total_min` and `total_max` as the sum of counts in the respective deques.  
- The operations:  
  - `min_dq[-1][0]` for back.  
  - `min_dq[0]` for front.  
  - `min_dq.popleft()`, `min_dq.pop()`.  
- When reducing count at front, update the tuple. Since tuples are immutable, we need to modify the deque element. We can do something like:  
  ```
  val, c = min_dq[0]
  min_dq[0] = (val, c - delta)
  ```
  This works for `deque`.  
- We also need to handle the case when we pop from the front and the new count becomes 0, but since we only reduce by `delta = total - k`, and `total` is at most `k + something`, and we only pop when `total > k`, the `delta` is at most the count of the front element, so if we reduce to exactly k, the front count could become 0 only if we removed all of it. The code `if c <= delta: pop else: reduce` handles that.  

**Edge cases:**  
- k = 0? The problem says k >= 1, so fine.  
- Negative numbers: handled.  
- Large n: O(n) time, O(k) space.  

**Pitfalls:**  
- Be careful with the direction of the comparison: for min, we pop while `dq[-1].value > x`; for max, we pop while `dq[-1].value < x`.  
- The `cnt` accumulation: for min, we start with `cnt=1` (the new subarray of length 1). For max, same.  
- The `cur_min_sum` and `cur_max_sum` must be updated correctly when popping.  
- The removal from the front must update both the sum and the total count.  
- The total count in the deque is exactly the number of subarrays ending at i with length ≤ k. It should never exceed k after the removal step.  
- Initially, the deques are empty.  

**Testing:**  
- Small cases, random cases with brute force for small n to verify.  

**Conclusion:**  
The monotonic deque method with length cap is the optimal O(n) solution. The plan is solid.

## worker: Implement the `minMaxSubarraySum` method in Python
The solution uses the classic monotonic stack technique adapted for a sliding window of size `k`. Two deques are maintained: one for minimums (non-decreasing values) and one for maximums (non-increasing values). Each deque entry stores `(value, count)` where `count` represents the number of consecutive subarrays ending at the current index that have that value as their min/max.

**Key operations:**
1. **Update step**: When processing a new element `x`, we pop from the back while the value violates the monotonic property, accumulating their counts into a new entry. This handles the transition where the min/max of extended subarrays changes.
2. **Window trimming**: After updating, if the total number of subarrays (sum of counts) exceeds `k`, we remove from the front (oldest subarrays, i.e., longest lengths) until we're within the limit.

The running sums `cur_min_sum` and `cur_max_sum` always reflect the sum of minimums and maximums of all valid subarrays ending at the current index. Adding these to the answer at each step yields the total sum.

**Verification**: Tested against the provided examples:
- `[1,2,3], k=2` → 20 ✓
- `[1,-3,1], k=2` → -6 ✓

**Complexity**: O(n) time amortized, O(k) space. Each element is pushed and popped at most once from each deque, and the trimming operations are O(1) amortized since each subarray is removed from the front at most once.

We need to count subarrays that can be made non-decreasing with at most `k` total increments. For any subarray, making it non-decreasing means we can raise any element to satisfy `b[i] >= b[i-1]`, where `b[i] = a[i] + inc[i]`, `inc[i] >= 0`, and sum of `inc[i] <= k`. The minimum increments needed for subarray `[L..R]` is sum over i of `max(0, a[i] - target_{i})` where target is the smallest non-decreasing sequence bounded below by the original values. Equivalently, the minimum total increments equals the sum of "drops" that must be repaired when we scan left-to-right, but since we can only increase, we actually need to increase elements that are smaller than the running maximum.

A standard trick: for a subarray, the minimal increments needed = sum_{i in [L..R]} (prev_max - a[i])_+ where prev_max is the running maximum starting from L (we never need to increase anything that is already >= previous). This is exactly the total amount needed to "lift" the subarray to become non-decreasing while keeping elements as small as possible.

We need to count subarrays where this sum <= k. Use a sliding window / two-pointer: expand right pointer, maintain a data structure (monotonic stack with Fenwick tree or segment tree) to track contributions of each element to the "drops" as we move the right pointer. When total drops > k, move left pointer and update.

Maintain the running maximums using a decreasing stack. When we add a new element `x`, any elements in the stack smaller than `x` become "absorbed"; their previous contributions to drops must be recomputed because they no longer cause drops relative to larger elements to their right. We can use a Fenwick tree over the original positions to maintain the current required increments per position, and keep a running total.

Specifically:
- Store elements in a decreasing stack (values strictly decreasing). Each stack entry holds (value, original_index).
- Also maintain a Fenwick tree `bit` where `bit[i]` = current minimal increment needed for position i within the current window, i.e., `max(0, max_of_left_part_up_to_i - a[i])`.
- When extending right by index `r` with value `x = nums[r]`:
  - While stack top value < x: pop it, and for the range of indices from popped_index to r-1, we previously had contribution based on that popped value as the running max. Now the new max is x, so we need to add `(x - popped_value)` to each position in that range (since they were lifted by popped_value previously, now they need to be lifted by x). We do a range add on Fenwick (difference array technique: two point updates).
  - Push (x, r) onto stack.
  - Update total = total + (value of x minus something) ... Actually simpler: we track total via Fenwick sum of window.
- When total > k, shrink from left: remove position l, and adjust stack if l corresponds to a stack element (its value was the max for suffix). Since we may have removed an element that was the "anchor" for some range, we need to redistribute: the next element in stack (if any) becomes the max for the remaining range. Use Fenwick range adds to subtract appropriately.

This is complex but O(n log n) is feasible for n=1e5.

Alternative simpler O(n log n) approach: use divide and conquer / segment tree with "min cost to make prefix non-decreasing" queries. For each left, find max right such that cost <= k via binary search + segment tree to compute cost. The cost function for subarray can be computed by: `cost(L,R) = sum_{i=L+1..R} max(0, max_{j in [L..i-1]} a[j] - a[i])`. This is like a range query that can be answered with a monotonic stack and prefix sums in O(log n) per query with a sparse table for RMQ and a Fenwick for sum, but it's intricate.

Given the complexity, let me consider a cleaner two-pointer with a multiset maintaining "breakpoints".

Actually, there's a known approach: maintain the subarray as non-decreasing by tracking the "cost" which is sum of (max_so_far - a[i]) for i in window. This is essentially the area between the running max and the array. When we add a new element, if it's >= current window max, cost doesn't change. If it's smaller than the window max, cost increases by (window_max - a[i]). But that's only true if window max remains the same. However, if the new element is the new minimum and is much smaller, it doesn't retroactively change cost for previous elements. Wait — cost formula `sum (running_max_up_to_i - a[i])` where running_max is computed within the subarray. This running_max is non-decreasing, so when we append a new element smaller than current max, only the new element contributes. So cost increment is simply `max(0, current_window_max - a[r])`. This is straightforward!

But wait, this formula works only if we keep the entire window's "running max from the left" which is exactly the prefix max. Yes, for any prefix, the cost to make it non-decreasing (with minimum increments) is the sum of (prefix_max - a[i])_+ because each element just needs to reach the current prefix max. So the cost of subarray [L..R] is computed using prefix maxes within the subarray.

So we can maintain a two-pointer window with the current maximum `cur_max` and total cost `cost` which is sum of `max(0, cur_max_at_position - a[i])` where cur_max_at_position is the running max from L.

When we expand right:
- New running max = max(cur_max, nums[r])
- Cost increase = max(0, cur_max - nums[r]) (since running max only changes if nums[r] < cur_max; if nums[r] >= cur_max, the new element doesn't need increment, and cur_max becomes nums[r], so previous cost stays the same).
- Wait, if nums[r] >= cur_max, then cur_max becomes nums[r], but the previous cost is unchanged because the previous running max values are still the same. So cost increase is max(0, cur_max - nums[r]).

When we shrink left:
- We need to recompute the cost. The "cur_max" tracked was for the whole window. After removing left, the running max for the remaining subarray might decrease, and cost values for each position might change.

This complicates shrinking. But we can use a monotonic stack that stores "segments" where a particular value is the running max. This is the standard technique.

Let me think carefully. Define for window [L..R] the running max array M[i] = max(nums[L..i]). The cost is sum_{i=L..R} (M[i] - nums[i])_+ = sum_{i=L..R} M[i] - sum_{i=L..R} nums[i] where we only count when M[i] > nums[i]. But M[i] >= M[i-1] >= ... >= M[L] = nums[L]. So we can think of cost as area between M curve and nums.

When we expand right by r:
- M_new[i] = M[i] for i in [L..r-1]
- M_new[r] = max(nums[r], M[r-1]) = max(nums[r], cur_max)
- Cost addition = (M_new[r] - nums[r])_+ = max(0, cur_max - nums[r]) if M[r-1] = cur_max (which it is). If nums[r] >= cur_max, no addition and M_new[r] = nums[r], cur_max updates. So cost addition is max(0, cur_max - nums[r]).

So expanding is easy! The problem is shrinking. When we remove L, the running max changes for positions where M[i] = nums[L]. Specifically, for the suffix positions whose M was nums[L], the new M becomes the next smaller maximum in the window.

This is exactly the segment maintenance problem. Let me think of an alternative: binary search for each L the maximum R. For each L, we can simulate expanding R from L and at each step compute cost. But that's O(n^2) in the worst case.

Wait, we can use a "for each L, find max R with cost <= k" using a two-pointer and when L moves forward, we need to undo. The undo is the hard part.

Let me think of using a segment tree to compute cost of any subarray [L..R] in O(log n). Then we can do for each L, binary search R. But cost is not monotonic in R? Actually, as R increases, the running max only goes up, so M[i] for each i is non-decreasing in R, hence cost is non-decreasing in R. So binary search works.

Now, can we compute cost(L, R) in O(log n)? 
cost(L,R) = sum_{i=L..R} (max(nums[L..i]) - nums[i])_+.

Hmm. This is like: process the subarray, maintain a running max `mx`, and add `mx - nums[i]` if `mx > nums[i]`. This is a single pass.

I can preprocess a sparse table for RMQ (max in range) in O(n log n) and prefix sums in O(n). But I need to compute this for arbitrary (L,R) quickly.

Alternative: For a fixed L, as we increase R, the running max only changes at certain "breakpoints" — positions where nums[i] is a new maximum. Between breakpoints, the running max is constant, and the cost contribution is (mx - nums[i]) for each i, which can be computed using prefix sums of nums.

Specifically, let the "record-breaking" positions in nums be positions p_1=L, p_2, p_3, ..., p_m where nums[p_j] > all previous. The running max over [L..i] is nums[p_j] for i in [p_j .. p_{j+1}-1]. So:
cost(L, R) = sum_{j=1}^{m'-1} (nums[p_j] - (sum of nums in [p_j..p_{j+1}-1])) + (nums[p_{m'}] - (sum of nums in [p_{m'}..R]))

This requires knowing the record-breaking positions and prefix sums. The record-breaking positions depend on L.

This is getting complex. Let me reconsider the two-pointer with a monotonic stack approach for O(n) or O(n log n).

I recall a similar problem (LeetCode "Maximum Number of Non-Decreasing Subarrays After Modifications" or similar) where the approach is:

- Maintain a stack of (value, count) representing the current "maxima" of the window. Specifically, process the array left to right, and maintain a decreasing stack of (value, count) where the value is the running max in order. Also maintain a Fenwick tree for the cost.

Actually, let me look up the technique: "minimum increments to make subarray non-decreasing with k operations, count subarrays" is LeetCode 3251? Or similar.

I think the intended solution is O(n log n) with a monotonic stack + Fenwick tree.

Algorithm:
- Two pointers L, R.
- Maintain a decreasing stack of (value, original_index) — but since we need range operations, we use a stack of (value, count) where count is the number of consecutive positions that have this value as their running max.
- Maintain a Fenwick tree storing the "extra cost" per position: the amount of increment needed for that position to reach the running max.

When we add position r with value x = nums[r]:
- Let `cur_max` be the current window max (top of stack value).
- If x >= cur_max: 
  - The running max becomes x. No extra cost added (since x is already >= previous max).
  - Wait, but the previous positions in the window have running max = cur_max, and now the new position has running max = x. The extra cost for the new position is 0.
  - But the cost for previous positions might need to change? No, because they were compared to cur_max before, and now they're still compared to cur_max (their own running max is still cur_max, since running max is from left to that position, not from the new element).
  - Hmm, but actually the running max for the whole subarray [L..R] for position i is max of nums[L..i], which depends only on L and i, not on the suffix. So adding a new element to the right doesn't change the running max for previous positions. Good.
  - So if x >= cur_max, cost addition is 0, cur_max becomes x, and we push (x, 1) onto stack? No, we merge with previous equal values. But since stack is strictly decreasing, we just push (x, 1).
  - Wait, the stack stores the values that are "currently the max from some point to the end". Actually, the standard technique is: the stack stores the "peaks" of the running max. For window [L..R], the running max is piecewise constant, and the stack (from bottom to top) represents the increasing sequence of max values.
  
Let me redefine. Let the stack be a sequence of (value, span_length) from left to right in the window, where:
- The first element (bottom) has value = nums[L] and span = 1.
- For subsequent elements, each represents a block of positions where the running max is constant and equal to that value.
- The values are strictly increasing (so stack is increasing from bottom to top? No, wait).

Actually, let me think again. For window [L..R], the running max starts at nums[L] and increases at positions where nums[i] exceeds all previous values. So the values are non-decreasing. If we have a stack (bottom to top) with values v_1 < v_2 < ... < v_k, and spans s_1, s_2, ..., s_k summing to R-L+1, where the running max for the first s_1 positions is v_1, the next s_2 positions is v_2, etc.

So the stack is increasing in value from bottom to top. When we add a new element x:
- Find the first stack element with value >= x. If all are < x, then x becomes the new max (push to top).
- Actually, since the stack is increasing, and x is a new element appended, we need to compare x with the top of stack.
- Case 1: x >= top of stack value. Then the running max for the new position is x, and x is the new global max. We can push (x, 1) onto the stack. The previous top now represents a range that is "blocked" by x? No, the previous top's range still has running max equal to its value, which is < x. The new position has running max x.
- Case 2: x < top of stack value. Then the running max for the new position is top of stack value. The extra cost for this position is (top_value - x). We increment the "total cost" by this amount. We also need to record that this position has extra cost top_value - x. We push (x, 1) onto stack? But then the stack is no longer increasing. Hmm.

Wait, I think the stack should store the actual values of nums, not the running max. Let me reconsider.

The "monotonic stack" technique for this problem (I've seen it before) maintains a stack of (value, count) where the values are the nums values that are "relevant" as local maxima from the left, and we need to compute the cost dynamically.

Let me look at it differently. Define the cost of window [L..R] as:
C = sum_{i=L..R} (M(i) - nums[i]) where M(i) = max_{j in [L..i]} nums[j].

This is the area between the running max and the array. We can maintain this incrementally.

When we extend R to R+1:
- Let M_new = max(M(R), nums[R+1]) where M(R) is the running max at R.
- If nums[R+1] >= M(R): M(R+1) = nums[R+1], and the cost addition is 0 (since nums[R+1] >= M(R), the new element needs no increment to satisfy non-decreasing; in fact, the running max increases, but previous elements are unaffected).
  - Wait, but the cost formula for position R+1 is (M(R+1) - nums[R+1])_+ = 0.
  - Previous positions' cost is unchanged because their M(i) depends only on [L..i], not on R+1.
  - So C_new = C + 0. Good.
- If nums[R+1] < M(R): M(R+1) = M(R), and the cost addition is (M(R) - nums[R+1]).
  - C_new = C + (M(R) - nums[R+1]).

So extension is easy! We just need to know M(R) and add max(0, M(R) - nums[R+1]).

Now for shrinking L to L+1:
- The running max for the window changes. Specifically, for the new window [L+1..R], the running max at position i is max_{j in [L+1..i]} nums[j].
- For positions where the old M(i) = nums[L], the new M(i) might be smaller.
- For positions where the old M(i) > nums[L], the new M(i) is the same.

This is the hard part. We need to efficiently update the cost when L moves.

Here's a way: maintain a stack of (value, count) representing the "blocks" in the current window where the running max is a particular value. The stack is increasing in value from bottom to top. The bottom value is the first element's value, and counts the number of positions that have this running max before the next increase.

Specifically, after processing [L..R], the stack represents:
- Block 1: positions from L to p_2-1, running max = nums[L].
- Block 2: positions from p_2 to p_3-1, running max = nums[p_2].
- ...
- Block k: positions from p_k to R, running max = nums[p_k].
where p_2, p_3, ... are the positions of record-breaking values in [L..R].

The cost of the window is:
C = sum_{block j} count_j * value_j - sum_{i=L..R} nums[i]
  = sum_{block j} count_j * value_j - prefix_sum[R] + prefix_sum[L-1].

So if we can maintain the sum of count_j * value_j (call it S), and the prefix sums of nums, then C = S - (prefix_sum[R] - prefix_sum[L-1]).

Now, how does S change when we extend or shrink?

When we extend R to R+1 with value x = nums[R+1]:
- If x >= top of stack (the current max for the suffix, which is value of last block):
  - New running max for position R+1 is x.
  - The previous last block (running max = old_top) is unchanged? No wait, the last block ends at R. The new position R+1 has running max = x, which is a new block.
  - We push a new block (x, 1) onto the stack.
  - S_new = S + x * 1.
- If x < top of stack:
  - New running max for position R+1 is top value.
  - We need to increase the count of the top block by 1.
  - But the top block might have value v. We need to add v to S (since the new position contributes v to S).
  - However, we also need to handle that x is a new "candidate" that could be a running max for future elements.
  - In the monotonic stack approach, we also push x onto the stack but with count 1, and then merge blocks that are "dominated".
  - Specifically, since x < v (the current top), the running max for position R+1 is v, not x. But x is a new element, and for future extensions, the running max will be at least v until we encounter an element > v. However, x itself doesn't become a running max.
  - Wait, actually, the running max for position i is max(nums[L..i]). Since x < v, and v was already the max up to R, the running max for R+1 is v, not x. So x doesn't form a new block. We just extend the count of the top block.
  - But what about the future? When we encounter a value y > v, the running max for those positions is y. The previous positions still have running max v. So we don't need to store x at all.
  - Hmm, but what if we later remove L? The block structure might change. Specifically, if the bottom block (which was nums[L]) is removed, and x was in that block... no, x is at position R+1, which is not L.

Actually, I think the correct invariant for the stack is:
The stack contains the "record-breaking" values from the left up to the current position, but only those that are still "active" as the running max for some suffix.

Standard technique: maintain a stack of (value, count) where:
- values are increasing from bottom to top.
- The top of the stack is the current running max (i.e., the max of all elements seen so far in the window).
- When we add a new element x:
  - Let cnt = 1.
  - While stack is not empty and stack.top.value <= x:
    - Pop the top, say (v, c).
    - S -= v * c.
    - cnt += c.
  - Push (x, cnt) onto stack.
  - S += x * cnt.

Let's verify: 
- When we add x, the running max for the new position is max(previous max, x). 
- If x >= previous max: all previous blocks have value <= x, and the new running max is x. The new position is in a block with value x. Also, the previous blocks are "merged" into this new block? No, the previous positions still have their original running max. The issue is that the new position's running max is x, but the previous position's running max is whatever it was.
- Wait, I think I'm confusing "running max" with "max so far". Let me re-examine.

The running max M(i) = max_{j=L..i} nums[j]. This is the same as the maximum of all elements seen so far from the left. So M(i) is exactly the max of nums[L..i]. As i increases, M(i) is non-decreasing.

The blocks are defined by when M(i) changes. The first block has M(i) = nums[L] for i from L to the next position where a larger value appears. The second block has M(i) = the second record-breaking value, etc.

So the stack (bottom to top) values are exactly the record-breaking values, and each value's count is the number of positions until the next record-breaking value.

Now, when we add a new position R+1 with value x:
- If x < M(R) (the current max): the new position is in the same block as the previous one (the top block, with value M(R)). So we increment the count of the top block by 1.
- If x >= M(R): the new position starts a new block. The new block has value x. The previous top block's count remains the same (its positions still have running max = its value). We push a new block (x, 1) onto the stack.

But wait, what about the case x = M(R)? Then the new position has running max = x = M(R), and it's in the same block. So we should increment count, not push a new block. But in the stack invariant, if we have (M(R), c) on top and x = M(R), we should increment c to c+1. The "while stack.top.value <= x" would pop the top if x equals it. That's wrong for our purposes because we want to keep the block.

Actually, the block should end when a strictly larger value appears. So if x = M(R), the new position is in the same block. The "while" condition should be stack.top.value < x, not <=.

Let's redo:
- When adding x:
  - cnt = 1.
  - While stack is not empty and stack.top.value < x:
    - Pop top (v, c).
    - S -= v * c.
    - cnt += c.
    - (This means the popped block's positions now have a new running max for future elements, but their own running max is still v. However, since a larger value x has appeared, the running max for those positions would be x if we were considering them as part of a longer subarray. But for the current subarray ending at R+1, the running max for those positions is still v, not x, because running max is max(L..i), and for i in the popped block, max(L..i) = v < x. So their running max is unchanged.)
    - Hmm, but if we later extend further, the running max for those positions remains v, not x. So why are we popping?
  
  I think I see the confusion. The stack is for the "current" window, and the top of the stack should be the current maximum. When we add x, the current maximum becomes max(old_max, x). If x > old_max, the new maximum is x. The previous positions in the top block had running max = old_max, but now they are "overtaken" by x, meaning that for future elements, the running max will be x. However, the running max for those previous positions (for the purpose of computing cost) is still old_max, because cost is based on M(i) = max(L..i), not on future values.

So when we add x, and x > old_max, the cost for the new position is 0 (since M(R+1) = x = nums[R+1]). The cost for previous positions is unchanged. The stack should now have x on top, and the previous top block is still there with its value and count.

But why would we pop? We pop only if the new x causes some previous block to be "subsumed" in the sense that the running max for that block's positions will never increase beyond x for the current window. But that's not right because the running max for those positions is fixed once determined.

I think the correct stack invariant is: the stack stores the values of the record-breaking positions in the current window, in order. The top is the largest. The counts are the number of positions that have that running max.

When we add x:
- If x < top: increment top's count. (No new block.)
- If x >= top: we need to start a new block with value x. But wait, if x == top, then the new position has running max = x = top, so it's in the same block. We should increment count, not start new block.
- If x > top: the new position has running max = x. The previous top block is now "covered" by a higher max, but its own positions' running max is still its value. However, for future elements, the max will be x. We push a new block (x, 1). We do not pop the previous block because the previous positions still have their original running max for the purpose of cost calculation.

Wait, but then the stack would have multiple blocks with values that are increasing, and the sum S = sum value * count would give sum of M(i) for i in [L..R]. And cost = S - (prefix_sum[R] - prefix_sum[L-1]).

This works! Let's verify extension:
- Before extension, stack has blocks (v1, c1), (v2, c2), ..., (vk, ck) with v1 < v2 < ... < vk. Total positions = sum c_j = R - L + 1. S = sum v_j * c_j.
- Add position R+1 with value x.
  - If x < vk: top block count becomes ck + 1. S_new = S + vk * 1. Cost change = vk - x (since new position needs increment of vk - x to reach running max vk). And C_new = S_new - (sum up to R+1) = (S + vk) - (sum up to R + x) = C + vk - x. Matches the formula: cost addition is (old_max - x) = vk - x.
  - If x == vk: same as above, top block count becomes ck + 1. S_new = S + vk. Cost change = vk - x = 0. Good.
  - If x > vk: we need a new block. Push (x, 1) onto stack. S_new = S + x. Cost change = 0 (since new position needs no increment; running max is x = nums[R+1]). Good.

So for extension, the stack is simply:
- If x <= top value: increment top count.
- If x > top value: push (x, 1).

This is simple! And cost = S - (prefix_sum[R] - prefix_sum[L-1]) where S is the sum of (value * count) over blocks.

Now for shrinking L to L+1:
- The bottom block loses one position. Specifically, if the bottom block has count > 1, we just decrement its count by 1, and S decreases by v1.
- If the bottom block has count == 1, we pop it, and the new bottom is the next block. The positions that were in the popped block are gone. The new L is the next position, which was the start of the new bottom block. But wait, the new L is the start of the next block? No, the next block started at the position where the record-breaking value appeared. The new L is that position.
- So after popping, the new bottom block represents positions from new L onward. Its value is v2. The cost for the new window is S_new - (prefix_sum[R] - prefix_sum[new_L - 1]) where S_new is the updated S after removing the first position.
- But is the stack still valid? The new bottom block's value is v2, which is the running max for position new_L. But originally, for position new_L, the running max was v2 only because all previous elements (including the popped one) had value <= v2. Since the popped one had value v1 < v2, this is still true. So yes, the new bottom block is still correct: positions from new_L have running max >= v2, and specifically, position new_L has running max v2 (since nums[new_L] = v2 and v2 > v1 = old bottom). The subsequent positions in that block have running max v2 until a larger value appears, which is handled by the upper blocks.
- So the invariant is maintained!

Wait, is that true? Let's test: window [L..R] with blocks (v1, c1), (v2, c2), ... at bottom, with v1 = nums[L]. Remove L. New window starts at L+1. The first position of the new window is L+1. What is its running max? It is max(nums[L+1..L+1]) = nums[L+1]. 
- If c1 > 1, then L+1 is in the same block, with running max v1. So the new bottom block is still (v1, c1-1).
- If c1 == 1, then L+1 is the start of the next block, with running max v2. So we pop (v1,1), and the new bottom is (v2, c2). The new L is L+1 = start of the (v2) block.
- In both cases, the stack correctly represents the new window.

So shrinking is also simple:
- Decrement count of bottom block.
- If count becomes 0, pop it.
- Update S accordingly: S_new = S - value_of_removed_position.
- But we need to know the value of the removed position. The removed position is the current L, which is the start of the bottom block. Its value is the bottom block's value.
- Wait, the bottom block represents the first c1 positions, all with running max v1. The actual values of these positions could be anything <= v1, but the running max is v1. The first position has value v1 (since it's the max so far). The other positions in the block have values < v1.
- When we remove the first position (L), the value removed from the sum of nums is nums[L] = v1. So the prefix sum decreases by v1.
- The sum S decreases by v1 * 1 (since one position with running max v1 is removed).
- So cost change: C_new - C = (S_new - sum_new) - (S - sum_old) = (S - v1) - (sum - v1) - (S - sum) = 0? 
- Wait, that means cost doesn't change when we remove a position from the bottom block with count > 1? Let's check.
- Suppose window is [3, 1, 2] with L=0. nums = [3,1,2]. M = [3,3,3]. Cost = (3-3)+(3-1)+(3-2) = 0+2+1=3. S = 3+3+3=9. sum = 3+1+2=6. C = 3.
- Remove L=0 (value 3). New window [1,2]. M = [1,2]. Cost = (1-1)+(2-2)=0. S = 1+2=3. sum = 1+2=3. C = 0.
- C decreased by 3. S decreased by 6. sum decreased by 3. So C = S - sum. 9-6=3, 3-3=0. Change in C = change in S - change in sum = (-6) - (-3) = -3. Matches.
- In general, when we remove position L with value v_L = nums[L] = v1 (the bottom block value), S decreases by v1 (since one position with running max v1 is removed), and sum decreases by v1. So C changes by (S_new - sum_new) - (S_old - sum_old) = (S_old - v1) - (sum_old - v1) - (S_old - sum_old) = 0? 
- That would imply C is unchanged, which is wrong in the example.
- Ah, I see the mistake. When we remove L, the running max for the remaining positions might decrease if the removed position was the unique maximum for some suffix. But in the case where the bottom block has count > 1, the removed position is not the unique maximum for any other position (since other positions in the block have running max v1 because of the removed position, but after removal, their running max becomes the max of [L+1..i], which is still v1 if there are other elements equal to v1, or smaller).
- Wait, in the example [3,1,2], the first block is (3,1) because position 0 is 3, and no other position is 3. So c1=1. The second block is (max(1,2)=2, 1) for position 2? Let's recompute the blocks.
- For window [0..2] = [3,1,2]:
  - i=0: M=3. New max at i=0. Block (3,1).
  - i=1: nums[1]=1 < 3, so M=3. Same block. Block becomes (3,2).
  - i=2: nums[2]=2 < 3, so M=3. Same block. Block becomes (3,3).
- So the stack is just [(3,3)]. S = 9. Cost = 9 - 6 = 3. Correct.
- Now remove L=0. New window [1,2] = [1,2].
  - i=0 (new): M=1. New max. Block (1,1).
  - i=1: nums[1]=2 > 1, so M=2. New max. Block (2,1).
  - Stack: [(1,1), (2,1)]. S = 1 + 2 = 3. Cost = 3 - 3 = 0. Correct.
- When we had the old window, the stack was [(3,3)]. We remove the first position. The bottom block has value 3, count 3. We remove one position, so count becomes 2. New stack: [(3,2)]. S = 6. sum = 1+2=3. C = 6-3=3. But the correct cost for the new window [1,2] is 0. 
- The issue is that after removing position 0, the remaining positions 1 and 2 no longer have running max 3. Their running max is now based on [1,2]. Position 1 has running max 1, position 2 has running max 2.
- So the old block (3,3) is invalid. We need to "split" or "rebuild" the stack when we remove from the bottom.
- Specifically, the bottom block (3,3) represented positions 0,1,2 with running max 3. But after removing position 0, the running max for positions 1 and 2 changes because the prefix [1..i] has different max.
- So shrinking requires recomputation of the affected positions.

This is the crux of the difficulty. The "monotonic stack" technique for this problem likely uses a different invariant, or it uses a more sophisticated data structure.

Let me reconsider. The standard solution for this problem (LeetCode 3251 "Maximum Number of Non-Decreasing Subarrays After Applying Operations" or similar) might use a segment tree with binary search on L.

Actually, I recall a solution using "offline queries" or "parallel binary search": for each L, we binary search the maximum R such that cost(L,R) <= k, and we can compute cost(L,R) efficiently.

The cost(L,R) = sum_{i=L..R} (max(nums[L..i]) - nums[i])_+. 

This can be computed as: let the record-breaking positions in [L..R] be at indices p_0=L, p_1, p_2, ..., p_m where p_{j+1} is the next position after p_j where nums[p_{j+1}] > nums[p_j] (strictly greater, since if equal, it's the same running max). Wait, running max changes when we see a strictly larger value. So p_0 = L, p_1 is the first index > L with nums[p_1] > nums[L], p_2 is the first index > p_1 with nums[p_2] > nums[p_1], etc.

For positions in [p_j .. p_{j+1}-1], the running max is nums[p_j]. So the cost contribution is (nums[p_j] - nums[i]) for i in that range (where i >= p_j, and nums[i] <= nums[p_j]).

Cost(L,R) = sum_{j=0}^{m-1} sum_{i=p_j}^{min(p_{j+1}-1, R)} (nums[p_j] - nums[i]) + sum_{i=p_m}^{R} (nums[p_m] - nums[i]) (where p_m is the last record-breaking position <= R, or if no record-breaking after p_{m-1}, then p_m = p_{m-1} and the range is [p_{m-1}..R]).

Actually, for the last segment, if R >= p_m, the running max is nums[p_m], so cost = (R - p_m + 1) * nums[p_m] - sum_{i=p_m}^R nums[i].

This can be computed using prefix sums if we know the record-breaking positions. But finding them for each (L,R) is hard.

Alternative: think of the cost as the integral of (max - nums). We can precompute a structure that for any L, as we scan R from L to n-1, we can update the cost incrementally. But that's O(n^2) for all L.

Let's go back to the two-pointer with a segment tree. We want to count the number of (L,R) pairs with L <= R and cost(L,R) <= k.

Two-pointer: for each L, find the maximum R such that cost(L,R) <= k, then add (R - L + 1) to the answer. Move L to L+1, and adjust.

When we increase L by 1, we need to update the cost for the current window. Specifically, we need to "remove" the contribution of position L from the cost.

The cost of window [L..R] is sum_{i=L}^R (M(i) - nums[i]) where M(i) = max_{j=L..i} nums[j].

When L becomes L+1, the new M'(i) for i in [L+1..R] is max_{j=L+1..i} nums[j]. This is the same as M(i) except possibly for positions where M(i) = nums[L] (i.e., where the running max was achieved at L and nowhere else in [L+1..i]).

Specifically, define the "next greater or equal" position: for each index i, let next[i] be the smallest index > i such that nums[next[i]] > nums[i], or n if none. Then for position i, the running max from L is nums[L] for i in [L..next[L]-1] (assuming next[L] > L), and for larger i, the running max is determined by later record-breaking values.

More generally, the record-breaking positions form a chain starting from L. Let g(i) be the "parent" in the next-greater-element tree: g(i) = next index > i with nums[g(i)] > nums[i], or -1 if none.

Then the running max for position i (from L) is nums[ancestor] where ancestor is the first node on the path from L to i (in the NGE tree) that is <= i and has no ancestor between it and i. Actually, it's the maximum of nums[j] for j in [L..i]. In the NGE tree, the nodes on the path from L to the root (excluding root) are exactly the record-breaking values in order.

So M(i) = max{ nums[j] : j in [L..i] } = the last (largest) record-breaking value <= i starting from L.

This is the value of the "highest" ancestor of i in the NGE tree that is >= L? Not exactly.

Actually, in the NGE tree (where each node points to the next greater element to its right), the ancestors of i are exactly the record-breaking values that affect i. Specifically, if we build a tree where each node i points to nge[i] (next greater element), then the chain from L upwards visits the record-breaking values. For a query [L..R], the running max for position i is the first ancestor of i in this tree that is >= L? No.

Let me think differently. For a fixed L, as i increases from L to n-1, the running max M(i) is a non-decreasing function. It changes at positions where nums[i] is greater than all previous in [L..i]. These positions are exactly the nodes on the path from L to n in the "cartesian tree" or the NGE chain.

If we build the "max Cartesian tree" of the array (or just the NGE array), we can navigate.

But perhaps there's a simpler O(n log n) solution using a segment tree to maintain the "cost" as we slide L.

Here's an idea: maintain a segment tree or BIT that stores, for each position i in the current window, the "required increment" to make the prefix up to i non-decreasing relative to the current L. This is (M(i) - nums[i]).

When we move L, we need to subtract the contribution of position L. This is not local because it affects M(i) for all i where M(i) = nums[L].

We can use a "difference" approach. The running max M(i) is piecewise constant. For a given L, the "breakpoints" are the record-breaking positions. The cost is sum over segments of (max_val - sum_of_nums_in_segment).

When L moves to L+1, the new breakpoints are the old breakpoints minus L if L was a breakpoint, and the first breakpoint is the next record-breaking position. The segment that contained L is split or modified.

This is exactly what the monotonic stack with Fenwick tree does! Let me recall the full algorithm.

I think the algorithm is:
- Maintain a stack of (value, index) where the values are the "current maxima" in decreasing order? Or increasing?
- Actually, I found a reference: this is similar to the "number of subarrays with bounded maximum" but different.

Let me think about the problem as: for each L, we want to know the cost of [L..R] for varying R. The cost is a function of R. We can precompute for each L, the cost increases as R increases by specific amounts.

Specifically, cost(L,R) = cost(L,R-1) + (M(R-1) - nums[R])_+.

So if we can quickly determine for each L, the value of M(R-1) = max_{j in [L..R-1]} nums[j], we can compute the sequence of costs. But M(R-1) depends on L.

Another approach: precompute for each i, the "next greater element" nge[i]. Then for a window [L..R], the running max at R is the maximum of nums on the path from L to R in the NGE forest? Not quite.

Let's try to formalize: define the "cartesian tree" of the array based on max. Or just the NGE array: nge[i] is the first index > i with nums[nge[i]] > nums[i], or n if none.

For a subarray [L..R], the record-breaking positions are obtained by starting at L and repeatedly jumping to nge[pos] as long as nge[pos] <= R.

The running max M(i) for i in [L..R] is the value of the "current record" as we scan. The maximum value in [L..R] is nums at the last record-breaking position in the chain.

To compute cost(L,R) quickly, we could precompute sparse tables for RMQ and prefix sums. But the cost involves the sum of (max_prefix - a[i]) for each i, which is not just based on the global max.

Wait, here's an O(n log n) solution using a segment tree that supports range add and range sum, combined with two pointers.

We maintain a window [L..R] and the cost C. We also maintain an array "inc" where inc[i] is the current required increment for position i to make the window non-decreasing. Specifically, inc[i] = max(0, current_running_max_up_to_i - nums[i]).

When we extend R, we update inc and C. When we shrink L, we update inc and C.

The challenge is updating inc efficiently. The key insight is that the running max is a non-decreasing function. We can represent the "profile" of the running max using a set of intervals where the running max is constant.

When we extend R by one position with value x:
- The running max for the new position is max(previous_max, x). Let's call it new_mx.
- The previous positions in the window have their running max unchanged.
- So we only need to set inc[R] = max(0, new_mx - x).
- If new_mx > previous max (i.e., x > previous max), then the running max for the new position is x, and the new max is x.
- If new_mx == previous max, inc[R] = previous max - x.
- No other changes to inc for i < R.

So extending is O(1) and only affects the new position.

Now for shrinking L:
- We remove position L. This affects the running max for positions i >= L+1. Specifically, for positions where the running max M(i) = nums[L], the new running max M'(i) is the next maximum in [L+1..i].
- This is equivalent to: the "block" starting at L with running max = nums[L] is removed. The next block starts at the next record-breaking position.
- The affected positions are those that were in the "tail" of the removed influence.
- Specifically, the positions i in [L..R] where M(i) = nums[L] and the maximum is achieved uniquely at L (i.e., no other element in [L..i] has value nums[L] that is the running max).
- This is getting complicated.

But here's a neat trick: we can maintain the running max profile as a set of segments [start, end] with a constant max value. The segments are disjoint and cover [L..R]. The values are strictly increasing from left to right (since each new segment is triggered by a larger value).

When we extend R:
- The new position R+1 has value x.
- Find the rightmost segment in the profile. Let its value be v and its range be [s, R]. 
- If x < v: the new position joins the last segment. Extend the last segment to [s, R+1]. inc for the new position is v - x.
- If x >= v: the last segment ends at R (its range is [s, R]). A new segment starts at R+1 with value x. The new max is x. inc for R+1 is 0.
- Update C: C += inc[R+1].

When we shrink L:
- The leftmost segment [L, e] with value v is affected.
- If the segment has more than one position (e > L): just shrink the segment to [L+1, e]. The running max for the remaining positions in the segment is still v. However, is that correct? 
  - Consider segment [L, e] with value v = nums[L]. The positions in this segment have running max v. The segment ends at e, which is the position just before the next record-breaking value.
  - If we remove L, the new L is L+1. The position L+1 is in the same segment. Its running max is still v, because the max of [L+1..L+1] is nums[L+1] <= v, and for i > L+1 in the segment, max of [L+1..i] is still v because there is no value > v in the segment.
  - So yes, the segment just shrinks.
  - The cost C decreases by inc[L] = v - nums[L] = v - v = 0. So C is unchanged.
- If the segment has only one position (e = L): we pop this segment. The new leftmost segment starts at L+1 with its own value.
  - But wait, after removing L, the position L+1 becomes the new L. Its running max is no longer determined by nums[L] but by nums[L+1] and subsequent.
  - Specifically, the new leftmost segment should have value = nums[L+1] (since for i=L+1, M(i) = nums[L+1]).
  - The original leftmost segment was [L, L] with value v = nums[L]. The next segment started at some index s > L with value v2 > v.
  - After removing L, the new profile for the window [L+1..R] should be: the first segment is [L+1, s-1] with value nums[L+1]? No.
  - The new running max for position L+1 is nums[L+1] (which is < v since L+1 was in the old leftmost segment, so nums[L+1] < v).
  - The new running max for position s (the start of the old second segment) is max(nums[L+1..s]) = v2 (since v2 > nums[L+1] and v2 is in [L+1..s]).
  - The new running max for position i in (L+1, s) is max(nums[L+1..i]) which could be less than v.
  - So the new profile is completely different from just popping the first segment.
  - In fact, removing L causes a "cascade" where the running max for the suffix decreases.

So the profile changes significantly when we remove a segment of length 1. This is the hard part.

To handle this efficiently, we can use a data structure that supports "remove leftmost element" and maintains the cost. One approach is to use a Fenwick tree or segment tree with "range add" capabilities to update the cost for a range of positions.

Specifically, when we remove L and the old segment was [L, L] with value v, the new running max for positions in the old second segment and beyond changes. The new running max for a position i in the old second segment is the max of [L+1..i], which is the same as the old running max except possibly reduced from v to something else.

Actually, the old running max for positions in [L+1..R] was:
- For i in [L+1, s-1]: v (since they were in the first segment).
- For i in [s, ...]: some value >= v2.

The new running max for [L+1..R] is:
- For i = L+1: nums[L+1] (< v).
- For i in (L+1, s): max(nums[L+1..i]) <= v.
- For i >= s: max(nums[L+1..i]) = max(max(nums[L+1..s-1]), nums[s], ...) = max(local_max, v2, ...). Since v2 is the max of [s..i] (old), and local_max <= v < v2, the new max is still v2 or higher. So for i >= s, the new running max is the same as the old running max! Because the old running max for i >= s was max(v, max([s..i])) = max(v, v2, ...) = max([s..i]) since v2 > v. And the new running max is max([L+1..i]) = max(max([L+1..s-1]), max([s..i])) = max(local_max, max([s..i])) = max([s..i]) since max([s..i]) >= v2 > v >= local_max. So yes, for i >= s, the running max is unchanged.

Only the positions in [L+1, s-1] have their running max changed from v to some smaller value (specifically, the max of the prefix [L+1..i]).

So when we remove L (a single-position segment), we need to:
- Recompute the running max for positions in [L+1, s-1], where s is the start of the next segment.
- The new running max for i in [L+1, s-1] is the prefix max of [L+1..i], which is <= v.
- This is exactly the problem of computing the cost for the subarray [L+1, s-1] independently, plus the unchanged suffix.

So we can handle the left boundary by maintaining a structure that for the "active" suffix starting at some pivot, the profile is stable. This suggests a divide-and-conquer or a different approach.

Given the complexity, let me look for a different O(n log n) method.

**Binary search with segment tree for cost queries:**

For each L, we binary search the maximum R. To do this, we need to compute cost(L, mid) quickly. 

cost(L, R) = sum_{i=L..R} (M(i) - nums[i])_+ where M(i) = max(nums[L..i]).

We can compute this in O(log n) using a segment tree that stores, for each segment, the necessary information to combine.

Specifically, for a segment [l..r], we want to know:
- The minimum cost to make the segment non-decreasing (starting from some base).
- The final "height" (the value of the last element after making non-decreasing with minimum increments).
- Or more generally, for a segment, if we know the required initial value (the running max from the left), we can compute the cost and the final value.

This is a classic "segment tree for non-decreasing with cost" problem.

Define for each segment a function f: given the input value (the running max from the left, i.e., the value that the first element must be >= to satisfy non-decreasing from the left side), compute the minimum cost to make the segment non-decreasing and the final output value (the max at the end of the segment, which will be the input to the next segment).

But cost is (M(i) - a[i]) which is the sum of (running_max - a[i]). This is like we have a sequence, and we can increase elements. The cost is sum of increases.

If we think of the process: we scan left to right, maintaining a "target" that is non-decreasing. The target is max(target, a[i]). The cost is target - a[i] (if target > a[i]).

For a segment [l..r], if the input target is T (the value that a[l] must be raised to at least, coming from the left), then:
- We process the segment with initial target T.
- For each i, target = max(target, a[i]), cost += target - a[i].
- Final target is the value after processing r.

This is a piecewise function. The state is (T). The output is (cost, final_target).

This can be composed. Since the function is monotonic and piecewise linear with slopes, we can represent it compactly.

Actually, there's a known segment tree approach for this. Each node stores a "stack" of (value, count) similar to what we had before, but for the static segment.

For a node representing range [l..r], we store the profile of the running max if we start with target = 0 (or some reference). Specifically, we store the sequence of (max_value, span) for the segment, assuming initial target = 0.

Then for a query with initial target T, we combine: the effective running max is max(T, profile). We can compute the cost and the final profile.

This is exactly the "monotonic stack" segment tree. Each node stores a decreasing stack of (value, count) where value is the running max and count is how many positions have that running max.

Wait, for a fixed segment, the running max is non-decreasing. The profile is a sequence of (value, count) with values increasing.

To combine two segments left and right:
- The profile of the combined segment is: take the left profile. Then merge with the right profile, but the right profile's values are "lifted" by the final value of the left profile.
- Specifically, the final value of the left is the last value in its profile.
- The right profile has values v1, v2, ... These are the running maxes within the right segment assuming initial target = 0.
- With initial target T_left (the final value of left), the effective running maxes for the right segment are max(T_left, v1), max(T_left, v2), etc.
- Since v1 is the first value in the right profile, and the profile is increasing, max(T_left, v1) might be T_left if T_left > v1, or v1 if v1 >= T_left.
- The new profile is the merge of the left profile (unchanged) and the transformed right profile.
- The cost is the cost of left profile (computed with some initial T) plus the cost of the transformed right profile.

This allows O(log n) query for cost(L,R) if we can quickly compute the cost of a profile with a given initial T.

But we also need to handle the "final value" to pass to the parent.

This is doable with O(log^2 n) per query or O(log n) with careful segment tree design.

However, the binary search for each L would be O(n log^2 n) which is acceptable for n=1e5 (about 1e7 operations).

But we can do better with two pointers and a segment tree that supports point updates and range sum queries. Let's think if we can maintain the cost incrementally with a segment tree.

Actually, I think the intended solution for this LeetCode problem is O(n log n) with two pointers and a monotonic stack, using a Fenwick tree to handle the "range add" when we pop from the stack.

Let me try to design the full algorithm with Fenwick tree.

We maintain:
- A stack of "active" elements. Each element is a tuple (value, original_index).
- The stack is increasing in value? Or decreasing?
- We also maintain a Fenwick tree `bit` over the positions, storing the "extra cost" for each position.
- The total cost is the sum of the Fenwick tree over the window.

The key operations are:
- Add position r with value x.
- Remove position l.

When we add r with x:
- While stack is not empty and stack.top.value <= x:
  - Pop top (v, idx).
  - The popped element v was the "current max" for the range from idx to r-1.
  - Now the new max is x, so the running max for the range [idx, r-1] increases from v to x.
  - The extra cost for each position in [idx, r-1] increases by (x - v).
  - We do a range add of (x - v) on [idx, r-1] in the Fenwick tree.
- Push (x, r) onto stack.
- Also, we need to add the cost for position r itself. The running max for r is x (since x is the new max). So extra cost is 0.
- Wait, what if x <= old top? Then the running max for r is old top. The extra cost is old_top - x. We need to add this to the Fenwick tree for position r.
- And we push (x, r) onto the stack? But the stack should be increasing in value? Or the stack stores the "max so far" boundaries.

I think the stack should be decreasing in value. Let me think:
- The stack represents the "record-breaking" values in the current window.
- The bottom of the stack is the first element, with value nums[L].
- The top of the stack is the current maximum.
- Values are increasing from bottom to top.
- When we add a new element x, if x < top, it doesn't create a new record. The running max for the new position is top. We add (top - x) to the Fenwick for position r. We also need to "remember" that x is a potential future record-breaking candidate, so we push it onto the stack? But then the stack is no longer increasing.
- Actually, we push x onto the stack, but we also need to merge consecutive elements with the same "effective" max.
- Hmm, this is the same as before.

Let me look at the "next greater element" approach differently. 

For a fixed L, as we extend R, the cost increases by (current_max - nums[R])_+. The current_max is the max of [L..R-1]. This is easy if we have a segment tree to query the max in [L..R-1] and sum the (max - a[i]) values. But we need to sum over i.

Wait, here's an O(n log n) solution without two pointers, using divide and conquer on the value or index.

Actually, I think the two-pointer with Fenwick tree is the way. Let me look up the solution structure mentally.

I recall a solution that goes like this:
- Initialize ans = 0, L = 0.
- Maintain a stack of pairs (value, count) where the stack is increasing in value.
- Maintain a Fenwick tree for the "base" values.
- For each R from 0 to n-1:
  - Add nums[R] to the window.
  - While total_cost > k, remove nums[L] from the window, L += 1.
  - ans += R - L + 1.
- The key is implementing add and remove in O(log n).

When adding R:
- Let x = nums[R].
- We need to find the first element in the stack with value > x. The elements in the stack with value <= x are "dominated" by x.
- Actually, the stack represents the "current" record-breaking values. The values are strictly increasing.
- When we add x, we merge all elements with value <= x into a single element with value x.
- The count is the sum of counts of the merged elements plus 1.
- The cost for the new range [old_pos, R] where the running max was previously the merged values is now x, which is higher (or equal). So the cost increases.
- We use a Fenwick tree to track the contribution.

Specifically, let's define for each position i, the "required increment" = max(0, running_max_at_i - nums[i]).
When we add x at position R:
- Find the stack entries with value <= x. Let them be (v1, c1), (v2, c2), ..., (vk, ck) from bottom to top, with v1 < v2 < ... < vk <= x.
- These entries correspond to ranges: the first entry covers some range, the second covers a later range, etc.
- Actually, the stack entries are (value, count) where the count is the number of positions having that value as the running max.
- When we add x, for the positions in the ranges covered by the popped entries, the running max increases from vi to x.
- So the required increment for those positions increases by (x - vi).
- We do a range add of (x - vi) for each popped entry's range.
- Then we push (x, 1) onto the stack, but we need to merge it with the previous entry if it has the same value? Or we push (x, total_count).

But we need to know the actual index ranges to do range add. The stack entries are (value, count), but we need the start index of each range. We can store (value, count, start_index) or similar.

Let me try to write the algorithm:

```
stack = []  # each element is (value, count, start_idx)
# value is the running max for the count positions starting at start_idx
# start_idx is the first position in this block

total_cost = 0
L = 0
ans = 0
bit = Fenwick(n)  # to store the "extra" cost for each position

for R in range(n):
    x = nums[R]
    # Add position R
    count = 1
    # While stack top has value <= x, we need to merge
    # The positions from stack.top.start_idx to R-1 had running max = stack.top.value
    # Now they have running max = x (or higher)
    # So their cost increases by (x - stack.top.value) * stack.top.count
    # Wait, not exactly. The positions in the top block had running max = top.value.
    # The new running max is max(top.value, x) = x (since x >= top.value).
    # So each position in the top block needs an extra (x - top.value) increment.
    # This is a range add of (x - top.value) on the range [top.start_idx, R-1].
    # But we also need to handle that the top block might span multiple "sub-blocks" if the stack has multiple entries with value <= x.
    # Actually, if we pop all entries with value <= x, we are merging all their ranges.
    
    while stack and stack[-1][0] <= x:
        v, c, s = stack.pop()
        # Range [s, s+c-1] had running max v, now has running max x
        # But wait, the current R is not yet added. The range [s, s+c-1] are the positions in the popped block.
        # The new position R will have running max x.
        # So we do range add of (x - v) on [s, s+c-1].
        # But this is in the past, so we update the Fenwick tree accordingly.
        # However, the total cost is tracked elsewhere.
        
        # Update total cost: the cost for these c positions increases by (x - v) * c.
        # But we need to subtract the old cost and add new? No, the cost is (running_max - a[i]).
        # Old running max was v, new is x. So increase is (x - v) per position.
        # total_cost += (x - v) * c.
        
        count += c
        # But the start index of the merged block is s.
    
    # Now stack is empty or top.value > x.
    # We push a new block for position R with value x and count.
    # The new block covers [R-count+1, R] with running max x.
    # But wait, if we popped some blocks, the first position of the new block is the start of the first popped block, or R if none popped.
    # The cost for the new positions in this block: for position R, running max x, cost = x - nums[R] = 0.
    # For the other positions in the merged block, we already accounted for the increase.
    # So total_cost doesn't change for position R (since x - x = 0).
    
    # But we need to add the cost for position R: it's max(0, x - nums[R]) = 0.
    # And we need to set the Fenwick value for position R to 0? Or we use the Fenwick to track the "current running max" for each position.
    
    # Actually, let's track the running max in an array M, maintained via range updates.
    # When we add x and pop a block (v, c, s), we do M[i] += (x - v) for i in [s, s+c-1].
    # This is a range add.
    # The cost is sum (M[i] - nums[i]) over i in [L..R].
    # We can maintain M in a Fenwick tree with range add and point query, or use a difference array.
    # But we also need range sum of (M[i] - nums[i]), which is range sum of M[i] minus prefix sum of nums.
    # If we maintain M in a segment tree with lazy propagation supporting range add and range sum, we can get the total cost in O(log n).
    
    # Let's do that.
    
    # When we pop (v, c, s), we add (x - v) to M[s..s+c-1].
    # When we push the new block, we add x to M[R-count+1..R]? But M[R] is set to x, and the others were already updated.
    # Actually, after the pops, the range [R-count+1, R-1] was updated. Position R needs M[R] = x.
    # So we can just set M[R] = x via point update.
    
    # But we also need to handle the case where no pops happen. Then count=1, and we just set M[R] = x.
    
    # Wait, if no pops, the stack top has value > x. Then the new position R has running max = stack.top.value, not x.
    # So M[R] = stack.top.value, and the cost is stack.top.value - x.
    # And we push (x, 1, R) onto the stack.
    
    # Let's re-examine the while loop condition. We want to pop elements with value <= x because they are "dominated" by x.
    # But if we pop them, the new running max for their ranges becomes x.
    # If we don't pop (i.e., x < top.value), then the new running max for position R is top.value, and we push x as a new "candidate" that doesn't affect the current max.
    # In this case, we don't merge; we just push (x, 1, R) with count 1.
    
    # So the algorithm is:
    # count = 1
    # start = R
    # while stack and stack[-1][0] <= x:
    #     v, c, s = stack.pop()
    #     # M[s..s+c-1] was v, now becomes x
    #     add (x - v) to M[s..s+c-1]
    #     count += c
    #     start = s
    # 
    # if stack:  # there is a larger value on top
    #     # M[R] = stack[-1][0]
    #     set M[R] = stack[-1][0]
    #     # cost for R is stack[-1][0] - x
    #     # We don't push to stack? Or we push?
    #     # If we push, the stack is no longer increasing.
    #     # We need to push x as a new block with count 1
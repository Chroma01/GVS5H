
## ideation
We need the sum of (minimum + maximum) for every subarray of length L where 1 ≤ L ≤ k. Naively O(n·k) is too slow for n up to 80k. A classic approach is to count contributions element-wise using monotonic stacks (the “sum of subarray minimums/maximums” pattern), but we must cap the subarray length at k.

Key observations:
- For each index i, the number of subarrays where `nums[i]` is the **minimum** is `leftMin[i] * rightMin[i]`, where:
  - `leftMin[i]` = number of consecutive elements to the left (including i) that are strictly greater than `nums[i]` before hitting a smaller element.
  - `rightMin[i]` = number of consecutive elements to the right (including i) that are strictly greater-or-equal (or similar) before hitting a smaller element.
  The exact definition (strict vs. non-strict) can be chosen consistently so that each subarray’s minimum is counted exactly once.
- To enforce max length k, we clamp the right side: for each i, the farthest right start we can use is `min(rightMin[i], k)` (because we cannot extend more than k-1 elements to the right of i, and the count of valid ending positions ≤ i+rightBound is limited). Similarly, we can clamp the left side, but clamping only the right suffices if we sweep in order (or we can clamp both sides for safety). The clamped contribution for i as minimum is `nums[i] * leftMin[i] * min(rightMin[i], k)`. Wait, we must be careful: if the true `rightMin[i]` exceeds k, the valid right side is at most k, but the left side is still `leftMin[i]`. However, some combinations of left×right where both are large might produce subarrays longer than k. Actually, the number of subarrays of length ≤ k where i is the minimum and i is the *leftmost* (or any) position is not simply `leftMin[i] * min(rightMin[i], k)`. We must count pairs (l, r) such that l ≤ i ≤ r, r-l+1 ≤ k, and no element in [l, r] is smaller than `nums[i]`.

A clean way: for each i, define the “window” of subarrays where i is the minimum:
- L = number of valid left extensions = distance to previous smaller element (or start).
- R = distance to next smaller element (or end).
The total number of subarrays where i is the minimum and length ≤ k is the number of pairs (a, b) with 0 ≤ a < L, 0 ≤ b < R, and a + b < k (because the total length = a + 1 + b). This count can be computed in O(1) if we know L, R, and k: it’s `sum_{a=0}^{L-1} min(R, k - a)`.

Alternatively, we can sweep with a sliding window: iterate over right endpoints, maintain a monotonic deque of minima and maxima for the current window of size k, and add min+max of the window. The window size grows from 1 to k as we expand, and when it exceeds k, we shrink from the left. This yields O(n) time! We just need to sum for every window size from 1 to k. As we slide the right pointer, the current window is `[right-k+1, right]` (clamped to start at 0). For each right, we consider the window ending at right with length up to k. But the problem asks for all subarrays of length up to k, not just those ending at each right. However, if we process every possible subarray exactly once by iterating over all subarrays, that's O(n·k). But the sliding window technique: for each right endpoint, we add the current window’s min+max to the answer. As right increases, the left boundary is `max(0, right - k + 1)`. This window represents the subarray `[left, right]`. Does it cover all subarrays? No, only those ending at the current right. But we iterate right from 0 to n-1, so every subarray ends at some right. However, the sliding window of size k only includes the subarray of length exactly up to k ending at right. For a given right, the subarray `[left, right]` is included if and only if its length ≤ k. The window of size k includes all left from `right-k+1` to `right`, which is exactly all subarrays ending at right of length ≤ k. So if we can efficiently compute the min and max of all subarrays ending at right with length ≤ k, we sum them. But a subarray has exactly one right endpoint, so summing over right, the window `[max(0, right-k+1), right]` covers all subarrays of length ≤ k exactly once. The challenge: we need the min and max for **each** subarray ending at right with left ranging in that window. We cannot just take the min of the whole window, because different left endpoints give different min/max. We need the sum of mins + sum of maxes over all left in the window.

So the sliding window approach is not straightforward either.

Back to the element-wise contribution method with length cap. The formula for the number of subarrays of length ≤ k where i is the minimum: for a given i, let `L` = distance to previous smaller (or 0), `R` = distance to next smaller (or 0). We need the number of pairs (a, b) such that 0 ≤ a < L, 0 ≤ b < R, a+b < k. This is a standard combinatorial sum that can be computed in O(1) with simple algebra.

Let `cnt = 0`. For a from 0 to L-1, the max b is min(R-1, k-1-a). So:
`cnt = sum_{a=0}^{min(L, k)-1} min(R, k - a)`.
This can be computed in O(1) by noting the sum splits at the point where k - a < R.

Similarly for maximum (using previous greater and next greater).

Then total answer = sum over i of (cnt_min[i] + cnt_max[i]) * nums[i]. This is O(n) after O(n) stack passes to compute L and R for min and max.

Edge cases: when there are duplicates, we must ensure each subarray's min is counted exactly once. We can define for min: strictly less on the left, less-or-equal on the right (or vice versa) consistently. Similarly for max. Standard trick: for min, we want left distance to previous strictly smaller, right distance to next smaller-or-equal; for max, left distance to previous strictly greater, right distance to next greater-or-equal. This ensures each subarray's minimum is assigned to its leftmost minimum element (or rightmost, consistently). The exact choice doesn't matter as long as it's consistent for all subarrays and we use the same for all i.

Now, constraints: n up to 80k, values up to 1e6 (fit in 32-bit int). Sum might be up to roughly n * k * max_val ≈ 8e4 * 8e4 * 1e6 = 6.4e15, which fits in 64-bit (Python int is arbitrary). So no overflow issue.

We need to implement:
- Compute `L_min[i]`, `R_min[i]` using monotonic stack for strictly smaller on left, smaller-or-equal on right.
- Compute `L_max[i]`, `R_max[i]` for strictly greater on left, greater-or-equal on right.
- For each i, compute the capped count for min:
  `c_min = 0`
  `limit_a = min(L_min[i], k)`
  For a in 0..limit_a-1: `c_min += min(R_min[i], k - a)`
  But iterating a in a loop is O(k) in worst case (k up to n=8e4, n=8e4, O(n*k) = 6.4e9 too big). We must compute the sum in O(1).

Let's derive the O(1) formula.

We want `S = sum_{a=0}^{A-1} min(R, k - a)` where A = min(L, k).
Let `R' = R`. For a such that k - a ≥ R, i.e., a ≤ k - R, min is R. For a > k - R, min is k - a.

Case 1: k - R ≥ A - 1 (i.e., A ≤ k - R + 1). Then for all a in [0, A-1], min = R. So S = A * R.

Case 2: k - R < 0 (i.e., R > k). Then for all a, k - a < R (since k - a ≤ k < R). min = k - a for all a. S = sum_{a=0}^{A-1} (k - a) = A*k - A*(A-1)/2.

Case 3: 0 ≤ k - R < A - 1. Then split at a = k - R. Let `split = k - R`. For a=0..split: min = R. Count = split + 1. For a=split+1..A-1: min = k - a. Count = A - 1 - split. Sum = (split+1)*R + sum_{a=split+1}^{A-1} (k - a).
The second sum = (A - 1 - split)*k - (sum_{a=split+1}^{A-1} a) = (A-1-split)*k - [ (A-1)*A/2 - split*(split+1)/2 ].

We can combine these into a simple formula using min/max. But implementing the three cases is trivial and O(1).

Similarly for max.

We also need to be careful: the distance to previous smaller for i is the number of consecutive elements strictly greater than nums[i] immediately to the left, including i? Standard: L[i] = i - prev_smaller_index, R[i] = next_smaller_index - i. So the subarray can start at i - L[i] + 1 (up to i) and end at i + R[i] - 1 (down to i). The number of choices for left is L[i], for right is R[i]. So a ranges 0..L[i]-1, b ranges 0..R[i]-1. The formulas above are correct.

We must be careful that when computing R[i] with the "next smaller-or-equal" rule, the distance to the next element that is ≤ nums[i] (for min) is correct. Let's verify with a simple array and ensure no double counting. For min, we want each subarray's min assigned to exactly one index. If we use previous strictly smaller (i.e., the nearest index to the left with value < nums[i]) and next smaller-or-equal (nearest to right with value ≤ nums[i]), then the leftmost minimum in case of duplicates will be chosen. That's standard and correct.

For max, use previous strictly greater, next greater-or-equal.

Algorithm steps:
1. n = len(nums)
2. Compute prev_smaller[i]: index of previous element strictly smaller, or -1.
   Stack of indices with increasing values (monotonic increasing stack).
   For i in 0..n-1:
     while stack not empty and nums[stack[-1]] >= nums[i]: pop  (we want strictly smaller, so pop while >= to find last <)
     prev_smaller[i] = stack[-1] if stack else -1
     push i
   Then L_min[i] = i - prev_smaller[i].

3. Compute next_smaller_eq[i]: index of next element ≤ nums[i], or n.
   Stack of indices with increasing values.
   For i in n-1 down to 0:
     while stack not empty and nums[stack[-1]] > nums[i]: pop (we want ≤, so pop while >)
     next_smaller_eq[i] = stack[-1] if stack else n
     push i
   Then R_min[i] = next_smaller_eq[i] - i.

Similarly for max:
4. prev_greater[i]: index of previous element strictly greater, or -1.
   Stack of indices with decreasing values.
   while stack and nums[stack[-1]] <= nums[i]: pop
   prev_greater[i] = stack[-1] if stack else -1
   L_max[i] = i - prev_greater[i]

5. next_greater_eq[i]: index of next element ≥ nums[i], or n.
   while stack and nums[stack[-1]] < nums[i]: pop
   next_greater_eq[i] = stack[-1] if stack else n
   R_max[i] = next_greater_eq[i] - i

6. For each i, compute capped_count(L, R, k) using the O(1) formula above.

7. ans = sum_i nums[i] * (capped_count(L_min[i], R_min[i], k) + capped_count(L_max[i], R_max[i], k))

Let's test the capped_count function on small examples to be sure.

Example 1: nums = [1,2,3], k=2.
Min:
i=0: L=1 (prev smaller -1, 0-(-1)=1), R: next ≤ is index 1? Wait, nums=[1,2,3], next ≤ for 1 is index 1 (value 2 > 1, not ≤). Actually for next smaller-or-equal, we need ≤. For 1, next is 2 (2>1), then 3 (3>1), none ≤, so R=3. So L=1,R=3,k=2.
capped_count(1,3,2): A=min(1,2)=1. a=0: min(3,2-0=2)=2. So count=2.
i=1: val=2. prev smaller: index 0 (1<2). L=1. next ≤: index 2 (3>2? 3≤2? no), so R=2? Wait, next ≤ means ≤2. nums[2]=3 not ≤2, so R=2 (to end). L=1,R=2,k=2. A=min(1,2)=1. a=0: min(2,2)=2. count=2.
i=2: val=3. L=1. R=1. A=1. a=0: min(1,2)=1. count=1.
Min contributions: 1*2 + 2*2 + 3*1 = 2+4+3=9.

Max:
i=0: val=1. prev greater: none, L=1. next ≥: index 1 (2≥1), so R=1. L=1,R=1. A=1. a=0: min(1,2)=1. count=1. contrib 1*1=1.
i=1: val=2. prev greater: none, L=1. next ≥: index 2 (3≥2), R=1. A=1. a=0: min(1,2)=1. contrib 2.
i=2: val=3. L=1. R=1. count=1. contrib 3.
Max total = 1+2+3=6.
Total = 9+6=15? But expected is 20. Wait, discrepancy.

Let's manually compute min contributions for [1,2,3], k=2.
All subarrays length ≤2:
[1]: min=1
[2]: min=2
[3]: min=3
[1,2]: min=1
[2,3]: min=2
Sum of mins = 1+2+3+1+2 = 9. OK.
Sum of maxes: 1+2+3+2+3 = 11. Total 20.
But my max contribution calculation gave 6, not 11. Something is wrong with the max L,R or the capped count.

For max, we need to find for each i the number of subarrays where nums[i] is the maximum, with length ≤2.
i=0 (val=1): It is max only in subarray [1] (since [1,2] max is 2). So count should be 1. My calculation gave 1. OK.
i=1 (val=2): It is max in [2] and [1,2] and [2,3]? [2,3] max is 3, so not. So subarrays where 2 is max: [2], [1,2]. That's 2. My calculation gave 1. Because for i=1, prev greater: none, L=1. next greater-or-equal: index 2 (val 3 ≥ 2), R=1. So L=1,R=1. This means i=1 can only extend right 0 positions (since next greater-or-equal is at index 2, R=1). But wait, for subarray [2], it extends right 0; for [1,2], left 0, right 0. So indeed only those. But where is [2,3]? Max is 3, not 2. So correct.
i=2 (val=3): max in [3] and [2,3]. Count=2. My calculation: prev greater: none, L=1. next greater-or-equal: none, R=1. Wait, for i=2, L=1,R=1 gives count 1, but it should be 2. Because R should be 2? Let's check: next greater-or-equal means nearest index to the right with value ≥ nums[i]. For i=2, val=3, there is no element to the right, so R = n - i = 1. But [2,3] has length 2, which is ≤ k. In this subarray, 3 is the max. The subarray starts at index 1 (left extension 1) and ends at index 2 (right extension 0). So left choices: 1 (start at 1 or 2). Right choices: 1 (end at 2). So L=1, R=1, count = 1*1 = 1? But we have two subarrays: [3] and [2,3]. In [2,3], the max is 3. According to the element-wise method, the subarray [2,3] has max 3. The leftmost max? Only one max. The previous greater for index 2 is -1, next greater-or-equal is n. So L=2? Wait, distance to previous greater: i - prev_greater = 2 - (-1) = 3? No, L is the number of choices for left start. If prev_greater is -1, then the element is greater than all to the left, so we can start at index 0,1,2. That's 3 choices. So L should be i - prev = 2 - (-1) = 3. I mistakenly computed L=1. Because I thought L= i - prev, but if prev=-1, i-(-1)=i+1, which is the number of elements from 0 to i. So for i=2, L = 3. But earlier I said L=1. That's the error.

Let's recompute L and R correctly:
L = i - prev_idx
R = next_idx - i
where prev_idx is the index of the previous element that breaks the monotonicity (strictly greater for max), or -1.
For i=0: prev=-1, L=1. OK.
For i=1: val=2, prev greater? none, L=2? Wait, i=1, prev=-1, L=1 - (-1) = 2. But earlier I said L=1. Because for val=2, previous greater means strictly greater. The element at 0 is 1, which is not greater than 2. So we pop nothing? Actually, to find previous strictly greater, we maintain a decreasing stack. For i=0, push 0. For i=1, while stack and nums[stack[-1]] <= nums[i]: pop. nums[0]=1 <= 2, so pop 0. Stack empty. prev=-1. L=1-(-1)=2. So L=2. That means for val=2, it can be the maximum for subarrays starting at index 0 or 1. Indeed, [2] and [1,2]. And for [2,3], it is not max. So R=1 (next greater-or-equal is 2, index 2, R=2-1=1). So L=2,R=1. A=min(2,2)=2. a=0: min(1,2)=1; a=1: min(1,1)=1. Sum=2. So count=2. That matches.

For i=2: val=3, prev greater: while stack and nums[stack[-1]] <= 3: after previous step stack might be empty? Let's trace stack for max:
i=0 (1): stack empty, push 0. stack=[0]
i=1 (2): while top <= 2? 1 <= 2, pop 0. stack empty. prev=-1. push 1. stack=[1]
i=2 (3): while top <= 3? 2 <= 3, pop 1. stack empty. prev=-1. L = 2 - (-1) = 3.
next greater-or-equal: scan from right.
i=2 (3): stack empty, push 2.
i=1 (2): while top < 2? 3 < 2 false. So next = 2. R = 2-1=1? Wait, next_greater_eq for min was ≤, for max it's ≥. So we want next index with value ≥ nums[i]. For i=1, val=2, next index with ≥2 is 2. R = 2-1 = 1. That means it can extend right 0 positions? But we need [2,3]? Actually for max, for i=1, val=2, the subarray [2,3] has max 3, not 2. So R=1 is correct: it cannot extend right to include a larger or equal element that would dominate. For i=2, val=3, next greater-or-equal: none, R = n - 2 = 1? n=3, so R=3-2=1. Wait, if no next greater-or-equal, R = n - i = 1. But we need R to be the number of choices for right end. If next is n, R = n - i. For i=2, n=3, R=1. That means only one choice for right: end at 2. But we also have subarray [1,2]? No, that's for index 1. For index 2, subarrays where it is max and length ≤2: [3] (right end 2) and [2,3]? No, [2,3] ends at 2, starts at 1. That's one left choice (start at 1) and one right choice (end at 2). So L=1? Wait, L should be i - prev_greater. For i=2, prev_greater = -1, L=3. That means left can be 0,1,2. But can we have subarray starting at 0? [1,2,3] length 3 > k=2, not allowed. So L choices that satisfy length constraint: a in 0..2. But we also have right R=1. So a+b < k. With R=1, b=0 always. So we need a < k => a=0 or 1. So two subarrays: [3] (a=0) and [2,3] (a=1). So count=2. My earlier formula with L=3,R=1,k=2: A=min(3,2)=2. a=0: min(1,2)=1; a=1: min(1,1)=1. Sum=2. Correct. So if I had used L=3, it works. I mistakenly used L=1 earlier.

So the formulas are correct, just need to compute L and R properly.

Now test min again with proper L and R.
nums=[1,2,3], k=2.
Min:
prev_smaller: strictly smaller on left.
i=0: prev=-1, L=1.
i=1: val=2, while top >= 2? For min, we want strictly smaller on left, so we pop while >= to find last <. Actually to get previous strictly smaller, we maintain increasing stack and pop while >=. Let's do:
i=0: push 0 (1).
i=1: while top >= 2? nums[0]=1 >=2? No. So prev=0. L=1-0=1.
i=2: val=3, while top >=3? nums[1]=2>=3? No. prev=1, L=2-1=1.
So L_min: [1,1,1].
next_smaller_eq: ≤ on right.
i=2: push 2.
i=1: val=2, while top > 2? nums[2]=3>2, pop 2. stack empty. next=n=3. R=3-1=2.
i=0: val=1, while top > 1? empty, next=3. R=3-0=3.
So R_min: [3,2,1].
capped_count for i=0: L=1,R=3,k=2. A=min(1,2)=1. a=0: min(3,2)=2. count=2. contrib 2.
i=1: L=1,R=2,k=2. A=1. a=0: min(2,2)=2. count=2. contrib 4.
i=2: L=1,R=1,k=2. A=1. a=0: min(1,2)=1. count=1. contrib 3.
Sum min = 9. Good.

Now test with duplicates to ensure no double counting. Consider nums=[1,1], k=2.
Subarrays: [1] (idx0), [1] (idx1), [1,1] (min=1, max=1).
Sum of min+max: 2+2+2=6.
Min contributions:
prev_smaller: strictly smaller. For both, no smaller, L=1 each.
next_smaller_eq: ≤. For idx0, next is idx1 (1≤1). R=1. For idx1, next=n, R=1.
capped_count:
i=0: L=1,R=1,k=2. A=min(1,2)=1. a=0: min(1,2)=1. count=1. contrib 1.
i=1: L=1,R=1. count=1. contrib 1.
Min total = 2.
Max contributions:
prev_greater: strictly greater. For both, none, L=1.
next_greater_eq: ≥. For idx0, next=idx1. R=1. For idx1, R=1.
Counts: both 1. Max total = 2.
Total = 4? But expected 6. Because the subarray [1,1] has min=1, max=1, sum=2. We only got 4. The issue is that for subarray [1,1], both elements are equal. The min is 1, but we assigned it to idx0 (since next smaller-or-equal is at idx1, so idx0 is the leftmost minimum). That's correct: min=1 counted once. Max=1 counted once for idx0 (since next greater-or-equal is at idx1, idx0 is leftmost maximum). But we need the subarray [1,1] to contribute its min and max. It does: 1 (from min) + 1 (from max) = 2. So total should be 2 (mins) + 2 (maxes) + 2 (the [1,1] subarray adds both). But my max total was 2, min total 2, sum 4. Where is the other 2? Wait, the subarray [1,1] has min=1 and max=1. In my min sum, I have 1 (from idx0) + 1 (from idx1) = 2. That accounts for mins of all three subarrays: [1] idx0 (min 1), [1] idx1 (min 1), [1,1] (min 1). So min sum should be 3? Wait, [1] idx0 min=1, [1] idx1 min=1, [1,1] min=1. Total min sum = 3. But my calculation gave 2. Let's see: i=0 count=1, i=1 count=1. That gives min sum = 2. Why is the subarray [1,1] not counted? For i=0, subarrays where it is min: [1] (left 0, right 0). [1,1] (left 0, right 1). That's two subarrays. But my count gave 1. Why?
L_min[0] = distance to previous smaller = 1 (prev=-1).
R_min[0] = distance to next smaller-or-equal = 1 (next is idx1, which is ≤ 1). So R=1.
With L=1,R=1, the number of subarrays is L*R = 1. That means only [1]. But [1,1] should also be counted because 1 is the minimum and there is no smaller element to the right? Wait, for [1,1], the minimum is 1. Which index is the "leftmost minimum"? If we use "next smaller-or-equal" as the boundary, then for index 0, the next smaller-or-equal is at index 1 (since 1 ≤ 1). That means the subarray cannot cross index 1 because index 1 is ≤ 1. So index 0 is only the minimum for subarrays that do not include index 1? But [1,1] includes index 1. However, the minimum of [1,1] is 1, and both indices have value 1. The rule "next smaller-or-equal" would assign the subarray to the rightmost minimum? Let's check standard algorithm for "sum of subarray minimums". The standard approach is: for each element, find previous less (strictly) and next less-or-equal. Then the element is the minimum for subarrays that start after prev_less and end before next_less_eq. For [1,1], if we take element at idx0, its next less-or-equal is idx1, so the subarray must end before idx1, i.e., cannot include idx1. So idx0 is not the minimum for [1,1]. The minimum for [1,1] would be assigned to idx1? For idx1, previous strictly smaller: none. Next smaller-or-equal: none (since n). So L=2, R=1. L*R=2. Subarrays: [1] (idx1) and [0,1]? Wait, for idx1, L=2 means it can start at idx0 or idx1. R=1 means it can end at idx1. So subarrays: [1] (start 1) and [0,1] (start 0). That includes [1,1]! So idx1 gets the subarray [1,1] as its minimum. So the count for idx1 should be 2, not 1. My R_min[1] was 1? Let's recompute: for idx1, next smaller-or-equal: none, so R = n - i = 2 - 1 = 1. But if R=1, that means it can only end at idx1. But L=2 gives start at 0 or 1. So [0,1] is included. So count = 2. Why did I get count=1 earlier? Because I used A=min(L,k). For L=2,k=2, A=2. a=0: min(R, k-a) = min(1,2)=1. a=1: min(1,1)=1. Sum=2. So count=2. I mistakenly said A=min(1,2)=1. That was because I used L=1. So if we use correct L, it works. So the algorithm is correct; my manual check used wrong L for i=1.

Now for max: similar. For idx0, next greater-or-equal is idx1, R=1, L=1. Count=1. For idx1, L=2 (prev greater none), R=1, count=2. So max sum = 1*1 + 1*2 = 3. Min sum = 1*1 + 1*2 = 3. Total = 6. Perfect.

So the algorithm works. We just need to implement the O(1) capped count correctly.

Let's formalize the capped count function:

def capped_count(L, R, k):
    # L and R are the number of choices for left and right extensions (>=1)
    # We need sum_{a=0}^{L-1} sum_{b=0}^{R-1} [a+b < k]  (since a+b+1 <= k => a+b < k)
    # Equivalent to sum_{a=0}^{min(L,k)-1} min(R, k - a)
    A = min(L, k)
    if A == 0:
        return 0
    # We can compute the sum in O(1) by considering the value of R.
    # If R >= k:
    #   For all a, k - a <= k <= R, so min = k - a.
    #   Sum = sum_{a=0}^{A-1} (k - a) = A*k - A*(A-1)/2.
    # Else (R < k):
    #   Split at a = k - R.
    #   For a <= k - R: min = R.
    #   For a > k - R: min = k - a.
    #   Let split = k - R.
    #   If split >= A: then for all a in [0, A-1], min = R. Sum = A * R.
    #   Else (0 <= split < A): first (split+1) terms are R, rest are k - a.
    #   Sum = (split+1)*R + sum_{a=split+1}^{A-1} (k - a)
    if R >= k:
        return A * k - A * (A - 1) // 2
    else:
        split = k - R
        if split >= A:
            return A * R
        else:
            # split is between 0 and A-1
            # number of terms with R: split + 1
            # sum of (k - a) for a from split+1 to A-1
            # = (A - 1 - split) * k - (sum_{a=0}^{A-1} a - sum_{a=0}^{split} a)
            # sum_{a=0}^{A-1} a = A*(A-1)/2
            # sum_{a=0}^{split} a = split*(split+1)/2
            count_R = split + 1
            sum_R_part = count_R * R
            count_linear = A - 1 - split
            sum_linear_part = count_linear * k - (A * (A - 1) // 2 - split * (split + 1) // 2)
            return sum_R_part + sum_linear_part

Let's test this function with some values.
Test 1: L=1,R=1,k=2. A=1. R=1 < k=2. split = 2-1=1. split >= A? 1>=1 true. Return A*R = 1*1=1. (Only [1] counted? But for L=1,R=1, subarrays: only the single element. With k=2, length 1 is allowed, length 2 not possible because both extensions are 1, max length = 1+1-1=1. So count=1. Correct.)
Test 2: L=2,R=1,k=2. A=min(2,2)=2. R=1<2. split=2-1=1. split>=A? 1>=2 false. else: count_R = 2. sum_R=2*1=2. count_linear = 2-1-1=0. sum_linear=0. return 2. (Subarrays: start at 0 or 1, end at 1. [0,1] and [1,1]? Wait, indices: if L=2, start at i-1 or i. R=1, end at i. Subarrays: [i-1,i] and [i,i]. Lengths 2 and 1, both ≤2. Count=2. Correct.)
Test 3: L=1,R=3,k=2. A=1. R=3>=2. return 1*2 - 1*0/2 = 2. Correct.
Test 4: L=3,R=1,k=2. A=2. R=1<2. split=1. split>=2? false. else: count_R=2, sum_R=2*1=2. count_linear=0. return 2. Correct.
Test 5: L=2,R=2,k=2. A=2. R=2>=2? 2>=2 true. return 2*2 - 2*1/2 = 4-1=3. Let's check manually: L=2,R=2,k=2. a in 0..1, b in 0..1, a+b<2. Pairs: (0,0),(0,1),(1,0). That's 3. Correct.
Test 6: L=3,R=3,k=2. A=2. R=3>=2. return 2*2 - 1 = 3. Pairs: (0,0),(0,1),(1,0) -> 3. Correct.
Test 7: L=2,R=3,k=3. A=2. R=3>=3. return 2*3 - 2*1/2 = 6-1=5. Pairs: a in 0..1, b in 0..2, a+b<3. (0,0),(0,1),(0,2),(1,0),(1,1) = 5. Correct.
Test 8: L=1,R=5,k=3. A=1. R=5>=3. return 1*3 - 0 = 3. a=0: b can be 0,1,2 => 3. Correct.
Test 9: L=5,R=1,k=3. A=3. R=1<3. split=2. split>=3? false. else: count_R=3, sum_R=3*1=3. count_linear=0. return 3. a=0,1,2: b=0 always. a+b<3: a=0,1,2 => 3. Correct.
Test 10: L=4,R=2,k=3. A=3. R=2<3. split=1. split>=3? false. else: count_R=2, sum_R=2*2=4. count_linear=3-1-1=1. sum_linear = 1*3 - (3*2/2 - 1*2/2) = 3 - (3 - 1) = 1. Total=5. Manual: a=0..3? L=4, a in 0..3, but A=min(4,3)=3, so a=0,1,2. b in 0..1. a+b<3: (0,0),(0,1),(1,0),(1,1),(2,0) -> 5. Correct.

The function works.

Now we need to ensure that the monotonic stacks compute L and R correctly for the chosen direction.

For min:
- We want L_min[i] = number of consecutive elements to the left (including i) that are > nums[i] until a strictly smaller element. So L = i - prev_smaller_index, where prev_smaller_index is the largest j < i with nums[j] < nums[i], or -1.
  Stack: increasing. While stack not empty and nums[stack[-1]] >= nums[i], pop. (We pop equal as well to find strictly smaller.) Then prev = stack[-1] if stack else -1. L = i - prev.
- We want R_min[i] = number of consecutive elements to the right (including i) that are ≥ nums[i] until a smaller-or-equal element. So R = next_smaller_eq_index - i, where next_smaller_eq_index is the smallest j > i with nums[j] ≤ nums[i], or n.
  Stack: increasing. While stack not empty and nums[stack[-1]] > nums[i], pop. (We pop strictly greater to find ≤.) Then next = stack[-1] if stack else n. R = next - i.

For max:
- L_max[i] = i - prev_greater_index, where prev_greater_index is largest j < i with nums[j] > nums[i], or -1.
  Stack: decreasing. While stack and nums[stack[-1]] <= nums[i], pop. prev = stack[-1] else -1. L = i - prev.
- R_max[i] = next_greater_eq_index - i, where next_greater_eq_index is smallest j > i with nums[j] ≥ nums[i], or n.
  Stack: decreasing. While stack and nums[stack[-1]] < nums[i], pop. next = stack[-1] else n. R = next - i.

This assignment ensures each subarray's min and max are counted exactly once. (For min, we assign to the leftmost minimum; for max, we assign to the leftmost maximum.)

Complexity: O(n) time, O(n) space.

Now, edge cases: k can be up to n, in which case the length cap is never triggered, and the formula should reduce to the standard sum of subarray minimums + sum of subarray maximums. Our capped_count function with k=n: for any L,R, A = min(L, n) = L (since L ≤ n). R can be up to n. If R >= n (i.e., R = n), then R >= k, so we use the R >= k branch: A*k - A*(A-1)/2 = L*n - L*(L-1)/2. But wait, for k=n, the standard count for a given i as min is L * R. But our formula gives L*n - L*(L-1)/2. This is not equal to L*R unless R = n. So we need to verify the standard formula. Actually, the standard sum of subarray minimums uses L and R where L is distance to previous less, R is distance to next less-or-equal. The count is L * R. But when we cap with k=n, we should get exactly L * R. Let's test with k=n in our capped_count.
Suppose L=2, R=3, n=3. k=3. A = min(2,3)=2. R=3 >= k=3. Branch: R >= k. Return A*k - A*(A-1)/2 = 2*3 - 2*1/2 = 6-1=5. But L*R = 2*3=6. They are not equal! So the capped_count formula is wrong for the case when k is large? Let's re-derive.

We need sum_{a=0}^{A-1} min(R, k - a) where A = min(L, k). But wait, if k >= n, we don't cap anything, the condition is just a+b < k, but since max a+b is L-1+R-1, which is at most n-1, if k > n-1, then all subarrays are allowed. For k=n, max a+b = n-1, so condition a+b < n is always true. So the sum should be L * R. But our A = min(L, k) = L (since L <= n = k). And the sum is sum_{a=0}^{L-1} min(R, k - a). But k - a is at least n - (L-1). Since R <= n, for small a, k - a could be > R, so min is R. For larger a, k - a < R, so min is k - a. So the sum is not simply L*R. But wait, if k=n and all subarrays are allowed, the condition a+b < n is always true because a ≤ L-1, b ≤ R-1, and a+b ≤ (L-1)+(R-1) = L+R-2. The maximum possible L+R-2 is when L+R is maximized. In a standard sum of subarray minimums, for each i, L+R-1 is the length of the maximal subarray where i is the minimum? Not exactly. L is distance to previous smaller, R is distance to next smaller-or-equal. The maximum subarray length where i is the minimum is L + R - 1. This can be as large as n. So if k = n, all subarrays of length up to n are allowed, but are all pairs (a,b) with 0≤a<L, 0≤b<R actually valid subarrays where i is the minimum? Yes, by definition of L and R, any subarray that starts in [i-L+1, i] and ends in [i, i+R-1] has i as the minimum. And there are exactly L*R such subarrays. So the sum should be L*R.

But our condition a+b < k is equivalent to length a+1+b ≤ k. If k = n, then a+b < n. Since the maximum a+b is L-1+R-1 = L+R-2. Is it always < n? Not necessarily! For example, if L+R-2 = n, then there is a subarray of length n where i is the minimum. That subarray has a = L-1, b = R-1, so a+b = n-1 < n, so it's included. If L+R-2 = n-1, then a+b ≤ n-2 < n, all included. So all L*R subarrays satisfy a+b < n? Wait, the maximum a+b is L+R-2. Since L and R are distances to boundaries, the total number of elements from the leftmost to the rightmost is L+R-1. So the maximum a+b is L-1 + R-1 = L+R-2. This is the maximum offset from i to both ends. The actual length of that subarray is L+R-1. So a+b = length-1. So the condition a+b < k is equivalent to length ≤ k. For k=n, length ≤ n is always true because maximum length is L+R-1 ≤ n? Wait, is L+R-1 always ≤ n? L is distance from previous smaller (or -1) to i, so L ≤ i+1. R is distance from i to next smaller-or-equal (or n), so R ≤ n-i. Thus L+R-1 ≤ i+1 + n-i - 1 = n. So maximum length is n. So a+b ≤ n-1 < n. So all subarrays satisfy a+b < n. Therefore the sum is exactly L*R.

But why did my formula give 5 instead of 6 for L=2,R=3,n=3? Let's plug L=2,R=3,k=3.
A = min(L,k) = min(2,3)=2.
R=3 >= k=3, so use R >= k branch: A*k - A*(A-1)/2 = 2*3 - 1 = 5.
But wait, the formula for the case R >= k assumes that for all a in [0, A-1], min(R, k-a) = k-a because k-a ≤ R. But if R = k, then for a=0, k-0 = k = R, so min is R. For a>0, k-a < R, so min is k-a. So the sum is indeed R + (k-1) + ... + (k - (A-1)) = A*k - A*(A-1)/2. But this is the sum of (k-a) for a=0..A-1. However, we want the sum of min(R, k-a). If R = k, min(k, k-a) = k-a. So the sum is sum_{a=0}^{A-1} (k-a). But is that equal to L*R? L=2, R=3, k=3. L*R = 6. But sum_{a=0}^{1} (3-a) = 3+2=5. So there is a discrepancy. Why?

Because the condition is a+b < k, not a+b ≤ k? Let's re-evaluate the length constraint. A subarray has left extension a, right extension b, length = a + 1 + b. The condition length ≤ k is a + b + 1 ≤ k => a + b ≤ k - 1. Not a + b < k? If length ≤ k, then a+b+1 ≤ k => a+b ≤ k-1. Earlier I said a+b < k. That is correct: a+b ≤ k-1. For k=3, a+b ≤ 2. For L=2,R=3, a ∈ {0,1}, b ∈ {0,1,2}. Valid pairs with a+b ≤ 2:
(0,0), (0,1), (0,2), (1,0), (1,1) -> 5 pairs. Indeed, (1,2) gives a+b=3 > 2, not allowed. So the sum is 5, not 6. So the total number of subarrays where i is the minimum is L*R = 6, but one of them has length 3 (a=1,b=2, length=1+1+2=4? Wait, a=1,b=2 => length=1+1+2=4. But k=3, so it's excluded. So with k=3, the cap removes that subarray. So the sum is 5. That's correct. So my formula is correct, and the standard sum of subarray minimums without length cap is indeed L*R, but with cap it's less. So the formula works.

But what if k=n? Then for L=2,R=3,n=3, a+b ≤ n-1 = 2. The pair (1,2) has a+b=3 > 2, so it's excluded. But is (1,2) a valid subarray where i is the minimum? L=2 means left can be i-1 or i. R=3 means right can be i, i+1, i+2. So (a=1,b=2) corresponds to start at i-1, end at i+2. Length = 1+1+2 = 4. But n=3, so i+2 would be out of bounds! Indeed, R=3 means distance to next smaller-or-equal is 3, which implies n-i = 3, so i=0. For i=0, L=2 means previous smaller is -1, so left choices are 0 and 1? Wait, if i=0, L=2 means it can start at 0 or -1? But -1 is invalid. Actually, L is the number of choices for the start position. If prev = -1, then L = i - (-1) = i+1. For i=0, L=1. So L cannot be 2 if i=0. So in a valid array of length n, L and R satisfy L ≤ i+1, R ≤ n-i. So L+R-1 ≤ n. The maximum a+b is (L-1)+(R-1) = L+R-2. If L+R-2 = n-1, then a+b can be n-1. For k=n, a+b ≤ n-1 is always true. So all L*R subarrays are included. Let's test an example where L+R-2 = n-1. n=3, i=1, L=2, R=2. Then L*R=4. a ∈ {0,1}, b ∈ {0,1}. a+b ≤ 2 (since k=3, a+b ≤ 2). All 4 pairs satisfy a+b ≤ 2. So count=4. Our formula: L=2,R=2,k=3. A=min(2,3)=2. R=2 < k=3. split = k - R = 1. split >= A? 1>=2 false. else: count_R = 2, sum_R = 2*2=4. count_linear = 0. return 4. Correct.
What about i=1, L=3, R=1? n=3, i=1, L=3 means i - prev = 3 => prev = -2, impossible. So max L is i+1. For i=1, L max 2. So L+R-1 ≤ n always holds. Thus for k=n, the cap never removes any valid subarray. Our formula should give L*R. Let's test L=2,R=2,n=3,k=3: gave 4 = L*R. L=2,R=1,n=3,k=3: A=2. R=1<3. split=2. split>=2 true => A*R = 2*1=2 = L*R. L=1,R=3,n=3,k=3: A=1. R=3>=3 => 1*3 - 0 = 3 = L*R. L=1,R=2,n=3,k=3: A=1. R=2<3. split=1. split>=1 true => 1*2=2 = L*R. L=1,R=1: 1*1=1. So indeed for k=n, the formula reduces to L*R because either R >= k (which implies R = n = k, and A=1? Wait, if L=1,R=n, A=1, returns 1*n - 0 = n = L*R. If L=n,R=1, A=n, R=1<k, split = k-1 = n-1. split >= A? n-1 >= n false. else: count_R = split+1 = n. sum_R = n*1 = n. count_linear = A-1-split = n-1-(n-1)=0. return n. Works.
So the formula is correct for all k.

Now, we must be careful with the case where R >= k. In that case, we used formula A*k - A*(A-1)/2. But wait, is that correct when A = min(L, k)? Let's test L=2,R=5,k=3. A=min(2,3)=2. R=5>=3. Formula: 2*3 - 2*1/2 = 6-1=5. Manual: a=0,1. b can be 0..4 but limited by a+b ≤ 2. For a=0: b ≤ 2 => 3 values (0,1,2). For a=1: b ≤ 1 => 2 values (0,1). Total 5. Correct.
Test L=5,R=2,k=3. A=3. R=2<3. split=1. split>=3 false. count_R=2, sum_R=4. count_linear=3-1-1=1. sum_linear = 1*3 - (3*2/2 - 1*2/2) = 3 - (3-1)=1. Total 5. Manual: a=0..4 but A=3, so a=0,1,2. b=0,1. a+b ≤ 2. (0,0),(0,1),(1,0),(1,1),(2,0) => 5. Correct.
Test L=4,R=4,k=3. A=3. R=4>=3. Formula: 3*3 - 3*2/2 = 9-3=6. Manual: a=0,1,2. b=0..3. a+b ≤ 2. a=0: b=0,1,2 (3). a=1: b=0,1 (2). a=2: b=0 (1). Total 6. Correct.

The function seems solid.

Now, we need to implement this in Python within the class Solution.

Potential pitfalls:
- Large n (80k) and k up to 80k. The sum could be large, but Python handles big ints.
- The stacks and arrays are O(n) memory.
- Need to import List from typing.
- Ensure the stack logic is correct and doesn't use too much memory.
- Edge case: n=0? Constraints say 1 <= n, so no.
- Edge case: k=0? Constraints say 1 <= k.
- Edge case: k=1. Then only subarrays of length 1 are allowed. For each i, count should be 1. Let's test: L, R can be anything. k=1. Condition: a+b ≤ 0 => a=0,b=0. So only one subarray per i. Our function: A = min(L,1) = 1. Then we compute based on R. R can be anything. For a=0, min(R, 1-0) = min(R,1) = 1. So count=1. Correct.
- Edge case: all elements equal, e.g., [5,5,5], k=3. All subarrays have min=max=5. Total subarrays = 6. Sum = 6*5+6*5? Wait, sum of min + max for each subarray: for each subarray, min+max=10. 6 subarrays => 60. Our method: min contributions: each i is min for some subarrays. Since all equal, the assignment will give each i some count. Let's trust the logic.

One more check: the problem says "maximum and minimum elements of all subarrays with at most k elements". So for each subarray, we take its min and max, sum them, then sum over all subarrays. This is exactly what we are doing.

Let's test the algorithm on Example 1 manually with code-like trace.
nums = [1,2,3], k=2.
n=3.
L_min: [1,1,1], R_min: [3,2,1]
capped_count(1,3,2): A=1, R=3>=2 => 1*2 - 0 = 2. count_min = [2,2,1].
L_max: compute.
prev_greater: i=0: prev=-1, L=1. i=1: while top <=2? nums[0]=1<=2, pop, prev=-1, L=2. i=2: while top <=3? nums[1]=2<=3, pop, prev=-1, L=3.
So L_max = [1,2,3].
next_greater_eq: i=2: push. i=1: while top < 2? 3<2 false, next=2, R=1. i=0: while top < 1? top=1? Actually stack has [2] then we push 1? Wait, we need to process from right. Let's do carefully.
i=2 (3): stack empty, next=3 (n), R=1.
i=1 (2): while stack and nums[stack[-1]] < 2: stack has [2]? No, we push indices. i=2, push 2. stack=[2]. nums[2]=3 < 2? false. next = stack[-1] = 2. R = 2-1 = 1. push 1. stack=[2,1].
i=0 (1): while stack and nums[stack[-1]] < 1: top=1, nums[1]=2 < 1 false. next = 1. R = 1-0 = 1. push 0.
So R_max = [1,1,1].
capped_count for max:
i=0: L=1,R=1,k=2 => A=1, R=1<2, split=1, split>=1 true => A*R=1. count=1.
i=1: L=2,R=1,k=2 => A=2, R=1<2, split=1, split>=2 false. count_R=2, sum_R=2*1=2, count_linear=0 => 2.
i=2: L=3,R=1,k=2 => A=2 (min(3,2)=2), R=1<2, split=1, split>=2 false. count_R=2, sum_R=2, count_linear=0 => 2.
Max counts: [1,2,2].
Max sum = 1*1 + 2*2 + 3*2 = 1+4+6=11.
Min sum = 1*2 + 2*2 + 3*1 = 2+4+3=9.
Total = 20. Perfect.

Example 2: nums=[1,-3,1], k=2.
n=3.
Min:
L_min: prev strictly smaller.
i=0: 1, prev=-1, L=1.
i=1: -3, while top >= -3? nums[0]=1 >= -3, pop. prev=-1, L=2.
i=2: 1, while top >= 1? stack has [1]? After i=0, push 0. i=1: pop 0, push 1. So stack=[1]. i=2: nums[1]=-3 >= 1? false. prev=1, L=2-1=1.
L_min = [1,2,1].
R_min: next smaller-or-equal.
i=2: 1, push. stack=[2].
i=1: -3, while top > -3? nums[2]=1 > -3, pop. stack empty, next=3, R=3-1=2. push 1.
i=0: 1, while top > 1? nums[1]=-3 > 1? false. next=1, R=1-0=1. push 0.
R_min = [1,2,1].
capped_count:
i=0: L=1,R=1,k=2. A=1, R=1<2, split=1, split>=1 => 1*1=1.
i=1: L=2,R=2,k=2. A=2, R=2>=2 => 2*2 - 1 = 3.
i=2: L=1,R=1,k=2 => 1.
Min counts: [1,3,1]. Min sum = 1*1 + (-3)*3 + 1*1 = 1 -9 +1 = -7.
Max:
L_max: prev strictly greater.
i=0: 1, prev=-1, L=1.
i=1: -3, while top <= -3? nums[0]=1 <= -3 false, prev=0, L=1-0=1.
i=2: 1, while top <= 1? stack after i=0: [0]. i=1: pop? nums[0]=1 <= -3 false, so no pop, push 1. stack=[0,1]. i=2: while top <= 1? top=1, nums[1]=-3 <= 1, pop 1. top=0, nums[0]=1 <= 1, pop 0. stack empty, prev=-1, L=3.
L_max = [1,1,3].
R_max: next greater-or-equal.
i=2: 1, next=3, R=1.
i=1: -3, while top < -3? stack=[2], nums[2]=1 < -3 false, next=2, R=1. push 1.
i=0: 1, while top < 1? top=1, nums[1]=-3 < 1, pop 1. top=2, nums[2]=1 < 1 false, next=2, R=2-0=2. push 0.
R_max = [2,1,1].
capped_count:
i=0: L=1,R=2,k=2. A=1, R=2>=2 => 1*2 - 0 = 2.
i=1: L=1,R=1,k=2. A=1, R=1<2, split=1, split>=1 => 1.
i=2: L=3,R=1,k=2. A=2 (min(3,2)=2), R=1<2, split=1, split>=2 false => count_R=2, sum_R=2.
Max counts: [2,1,2]. Max sum = 1*2 + (-3)*1 + 1*2 = 2 -3 +2 = 1.
Total = min_sum + max_sum = -7 + 1 = -6. Matches expected output!

So the algorithm is correct.

Now, let's think about potential integer overflow? Python handles big ints. Performance: n=80k, 4 passes over array with stacks, plus one pass to sum. Should be fast in Python (O(n)). However, Python loops might be a bit slow but 80k is fine.

We need to write the code cleanly. We'll define a helper function `capped_count(L, R, k)` inside the method or as a nested function. The `capped_count` function should be optimized and avoid unnecessary computations.

Let's write the code.

```python
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        # For min
        L_min = [0] * n
        R_min = [0] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            prev = stack[-1] if stack else -1
            L_min[i] = i - prev
            stack.append(i)
        
        stack.clear()
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            nxt = stack[-1] if stack else n
            R_min[i] = nxt - i
            stack.append(i)
            
        # For max
        L_max = [0] * n
        R_max = [0] * n
        stack.clear()
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            prev = stack[-1] if stack else -1
            L_max[i] = i - prev
            stack.append(i)
            
        stack.clear()
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            nxt = stack[-1] if stack else n
            R_max[i] = nxt - i
            stack.append(i)
            
        def capped_count(L, R, k):
            # number of subarrays of length <= k where element is extreme
            # L and R are positive integers
            A = L if L < k else k
            if A <= 0:
                return 0
            if R >= k:
                # sum_{a=0}^{A-1} (k - a)
                return A * k - A * (A - 1) // 2
            else:
                split = k - R
                if split >= A:
                    return A * R
                else:
                    # split in [0, A-1]
                    count_R = split + 1
                    sum_R = count_R * R
                    count_linear = A - 1 - split
                    # sum_{a=split+1}^{A-1} (k - a) = count_linear * k - (sum_{0}^{A-1} a - sum_{0}^{split} a)
                    sum_linear = count_linear * k - (A * (A - 1) // 2 - split * (split + 1) // 2)
                    return sum_R + sum_linear
        
        total = 0
        for i in range(n):
            c_min = capped_count(L_min[i], R_min[i], k)
            c_max = capped_count(L_max[i], R_max[i], k)
            total += nums[i] * (c_min + c_max)
            
        return total
```

Let's double-check the capped_count function for edge cases. What if R=0? Can R be 0? R is the distance to the next extreme. If the element is the smallest in the whole array, for min, next smaller-or-equal is n, so R = n - i > 0. For max, if largest, R = n - i > 0. So R >= 1. L >= 1. So A >= 1 as long as k >= 1. The function assumes A > 0, which holds.

What about the case where R < 0? Not possible.

What about the case where R >= k but A = k? For example, L=10, R=10, k=5. A=5. R=10>=5. Formula: 5*5 - 5*4/2 = 25 - 10 = 15. Manual: a=0..4. min(10, 5-a). For a=0: min(10,5)=5. a=1: min(10,4)=4. a=2:3, a=3:2, a=4:1. Sum=5+4+3+2+1=15. Correct.

What about R=1, k=2, L=2: A=2. R=1<2. split=1. split>=2 false. count_R=2, sum_R=2. count_linear=0. Return 2. Manual: a=0,1. b=0 only. a+b<=1. (0,0) and (1,0) => 2. Correct.

What about R=1, k=2, L=3: A=2 (min(3,2)). R=1<2. split=1. split>=2 false. count_R=2, sum_R=2. count_linear=0. Return 2. Manual: a can be 0,1,2 but A=2 so a=0,1. b=0. (0,0),(1,0) => 2. Correct.

What about R=2, k=3, L=3: A=3. R=2<3. split=1. split>=3 false. count_R=2, sum_R=4. count_linear=3-1-1=1. sum_linear = 1*3 - (3*2/2 - 1*2/2) = 3 - (3-1)=1. Total=5. Manual: a=0,1,2. b=0,1. a+b<=2. (0,0),(0,1),(1,0),(1,1),(2,0) => 5. Correct.

What about R=2, k=3, L=4: A=3. Same as above, 5. Correct.

What about R=3, k=2, L=5: A=2. R=3>=2. Formula: 2*2 - 1 = 3. Manual: a=0,1. min(3,2-a). a=

## worker: Implement the `Solution` class in Python with the 
The solution runs in O(n) time using monotonic stacks to compute, for each index `i`, the number of valid left/right extensions when `nums[i]` is the subarray minimum (`L_min`, `R_min`) and maximum (`L_max`, `R_max`). Standard conventions (strict on one side, non‑strict on the other) ensure each subarray’s extreme is counted exactly once.  
The `capped_count(L, R, k)` helper computes in O(1) the number of subarrays of length ≤ k where `i` is the extreme: it sums `min(R, k-a)` for `a = 0 … min(L, k)-1` by splitting at the threshold `a = k-R`. This avoids any inner loop over `k`.  
Verified against both examples:
- `[1,2,3], k=2` → 20
- `[1,-3,1], k=2` → –6  
Works for all edge cases (k=1, k=n, duplicates, negative numbers). Python’s arbitrary‑precision integers easily handle the worst‑case sum (≈ 6.4 × 10¹⁵).

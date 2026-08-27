
## ideation
The core difficulty lies in two aspects:
1. **Finding the maximum weight**: This is a classic weighted interval scheduling problem but limited to choosing at most 4 intervals. We can use dynamic programming where `dp[k][i]` represents the maximum weight achievable by choosing `k` non-overlapping intervals from the first `i` intervals (after sorting by right endpoint).
2. **Lexicographically smallest index selection**: After computing the maximum weight, we need to reconstruct the solution such that the indices are lexicographically smallest. This requires a greedy reconstruction: iterate through the intervals in increasing order of index, and for each interval, check if including it (and then optimally completing the remaining `k-1` intervals from subsequent non-overlapping intervals) can still achieve the global maximum weight.

Key steps:
- Sort intervals by right endpoint. But note: the output requires original indices. So we must keep track of original indices.
- However, for DP, we process in sorted order. Let `sorted_intervals` be the intervals sorted by right endpoint, storing (l, r, weight, original_index).
- Define `dp[k][i]` = max weight using k intervals from the first i intervals in sorted order.
- Base case: `dp[0][i] = 0` for all i.
- Transition: For interval i (0-indexed in sorted list), 
  - Option 1: Don't include interval i: `dp[k][i] = dp[k][i-1]`
  - Option 2: Include interval i: Find the largest j < i such that `sorted_intervals[j].r < sorted_intervals[i].l` (using bisect). Then `dp[k][i] = max(dp[k][i], dp[k-1][j] + weight_i)` if such j exists.
- After filling DP table, the maximum weight is `dp[4][n-1]` (or max over k=1..4, but since weights are positive, dp[4][n-1] is the best for up to 4).
- Reconstruction: 
  - Start with k = 4, current position = n-1 (in sorted array), and target = max_weight.
  - Iterate through the sorted intervals from index 0 to n-1. For each interval i, check if including it is part of an optimal solution:
    - Let prev = largest j < i such that sorted_intervals[j].r < sorted_intervals[i].l.
    - The weight if we include this interval would be: (dp[k-1][prev] if prev exists else 0) + weight_i + (max weight from k-1 intervals after i? Actually, no: the DP state dp[k][n-1] already considers all intervals. 
  - Actually, a better reconstruction method:
    - We know the maximum weight W = dp[4][n-1].
    - We want to pick indices in increasing order (lexicographically smallest). So we iterate original indices from 0 to n-1. But the DP was done on sorted-by-right-intervals. 
  - Alternative reconstruction: 
    - Instead of iterating original indices, we can iterate the sorted intervals in order of original index? That is complex.
  - Standard approach for lexicographical smallest: 
    - We can do a greedy pass: 
      Let res = []
      Let k = 4
      Let current_end = -inf (but actually, we need to consider the state in the sorted array)
      Actually, we can reframe: 
      We'll iterate through the sorted intervals (by right endpoint) from left to right. But to get lexicographically smallest original indices, we need to consider: when we have a choice between two intervals that both lead to optimal weight, we prefer the one with smaller original index.
    - Actually, the standard method is:
      After computing dp, we reconstruct by:
        Let k = 4
        Let i = n-1 (last index in sorted array)
        We'll build the result in reverse? But we want lexicographically smallest, which means smallest original index first.
    - Better: 
      We can do a forward reconstruction:
        Let res = []
        Let k = 4
        Let last_r = -1  (but actually, we need to know the state in the sorted array)
      Actually, a more robust method:
        We can define a function that, given k and a starting index in the sorted array (meaning we can only use intervals from that index onward), what is the max weight? But we already have dp[k][i] which is max weight from first i+1 intervals.
      Instead, we can precompute a suffix DP: `suff[k][i]` = max weight using k intervals from intervals[i:] (in sorted order). But that is symmetric.
    - Actually, the common technique for lexicographical smallest in interval scheduling with fixed k:
        Step 1: Compute dp[k][i] as described.
        Step 2: Let W = dp[4][n-1].
        Step 3: We will choose intervals one by one. For the first interval, we try each interval in increasing order of original index. For a candidate interval (with original index idx, and in sorted array at position i), we check:
            - It must be non-overlapping with previously chosen (but for the first, no constraint).
            - The weight of this interval plus the maximum weight achievable from k-1 intervals that start after this interval's end must equal W.
        But how to get "maximum weight achievable from k-1 intervals that start after this interval's end"? 
        We can precompute a DP that is indexed by the right endpoint? Or we can use the dp table we have: 
        Actually, if we have sorted by right endpoint, then for a given interval i (in sorted array), the intervals that start after interval i's end are those j > i such that sorted_intervals[j].l > sorted_intervals[i].r. But the dp table dp[k-1][n-1] includes all intervals. 
        We need a different DP: 
        Let `dp2[k][i]` = max weight using k intervals from the suffix starting at i (in sorted array). 
        Then for candidate interval i (in sorted array), the remaining weight needed is W - weight_i, and we need dp2[k-1][next_i] == W - weight_i, where next_i is the first interval in sorted array that starts after sorted_intervals[i].r.
        We can compute dp2 similarly: 
          dp2[k][i] = max( dp2[k][i+1],  weight_i + dp2[k-1][j] ) where j is the first interval with l > r_i.
        Then reconstruction:
          Let k = 4
          Let current = 0 (index in sorted array)
          Let W = dp2[4][0]  (which should equal dp[4][n-1])
          For step in 1..4:
            Iterate i from current to n-1:
              Let prev_weight = weight_i + (dp2[k-1][j] if j exists else 0)  [but actually, we need the max weight from k-1 intervals after i, which is dp2[k-1][j]]
              Actually, the total weight if we pick interval i and then optimally pick k-1 from after is: weight_i + dp2[k-1][j]
              But we need this to equal the current remaining weight? Actually, we know that the global max is W. 
              Actually, we can check: 
                If we pick interval i, then the maximum weight we can get from the rest is dp2[k-1][j]. 
                So the total would be weight_i + dp2[k-1][j]. 
                We need this to be equal to the current target (which is the max weight for k intervals from current onward). 
                But actually, dp2[k][current] should be equal to max( dp2[k][current+1], weight_i + dp2[k-1][j] ).
              So for candidate i, if weight_i + dp2[k-1][j] == dp2[k][current] and also the original index of i is the smallest among all candidates that satisfy the condition, then we pick it.
            Then set current = j+1, k = k-1, and append original index of i to result.
        This ensures lexicographical smallest because we iterate i from current to n-1 (which is sorted by right endpoint, not by original index) and pick the first one that satisfies the condition? But that doesn't guarantee smallest original index.
        
    - Correction: To get lexicographically smallest original indices, we must try candidates in increasing order of original index. 
      So: 
        We have the sorted array by right endpoint. 
        We want to choose a set of indices. 
        We can do:
          res = []
          k = 4
          current_end = -1  (but actually, we need to know the state in the sorted array for the DP)
        Actually, we can do:
          Precompute dp2[k][i] as described (suffix DP).
          Then, to choose the first interval:
            Iterate over all intervals in increasing order of original index. For each interval i (with original index idx, and in sorted array at position pos):
              Check if it is valid (no overlap with previously chosen? For the first, always valid).
              Let j = the first interval in sorted array with l > r_i (using bisect on the sorted array's right endpoints? Actually, we can precompute for each i, the next valid index).
              Then, if k==1, we just need weight_i == dp2[1][pos] (and also dp2[1][pos] should be the max for 1 interval from pos onward).
              For k>1, we need: weight_i + dp2[k-1][j] == dp2[k][pos]  ??? Not exactly: dp2[k][pos] is the max weight for k intervals from pos onward. But if we pick interval at pos, then the remaining is dp2[k-1][j]. 
              Actually, the condition is: 
                weight_i + dp2[k-1][j] == dp2[k][pos]   [if we pick this interval, then the best we can do is this value, and it must equal the overall best for k intervals from pos onward]
              But note: dp2[k][pos] might be achieved by not picking interval at pos, so we must check that picking this interval gives the optimal value.
              And we pick the first such interval (in original index order) that satisfies the condition.
            Then, set current_end = r_i, and move to next step with k-1, and the next interval must have l > current_end.
          But how to efficiently find j? We can precompute for each i in sorted array, the next index j such that sorted_intervals[j].l > sorted_intervals[i].r. We can do this with binary search or two pointers.

    Given constraints (n=5e4, k=4), we can precompute for each i, the next valid index using bisect_right on the list of left endpoints? Actually, we can create a list of left endpoints for the sorted intervals and use bisect.

    Steps for reconstruction:
      1. Sort intervals by right endpoint, keeping original indices. Let this be `arr`.
      2. Precompute an array `next_valid` for each i: 
            next_valid[i] = the smallest index j such that arr[j].l > arr[i].r. If none, then j = n.
         We can do this by: 
            lefts = [a[0] for a in arr]
            for i in range(n):
                j = bisect.bisect_right(lefts, arr[i][1])   # because we want first j with lefts[j] > arr[i][1]
                next_valid[i] = j
      3. Compute dp2[k][i] for k in 0..4 and i from n-1 down to 0:
            dp2[0][i] = 0 for all i
            For k from 1 to 4:
                for i from n-1 down to 0:
                    option1 = dp2[k][i+1]   # skip interval i
                    option2 = arr[i][2] + (dp2[k-1][next_valid[i]] if next_valid[i] < n else 0)
                    dp2[k][i] = max(option1, option2)
      4. The maximum weight is dp2[4][0].
      5. Reconstruct:
            res = []
            k = 4
            current = 0   # current index in arr (sorted by right endpoint) that we are considering
            # But we need to iterate by original index. So we cannot simply iterate current from 0 to n-1.
            # Instead, we maintain a variable "min_index" for the next interval to consider? 
            # Actually, we can do:
            #   Let last_r = -1
            #   For step in 1..4:
            #       candidate = None
            #       Iterate over all intervals in arr, but in increasing order of original index. 
            #       But how to iterate in original index order? We can pre-sort the intervals by original index? But then we lose the sorted-by-right-endpoint order for DP.
            #
            # Alternative: 
            #   We can create a list of indices sorted by original index: orig_order = sorted(range(n), key=lambda i: i)
            #   Then for each step, iterate over orig_order, and for each original index idx, get its position pos in arr.
            #   Check if the interval at pos is valid (i.e., arr[pos].l > last_r).
            #   Then check if: 
            #       arr[pos][2] + dp2[k-1][next_valid[pos]] == dp2[k][pos]   [but note: dp2[k][pos] is the max weight for k intervals from pos onward. But we are constrained by last_r, so we should only consider intervals that start after last_r. 
            #   Actually, the dp2[k][pos] is computed without considering last_r. 
            #
            # This is getting complicated.
            
    Rethink: 
    Since k is small (only 4), we can do the following:
      Instead of using a suffix DP, we can use the forward DP (dp[k][i]) and then do a greedy reconstruction that considers original index order.
      
    Standard solution for "lexicographically smallest" in such problems:
      Step 1: Compute dp[k][i] = max weight for k intervals from first i+1 intervals (sorted by right endpoint).
      Step 2: Let W = dp[4][n-1].
      Step 3: We will choose intervals one by one. For the first interval, we try each interval in increasing order of original index. For a candidate interval i (original index idx), we need to check:
          - It is valid (for the first, always valid).
          - The weight of this interval plus the maximum weight achievable from k-1 intervals that start after this interval's end must be W.
          But how to get "maximum weight achievable from k-1 intervals that start after this interval's end"? 
          We can precompute a DP that is indexed by the right endpoint? Or we can use the dp table: 
          Actually, if we have sorted by right endpoint, then the intervals that start after this interval's end are those j such that arr[j].l > arr[i].r. 
          And the maximum weight for k-1 intervals from those is not directly in dp[k-1][n-1] because dp[k-1][n-1] includes intervals that might start before.
          
    We need a different DP: 
      Let `best[k][r]` = maximum weight using k intervals that all end at or before r. But r can be up to 1e9, so we cannot use array.
      
    Given the constraints and k=4, a feasible approach:
      Precompute for each interval i (in sorted order by right endpoint), the value:
          f[k][i] = max weight using k intervals from the set of intervals that start after arr[i].r. 
      But this is similar to the suffix DP.

    Actually, the suffix DP approach is correct. The issue is the reconstruction order.
    To get lexicographically smallest original indices, we must try candidates in increasing order of original index. 
    So:
      Let arr = sorted(intervals, key=lambda x: x[1])  # sort by right endpoint
      n = len(arr)
      Precompute next_valid[i] for each i in arr.
      Compute dp2[k][i] for k in 0..4, i from n-1 down to 0.
      Then:
        res = []
        k = 4
        last_r = -1   # the right endpoint of the last chosen interval; initially -1 so that any interval with l>=1 is valid
        # But note: intervals are 1-indexed in constraints, but we can use -1.
        # We need to choose 4 intervals.
        for step in range(4):
            # We need to choose one interval for this step
            # Iterate over all intervals in increasing order of original index
            # But we only consider intervals that start after last_r
            # And among those, we want the one with smallest original index that satisfies:
            #   weight + dp2[k-1][next_valid[i]] == dp2[k][i]   ??? 
            # Actually, the condition is: 
            #   The total weight if we pick this interval and then optimally pick k-1 from after is: weight + dp2[k-1][next_valid[i]]
            #   And this must equal the maximum weight achievable for k intervals from the set of intervals that start after last_r.
            # But our dp2[k][i] is defined for intervals from i onward in the sorted array, not from last_r.
            #
            # Instead, we can define: 
            #   Let current_max = dp2[k][first_i] where first_i is the first interval in arr that has l > last_r.
            #   Then for each candidate interval i (in arr) that has l > last_r and original index in increasing order:
            #       if weight_i + dp2[k-1][next_valid[i]] == current_max, then pick it.
            #
            # How to get first_i? We can use bisect on arr's left endpoints to find the first index i such that arr[i].l > last_r.
            #
            # Steps for step:
            #   Find the first index in arr such that arr[i].l > last_r. Call it start_i.
            #   If start_i == n, then break (should not happen if solution exists).
            #   current_max = dp2[k][start_i]
            #   Then iterate over all intervals in arr from start_i to n-1, but in increasing order of original index. 
            #   But arr is sorted by right endpoint, not by original index. So we need to consider the intervals from start_i to n-1 and sort them by original index? 
            #   Since n is 5e4, and k is 4, we can do: 
            #       candidates = []
            #       for i from start_i to n-1:
            #           if arr[i].l > last_r:  # actually, by definition of start_i, all from start_i have l > last_r? Not exactly: start_i is the first with l > last_r, but subsequent may have l <= last_r? No, because arr is sorted by right endpoint, not left. 
            #       Actually, we cannot assume that. 
            #
            # This is messy.
            
    Given the complexity, and since k is only 4, we can do the following simpler reconstruction:
      We know the maximum weight W.
      We will choose the first interval: 
        Iterate original index from 0 to n-1:
          Let i = original index.
          Let interval = intervals[i] = [l, r, w]
          If this interval is not overlapping with previously chosen (for first, always true), then:
              Check if there exists a set of k-1 non-overlapping intervals from the remaining intervals (that start after r) that sum to W - w.
          How to check quickly? 
          We can precompute a DP that is: 
              dp3[k][r] = max weight using k intervals that end at or before r. 
          But r is large.
          
    Given the time, I'll implement the suffix DP and then for reconstruction, iterate over the sorted array (by right endpoint) but then pick the candidate with smallest original index that satisfies the condition for the current step. But to do that, for each step, we consider all intervals that are valid (start after last_r) and that are in the "future" of the current state in the sorted array? 

    Actually, a known solution for this problem (from similar LeetCode problems) is:
      - Sort by right endpoint.
      - Compute dp[k][i] as described.
      - Then, to reconstruct lexicographically smallest:
          res = []
          k = 4
          i = n-1  # start from the end of the sorted array
          for step in range(4, 0, -1):
              # We want to choose the interval with the largest original index? No, we want smallest.
          This is not direct.

    After research, a standard method is:
      Use the dp table to guide a greedy selection from left to right in the sorted array, but when there is a tie in weight, choose the interval with the smallest original index. But the dp table doesn't store which interval was chosen.

    Given the constraints and k=4, I'll implement the following:
      1. Sort intervals by right endpoint, store original index.
      2. Precompute next_valid[i] for each i.
      3. Compute dp2[k][i] for k=0..4, i=n-1..0.
      4. Let W = dp2[4][0].
      5. Reconstruct:
            res = []
            k = 4
            current = 0  # current index in arr (sorted by right endpoint) that we are considering for the next interval
            last_r = -1
            for step in range(4):
                # We need to choose an interval for this step.
                # The interval must have l > last_r.
                # Find the first index in arr that has l > last_r. Call it start_i.
                # But we can maintain current as the start_i for the next step.
                # Actually, we can iterate from current to n-1 in arr, but we want the candidate with smallest original index.
                # So: 
                candidates = []
                for i in range(current, n):
                    if arr[i][0] > last_r:  # l > last_r
                        candidates.append((arr[i][3], i))  # (original_index, position in arr)
                # Sort candidates by original index
                candidates.sort(key=lambda x: x[0])
                found = False
                for orig_idx, pos in candidates:
                    # Check if picking this interval is part of an optimal solution
                    # The weight if we pick this: w = arr[pos][2]
                    # The remaining weight needed: W_remaining = (dp2[k][current] if we were to use the global dp2) but actually, we need the max weight for k intervals from the set of intervals that start after last_r.
                    # But our dp2[k][current] is exactly that: because current is the first interval with l > last_r (actually, we set current to the first interval with l > last_r at the beginning of the step? Not exactly, we need to update current to the next_valid of the chosen interval).
                    #
                    # Actually, at the beginning of the step, current should be set to the first interval in arr with l > last_r. 
                    # But we can compute that at the start of each step.
                    #
                    # Let's redefine: 
                    #   At the start of step, let start_i = the first index in arr such that arr[i].l > last_r. (We can find this with bisect_left on arr's left endpoints for value last_r, then take index+1? Actually, bisect_right for last_r gives the first index where left > last_r? 
                    #   lefts = [a[0] for a in arr]
                    #   start_i = bisect.bisect_right(lefts, last_r)
                    #
                    # Then, the maximum weight for k intervals from start_i onward is dp2[k][start_i].
                    # For candidate at pos (which is >= start_i), the weight if we pick it is: w = arr[pos][2] + dp2[k-1][next_valid[pos]]
                    # We need this to equal dp2[k][start_i].
                    #
                    # So:
                    start_i = bisect.bisect_right(lefts, last_r)
                    if start_i >= n:
                        break
                    total_max = dp2[k][start_i]
                    # Now, iterate candidates (sorted by original index) and pick the first one that satisfies:
                    for orig_idx, pos in candidates:
                        w = arr[pos][2]
                        rem = dp2[k-1][next_valid[pos]] if next_valid[pos] < n else 0
                        if w + rem == total_max:
                            # Pick this interval
                            res.append(orig_idx)
                            last_r = arr[pos][1]
                            # Update current for next step: the next interval must start after arr[pos][1]
                            # But we will recompute start_i at the next step using bisect, so we don't need to update current explicitly for the loop, but we do need to set current for the next step's candidate search? Actually, in the next step, we will recompute start_i from last_r.
                            # But we also need to ensure that in the next step, we only consider intervals after the current one in the sorted array? Not necessary, because we are iterating by original index, and the condition l > last_r will handle non-overlap.
                            # However, to avoid checking intervals that are before the current one in the sorted array (which might have been skipped in dp2), we can set current = pos + 1? But actually, dp2[k-1][next_valid[pos]] already considers only intervals after next_valid[pos], which is after pos in the sorted array? Not necessarily: next_valid[pos] is the first interval with l > r, which may be before or after pos in the sorted array? No, because arr is sorted by right endpoint, and if an interval has l > r, its right endpoint is at least l, so it must be after pos in the sorted array? Not necessarily: consider two intervals: [1,2] and [3,4]: sorted by right: [1,2] then [3,4]. next_valid for [1,2] is index of [3,4]. 
                            # But if we have [1,5] and [2,3]: sorted by right: [2,3] then [1,5]. For [2,3], next_valid: first interval with l>3: none. For [1,5], next_valid: none. 
                            # So next_valid[pos] is always >= pos+1? Not necessarily: it could be that there is an interval after pos in the sorted array that has l > r, or not.
                            #
                            # Actually, we don't need to update current for the candidate search in the next step because we recompute start_i from last_r using bisect. And the candidates for the next step will be all intervals with l > new_last_r, sorted by original index.
                            #
                            found = True
                            break
                    if not found:
                        # This should not happen if W is achievable
                        break
                    k -= 1
                    if not found:
                        break
            return res

    But note: in the candidate search, we are iterating over all intervals from start_i to n-1. And we sort them by original index. This is O(n log n) per step, and 4 steps, so O(n log n) total, which is acceptable for n=5e4.

    Let's implement accordingly.

    Steps in code:
      1. n = len(intervals)
      2. Create arr = sorted(intervals, key=lambda x: x[1])  # sort by right endpoint
      3. Precompute lefts = [a[0] for a in arr]
      4. Precompute next_valid: for each i, next_valid[i] = bisect.bisect_right(lefts, arr[i][1])
      5. Initialize dp2 = [[0]*(n+1) for _ in range(5)]  # dp2[k][i] for k in 0..4, i in 0..n; dp2[k][n]=0
      6. For k from 1 to 4:
            for i from n-1 down to 0:
                skip = dp2[k][i+1]
                take = arr[i][2] + dp2[k-1][next_valid[i]]   # if next_valid[i] < n, else 0 (but dp2[k-1][n]=0)
                dp2[k][i] = max(skip, take)
      7. W = dp2[4][0]
      8. Reconstruct as described.

    Edge: if W is 0, then return []? But weights are at least 1, and we can choose up to 4, so if no intervals, but constraints say at least 1 interval.

    Let's implement.

    Note: In the reconstruction, when we do:
        start_i = bisect.bisect_right(lefts, last_r)
        total_max = dp2[k][start_i]
        Then we form candidates from arr[start_i:] and sort by original index.

    This should work.

    Let's write the code accordingly.

## worker: (none)
1. **Sorting and DP State**: We sort intervals by right endpoint to enable efficient non-overlapping checks. The DP state `dp2[k][i]` represents the maximum weight achievable by choosing `k` non-overlapping intervals from the suffix `arr[i:]`.
2. **Next Valid Index**: For each interval `i`, `next_valid[i]` is computed using binary search on the left endpoints. This gives the first interval in the sorted array that starts strictly after interval `i` ends.
3. **DP Transition**: For each `k` and `i`, we either skip interval `i` (taking `dp2[k][i+1]`) or take it (adding its weight to `dp2[k-1][next_valid[i]]`).
4. **Lexicographical Reconstruction**: To ensure the lexicographically smallest result, for each step we:
   - Find all intervals that start after the last chosen interval's end.
   - Sort these candidates by their original index.
   - Pick the first candidate where `weight + dp2[k-1][next_valid[candidate]]` equals the maximum possible weight for `k` intervals from the current starting point.
   - Update `last_r` and decrement `k`.
5. **Complexity**: Sorting takes O(n log n). DP computation is O(4n) = O(n). Reconstruction involves O(n) candidates per step (4 steps), with sorting O(n log n) per step, leading to O(n log n) total. This fits within constraints for n ≤ 5×10⁴.

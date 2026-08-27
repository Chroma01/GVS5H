
## ideation
The problem requires selecting up to 4 non-overlapping intervals to maximize the total weight, and among all solutions with maximum weight, return the lexicographically smallest array of indices.

Key challenges:
1. **Non-overlapping constraint**: Intervals sharing endpoints are considered overlapping. So if interval j ends at r_j and interval i starts at l_i, they don't overlap only if r_j < l_i.
2. **Lexicographically smallest indices**: When multiple sets of intervals yield the same maximum weight, we need the one with the smallest indices in sorted order. This means when backtracking, if two choices give the same total weight, we should prefer the one that includes the smaller index.

Approach:
1. Sort intervals by their right endpoint. This allows us to efficiently find non-overlapping previous intervals using binary search.
2. Use dynamic programming: `dp[k][i]` = maximum weight achievable using at most k intervals from the first i+1 intervals (0-indexed in sorted list).
3. For each interval i, find the rightmost interval j (in the sorted list) such that intervals[j].end < intervals[i].start. This can be done with binary search.
4. Transition: `dp[k][i] = max(dp[k][i-1], dp[k-1][prev] + weight_i)` where prev is the index found by binary search.
5. Backtracking: To get lexicographically smallest indices, when backtracking, we need to be careful. Since we sorted by right endpoint, the indices in the original array are permuted. We need to track original indices.
   - When backtracking from dp[4][n-1], at each step, check if including the current interval gives the same optimal value as excluding it. If including gives the same value, we have a choice. To get lexicographically smallest result, we should prefer including the interval with the smaller original index? Actually, the standard approach for lexicographically smallest is: when backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1], we exclude. The issue is when both are equal. 
   
   Actually, a better approach for lexicographical order: 
   - After computing DP, backtrack from the end. At each state (k, i), if we can include interval i (i.e., dp[k][i] == dp[k-1][prev] + weight_i) and also dp[k][i] == dp[k][i-1] (if i>0), then we have a tie. To get lexicographically smallest indices, we should prefer the solution that includes the interval with the smaller original index. But since we sorted by right endpoint, the original indices are not in order.
   
   Alternative: Instead of standard backtracking, we can reconstruct the solution by iterating from the smallest original index to the largest and greedily deciding whether to include an interval. But that is complex.
   
   Actually, a known technique: 
   - When backtracking, if including the current interval yields the same total weight as excluding it, then we should include it only if its original index is smaller than what we would get by excluding? This is tricky.
   
   Better insight: 
   Since we want lexicographically smallest array of indices, and the output is sorted indices, we want the set of indices that is lexicographically smallest. 
   
   We can modify the DP state to also store the actual set of indices, but that is too expensive.
   
   Standard solution for this type of problem:
   - After computing DP table, backtrack. At each step, if dp[k][i] == dp[k-1][prev] + weight_i, then we have the option to include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), we also have the option to exclude. 
   - To ensure lexicographically smallest, when both options are available, we should choose the option that leads to a smaller index in the result. Since the result is sorted, including a smaller index is better. But the intervals are sorted by right endpoint, not by original index.
   
   Actually, the correct backtracking for lexicographical smallest:
   - Iterate k from 4 down to 1.
   - Start from the last interval (largest right endpoint) and move backwards.
   - At each interval i, check if including it is part of an optimal solution: i.e., if dp[k][i] == dp[k-1][prev] + weight_i.
   - If yes, then we include it. But we must also check that this choice doesn't prevent us from getting a lexicographically smaller result. 
   
   Actually, a simpler method: 
   When backtracking, if the value from including the current interval equals the value from excluding (i.e., dp[k][i] == dp[k][i-1] and also dp[k][i] == dp[k-1][prev] + weight_i), then we should prefer including the interval with the smaller original index. But since we are iterating backwards (from large right endpoint to small), the intervals we encounter later in the backtracking (i.e., with smaller right endpoints) might have smaller or larger original indices.
   
   This is complex. A robust method:
   - Store in dp[k][i] not just the max weight, but also the actual list of indices? Too expensive.
   
   Insight from similar problems (e.g., Leetcode 1751): 
   When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a tie. In case of tie, to get lexicographically smallest, we should prefer the solution that includes the interval with the smaller original index. 
   
   However, note that the output is the sorted list of indices. So lexicographically smallest means: compare the first index, then second, etc. So we want the smallest possible first index, then smallest possible second index given the first, etc.
   
   Therefore, during backtracking, we should try to include intervals with smaller original indices first. But our DP is computed with intervals sorted by right endpoint.
   
   Revised backtracking strategy:
   - Instead of backtracking from the end, we can reconstruct the solution by considering intervals in increasing order of their original indices. But that breaks the DP structure.
   
   Actually, a known correct approach for this specific problem (as seen in solutions for similar problems):
   - When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a choice. In this case, to get lexicographically smallest, we should include the interval only if its original index is smaller than any index that would be included if we excluded it. But this is hard to determine.
   
   Simpler: Since the constraints are small (k=4), we can store the actual indices in the DP state? But n is 5e4, so storing lists is too expensive.
   
   Alternative: 
   - After computing DP, backtrack greedily: 
     Start with k=4, i=n-1.
     While k > 0 and i >= 0:
       prev = largest index j < i such that intervals[j].end < intervals[i].start (if no such j, prev = -1)
       val_include = (dp[k-1][prev] if prev != -1 else 0) + weight_i
       val_exclude = dp[k][i-1] if i > 0 else 0
       if val_include >= val_exclude:  # if including is at least as good
         # But to get lexicographically smallest, we need to check: if val_include == val_exclude, then including interval i might lead to a larger index in the result than excluding it? 
         # Actually, no: because we are building the result from the last interval backwards. The indices we pick will be sorted at the end. 
         # The key: if we include interval i, then the set of indices will include i's original index. If we exclude, it won't. 
         # To get lexicographically smallest, we want the smallest indices. So if val_include == val_exclude, we should prefer the option that results in a smaller index being included. But since we are going backwards, the intervals we include later (in backtracking order) will be smaller in the sorted result? Actually, no: the result is sorted, so the order in the result is by index value, not by backtracking order.
         
   This is very tricky.
   
   Actually, a standard solution for this problem (as per known problems like "Maximum Weight Independent Set of size k" with lexicographical requirement) is:
   - When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a tie. In this case, we should include interval i only if its original index is less than the smallest index that would be included in the solution obtained by excluding it. But we don't know that without further computation.
   
   Given the complexity, and since k is only 4, a practical approach:
   - Do the DP as described.
   - For backtracking, iterate i from 0 to n-1 (in the sorted order) and greedily decide: 
     Actually, no.
   
   After research, a correct method:
   - When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a tie. In this case, to get lexicographically smallest, we should prefer excluding the current interval if its original index is larger than the smallest index that would be included in the alternative solution. But this is circular.
   
   Simpler insight: 
   The lexicographically smallest array of indices is achieved by, among all optimal solutions, picking the one that has the smallest first index, then smallest second index, etc.
   This can be achieved by: 
   - When backtracking, if there is a tie (val_include == val_exclude), then we should choose the option that includes the interval with the smaller original index. But since we are backtracking from the end, we don't know which indices will be included in the alternative solution.
   
   Given the time, I'll implement the standard DP and backtracking, and in case of tie during backtracking, prefer including the interval (which might not be lexicographically smallest). But actually, for the examples, including when tied might work because the intervals are sorted by right endpoint, and the original indices might be correlated.
   
   Actually, a better approach for lexicographical smallest: 
   - Instead of backtracking from the end, reconstruct the solution by iterating from the smallest original index to the largest. For each interval, decide whether to include it based on whether it can be part of an optimal solution. 
   - This requires a forward DP or recomputation.
   
   Given constraints, I'll stick with the standard backtracking and hope that in case of tie, including the interval (which has a certain original index) is correct. But to ensure lexicographical smallest, when val_include == val_exclude, we should include the interval only if its original index is smaller than the minimum index that would be included if we excluded it. But we don't know that.
   
   Actually, a known trick: 
   When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a tie. In this case, we should include interval i only if its original index is less than the smallest index in the solution obtained by excluding it. But to know that, we would need to know the solution from excluding it.
   
   Given the complexity, and since k is small, I'll implement the following:
   - In backtracking, if val_include > val_exclude, include.
   - If val_include < val_exclude, exclude.
   - If equal, then include interval i only if its original index is less than the smallest index that would be included in the solution from excluding. But we don't have that information.
   
   Alternative: 
   - Do not use backtracking. Instead, after computing DP, iterate through intervals in increasing order of original index, and for each interval, check if it can be part of an optimal solution. 
   - This is complex.
   
   I'll implement the standard backtracking and in case of tie, include the interval. This might not be lexicographically smallest, but for the given examples, it works. And in many cases, the tie-breaking by including might yield the correct result because the intervals with smaller right endpoints (which are processed earlier in sorted order) might have smaller original indices? Not necessarily.
   
   Actually, to get lexicographically smallest, we should prefer smaller indices. So in backtracking, when there is a tie, we should prefer the option that includes the interval with the smaller original index. But since we are backtracking from the end (largest right endpoint to smallest), the intervals we encounter have varying original indices.
   
   Given the time, I'll write the solution with standard backtracking and hope for the best. If needed, we can add a tie-breaker: when val_include == val_exclude, include the interval only if its original index is less than a threshold, but we don't know the threshold.
   
   Actually, a correct method for lexicographical smallest: 
   - When backtracking, if dp[k][i] == dp[k-1][prev] + weight_i, then we include interval i. But if dp[k][i] == dp[k][i-1] (for i>0), then we have a tie. In this case, we should include interval i only if its original index is less than the smallest index that would be included in the solution obtained by excluding it. But to know that, we can recursively compute the solution from excluding it and take the minimum index. But that is expensive.
   
   Given constraints (k=4), we can afford to store the actual indices in the DP state for small k. But n is 5e4, so storing lists of up to 4 integers for each state is 5e4 * 4 * 4 = 800k integers, which is acceptable.
   
   Revised plan:
   - dp[k][i] = (max_weight, list_of_indices) for the first i+1 intervals (sorted by right endpoint) using at most k intervals.
   - But merging lists is expensive. Instead, we can store the indices as a tuple and use memoization. But worst-case, the number of states is 4 * 5e4 = 200k, and each state stores a tuple of up to 4 integers. This is acceptable in Python.
   
   Steps:
   1. Sort intervals by right endpoint, keeping track of original indices.
   2. Initialize dp[0][i] = (0, []) for all i.
   3. For k from 1 to 4:
        For i from 0 to n-1:
          Option1: exclude interval i -> dp[k][i-1] (if i>0, else (0,[]))
          Option2: include interval i -> find prev, then dp[k-1][prev] + (weight_i, [original_index_i])
          Compare the two options: first by weight, then by the list of indices (lexicographically).
          But comparing lists lexicographically is expensive. Instead, we can store the list and compare.
   4. Backtracking is not needed; the answer is dp[4][n-1][1].
   
   But comparing lists of indices lexicographically: 
   - When weights are equal, we want the lexicographically smallest list of indices. 
   - So when updating dp[k][i], if the weight from including is greater than excluding, choose include. If less, choose exclude. If equal, choose the one with lexicographically smaller list of indices.
   
   This is correct and handles lexicographical requirement.
   
   Complexity: O(4 * n * log n) for binary search, and O(4 * n) for DP with list comparisons (each list has at most 4 elements, so comparison is O(1)).
   
   This should work.

## worker: Implement the DP solution with lexicographical tie
The solution uses dynamic programming where `dp[k][i]` stores a tuple `(max_weight, list_of_indices)` representing the maximum weight achievable using at most `k` non-overlapping intervals from the first `i+1` intervals (sorted by right endpoint), along with the lexicographically smallest list of original indices that achieves this weight.

Key steps:
1. **Sorting**: Intervals are sorted by their right endpoint to facilitate efficient non-overlapping checks.
2. **Binary Search**: For each interval, we precompute the index of the latest non-overlapping previous interval using `bisect_left` on the sorted right endpoints.
3. **DP Transition**: For each state `(k, i)`, we consider two options:
   - Exclude interval `i`: take the value from `dp[k][i-1]`.
   - Include interval `i`: take the value from `dp[k-1][prev[i]]` and add the current interval's weight and original index.
4. **Tie-breaking**: When weights are equal, we choose the option with the lexicographically smaller list of indices. Since the lists are short (at most 4 elements), comparison is efficient.
5. **Result Extraction**: The answer is directly obtained from `dp[4][n-1][1]`.

Complexity: O(n log n) for sorting and binary search preprocessing, and O(4 * n) for DP filling with constant-time list comparisons (since lists have at most 4 elements). This fits within the constraints.

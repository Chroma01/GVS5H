
## ideation
We need to select up to 4 non-overlapping intervals to maximize total weight, and if multiple subsets achieve the max weight, return the lexicographically smallest list of original indices (with shorter prefix preferred when the first min(len(a), len(b)) elements are identical). Intervals must be strictly non‑overlapping: if one ends at x, the next must start > x.

Constraints: n up to 5·10⁴, coordinates up to 10⁹, weights up to 10⁹, max k=4. So O(n log n) or O(k·n log n) is fine. O(n²) is too slow.

Observations:
- This is a weighted interval scheduling problem with a limit k=4 and a tie‑breaking rule on indices.
- We can sort intervals by right endpoint (and perhaps left for stability). When sorting we need to keep original indices.
- We need to consider subsets of size ≤ 4. Classic DP for k up to 4 can be done in O(k·n log n) using binary search to find the previous compatible interval.
- But the main difficulty is the lexicographic tie‑breaking. The result must be the lexicographically smallest index list among all optimal-weight subsets.
- Note: lexicographic order is defined on arrays of indices. Shorter array is lexicographically smaller if all first min(len) elements are equal.
- Since the number of intervals is large, we cannot enumerate subsets; we must compare DP states directly.

DP formulation:
- Sort intervals by `r` ascending, then `l` ascending. Let `intervals_sorted = sorted(enumerate(intervals), key=lambda x: (x[1][1], x[1][0]))` but we need to store original index.
- Let `n` = number of intervals.
- `dp[k][i]` = best (highest weight) achievable using at most k intervals among the first i sorted intervals (i.e., considering intervals 0..i-1). But to also handle lexicographic tie‑breaking, we need to store the actual best subset of indices.
- Since weights can be large (up to 10⁹) and we have up to 4 intervals, total weight up to 4·10⁹, fits in Python int.
- For each i (interval i in sorted order), we want to compute dp[k][i+1] from dp[k][i] (skip) and dp[k-1][j+1] + w_i (include), where j is the largest index < i such that intervals[j].r < intervals[i].l.
- But storing the full subset for each state might be expensive if we store lists of length up to 4; n=5·10⁴, k=5 (0..4), so total states ~2.5·10⁵, each storing a tuple of up to 4 indices — manageable (memory ~ a few MB). However copying tuples frequently may be slower but should be okay.

Alternative: We can store dp as a list of length n for each k, but we only need the previous column? Actually transitions go from dp[k][j+1] to dp[k][i+1]. This is similar to standard weighted interval scheduling where we can just keep dp[k] as an array and update it in order of increasing r. But careful: When processing interval i, we need the dp value at position p = j+1, which is the best using at most k-1 intervals among first p intervals (0..p-1). If we process intervals in order of r, we can keep dp[k] as a list of length n+1 where dp[k][i] is the best using at most k intervals among first i intervals. Then dp[k][i+1] = max(dp[k][i], combine(dp[k-1][p], interval i)). But this requires dp[k-1][p] to be already computed, which it is because p <= i. However we also need to store the actual best subset for each state to be able to compare lexicographically.

But we must be careful: dp[k][i] should be the best among first i intervals. The combine operation: take the best subset for at most k-1 intervals among first p intervals, add interval i. The new subset has size at most k. The new total weight is dp[k-1][p].weight + w_i. We need to compare this candidate with the current best dp[k][i] (which is the best using up to k intervals among first i intervals, i.e., excluding i or some earlier combination). We choose the one with larger weight; if equal weight, choose lexicographically smaller index list; if still equal, choose shorter list? Actually the problem says: "If the first min(a.length, b.length) elements do not differ, then the shorter array is the lexicographically smaller one." So yes, shorter is better when prefixes match.

So we need a comparison function for two candidates (weight, index_list). But careful: The DP states might have different numbers of intervals. For example, dp[k][i] could be achieved with 1, 2, 3, or 4 intervals. The "weight" is the sum, and the "index list" is the actual indices. The comparison for picking the best among candidates of same k (max weight) is:
- Higher total weight is better.
- If equal weight, lexicographically smaller index list is better.
Note: The problem says "lexicographically smallest array of at most 4 indices ... with maximum score". So we only care about maximum score; among those, lexicographically smallest. So we don't need to compare across different k values for the same state? Wait, dp[k][i] is "up to k intervals". So if k=4, we consider subsets of size 1,2,3,4. But the final answer should be the best among all subsets of size ≤4. So we can compute dp[4] over all n, and the final answer is the best state for k=4 at i=n. However, we must ensure that among subsets of size ≤4 with the same maximum weight, we pick the lexicographically smallest. The DP with "up to k" naturally compares subsets of different sizes: if a subset of size 2 has weight 10 and a subset of size 3 has weight 10, the size 2 subset is lexicographically smaller? Not necessarily: lexicographic order compares element by element. Example: subset A = [5, 6] (indices), subset B = [2, 3, 4]. Compare: first element 5 > 2, so B is smaller lexicographically even though A is shorter. The problem's rule: "If the first min(a.length, b.length) elements do not differ, then the shorter array is the lexicographically smaller one." So if A = [2, 3, 4] and B = [2, 3], then first two elements [2,3] equal, B is shorter, so B is smaller. If A = [1, 5] and B = [1, 5, 6], first two equal, B is shorter, so B is smaller. So among equal-weight subsets, we need to pick the lexicographically smallest list. This is not simply "prefer fewer intervals" because a longer list could have a smaller first differing element.

Therefore, the comparison must be: given two candidates (weight1, list1) and (weight2, list2), we say candidate1 is better than candidate2 if:
- weight1 > weight2, or
- weight1 == weight2 and list1 is lexicographically smaller than list2.

We don't need a separate tie-breaker on length because the lexicographic rule already handles it: if one list is a prefix of the other, the shorter is smaller.

So we can define a comparison: (weight, list) where list is a tuple of indices. But we need to be careful: the weight is the primary key. So we can store each DP state as a tuple (weight, list) or just store the list and keep weight separately. Since we need to compare many states, we can store weight and list. For comparison:
```
if w1 != w2: return w1 > w2
return list1 < list2  # Python tuple comparison is lexicographic
```
But Python's tuple comparison compares element by element. However, we need to ensure that shorter list is considered smaller when it's a prefix. Python's tuple comparison does exactly that: (1,2) < (1,2,3) is True. So we can just store the list as a tuple and compare.

Thus DP state: dp[k][i] = (max_weight, best_indices_tuple). For k=0, dp[0][i] = (0, ()).

Transition:
- For each i from 0 to n-1 (sorted intervals):
  - For k from 1 to 4:
    - Option 1: not take interval i. Candidate = dp[k][i] (the best among first i intervals).
    - Option 2: take interval i. Find p = binary search for largest index j < i such that intervals[j].r < intervals[i].l. Then candidate from dp[k-1][p+1]? Wait careful: dp[k-1][j+1] is the best among first j+1 intervals. Since we want to combine with interval i, we need the best among first j+1 intervals (0..j) that are non-overlapping with i. Actually intervals up to j (inclusive) are all before i in sorted order by r. But we need the best among intervals that end before l_i. Since we sorted by r, all intervals with index <= j have r <= r_j < l_i, so they are all compatible. So we can take dp[k-1][j+1] (where j+1 is the count). Then add interval i's original index to the tuple. The new weight = dp[k-1][j+1].weight + w_i. The new tuple = dp[k-1][j+1].tuple + (original_index_i,).
    - We need to compare Option 1 and Option 2 using the comparison rule to get dp[k][i+1].

We also need to handle the base case: dp[0][i] = (0, ()) for all i.

But we must ensure that when we take interval i, we don't exceed k intervals. Since we transition from k-1 to k, that's fine.

Complexity: For each i, we do binary search (O(log n)) to find p, and for each k (1..4) we compare two candidates. So total O(4 * n log n) = O(n log n), which is fine for n=5e4.

However, storing dp as a 2D list of tuples of size (5 x (n+1)) might be memory heavy but acceptable: 5 * 50001 * (two integers + small tuple). Actually each state stores a tuple of indices. The total number of stored tuples is about 5 * 5e4 = 2.5e5. Each tuple is small (up to 4 ints). Memory: 2.5e5 * (say 48 bytes per tuple overhead) ~ 12 MB, plus the list overhead. Should be fine in Python.

But we can optimize: we don't need to store dp[k][i] for all k and all i; we can just keep dp[k] as a list of length n+1 for each k, or even keep only the previous column? However, the transition from dp[k-1][p+1] needs a value that is computed earlier (since p+1 <= i). If we process i in increasing order and maintain dp[k] as an array where dp[k][i] is the best for first i intervals, we can update dp[k][i+1] in place? Actually we need dp[k-1][p+1] which is already computed because p+1 <= i+1? Wait, p is the index of the last compatible interval. Since p < i, p+1 <= i. So dp[k-1][p+1] is already computed when we are at step i (processing interval i). But if we update dp[k][i+1] in place, we need to have dp[k-1] available as a full array. So we need to store dp for all k. Alternatively, we can process intervals in order and for each k maintain a list dp_k of length n+1, but we must be careful not to overwrite dp[k-1] values needed later. Actually dp[k-1] is used only for transitions to dp[k] for the same i or later i? For a given i, we need dp[k-1][p+1] where p+1 <= i. If we have already updated dp[k-1] for the current i? Let's think: We can process k from 1 to 4 in increasing order for each i. For k=1, we need dp[0][p+1] which is always (0,()). For k=2, we need dp[1][p+1], which we have just computed in the current i iteration (since we process k=1 first). But is dp[1][p+1] available? p+1 could be less than or equal to i. If we are updating dp[1] in place, then dp[1][p+1] might have been updated in this same i iteration? But p+1 <= i, and we are processing i. The value dp[1][p+1] corresponds to the best using at most 1 interval among the first p+1 intervals. Since we are currently considering taking interval i, the state dp[1][p+1] should not include interval i. But if we have already updated dp[1][i+1] (when i was the previous interval?), no, because we process i sequentially. Actually for a fixed i, when we compute dp[1][i+1], we are only using dp[1][i] and dp[0][p+1]. dp[1][i] is already computed. So dp[1][p+1] for p+1 <= i is already computed and not changed during the processing of the current i (unless we are in the same i and k=1, we haven't updated dp[1][i+1] yet, but dp[1][p+1] is at index <= i, which is not the current index i+1). So it's safe. So we can keep dp as a list of lists: dp[k] is a list of length n+1, and we update dp[k][i+1] based on dp[k][i] and dp[k-1][p+1]. Since we process k in increasing order, dp[k-1] is already fully computed for all indices up to i+1. So we don't need to store the whole 2D array; we can store dp as a list of 5 lists (k=0..4). But we must be careful: dp[k][i] is the best among first i intervals. When we move to i+1, we update dp[k][i+1]. Since we need dp[k-1][p+1] and p+1 <= i+1, it's fine. However, we must ensure that we don't overwrite dp[k-1] values that might be needed for later i? No, because dp[k-1] is only updated at index i+1 when we process interval i, but later intervals will need dp[k-1] at indices less than or equal to their own p+1. Since we only increase i, the values at smaller indices remain unchanged. So we can update in place.

But there is a subtle point: For k=4, we need dp[3][p+1]. If we update dp[3][i+1] in the current i iteration, then later when we process a larger i', we might need dp[3][p'+1] where p'+1 could be i+1? That would be the case if p' = i. Then we would need dp[3][i+1] which we just updated. That's fine because it's available. So updating in place works as long as we process k in increasing order: for a given i, we first update dp[1][i+1], then dp[2][i+1], etc. When updating dp[k][i+1], we rely on dp[k-1][p+1] which is already updated for this i (since k-1 < k, we have already updated dp[k-1][i+1]? Wait, p+1 could be i+1? No, p is the index of the last compatible interval before i. Since intervals are sorted by r, and p < i, p+1 <= i. So p+1 is at most i. It cannot be i+1 because the current interval is i, and p is the last interval with r < l_i, so p <= i-1. So p+1 <= i. So dp[k-1][p+1] is at an index <= i. That value was computed in previous iterations (or in the current iteration for index i? Actually dp[k-1][i] is the value after processing intervals 0..i-1. We are currently processing interval i. So dp[k-1][i] is already computed. We haven't touched dp[k-1][i+1] yet. So it's safe.

Thus we can implement with dp as a list of 5 lists of length n+1. Initialize dp[0] = [(0, ())] * (n+1). Then for i in range(n): for k in range(1,5): compute.

But we need to be careful with the comparison and the tuple addition. We can store the best tuple as a list or tuple. Since we need to add the current interval's original index, we can do:
```
candidate_tuple = dp[k-1][p+1][1] + (original_index,)
candidate_weight = dp[k-1][p+1][0] + w_i
```
Then compare with dp[k][i] (which is the best among first i intervals). Note: dp[k][i] is a tuple (weight, indices). We want to pick the better between (dp[k][i].weight, dp[k][i].indices) and (candidate_weight, candidate_tuple). Use the comparison function.

But wait: dp[k][i] is the best among first i intervals. That includes the possibility of using fewer than k intervals. So we must compare the candidate (which uses exactly k intervals if we take it) with dp[k][i] (which could use up to k). That's correct.

So the transition is:
```
best = dp[k][i]  # not taking i
# take i
p = find_last_compatible(i)  # returns index of last interval with r < l_i, or -1
if p >= 0:
    prev = dp[k-1][p+1]
    cand_weight = prev[0] + w_i
    cand_tuple = prev[1] + (orig_idx,)

## worker: Implement the data structures and DP transitions i
I implemented the DP approach as planned: sort intervals by right endpoint, then for each interval and each k from 1 to 4, compute the best state by either skipping it or taking it (combined with the best compatible previous state). The comparison handles both weight maximization and lexicographic tie-breaking (using Python's tuple comparison, which naturally prefers shorter lists when one is a prefix of the other). The binary search finds the last non-overlapping interval in O(log n) per transition, giving overall O(n log n) time. Memory is O(n) for the DP table.

## worker: finalize
The solution uses dynamic programming with a twist for lexicographic tie-breaking. After sorting intervals by right endpoint, we maintain `dp[k][i]` representing the best state (maximum weight, lexicographically smallest index tuple) achievable using at most `k` intervals among the first `i` sorted intervals. The comparison function prioritizes higher weight, and breaks ties using Python's built-in tuple comparison which naturally handles the "shorter prefix is smaller" rule. The binary search finds the last compatible interval in O(log n), and updating DP for k=1..4 gives O(4·n·log n) time complexity, well within the limits for n=5×10⁴.

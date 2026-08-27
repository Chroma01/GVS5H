
## ideation
The problem is a constrained version of weighted interval scheduling: pick at most 4 non-overlapping intervals maximizing total weight, and among all optimal selections return the lexicographically smallest index list (shorter preferred on ties).  
Key points and pitfalls:

1. **Strict non-overlap**: Intervals sharing an endpoint overlap (`r_i >= l_j` and `l_i <= r_j` means they conflict). For DP we need the last interval that ends **strictly** before the current start, i.e. `r < l_i`.

2. **Lexicographic order on index lists**:
   - Compare total weight first.
   - If equal weight, we need the smallest list in lex order. Python’s built‑in list comparison works if we keep the lists the same length; but the problem says *shorter* list is considered smaller when prefixes are equal. So the comparison must be:
     ```
     (weight, len(indices), indices)
     ```
     (shorter length is “smaller” only when prefixes equal, which tuple comparison handles because Python compares shorter tuple as smaller when the first differing element is compared, and here `len` will break the tie). However, careful: if `len` differs but the longer list is a prefix of the shorter? Not possible because we never prefix‑extend. A simple and correct key is `(weight, -weight_of_indices?)`. Actually a safe representation is `(weight, indices)` but with a custom comparator. Easier: store `(-weight, len(indices), indices)` because we want max weight, but we also need smallest indices on tie. Let's settle on key `(-weight, len(indices), indices)` for max‑heap style. Or keep DP as normal `dp[k][i] = (weight, indices)` and compare `(weight, -len, indices)` when taking max. Actually we need **largest weight**, and for equal weight we want **lexicographically smallest indices**, which includes preferring shorter length. So the ordering is:
     - higher weight is better,
     - if weights equal, the list with smaller length is better,
     - if lengths equal, the list with lexicographically smaller indices is better.
   - Therefore we can use a tuple `(weight, -len, indices)` and take the **maximum** according to this tuple. In Python, `max` uses lexicographic order, so this works.

3. **DP transitions**:
   For each interval `i` (sorted by end), for each `k` (1..K):
   - Not take: `dp[k][i] = dp[k][i-1]`.
   - Take: if we take interval `i`, we add its weight to `dp[k-1][p[i]]` plus interval's own index. Compare with `dp[k][i-1]` and keep the better according to the ordering above.

4. **Backtracking**:
   To recover the indices, we can store predecessor information (a `choice` array) indicating whether interval `i` was taken at state `(k, i)`. Or we can simply recompute during backtracking using the same DP logic, which is O(K·n) extra but simpler. Since n is 5e4 and K=4, we can recompute or store a boolean `take[k][i]`. Storing booleans is fine: (K+1)*(n+1) ≤ 5*5e4 = 2.5e5 booleans.

5. **Indices**:
   After selecting indices according to sorted order, we need to return them sorted by original index. The example shows the answer is `[2,3]` (original indices, 0‑based) and `[1,3,5,6]`. So we must sort the result before returning.

6. **Complexities**:
   - Sorting: O(n log n).
   - Computing `p` with two‑pointer: O(n).
   - DP: O(K·n) = O(4·n) = O(n).
   - Memory: dp tables of size (K+1) x (n+1). Each entry stores a weight and a list of indices. Storing full lists for every entry would be O(K·n·avg_len) which is too large. We need to store only the optimal list for each state. Since K=4 and n=5e4, we could store Python lists; in worst case each list could be up to 4 elements, so total memory is about 4 * 5e4 * 4 = 8e5 integers, which is fine (~3 MB). However copying lists for each transition could be O(K·n) overhead but still acceptable (4*5e4 = 2e5 list copies of at most 4 elements). Python list copy of 4 elements is cheap, but we can also store tuples and convert later. For safety, we can store a tuple of indices to avoid mutation issues, and convert to list at the end. Tuples are immutable and slightly faster to compare than lists? List compare works elementwise. We'll store tuples.

   But note: when we do `dp[k][i] = dp[k][i-1]`, we are just referencing the same tuple; no copy needed. For the “take” case we do `new_tuple = dp[k-1][p[i]] + (orig_idx,)`. That creates a new tuple. So total O(K·n) tuple creations, each up to 4 elements: fine.

7. **Binary search for p[i]**:
   We can use `bisect_right` on the array of end times to find the rightmost interval with end < start. Since we need the predecessor in the sorted order, we can store an array of end times for the sorted intervals. Then `pos = bisect_left(ends, l_i) - 1` (because `bisect_left` gives first end >= l_i, we want last < l_i). Use that index +1 for DP indexing (since DP is 1‑based). This is O(n log n) but fine. Two‑pointer O(n) is also easy.

8. **Edge cases**:
   - No intervals: return [].
   - Fewer than 4 intervals: DP still works.
   - All intervals overlap: answer could be a single interval with max weight; lexicographically smallest index among those with max weight (since lists of length 1 are shorter than longer lists of same weight). Our tuple ordering ensures that shorter list is considered better when weight equal, and for length 1 vs 1 we pick smallest index.

9. **Lexicographic tie‑breaking in DP**:
   Because we compare `(-weight, len, indices)` via Python's `max`, we need to make sure that when weights are equal, we compare lengths and then indices correctly. Example: weight=10, indices (2,3) vs (1,4). Both length=2. Lexicographically, (1,4) < (2,3) because first element 1<2. Our tuple `(-10, 2, (1,4))` vs `(-10, 2, (2,3))`. Python compares first -10 equal, then 2 equal, then (1,4) vs (2,3) -> (1,4) is smaller, so `max` will pick (2,3) because it is larger? Wait: We want the lexicographically **smallest** indices. So we want to pick the *smaller* tuple. But we are using `max` to get the *best* DP value. So we need to define the ordering such that the *best* DP value is the *maximum* in that order. So we need:
   - larger weight is better → first component should be weight (so max weight is larger).
   - for equal weight, smaller length is better → second component should be -length (so shorter length gives larger -length, i.e. larger value).
   - for equal weight and length, lexicographically smaller indices is better → third component should be the negative of the indices? Or we can store the indices but we need the max to correspond to smaller indices. That means we want to treat indices as a number where smaller is larger. We can store `-indices` elementwise? Or we can store the indices as a tuple and then compare with `max` using a custom key.

   Simplest: don't use `max`; just write a helper `better(a, b)` that returns True if a is better than b (i.e., a should be chosen over b). Then `dp = better(dp, candidate)`. This avoids messing with sign flips. Since we only compare a few candidates (two per transition), the overhead is negligible.

   Define a tuple representation for comparison:
   `key = (weight, -len(indices), indices)`? Wait, we want the *better* to have:
   - higher weight,
   - if weight equal, lower length,
   - if weight and length equal, lower lexicographic indices.
   So we can store the "score" as a tuple `(weight, -len, indices)` and use Python's `>` to compare which is better (i.e., greater tuple = better). Let's verify:
   - A: weight 10, len 2, indices (2,3) → tuple (10, -2, (2,3)).
   - B: weight 10, len 2, indices (1,4) → tuple (10, -2, (1,4)).
   - Compare: 10==10, -2==-2, then (2,3) > (1,4) lexicographically, so tuple (10,-2,(2,3)) > (10,-2,(1,4)). That would consider A better, but B is lexicographically smaller. So using this tuple would favor larger indices, which is wrong.

   So we need a representation where lexicographically smaller indices yields a *larger* tuple. We can store `(-weight, len, indices)`? No, that would invert weight. We need:
   - Larger weight → larger tuple.
   - Smaller length → larger tuple.
   - Lexicographically smaller indices → larger tuple.
   So for indices, we can store the *negative* of each index? But indices are variable length. One trick: store the indices reversed? Not helpful. Another trick: store the indices and compare by custom logic.

   Simpler: just write a comparison function:
   ```python
   def is_better(a, b):
       # a and b are (weight, indices_tuple)
       wa, ia = a
       wb, ib = b
       if wa != wb:
           return wa > wb
       if len(ia) != len(ib):
           return len(ia) < len(ib)
       return ia < ib
   ```
   Then `if is_better(candidate, dp): dp = candidate`. This is clear and correct.

   We can also encode as `(-wa, len(ia), tuple(-x for x in ia))` but that's messy.

   So we'll use a helper function or a lambda with `key` to a tuple that is compared with `max`. Let's try to make a key that sorts ascending by "badness" so that `max` picks the best. Equivalent: `key = (-weight, len, indices)` because:
   - We want max of key to be best.
   - For higher weight, `-weight` is smaller (more negative), so `max` would prefer less negative → lower weight? That's opposite. So we need to flip sign carefully.

   Let's think: Suppose we want a key `K` such that `a is better than b` iff `K(a) > K(b)`. Then we can set:
   - First component: weight (higher better).
   - Second component: -len (so shorter length gives higher -len? Actually shorter length is better, so we want higher key for shorter length → -len is larger for shorter length? No: if len=2, -len=-2; len=3, -len=-3. -2 > -3, so shorter length gives larger -len, which is good. So second component can be `-len`.
   - Third component: we need lexicographically smaller indices to give larger key. We can store `(-x for x in indices)` and compare lexicographically. Since each element is negated, the order is reversed: smaller original x becomes larger -x. For example, indices (1,4) vs (2,3):
     - Negated: (-1, -4) vs (-2, -3). Compare: -1 > -2, so (-1,-4) > (-2,-3). So (1,4) yields larger key, which corresponds to lexicographically smaller original indices. Perfect.
   So the key is:
   ```python
   key = (weight, -len(indices), tuple(-x for x in indices))
   ```
   Then `max(candidates, key=key)` will pick the best according to our criteria.

   However, generating the negated tuple for every candidate might be overhead, but K=4 and n=5e4, total candidates 2e5, each tuple of at most 4 elements. That's fine.

   Alternatively, just implement `is_better` and avoid the key. Simplicity vs performance: both fine. I'll use the key approach for brevity.

   Let's test the key on examples:
   - A: weight 10, idx (2,3) → key (10, -2, (-2,-3)).
   - B: weight 10, idx (1,4) → key (10, -2, (-1,-4)).
   - Compare: (10,-2,(-2,-3)) vs (10,-2,(-1,-4)). First two equal, third: -2 < -1, so B's key > A's key → max picks B, which is lexicographically smaller indices. Good.
   - Weight 10, len 1, idx (5) vs len 2, idx (1,4): keys (10,-1,(-5)) vs (10,-2,(-1,-4)). Compare: -1 > -2, so len=1 is better, good.
   - Weight 9 vs 10: first component 10 > 9, so weight 10 wins, good.

   So the key works.

   Implementation details:
   - DP array: list of size (K+1) x (n+1) (or list of lists). `dp[k][i]` stores the optimal tuple `(weight, indices_tuple)`. We can store only the indices tuple and keep a separate `weight` array, but storing the whole tuple is okay.
   - Actually to avoid storing weight twice, we can store a tuple `(weight, indices_tuple)` or two parallel arrays. Let's store the key? No, we need weight and indices to reconstruct. Storing `(weight, indices_tuple)` is fine.
   - Base: `dp[0][i] = (0, ())` for all i. `dp[k][0] = (0, ())`.
   - For each i from 1..n:
     - For k from 1..K:
       - `not_take = dp[k][i-1]`.
       - `take_weight = intervals[i-1][2] + dp[k-1][p[i-1]][0]`.
         Wait: `dp[k-1][p[i-1]]` is for the first `p[i-1]` intervals in sorted order. Since DP is 1-indexed and we use `p` as 0-indexed position in sorted array, we need to map to DP index: `p_idx = p[i-1] + 1`? Let's be careful.
       - Sorted intervals are 0-indexed in array `sorted_intervals`. We compute `p[i]` as the index (0-based) in sorted array of the last interval that ends before current start. Then in DP, which is 1-indexed, the prefix of length `p[i]+1` corresponds to DP index `p[i]+1`. So:
         `prev = dp[k-1][p[i-1] + 1]` (since DP is 1-indexed, position 0 is dummy). Actually `p[i-1]` is the 0-based index, so the number of intervals considered is `p[i-1] + 1`. So DP index = `p[i-1] + 1`.
       - `take_indices = prev[1] + (original_index_of_i,)`.
       - `take = (take_weight, take_indices)`.
       - Compare `take` and `not_take` using our key, keep the better.

   - After filling DP, the answer is `dp[K][n][1]` (the indices tuple). But we need at most 4, so we could also check `dp[k][n]` for k=0..4 and pick the best among them? Actually the problem says "up to 4", meaning we can choose 0 to 4 intervals. The DP for k=4 already considers the possibility of not taking some intervals (by inheriting from k-1 or from not taking). Wait, does the DP for k=4 allow taking fewer than 4? Yes, because at each step we can skip. So `dp[4][n]` is the best using *at most* 4 intervals. So we can just take `dp[4][n]`. However, we must ensure that the DP for k allows 0 intervals. The base case is 0 weight, empty tuple. And transitions allow not taking. So `dp[4][n]` is correct. But we also have `dp[0]`, `dp[1]`, etc. Since the "at most" is included, `dp[4][n]` is the global optimum for at most 4. Good.

   - But we must also consider that we might have fewer than 4 intervals in the optimal set; that's fine.

   - To backtrack and get indices, we can either:
     - Store a `choice[k][i]` boolean indicating whether we took interval i at state (k,i). Then backtrack from (K,n) to 0.
     - Or just re-run a forward/backward reconstruction using the DP table and the sorted order, checking if `dp[k][i] == dp[k][i-1]` to decide not take, else take. Since dp values are tuples, equality works if they are the same object or equal. But they might be the same tuple object (we reuse references). We can just compare `dp[k][i] is dp[k][i-1]` or `==`. But due to tuple creation, they may be different objects with same content. We can store a boolean `took` to be safe. Memory for booleans: (K+1)*(n+1) = 5*50001 = 250005 booleans ≈ 250KB. Acceptable.
     - Or we can backtrack by recomputing: starting from (k,i) = (K,n), if i>0 and dp[k][i] != dp[k][i-1], then we must have taken interval i (since if not take, dp would be same as dp[k][i-1]). But we need to ensure that the "not take" case is indeed dp[k][i-1]. However, there is a subtle case: dp[k][i] could equal dp[k][i-1] even if we took i, if taking i yields the same weight and lexicographically smaller indices? No, if we take i, the indices tuple will be different (includes i). So dp[k][i] would be different. The only way dp[k][i] == dp[k][i-1] is if we didn't take i. So we can backtrack by checking inequality. But we need to be careful: dp[k][i] might be a different tuple object but with same content. Python's tuple equality compares contents, so it works. So we can avoid storing booleans. However, we need to be able to subtract the interval when taking. Let's design a backtrack function:

       ```python
       def backtrack(k, i):
           if k == 0 or i == 0:
               return []
           if dp[k][i] == dp[k][i-1]:
               return backtrack(k, i)
           else:
               # took interval i-1 (0-indexed in sorted)
               # the predecessor state is (k-1, p[i-1] + 1)
               prev = backtrack(k-1, p[i-1] + 1)
               prev.append(original_index_of_i)
               return prev
       ```

       This recursion depth is at most K=4, so fine.

   - However, we must be careful: dp[k][i] could be equal to dp[k][i-1] but we could have taken i and the result coincidentally is the same? That would require that taking i and not taking i result in exactly the same (weight, indices). But taking i adds the index of i to the indices tuple, making it longer. So they cannot be equal. So the check is safe.

   - So we can backtrack without extra storage.

10. **Computing p[i] with two pointers**:
    - Sort intervals by end time. Let `sorted_intervals = sorted(enumerate(intervals), key=lambda x: x[1][1])`. Actually we need to sort by `r`. For each sorted interval, we also have original index.
    - Create an array `ends` of the end times.
    - Use pointer `j` that points to the last interval with end < current start. Initialize j = -1 (0-indexed). For each i from 0 to n-1:
      - While j+1 < i and ends[j+1] < starts[i]: j += 1.
      - Then `p[i] = j`. If j < 0, then `p[i] = -1`, meaning no predecessor. In DP, we map to index 0 (empty prefix).
    - Actually we need `p[i]` to be the 0-based index of the last interval ending before start_i. The loop above works.

    Alternatively, use binary search:
    ```python
    p[i] = bisect_left(ends, starts[i]) - 1
    ```
    Since `ends` is sorted, `bisect_left` returns the first index where end >= start. So index-1 is the last end < start. This is O(n log n). Both are fine. I'll use binary search for clarity.

11. **Handling large coordinates**:
    Coordinates up to 1e9, but we only compare them, no issue.

12. **Output format**:
    Return list of indices (original indices) sorted ascending. The problem expects an array of indices. The examples show 0-based indices.

13. **Testing on examples**:
    - Example 1: intervals = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
      - Sort by end:
        - [1,3] (0)
        - [4,5] (1)
        - [1,5] (2)  (end 5)
        - [6,7] (4)  (end 7)
        - [6,9] (3)  (end 9)
        - [8,9] (5)  (end 9)
        Actually [6,9] end 9, [8,9] end 9. Sort by end, tie by start? For DP we need consistent order. Tie-breaking by start doesn't matter for correctness as long as we handle p correctly. But for p (predecessor), if two intervals have same end, we need to ensure that an interval with start equal to that end is considered overlapping (since r >= l). Our p condition is end < start. So if end = start, it's overlapping, so we should not consider it as predecessor. In binary search, `bisect_left(ends, start)` returns the first index with end >= start. So index-1 is last with end < start. That's correct. For ties in end, order doesn't affect p because end < start condition is independent of order among same end. So sorting by end is sufficient.

      - Let's compute manually to verify the algorithm yields [2,3] (original indices 2 and 3). The optimal is intervals 2 ([1,5] weight 5) and 3 ([6,9] weight 3). Note that [4,5] weight 2 also fits, but 5+3=8 vs 5+2=7, so 5+3 is better. Also maybe [1,3] weight 2 and [4,5] weight 2 and [6,7] weight 1 and [8,9] weight 1: sum=6, less. So correct.

      - Our DP should find max weight 8, and lexicographically smallest indices: among all weight-8 solutions, are there others? Could we take [1,3] (0) + [4,5] (1) + [6,9] (3)? Sum=2+2+3=7, no. So unique solution. Output sorted: [2,3].

    - Example 2: intervals = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
      - The answer is [1,3,5,6] (0-based). Let's trust the algorithm.

14. **Potential pitfalls**:
    - **Empty result**: DP[K][n] might be (0, ()). We should return [].
    - **Sorting indices**: The backtrack returns indices in the order they were added (which is sorted by end time because we process sorted intervals). We need to sort them by original index before returning.
    - **Stable sorting**: Not required.
    - **Large n**: 5e4, DP O(n) with small constant is fine.
    - **Using recursion for backtrack**: depth K=4, safe. Or we can do iteratively.
    - **Tuple vs list for indices**: Use tuple for immutability and to avoid accidental mutation.
    - **Key function for max**: We can use a custom comparator in the loop: `if is_better(candidate, dp[k][i]): dp[k][i] = candidate`. This avoids creating key tuples. Simpler to code and less error-prone regarding signs. I'll implement `is_better`.

    Define:
    ```python
    def is_better(cand, cur):
        w_c, idx_c = cand
        w_cur, idx_cur = cur
        if w_c != w_cur:
            return w_c > w_cur
        if len(idx_c) != len(idx_cur):
            return len(idx_c) < len(idx_cur)
        return idx_c < idx_cur
    ```
    Then in transition:
    ```python

## worker: Implement the DP-based solution for up to 4 non-ov
- Implemented weighted interval scheduling with at most K=4 intervals using DP.
- Sorted intervals by end time while preserving original indices.
- Used `bisect_left` to compute for each interval the last non-overlapping predecessor (strict `end < start`).
- DP state: `dp[k][i]` = best `(weight, tuple_of_indices)` using up to `k` intervals from the first `i` sorted intervals.
- Custom comparator `is_better` implements the required ordering: higher weight first, then shorter length, then lexicographically smaller indices.
- Transitions consider both "skip" and "take" options, updating with the better candidate.
- Final answer is `dp[4][n]` (allows 0–4 intervals), indices sorted by original position as required.
- Complexity: O(n log n) for sorting + binary search, O(K·n) DP, K=4. Memory O(K·n) storing tuples (max 4 indices each). Efficient for n ≤ 5·10⁴.

## worker: Test the solution thoroughly with the provided exa
The solution implements weighted interval scheduling with at most K=4 intervals using dynamic programming. It sorts intervals by end time, computes the predecessor index for each interval using binary search (strictly less than start to ensure non-overlap), and fills a DP table where each state stores the best `(weight, indices_tuple)` according to the required ordering: higher weight, then shorter index list, then lexicographically smaller indices.

The `is_better` function encapsulates this comparison logic. The final answer is taken from `dp[4][n]`, which allows 0 to 4 intervals. Indices are returned sorted by original position.

Testing covers the provided examples plus edge cases: single interval, empty input, fewer than 4 intervals, all overlapping (max weight, smallest index), tie-breaking on weight (shortest list), tie-breaking on weight and length (lexicographically smallest indices), boundary overlaps (endpoints count as overlap), and cases where all 4 intervals can be selected.

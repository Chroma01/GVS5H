
## ideation
- **Core Difficulty**: 
  - Selecting up to 4 non-overlapping intervals to maximize total weight.
  - Breaking ties by lexicographically smallest index array.
  - Large coordinate range ($10^9$) requires coordinate compression or sorting by end time for efficient DP transitions.
  - Need to reconstruct the actual indices, not just the max weight.
  - Lexicographical comparison involves comparing the full sequence of indices, which complicates standard DP state design (usually DP stores just the max value).

- **Candidate Approaches**:
  1. **DP with Sorting**:
     - Sort intervals by end time (primary) and start time (secondary) to enable efficient transition checks.
     - Define `dp[k][i]` = max weight using exactly `k` intervals where the last interval is `i`.
     - To handle the "up to 4" constraint, we can run DP for $k=1$ to $4$.
     - Transition: For each interval `i` and count `k`, iterate over all previous intervals `j` such that `intervals[j].end < intervals[i].start`. Update `dp[k][i] = max(dp[k][i], dp[k-1][j] + weight[i])`.
     - **Pitfall**: The naive transition is $O(N^2)$, which is too slow for $N=5 \times 10^4$. We need an optimization.
     - **Optimization**: Since we sort by end time, when considering interval `i`, we only need the best `dp[k-1][j]` among all `j` where `intervals[j].end < intervals[i].start`. We can precompute suffix maximums or use a Fenwick tree/Segment tree if coordinates were compressed, but since we sort by end time, a simple linear scan or binary search + precomputed max array might work. Specifically, for a fixed `k`, as we iterate `i` in sorted order, the set of valid `j`'s grows. We can maintain the best `dp[k-1][j]` seen so far that satisfies the non-overlapping condition.
     - **Lexicographical Tie-Breaking**: This is the hardest part. Standard DP only stores the max weight. If multiple sequences yield the same max weight, we need the lexicographically smallest one. 
       - Option A: Store the full path in DP state? Too memory intensive.
       - Option B: Store the "best previous index" that leads to the optimal solution. But "best" depends on the future choices too? No, because we fix the last interval `i` for the current step. The lexicographical order of the whole array is determined by the first element first. However, our DP builds from the end (last interval chosen). 
       - Re-evaluating Lexicographical Requirement: We want the array of indices $[idx_1, idx_2, \dots, idx_m]$ to be lexicographically smallest. This means we prefer smaller $idx_1$, then smaller $idx_2$, etc.
       - Since the DP builds backwards (from last interval to first), the lexicographical order is hard to enforce directly in the DP state unless we reframe the problem.
       - Alternative: Since $k$ is very small (up to 4), maybe we can iterate on the *first* interval index? No, that's $O(N)$ starts, then $O(N)$ for second, etc., leading to $O(N^4)$ worst case if not careful, but with pruning it might be acceptable? $50000^4$ is definitely too big.
       - Better approach for Lexicographical: 
         - We can compute the max weight for each possible "first interval" $i$ and "last interval" $j$? No.
         - Let's reconsider the DP state. Maybe we don't need to store the path in DP. We can compute `max_weight[k][i]` (max weight using $k$ intervals ending at $i$). Then, to find the lexicographically smallest sequence:
           - We know the total max weight $W_{max}$.
           - We need to find the smallest index $i_1$ such that there exists a valid sequence starting with $i_1$ with total weight $W_{max}$.
           - Once $i_1$ is fixed, find the smallest $i_2$ such that $i_2$ is non-overlapping with $i_1$, and there exists a valid sequence $i_1, i_2, \dots$ with remaining weight $W_{max} - weight[i_1]$.
           - This greedy reconstruction works if we have precomputed `max_weight[k][start_index]` or similar.
         - Let's refine the DP:
           - Sort intervals by end time.
           - `dp[k][i]` = max weight using $k$ intervals ending with interval $i$.
           - To optimize transitions: For a fixed $k$, iterate $i$ in sorted order. We need $\max_{j: end_j < start_i} dp[k-1][j]$. We can maintain a running maximum of `dp[k-1][j]` as we iterate. However, the condition is $end_j < start_i$. Since we sort by $end_j$, as $i$ increases, $start_i$ increases, so the set of valid $j$'s (where $end_j < start_i$) is a prefix of the sorted list (roughly). We can use two pointers or binary search to find the split point and maintain the max.
           - After filling `dp[k][i]` for all $i$ and $k \in [1, 4]$, we find the global maximum weight $W_{max}$.
           - Now, reconstruct lexicographically:
             - Try all possible first indices $idx_1$ in increasing order. Check if there exists a sequence starting with $idx_1$ with total weight $W_{max}$.
             - How to check efficiently? We need `max_weight_remaining(k-1, min_end_after_idx1)`.
             - So we need another DP: `best[k][i]` = max weight using $k$ intervals where the *first* interval is $i$. Or, more simply, `suffix_max[k][i]` = max weight using $k$ intervals starting from any interval with $start \ge i$? No, the constraint is on the *end* of the previous interval.
             - Actually, the standard "max weight with $k$ intervals" DP gives us `dp[k][last]`.
             - To support greedy reconstruction:
               - Precompute `dp[k][i]` = max weight of $k$ intervals ending at $i$.
               - Also precompute `dp_suffix[k][i]` = max weight of $k$ intervals where the *first* interval has index $\ge i$? No, the intervals are not sorted by index.
               - Let's sort intervals by index? No, sorting by end time is crucial for the DP transition.
               - Let's stick to sorting by end time. Let the sorted intervals be $S_0, S_1, \dots, S_{N-1}$.
               - `dp[k][i]` = max weight of $k$ intervals ending with $S_i$.
               - To reconstruct:
                 - Find global max $W$.
                 - Iterate $i$ from $0$ to $N-1$ (sorted index). If $S_i$ could be the first interval:
                   - We need to know if there exists a sequence of length $m$ starting with $S_i$ with weight $W$.
                   - This requires knowing the max weight of $m-1$ intervals that start *after* $S_i$ ends.
                   - Let `next_max[k][j]` = max weight of $k$ intervals where the *first* interval is $S_j$ (in the sorted list).
                   - Then `next_max[k][j] = weight[j] + max(next_max[k-1][p])` for all $p$ such that $S_p.start > S_j.end$.
                   - We can precompute `next_max` similarly to `dp` but iterating backwards? Or just compute `dp` (ending at $i$) and `next_max` (starting at $j$).
                   - Actually, `next_max[k][j]` is exactly the max weight of $k$ intervals where the first chosen interval is $S_j$.
                   - Then `next_max[k][j] = weight[j] + max_{p: S_p.start > S_j.end} (next_max[k-1][p])`.
                   - We can compute this by iterating $j$ in reverse order of sorted list? No, the dependency is on $p$ where $S_p.start > S_j.end$. Since we sort by end time, $S_p.start$ isn't necessarily monotonic with $p$. But we can coordinate compress or use a segment tree/Fenwick tree over the start times to query max efficiently.
                   - Given constraints ($N=50000$), $O(N \log N)$ or $O(N)$ is needed.
                   - With sorting by end time, we can use a Fenwick tree (or just an array with coordinate compression on start times) to query max `next_max[k-1][p]` for $S_p.start > S_j.end$.
                   - Once we have `next_max[k][j]` for all $j$ and $k$, we can reconstruct:
                     - Global max $W$.
                     - Try $idx_1$ from $0$ to $N-1$ (sorted index). If `next_max[m][idx_1] == W` for some $m \in [1, 4]$, then $idx_1$ is a candidate for the first interval. Pick the smallest such $idx_1$.
                     - Then for the next interval, we need the smallest index $idx_2$ (in the original array) such that $S_{idx_2}.start > S_{idx_1}.end$ and `next_max[m-1][idx_2] == remaining_weight`.
                     - Wait, "smallest index" refers to the original index, not the sorted index. So we need to map back.
                     - Algorithm:
                       1. Sort intervals by end time, keep original indices.
                       2. Compute `dp[k][i]` (max weight ending at sorted index $i$) using forward pass with Fenwick/Two-pointers.
                       3. Compute `next_max[k][i]` (max weight starting at sorted index $i$) using backward pass? No, the dependency is on start time.
                          - Actually, `next_max[k][i]` depends on `next_max[k-1][p]` where $S_p.start > S_i.end$.
                          - We can compute `next_max` by iterating $i$ from $N-1$ down to $0$? No, because $S_p.start > S_i.end$ doesn't imply $p > i$.
                          - Instead, we can use coordinate compression on start times. Map each unique start time to a rank.
                          - Build a Fenwick tree (or Segment Tree) that stores max `next_max[k-1][p]` at position `rank(S_p.start)`.
                          - Iterate $i$ from $0$ to $N-1$: query max in range `(rank(S_i.end), max_rank)`.
                          - This gives `next_max[k][i]`.
                       4. Reconstruct:
                          - Find global max $W$.
                          - Iterate original index $u$ from $0$ to $N-1$. Let $i$ be the sorted index of $u$.
                          - Check if there exists $m \in [1, 4]$ such that `next_max[m][i] == W`.
                          - If yes, pick the smallest such $u$ (since we iterate $u$ increasingly).
                          - Then fix $u_1 = u$. Remaining weight $W' = W - weight[u_1]$.
                          - Next, iterate original index $v$ from $u_1+1$ to $N-1$. Let $j$ be sorted index of $v$.
                          - Check if $S_j.start > S_i.end$ and `next_max[m-1][j] == W'`.
                          - Pick smallest $v$.
                          - Repeat until $m$ intervals are chosen or we run out.
                          - Since we want *at most* 4, we should also consider sequences of length 1, 2, 3, 4. We find the max weight over all lengths $1..4$. Let $W_{max}$ be that.
                          - Then we try to build a sequence of length $L$ ($1 \le L \le 4$) with weight $W_{max}$.
                          - To ensure lexicographical smallest, we try lengths $L=1, 2, 3, 4$. For a fixed $L$, we try to find the lexicographically smallest sequence of length $L$ with weight $W_{max}$.
                          - Actually, the problem says "up to 4". So we maximize weight first. If multiple lengths give same max weight, which one to pick? The problem says "Return the lexicographically smallest array". A shorter array is lexicographically smaller if it's a prefix? No, "If the first min(a.length, b.length) elements do not differ, then the shorter array is the lexicographically smaller one."
                          - So if we have a sequence of length 3 with weight $W$ and length 4 with weight $W$, the length 3 one is smaller? Only if the first 3 elements are the same. But they can't be the same because the 4th element adds weight? No, weights are positive. So if we have a sequence of length 4 with weight $W$, we can't have a subsequence of length 3 with weight $W$ (since weights are positive). Thus, the max weight sequence will have a specific length. We just need to find the lexicographically smallest among all sequences (of any length $1..4$) that achieve $W_{max}$.
                          - Wait, could a length 3 sequence have weight $W_{max}$ and a length 4 sequence have weight $W_{max}$? Only if the 4th interval has weight 0, but weights are $\ge 1$. So the length is uniquely determined by the weight? Not necessarily, different combinations could sum to same total.
                          - Example: 3 intervals of weight 10 vs 10 intervals of weight 1 (but max 4). So 3 intervals of 10 = 30, 2 intervals of 15 = 30. Both length 3 and 2. Length 2 is smaller.
                          - So we need to check all lengths $L \in [1, 4]$. For each $L$, find if max weight $W_{max}$ is achievable. If yes, find the lexicographically smallest sequence of length $L$ with weight $W_{max}$. Then compare these candidates across $L$.
                          - Since $L$ is small, we can just generate the best candidate for each $L$ and pick the best overall.

- **Pitfalls**:
  - Coordinate range $10^9$: Must compress start times for Fenwick tree or use sorting + two pointers carefully.
  - Lexicographical comparison: Must iterate original indices in increasing order during reconstruction.
  - "Up to 4": Must check lengths 1 to 4.
  - Time complexity: $O(N \log N)$ or $O(N)$ with good implementation. $N=50000$ allows $O(N \log N)$.
  - Memory: Storing DP tables for $k=1..4$ and $N$ items is fine ($4 \times 50000$ integers).

## worker: Sort the intervals by end time (primary) and start
1.  **Sorting and Coordinate Compression**: Intervals are sorted by end time (primary) and start time (secondary) to facilitate DP transitions. Start times are coordinate-compressed to map large values ($10^9$) to ranks $[0, m-1]$ for efficient range queries.
2.  **Forward DP (`dp`)**: Computes `dp[k][i]` = max weight using exactly $k$ intervals ending with sorted interval $i$. This is done in $O(N \log N)$ using a prefix max array and binary search to find valid previous intervals.
3.  **Backward DP (`suffix_dp`)**: Computes `suffix_dp[k][i]` = max weight using exactly $k$ intervals starting with sorted interval $i$. This is done using a Segment Tree over the compressed start times to efficiently query the max weight of $k-1$ intervals that start after the current interval ends. This step is $O(N \log N)$.
4.  **Reconstruction**: Iterates through possible lengths $L \in [1, 4]$. For each length, it greedily selects the smallest original index $v$ that allows completing a sequence of length $L$ with the target weight `max_w`. The validity of a choice is checked using the precomputed `suffix_dp` table. The lexicographically smallest sequence among all valid lengths is returned.
5.  **Complexity**: Time complexity is dominated by sorting and the DP steps, $O(N \log N)$. Space complexity is $O(N)$ for storing DP tables and the segment tree.

## worker: Implement the `maximumWeight` method with the comp
1.  **Sorting**: Intervals are sorted by end time (primary) and start time (secondary) to facilitate the forward DP transition. This allows us to efficiently find valid previous intervals using binary search on end times.
2.  **Coordinate Compression**: Start times are compressed to ranks $[0, m-1]$ to enable efficient range queries using a Segment Tree for the backward DP.
3.  **Forward DP (`dp`)**: `dp[k][i]` stores the maximum weight of a sequence of length $k$ ending at sorted interval $i$. Transitions use a prefix maximum array to find the best previous interval in $O(1)$ after an $O(\log N)$ binary search.
4.  **Backward DP (`suffix_dp`)**: `suffix_dp[k][i]` stores the maximum weight of a sequence of length $k$ starting at sorted interval $i$. Transitions use a Segment Tree over compressed start times to query the maximum weight of $k-1$ intervals that start after the current interval ends.
5.  **Reconstruction**: We iterate through possible lengths $L \in [1, 4]$. For each length, we greedily select the smallest original index $v$ that allows completing a sequence of length $L$ with the target weight `max_w`. The validity of a choice is checked using the precomputed `suffix_dp` table. The lexicographically smallest sequence among all valid lengths is returned.
6.  **Complexity**: Time complexity is $O(N \log N)$ due to sorting and Segment Tree operations. Space complexity is $O(N)$ for DP tables and the Segment Tree.

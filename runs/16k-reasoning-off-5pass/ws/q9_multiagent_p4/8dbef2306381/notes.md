
## ideation
The core difficulty is the large constraint on $N$ ($10^{12}$) versus the small constraints on $M$ ($2 \times 10^4$) and the jump range $B$ ($20$). A simple BFS or DP over all squares $1 \dots N$ is impossible due to time and memory limits.

Key observations:
1.  **Bad Squares are Intervals**: The bad squares form $M$ disjoint intervals $[L_i, R_i]$. Since $R_i < L_{i+1}$, we can process the number line in segments separated by these intervals.
2.  **Reachability Propagation**: From a set of reachable squares, jumping by $[A, B]$ creates a new set of reachable squares. If we have a contiguous block of reachable squares of length at least $B$, we can reach every subsequent square until the next obstacle (or indefinitely if no more obstacles).
3.  **State Compression**: Instead of tracking every square, we only need to track the "frontier" of reachable squares. Specifically, after passing a bad interval, we need to know the smallest reachable square $\ge$ start of next interval and the largest reachable square $\le$ end of next interval (if any).
4.  **Algorithm Strategy**:
    -   Add virtual bad intervals $[1, 0]$ (empty) and $[N, N]$ (target is bad? No, target is $N$, usually safe, but we must land *on* $N$. The problem says "Square $x+i$ is not bad". So $N$ must not be bad. The constraints say $R_i < N$, so $N$ is never bad).
    -   Sort the bad intervals.
    -   Maintain a set of reachable squares. Initially $\{1\}$.
    -   Iterate through bad intervals. For each interval $[L, R]$:
        -   Calculate all reachable squares in the range $[L-1, R]$.
        -   Since the jump range is small ($B \le 20$), the set of reachable squares in any small window can be computed by iterating backwards from the current reachable set.
        -   Specifically, if we know the set of reachable squares up to $L-1$, we can determine which squares in $[L, R]$ are reachable by jumping from them.
        -   However, since intervals are disjoint, we can just calculate the set of reachable squares immediately before the gap ($L-1$) and then see which squares inside the gap are reachable.
        -   Actually, a more efficient way: Maintain the set of reachable squares $S$. When approaching interval $[L, R]$, we compute $S' = \{ x \mid \exists s \in S, A \le x-s \le B \}$. We filter out bad squares.
        -   Crucially, if the gap between the last reachable square and the start of a bad interval is large, the reachable set might become "full" (contiguous). If we have a contiguous range of length $B$ reachable, we can reach everything up to the next obstacle.
    -   **Optimization**: Since $B$ is very small, we can just maintain the set of reachable offsets relative to the current "interesting" point, or simply the set of reachable squares in the range $[L, L+B]$.
    -   Better approach:
        1.  Collect all critical points: $1$, $L_i$, $R_i+1$, $N$. Sort them.
        2.  Actually, we don't need all points. We just need to simulate the propagation of reachability across the gaps.
        3.  Let `reachable` be a boolean array or set of squares reachable *before* the current bad interval starts.
        4.  Since $N$ is huge, we can't store an array. But the number of bad intervals is small.
        5.  We can process interval by interval.
            -   Start with `reachable = {1}`.
            -   Current position `cur = 1`.
            -   For each bad interval $[L, R]$:
                -   We need to find all squares $x \in [L, R]$ that are reachable.
                -   A square $x$ is reachable if there exists $s \in \text{reachable}$ such that $x-s \in [A, B]$.
                -   This implies $s \in [x-B, x-A]$.
                -   So $x$ is reachable if $[x-B, x-A] \cap \text{reachable} \neq \emptyset$.
                -   Since we are moving forward, we can compute the set of reachable squares in the current segment $[L, R]$.
                -   Wait, the "reachable" set before $L$ might be sparse. But once we pass $L$, we generate new reachable squares.
                -   Key insight: The set of reachable squares will eventually become a contiguous interval $[min\_reach, max\_reach]$. Once the length of this contiguous interval is $\ge B$, we can reach every square up to the next obstacle (and beyond).
                -   So, we maintain the set of reachable squares. If the set becomes contiguous with length $\ge B$, we can assume "infinite" reachability until the next obstacle.
                -   Algorithm:
                    1.  Sort bad intervals.
                    2.  `reachable` = set containing `1`.
                    3.  `last_safe` = 1.
                    4.  For each interval $[L, R]$:
                        -   If `last_safe` < $L$:
                            -   We have a gap between `last_safe` and $L$. In this gap, we can reach squares $[last\_safe + A, last\_safe + B]$.
                            -   Actually, we need to propagate reachability from `last_safe` up to $L$.
                            -   Let's refine: We maintain the set of reachable squares $S$. Initially $S=\{1\}$.
                            -   We iterate through the bad intervals. Let the current interval be $[L, R]$.
                            -   We need to determine which squares in $[L, R]$ are reachable.
                            -   A square $x \in [L, R]$ is reachable if $\exists s \in S$ such that $x-s \in [A, B]$.
                            -   This is equivalent to $s \in [x-B, x-A]$.
                            -   Since $S$ is finite and we process intervals in order, we can compute the intersection.
                            -   However, $S$ can grow. But notice that if we have a contiguous block of reachable squares of size $B$, we can reach everything after that block until the next obstacle.
                            -   So, we can track the "contiguous reachable segment" ending at the current point.
                            -   Let `min_reach` and `max_reach` be the bounds of the contiguous reachable segment ending at some point.
                            -   Actually, simpler: Just maintain the set of reachable squares $S$. Since $B$ is small, $|S|$ won't explode if we prune.
                            -   Wait, if we have a gap of size $> B$ with no bad squares, $S$ becomes $[start, end]$.
                            -   Correct logic:
                                -   Maintain a set `reachable` of squares that are reachable.
                                -   Initially `reachable = {1}`.
                                -   Sort bad intervals.
                                -   Current max reachable square `curr_max = 1`.
                                -   For each bad interval $[L, R]$:
                                    -   If `curr_max` < $L$:
                                        -   We can't reach $L$ directly from `curr_max` if the gap is too big? No, we can jump from any $s \le curr\_max$ to $x \ge L$ if $x-s \le B$.
                                        -   So the reachable squares in $[L, R]$ are those $x$ where $[x-B, x-A] \cap \{s \mid s \le curr\_max\} \neq \emptyset$.
                                        -   This simplifies to: $x$ is reachable if $x-A \le curr\_max$ AND $x-B \ge \text{min\_reachable\_in\_S}$.
                                        -   Actually, if we have a contiguous block of reachable squares ending at `curr_max`, say $[curr\_max - k + 1, curr\_max]$, then any $x$ such that $[x-B, x-A]$ overlaps this block is reachable.
                                        -   Specifically, if we have a contiguous range $[u, v]$ of reachable squares, then any $x$ such that $x-A \le v$ and $x-B \ge u$ is reachable.
                                        -   So $x \in [u+B, v+A]$.
                                        -   We intersect this with $[L, R]$ to find reachable squares inside the bad interval.
                                        -   Update the contiguous range if possible.
                                    -   If `curr_max` $\ge L$:
                                        -   We can reach $L$. The contiguous range continues or extends.
                                        -   We need to check if the gap between the previous contiguous end and $L$ is small enough to bridge.
                                        -   Actually, if `curr_max` $\ge L$, then $L$ is reachable (since $L - curr\_max \le 0 < A$? No. $L$ is reachable if $\exists s \in [u, v]$ such that $L-s \in [A, B]$).
                                        -   Condition: $L-B \le v$ and $L-A \ge u$.
                                        -   If reachable, we extend the contiguous range.
                                        -   If not reachable, the contiguous range breaks. We need to track multiple components?
                                        -   Given $B \le 20$, the number of components is small. Or maybe just one component matters?
                                        -   If a component breaks, can it reconnect? Yes, if there's a gap of bad squares, we might lose connectivity.
                                        -   But since $B$ is small, we can just maintain the set of reachable squares explicitly as a list of intervals or a set of integers. Since the number of bad intervals is $2 \times 10^4$, and we only care about the "frontier", the set of reachable squares won't be huge.
                                        -   Wait, if we have a long gap of good squares, the reachable set becomes a single interval $[min, max]$.
                                        -   So the state is either a single interval or a few small intervals near the obstacles.
                                        -   Algorithm refinement:
                                            1.  `reachable` = list of disjoint intervals $[start, end]$. Initially `[[1, 1]]`.
                                            2.  Sort bad intervals $[L_i, R_i]$.
                                            3.  For each bad interval $[L, R]$:
                                                -   Compute new reachable intervals.
                                                -   An interval $[s, e]$ in `reachable` can reach squares in $[s+A, e+B]$.
                                                -   Intersect $[s+A, e+B]$ with $[L, R]$ to find which bad squares are reachable.
                                                -   Wait, we need to know which squares are reachable *after* the bad interval to continue.
                                                -   Actually, the bad squares themselves don't help us jump further. We only care about squares $\le R$ that are reachable, to jump from them to squares $> R$.
                                                -   So, after processing $[L, R]$, the new `reachable` set consists of:
                                                    1.  Intervals from the old `reachable` that are completely $< L$ (they remain reachable, but they can't jump into $[L, R]$ effectively if the gap is too big? No, they can jump to $L$ if $L-s \le B$).
                                                    2.  Intervals formed by jumping from old `reachable` into $[L, R]$.
                                                    3.  But squares in $[L, R]$ are bad, so we cannot jump *from* them.
                                                    4.  Therefore, the only useful reachable squares after $R$ must come from jumps originating from squares $\le R$.
                                                    5.  Specifically, if we land on $x \in [L, R]$, we are stuck? No, we can't land on bad squares.
                                                    6.  "Square $x+i$ is not bad". So we cannot land on $[L, R]$.
                                                    7.  This means any jump that lands in $[L, R]$ is invalid.
                                                    8.  So we can only jump from $s$ to $x$ if $x \notin [L, R]$.
                                                    9.  So, if we have a reachable interval $[s, e]$ before $L$:
                                                        -   We can jump to $x > R$ if $\exists s \in [s, e]$ such that $x-s \in [A, B]$ and $x > R$.
                                                        -   Also, we might jump to $x \in [L, R]$? No, that's forbidden.
                                                        -   So we skip $[L, R]$.
                                                        -   The next reachable squares will be in $[R+1, \infty)$.
                                                        -   Which ones? Those $x > R$ such that $[x-B, x-A] \cap [s, e] \neq \emptyset$.
                                                        -   This creates a new interval (or intervals) starting after $R$.
                                                -   Wait, what if there are multiple bad intervals?
                                                -   We process them one by one.
                                                -   Between bad intervals, there might be good squares.
                                                -   If there is a gap of good squares between $R_i$ and $L_{i+1}$, we can propagate reachability through it.
                                                -   If the gap is large ($\ge B$), the reachable set becomes a single contiguous interval $[min, max]$ covering the whole gap.
                                                -   If the gap is small, we might have multiple components.
                                                -   Since $B$ is small, we can simulate the propagation through the gap explicitly.
                                                -   Steps:
                                                    1.  Start with `reachable` = `[[1, 1]]`.
                                                    2.  Current position `pos = 1`.
                                                    3.  For each bad interval $[L, R]$:
                                                        -   If `pos` < $L$:
                                                            -   We have a gap $(pos, L)$.
                                                            -   Propagate reachability from `reachable` through the gap to $L-1$.
                                                            -   Since the gap is good, any square reachable from `reachable` is also reachable (if we can jump to it).
                                                            -   Actually, if we have a reachable interval $[s, e]$, we can reach $[s+A, e+B]$.
                                                            -   If $e+B \ge L$, we can reach into the bad interval? No, we can't land on bad squares.
                                                            -   So we can reach up to $L-1$ if $e+B \ge L-1$.
                                                            -   If we can reach $L-1$, then we have a reachable interval ending at $L-1$.
                                                            -   Then we try to jump over $[L, R]$.
                                                            -   From any $s \in [s_{start}, e_{end}]$ (the reachable set before $L$), we can jump to $x > R$ if $x \in [s+A, s+B]$ and $x > R$.
                                                            -   The set of such $x$ forms a union of intervals.
                                                            -   Since we only care about the "frontier" to continue, we can merge these intervals.
                                                            -   If the resulting set of reachable squares after $R$ has a contiguous block of length $\ge B$, we can simplify it to a single interval $[min, max]$ where $max$ is the largest reachable square.
                                                        -   If `pos` $\ge L$:
                                                            -   We are already past the start of the bad interval.
                                                            -   We need to check if we can jump over $[L, R]$.
                                                            -   Same logic: from the current reachable set, find all $x > R$ reachable.
                                                    4.  After processing all bad intervals, check if $N$ is reachable.
                                                    5.  If the final reachable set contains $N$, output Yes. Else No.

        -   **Refined Simulation**:
            -   `reachable`: list of tuples `(start, end)` representing contiguous intervals of reachable squares.
            -   Initially `[(1, 1)]`.
            -   Sort bad intervals.
            -   For each bad interval $[L, R]$:
                -   Filter `reachable` to keep only intervals that can potentially jump over $[L, R]$ or are before it.
                -   Actually, simpler:
                    -   Calculate the set of reachable squares *strictly greater* than $R$.
                    -   A square $x > R$ is reachable if $\exists s \in \text{reachable}$ such that $x-s \in [A, B]$.
                    -   This means $x \in [s+A, s+B]$.
                    -   So we take the union of $[s+A, s+B]$ for all $s \in \text{reachable}$.
                    -   Intersect this union with $(R, \infty)$.
                    -   This gives the new `reachable` set.
                    -   However, if there are good squares between $R$ and $L_{next}$, we need to propagate further.
                    -   But wait, the "bad" intervals are the only obstacles. Between $R_i$ and $L_{i+1}$, all squares are good.
                    -   So if we have a set of reachable squares after $R_i$, say $S_i$, and the next bad interval starts at $L_{i+1}$:
                        -   If $S_i$ allows us to reach $L_{i+1}-1$, we can continue propagating.
                        -   If the gap $L_{i+1} - (\max(S_i))$ is small, we might not reach $L_{i+1}$.
                        -   Actually, we can just run the "jump over" logic repeatedly until we either hit a bad interval or run out of reach.
                        -   But since $B$ is small, we can just simulate step-by-step? No, $N$ is large.
                        -   We need to handle the gap $[R_i+1, L_{i+1}-1]$ efficiently.
                        -   If we have a reachable interval $[u, v]$ and the next bad interval is $[L, R]$:
                            -   We can reach any $x \in [u+A, v+B]$.
                            -   We need to intersect this with $[R+1, \infty)$? No, we need to intersect with $[R+1, L-1]$ to see what's reachable before the next obstacle.
                            -   If $v+B \ge L-1$, then we can reach up to $L-1$.
                            -   If we can reach $L-1$, then we have a reachable interval ending at $L-1$.
                            -   Then we try to jump over $[L, R]$ again.
                            -   If we can't reach $L-1$, then we are blocked.
                            -   Wait, if we have multiple intervals in `reachable`, we take the union.
                            -   If the union of reachable intervals covers a range $[min, max]$ such that $max \ge L-1$, then we can reach $L-1$.
                            -   Actually, if we have a contiguous block of reachable squares of length $\ge B$, we can reach everything up to the next obstacle.
                            -   So, after computing the reachable set after $R_i$, we check if it forms a contiguous block of length $\ge B$.
                            -   If yes, we can assume we can reach any square up to $L_{i+1}-1$ (and even jump over $[L_{i+1}, R_{i+1}]$ if the block is long enough? No, we need to check the jump condition).
                            -   If we have a contiguous block $[u, v]$ with $v-u+1 \ge B$:
                                -   We can reach any $x$ such that $x \in [u+A, v+B]$.
                                -   If $v+B \ge L_{i+1}$, we can reach into the next bad interval? No, we can't land on bad squares.
                                -   But we can jump *over* the bad interval if there exists $s \in [u, v]$ such that $s+A > R_{i+1}$.
                                -   Condition: $v+A > R_{i+1}$.
                                -   If $v+A > R_{i+1}$, we can jump to some $x > R_{i+1}$.
                                -   Specifically, the smallest reachable square after $R_{i+1}$ is $\max(R_{i+1}+1, v+A)$.
                                -   And we can reach up to $v+B$.
                                -   So the new reachable set after $R_{i+1}$ will be $[ \max(R_{i+1}+1, v+A), v+B ]$.
                                -   This new interval will also be contiguous and of length $\ge B$ (since $v-u+1 \ge B \implies v+B - (v+A) + 1 = B-A+1 \ge 1$, wait. Length might shrink).
                                -   Actually, if we have a block of length $B$, we can reach a block of length $B$ after the jump?
                                -   Let's trace: $s \in [u, v]$. $x = s+k, k \in [A, B]$.
                                -   $x \in [u+A, v+B]$. Length is $(v-u+1) + (B-A)$.
                                -   If we filter $x > R$, the length might be cut.
                                -   But if $v+A > R$, then the interval $[v+A, v+B]$ is fully $> R$. Length is $B-A+1$.
                                -   If $B-A+1 \ge 1$, we have at least one point.
                                -   If we have a contiguous block of length $\ge B$, we can definitely reach the next obstacle's end if the jump range allows.
                                -   Actually, the condition "contiguous block of length $\ge B$" is sufficient to say "we can reach everything up to the next obstacle and potentially jump over it".
                                -   So, algorithm:
                                    1.  `reachable` = `[(1, 1)]`.
                                    2.  Sort bad intervals.
                                    3.  For each bad interval $[L, R]$:
                                        -   Compute `new_reachable` = $\bigcup_{[s, e] \in reachable} ([s+A, s+B] \cap (R, \infty))$.
                                        -   Simplify `new_reachable` into disjoint intervals.
                                        -   If `new_reachable` is empty, return "No".
                                        -   Check if `new_reachable` contains a contiguous interval of length $\ge B$.
                                            -   If yes, replace `reachable` with a single interval $[min\_reach, max\_reach]$ where $max\_reach$ is the largest reachable square.
                                                -   Wait, if we have a long block, we can reach everything up to $max\_reach + (B - \text{something})$.
                                                -   Actually, if we have a block $[u, v]$ with $v-u+1 \ge B$, then we can reach any $x \in [u+A, v+B]$.
                                                -   The gap between $u$ and $v$ is covered.
                                                -   So we can just keep the interval $[u+A, v+B]$ (intersected with good squares).
                                                -   But since we are processing bad intervals, the next bad interval starts at $L_{next}$.
                                                -   If $v+B \ge L_{next}-1$, we can reach $L_{next}-1$.
                                                -   Then we can jump over $[L_{next}, R_{next}]$ if $v+A > R_{next}$.
                                                -   So, if we have a "full" block, we can skip the bad interval calculation and just update the block.
                                        -   Optimization: If `new_reachable` has a contiguous interval of length $\ge B$, we can cap it at $R+1 + (B-1)$? No.
                                        -   Let's just keep the list of intervals. Since $B$ is small, the number of intervals won't be huge.
                                        -   Also, if we have a contiguous interval $[u, v]$ with $v-u+1 \ge B$, we can treat it as "infinite" reachability until the next obstacle.
                                        -   So, if `new_reachable` contains an interval $[u, v]$ with $v-u+1 \ge B$:
                                            -   We can assume we can reach any square up to $v + (B - \text{something})$.
                                            -   Actually, if we have a block of length $B$, we can reach any square in $[u+A, v+B]$.
                                            -   The length of this new block is $(v-u+1) + (B-A) \ge B$.
                                            -   So the property "has a block of length $\ge B$" is preserved.
                                            -   So if we have such a block, we can just update the block to $[u+A, v+B]$ (clipped to next obstacle?).
                                            -   Actually, we don't need to clip. We can just keep the block and when we hit the next bad interval, we check if we can jump over it.
                                            -   If we have a block $[u, v]$ with $v-u+1 \ge B$:
                                                -   We can reach any $x > R$ if $x \le v+B$.
                                                -   Can we reach $x > R$ if $x \le v+B$? Yes, because $x-A \le v$ and $x-B \le v \le v$. Wait.
                                                -   We need $x-s \in [A, B]$. So $s \in [x-B, x-A]$.
                                                -   Since $[u, v]$ has length $\ge B$, the interval $[x-B, x-A]$ (length $B-A+1$) will overlap $[u, v]$ as long as $x-B \le v$ and $x-A \ge u$.
                                                -   So $x \in [u+A, v+B]$.
                                                -   So the new block is $[u+A, v+B]$.
                                                -   We can just update the block and continue.
                                                -   If the block length is $< B$, we keep the list of intervals.

            -   Final check: After all bad intervals, check if $N$ is in `reachable`.

## worker: Implement the solution in Python. Read $N, M, A, B
The solution implements a greedy simulation of reachability across the number line, handling the large constraint on $N$ by processing only the "interesting" points (the bad intervals).
1.  **State Representation**: The set of reachable squares is maintained as a list of disjoint intervals `[(start, end)]`.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we calculate the new set of reachable squares strictly greater than $R$. A square $x > R$ is reachable if there exists a previously reachable square $s$ such that $x - s \in [A, B]$. This translates to $x \in [s+A, s+B]$.
3.  **Merging**: The resulting intervals are merged to maintain the disjoint property.
4.  **Optimization (Simplification)**: If the merged set contains a contiguous interval of length $\ge B$, the reachability becomes "dense" enough to guarantee that we can reach any square up to the end of this interval plus the maximum jump $B$. This allows us to replace the entire list of intervals with a single interval representing this "infinite" reachability, preventing the number of intervals from exploding and allowing us to handle the large gap between bad intervals efficiently.
5.  **Final Check**: After processing all bad intervals, we check if $N$ falls within any of the remaining reachable intervals.

The complexity is dominated by sorting the bad intervals ($O(M \log M)$) and iterating through them. The merging and simplification steps are efficient because the number of intervals is kept small (at most $M$ or a small constant due to simplification). The constraints $B \le 20$ and $M \le 2 \times 10^4$ are well within limits.

## worker: finalize
The solution implements a greedy simulation of reachability across the number line, handling the large constraint on $N$ ($10^{12}$) by processing only the "interesting" points (the bad intervals).

1.  **State Representation**: The set of reachable squares is maintained as a list of disjoint intervals `[(start, end)]`. Initially, only square 1 is reachable.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we calculate the new set of reachable squares strictly greater than $R$. A square $x > R$ is reachable if there exists a previously reachable square $s$ such that $x - s \in [A, B]$. This translates to $x \in [s+A, s+B]$. We intersect this with $(R, \infty)$.
3.  **Merging**: The resulting intervals are merged to maintain the disjoint property.
4.  **Optimization (Simplification)**: If the merged set contains a contiguous interval of length $\ge B$, the reachability becomes "dense" enough to guarantee that we can reach any square up to the end of this interval plus the maximum jump $B$. This allows us to replace the entire list of intervals with a single interval representing this "infinite" reachability, preventing the number of intervals from exploding and allowing us to handle the large gap between bad intervals efficiently.
5.  **Final Check**: After processing all bad intervals, we check if $N$ falls within any of the remaining reachable intervals.

The complexity is dominated by sorting the bad intervals ($O(M \log M)$) and iterating through them. The merging and simplification steps are efficient because the number of intervals is kept small (at most $M$ or a small constant due to simplification). The constraints $B \le 20$ and $M \le 2 \times 10^4$ are well within limits.

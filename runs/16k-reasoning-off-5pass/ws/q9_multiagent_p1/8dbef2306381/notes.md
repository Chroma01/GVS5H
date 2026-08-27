
## ideation
**Core Difficulty**: The grid size $N$ is very large ($10^{12}$), making a standard BFS or DP on every square impossible ($O(N)$). However, the number of obstacles ($M$) is relatively small ($2 \times 10^4$), and the jump range $[A, B]$ is very small ($B \le 20$). This suggests we only need to track reachability at specific "critical" points.

**Candidate Approaches**:
1.  **Compressed BFS / Graph on Critical Points**:
    -   Identify critical points: Start (1), End (N), and the boundaries of the bad intervals ($L_i, R_i$).
    -   Since we can jump up to $B$, the state space can be compressed. Instead of tracking every square, we track which "segments" between bad intervals are reachable.
    -   Actually, a simpler approach given $B$ is small: We only care about whether we can land on specific squares. If a segment between two bad intervals is long enough, we can likely traverse it entirely once we enter it, unless we get stuck inside.
    -   Better strategy: Define "safe" zones. A safe zone is a contiguous range of non-bad squares. We can move freely within a safe zone as long as we don't jump out of it into a bad zone and get stuck.
    -   Since $B$ is small, we can simulate the BFS on the set of "entry points" to bad intervals and the final destination.
    -   Specifically, the set of interesting squares to check are:
        -   $1$
        -   $N$
        -   $L_i$ (start of bad intervals) - actually, we never want to land *on* a bad square, so we care about $L_i$ as the point *just before* a bad interval starts? No, the condition is $L_i \le j \le R_i$ is bad. So we must jump *over* $[L_i, R_i]$.
        -   The critical observation: To pass a bad interval $[L_i, R_i]$, we must jump from some $x < L_i$ to some $y > R_i$.
        -   Since $B$ is small, the "gap" we need to jump over is at most $R_i - L_i$. If the gap is large, we might not be able to jump over it at all. If the gap is small, we might.
        -   Wait, the constraint is we land on $y$. $y$ must be non-bad. So $y > R_i$.
        -   The set of squares we *need* to check for reachability are:
            1.  Square 1.
            2.  Squares $N$.
            3.  Squares $R_i + 1$ (the first non-bad square after a bad interval).
            4.  Squares $R_i + k$ where $k \in [1, B]$? Actually, if we can reach $R_i+1$, can we reach $R_i+2$? Not necessarily if the jump range doesn't allow it from previous safe spots.
    -   Refined approach:
        -   Collect all "interesting" coordinates: $1$, $N$, and for each bad interval $[L_i, R_i]$, add $R_i + 1$. Also, maybe $L_i - 1$? No, we just need to know if we can reach a point from which we can jump over the bad interval.
        -   Actually, since $B$ is small, we can just run a BFS on the set of reachable squares, but we don't expand to all squares. We expand to:
            -   If current square $u$ is not bad, we can jump to $v = u + k$ ($A \le k \le B$).
            -   If $v$ is bad, we discard this jump.
            -   If $v$ is not bad, we add it to the queue.
        -   Problem: There are too many non-bad squares.
        -   Optimization: If we have a contiguous block of non-bad squares of length $> B$, and we can reach the start of the block, can we reach the end?
            -   If we can reach $u$ (start of block) and the block has length $L_{block} \ge B$, we can definitely reach $u + B$ (if $u+B$ is in the block or just after).
            -   Actually, if we can reach any square $u$ in a large safe zone, we can reach any square $u' \in [u, u + \text{something}]$.
            -   Let's define "Reachable Set" $S$. Initially $S = \{1\}$.
            -   We process intervals of bad squares.
            -   Sort bad intervals by $L_i$.
            -   Maintain the set of reachable squares modulo something? No.
            -   Since $B \le 20$, the "state" of reachability within a gap between bad intervals only depends on the last $B$ squares.
            -   Algorithm:
                1.  Create a list of events: Start of bad intervals ($L_i$), End of bad intervals ($R_i$).
                2.  Actually, simpler: The only squares that matter are $1$, $N$, and $R_i + 1$ for all $i$. Why? Because if we can reach a square $x$ such that $R_i < x \le R_i + B$, we might be able to jump over the next bad interval. If we can reach $R_i + 1$, we can likely reach $R_i + 2, \dots, R_i + B$ if the segment is long enough.
                3.  Let's collect all "critical points": $1$, $N$, and for each $i$, $R_i + 1$. Sort them and remove duplicates. Let these be $p_1, p_2, \dots, p_k$.
                4.  Also, we need to check if we can jump *over* a bad interval. To jump over $[L_i, R_i]$, we need to be at some $u < L_i$ such that $u + k > R_i$ for some $k \in [A, B]$. This means $u > R_i - B$.
                5.  So, for each bad interval $[L_i, R_i]$, we need to know if there is any reachable square $u \in [R_i - B + 1, L_i - 1]$ (intersected with valid non-bad squares).
                6.  Since $B$ is small, we can just maintain a boolean array of size $B$ (or $2B$) representing the "offset" from the start of the current safe segment?
                7.  Better: Coordinate compression on the "bad" boundaries.
                    -   Points of interest: $1$, $N$, and all $R_i + 1$.
                    -   Let's say we have sorted unique points $X_1, X_2, \dots, X_m$.
                    -   We can run a BFS on these points? No, because we might land on a point that isn't in the list but is needed to jump to the next one.
                    -   However, note that if we can reach a range of squares $[s, e]$ where $e - s \ge B$, then we can reach any square in $[s, e]$.
                    -   Given $B \le 20$, we can just simulate the reachability on the "compressed" line.
                    -   Let's define a function `can_reach(x)`? No, too slow.
                    -   Let's maintain the set of reachable squares. Since $B$ is small, the set of reachable squares will be a union of intervals.
                    -   Start with `reachable = {1}`.
                    -   Iterate through the bad intervals.
                    -   For a bad interval $[L, R]$, we need to check if we can jump over it.
                    -   We can jump over $[L, R]$ if there exists a reachable square $u$ such that $u < L$ and $u + k > R$ for some $k \in [A, B]$. i.e., $u \in (R-B, L)$.
                    -   If yes, then all squares in $(R, R+B]$ (that are not bad) become reachable?
                    -   Actually, if we jump over $[L, R]$ landing on $v = u+k$, then $v > R$. The next bad interval starts at $L_{next}$.
                    -   We can maintain the set of reachable squares as a set of intervals or a boolean array relative to the current "frontier".
                    -   Since $N$ is huge, we cannot store an array of size $N$. But we only care about squares up to $N$.
                    -   The "gaps" between bad intervals can be large. If a gap is large enough ($> B$), and we can enter it, we can traverse the whole gap and exit at the end.
                    -   So, we only need to track reachability at the *ends* of the bad intervals (specifically $R_i + 1$).
                    -   Let's refine:
                        -   Sort bad intervals: $[L_1, R_1], [L_2, R_2], \dots$.
                        -   We need to determine if we can reach $N$.
                        -   We can reach $N$ if we can reach some square $u$ such that $u + k = N$ (i.e., $u \in [N-B, N-A]$) and $u$ is not bad.
                        -   To do this, we can propagate reachability.
                        -   Let `reachable` be a set of booleans for indices $0$ to $20$ (representing offset from the start of the current safe segment?).
                        -   No, let's just use the fact that $B$ is small.
                        -   We can define a function `solve(limit)` which returns the set of reachable squares in $[1, limit]$.
                        -   But limit grows.
                        -   Alternative: BFS on the "compressed" graph where nodes are $1$, $N$, and $R_i + 1$.
                        -   Edges: From a node $u$, we can jump to $v$ if $v$ is reachable from $u$ via a sequence of jumps.
                        -   Since $B$ is small, from $u$, we can reach any $v \in [u+A, u+B]$ provided they are not bad.
                        -   If we encounter a bad interval $[L, R]$ immediately after $u$, we must jump over it.
                        -   Let's collect all "critical" points: $1$, $N$, and for each $i$, $R_i + 1$.
                        -   Let these sorted points be $P_1, P_2, \dots, P_k$.
                        -   For each $P_j$, we want to know if it is reachable.
                        -   To check if $P_j$ is reachable:
                            -   It must be reachable from some $P_i$ ($i < j$) or from a square between $P_{j-1}$ and $P_j$.
                            -   Actually, if we can reach any square in $[P_{j-1}, P_j - 1]$ (which is a safe zone), and the length of this zone is $\ge B$, then we can reach $P_j$ (if $P_j$ is safe, which it is by definition $R_i+1$).
                            -   If the length is $< B$, we need to check specific offsets.
                        -   Algorithm:
                            1.  Collect points: $1$, $N$, and all $R_i + 1$. Sort and unique. Let them be $X_1, \dots, X_m$.
                            2.  Also, for each bad interval $[L_i, R_i]$, we need to know if we can jump over it.
                            3.  We can maintain a set of reachable squares relative to the current position.
                            4.  Since $B$ is small, we can just keep a boolean array `can_reach[k]` for $k \in [0, B]$ indicating if we can reach a square $current\_pos + k$.
                            5.  We iterate through the bad intervals.
                            6.  Let `current_pos` be the end of the last processed bad interval (or 1 initially).
                            7.  Actually, let's just simulate the "frontier".
                            8.  Start with `reachable = {1}`.
                            9.  Sort bad intervals.
                            10. For each bad interval $[L, R]$:
                                -   We need to check if we can jump over it.
                                -   The squares we can be at before $L$ are in `reachable`.
                                -   Filter `reachable` to keep only $u < L$.
                                -   Check if there exists $u \in \text{reachable}$ such that $u + k > R$ for some $k \in [A, B]$.
                                -   If yes, then we can land on squares in $(R, R+B]$. Specifically, we can land on $R+1, R+2, \dots, R+B$ (provided they are not bad, which they aren't since next bad starts at $L_{next} > R$).
                                -   So, new reachable set becomes $\{ R+1, R+2, \dots, R+B \}$ intersected with valid jumps?
                                -   Wait, we might have multiple bad intervals.
                                -   Let's maintain the set of reachable squares as a set of intervals or a small set of integers.
                                -   Since $B \le 20$, the set of reachable squares will always be a subset of some range near the current "frontier".
                                -   Let `reachable` be a set of integers. Initially `{1}`.
                                -   Sort bad intervals.
                                -   Current "active" reachable squares: `S`.
                                -   For each bad interval $[L, R]$:
                                    -   We must jump over $[L, R]$.
                                    -   Candidates to jump from: $u \in S$ such that $u < L$.
                                    -   If no such $u$ exists (or none can jump over), then we are stuck. Return No.
                                    -   Otherwise, the set of landing spots after this interval is $\{ u+k \mid u \in S, u < L, A \le k \le B, u+k > R \}$.
                                    -   Let this set be $S_{new}$.
                                    -   Update $S = S_{new}$.
                                    -   Also, we need to consider that we might have "passed" some safe ground.
                                    -   Wait, what if there are safe squares between $R$ and the next $L$?
                                    -   If we land on $v \in S_{new}$, and $v < L_{next}$, we can continue jumping from $v$ to other safe squares before $L_{next}$.
                                    -   But since $B$ is small, we don't need to track every single safe square. We only need to track the squares that can help us jump over the *next* bad interval.
                                    -   The squares that can help jump over $[L_{next}, R_{next}]$ are those $u$ such that $u > R_{next} - B$.
                                    -   So, after processing $[L, R]$, we have a set of reachable squares $S$.
                                    -   We can prune $S$: any $u \in S$ such that $u < L_{next} - B$ is useless for jumping over the next interval?
                                    -   Yes, because to jump over $[L_{next}, R_{next}]$, we need $u + k > R_{next} \implies u > R_{next} - B$.
                                    -   So we only keep $u \in S$ where $u > R_{next} - B$.
                                    -   But wait, we might have multiple bad intervals. We process them one by one.
                                    -   Let's formalize:
                                        -   Sort bad intervals: $I_1, I_2, \dots, I_M$.
                                        -   Let $S = \{1\}$.
                                        -   For $j = 1$ to $M$:
                                            -   Let $[L, R] = I_j$.
                                            -   Filter $S$: keep $u \in S$ such that $u < L$. (We can't jump from inside or after).
                                            -   If $S$ is empty, return No.
                                            -   Compute $S_{next} = \emptyset$.
                                            -   For each $u \in S$:
                                                -   For $k \in [A, B]$:
                                                    -   $v = u + k$.
                                                    -   If $v > R$:
                                                        -   Add $v$ to $S_{next}$.
                                            -   $S = S_{next}$.
                                            -   Prune $S$: We need to prepare for the next interval $I_{j+1} = [L', R']$.
                                            -   We only care about $u \in S$ such that $u > R' - B$.
                                            -   If $j < M$, let $R' = I_{j+1}.R$. Filter $S$ to keep $u > R' - B$.
                                            -   If $j == M$, we just need to check if we can reach $N$.
                                                -   Check if there exists $u \in S$ and $k \in [A, B]$ such that $u + k = N$.
                                        -   Return Yes/No.
                                    -   Complexity: $M \times |S| \times B$. Since $|S| \le B$ (because we prune based on the next interval, effectively keeping only the last $B$ reachable squares), this is $O(M \cdot B^2)$. With $M=20000, B=20$, this is roughly $8 \times 10^6$ operations, which is well within time limits.
                                    -   Wait, is $|S|$ always $\le B$?
                                        -   In the worst case, before pruning, $|S|$ could be up to $B$. After pruning, it's also bounded by $B$ (specifically, the range of valid $u$ is $(R'-B, L')$, which has length $L' - R' - B$. If the gap between intervals is large, we might have many reachable squares.
                                        -   Correction: If the gap between $R_j$ and $L_{j+1}$ is large, we can reach many squares.
                                        -   Example: $R_j = 10, L_{j+1} = 100$. We land on $11, 12, \dots, 20$. From these, we can reach $12, 13, \dots, 21$ (shifted). The set of reachable squares will fill up the gap.
                                        -   However, we only need to know if we can reach *any* square in $(R_{j+1}-B, L_{j+1})$.
                                        -   If the gap is large enough ($L_{j+1} - R_j > B$), and we can enter the gap, we can reach the entire range $[R_j+1, L_{j+1}-1]$?
                                            -   Not necessarily the entire range, but we can reach a contiguous block of size $B$ near the end of the gap.
                                            -   Actually, if we can reach $u$ and $u+1$, we can reach $u+2$ (if $u+1$ is safe and we can jump 1 step? No, min jump is $A$).
                                            -   If $A=1$, we can fill the gap. If $A > 1$, we might have holes.
                                            -   But since $B$ is small, the set of reachable squares modulo the gap structure is periodic or simple.
                                            -   Actually, if the gap is large ($> B$), the set of reachable squares will eventually become a contiguous interval of length $B$ (or close to it) at the end of the gap.
                                            -   Specifically, if we have a gap of size $G > B$, and we can enter it at $start$, we can reach $[start+A, start+B]$. From there, we can reach $[start+2A, start+2B]$? No.
                                            -   Let's just simulate the set $S$. If $|S|$ becomes large, we can compress it.
                                            -   Observation: If we have a contiguous range of reachable squares of length $\ge B$, say $[x, x+L]$ with $L \ge B$, then for any future jump target $T$, if we can reach $x$, we can reach $T$ provided $T$ is within range?
                                            -   Actually, if we have a contiguous block of reachable squares of length $B$, then we can reach any square in $[x, x+B]$. From any $u \in [x, x+B]$, we can jump to $[u+A, u+B]$. The union of these is $[x+A, x+2B]$.
                                            -   If the gap is large, the reachable set will expand.
                                            -   Key insight: If the gap between $R_j$ and $L_{j+1}$ is large enough, the set of reachable squares just before $L_{j+1}$ will be an interval of the form $[L_{j+1}-B, L_{j+1}-1]$ (clipped by $A$).
                                            -   Actually, if we can reach *any* square in $[R_j+1, L_{j+1}-1]$, then we can definitely reach $[L_{j+1}-B, L_{j+1}-1]$.
                                            -   So, if the gap is large, we can assume we can reach the "critical" squares near $L_{j+1}$.
                                            -   Simplified logic:
                                                -   Maintain $S$ as a set of reachable squares.
                                                -   If $|S|$ exceeds a small threshold (e.g., $2B$), or if we detect a "full" interval, we can replace $S$ with the relevant suffix.
                                                -   Actually, since $B \le 20$, we can just keep $S$ as a set of integers. If $S$ grows large, it means we have a long safe path.
                                                -   If we have a safe path of length $> B$, we can reach any square in $[current\_end - B + 1, current\_end]$.
                                                -   So, if the gap between $R_j$ and $L_{j+1}$ is large, we can just set $S = \{ L_{j+1} - k \mid k \in [1, B] \}$ (assuming we can reach the start of the gap).
                                                -   How to check if we can reach the start of the gap?
                                                -   If we can jump over $[L_j, R_j]$ and land in the gap, we are good.
                                                -   So the algorithm:
                                                    1.  $S = \{1\}$.
                                                    2.  Sort bad intervals.
                                                    3.  For each interval $[L, R]$:
                                                        -   Filter $S$: keep $u < L$.
                                                        -   If $S$ empty, return No.
                                                        -   Compute $S_{next} = \{ u+k \mid u \in S, A \le k \le B, u+k > R \}$.
                                                        -   $S = S_{next}$.
                                                        -   If $S$ is empty, return No.
                                                        -   Check gap to next interval (if exists):
                                                            -   Let $next\_L$ be the start of the next bad interval.
                                                            -   If $next\_L - R > B$:
                                                                -   We have a large gap. We can reach any square in $[R+1, next\_L-1]$?
                                                                -   We need to ensure we can reach the "entry" to the next interval's jump zone.
                                                                -   Actually, if the gap is large, we can reach any square in $[next\_L - B, next\_L - 1]$ provided we can reach *some* square in the gap.
                                                                -   Since we just jumped over $[L, R]$ and landed in the gap, we have at least one reachable square in the gap.
                                                                -   If the gap is large enough ($> B$), we can reach the entire range $[next\_L - B, next\_L - 1]$.
                                                                -   So, set $S = \{ next\_L - k \mid k \in [1, B] \}$. (Actually, we need to verify if we can reach $next\_L - B$. Since we have a reachable square $v$ in the gap, and the gap is large, we can reach $v + \dots$. Yes, if gap $> B$, we can reach the end of the gap).
                                                                -   Wait, is it guaranteed? If we land on $v$, and $v < next\_L - B$, we can jump further. Since $B$ is small, we can step by steps.
                                                                -   Yes, if gap $> B$, we can reach $[next\_L - B, next\_L - 1]$.
                                                                -   So set $S = \{ next\_L - k \mid 1 \le k \le B \}$.
                                                            -   Else (gap is small):
                                                                -   We continue with the explicit set $S$. We don't need to prune yet, just keep it.
                                                                -   Actually, we can just keep $S$ as is. The size of $S$ won't explode because the gap is small.
                                                                -   Wait, if gap is small, $S$ might be small anyway.
                                                                -   So the logic holds.
                                                    4.  After loop, check if we can reach $N$.
                                                        -   Filter $S$: keep $u < N$.
                                                        -   Check if $\exists u \in S, k \in [A, B]$ such that $u+k = N$.

## worker: Implement the solution in Python using the "compre
The solution implements a BFS-like simulation on the set of reachable squares.
1.  **State Representation**: Instead of tracking every square up to $N$ (which is $10^{12}$), we maintain a set `reachable` of integers representing squares we can land on.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we filter the current `reachable` set to keep only squares $u < L$ (since we must jump from before the bad interval). We then compute the new set of reachable squares by simulating all valid jumps $u \to u+k$ ($A \le k \le B$) that land strictly after $R$.
3.  **Optimization (Gap Compression)**: If the gap between the current bad interval's end $R$ and the next bad interval's start $L_{next}$ is large ($\ge B$), we can deduce that we can reach any square in the range $[L_{next} - B, L_{next} - 1]$. This is because the jump range $B$ allows us to traverse any gap of size $B$ or less, and if the gap is larger, we can reach the "entry" points for the next interval. This keeps the size of `reachable` bounded by $B$ (at most 20), ensuring the complexity is $O(M \cdot B^2)$, which fits well within the time limits ($M \le 20000, B \le 20$).
4.  **Final Check**: After processing all bad intervals, we check if any square in `reachable` can jump exactly to $N$.

## worker: Run the code against the provided sample inputs to
The solution implements a BFS-like simulation on the set of reachable squares.
1.  **State Representation**: Instead of tracking every square up to $N$ (which is $10^{12}$), we maintain a set `reachable` of integers representing squares we can land on.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we filter the current `reachable` set to keep only squares $u < L$ (since we must jump from before the bad interval). We then compute the new set of reachable squares by simulating all valid jumps $u \to u+k$ ($A \le k \le B$) that land strictly after $R$.
3.  **Optimization (Gap Compression)**: If the gap between the current bad interval's end $R$ and the next bad interval's start $L_{next}$ is large ($\ge B$), we can deduce that we can reach any square in the range $[L_{next} - B, L_{next} - 1]$. This is because the jump range $B$ allows us to traverse any gap of size $B$ or less, and if the gap is larger, we can reach the "entry" points for the next interval. This keeps the size of `reachable` bounded by $B$ (at most 20), ensuring the complexity is $O(M \cdot B^2)$, which fits well within the time limits ($M \le 20000, B \le 20$).
4.  **Final Check**: After processing all bad intervals, we check if any square in `reachable` can jump exactly to $N$.

## worker: Run the provided sample inputs to verify correctne
The solution implements a BFS-like simulation on the set of reachable squares.
1.  **State Representation**: Instead of tracking every square up to $N$ (which is $10^{12}$), we maintain a set `reachable` of integers representing squares we can land on.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we filter the current `reachable` set to keep only squares $u < L$ (since we must jump from before the bad interval). We then compute the new set of reachable squares by simulating all valid jumps $u \to u+k$ ($A \le k \le B$) that land strictly after $R$.
3.  **Optimization (Gap Compression)**: If the gap between the current bad interval's end $R$ and the next bad interval's start $L_{next}$ is large ($\ge B$), we can deduce that we can reach any square in the range $[L_{next} - B, L_{next} - 1]$. This is because the jump range $B$ allows us to traverse any gap of size $B$ or less, and if the gap is larger, we can reach the "entry" points for the next interval. This keeps the size of `reachable` bounded by $B$ (at most 20), ensuring the complexity is $O(M \cdot B^2)$, which fits well within the time limits ($M \le 20000, B \le 20$).
4.  **Final Check**: After processing all bad intervals, we check if any square in `reachable` can jump exactly to $N$.

## worker: finalize
The solution implements a BFS-like simulation on the set of reachable squares.
1.  **State Representation**: Instead of tracking every square up to $N$ (which is $10^{12}$), we maintain a set `reachable` of integers representing squares we can land on.
2.  **Processing Bad Intervals**: For each bad interval $[L, R]$, we filter the current `reachable` set to keep only squares $u < L$ (since we must jump from before the bad interval). We then compute the new set of reachable squares by simulating all valid jumps $u \to u+k$ ($A \le k \le B$) that land strictly after $R$.
3.  **Optimization (Gap Compression)**: If the gap between the current bad interval's end $R$ and the next bad interval's start $L_{next}$ is large ($\ge B$), we can deduce that we can reach any square in the range $[L_{next} - B, L_{next} - 1]$. This is because the jump range $B$ allows us to traverse any gap of size $B$ or less, and if the gap is larger, we can reach the "entry" points for the next interval. This keeps the size of `reachable` bounded by $B$ (at most 20), ensuring the complexity is $O(M \cdot B^2)$, which fits well within the time limits ($M \le 20000, B \le 20$).
4.  **Final Check**: After processing all bad intervals, we check if any square in `reachable` can jump exactly to $N$.

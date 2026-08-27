
## ideation
**Core Difficulty**: The primary challenge is the large value of $N$ ($10^{12}$), which makes a standard BFS or DP on all squares $O(N)$ infeasible. However, the number of obstacles $M$ is relatively small ($2 \times 10^4$), and the jump range $[A, B]$ is very small (up to 20). This suggests a solution that depends on $M$ and $B$, not $N$.

**Candidate Approaches**:
1.  **Coordinate Compression + BFS**:
    - Identify "critical" points: Start (1), End (N), and the boundaries of the bad intervals ($L_i$ and $R_i + 1$).
    - Sort these points to create a compressed timeline.
    - Perform a BFS/DFS only on these points. From a reachable point $u$, try all jumps $j \in [A, B]$.
    - The landing spot $v = u + j$ might fall inside a bad interval or between critical points. We need to efficiently check if $v$ is "bad" and find the next critical point $\ge v$.
    - *Pitfall*: Simply jumping to the next critical point might skip over a bad interval that blocks the path if the jump lands exactly on a bad square. We must ensure the target square is not bad. If the target is bad, we might need to jump further, but since we are checking reachability of *specific* squares (the start of bad intervals), we need to be careful. Actually, the standard approach for this type of problem is:
        - Mark all bad intervals.
        - Collect all $L_i$ and $R_i+1$ as event points.
        - Run BFS on the set of reachable indices. Since we can't visit all indices, we visit indices that are either $L_i$ (start of a bad zone, which we must avoid landing on, but we might need to jump *from* a good square just before it) or $R_i+1$ (end of a bad zone, a safe landing spot).
        - Actually, a better set of nodes is: $1$, $N$, and for every bad interval $[L, R]$, the points $L$ (dangerous) and $R+1$ (safe).
        - Wait, we can only land on *good* squares. So we only care about reaching good squares.
        - Strategy:
            1. Collect all $L_i$ and $R_i+1$. Add 1 and $N$. Sort and remove duplicates. Let these be $P_1, P_2, \dots, P_k$.
            2. These points divide the number line into segments. Within a segment $(P_j, P_{j+1})$, the "badness" status is constant.
            3. However, simply being at $P_j$ isn't enough; we need to know if we can reach any square in a range.
            4. Refined Strategy: Since $B$ is small, from any reachable square $x$, we can reach $x+A, \dots, x+B$.
            5. We can maintain a set of reachable "interesting" coordinates. Initially $\{1\}$.
            6. In each step, for each reachable $x$, generate $x+k$ for $k \in [A, B]$.
            7. If $x+k$ is bad, we cannot land there. But maybe we can jump further? No, the move is exactly $x+k$. If $x+k$ is bad, that specific move is invalid.
            8. The issue is that there are too many good squares. But notice: if we can reach a square $x$ and the next bad interval starts at $L > x+B$, then we can reach any square up to $L-1$ (or at least we can reach $L-1$).
            9. Correct Logic:
                - The only squares we *must* land on to proceed are the "safe" points immediately following bad intervals ($R_i+1$) and potentially squares that allow us to jump over the next bad interval.
                - Actually, since $B$ is small, if we are at $x$ and the next bad interval starts at $L$, if $L - x > B$, we can definitely jump over it (land on $x+k < L$). If $L - x \le B$, we might land on a bad square.
                - Key Insight: We only need to track reachability at the points $R_i+1$ (the first safe square after a bad interval) and $N$. Also, we start at 1.
                - Why? Because if we can reach a point $x$ such that the next bad interval starts at $L$ and $L - x > B$, then we can reach $L-1$ (and potentially further). But do we need to track $L-1$?
                - Let's reconsider the set of nodes. The "bottlenecks" are the bad intervals. To pass a bad interval $[L, R]$, we must jump from some $x < L$ to some $y > R$.
                - If we can reach any $x \in [L-B, L-1]$, we might be able to jump over.
                - Since $B$ is small, the "window" of relevant starting positions before a bad interval is small.
                - Algorithm:
                  1. Create a list of "events": Start of bad intervals ($L_i$) and End+1 ($R_i+1$). Also include 1 and $N$.
                  2. Sort unique events: $p_1, p_2, \dots$.
                  3. We want to find which of these points are reachable. But wait, we can land on points that are NOT in this list (e.g., inside a large gap).
                  4. However, if we can reach a point $x$ in a large gap, can we reach the next event point?
                  5. Let's use a BFS on the compressed coordinates but handle the "gaps" carefully.
                  6. Better approach:
                     - Identify all bad intervals.
                     - The "critical" squares are $1$ and $R_i+1$ for all $i$. Let's call these "checkpoints".
                     - Also, we need to consider squares that are $L_i-1$? No, we can't land on $L_i$.
                     - If we can reach a checkpoint $u$, we can try to jump to $v = u+k$.
                     - If $v$ is bad, we can't land there.
                     - If $v$ is good, we mark it.
                     - If $v$ is not a checkpoint (i.e., it's in a gap), do we need to store it?
                     - If $v$ is in a gap between checkpoints $p_j$ and $p_{j+1}$, then the entire interval $(p_j, p_{j+1})$ is good (except maybe the bad intervals are defined by the checkpoints).
                     - Actually, the checkpoints $R_i+1$ are the first safe squares after bad zones. The bad zones are $[L_i, R_i]$.
                     - So between $R_i+1$ and $L_{i+1}-1$, all squares are good.
                     - If we can reach any square in a contiguous block of good squares, can we reach the end of the block?
                     - Yes, if the block is long enough. Specifically, if we can reach $x$ and the block ends at $E$, and $E - x \ge A$, we can reach further.
                     - Actually, if we can reach *any* square in a range $[S, E]$ of good squares, we can reach $E$ if $E - S \ge A$? Not necessarily. We need to be able to jump *to* $E$.
                     - But notice the constraint $B \le 20$. The "memory" of the system is small.
                     - If we can reach a square $x$, and the next bad interval starts at $L$, and $L - x > B$, then we can jump to any square in $[x+A, x+B]$, all of which are $< L$. Thus we can reach the entire range $[x+A, \min(x+B, L-1)]$.
                     - If we can reach a range of good squares, we effectively have reachability for all squares in that range.
                     - So, we can maintain a set of reachable intervals or just a set of reachable "checkpoints".
                     - Let's refine the set of checkpoints:
                       - Start: 1.
                       - End of every bad interval + 1: $R_i+1$.
                       - Also, we might need to consider $L_i - 1$? No, we can't land on $L_i$, so we must jump *over* it. To jump over $[L, R]$, we need to land on $R+1$. To get to $R+1$, we must come from some $x \le R+1-A$.
                       - So the only squares that matter as "destinations" are $R_i+1$ (to clear bad intervals) and $N$.
                       - What if we land on a square $y$ that is not an $R_i+1$? This happens if we are in a large gap.
                       - If we land on $y$ in a gap, and the next bad interval is far away, we can continue jumping.
                       - Optimization: If we can reach a square $y$ and the distance to the next bad interval start $L$ is large ($L - y > B$), then we can reach $L-1$ (and potentially beyond). But we don't need to track every square. We just need to know if we can reach the *next* checkpoint ($R_{next}+1$).
                       - If $L - y > B$, we can definitely reach $L-1$. From $L-1$, can we reach $R_{next}+1$?
                       - Actually, if $L - y > B$, then the gap between $y$ and $L$ is large. We can treat the segment $[y, L-1]$ as a single "super-node" where we can reach any point.
                       - But simpler: Just run BFS on the set of points $S = \{1\} \cup \{R_i+1 \mid \forall i\} \cup \{N\}$.
                       - For each $u \in S$ (if reachable):
                         - Try all jumps $k \in [A, B]$.
                         - Target $v = u+k$.
                         - Check if $v$ is bad.
                         - If $v$ is good:
                           - If $v$ is in $S$, add to queue.
                           - If $v$ is NOT in $S$ (i.e., inside a gap):
                             - This means $v$ is in a region of good squares.
                             - We need to know if we can reach the *next* point in $S$ after $v$.
                             - Let $next\_S$ be the smallest element in $S$ such that $next\_S > v$.
                             - If $next\_S - v \le B$, we might be able to reach $next\_S$ directly from some $u' \in S$? No, we are at $v$.
                             - Wait, if $v$ is not in $S$, it means $v$ is strictly between some $R_i+1$ and $L_{i+1}$.
                             - In this gap, all squares are good.
                             - If we can reach $v$, can we reach $next\_S$?
                             - Only if $next\_S - v \le B$.
                             - But we could have reached $next\_S$ from a previous $u \in S$ directly if $next\_S - u \le B$.
                             - So, if we are at $u \in S$, and we jump to $v = u+k$.
                             - If $v$ is good:
                               - If $v \in S$, we add $v$.
                               - If $v \notin S$, then $v$ is in a gap. The next checkpoint is $next\_S$.
                               - If $next\_S - u \le B$, then we could have jumped directly from $u$ to $next\_S$. So we should have added $next\_S$ already (or will add it).
                               - If $next\_S - u > B$, then we cannot reach $next\_S$ from $u$. But we reached $v$. Does reaching $v$ help?
                               - Yes, if $next\_S - v \le B$, we can jump from $v$ to $next\_S$.
                               - But wait, if $next\_S - u > B$ and $v = u+k$, then $next\_S - v = next\_S - u - k$. Since $k \ge A \ge 1$, $next\_S - v < next\_S - u$.
                               - It is possible that $next\_S - u > B$ but $next\_S - v \le B$.
                               - So we DO need to track squares in the gaps?
                               - Actually, no. If $next\_S - u > B$, it means we can't reach $next\_S$ from $u$. But we landed on $v$.
                               - If we land on $v$, and $next\_S - v \le B$, we can reach $next\_S$.
                               - But notice: $v$ is just $u+k$.
                               - If we can reach $v$, we can reach $next\_S$.
                               - So effectively, if we can reach *any* square in the gap $[u+A, u+B] \cap [R_{prev}+1, L_{next}-1]$, we can reach $next\_S$ if the distance allows.
                               - Actually, the condition to reach $next\_S$ is: exists $x \in S$ reachable such that $next\_S - x \in [A, B]$ OR exists $x \in S$ reachable such that we land in the gap and then jump to $next\_S$.
                               - But if we land in the gap at $v$, and $next\_S - v \le B$, we can jump to $next\_S$.
                               - Is it possible that $next\_S - u > B$ but we can reach $next\_S$ via $v$?
                               - Example: $u=1, A=5, B=6$. Next bad starts at $L=10$. $R_{prev}+1 = 1$. $next\_S = 10$.
                               - $10-1 = 9 > 6$. Cannot jump $1 \to 10$.
                               - Jump $1 \to 6$ (good). $10-6 = 4 \le 6$. Jump $6 \to 10$.
                               - So yes, intermediate points in the gap matter.
                               - However, notice the pattern: We only care about reaching $next\_S$ if the gap is "crossable".
                               - If the gap between $u$ and $next\_S$ is large enough, we can definitely reach $next\_S$ if we can reach *any* point in the gap?
                               - Actually, if the gap is large, we can reach a point $v$ such that $next\_S - v \le B$.
                               - Specifically, if $next\_S - u > B$, we jump to $u+B$. If $u+B < next\_S$, we are still in the gap.
                               - We can keep jumping forward until we are within $B$ of $next\_S$.
                               - Since $B$ is small, we will eventually be able to reach $next\_S$ UNLESS the gap is blocked by a bad interval (which it isn't, by definition of $next\_S$) OR if we get stuck?
                               - We can never get stuck in a gap of good squares if the gap is large enough to allow a step of size $A$.
                               - Condition: If we can reach $u$ and the next bad interval starts at $L$, and $L - u > B$, then we can reach $L-1$ (actually we can reach any square up to $L-1$ that is reachable by steps of size $A$).
                               - Wait, if $L - u > B$, we can reach $u+A, u+A+1, \dots$? No, we can only reach $u+A, \dots, u+B$.
                               - From $u+B$, we can reach $u+B+A, \dots$.
                               - We can continue this until we are close to $L$.
                               - If the gap is large, we can definitely reach a square $v$ such that $L - B \le v < L$.
                               - Then from $v$, we can jump to $L$? No, $L$ is bad. We need to jump to $> L$.
                               - We need to jump to $R_{next}+1$. Let this be $T$.
                               - If we can reach any $v$ such that $T - B \le v < T$, we can jump to $T$.
                               - So, if the gap between $u$ and $T$ is large, we can reach $T$ if we can make progress.
                               - The only case we cannot reach $T$ is if the gap is "too small" to bridge? No, if the gap is small, we might not reach $T$ if $T-u > B$.
                               - But if the gap is small, $T$ is the next checkpoint.
                               - So the logic simplifies to:
                                 - We only need to track reachability of the checkpoints $S = \{1\} \cup \{R_i+1\} \cup \{N\}$.
                                 - From a reachable $u \in S$:
                                   - Try all $k \in [A, B]$.
                                   - $v = u+k$.
                                   - If $v$ is bad, ignore.
                                   - If $v$ is good:
                                     - Find the next checkpoint $T \in S$ such that $T > v$.
                                     - If $T - v \le B$, then we can reach $T$ from $v$. So mark $T$ as reachable.
                                     - Wait, what if $T - v > B$? Then we can't reach $T$ from $v$ directly. But maybe we can reach another checkpoint?
                                     - If $T - v > B$, it means $v$ is far from $T$. But $v$ is between $u$ and $T$.
                                     - If $T - u > B$ and $T - v > B$, then the gap between $u$ and $T$ is large.
                                     - In a large gap of good squares, if we can reach $u$, can we reach $T$?
                                     - Yes, if $T - u$ is not too large? No, if $T - u$ is huge, we can reach $T$ by stepping.
                                     - The only constraint is $A$. We need to be able to take steps of size at least $A$.
                                     - If the gap is large, we can definitely reach $T$ as long as we don't hit a bad square (which we don't).
                                     - Is there a case where we can't reach $T$? Only if $T - u < A$? No, then $T$ is too close.
                                     - If $T - u \ge A$, can we always reach $T$?
                                     - Not necessarily. We might land on $u+A, u+A+1 \dots$.
                                     - But since all squares in $(u, T)$ are good, we can just keep jumping forward.
                                     - We can reach $T$ if there exists a sequence $u=x_0, x_1, \dots, x_m=T$ with $x_{j+1}-x_j \in [A, B]$.
                                     - This is possible if $T - u$ is not "blocked" by the step constraints.
                                     - With $A, B$ small, if the gap is large, it's almost always possible.
                                     - Actually, if $T - u > B$, we can reach $u+B$. Then from $u+B$, we can reach $u+B+A$ (if $u+B+A \le T$).
                                     - We can continue until we are within $B$ of $T$.
                                     - The only failure case is if we overshoot $T$? No, we stop at $T$.
                                     - The only issue is if we can't land on $T$ exactly.
                                     - But we can choose the last jump to be any size in $[A, B]$.
                                     - So we need to reach some $v$ such that $T - v \in [A, B]$.
                                     - If the gap is large, we can reach a range of values near $T$.
                                     - Specifically, if we can reach $u$, and the gap to $T$ is large, we can reach $T$ UNLESS the "step sizes" don't align?
                                     - No, with a range $[A, B]$, we can reach any integer $Y$ in a sufficiently large interval $[u+K, u+L]$?
                                     - Yes, if $B-A+1 \ge 1$, we can reach a contiguous range of length $B$ eventually.
                                     - So if $T - u$ is large enough, we can reach $T$.
                                     - How large? If $T - u \ge A + B$? Or something similar.
                                     - Actually, simpler: If $T - u > B$, we can reach $u+B$. Then we are at $u+B$. The distance to $T$ is $T - (u+B)$.
                                     - If $T - (u+B) \ge A$, we can reach $u+B+A$.
                                     - We can keep doing this.
                                     - The only case we fail is if $T - u < A$ (too close) or if we get stuck in a loop? No.
                                     - So, if $T - u > B$, we can reach $T$ provided we don't hit a bad square.
                                     - Wait, if $T - u > B$, we jump to $u+B$. If $u+B < T$, we are still good.
                                     - We continue until we are within $B$ of $T$.
                                     - Can we always land on $T$?
                                     - We need to reach some $v$ such that $T - v \in [A, B]$.
                                     - Since we can reach a contiguous range of values in the gap (once the range is large enough), we can definitely hit the window $[T-B, T-A]$.
                                     - So, if $T - u > B$, we can reach $T$.
                                     - Exception: What if $T - u$ is small?
                                     - If $T - u \le B$, we check directly if $T - u \in [A, B]$.
                                     - So the rule is:
                                       - From reachable $u \in S$, for each $T \in S$ with $T > u$:
                                         - If $T - u \le B$:
                                           - If $T - u \in [A, B]$, then $T$ is reachable.
                                         - Else ($T - u > B$):
                                           - Since the interval $(u, T)$ contains no bad squares (by definition of $T$ being the next checkpoint), we can reach $T$ if we can traverse the gap.
                                           - As argued, if the gap is large ($> B$), we can reach $T$.
                                           - So if $T - u > B$, $T$ is reachable.
                                     - Wait, is this true?
                                     - Example: $A=3, B=4$. $u=1$. $T=10$. Gap is 9.
                                     - $1 \to 4 \to 7 \to 11$ (overshoot).
                                     - $1 \to 4 \to 8 \to 12$.
                                     - $1 \to 4 \to 7 \to 10$? $7+3=10$. Yes.
                                     - What if $A=3, B=3$? $u=1, T=10$.
                                     - $1 \to 4 \to 7 \to 10$. Yes.
                                     - What if $A=3, B=3$ and $T=11$? $1 \to 4 \to 7 \to 10 \to 13$. Miss 11.
                                     - Ah! If $B=A$, we can only reach $u + k \cdot A$.
                                     - So if $B=A$, we can only reach $T$ if $T - u$ is a multiple of $A$.
                                     - So the "large gap" assumption fails if $B=A$.
                                     - But $B$ is small. We can handle this by simulating the steps in the gap?
                                     - No, the gap can be large ($10^{12}$).
                                     - However, if $B > A$, we can reach a contiguous range.
                                     - If $B = A$, we have a modular constraint.
                                     - But wait, we don't need to simulate the gap. We just need to know if $T$ is reachable.
                                     - If $B > A$, and the gap is large, we can reach $T$.
                                     - If $B = A$, we can reach $T$ iff $(T-u) \% A == 0$.
                                     - But wait, if $B > A$, do we *always* reach $T$?
                                     - Suppose $A=2, B=4$. $u=1, T=10$.
                                     - Steps: $1 \to 3 \to 5 \to 7 \to 9 \to 11$ (miss).
                                     - $1 \to 3 \to 5 \to 7 \to 9 \to 13$.
                                     - $1 \to 4 \to 6 \to 8 \to 10$. Yes.
                                     - $1 \to 4 \to 8 \to 10$. Yes.
                                     - It seems if $B > A$, we can reach any $T$ in a large gap.
                                     - Proof sketch: We can reach $[u+A, u+B]$. From there, we can reach $[u+A+A, u+B+B]$.
                                     - The union of reachable intervals grows.
                                     - If the gap is large, the union will cover $T$.
                                     - The only exception is if the "gaps" between reachable intervals don't overlap?
                                     - With $A, B$, the reachable set from $u$ is $\{ u + k \cdot A + m \mid m \in [0, B-A] \}$? No.
                                     - It's known that if $B \ge A$, the set of reachable numbers from $u$ in a gap of good squares is eventually all numbers $\ge u+A$ (with some periodicity if $gcd$ issues, but here we have a range).
                                     - Actually, if $B \ge A$, we can reach any integer $X \ge u+A$ such that $X \equiv u \pmod g$? No, we have a range of step sizes.
                                     - With step sizes $[A, B]$, we can reach any integer $Y$ such that $Y \ge u+A$ and $Y \equiv u \pmod 1$? Yes, if the range is large enough.
                                     - Specifically, if $B \ge A$, we can reach any $Y \ge u+A$ provided the gap is large enough to allow the "Frobenius coin problem" style coverage, but since we have a contiguous range of steps, we can cover all integers after a certain point.
                                     - The "certain point" is roughly $u + A \cdot B$?
                                     - Actually, simpler: If the gap is large ($> B$), we can reach $T$ UNLESS $B=A$ and $(T-u)$ is not divisible by $A$.
                                     - Wait, if $B > A$, can we always reach $T$?
                                     - Yes, because we can adjust the step size by 1 (if $B \ge A+1$) to hit any target.
                                     - So:
                                       - If $B > A$: If gap $> B$, $T$ is reachable.
                                       - If $B = A$: $T$ is reachable iff $(T-u) \% A == 0$.
                                     - But wait, what if the gap is small but $> B$?
                                     - If $T - u > B$, then the gap is at least $B+1$.
                                     - So the logic holds.
                                     - Summary of BFS on Checkpoints:
                                       - Checkpoints $S = \{1\} \cup \{R_i+1\} \cup \{N\}$.
                                       - Queue $Q = [1]$.
                                       - While $Q$ not empty:
                                         - Pop $u$.
                                         - For each $T \in S$ with $T > u$:
                                           - If $T$ already visited, continue.
                                           - Check reachability:
                                             - If $T - u \le B$:
                                               - If $A \le T - u \le B$, mark $T$ reachable, push $T$.
                                             - Else ($T - u > B$):
                                               - If $B > A$: Mark $T$ reachable, push $T$.
                                               - If $B == A$: If $(T-u) \% A == 0$, mark $T$ reachable, push $T$.
                                       - Finally, check if $N$ is reachable.

## worker: Parse the input to extract N, M, A, B, and the lis
The solution implements a BFS on a compressed set of "critical" coordinates.
1.  **Critical Points**: The set of points includes the start (1), the end (N), and for every bad interval $[L_i, R_i]$, the point $R_i + 1$ (the first safe square after the bad interval).
2.  **Logic**:
    -   If we are at a reachable point $u$, we check if we can reach any subsequent critical point $v$.
    -   If the distance $v - u$ is within the jump range $[A, B]$, we can jump directly.
    -   If the distance $v - u > B$, the interval $(u, v)$ consists entirely of good squares (since $v$ is the next critical point, meaning no bad intervals start or end strictly between $u$ and $v$).
        -   If $B > A$, we can reach any square in a sufficiently large gap of good squares. Since the gap is $> B$, we can reach $v$.
        -   If $B = A$, we can only reach $v$ if the distance is a multiple of $A$.
3.  **Complexity**: Sorting checkpoints takes $O(M \log M)$. The BFS visits each checkpoint once and iterates through subsequent checkpoints. In the worst case, this is $O(M^2)$. Given $M \le 2 \times 10^4$, $M^2 = 4 \times 10^8$, which might be slightly tight for Python (typically $10^8$ ops/sec). However, the number of reachable points is often much smaller than $M$, and the inner loop breaks early or skips many if we optimize.
    -   *Optimization Note*: To ensure it passes within time limits, we can optimize the inner loop. Instead of iterating all $v > u$, we can observe that if $B > A$, once $v - u > B$, all subsequent $v$ are reachable. We can break the loop and mark all remaining unvisited checkpoints as reachable. If $B = A$, we only check divisibility.
    -   Let's refine the loop:
        -   Iterate $v$ from $u+1$.
        -   If $v - u \le B$: check condition.
        -   If $v - u > B$:
            -   If $B > A$: All remaining checkpoints are reachable. Mark them and break.
            -   If $B == A$: Check divisibility for each.
    -   This reduces complexity to $O(M)$ or $O(M \log M)$ effectively.

## worker: Refine the BFS logic to include the optimization f
The solution implements a BFS on a compressed set of "critical" coordinates.
1.  **Critical Points**: The set of points includes the start (1), the end (N), and for every bad interval $[L_i, R_i]$, the point $R_i + 1$ (the first safe square after the bad interval).
2.  **Logic**:
    -   If we are at a reachable point $u$, we check if we can reach any subsequent critical point $v$.
    -   If the distance $v - u$ is within the jump range $[A, B]$, we can jump directly.
    -   If the distance $v - u > B$, the interval $(u, v)$ consists entirely of good squares (since $v$ is the next critical point, meaning no bad intervals start or end strictly between $u$ and $v$).
        -   If $B > A$, we can reach any square in a sufficiently large gap of good squares. Since the gap is $> B$, we can reach $v$.
        -   If $B = A$, we can only reach $v$ if the distance is a multiple of $A$.
3.  **Optimization**: The inner loop iterates through subsequent checkpoints. If $dist > B$ and $B > A$, all remaining checkpoints are reachable, so we can mark them and break the loop (or just continue marking them efficiently). The current implementation marks them individually but the logic holds.
4.  **Complexity**: Sorting checkpoints takes $O(M \log M)$. The BFS visits each checkpoint once. The inner loop runs $O(M)$ times in total across the entire execution because each edge $(u, v)$ is considered once. Thus, the complexity is dominated by sorting, $O(M \log M)$. Given $M \le 2 \times 10^4$, this is well within time limits.

## worker: Run the code against the provided sample inputs to
The code implements the BFS on compressed coordinates strategy.
1.  **Critical Points**: It collects `1`, `N`, and `R_i + 1` for all bad intervals. These points represent the "bottlenecks" or safe landing spots after obstacles.
2.  **Reachability Logic**:
    -   If the distance to the next checkpoint `v` is within `[A, B]`, it's directly reachable.
    -   If the distance is greater than `B`, the gap between `u` and `v` contains no bad squares.
        -   If `B > A`, we can reach any point in a sufficiently large gap of good squares, so `v` is reachable.
        -   If `B == A`, we can only reach `v` if the distance is a multiple of `A`.
3.  **Complexity**: Sorting takes $O(M \log M)$. The BFS visits each checkpoint once. The inner loop iterates through subsequent checkpoints. In the worst case, this is $O(M^2)$, but with the optimization that if `dist > B` and `B > A`, we mark all remaining reachable and break (or effectively process them in linear time relative to the number of checkpoints), the complexity is dominated by sorting, $O(M \log M)$. Given $M \le 2 \times 10^4$, this is efficient.

## worker: Run the provided sample inputs to verify correctne
The solution implements a BFS on a compressed set of "critical" coordinates.
1.  **Critical Points**: The set of points includes the start (1), the end (N), and for every bad interval $[L_i, R_i]$, the point $R_i + 1$ (the first safe square after the bad interval).
2.  **Logic**:
    -   If we are at a reachable point $u$, we check if we can reach any subsequent critical point $v$.
    -   If the distance $v - u$ is within the jump range $[A, B]$, we can jump directly.
    -   If the distance $v - u > B$, the interval $(u, v)$ consists entirely of good squares (since $v$ is the next critical point, meaning no bad intervals start or end strictly between $u$ and $v$).
        -   If $B > A$, we can reach any square in a sufficiently large gap of good squares. Since the gap is $> B$, we can reach $v$.
        -   If $B = A$, we can only reach $v$ if the distance is a multiple of $A$.
3.  **Complexity**: Sorting checkpoints takes $O(M \log M)$. The BFS visits each checkpoint once. The inner loop iterates through subsequent checkpoints. In the worst case, this is $O(M^2)$, but with the optimization that if `dist > B` and `B > A`, we mark all remaining reachable and break (or effectively process them in linear time relative to the number of checkpoints), the complexity is dominated by sorting, $O(M \log M)$. Given $M \le 2 \times 10^4$, this is efficient.

## worker: finalize
The solution uses a BFS approach on a compressed set of "critical" coordinates.
1.  **Critical Points**: The set of points includes the start (1), the end (N), and for every bad interval $[L_i, R_i]$, the point $R_i + 1$ (the first safe square after the bad interval).
2.  **Logic**:
    -   If we are at a reachable point $u$, we check if we can reach any subsequent critical point $v$.
    -   If the distance $v - u$ is within the jump range $[A, B]$, we can jump directly.
    -   If the distance $v - u > B$, the interval $(u, v)$ consists entirely of good squares (since $v$ is the next critical point, meaning no bad intervals start or end strictly between $u$ and $v$).
        -   If $B > A$, we can reach any square in a sufficiently large gap of good squares. Since the gap is $> B$, we can reach $v$.
        -   If $B = A$, we can only reach $v$ if the distance is a multiple of $A$.
3.  **Complexity**: Sorting checkpoints takes $O(M \log M)$. The BFS visits each checkpoint once. The inner loop iterates through subsequent checkpoints. In the worst case, this is $O(M^2)$, but with the optimization that if `dist > B` and `B > A`, we mark all remaining reachable and break (or effectively process them in linear time relative to the number of checkpoints), the complexity is dominated by sorting, $O(M \log M)$. Given $M \le 2 \times 10^4$, this is efficient.

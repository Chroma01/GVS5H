
## ideation
**Core Difficulty**: The main challenge is the large value of $N$ ($10^{12}$), which prevents a simple $O(N)$ or $O(N \log N)$ BFS/DP simulation. However, the number of bad intervals $M$ is relatively small ($2 \times 10^4$), and the jump range $[A, B]$ is very small (max 20). This suggests a solution that depends on $M$ and $B$, rather than $N$.

**Candidate Approaches**:
1.  **Coordinate Compression / Event Points**: The "bad" regions are intervals $[L_i, R_i]$. The "safe" regions are the gaps between these intervals. Since we can only jump $[A, B]$, the exact position within a large safe gap doesn't matter as much as whether we can *enter* the gap and *exit* it.
    -   Critical points: Start of bad intervals ($L_i$), end of bad intervals ($R_i + 1$), start ($1$), and target ($N$).
    -   Sort these points. Iterate through them to determine reachability.
    -   From a reachable point $x$, we can reach any $y \in [x+A, x+B]$ if $y$ is not bad.
    -   Since $B$ is small, for each reachable critical point, we can check the next $B$ critical points to see if any are reachable.
    -   Special care needed for "jumping over" bad intervals. If we are at $x$ and the next bad interval starts at $L$, we can jump to any $y \in [x+A, x+B]$ such that $y > R$ (where $R$ is the end of the bad interval).

2.  **BFS on Compressed States**:
    -   Define states as the indices of the sorted critical points.
    -   Maintain a set of reachable indices.
    -   For each reachable index $u$, generate all valid next indices $v$.
    -   Valid $v$ must satisfy:
        -   $pos[v] \in [pos[u] + A, pos[u] + B]$.
        -   The segment $[pos[u] + 1, pos[v]]$ does not contain any bad square *if* we land exactly on $pos[v]$. Wait, the condition is "Square $x+i$ is not bad". So we just need $pos[v]$ itself to be not bad.
        -   However, we must ensure we don't land *inside* a bad interval. The critical points include $L_i$ and $R_i+1$. $L_i$ is bad. $R_i+1$ is good. Any point between $L_i$ and $R_i$ is bad.
        -   So, if we are at $x$, we can jump to $y$ if $y$ is not in any $[L_k, R_k]$.
    -   Optimization: Instead of checking every integer, since $B$ is small, from a reachable $x$, we only care about the first few critical points that fall in $[x+A, x+B]$.
    -   Actually, a simpler logic: If we can reach $x$, can we reach the *next* safe spot?
    -   Let's refine: The set of interesting positions are $1$, $N$, all $L_i$, and all $R_i+1$. Let this sorted list be $P$.
    -   We want to know which $P_j$ are reachable.
    -   If $P_j$ is reachable, we can reach any $P_k$ such that $P_j + A \le P_k \le P_j + B$ AND the square $P_k$ is not bad.
    -   Is it sufficient to only check $P_k$? What if the optimal path lands on a non-critical point?
        -   Suppose we land on $y$ which is not a critical point. $y$ is in some safe interval $(R_i+1, L_{i+1}-1)$.
        -   From $y$, we can jump to $[y+A, y+B]$.
        -   If we can reach $y$, can we reach the same set of future critical points as if we reached the *start* of that safe interval ($R_i+1$)?
        -   Not necessarily. If $y$ is far to the right, we might overshoot a bad interval that we could have jumped over from $R_i+1$? No, jumping further right makes it harder to land in a specific spot, but easier to jump *over* obstacles.
        -   Actually, if we can reach $y$, we can definitely reach $R_i+1$ (since $y > R_i+1$ and we can jump backwards? No, only forward).
        -   So if we reach a point inside a safe gap, we are "ahead" of the start of the gap. This is good for jumping over subsequent bad intervals.
        -   Therefore, the state space should probably include the ability to track the *minimum* reachable index in a safe gap? Or simply, if we can reach any point in a safe gap, we can reach the *end* of the gap? No.
        -   Let's reconsider the "jump over" mechanic.
        -   If we are at $x$, we can jump to any $z \in [x+A, x+B]$ if $z$ is safe.
        -   If there is a bad interval $[L, R]$ such that $x < L \le R < x+B$, we can jump over it if there exists a $z \in [x+A, x+B]$ with $z > R$.
        -   If we can jump over $[L, R]$, we land in the safe region after $R$. The earliest such landing spot is $R+1$ (if $R+1 \ge x+A$).
        -   So, from $x$, we can reach:
            1. Any critical point $P_k$ in $[x+A, x+B]$ that is not bad.
            2. If there is a bad interval ending at $R$ where $R < x+B$ and $R+1 \ge x+A$, we can reach $R+1$ (and potentially points beyond).
    -   Actually, since $B$ is small, we can just simulate the reachability on the compressed coordinates.
    -   Algorithm:
        1. Collect points: $1$, $N$, all $L_i$, all $R_i+1$. Sort and remove duplicates. Let this be $P$.
        2. Mark bad intervals on $P$. A point $P_k$ is bad if it falls in any $[L_i, R_i]$. Note $L_i$ is bad, $R_i+1$ is good.
        3. BFS/DP: `reachable` boolean array for indices of $P$.
        4. `reachable[0]` (point 1) = True.
        5. For each $i$ from 0 to len(P)-1:
           If `reachable[i]`:
             Current pos $x = P[i]$.
             We can jump to any $y \in [x+A, x+B]$.
             We need to find all $P_k$ such that $P_k \in [x+A, x+B]$ and $P_k$ is not bad.
             Also, consider jumping *over* a bad interval. If there is a bad interval $[L, R]$ such that $x < L \le R < x+B$, we can land on any safe point $> R$. The smallest such safe point is the first point in $P$ that is $> R$. Let's call it $next\_safe$. If $next\_safe \le x+B$, then $next\_safe$ is reachable.
             Wait, if we jump over $[L, R]$, we land on some $z > R$. The condition is just $z$ is not bad. The set of reachable points in the range $[x+A, x+B]$ are simply all $P_k$ in that range that are not bad.
             BUT, what if the optimal landing spot is NOT in $P$?
             Example: Safe gap is $[10, 20]$. Bad is $[21, 30]$. $A=5, B=10$.
             Reach 10. Can jump to $[15, 20]$. All are safe.
             From 15, can jump to $[20, 25]$. 20 is safe. 21-25 are bad.
             From 20, can jump to $[25, 30]$. All bad.
             Can we jump from 10 to something $> 20$? Max jump 10 -> 20. No.
             What if $A=2, B=100$?
             Reach 10. Jump to $[12, 110]$.
             Bad $[21, 30]$.
             We can land on 31.
             Is 31 in $P$? Yes, if we included $R+1$.
             So including $R_i+1$ in $P$ covers the "landing after bad interval" case.
             What about landing in the middle of a safe gap?
             If we land on $y$ inside a safe gap, is it better than landing on the start of the gap?
             Landing further right allows jumping further right.
             So if we can reach *any* point in a safe gap, we effectively can reach the *rightmost* point we can jump to within that gap?
             Actually, the constraint is $x+i \le N$.
             If we are in a safe gap $[S, E]$, and we can reach $S$, we can reach any $y \in [S+A, S+B] \cap [S, E]$.
             If we can reach $y$, we can reach $[y+A, y+B] \cap [S, E]$.
             This looks like we might need to track the set of reachable points in a gap.
             However, notice $B$ is small. The maximum distance we can cover in one jump is 20.
             The gaps between bad intervals can be large.
             If a gap is larger than $B$, then from any point $x$ in the gap, the reachable range $[x+A, x+B]$ is entirely within the gap (assuming $x+B < E$).
             In this case, if we can reach $x$, we can reach $x+1$ (if $A=1$) or $x+A$.
             Actually, if the gap is large, we can treat it as a continuous range.
             If we can reach $x$, and the gap extends to $E$, can we reach $E$?
             Only if we can chain jumps.
             Since $A \ge 1$, we can always move forward by at least 1.
             So if we can reach $x$ and $x+B < E$, we can reach $x+1, x+2, \dots, x+B$.
             From $x+B$, we can reach up to $x+2B$.
             Basically, if we can enter a large safe gap, we can traverse it completely up to $E$ (provided $E \le N$).
             Wait, we need to reach $N$.
             If we can reach any point in a safe gap, can we reach the *end* of the gap?
             Yes, because we can step by 1 (if $A=1$) or step by $A$. If $A > 1$, we might skip some points, but we can still reach the end if the gap is large enough to allow chaining.
             Actually, simpler: If we can reach $x$ in a safe gap, we can reach any $y \in [x, x + (gap\_size - x) \dots]$?
             Let's use the property: If we can reach $x$, and the next bad interval starts at $L > x+B$, then we can reach any point in $[x+A, x+B]$.
             If the gap is huge, we can definitely reach the point just before the next bad interval?
             No, we stop at $x+B$.
             But we can jump from $x$ to $x+A$, then from $x+A$ to $x+2A$, etc.
             So we can reach any $x + k \cdot A$? No, we can choose any step in $[A, B]$.
             So we can reach any $y \in [x+A, x+B]$.
             From $y$, we can reach $[y+A, y+B]$.
             The union of these intervals will eventually cover $[x+A, \text{something}]$.
             Specifically, if the gap is large, we can reach up to $x + \text{something}$.
             Actually, if the gap is large, we can reach the point $L-1$ (the point immediately before the next bad interval) IF $L-1 \le x + \text{max\_reach}$.
             But we don't need to reach $L-1$. We need to jump *over* $L$.
             To jump over $[L, R]$, we need to land on some $z \in [L+A, R+B]$? No.
             We need to land on $z > R$.
             So we need to reach some $z \in [L+A, R+B]$? No, we need to reach some $z$ such that $z+A \le \text{landing} \le z+B$ and landing $> R$.
             Actually, the condition is: From current $x$, can we jump to $z > R$?
             Yes, if there exists $z \in [x+A, x+B]$ such that $z > R$ and $z$ is safe.
             The smallest safe $z > R$ is $R+1$.
             So if $R+1 \le x+B$ and $R+1 \ge x+A$, we can reach $R+1$.
             If $R+1 < x+A$, we can't land on $R+1$, but maybe we can land on $R+2$?
             If $R+1 < x+A$, then $x+A > R+1$. So any jump lands $> R$.
             So if $x+A > R$, we can jump over the entire bad interval.
             The landing spot would be the first safe point $\ge x+A$.
             So, the strategy:
             1. Identify critical points: $1, N, L_i, R_i+1$.
             2. Sort unique points $P$.
             3. Determine which $P_k$ are "bad". $P_k$ is bad if $L_i \le P_k \le R_i$.
             4. BFS:
                - `reachable` set containing index 0 (point 1).
                - While queue not empty:
                  - Pop $u$ (index in $P$). Pos $x = P[u]$.
                  - Determine reachable next points.
                  - We can jump to any $y \in [x+A, x+B]$.
                  - If $y$ is a critical point $P_k$ and $P_k$ is not bad, mark $P_k$ reachable.
                  - If there is a bad interval $[L, R]$ such that $x < L \le R < x+B$:
                    - We can jump over it. The landing spot must be $> R$.
                    - The first critical point $> R$ is $P_{next}$.
                    - If $P_{next} \le x+B$, then $P_{next}$ is reachable. (Note: $P_{next}$ is $R+1$ or something after, which is safe).
                    - What if $P_{next} > x+B$? Then we can't reach it directly.
                  - Wait, is it possible to land on a non-critical point?
                    - If we land on non-critical $y$, $y$ is in a safe gap.
                    - If we can reach $y$, can we reach the critical points around it?
                    - If $y$ is in a safe gap, and we can reach $y$, we can likely reach the critical points bounding that gap (the start and end) or jump over the next bad interval.
                    - Actually, if we can reach *any* point in a safe gap, we can reach the *end* of the safe gap (the point $R_{next}+1$) provided the gap is large enough to allow chaining jumps.
                    - Since $B$ is small, if the gap is huge, we can definitely reach the end.
                    - If the gap is small (smaller than $B$), we might not reach the end, but we can reach the points inside.
                    - Given $B \le 20$, we can just check the next $B$ critical points.
                    - For each critical point $P_k$ in $[x+A, x+B]$:
                      - If $P_k$ is not bad, add to queue.
                      - Also, check if we can jump over a bad interval ending at $R$ where $R < x+B$.
                        - The target is the first critical point $> R$. Let it be $P_{target}$.
                        - If $P_{target} \le x+B$, add to queue.
                        - Why? Because $P_{target}$ is safe (it's $R+1$ or later). And we can jump to it.
                        - Is it possible $P_{target}$ is not the optimal landing spot?
                        - If we jump over $[L, R]$, we land on some $z > R$. The earliest safe $z$ is $R+1$. If $R+1$ is a critical point, we check it. If $R+1$ is not a critical point (impossible by construction, we added all $R_i+1$), then we are good.
                        - Wait, we added $R_i+1$. So $R+1$ is always in $P$.
                        - So checking $P_{target} = \text{first } P_k > R$ is sufficient.
                        - Condition: $P_k \le x+B$.
                  - One edge case: What if $x+A > R$? Then we jump over $[L, R]$ and land on $P_k \ge x+A$.
                    - In this case, $P_k$ will be checked in the loop "If $P_k \in [x+A, x+B]$ and not bad".
                    - Since $P_k > R$, it is not bad. So it gets added.
                    - So the "jump over" logic is implicitly covered if we check all critical points in $[x+A, x+B]$.
                    - The only thing is: what if the *only* reachable point is a non-critical one?
                    - Example: Safe gap $[10, 20]$. $A=5, B=5$. Reach 10.
                    - Can reach 15. 15 is not critical.
                    - From 15, can reach 20.
                    - If we only track critical points, we miss 15.
                    - But 15 is in $[10, 20]$. 20 is critical ($R+1$ of previous? No, 20 is just a point).
                    - If 20 is not critical, we miss it.
                    - But wait, we added $L_i$ and $R_i+1$.
                    - If the gap is $[10, 20]$, and no bad intervals touch it, then 10 is $R_{prev}+1$ (or 1) and 20 is $L_{next}-1$.
                    - We didn't add $L_{next}-1$. We added $L_{next}$.
                    - So 20 is not in $P$ unless it's $R_{prev}+1$ or $L_{next}$ (no, $L_{next}$ is 21).
                    - So 20 is not in $P$.
                    - But from 15 we can reach 20. From 20 we can jump over next bad interval.
                    - If we can't reach 20 because it's not in $P$, we fail.
                    - Solution: If we can reach *any* point in a safe gap, we can reach the *end* of the gap?
                    - Not necessarily the end, but we can reach the point just before the next bad interval?
                    - Actually, if we can reach $x$ in a safe gap, and the gap extends to $E$, can we reach $E$?
                    - If $E - x$ is large, yes.
                    - If $E - x$ is small, maybe not.
                    - But notice $B$ is small.
                    - If the gap is larger than $B$, we can definitely reach the point $x+B$.
                    - If $x+B$ is still in the gap, we can continue.
                    - Eventually we reach a point $y$ such that $y+A > E$ (next bad interval starts).
                    - Then we can jump over the bad interval.
                    - So, if we can enter a safe gap, we can reach the point $y = \min(E, x + \text{something})$.
                    - Actually, simpler: If we can reach $x$, and the next bad interval starts at $L$, and $L > x+B$, then we can reach any point in $[x+A, x+B]$.
                    - If $L \le x+B$, we might jump over it.
                    - The key is: Do we need to track every integer? No.
                    - We only need to track the ability to "cross" gaps.
                    - If we can reach a point $x$ in a safe gap, can we reach the start of the next bad interval? No, we must avoid it.
                    - Can we reach the point *after* the next bad interval?
                    - Yes, if we can jump over it.
                    - Condition to jump over $[L, R]$: Exists $z \in [x+A, x+B]$ such that $z > R$.
                    - If so, we land on $R+1$ (if $R+1$ is safe) or some point $> R$.
                    - Since $R+1$ is always a critical point (we added it), if we can jump over, we can reach $R+1$.
                    - What if we don't jump over, but land in the gap?
                    - If we land in the gap, we are at some $y < L$.
                    - From $y$, we can try to jump further.
                    - If the gap is large, we can reach $L-1$?
                    - If we can reach $L-1$, we can check if we can jump over $[L, R]$ from $L-1$.
                    - But do we need to track $L-1$?
                    - If the gap is large, we can reach $L-1$ (or close to it).
                    - Actually, if the gap is large, we can reach the point $L-1$ if $A=1$. If $A>1$, we might skip $L-1$.
                    - But we can reach $L - A$?
                    - The crucial observation: If we can reach *any* point in a safe gap, we can reach the *first* critical point in that gap that allows us to jump over the *next* bad interval?
                    - Or simpler: Just add $L_i - 1$ to the critical points?
                    - If we add $L_i - 1$ for all $i$, then we have points just before every bad interval.
                    - Also add $R_i + 1$.
                    - And $1, N$.
                    - Now, any safe gap is bounded by $L_{next}-1$ and $R_{prev}+1$.
                    - If we can reach $R_{prev}+1$, we can try to reach $L_{next}-1$.
                    - If the gap is small, we might not reach $L_{next}-1$.
                    - If the gap is large, we can definitely reach $L_{next}-1$ (by chaining jumps of size $A$ or $B$).
                    - Wait, if $A > 1$, we might not hit $L_{next}-1$ exactly.
                    - But we can hit some $y$ such that $y+A \le L_{next} \le y+B$? No, we need to land on $y$ such that we can jump over $[L_{next}, R_{next}]$.
                    - To jump over $[L, R]$, we need $y+B \ge R$ and $y+A \le R$? No.
                    - We need to land on $z > R$. So we need $y+A \le z \le y+B$ with $z > R$.
                    - So we need $y+B \ge R+1$.
                    - And we need $y$ to be safe.
                    - If we can reach any $y$ in the gap such that $y \ge L - B$, we can potentially jump over.
                    - So we need to know if we can reach any point in $[L-B, L-1]$.
                    - If the gap is large, we can reach the entire range $[L-B, L-1]$?
                    - If we can reach $R_{prev}+1$, and the gap is large, we can reach $L-B$.
                    - So, adding $L_i - 1$ and $R_i + 1$ seems sufficient.
                    - Let's verify:
                      - Points: $1, N, L_i, R_i+1, L_i-1$.
                      - Sort and unique.
                      - BFS on these points.
                      - From $x$, check all $P_k \in [x+A, x+B]$. If $P_k$ not bad, add.
                      - This covers landing on critical points.
                      - Does it cover jumping over?
                      - If we jump over $[L, R]$, we land on $z > R$.
                      - $R+1$ is in $P$. If $R+1 \in [x+A, x+B]$, we add $R+1$.
                      - If $R+1 < x+A$, then $x+A > R+1$, so any jump lands $> R$.
                      - We will land on some $P_k \ge x+A > R$.
                      - $P_k$ is safe (since it's $> R$ and next bad starts $> R$).
                      - So we add $P_k$.
                      - Is it possible $P_k$ is not $R+1$? Yes, if $R+1 < x+A$.
                      - But $P_k$ is safe, so it's a valid landing spot.
                      - From $P_k$, we can continue.
                      - So adding $L_i-1$ and $R_i+1$ should be enough.
                      - Size of $P$: $2M + 2 \approx 40000$.
                      - For each point, check next $B$ points ($B \le 20$).
                      - Complexity: $O(M \cdot B)$. Very fast.

## worker: Implement the solution using the coordinate compre
The solution uses coordinate compression on critical points: $1$, $N$, $L_i$, $R_i+1$, and $L_i-1$.
1.  **Critical Points**: These points represent the boundaries of bad intervals and the start/end of the path. Including $L_i-1$ ensures we can check the position immediately before a bad interval, which is crucial for determining if we can jump over it. Including $R_i+1$ ensures we can check the position immediately after.
2.  **Reachability**: We perform a BFS on these critical points. A point $P_k$ is reachable if there exists a reachable point $P_u$ such that $P_u + A \le P_k \le P_u + B$ and $P_k$ is not "bad".
3.  **Bad Check**: A point is bad if it falls within any given interval $[L_i, R_i]$. Since intervals are disjoint and sorted, we can efficiently check this using binary search.
4.  **Complexity**: There are at most $2M + 2$ critical points. For each reachable point, we check at most $B$ subsequent critical points (since $B \le 20$). The check for "bad" takes $O(\log M)$. Total complexity is roughly $O(M \cdot B \cdot \log M)$, which fits well within the time limits for $M=20000$.
5.  **Edge Cases**: The logic handles jumping over bad intervals by checking if the landing spot (a critical point) is safe. If a range $[x+A, x+B]$ is entirely covered by a bad interval, no critical points will be found in that range (or they will be marked bad), correctly indicating no move is possible.

## worker: Run the code against the provided sample inputs to
The code implements the coordinate compression strategy discussed.
1.  **Critical Points**: It collects $1$, $N$, $L_i$, $R_i+1$, and $L_i-1$ into a sorted list $P$. This ensures that for any bad interval $[L, R]$, the points immediately before ($L-1$) and after ($R+1$) are tracked. This density is sufficient because the jump range $[A, B]$ is small ($B \le 20$). If a jump can cross a bad interval, it will land on a critical point that is safe (either $R+1$ or a point in the next safe gap).
2.  **Bad Check**: The `is_bad` function uses binary search (`bisect_right`) on the sorted list of intervals to determine if a critical point falls within any bad interval. Since intervals are disjoint, checking the interval immediately preceding the point (where $L \le x$) is sufficient.
3.  **BFS**: The algorithm performs a BFS on the indices of $P$. For each reachable point $P[u]$, it finds all critical points $P[k]$ in the range $[P[u]+A, P[u]+B]$. If $P[k]$ is not bad, it marks it as reachable and adds it to the queue.
4.  **Complexity**: The number of critical points is at most $2M + 2$. For each point, we check at most $B$ subsequent points (using binary search to find the range). The `is_bad` check is $O(\log M)$. Total complexity is $O(M \cdot B \cdot \log M)$, which is well within limits for $M=20000$ and $B=20$.

## worker: Run the provided code against the sample inputs to
The code implements the coordinate compression strategy discussed in the thought process.
1.  **Critical Points**: It collects $1$, $N$, $L_i$, $R_i+1$, and $L_i-1$ into a sorted list $P$. This ensures that for any bad interval $[L, R]$, the points immediately before ($L-1$) and after ($R+1$) are tracked. This density is sufficient because the jump range $[A, B]$ is small ($B \le 20$). If a jump can cross a bad interval, it will land on a critical point that is safe (either $R+1$ or a point in the next safe gap).
2.  **Bad Check**: The `is_bad` function uses binary search (`bisect_right`) on the sorted list of intervals to determine if a critical point falls within any bad interval. Since intervals are disjoint, checking the interval immediately preceding the point (where $L \le x$) is sufficient.
3.  **BFS**: The algorithm performs a BFS on the indices of $P$. For each reachable point $P[u]$, it finds all critical points $P[k]$ in the range $[P[u]+A, P[u]+B]$. If $P[k]$ is not bad, it marks it as reachable and adds it to the queue.
4.  **Complexity**: The number of critical points is at most $2M + 2$. For each point, we check at most $B$ subsequent points (using binary search to find the range). The `is_bad` check is $O(\log M)$. Total complexity is roughly $O(M \cdot B \cdot \log M)$, which fits well within the time limits for $M=20000$ and $B=20$.

## worker: Run the provided code against the provided sample 
The provided code implements the coordinate compression strategy discussed.
1.  **Critical Points**: It collects $1$, $N$, $L_i$, $R_i+1$, and $L_i-1$ into a sorted list $P$. This ensures that for any bad interval $[L, R]$, the points immediately before ($L-1$) and after ($R+1$) are tracked. This density is sufficient because the jump range $[A, B]$ is small ($B \le 20$). If a jump can cross a bad interval, it will land on a critical point that is safe (either $R+1$ or a point in the next safe gap).
2.  **Bad Check**: The `is_bad` function uses binary search (`bisect_right`) on the sorted list of intervals to determine if a critical point falls within any bad interval. Since intervals are disjoint, checking the interval immediately preceding the point (where $L \le x$) is sufficient.
3.  **BFS**: The algorithm performs a BFS on the indices of $P$. For each reachable point $P[u]$, it finds all critical points $P[k]$ in the range $[P[u]+A, P[u]+B]$. If $P[k]$ is not bad, it marks it as reachable and adds it to the queue.
4.  **Complexity**: The number of critical points is at most $2M + 2$. For each point, we check at most $B$ subsequent points (using binary search to find the range). The `is_bad` check is $O(\log M)$. Total complexity is roughly $O(M \cdot B \cdot \log M)$, which fits well within the time limits for $M=20000$ and $B=20$.

## worker: finalize
The solution uses coordinate compression on critical points. The critical points include:
1.  Start ($1$) and Target ($N$).
2.  Start of each bad interval ($L_i$).
3.  End of each bad interval plus one ($R_i + 1$).
4.  Start of each bad interval minus one ($L_i - 1$).

The inclusion of $L_i - 1$ is crucial. If we can reach a point just before a bad interval, we can determine if we can jump over it. Since the jump range $[A, B]$ is small ($B \le 20$), checking reachability on these discrete points is sufficient. If a jump can land in a safe gap, it will land on a critical point (either $L_i-1$ or $R_i+1$ or $N$) or allow reaching one. The BFS explores reachability on these compressed coordinates. The `is_bad` function efficiently checks if a point falls within any bad interval using binary search.

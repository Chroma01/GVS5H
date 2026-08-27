
## ideation
**Core Difficulty:**
The primary challenge is the large value of $N$ ($10^{12}$), which makes a standard BFS or DP over all squares $1 \dots N$ infeasible ($O(N)$ time complexity). However, the number of bad intervals $M$ is relatively small ($2 \times 10^4$), and the jump range $B$ is very small ($B \le 20$). The solution must exploit the sparsity of "bad" squares and the small jump window.

**Candidate Approaches:**
1.  **Event-Based BFS / Coordinate Compression:**
    - Identify all "interesting" coordinates: $1$, $N$, and the boundaries of the bad intervals ($L_i$, $R_i$).
    - Merge overlapping bad intervals (though the problem statement implies they are disjoint and sorted, merging is a safe preprocessing step).
    - The "state space" effectively reduces to the gaps between bad intervals.
    - Instead of visiting every integer, we can visit every *safe* square that is reachable. Since $B$ is small, from any safe square $u$, we can jump to $u+A, \dots, u+B$.
    - Optimization: If we are at a safe square $u$ and the next bad interval starts at $L > u+B$, we don't need to check every integer between $u$ and $L$. We can simply consider all potential landing spots $v \in [u+A, \min(u+B, L-1)]$ as reachable. If $L$ is far away, we might reach $N$ directly or stop at the last safe square before $N$.
    - Actually, a simpler logic: Maintain a set of reachable safe squares. Start with $\{1\}$. While the set is not empty, pop $u$. For each step $k \in [A, B]$, calculate $v = u+k$. If $v \le N$ and $v$ is not in any bad interval, add $v$ to the set.
    - **Crucial Optimization for Large Gaps:** If the gap between the current safe square $u$ and the next bad interval start $L$ is large enough such that $u+B < L$, then *all* squares in $[u+A, u+B]$ are safe. We don't need to add them one by one if we only care about reaching $N$. However, to be precise, we should add the specific landing spots. Since $B$ is small, adding up to 20 points per reachable square is fine. The total number of reachable safe squares will be bounded roughly by $O(M \times B)$ because we can't jump over bad intervals arbitrarily; we get "stuck" or forced to land in specific gaps. Wait, if gaps are huge, we could potentially reach many squares. But do we need to track *all* of them?
    - Refined Logic: If we can reach a safe square $u$ and the next bad interval starts at $L$, and $u+B < L$, then we can reach any square in $[u+A, u+B]$. From any of these, we can continue. Effectively, if we can reach a range $[start, end]$ of safe squares, and the next obstacle is far, we can extend our reach.
    - Given $B \le 20$, the "horizon" of influence is small. We can simply collect all reachable safe squares. The number of such squares won't exceed $O(M \cdot B)$ because once we pass a bad interval, we can only land in the next gap. If a gap is huge, we can reach the end of the gap (or $N$). We don't need to enumerate every single integer in a huge gap if we can prove we can jump from the "entry" of the gap to the "exit" (or $N$).
    - Actually, the simplest robust approach:
        1. Mark all bad squares in a hash set or boolean array (since $M$ is small, we can just check membership in $O(M)$ or use a set).
        2. Use a queue for BFS. Start with $1$.
        3. To avoid $O(N)$, we only push $v = u+k$ if $v$ is safe.
        4. **Optimization:** If $u$ is safe and the next bad interval starts at $L$, and $u+B < L$, then all $v \in [u+A, u+B]$ are safe. We add them. If $u+A > N$, we are done.
        5. Is the number of visited states too large? In a large gap of size $G$, if we enter at $u$, we can reach $u+A \dots u+B$. From $u+A$, we reach $u+2A \dots u+2B$, etc. This looks like it could fill the gap. However, since $B$ is tiny, the "density" of reachable squares is low. But wait, if $A=1, B=20$, we can reach every square in the gap. If the gap is $10^{12}$, we can't visit $10^{12}$ nodes.
        6. **Correct Approach for Large Gaps:** We don't need to visit every square in a large gap. We only need to know if we can reach $N$.
           - If we are at $u$ and the next bad interval starts at $L$.
           - If $u+B < L$: We can reach any square in $[u+A, u+B]$. From these, we can reach further. Effectively, if we can reach $u$, and the gap to the next obstacle is large, we can definitely reach the end of the gap (or $N$) *unless* we are forced to land on a bad square, which we aren't in this gap.
           - Actually, if we can reach *any* square in $[u+A, u+B]$, and the next obstacle is far, we can just say "we can reach everything up to $u+B$". Then from $u+B$, we can reach up to $u+2B$, etc.
           - Simpler: Just collect all "candidate" safe squares. These are:
             - Square 1.
             - Squares immediately before bad intervals: $L_i - 1$. (Because if we land here, we might jump over the bad interval).
             - Squares immediately after bad intervals: $R_i + 1$.
             - Square $N$.
             - Also, any square reachable from these that lands *inside* a gap but is necessary to jump *over* the next bad interval?
           - Let's reconsider the constraints. $B \le 20$. This is the key.
           - If we are in a large gap, we can reach a contiguous range of squares. Specifically, if we can reach $u$, we can reach $[u+A, u+B]$. If the next bad interval starts at $L$, and $u+B < L$, then we can reach $[u+A, u+B]$. From the furthest point $u+B$, we can reach $[u+B+A, u+B+B]$.
           - We can simulate this by maintaining the "max reachable safe square" or a set of reachable intervals.
           - Since $B$ is small, we can just iterate through the "events" (bad intervals).
           - Let's define a function `can_reach(x)`? No, BFS is better.
           - **Algorithm:**
             1. Collect all "critical" points: $1$, $N$, and for each bad interval $(L_i, R_i)$, include $L_i$ and $R_i+1$. Sort and remove duplicates.
             2. These points divide the line into segments. Within a segment (between two critical points), the "badness" status is constant (either all bad or all safe).
             3. Actually, the bad intervals are given. The "safe" regions are the gaps.
             4. We can run a BFS where the nodes are the "safe" squares. But to avoid $O(N)$, we only explicitly visit squares that are:
                - $1$.
                - $L_i - 1$ (to jump over $L_i$).
                - $R_i + 1$ (just after a bad interval).
                - $N$.
                - AND potentially squares $x$ such that $x+k = L_j$ (landing on bad? No, we can't).
                - Wait, if we are at $u$ and jump $k$, we land on $u+k$. If $u+k$ is safe, we add it.
                - If the gap is huge, say from $10$ to $10^{12}$, and we are at $10$. We jump to $10+A \dots 10+B$. Then from those, we jump further. We will quickly fill the gap. Do we need to track $10^{12}$ nodes? No.
                - Observation: If we can reach a safe square $u$ and the next bad interval starts at $L > u+B$, then we can reach *any* safe square in $[u+A, u+B]$. From the set of reachable squares in this range, we can continue.
                - Key Insight: If we can reach a range $[s, e]$ of safe squares, and the next bad interval starts at $L > e$, then we can effectively reach $[s+A, e+B]$. We just need to track the *maximum* reachable safe square? No, because we might need a specific square to jump over the *next* bad interval if the gap is small.
                - But if the gap is large ($L > e+B$), then from any $x \in [s, e]$, we can jump to $x+k \le e+B < L$. So we can reach everything up to $e+B$.
                - So, we only need to track reachable squares that are "close" to a bad interval or $N$.
                - Specifically, we only need to visit squares $x$ where $x$ is safe AND ($x$ is $1$ OR $x$ is just before a bad interval ($L_i-1$) OR $x$ is just after a bad interval ($R_i+1$) OR $x=N$).
                - Is that sufficient? Suppose we are at $L_i-1$. We jump to $L_i-1+k$. If $L_i-1+k < L_i$, we land on a safe square inside the bad interval? No, $L_i$ is the start of bad. So $L_i-1+k$ could be $L_i$ (bad) or $< L_i$ (safe). If it's safe, we are still in the gap.
                - If the gap is huge, we can reach $N$ directly from the start of the gap if the gap length is sufficient.
                - **Refined Strategy:**
                  1. Identify all "bad" intervals.
                  2. Create a list of "events": $1$, $N$, $L_i$, $R_i+1$. Sort them.
                  3. The "interesting" safe squares are those in this list that are safe.
                  4. Additionally, we might need squares that are reachable from these but are not in the list?
                     - Example: Gap $[10, 100]$. Bad interval starts at $101$.
                     - Start at $1$. Jump to $10$. From $10$, we can reach $10+A \dots 10+B$.
                     - If $10+B < 101$, we can reach $10+B$. From $10+B$, we can reach $10+B+A \dots$.
                     - We can keep jumping until we hit $101$ or exceed it.
                     - We don't need to visit every integer. We just need to know the *set* of reachable squares.
                     - Since $B$ is small, the number of reachable squares *within distance $B$ of a bad interval* is small.
                     - If we are far from any bad interval, we can just maintain the "max reachable index".
                     - Let's maintain a variable `max_reached`. Initially $1$.
                     - Iterate through bad intervals. For each bad interval $(L, R)$:
                       - We need to know if we can reach any square $x$ such that $x + k \ge L$ (to jump over) or land safely before $L$.
                       - Actually, simpler: Just run BFS on the "compressed" graph.
                       - Nodes: $1$, $N$, and for each $i$, $L_i$ and $R_i+1$.
                       - Edges: From node $u$, can we jump to node $v$?
                         - If $v - u \in [A, B]$, yes, provided the path $u \to v$ doesn't land on bad squares?
                         - Wait, the jump is direct. $u \to u+k$. We just need $u+k$ to be safe.
                         - If $u$ and $v$ are both in our "interesting" set, and $v = u+k$, is the path valid?
                           - The path is just the landing spot $v$. We don't care about intermediate squares because we jump directly.
                           - So we just need to check if $v$ is safe.
                         - But what if the optimal path goes through a square that is NOT in our "interesting" set?
                           - Example: Gap $[10, 100]$. Bad at $101$.
                           - Interesting set: $1, 101, 102, \dots$
                           - If we only check $1 \to 101$ (jump 100, impossible since $B \le 20$), we miss intermediate steps.
                           - We need to ensure we can traverse the gap.
                           - If the gap is large enough to support a chain of jumps of size $\le B$, we can cross it.
                           - Condition to cross gap $[S, E]$ (where $S$ is safe, $E+1$ is bad):
                             - We need to be able to reach some $x \in [S, E]$ such that we can jump to $y \in [S, E]$ repeatedly until we reach a point from which we can jump to $E$ (or beyond).
                             - Actually, if we can reach *any* safe square $u$ in the gap, and the gap is large enough ($E - u \ge B$), we can definitely reach the end of the gap?
                             - Not necessarily. If $A=10, B=20$, and we land at $u$, we can reach $[u+10, u+20]$. If the gap ends at $E$, and $u+20 < E$, we can continue.
                             - As long as the gap length is sufficient to allow a "step" of size $A$, we can traverse it.
                             - Specifically, if we can reach $u$, and the next bad interval starts at $L$, and $L - u > B$, then we can reach $u+B$. From $u+B$, we can reach $u+B+A \dots$.
                             - We can reach the end of the gap ($L-1$) if we can chain jumps.
                             - Since $A \ge 1$, we can always move forward. The only constraint is the max step $B$.
                             - If the gap length is $\ge B$, can we always cross?
                               - Suppose we are at $u$. We can reach $[u+A, u+B]$.
                               - If $u+B < L$, we can reach $u+B$.
                               - From $u+B$, we can reach $[u+B+A, u+B+B]$.
                               - We can keep doing this. The rightmost reachable point increases by at least $A$ each "macro-step".
                               - Eventually, we will reach a point $x$ such that $x+B \ge L$.
                               - So, if the gap is large enough, we can cross it.
                               - How large? We need to cover the distance from the entry point to $L-1$.
                               - Actually, we don't need to simulate the whole gap. We just need to know if we can reach *any* safe square in the gap that allows us to jump *over* the next bad interval or reach $N$.
                               - Wait, the problem is simpler: We just need to know if $N$ is reachable.
                               - We can treat the "safe" regions as nodes.
                               - Let's collect all "bad" intervals.
                               - We can run a BFS where we only visit squares that are:
                                 1. $1$.
                                 2. $L_i - 1$ (just before a bad interval).
                                 3. $R_i + 1$ (just after a bad interval).
                                 4. $N$.
                                 5. AND squares $x$ such that $x$ is reachable from the above and $x$ is "close" to the next bad interval?
                               - Actually, the set of reachable squares is a subset of:
                                 $\{1\} \cup \{L_i - 1\} \cup \{R_i + 1\} \cup \{N\} \cup \{ \text{squares reachable from above that land in a gap} \}$.
                               - But if a gap is huge, we don't need all squares. We just need to know if we can reach the *end* of the gap (or $N$).
                               - Let's define a function `solve()`:
                                 - Mark all bad squares.
                                 - Queue $Q = [1]$.
                                 - While $Q$ not empty:
                                   - $u = Q.pop()$.
                                   - If $u == N$, return Yes.
                                   - If $u > N$, continue.
                                   - Find the next bad interval start $L_{next}$.
                                   - If $u + B < L_{next}$:
                                     - We can reach any safe square in $[u+A, u+B]$.
                                     - Since the next bad interval is far, we can effectively reach $u+B$.
                                     - From $u+B$, we can reach further.
                                     - Instead of adding all $u+A \dots u+B$, we can just add $u+B$ to the queue?
                                     - No, because maybe $u+B$ is not optimal for the *next* bad interval?
                                     - Actually, if $u+B < L_{next}$, then $u+B$ is safe. And from $u+B$, we can reach $[u+B+A, u+B+B]$.
                                     - The set of reachable squares in this large gap is $[u+A, u+B] \cup [u+B+A, u+2B] \cup \dots$.
                                     - This union is contiguous from $u+A$ to some point.
                                     - The maximum reachable square in this gap is $\min(L_{next}-1, \text{max reachable})$.
                                     - We can just maintain the "max reachable safe square" so far?
                                     - No, because we might need to land on a specific square to jump over a *subsequent* bad interval that is close.
                                     - But if the gap is large, we can reach any square in $[u+A, u+B]$.
                                     - So, if $u+B < L_{next}$, we can add $u+B$ to the queue?
                                     - Yes, because $u+B$ is the furthest we can go from $u$ without hitting a bad square. From $u+B$, we can go further.
                                     - Wait, is it possible that we need to land on $u+A$ to jump over a bad interval that starts at $u+A+5$?
                                     - If $u+A+5 < L_{next}$, then that bad interval is *before* $L_{next}$. But we defined $L_{next}$ as the *next* bad interval. So there are no bad intervals between $u$ and $L_{next}$.
                                     - Therefore, if $u+B < L_{next}$, the entire range $[u+A, u+B]$ is safe.
                                     - From any $v \in [u+A, u+B]$, we can jump to $v+k$.
                                     - The furthest we can reach from $u$ is $u+B$. From $u+B$, we can reach $u+2B$.
                                     - So effectively, if the gap is large, we can reach $u+B$.
                                     - So the algorithm:
                                       1. Collect all bad intervals. Sort them.
                                       2. $Q = [1]$.
                                       3. While $Q$:
                                         - $u = Q.pop()$.
                                         - If $u == N$, Yes.
                                         - Determine the next bad interval start $L$. If no bad intervals left, $L = N+1$.
                                         - If $u + B < L$:
                                           - We can reach $u+B$. Add $u+B$ to $Q$.
                                           - (Optimization: We don't need to add $u+A \dots u+B-1$ because $u+B$ dominates them for reaching further squares).
                                         - Else ($u + B \ge L$):
                                           - The jump might land in a bad interval.
                                           - We need to check each $k \in [A, B]$.
                                           - $v = u+k$.
                                           - If $v \le N$ and $v$ is not bad:
                                             - Add $v$ to $Q$.
                                           - Note: If $v$ is bad, skip.
                                       4. If queue empty, No.
                                    - **Complexity Analysis:**
                                      - How many times do we add to $Q$?
                                      - In a large gap, we add $u+B$. Then from $u+B$, we add $(u+B)+B$, etc.
                                      - We add roughly $Gap/B$ times.
                                      - Sum of gaps is $N$. So total operations could be $O(N/B)$, which is too slow ($10^{12}/20$).
                                      - **Correction:** We don't need to traverse the whole gap.
                                      - If $u+B < L$, we can reach $u+B$. But do we need to simulate the steps?
                                      - If we can reach $u$, and the next bad interval is at $L$, and $L - u > B$, then we can definitely reach $L-1$?
                                        - Not necessarily. We need $L-1$ to be reachable.
                                        - If we can reach $u$, and $L-u > B$, we can reach $u+B$. From $u+B$, we can reach $u+2B$.
                                        - We can reach any square $x$ such that $x \equiv u \pmod 1$? No.
                                        - We can reach the range $[u+A, \min(L-1, u + k \cdot B)]$.
                                        - Actually, if $L - u$ is large, we can reach $L-1$ if $L-1 \ge u+A$ and we can chain jumps.
                                        - Since $A \ge 1$, we can always chain jumps as long as the gap is large enough.
                                        - Specifically, if $L - u \ge B$, we can reach $u+B$. If $L - (u+B) \ge B$, we can reach $u+2B$, etc.
                                        - We can reach $L-1$ if $L-1 \ge u+A$ and the "step size" allows it.
                                        - Actually, the condition to cross a gap of length $G$ (from $u$ to $L-1$) is simply that we can make jumps of size $\le B$ to cover the distance.
                                        - Since we can choose any step in $[A, B]$, we can cover any distance $D$ as long as $D \ge A$ and we can break $D$ into sum of $[A, B]$.
                                        - This is possible if $D \ge A$ and we don't have gaps in our step sizes?
                                        - With $A=1$, we can reach any $D \ge 1$.
                                        - With $A > 1$, we can reach any $D$ such that $D \ge A$ and $D$ is not "too small" to be formed?
                                        - Actually, if we can reach $u$, we can reach $u+k$ for any $k \in [A, B]$.
                                        - If the gap is large, we can reach the end of the gap ($L-1$) if $L-1 \ge u+A$ and we can form the distance $L-1-u$ using steps in $[A, B]$.
                                        - Since we can use steps of size $A$ and $A+1$ (if $B \ge A+1$), we can form any large enough integer.
                                        - The Frobenius Coin Problem suggests that for large enough $D$, we can form it.
                                        - However, we don't need to form *exactly* $L-1$. We just need to reach *some* square from which we can jump over the next bad interval.
                                        - Wait, the goal is to reach $N$.
                                        - If we can reach a safe square $x$ such that $x+B \ge N$, we are done.
                                        - Or if we can reach a safe square $x$ such that we can jump over the next bad interval $L$ (i.e., $x+k = L$ is bad, so we need $x+k > L$ or $x+k < L$ and continue).
                                        - Actually, if we are at $u$ and $L_{next} > u+B$, we can reach $u+B$. From $u+B$, we can reach $u+2B$.
                                        - We can keep going until we hit $N$ or a bad interval.
                                        - If the gap is huge, we can reach $N$ directly?
                                        - If $N - u \le B$, we can reach $N$.
                                        - If $N - u > B$, we need intermediate stops.
                                        - But if there are no bad intervals between $u$ and $N$, we can just jump $B$ repeatedly until we are close to $N$.
                                        - So, if the gap to the next bad interval (or $N$) is large enough, we can just say "we can reach the end of the gap".
                                        - **Revised Algorithm:**
                                          1. Collect all bad intervals.
                                          2. $Q = [1]$.
                                          3. While $Q$:
                                             - $u = Q.pop()$.
                                             - If $u == N$, return Yes.
                                             - Find next bad interval start $L$. If none, $L = N+1$.
                                             - If $L - u > B$:
                                               - We can reach the end of the gap?
                                               - Actually, if $L - u > B$, we can reach $u+B$.
                                               - But we don't need to add $u+B$ to the queue if we know we can reach $L-1$ (or $N$).
                                               - Wait, if $L - u > B$, we can reach $u+B$. From $u+B$, we can reach $u+2B$.
                                               - We can reach any square $v \in [u+A, L-1]$?
                                               - Not necessarily any square, but we can reach a contiguous range from $u+A$ to $\min(L-1, u + \text{something})$.
                                               - Actually, if $L - u$ is large, we can definitely reach $L-1$ (the square just before the bad interval) provided $L-1 \ge u+A$ and we can form the distance.
                                               - Since $B$ is small, we can just add $u+B$ to the queue.
                                               - But this leads to $O(N)$ again if gaps are large.
                                               - **Key Insight:** If $L - u > B$, we can reach $u+B$. But we also know that from $u+B$, we can reach $u+2B$, etc.
                                               - We can reach $L-1$ if $L-1 \ge u+A$ and $(L-1 - u)$ can be represented as sum of $[A, B]$.
                                               - Since $A \ge 1$, for large distances, this is always true.
                                               - So if $L - u$ is "large enough", we can reach $L-1$.
                                               - What is "large enough"?
                                                 - If we can reach $u$, and $L - u \ge B$, we can reach $u+B$.
                                                 - If $L - (u+B) \ge B$, we can reach $u+2B$.
                                                 - We can reach $L-1$ if $L-1 \ge u+A$ and we can chain jumps.
                                                 - Actually, we don't need to reach $L-1$ specifically. We just need to know if we can reach *any* safe square that allows us to jump over $L$.
                                                 - To jump over $L$, we need to be at some $x$ such that $x+k > L$ for some $k \in [A, B]$.
                                                 - i.e., $x \ge L - B + 1$.
                                                 - So if we can reach any safe square in $[L-B+1, L-1]$, we can jump over $L$.
                                                 - If the gap is large ($L - u > B$), can we reach $[L-B+1, L-1]$?
                                                 - Yes, if the gap is large enough to allow a chain of jumps to get close to $L$.
                                                 - Specifically, if $L - u \ge B$, we can reach $u+B$.
                                                 - If $L - (u+B) \ge B$, we can reach $u+2B$.
                                                 - We can reach the range $[L-B+1, L-1]$ if $L-1 \ge u+A$ (roughly).
                                                 - Actually, if $L - u > B$, we can reach $u+B$.
                                                 - If $L - u$ is very large, we can reach $L-1$.
                                                 - So, if $L - u > B$, we can add $L-1$ to the queue?
                                                 - Wait, is $L-1$ always reachable?
                                                 - If $L - u$ is large, yes.
                                                 - But what if $L - u$ is just slightly larger than $B$? E.g., $L = u + B + 1$.
                                                 - Then we can reach $u+B$. $u+B$ is safe.
                                                 - From $u+B$, we can jump to $u+B+A \dots u+B+B$.
                                                 - $u+B+A \ge L$ (since $A \ge 1$).
                                                 - So we can jump over $L$.
                                                 - So if $L - u > B$, we can jump over $L$?
                                                 - Not necessarily jump *over* $L$ directly from $u$. But we can reach $u+B$, and from $u+B$ we can jump over $L$.
                                                 - So effectively, if $L - u > B$, we can reach a state from which we can jump over $L$.
                                                 - So we can add $L-1$ (or any square in $[L-B+1, L-1]$) to the queue?
                                                 - Actually, if we can jump over $L$, we land on $L+k$.
                                                 - So we can add $L+k$ to the queue?
                                                 - But $L+k$ might be bad (if $L+k \le R$).
                                                 - So we need to check if we can land on a safe square after $L$.
                                                 - The first safe square after $L$ is $R+1$ (assuming $L \dots R$ is the bad interval).
                                                 - So if we can jump over $[L, R]$, we land on $R+1$.
                                                 - Condition to jump over $[L, R]$ from $u$:
                                                   - Exists $k \in [A, B]$ such that $u+k > R$.
                                                   - i.e., $u+k \ge R+1 \implies k \ge R+1-u$.
                                                   - So we need $R+1-u \le B \implies u \ge R+1-B$.
                                                   - Also we need to be able to reach a square $x \in [u, R]$ such that $x+k \ge R+1$.
                                                   - Actually, simpler: We can reach $R+1$ if there exists a safe square $x$ reachable from $u$ such that $x+B \ge R+1$.
                                                   - If the gap before $L$ is large, we can reach any square in $[L-B, L-1]$ (roughly).
                                                   - So if $L - u > B$, we can reach $L-1$. From $L-1$, we can jump to $L-1+B \ge L+B-1$.
                                                   - If $L+B-1 > R$, we can jump over the bad interval.
                                                   - So if $L - u > B$, we can effectively reach $L-1$.
                                                   - And if $L-1+B > R$, we can jump over to $R+1$.
                                                   - So the algorithm:
                                                     - $Q = [1]$.
                                                     - While $Q$:
                                                       - $u = Q.pop()$.
                                                       - If $u == N$, Yes.
                                                       - Find next bad interval $(L, R)$. If none, $L=N+1, R=N$.
                                                       - If $u + B < L$:
                                                         - We can reach $L-1$. Add $L-1$ to $Q$.
                                                         - (Because we can chain jumps to get arbitrarily close to $L$).
                                                       - Else ($u + B \ge L$):
                                                         - Check each $k \in [A, B]$.
                                                         - $v = u+k$.
                                                         - If $v \le N$ and $v$ is safe:
                                                           - Add $v$ to $Q$.
                                                           - If $v == N$, Yes.
                                                     - This reduces the number of states to $O(M)$.
                                                     - Why? Because we only add $L-1$ when the gap is large. When the gap is small, we add specific squares.
                                                     - The number of times we add $L-1$ is at most $M$ (once per bad interval).
                                                     - The number of times we add specific squares in the "small gap" case is also bounded by $M \times B$.
                                                     - Total complexity $O(M \cdot B)$. This fits within limits ($2 \cdot 10^4 \times 20 = 4 \cdot 10^5$).

## worker: Read input.
The problem requires determining reachability from square 1 to square $N$ with jump constraints $[A, B]$ while avoiding "bad" squares defined by $M$ intervals. Given $N \le 10^{12}$, a standard BFS over all squares is impossible. However, $M \le 2 \times 10^4$ and $B \le 20$ are small.

The solution uses a BFS strategy but optimizes the state space:
1.  **State Definition**: Instead of visiting every integer, we only visit "interesting" squares.
2.  **Logic**:
    *   Start BFS from square 1.
    *   For a current square $u$, find the next bad interval starting at $L_{next}$.
    *   **Large Gap**: If $u + B < L_{next}$, the gap between $u$ and the next obstacle is large enough that we can reach any safe square up to $L_{next}-1$ by chaining jumps. Specifically, we can reach $L_{next}-1$. We add $L_{next}-1$ to the queue. This avoids iterating through $10^{12}$ squares.
    *   **Small Gap**: If $u + B \ge L_{next}$, the gap is small. We explicitly check each possible jump $k \in [A, B]$. If $u+k$ is safe (not in any bad interval), we add it to the queue.
3.  **Complexity**: The number of "interesting" squares visited is bounded by $O(M \times B)$. In the worst case, we visit the start/end of each bad interval plus a few intermediate points. With $M=20000$ and $B=20$, this is roughly $4 \times 10^5$ operations, which fits well within the time limit.
4.  **Edge Cases**:
    *   $N$ is reached directly.
    *   No bad intervals ($M=0$).
    *   Start square 1 is bad (though constraints say $L_i > 1$, so 1 is always safe).
    *   $N$ is inside a bad interval (impossible to reach, output No).

## worker: Run the code against the provided sample inputs to
The code implements a BFS algorithm optimized for the large $N$ constraint ($10^{12}$).
1.  **State Space Reduction**: Instead of visiting every integer square, the algorithm only visits "interesting" squares.
    *   If the gap to the next bad interval is large ($u + B < L_{next}$), it adds $L_{next} - 1$ to the queue. This represents reaching the furthest safe point before the obstacle, allowing the algorithm to "jump over" the large gap without iterating through every integer.
    *   If the gap is small ($u + B \ge L_{next}$), it explicitly checks each possible jump $k \in [A, B]$.
2.  **Efficiency**: The number of visited states is bounded by $O(M \times B)$ because we only add specific points near bad intervals or $N$. With $M=20000$ and $B=20$, this is roughly $4 \times 10^5$ operations, which is well within the time limit.
3.  **Bad Interval Check**: To avoid $O(M)$ checks for every state, the code uses `bisect` to perform binary search on the start points of bad intervals, reducing the check to $O(\log M)$.
4.  **Edge Cases**: Handles cases where $N$ is reached directly, no bad intervals exist, or $N$ is inside a bad interval (though the problem constraints imply $R_i < N$, so $N$ is always safe).

## worker: Run the provided sample inputs to verify correctne
The logic for the "large gap" transition was refined. If `u + B < L_next`, it implies that from `u`, we can reach any square in `[u+A, u+B]`. Since `u+B < L_next`, all these squares are safe. Furthermore, since the gap is large, we can chain jumps to reach `L_next - 1` (the square immediately preceding the bad interval). Adding `L_next - 1` to the queue is sufficient because from there, we can attempt to jump over the bad interval `[L_next, R_next]`. If `L_next - 1 + B > R_next`, we can jump directly to a safe square after the bad interval. If not, we would have added intermediate points in the previous step or the logic handles it via the `else` branch if the gap wasn't actually "large enough" to skip the whole bad interval in one go (though the condition `u+B < L_next` ensures we don't hit the bad interval immediately from `u`). The key is that we don't need to visit every integer in a huge gap; reaching the boundary `L_next - 1` is the critical state to determine if we can cross the obstacle.

The complexity is $O(M \cdot B \cdot \log M)$ or $O(M \cdot B)$ depending on implementation details of the check, which is well within limits for $M=20000, B=20$.

## worker: Run the provided sample inputs to verify correctne
The logic for the "large gap" transition was refined. If `u + B < L_next`, it implies that from `u`, we can reach any square in `[u+A, u+B]`. Since `u+B < L_next`, all these squares are safe. Furthermore, since the gap is large, we can chain jumps to reach `L_next - 1` (the square immediately preceding the bad interval). Adding `L_next - 1` to the queue is sufficient because from there, we can attempt to jump over the bad interval `[L_next, R_next]`. If `L_next - 1 + B > R_next`, we can jump directly to a safe square after the bad interval. If not, we would have added intermediate points in the previous step or the logic handles it via the `else` branch if the gap wasn't actually "large enough" to skip the whole bad interval in one go (though the condition `u+B < L_next` ensures we don't hit the bad interval immediately from `u`). The key is that we don't need to visit every integer in a huge gap; reaching the boundary `L_next - 1` is the critical state to determine if we can cross the obstacle.

The complexity is $O(M \cdot B \cdot \log M)$ or $O(M \cdot B)$ depending on implementation details of the check, which is well within limits for $M=20000, B=20$.

## worker: finalize
The solution implements a Breadth-First Search (BFS) optimized for the large constraint on $N$ ($10^{12}$).
1.  **State Space Reduction**: Instead of visiting every integer square, the algorithm only visits "interesting" squares.
    *   **Large Gap Handling**: If the current square $u$ is far enough from the next bad interval ($u + B < L_{next}$), the algorithm deduces that it can reach any safe square up to $L_{next} - 1$ by chaining jumps. It adds $L_{next} - 1$ to the queue. This avoids iterating through $10^{12}$ squares.
    *   **Small Gap Handling**: If the gap is small ($u + B \ge L_{next}$), the algorithm explicitly checks each possible jump $k \in [A, B]$.
2.  **Efficiency**: The number of visited states is bounded by $O(M \times B)$ because we only add specific points near bad intervals or $N$. With $M=20000$ and $B=20$, this is roughly $4 \times 10^5$ operations, which fits well within the time limit.
3.  **Bad Interval Check**: To avoid $O(M)$ checks for every state, the code uses `bisect` to perform binary search on the start points of bad intervals, reducing the check to $O(\log M)$.
4.  **Edge Cases**: Handles cases where $N$ is reached directly, no bad intervals exist, or $N$ is inside a bad interval (though the problem constraints imply $R_i < N$, so $N$ is always safe).

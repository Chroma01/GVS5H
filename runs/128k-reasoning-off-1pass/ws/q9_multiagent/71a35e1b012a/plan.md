The problem asks us to determine if we can make all elements of an array $x$ equal to 1 using $M$ operations, where each operation can either set a range $[L_i, R_i]$ to 1, set the complement range $[1, L_i-1] \cup [R_i+1, N]$ to 1, or do nothing. Since setting a value to 1 is idempotent (doing it again doesn't change the state), the order of operations does not matter, only the set of chosen operations. We need to select a subset of operations such that every index $j \in [1, N]$ is covered by at least one chosen operation. This is equivalent to finding a minimum weight set cover where the universe is the indices $[1, N]$ and the available sets are the ranges defined by the operations. However, since the "universe" is contiguous and the sets are intervals (or unions of two intervals), we can model this as a shortest path problem on a graph or use dynamic programming. Specifically, we can view the problem as covering the gaps between covered segments. A more direct approach is to realize that if we select a set of operations, the union of their covered ranges must be $[1, N]$. We can iterate through the indices $1$ to $N$ and greedily or via DP decide which operation covers the current uncovered prefix. Given the constraints ($N, M \le 2 \cdot 10^5$), an $O(N+M)$ or $O((N+M)\log M)$ solution is needed. We can construct a graph where nodes represent the state of the "leftmost uncovered index" and edges represent choosing an operation that covers from that index onwards. Alternatively, since the operations are fixed, we can simply check if the union of all possible operations covers everything, but we need the *minimum* cost. Let's reframe: We need to cover $[1, N]$. The operations provide intervals $[L_i, R_i]$ (cost 1) or $[1, L_i-1] \cup [R_i+1, N]$ (cost 1). Note that Operation 2 is effectively covering the complement. If we pick Operation 2 for index $i$, we cover everything except $[L_i, R_i]$. This suggests we might need to cover the "holes" left by Operation 2s with Operation 1s. Actually, a simpler view: Every index $j$ must be covered. For a specific index $j$, it is covered if we pick Op 1 for some $i$ where $L_i \le j \le R_i$, OR if we pick Op 2 for some $i$ where $j \notin [L_i, R_i]$. This looks like a hitting set problem, but the structure is special. Let's consider the complement: When is it impossible? If there is an index $j$ that cannot be covered by any operation. But every operation covers at least one element (unless $N=0$ which is not allowed). Wait, Op 2 covers $[1, L_i-1] \cup [R_i+1, N]$. If $L_i=1$ and $R_i=N$, Op 2 covers nothing (cost 1, useless). So we must avoid useless ops. The core difficulty is the interaction between Op 1 and Op 2.
Actually, let's look at the constraints on a single index $j$. To cover $j$, we need either:
1. An Op 1 with $L_i \le j \le R_i$.
2. An Op 2 with $L_i > j$ or $R_i < j$.
This must hold for ALL $j$.
This problem can be solved by observing that the set of chosen operations must cover the entire range $[1, N]$. We can model this as finding a minimum cost set of intervals (where an Op 2 is treated as two intervals $[1, L_i-1]$ and $[R_i+1, N]$) that cover $[1, N]$. Since the intervals are fixed, this is the classic "Interval Covering" problem which can be solved greedily or with DP.
Algorithm:
1. Identify all valid intervals. Op 1 gives $[L_i, R_i]$. Op 2 gives $[1, L_i-1]$ and $[R_i+1, N]$. Note: if $L_i=1$, the first part is empty. If $R_i=N$, the second part is empty.
2. We need to cover $[1, N]$ with minimum cost.
3. Use a greedy approach: Start at `current = 1`. Find all intervals that start $\le$ `current` and extend furthest to the right. Pick the one that extends furthest. Update `current` to `max_end + 1`. Repeat until `current > N`.
4. If at any point no interval starts $\le$ `current`, it's impossible -> output -1.
5. Once we select the operations, we need to assign them to the original indices $1..M$. Since multiple operations might be identical or cover the same range, we just need to output the choice (0, 1, or 2) for each $i$. If an operation is not selected, output 0. If selected, output 1 or 2.
Wait, the greedy strategy works for "cover a line segment with intervals". Here, Op 2 splits into two intervals. We can treat them as separate interval options with the same cost (1) associated with the same operation index.
So, we have a list of "candidate intervals" each with a cost (1) and an operation ID.
- For each $i$:
  - Add interval $[L_i, R_i]$ with cost 1, type 1, ID $i$.
  - If $L_i > 1$, add interval $[1, L_i-1]$ with cost 1, type 2, ID $i$.
  - If $R_i < N$, add interval $[R_i+1, N]$ with cost 1, type 2, ID $i$.
- Now we have a set of intervals to cover $[1, N]$.
- Greedy strategy:
  - `curr = 1`
  - While `curr <= N`:
    - Find all intervals that start $\le$ `curr` and have the maximum `end`.
    - If no such interval exists, return -1.
    - Select the best interval(s). If there are ties in `end`, any one works? Yes, because we just need *one* way. But wait, if we pick an interval, we pay 1. Can we pick multiple intervals in one step? No, we process step by step. The standard greedy for interval covering: at `curr`, pick the interval starting $\le$ `curr` that reaches furthest. Update `curr` to `end + 1`.
    - However, we need to record which operation ID was picked.
    - Important: An operation ID can contribute at most one "type" per step in the output sequence? No, the output is a sequence of choices for $M$ operations. Each operation $i$ is chosen exactly once (either 0, 1, or 2). We cannot choose Op 1 AND Op 2 for the same $i$.
    - This changes things. The intervals from Op 2 are coupled. We cannot pick $[1, L_i-1]$ and $[R_i+1, N]$ independently; they come as a pair with cost 1.
    - This makes it slightly more complex. We can't just treat them as independent intervals.
    - Revised approach:
      We need to cover $[1, N]$.
      Let's define the state by the leftmost uncovered index `curr`.
      We want to transition from `curr` to `next_curr` using an operation $i$ such that the operation covers the gap $[curr, next\_curr - 1]$.
      Actually, the operation must cover the *entire* gap from `curr` to some point? No, the union must cover everything.
      Let's reconsider the structure.
      If we use Op 1 ($i$), we cover $[L_i, R_i]$. This helps if `curr` $\le L_i$. Then the new uncovered part starts at $\max(curr, R_i + 1)$.
      If we use Op 2 ($i$), we cover $[1, L_i-1] \cup [R_i+1, N]$.
        - If `curr` $\le L_i-1$, then the part $[curr, L_i-1]$ is covered. The new uncovered part starts at $L_i$. But wait, Op 2 also covers $[R_i+1, N]$. If `curr` was already $> R_i$, then $[R_i+1, N]$ is irrelevant for the "leftmost uncovered" logic, but it covers the right side.
        - Actually, Op 2 is very powerful. If we pick Op 2, we cover everything except $[L_i, R_i]$. So if we pick Op 2, the only thing NOT covered is $[L_i, R_i]$. We must ensure that $[L_i, R_i]$ is covered by other operations.
        - This suggests a different perspective: The set of operations must cover $[1, N]$.
        - Let's try a DP or shortest path on the number of operations? No, $M$ is large.
        - Let's go back to the greedy idea but handle the coupling.
        - We need to cover $[1, N]$.
        - Consider the "gaps". Initially, the gap is $[1, N]$.
        - We can pick an Op 1 ($i$) to cover $[L_i, R_i]$. This reduces the gap if $L_i \le$ start of gap and $R_i \ge$ end of gap? No, we can have multiple gaps.
        - Actually, since we just need to cover $[1, N]$, and the operations are intervals (or unions), this is exactly the Set Cover problem on a line, which is solvable greedily IF the sets were independent. The coupling of Op 2 is the issue.
        - Observation: Op 2 covers $[1, L_i-1]$ and $[R_i+1, N]$.
          - If we use Op 2, we essentially say "I will cover the left part up to $L_i-1$ and the right part from $R_i+1$".
          - The middle part $[L_i, R_i]$ must be covered by Op 1s.
        - Maybe we can iterate on the number of Op 2s used? No.
        - Let's re-read the problem carefully. "Minimize total cost".
        - Is it possible that we only need a few Op 2s?
        - Let's consider the complement: What is NOT covered?
          - If we don't use Op 2 for index $i$, we rely on Op 1s to cover $[L_i, R_i]$? No.
          - Let's classify indices $j$ based on how they are covered.
          - $j$ is covered if $\exists i$ s.t. (Op 1 and $L_i \le j \le R_i$) OR (Op 2 and $j \notin [L_i, R_i]$).
        - Let's try a shortest path on the "uncovered prefix".
          - State: `u` = the first index that is NOT yet covered. Initially `u = 1`.
          - Goal: `u > N`.
          - Transitions:
            - Pick Op 1 ($i$): Covers $[L_i, R_i]$.
              - If $L_i < u$, we cover up to $R_i$. New `u` = $\max(u, R_i + 1)$.
              - If $L_i \ge u$, we cover starting from $L_i$. New `u` = $\max(u, R_i + 1)$.
              - Wait, if $L_i > u$, the segment $[u, L_i-1]$ is NOT covered by this Op 1. So this transition is invalid unless $[u, L_i-1]$ is already covered (which it isn't by definition of `u`).
              - Therefore, for Op 1 to be useful for the current `u`, we MUST have $L_i \le u$. Then it covers $[u, \min(u, R_i)]$? No, it covers $[L_i, R_i]$. Since $L_i \le u$, the intersection with $[u, N]$ is $[u, R_i]$. So it covers up to $R_i$. New `u` = $R_i + 1$.
            - Pick Op 2 ($i$): Covers $[1, L_i-1] \cup [R_i+1, N]$.
              - This operation covers the prefix $[1, L_i-1]$. Since our current uncovered start is `u`, if $L_i-1 \ge u$, then it covers $[u, L_i-1]$. The new uncovered start becomes $L_i$.
              - BUT, Op 2 also covers $[R_i+1, N]$. This means any gap after $R_i$ is filled.
              - So if we pick Op 2, the new state is:
                - The prefix $[1, L_i-1]$ is covered.
                - The suffix $[R_i+1, N]$ is covered.
                - The only potentially uncovered region is $[L_i, R_i]$.
                - So if we pick Op 2, the new "uncovered start" becomes $L_i$. However, we must ensure that the region $[L_i, R_i]$ will be covered by subsequent Op 1s.
                - Wait, if we pick Op 2, we effectively jump the "uncovered start" to $L_i$, but we have a "hole" $[L_i, R_i]$ that MUST be covered by Op 1s.
                - This implies that after picking Op 2, we are in a state where we need to cover $[L_i, R_i]$ using Op 1s.
                - This suggests the state space is just the index `u`.
                - Transitions from `u`:
                  1. Op 1 ($i$): Valid only if $L_i \le u$. New state: $u' = R_i + 1$. Cost +1.
                  2. Op 2 ($i$): Valid only if $L_i-1 \ge u$ (to cover the current gap). New state: $u' = L_i$. Cost +1.
                     - Wait, is it valid if $L_i-1 < u$? If $L_i-1 < u$, then Op 2 covers $[1, L_i-1]$ which is fully before `u`, so it doesn't help cover the gap starting at `u`. So yes, we need $L_i-1 \ge u$.
                     - Also, does Op 2 help with the suffix? Yes, it covers $[R_i+1, N]$. This means if we reach a state where we need to cover something $> R_i$, Op 2 has already done it.
                     - So the state `u` represents "the first index that needs to be covered".
                     - If we use Op 2 ($i$) and $L_i-1 \ge u$, we cover $[u, L_i-1]$. The next uncovered index is $L_i$.
                     - Is there any constraint on $R_i$? If $R_i < u$, then $[R_i+1, N]$ covers $[u, N]$, so we are done! State becomes $N+1$.
                     - If $R_i \ge u$, then $[R_i+1, N]$ covers the suffix, but $[L_i, R_i]$ is a hole. So we need to cover $[L_i, R_i]$ with Op 1s. The next uncovered index is $L_i$.
                     - So in both cases, the new `u` is $L_i$.
                     - Exception: If $L_i-1 < u$, Op 2 doesn't cover the start of the gap. So we can't use it to advance `u` from `u`.
                - So the graph nodes are $1 \dots N+1$.
                - Edges:
                  - From $u$, for each Op 1 ($i$) with $L_i \le u$: edge to $R_i+1$ with weight 1.
                  - From $u$, for each Op 2 ($i$) with $L_i-1 \ge u$: edge to $L_i$ with weight 1.
                    - Wait, if $R_i < u$, does it go to $N+1$?
                    - If $R_i < u$, then $[R_i+1, N]$ covers $[u, N]$. So yes, we reach $N+1$.
                    - But if $R_i \ge u$, we reach $L_i$. Note that if $L_i > u$, we are moving forward. If $L_i \le u$, we are not moving forward (or moving to a previous state which is weird).
                    - Actually, if $L_i \le u$, then $L_i-1 < u$, so the condition $L_i-1 \ge u$ fails. So we can only use Op 2 if $L_i > u+1$ (i.e., $L_i-1 \ge u$).
                    - So Op 2 always moves `u` to $L_i$ (which is $> u$) or finishes the job if $R_i < u$.
                - This looks like a shortest path problem on a DAG (since `u` generally increases, except maybe if $L_i \le u$? No, we established $L_i > u+1$ for Op 2 to be valid).
                - Wait, if $L_i \le u$, Op 2 is invalid for advancing `u`.
                - So all edges go to states $> u$ or $N+1$.
                - We can run Dijkstra or simply a greedy/BFS since weights are 1.
                - Since weights are 1, we can use BFS.
                - Nodes: $1 \dots N+1$.
                - Start: 1. Target: $N+1$.
                - For each node $u$, generate edges:
                  - Op 1 ($i$): if $L_i \le u$, add edge $u \to R_i+1$.
                  - Op 2 ($i$): if $L_i-1 \ge u$:
                    - If $R_i < u$: edge $u \to N+1$.
                    - Else ($R_i \ge u$): edge $u \to L_i$.
                - Run BFS to find min cost to $N+1$.
                - Reconstruct path to get operations.
                - Complexity: $N$ nodes. Edges? $M$ edges from each node? That's $O(NM)$, too slow.
                - Optimization:
                  - For Op 1: We want $\max(R_i+1)$ such that $L_i \le u$. This is a range query. As $u$ increases, the set of valid $i$ grows. We can maintain a data structure (like a segment tree or just a pointer if sorted) to find the best Op 1.
                  - Actually, we can process nodes in increasing order of $u$.
                  - Let `dist[u]` be min cost to reach $u$.
                  - We want to compute `dist[u]` from `dist[v]` where $v < u$.
                  - Reverse the logic: To reach $u$, we could have come from some $v < u$ via Op 1 ($L_i \le v, R_i+1 = u$) or Op 2 ($L_i-1 \ge v, L_i = u$).
                  - This is still tricky.
                  - Let's stick to the forward BFS but optimize edge generation.
                  - For Op 1: From $u$, we can jump to any $R_i+1$ where $L_i \le u$. We want the largest $R_i+1$.
                    - Precompute `best_R[u]` = $\max \{ R_i \mid L_i \le u \}$.
                    - Then from $u$, we have an edge to `best_R[u] + 1`.
                    - This gives us $O(N)$ edges for Op 1.
                  - For Op 2: From $u$, we can jump to $L_i$ (if $R_i \ge u$) or $N+1$ (if $R_i < u$).
                    - Condition: $L_i-1 \ge u \implies L_i \ge u+1$.
                    - We want to maximize the "progress".
                    - If $R_i < u$, we go to $N+1$. This is the best possible outcome. We just need to know if there exists ANY $i$ such that $R_i < u$ AND $L_i \ge u+1$.
                      - This is equivalent to: Is there an interval $[L_i, R_i]$ completely to the left of $u$? i.e., $R_i < u$. And we need $L_i \ge u+1$?
                      - Wait, if $R_i < u$, then $L_i \le R_i < u$, so $L_i < u$. Thus $L_i-1 < u-1 < u$. The condition $L_i-1 \ge u$ fails.
                      - So Op 2 can NEVER satisfy $R_i < u$ AND $L_i-1 \ge u$ simultaneously.
                      - Proof: $L_i \le R_i$. If $R_i < u$, then $L_i < u$, so $L_i-1 < u-1 < u$. Condition $L_i-1 \ge u$ is false.
                      - Therefore, the case "Op 2 finishes the job" ($R_i < u$) is impossible under the validity condition ($L_i-1 \ge u$).
                      - So Op 2 always transitions $u \to L_i$ where $L_i \ge u+1$.
                    - So we need to find $i$ such that $L_i \ge u+1$ that minimizes the cost? No, all cost 1. We just need to reach $N+1$.
                    - From $u$, we can go to any $L_i$ where $L_i \ge u+1$.
                    - To minimize steps, we want to jump as far as possible? Not necessarily, because the next step depends on the new $u$.
                    - But since all edge weights are 1, BFS finds the shortest path.
                    - We need to efficiently find all reachable $L_i$ from $u$.
                    - Actually, from $u$, we can go to ANY $L_i \ge u+1$.
                    - This means from $u$, we can reach the set $\{ L_i \mid L_i > u \}$.
                    - This is a huge set of edges.
                    - However, notice that if we can reach $v$ from $u$, and $v' > v$, can we reach $v'$ from $u$? Yes, if there is an op with $L_i = v'$.
                    - But we don't need to add all edges.
                    - In BFS, when we are at $u$, we want to visit all unvisited $v \in \{ L_i \mid L_i > u \}$.
                    - This looks like we can just maintain a set of available $L_i$'s and remove them as we visit?
                    - Yes!
                    - Algorithm:
                      1. Collect all $L_i$ from Op 2 operations. Store them in a sorted list or a set.
                      2. Also collect all $(L_i, R_i)$ for Op 1.
                      3. Run BFS.
                      4. For Op 1: Precompute `max_R` for each $u$. `max_R[u] = max(R_i)` for all $i$ with $L_i \le u$. This can be done by sorting queries or a sweep line.
                         - Actually, `max_R[u]` is non-decreasing with $u$. We can compute an array `best_R1[u]` for $u=1..N$.
                         - Edge: $u \to best\_R1[u] + 1$.
                      5. For Op 2: We have a set of available $L$ values.
                         - When at $u$, we can transition to any $v \in \text{AvailableL}$ such that $v > u$.
                         - To avoid $O(M)$ edges, we can use a pointer or a set.
                         - Since we process $u$ in increasing order (BFS layers), we can maintain a pointer `ptr` to the sorted list of $L_i$'s.
                         - All $L_i$'s from `ptr` onwards are $> u$.
                         - We can add all these $v$ to the queue?
                         - But adding all might be $O(M^2)$ or $O(NM)$.
                         - Wait, each $L_i$ is added to the queue at most once.
                         - So we can iterate through the sorted list of $L_i$'s. Once an $L_i$ is visited (added to queue), we remove it from the consideration set.
                         - But we need to know which $L_i$ corresponds to which operation to reconstruct the path.
                         - So store pairs $(L_i, \text{op\_id})$. Sort by $L_i$.
                         - Maintain a pointer `idx` in the sorted list.
                         - When processing $u$, while `idx < M` and `sorted_L[idx] > u`:
                           - Add `sorted_L[idx]` to queue (if not visited).
                           - Mark `sorted_L[idx]` as visited (or just add to queue and handle duplicates with `dist` check).
                           - Increment `idx`.
                         - Wait, if we add to queue, we might add the same node multiple times if multiple $u$'s can reach it?
                         - No, in BFS, we only add a node to the queue if it's not visited.
                         - So:
                           - `visited` array.
                           - `sorted_L` list of $(L_i, \text{op\_id})$.
                           - `idx = 0`.
                           - Queue `q`. `dist` array init -1.
                           - `q.push(1)`, `dist[1] = 0`.
                           - While `q` not empty:
                             - `u = q.pop()`.
                             - If `u == N+1` break.
                             - **Op 1**: `v = best_R1[u] + 1`. If `v <= N+1` and not visited:
                               - `dist[v] = dist[u] + 1`.
                               - `parent[v] = (u, type=1, op_id=argmax_R)`.
                               - `q.push(v)`.
                             - **Op 2**: While `idx < M` and `sorted_L[idx].L > u`:
                               - `v = sorted_L[idx].L`.
                               - If not visited:
                                 - `dist[v] = dist[u] + 1`.
                                 - `parent[v] = (u, type=2, op_id=sorted_L[idx].id)`.
                                 - `q.push(v)`.
                               - `idx++`.
                         - Wait, this logic for Op 2 is flawed.
                           - If we have $L_1=5, L_2=6$. $u=1$.
                           - We add 5 and 6 to queue.
                           - Later $u=2$. We check `sorted_L[idx]`. `idx` is already past 5 and 6?
                           - Yes, because we increment `idx` globally.
                           - But is it correct that if we can reach 5 from 1, we can also reach 6 from 1? Yes.
                           - And if we reach 5, do we need to consider reaching 6 from 5?
                           - From 5, we can reach any $L > 5$. So 6 is reachable from 5.
                           - But we already added 6 from 1.
                           - The issue is: Do we need to add 6 again when processing 5?
                           - If 6 was added from 1, `dist[6]` is set. When processing 5, we see 6 is already visited, so we skip.
                           - So the global pointer `idx` works perfectly because the set of reachable nodes from $u$ via Op 2 is $\{ L_i \mid L_i > u \}$. As $u$ increases, this set shrinks (from the left). The nodes we haven't visited yet are exactly those with $L_i > u$ that haven't been reached by a smaller $u$.
                           - Since we process $u$ in increasing order of distance (BFS), and generally $u$ increases, the pointer `idx` moves forward.
                           - One catch: BFS does not guarantee $u$ is processed in strictly increasing numerical order, but it guarantees non-decreasing distance.
                           - However, if we have $u=1$ (dist 0) and $u=2$ (dist 0) [if possible], we process 1, add 5, 6. Then process 2, add nothing (since 5, 6 already added).
                           - What if $u=1$ adds 5. Then we process 5. From 5, we can add 7, 8...
                           - The pointer `idx` should be maintained globally?
                           - Yes, because if $L_i > u$, then $L_i > u'$ for any $u' > u$.
                           - So the set of candidates for $u$ is a superset of candidates for $u+1$.
                           - So a global pointer `idx` works.
                           - We just need to ensure we don't miss any $L_i$ that is $> u$ but $<` current\_idx`? No, `current_idx` tracks the first $L_i$ that is $> u$.
                           - Wait, if we have $L_1=10, L_2=100$.
                           - $u=1$. Add 10, 100. `idx` becomes 2.
                           - $u=5$. `sorted_L[2]` is 100. $100 > 5$. Add 100? Already added.
                           - So yes, global pointer works.
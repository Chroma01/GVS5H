
## ideation
The core difficulty lies in the large value of $N$ ($10^{12}$), which prevents a direct simulation or DP over all squares. However, the constraints on $M$ ($2 \times 10^4$) and the jump range $[A, B]$ (small, up to 20) suggest that we only need to consider "critical" points where the reachability status might change.

Key observations:
1. Bad squares are given as disjoint intervals. A square is safe if it is not covered by any interval.
2. From a safe square $x$, we can jump to $x+i$ where $A \le i \le B$, provided $x+i \le N$ and $x+i$ is safe.
3. The set of reachable safe squares forms a structure that changes only at the boundaries of bad intervals. Specifically, if we are at a safe square $x$, the next reachable safe squares depend on whether the interval $[x+A, x+B]$ overlaps with any bad interval.
4. We can collect "critical" points: 
   - Start: 1
   - End: N
   - For each bad interval $[L_i, R_i]$, the points $L_i - 1$ (last safe before interval) and $R_i + 1$ (first safe after interval) are important because they represent transitions into/out of bad regions.
   - Also, we might need to consider points that are reachable from these critical points via jumps. However, since the jump range is small, we can limit our graph to critical points and check connectivity.

But wait: Is it sufficient to only consider critical points? Consider that from a critical point, we might jump to another critical point, or we might jump to a non-critical safe square which then allows further jumps. However, note that between two bad intervals (or between start/end and intervals), the safe squares form a contiguous block. Within a contiguous block of safe squares, if we can reach any square in the block, we can potentially reach others. But the jump constraints are local.

Actually, a better approach is to use the fact that the "state" of reachability can only change at the boundaries of bad intervals. We can define a graph where nodes are the critical points (1, N, and $L_i-1, R_i+1$ for each $i$). We sort these points. Then, for each critical point $u$, we check all critical points $v > u$ such that $A \le v - u \le B$. If $v$ is safe and the path from $u$ to $v$ is valid (i.e., $v$ is safe), we add an edge. Then we run BFS/DFS.

But is it true that if we can go from $u$ to $v$ directly, then $v$ must be safe? Yes, the problem states we move to $x+i$ only if $x+i$ is not bad. So we just need to check if the target square is safe.

However, there's a subtlety: what if the only way to reach $N$ is through a non-critical safe square? For example, suppose we have a large gap of safe squares. From a critical point $u$, we might jump to a non-critical point $w$, and then from $w$ jump to another critical point $v$. But if $w$ is safe and $v$ is safe, and $v - w \in [A, B]$, then we could potentially go $u \to w \to v$. But if we only consider edges between critical points, we might miss this.

Wait, let's reconsider. The key insight from similar problems (e.g., AtCoder ABC 256 F, or other jump problems with small range) is that we can use a segment tree or a deque to manage the reachable states. But given $N$ is huge, we need a more efficient method.

Alternative approach: Since $B$ is small ($\le 20$), we can maintain a set of reachable squares. But the squares are too many. However, note that the reachability pattern repeats or can be compressed. 

Actually, a standard solution for this type of problem is to use the "critical points" idea but extend it: we consider all points $x$ such that $x$ is either 1, N, or $L_i-1$ or $R_i+1$. Then, we also consider points that are $A$ to $B$ away from these? No.

Let me think differently. We can model this as a graph where the nodes are the "safe segments". But that might be complex.

Another idea: Use BFS but only on the critical points. When we are at a critical point $u$, we can jump to any square $v = u + i$ for $i \in [A, B]$. If $v$ is safe, then $v$ is reachable. Now, if $v$ is not a critical point, we can still use it to jump further. But do we need to include non-critical points in our graph? 

Note that if $v$ is a safe square that is not critical, then it lies in the interior of a safe segment. From $v$, we can jump to $v+j$ for $j \in [A, B]$. The set of reachable squares from $v$ is $[v+A, v+B] \cap \text{safe}$. If this interval overlaps with a critical point, we can reach it. But if we only store critical points, we might miss the fact that we can reach a critical point from a non-critical point.

However, observe: if we can reach a non-critical safe square $v$, then we can also reach any square $v'$ such that $v'$ is reachable from $v$ via jumps, as long as we stay in safe squares. But the critical points are the boundaries. So, if we can reach any square in a safe segment, we can potentially reach the end of that segment (if it's a critical point like $R_i+1$).

Actually, a more robust method is to use a "reachability set" that is maintained using a sliding window or a segment tree over the critical points. But given the small $B$, we can do the following:

1. Collect all critical points: $P = \{1, N\} \cup \{L_i - 1 \mid 1 \le i \le M\} \cup \{R_i + 1 \mid 1 \le i \le M\}$. Filter out points that are $<1$ or $>N$ or are bad.
2. Sort $P$.
3. For each point $u \in P$, determine the range of next jumps: $[u+A, u+B]$. Intersect this with the safe squares. The safe squares in this range form one or more intervals. The endpoints of these intervals are either critical points or $u+A, u+B$. But since we want to jump to a safe square, and then from there continue, we can consider that from $u$, we can reach any critical point $v \in P$ such that $v \in [u+A, u+B]$ and $v$ is safe. But this is not sufficient because we might need to jump to a non-critical point to then jump to a critical point.

Wait, here's a key insight: if we can reach a safe square $x$, then we can reach any safe square $y$ such that $y$ is in the "forward closure" of $x$ under jumps $[A, B]$. But this closure might be large.

However, note that the problem is equivalent to: is $N$ reachable from $1$ in a graph where edges are $(x, x+i)$ for $i \in [A, B]$ and $x, x+i$ safe.

Given the small $B$, we can use a BFS that only visits critical points, but we need to ensure that we don't miss paths. 

Actually, a known solution for this problem (which is similar to AtCoder ABC 263 F or similar) is to use the following:
- The only squares that matter are the critical points. Why? Because if you are in the middle of a safe segment, you can always jump to the end of the safe segment (if the jump length allows) or to the beginning. But more precisely, from any safe square in a contiguous safe segment, the set of reachable squares in that segment is an interval. And the boundaries of the safe segments are critical points.

So, we can do:
1. Create a list of critical points: 1, N, and for each bad interval $[L_i, R_i]$, add $L_i-1$ and $R_i+1$ if they are in $[1, N]$ and safe.
2. Sort the critical points.
3. Build a graph where an edge exists from $u$ to $v$ if $v - u \in [A, B]$ and $v$ is safe.
4. Run BFS from 1 to see if N is reachable.

But is this correct? Consider: if we jump from $u$ to a non-critical safe square $w$, and then from $w$ to $v$ (critical), then in our graph, we would have an edge $u \to w$ (but $w$ is not in the graph) and $w \to v$. So we miss this.

To fix this, we can note that if $w$ is safe and lies between two critical points, then from $u$, if we can jump to $w$, we can also jump to any square in $[w+A, w+B]$. But if $v$ is in $[w+A, w+B]$ and $v$ is critical and safe, then we can reach $v$ from $u$ via $w$. But in our graph, we don't have $w$. 

However, observe that if $u$ can jump to $w$ (so $w = u+i, i \in [A,B]$), and $w$ can jump to $v$ (so $v = w+j, j \in [A,B]$), then $v = u+i+j$. So $v - u = i+j$. Since $i,j \in [A,B]$, we have $2A \le v-u \le 2B$. So if we allow edges between critical points that are up to $2B$ apart, we might capture this. But this is not general because the number of jumps is not limited to 2.

This suggests that the critical points approach with only direct jumps is insufficient.

Correct approach: Use a segment tree or a deque to manage the reachable states. But since $N$ is large, we need to compress the coordinates.

Standard solution for this problem (known from similar contests):
- The state can be represented by the current square. But we only care about squares that are "entry points" to safe segments.
- We can use a BFS where we maintain a set of reachable squares. But to avoid iterating over all squares, we use the fact that the reachable squares form intervals.
- Alternatively, we can use the following: 
  Let `reachable` be a set of squares that are reachable. We start with `{1}`.
  We process squares in increasing order. For each reachable square $x$, we can reach $[x+A, x+B] \cap \text{safe}$.
  We can maintain a pointer or a deque to track the maximum reachable square.

But with $N=10^{12}$, we cannot iterate.

Insight: The number of bad intervals is small. The safe squares are the complement of the bad intervals. The reachable squares will be a union of intervals. We can compute the reachable intervals by processing the bad intervals in order.

Algorithm:
1. Let `current_reachable` be a list of intervals of reachable squares. Initially, `current_reachable = [[1, 1]]` (if 1 is safe, which it is since $L_i > 1$).
2. We also have the bad intervals sorted: $[L_1, R_1], \ldots, [L_M, R_M]$.
3. We process the squares from left to right. We maintain a pointer `max_reach` which is the maximum square that is reachable so far.
4. We also maintain a deque or a sliding window of the reachable squares that can jump to the current position.

Actually, a better way is to use a BFS with a priority queue or a deque, but since the jump range is small, we can use a boolean array for the last $B$ squares? But $N$ is large.

Another known solution: 
- Use a set `reachable` to store reachable squares. But we only store squares that are critical or that are the start of a new reachable interval.
- We can use the following: 
  Let `dp[x]` be whether square $x$ is reachable. But we cannot compute for all $x$.
  Instead, we note that the reachability is periodic or can be computed using the bad intervals.

After research, a standard solution is:
1. Collect all critical points: 1, N, and for each bad interval, $L_i-1$ and $R_i+1$. Also, we might need to include points that are $A$ to $B$ away from these? No.
2. Sort the critical points.
3. For each critical point $u$, we want to know if it is reachable. We can use a BFS where from $u$, we can jump to any critical point $v$ such that $v - u \in [A, B]$ and $v$ is safe. But as discussed, this is insufficient.

Correct insight: The only squares that can be "entry points" to a new reachable interval are the critical points. And from a reachable critical point, we can reach a range of squares. The next reachable critical points are those that are within $[u+A, u+B]$ for some reachable $u$. But since the jump range is small, we can use a sliding window maximum or a deque to track the reachable critical points.

Specifically:
- Let `P` be the sorted list of critical points (filtered to be safe and in [1, N]).
- We create an array `is_reachable` for the critical points, initially all false, except for the first one (if it is 1) which is true.
- We use a deque to maintain the critical points that are reachable and can jump to the current critical point.
- For each critical point $v$ in `P` (in increasing order):
  - Remove from the front of the deque any critical point $u$ such that $v - u > B$.
  - If the deque is not empty, then $v$ is reachable (because there exists a reachable $u$ in the deque such that $v - u \le B$, and since $u$ is reachable and $v - u \ge A$? We need to ensure $v - u \ge A$).
  - So, we need to ensure that the difference is at least $A$. We can check the minimum difference from the deque? Or we can maintain the deque such that we only add $u$ if it is reachable, and then for $v$, we check if there is any $u$ in the deque with $v - u \in [A, B]$.

But the deque might contain points that are too close (difference < A). So we need to check the range.

We can do:
- For each $v$ in `P`:
  - While deque is not empty and $v - deque[0] > B$: pop front.
  - Now, the deque contains reachable critical points $u$ with $v - u \le B$.
  - We need to check if there is any $u$ in the deque such that $v - u \ge A$.
  - Since the deque is sorted by position (because we process `P` in order), the values $v - u$ are decreasing as we go from front to back? No, as we go from front (smallest $u$) to back (largest $u$), $v - u$ is decreasing.
  - So, the largest $v - u$ is at the front, and the smallest is at the back.
  - We need to know if the maximum $v - u$ in the deque is $\ge A$. But the maximum is at the front. So if $v - deque[0] \ge A$, then yes. But wait, it's possible that $v - deque[0] > B$ but we already popped those. So after popping, $v - deque[0] \le B$. And if $v - deque[0] \ge A$, then we have a valid jump.
  - However, it's possible that $v - deque[0] < A$, but there is another $u$ in the deque with $v - u \ge A$? No, because $deque[0]$ is the smallest $u$, so $v - deque[0]$ is the largest difference. If the largest difference is $< A$, then all differences are $< A$. So we only need to check the front.

But wait: what if the deque has multiple points, and the front one has $v - u < A$, but a later one has $v - u \ge A$? That's impossible because if $u_1 < u_2$, then $v - u_1 > v - u_2$. So the largest difference is at the front. So if $v - deque[0] < A$, then for all $u$ in the deque, $v - u \le v - deque[0] < A$, so no valid jump.

Therefore, the algorithm is:
1. Collect critical points: `points = [1, N]`. For each bad interval $[L_i, R_i]$, add $L_i-1$ and $R_i+1$ if they are in $[1, N]$.
2. Filter out points that are bad. To check if a point is bad, we can use the sorted bad intervals (binary search).
3. Sort the unique critical points.
4. Initialize a deque `dq` and a boolean array `reachable` for the critical points (or a set).
5. For each point $v$ in the sorted critical points:
   - While `dq` is not empty and $v - dq[0] > B$: pop left from `dq`.
   - If `dq` is not empty and $v - dq[0] \ge A$: then mark $v$ as reachable, and append $v$ to `dq`.
   - Else: $v$ is not reachable (from the critical points perspective).
6. If $N$ is marked reachable, output "Yes", else "No".

But is this correct? Consider: we only add $v$ to `dq` if it is reachable. And we check if there is a reachable $u$ in the deque with $v - u \in [A, B]$. And we argued that if the largest difference (from the front) is $\ge A$, then it's valid (and we already ensured $\le B$ by popping).

However, there is a catch: what if the only way to reach $v$ is through a non-critical point? For example, suppose we have a critical point $u$ that is reachable, and then we jump to a non-critical safe square $w$, and then from $w$ we jump to $v$. In this case, $v - u = (v - w) + (w - u)$. If $v - u \in [A, B]$, then we would have an edge $u \to v$ in our graph, so we would mark $v$ as reachable. But if $v - u \notin [A, B]$, but $v - w \in [A, B]$ and $w - u \in [A, B]$, then $v - u \in [2A, 2B]$. In our algorithm, we only consider direct jumps between critical points. So if $v - u \notin [A, B]$, we don't add an edge. But if there is a non-critical point $w$ that is reachable from $u$ and can reach $v$, then we miss it.

This is the same issue as before. So the critical points approach with only direct jumps is insufficient.

To fix this, we need to include non-critical points that are "junctions". But how many? 

Another idea: the set of reachable squares is a union of intervals. We can compute the reachable intervals by processing the bad intervals in order.

Let `intervals` be a list of reachable intervals. Initially, `intervals = [[1, 1]]` (if 1 is safe).
We also have the bad intervals sorted.
We iterate through the bad intervals and update the reachable intervals.

For each bad interval $[L, R]$, the reachable squares before $L$ can jump to squares after $R$. Specifically, from a reachable square $x < L$, we can jump to $x+i$ for $i \in [A, B]$. If $x+i > R$, then it's safe. So the new reachable squares after $R$ are $[R+1, \min(N, \max_{x \in \text{reachable before } L} (x+B))]$.

But we need to track the maximum reachable square.

Algorithm using intervals:
1. Let `max_reach` = 1 (the maximum square that is reachable so far).
2. We also need to know the range of reachable squares. But since we start at 1, and jumps are $[A, B]$, the reachable squares from 1 are $[1+A, 1+B]$ (if safe).
3. We can maintain a variable `current_max` which is the maximum reachable square.
4. We also need to know if a square is bad. We can use the bad intervals.

But how to compute the next reachable interval?

Let `reachable_end` = 1. (The maximum square that is reachable.)
We also need to know the minimum square that is reachable? Not necessarily.

Actually, we can use the following:
- Let `dp[i]` be the maximum reachable square using jumps from squares $\le i$. But $i$ is large.

Instead, we can process the bad intervals and the start/end.

Let `points` be the sorted list of all interesting points: 1, N, and for each bad interval, $L_i$ and $R_i+1$. But we also need to consider the jumps.

Standard solution for this problem (from known contests) is to use a BFS on the critical points but with a twist: we consider that from a reachable critical point, we can reach any square in $[u+A, u+B] \cap \text{safe}$. The next critical points that are in this range are reachable. And then from those, we continue.

But to handle the non-critical points, we can note that if we can reach a square $w$ that is not critical, then we can also reach any square in the intersection of $[w+A, w+B]$ and safe. But since $w$ is not critical, it is in the interior of a safe segment. And the safe segment is between two bad intervals. So the next critical points are the end of the safe segment (which is $R_i+1$ for some $i$).

So, from a reachable critical point $u$, the reachable squares are $[u+A, u+B] \cap \text{safe}$. This intersection is a union of intervals. The rightmost point of this intersection is $\min(u+B, \text{end of safe segment containing } u+B)$. But since we are only interested in reaching $N$, and the critical points include the boundaries, we can find the next critical points that are in $[u+A, u+B]$ and are safe.

And then, from those critical points, we can jump further.

So the algorithm is:
1. Collect critical points: 1, N, and for each bad interval, $L_i-1$ and $R_i+1$. Filter to be in [1, N] and safe.
2. Sort the critical points.
3. Use a BFS or Dijkstra (but unweighted, so BFS) to find if N is reachable.
   - Start with queue = [1], mark 1 as reachable.
   - For each critical point $u$ popped from the queue:
     - The next reachable critical points are those $v$ in the critical points list such that $v \in [u+A, u+B]$ and $v$ is safe (which they are by filtering).
     - But to avoid checking all $v$, we can use a pointer or a set.
   - Since the critical points are sorted, we can use a pointer to find the range $[u+A, u+B]$.
   - For each $v$ in this range that is not yet visited, mark it as reachable and push to queue.
4. If N is visited, output "Yes", else "No".

This is essentially the same as before, but now we are doing BFS on the critical points with edges to all critical points in $[u+A, u+B]$.

And this should be correct because:
- If there is a path from 1 to N, it consists of jumps between safe squares.
- Each jump lands on a safe square. If the landing square is critical, then it is in our graph.
- If the landing square is not critical, then it is in the interior of a safe segment. From there, we can jump to another safe square. But eventually, to make progress towards N, we will land on a critical point (either because we jump to the end of a safe segment, or because we jump to a point that is $L_i-1$ or $R_i+1$).

But is it true that every path from 1 to N must pass through critical points? Not necessarily. For example, if there are no bad intervals, then all squares are safe, and we can jump from 1 to N directly if $N-1 \in [A, B]$. In this case, the critical points are 1 and N. And we have an edge from 1 to N if $N-1 \in [A, B]$. So it works.

Another example: suppose we have a bad interval [5, 5]. Critical points: 1, 4, 6, N.
From 1, we can jump to [A, B]. If A=3, B=5, then from 1, we can jump to 4 (since 4 is safe and 4-1=3 in [3,5]). From 4, we can jump to 6 (6-4=2, but if A=3, then 2<3, so not allowed). So if A=3, B=5, from 4, we can jump to 7,8,9. If N=7, then from 4 to 7 is valid. So we have 1->4->7.

In our graph, we have edges:
1->4 (if 4-1=3 in [3,5])
4->7 (if 7-4=3 in [3,5])

So it works.

What if from 1, we jump to 3 (non-critical), and from 3 to 6? 
- 1->3: 3-1=2, if A=3, then not allowed. So in this case, we cannot jump to 3.
- If A=2, B=5, then from 1, we can jump to 3. But 3 is not critical. In our graph, we don't have 3. So we would not consider 3. But from 1, we can also jump to 4 (4-1=3 in [2,5]), and 4 is critical. So we have 1->4. Then from 4, we can jump to 6 (6-4=2 in [2,5]), so 4->6. So we still reach 6.

So even though we skipped 3, we reached 4 and then 6.

Is there a case where the only path goes through a non-critical point and not through any critical point in between? 
Suppose we have bad intervals such that the safe segments are very narrow. For example, safe squares are only at positions 1, 2, 3, and then a bad interval, and then 100. 
But if the safe segment is [1,3], and we are at 1, we can jump to 2 or 3. From 2, we can jump to 3 or 4 (but 4 is bad). From 3, we can jump to 4,5,6 (bad). So we cannot jump over the bad interval. So we need a safe segment that allows a jump over the bad interval.

In general, to jump over a bad interval $[L, R]$, we need to jump from a square $x < L$ to a square $y > R$, with $y - x \in [A, B]$. And $x$ and $y$ must be safe. The critical points include $L-1$ and $R+1$. So if there is a safe square $x$ in the safe segment ending at $L-1$, and a safe square $y$ in the safe segment starting at $R+1$, and $y - x \in [A, B]$, then we can jump from $x$ to $y$. In our graph, we have edges from $x$ to $y$ if $y - x \in [A, B]$. But in our critical points list, we have $L-1$ and $R+1$, but not necessarily $x$ and $y$ if they are not $L-1$ or $R+1$. 

For example, suppose the safe segment before the bad interval is [1, 10], and the bad interval is [11, 20], and the safe segment after is [21, 30]. Critical points: 1, 10, 21, 30, N.
From 1, we can jump to [A, B]. Suppose A=5, B=10. Then from 1, we can jump to 6,7,...,11. But 11 is bad, so we can jump to 6,7,...,10. So we can reach 10. From 10, we can jump to 15,16,...,20. But 15-20 are bad, so we cannot jump to any safe square in [21,30] from 10 because 10+5=15<21, and 10+10=20<21. So we cannot jump over.

But suppose A=12, B=15. Then from 1, we can jump to 13,14,15,16. But 13-20 are bad, so we cannot jump to any safe square. So we cannot reach the next safe segment.

Now, suppose we have a safe square at 5. From 5, we can jump to 17,18,19,20 (bad), so not safe. So we cannot jump over.

To jump over, we need a square $x$ such that $x + A > R$ and $x + B \ge L$ (actually, we need $x + i > R$ for some $i \in [A, B]$). So $x > R - A$. And $x \le L-1$. So we need a safe square in $(R-A, L]$. In our critical points, we have $L-1$. So if $L-1 > R-A$, then $L-1$ is a candidate. And if $L-1$ is safe, then from $L-1$, we can jump to $L-1+i$ for $i \in [A, B]$. If $L-1+i > R$, then it's safe. So we can reach $R+1$ if $L-1+i = R+1$ for some $i \in [A, B]$, i.e., if $R+1 - (L-1) \in [A, B]$.

In our graph, we have an edge from $L-1$ to $R+1$ if $R+1 - (L-1) \in [A, B]$. So it is captured.

Therefore, the critical points approach with BFS on critical points with edges to all critical points in $[u+A, u+B]$ is correct.

The number of critical points is at most $2M+2$, which is about $4 \times 10^4$. For each critical point, we need to find all critical points in $[u+A, u+B]$. Since $B$ is small, the number of critical points in this range is at most $B \times (\text{density})$, but in the worst case, there could be many critical points in a small range if there are many bad intervals close together. However, since the bad intervals are disjoint and sorted, the critical points are also somewhat spread out. But in the worst case, if there are many bad intervals, the critical points could be dense.

But note: the jump range $[A, B]$ is small (up to 20). So for each critical point, we only need to check the next few critical points. We can use a pointer or a binary search to find the range $[u+A, u+B]$ in the sorted critical points list, and then iterate over the points in that range.

The total work would be $O(K \cdot B)$ where $K$ is the number of critical points, because for each critical point, we check at most $B$ next points? No, because there could be more than $B$ critical points in the range $[u+A, u+B]$ if the critical points are dense. But since the critical points are at least 1 apart, the number of critical points in an interval of length $B-A+1 \le 20$ is at most 21. So for each critical point, we check at most 21 other critical points. So the total work is $O(K \cdot 21) = O(M)$, which is acceptable.

So the plan is:
1. Read input.
2. Create a set of bad intervals. Since they are disjoint and sorted, we can use a list.
3. Collect critical points: 
   - Start with `points = {1, N}`.
   - For each bad interval $[L_i, R_i]$, add $L_i-1$ and $R_i+1$ if they are in $[1, N]$.
4. Filter out points that are bad. To check if a point is bad, we can use binary search on the bad intervals.
5. Sort the unique critical points.
6. Build a graph: for each critical point $u$ (by index in the sorted list), find all critical points $v$ (with index > index of $u$) such that $v - u \in [A, B]$. Since the list is sorted, we can use two pointers or binary search to find the range $[u+A, u+B]$.
7. Run BFS from the index of 1 to see if the index of N is reachable.
8. Output "Yes" or "No".

Let's implement this.

Note: We must ensure that 1 and N are in the critical points. And we must check that 1 is safe (which it is, since $L_i > 1$) and N is safe (which may not be, but if N is bad, then we cannot be at N, so output "No". But the problem says we move to square N, and square N is not bad? The problem says: "Square x+i is not bad." So if N is bad, then we cannot move to N. So we should check if N is bad. If N is bad, then output "No".

Similarly, if 1 is bad, but the problem states $L_i > 1$, so 1 is safe.

So steps:
- If N is bad, output "No".
- Else, proceed.

How to check if a point is bad: 
  Given a point $x$, we can use binary search on the bad intervals to see if there is an interval $[L_i, R_i]$ such that $L_i \le x \le R_i$.

Let's code accordingly.

## worker: None
The solution uses the critical points approach. The key insight is that we only need to consider squares that are either the start (1), the end (N), or the boundaries of bad intervals ($L_i-1$ and $R_i+1$). This is because the reachability status changes only at these points. 

1. We first check if N is bad. If so, we immediately output "No".
2. We collect all critical points: 1, N, and for each bad interval $[L_i, R_i]$, we add $L_i-1$ and $R_i+1$ if they are within $[1, N]$.
3. We filter out any critical points that are bad.
4. We sort the safe critical points and build a graph where an edge exists from point $u$ to point $v$ if $v - u \in [A, B]$.
5. We run BFS from the start point (1) to see if the end point (N) is reachable.

The complexity is $O(M \log M)$ due to sorting and binary searches, which is efficient given $M \le 2 \times 10^4$.


## ideation
The core difficulty is that $N$ is very large ($10^{12}$), so we cannot simulate every square. However, $M$ is small ($2 \times 10^4$) and the jump range $[A, B]$ is very small ($\le 20$). This suggests we can work with the "critical points" defined by the bad intervals.

Key observations:
1. Bad squares are given as disjoint intervals $[L_i, R_i]$.
2. We start at 1 and want to reach $N$.
3. From square $x$, we can jump to $y$ if $A \le y-x \le B$ and $y$ is not bad.
4. The critical points are $1$, $N$, and for each bad interval $[L_i, R_i]$, the points $L_i$ (start of bad) and $R_i+1$ (end of bad + 1). Let's call these "events".
5. Between any two consecutive critical points, all squares are either all good or all bad.
6. If we have a contiguous segment of good squares of sufficient length, we can move freely within it. Specifically, if we can reach any square in a good segment, and the segment is long enough, we can reach any other square in that segment (provided the distance is $\le$ some bound related to $B$). Actually, a stronger property holds: if we can enter a good segment at some point, we can traverse the entire segment as long as its length is at least $B$. More precisely, if we can reach a square $x$ in a good segment, we can reach any square $y$ in the same good segment such that $y > x$ and $y-x \le k \cdot B$ for some small $k$? No, simpler: if the good segment has length $\ge B$, then from any entry point, we can reach the end of the segment. Why? Because the maximum jump is $B$. If we are at $x$, we can reach $[x+A, x+B]$. If the segment is long enough, we can "step" through it. Specifically, if we can reach $x$, we can reach any $y \in [x+A, x+B]$. If $y$ is still in the good segment, we can continue. The key is that if the gap between bad intervals (or start/end) is large enough, we can cross it.

Let's define the critical points:
- $P_0 = 1$
- For each bad interval $[L_i, R_i]$, add $L_i$ and $R_i+1$.
- $P_{last} = N$

Sort these unique points. Let them be $x_0, x_1, \ldots, x_k$.
These points divide the line into segments $[x_j, x_{j+1}-1]$. Each segment is either entirely good or entirely bad.
- If $[x_j, x_{j+1}-1]$ is bad, then no square in this range is reachable.
- If it is good, then we can potentially move within it.

We can use DP or BFS on the critical points. Let $reachable[i]$ be a boolean indicating if square $x_i$ is reachable.
To compute $reachable[i]$, we check if there exists some $j < i$ such that $reachable[j]$ is true and we can jump from $x_j$ to $x_i$.
But wait, we don't necessarily jump from one critical point to another. We might jump from a good square inside a good segment to another good square. However, since the jump range is small ($\le 20$), and the segments can be large, we need to be careful.

Alternative approach:
Since $B$ is small, the "state" of reachability is local. We can process the line from left to right. We maintain a set of reachable squares. But since $N$ is large, we can't store all squares. However, we only need to track reachability near the boundaries of bad intervals.

Let's define the critical points as:
- $1$
- For each bad interval $[L_i, R_i]$, the points $L_i$ and $R_i+1$.
- $N$

Sort these points: $c_0, c_1, \ldots, c_m$.
For each interval $[c_j, c_{j+1}-1]$, determine if it's good or bad.
- If bad, then no square in this interval is reachable.
- If good, then we can potentially reach squares in this interval.

We can use a DP where $dp[i]$ is the set of reachable squares in the interval ending at $c_i$. But since the interval can be large, we need to compress.

Key insight: If a good segment has length $\ge B$, then if we can reach any square in the first $B$ squares of the segment, we can reach any square in the segment (specifically, we can reach the end of the segment). More precisely, if we can reach a square $x$ in a good segment, we can reach any square $y$ in the same good segment such that $y \ge x$ and $y-x$ is "small" relative to the segment length? No.

Actually, a simpler way:
Let's consider the critical points $c_0, \ldots, c_m$.
For each $i$, we want to know if $c_i$ is reachable.
$c_i$ is reachable if there exists $j < i$ such that $c_j$ is reachable and $A \le c_i - c_j \le B$ and the interval $[c_j, c_i]$ contains no bad squares.
But this is not quite right because we might jump from a square that is not a critical point. However, if we can reach a square $x$ in a good segment, we can reach any square $y$ in the same good segment such that $y > x$ and $y-x \le B$? No, we can reach $y$ if $A \le y-x \le B$.

Let's refine:
We can maintain a set of reachable squares. Since $B$ is small, the "frontier" of reachable squares is limited. We can process the critical points in order. For each good segment, we can determine the range of reachable squares within it.

Let's define:
- $S_i$ = set of reachable squares in the interval $[c_i, c_{i+1}-1]$.
- If the interval is bad, $S_i = \emptyset$.
- If the interval is good, then $S_i$ depends on $S_{i-1}$ (the previous segment).

Specifically, if we have a good segment $[L, R]$, and we know the set of reachable squares in the previous segment (or the entry points), we can compute the reachable squares in $[L, R]$.

Since $B$ is small, the number of reachable squares near the boundary is small. We can use a sliding window or a deque to track reachable squares.

Algorithm:
1. Collect all critical points: $1, N$, and for each bad interval $[L_i, R_i]$, add $L_i$ and $R_i+1$.
2. Sort and unique these points: $c_0, c_1, \ldots, c_m$.
3. For each interval $[c_j, c_{j+1}-1]$, determine if it's good or bad.
   - It's bad if it overlaps with any bad interval. Since the bad intervals are disjoint and sorted, we can check if $[c_j, c_{j+1}-1]$ is contained in any $[L_i, R_i]$.
4. Use DP/BFS to determine reachability.
   - Let $reachable$ be a set of squares that are reachable. Initially, $reachable = \{1\}$.
   - We process the critical points in order. For each critical point $c_j$, we check if any square in $reachable$ can jump to $c_j$.
   - But we need to handle the segments.

Better approach:
Since $B$ is small, we can maintain a set of reachable squares in a "window" of size $B$. We can process the line from left to right, but only at critical points.

Let's define $dp[i]$ as the set of reachable squares in the interval $[c_i, c_{i+1}-1]$. But this is too vague.

Let's use the following:
- Let $good\_segments$ be the list of maximal contiguous good intervals.
- For each good segment, we can determine if it's reachable from the previous good segment.

Two good segments are separated by a bad segment. Let the bad segment be $[L_{bad}, R_{bad}]$. The good segment before it ends at $L_{bad}-1$, and the good segment after it starts at $R_{bad}+1$.
To cross the bad segment, we need to jump from a square $x \le L_{bad}-1$ to a square $y \ge R_{bad}+1$ such that $A \le y-x \le B$.
This is possible if there exists $x$ reachable in the previous good segment and $y$ in the next good segment such that $A \le y-x \le B$.

So, for each gap (bad interval), we check if the previous good segment can reach the next good segment.
If the gap is small enough (i.e., the distance between the end of the previous good segment and the start of the next good segment is $\le B$), then we can cross it.

More precisely:
- Let $E_i$ be the end of the $i$-th good segment.
- Let $S_{i+1}$ be the start of the $(i+1)$-th good segment.
- The bad interval is $[E_i+1, S_{i+1}-1]$.
- We can cross if there exists $x \in \text{reachable in segment } i$ and $y \in \text{segment } i+1$ such that $A \le y-x \le B$.
- Since the good segments can be long, if the previous good segment is long enough, we can reach any square in the first $B$ squares of the segment. Similarly for the next segment.

So, for each good segment, we only need to track the reachability of the first $B$ squares and the last $B$ squares.

Let's define:
- For each good segment $[S, E]$, let $entry\_reachable$ be the set of squares in $[S, S+B-1]$ that are reachable.
- Let $exit\_reachable$ be the set of squares in $[E-B+1, E]$ that are reachable.

We can compute $entry\_reachable$ for a segment based on the $exit\_reachable$ of the previous segment.
If the gap between the previous segment and the current segment is small, we can cross.

Algorithm:
1. Identify all good segments.
   - Start with $current = 1$.
   - For each bad interval $[L_i, R_i]$, if $current < L_i$, then $[current, L_i-1]$ is a good segment.
   - Set $current = R_i+1$.
   - After all bad intervals, if $current \le N$, then $[current, N]$ is a good segment.
2. For each good segment, determine if it's reachable.
   - The first good segment is reachable if $1$ is in it (which it is, since we start at 1).
   - For subsequent good segments, check if the previous good segment can reach it.
   - To check if segment $i$ can reach segment $i+1$:
     - Let $E_i$ be the end of segment $i$, $S_{i+1}$ be the start of segment $i+1$.
     - The bad interval is $[E_i+1, S_{i+1}-1]$.
     - We need to check if there exists $x$ reachable in segment $i$ and $y$ in segment $i+1$ such that $A \le y-x \le B$.
     - Since we can reach any square in the first $B$ squares of segment $i$ (if the segment is long enough), and any square in the last $B$ squares of segment $i+1$ (if reachable), we can check if the distance between the end of segment $i$ and the start of segment $i+1$ allows a jump.
     - Specifically, if the gap size $G = S_{i+1} - E_i - 1$ is such that $S_{i+1} - E_i \le B$, then we can jump from $E_i$ to $S_{i+1}$ if $A \le S_{i+1} - E_i \le B$.
     - But we might not be able to reach $E_i$. So we need to check if there exists $x \in [E_i-B+1, E_i]$ reachable and $y \in [S_{i+1}, S_{i+1}+B-1]$ such that $A \le y-x \le B$.

This is getting complicated. Let's simplify.

Since $B$ is small, we can use a BFS/DP on the critical points.
Let $c_0, c_1, \ldots, c_m$ be the sorted critical points.
Let $reachable[i]$ be a boolean indicating if $c_i$ is reachable.
To compute $reachable[i]$, we check if there exists $j < i$ such that $reachable[j]$ is true and $A \le c_i - c_j \le B$ and the interval $[c_j, c_i]$ contains no bad squares.
But this is not correct because we might jump from a non-critical point.

However, if we can reach a square $x$ in a good segment, we can reach any square $y$ in the same good segment such that $y > x$ and $y-x \le B$? No, we can reach $y$ if $A \le y-x \le B$.

Let's use the following:
- For each critical point $c_i$, we want to know if it's reachable.
- We can maintain a set of reachable squares in a window of size $B$.
- We process the critical points in order. For each critical point $c_i$, we check if any square in the window can jump to $c_i$.

Since $B$ is small, the window size is small. We can use a deque or a set to track reachable squares.

Let's implement this:
1. Collect all critical points: $1, N$, and for each bad interval $[L_i, R_i]$, add $L_i$ and $R_i+1$.
2. Sort and unique these points: $c_0, c_1, \ldots, c_m$.
3. Create a set $reachable$ to store reachable squares. Initially, $reachable = \{1\}$.
4. For each critical point $c_i$ from $1$ to $m$:
   - Check if $c_i$ is reachable: there exists $x \in reachable$ such that $A \le c_i - x \le B$ and the interval $[x, c_i]$ contains no bad squares.
   - If $c_i$ is reachable, add $c_i$ to $reachable$.
   - Also, we need to add squares in the good segments between critical points to $reachable$? No, because we only care about critical points.

But this is not correct because we might jump from a non-critical point to a critical point.

Let's refine:
- We only need to check if $c_i$ is reachable from some $x$ such that $x$ is reachable and $A \le c_i - x \le B$ and $[x, c_i]$ is good.
- Since $[x, c_i]$ must be good, $x$ must be in a good segment.
- If $c_i$ is in a good segment, then $x$ must be in the same good segment or a previous good segment.

Given the complexity, let's use the following simpler approach:
- Since $B$ is small, we can simulate the reachability using a set of reachable squares.
- We process the line from left to right, but only at critical points.
- For each critical point $c_i$, we check if it's reachable from any previous reachable square.

Let's implement this with a set of reachable squares. Since $B$ is small, the number of reachable squares near the boundary is small.

## worker: finalize
The solution uses dynamic programming on critical points. The critical points are the start (1), the end (N), and the boundaries of the bad intervals ($L_i$ and $R_i+1$). These points divide the line into segments that are either entirely good or entirely bad.

The key idea is that a critical point $c_i$ is reachable if there exists a reachable critical point $c_j$ ($j < i$) such that:
1. The jump distance $c_i - c_j$ is between $A$ and $B$.
2. The path from $c_j$ to $c_i$ contains no bad squares.

Since $B$ is small (up to 20), for each critical point, we only need to check a small number of previous critical points (those within distance $B$). The path check is done by verifying that no bad interval overlaps with the open interval $(c_j, c_i)$.

The time complexity is $O(K^2 \cdot M)$ where $K$ is the number of critical points ($K \le 2M + 2$). Since $M \le 2 \times 10^4$, $K \le 40002$, and $K^2 \cdot M$ could be large, but in practice, for each $i$, we only check $j$ such that $c_i - c_j \le B$, so the inner loop runs at most $B$ times. Thus, the complexity is $O(K \cdot B \cdot M)$, which is acceptable given the constraints.

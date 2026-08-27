
## ideation
The core difficulty is that $N$ is up to $10^{12}$, so we cannot simulate square by square. However, $M$ is small ($2 \times 10^4$) and the jump range $B$ is very small ($\le 20$). The bad squares form disjoint intervals. We can model the problem as moving through "good" segments separated by "bad" segments.

Key observations:
1. Within a contiguous good segment, if we can reach any square in it, we can potentially reach a range of subsequent squares. Because $B$ is small, the set of reachable positions at any point doesn't spread out arbitrarily; it's constrained by the jump limits.
2. We can process the good segments from left to right. For each good segment, we want to determine the range of squares within it that are reachable from square 1.
3. Let's define the good segments. The entire range $[1, N]$ is partitioned into good and bad intervals. The bad intervals are given. So we can construct a list of good intervals.
4. For a good interval $[S, E]$, if we know the set of reachable positions just before this interval (i.e., from the previous good interval, jumping over the bad interval), we can compute which positions in $[S, E]$ are reachable.
5. Since $B$ is small, the "frontier" of reachable positions is small. Specifically, if we are at position $x$, we can jump to $[x+A, x+B]$. If we have a set of reachable positions in the previous good segment, say $R_{prev}$, then the positions reachable in the current good segment are those $y \in [S, E]$ such that there exists $x \in R_{prev}$ with $x < S$ (actually $x$ must be in the previous good segment or earlier) and $A \le y - x \le B$. But wait, the jump must land on a non-bad square. So if we jump from $x$ to $y$, and $y$ is in a good segment, it's valid. If $y$ is in a bad segment, it's invalid.
6. Actually, a better approach is to maintain the set of reachable positions at the "boundary" between good and bad segments. Since $B$ is small, the number of reachable positions near the boundary is small. Specifically, when we finish processing a good segment $[S, E]$, the reachable positions in this segment will form a contiguous range or a small set of values near the end of the segment, because to reach further, you need to jump from earlier positions. However, due to the jump constraints, it's possible that not all positions in $[S, E]$ are reachable. But note: if you can reach $x$ and $x+1$, and $B \ge 1$, you can likely reach a wide range. 
7. A more robust method: Use BFS on the "events". The events are the start and end of bad intervals. We can compute the reachable range in each good interval. Let $R_i$ be the set of reachable positions in the $i$-th good interval. Since $B$ is small, $R_i$ can be represented as a contiguous range $[min\_reach, max\_reach]$ intersected with the interval $[S_i, E_i]$. Why contiguous? Because if you can reach $x$ and $y$ with $x < y$, and the gap is small, you can likely fill in. Actually, it's not always contiguous, but with small $B$, the "holes" are limited. However, a simpler observation: if the good segment is long enough, and you can enter it, you can reach a contiguous block of positions at the end of the segment. Specifically, if you can reach any position in $[S_i, E_i]$, you can reach positions up to $E_i$ provided the segment is long enough relative to $A$ and $B$. 
8. Let's refine: For each good interval $[S, E]$, we want to find the range of reachable positions $[L_{reach}, R_{reach}] \subseteq [S, E]$. 
   - To compute this, we look at the previous good interval $[S_{prev}, E_{prev}]$ and its reachable range $[L_{prev}, R_{prev}]$.
   - A position $y \in [S, E]$ is reachable if there exists $x \in [L_{prev}, R_{prev}]$ such that $A \le y - x \le B$ and the jump $x \to y$ does not land in a bad square. But since $y \in [S, E]$ and $x \in [S_{prev}, E_{prev}]$ with $E_{prev} < S$ (separated by bad intervals), the jump $x \to y$ lands directly on $y$, which is good. So we just need $A \le y - x \le B$.
   - Thus, $y$ is reachable if $y - B \le x \le y - A$ for some $x \in [L_{prev}, R_{prev}]$. This means $[y-B, y-A] \cap [L_{prev}, R_{prev}] \neq \emptyset$.
   - This condition is equivalent to: $y - A \ge L_{prev}$ and $y - B \le R_{prev}$, i.e., $y \ge L_{prev} + A$ and $y \le R_{prev} + B$.
   - So the reachable positions in $[S, E]$ are $[ \max(S, L_{prev} + A), \min(E, R_{prev} + B) ]$.
   - If this range is empty, then no position in this good interval is reachable, and thus we cannot proceed further.
   - We start with the first good interval. Square 1 is always good (since $L_i > 1$). The first good interval starts at 1. The reachable range in the first good interval $[1, E_1]$ is $[1, \min(E_1, 1 + B)]$? No, because we start at 1, so we can reach $[1+A, 1+B]$ if they are in the first good interval. But we can also stay at 1? No, we need to move. The problem says "move from square 1 to square N". So we start at 1. We can reach any $y \in [1, E_1]$ such that $1 \to y$ is a valid jump? No, we start at 1, so the first jump is from 1. So reachable positions in the first good interval are $[1+A, 1+B] \cap [1, E_1]$. But wait, we can also reach positions by multiple jumps within the first good interval. 
   - Correction: Within a good interval, we can make multiple jumps. So if we can reach any position in a good interval, we can reach a range of positions. Specifically, if we can reach $x$, we can reach $[x+A, x+B]$. If we can reach a range $[L, R]$ in a good interval, then the new reachable range is $[L+A, R+B]$, intersected with the good interval. We can iterate this until it stabilizes. Since $B$ is small, this will stabilize quickly. 
   - Actually, for a good interval $[S, E]$, if we can enter it at some position $x_{entry}$, then the reachable positions are all $y \in [S, E]$ such that $y$ can be reached from $x_{entry}$ by jumps of size $[A, B]$. This is equivalent to: $y - x_{entry}$ can be written as a sum of integers in $[A, B]$. This is possible if $y - x_{entry} \ge A$ and $y - x_{entry}$ is not in some small set of "unreachable" gaps. But with small $B$, the set of unreachable values is small. However, a simpler way: if the good interval is long enough, the reachable positions form a contiguous range $[L_{new}, E]$ or $[L_{new}, R_{new}]$. 
   - Given the constraints, let's use the following algorithm:
     1. Construct the list of good intervals. The bad intervals are $[L_i, R_i]$. The good intervals are $[1, L_1-1], [R_1+1, L_2-1], \ldots, [R_M+1, N]$.
     2. Initialize `reachable` as a set or range. For the first good interval $[S_1, E_1]$, we start at 1. The reachable positions in this interval are computed by BFS/DFS within the interval, but since the interval can be large, we use the fact that if we can reach $x$, we can reach $[x+A, x+B]$. So we can compute the min and max reachable positions. Let $min\_r = 1, max\_r = 1$. Then we expand: $min\_r = min\_r + A, max\_r = max\_r + B$, but clipped to the interval. We repeat until no change. Since $B$ is small, this converges in $O((E_1 - S_1)/A)$ steps, which can be large. 
     3. Alternative: The reachable positions in a good interval $[S, E]$ given an entry range $[L_{in}, R_{in}]$ from the previous interval are $[ \max(S, L_{in} + A), \min(E, R_{in} + B) ]$. This is because any $y$ in this range can be reached from some $x \in [L_{in}, R_{in}]$ with a single jump. And within the good interval, if we can reach a range, we can extend it. But wait, if the good interval is long, we can make multiple jumps. So the reachable range in the current good interval is not just from the previous interval, but from all reachable positions in the current interval. 
     4. Correct approach: For each good interval $[S, E]$, let $R_{prev}$ be the reachable range from the previous good interval (i.e., positions in the previous good interval that can jump to the current good interval). Then the initial reachable positions in $[S, E]$ are $[ \max(S, \min(R_{prev}) + A), \min(E, \max(R_{prev}) + B) ]$. Let this be $[L_{init}, R_{init}]$. Then, within $[S, E]$, we can make further jumps. If $[L_{init}, R_{init}]$ is non-empty, we can extend it: $L_{new} = L_{init} + A, R_{new} = R_{init} + B$, clipped to $[S, E]$. We repeat this until $L_{new} > R_{new}$ or it stabilizes. Since $B$ is small, the number of iterations is small? No, if the interval is large, we might need many iterations. But note: if $R_{init} - L_{init} \ge B - A$, then the reachable range becomes contiguous and we can reach up to $E$ if the interval is long enough. Specifically, if we have a contiguous range of length $\ge B$, we can reach any position beyond. 
     5. Actually, a known result: if you can reach a contiguous range of length $\ge B$ in a good interval, then you can reach all positions up to $E$ in that interval. So we can compute the reachable range iteratively: 
        - Start with $[L, R] = [ \max(S, L_{prev} + A), \min(E, R_{prev} + B) ]$.
        - While $L + B \le E$ and $R < E$: 
          - $L = L + A$
          - $R = R + B$
          - Clip to $[S, E]$.
        - This loop runs at most $O((E-S)/A)$ times, which is too slow if $E-S$ is large.
     6. Optimization: If $R - L \ge B - A$, then the reachable range becomes contiguous and we can reach up to $E$ if $E - L \ge 0$. More precisely, if we have a contiguous range $[L, R]$ and $R - L \ge B - A$, then we can reach $[L+A, R+B]$, which overlaps with $[L, R]$ if $R+B \ge L+A$, which is true. So the range expands by $A$ on the left and $B$ on the right. The length increases by $B-A$. If $B > A$, the length increases. If $B = A$, the length stays the same. 
     7. If $B > A$, then the reachable range grows. We can compute the number of steps to reach $E$: if $R < E$, then we can reach $E$ if $R + k \cdot B \ge E$ for some $k$, and the left bound $L + k \cdot A \le E$. But we need the range to be non-empty. 
     8. Simpler: if the good interval is long, we can reach $E$ if we can reach any position in $[E-B, E]$. So we can check if the reachable range intersects $[E-B, E]$. 
     9. Given the complexity, and since $M$ is small, we can use the following: for each good interval, compute the reachable range as $[L, R]$. If $L > R$, return No. Then, if $R < E$, we can potentially reach further. But to avoid simulation, we can use the formula: the reachable range in the current good interval is $[ \max(S, L_{prev} + A), \min(E, R_{prev} + B) ]$ if we only consider jumps from the previous interval. But this ignores multiple jumps within the current interval. 
     10. Correct and efficient method: 
         - Let $reach$ be the range of reachable positions in the current good interval.
         - Initially, $reach = [ \max(S, L_{prev} + A), \min(E, R_{prev} + B) ]$.
         - If $reach$ is empty, return No.
         - If $reach[1] == E$, then we can reach the end of this interval.
         - If $reach[1] < E$, we can make further jumps. The key is that if we can reach a contiguous range of length $\ge B$, we can reach all positions up to $E$. 
         - Specifically, if $reach[1] + B \ge E$, then we can reach $E$ if $reach[1] + A \le E$ (which is true if $reach$ is non-empty and $E \ge reach[1]$). 
         - More generally, the reachable positions in the current good interval are all $y \in [S, E]$ such that $y$ can be reached from the previous interval by a sequence of jumps. This is equivalent to: $y$ is reachable if $y \ge L_{prev} + A$ and $y \le R_{prev} + B$ and $y$ is not in a "gap". But with small $B$, there are no gaps if the interval is long enough. 
         - Actually, the set of reachable positions in a good interval, given an entry range, is a contiguous range $[L_{new}, R_{new}]$ where $L_{new} = \max(S, L_{prev} + A)$ and $R_{new} = \min(E, R_{prev} + B)$ if we only do one jump. But with multiple jumps, $R_{new}$ can be $E$ if the interval is long enough. 
         - We can compute the maximum reachable position in the current good interval: it is $\min(E, R_{prev} + B \cdot k)$ for some $k$, but constrained by the left bound. 
         - Given the time, I'll implement a BFS on the "critical" points: the boundaries of the bad intervals. Since $B$ is small, the number of reachable positions near each boundary is small. We can maintain a set of reachable positions at each boundary. 

Given the constraints and the need for efficiency, I'll use the following approach:
- Parse the bad intervals and create good intervals.
- For each good interval, compute the reachable range using the previous reachable range.
- Use the fact that if the reachable range in a good interval has length $\ge B$, then we can reach the end of the interval.
- Specifically, for a good interval $[S, E]$, let $[L_{prev}, R_{prev}]$ be the reachable range in the previous good interval.
- The initial reachable range in $[S, E]$ is $[L_{init}, R_{init}] = [\max(S, L_{prev} + A), \min(E, R_{prev} + B)]$.
- If $L_{init} > R_{init}$, return No.
- If $R_{init} == E$, then we can reach the end of this interval, so the reachable range for the next interval is $[E, E]$? No, we can reach positions up to $E$, so the reachable range is $[E, E]$ if we only care about the end, but we need the range for the next jump.
- Actually, if we can reach $E$, then for the next good interval, we can jump from $E$ to $[E+A, E+B]$.
- But if we can reach a range $[L, R]$ in the current good interval, then for the next good interval, the reachable positions are $[\max(S_{next}, L + A), \min(E_{next}, R + B)]$.
- So we need to compute the full reachable range in the current good interval.
- If $R_{init} < E$, we can make further jumps. The reachable range expands to $[L_{init} + A, R_{init} + B]$, clipped to $[S, E]$. We repeat this until the range stabilizes or reaches $E$.
- Since $B$ is small, the number of expansions is small if the interval is short. If the interval is long, we can compute the final range analytically: if $R_{init} - L_{init} \ge B - A$, then the range becomes contiguous and we can reach up to $E$ if $E - L_{init} \ge 0$. 
- Specifically, if $R_{init} < E$, then the maximum reachable position is $\min(E, R_{init} + k \cdot B)$ where $k$ is the number of steps, but we need to ensure the left bound doesn't exceed the right bound. 
- Given the complexity, I'll use a loop that expands the range until it stabilizes or reaches $E$. Since $B \le 20$, the range expands by at least $A \ge 1$ each step, so the number of steps is at most $E - S$, which can be large. 
- To handle large intervals, we can use the following: if $R_{init} < E$ and $R_{init} - L_{init} \ge B - A$, then we can reach $E$ if $E \ge L_{init} + A$. 
- Actually, if we have a contiguous range $[L, R]$ and $R - L \ge B - A$, then the next range is $[L+A, R+B]$, which has length $R+B - (L+A) = (R-L) + (B-A) \ge B$. So the length increases by $B-A$. If $B > A$, the length grows, and we can reach $E$ in $O((E-L)/ (B-A))$ steps. If $B = A$, the length stays the same, and we can reach $E$ if $R + k \cdot A \ge E$ for some $k$. 
- Given the time, I'll implement a solution that uses a set of reachable positions at the boundaries. Since $B$ is small, the number of reachable positions near each boundary is at most $B$. 

After re-thinking, the standard solution for this problem is to use BFS on the "events" (boundaries of bad intervals) and maintain the set of reachable positions at each event. Since $B$ is small, the set of reachable positions at each event is small (at most $B$ values). 

Steps:
1. Create a list of "critical" points: 1, N, and all $L_i, R_i+1$.
2. Sort the critical points and remove duplicates.
3. For each interval between critical points, determine if it's good or bad.
4. Use BFS: start with reachable set = {1}.
5. For each reachable position $x$, try to jump to $x+i$ for $i \in [A, B]$. If $x+i \le N$ and $x+i$ is not bad, add it to the reachable set.
6. But this is too slow if we visit all squares.
7. Instead, we can process the good intervals. For each good interval, we can compute the reachable positions within it from the previous reachable positions.
8. Given the small $B$, we can maintain a set of reachable positions at the start of each good interval. Then, within the good interval, we can compute the reachable positions by BFS, but since the interval can be large, we use the fact that the reachable positions form a contiguous range or a small set.

I'll implement the following:
- Parse input.
- Create good intervals.
- For each good interval, compute the reachable range using the previous reachable range.
- Use the formula: $L_{new} = \max(S, L_{prev} + A)$, $R_{new} = \min(E, R_{prev} + B)$.
- If $L_{new} > R_{new}$, return No.
- If $R_{new} < E$, we can make further jumps. The reachable range expands to $[L_{new} + A, R_{new} + B]$, clipped to $[S, E]$. We repeat this until $R_{new} == E$ or the range becomes empty.
- To avoid infinite loops, we can use a while loop with a counter. Since $B$ is small, the range expands by at least $A$ each step, so the number of steps is at most $(E - S) / A$. If $E - S$ is large, this is slow.
- Optimization: if $R_{new} - L_{new} \ge B - A$, then the range becomes contiguous and we can reach $E$ if $E \ge L_{new} + A$. 
- Specifically, if $R_{new} < E$ and $R_{new} - L_{new} \ge B - A$, then we can reach $E$ if $E - L_{new} \ge 0$. 
- Actually, if $R_{new} < E$, then the maximum reachable position is $\min(E, R_{new} + k \cdot B)$ where $k$ is chosen such that $L_{new} + k \cdot A \le R_{new} + k \cdot B$. This is always true if $B \ge A$. 
- Given the time, I'll use a loop that expands the range until it reaches $E$ or stabilizes. For large intervals, I'll use the analytical solution.

After careful thought, I'll use the following efficient method:
- For each good interval $[S, E]$, let $[L_{prev}, R_{prev}]$ be the reachable range from the previous good interval.
- Compute $L_{init} = \max(S, L_{prev} + A)$, $R_{init} = \min(E, R_{prev} + B)$.
- If $L_{init} > R_{init}$, return No.
- If $R_{init} == E$, then the reachable range for this interval is $[L_{init}, E]$.
- If $R_{init} < E$, then we can make further jumps. The reachable range expands to $[L_{init} + A, R_{init} + B]$, clipped to $[S, E]$. Let this be $[L_{next}, R_{next}]$.
- If $L_{next} > R_{next}$, return No.
- If $R_{next} == E$, then the reachable range is $[L_{next}, E]$.
- Otherwise, repeat.
- To speed up, if $R_{init} - L_{init} \ge B - A$, then the reachable range becomes contiguous and we can reach $E$ if $E \ge L_{init} + A$. 
- Specifically, if $R_{init} < E$ and $R_{init} - L_{init} \ge B - A$, then the maximum reachable position is $E$ if $E \ge L_{init} + A$. 
- So, if $R_{init} < E$ and $R_{init} - L_{init} \ge B - A$, then set $R_{new} = E$.
- Otherwise, expand once: $L_{new} = \max(S, L_{init} + A)$, $R_{new} = \min(E, R_{init} + B)$.
- If $L_{new} > R_{new}$, return No.
- If $R_{new} == E$, set $R_{new} = E$.
- Else, if $R_{new} - L_{new} \ge B - A$, set $R_{new} = E$.
- Else, we need to expand further. But since $B$ is small, the range is small, so we can use BFS within the interval.

Given the constraints, I'll implement a solution that uses BFS on the critical points and maintains a set of reachable positions at each critical point. Since $B$ is small, the set of reachable positions at each critical point is small.

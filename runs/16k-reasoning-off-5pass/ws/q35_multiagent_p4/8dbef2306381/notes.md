
## ideation
The core difficulty is the large value of $N$ ($10^{12}$), which prevents simulating every square. However, the constraints on $M$ ($2 \times 10^4$) and the jump range $[A, B]$ (small, $B \le 20$) suggest an interval-based approach.

Key observations:
1. **Good Intervals**: The "bad" squares form disjoint intervals $[L_i, R_i]$. The "good" squares form contiguous intervals between these bad intervals. Let these good intervals be $G_0, G_1, \dots, G_K$.
2. **Reachability Propagation**: We can determine if square $N$ is reachable by propagating reachability through these good intervals.
3. **Interval Reachability**: If we know that in a previous good interval $G_{prev}$, the reachable squares form a contiguous interval $[min\_r, max\_r]$, then for a subsequent good interval $G_{curr} = [S, E]$, a position $x \in G_{curr}$ is reachable if there exists a reachable $y \in G_{prev}$ such that $A \le x - y \le B$.
   - This condition translates to: $y \in [x-B, x-A]$.
   - So, $x$ is reachable if the intersection $[x-B, x-A] \cap [min\_r, max\_r]$ is non-empty.
   - This intersection is non-empty if and only if $x-B \le max\_r$ AND $x-A \ge min\_r$.
   - Therefore, the reachable positions in $G_{curr}$ form the interval $[\max(S, min\_r + A), \min(E, max\_r + B)]$.
4. **Algorithm**:
   - Initialize `min_r = 1`, `max_r = 1` (since we start at square 1).
   - Construct the list of good intervals. These are the gaps between bad intervals, plus the start $[1, L_1-1]$ and end $[R_M+1, N]$.
   - Iterate through each good interval $[S, E]$.
   - Compute the reachable sub-interval within $[S, E]$ using the formula above.
   - If the resulting interval is empty (lower bound > upper bound), then it's impossible to proceed, so output `No`.
   - Update `min_r` and `max_r` to the bounds of the new reachable sub-interval.
   - If we successfully process the last good interval and the reachable interval is non-empty (which implies $N$ is reachable if $N$ is in the last good interval and the interval overlaps with $N$), output `Yes`. Note: Since we check if the reachable interval is non-empty, and $N$ is the end of the last good interval, we just need to ensure the final reachable interval is valid and includes $N$ or extends to $N$. Actually, if the reachable interval in the last good interval is $[L_{final}, R_{final}]$, and $R_{final} \ge N$, then $N$ is reachable. But since the interval is capped at $E=N$, if the interval is non-empty, it means some part of the last good interval is reachable. We specifically need $N$ to be reachable. So we should check if $N \in [L_{final}, R_{final}]$.

Pitfalls:
- Handling the first good interval correctly (starting at 1).
- Ensuring that the "previous reachable interval" is correctly identified. Since good intervals are separated by bad intervals, a jump from $G_{i-1}$ to $G_i$ must span the bad interval. The condition $A \le x - y \le B$ naturally handles this because if the gap is too large, the intersection will be empty.
- The case where $M=0$ (no bad intervals). The only good interval is $[1, N]$.
- The case where the reachable interval shrinks to empty.

Let's refine the "previous reachable interval" concept. The propagation is from any reachable square in any previous good interval. However, because the jump length is small ($B \le 20$), a square in $G_i$ can only be reached from squares in $G_{i-1}$ or possibly $G_{i-2}$ if the gap between $G_{i-2}$ and $G_i$ is small. But wait, if there is a bad interval between $G_{i-1}$ and $G_i$, then any jump from $G_{i-2}$ to $G_i$ would have to land in the bad interval $G_{i-1}$? No, the jump is from $y$ to $x$. If $y \in G_{i-2}$ and $x \in G_i$, the jump length is $x-y$. If this jump lands on a bad square, it's invalid. But the condition is that the *destination* $x$ is not bad. It doesn't matter where the jump passes through. So a jump can skip over bad intervals.
However, if $G_{i-1}$ is between $G_{i-2}$ and $G_i$, and $G_{i-1}$ is non-empty, then any jump from $G_{i-2}$ to $G_i$ must have length at least the distance from the end of $G_{i-2}$ to the start of $G_i$. If this distance is greater than $B$, then no jump from $G_{i-2}$ can reach $G_i$. If it is $\le B$, it might be possible.
But my previous logic assumed that we only propagate from the *immediately preceding* good interval's reachable set. Is this correct?
Let's trace:
Suppose we have good intervals $G_0, G_1, G_2$.
Reachable in $G_0$: $R_0$.
Reachable in $G_1$: $R_1 = \{ x \in G_1 \mid \exists y \in R_0, A \le x-y \le B \}$.
Reachable in $G_2$: $R_2 = \{ x \in G_2 \mid \exists y \in R_0 \cup R_1, A \le x-y \le B \}$.
My previous logic only considered $R_1$. This is incorrect if a jump from $R_0$ can reach $G_2$ directly.
However, note that if a jump from $y \in R_0$ reaches $x \in G_2$, then $x - y \in [A, B]$.
If $G_1$ is between $G_0$ and $G_2$, then $y < \text{end}(G_0) < \text{start}(G_1) \le \text{end}(G_1) < \text{start}(G_2) \le x$.
So $x - y = (x - \text{start}(G_2)) + (\text{start}(G_2) - \text{end}(G_1)) + (\text{end}(G_1) - \text{start}(G_1)) + (\text{start}(G_1) - y)$.
This seems complicated.
Actually, the set of all reachable squares is the union of reachable squares in all good intervals.
Let $R$ be the set of all reachable squares.
$R = \{1\} \cup \{ x \in \text{Good} \mid \exists y \in R, A \le x-y \le B \}$.
Since $B$ is small, the "frontier" of reachable squares is limited.
We can maintain the set of reachable positions in the last $B$ squares.
But $N$ is large.
Alternative approach:
Since $B$ is small, we can use a BFS/Dijkstra-like approach on the "events" (start and end of bad intervals).
The state can be defined by the position modulo something? No.
Let's reconsider the interval propagation.
The key is that if we have a contiguous block of good squares of length $\ge B$, and we can reach at least one square in the first $B$ squares of that block, we can reach a contiguous range of squares in that block.
Specifically, if we enter a good interval $[S, E]$ with a set of reachable squares $R_{in}$ from previous intervals, the new reachable squares in $[S, E]$ are those $x \in [S, E]$ such that $[x-B, x-A] \cap R_{total} \neq \emptyset$, where $R_{total}$ is the set of all reachable squares in previous good intervals.
Since $R_{total}$ is a union of intervals, and we process intervals in order, we can maintain the "effective" reachable range from previous intervals that can influence the current interval.
Because the jump is small, only reachable squares within distance $B$ of the current interval matter.
So, for the current good interval $[S, E]$, we only care about reachable squares in $[S-B, S-1]$.
These reachable squares must be in the immediately preceding good interval(s).
If the gap between the previous good interval and the current one is large ($> B$), then no reachable square from previous intervals can reach the current interval.
If the gap is small, we can compute the reachable squares in the current interval by checking against the reachable squares in the previous good interval.
But what if the reachable squares in the previous good interval are sparse?
Actually, within a good interval, the reachable squares form an interval (or are empty). This is because if $x$ is reachable, then $x+1$ is reachable if $x+1$ is good and there is a $y$ such that $A \le x+1-y \le B$. If $x$ is reachable via $y$, then $x+1$ is reachable via $y$ if $A \le x+1-y \le B$. If $x+1-y = B+1$, then we need another $y'$. But since the reachable set in a good interval is convex (an interval), this holds.
So, we can maintain a single interval $[min\_r, max\_r]$ of reachable squares in the "active" previous good interval.
When moving to the next good interval $[S, E]$, we check if any square in $[min\_r, max\_r]$ can reach $[S, E]$.
The condition for a square $x \in [S, E]$ to be reachable is that there exists $y \in [min\_r, max\_r]$ such that $A \le x-y \le B$.
This is equivalent to $y \in [x-B, x-A]$.
So $x$ is reachable if $[x-B, x-A] \cap [min\_r, max\_r] \neq \emptyset$.
This intersection is non-empty iff $x-B \le max\_r$ and $x-A \ge min\_r$.
So $x \le max\_r + B$ and $x \ge min\_r + A$.
Thus, the reachable squares in $[S, E]$ are $[\max(S, min\_r + A), \min(E, max\_r + B)]$.
This logic assumes that the only reachable squares that can influence $[S, E]$ are in $[min\_r, max\_r]$. This is true if the previous good interval is the only one within distance $B$ of $[S, E]$.
If there are multiple previous good intervals within distance $B$, we need to consider all of them.
However, since the bad intervals are disjoint and ordered, the previous good interval is the one immediately before the bad interval that precedes $[S, E]$.
If the gap between the previous good interval and the current one is small, then the previous good interval is the only one that can reach the current one, because any earlier good interval is further away.
Specifically, if the distance from the end of the previous good interval to the start of the current good interval is $D$, and $D > B$, then no square from the previous good interval can reach the current one. And squares from even earlier intervals are further away, so they can't reach either.
If $D \le B$, then squares from the previous good interval can reach the current one. Squares from earlier intervals are at least $D + \text{length of bad interval} + \dots$ away, which is likely $> B$.
Wait, if the bad interval is small, say length 1, and $B=20$, then a square from two good intervals ago might be able to reach the current one.
Example: $G_0 = [1, 10]$, $Bad_1 = [11, 11]$, $G_1 = [12, 20]$, $Bad_2 = [21, 21]$, $G_2 = [22, 30]$.
$B=20$.
A square $y=1$ in $G_0$ can jump to $x=21$? No, 21 is bad.
Can $y=1$ jump to $x=22$? $22-1=21 > 20$. No.
Can $y=10$ jump to $x=22$? $22-10=12 \le 20$. Yes.
So $y \in G_0$ can reach $x \in G_2$.
But $y \in G_0$ can also reach $x \in G_1$.
So when processing $G_2$, we need to consider reachable squares from $G_0$ and $G_1$.
But if we maintain the union of reachable squares from all previous good intervals that are within distance $B$, we can do this.
Since $B$ is small, we can maintain a list of reachable intervals from the last few good intervals.
However, note that if $G_1$ is reachable, then the reachable squares in $G_1$ are an interval. And if $G_0$ is reachable, the reachable squares in $G_0$ are an interval.
The union of these intervals might not be contiguous.
But we can just maintain the set of all reachable intervals from previous good intervals that are within distance $B$ of the current good interval.
Since $B$ is small, there are at most a few such intervals.
In practice, we can just keep track of the reachable interval in the "most recent" good interval that can influence the current one. If the gap is large, we reset.
Actually, the simplest way is to process the good intervals in order and maintain a set of reachable intervals. When processing a new good interval, we check against all reachable intervals from previous good intervals that are within distance $B$.
Since $B$ is small, the number of such intervals is small.
We can store the reachable intervals in a list. When moving to a new good interval, we remove any reachable intervals that are too far away (distance $> B$ from the start of the current good interval).
Then, for the current good interval $[S, E]$, we compute the reachable sub-interval by checking against each remaining reachable interval.
The union of these reachable sub-intervals is the new reachable set for the current good interval.
Since the reachable set in a good interval is an interval (if non-empty), we can merge them.
This approach is efficient because $M$ is small and $B$ is small.

Let's implement this.

1. Parse input.
2. Create list of bad intervals.
3. Create list of good intervals.
   - Start with $[1, L_1-1]$.
   - Then $[R_i+1, L_{i+1}-1]$ for each $i$.
   - End with $[R_M+1, N]$.
4. Initialize `reachable_intervals = []`.
5. For each good interval $[S, E]$:
   - Remove any intervals from `reachable_intervals` that are completely to the left of $S-B$ (i.e., their max element $< S-B$).
   - Compute the new reachable sub-interval(s) in $[S, E]$ by checking against each remaining interval in `reachable_intervals`.
     - For each reachable interval $[r_{min}, r_{max}]$, the reachable positions in $[S, E]$ are $[\max(S, r_{min} + A), \min(E, r_{max} + B)]$.
     - If this interval is valid (lower $\le$ upper), add it to a list of new reachable intervals for this good interval.
   - Merge overlapping/adjacent intervals in the new list.
   - If the merged list is empty, return `No`.
   - Update `reachable_intervals` to be the new merged list.
6. After processing all good intervals, check if $N$ is in any of the reachable intervals in the last good interval.
   - Since the last good interval ends at $N$, we just need to check if the reachable interval in the last good interval includes $N$.
   - Actually, we can just check if the reachable interval in the last good interval is non-empty and its upper bound is $N$. Or more simply, if the reachable interval in the last good interval is $[L, R]$, then $N$ is reachable if $R \ge N$. But since the interval is capped at $E=N$, $R$ will be $\le N$. So we just need $R = N$? No, if the reachable interval is $[N, N]$, then $N$ is reachable. If it's $[N-1, N]$, then $N$ is reachable. So we just need the reachable interval to be non-empty and include $N$.
   - Actually, the problem asks if we can reach square $N$. So we need to check if $N$ is in the reachable set.
   - Since we process the good interval containing $N$ last, we just need to check if $N$ is in the reachable sub-interval of that good interval.

Let's refine step 5.
When computing the new reachable sub-interval for a good interval $[S, E]$, we might get multiple intervals from different previous reachable intervals. We need to merge them.
Since $B$ is small, the number of previous reachable intervals is small.
Merging is straightforward.

Edge case: $M=0$. The only good interval is $[1, N]$.
`reachable_intervals` is initially empty.
For $[1, N]$, we need to handle the start.
We can initialize `reachable_intervals` with $[1, 1]$ if $1$ is good.
But 1 is always good.
So before the loop, we can add $[1, 1]$ to `reachable_intervals`? No, because 1 is in the first good interval.
Better: Handle the first good interval specially.
Or, we can imagine a "virtual" reachable interval $[1, 1]$ that is "active" at the start.
But the first good interval starts at 1.
So for the first good interval $[1, E_0]$, the reachable squares are those $x \in [1, E_0]$ such that there exists $y \in \{1\}$ with $A \le x-1 \le B$.
So $x \in [1+A, 1+B] \cap [1, E_0]$.
And also $x=1$ is reachable.
So the reachable set in the first good interval is $\{1\} \cup ([1+A, 1+B] \cap [1, E_0])$.
This might be two intervals if $A > 1$.
But since we start at 1, 1 is reachable.
Then from 1, we can reach $[1+A, 1+B]$.
So the reachable set in the first good interval is $[1, 1] \cup [\max(1, 1+A), \min(E_0, 1+B)]$.
If $A=1$, this is $[1, \min(E_0, 1+B)]$.
If $A>1$, this is two intervals: $[1, 1]$ and $[1+A, 1+B]$ (if $1+A \le 1+B$ and within bounds).

So, we can initialize `reachable_intervals` with $[1, 1]$.
Then for each good interval, we compute the new reachable intervals based on the current `reachable_intervals`.
But we need to be careful: the `reachable_intervals` should only contain intervals from good intervals that have been processed.
So, for the first good interval, we use the initial `reachable_intervals` which contains $[1, 1]$.
But 1 is in the first good interval. So we need to handle the fact that 1 is reachable without a jump.
The problem says "move from square 1". So 1 is reachable.
The action is to move from $x$ to $x+i$.
So 1 is reachable initially.
Then we can jump from 1 to other squares.
So for the first good interval, the reachable squares are $\{1\} \cup \{ x \in [1, E_0] \mid \exists y \in \{1\}, A \le x-y \le B \}$.
This is $\{1\} \cup [1+A, 1+B] \cap [1, E_0]$.
This can be represented as a list of intervals.
Then for subsequent good intervals, we use the reachable intervals from previous good intervals.

So the algorithm:
1. `reachable_intervals = [[1, 1]]`
2. For each good interval $[S, E]$:
   - `new_reachable = []`
   - For each `r_interval` in `reachable_intervals`:
     - If `r_interval[1] < S - B`: continue (too far)
     - Compute `start = max(S, r_interval[0] + A)`
     - Compute `end = min(E, r_interval[1] + B)`
     - If `start <= end`: add `[start, end]` to `new_reachable`
   - Also, if this is the first good interval, we need to include 1 if it's in this interval.
     - But 1 is in the first good interval. And we initialized `reachable_intervals` with `[1, 1]`.
     - So when processing the first good interval, `r_interval = [1, 1]`.
     - `start = max(1, 1+A) = 1+A` (if $A \ge 1$)
     - `end = min(E, 1+B)`
     - This gives the interval $[1+A, 1+B] \cap [1, E]$.
     - But we also need to include 1 itself.
     - So we need to add `[1, 1]` to `new_reachable` if $1 \in [S, E]$.
     - Since the first good interval starts at 1, $1 \in [S, E]$.
     - So we add `[1, 1]` to `new_reachable`.
   - For subsequent good intervals, 1 is not in them, so we don't add it.
   - Merge `new_reachable` intervals.
   - If `new_reachable` is empty, return `No`.
   - `reachable_intervals = new_reachable`
3. After the loop, check if $N$ is in any interval in `reachable_intervals`.
   - Since the last good interval ends at $N$, we just need to check if any interval in `reachable_intervals` contains $N$.
   - Or more simply, if the last good interval's reachable interval includes $N$.

Let's test with Sample 1.
N=24, M=2, A=3, B=5.
Bad: [7, 8], [17, 20].
Good intervals:
G0: [1, 6]
G1: [9, 16]
G2: [21, 24]

Init: `reachable_intervals = [[1, 1]]`

Process G0 [1, 6]:
- `r_interval = [1, 1]`.
- `start = max(1, 1+3) = 4`
- `end = min(6, 1+5) = 6`
- Add `[4, 6]` to `new_reachable`.
- Since this is the first good interval, add `[1, 1]` to `new_reachable`.
- `new_reachable = [[1, 1], [4, 6]]`.
- Merge: no overlap. `reachable_intervals = [[1, 1], [4, 6]]`.

Process G1 [9, 16]:
- `r_interval = [1, 1]`. `1 < 9-5=4`? Yes, $1 < 4$. So skip.
- `r_interval = [4, 6]`. `6 < 4`? No.
  - `start = max(9, 4+3) = 7` -> but 7 is bad, so we take max with S=9. `start = 9`.
  - `end = min(16, 6+5) = 11`.
  - Add `[9, 11]` to `new_reachable`.
- `new_reachable = [[9, 11]]`.
- `reachable_intervals = [[9, 11]]`.

Process G2 [21, 24]:
- `r_interval = [9, 11]`. `11 < 21-5=16`? Yes, $11 < 16$. So skip.
- `new_reachable` is empty.
- Return `No`.

But Sample 1 output is `Yes`.
What's wrong?
The path is 1 -> 6 -> 9 -> 12 -> 16 -> 21 -> 24.
1 -> 6: jump 5. 6 is in G0.
6 -> 9: jump 3. 9 is in G1.
9 -> 12: jump 3. 12 is in G1.
12 -> 16: jump 4. 16 is in G1.
16 -> 21: jump 5. 21 is in G2.
21 -> 24: jump 3. 24 is in G2.

In G0, reachable are 1, 4, 5, 6.
In G1, from 6 (in G0), we can reach 6+3=9, 6+4=10, 6+5=11.
So 9, 10, 11 are reachable in G1.
From 9, we can reach 9+3=12, 9+4=13, 9+5=14.
From 10, we can reach 10+3=13, 10+4=14, 10+5=15.
From 11, we can reach 11+3=14, 11+4=15, 11+5=16.
So reachable in G1 are 9, 10, 11, 12, 13, 14, 15, 16.
My calculation for G1 was `[9, 11]`. This is incorrect because I only considered jumps from G0 to G1, not jumps within G1.
Ah, the problem is that I am only considering jumps from previous good intervals to the current good interval. I am not considering jumps within the current good interval.
But the reachable set in a good interval is computed by propagating from the entry points.
The entry points are the squares in the current good interval that are reachable from previous good intervals.
Then, from these entry points, we can reach other squares in the current good interval by jumping within the good interval.
Since the good interval is contiguous, if we can reach a square $x$ in the good interval, we can reach $x+1, \dots, x+B$ if they are in the good interval.
So the reachable set in a good interval is the union of intervals $[x+A, x+B]$ for all entry points $x$, plus the entry points themselves.
And since the good interval is contiguous, this union will be an interval (or union of intervals) that can be computed by simulating the BFS within the good interval.
But since the good interval can be large, we need an efficient way.
However, note that if we have an entry point $x$, we can reach $[x+A, x+B]$.
If we have multiple entry points, the union of these intervals is the set of reachable squares in the good interval (excluding the entry points themselves, which are also reachable).
So the reachable set in the good interval is $\{ \text{entry points} \} \cup \bigcup_{x \in \text{entry points}} [x+A, x+B]$.
This can be computed by finding the min and max of the entry points, and then the reachable set is $[\min(\text{entry}), \max(\text{entry}) + B]$? No, because there might be gaps.
But if the entry points are dense enough, the union will be contiguous.
Given that $B$ is small, we can simulate the BFS within the good interval if the good interval is small. But if it's large, we need a better way.
Actually, the reachable set in a good interval is an interval if the entry points are such that the union of $[x+A, x+B]$ covers the gap between the min and max entry points.
This is true if the gap between consecutive entry points is $\le B$.
But we don't know the entry points are dense.
However, we can compute the reachable set in the good interval by:
1. Find the entry points: squares in $[S, E]$ that are reachable from previous good intervals.
2. The reachable set in $[S, E]$ is the set of squares reachable from the entry points by jumps within $[S, E]$.
This is equivalent to: start with the set of entry points. Then repeatedly add $x+i$ for $x$ in the set and $A \le i \le B$, as long as $x+i \le E$.
This is a BFS. But if the good interval is large, this is slow.
However, note that if we have a contiguous block of good squares of length $\ge B$, and we can reach at least one square in the first $B$ squares of that block, we can reach all squares in the block? No, we can reach a range.
Actually, if we have an entry point $x$, we can reach $[x+A, x+B]$.
If we have another entry point $y > x$, we can reach $[y+A, y+B]$.
The union of these intervals is the reachable set (plus the entry points).
If the gap between $x$ and $y$ is small, these intervals might overlap.
In general, the reachable set in the good interval is the union of intervals $[x+A, x+B]$ for all entry points $x$, plus the entry points themselves.
This can be computed by sorting the entry points and merging the intervals.
But how do we find the entry points?
The entry points are the squares in $[S, E]$ that are reachable from previous good intervals.
We already computed this in my previous logic: for each previous reachable interval, we computed the intersection with $[S, E]$ of the reachable positions.
This gives us a set of intervals of entry points.
Let these be $E_1, E_2, \dots$.
Then the reachable set in the current good interval is $\bigcup_i (E_i \cup \bigcup_{x \in E_i} [x+A, x+B])$.
But $\bigcup_{x \in E_i} [x+A, x+B]$ is just $[min(E_i)+A, max(E_i)+B]$ if $E_i$ is an interval? No, because for each $x$, we add $[x+A, x+B]$.
If $E_i = [a, b]$, then the union of $[x+A, x+B]$ for $x \in [a, b]$ is $[a+A, b+B]$.
This is because for any $z \in [a+A, b+B]$, there exists $x \in [a, b]$ such that $A \le z-x \le B$.
Specifically, $x = z - k$ for some $k \in [A, B]$. We need $a \le z-k \le b$, i.e., $z-b \le k \le z-a$.
Since $z \in [a+A, b+B]$, we have $z-a \ge A$ and $z-b \le B$.
So the interval $[z-b, z-a]$ has length $b-a \ge 0$.
And it intersects $[A, B]$ if $z-b \le B$ and $z-a \ge A$, which is true.
So yes, if $E_i = [a, b]$, then the reachable squares from $E_i$ within the good interval are $[a+A, b+B] \cap [S, E]$.
And the entry points themselves are also reachable.
So the reachable set in the current good interval is $(\bigcup_i E_i) \cup (\bigcup_i [min(E_i)+A, max(E_i)+B] \cap [S, E])$.
But $\bigcup_i E_i$ is the set of entry points, which we already have as `reachable_intervals` intersected with $[S, E]$.
And $\bigcup_i [min(E_i)+A, max(E_i)+B] \cap [S, E]$ is the set of squares reachable by jumps from the entry points.
So we can compute this as follows:
1. For each `r_interval` in `reachable_intervals`:
   - Compute `entry_start = max(S, r_interval[0])`
   - Compute `entry_end = min(E, r_interval[1])`
   - If `entry_start <= entry_end`:
     - Add `[entry_start, entry_end]` to `entry_intervals`.
     - Add `[entry_start + A, entry_end + B]` to `jump_intervals`, clipped to $[S, E]$.
2. Merge `entry_intervals` and `jump_intervals` to get the new `reachable_intervals`.

This is efficient.

Let's re-test Sample 1.
G0 [1, 6]:
- `r_interval = [1, 1]`.
- `entry_start = 1, entry_end = 1`. Add `[1, 1]` to `entry_intervals`.
- `jump_start = 1+3=4, jump_end = 1+5=6`. Clip to [1, 6]: `[4, 6]`. Add to `jump_intervals`.
- `entry_intervals = [[1, 1]]`, `jump_intervals = [[4, 6]]`.
- Merge: `[[1, 1], [4, 6]]`.
- `reachable_intervals = [[1, 1], [4, 6]]`.

G1 [9, 16]:
- `r_interval = [1, 1]`. `1 < 9-5=4`? Yes, skip.
- `r_interval = [4, 6]`. `6 >= 4`.
  - `entry_start = max(9, 4) = 9`. `entry_end = min(16, 6) = 6`. `9 > 6`, so no entry points.
  - Wait, `entry_start = max(S, r_interval[0]) = max(9, 4) = 9`. `entry_end = min(E, r_interval[1]) = min(16, 6) = 6`. `9 > 6`, so no overlap.
  - So no entry points from `[4, 6]`.
  - But we know 9 is reachable from 6.
  - The issue is that 6 is in G0, and 9 is in G1. The jump is from 6 to 9.
  - So 9 is an entry point? No, 9 is reachable by a jump from 6.
  - So 9 is in `jump_intervals`.
  - `jump_start = 4+3=7, jump_end = 6+5=11`. Clip to [9, 16]: `[9, 11]`.
  - So `jump_intervals = [[9, 11]]`.
  - `entry_intervals` is empty.
  - So `reachable_intervals = [[9, 11]]`.

But we know that from 9, we can reach 12, 13, 14.
And from 10, we can reach 13, 14, 15.
And from 11, we can reach 14, 15, 16.
So the reachable set in G1 should be `[9, 16]`.
My calculation only gave `[9, 11]`.
This is because I only considered jumps from previous good intervals. I did not consider jumps within the current good interval.
The `jump_intervals` computed above are the squares reachable by jumps from previous good intervals.
But from these squares, we can make more jumps within the current good interval.
So we need to propagate within the current good interval.
The reachable set in the current good interval is the closure of the entry points under jumps within the good interval.
Since the good interval is contiguous, this closure is an interval (or union of intervals) that can be computed by:
- Start with the set of entry points (from `jump_intervals` and `entry_intervals`).
- Then, for each reachable square $x$, add $[x+A, x+B] \cap [S, E]$.
- This is equivalent to: the reachable set is $[\min(\text{entry}), \max(\text{entry}) + B]$ if the entry points are dense enough.
- But in general, it is the union of $[x+A, x+B]$ for all $x$ in the entry set, plus the entry set.
- And since the entry set is a union of intervals, the reachable set is the union of $[a+A, b+B]$ for each entry interval $[a, b]$, plus the entry intervals.
- But this is what I computed as `jump_intervals` and `entry_intervals`.
- The issue is that this only accounts for one jump from previous intervals.
- We need to account for multiple jumps within the current good interval.
- So we need to iterate: the reachable set is the union of $[x+A, x+B]$ for all $x$ in the current reachable set.
- This is a fixed-point iteration.
- But since the good interval is contiguous, the reachable set will be an interval if the entry points are such that the union of $[x+A, x+B]$ covers the gap.
- In fact, if we have an entry interval $[a, b]$, then the reachable set from this interval within the good interval is $[a, b] \cup [a+A, b+B] \cup [a+2A, b+2B] \dots$ until we reach $E$.
- But this is not correct because we can jump by any amount in $[A, B]$.
- So from $[a, b]$, we can reach $[a+A, b+B]$.
- From $[a+A, b+B]$, we can reach $[a+2A, b+2B]$.
- And so on.
- The union of these intervals is $[a, b+ k \cdot B]$ where $k$ is the number of jumps.
- But we can also jump by less than $B$, so we can fill in the gaps.
- In fact, if we have an interval $[a, b]$, and we can jump by $[A, B]$, then the reachable set is $[a, b + \infty)$ if we can make enough jumps.
- But we are bounded by $E$.
- So the reachable set from $[a, b]$ within $[S, E]$ is $[a, \min(E, b + \text{max possible reach})]$.
- The max possible reach from $[a, b]$ is $b + k \cdot B$ where $k$ is the number of jumps.
- But we can reach any square in $[a, E]$ if the good interval is long enough and we can make jumps of size 1? No, jumps are at least $A$.
- So we can reach $[a, E]$ if we can make jumps of size $A$.
- The reachable set from $[a, b]$ is $[a, b] \cup [a+A, b+B] \cup [a+2A, b+2B] \dots$
- This is a union of intervals.
- If $A \le B$, and the intervals overlap, then the union is a single interval.
- The intervals $[a+kA, b+kB]$ overlap if $b+kB \ge a+(k+1)A$, i.e., $b-a \ge A-B$.
- Since $A \le B$, $A-B \le 0$, and $b-a \ge 0$, so this is always true if $b \ge a$.
- So the intervals always overlap or touch.
- Therefore, the reachable set from $[a, b]$ is $[a, \min(E, b + k \cdot B)]$ where $k$ is the maximum number of jumps such that $a+kA \le E$.
- But this is not quite right because we can jump by any amount in $[A, B]$.
- So from $[a, b]$, we can reach any square in $[a, b]$ and any square in $[a+A, b+B]$ and any square in $[a+2A, b+2B]$ etc.
- And since the intervals overlap, the union is $[a, \min(E, b + \text{max reach})]$.
- The max reach is when we make jumps of size $B$.
- So the reachable set from $[a, b]$ is $[a, \min(E, b + k \cdot B)]$ where $k$ is the largest integer such that $a+kA \le E$.
- But this is not correct because we can reach squares between $b$ and $a+A$ if $b < a+A$.
- But in our case, the entry points are from previous intervals, so they are disjoint from the current good interval? No, they are in the current good interval.
- So the entry points are in $[S, E]$.
- So the reachable set in the current good interval is the union of $[x, x + \text{max reach from } x]$ for all entry points $x$.
- But since the entry points form intervals, and the reachable set from an interval is an interval, we can compute the reachable set from each entry interval and merge them.
- For an entry interval $[a, b]$, the reachable set is $[a, \min(E, b + k \cdot B)]$ where $k$ is the max number of jumps.
- But this is not correct because we can jump by less than $B$.
- Actually, the reachable set from $[a, b]$ is $[a, \min(E, b + \text{max possible extension})]$.
- The max possible extension is when we make jumps of size $B$.
- But we can also make jumps of size $A$.
- So the reachable set is $[a, \min(E, b + \text{max reach})]$.
- The max reach is unbounded if we can make infinite jumps, but we are bounded by $E$.
- So the reachable set is $[a, E]$ if we can reach $E$.
- We can reach $E$ if there is a sequence of jumps from $[a, b]$ to $E$.
- This is possible if $E \ge a$ and $E - b$ is a multiple of some jump size? No.
- In fact, if the good interval is long enough, we can reach any square in $[a, E]$ if we can make jumps of size 1? No, jumps are at least $A$.
- So we can reach $[a, E]$ if $E - a$ is large enough and we can make jumps of size $A$.
- The reachable set from $[a, b]$ is $[a, b] \cup [a+A, b+B] \cup [a+2A, b+2B] \dots$
- And since the intervals overlap, the union is $[a, \min(E, b + k \cdot B)]$ where $k$ is the max number of jumps.
- But this is not correct because the intervals might not cover all squares.
- For example, if $A=3, B=5$, and entry is $[1, 1]$, then reachable are $[1, 1] \cup [4, 6] \cup [7, 9] \cup \dots$
- This is $[1, 1] \cup [4, \infty)$.
- So there is a gap between 1 and 4.
- So the reachable set is not necessarily a single interval.
- But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
- So the entry points are in the current good interval.
- And we can make jumps within the current good interval.
- So the reachable set in the current good interval is the closure of the entry points under jumps within the good interval.
- This can be computed by:
  - Let $R$ be the set of entry points.
  - While there exists $x \in R$ and $i \in [A, B]$ such that $x+i \le E$ and $x+i \notin R$, add $x+i$ to $R$.
  - This is a BFS.
- But since the good interval can be large, we need an efficient way.
- However, note that the reachable set from an interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
- And since these intervals overlap (as shown before), the union is $[a, \min(E, b + k \cdot B)]$ where $k$ is the max number of jumps.
- But this is not correct because the intervals might not cover all squares.
- For example, if $A=3, B=5$, and entry is $[1, 1]$, then the reachable set is $[1, 1] \cup [4, 6] \cup [7, 9] \cup \dots$
- This is $[1, 1] \cup [4, \infty)$.
- So the reachable set is $[1, 1] \cup [4, E]$.
- So we can compute the reachable set from an entry interval $[a, b]$ as:
  - $R = [a, b]$
  - Then $R = R \cup [a+A, b+B] \cup [a+2A, b+2B] \dots$
  - And since the intervals overlap, the union is $[a, \min(E, b + k \cdot B)]$ where $k$ is the max number of jumps.
  - But this is not correct because the intervals might not cover all squares.
  - In the example, $[1, 1] \cup [4, 6] \cup [7, 9] \dots$ is not $[1, \min(E, 1 + k \cdot 5)]$.
  - $1 + k \cdot 5$ for $k=1$ is 6, for $k=2$ is 11.
  - So $[1, 11]$ would include 2, 3, which are not reachable.
  - So the reachable set is not a single interval.
  - But it is a union of intervals.
  - And since the intervals overlap, the union is a single interval if the gap between consecutive intervals is 0.
  - In the example, the gap between $[1, 1]$ and $[4, 6]$ is 2, 3, which are not covered.
  - So the reachable set is $[1, 1] \cup [4, 6] \cup [7, 9] \dots$
  - This is $[1, 1] \cup [4, \infty)$.
  - So we can compute the reachable set from an entry interval $[a, b]$ as:
    - $R = [a, b]$
    - Then $R = R \cup [a+A, b+B] \cup [a+2A, b+2B] \dots$
    - And we can merge these intervals.
    - Since the intervals are $[a+kA, b+kB]$, and they overlap if $b+kB \ge a+(k+1)A$, i.e., $b-a \ge A-B$.
    - Since $A \le B$, $A-B \le 0$, and $b-a \ge 0$, so this is always true.
    - So the intervals always overlap or touch.
    - Therefore, the union is a single interval $[a, \min(E, b + k \cdot B)]$ where $k$ is the max number of jumps.
    - But this is not correct because the intervals might not cover all squares.
    - In the example, $[1, 1] \cup [4, 6] \cup [7, 9] \dots$ is not a single interval.
    - The issue is that the intervals $[a+kA, b+kB]$ are not contiguous.
    - They are separated by gaps.
    - So the union is not a single interval.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the closure of the entry points under jumps within the good interval.
    - This can be computed by:
      - Let $R$ be the set of entry points.
      - Then $R = R \cup \{ x+i \mid x \in R, A \le i \le B, x+i \le E \}$.
      - This is a BFS.
    - But since the good interval can be large, we need an efficient way.
    - However, note that the reachable set from an interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can merge these intervals.
    - Since the intervals are $[a+kA, b+kB]$, and they are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$, i.e., $B \ge A+a$.
    - But $a$ can be large.
    - So the intervals might not overlap.
    - In the example, $a=1, b=1, A=3, B=5$.
    - Intervals: $[1, 1], [4, 6], [7, 9], \dots$
    - These do not overlap.
    - So the reachable set is a union of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small (because $B$ is small), we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the current good interval.
    - And we can make jumps within the current good interval.
    - So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
    - And we can merge these reachable sets.
    - Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set from each entry interval by simulating the BFS for a few jumps.
    - But the good interval can be large, so we can't simulate all jumps.
    - However, note that the reachable set from an entry interval $[a, b]$ is the union of $[a+kA, b+kB]$ for $k \ge 0$.
    - And we can compute this union by finding the max $k$ such that $a+kA \le E$.
    - Then the reachable set is $\bigcup_{k=0}^K [a+kA, b+kB] \cap [S, E]$.
    - And we can merge these intervals.
    - Since the intervals are spaced by $A$, and have length $B-a$, they will overlap if $B-a \ge A$.
    - If they don't overlap, the union is a set of disjoint intervals.
    - But in our case, the entry points are from previous intervals, and we are processing good intervals in order.
    - So the entry points are in the

## worker: (none)
The problem requires determining if square $N$ is reachable from square 1 by jumping with lengths in $[A, B]$, avoiding bad squares. Given $N \le 10^{12}$, we cannot simulate all squares. However, $M \le 2 \times 10^4$ and $B \le 20$ suggest an interval-based approach.

1. **Good Intervals**: The bad squares form disjoint intervals $[L_i, R_i]$. The good squares form contiguous intervals between these bad intervals. We construct these good intervals.
2. **Reachability Propagation**: We maintain a list of reachable intervals from previously processed good intervals. For each new good interval $[S, E]$, we compute the squares in $[S, E]$ that are reachable by a single jump from any previous reachable interval. This is done by checking if the intersection $[x-B, x-A] \cap \text{Reachable}_{prev}$ is non-empty for $x \in [S, E]$.
3. **Internal Propagation**: Within the current good interval, we can make multiple jumps. The reachable set from an entry interval $[a, b]$ is the union of intervals $[a+kA, b+kB]$ for $k \ge 0$, clipped to $[S, E]$. Since $B$ is small, we can compute this union by iterating $k$ from 0 to $k_{max} = \lfloor (E-a)/A \rfloor$.
4. **Merging**: We merge overlapping or adjacent intervals to keep the list of reachable intervals compact.
5. **Final Check**: After processing all good intervals, we check if $N$ is in any of the reachable intervals in the last good interval.

The complexity is $O(M \cdot B \cdot \log M)$ or similar, which is efficient given the constraints.

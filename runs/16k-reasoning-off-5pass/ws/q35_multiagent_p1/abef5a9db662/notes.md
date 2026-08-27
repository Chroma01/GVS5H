
## ideation
The core difficulty is that simulating each query independently is $O(NQ)$, which is too slow given $N, Q \le 3 \times 10^5$. The rating at each step depends on previous increments, creating a dependency chain. However, since the maximum possible rating is bounded ($5 \times 10^5$), we can process all possible initial ratings $X \in [1, 500000]$ simultaneously.

The key insight is to track the *distribution* of current ratings. Let `cnt[v]` be the number of initial ratings $X$ that currently have a rating of $v$. Initially, `cnt[v] = 1` for $1 \le v \le 500000$ and 0 otherwise. For each contest $[L_i, R_i]$, all people with current rating $v \in [L_i, R_i]$ get their rating incremented by 1. This means `cnt[v]` people move from rating $v$ to $v+1$.

A naive simulation of moving counts would be $O(N \cdot \max\_R)$, which is too slow. We can optimize this using a Disjoint Set Union (DSU) or a "next pointer" array to skip over empty rating slots. Specifically:
1. Maintain `cnt[v]` for each rating value $v$.
2. Maintain a DSU structure `parent[v]` that points to the next rating value $> v$ that has `cnt > 0`. Initially, `parent[v] = v+1`.
3. For each contest $[L, R]$:
   - Find the first non-empty rating slot $v \ge L$ using DSU: `v = find(L)`.
   - While $v \le R$:
     - Move all people from $v$ to $v+1$: `cnt[v+1] += cnt[v]`, `cnt[v] = 0`.
     - Union $v$ with $v+1$ in DSU so future queries skip $v$.
     - Move to the next non-empty slot: `v = find(v)`.
4. After processing all contests, the final rating for initial $X$ is $X + \text{total increments}$. But wait, we need to know how many times *each specific* $X$ was incremented. The DSU approach above aggregates counts by *current rating value*, not by initial $X$. This loses the mapping from initial $X$ to final rating.

Correction: The DSU approach on `cnt` array tells us the distribution of final ratings, but not which initial $X$ leads to which final rating. We need the function $f(X) = \text{final rating}$.

Alternative correct approach:
Since $f(X)$ is non-decreasing and the maximum rating is small, we can compute $f(X)$ for all $X$ by simulating the process but using a segment tree or similar structure to efficiently find which $X$ fall into $[L_i, R_i]$ at step $i$. However, the condition is on the *current* rating, which changes.

Actually, there is a simpler observation: The final rating for initial $X$ is $X + \sum_{i=1}^N [L_i \le \text{rating}_i(X) \le R_i]$. The function $g_i(X) = \text{rating}_i(X)$ is non-decreasing. We can use a segment tree over the domain of initial ratings $X \in [1, 500000]$ where each leaf stores the current rating of that $X$. For each contest $[L, R]$, we want to find all leaves with value in $[L, R]$ and increment them. This can be done with a segment tree that supports "range increment for leaves with value in $[L, R]$". This is a known technique using a segment tree where each node stores the min and max value in its range. If the node's max $< L$ or min $> R$, skip. If the node's min $\ge L$ and max $\le R$, increment the whole range (lazy propagation). Otherwise, recurse. This is $O(N \log (\max\_R))$ because each leaf is incremented at most $N$ times, but the structure ensures we don't visit too many nodes.

Given the constraints and complexity, the segment tree approach is feasible.

## worker: (None)
The problem requires determining the final rating for multiple initial ratings $X$ after $N$ contests. A direct simulation per query is $O(NQ)$, which is too slow. The key insight is that the function $h(X) = \text{current rating for initial } X$ is non-decreasing. This allows us to use a segment tree to maintain $h(X)$ for all $X \in [1, 500000]$.

For each contest $[L, R]$, the set of initial ratings $X$ that get incremented is an interval $[A, B]$ because $h(X)$ is non-decreasing. Specifically:
- $A$ is the smallest $X$ such that $h(X) \ge L$.
- $B$ is the largest $X$ such that $h(X) \le R$.

We can find $A$ and $B$ efficiently using the segment tree's min/max values and binary search-like traversal in $O(\log (\max\_R))$ time. Once $A$ and $B$ are found, we perform a range update on the segment tree to increment $h(X)$ by 1 for all $X \in [A, B]$. This range update uses lazy propagation for efficiency.

The total complexity is $O(N \log (\max\_R) + Q)$, which fits well within the time limits.

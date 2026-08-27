The problem asks for the final rating after $N$ contests for $Q$ different initial ratings. Since the rating only increases and the condition for each contest is a range check, the number of times a rating increases is simply the count of ranges $[L_i, R_i]$ that contain the current rating. Because the rating only grows, we can simulate the process by iterating through the contests, but doing this naively for each query is too slow ($O(N \cdot Q)$). Instead, we can observe that the total increase for a starting rating $X$ is the sum of increments gained at each step. This can be modeled as a dynamic process where we track the "active" ranges. A more efficient approach is to realize that the final rating is $X + \text{count of intervals covering the current value}$. However, since the current value changes, we need a way to quickly calculate the total increments. We can use a difference array or a segment tree approach. Specifically, we can process the intervals to determine how many times a specific rating value is covered across the sequence of contests, but the "coverage" depends on the current rating which is dynamic. 

Actually, a simpler observation is that the total increase is the number of times the current rating falls into $[L_i, R_i]$. Since the rating only increases by 1, the path of the rating is monotonic. We can precompute the answer for all possible initial ratings up to the maximum constraint ($5 \times 10^5$) using dynamic programming or a sweep-line algorithm. Let $dp[v]$ be the final rating starting with $v$. Then $dp[v] = v + \sum_{i=1}^N \mathbb{I}(v + \text{increments so far} \in [L_i, R_i])$. This dependency on "increments so far" makes direct DP hard.

Alternative approach: The final rating is $X + \text{total increments}$. The total increments is the number of indices $i$ such that the rating at step $i$ is in $[L_i, R_i]$. Let $f(X)$ be the final rating. Note that $f(X) = X + \text{count}$. The count depends on the trajectory.
Let's reconsider the constraints. $N, Q, \text{max\_val} \approx 5 \times 10^5$. We can compute the answer for all $X$ in one pass.
Let $ans[x]$ be the final rating starting at $x$.
We can simulate the process for all $x$ simultaneously.
Let $current\_rating[x]$ be the rating of a person who started at $x$ at step $k$. Initially $current\_rating[x] = x$.
At step $i$ with range $[L_i, R_i]$, if $L_i \le current\_rating[x] \le R_i$, then $current\_rating[x] \leftarrow current\_rating[x] + 1$.
This looks like we are shifting values. If we maintain a data structure of current ratings for all starting positions, we can update them.
However, notice that if $current\_rating[x] < L_i$, it stays same. If $> R_i$, it stays same. If inside, it increments.
This is equivalent to: $new\_rating[x] = old\_rating[x] + 1$ if $L_i \le old\_rating[x] \le R_i$, else $old\_rating[x]$.
We can process the queries offline or precompute for all $X$. Since the max value is small ($5 \times 10^5$), we can iterate $X$ from $1$ to $500000$. But simulating $N$ steps for each $X$ is $O(N \cdot \max\_X)$, which is $2.5 \times 10^{11}$, too slow.

We need a faster way. Notice that the operation is: add 1 to all $v$ such that $L_i \le v \le R_i$. But the set of $v$ changes because $v$ increases.
Wait, the condition is on the *current* rating.
Let's reverse the thinking. Or use a difference array on the "potential" increments.
Actually, this problem can be solved by realizing that the total increase for a starting value $X$ is the number of intervals $[L_i, R_i]$ that the trajectory passes through.
Let's try a different perspective. The final rating is $X + \text{total\_increments}$.
Can we compute the total increments for all $X$ efficiently?
Yes. We can use a segment tree or a difference array approach over the range of ratings.
Let $diff[v]$ be the number of times a rating $v$ is incremented. But a rating $v$ at step $i$ comes from some starting value $X$.
Actually, we can simulate the process on the array of starting values.
Let $A$ be an array where $A[x] = x$.
For each contest $i$ with $[L_i, R_i]$:
  For all $x$, if $L_i \le A[x] \le R_i$, then $A[x]++$.
This is hard to do efficiently because the condition depends on the current value of $A[x]$.
However, note that if $A[x]$ is in $[L_i, R_i]$, it becomes $A[x]+1$. If it was in $[L_i, R_i-1]$, it might move out.
Key Insight: The relative order of starting values is preserved. $A[x] < A[y]$ implies $A[x]_{new} < A[y]_{new}$.
Also, the values only increase.
We can process the contests. For a contest $[L, R]$, we want to increment all $A[x]$ that are currently in $[L, R]$.
Since $A$ is sorted, the indices $x$ such that $A[x] \in [L, R]$ form a contiguous range of indices.
We can find the range of indices $[idx_{start}, idx_{end}]$ such that $A[idx_{start}] \ge L$ and $A[idx_{end}] \le R$. Then increment $A[x]$ for all $x$ in this range.
Since we have $N$ contests, and each contest might take $O(\log N)$ to find the range and $O(\text{range\_size})$ to update, worst case is still bad.
BUT, we can use a segment tree with lazy propagation. The segment tree will store the current rating for each starting position $x \in [1, 500000]$.
Initially, leaf $x$ has value $x$.
For each contest $[L, R]$:
  Query the segment tree to find the range of indices $[l, r]$ such that values in leaves $l \dots r$ are in $[L, R]$.
  Apply lazy update: add 1 to range $[l, r]$.
  Wait, finding the range of indices whose values are in $[L, R]$ on a segment tree storing values is possible. We can traverse the tree. If a node's min value $> R$, ignore. If max value $< L$, ignore. Otherwise, recurse. If a node is fully within $[L, R]$ (i.e., min $\ge L$ and max $\le R$), then we apply the lazy +1 and stop.
  This is a standard "range add, range query min/max" problem where we dynamically find the sub-ranges to update.
  Complexity: Each contest takes $O(\log (\max\_X))$ if we only visit nodes that need splitting? No, in the worst case we might visit many nodes.
  However, notice that we only care about the final values.
  Actually, there is a simpler observation. The total increase for a starting value $X$ is the number of times the trajectory hits an interval.
  Let's reconsider the constraints and the nature of the update.
  Is it possible to solve this with a difference array?
  Let $cnt[v]$ be the number of contests where the rating is exactly $v$. No, that's not right.
  
  Let's go back to the segment tree idea. It is $O(N \log (\max\_X))$ if implemented correctly?
  Actually, we can just use a difference array approach on the *values*.
  Let $dp[v]$ be the final rating starting at $v$.
  Consider the process in reverse? No.
  
  Let's try the segment tree approach again. It is robust.
  Max value $M = 500000$.
  Build a segment tree over $[1, M]$. Each leaf $i$ stores value $i$.
  Each node stores `min_val` and `max_val` of the range covered.
  For each contest $[L, R]$:
    Find all leaves with values in $[L, R]$.
    Since the tree is sorted by value (initially), and we only add 1, the relative order is preserved.
    So the set of indices with values in $[L, R]$ is always a contiguous range of indices?
    Yes! Because if $A[i] \in [L, R]$ and $A[j] \in [L, R]$ with $i < j$, then for any $k$ with $i < k < j$, $A[i] \le A[k] \le A[j]$ implies $A[k] \in [L, R]$.
    So we just need to find the smallest index $l$ such that $A[l] \ge L$ and the largest index $r$ such that $A[r] \le R$.
    Then we add 1 to all $A[k]$ for $k \in [l, r]$.
    Since $A$ is sorted, we can use binary search (or `lower_bound`/`upper_bound`) to find $l$ and $r$.
    Then we perform a range add on the array $A$.
    Wait, if we just maintain the array $A$ and do range adds, finding $l$ and $r$ requires knowing the current values.
    If we use a Fenwick tree or Segment Tree to maintain the array $A$ (initially $A[i]=i$), we can support:
    1. Range Add $(l, r, +1)$
    2. Find smallest index $l$ such that $A[l] \ge L$.
    3. Find largest index $r$ such that $A[r] \le R$.
    
    With a Segment Tree supporting range add and range minimum/maximum (or just finding the first element $\ge L$), we can do this.
    Specifically, to find the first index $l$ with $A[l] \ge L$:
      Traverse the segment tree. If a node's max value $< L$, skip. If a node's min value $\ge L$, this node is a candidate. We want the leftmost.
      Actually, we can just search for the first leaf with value $\ge L$.
      Similarly for $r$: search for the last leaf with value $\le R$.
    Then update range $[l, r]$ by adding 1.
    Complexity: $N$ updates. Each update involves 2 searches ($O(\log M)$) and 1 range update ($O(\log M)$). Total $O(N \log M)$.
    $N = 2 \times 10^5$, $M = 5 \times 10^5$. $\log M \approx 19$. Operations $\approx 4 \times 10^6$, well within time limits (usually $10^8$ ops/sec).
    
    After processing all $N$ contests, the array $A$ will contain the final ratings for all starting values $1 \dots M$. We can answer queries in $O(1)$.
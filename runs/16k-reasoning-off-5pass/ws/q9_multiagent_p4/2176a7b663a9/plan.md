The problem asks for the minimum weight path in a graph where edges connect intervals that do not overlap. This is equivalent to finding the shortest path in a graph where adjacency is defined by the "non-overlapping" condition. Since $N$ and $Q$ are up to $2 \times 10^5$, we cannot build the graph explicitly ($O(N^2)$ edges). We need to identify connected components and find shortest paths within them. The "non-overlapping" relation is transitive in a specific way via a third interval, but more importantly, the complement graph (overlapping intervals) often forms a structure where connected components can be found using a sweep-line algorithm or by processing intervals sorted by their endpoints. Specifically, if two intervals overlap, they are not connected directly, but they belong to the same "cluster" of overlapping intervals. The graph $G$ connects nodes in different clusters. However, a simpler observation is that if we sort intervals by $R_i$, we can efficiently determine reachability. Actually, the standard approach for "intervals that do not intersect" shortest path is to realize that the graph is the complement of the intersection graph. The intersection graph of intervals is an interval graph. The connected components of the complement of an interval graph can be found by sorting intervals by $R_i$ and using a set to track active intervals. For shortest path queries, if $s$ and $t$ are in different connected components of $G$, output -1. If they are in the same component, the shortest path usually involves at most 2 or 3 hops due to the structure of interval graphs (specifically, if $s$ and $t$ don't overlap, they might connect directly; if not, they might connect via a node that overlaps with neither, or via a chain). Wait, the condition is: edge $(i, j)$ exists if $[L_i, R_i] \cap [L_j, R_j] = \emptyset$.
Let's re-evaluate the connectivity. If we sort intervals by $R_i$, we can process them. Two intervals $i$ and $j$ are connected if $R_i < L_j$ or $R_j < L_i$.
The key insight for this specific problem (AtCoder ABC 313 F or similar difficulty) is that the graph $G$ is connected if the union of all intervals covers a range? No.
Actually, the connected components of $G$ (non-overlapping graph) correspond to the connected components of the "overlap" graph's complement.
A known property: In the graph where edges are non-overlapping intervals, the connected components can be determined by sorting intervals by $R_i$. If we sort by $R_i$, we can maintain a set of "active" intervals that haven't been "closed" yet.
However, a more robust approach for shortest path with weights:
1. Determine connected components. If $s$ and $t$ are in different components, answer -1.
2. If in the same component, the shortest path is likely very short (length 1 or 2).
   - Length 1: Direct edge ($R_s < L_t$ or $R_t < L_s$). Cost $W_s + W_t$.
   - Length 2: Path $s \to k \to t$. This requires an interval $k$ that does not overlap $s$ and does not overlap $t$.
   - Is length 3 ever needed? In interval graphs, the diameter of the complement graph is small. Specifically, if $s$ and $t$ are connected, there is often a path of length at most 2 or 3.
   Actually, let's consider the structure. If we sort intervals by $R_i$, we can find the "gap" between $s$ and $t$.
   If $s$ and $t$ overlap, no direct edge.
   If they don't overlap, direct edge.
   If they overlap, we need an intermediate $k$. We need $k$ such that $[L_k, R_k] \cap [L_s, R_s] = \emptyset$ and $[L_k, R_k] \cap [L_t, R_t] = \emptyset$.
   This means $R_k < L_s$ (and $R_t < L_k$ impossible if $s,t$ overlap? No).
   Case 1: $s$ and $t$ are disjoint. Edge exists.
   Case 2: $s$ and $t$ overlap. We need $k$ disjoint from both.
   The condition "disjoint from both" means $k$ is either completely to the left of both, or completely to the right of both, or in a gap between them (if they don't cover the whole line).
   Since $s$ and $t$ overlap, their union is a single interval $[\min(L_s, L_t), \max(R_s, R_t)]$.
   Any $k$ disjoint from both must satisfy $R_k < \min(L_s, L_t)$ or $L_k > \max(R_s, R_t)$.
   So we just need to check if there exists any interval $k$ with $R_k < \min(L_s, L_t)$ or $L_k > \max(R_s, R_t)$.
   If such a $k$ exists, the shortest path is $\min(W_s+W_k+W_t)$ over all such $k$.
   Is it possible we need 3 hops? Suppose $s$ and $t$ overlap. We need $k$ disjoint from both. If no such $k$ exists, can we go $s \to u \to v \to t$?
   If no $k$ is disjoint from both $s$ and $t$, then every interval overlaps at least one of $s$ or $t$.
   This implies that the union of intervals overlapping $s$ and the union of intervals overlapping $t$ covers all other nodes.
   However, in the context of interval graphs, if $s$ and $t$ are in the same connected component of the complement graph, and there is no node disjoint from both, does a path exist?
   Actually, if $s$ and $t$ overlap, and there is no node disjoint from both, then $s$ and $t$ might still be connected via a chain.
   Example: $s=[1, 10], t=[5, 15]$. No node can be $<1$ or $>15$. But maybe $u=[2, 3]$ (overlaps $s$), $v=[12, 13]$ (overlaps $t$). $u$ and $v$ are disjoint? $[2,3] \cap [12,13] = \emptyset$. Yes. So $s \to u \to v \to t$?
   Wait, $s$ and $u$ overlap, so NO edge. Edge exists only if disjoint.
   So $s$ connects to $u$ only if $s \cap u = \emptyset$.
   If $s=[1,10]$ and $u=[2,3]$, they overlap, so NO edge.
   So $s$ can only connect to nodes strictly to its left or strictly to its right.
   Similarly for $t$.
   If $s$ and $t$ overlap, say $s=[1,10], t=[5,15]$.
   $s$ connects to $k$ if $R_k < 1$ or $L_k > 10$.
   $t$ connects to $k$ if $R_k < 5$ or $L_k > 15$.
   To go $s \to k \to t$:
   $k$ must be disjoint from $s$ AND disjoint from $t$.
   Disjoint from $s \implies R_k < 1$ or $L_k > 10$.
   Disjoint from $t \implies R_k < 5$ or $L_k > 15$.
   Intersection of conditions:
   1. $R_k < 1$ (satisfies both).
   2. $L_k > 15$ (satisfies both).
   3. $R_k < 1$ and $L_k > 15$ (impossible).
   4. $L_k > 10$ and $R_k < 5$ (impossible).
   So the only candidates for $k$ are those with $R_k < \min(L_s, L_t)$ or $L_k > \max(R_s, R_t)$.
   Thus, if $s$ and $t$ overlap, a path of length 2 exists IF AND ONLY IF there is a node to the far left or far right.
   What if no such node exists? Then $s$ and $t$ are not connected?
   Let's trace: $s$ can only reach nodes $L > R_s$ or $R < L_s$.
   $t$ can only reach nodes $L > R_t$ or $R < L_t$.
   If $s$ and $t$ overlap, the set of neighbors of $s$ is $N(s) = \{k \mid R_k < L_s\} \cup \{k \mid L_k > R_s\}$.
   The set of neighbors of $t$ is $N(t) = \{k \mid R_k < L_t\} \cup \{k \mid L_k > R_t\}$.
   Since $s, t$ overlap, $L_t < R_s$ and $L_s < R_t$.
   Then $N(s) \cap N(t) = (\{R_k < L_s\} \cap \{R_k < L_t\}) \cup (\{R_k < L_s\} \cap \{L_k > R_t\}) \cup (\{L_k > R_s\} \cap \{R_k < L_t\}) \cup (\{L_k > R_s\} \cap \{L_k > R_t\})$.
   Since $L_s < R_t$ and $L_t < R_s$:
   - $R_k < L_s \implies R_k < L_t$ (since $L_s < R_t$ doesn't imply $L_s < L_t$, wait. Overlap means $L_t \le R_s$ and $L_s \le R_t$. It does NOT imply $L_s < L_t$ or vice versa.
   Let's assume $L_s \le L_t$. Then overlap implies $L_t \le R_s$.
   Then $L_s \le L_t \le R_s \le R_t$.
   $N(s) = \{R_k < L_s\} \cup \{L_k > R_s\}$.
   $N(t) = \{R_k < L_t\} \cup \{L_k > R_t\}$.
   Intersection:
   - $R_k < L_s$: Since $L_s \le L_t$, $R_k < L_s \implies R_k < L_t$. So this set is in $N(t)$.
   - $L_k > R_t$: Since $R_s \le R_t$, $L_k > R_t \implies L_k > R_s$. So this set is in $N(s)$.
   - Cross terms: $R_k < L_s$ and $L_k > R_t$? Impossible since $L_s \le R_t$.
   - Cross terms: $L_k > R_s$ and $R_k < L_t$? Impossible since $R_s \ge L_t$.
   So $N(s) \cap N(t) = \{k \mid R_k < L_s\} \cup \{k \mid L_k > R_t\}$.
   These are exactly the nodes disjoint from both.
   If this intersection is empty, then $s$ and $t$ have no common neighbor.
   Can they be connected via a path of length 3? $s \to u \to v \to t$.
   $u \in N(s)$, $v \in N(t)$. We need $u, v$ connected ($u \cap v = \emptyset$).
   $u$ is either far left ($R_u < L_s$) or far right ($L_u > R_s$).
   $v$ is either far left ($R_v < L_t$) or far right ($L_v > R_t$).
   If $u$ is far left and $v$ is far left: $R_u < L_s \le L_t \le R_v$? No, $R_v < L_t$. So $R_u < L_s$ and $R_v < L_t$. They are both far left. Are they disjoint? Not necessarily. But if they are disjoint, we have a path.
   However, if there are NO nodes far left or far right (i.e., the union of all intervals covers $(-\infty, \infty)$ effectively, or at least covers the gap between $s$ and $t$), then $N(s)$ and $N(t)$ are empty?
   If $N(s)$ is empty, $s$ is isolated.
   If $N(s)$ is not empty but $N(s) \cap N(t)$ is empty, we need $u \in N(s), v \in N(t)$ such that $u, v$ are disjoint.
   If all nodes in $N(s)$ are "far left" and all nodes in $N(t)$ are "far left", then any $u, v$ are both far left. Do they overlap? Maybe.
   But note: if there is a node $u$ far left ($R_u < L_s$) and a node $v$ far left ($R_v < L_t$), then $u$ and $v$ are both to the left of $s$ and $t$.
   If $u$ and $v$ overlap, we can't go $s \to u \to v \to t$.
   However, if there is ANY node $u$ far left and ANY node $v$ far right, then $u$ and $v$ are disjoint (since $R_u < L_s \le L_t < R_t < L_v$). So $s \to u \to v \to t$ works.
   If there are no far right nodes, then all neighbors are far left.
   If there are no far left nodes, then all neighbors are far right.
   If there are no far left AND no far right nodes, then $N(s)$ and $N(t)$ are empty, so $s$ and $t$ are isolated.
   So, if $s$ and $t$ overlap, they are connected iff there exists a node far left OR a node far right?
   Wait, if there is a node far left ($u$) and a node far left ($v$) that are disjoint from each other?
   If $u, v$ are both far left, $R_u < L_s$ and $R_v < L_t$.
   If $u$ and $v$ are disjoint, then $s \to u \to v \to t$ is a path.
   But if $u$ and $v$ overlap, we can't use them directly.
   However, if there are multiple nodes far left, can we chain them?
   Actually, the set of intervals far left forms an interval graph itself. If they are connected, we can reach any far left node from any other far left node?
   But we need to connect $s$ to $t$.
   If $N(s) \cap N(t) = \emptyset$, we need $u \in N(s), v \in N(t)$ with $u \cap v = \emptyset$.
   If all $N(s)$ are far left and all $N(t)$ are far left, then $u, v$ are both far left.
   If the set of far left nodes is connected (in the non-overlapping sense), then we can go $s \to u \to \dots \to v \to t$.
   But wait, if $u, v$ are far left, they are to the left of $s$.
   The condition "disjoint" for far left nodes is just standard interval disjointness.
   However, there is a simpler logic:
   If $s$ and $t$ overlap, they are connected if and only if there is a path.
   Given the constraints and problem type, it is highly likely that if $s$ and $t$ are in the same component, the shortest path is either 1 (disjoint), 2 (common neighbor), or 3 (via two disjoint intermediates).
   But actually, if $s$ and $t$ overlap, and there is no common neighbor, can they be connected?
   Yes, if there are two disjoint nodes $u, v$ such that $u$ is disjoint from $s$ and $v$ is disjoint from $t$.
   Since $s, t$ overlap, $u$ must be far left or far right of $s$. $v$ must be far left or far right of $t$.
   If $u$ is far left and $v$ is far right, they are disjoint. Path length 3.
   If $u, v$ both far left, they might overlap. If they don't, path length 3.
   If they overlap, we might need more hops.
   BUT, notice that if there are multiple far left nodes, they form a chain?
   Actually, the critical realization for this problem (based on similar CP problems) is:
   1. Sort intervals by $R_i$.
   2. The graph $G$ (non-overlapping) has connected components that can be identified.
   3. For shortest path:
      - Check direct edge ($O(1)$).
      - Check common neighbor ($O(\log N)$ or $O(1)$ with precalc).
      - Check path of length 3 ($s \to u \to v \to t$). This requires $u$ disjoint from $s$, $v$ disjoint from $t$, $u$ disjoint from $v$.
        Since $s, t$ overlap, $u$ must be $< \min(L_s, L_t)$ or $> \max(R_s, R_t)$. Same for $v$.
        If we pick $u$ far left and $v$ far right, they are always disjoint.
        So if there exists at least one far left node and one far right node, we have a path of length 3.
        What if only far left nodes exist? Then we need two disjoint far left nodes.
        What if only far right nodes exist? Then we need two disjoint far right nodes.
        What if neither? Then no path.
   
   Algorithm:
   1. Precompute min_weight_far_left and min_weight_far_right.
      - Far left: $R_i < \min(L_s, L_t)$.
      - Far right: $L_i > \max(R_s, R_t)$.
      - Actually, we need the minimum weight of any node in the "far left" region and "far right" region.
      - But the region depends on $s$ and $t$.
      - Better: Sort all intervals by $R_i$.
      - Precompute prefix minimums of $W$ for intervals sorted by $R$. This gives min weight of any interval with $R_i \le X$.
      - Precompute suffix minimums of $W$ for intervals sorted by $L$. This gives min weight of any interval with $L_i \ge Y$.
   2. For each query $(s, t)$:
      - If $s, t$ disjoint: ans = $W_s + W_t$.
      - Else (overlap):
        - Option 2a: Common neighbor.
          Need $k$ such that $R_k < \min(L_s, L_t)$ OR $L_k > \max(R_s, R_t)$.
          Cost = $W_s + W_t + \min(\text{min\_weight}(R < \min(L)), \text{min\_weight}(L > \max(R)))$.
          If no such $k$, this option is $\infty$.
        - Option 2b: Path of length 3 ($s \to u \to v \to t$).
          Requires $u$ disjoint from $s$, $v$ disjoint from $t$, $u$ disjoint from $v$.
          Candidates for $u$: Far Left of $s$ ($R_u < L_s$) or Far Right of $s$ ($L_u > R_s$).
          Candidates for $v$: Far Left of $t$ ($R_v < L_t$) or Far Right of $t$ ($L_v > R_t$).
          Since $s, t$ overlap, $L_s \le R_t$ and $L_t \le R_s$.
          Pairs $(u, v)$:
          1. $u$ Far Left ($R_u < L_s$), $v$ Far Right ($L_v > R_t$).
             Since $L_s \le R_t$, $R_u < L_s \le R_t < L_v \implies R_u < L_v$. Disjoint!
             Cost: $W_s + W_t + \min(W_u \text{ s.t. } R_u < L_s) + \min(W_v \text{ s.t. } L_v > R_t)$.
          2. $u$ Far Left ($R_u < L_s$), $v$ Far Left ($R_v < L_t$).
             Need $u, v$ disjoint. Since both are far left, we need two disjoint intervals in the set $\{k \mid R_k < \min(L_s, L_t)\}$.
             This is equivalent to: does the set of intervals with $R < \min(L_s, L_t)$ contain at least two disjoint intervals?
             If yes, we can pick the two with minimum weights? Not necessarily. We need $\min(W_u + W_v)$ where $u, v$ disjoint.
             This subproblem is: given a set of intervals, find min sum of weights of two disjoint intervals.
             This can be solved by sorting by $R$ and using DP or a segment tree, but here the set is defined by a threshold.
             Actually, if we have a set of intervals, the minimum sum of two disjoint ones is $\min( \min_{u} (W_u + \min_{v: R_v < L_u} W_v), \min_{v} (W_v + \min_{u: R_u < L_v} W_v) )$.
             Basically, we need the minimum weight of a pair of disjoint intervals within the "far left" pool.
             Let $M_1 = \min \{ W_k \mid R_k < X \}$.
             Let $M_2 = \min \{ W_k + W_j \mid R_k < L_j < X \}$.
             We can precompute for every possible $X$ (coordinate) the min weight of a single interval and min weight of a pair of disjoint intervals to the left of $X$.
             Similarly for the "far right" pool ($L > Y$).
          3. $u$ Far Right, $v$ Far Right. Similar to case 2.
          4. $u$ Far Left, $v$ Far Right (Case 1) is always valid if both pools are non-empty.
   
   So the strategy:
   - Coordinate compression or just use the values $L_i, R_i$ since they are up to $2N$.
   - Sort intervals by $R$.
   - Precompute `min_single_left[x]` = min $W_k$ such that $R_k < x$.
   - Precompute `min_pair_left[x]` = min $W_u + W_v$ such that $R_u < L_v < x$ (i.e., two disjoint intervals both to the left of $x$).
     - To compute `min_pair_left[x]`: Iterate $x$ from 1 to max_coord.
     - Maintain a list of intervals added as $R$ increases.
     - Actually, simpler: `min_pair_left[x]` is the min sum of two disjoint intervals in the set $\{k \mid R_k < x\}$.
     - We can compute this by iterating $x$ and adding intervals with $R_k = x-1$ to a data structure that maintains the min weight of a single interval and the min weight of a pair.
     - Data structure: Just keep `min1` (min weight) and `min2` (min weight of a pair).
     - When adding interval $k$ with weight $w$:
       - New pair can be formed with existing `min1`: $w + \text{min1}$.
       - Update `min1 = min(min1, w)`.
       - Update `min2 = min(min2, w + \text{old_min1})`.
     - Wait, we need to ensure disjointness. If we add intervals sorted by $R$, any interval $k$ added later has $R_k \ge$ previous $R$'s.
     - If we process intervals sorted by $R$, when we consider a threshold $X$, all intervals with $R < X$ are processed.
     - Among these, we want two disjoint ones.
     - If we sort all intervals by $R$, then for any two intervals $u, v$ with $R_u \le R_v$, they are disjoint iff $R_u < L_v$.
     - So, as we iterate through sorted intervals, we maintain the minimum weight of a single interval seen so far (`best_single`).
     - For current interval $v$ (with $L_v, R_v$), we can form a pair with any previous $u$ if $R_u < L_v$.
     - But we need the global min over all pairs in the set $\{k \mid R_k < X\}$.
     - This is slightly tricky because the condition $R_u < L_v$ depends on $v$.
     - Alternative: The set of intervals with $R < X$ is fixed. We want $\min (W_u + W_v)$ s.t. $R_u < L_v$ and $R_v < X$.
     - Since $R_u < L_v$ implies $R_u < R_v$ (usually), we can just iterate.
     - Actually, we can precompute `min_pair_left[x]` for all relevant $x$.
     - Let's define `dp[x]` = min sum of two disjoint intervals in $\{k \mid R_k < x\}$.
     - We can compute this by sweeping $x$.
     - Maintain a Fenwick tree or Segment tree over $L$ coordinates?
     - Or simpler: Just sort intervals by $R$.
     - `min_pair_left[x]` is the answer for threshold $x$.
     - As we increase $x$, we add intervals with $R = x-1$.
     - For the new interval $k$, it can pair with any previous interval $j$ if $R_j < L_k$.
     - We need $\min (W_j)$ for $j$ with $R_j < L_k$.
     - We can maintain a data structure that stores $W_j$ for all processed intervals, and supports query "min $W_j$ where $R_j < Y$".
     - Since we process by $R$, the condition $R_j < L_k$ is naturally satisfied for all $j$ processed before $k$ IF $L_k > R_j$.
     - But we need to query based on $L_k$.
     - So: Sort intervals by $R$.
     - Iterate $i$ from 1 to $N$. Let current interval be $u_i$.
     - Query min $W_j$ among $j < i$ such that $R_{u_j} < L_{u_i}$.
     - Update global `min_pair` with $W_{u_i} + \text{query\_result}$.
     - Also update `min_single` with $W_{u_i}$.
     - Store the results in an array indexed by $R_{u_i}$.
     - Then fill the gaps.
     - This gives us `min_pair_left[x]` for all $x$.
   - Similarly for `min_pair_right[x]` (intervals with $L > x$).
     - Sort by $L$ descending? Or just symmetric logic.
     - Condition: $L_u > R_v$ (for $u, v$ disjoint, both far right).
     - We need two intervals with $L > Y$ that are disjoint.
     - Symmetric to left case.
   - Finally, for each query:
     - If disjoint: $W_s + W_t$.
     - Else:
       - $opt1 = \infty$.
       - Check single common neighbor: $k$ with $R_k < \min(L_s, L_t)$ or $L_k > \max(R_s, R_t)$.
         - $c1 = \text{min\_single\_left}[\min(L_s, L_t)]$.
         - $c2 = \text{min\_single\_right}[\max(R_s, R_t)]$.
         - If $c1 \neq \infty$, $opt1 = \min(opt1, W_s + W_t + c1)$.
         - If $c2 \neq \infty$, $opt1 = \min(opt1, W_s + W_t + c2)$.
       - $opt2 = \infty$.
       - Check path length 3:
         - Case A: $u$ far left of $s$, $v$ far right of $t$.
           - $cost = W_s + W_t + \text{min\_single\_left}[L_s] + \text{min\_single\_right}[R_t]$.
           - Update $opt2$.
         - Case B: $u, v$ both far left.
           - Need two disjoint in $\{k \mid R_k < \min(L_s, L_t)\}$.
           - $cost = W_s + W_t + \text{min\_pair\_left}[\min(L_s, L_t)]$.
           - Update $opt2$.
         - Case C: $u, v$ both far right.
           - Need two disjoint in $\{k \mid L_k > \max(R_s, R_t)\}$.
           - $cost = W_s + W_t + \text{min\_pair\_right}[\max(R_s, R_t)]$.
           - Update $opt2$.
       - Result = $\min(opt1, opt2)$. If $\infty$, -1.
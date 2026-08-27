The problem can be modeled using prefix sums of road strengths. Let $P_i$ be the cumulative sum of strengths from road 1 to road $i$, with $P_0 = 0$. The stamina of a person traveling from $S$ to $T$ (assuming $S < T$) at town $k$ ($S < k < T$) is $P_{k-1} - P_{S-1}$. The condition that stamina is 0 at start/end and positive in between translates to:
1. $P_{S-1} = P_{T-1}$ (since stamina at $T$ is $P_{T-1} - P_{S-1} = 0$).
2. For all $k$ such that $S \le k < T$, $P_{k-1} > P_{S-1}$. This implies $P_j > P_{S-1}$ for all $j \in [S-1, T-2]$. Note that at $j=T-1$, $P_{T-1} = P_{S-1}$, so the strict inequality only applies to intermediate nodes. Specifically, for towns $S+1, \dots, T-1$, the stamina is positive. Town $S+1$ corresponds to edge $S$, so stamina is $w_S = P_S - P_{S-1}$. Thus $P_S > P_{S-1}$. Generally, $P_j > P_{S-1}$ for $S \le j \le T-2$? No, let's re-verify.
   - Start at $S$: Stamina 0.
   - Arrive at $S+1$: Stamina $w_S = P_S - P_{S-1}$. Must be $>0 \implies P_S > P_{S-1}$.
   - Arrive at $k$ ($S < k < T$): Stamina $P_{k-1} - P_{S-1}$. Must be $>0 \implies P_{k-1} > P_{S-1}$.
   - Arrive at $T$: Stamina $P_{T-1} - P_{S-1} = 0 \implies P_{T-1} = P_{S-1}$.
   So, for $S < T$, we require $P_{S-1} = P_{T-1}$ and $P_j > P_{S-1}$ for all $j \in [S, T-2]$. Wait, the last intermediate town is $T-1$. The stamina at town $T-1$ is $P_{T-2} - P_{S-1}$. So we need $P_j > P_{S-1}$ for $j \in [S, T-2]$. And $P_{T-1} = P_{S-1}$.
   If $S > T$, the path is backwards. Stamina at town $k$ is $P_{S-1} - P_{k-1}$. Conditions: $P_{S-1} = P_{T-1}$ and $P_{k-1} < P_{S-1}$ for $k \in (T, S)$. This means $P_j < P_{S-1}$ for $j \in [T-1, S-2]$.

This structure suggests that each person imposes constraints on the relative order of values in the prefix sum array $P$. Specifically, it defines a "valley" or "peak" shape.
We can model this as a 2-SAT or difference constraints problem, but with $Q$ queries, we need a faster approach.
Notice that the constraints are local. We can determine for each pair of people if they are compatible. Two people are incompatible if their constraints on the same road segments conflict.
Specifically, if two paths overlap, their "height" requirements relative to their endpoints must be consistent.
A key observation is that the conditions can be mapped to checking if a certain graph of dependencies has a cycle or contradiction.
However, a more efficient way for range queries is to use a Segment Tree or similar structure to maintain consistency.
Actually, this problem is equivalent to checking if a set of intervals with "minimum height" constraints can be satisfied.
Let's define the constraint for person $i$ as: $P_{S_i-1} = P_{T_i-1}$ and $\min_{j \in [\min(S_i, T_i)-1, \max(S_i, T_i)-2]} P_j > P_{S_i-1}$ (if $S<T$) or $P_j < P_{S_i-1}$ (if $S>T$).
This looks like we can assign a "level" to each index.
A known technique for this type of problem is to use a Disjoint Set Union (DSU) with potential or a Segment Tree to check for contradictions.
Given the constraints and the nature of "range minimum/maximum > value", we can transform this.
Let's consider the differences $D_j = P_j - P_{j-1} = w_j$.
The condition is that the partial sums from $S-1$ to $k-1$ are positive, and the total sum from $S-1$ to $T-1$ is 0.
This is equivalent to: The minimum prefix sum in the range $[S, T-1]$ (relative to start) is positive, and the final sum is 0.
This implies that the path goes up and comes down.
We can check compatibility of two people by seeing if their required "ups" and "downs" conflict.
A simpler necessary and sufficient condition for a set of people to be satisfiable is that there are no "crossing" constraints that force a contradiction.
Specifically, if we view the indices $0 \dots N-1$ as nodes, each person $i$ with $S<T$ requires $P_{S-1}=P_{T-1}$ and $P_k > P_{S-1}$ for $k \in [S, T-2]$.
This can be solved by checking if the intersection of any two "forbidden" regions creates a contradiction.
Actually, we can use a Segment Tree to maintain the "tightest" constraints. For each query $[L, R]$, we want to know if the union of constraints is consistent.
We can precompute the "conflict" intervals. Two people $i$ and $j$ conflict if their paths overlap in a way that requires $P_a > P_b$ and $P_b > P_a$ or similar.
Given the complexity, a standard solution for this AtCoder problem (ABC 277 F / similar) involves checking if the set of people forms a valid "mountain" structure.
We can use a Segment Tree to store the minimum and maximum possible values for $P_k$ relative to some root, or simply check for cycles in a constraint graph.
However, with $Q$ queries, we can use a divide and conquer approach or a Segment Tree over the queries.
Let's use the property that if a range $[L, R]$ is valid, then any sub-range is valid. We can use binary search on the answer for each query? No, queries are arbitrary ranges.
We can process queries offline. Sort queries by right endpoint?
A more direct approach:
1. For each person, identify the range of roads they traverse.
2. The condition is that $P$ must be strictly greater than the endpoint values in the interior.
3. This is equivalent to saying that the minimum value of $P$ on the path (excluding endpoints) is strictly greater than the endpoint value.
4. We can check consistency by ensuring that for any two overlapping paths, the "base" levels and "height" requirements don't clash.

A robust method is to use a Segment Tree to maintain the constraints. Each leaf represents a road strength $w_j$.
But $w_j$ can be negative.
Let's map this to a 2-SAT problem on intervals? No.
Let's use the fact that $N, M, Q$ are up to $2 \cdot 10^5$.
We can determine for each pair of people if they conflict. If we build a conflict graph, a query $[L, R]$ is valid iff the subgraph induced by $L \dots R$ has no edges? No, conflicts can be transitive or complex.
Actually, the constraints are "local" in terms of prefix sums.
We can define a graph where nodes are indices $0 \dots N-1$.
Edges: $P_{S-1} = P_{T-1}$.
Inequalities: $P_k \ge P_{S-1} + 1$.
This is a system of difference constraints. We can check satisfiability using Bellman-Ford or SPFA, but that's too slow per query.
However, the structure is special: it's a line.
We can use a Segment Tree to maintain the "potential" differences.
For each query, we can check if the constraints are consistent by verifying that no cycle of inequalities exists.
Since the graph is a line, cycles only arise from equality constraints closing a loop with inequality constraints.
Specifically, if we have $P_a = P_b$ and a path of inequalities from $a$ to $b$ that sums to $\le 0$, it's a contradiction.
We can use a DSU with potentials to maintain equality constraints and check inequalities.
For each query $[L, R]$, we add constraints for people $L \dots R$.
To answer $Q$ queries efficiently, we can use a Segment Tree where each node stores the DSU state? No, DSU is not easily mergeable.
Instead, we can use a "Segment Tree Beats" or similar technique?
Actually, we can process the queries offline using a sweep-line or divide and conquer.
Divide and Conquer on the queries:
For a range of queries $[ql, qr]$, pick a middle person $mid$. Check if adding person $mid$ to any valid subset of $[ql, mid-1]$ and $[mid+1, qr]$ causes conflict.
This is still complex.

Alternative Insight:
The problem is equivalent to checking if the intersection of all "valid" regions for $P$ is non-empty.
The constraints for person $i$ define a convex polytope.
The intersection is non-empty iff there are no contradictory cycles.
Given the line structure, we can check for contradictions by ensuring that for any two people $i, j$ with overlapping paths, the relative order of their "base" levels $P_{S_i-1}$ and $P_{S_j-1}$ is not forced to be both $>$ and $<$.
We can precompute all pairwise conflicts? $M^2$ is too big.
However, conflicts only happen if paths overlap significantly.
We can use a Segment Tree to store the "tightest" lower and upper bounds for each $P_k$.
Initialize $L_k = -\infty, R_k = \infty$.
For each person, update the bounds.
If for any $k$, $L_k > R_k$, it's invalid.
But we have $Q$ queries. We can't rebuild the tree for each query.
We can use a Persistent Segment Tree or a Mergeable Segment Tree.
Each person adds constraints. We can build a persistent segment tree where version $i$ includes constraints from person $1 \dots i$.
Then for query $[L, R]$, we need to combine constraints from $L \dots R$.
This is not directly supported by standard persistent segment trees which support prefix sums.
We can use a Segment Tree over the queries?
Let's use the standard technique: "Offline Dynamic Connectivity" or "Divide and Conquer on Queries".
We can use a Segment Tree over the array of people $1 \dots M$. Each leaf $i$ stores the constraints of person $i$.
We want to query the consistency of the range $[L, R]$.
We can build a Segment Tree where each node stores a DSU structure representing the constraints of the people in that range.
Merging two DSUs is expensive.
However, we only need to check consistency.
We can use the fact that the constraints are simple.
Let's try a simpler approach:
For each query, we can check consistency by verifying that there is no cycle in the constraint graph.
The constraint graph has nodes $0 \dots N-1$.
Edges from equality: $S_i-1 \leftrightarrow T_i-1$ (weight 0).
Edges from inequality: $k \to S_i-1$ with weight $-1$ (since $P_k \ge P_{S_i-1} + 1 \implies P_{S_i-1} \le P_k - 1$).
And $S_i-1 \to k$ with weight $1$? No, $P_k - P_{S_i-1} \ge 1$.
So $P_k \ge P_{S_i-1} + 1$.
This is a standard difference constraints system.
We can check for negative cycles.
Since the graph is sparse, we can use SPFA. But $Q$ queries is too many.

Final Plan:
1. Use a Segment Tree over the indices $1 \dots M$.
2. Each node in the Segment Tree will store a DSU with potentials that represents the constraints of the people in that range.
3. To answer a query $[L, R]$, we decompose $[L, R]$ into $O(\log M)$ nodes and merge their DSU structures.
4. Merging DSUs with potentials can be done in $O(N \alpha(N))$ or $O(N)$ if we are careful, but $N$ is large.
5. However, we only need to check for contradictions. We can use a "rollback" DSU or simply rebuild.
6. Given time limits, a simpler $O(Q \sqrt{M} \alpha(N))$ or $O(Q \log M \cdot N)$ might TLE.
7. There is a known solution using a Segment Tree to maintain the minimum and maximum prefix sums.
   - For each person, they impose $P_{S-1} = P_{T-1}$ and $P_k > P_{S-1}$ for $k \in (S, T)$.
   - This implies $P_k \ge P_{S-1} + 1$.
   - We can maintain for each index $j$, the lower bound $LB_j$ and upper bound $UB_j$ for $P_j$.
   - Initially $LB_j = -\infty, UB_j = \infty$.
   - For a person $S<T$: $LB_{S-1} = \max(LB_{S-1}, P_{base})$, $UB_{T-1} = \min(UB_{T-1}, P_{base})$, and $LB_k = \max(LB_k, P_{base} + 1)$ for $k \in [S, T-2]$. Also $P_{S-1} = P_{T-1}$ implies we can link them.
   - This is complex to maintain dynamically.

Given the constraints and problem type, the intended solution likely involves checking for "crossing" intervals.
Two people $i$ ($S_i < T_i$) and $j$ ($S_j < T_j$) conflict if their intervals $[S_i-1, T_i-1]$ and $[S_j-1, T_j-1]$ overlap in a specific way that forces $P_a > P_b$ and $P_b > P_a$.
Specifically, if one interval is contained in another, or they cross.
We can precompute a "conflict" array.
For each person, find the nearest conflicting person to the left and right.
Then use a Segment Tree or Sparse Table to answer range queries: "Is there any conflict in $[L, R]$?"
If we can define a conflict as a pair $(i, j)$, then the query is valid iff no pair $(i, j)$ with $L \le i < j \le R$ is conflicting.
This can be solved by finding the maximum $L$ such that $[L, R]$ has no conflicts.
Let $R_{max}[i]$ be the smallest $j > i$ such that $i$ and $j$ conflict.
Then for a query $[L, R]$, it is valid iff for all $i \in [L, R]$, $R_{max}[i] > R$.
This is equivalent to $\max_{i \in [L, R]} R_{max}[i] > R$? No, if $\max R_{max}[i] \le R$, then there is a conflict.
So valid iff $\max_{i \in [L, R]} R_{max}[i] \le R$ is FALSE?
If there is a conflict $(i, j)$ with $L \le i < j \le R$, then $R_{max}[i] = j \le R$.
So if $\max_{i \in [L, R]} R_{max}[i] \le R$, it means for all $i$, the first conflict is after $R$, so no conflict in $[L, R]$.
Wait, if $R_{max}[i] > R$, then the conflict is outside.
So valid iff $\max_{i \in [L, R]} R_{max}[i] > R$? No.
If $\max R_{max}[i] \le R$, then there exists $i$ with conflict $j \le R$. So Invalid.
If $\max R_{max}[i] > R$, it doesn't guarantee no conflict. It just means the *first* conflict for some $i$ is outside. But there might be a later conflict?
No, $R_{max}[i]$ is the *first* conflict. If the first conflict is outside, are there any conflicts inside?
If $i$ conflicts with $j$ and $k$ with $j < k$, and $j \le R < k$, then $R_{max}[i] = j \le R$.
So if $\max_{i \in [L, R]} R_{max}[i] \le R$, then there is at least one conflict inside.
Conversely, if there is a conflict $(i, j)$ with $L \le i < j \le R$, then $R_{max}[i] = j \le R$.
So the condition is: Valid iff $\max_{i \in [L, R]} R_{max}[i] > R$? No.
If there is a conflict, $\max R_{max}[i] \le R$.
If there is NO conflict, then for all $i$, $R_{max}[i] > R$ (or no conflict).
So Valid iff $\min_{i \in [L, R]} R_{max}[i] > R$.
We can precompute $R_{max}[i]$ for all $i$.
Then use a Segment Tree or Sparse Table to query the minimum in $[L, R]$.
If $\min_{i \in [L, R]} R_{max}[i] > R$, print Yes, else No.
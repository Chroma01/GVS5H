1. **Model the Problem**: The problem requires assigning weights $w_j$ to edges such that for each person $i$, the cumulative sum of weights along their path is 0 at the endpoints and positive in between. This translates to constraints on prefix sums of the edge weights. Let $P_k$ be the prefix sum of weights up to edge $k$ (with $P_0 = 0$). For a person traveling from $S$ to $T$ (assume $S < T$), the condition is $P_T - P_{S-1} = 0$ (so $P_T = P_{S-1}$) and for all intermediate nodes $k$ ($S \le k < T$), the partial sum $P_k - P_{S-1} > 0$. This implies $P_k > P_{S-1}$ for $S \le k < T$. Similarly, if $S > T$, the path goes backwards, and we can define the constraints accordingly. Essentially, for each person, we have an equality constraint between two prefix sums and inequality constraints that certain prefix sums are strictly greater than that value.

2. **Simplify Constraints**: The strict inequalities $P_k > C$ can be treated as $P_k \ge C + \epsilon$. Since we are looking for *existence* of real (or integer) solutions, we can often relax strict inequalities to non-strict ones if we handle the structure carefully. However, a more robust way is to use a difference constraint system or check for cycles in a graph of dependencies. Specifically, the conditions imply that for a set of people to be simultaneously satisfiable, there must be no "contradictory" cycles. A cycle would involve equalities and inequalities that force a value to be strictly less than itself.

3. **Offline Processing with Disjoint Set Union (DSU) or Segment Tree**: Since we have range queries $[L, R]$, we can process them offline. A common technique for "is this range valid" problems is to find for each $L$, the smallest $R$ such that the range $[L, R]$ is invalid, or vice versa. Alternatively, we can use a two-pointer approach or a segment tree to maintain the validity of the current set of constraints.
   However, the constraints are complex. Let's rephrase: Each person $i$ imposes:
   - $P_{T_i} = P_{S_i-1}$ (if $S_i < T_i$) or $P_{S_i-1} = P_{T_i}$ (if $S_i > T_i$). Let's standardize indices. Let $u_i = \min(S_i, T_i)-1$ and $v_i = \max(S_i, T_i)$. The path covers edges $u_i+1 \dots v_i$. The condition is $P_{v_i} = P_{u_i}$ and $P_k > P_{u_i}$ for $u_i < k < v_i$.
   - This looks like a system of difference constraints. We can model this with a graph where nodes are $0 \dots N-1$ (representing prefix sums $P_0 \dots P_{N-1}$).
   - Equality $P_a = P_b$ can be modeled as $P_a \le P_b$ and $P_b \le P_a$.
   - Inequality $P_k > P_a$ can be modeled as $P_k \ge P_a + 1$ (if integers) or just $P_k \ge P_a + \epsilon$. In a difference constraint system for existence, strict inequalities are tricky. But note that if we have a chain of inequalities $P_k \ge P_a + 1$ and equalities, we can detect contradictions.
   - A simpler observation: The condition is satisfiable if and only if there is no cycle in the constraint graph that forces a variable to be strictly less than itself. Specifically, if we contract the equality components, we get a DAG of inequalities. If there's a cycle in the inequality graph, it's unsatisfiable.

4. **Efficient Query Handling**: Given $Q$ and $M$ are up to $2 \cdot 10^5$, we need an efficient way. We can use a **Segment Tree** over the queries or the people. Or, we can use the fact that if a range $[L, R]$ is invalid, then $[L, R+1]$ is also invalid. This monotonicity allows us to use a two-pointer approach. For each left endpoint $L$, we find the smallest $R$ such that $[L, R]$ is invalid. Let this be $bad[L]$. Then for any query $[L, R]$, the answer is Yes if $R < bad[L]$.
   To implement the two-pointer approach, we maintain a data structure that supports adding a person (adding constraints) and checking for satisfiability. When moving $L$ forward, we remove constraints.
   The data structure needs to handle:
   - Merging sets of indices that must have equal prefix sums (DSU).
   - Checking for inequality conflicts within/between these sets.
   
   Actually, a known technique for this specific problem (AtCoder ABC 274 F or similar) involves checking if the constraints form a valid "mountain" shape. A simpler sufficient condition for small constraints is to use a **DSU with potential** or just check for cycles in a graph where edges are $u \to v$ with weight 0 (equality) and $u \to v$ with weight 1 (inequality $P_v \ge P_u + 1$).
   
   Let's refine the "Two Pointer + DSU" idea:
   - We maintain a DSU structure for the equality constraints. Each set in DSU has a representative.
   - We also maintain a graph of inequalities between these sets. If we have $P_k > P_u$, and $u$ is in set $A$, $k$ is in set $B$, we add a directed edge $A \to B$ with weight $\ge 1$.
   - If we have a cycle in this inequality graph, it's unsatisfiable.
   - Since $N$ is large, we can't maintain the full graph. However, note that the inequalities are always of the form $P_k > P_{u_i}$ for $k$ in a range.
   
   Alternative Insight: The problem is equivalent to checking if the system of difference constraints has no negative cycles. We can use a standard algorithm, but it's too slow per query.
   
   Let's look at the constraints again. $P_{v_i} = P_{u_i}$ and $P_k > P_{u_i}$ for $u_i < k < v_i$.
   This implies that for any two people $i, j$, if their intervals overlap, there might be conflicts.
   
   Actually, there is a simpler characterization: The system is satisfiable if and only if there is no "nested" or "crossing" contradiction.
   Specifically, consider the intervals $[u_i, v_i]$.
   If we have two people $i$ and $j$:
   - If their intervals are disjoint, they don't interact directly.
   - If one is inside the other, say $[u_j, v_j] \subset [u_i, v_i]$, then $P_{u_j} > P_{u_i}$ and $P_{v_j} > P_{u_i}$. Also $P_{v_j} = P_{u_j}$.
   - If they cross, e.g., $u_i < u_j < v_i < v_j$, then $P_{v_i} = P_{u_i}$ and $P_{v_j} = P_{u_j}$. Also $P_{u_j} > P_{u_i}$ (since $u_j$ is inside $i$'s path? No, $u_j$ is start of $j$. If $j$ goes $u_j \to v_j$, then for $k$ in $(u_j, v_j)$, $P_k > P_{u_j}$. Does $i$ impose constraints on $u_j$? If $u_i < u_j < v_i$, then $u_j$ is an intermediate node for $i$, so $P_{u_j} > P_{u_i}$. Similarly $P_{v_i} > P_{u_j}$? No, $v_i$ is intermediate for $j$? If $u_j < v_i < v_j$, then $v_i$ is intermediate for $j$, so $P_{v_i} > P_{u_j}$.
     So we have $P_{u_j} > P_{u_i}$ and $P_{v_i} > P_{u_j}$ and $P_{v_i} = P_{u_i}$.
     This leads to $P_{u_i} = P_{v_i} > P_{u_j} > P_{u_i}$, a contradiction.
     Thus, **crossing intervals are always invalid**.
   
   What about nested intervals?
   $[u_j, v_j] \subset [u_i, v_i]$.
   $P_{u_j} > P_{u_i}$, $P_{v_j} > P_{u_i}$.
   $P_{v_j} = P_{u_j}$.
   $P_{v_i} = P_{u_i}$.
   Also for $k$ in $(u_i, u_j)$, $P_k > P_{u_i}$.
   For $k$ in $(v_j, v_i)$, $P_k > P_{u_i}$.
   This is generally satisfiable (e.g., go up, stay flat, go down).
   
   So the condition is: **No two intervals in the set $[L, R]$ may cross.**
   Two intervals $[a, b]$ and $[c, d]$ (with $a<b, c<d$) cross if $a < c < b < d$ or $c < a < d < b$.
   
   Therefore, the problem reduces to: For each query $[L, R]$, do any pair of intervals in the subset $\{L, \dots, R\}$ cross?
   
   This is a classic problem: **Range Query for Existence of Crossing Intervals**.
   We can solve this by:
   1. Precomputing for each interval $i$, the nearest interval $j > i$ that crosses it. Let this be $next\_cross[i]$. If no such $j$ exists, $\infty$.
   2. Then for a query $[L, R]$, the answer is "No" if there exists an $i \in [L, R]$ such that $next\_cross[i] \in [L, R]$ and $next\_cross[i] > i$.
   3. This is equivalent to: Is $\max_{i \in [L, R]} (\text{if } next\_cross[i] \le R \text{ then } 1 \text{ else } 0) == 1$?
   4. Or simpler: Let $bad[i] = next\_cross[i]$. The range $[L, R]$ is invalid if there is an $i \in [L, R]$ such that $L \le bad[i] \le R$.
   5. We can precompute $bad[i]$ for all $i$. Then for each query, we check if $\min_{i \in [L, R]} bad[i] \le R$? No, we need $bad[i] \ge L$.
      Actually, if we define $valid[i]$ as the smallest $R' > i$ such that $[i, R']$ contains a crossing pair involving $i$, then we can use a segment tree.
      
   Algorithm to find $next\_cross[i]$:
   - Use a sweep-line or a stack-based approach similar to finding the next greater element, but for intervals.
   - Sort intervals by start point.
   - Iterate and maintain a data structure of active intervals.
   - For current interval $[u_i, v_i]$, any active interval $[u_j, v_j]$ with $u_j < u_i$ crosses if $v_j > u_i$ and $v_j < v_i$? No, crossing is $u_j < u_i < v_j < v_i$.
   - So for $i$, we want the smallest $j < i$ such that $u_j < u_i < v_j < v_i$.
   - This can be done by iterating $i$ from 1 to $M$. Maintain a set of active intervals (those with $u_j < u_i$ and $v_j \ge u_i$).
   - Among active intervals, we need one with $v_j < v_i$. If multiple, we want the one that creates a crossing. Actually, ANY active interval with $v_j < v_i$ crosses $i$ because $u_j < u_i < v_j < v_i$.
   - So for each $i$, we want to know if there is an active $j$ with $v_j < v_i$. If so, let $j^*$ be the one with the largest $v_j$ such that $v_j < v_i$? Or just any?
   - We need to record the conflict. For the query, we need to know if the conflict is within $[L, R]$.
   - Let's define $conflict\_end[j]$ for each $j$: the smallest $i > j$ such that $i$ crosses $j$.
   - Then for a query $[L, R]$, it is invalid if there exists $j \in [L, R]$ such that $conflict\_end[j] \in [L, R]$.
   
   Steps:
   1. Parse input. Convert $(S_i, T_i)$ to $(u_i, v_i)$ with $u_i < v_i$.
   2. Find $conflict\_end[i]$ for each $i$.
      - Use a segment tree or Fenwick tree over the values of $v$.
      - Iterate $i$ from 1 to $M$.
      - Active intervals are those $j < i$ with $v_j \ge u_i$.
      - We want to find if there is a $j$ in active set with $v_j < v_i$.
      - If yes, let $j^*$ be the active $j$ with the largest $v_j$ that is still $< v_i$? Actually, if there are multiple, any of them crosses. But we need to assign the conflict to the pair.
      - To minimize the "right endpoint" of the conflict for the purpose of the query, we can define $conflict\_end[j]$ as the smallest $i$ that crosses $j$.
      - So for each $i$, we find all $j < i$ that cross it. The crossing condition is $u_j < u_i < v_j < v_i$.
      - We can query the data structure for intervals with $v_j \in [u_i, v_i - 1]$.
      - If such $j$ exists, we update $conflict\_end[j] = \min(conflict\_end[j], i)$.
      - We only need the *first* crossing for each $j$.
   3. After computing $conflict\_end[i]$ for all $i$, we have a set of "bad" pairs $(i, conflict\_end[i])$.
   4. For a query $[L, R]$, it is invalid if there is any $i \in [L, R]$ such that $conflict\_end[i] \le R$ (and obviously $conflict\_end[i] > i \ge L$).
   5. This is equivalent to: $\min_{i \in [L, R]} conflict\_end[i] \le R$?
      - Careful: If $conflict\_end[i] < L$, it doesn't matter. But since $i \ge L$ and $conflict\_end[i] > i$, we have $conflict\_end[i] > L$. So we just check if $\min_{i \in [L, R]} conflict\_end[i] \le R$.
   6. Use a Segment Tree or Sparse Table to answer range minimum queries on the array $conflict\_end$. Initialize $conflict\_end[i] = \infty$ if no crossing.
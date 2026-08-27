
## ideation
The problem asks us to determine if there exists an assignment of road strengths $w_j$ such that for a subset of people, their stamina constraints are satisfied.
1.  **Modeling**:
    *   Let $P_k$ be the prefix sum of road strengths from town 1 to town $k$ (specifically, $P_1 = 0$, $P_{k+1} = P_k + w_k$).
    *   For a person traveling from $S$ to $T$:
        *   If $S < T$: The path is $S \to S+1 \to \dots \to T$. The stamina at town $k$ ($S < k < T$) is $P_k - P_S$. The condition is $P_k - P_S > 0$ for all intermediate $k$, and $P_T - P_S = 0$. This implies $P_S = P_T$ and $P_k > P_S$ for $k \in (S, T)$.
        *   If $S > T$: The path is $S \to S-1 \to \dots \to T$. The stamina at town $k$ ($T < k < S$) is $P_S - P_k$. The condition is $P_S - P_k > 0$ for all intermediate $k$, and $P_S - P_T = 0$. This implies $P_S = P_T$ and $P_k < P_S$ for $k \in (T, S)$.

2.  **Constraints**:
    *   Equality: $P_S = P_T$.
    *   Inequality: $P_k > P_S$ (if $S < T$) or $P_k < P_S$ (if $S > T$) for all $k$ strictly between $S$ and $T$.

3.  **Feasibility Check**:
    *   The equality constraints partition the towns into connected components where all $P$ values in a component must be equal. We can use a Disjoint Set Union (DSU) to manage these components.
    *   The inequality constraints impose directed relationships between components. Specifically, if $S < T$, then for all $k \in (S, T)$, the component containing $k$ must have a strictly greater value than the component containing $S$. This creates a directed edge $Comp(S) \to Comp(k)$ in a "less-than" graph (meaning $Val(Comp(S)) < Val(Comp(k))$).
    *   If $S > T$, then for all $k \in (T, S)$, $Val(Comp(k)) < Val(Comp(S))$, creating an edge $Comp(k) \to Comp(S)$.
    *   The system is feasible if and only if this directed graph of components has no cycles. A cycle would imply $A < B < \dots < A$, which is impossible.

4.  **Handling Queries**:
    *   We have $Q$ queries, each asking about a range of people $[L, R]$.
    *   A naive solution building the graph for each query is too slow ($O(Q \cdot (M+N))$).
    *   We can process queries offline. Sort queries by $R$. Iterate $R$ from 1 to $M$. Add person $R$'s constraints to our data structure.
    *   To efficiently check for cycles and manage the "range" inequalities, we can use a Segment Tree.
    *   However, a simpler observation for this specific problem structure: The constraints are local. We can maintain the DSU and the inequality graph. When adding a new person, we union the endpoints and add edges between the endpoint's component and all intermediate nodes' components.
    *   Since $N$ is large, we cannot iterate all intermediate nodes for each person.
    *   **Optimization**: The inequality $P_k > P_S$ for all $k \in (S, T)$ is equivalent to saying that the minimum value in the range $(S, T)$ must be greater than $P_S$. Similarly for the other case.
    *   We can maintain a Segment Tree that stores the "tightest" bounds. But checking for cycles in a dynamic graph is hard.
    *   **Alternative Approach**: Since we only need to output Yes/No, and the constraints are strict inequalities, we can use a **Difference Constraints** system. The condition $P_k > P_S$ becomes $P_k \ge P_S + 1$. This is a standard system of difference constraints. We can check for negative cycles.
    *   Given the constraints and the nature of competitive programming problems of this type, a common solution involves using a **Segment Tree** to maintain the minimum and maximum possible values for each $P_i$ relative to a root, or using a **DSU with rollback** if we were doing binary search on the answer, but here we have range queries.
    *   Actually, a key insight is that if a set of constraints is inconsistent, there is a "minimal" inconsistent subset. We can use a **DSU** to merge components for equalities. For inequalities, we can store them in a graph. To avoid $O(N)$ per person, we can use a **Segment Tree** to quickly find if there is any node $k$ in $(S, T)$ that violates the condition.
    *   Specifically, for $S < T$, we require $P_k > P_S$ for all $k \in (S, T)$. If we maintain the current assigned values (or bounds) in a Segment Tree, we can query the minimum value in $(S, T)$. If $\min_{k \in (S, T)} P_k \le P_S$, then it's a contradiction.
    *   But we don't have fixed values, we have relative constraints.
    *   Let's use the property that we can assign values greedily. If we process constraints, we can maintain the "height" of each component.
    *   Given the complexity, I will implement a solution that uses **DSU** for equalities and a **Segment Tree** to maintain the minimum and maximum "offsets" for each town. For each person, we check if the range constraints are consistent with the current offsets. If not, we return No. If consistent, we update the offsets.
    *   Wait, updating offsets for range queries is complex.
    *   Let's stick to the **Cycle Detection** idea but optimize it. We can use a **DSU** to merge components. For inequalities, we add edges. To check for cycles, we can use DFS. But the graph can be large.
    *   **Correct Efficient Approach**: Use a **Segment Tree** to store the "active" inequality constraints. For each query $[L, R]$, we can check consistency by building the graph for people $L \dots R$. To do this fast, we can use **Mo's Algorithm** or **Offline Processing with a Segment Tree**.
    *   Given the token limit and complexity, I will provide a solution that uses **DSU** and a **graph** for inequalities, but optimized by noting that we only need to check for cycles. For the range queries, I will use a **Segment Tree** to store the "tightest" bounds.
    *   Actually, a simpler method: For each query, we can check if the constraints are consistent by verifying that there are no cycles in the inequality graph. We can build this graph incrementally.
    *   I will implement a solution that processes queries offline, adding people one by one and maintaining the DSU and inequality graph. To handle the range queries, I will store the queries and process them as I add people. If a query $[L, R]$ is asked, and I am at $R$, I need to know if the subset $L \dots R$ is consistent. This requires "removing" people $1 \dots L-1$. This suggests **Mo's Algorithm** or a **Persistent DSU**.
    *   Persistent DSU is complex.
    *   Let's try a different angle: **Difference Constraints with Segment Tree**.
    *   We can transform the problem into: Is there a valid assignment of $P_i$?
    *   We can use a Segment Tree to maintain the minimum and maximum possible values for each $P_i$.
    *   For $S < T$: $P_S = P_T$, and $P_k > P_S$ for $k \in (S, T)$.
    *   This implies $P_k \ge P_S + 1$.
    *   We can maintain for each node in the segment tree the minimum and maximum possible value of $P_i$ relative to some base.
    *   This is getting too complex for a quick implementation.
    *   **Simpler Heuristic**: For small $N$, we can solve directly. For large $N$, we need the efficient method.
    *   I will implement a solution using **DSU** and **Cycle Detection** with a **Segment Tree** to manage the range inequalities.
    *   Specifically, for each person, we add edges $S \to k$ (weight 1) for all $k \in (S, T)$ if $S < T$. This is too many edges.
    *   Instead, we can add a single edge $S \to T$ with weight 0, and then use the Segment Tree to enforce that all intermediate nodes are "higher".
    *   I will use a **Segment Tree** to store the minimum value in each range. When adding a constraint $P_k > P_S$, we update the minimum value in the range $(S, T)$ to be at least $P_S + 1$. If this conflicts with existing constraints, we return No.
    *   This "range update, point query" or "range min query" approach can work if we maintain the values.
    *   Let's maintain an array $V$ where $V[i]$ is the current "height" of town $i$. Initially 0.
    *   For $S < T$: We require $V[k] > V[S]$ for all $k \in (S, T)$ and $V[T] = V[S]$.
    *   This is not just a value update, but a relative constraint.
    *   Given the time, I will provide a solution that uses **DSU** for equalities and a **graph** for inequalities, checking for cycles. To handle the range queries, I will use a **Segment Tree** to store the "tightest" bounds.

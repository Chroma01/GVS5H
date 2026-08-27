
## ideation
**Core Difficulty:**
The problem asks if there exists an assignment of integer weights $w_j$ to $N-1$ roads such that $M$ people can travel from $S_i$ to $T_i$ satisfying specific stamina constraints:
1. Start at $S_i$: Stamina = 0.
2. End at $T_i$: Stamina = 0.
3. Intermediate towns: Stamina > 0 (positive integer).

Let $P_i$ be the prefix sum of weights from town 1 to town $k$, with $P_1 = 0$. The weight of road $j$ (between $j$ and $j+1$) is $w_j = P_{j+1} - P_j$.
If a person travels from $S$ to $T$ (assume $S < T$ without loss of generality), their stamina at town $k$ ($S \le k \le T$) is:
$Stamina_k = (P_S - P_S) + (P_{S+1} - P_S) + \dots + (P_k - P_{k-1}) = P_k - P_S$.
Wait, the problem says "starts with stamina 0". So at $S$, stamina is 0.
After crossing road $S$ (to $S+1$), stamina becomes $0 + w_S = P_{S+1} - P_S$.
At town $k$, stamina is $\sum_{j=S}^{k-1} w_j = P_k - P_S$.
Constraints:
1. At $S$: $P_S - P_S = 0$ (Always true).
2. At $T$: $P_T - P_S = 0 \implies P_T = P_S$.
3. For $k \in (S, T)$: $P_k - P_S \ge 1 \implies P_k \ge P_S + 1$.

So for each person $i$ with range $[S_i, T_i]$ (assuming $S_i < T_i$), we need:
- $P_{S_i} = P_{T_i}$
- $\min_{k=S_i+1}^{T_i-1} P_k \ge P_{S_i} + 1$

Let $x_i = P_{S_i}$. Then $P_{T_i} = x_i$.
The condition becomes:
- $P_{S_i} = P_{T_i}$
- $\forall k \in (S_i, T_i), P_k \ge P_{S_i} + 1$.

We need to assign values $P_1, P_2, \dots, P_N$ (integers) such that for a subset of people (range $[L, R]$), these conditions hold.
Notice that the relative differences matter. We can fix $P_1 = 0$ (or any value) and look for consistency.
However, the constraints link different segments.
Consider the "height" of the path. If we have overlapping intervals, the values of $P$ at intersection points must satisfy inequalities from all covering intervals.

Let's rephrase: We need to assign integer values $v_1, \dots, v_N$ to nodes such that:
For each $i \in [L, R]$:
1. $v_{S_i} = v_{T_i}$
2. $\forall k \in (S_i, T_i), v_k \ge v_{S_i} + 1$.

This looks like a 2-SAT or constraint satisfaction problem, but $N, M, Q$ are large ($4 \cdot 10^5$). We need a faster check per query.
Actually, this structure implies that if we have a set of constraints, they must be consistent.
Key observation: The condition $v_k \ge v_{S_i} + 1$ for all $k \in (S_i, T_i)$ combined with $v_{S_i} = v_{T_i}$ implies that the "minimum" value in the interval $(S_i, T_i)$ must be strictly greater than the endpoints.
If we have two intervals $[S_1, T_1]$ and $[S_2, T_2]$ that "cross" or nest in a conflicting way, it might be impossible.

Consider the case where we have intervals $[1, 3]$ and $[2, 4]$.
1. $v_1 = v_3$, $v_2 \ge v_1 + 1$.
2. $v_2 = v_4$, $v_3 \ge v_2 + 1$.
Substitute: $v_3 \ge v_2 + 1 \ge (v_1 + 1) + 1 = v_1 + 2$.
But $v_3 = v_1$. Contradiction ($v_1 \ge v_1 + 2$).
So crossing intervals where one is "inside" the other partially can cause issues.

General Condition for Consistency:
For any two people $i, j$ in the query range:
If their intervals $[S_i, T_i]$ and $[S_j, T_j]$ are disjoint, no interaction.
If they nest ($[S_j, T_j] \subset [S_i, T_i]$), then $v_{S_j} = v_{T_j}$ and $v_k \ge v_{S_j} + 1$ for $k \in (S_j, T_j)$. Also $v_{S_i} = v_{T_i}$ and $v_k \ge v_{S_i} + 1$ for $k \in (S_i, T_i)$.
Since $S_j, T_j \in (S_i, T_i)$, we must have $v_{S_j} \ge v_{S_i} + 1$ and $v_{T_j} \ge v_{S_i} + 1$.
Since $v_{S_j} = v_{T_j}$, this is consistent as long as we can pick $v_{S_j} = v_{S_i} + 1$.
The problematic case is the "crossing" one: $S_i < S_j < T_i < T_j$.
From $i$: $v_{S_j} \ge v_{S_i} + 1$ (since $S_j \in (S_i, T_i)$).
From $j$: $v_{T_i} \ge v_{S_j} + 1$ (since $T_i \in (S_j, T_j)$).
Also $v_{S_i} = v_{T_i}$ and $v_{S_j} = v_{T_j}$.
Chain: $v_{S_i} = v_{T_i} \ge v_{S_j} + 1 \ge (v_{S_i} + 1) + 1 = v_{S_i} + 2$.
Contradiction.
So, **no two intervals in the selected set can cross**.
Is this the only condition?
What if they share an endpoint? $S_i < S_j = T_i < T_j$.
From $i$: $v_{S_j} \ge v_{S_i} + 1$.
From $j$: $v_{S_j} = v_{T_j}$. No internal constraint involving $T_i$ (since $T_i$ is start of $j$).
Wait, $T_i$ is an endpoint of $j$, so no internal constraint.
So $v_{S_j} \ge v_{S_i} + 1$. Consistent.
What if $S_i = S_j$? Then $T_i \neq T_j$. Assume $T_i < T_j$.
$i$: $v_k \ge v_{S_i} + 1$ for $k \in (S_i, T_i)$.
$j$: $v_k \ge v_{S_j} + 1$ for $k \in (S_j, T_j)$.
Since $S_i=S_j$, the condition for $j$ is stronger (covers more). If $i$'s condition holds, $j$'s holds for the shared part.
But we also need $v_{T_i} = v_{S_i}$ and $v_{T_j} = v_{S_j} = v_{S_i}$.
Does $j$ require $v_{T_i} \ge v_{S_j} + 1$? No, $T_i$ is not in $(S_j, T_j)$ if $T_i < T_j$. Wait, $T_i$ is inside $(S_j, T_j)$.
Yes, $S_j < T_i < T_j$. So $v_{T_i} \ge v_{S_j} + 1$.
But $v_{T_i} = v_{S_i} = v_{S_j}$.
So $v_{S_j} \ge v_{S_j} + 1$. Contradiction.
So we cannot have one interval starting at the same point as another and ending before the other ends.
Basically, the intervals must be **non-crossing and non-overlapping in a specific way**.
Actually, the condition simplifies to: The set of intervals must form a **laminar family** (nested or disjoint), but with a twist?
Let's re-evaluate the "same start" case: $[1, 3]$ and $[1, 4]$.
1: $v_1=v_3, v_2 \ge v_1+1$.
2: $v_1=v_4, v_2 \ge v_1+1, v_3 \ge v_1+1$.
From 2: $v_3 \ge v_1+1$. But from 1: $v_3 = v_1$. Contradiction.
So we cannot have $[S, T_1]$ and $[S, T_2]$ with $T_1 < T_2$.
Similarly, cannot have $[S_1, T]$ and $[S_2, T]$ with $S_1 < S_2$.
So, for any two intervals in the set, they must be either:
1. Disjoint.
2. One is strictly inside the other ($[S_2, T_2] \subset [S_1, T_1]$).
AND if nested, we need to check consistency.
Nested: $[S_1, T_1]$ contains $[S_2, T_2]$.
Conditions:
$v_{S_1} = v_{T_1}$, $v_k \ge v_{S_1}+1$ for $k \in (S_1, T_1)$.
$v_{S_2} = v_{T_2}$, $v_k \ge v_{S_2}+1$ for $k \in (S_2, T_2)$.
Since $S_2, T_2 \in (S_1, T_1)$, we have $v_{S_2} \ge v_{S_1}+1$ and $v_{T_2} \ge v_{S_1}+1$.
Since $v_{S_2}=v_{T_2}$, this is fine. We can set $v_{S_2} = v_{S_1}+1$.
Then for $k \in (S_2, T_2)$, we need $v_k \ge v_{S_2}+1 = v_{S_1}+2$.
The outer constraint requires $v_k \ge v_{S_1}+1$. The inner is stronger.
So nested intervals are always consistent (we can just stack heights).
The forbidden configurations are:
1. Crossing: $S_1 < S_2 < T_1 < T_2$.
2. Same start, different end: $S_1 = S_2 < T_1 < T_2$.
3. Same end, different start: $S_1 < S_2 = T_1 < T_2$.

These three cases are exactly the cases where the intervals are **not laminar** (in the sense of set inclusion).
Wait, "Same start" is not laminar? Laminar means $A \subseteq B$ or $B \subseteq A$ or $A \cap B = \emptyset$.
$[1, 3]$ and $[1, 4]$: Intersection is $[1, 3]$. Neither is subset of other? No, $[1, 3] \subset [1, 4]$?
Set inclusion: $\{1, 2, 3\} \subset \{1, 2, 3, 4\}$. Yes, it is a subset.
But the interval definition includes endpoints.
Person 1: $S=1, T=3$. Condition: $v_1=v_3, v_2 \ge v_1+1$.
Person 2: $S=1, T=4$. Condition: $v_1=v_4, v_2 \ge v_1+1, v_3 \ge v_1+1$.
The conflict is $v_3 = v_1$ vs $v_3 \ge v_1+1$.
Why did the subset logic fail? Because the "subset" of intervals implies the inner interval's endpoints are in the outer's interior.
Here $S_2 = S_1$. $S_2$ is NOT in $(S_1, T_1)$. It is the boundary.
The condition $v_k \ge v_{S_1}+1$ applies for $k \in (S_1, T_1)$. $S_1$ is not in this set.
But for the outer interval $[S_2, T_2]$, $T_1$ is in $(S_2, T_2)$ (since $S_2=S_1 < T_1 < T_2$).
So $v_{T_1} \ge v_{S_2} + 1$.
But $v_{T_1} = v_{S_1} = v_{S_2}$.
Contradiction.
So, the condition is: **For any two intervals, they must not overlap such that one starts before the other and ends before the other ends, UNLESS the one that ends first is completely contained in the other in a way that doesn't trigger the boundary conflict?**
Actually, the conflict arises if $S_1 < S_2 < T_1 < T_2$ (Crossing) OR $S_1 = S_2 < T_1 < T_2$ (Same Start) OR $S_1 < S_2 = T_1 < T_2$ (Same End).
In all these cases, the intervals are not "properly laminar" with respect to the constraints.
Specifically, if we sort intervals by $S$, then by $T$:
If we have $[S_1, T_1]$ and $[S_2, T_2]$ with $S_1 \le S_2$.
If $T_1 < S_2$: Disjoint. OK.
If $T_1 = S_2$: Touching. OK?
$[1, 2]$ and $[2, 3]$.
1: $v_1=v_2$. 2: $v_2=v_3$.
No internal constraints (length 1 paths have no intermediate towns).
So touching is OK.
If $S_1 < T_1 \le S_2$: Overlap? No, $T_1 \le S_2$ means disjoint or touching.
If $S_1 < T_1 < T_2$ and $S_2 = S_1$: Conflict.
If $S_1 < S_2 < T_1 < T_2$: Conflict.
If $S_1 < S_2 < T_1 = T_2$:
1: $v_{S_1}=v_{T_1}, v_k \ge v_{S_1}+1$.
2: $v_{S_2}=v_{T_2}=v_{T_1}, v_k \ge v_{S_2}+1$.
Since $S_2 \in (S_1, T_1)$, $v_{S_2} \ge v_{S_1}+1$.
Since $T_1 \in (S_2, T_2)$? No, $T_1=T_2$, so $T_1$ is endpoint of 2. No constraint on $T_1$ from 2.
But $T_1$ is endpoint of 1.
Is there a conflict?
$v_{S_2} \ge v_{S_1}+1$.
$v_{T_1} = v_{S_1}$.
$v_{T_1} = v_{S_2}$.
So $v_{S_1} \ge v_{S_1}+1$. Conflict.
So $[S_1, T]$ and $[S_2, T]$ with $S_1 < S_2$ is also a conflict.

**Conclusion:** The set of intervals must be such that for any two, either they are disjoint, or one is strictly inside the other ($S_1 < S_2$ and $T_2 < T_1$).
Wait, what about $S_1 < S_2 < T_1 < T_2$? Not allowed.
$S_1 = S_2$? Not allowed (unless $T_1=T_2$, but problem says distinct pairs).
$T_1 = T_2$? Not allowed (unless $S_1=S_2$, same pair).
So, the condition is: **The intervals must form a laminar family where no two intervals share an endpoint unless they are identical (which is forbidden) or one is inside the other?**
Actually, simpler: Sort intervals by $S$. If we have multiple intervals starting at the same $S$, we have a conflict.
If we have $[S, T_1]$ and $[S, T_2]$ with $T_1 < T_2$, conflict.
If we have $[S_1, T]$ and $[S_2, T]$ with $S_1 < S_2$, conflict.
So, in the valid set:
1. All $S_i$ must be distinct? No, if $S_1 < S_2$, we must have $T_1 < S_2$ (disjoint) or $T_1 > T_2$ (nested).
   If $S_1 < S_2$ and $T_2 < T_1$: Nested. OK.
   If $S_1 < S_2$ and $T_1 < T_2$: Crossing or Same-Start-like.
     If $T_1 < S_2$: Disjoint. OK.
     If $S_2 < T_1 < T_2$: Crossing. Conflict.
     If $T_1 = S_2$: Disjoint. OK.
     If $T_1 = T_2$: Same End. Conflict.
So, for sorted $S$:
If $S_i < S_j$, then we must have $T_i < S_j$ (disjoint) OR $T_j < T_i$ (nested).
This implies that if we sort by $S$, the $T$ values must be decreasing for nested ones, and increasing for disjoint ones?
Actually, if we sort by $S$, and we have a sequence of intervals, the condition "No crossing, No same start, No same end" implies that the intervals must be properly nested or disjoint.
This is equivalent to saying: **The intervals must not have any "crossing" pairs.**
A pair $(i, j)$ crosses if $S_i < S_j < T_i < T_j$.
Does this cover all conflicts?
- Same start $S_i = S_j < T_i < T_j$: This is not strictly $S_i < S_j$. But if we break ties by $T$, say $T_i < T_j$, then $S_i \le S_j$. If we treat $S_i=S_j$ as "crossing" in a generalized sense?
Actually, the condition derived is: **For any two intervals, they must be either disjoint or one strictly contains the other.**
This is the definition of a laminar family of intervals.
Wait, $[1, 3]$ and $[1, 4]$. Intersection $[1, 3]$. $[1, 3] \subseteq [1, 4]$.
But we found a conflict.
Why? Because the "containment" requires the inner interval's endpoints to be in the *interior* of the outer interval.
If $S_{inner} = S_{outer}$, then $S_{inner}$ is not in $(S_{outer}, T_{outer})$.
So the condition is: **The intervals must be laminar AND no two intervals share an endpoint.**
Wait, if $[1, 3]$ and $[2, 4]$. $S_1=1, T_1=3, S_2=2, T_2=4$. Crossing. Conflict.
If $[1, 3]$ and $[1, 4]$. Same start. Conflict.
If $[1, 3]$ and $[2, 3]$. Same end. Conflict.
So, the valid sets are those where:
1. No two intervals share an endpoint.
2. No two intervals cross.
This means the intervals must be disjoint or strictly nested, AND they cannot touch at endpoints.
Wait, if they are disjoint, they don't share endpoints.
If they are nested, $S_1 < S_2 < T_2 < T_1$. Endpoints are distinct.
So the condition is simply: **The set of intervals must be pairwise non-crossing and pairwise non-touching.**
i.e., For any $i, j$, either $[S_i, T_i] \cap [S_j, T_j] = \emptyset$ or $[S_i, T_i] \subset (S_j, T_j)$ (strictly inside).
Actually, if they are disjoint, they don't share endpoints.
If they are nested, $S_j > S_i$ and $T_j < T_i$. Endpoints distinct.
So yes, **No shared endpoints and No crossing**.

**Algorithm:**
We need to check if the subset of people $[L, R]$ satisfies:
1. All $S_i$ are distinct.
2. All $T_i$ are distinct.
3. No crossing: $S_i < S_j < T_i < T_j$ (or vice versa).

This is equivalent to checking if the intervals form a valid non-crossing partition.
We can model this using a segment tree or sweep-line.
Sort people by $S$.
Iterate $i$ from 1 to $M$. Maintain the current "active" intervals.
For a query $[L, R]$, we need to check if the subset of people in this range has any conflicts.
Conflict types:
- Same $S$: Two people in $[L, R]$ have same $S$.
- Same $T$: Two people in $[L, R]$ have same $T$.
- Crossing: $S_i < S_j < T_i < T_j$.

This can be solved by:
1. Check distinct $S$ in range.
2. Check distinct $T$ in range.
3. Check no crossing.

Checking distinct $S$ and $T$ is easy with a frequency array or hash map, but we need it for arbitrary ranges.
We can use a Segment Tree to store the count of each $S$ and $T$. Query max count. If max > 1, fail.
Checking crossing:
This is the hard part.
Crossing condition: $S_i < S_j < T_i < T_j$.
This is equivalent to saying that if we sort by $S$, the $T$ values must not "interleave".
Actually, if we sort the subset by $S$, let the sorted intervals be $I_1, I_2, \dots, I_k$.
If they are non-crossing and non-touching, then for any $a < b$, either $T_a < S_b$ (disjoint) or $T_b < T_a$ (nested).
This implies that the sequence of $T$'s must be monotonic?
No. Consider $[1, 10], [2, 3], [4, 5]$.
Sorted by $S$: $[1, 10], [2, 3], [4, 5]$.
$T$'s: $10, 3, 5$. Not monotonic.
But $[2, 3]$ is inside $[1, 10]$, $[4, 5]$ is inside $[1, 10]$. They are disjoint from each other.
So the structure is a tree (nested).
The condition "No crossing" is equivalent to: The intervals form a laminar family.
How to check laminar family for a subset?
We can use a segment tree over the positions $1 \dots N$.
For each person $i$, we have an interval $[S_i, T_i]$.
We want to know if there exist $i, j \in [L, R]$ such that they cross or share endpoints.
Actually, we can simplify:
If we have distinct $S$ and distinct $T$, does that prevent crossing?
No. $[1, 4]$ and $[2, 3]$ are nested. Distinct $S, T$. OK.
$[1, 3]$ and $[2, 4]$ cross. Distinct $S, T$. Conflict.
So we need to explicitly check crossing.
Condition for crossing: $S_i < S_j < T_i < T_j$.
This is a 2D range query problem?
Points $(S_i, T_i)$. We want to know if there exist two points in the query set such that $S_i < S_j$ and $T_i > T_j$ and $S_j < T_i$ and $T_j > T_i$?
Wait, crossing is $S_i < S_j < T_i < T_j$.
So $S_i < S_j$, $T_i > S_j$, $T_j > T_i$.
Also need $S_j < T_i$.
Basically, if we sort by $S$, we need to check if there exists $j > i$ (in sorted order) such that $S_j < T_i < T_j$.
If such a pair exists, then crossing.
So for a subset of people, sort them by $S$. Check if there is any $i, j$ with $S_i < S_j < T_i < T_j$.
This is equivalent to: Does the set of intervals have a "crossing"?
We can use a Segment Tree over the domain $1 \dots N$.
Each person $i$ covers $[S_i, T_i]$.
If we have a set of intervals, they are non-crossing iff for every $x$, the number of intervals covering $x$ is consistent with nesting?
Actually, a known result: A set of intervals is non-crossing (laminar) iff for any $x$, the intervals covering $x$ are nested.
But we also have the "no shared endpoint" constraint.
Let's combine:
1. Check distinct $S$ in $[L, R]$.
2. Check distinct $T$ in $[L, R]$.
3. Check no crossing.

To check no crossing efficiently:
Sort all people by $S$.
For a query $[L, R]$, consider the subset.
If we process queries offline, sorted by something?
Maybe we can use a Segment Tree to maintain the "rightmost $T$" seen so far?
If we iterate $S$ from 1 to $N$, and maintain the set of active intervals (those with $S \le current$ and $T > current$).
For a new interval $[S, T]$, if there is an active interval $[S', T']$ with $S' < S < T' < T$, then crossing.
Also if $S' < S$ and $T' < T$, then nested (OK).
If $S' < S$ and $T' > T$, then crossing?
Wait, $S' < S < T < T'$. This is crossing.
So if we have an active interval $[S', T']$ (where $S' < S < T'$), then for a new $[S, T]$:
- If $T < T'$: Nested ($[S, T] \subset [S', T']$). OK.
- If $T > T'$: Crossing ($S' < S < T' < T$). Conflict.
So, if we maintain the set of active intervals, we need to ensure that for the new interval, all active intervals containing $S$ must have $T > T_{new}$.
Wait, if there are multiple active intervals containing $S$, they must be nested among themselves.
If they are nested, say $[S_1, T_1] \subset [S_2, T_2] \subset \dots$, then $T_1 < T_2 < \dots$.
When we encounter $[S, T]$, we need $T$ to be smaller than the smallest $T$ of any active interval that contains $S$?
No. If $[S, T]$ is nested inside $[S_1, T_1]$, then $T < T_1$.
If $[S, T]$ contains $[S_1, T_1]$, then $T > T_1$. But $S_1 < S$, so $[S_1, T_1]$ starts before $S$.
If $[S, T]$ contains $[S_1, T_1]$, then $S_1 < S$ and $T_1 < T$.
But we also need $S_1 < S < T_1 < T$ to be a crossing? No, $S_1 < S < T_1 < T$ is crossing.
If $T_1 < T$, then $[S_1, T_1]$ is not containing $S$?
Wait, active intervals are those with $S' < S < T'$.
So $S'$ starts before $S$, and ends after $S$.
If we have multiple such intervals, they must be nested.
Let $T_{min}$ be the minimum $T$ among all active intervals containing $S$.
If we add $[S, T]$:
- If $T < T_{min}$: Then $[S, T]$ is inside all active intervals. OK.
- If $T > T_{min}$: Then there exists an active interval $[S', T']$ with $T' < T$. Since $S' < S < T' < T$, this is a crossing. Conflict.
So, the condition is: **For every $S$, if we consider all intervals starting at or before $S$ and ending after $S$, their $T$ values must be such that any new interval starting at $S$ must have $T$ smaller than the minimum $T$ of the active ones.**
Wait, this must hold for the whole set.
Actually, this implies that if we process intervals by increasing $S$, the $T$ values of intervals that "overlap" at any point must be monotonic?
Specifically, if we sort all intervals by $S$, then for any $i < j$, if $S_i < S_j < T_i$, then we must have $T_j < T_i$ (nested) OR $T_j > T_i$ (crossing -> fail).
Wait, if $T_j > T_i$, then $S_i < S_j < T_i < T_j$ -> Crossing. Fail.
So if $S_i < S_j < T_i$, we MUST have $T_j < T_i$.
This means: **If we sort intervals by $S$, then for any $i$, all $j > i$ with $S_j < T_i$ must have $T_j < T_i$.**
This is equivalent to: **The sequence of $T$ values for intervals sorted by $S$ must be decreasing whenever the interval starts before the previous one ends.**
More simply: **There is no pair $(i, j)$ with $S_i < S_j < T_i < T_j$.**
This is exactly the condition that the intervals form a non-crossing family.
Combined with distinct $S$ and distinct $T$.

**Solution Strategy:**
1. **Distinct S**: Check if max frequency of $S$ in $[L, R]$ is 1.
2. **Distinct T**: Check if max frequency of $T$ in $[L, R]$ is 1.
3. **No Crossing**: Check if there exists $i, j \in [L, R]$ with $S_i < S_j < T_i < T_j$.
   This can be checked using a Segment Tree.
   Sort people by $S$.
   For each person $i$, we have a constraint: if there is any $j$ with $S_j < S_i < T_j$, then we must have $T_j > T_i$ (which is crossing) -> Fail.
   Wait, if $S_j < S_i < T_j$, then $j$ is an "active" interval at $S_i$.
   If $T_j < T_i$, then $i$ is nested in $j$. OK.
   If $T_j > T_i$, then crossing. Fail.
   So, for each $i$, we need $\max \{ T_j \mid S_j < S_i < T_j \} < T_i$?
   No. If there is any $j$ with $S_j < S_i < T_j$ and $T_j > T_i$, then fail.
   So we need: For all $i$, $\max \{ T_j \mid S_j < S_i < T_j \} \le T_i$?
   Wait, if $T_j = T_i$, then $S_j < S_i < T_j = T_i$.
   This means $S_j < S_i$ and $T_i = T_j$.
   This is the "Same End" conflict.
   So we need $\max \{ T_j \mid S_j < S_i < T_j \} < T_i$.
   If this holds for all $i$, then no crossing and no same-end conflict?
   What about same-start? $S_i = S_j$.
   If we sort by $S$, and handle same $S$ carefully.
   If $S_i = S_j$, then one must be inside other? No, same start conflict.
   So we need distinct $S$ as well.
   
   So the algorithm:
   - Build a Segment Tree over $1 \dots N$.
   - For each person $i$, update the range $[S_i, T_i-1]$ with value $T_i$. (Mark that at any point $x \in [S_i, T_i-1]$, there is an interval $i$ covering $x$ with end $T_i$).
   - Actually, we need to query: For a given $i$, what is the maximum $T_j$ among all $j$ such that $S_j < S_i < T_j$?
     This is equivalent to: Query the range $[S_i+1, T_i-1]$? No.
     The condition $S_j < S_i < T_j$ means $j$ covers $S_i$.
     So we need to query the maximum $T_j$ for all intervals covering $S_i$.
     But we only care about $j$ in the query range $[L, R]$.
     This is a 2D range query: Points $(S_j, T_j)$. Query: $S_j < S_i$ and $T_j > S_i$. Maximize $T_j$.
     Then check if max $T_j < T_i$.
   
   Since we have $Q$ queries, we can process offline.
   Sort queries by $S_i$? No, queries are ranges of people.
   We can use a Segment Tree over the people indices $1 \dots M$.
   But the condition depends on values $S, T$.
   
   Alternative:
   Use a Segment Tree over the coordinate $1 \dots N$.
   Each leaf $x$ stores the list of people covering $x$.
   Too slow.
   
   Better:
   Sort people by $S$.
   Use a Fenwick Tree / Segment Tree over $T$ coordinates.
   Iterate $S$ from 1 to $N$.
   Add people with $S_i = current$ to the data structure?
   No, we need to check for pairs in the query range.
   
   Let's use the property: **No crossing iff for all $i$, $\max \{ T_j \mid S_j < S_i < T_j \} < T_i$**.
   Also distinct $S$, distinct $T$.
   
   We can check "No crossing" by:
   Sort people by $S$.
   Maintain a data structure of active intervals (those with $S_j < current\_S < T_j$).
   For each $i$, we need to know if there is any active $j$ with $T_j > T_i$.
   This is equivalent to: $\max(T_{active}) > T_i$.
   So we maintain the maximum $T$ of active intervals.
   But we need to do this for subsets $[L, R]$.
   
   This looks like a 2D range maximum query.
   Points: $(S_j, j)$. Value: $T_j$.
   Condition: For a query $[L, R]$, and for each $i \in [L, R]$, check if $\exists j \in [L, R]$ such that $S_j < S_i < T_j$ and $T_j > T_i$.
   This is complex.
   
   Simpler approach:
   The condition "No crossing" is equivalent to: The intervals form a laminar family.
   We can check this by verifying that the set of intervals is non-crossing.
   A known technique: Sort intervals by $S$. If we have $S_i < S_j < T_i < T_j$, then crossing.
   We can check this by:
   Sort all people by $S$.
   Build a Segment Tree over the indices $1 \dots M$ (sorted by $S$).
   For each person $i$, we want to check if there is any $j$ in the query range such that $S_j < S_i < T_j$ and $T_j > T_i$.
   This is still hard.
   
   Wait, the sample solution hint says "sweep-line with BIT".
   Maybe we can check the condition: **For any $x$, the number of intervals covering $x$ is at most 1?**
   No, nested intervals cover the same points. $[1, 10]$ and $[2, 3]$ both cover $[2, 3]$. Count is 2.
   But they are valid.
   The invalid case is crossing.
   Crossing intervals $[1, 4]$ and $[2, 3]$? No, $[2, 3]$ is inside.
   Crossing: $[1, 4]$ and $[2, 5]$. Overlap $[2, 4]$.
   At any point $x$ in the overlap, we have two intervals.
   If they are nested, one contains the other.
   If they cross, they are not nested.
   How to distinguish?
   If we have two intervals $I_1, I_2$ overlapping.
   If $S_1 < S_2 < T_1 < T_2$, then they cross.
   If $S_1 < S_2 < T_2 < T_1$, then nested.
   If $S_1 < S_2$ and $T_1 < S_2$, disjoint.
   So, for any overlapping pair, we must have nesting.
   This implies that if we sort by $S$, the $T$ values must be decreasing for overlapping intervals.
   Specifically, if we have a set of intervals, sort by $S$.
   For any $i < j$, if $S_i < T_j$ (overlap), then we must have $T_j < T_i$.
   This means the sequence of $T$'s for overlapping intervals must be decreasing.
   So, for the subset $[L, R]$, if we sort them by $S$, then for any $i < j$ with $S_i < T_j$, we must have $T_j < T_i$.
   This is equivalent to: **There is no $i < j$ such that $S_i < S_j < T_i < T_j$.**
   
   Algorithm to check this for a range:
   Sort people by $S$.
   For each person $i$, define $next\_cross(i)$ as the smallest index $j > i$ such that $S_j < T_i$ and $T_j > T_i$.
   If such $j$ exists, then crossing.
   We need to check if for any $i \in [L, R]$, there exists $j \in [L, R]$ with $j > i$ and $S_j < T_i$ and $T_j > T_i$.
   This is a 2D range query: $j \in [i+1, R]$, $S_j \in [S_i+1, T_i-1]$, $T_j \in [T_i+1, N]$.
   We can solve this with a Segment Tree over $j$.
   Store pairs $(S_j, T_j)$.
   Query: Max $T_j$ in range $[i+1, R]$ with $S_j < T_i$.
   If max $T_j > T_i$, then crossing.
   Also check distinct $S$ and distinct $T$ using frequency arrays.
   
   Steps:
   1. Store people as $(S_i, T_i, i)$.
   2. Sort people by $S_i$.
   3. Build a Segment Tree over indices $1 \dots M$ (sorted order).
      Each node stores the max $T$ in its range.
      Actually, we need to query by $S_j$.
      So we need a 2D structure or offline processing.
      Offline: Sort queries by $T_i$?
      For a fixed $i$, we want to know if there is $j > i$ with $S_j < T_i$ and $T_j > T_i$.
      This is equivalent to: In the range $[i+1, R]$, is there any $j$ with $S_j < T_i$ and $T_j > T_i$?
      We can process queries offline.
      Sort queries by $R$.
      Iterate $R$ from 1 to $M$.
      Add person $R$ to the data structure.
      For a query $[L, R]$, we need to check all $i \in [L, R]$.
      This is too slow ($O(M \cdot Q)$).
      
   Optimization:
   We only need to check if **any** crossing exists.
   Condition: $\exists i \in [L, R]$ such that $\exists j \in [L, R], j > i, S_j < T_i, T_j > T_i$.
   This is equivalent to: $\max_{i \in [L, R]} (\text{something}) > \text{threshold}$.
   Actually, we can rewrite:
   For each $j$, let $min\_S_j = S_j$.
   We want to know if there is $i < j$ with $S_i < S_j < T_i$ and $T_i > T_j$.
   This is symmetric.
   
   Let's use the Segment Tree over the sorted people.
   Each leaf $j$ stores $T_j$.
   We want to query: $\max \{ T_j \mid j \in [L, R], S_j < T_i \}$ for each $i$.
   This is hard.
   
   Alternative:
   Check if the set of intervals is laminar.
   This can be done by checking if the "depth" is consistent.
   But given the constraints and the nature of the problem, the intended solution is likely:
   1. Check distinct $S$ and $T$ in range.
   2. Check no crossing.
   For no crossing, we can use a Segment Tree to store the minimum $S$ for a given $T$?
   Or: Sort by $S$. For each $i$, find the first $j > i$ with $S_j < T_i$.
   If $T_j > T_i$, crossing.
   We can precompute for each $i$, the smallest $j > i$ such that $S_j < T_i$. Let this be $next\_overlap[i]$.
   If $next\_overlap[i]$ exists and $T_{next\_overlap[i]} > T_i$, then $i$ crosses with $next\_overlap[i]$.
   Also, we need to check if this crossing partner is in $[L, R]$.
   So for each $i$, we have a "bad partner" $j$. If $i \in [L, R]$ and $j \in [L, R]$, then fail.
   We can store these bad pairs $(i, j)$ and check if any pair is fully contained in $[L, R]$.
   This is a standard problem: Given a set of segments $[i, j]$, is there any segment contained in $[L, R]$?
   We can solve this by checking if $\min(j) \ge L$ and $\max(i) \le R$? No.
   We need to check if there exists a pair $(i, j)$ such that $L \le i < j \le R$.
   This is equivalent to: Is there any pair $(i, j)$ with $i \ge L$ and $j \le R$?
   We can collect all such pairs and check if any satisfies $i \ge L$ and $j \le R$.
   This can be done with a Segment Tree or Fenwick Tree.
   Store pairs $(i, j)$. Query: $\min j$ for $i \in [L, R]$. If $\min j \le R$, then fail.
   Wait, we need to ensure $i < j$.
   So:
   1. Identify all crossing pairs $(i, j)$ with $i < j$.
   2. For each such pair, if both $i, j$ are in $[L, R]$, then answer is No.
   3. This is equivalent to: Is there any pair $(i, j)$ with $L \le i < j \le R$?
   4. We can store all such pairs in a list.
   5. Sort queries by $L$.
   6. Use a Segment Tree over $j$. Add pairs with $i \ge current\_L$.
   7. Query min $j$ in range $[L, R]$. If min $j \le R$, then fail.
   
   Steps refined:
   1. Sort people by $S$.
   2. For each $i$, find the smallest $j > i$ such that $S_j < T_i$. (Using a Segment Tree or two pointers).
      Let this be $next\_overlap[i]$.
      If $next\_overlap[i]$ exists and $T_{next\_overlap[i]} > T_i$, then $(i, next\_overlap[i])$ is a crossing pair.
      Store this pair.
      Note: We only need to store the first such $j$ because if $i$ crosses with $j$, it's invalid.
      Actually, if $i$ crosses with $j$, we just need to mark that pair.
   3. Also check distinct $S$ and $T$.
      Store positions of each $S$ and $T$.
      For distinct $S$: If $S$ appears $k$ times, we have $k(k-1)/2$ pairs.
      Actually, if $S$ appears $>1$ times in $[L, R]$, fail.
      We can check this by storing the list of indices for each $S$.
      For a query $[L, R]$, check if any list has $\ge 2$ indices in $[L, R]$.
      This is a standard problem: Given lists of points, check if any list has $\ge 2$ points in $[L, R]$.
      We can use a Segment Tree to store the count of occurrences.
      Or simpler: For each $S$, if it appears at indices $p_1, p_2, \dots$, then pairs $(p_k, p_{k+1})$ are bad.
      Check if any bad pair is in $[L, R]$.
      Same for $T$.
   4. Combine all bad pairs (crossing, same-S, same-T) into a single list of pairs $(u, v)$ with $u < v$.
   5. Check if any pair $(u, v)$ satisfies $L \le u < v \le R$.
      Use a Segment Tree over $v$. For each $u$, update position $v$ with value $u$.
      Query: $\min v$ for $u \in [L, R]$. If $\min v \le R$, then fail.
      Wait, we need to ensure $u \ge L$.
      So we can process queries by sorting $L$.
      Add pairs with $u \ge current\_L$.
      Query min $v$ in $[L, R]$.
      
   Complexity: $O((M+Q) \log M)$.
   This fits the constraints.

## worker: Implement the solution using the offline sweep-lin
1.  **Problem Analysis**: The problem asks if a subset of people's paths can be satisfied simultaneously. The constraints imply that the intervals $[S_i, T_i]$ must form a laminar family (nested or disjoint) and no two intervals can share endpoints. Specifically, we cannot have:
    *   Same Start ($S_i = S_j$)
    *   Same End ($T_i = T_j$)
    *   Crossing ($S_i < S_j < T_i < T_j$)
2.  **Algorithm**:
    *   **Same Start/End**: Group people by $S$ and $T$. For each group, any pair of indices forms a conflict. We generate all such pairs $(u, v)$ with $u < v$.
    *   **Crossing**: Sort people by $S$. For any two people $i, j$ with $S_i < S_j$, if they cross, it must be that $S_j < T_i < T_j$. Since $S$ is sorted, the only candidate for $j$ that could cross $i$ immediately after $i$ in the sorted list is $i+1$. If $S_{i+1} < T_i$ and $T_{i+1} > T_i$, then $(i, i+1)$ is a crossing pair. (Note: If $S_{i+1} \ge T_i$, no subsequent $j$ can satisfy $S_j < T_i$ because $S$ is non-decreasing).
    *   **Query Processing**: We need to check if any conflict pair $(u, v)$ is fully contained in $[L, R]$, i.e., $L \le u$ and $v \le R$.
    *   **Offline Sweep**: Sort queries by $L$ descending. Sort conflict pairs by $u$ descending. Iterate $L$ from $M$ down to 1. Add pairs with $u \ge L$ into a data structure (Fenwick Tree) at position $v$. For a query $(L, R)$, check if there is any marked position $\le R$ using a prefix sum query on the BIT. If `query(R) > 0`, a conflict exists.
3.  **Complexity**: Sorting takes $O(M \log M)$. Generating pairs takes $O(M)$. Sorting queries and pairs takes $O((M+Q) \log (M+Q))$. The sweep-line with BIT takes $O((M+Q) \log M)$. Total time complexity is dominated by sorting, $O((M+Q) \log M)$, which fits within the limits ($N, M, Q \le 4 \cdot 10^5$).

## worker: Generate "bad pairs" for same $S$ and same $T$ con
The solution implements an offline sweep-line algorithm to check for conflicts among a subset of people.
1.  **Conflict Identification**:
    *   **Same Start/End**: We group people by their start ($S$) and end ($T$) towns. Any two people sharing the same $S$ or same $T$ create a conflict. We generate all pairs $(u, v)$ from these groups.
    *   **Crossing**: We sort people by $S$. For any two people $i, j$ with $S_i < S_j$, they cross if $S_j < T_i < T_j$. Since $S$ is sorted, we only need to check the immediate next person in the sorted list ($j = i+1$) because if $S_{i+1} \ge T_i$, no subsequent person can satisfy $S_k < T_i$.
2.  **Query Processing**:
    *   A query $[L, R]$ is valid if and only if no conflict pair $(u, v)$ satisfies $L \le u < v \le R$.
    *   We sort queries by $L$ in descending order.
    *   We sort conflict pairs by $u$ in descending order.
    *   We iterate $L$ from $M$ down to 1. For each $L$, we add all conflict pairs with $u \ge L$ into a Fenwick Tree (BIT) at position $v$.
    *   For a query $(L, R)$, we check if there is any marked position $\le R$ in the BIT using a prefix sum query. If `query(R) > 0`, a conflict exists within the range.
3.  **Complexity**: Sorting takes $O(M \log M)$. Generating pairs takes $O(M)$. The sweep-line with BIT takes $O((M+Q) \log M)$. This fits well within the time limits.

## worker: Generate "bad pairs" for crossing intervals ($S_i 
The solution implements an offline sweep-line algorithm to efficiently check for conflicts among a subset of people.
1.  **Conflict Identification**:
    *   **Same Start/End**: We group people by their start ($S$) and end ($T$) towns. Any two people sharing the same $S$ or same $T$ create a conflict. We generate all pairs $(u, v)$ from these groups.
    *   **Crossing**: We sort people by $S$. For any two people $i, j$ with $S_i < S_j$, they cross if $S_j < T_i < T_j$. Since $S$ is sorted, we only need to check the immediate next person in the sorted list ($j = i+1$) because if $S_{i+1} \ge T_i$, no subsequent person can satisfy $S_k < T_i$.
2.  **Query Processing**:
    *   A query $[L, R]$ is valid if and only if no conflict pair $(u, v)$ satisfies $L \le u < v \le R$.
    *   We sort queries by $L$ in descending order.
    *   We sort conflict pairs by $u$ in descending order.
    *   We iterate $L$ from $M$ down to 1. For each $L$, we add all conflict pairs with $u \ge L$ into a Fenwick Tree (BIT) at position $v$.
    *   For a query $(L, R)$, we check if there is any marked position $\le R$ in the BIT using a prefix sum query. If `query(R) > 0`, a conflict exists within the range.
3.  **Complexity**: Sorting takes $O(M \log M)$. Generating pairs takes $O(M)$. The sweep-line with BIT takes $O((M+Q) \log M)$. This fits well within the time limits.

## worker: Generate "bad pairs" for crossing intervals ($S_i 
The solution implements an offline sweep-line algorithm to efficiently check for conflicts among a subset of people.
1.  **Conflict Identification**:
    *   **Same Start/End**: We group people by their start ($S$) and end ($T$) towns. Any two people sharing the same $S$ or same $T$ create a conflict. We generate all pairs $(u, v)$ from these groups.
    *   **Crossing**: We sort people by $S$. For any two people $i, j$ with $S_i < S_j$, they cross if $S_j < T_i < T_j$. Since $S$ is sorted, we only need to check the immediate next person in the sorted list ($j = i+1$) because if $S_{i+1} \ge T_i$, no subsequent person can satisfy $S_k < T_i$.
2.  **Query Processing**:
    *   A query $[L, R]$ is valid if and only if no conflict pair $(u, v)$ satisfies $L \le u < v \le R$.
    *   We sort queries by $L$ in descending order.
    *   We sort conflict pairs by $u$ in descending order.
    *   We iterate $L$ from $M$ down to 1. For each $L$, we add all conflict pairs with $u \ge L$ into a Fenwick Tree (BIT) at position $v$.
    *   For a query $(L, R)$, we check if there is any marked position $\le R$ in the BIT using a prefix sum query. If `query(R) > 0`, a conflict exists within the range.
3.  **Complexity**: Sorting takes $O(M \log M)$. Generating pairs takes $O(M)$. The sweep-line with BIT takes $O((M+Q) \log M)$. This fits well within the time limits.

## worker: finalize
The solution implements an offline sweep-line algorithm to efficiently check for conflicts among a subset of people.
1.  **Conflict Identification**:
    *   **Same Start/End**: We group people by their start ($S$) and end ($T$) towns. Any two people sharing the same $S$ or same $T$ create a conflict. We generate all pairs $(u, v)$ from these groups.
    *   **Crossing**: We sort people by $S$. For any two people $i, j$ with $S_i < S_j$, they cross if $S_j < T_i < T_j$. Since $S$ is sorted, we only need to check the immediate next person in the sorted list ($j = i+1$) because if $S_{i+1} \ge T_i$, no subsequent person can satisfy $S_k < T_i$.
2.  **Query Processing**:
    *   A query $[L, R]$ is valid if and only if no conflict pair $(u, v)$ satisfies $L \le u < v \le R$.
    *   We sort queries by $L$ in descending order.
    *   We sort conflict pairs by $u$ in descending order.
    *   We iterate $L$ from $M$ down to 1. For each $L$, we add all conflict pairs with $u \ge L$ into a Fenwick Tree (BIT) at position $v$.
    *   For a query $(L, R)$, we check if there is any marked position $\le R$ in the BIT using a prefix sum query. If `query(R) > 0`, a conflict exists within the range.
3.  **Complexity**: Sorting takes $O(M \log M)$. Generating pairs takes $O(M)$. The sweep-line with BIT takes $O((M+Q) \log M)$. This fits well within the time limits.

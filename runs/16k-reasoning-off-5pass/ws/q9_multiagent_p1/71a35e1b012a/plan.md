The problem requires covering every index $j \in [1, N]$ with at least one operation that sets $x_j=1$. Operation 1 covers $[L_i, R_i]$, while Operation 2 covers $[1, L_i-1] \cup [R_i+1, N]$. We can model this as a set cover problem where we need to select a subset of operations (and their types) to cover all positions. Since $N$ is large, we cannot iterate over positions directly for the DP state, but we can process intervals. A greedy approach or a flow-based approach might work, but given the specific structure (union of intervals and complements), we can rephrase: for each position $j$, it must be covered by either an Op1 covering $j$ or an Op2 covering $j$. An Op2 covering $j$ means the interval $[L_i, R_i]$ does *not* contain $j$. This is equivalent to saying $j < L_i$ or $j > R_i$. 

Actually, a simpler perspective is needed. Let's consider the complement: which positions are *not* covered by any chosen Op1? Those must be covered by Op2. However, choosing Op2 for an interval $[L, R]$ covers everything *outside* it. If we choose Op1 for some intervals and Op2 for others, the union of the "covered by Op1" sets and the "covered by Op2" sets must be $[1, N]$.
Wait, the cost is per operation instance. We process $M$ operations. For each $i$, we choose type 0, 1, or 2.
If we choose type 1, we cover $[L_i, R_i]$.
If we choose type 2, we cover $[1, L_i-1] \cup [R_i+1, N]$.
We need $\bigcup_{i \in S_1} [L_i, R_i] \cup \bigcup_{i \in S_2} ([1, L_i-1] \cup [R_i+1, N]) = [1, N]$.
This looks like we can determine the necessary coverage for each segment.
Actually, this problem can be solved by checking if the union of all possible "Op1" intervals covers everything, or if the union of all possible "Op2" intervals covers everything, or a mix.
But notice: Op2 on $[L, R]$ is very powerful; it covers almost everything except $[L, R]$.
Let's reconsider the constraints. $N, M$ up to $10^6, 2*10^5$.
Maybe we can iterate through the "gaps".
Let's define $A$ as the set of indices covered by at least one Op1. Let $B$ as the set of indices covered by at least one Op2. We need $A \cup B = [1, N]$.
This is equivalent to: for every $j$, either $j \in A$ or $j \in B$.
$j \notin A \implies$ no Op1 covers $j$. Then we *must* have $j \in B$.
$j \notin B \implies$ no Op2 covers $j$. Then we *must* have $j \in A$.
Note that $j \in B$ means there exists some $i \in S_2$ such that $j < L_i$ or $j > R_i$.
$j \notin B$ means for all $i \in S_2$, $L_i \le j \le R_i$. i.e., $j$ is inside every chosen Op2 interval.
Similarly, $j \notin A$ means for all $i \in S_1$, $j \notin [L_i, R_i]$.

This looks like we can determine the minimal set of Op1s and Op2s.
Actually, there is a known trick for this specific problem (it appeared in a contest).
Consider the intervals $[L_i, R_i]$.
If we pick Op1 for $i$, we cover $[L_i, R_i]$.
If we pick Op2 for $i$, we cover $[1, L_i-1] \cup [R_i+1, N]$.
Let's try to cover the "hardest" points.
Actually, we can solve this by iterating $j$ from 1 to $N$ and maintaining the current coverage? No, $N$ is too big for linear scan if we do complex logic, but $O(N)$ is fine. $2 \cdot 10^5$ operations, $10^6$ points. $O(N+M)$ is acceptable.
Algorithm idea:
We need to cover $[1, N]$.
Let's try a greedy strategy from left to right?
Or maybe we can determine the minimum cost by checking specific conditions.
Wait, if we select a set of Op1s, the uncovered parts must be covered by Op2s.
The uncovered parts by Op1s are a set of disjoint intervals. For each such gap $(u, v)$, we need at least one Op2 that covers $(u, v)$. An Op2 covers $(u, v)$ if its interval $[L, R]$ satisfies $R < u$ or $L > v$.
So, if we fix the set of Op1s, we need to cover the gaps with Op2s.
Conversely, if we fix Op2s, the uncovered parts (which are intersections of $[L_i, R_i]$ for all chosen Op2s) must be covered by Op1s.
This suggests we can iterate on the number of Op1s? No.

Let's rethink. Is it possible that we only need to cover specific critical points?
Actually, the problem can be transformed.
Let $U$ be the union of all $[L_i, R_i]$. If $U = [1, N]$, we can just pick Op1 for all $i$ that are part of a cover? No, we need to pick specific types.
If we pick Op1 for all $i$, cost is $|S_1|$. If we pick Op2 for all $i$, cost is $|S_2|$.
We want to minimize $|S_1| + |S_2|$.
Let's consider the complement.
Suppose we decide NOT to pick Op1 for a set of indices $I_{no1}$. Then for every $j$ not covered by the remaining Op1s, we MUST pick Op2 for some $i$ such that $j \notin [L_i, R_i]$.
This seems complicated.

Alternative approach:
Consider the intervals $[L_i, R_i]$.
Let's compute the "coverage" of Op1s.
Actually, let's look at the gaps between the union of all $[L_i, R_i]$.
Let the union of all $[L_i, R_i]$ be $U$.
If $U \neq [1, N]$, there are gaps. These gaps MUST be covered by Op2.
Specifically, if there is a gap $(a, b)$ (meaning $a, a+1, \dots, b$ are not in any $[L_i, R_i]$), then for any $j \in (a, b)$, no Op1 can cover $j$. Thus, we MUST pick Op2 for some $i$ such that $j \notin [L_i, R_i]$. Since $j$ is not in any $[L_i, R_i]$ at all (by definition of the gap in the union of ALL intervals), ANY Op2 will cover $j$ (because Op2 covers everything outside $[L_i, R_i]$, and $j$ is outside all $[L_k, R_k]$).
Wait, if $j$ is not in any $[L_i, R_i]$, then for ANY $i$, $j \notin [L_i, R_i]$, so Op2 on $i$ covers $j$.
So if there are gaps in the union of all intervals, we just need to pick at least one Op2 to cover those gaps?
Actually, if we pick Op2 for ANY $i$, it covers everything outside $[L_i, R_i]$.
If the union of all $[L_i, R_i]$ is NOT $[1, N]$, let the gaps be $G_1, G_2, \dots$.
For any $j \in G_k$, we need an Op2.
If we pick Op2 for a specific $i$, it covers all $j \notin [L_i, R_i]$.
If we pick Op2 for ALL $i$, we cover everything except $\bigcap [L_i, R_i]$.
If $\bigcap [L_i, R_i]$ is empty, then Op2 for all $i$ covers everything.
But we want to minimize cost.

Let's refine the strategy:
1. Calculate the union of all $[L_i, R_i]$. Let this be $U$.
2. If $U \neq [1, N]$, there are gaps. Let the gaps be intervals $(a, b)$. For any $j$ in a gap, we MUST use Op2.
   To cover a gap $(a, b)$, we need at least one $i$ such that we choose Op2 and $j \notin [L_i, R_i]$. But since $j$ is not in ANY $[L_i, R_i]$, ANY Op2 choice covers $j$.
   So, if there are gaps, we just need to pick at least one Op2?
   Wait. If we pick Op2 for $i$, we cover $[1, L_i-1] \cup [R_i+1, N]$.
   If we have a gap $(a, b)$, it means for all $k$, $[L_k, R_k] \cap (a, b) = \emptyset$.
   So for any $i$, $(a, b) \subseteq [1, L_i-1] \cup [R_i+1, N]$.
   So picking Op2 for ANY single $i$ covers the entire gap $(a, b)$.
   So if there are gaps, we just need to pick at least one Op2?
   But wait, picking one Op2 might not cover the rest of the array.
   Example: $N=5$, intervals $[2, 3]$. Union is $[2, 3]$. Gaps: $[1, 1]$ and $[4, 5]$.
   Pick Op2 for $[2, 3]$: covers $[1, 1] \cup [4, 5]$. Now $[2, 3]$ is not covered by Op2.
   So we need to cover $[2, 3]$ with Op1.
   So we pick Op1 for $[2, 3]$ and Op2 for $[2, 3]$. Cost 2.
   Is it possible to do better?
   Maybe pick Op1 for nothing? Then we need Op2 to cover everything. Op2 covers complement of $[2, 3]$. $[2, 3]$ remains 0. Fail.
   So we need Op1 to cover the "holes" of the Op2s.

General Logic:
Let $S_1$ be the set of indices where we choose Op1.
Let $S_2$ be the set of indices where we choose Op2.
Condition: $(\bigcup_{i \in S_1} [L_i, R_i]) \cup (\bigcup_{i \in S_2} ([1, L_i-1] \cup [R_i+1, N])) = [1, N]$.
This is equivalent to: For every $j \in [1, N]$, either ($\exists i \in S_1, j \in [L_i, R_i]$) OR ($\exists i \in S_2, j \notin [L_i, R_i]$).
Let $U_1 = \bigcup_{i \in S_1} [L_i, R_i]$.
Let $U_2 = \bigcup_{i \in S_2} ([1, L_i-1] \cup [R_i+1, N])$.
We need $U_1 \cup U_2 = [1, N]$.
Note that $U_2$ is the complement of $\bigcap_{i \in S_2} [L_i, R_i]$.
Let $I_{S_2} = \bigcap_{i \in S_2} [L_i, R_i]$. Then $U_2 = [1, N] \setminus I_{S_2}$.
So we need $U_1 \cup ([1, N] \setminus I_{S_2}) = [1, N]$.
This is equivalent to $U_1 \supseteq I_{S_2}$.
So the condition simplifies to: The union of intervals chosen for Op1 must cover the intersection of intervals chosen for Op2.
We want to minimize $|S_1| + |S_2|$.
We can iterate over all possible sets $S_2$? No, too many.
However, $I_{S_2}$ is an intersection of intervals, so it is also an interval (or empty).
Let $I_{S_2} = [L_{max}, R_{min}]$ where $L_{max} = \max_{i \in S_2} L_i$ and $R_{min} = \min_{i \in S_2} R_i$.
If $S_2 = \emptyset$, then $I_{S_2} = [1, N]$ (by convention, intersection of empty set is the whole space? No, if $S_2$ is empty, $U_2$ is empty, so we need $U_1 = [1, N]$. This corresponds to $I_{S_2} = [1, N]$ effectively).
If $S_2 \neq \emptyset$, $I_{S_2} = [\max L_i, \min R_i]$. If $\max L_i > \min R_i$, the intersection is empty. In this case, $U_2 = [1, N]$, so condition $U_1 \supseteq \emptyset$ is always true. We just need to ensure $S_2$ makes the intersection empty?
Wait, if intersection is empty, $U_2 = [1, N]$, so we are done regardless of $S_1$. We can set $S_1 = \emptyset$.
So if we can find a non-empty $S_2$ such that $\bigcap_{i \in S_2} [L_i, R_i] = \emptyset$, then cost is $|S_2|$. We want to minimize $|S_2|$.
This is the "hitting set" problem? No, we want the intersection to be empty.
Intersection of $[L_i, R_i]$ is empty iff there is no point common to all.
This is equivalent to: there exist $i, k \in S_2$ such that $[L_i, R_i] \cap [L_k, R_k] = \emptyset$? No, pairwise disjoint doesn't imply total intersection empty (e.g., 3 intervals).
Actually, intersection of a set of intervals is empty iff the max of left endpoints > min of right endpoints.
So we need to find a subset $S_2$ such that $\max_{i \in S_2} L_i > \min_{i \in S_2} R_i$.
To minimize $|S_2|$, we can try small sizes.
Size 1: $[L_i, R_i]$ is never empty.
Size 2: Find $i, k$ such that $L_i > R_k$ or $L_k > R_i$. i.e., disjoint intervals.
If we find two disjoint intervals, say $[L_i, R_i]$ and $[L_k, R_k]$ with $R_i < L_k$, then intersection is empty. Cost 2.
Can we do size 1? No.
So if there exist two disjoint intervals, min cost is 2 (using only Op2).
What if all intervals overlap? Then for any $S_2$, intersection is non-empty.
Then we need $U_1 \supseteq I_{S_2}$.
We want to minimize $|S_1| + |S_2|$.
Let $I = I_{S_2} = [L_{max}, R_{min}]$. We need to cover $I$ with $S_1$.
Cost = $|S_1| + |S_2|$.
We can iterate over all possible intervals $I$ that can be formed as an intersection of some $S_2$?
The possible intersections are of the form $[\max L_{subset}, \min R_{subset}]$.
Actually, the intersection of a subset is determined by the element with max L and min R in that subset.
Let's consider all pairs $(i, k)$. If we pick $S_2 = \{i, k\}$, intersection is $[\max(L_i, L_k), \min(R_i, R_k)]$.
If we add more elements to $S_2$, the intersection shrinks (or stays same).
So the "critical" intersections are formed by subsets of size 2? Or maybe size 1?
Actually, if we fix the intersection interval $I = [A, B]$, we need to cover $[A, B]$ with minimum number of Op1s.
And we need to form $I$ using minimum number of Op2s.
But forming $I$ requires that for all $j \in S_2$, $[L_j, R_j] \supseteq I$.
So $S_2$ must be a subset of $\{i \mid L_i \le A \text{ and } R_i \ge B\}$.
To minimize $|S_2|$, we should pick the smallest subset of such intervals whose intersection is exactly $[A, B]$?
Actually, if we pick ANY subset of intervals that all contain $[A, B]$, their intersection will contain $[A, B]$. It might be larger.
But we defined $I$ as the intersection. So we need the intersection to be exactly $[A, B]$.
This means $\max_{i \in S_2} L_i = A$ and $\min_{i \in S_2} R_i = B$.
So we need to pick at least one $i$ with $L_i = A$ and one $k$ with $R_k = B$, and all others must contain $[A, B]$.
To minimize $|S_2|$, we can just pick one $i$ with $L_i=A$ and one $k$ with $R_k=B$?
Wait, if we pick just $\{i, k\}$, intersection is $[\max(L_i, L_k), \min(R_i, R_k)]$.
We need this to be $[A, B]$.
So we need $L_i=A, R_k=B$ and $L_k \le A, R_i \ge B$.
So for a fixed $[A, B]$, we need to find if there exists $i, k$ such that $L_i=A, R_k=B, L_k \le A, R_i \ge B$.
If so, $|S_2| = 2$.
If we can find such a pair, cost is $2 + \text{min\_cover}(A, B)$.
What if we need $|S_2| = 1$? Then intersection is $[L_i, R_i]$. So $A=L_i, B=R_i$.
Cost $1 + \text{min\_cover}(L_i, R_i)$.
What if $|S_2| = 3$? Intersection is determined by max L and min R.
Generally, the intersection is determined by the "tightest" constraints.
So we can iterate over all possible $A$ and $B$ that appear as $L_i$ or $R_i$?
There are $O(M)$ such values. $O(M^2)$ is too slow ($4 \cdot 10^{10}$).
We need a better way.

Let's re-evaluate the condition: $U_1 \supseteq I_{S_2}$.
Case 1: $I_{S_2} = \emptyset$. Then any $S_1$ works (even empty). Minimize $|S_2|$.
As discussed, min $|S_2|$ for empty intersection is 2 (if there are two disjoint intervals). If all intervals intersect, impossible to get empty intersection with finite set? No, if all intersect, intersection of all is non-empty. But we can pick a subset? If all pairwise intersect, Helly's theorem in 1D says total intersection is non-empty. So if all intervals intersect, we cannot get empty intersection.
So if all intervals intersect, Case 1 is impossible.
If there are disjoint intervals, min $|S_2| = 2$. Cost = 2. (Since $S_1$ can be empty).
Wait, if we pick two disjoint intervals $i, k$, intersection is empty. $U_2 = [1, N]$. $S_1 = \emptyset$. Total cost 2.
Is it possible to get cost 1?
If $|S_2|=1$, intersection is $[L_i, R_i] \neq \emptyset$. Need $U_1 \supseteq [L_i, R_i]$.
If $|S_1|=0$, need $[L_i, R_i] = \emptyset$ (impossible).
So cost 1 is impossible if we rely on empty intersection.
What if $|S_1|=1, S_2=\emptyset$? Then $U_1 = [L_i, R_i]$. Need $[L_i, R_i] = [1, N]$. If there is an interval $[1, N]$, cost 1.
So if there is an interval $[1, N]$, answer is 1 (Op1).
If not, check if there are two disjoint intervals -> cost 2 (Op2, Op2).
If neither, we need mixed.
Mixed: $S_2 \neq \emptyset, S_1 \neq \emptyset$.
We need $U_1 \supseteq I_{S_2}$.
Let $I = [A, B] = I_{S_2}$.
We need to cover $[A, B]$ with minimum Op1s.
And we need to form $[A, B]$ with minimum Op2s.
To form $[A, B]$ with $k$ Op2s, we need $k$ intervals such that their intersection is $[A, B]$.
Actually, we can just pick the minimal set of intervals that "force" the intersection to be $[A, B]$.
The intersection of a set of intervals containing $[A, B]$ is $[\max L, \min R]$.
To get exactly $[A, B]$, we need at least one interval with $L=A$ and one with $R=B$.
And all chosen intervals must contain $[A, B]$.
So we need to pick a set $S_2 \subseteq \{i \mid L_i \le A, R_i \ge B\}$ such that $\max_{i \in S_2} L_i = A$ and $\min_{i \in S_2} R_i = B$.
To minimize $|S_2|$, we can just pick one $i$ with $L_i=A$ and one $k$ with $R_k=B$ (provided $L_k \le A$ and $R_i \ge B$).
If such a pair exists, $|S_2|=2$.
If no such pair exists, maybe we need more?
Actually, if we pick one $i$ with $L_i=A$, then $\max L = A$. We need $\min R = B$.
So we need to pick some $k$ with $R_k=B$ such that $L_k \le A$.
If we find such $k$, we are done with $|S_2|=2$.
If not, maybe we need to pick multiple to reduce the min R?
No, if we pick multiple, the min R is the minimum of their R's.
So we just need at least one $k$ with $R_k=B$ and $L_k \le A$.
If no such $k$ exists, then for all $k$ with $R_k=B$, $L_k > A$. Then intersection of any set containing such $k$ and $i$ (with $L_i=A$) will have $\max L \ge L_k > A$. So intersection starts after $A$.
Thus, if we want intersection to start at $A$, we MUST include an interval with $L=A$.
And to end at $B$, we MUST include an interval with $R=B$.
And they must be compatible ($L_{end} \le A, R_{start} \ge B$).
So for a fixed $[A, B]$, minimal $|S_2|$ is 2 if there exists $i, k$ with $L_i=A, R_k=B, L_k \le A, R_i \ge B$.
Otherwise, we cannot form $[A, B]$ with 2 intervals. Can we with more?
If we pick $i$ with $L_i=A$ and $k$ with $R_k=B$, but $L_k > A$, then intersection is $[L_k, B]$. This is a different interval.
So we can only form intervals $[A, B]$ where there exists a pair satisfying the condition.
So the candidate intervals $[A, B]$ are those where $\exists i, k$ such that $L_i=A, R_k=B, L_k \le A, R_i \ge B$.
Note that $A$ must be some $L_i$ and $B$ must be some $R_k$.
So we can iterate over all pairs $(i, k)$? $O(M^2)$ is too slow.
But notice: we only care about $A = L_i$ and $B = R_k$.
Condition: $L_k \le L_i$ and $R_i \ge R_k$.
This means interval $k$ starts before or at $i$'s start, and ends after or at $i$'s end.
So $k$ "contains" $i$? No, $k$ starts earlier and ends later. Yes, $k$ contains $i$.
So if we pick $i$ and $k$ where $k$ contains $i$, intersection is $[L_k, R_k]$? No.
Intersection of $[L_i, R_i]$ and $[L_k, R_k]$ where $L_k \le L_i$ and $R_i \le R_k$ is $[L_i, R_i]$.
Wait, my condition was $L_k \le A$ and $R_i \ge B$.
If $A=L_i, B=R_k$, then $L_k \le L_i$ and $R_i \ge R_k$.
Intersection is $[\max(L_i, L_k), \min(R_i, R_k)] = [L_i, R_k]$ (since $L_k \le L_i$ and $R_k \le R_i$).
So the intersection is $[L_i, R_k]$.
So the candidate intervals are $[L_i, R_k]$ where $L_k \le L_i$ and $R_k \le R_i$.
This means $[L_i, R_k] \subseteq [L_k, R_i]$.
So we are looking for pairs $(i, k)$ such that $[L_i, R_k] \subseteq [L_k, R_i]$.
Then the intersection is $[L_i, R_k]$.
We need to cover $[L_i, R_k]$ with Op1s.
Cost = $2 + \text{min\_cover}(L_i, R_k)$.
We want to minimize this over all valid pairs.
Also consider $|S_2|=1$: Interval $[L_i, R_i]$. Cost $1 + \text{min\_cover}(L_i, R_i)$.
Also consider $|S_1|=1, S_2=\emptyset$: Interval $[1, N]$. If exists $[1, N]$, cost 1.
Also consider $|S_2|=2$ disjoint: Cost 2.

So the algorithm:
1. Check if any interval is $[1, N]$. If yes, ans = 1, op = 1 for that interval, 0 others.
2. Check if there exist two disjoint intervals. If yes, ans = 2, ops = 2 for those two, 0 others.
3. Otherwise, iterate over all pairs $(i, k)$ such that $L_k \le L_i$ and $R_k \le R_i$.
   The intersection is $[L_i, R_k]$.
   We need to cover $[L_i, R_k]$ with minimum Op1s.
   How to compute min Op1s to cover $[A, B]$?
   This is the classic interval cover problem.
   Given a set of intervals, find min subset to cover $[A, B]$.
   Since we have $M$ intervals, we can precompute this?
   But we have $O(M^2)$ pairs.
   However, notice that for a fixed $i$, we want to find $k$ such that $L_k \le L_i$ and $R_k \le R_i$ and $R_k$ is maximized?
   No, we want to minimize $2 + \text{cover}(L_i, R_k)$.
   Cover cost depends on $L_i$ and $R_k$.
   Actually, the cover cost for $[A, B]$ is monotonic with respect to $A$ and $B$.
   Larger interval -> larger or equal cost.
   So for a fixed $i$, we want to maximize $R_k$ (to make interval smaller) subject to $R_k \le R_i$ and $L_k \le L_i$.
   Let $R_{max}(L) = \max \{ R_k \mid L_k \le L \}$.
   Then for fixed $i$, best $k$ has $R_k = R_{max}(L_i)$.
   Then interval is $[L_i, R_{max}(L_i)]$.
   We need to check if $R_{max}(L_i) \le R_i$. If so, valid.
   Then cost = $2 + \text{cover}(L_i, R_{max}(L_i))$.
   We can iterate $i$ from 1 to $M$, compute this, and take min.
   Also check $1 + \text{cover}(L_i, R_i)$ for all $i$.
   
   How to compute cover cost efficiently?
   Cover $[A, B]$ with intervals $[L_j, R_j]$.
   Greedy: Start at $curr = A$. Find interval with $L_j \le curr$ and max $R_j$. Update $curr = \max R_j$. Repeat until $curr \ge B$.
   This takes $O(M)$ per query. Total $O(M^2)$. Too slow.
   We need $O(1)$ or $O(\log M)$ per query.
   We can precompute the cover cost for all possible $[A, B]$? No.
   But notice we only query $[L_i, R']$ where $R' = R_{max}(L_i)$.
   Maybe we can optimize the greedy.
   Actually, the number of distinct intervals is $M$.
   We can precompute the "next jump" for each starting point?
   Or simply, since we only need the minimum cost, and $M$ is $2 \cdot 10^5$, maybe $O(M \log M)$ is fine.
   We can sort intervals by L.
   For a fixed $A$, we want to cover $[A, B]$.
   This is standard.
   But we have many queries.
   Wait, the queries are of the form $[L_i, R_{max}(L_i)]$.
   Let's just implement the greedy with a segment tree or similar to find the best interval?
   Actually, we can precompute the "reach" from any point $x$.
   Let $next\_reach[x]$ be the max $R$ of an interval starting $\le x$.
   This is easy: $next\_reach[x] = \max_{j: L_j \le x} R_j$.
   Then from $x$, we jump to $next\_reach[x]$.
   But we need to count steps.
   This is a functional graph (or path). We can use binary lifting (doubling) to find the number of steps to reach $\ge B$.
   Preprocessing: $O(M \log M)$ or $O(M)$.
   Query: $O(\log M)$.
   Total: $O(M \log M)$.
   
   Steps:
   1. Read input.
   2. Check for $[1, N]$ -> cost 1.
   3. Check for disjoint pair -> cost 2.
   4. Precompute $next\_reach[x]$ for all $x \in [1, N]$.
      Actually, we only need it for $x = L_i$.
      But $L_i$ can be up to $N$.
      We can compute an array `max_R` of size $N+1$.
      `max_R[x] = max(R_j for all j with L_j <= x)`.
      This can be done by sorting intervals by L and prefix max.
   5. Build binary lifting table `up[k][i]` = the position reached after $2^k$ steps starting from $i$.
      Wait, the state is the current covered end.
      From current end $curr$, we can jump to $next\_reach[curr]$.
      But $next\_reach[curr]$ might be the same as $curr$ if no interval starts $\le curr$ extends beyond $curr$.
      We need to handle this.
      Actually, the greedy strategy:
      Current covered $[A, B]$. We need to cover $A$.
      Find interval with $L \le A$ and max $R$. Let this be $R_{new}$.
      If $R_{new} < A$, then impossible (but we assume we can cover, or return infinity).
      New covered $[A, R_{new}]$.
      Next step: find interval with $L \le R_{new}$ and max $R$.
      So the transition is $f(x) = \max \{ R_j \mid L_j \le x \}$.
      We want to find min $k$ such that $f^k(A) \ge B$.
      We can precompute $f(x)$ for all $x$.
      Then build doubling table.
      Query $A, B$: find smallest $k$ such that $f^k(A) \ge B$.
      This gives the number of Op1s needed.
   6. Iterate all $i$:
      $A = L_i$.
      $B_{cand} = \max \{ R_k \mid L_k \le A \text{ and } R_k \le R_i \}$.
      Actually, we want $R_k \le R_i$ and $L_k \le A$.
      To minimize cover cost, we want $B_{cand}$ to be as large as possible (closest to $R_i$).
      So $B_{cand} = \min(R_i, \max \{ R_k \mid L_k \le A \})$.
      Let $M_A = \max \{ R_k \mid L_k \le A \}$.
      If $M_A < A$, then we cannot even start covering $A$ with Op1s?
      Wait, if $M_A < A$, then no interval covers $A$. So cover cost is infinity.
      If $M_A \ge A$, then we can cover.
      The interval to cover is $[A, \min(R_i, M_A)]$.
      Let $Target = \min(R_i, M_A)$.
      If $Target < A$, impossible.
      Else, cost = $2 + \text{steps}(A, Target)$.
      Update global min.
   7. Also check $1 + \text{steps}(L_i, R_i)$ for all $i$.
   8. Output result.

   Corner cases:
   - If no solution found, output -1.
   - When checking disjoint, if found, cost 2. But maybe cost 1 is possible? (Checked first).
   - If $Target == A$, steps = 0? No, if $Target == A$, we need to cover $[A, A]$.
     If there is an interval covering $A$, steps=1?
     Wait, if $Target == A$, it means we need to cover a single point $A$.
     We need at least one interval covering $A$.
     So steps = 1 if $M_A \ge A$.
     My doubling logic: $f(A) = M_A$. If $M_A \ge A$, then 1 step reaches $M_A \ge A$.
     So if $Target == A$, we need 1 step.
     Correct.

   Complexity:
   - Precompute $M_A$: $O(N)$ or $O(M \log M)$.
   - Build doubling: $O(N \log N)$.
   - Iterate $M$ times, each query $O(\log N)$.
   - Total $O(N \log N + M \log N)$. Acceptable.

   One detail: The doubling table size. $N=10^6$, $\log N \approx 20$. Table size $20 \times 10^6$ ints = 80MB. OK.

   Implementation details:
   - Arrays 1-indexed.
   - Handle $M_A < A$ case.
   - Handle $Target < A$ case.
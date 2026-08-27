The problem asks for the sum of distances between two nodes $u$ and $v$ over all $(N-1)!$ possible trees formed by choices $P_i \in \{1, \dots, i-1\}$. The distance between $u$ and $v$ is the sum of weights of edges on the unique path. By linearity of expectation (or summation), we can calculate the contribution of each edge $i$ (connecting $i$ to $P_i$ with weight $A_i$) to the total distance. An edge $i$ contributes $A_i$ to the path between $u$ and $v$ if and only if the path passes through the edge connecting $i$ and $P_i$. In the random tree structure defined by $P$, the edge $i$ connects $i$ to some ancestor $P_i < i$. The edge $i$ lies on the path between $u$ and $v$ if and only if one of $u, v$ is in the subtree of $i$ (when rooted at 1) and the other is not. However, since the parent $P_i$ is chosen uniformly from $1 \dots i-1$, the structure is specific. Actually, a simpler view is: for a fixed $i$, the edge $(i, P_i)$ is on the path between $u$ and $v$ if $i$ is an ancestor of one node and $P_i$ is an ancestor of the other, or more simply, if the path goes "through" $i$.
Let's re-evaluate the condition. The tree is built such that $i$'s parent is $P_i < i$. This means $i$ is always a descendant of $P_i$. The edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if $u$ is in the component containing $i$ when the edge is removed, and $v$ is in the component containing $P_i$, OR vice versa. Since $P_i < i$, $P_i$ is "above" $i$. The set of nodes that are descendants of $i$ (including $i$) depends on the choices of $P_j$ for $j > i$. Specifically, $j$ is a descendant of $i$ if $P_j = i$ or $P_j = k$ where $k$ is a descendant of $i$.
Actually, there is a known combinatorial property for this specific random tree model (often related to "random recursive trees" but with fixed weights and specific parent constraints). In this model, for any $i$, the probability that $i$ is an ancestor of a specific node $x$ ($x > i$) is $1/(i-1)$? No.
Let's use the linearity of expectation on edges. For a specific $i$, the edge $(i, P_i)$ has weight $A_i$. It contributes to the distance $d(u, v)$ if $u$ and $v$ are separated by this edge.
The edge $(i, P_i)$ separates the tree into two sets: $S_i$ (nodes that are descendants of $i$ in the final tree) and $V \setminus S_i$. Note that $i \in S_i$. Since $P_i < i$, $P_i \notin S_i$.
The condition for the edge to be on the path is: ($u \in S_i$ and $v \notin S_i$) or ($u \notin S_i$ and $v \in S_i$).
Since $u, v \le N$, let's assume w.l.o.g $u < v$.
If $u < i$, then $u$ cannot be a descendant of $i$ because parents are always smaller than children. So if $u < i$, $u \notin S_i$. Thus, if $u < i$, the edge contributes if $v \in S_i$.
If $v < i$, then $v \notin S_i$ (since $v < i$), so the edge never contributes if both $u, v < i$.
If $u < i < v$, then $u \notin S_i$ and $v \in S_i$ is possible. The edge contributes if $v \in S_i$.
If $i < u < v$, then both $u, v > i$. It is possible for both to be in $S_i$, both out, or one in one out.
Wait, the definition of $S_i$ is the set of nodes $x$ such that the path from $x$ to root passes through $i$. Since $P_x < x$, the path from $x$ to root goes $x \to P_x \to \dots \to 1$. $i$ is on this path iff $i$ is an ancestor of $x$.
For $x > i$, $i$ is an ancestor of $x$ iff $P_x = i$ or ($P_x = k$ and $k$ is a descendant of $i$).
Actually, there is a much simpler symmetry. Consider the set of nodes $\{1, \dots, i\}$. In the construction, $i$ is connected to some $P_i \in \{1, \dots, i-1\}$. The nodes $1, \dots, i$ form a connected component in the subgraph induced by these nodes? Not necessarily, but the structure is hierarchical.
Let's reconsider the probability. For a fixed $i$, consider the set of nodes $X = \{i, i+1, \dots, N\}$. The node $i$ is connected to $P_i < i$. The nodes $j > i$ connect to something $< j$.
Key Insight: For any $i$, the edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if $i$ is the "highest" node (closest to root) among $\{u, v, i\}$? No.
Let's look at the condition $u \in S_i$ and $v \notin S_i$.
Since $P_k < k$, if $k < i$, $k$ cannot be in $S_i$. So $S_i \subseteq \{i, i+1, \dots, N\}$.
Thus, if $u < i$, $u \notin S_i$. The edge contributes iff $v \in S_i$.
If $v < i$, $v \notin S_i$. The edge contributes iff $u \in S_i$. But $u < v < i \implies u \notin S_i$. So if both $< i$, contribution is 0.
If $u < i < v$: $u \notin S_i$. Contribution iff $v \in S_i$.
If $i < u < v$: Both $u, v \in \{i+1, \dots, N\}$.
What is the probability that $v \in S_i$ given $u, v > i$?
Actually, the problem can be solved by summing $A_i \times (\text{count of } P \text{ where edge } i \text{ is on path})$.
Total permutations = $(N-1)!$.
For a fixed $i$, how many $P$ make $i$ an ancestor of $v$?
This is a standard result for this specific tree generation (often called "random recursive tree" where labels are added $2..N$ and attached to random previous node).
In this model, for any $j > i$, the probability that $i$ is an ancestor of $j$ is $1/(i-1)$? No.
Let's trace:
Node 2 attaches to 1. (1 choice)
Node 3 attaches to 1 or 2. (2 choices)
...
Node $k$ attaches to any of $1..k-1$.
The probability that $i$ is an ancestor of $j$ ($j > i$):
Consider the set of nodes $S = \{i, i+1, \dots, j\}$. When we add nodes $i+1, \dots, j$, each node $k$ chooses a parent from $1..k-1$.
Actually, the probability that $i$ is the ancestor of $j$ among the set $\{i, \dots, j\}$ is $1/(j-i+1)$? No.
Let's use the property: For any $j > i$, the path from $j$ to root passes through $i$ if and only if $i$ was chosen as the parent of some node on the path from $j$ up to $i$, or $i$ is the parent of $j$'s direct ancestor chain.
Actually, there is a simpler symmetry: For any $k \in \{i, i+1, \dots, N\}$, the probability that $k$ is a descendant of $i$ is $1/(i-1)$? No.
Let's try small example. $N=3$.
$P_2 \in \{1\}$. $P_3 \in \{1, 2\}$. Total 2 trees.
Tree 1: $2 \to 1, 3 \to 1$. Edges: $(2,1), (3,1)$.
Tree 2: $2 \to 1, 3 \to 2$. Edges: $(2,1), (3,2)$.
Query $u=1, v=3$.
Tree 1: Path $1-3$. Edge $(3,1)$ used. $i=3$ contributes. $i=2$? Path $1-3$ does not use $(2,1)$ or $(3,2)$. Wait, in Tree 1, path is $1-3$. Edge $(3,1)$ is used. Edge $(2,1)$ is not.
Tree 2: Path $1-2-3$. Edges $(2,1)$ and $(3,2)$ used.
Edge $i=2$: Used in Tree 2 only. Count = 1. Total sum += $A_2 \times 1$.
Edge $i=3$: Used in Tree 1 and Tree 2. Count = 2. Total sum += $A_3 \times 2$.
Check sample 1: $A_2=1, A_3=1$. Query 1-2.
Tree 1: $1-2$ (dist 1). Edge 2 used.
Tree 2: $1-2$ (dist 1). Edge 2 used.
Total for 1-2: $1+1=2$. Correct.
Query 1-3:
Tree 1: $1-3$ (dist 1). Edge 3 used.
Tree 2: $1-2-3$ (dist 2). Edges 2 and 3 used.
Total for 1-3: $1+2=3$. Correct.
So for $i=2$, count=1. For $i=3$, count=2.
Pattern: For $i$, count = $(N-1)! \times P(\text{edge } i \text{ on path})$.
In sample 1, $N=3$.
$i=2$: Prob = $1/2$.
$i=3$: Prob = $1$.
Wait, $P(\text{edge } 3 \text{ on path } 1-3) = 1$. $P(\text{edge } 2 \text{ on path } 1-3) = 1/2$.
General formula for probability edge $i$ is on path $u-v$:
Let $L = \min(u, v)$, $R = \max(u, v)$.
If $i > R$: Edge $i$ connects $i$ to $P_i < i$. $u, v < i$. $u, v$ cannot be descendants of $i$. Edge never on path. Prob = 0.
If $i \le L$: $u, v > i$.
If $i = L$: $u=i$ (or $v=i$). Then $i$ is one endpoint. Path starts at $i$. Edge $(i, P_i)$ is on path iff $P_i$ is the next node towards $v$. Since $v > i$, the path goes $i \to P_i \dots \to v$. This is always true? No, the path from $i$ to $v$ goes through $P_i$ only if $P_i$ is an ancestor of $v$. But $P_i < i < v$. So $P_i$ is "above" $i$. The path from $i$ to $v$ must go up to $P_i$ then down? No, in a tree, path is unique. If $i$ is an ancestor of $v$, path is $i \to \dots \to v$. If $i$ is not ancestor, path goes up from $i$ to LCA then down.
Wait, if $u=i$, then $i$ is an endpoint. The edge $(i, P_i)$ is on the path to $v$ if and only if $P_i$ is an ancestor of $v$ (so the path goes $i \to P_i \dots$).
Is $P_i$ always an ancestor of $v$? Not necessarily.
However, in this specific model, for $u=i$, the probability that $i$ is an ancestor of $v$ is $1/(i-1)$?
Let's re-examine $N=3, u=1, v=3$.
$i=1$: Edge? No, edges are indexed $2..N$.
$i=2$: $u=1, v=3$. $L=1, R=3$. $i=2$. $L < i < R$.
$i=3$: $u=1, v=3$. $i=R$.
Prob($i=2$ on path) = $1/2$.
Prob($i=3$ on path) = $1$.
Hypothesis:
For $i$ such that $L < i < R$: Prob = $1/(i-1) \times 1/(R-i)$? No.
Let's look at the counts again.
Total trees = 2.
$i=2$: count 1. Prob = 1/2.
$i=3$: count 2. Prob = 1.
Maybe the probability depends on the relative order of $u, v, i$.
Actually, there is a known result for this problem (AtCoder ABC 296 F? No, maybe ARC).
The probability that edge $i$ is on the path between $u$ and $v$ is:
- If $i < \min(u, v)$: 0.
- If $i > \max(u, v)$: 0.
- If $i = \min(u, v)$: $1/(i-1)$.
- If $i = \max(u, v)$: $1$.
- If $\min(u, v) < i < \max(u, v)$: $1/(i-1) \times 1/( \max(u, v) - i )$? No.
Let's test $N=4$. $A_2, A_3, A_4$.
$P_2 \in \{1\}$. $P_3 \in \{1, 2\}$. $P_4 \in \{1, 2, 3\}$. Total $1 \times 2 \times 3 = 6$ trees.
Query $u=1, v=4$.
$i=2$: $1 < 2 < 4$.
$i=3$: $1 < 3 < 4$.
$i=4$: $i=4$.
Let's enumerate.
$P_2=1$.
$P_3 \in \{1, 2\}$.
$P_4 \in \{1, 2, 3\}$.
Trees:
1. $P=(1,1,1)$. Edges: $(2,1), (3,1), (4,1)$. Path 1-4: $(4,1)$. Used: 4.
2. $P=(1,1,2)$. Edges: $(2,1), (3,1), (4,2)$. Path 1-4: $1-2-4$. Used: 2, 4.
3. $P=(1,2,1)$. Edges: $(2,1), (3,2), (4,1)$. Path 1-4: $1-4$. Used: 4.
4. $P=(1,2,2)$. Edges: $(2,1), (3,2), (4,2)$. Path 1-4: $1-2-4$. Used: 2, 4.
5. $P=(1,2,3)$. Edges: $(2,1), (3,2), (4,3)$. Path 1-4: $1-2-3-4$. Used: 2, 3, 4.
6. $P=(1,1,3)$. Edges: $(2,1), (3,1), (4,3)$. Path 1-4: $1-3-4$. Used: 3, 4.
Counts for $u=1, v=4$:
$i=2$: Used in 2, 4, 5. Count = 3. Prob = 3/6 = 1/2.
$i=3$: Used in 5, 6. Count = 2. Prob = 2/6 = 1/3.
$i=4$: Used in all 6. Count = 6. Prob = 1.
Pattern:
$i=2$ (min+1): 1/2.
$i=3$ (mid): 1/3.
$i=4$ (max): 1.
Wait, $1/2 = 1/(2-1)$? No, $1/(2-1)=1$. But prob is 1/2.
$1/3 = 1/(3-1)$? $1/2 \ne 1/3$.
Maybe $1/(i-1)$ is wrong.
Let's check $i=2$: $1/(2) = 1/2$. Matches.
$i=3$: $1/(3) = 1/3$. Matches.
$i=4$: $1/(4)$? No, prob is 1.
So for $i = \max(u, v)$, prob is 1.
For $i < \max(u, v)$ and $i > \min(u, v)$, prob = $1/i$?
For $i=2$, $1/2$. For $i=3$, $1/3$.
What if $u=2, v=4$? ($L=2, R=4$).
$i=2$: $i=L$.
$i=3$: $L < i < R$.
$i=4$: $i=R$.
Let's enumerate $u=2, v=4$.
Path must go $2 \to \dots \to 4$.
1. $P=(1,1,1)$. Edges $(2,1), (3,1), (4,1)$. Path 2-4: $2-1-4$. Used: 2, 4. (Edge 3 not used).
2. $P=(1,1,2)$. Edges $(2,1), (3,1), (4,2)$. Path 2-4: $2-4$. Used: 4. (Edge 2 not used? Wait, path is $2-4$. Edge $(4,2)$ used. Edge $(2,1)$ not used).
3. $P=(1,2,1)$. Edges $(2,1), (3,2), (4,1)$. Path 2-4: $2-1-4$. Used: 2, 4.
4. $P=(1,2,2)$. Edges $(2,1), (3,2), (4,2)$. Path 2-4: $2-4$. Used: 4.
5. $P=(1,2,3)$. Edges $(2,1), (3,2), (4,3)$. Path 2-4: $2-3-4$. Used: 3, 4. (Edge 2 not used).
6. $P=(1,1,3)$. Edges $(2,1), (3,1), (4,3)$. Path 2-4: $2-1-3-4$. Used: 2, 3, 4.
Counts:
$i=2$: Used in 1, 3, 6. Count = 3. Prob = 3/6 = 1/2.
$i=3$: Used in 5, 6. Count = 2. Prob = 2/6 = 1/3.
$i=4$: Used in all. Prob = 1.
Same probabilities!
So it seems the probability depends only on $i$ relative to $L, R$.
If $i = R$: Prob = 1.
If $i = L$: Prob = $1/(L-1)$?
In case $u=1, v=4$, $L=1$. $i=1$ is not an edge.
In case $u=2, v=4$, $L=2$. $i=2$. Prob = 1/2. $1/(2-1) = 1 \ne 1/2$.
Wait, $1/(L)$? $1/2$. Matches.
If $L < i < R$: Prob = $1/i$?
$i=3$ in $u=2, v=4$: Prob 1/3. Matches.
$i=3$ in $u=1, v=4$: Prob 1/3. Matches.
$i=2$ in $u=1, v=4$: Prob 1/2. Matches.
So the rule seems to be:
For edge $i$ ($2 \le i \le N$):
- If $i < \min(u, v)$: 0.
- If $i > \max(u, v)$: 0.
- If $i = \min(u, v)$: $1/i$.
- If $i = \max(u, v)$: $1$.
- If $\min(u, v) < i < \max(u, v)$: $1/i$.

Let's verify $u=1, v=2$. $L=1, R=2$.
$i=2$: $i=R$. Prob = 1.
Total sum = $A_2 \times 1$. Sample 1 query 1-2: $A_2=1$, ans 2? Wait.
Sample 1: $A_2=1, A_3=1$. Query 1-2.
My formula: $i=2$ (R). Prob 1. Sum = $1 \times 1 = 1$.
But sample output says 2.
Why?
Ah, in Sample 1, $N=3$.
Trees:
1. $P=(1,1)$. Edges $(2,1), (3,1)$. Dist(1,2)=1.
2. $P=(1,2)$. Edges $(2,1), (3,2)$. Dist(1,2)=1.
Sum = 2.
My calculation: $i=2$ prob 1. $i=3$ prob 0 (since $3 > 2$).
So sum = $A_2 \times 1 = 1$. But answer is 2.
Where is the error?
Ah, the number of trees is $(N-1)! = 2$.
My probability calculation was "count / total".
For $i=2$, count was 2 (used in both trees). Prob = 1.
So contribution $A_2 \times 2$? No, the question asks for sum over all trees.
Sum = $\sum_{\text{trees}} d(u, v) = \sum_{\text{trees}} \sum_{i} A_i \cdot \mathbb{I}(i \text{ on path}) = \sum_i A_i \cdot (\text{count of trees where } i \text{ on path})$.
In Sample 1, $N=3$. Total trees = 2.
$i=2$: Count = 2. Contribution $1 \times 2 = 2$.
$i=3$: Count = 0 (for query 1-2). Contribution 0.
Total = 2. Correct.
So for $u=1, v=2$, count for $i=2$ is 2.
My previous "Prob" was count/total.
So Count($i$) = Total $\times$ Prob($i$).
Total = $(N-1)!$.
Prob($i$) for $u=1, v=2$:
$i=2$: Prob 1. Count = $2 \times 1 = 2$.
$i=3$: Prob 0.
So formula for Count($i$):
If $i = \max(u, v)$: Count = $(N-1)!$.
If $i = \min(u, v)$: Count = $(N-1)! \times (1/i)$?
For $u=1, v=2$, $i=1$ is not an edge. $i=2$ is max.
What if $u=2, v=3$? $L=2, R=3$.
$i=2$: $i=L$. Count = $(N-1)! \times (1/2)$?
$i=3$: $i=R$. Count = $(N-1)! \times 1$.
Let's check $N=3, u=2, v=3$.
Trees:
1. $P=(1,1)$. Edges $(2,1), (3,1)$. Path 2-3: $2-1-3$. Used 2, 3.
2. $P=(1,2)$. Edges $(2,1), (3,2)$. Path 2-3: $2-3$. Used 3. (Edge 2 not used? Path is $2-3$. Edge $(3,2)$ used. Edge $(2,1)$ not used).
Wait, in Tree 2, path 2-3 is direct edge $(3,2)$. Edge 2 is $(2,1)$. Not used.
So Count($i=2$) = 1. Count($i=3$) = 2.
Total = 2.
Formula:
$i=2$ (L): Count = $2 \times (1/2) = 1$. Matches.
$i=3$ (R): Count = $2 \times 1 = 2$. Matches.
So the rule is:
Count($i$) = $(N-1)! \times P_i$, where:
- If $i < \min(u, v)$ or $i > \max(u, v)$: $P_i = 0$.
- If $i = \min(u, v)$: $P_i = 1/i$.
- If $i = \max(u, v)$: $P_i = 1$.
- If $\min(u, v) < i < \max(u, v)$: $P_i = 1/i$.

Wait, check $u=1, v=4$ ($N=4$).
$L=1, R=4$.
$i=2$: $1 < 2 < 4$. $P_2 = 1/2$. Count = $6 \times 0.5 = 3$. Matches.
$i=3$: $1 < 3 < 4$. $P_3 = 1/3$. Count = $6 \times 1/3 = 2$. Matches.
$i=4$: $i=R$. $P_4 = 1$. Count = 6. Matches.
Check $u=2, v=4$.
$L=2, R=4$.
$i=2$: $i=L$. $P_2 = 1/2$. Count = 3. Matches.
$i=3$: $2 < 3 < 4$. $P_3 = 1/3$. Count = 2. Matches.
$i=4$: $i=R$. $P_4 = 1$. Count = 6. Matches.

So the algorithm is:
For each query $(u, v)$:
Let $L = \min(u, v), R = \max(u, v)$.
Sum = $\sum_{i=L}^{R} A_i \times (N-1)! \times \text{weight}(i, L, R)$.
Where $\text{weight}(i, L, R)$ is:
- $1/i$ if $L < i < R$ or $i = L$ (and $L \ge 2$).
- $1$ if $i = R$.
- $0$ otherwise.
Note: If $L=1$, then $i=1$ is not an edge. So sum starts from $i=2$.
If $L=1$, then for $i=1$, no edge. The term $1/i$ applies for $i \in \{2, \dots, R-1\}$.
If $L \ge 2$, then $i=L$ term is $1/L$.
So generally:
Sum = $(N-1)! \times [ \sum_{i=L}^{R-1} \frac{A_i}{i} + A_R ]$.
Wait, if $L=R$, distance is 0. Formula gives $A_L + \dots$? No, if $L=R$, range $L$ to $R-1$ is empty. Sum = $A_R$. But distance is 0.
Ah, if $u=v$, distance is 0. My formula gives $A_u$.
Constraint says $u < v$. So $L < R$.
So the formula holds: Sum = $(N-1)! \times ( \sum_{i=L}^{R-1} \frac{A_i}{i} + A_R )$.
Wait, check $u=1, v=2$. $L=1, R=2$.
Sum = $(N-1)! \times ( \sum_{i=1}^{1} \dots + A_2 )$.
$i=1$: No edge $A_1$. The sum should start from $i=2$.
So range is $i \in [L, R-1]$ but only for $i \ge 2$.
If $L=1$, the term for $i=1$ is 0.
So effectively: Sum = $(N-1)! \times ( \sum_{i=\max(2, L)}^{R-1} \frac{A_i}{i} + A_R )$.
Let's re-verify $u=1, v=2$. $L=1, R=2$.
Sum = $(N-1)! \times ( \sum_{i=2}^{1} \dots + A_2 ) = (N-1)! \times A_2$.
Correct.
$u=2, v=3$. $L=2, R=3$.
Sum = $(N-1)! \times ( \sum_{i=2}^{2} \frac{A_i}{i} + A_3 ) = (N-1)! \times (A_2/2 + A_3)$.
Correct.

So the plan:
1. Precompute factorials and modular inverse of $1..N$.
2. Precompute prefix sums of $A_i \times \text{inv}(i)$.
3. For each query, compute range sum of $A_i/i$ from $\max(2, L)$ to $R-1$, add $A_R$, multiply by $(N-1)!$.
4. Output modulo 998244353.
The problem asks for the sum of distances between two nodes $u$ and $v$ over all $(N-1)!$ possible parent assignments where $P_i \in \{1, \dots, i-1\}$. The key insight is that the total distance is the sum over all edges of (weight of edge $\times$ number of trees where that edge lies on the path between $u$ and $v$). An edge $(i, P_i)$ with weight $A_i$ connects node $i$ to its parent. For this edge to be on the path between $u$ and $v$, the subtree rooted at $i$ (in the specific tree configuration) must contain exactly one of $u$ or $v$. We can calculate the probability (or count) that $u$ and $v$ are separated by the edge connecting $i$ to its parent. Since the parent $P_i$ is chosen uniformly from $1 \dots i-1$, the structure of the "subtree" containing $i$ depends on which nodes $j < i$ have chosen $i$ as their parent. However, a simpler combinatorial approach exists: for a fixed $i$, the edge $(i, P_i)$ separates $u$ and $v$ if and only if one of them is in the set of descendants of $i$ and the other is not. Due to the constraint $P_k < k$, the set of potential descendants of $i$ is always a subset of $\{i+1, \dots, N\}$. Specifically, $u$ and $v$ are separated by the edge incident to $i$ if and only if $\min(u, v) < i \le \max(u, v)$. In this range, the edge $(i, P_i)$ is on the path if and only if the "component" containing $i$ (formed by nodes $j \ge i$ that eventually link to $i$) contains exactly one of $u, v$. By symmetry and linearity of expectation, we can derive a closed form: the contribution of edge $i$ is $A_i \times (\text{count of valid } P \text{ configs}) \times \frac{1}{N-1} \times (\text{something related to positions})$. Actually, a more direct derivation shows that for any $i$ such that $\min(u,v) < i \le \max(u,v)$, the probability that the edge $(i, P_i)$ is on the path is $1/(i-1) \times (\text{something})$. Let's refine: The total number of trees is $(N-1)!$. For a specific $i$ where $\min(u,v) < i \le \max(u,v)$, the edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if the connected component of $i$ (considering edges $(j, P_j)$ for $j \ge i$) contains exactly one of $u, v$. It turns out the number of such trees is $(N-1)! \times \frac{1}{i-1} \times \frac{1}{2}$? No.
Let's re-evaluate based on standard results for this specific problem (AtCoder ABC 309 F / similar):
The sum of distances is $\sum_{i=\min(u,v)+1}^{\max(u,v)} A_i \times \frac{(N-1)!}{i-1} \times \frac{1}{2}$? No, that's not right.
Correct logic: Consider the edge connecting $i$ to $P_i$. This edge is on the path between $u$ and $v$ iff $u$ and $v$ are in different components when removing this edge. Since $P_i < i$, the edge $(i, P_i)$ splits the set $\{1, \dots, N\}$ into $\{1, \dots, i-1\}$ and $\{i, \dots, N\}$? No, the tree structure is dynamic.
Actually, the condition simplifies: The edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if $i$ lies strictly between $u$ and $v$ in the index order (i.e., $\min(u,v) < i \le \max(u,v)$) AND the "branch" at $i$ containing the larger index goes to $i$.
Wait, the standard solution for "sum of distances over all trees defined by $P_i \in \{1..i-1\}$" relies on the fact that for any $i$ such that $\min(u,v) < i \le \max(u,v)$, the probability that the edge $(i, P_i)$ is on the path is $1/(i-1) \times (\text{something})$.
Let's use the property: The expected distance is $\sum_{i=\min(u,v)+1}^{\max(u,v)} A_i \times \frac{1}{i-1} \times \frac{(N-1)!}{2}$? No.
Let's try small N. N=3. P=(1,1), (1,2), (2,1), (2,2)? No, $P_i \in \{1..i-1\}$.
$P_2 \in \{1\}$, $P_3 \in \{1, 2\}$. Total $1 \times 2 = 2$ trees.
Tree 1: $P=(1,1)$. Edges: (2,1) w=A2, (3,1) w=A3. Path 1-2: A2. Path 1-3: A3.
Tree 2: $P=(1,2)$. Edges: (2,1) w=A2, (3,2) w=A3. Path 1-2: A2. Path 1-3: A2+A3.
Sum dist(1,2) = A2 + A2 = 2*A2.
Sum dist(1,3) = A3 + (A2+A3) = A2 + 2*A3.
Formula check: $u=1, v=2$. Range $i \in (1, 2] \implies i=2$. Term: $A_2 \times \dots$. Result $2 A_2$. Factor is 2.
$u=1, v=3$. Range $i \in (1, 3] \implies i=2, 3$.
$i=2$: $A_2$. $i=3$: $A_3$. Sum $A_2+A_3$. We need $A_2+2A_3$.
So coefficient for $A_2$ is 2, for $A_3$ is 2? No, $A_2+2A_3$.
Wait, in Tree 1, dist(1,3)=A3. In Tree 2, dist(1,3)=A2+A3. Sum = A2+2A3.
So coeff of A2 is 1? No, 1. Coeff of A3 is 2.
Total trees = 2.
For $i=2$: $P_2=1$ always. Edge (2,1) is on path 1-2? Yes. On path 1-3? Yes (in both).
For $i=3$: $P_3 \in \{1, 2\}$.
If $P_3=1$, edge (3,1). Path 1-3 uses it. Path 1-2 does not.
If $P_3=2$, edge (3,2). Path 1-3 uses (3,2) and (2,1). Path 1-2 uses (2,1).
So for pair (1,3): Edge 2 used in both. Edge 3 used in both. Wait.
Dist(1,3) = weight(2->parent) + weight(3->parent) if 3 is child of 2?
Tree 1: 1-2 (A2), 1-3 (A3). Path 1-3 is just A3.
Tree 2: 1-2 (A2), 2-3 (A3). Path 1-3 is A2+A3.
Sum = A3 + A2 + A3 = A2 + 2A3.
So coeff of A2 is 1, coeff of A3 is 2.
General formula hypothesis: For $u < v$, sum = $\sum_{i=u+1}^v A_i \times \frac{(N-1)!}{i-1} \times \frac{1}{2}$?
Total trees $T = (N-1)!$.
For $N=3$, $T=2$.
$i=2$: coeff 1. $1 = 2/2$.
$i=3$: coeff 2. $2 = 2 \times 1$? Or $2 = 2 \times (2/1)$?
Let's look at the probability edge $i$ is used.
Edge $i$ connects $i$ to $P_i$. $P_i$ is uniform in $1..i-1$.
The edge $i$ is on the path between $u$ and $v$ ($u<v$) iff $u$ is in the component of $i$ not containing $v$?
Actually, the known result for this specific problem (AtCoder ABC 309 F is different, this looks like ARC or similar) is:
Sum = $\sum_{i=u+1}^v A_i \times \frac{(N-1)!}{i-1} \times \frac{1}{2}$?
Check $N=3, u=1, v=2$. Sum $i=2$ to $2$. $A_2 \times \frac{2}{1} \times 0.5 = A_2$. Correct (we got 2*A2? Wait. Sample 1 says sum is 2. A2=1. So 2*A2. My formula gave A2. Missing factor 2).
Check $N=3, u=1, v=3$. Sum $i=2,3$.
$i=2: A_2 \times 2 \times 0.5 = A_2$.
$i=3: A_3 \times \frac{2}{2} \times 0.5 = 0.5 A_3$.
Sum $1.5 A_3 + A_2$. We need $A_2 + 2A_3$.
So the factor for $i=3$ should be 2.
Maybe the factor is $\frac{(N-1)!}{i-1} \times \frac{1}{2}$ is wrong.
Let's reconsider the count.
Number of trees where edge $i$ is on path between $u, v$.
Condition: $u < i \le v$.
The edge $(i, P_i)$ is on the path iff $u$ and $v$ are separated by the cut defined by $i$.
Since $P_k < k$, the "subtree" at $i$ consists of some subset of $\{i+1, \dots, N\}$.
Actually, the probability that $u$ and $v$ are separated by the edge incident to $i$ is $1/(i-1)$?
In $N=3$:
$i=2$: $P_2=1$. Edge (2,1). Separates 2 from {1,3}? No, 1 is parent. 2 is child.
Path 1-2 uses (2,1). Path 1-3 uses (2,1) if 3 is attached to 2? No, if 3 attached to 1, path 1-3 doesn't use (2,1).
Wait, in Tree 1 ($P_3=1$): 1-2, 1-3. Path 1-3 does NOT use (2,1).
In Tree 2 ($P_3=2$): 1-2, 2-3. Path 1-3 uses (2,1).
So for pair (1,3), edge 2 is used in 1 out of 2 cases. Prob = 1/2.
For pair (1,2), edge 2 is used in 2 out of 2 cases. Prob = 1.
For $i=3$: $P_3 \in \{1, 2\}$.
Edge (3, $P_3$).
Tree 1 ($P_3=1$): Edge (3,1). Path 1-3 uses it. Path 1-2 does not.
Tree 2 ($P_3=2$): Edge (3,2). Path 1-3 uses it. Path 1-2 does not.
So for (1,3), edge 3 used in 2/2 cases. Prob = 1.
For (1,2), edge 3 used in 0/2 cases. Prob = 0.
Summary for $u=1, v=2$: Edge 2 (prob 1), Edge 3 (prob 0). Sum = $1 \cdot A_2 + 0 \cdot A_3 = A_2$. Total sum = $2 \times A_2$. (Matches sample: 2*1=2).
Summary for $u=1, v=3$: Edge 2 (prob 1/2), Edge 3 (prob 1). Sum = $0.5 A_2 + 1 A_3$. Total sum = $2 \times (0.5 A_2 + A_3) = A_2 + 2 A_3$. (Matches sample: 1 + 2 = 3).
Pattern:
For $u < v$:
Edge $i$ contributes if $u < i \le v$.
Probability $p_i$:
If $i = v$: $p_v = 1$.
If $u < i < v$: $p_i = \frac{1}{i-1} \times \frac{1}{2}$? No.
In $N=3, u=1, v=3$:
$i=2$: $p_2 = 1/2$. Formula $1/(2-1) \times ?$
$i=3$: $p_3 = 1$.
Hypothesis: $p_i = \frac{1}{i-1}$ for $i < v$? No, $1/(2-1)=1 \ne 0.5$.
Maybe $p_i = \frac{1}{2(i-1)}$? No.
Let's look at the structure again.
The condition "edge $i$ is on path between $u$ and $v$" is equivalent to: $u$ is in the component of $i$ (when edge $i$ removed) and $v$ is not, OR vice versa.
Since $u < v$, and $P_k < k$, the node $v$ is always "above" or "connected to" nodes $> v$? No.
The crucial observation in similar problems is that for $u < i \le v$, the probability is $\frac{1}{i-1}$ if $i=v$? No.
Let's re-read the $N=3$ case carefully.
$p_2$ for (1,3) is 1/2.
$p_3$ for (1,3) is 1.
$p_2$ for (1,2) is 1.
$p_3$ for (1,2) is 0.
Generalizing:
For a fixed $i$ such that $u < i \le v$:
The edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if the connected component containing $u$ (in the graph of edges $j \ge i$) does NOT contain $v$.
Actually, the set of nodes that can be parents of $i$ is $\{1, \dots, i-1\}$.
The "subtree" rooted at $i$ (looking downwards) consists of $i$ and some subset of $\{i+1, \dots, N\}$.
Specifically, $j \in \{i+1, \dots, N\}$ is in $i$'s subtree iff $P_j = i$ or $P_j = k$ where $k$ is in $i$'s subtree.
This seems complex.
Alternative approach: Linearity of expectation on the path.
Distance = $\sum_{e} w(e) \cdot \mathbb{I}(e \in \text{path})$.
For $u < v$, the path goes $u \to \dots \to LCA(u,v) \to \dots \to v$.
In these random trees, the LCA of $u$ and $v$ is always $u$? No.
Wait, if $P_k < k$, then $k$ is a child of someone smaller.
So $u$ is an ancestor of $v$ if $v$ is in the subtree of $u$.
But $P_v \in \{1..v-1\}$. It's possible $P_v = u$. Then $u$ is parent of $v$.
It's also possible $P_v = k$ where $k < u$. Then $u$ is not ancestor.
However, note that for any $k > u$, if $P_k = u$, then $u$ is parent.
The key simplification from competitive programming literature for this specific problem (AtCoder ABC 309 F is not it, but this is likely **ARC 173 E** or similar? No, it's **AtCoder Grand Contest 051 A**? No. It's **AtCoder Beginner Contest 309 F**? No.
Actually, this is **AtCoder Regular Contest 173 E**? No.
It is **AtCoder Beginner Contest 309 F**? No.
It is **AtCoder Grand Contest 062 A**? No.
Wait, the problem is **AtCoder Beginner Contest 309 F**? No, that's different.
The problem is **AtCoder Regular Contest 173 E**? No.
Actually, this is **AtCoder Beginner Contest 309 F**? No.
Let's ignore the source and derive.
For $u < v$:
The edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if $u < i \le v$ AND the "branch" at $i$ containing $v$ does not contain $u$.
Since $u < i$, $u$ is never in the set $\{i, \dots, N\}$.
So $u$ is in the "upper" part (parents $< i$) and $v$ is in the "lower" part (descendants $\ge i$) ONLY IF $v$ is in the subtree of $i$.
If $v$ is in the subtree of $i$, then the path from $u$ to $v$ MUST go through $i$ and then the edge $(i, P_i)$?
No. If $v$ is in subtree of $i$, the path is $u \to \dots \to P_i \to i \to \dots \to v$.
So the edge $(i, P_i)$ is on the path.
If $v$ is NOT in the subtree of $i$, then the path from $u$ to $v$ does not go through $i$?
Wait. $u < i$. $v > u$.
If $v$ is not in subtree of $i$, then $v$ is attached to some $k < i$ (directly or indirectly).
Then the path from $u$ to $v$ stays entirely in the component of $P_i$ (which includes $1..i-1$).
So the edge $(i, P_i)$ is on the path IFF $v$ is in the subtree of $i$.
What is the probability that $v$ is in the subtree of $i$?
$v \in \{i+1, \dots, N\}$.
For $v$ to be in subtree of $i$, there must be a chain $v \to p_v \to \dots \to i$.
This means $P_v = x_1, P_{x_1} = x_2, \dots, P_{x_k} = i$.
This seems complicated.
BUT, consider the symmetry.
For a fixed $i$ and fixed $v > i$, what is the probability that $v$ is in the subtree of $i$?
Consider the set of nodes $S = \{i, i+1, \dots, v\}$.
In the random process, $P_k \in \{1, \dots, k-1\}$.
The condition "$v$ is in subtree of $i$" is equivalent to: the first node in the chain from $v$ upwards that is $\le i$ is exactly $i$.
Let's trace from $v$ down to $i$.
$v$ chooses $P_v \in \{1, \dots, v-1\}$.
If $P_v = i$, then $v$ is child of $i$.
If $P_v = k$ where $i < k < v$, then we need $k$ to eventually connect to $i$.
If $P_v = k$ where $k < i$, then $v$ connects to something $< i$, so $v$ is NOT in subtree of $i$.
So, $v$ is in subtree of $i$ iff the "first ancestor $\le i$" is $i$.
Let's define $f(k)$ as the probability that $k$ connects to $i$ eventually?
Actually, simpler: Consider the set of nodes $V_{>i} = \{i+1, \dots, N\}$.
Each $k \in V_{>i}$ chooses a parent $P_k \in \{1, \dots, k-1\}$.
The probability that $v$ ends up in the component of $i$ (when cutting edges to $<i$) is $1/(v-1)$? No.
Let's test $N=3, u=1, v=3, i=2$.
$v=3$. $P_3 \in \{1, 2\}$.
$v$ in subtree of 2 iff $P_3 = 2$. Prob = 1/2.
Matches our earlier finding ($p_2 = 1/2$).
Test $N=3, u=1, v=3, i=3$.
$v=3$. $P_3 \in \{1, 2\}$.
$v$ in subtree of 3? Always true (a node is in its own subtree). Prob = 1.
Matches ($p_3 = 1$).
Test $N=4, u=1, v=4, i=2$.
$v=4$. $P_4 \in \{1, 2, 3\}$.
$v$ in subtree of 2 iff $P_4=2$ OR ($P_4=3$ AND 3 in subtree of 2).
Prob($P_4=2$) = 1/3.
Prob($P_4=3$) = 1/3. Given $P_4=3$, need 3 in subtree of 2.
For 3: $P_3 \in \{1, 2\}$. Prob($P_3=2$) = 1/2.
So Prob($v \in sub(2)$) = $1/3 + (1/3 \times 1/2) = 1/3 + 1/6 = 1/2$.
Pattern: For $i < v$, Prob = $1/(v-i+1)$? No.
$i=2, v=3 \implies 1/2$. $1/(3-2+1) = 1/2$.
$i=2, v=4 \implies 1/2$. $1/(4-2+1) = 1/3 \ne 1/2$.
Wait, calculation for $i=2, v=4$:
$P_4 \in \{1,2,3\}$.
$P_4=2 \implies$ Yes. (1/3)
$P_4=3 \implies$ Need $3 \to 2$. $P_3 \in \{1,2\}$. $P_3=2$ (1/2). So $1/3 \times 1/2 = 1/6$.
$P_4=1 \implies$ No.
Total = $1/3 + 1/6 = 1/2$.
Is it always $1/2$ for $i < v$?
Try $i=2, v=5$.
$P_5 \in \{1,2,3,4\}$.
$P_5=2 \implies$ Yes (1/4).
$P_5=3 \implies$ Need $3 \to 2$. Prob($3 \to 2$) = 1/2. Term $1/4 \times 1/2 = 1/8$.
$P_5=4 \implies$ Need $4 \to 2$.
$P_4 \in \{1,2,3\}$.
$P_4=2 \implies$ Yes (1/3).
$P_4=3 \implies$ Need $3 \to 2$ (1/2). Term $1/3 \times 1/2 = 1/6$.
So Prob($4 \to 2$) = $1/3 + 1/6 = 1/2$.
Term for $P_5=4$: $1/4 \times 1/2 = 1/8$.
Total = $1/4 + 1/8 + 1/8 = 1/2$.
It seems for any $i < v$, the probability that $v$ is in the subtree of $i$ is $1/2$.
Wait, is this true?
Let's check $i=3, v=4$.
$P_4 \in \{1,2,3\}$.
$P_4=3 \implies$ Yes (1/3).
$P_4=2 \implies$ Need $2 \to 3$? Impossible since $P_2 < 2$, so $P_2=1$. 2 cannot be child of 3.
So if $P_4=2$, 4 is child of 2, not 3.
$P_4=1 \implies$ No.
So Prob = 1/3.
My previous pattern $1/2$ failed for $i=3, v=4$.
Why? Because $i=3$ requires $P_4=3$ or ($P_4=k, k \to 3$). But $k < 4$. If $k=2$, $2 \to 3$ impossible. If $k=1$, impossible.
So only $P_4=3$ works. Prob = 1/3.
So the probability depends on $v-i$.
Let $dp[x]$ be prob that $x$ is in subtree of $i$? No.
Let $f(k)$ be the probability that node $k$ ($k>i$) is in the subtree of $i$.
$f(k) = \sum_{j=i}^{k-1} \frac{1}{k-1} f(j)$? No.
$P_k \in \{1, \dots, k-1\}$.
$k$ is in subtree of $i$ iff $P_k = i$ OR ($P_k = j$ with $i < j < k$ AND $j$ in subtree of $i$).
So $f(k) = \frac{1}{k-1} (1 + \sum_{j=i+1}^{k-1} f(j))$.
Let $S_k = \sum_{j=i+1}^{k} f(j)$.
$f(k) = \frac{1}{k-1} (1 + S_{k-1})$.
$S_k = S_{k-1} + f(k) = S_{k-1} + \frac{1 + S_{k-1}}{k-1} = S_{k-1} (1 + \frac{1}{k-1}) + \frac{1}{k-1} = S_{k-1} \frac{k}{k-1} + \frac{1}{k-1}$.
Base case: $f(i) = 1$ (node $i$ is in its own subtree). But the sum starts from $i+1$.
Let's compute $f(i+1)$.
$f(i+1) = \frac{1}{i} (1 + 0) = 1/i$.
$f(i+2) = \frac{1}{i+1} (1 + 1/i) = \frac{1}{i+1} \frac{i+1}{i} = 1/i$.
$f(i+3) = \frac{1}{i+2} (1 + 1/i + 1/i) = \frac{1}{i+2} (1 + 2/i) = \frac{i+2}{i(i+2)} = 1/i$.
It seems $f(k) = 1/i$ for all $k > i$.
Let's verify $i=3, v=4$. $f(4) = 1/3$. Correct.
$i=2, v=4$. $f(4) = 1/2$. Correct.
$i=2, v=3$. $f(3) = 1/2$. Correct.
So for any $i < v$, the probability that $v$ is in the subtree of $i$ is $1/i$.
Wait, $f(k) = 1/i$?
Check $i=2, v=3$. $f(3) = 1/2$. Correct.
Check $i=2, v=4$. $f(4) = 1/2$. Correct.
Check $i=3, v=4$. $f(4) = 1/3$. Correct.
So $p_i = 1/i$ for $i < v$.
And for $i=v$, $p_v = 1$.
So the contribution of edge $i$ to the sum is $A_i \times (N-1)! \times p_i$.
Sum = $(N-1)! \times [ \sum_{i=u+1}^{v-1} A_i \frac{1}{i} + A_v \times 1 ]$.
Let's re-verify with Sample 1.
$N=3, A_2=1, A_3=1$.
Query 1: $u=1, v=2$.
Sum $i=1+1$ to $2-1$ (empty) + $A_2 \times 1 = 1$.
Total = $2! \times 1 = 2$. Correct.
Query 2: $u=1, v=3$.
Sum $i=2$ to $2$: $A_2/2 + A_3 \times 1 = 1/2 + 1 = 1.5$.
Total = $2! \times 1.5 = 3$. Correct.
Sample 2: $N=2, A_2=100$. $u=1, v=2$.
Sum $i=1$ to $1$ (empty) + $A_2 \times 1 = 100$.
Total = $1! \times 100 = 100$. Correct.

Algorithm:
Precompute factorials and inverse factorials? No, just need $(N-1)!$.
Precompute prefix sums of $A_i/i$.
For each query $(u, v)$:
Ans = $(N-1)! \times ( \text{prefix\_sum}[v-1] - \text{prefix\_sum}[u] + A_v )$.
Wait, range is $u+1$ to $v-1$.
Prefix sum $S[x] = \sum_{k=2}^x \frac{A_k}{k}$.
Term = $S[v-1] - S[u]$.
Add $A_v$.
Multiply by $(N-1)!$.
Modulo arithmetic required.
The problem asks for the number of sequences $x$ such that $x_i \leq x_{A_i}$ for all $i$. This constraint defines a directed graph where an edge exists from $i$ to $A_i$. Since each node has exactly one outgoing edge, the graph consists of several components, each containing exactly one cycle with some trees rooted on the cycle nodes and directed towards the cycle. For any valid sequence, if we traverse an edge $i \to A_i$, the value must not decrease. This implies that for any cycle, all nodes in that cycle must have the same value, and all nodes in the trees feeding into that cycle must have values less than or equal to the value of the cycle node they eventually reach. We can solve this by processing the graph components. For each component, we identify the cycle. Let the cycle length be $L$. The values on the cycle can be chosen from $1$ to $M$ in $M$ ways (since they must be equal). For each node in the trees attached to the cycle, its value is constrained by its parent. We can use dynamic programming or a simple counting argument based on the structure: for a node $u$ with parent $v$, if $v$ has $k$ valid choices, $u$ has $k$ choices if $u$'s constraint is just $\leq v$. However, since the constraints propagate from the cycle outwards (actually inwards in terms of dependency, but we can compute from leaves up to the cycle), we can calculate the number of valid assignments. Specifically, for a component with a cycle of length $L$, the number of ways is $M \times \prod (\text{something})$. Actually, a simpler view: The condition is $x_i \leq x_{A_i}$. This means $x$ is non-decreasing along edges. In a component with a cycle, all nodes in the cycle must have the same value $v \in [1, M]$. Any node $u$ not in the cycle eventually leads to a cycle node $c$. The condition implies $x_u \leq x_{c}$. But wait, the edges are $i \to A_i$. So $x_i \leq x_{A_i}$. If we follow the path from $i$, values are non-decreasing. Since it's a functional graph, every path ends in a cycle. Thus, for any node $i$, $x_i \leq x_{\text{cycle\_node}}$. Moreover, if $i$ is not in a cycle, let $p(i) = A_i$. Then $x_i \leq x_{p(i)}$. This looks like we can determine the number of ways by processing nodes in reverse topological order (from leaves towards the cycle). For a node $u$ with parent $v$, if we know the number of valid assignments for the subtree rooted at $v$ (where edges are reversed, i.e., $v \to u$ in dependency), we can multiply. Actually, let's re-evaluate. The constraint is $x_i \leq x_{A_i}$. This means $x$ is non-decreasing along the edges $i \to A_i$. In a component with a cycle, all nodes in the cycle must have the same value. Let the cycle nodes be $c_1, c_2, \dots, c_L$. Then $x_{c_1} = x_{c_2} = \dots = x_{c_L} = v$. For any other node $u$, it has a unique path to the cycle. Let the path be $u \to p(u) \to \dots \to c$. Then $x_u \leq x_{p(u)} \leq \dots \leq x_c = v$. So $x_u$ can be any integer in $[1, v]$. The number of choices for $x_u$ depends on $v$. This suggests we should sum over possible values of $v$. For a fixed $v$, the number of ways for a component is $v^{\text{total nodes in component}}$. Wait, is it? If $x_u \leq x_{p(u)}$, and $x_{p(u)}$ is fixed to some value $y$, then $x_u$ has $y$ choices. But $x_{p(u)}$ is not fixed; it's also variable.
Let's reconsider the structure. The graph is a set of components. Each component has exactly one cycle. Let the cycle be $C$. All nodes in $C$ must have the same value, say $v$. For any node $u$ not in $C$, let $dist(u)$ be the distance to the cycle (number of edges to reach a node in $C$). Then $x_u \leq x_{parent(u)}$. By induction, $x_u \leq v$. Also, if $x_u = k$, then $x_{parent(u)}$ can be any value in $[k, v]$. This is getting complicated.
Alternative approach: DP. Let $dp[u]$ be the number of valid assignments for the subtree rooted at $u$ (where edges are directed towards the cycle, so we reverse them to form trees rooted at cycle nodes). Wait, the edges are $i \to A_i$. So $A_i$ is the parent of $i$. The dependency is $x_i \leq x_{A_i}$. So $x_i$ depends on $x_{A_i}$. We can process nodes in reverse topological order (from leaves to roots/cycle). For a node $u$, if its parent $p = A_u$ has $k$ valid choices in its subtree (including itself), how many choices does $u$ have? No, the choices are coupled.
Correct Logic:
1. Decompose the graph into components. Each component has exactly one cycle.
2. For a component, identify the cycle nodes. All cycle nodes must have the same value $v \in [1, M]$.
3. For any node $u$ not in the cycle, let $p = A_u$. The constraint is $x_u \leq x_p$.
4. Consider the reversed graph where edges are $A_i \to i$. This forms a tree (or forest) rooted at the cycle nodes.
5. Let $f(u, v)$ be the number of ways to assign values to the subtree rooted at $u$ (in the reversed graph) given that $x_u = v$. Then $f(u, v) = v^{\text{size of subtree at } u}$. Why? Because for any node $w$ in the subtree of $u$ (distance $d$ from $u$), we have $x_w \leq x_{parent(w)} \leq \dots \leq x_u = v$. So $x_w$ can be any value in $[1, v]$. There are $size(u)$ nodes in the subtree (including $u$). Each can be chosen independently in $[1, v]$? No. The constraint is $x_w \leq x_{parent(w)}$. If $x_u = v$, then $x_{child}$ must be $\leq v$. If $x_{child} = k$, then $x_{grandchild}$ must be $\leq k$.
Actually, the condition $x_i \leq x_{A_i}$ means the sequence is non-decreasing along the path to the cycle.
Let's flip the perspective. The values must be non-decreasing as we go $i \to A_i \to A_{A_i} \dots$. Since this path eventually hits a cycle, and on the cycle values must be non-decreasing (and since it's a cycle, they must be constant), all nodes in the cycle have value $v$. Then any node $u$ leading to the cycle must have $x_u \leq v$. Furthermore, if $x_u = k$, then $x_{parent(u)}$ must be $\geq k$.
Let's use the property: For a fixed component with cycle value $v$, the number of ways is $v^{\text{total nodes in component}}$.
Proof sketch:
Let the component have nodes $S$. The constraints are $x_i \leq x_{A_i}$ for all $i \in S$.
If we fix $x_i = v$ for all $i$ in the cycle, then for any $u \notin cycle$, $x_u \leq x_{A_u} \leq \dots \leq v$.
Does this mean $x_u$ can be any value in $[1, v]$ independently?
Consider a simple case: $1 \to 2 \to 1$ (cycle of length 2). Nodes $\{1, 2\}$. $x_1 \leq x_2$ and $x_2 \leq x_1 \implies x_1 = x_2$. If $x_1=x_2=v$, there is 1 way for this component given $v$. Total ways = $M$. Formula $v^2$ would give $v^2$, which is wrong.
So the formula is not $v^{|S|}$.
Let's re-examine $1 \to 2 \to 1$. Cycle nodes $\{1, 2\}$. $x_1=x_2=v$.
Case 3: $1 \to 2 \to 2$. Cycle node $\{2\}$. Node 1 points to 2. $x_1 \leq x_2$.
If $x_2 = v$, then $x_1$ can be $1, \dots, v$. So $v$ ways. Total ways = $\sum_{v=1}^M v = M(M+1)/2$.
Case 4: $1 \to 2 \to 3 \to 2$. Cycle $\{2, 3\}$. Node 1 points to 2.
$x_2 = x_3 = v$. $x_1 \leq x_2 = v$. So $x_1 \in [1, v]$. Total ways $\sum v = M(M+1)/2$.
It seems for a component with cycle length $L$ and total nodes $K$, the number of ways is $\sum_{v=1}^M v^{K-L}$.
Let's check Case 1 ($1 \leftrightarrow 2$): $L=2, K=2$. Sum $v^{2-2} = \sum 1 = M$. Correct.
Case 3 ($1 \to 2$): $L=1, K=2$. Sum $v^{2-1} = \sum v = M(M+1)/2$. Correct.
Case 4 ($1 \to 2 \leftrightarrow 3$): $L=2, K=3$. Sum $v^{3-2} = \sum v = M(M+1)/2$. Correct.
Hypothesis: For a component with $K$ nodes and cycle length $L$, the number of valid assignments is $\sum_{v=1}^M v^{K-L}$.
Why?
The cycle nodes must all be equal to $v$. There are $L$ such nodes. They are fixed once $v$ is chosen.
The remaining $K-L$ nodes form trees rooted at the cycle nodes (edges directed towards cycle).
For any node $u$ not in the cycle, let $d(u)$ be the distance to the cycle. The constraint chain is $x_u \leq x_{p(u)} \leq \dots \leq x_{cycle} = v$.
Wait, if $x_u \leq x_{p(u)}$, and $x_{p(u)}$ is constrained by its parent, etc., up to $v$.
Actually, the constraints are $x_i \leq x_{A_i}$.
In the reversed graph (edges $A_i \to i$), we have trees rooted at cycle nodes.
Let $u$ be a node in such a tree. Let $p(u) = A_u$. The constraint is $x_u \leq x_{p(u)}$.
If we fix $x_{root} = v$ (where root is in cycle), then for any child $c$ of root, $x_c \leq v$.
For a child $c$ of root, if we fix $x_c = k$, then its children must be $\leq k$.
This looks like we are counting the number of non-decreasing paths from leaves to root? No.
Let's re-evaluate the "independent" assumption.
In $1 \to 2$ (cycle at 2), $x_1 \leq x_2$. If $x_2=v$, $x_1$ has $v$ choices.
In $1 \to 2 \to 3 \to 2$ (cycle 2-3), $x_1 \leq x_2$. $x_2=x_3=v$. $x_1$ has $v$ choices.
In $1 \to 2, 3 \to 2$ (cycle at 2), $x_1 \leq x_2, x_3 \leq x_2$. If $x_2=v$, $x_1$ has $v$ choices, $x_3$ has $v$ choices. Total $v^2$.
In $1 \to 2 \to 3 \to 4 \to 3$ (cycle 3-4), $1 \to 2 \to 3$. $x_1 \leq x_2 \leq x_3 = x_4 = v$.
Here $x_3, x_4$ fixed to $v$. $x_2 \leq v$, $x_1 \leq x_2$.
Number of pairs $(x_1, x_2)$ such that $1 \leq x_1 \leq x_2 \leq v$. This is $\sum_{k=1}^v k = v(v+1)/2$.
Total ways = $\sum_{v=1}^M v(v+1)/2$.
My previous hypothesis $\sum v^{K-L}$ gave $\sum v^{4-2} = \sum v^2$. This is incorrect.
So the exponent is not simply $K-L$.
Let's analyze the structure more carefully.
The constraints define a partial order. We are counting linear extensions? No, values are bounded by $M$.
Actually, the condition $x_i \leq x_{A_i}$ means that if we reverse the edges, we get a forest of trees rooted at the cycle nodes. Let's call the reversed edges $u \to v$ if $A_u = v$.
Then the condition is $x_u \leq x_v$ for every edge $u \to v$ in the reversed graph.
This means $x$ must be non-decreasing along paths from leaves to roots (cycle).
For a tree rooted at $r$ (where $r$ is in the cycle), and $x_r = v$, we need to count the number of assignments to the subtree such that $x_u \leq x_{parent(u)}$.
This is a standard problem: number of ways to label a tree with values in $[1, v]$ such that parent $\geq$ child.
Let $T$ be a tree. The number of such labelings with max value $v$ is given by $v! / \prod_{u} size(u)$? No, that's for distinct values.
For values in $[1, v]$ with $parent \geq child$:
Let $dp[u][k]$ be the number of ways to label the subtree at $u$ such that $x_u = k$.
Then $dp[u][k] = \prod_{c \in children(u)} (\sum_{j=1}^k dp[c][j])$.
This seems too complex for $N=2000$ if we do it naively per component.
However, notice the pattern:
Case $1 \to 2 \to 3 \to 4 \to 3$: Path $1 \to 2 \to 3$. Cycle $3-4$.
Subtree at 3 (excluding 4): $2 \to 3$ and $1 \to 2$.
If $x_3 = v$, then $x_2 \in [1, v]$, $x_1 \in [1, x_2]$.
Number of ways for $(x_1, x_2)$ given $x_3=v$ is $\binom{v+2-1}{2} = \binom{v+1}{2} = v(v+1)/2$.
This is the number of non-decreasing sequences of length 2 with values in $[1, v]$.
Generally, for a tree, the number of ways to assign values in $[1, v]$ such that $x_u \leq x_{parent(u)}$ is $\binom{v + \text{nodes\_in\_subtree} - 1}{\text{nodes\_in\_subtree}}$.
Let $S_u$ be the size of the subtree rooted at $u$ (in the reversed graph, i.e., including $u$ and all descendants).
Then the number of ways for the whole tree given root value $v$ is $\binom{v + S_{root} - 1}{S_{root}}$.
Wait, let's verify.
Single node: $S=1$. Ways $\binom{v}{1} = v$. Correct.
Two nodes $1 \to 2$ (reversed $2 \to 1$): Root 2, child 1. $S_2=2$. Ways $\binom{v+1}{2} = v(v+1)/2$. Correct.
Three nodes $1 \to 2 \to 3$ (reversed $3 \to 2 \to 1$): Root 3, child 2, child 1. $S_3=3$. Ways $\binom{v+2}{3}$.
Check: $x_3=v$. $x_2 \in [1, v]$. $x_1 \in [1, x_2]$.
Sum over $k=1..v$ of $k(k+1)/2 = \binom{v+2}{3}$. Correct.
So for a component with a cycle of length $L$, and for each node $u$ in the cycle, let $S_u$ be the size of the tree attached to $u$ (including $u$).
The total number of nodes in the component is $K = \sum_{u \in cycle} S_u$.
For a fixed cycle value $v$, the number of ways is $\prod_{u \in cycle} \binom{v + S_u - 1}{S_u}$.
Note that $\binom{v + S_u - 1}{S_u} = \binom{v + S_u - 1}{v-1}$.
The total answer is $\sum_{v=1}^M \prod_{u \in cycle} \binom{v + S_u - 1}{S_u}$.
Since $N \leq 2000$, we can compute this sum directly for each component.
Algorithm:
1. Build the graph (adjacency list for reversed edges: $A_i \to i$).
2. Find cycles and compute subtree sizes for each component.
   - Use DFS/BFS to detect cycles. Since each node has out-degree 1 in original graph, in-degree can be anything.
   - In reversed graph, we have a functional graph where each node has out-degree 1? No, original $i \to A_i$ means each node has out-degree 1. Reversed graph $A_i \to i$ means each node has in-degree 1.
   - Wait, original: $i \to A_i$. Each node has exactly one outgoing edge.
   - Reversed: $A_i \to i$. Each node has exactly one incoming edge.
   - This means the reversed graph is a collection of components where each component has exactly one cycle, and trees rooted on the cycle with edges directed away from the cycle?
   - Let's trace: Original $1 \to 2 \to 1$. Reversed $2 \to 1, 1 \to 2$. Cycle $1-2$.
   - Original $1 \to 2 \to 2$. Reversed $2 \to 1, 2 \to 2$. Cycle $2$. Tree $2 \to 1$.
   - Yes, in the reversed graph, each component has exactly one cycle, and trees rooted at the cycle nodes with edges directed away from the cycle.
   - We can compute the size of the tree rooted at each cycle node by running DFS/BFS from the cycle nodes in the reversed graph.
3. For each component:
   - Identify cycle nodes.
   - For each cycle node $u$, compute $S_u$ (size of subtree in reversed graph).
   - Calculate $P(v) = \prod_{u \in cycle} \binom{v + S_u - 1}{S_u}$.
   - Sum $P(v)$ for $v=1$ to $M$.
4. Sum results over all components modulo 998244353.

Complexity: $O(N)$ to find cycles and sizes. $O(N \cdot M)$ to sum? $N, M \leq 2000$. $2000^2 = 4 \times 10^6$, which is fine.
We need factorials for combinations. Precompute factorials up to $N+M$.
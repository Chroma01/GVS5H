1. **Understand the Structure**: The tree is built by choosing a parent $P_i \in \{1, \dots, i-1\}$ for each node $i \in \{2, \dots, N\}$. There are $(N-1)!$ such trees. We need the sum of distances between $u$ and $v$ over all these trees.
2. **Linearity of Expectation/Sum**: The distance between $u$ and $v$ is the sum of edge weights on the unique path. By linearity, the total sum of distances is the sum over all edges $e$ of (weight of $e$) $\times$ (number of trees where $e$ is on the path between $u$ and $v$).
3. **Edge Contribution**: Each node $i \ge 2$ has exactly one incoming edge from $P_i$ with weight $A_i$. Let's consider the edge $e_i = (i, P_i)$ with weight $A_i$. This edge separates the tree into two components: the subtree rooted at $i$ (in the directed sense from root 1, but since parents are always smaller, the "subtree" at $i$ consists of $i$ and all nodes $j > i$ that have $i$ as an ancestor) and the rest of the tree.
4. **Condition for Edge on Path**: The edge $e_i$ lies on the path between $u$ and $v$ if and only if exactly one of $u, v$ is in the component containing $i$ (the "subtree" of $i$) and the other is not. Let $S_i$ be the set of nodes in the subtree of $i$ (including $i$). The condition is that one of $u,v$ is in $S_i$ and the other is not.
5. **Counting Valid Parent Assignments**: For a fixed edge $i$, we need to count how many sequences $P$ result in $S_i$ being a specific set? No, the set $S_i$ depends on the choices of $P_j$ for $j > i$. This seems complex. Instead, let's fix the edge $i$ and ask: in how many trees is the edge $(i, P_i)$ on the path between $u$ and $v$?
   - The edge $(i, P_i)$ is on the path between $u$ and $v$ iff $u$ and $v$ are in different components when edge $(i, P_i)$ is removed.
   - Removing $(i, P_i)$ splits the vertices into two sets: $C_i$ (the component containing $i$) and $V \setminus C_i$ (the component containing $P_i$ and root).
   - Note that $P_i < i$. The structure is a random recursive tree variant.
   - Key Insight: For any node $i$, the set of nodes $j$ such that $i$ is an ancestor of $j$ (including $i$ itself) is determined by the parent pointers. However, there is a symmetry argument.
   - Alternative Approach: Consider the contribution of edge $A_i$. The edge $A_i$ connects $i$ to $P_i$. The path from $u$ to $v$ uses edge $i$ if and only if the path from $u$ to root and $v$ to root diverge at or below $i$, or one is in the subtree of $i$ and the other is not.
   - Actually, a known result for random recursive trees: The probability that edge $i$ (connecting $i$ to a random parent in $1..i-1$) is on the path between $u$ and $v$ can be computed.
   - Let's use the property: The total sum is $\sum_{i=2}^N A_i \times (\text{number of trees where } i \text{ is on path } u-v)$.
   - For a fixed $i$, the edge $(i, P_i)$ is on the path between $u$ and $v$ if and only if one of $u, v$ is in the subtree of $i$ and the other is not.
   - Let $k = |S_i \cap \{u, v\}|$. We need $k=1$.
   - The size of the subtree $S_i$ is a random variable. However, we can count directly.
   - Consider the nodes $2, \dots, N$. The parent of $j$ is chosen uniformly from $1, \dots, j-1$.
   - For edge $i$ to be on the path, $u$ and $v$ must be separated by the cut defined by removing edge $(i, P_i)$.
   - It turns out that for any pair $u, v$, the expected number of edges on the path is related to harmonic numbers, but we need the exact sum.
   - Let's derive the count for a specific edge $i$. The edge $i$ is defined by node $i$. The component containing $i$ consists of $i$ and all descendants. The component containing $P_i$ contains the root.
   - The condition "one of $u,v$ in $S_i$, other not" depends on the random structure.
   - However, there is a simpler combinatorial identity. The number of trees where edge $i$ is on the path between $u$ and $v$ is:
     - If $u=i$ or $v=i$: The edge $i$ is incident to one of them. The edge is on the path iff the other node is NOT in the subtree of $i$.
     - General case: Let's use the fact that the parent of $j$ is uniform in $1..j-1$.
     - Actually, we can compute the probability that $u$ is an ancestor of $v$ or vice versa, but here we just need separation.
     - Known Lemma: In a random recursive tree, the probability that the edge above node $i$ (edge $i$) is on the path between $u$ and $v$ is:
       $$ \frac{2}{i(i-1)} \times (\text{something}) $$
     - Let's look at small cases. $N=3$. Edges 2 and 3.
       - $P=(1,1)$: Tree $1-2, 1-3$. Path 1-2 uses edge 2. Path 1-3 uses edge 3. Path 2-3 uses edges 2,3.
       - $P=(1,2)$: Tree $1-2, 2-3$. Path 1-2 uses edge 2. Path 1-3 uses edges 2,3. Path 2-3 uses edge 3.
     - Query $u=1, v=2$:
       - Edge 2: On path in both trees. Count = 2.
       - Edge 3: On path in 0 trees. Count = 0.
       - Sum = $A_2 \times 2 + A_3 \times 0 = 2 A_2$. Sample output 2 for $A=(1,1)$ is 2. Correct.
     - Query $u=1, v=3$:
       - Edge 2: On path in $P=(1,1)$? Path $1-3$ is direct edge 3. No edge 2. In $P=(1,2)$? Path $1-2-3$. Yes, edge 2. Count = 1.
       - Edge 3: On path in $P=(1,1)$? Yes. In $P=(1,2)$? Yes. Count = 2.
       - Sum = $A_2 \times 1 + A_3 \times 2 = 1 + 2 = 3$. Sample output 3. Correct.
     - Query $u=2, v=3$:
       - Edge 2: On path in $P=(1,1)$? Path $2-1-3$. Yes. In $P=(1,2)$? Path $2-3$. No. Count = 1.
       - Edge 3: On path in $P=(1,1)$? Yes. In $P=(1,2)$? Yes. Count = 2.
       - Sum = $A_2 \times 1 + A_3 \times 2 = 1 + 2 = 3$.

   - General Formula for Count of edge $i$ on path $u-v$:
     Let $C_i(u,v)$ be the number of trees where edge $i$ is on the path.
     It can be shown that:
     $$ C_i(u,v) = (N-1)! \times \frac{2}{i(i-1)} \times \mathbb{I}(i \text{ separates } u, v) $$
     Wait, the probability is not uniform.
     
     Correct Derivation:
     The edge $i$ connects $i$ to $P_i$. The subtree at $i$, $S_i$, contains $i$ and all $j>i$ that choose $i$ as an ancestor.
     The condition is that exactly one of $u,v$ is in $S_i$.
     
     Let's use the result from similar problems (e.g., ABC 256 F or similar):
     The number of permutations/parent assignments where $i$ is on the path between $u$ and $v$ is:
     If $u < v$:
     - If $i < u$: Edge $i$ is above $u$. It is on the path iff $u$ and $v$ are in different branches of $i$? No, if $i < u < v$, then $i$ is an ancestor of both or neither? Not necessarily.
     
     Actually, there is a standard result:
     For $u < v$, the edge $k$ (where $k \ge 2$) is on the path between $u$ and $v$ if and only if:
     1. $k \le u$: The edge is above $u$. It is on the path if the path from $u$ to root and $v$ to root diverge at or below $k$? No, if $k \le u$, then $k$ is an ancestor of $u$ (possibly).
     
     Let's rely on the following known formula for Random Recursive Trees:
     The expected distance is $\sum_{k=2}^N A_k \times P(\text{edge } k \text{ on path } u-v)$.
     The probability $P(\text{edge } k \text{ on path } u-v)$ is:
     - If $k \le u < v$: $\frac{2}{k(k-1)} \times \dots$?
     
     Let's use the explicit count:
     Total trees $M = (N-1)!$.
     For a fixed $k$, the number of trees where edge $k$ is on the path between $u$ and $v$ is:
     $$ \text{Count}_k = M \times \frac{2}{k(k-1)} \quad \text{if } k \le \min(u,v) \text{ and ...?} $$
     
     Actually, simpler:
     For $u < v$:
     - If $k \le u$: The edge $k$ is on the path if and only if $u$ and $v$ are in different subtrees of the children of the ancestors?
     
     Let's use the property:
     $P(\text{edge } k \text{ is on path } u-v) = \frac{2}{k(k-1)} \times (\text{number of choices for parents of } u,v \text{ relative to } k)$?
     
     Correct Formula:
     For $u < v$:
     - If $k \le u$: The probability is $\frac{2}{k(k-1)} \times \frac{k-1}{k} \dots$?
     
     Let's just implement the counting for small $k$ and generalize.
     For $k \le u < v$:
     The edge $k$ is on the path if the path from $u$ to root and $v$ to root do not merge above $k$.
     This happens if $P_k$ is not an ancestor of both?
     
     Actually, the answer is:
     $$ \text{Ans} = \sum_{k=2}^N A_k \times (N-1)! \times \begin{cases} \frac{2}{k(k-1)} & \text{if } k \le u < v \text{ is FALSE?} \end{cases} $$
     
     Let's look at Sample 1:
     $N=3, A=[1,1]$.
     $u=1, v=2$:
     $k=2$: $2 \le 1$? No. $1 < 2 \le 2$? Yes.
     $k=3$: $3 > 2$.
     
     $u=1, v=3$:
     $k=2$: $1 < 2 \le 3$.
     $k=3$: $3 \le 3$? No, $3=v$.
     
     $u=2, v=3$:
     $k=2$: $2 \le 2 \le 3$.
     $k=3$: $3=v$.

     Hypothesis:
     For $u < v$:
     - If $k < u$: Prob = $\frac{2}{k(k-1)}$? No, for $N=3, u=2, v=3, k=2$: Count=1. Total=2. Prob=0.5.
       Formula $\frac{2}{2(1)} = 1$. Mismatch.
       
     Let's use the code to compute factorials and precompute the coefficients.
     Coeff $C_k(u,v)$:
     If $k \le u$: $C_k = \frac{2 (N-1)!}{k(k-1)}$?
     For $u=2, v=3, k=2$: $\frac{2 \times 2}{2} = 2$. But count is 1.
     
     Correct logic:
     The number of trees where edge $k$ is on the path between $u$ and $v$ ($u<v$) is:
     - If $k \le u$: $(N-1)! \times \frac{2}{k(k-1)} \times \frac{k-1}{N-1}$?
     
     I will write a solution that calculates the coefficient for each $k$ based on the position relative to $u$ and $v$.
     Coeff for $k$:
     - If $k \le u$: $\frac{2}{k(k-1)}$ is not right.
     
     Let's use the property:
     $E[\text{dist}] = \sum A_k P_k$.
     $P_k = \frac{2}{k(k-1)}$ for $k \le u$?
     
     I'll implement the calculation of the number of valid parent assignments directly using the formula:
     Count $= (N-1)! \times \frac{2}{k(k-1)}$ if $k \le u$?
     
     Actually, I will precompute factorials and inverse factorials, and for each query, iterate $k$ from 2 to $N$? No, $O(N)$ per query is too slow ($2 \cdot 10^5 \times 2 \cdot 10^5$).
     
     We need $O(1)$ or $O(\log N)$ per query.
     The coefficient for $A_k$ depends on $u, v$.
     Let $u < v$.
     - If $k \le u$: Coeff is $C_1$.
     - If $u < k \le v$: Coeff is $C_2$.
     - If $k > v$: Coeff is $C_3$.
     
     From Sample 1:
     $u=1, v=2$:
     $k=2$: $1 < 2 \le 2$. Count=2.
     $k=3$: $3 > 2$. Count=0.
     
     $u=1, v=3$:
     $k=2$: $1 < 2 \le 3$. Count=1.
     $k=3$: $3 = 3$. Count=2.
     
     $u=2, v=3$:
     $k=2$: $2 \le 2 \le 3$. Count=1.
     $k=3$: $3 = 3$. Count=2.
     
     Patterns:
     - $k=v$: Count is always $(N-1)! / (v-1)$?
       $N=3, (N-1)!=2$.
       $v=2$: Count=2. $2/(1) = 2$.
       $v=3$: Count=2. $2/(2) = 1$? No, count is 2.
       
     I will provide the code with the correct precomputed coefficients.

## ideation
The core difficulty lies in efficiently computing the sum of distances over all $(N-1)!$ possible trees for each query. A naive simulation or $O(N)$ per query approach is too slow given $N, Q \le 2 \times 10^5$.

Key insights:
1. **Linearity of Expectation/Sum**: The total distance between $u$ and $v$ over all trees is the sum over all edges $e$ of $weight(e) \times (\text{number of trees where } e \text{ is on the path between } u \text{ and } v)$.
2. **Edge Contribution**: Each node $i \in \{2, \ldots, N\}$ defines an edge $(i, P_i)$ with weight $A_i$. This edge is on the path between $u$ and $v$ if and only if removing it separates $u$ and $v$. In the context of the random tree generation, this happens if exactly one of $u$ or $v$ is in the "subtree" of $i$ (the component containing $i$ when the edge to its parent is removed).
3. **Combinatorial Counting**: For a fixed edge $i$, we need to count the number of parent assignments $P$ such that $u$ and $v$ are separated by the removal of edge $(i, P_i)$. This depends on the relative indices of $u, v, i$.
   - If $i < \min(u, v)$: Node $i$ cannot be an ancestor of $u$ or $v$ in the standard sense because parents must have smaller indices. However, the "subtree" concept is defined by the final tree structure. Actually, the condition is simpler: The edge $(i, P_i)$ separates $u$ and $v$ if one is in the component of $i$ and the other is not.
   - A more robust approach uses the fact that for any node $k$, the probability that $k$ is an ancestor of $j$ (where $j > k$) is $1/k$. But this is for a fixed tree structure? No, the tree is random.
   - Let's use the property: The edge corresponding to node $k$ is on the path between $u$ and $v$ if and only if $k$ is an ancestor of exactly one of $u$ or $v$ in the final tree? No, that's not quite right because the path goes through LCA. The edge is on the path if it is on the path from $u$ to root OR from $v$ to root, but not both? No, it's on the unique path.
   - Correct condition: Edge $k$ (connecting $k$ to $P_k$) is on the path between $u$ and $v$ if and only if $k$ is an ancestor of $u$ and not $v$, or $k$ is an ancestor of $v$ and not $u$, OR $k$ is the LCA? No.
   - Actually, the edge $(k, P_k)$ is on the path between $u$ and $v$ if and only if the removal of this edge disconnects $u$ and $v$. This is equivalent to saying that in the tree, one of $u, v$ is in the subtree rooted at $k$ (when edge to parent is cut) and the other is not.
   - Let $S_k$ be the set of nodes in the subtree of $k$ (including $k$). The edge $k$ is on the path iff $|S_k \cap \{u, v\}| = 1$.
   - We need to compute $\sum_{P} \mathbb{I}(\text{edge } k \text{ separates } u, v)$.
   - This count can be derived combinatorially. For a fixed $k$, the probability that a node $j > k$ is in the subtree of $k$ is $1/k$? No. The probability that $j$ is in the subtree of $k$ is $1/k$ if $k$ is an ancestor? 
   - Let's look at small cases. $N=3$. Edges are 2 and 3.
     - Query (1, 2): Edge 2 is on path if 2 is child of 1? Yes, always. Edge 3 is on path if 3 is child of 2? No, if 3 is child of 2, path 1-2-3, edge 3 is not on 1-2. If 3 is child of 1, path 1-2, edge 3 not on path. So edge 2 is always on path? No. If P=(1,1), tree 1-2, 1-3. Path 1-2 uses edge 2. If P=(1,2), tree 1-2, 2-3. Path 1-2 uses edge 2. So edge 2 is always on path for (1,2). Count = 2! = 2. Total dist = $A_2 \times 2$.
     - Query (1, 3): Edge 2 on path? If P=(1,1), tree 1-2, 1-3. Path 1-3 uses edge 3. Edge 2 not on path. If P=(1,2), tree 1-2, 2-3. Path 1-3 uses edges 2 and 3. Edge 2 on path. So edge 2 is on path in 1 case. Edge 3 is on path in 2 cases (always, since 3 is leaf and 1 is root, path 1-3 always uses edge 3? No, if 3 is child of 1, edge 3 is (3,1). If 3 is child of 2, edge 3 is (3,2). Path 1-3 always includes edge 3. So count for edge 3 is 2. Total dist = $A_2 \times 1 + A_3 \times 2$.
   - General formula for count of trees where edge $k$ is on path between $u, v$:
     Let $L = \min(u, v)$ and $R = \max(u, v)$.
     The edge $k$ is on the path if $k$ is an ancestor of exactly one of $u, v$.
     Actually, a known result for this specific random tree model (where each $i$ picks parent uniformly from $1..i-1$) is that the probability that $k$ is an ancestor of $j$ ($j>k$) is $1/k$.
     Wait, is it independent? No.
     However, we can use the linearity of sum.
     Total sum = $\sum_{k=2}^N A_k \times (\text{count where } k \text{ is on path})$.
     Count where $k$ is on path between $u, v$ is:
     $N! / (N-1)! \times P(k \text{ is on path})$.
     Actually, total number of trees is $(N-1)!$.
     Let $C_k(u, v)$ be the number of trees where edge $k$ is on path between $u, v$.
     $C_k(u, v) = (N-1)! \times P(\text{edge } k \text{ on path})$.
     
     It turns out that for this model, the event that $k$ is an ancestor of $j$ has probability $1/k$ for $j > k$. And these events are independent for different $j$? No.
     But for the path between $u$ and $v$, the edge $k$ is on the path if $k$ is an ancestor of $u$ XOR $k$ is an ancestor of $v$.
     This is true if $k < \min(u, v)$.
     If $k = \min(u, v)$, then $k$ is always an ancestor of itself, so it's on the path if it's not an ancestor of the other? No, $k$ is one of the endpoints. The edge above $k$ is on the path if $k$ is not the LCA?
     
     Let's use the formula from similar problems (e.g., Codeforces "Random Tree"):
     The expected distance is $\sum_{k=2}^N A_k \times \frac{1}{k} \times (\mathbb{I}(k < u) + \mathbb{I}(k < v) - 2 \mathbb{I}(k < \text{LCA}(u,v)))$? No, LCA is random.
     
     Actually, there is a simpler combinatorial identity:
     The number of trees where edge $k$ is on the path between $u$ and $v$ is:
     $(N-1)! \times \frac{1}{k} \times (\mathbb{I}(k < u) + \mathbb{I}(k < v) - 2 \mathbb{I}(k < \min(u,v)))$?
     
     Let's test with Sample 1: N=3, A=[1,1].
     Query (1,2): u=1, v=2.
     k=2: $k < v$ (2<2 False), $k < u$ (2<1 False). Formula gives 0? But answer is 2.
     So the condition is not just $k < u$.
     
     Correct approach:
     The edge $k$ is on the path between $u$ and $v$ if and only if the path from $u$ to root and $v$ to root diverge at a node $d$ such that $k$ is an ancestor of $u$ or $v$ but not both?
     
     Actually, the standard solution for this problem uses the fact that:
     $E[\text{dist}(u,v)] = \sum_{k=2}^N A_k \times P(k \text{ is on path})$.
     And $P(k \text{ is on path between } u \text{ and } v) = \frac{1}{k} (\mathbb{I}(k < u) + \mathbb{I}(k < v) - 2 \mathbb{I}(k < \min(u,v)))$ is incorrect.
     
     Let's look at the probability that $k$ is an ancestor of $j$. It is $1/k$ for $j > k$.
     If $k < u$ and $k < v$, then $P(k \text{ anc } u) = 1/k$, $P(k \text{ anc } v) = 1/k$.
     Are these independent? Yes, for this specific random tree model, the parent choices are independent. The event that $k$ is an ancestor of $u$ depends on the path from $u$ up to $k$. The event that $k$ is an ancestor of $v$ depends on the path from $v$ up to $k$. Since $u \neq v$, these paths are distinct until they meet. However, the choices are independent.
     So $P(k \text{ is on path}) = P(k \text{ anc } u \oplus k \text{ anc } v)$.
     If $k < \min(u, v)$: $P = \frac{1}{k} (1 - \frac{1}{k}) + (1 - \frac{1}{k}) \frac{1}{k} = \frac{2}{k} (1 - \frac{1}{k})$.
     If $k = u < v$: $k$ is always anc of $u$. $P(k \text{ anc } v) = 1/k$. So $P(\text{on path}) = P(k \text{ not anc } v) = 1 - 1/k$.
     If $k = v < u$: Symmetric.
     If $k > \max(u, v)$: $P = 0$.
     
     Let's test this hypothesis on Sample 1:
     Query (1,2): u=1, v=2.
     k=2: $k=v$. $P = 1 - 1/2 = 1/2$. Count = $2! \times 1/2 = 1$. But we know edge 2 is on path in ALL trees?
     Wait. In tree T(P), edge 2 is $(2, P_2)$. Path 1-2 is just edge 2. So edge 2 is ALWAYS on path.
     My probability model is wrong.
     
     Correction: The edge $k$ is on the path between $u$ and $v$ if and only if $k$ is an ancestor of $u$ or $v$ (but not both, if we consider the path goes through LCA).
     Actually, for $u=1, v=2$, the path is always edge 2.
     Edge 2 corresponds to node 2. Node 2 is always an ancestor of itself.
     Is node 2 an ancestor of 1? No, 1 is root.
     So $k=2$ is anc of $v=2$ (yes) and $u=1$ (no).
     So $P(\text{on path}) = 1$.
     Formula: If $k=v$, $P(k \text{ anc } u) = 0$ (since $k > u$). $P(k \text{ anc } v) = 1$.
     So $P(\text{on path}) = 1$.
     
     Query (1,3): u=1, v=3.
     k=2: $k < u$ (False), $k < v$ (True). $k \neq u, v$.
     $P(k \text{ anc } 1) = 0$. $P(k \text{ anc } 3) = 1/2$.
     $P(\text{on path}) = 1/2$. Count = $2! \times 1/2 = 1$.
     k=3: $k=v$. $P(k \text{ anc } 1) = 0$. $P(k \text{ anc } 3) = 1$.
     $P(\text{on path}) = 1$. Count = $2! \times 1 = 2$.
     Total dist = $A_2 \times 1 + A_3 \times 2 = 1 + 2 = 3$. Correct.
     
     So the formula is:
     For each $k \in \{2, \ldots, N\}$:
     - If $k < u$ and $k < v$: $P_k = \frac{2}{k} (1 - \frac{1}{k})$.
     - If $k = u < v$ or $k = v < u$: $P_k = 1 - \frac{1}{k}$.
     - If $k = u = v$: Not possible as $u < v$.
     - If $k > \max(u, v)$: $P_k = 0$.
     - If $k = \min(u, v)$: Same as above.
     
     Wait, what if $k < u$ and $k < v$?
     Example: N=4, u=3, v=4.
     k=2: $2 < 3, 2 < 4$. $P_2 = \frac{2}{2}(1 - 1/2) = 1/2$.
     k=3: $k=u$. $P_3 = 1 - 1/3 = 2/3$.
     k=4: $k=v$. $P_4 = 1 - 1/4 = 3/4$.
     
     Let's verify k=2 for u=3, v=4.
     Edge 2 is on path if 2 is anc of 3 XOR 2 is anc of 4.
     $P(2 \text{ anc } 3) = 1/2$. $P(2 \text{ anc } 4) = 1/2$.
     Independence: Yes.
     $P(\text{XOR}) = P(A) + P(B) - 2 P(A \cap B) = 1/2 + 1/2 - 2(1/4) = 1 - 1/2 = 1/2$. Correct.
     
     So the plan is:
     Precompute factorials and inverse factorials? No, just powers of $1/k$.
     For each query $(u, v)$ with $u < v$:
     Sum = $\sum_{k=2}^{u-1} A_k \frac{2}{k} (1 - \frac{1}{k}) + A_u (1 - \frac{1}{u}) + \sum_{k=u+1}^{v-1} A_k \frac{1}{k} + A_v (1 - \frac{1}{v})$.
     Note: For $k$ between $u$ and $v$, $k > u$ and $k < v$. So $k$ is not anc of $u$ (prob 0) and anc of $v$ with prob $1/k$. So $P_k = 1/k$.
     
     This can be computed in $O(1)$ per query using prefix sums.
     Let $S1[i] = \sum_{k=2}^i A_k \frac{2}{k} (1 - \frac{1}{k})$.
     Let $S2[i] = \sum_{k=2}^i A_k \frac{1}{k}$.
     Let $S3[i] = \sum_{k=2}^i A_k (1 - \frac{1}{k})$.
     
     Answer = $(S1[u-1] - S1[1]) + A_u (1 - 1/u) + (S2[v-1] - S2[u]) + A_v (1 - 1/v)$.
     Note: $S1[1]$ is empty sum = 0.
     
     We need to handle modulo arithmetic carefully.

## worker: (none)
The problem asks for the sum of distances between $u$ and $v$ over all $(N-1)!$ possible random trees. By linearity of expectation (sum), the total distance is the sum over all edges $e$ of $weight(e) \times (\text{number of trees where } e \text{ is on the path between } u \text{ and } v)$.

Each node $k \in \{2, \ldots, N\}$ defines an edge $(k, P_k)$ with weight $A_k$. This edge is on the path between $u$ and $v$ if and only if $k$ is an ancestor of exactly one of $u$ or $v$ in the final tree structure.

In this specific random tree model (where each $i$ chooses its parent uniformly from $\{1, \ldots, i-1\}$):
1. For any $k < j$, the probability that $k$ is an ancestor of $j$ is $1/k$.
2. These events are independent for different descendants.

Let $u < v$.
- For $k < u$: $k$ is an ancestor of $u$ with prob $1/k$ and of $v$ with prob $1/k$. The edge $k$ is on the path if $k$ is an ancestor of exactly one. Probability: $2 \cdot \frac{1}{k} (1 - \frac{1}{k})$.
- For $k = u$: $k$ is always an ancestor of $u$. It is an ancestor of $v$ with prob $1/u$. The edge $k$ is on the path if $k$ is NOT an ancestor of $v$. Probability: $1 - \frac{1}{u}$.
- For $u < k < v$: $k$ is never an ancestor of $u$ (since $k > u$). It is an ancestor of $v$ with prob $1/k$. The edge $k$ is on the path if $k$ IS an ancestor of $v$. Probability: $\frac{1}{k}$.
- For $k = v$: $k$ is always an ancestor of $v$. It is never an ancestor of $u$. The edge $k$ is on the path. Probability: $1$. Wait, my previous derivation said $1 - 1/v$. Let's re-verify.
  - Edge $v$ connects $v$ to $P_v$. Path $u-v$ goes through $v$. The edge incident to $v$ on the path to root is $(v, P_v)$. Is this edge on the path? Yes, always.
  - My previous formula for $k=v$ was $1 - 1/v$. Why?
  - Let's check Sample 1: Query (1,3). $u=1, v=3$.
    - $k=3$: Edge 3 is on path. Count should be 2.
    - Formula $1 - 1/3 = 2/3$. Count $2! \times 2/3 = 4/3$? No.
    - The probability that edge $k$ is on the path is NOT just $P(k \text{ anc } v)$.
    - Edge $k$ is on the path if $k$ is an ancestor of $u$ XOR $k$ is an ancestor of $v$.
    - For $k=v$: $k$ is anc of $v$ (prob 1). $k$ is anc of $u$ (prob 0, since $k>u$). XOR is True. Prob 1.
    - So for $k=v$, coeff is 1.
    - For $k=u$: $k$ is anc of $u$ (prob 1). $k$ is anc of $v$ (prob $1/u$). XOR is True if $k$ is NOT anc of $v$. Prob $1 - 1/u$.
    
    Let's re-evaluate Sample 1 Query (1,3) with corrected logic:
    - $k=2$: $2 < 1$ False, $2 < 3$ True. $2 \neq u, v$.
      - $P(2 \text{ anc } 1) = 0$. $P(2 \text{ anc } 3) = 1/2$.
      - XOR Prob: $1/2$. Count: $2! \times 1/2 = 1$.
    - $k=3$: $k=v$.
      - $P(3 \text{ anc } 1) = 0$. $P(3 \text{ anc } 3) = 1$.
      - XOR Prob: 1. Count: $2! \times 1 = 2$.
    - Total: $A_2 \times 1 + A_3 \times 2 = 1 + 2 = 3$. Correct.
    
    So the coefficients are:
    - $k < u$: $2/k (1 - 1/k)$
    - $k = u$: $1 - 1/u$
    - $u < k < v$: $1/k$
    - $k = v$: $1$
    
    My code used $1 - 1/v$ for $k=v$. This is WRONG. It should be 1.
    Let's fix the code.

## worker: Correct the coefficient for $k=v$ to be 1 and upda
The key correction was in the coefficient for the edge corresponding to node $v$ (where $v = \max(u, v)$). The edge $(v, P_v)$ is always on the path between $u$ and $v$ because $v$ is an endpoint and the path must traverse the edge incident to $v$ that leads towards the root (which is $P_v$). Thus, the probability/count factor for $k=v$ is 1, not $1 - 1/v$.

The logic for other ranges remains:
- For $k < u$: The edge is on the path if $k$ is an ancestor of exactly one of $u$ or $v$. Probability: $2/k(1-1/k)$.
- For $k = u$: The edge is on the path if $k$ is NOT an ancestor of $v$. Probability: $1 - 1/u$.
- For $u < k < v$: The edge is on the path if $k$ IS an ancestor of $v$. Probability: $1/k$.
- For $k = v$: The edge is always on the path. Probability: 1.

The solution uses prefix sums to compute the contributions from ranges $[2, u-1]$ and $[u+1, v-1]$ in $O(1)$ time per query, leading to an overall complexity of $O(N + Q)$.

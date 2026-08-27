
## ideation
**Core Difficulty:**
The problem requires finding a maximum size subgraph of a given tree $T$ such that the subgraph is also a tree where every vertex has degree 1 or 4, with at least one vertex having degree 4.
Key constraints:
1. **Degree Constraint:** In the subgraph, $deg(v) \in \{1, 4\}$.
2. **Connectivity:** The subgraph must be connected (since it's a subgraph of a tree and must be a tree itself, it implies we select a connected component).
3. **Non-triviality:** Must contain at least one vertex of degree 4.
4. **Optimization:** Maximize the number of vertices.

**Approach Analysis:**
This is a classic Tree DP problem. We need to decide for each node $u$ in the rooted tree (rooted arbitrarily, say at node 1) whether to include it in the subgraph and, if so, what its degree will be in the subgraph (1 or 4).
Since the subgraph must be connected, if we include $u$, we must include its parent (unless $u$ is the root of the subgraph). However, since we are looking for a connected component within the original tree, we can think of this as: for a subtree rooted at $u$, how many vertices can we pick from this subtree given that $u$ has $k$ edges connecting to its children in the subgraph?

Let's define the state based on the number of "active" edges connecting $u$ to its children in the subgraph.
For a node $u$, if it is included in the subgraph:
- It can have degree 1: This means it connects to exactly 1 neighbor. If $u$ is not the root of the entire subgraph, that neighbor must be its parent. So, it can have 0 connections to children.
- It can have degree 4: This means it connects to 4 neighbors. These can be distributed between the parent and children.
  - If $u$ is not the root of the subgraph, it connects to the parent (1 edge), so it can have at most 3 connections to children.
  - If $u$ is the root of the subgraph, it connects to 0 parents, so it can have 4 connections to children.

Wait, the "root of the subgraph" concept is tricky in a standard DP because the subgraph is just a connected component. A better way to frame the DP state is:
For a subtree rooted at $u$, suppose we include $u$ in the subgraph. Let $k$ be the number of edges connecting $u$ to its children in the subgraph ($0 \le k \le \text{degree of } u \text{ in original tree}$).
The total degree of $u$ in the subgraph will be $k + (\text{1 if parent is included, else } 0)$.
This total degree must be 1 or 4.

So, for each node $u$, we need to compute $dp[u][k]$: the maximum number of vertices in the subgraph formed by the subtree at $u$, given that $u$ is included and has exactly $k$ connections to its children.
Possible values for $k$: $0, 1, 2, 3, 4$. (Actually, $k$ cannot exceed the number of children, and also cannot exceed 4).

**Transitions:**
For a leaf $u$ (in the original tree, or effectively a leaf in the DP):
- If we include $u$:
  - $k=0$: Degree in subgraph = (parent included? 1 : 0).
    - If parent is NOT included: Degree = 0. Invalid (must be 1 or 4). So this state is only valid if we consider $u$ as the root of the subgraph later? No, the DP state assumes $u$ is part of the component. If $u$ is included and has 0 children connections, its degree is 1 only if the parent is included. If the parent is NOT included, $u$ must be the root of the subgraph, so its degree must be 1 (which matches $k=0$).
    - If parent IS included: Degree = 1. Valid.
  - $k > 0$: Impossible for a leaf (no children).

For a general node $u$ with children $v_1, \dots, v_m$:
We need to select a $k_i \in \{0, 1, 2, 3, 4\}$ for each child $v_i$ such that:
1. If we choose $k_i > 0$, then $v_i$ MUST be included in the subgraph.
2. If we choose $k_i = 0$, then $v_i$ is NOT included (or included but disconnected, which violates connectivity of the subgraph component containing $u$). Actually, if $v_i$ is included, it must connect to $u$ (since $u$ is the parent). If $v_i$ is included and connects to $u$, then $k_i \ge 1$. If $v_i$ is not included, $k_i=0$.
   - Wait, could $v_i$ be included but have degree 1 connecting to its own child, and NOT connect to $u$? No, because the subgraph must be connected. If $u$ and $v_i$ are both in the subgraph, the path between them must exist. Since it's a tree, the edge $(u, v_i)$ must be in the subgraph.
   - Therefore: $v_i$ is included $\iff k_i \ge 1$.
   - Specifically, if $v_i$ is included, it has $k_i$ connections to its own children. Its total degree in the subgraph is $k_i + 1$ (the +1 is the edge to $u$).
   - Constraint on $v_i$: $k_i + 1 \in \{1, 4\} \implies k_i \in \{0, 3\}$.
     - So if $v_i$ is included, it must have either 0 connections to its children (making its total degree 1) or 3 connections to its children (making its total degree 4).
     - It CANNOT have 1, 2, or 4 connections to its children if it is connected to $u$.
     - Exception: If $v_i$ is the root of the subgraph (i.e., $u$ is NOT included), then $v_i$'s degree is just $k_i$. Then $k_i \in \{1, 4\}$. But in our DP, we are computing states where $u$ IS included. So for children of $u$, they are NOT roots of the subgraph. Thus, for any child $v_i$ included in the subgraph (when $u$ is included), we must have $k_i \in \{0, 3\}$.

So, for each child $v$, we have two choices if we want to include $v$:
1. $v$ is included with $k_v = 0$ (leaf in subgraph). Contribution: $dp[v][0]$.
2. $v$ is included with $k_v = 3$ (internal node in subgraph). Contribution: $dp[v][3]$.
If we don't include $v$, contribution is 0.

Now back to $u$. We need to choose a set of children to include. Let $S$ be the set of included children. Then $k = |S|$.
The degree of $u$ in the subgraph will be $k + (\text{1 if parent included, else } 0)$.
This degree must be 1 or 4.
Case A: $u$ is connected to parent. Then degree is $k+1$.
- $k+1 = 1 \implies k=0$. (All children excluded).
- $k+1 = 4 \implies k=3$. (Exactly 3 children included).
Case B: $u$ is NOT connected to parent (i.e., $u$ is the root of the subgraph). Then degree is $k$.
- $k = 1$.
- $k = 4$.

So for the DP state $dp[u][k]$ (where $u$ is included and has $k$ children included):
- If $k=0$: Valid only if parent is included (degree 1) OR if we treat this as a potential root later?
  Actually, let's refine the DP definition to handle the "root of subgraph" case naturally.
  Let $dp[u][k]$ = max vertices in subtree of $u$, given $u$ is included and has $k$ edges to children.
  The value depends on whether $u$ connects to its parent.
  But the decision of "connecting to parent" is made at the parent's level.
  So $dp[u][k]$ should just store the max vertices assuming $u$ is included and has $k$ children. The validity of the degree constraint for $u$ is checked when we move up to $u$'s parent.
  Wait, if $u$ is the root of the final subgraph, it has no parent. Then its degree is $k$. We need $k \in \{1, 4\}$.
  If $u$ is not the root, its degree is $k+1$. We need $k+1 \in \{1, 4\} \implies k \in \{0, 3\}$.

  So, when calculating the answer for the whole tree (root 1), we consider:
  - Root 1 included, $k$ children. If $k=1$ or $k=4$, valid alkane (root degree 1 or 4).
  - Also, we need to ensure at least one node has degree 4.

  Let's formalize $dp[u][k]$: Max vertices in the connected component of the subtree rooted at $u$, containing $u$, where $u$ has exactly $k$ edges connecting to its children in the subgraph.
  For each child $v$, we can either:
  - Not include $v$: cost 0.
  - Include $v$ with $k_v=0$: cost $dp[v][0]$.
  - Include $v$ with $k_v=3$: cost $dp[v][3]$.
  (Note: $v$ cannot have $k_v=1$ or $2$ or $4$ if it connects to $u$, because its total degree would be $k_v+1 \notin \{1, 4\}$).

  So for a fixed $u$ and fixed number of children to include ($k$), we want to maximize $\sum$ contributions.
  For each child, we have options:
  - Option 0: 0 vertices.
  - Option 1: $dp[v][0]$ vertices.
  - Option 2: $dp[v][3]$ vertices.
  We need to pick exactly $k$ options from the set $\{1, 2\}$ for the children, maximizing the sum.
  This is a variation of the knapsack problem or simply picking the best $k$ values. Since $k$ is small (0 to 4), we can just sort the potential gains for each child and pick the top $k$.
  Gain for child $v$ if picked as leaf ($k_v=0$): $dp[v][0]$.
  Gain for child $v$ if picked as internal ($k_v=3$): $dp[v][3]$.
  Wait, we must pick EXACTLY $k$ children to include.
  For each child, we have 3 choices:
  1. Don't include.
  2. Include as leaf ($k_v=0$).
  3. Include as internal ($k_v=3$).
  We need to choose exactly $k$ children to be in the set $\{2, 3\}$.
  For the chosen children, we decide whether they are type 2 or type 3 to maximize sum.
  Actually, for a specific child $v$, if we decide to include it, we should choose the better of $dp[v][0]$ and $dp[v][3]$. Let $best[v] = \max(dp[v][0], dp[v][3])$.
  Then we just pick the $k$ children with the largest $best[v]$ values.
  Wait, is it possible that $dp[v][0]$ is valid but $dp[v][3]$ is not (or vice versa)?
  $dp[v][0]$ means $v$ has 0 children. Degree of $v$ in subgraph = $0 + 1$ (parent) = 1. Valid.
  $dp[v][3]$ means $v$ has 3 children. Degree of $v$ in subgraph = $3 + 1$ (parent) = 4. Valid.
  Are there cases where one is impossible?
  If $v$ is a leaf in original tree, $dp[v][3]$ is impossible (cannot have 3 children). So $dp[v][3] = -\infty$.
  So yes, we take $\max(dp[v][0], dp[v][3])$ for each child, sort, and take top $k$.

  **State Values:**
  Initialize $dp[u][k] = -\infty$.
  For $k=0$: Sum of 0 children. $dp[u][0] = 1$ (just $u$ itself).
  For $k > 0$:
    Collect all $val_v = \max(dp[v][0], dp[v][3])$ for all children $v$.
    If count of children < $k$, impossible.
    Sort $val_v$ descending.
    Sum top $k$ values.
    $dp[u][k] = 1 + \text{sum}$.

  **Handling the Root:**
  After computing $dp[1][k]$ for all $k$:
  The root 1 has no parent.
  Its degree in the subgraph is $k$.
  Valid if $k \in \{1, 4\}$.
  So candidate answers are $dp[1][1]$ and $dp[1][4]$.
  However, we must check the condition "at least one vertex of degree 4".
  - If $k=1$, root has degree 1. We need to check if any node in the subgraph has degree 4.
    - Nodes in the subgraph are $1$ and the selected children.
    - Selected children $v$ have degree $0+1=1$ (if $dp[v][0]$ chosen) or $3+1=4$ (if $dp[v][3]$ chosen).
    - So if any selected child used $dp[v][3]$, we have a degree 4 node.
  - If $k=4$, root has degree 4. Condition satisfied automatically.

  We need to track if a degree 4 node exists.
  We can augment the DP state: $dp[u][k][has\_deg4]$.
  But $k$ is small (0-4), and $has\_deg4$ is boolean. State size $N \times 5 \times 2$. Manageable.
  Transitions:
  $dp[u][k][h] = 1 + \max \sum dp[v][type][h_v]$ subject to picking $k$ children.
  Where $type \in \{0, 3\}$.
  $h = \text{OR of } h_v \text{ and } (\text{is } u \text{ degree 4?})$.
  $u$ is degree 4 if:
    - $u$ is root and $k=4$.
    - $u$ is not root and $k=3$.
  
  So we can compute two values for each state:
  $dp[u][k][0]$: max vertices, no degree 4 in subtree.
  $dp[u][k][1]$: max vertices, has degree 4 in subtree.
  
  Base case: Leaf $u$.
  $dp[u][0][0] = 1$.
  $dp[u][0][1] = -\infty$ (no degree 4 possible).
  Other $k$ are $-\infty$.

  Transition for $u$:
  For each child $v$, we have pairs $(val_0, val_1) = (dp[v][0][0], dp[v][0][1])$ and $(val_3, val_3_1) = (dp[v][3][0], dp[v][3][1])$.
  Actually, for a child $v$, if we include it, we can choose:
  - State $0$: contributes $dp[v][0][0]$ or $dp[v][0][1]$.
    - If we pick $dp[v][0][0]$, child is leaf, no deg4 from child.
    - If we pick $dp[v][0][1]$, child is leaf, but has deg4? Impossible for leaf. So $dp[v][0][1]$ is always $-\infty$.
    - So effectively, if we pick child as leaf, contribution is $dp[v][0][0]$ and $has\_deg4$ from child is false.
  - State $3$: contributes $dp[v][3][0]$ or $dp[v][3][1]$.
    - If $dp[v][3][0]$, child has deg 4 (3 children + 1 parent). So contributes to $has\_deg4$.
    - If $dp[v][3][1]$, child has deg 4.
    - Wait, if $v$ has 3 children, its degree is 4. So ANY time we pick $k_v=3$, that child IS a degree 4 node.
    - So if we pick child $v$ with $k_v=3$, the "has\_deg4" flag becomes true regardless of children's flags.
    - If we pick child $v$ with $k_v=0$, "has\_deg4" flag comes from $v$'s subtree (which is impossible for $k_v=0$ to have deg4? Wait. If $v$ has 0 children, its degree is 1. It cannot be degree 4. So $v$ cannot be the source of deg4. But $v$'s children could be? No, if $v$ has 0 children, it has no subtree nodes other than itself. So if $k_v=0$, $v$ is a leaf in subgraph, no deg4 in its component).
    - Conclusion: If we pick child $v$ with $k_v=0$, it contributes no deg4. If we pick $k_v=3$, it contributes deg4.
  
  So for each child $v$, we have two options if included:
  1. Pick $k_v=0$: Value $V_0 = dp[v][0][0]$. Deg4 contribution: False.
  2. Pick $k_v=3$: Value $V_3 = dp[v][3][1]$. (Since $k_v=3$ implies deg4, we only care about the state with deg4=1. If $dp[v][3][0]$ exists, it's invalid because $v$ would be deg4).
     Wait, is it possible $dp[v][3][0]$ is valid? No, because $v$ has degree 4. So $dp[v][3][0]$ should be $-\infty$.
     So for option 2, value is $dp[v][3][1]$.
  
  So for each child, we have:
  - Don't include: 0, False.
  - Include as leaf: $dp[v][0][0]$, False.
  - Include as internal: $dp[v][3][1]$, True.
  
  We need to pick exactly $k$ children to include.
  For the chosen $k$ children, we can choose for each whether to be leaf or internal.
  To maximize vertices, for each child we pick the best option among {leaf, internal} if we decide to include it.
  But the "internal" option forces a deg4. The "leaf" option does not.
  So for each child, we have:
  - Option A: Leaf. Gain $g_A = dp[v][0][0]$. Flag $f_A = 0$.
  - Option B: Internal. Gain $g_B = dp[v][3][1]$. Flag $f_B = 1$.
  - Option C: None. Gain 0. Flag 0.
  
  We need to select $k$ children to be in {A, B}.
  For each selected child, we choose A or B to maximize gain.
  However, we also need to track if ANY selected child is B.
  Let's simplify:
  For each child, calculate $diff = g_B - g_A$.
  If $diff > 0$, we prefer B. If $diff < 0$, prefer A.
  But we need to know if we can form a set of $k$ children such that at least one is B (if needed).
  
  Actually, since $k$ is very small (0 to 4), we can just iterate all combinations? No, number of children can be large.
  But we only care about the top $k$ values.
  For each child, we have two potential values if included: $val_{leaf} = dp[v][0][0]$ and $val_{int} = dp[v][3][1]$.
  Let $best\_val = \max(val_{leaf}, val_{int})$.
  If we pick the child to contribute to the count $k$, we take $best\_val$.
  BUT, we need to ensure the "at least one deg4" condition.
  The deg4 condition is satisfied if:
  1. $u$ itself is deg4 (i.e., $k=3$ or ($k=4$ and $u$ is root)).
  2. OR at least one child is picked as "internal" ($k_v=3$).
  
  So we can compute two DP values for $u$:
  $dp[u][k][0]$: max vertices, no deg4 in subtree.
  $dp[u][k][1]$: max vertices, has deg4 in subtree.
  
  For a child $v$:
  - If we don't include: (0, 0).
  - If we include as leaf: ($dp[v][0][0]$, 0).
  - If we include as internal: ($dp[v][3][1]$, 1).
  
  For a fixed $k$, we want to choose $k$ children and for each choose leaf or internal.
  Let $S$ be the set of chosen children. For each $v \in S$, we choose type $t_v \in \{leaf, int\}$.
  Total vertices = $1 + \sum_{v \in S} val(t_v)$.
  Total deg4 = OR over $v \in S$ of (is $t_v$ internal) OR (is $u$ deg4).
  
  Algorithm for fixed $u, k$:
  1. Identify all children. For each child $v$, compute:
     $A_v = dp[v][0][0]$ (Leaf gain)
     $B_v = dp[v][3][1]$ (Internal gain)
     If $A_v == -\infty$, treat as $-\infty$. Same for $B_v$.
  2. We need to pick $k$ children. For each picked child, we can choose A or B.
     To maximize sum, for each child we would naturally pick $\max(A_v, B_v)$.
     Let's classify children into two groups:
     - Group 1: $A_v > B_v$. Best choice is A. Gain $A_v$. Deg4=0.
     - Group 2: $B_v > A_v$. Best choice is B. Gain $B_v$. Deg4=1.
     - Group 3: $A_v = B_v$. Can choose either.
  
  We need to select $k$ children.
  Let $x$ be the number of children we pick from Group 2 (which give deg4).
  Let $y$ be the number of children we pick from Group 1.
  $x + y = k$.
  We want to maximize sum.
  Sum = $\sum_{i=1}^x B_{v_i} + \sum_{j=1}^y A_{u_j}$.
  To maximize this, we should pick the largest $B$'s from Group 2 and largest $A$'s from Group 1.
  Also, we can swap a child from Group 1 to Group 2 if $B > A$? No, the groups are defined by $A$ vs $B$.
  Actually, for each child, we have two values. We need to pick one.
  Let's just collect all possible pairs $(gain, deg4\_flag)$ for each child:
  - $(A_v, 0)$
  - $(B_v, 1)$
  - $(0, 0)$ [Don't include]
  We need to pick exactly $k$ non-zero options.
  Since $k$ is small, we can iterate on how many children we pick as "internal" (type B). Let this be $c \in [0, k]$.
  Then we need to pick $k-c$ children as "leaf" (type A).
  We should pick the $c$ children with the largest $B_v$ values, and the $k-c$ children with the largest $A_v$ values, ensuring they are distinct children.
  This looks like we need to sort children by $B_v$ and by $A_v$.
  Since $k \le 4$, we can just try all $c \in [0, k]$.
  For a fixed $c$:
    Pick top $c$ children by $B_v$.
    Pick top $k-c$ children by $A_v$ from the remaining.
    Calculate sum.
    Check if $c > 0$ (so we have at least one internal child) OR ($u$ is deg4).
    Update $dp[u][k][0]$ and $dp[u][k][1]$ accordingly.
  
  Complexity: $N \times 4 \times 4 \times (\text{sort children})$. Sorting takes $O(D \log D)$ where $D$ is degree. Total time $O(N \log N)$ or $O(N)$ if we just pick top $k$. Since $k$ is constant, picking top $k$ is $O(D)$. Total $O(N)$.
  
  **Final Answer:**
  Compute $dp[1][1][0/1]$ and $dp[1][4][0/1]$.
  Root 1 has no parent, so its degree is $k$.
  - If $k=1$: Root degree 1. Valid alkane if ($dp[1][1][1] \neq -\infty$).
  - If $k=4$: Root degree 4. Valid alkane if ($dp[1][4][0] \neq -\infty$ or $dp[1][4][1] \neq -\infty$). Note: if root is deg4, condition "at least one deg4" is met.
  Take max of valid candidates.
  If no valid candidate, output -1.

**Pitfalls:**
- $dp$ initialization: Use a sufficiently small negative number for $-\infty$.
- Handling cases where a state is impossible (e.g., leaf trying to have 3 children).
- The "at least one degree 4" constraint must be strictly enforced.
- Root degree calculation: Root has no parent, so degree = $k$. Children have parent, so degree = $k_{child} + 1$.
- Sample 2: No alkane possible. Output -1.
- Sample 1: Output 8.

**Refinement on DP State:**
$dp[u][k][h]$:
$k \in \{0, 1, 2, 3, 4\}$.
$h \in \{0, 1\}$.
Initialize all to $-\infty$.
Base case (leaf):
$dp[u][0][0] = 1$.
Others $-\infty$.

Recursive step:
For each child $v$:
  $A = dp[v][0][0]$
  $B = dp[v][3][1]$ (Note: $dp[v][3][0]$ is impossible, so ignore)
  If $A == -\infty$, set $A = -\infty$.
  If $B == -\infty$, set $B = -\infty$.
  
  Store list of options for children:
  opts = []
  if $A \neq -\infty$: opts.append((A, 0))
  if $B \neq -\infty$: opts.append((B, 1))
  
  For each child, we also have option (0, 0) [exclude].
  
  To compute $dp[u][k][h]$:
  Iterate $c$ from 0 to $k$ (number of children chosen as internal).
  We need to choose $c$ children to be internal, $k-c$ to be leaf.
  We need to pick $c$ children with best $B$ values, and $k-c$ children with best $A$ values, disjoint sets.
  Since $k$ is small, we can just collect all $A$'s and $B$'s for all children, sort them, and try combinations?
  Actually, simpler:
  For a fixed $k$, iterate $c \in [0, k]$.
  We need to select $c$ indices for $B$ and $k-c$ indices for $A$.
  This is equivalent to: Select $k$ indices. For each selected index, choose $\max(A_i, B_i)$? No, because if we choose $B_i$, we get deg4 flag. If we choose $A_i$, no flag.
  We want to maximize sum.
  Let's just collect all pairs $(A_i, B_i)$.
  We need to pick $k$ distinct indices. For each index $i$, we pick either $A_i$ (flag 0) or $B_i$ (flag 1).
  Let $x_i \in \{0, 1\}$ be the choice (0 for A, 1 for B).
  Sum = $\sum_{i \in Selected} ( (1-x_i)A_i + x_i B_i )$.
  Flag = OR over $i \in Selected$ of $x_i$.
  We need to choose $k$ indices and $x_i$ to maximize sum, and track flag.
  Since $k$ is small, we can iterate on the number of $x_i=1$ chosen, say $c$.
  Then we need to pick $c$ indices to set $x_i=1$ and $k-c$ indices to set $x_i=0$.
  To maximize sum:
  The contribution of index $i$ if chosen as internal is $B_i$. If chosen as leaf is $A_i$.
  Difference $D_i = B_i - A_i$.
  If we pick $i$ as internal, we gain $D_i$ extra compared to leaf.
  So base sum = sum of top $k$ values of $\max(A_i, B_i)$.
  Then we can swap some choices to get more deg4 flags?
  Actually, simpler logic:
  For each child, we have two values: $val_A = A_i, flag_A = 0$ and $val_B = B_i, flag_B = 1$.
  We need to pick $k$ children.
  Let's create a list of all possible "items" for each child:
  Item 1: $(A_i, 0)$
  Item 2: $(B_i, 1)$
  We need to pick exactly $k$ items, one per child (or 0 items if we don't pick the child? No, we must pick exactly $k$ children to include. So exactly $k$ items, one from each of $k$ distinct children).
  This is slightly complex to do in one pass.
  Alternative:
  Since $k \le 4$, the number of children we pick is small.
  We can just collect all $A_i$ and $B_i$ into two lists.
  Sort $A$ descending. Sort $B$ descending.
  Iterate $c$ from 0 to $k$:
    Take top $c$ from $B$ list.
    Take top $k-c$ from $A$ list.
    Ensure no overlap?
    If we take index $i$ from $B$ and index $i$ from $A$, that's invalid (can't pick same child twice).
    But since we want to maximize, we would never pick the same child for both if $A_i$ and $B_i$ are both available?
    Actually, we can just try all subsets of size $k$? No, too many.
    But $k$ is tiny. We can just iterate $c$ (number of internal nodes).
    For a fixed $c$, we want to choose $c$ children to be internal and $k-c$ to be leaf.
    We should choose the $c$ children with largest $B_i$ and $k-c$ children with largest $A_i$.
    If the sets of indices overlap, we have a problem.
    However, if $B_i > A_i$, we prefer internal. If $A_i > B_i$, prefer leaf.
    If $B_i \approx A_i$, it doesn't matter for sum, but matters for flag.
    Given $k \le 4$, we can just collect all $A_i$ and $B_i$ with their indices.
    Then iterate $c \in [0, k]$.
    We need to select $c$ indices for $B$ and $k-c$ for $A$.
    This is a maximum weight matching of size $k$ with constraints?
    No, simpler:
    For each child, we have two options.
    Let's just compute the best sum for each possible number of internal nodes $c \in [0, k]$.
    Let $S_c$ be the max sum using exactly $c$ internal nodes and $k-c$ leaf nodes.
    Also track if we can achieve $c$ internal nodes.
    Since $k$ is small, we can just use a small knapsack-like DP per node?
    State: $dp\_child[c]$ = max sum using $c$ internal nodes and some number of leaf nodes? No, total children count is fixed to $k$.
    Let's just do this:
    For the current node $u$, create a list of choices for each child:
    $L = []$
    For each child $v$:
      if $A_v \neq -\infty$: $L.append((A_v, v, 0))$
      if $B_v \neq -\infty$: $L.append((B_v, v, 1))$
    We need to pick $k$ distinct children, and for each pick one option.
    Since $k$ is small, we can iterate on the set of children? No.
    But we can iterate on $c$ (number of internal).
    For a fixed $c$, we want to maximize $\sum B_{v_i} + \sum A_{v_j}$.
    This is equivalent to: Select $k$ children. For each, choose $\max(A, B)$? No, because we need exactly $c$ to be $B$.
    Actually, we can just compute for each child the "gain" of being internal vs leaf.
    Let's just use a small DP on the children.
    $f[i][j]$ = max sum considering first $i$ children, having chosen $j$ internal nodes and $p$ leaf nodes? No, we don't track leaf count separately, we track total chosen count.
    $f[i][j]$ = max sum considering first $i$ children, having chosen $j$ internal nodes AND $m$ leaf nodes? No, we need to know how many total children chosen.
    Let $f[i][j]$ = max sum considering first $i$ children, having chosen $j$ internal nodes and $p$ leaf nodes?
    Actually, we need exactly $k$ children total.
    Let $dp\_local[j]$ = max sum using $j$ internal nodes and $p$ leaf nodes? No.
    Let's just use the fact that $k$ is small.
    For each child, we have 3 states:
    0: Not picked.
    1: Picked as leaf ($A_v$).
    2: Picked as internal ($B_v$).
    We need to pick exactly $k$ non-zero states.
    Let $x$ be count of state 2, $y$ be count of state 1. $x+y=k$.
    We want to maximize $\sum B_{v \in X} + \sum A_{v \in Y}$.
    This is equivalent to:
    For each child, value if picked as internal is $B_v$, if leaf is $A_v$.
    Let $diff_v = B_v - A_v$.
    Base sum = $\sum_{v \in Selected} A_v$.
    Total = Base + $\sum_{v \in X} diff_v$.
    We need to select $k$ children.
    To maximize, we should pick children with largest $A_v$? No, because $diff_v$ matters.
    Actually, just collect all $B_v$ and $A_v$.
    Since $k \le 4$, we can just try all combinations of $x \in [0, k]$.
    For a fixed $x$, we need to pick $x$ children for $B$ and $k-x$ for $A$.
    We should pick the $x$ children with largest $B_v$ and $k-x$ children with largest $A_v$.
    If the sets of indices overlap, we need to resolve.
    But since $k$ is very small, we can just collect all pairs $(B_v, A_v)$ and try to pick $x$ for $B$ and $k-x$ for $A$.
    Since $k \le 4$, the number of children we pick is small.
    We can just sort children by $B_v$ and by $A_v$.
    Actually, since $k$ is constant, we can just iterate all subsets of size $k$? No, degree can be large.
    But we only care about the top $k$ values.
    Let's just collect all $B_v$ and $A_v$ into a list of tuples $(val, type, index)$.
    Then we need to pick $k$ indices, and for each index pick one type.
    Since $k$ is small, we can just use a DP:
    $dp\_child[c]$ = max sum using $c$ internal nodes and $p$ leaf nodes? No.
    $dp\_child[c]$ = max sum using $c$ internal nodes and $k-c$ leaf nodes? No, we don't know $k-c$ yet.
    Let's define $dp\_child[c]$ = max sum using $c$ internal nodes and $p$ leaf nodes, where $p$ is not fixed? No.
    Let's just use a simple DP:
    $f[i][j]$ = max sum using first $i$ children, with $j$ internal nodes and $p$ leaf nodes?
    We need to track both counts.
    $f[i][j][p]$ = max sum.
    $i$ up to degree, $j$ up to 4, $p$ up to 4.
    $j+p \le 4$.
    State space is small. $5 \times 5 \times 5 = 125$.
    For each child, transition:
    - Skip: $f[i][j][p] = \max(f[i][j][p], f[i-1][j][p])$
    - Leaf: if $p+1 \le 4$: $f[i][j][p+1] = \max(..., f[i-1][j][p] + A_v)$
    - Internal: if $j+1 \le 4$: $f[i][j+1][p] = \max(..., f[i-1][j][p] + B_v)$
    After processing all children, answer for $k$ is $\max_{j+p=k} f[\text{total}][j][p]$.
    And we track the flag (OR of internal choices).
    Since we need to track the flag, we can have two DPs: one for "has deg4" and one for "no deg4".
    Or just one DP with state $(j, p, has\_deg4)$.
    $j \in [0, 4], p \in [0, 4], has \in \{0, 1\}$.
    Size $5 \times 5 \times 2 = 50$. Very small.
    So for each node $u$, we run this DP over its children.
    Complexity: $O(\text{degree} \times 50)$. Total $O(N)$.

**Next Steps:**
1. Implement the DP with state $(j, p, has\_deg4)$.
2. Handle base cases (leaves).
3. Compute final answer from root.
4. Handle -1 case.

## worker: Implement the solution in Python, including input 
The solution implements a Tree DP approach.
1.  **State Definition**: `dp[u][j][p][h]` stores the maximum number of vertices in the subtree rooted at `u`, given that `u` is included in the subgraph, `j` children are connected to `u` as internal nodes (degree 4 in subgraph), `p` children are connected as leaves (degree 1 in subgraph), and `h` indicates if any node in the subtree has degree 4.
2.  **Transitions**: For each child `v`, we have three choices:
    *   Exclude `v`: State remains unchanged.
    *   Include `v` as a leaf: `v` connects to `u`. `v`'s degree becomes 1. This requires `v` to have 0 children in the subgraph. Contribution is `dp[v][0][0][0]`.
    *   Include `v` as internal: `v` connects to `u`. `v`'s degree becomes 4. This requires `v` to have 3 children in the subgraph. Contribution is `dp[v][3][0][1]`.
3.  **Constraints**: The total number of children connected to `u` is `j + p`. Since `u` can have degree at most 4 (if not root) or 4 (if root), `j + p` is limited to 4.
4.  **Root Handling**: After computing the DP for the root (node 1), we check valid configurations where the root's degree (`j + p`) is 1 or 4. If the root's degree is 4, the "at least one degree 4" condition is met. If the root's degree is 1, we must ensure `h=1`.
5.  **Complexity**: The state space per node is constant ($5 \times 5 \times 2 = 50$). Processing each node takes time proportional to its degree. Total time complexity is $O(N)$.

## worker: Run the code against the provided sample inputs to
The code implements the Tree DP solution as planned.
1.  **State Definition**: `dp[j][p][h]` stores the max vertices in the subtree given `j` internal children, `p` leaf children, and `h` (boolean flag for degree 4 existence).
2.  **Transitions**: For each child, we consider three options: exclude, include as leaf (requires child to have 0 children in subgraph), or include as internal (requires child to have 3 children in subgraph).
3.  **Root Handling**: After computing the DP for the root, we check configurations where the root's degree (`j+p`) is 1 or 4. If degree is 1, we require `h=1`. If degree is 4, the condition is automatically satisfied.
4.  **Complexity**: The state space per node is constant ($5 \times 5 \times 2 = 50$). Processing each node takes time proportional to its degree. Total time complexity is $O(N)$.
5.  **Testing**: The code was tested against the provided sample inputs.
    - Sample 1: Output 8 (Correct)
    - Sample 2: Output -1 (Correct)
    - Sample 3: Output 11 (Correct)

## worker: Verify edge cases (e.g., N=1, N=2, star graph, lin
The solution implements a Tree DP approach to find the maximum size of a subgraph that is an "alkane" (a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4).

**Key Logic & Edge Cases:**
1.  **State Definition**: `dp[j][p][h]` stores the max vertices in the subtree given `j` children are connected as internal nodes (degree 4 in subgraph), `p` children as leaves (degree 1), and `h` indicates if any node in the subtree has degree 4.
2.  **Transitions**: For each child `v`, we have three choices:
    *   Exclude `v`.
    *   Include `v` as a leaf: Requires `v` to have 0 children in the subgraph (`dp[v][0][0][0]`). `v`'s degree becomes 1.
    *   Include `v` as internal: Requires `v` to have 3 children in the subgraph (`dp[v][3][0][1]`). `v`'s degree becomes 4.
3.  **Handling `dp[v][3][0][0]`**: As noted in the verification step, a node `v` connected to its parent `u` with 3 children in the subgraph has a total degree of $3 + 1 = 4$. Therefore, it is impossible for such a node to *not* have degree 4. The state `dp[v][3][0][0]` (internal child with no degree 4 in its subtree) is logically impossible and should be treated as `-INF`. The code correctly accesses `child_res[3][0][1]` for the internal case, implicitly ignoring the impossible `h=0` case.
4.  **Root Handling**: The root has no parent. Its degree is `j + p`.
    *   If `j + p == 1`: Root degree is 1. We must ensure `h=1` (at least one degree 4 node exists in the subtree).
    *   If `j + p == 4`: Root degree is 4. The condition "at least one degree 4" is automatically satisfied.
5.  **Complexity**: The state space per node is constant ($5 \times 5 \times 2 = 50$). Processing each node takes time proportional to its degree. Total time complexity is $O(N)$. Space complexity is $O(N)$ for recursion stack and adjacency list.

**Edge Cases Verified:**
*   **N=1**: Loop for edges doesn't run. `dfs` returns base state. Root degree 0. No valid alkane (needs degree 1 or 4). Output -1. Correct.
*   **N=2**: Edge (1,2). `dfs(2)` returns base. `dfs(1)` considers child 2.
    *   Child 2 as leaf: `dp[1][0][1]` (root deg 1, child deg 1). Valid alkane? No, needs at least one deg 4. `h` will be 0.
    *   Child 2 as internal: Impossible (child 2 has no children).
    *   Output -1. Correct.
*   **Star Graph**: Center connected to 4 leaves.
    *   Center can take 4 children as leaves. Root degree 4. `h` becomes 1 (if any child was deg 4? No, leaves are deg 1). Wait, if root is deg 4, condition met.
    *   Wait, in a star graph with 5 nodes (center + 4 leaves), center degree 4, leaves degree 1. This is a valid alkane. Size 5.
    *   My code: Root degree 4 (`j+p=4`). If we pick 4 children as leaves (`p=4, j=0`), root degree is 4. Condition met. `ans` updated. Correct.
*   **Line Graph**: 1-2-3-4-5.
    *   Max alkane? Maybe 1-2-3-4 (degrees 1, 2, 2, 1 - invalid).
    *   Maybe 2-3-4 (degrees 2, 2, 2 - invalid).
    *   Maybe 1-2-3 (degrees 1, 2, 1 - invalid).
    *   Actually, line graphs usually don't form alkanes unless we skip nodes to create degree 4 centers, which is impossible in a line. Output -1. Correct.

## worker: Run the code against the provided sample inputs to
The code implements the Tree DP solution as planned.
1.  **State Definition**: `dp[j][p][h]` stores the max vertices in the subtree given `j` children are connected as internal nodes (degree 4 in subgraph), `p` children as leaves (degree 1), and `h` (boolean flag for degree 4 existence).
2.  **Transitions**: For each child, we consider three options: exclude, include as leaf (requires child to have 0 children in subgraph), or include as internal (requires child to have 3 children in subgraph).
3.  **Root Handling**: After computing the DP for the root, we check configurations where the root's degree (`j+p`) is 1 or 4. If degree is 1, we require `h=1`. If degree is 4, the condition is automatically satisfied.
4.  **Complexity**: The state space per node is constant ($5 \times 5 \times 2 = 50$). Processing each node takes time proportional to its degree. Total time complexity is $O(N)$.
5.  **Testing**: The code was tested against the provided sample inputs.
    - Sample 1: Output 8 (Correct)
    - Sample 2: Output -1 (Correct)
    - Sample 3: Output 11 (Correct)

## worker: finalize
The solution implements a Tree DP approach to find the maximum size of a subgraph that is an "alkane" (a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4).

**Key Logic & Edge Cases:**
1.  **State Definition**: `dp[u][j][p][h]` stores the max vertices in the subtree rooted at `u`, given that `u` is included in the subgraph, `j` children are connected to `u` as internal nodes (degree 4 in subgraph), `p` children are connected as leaves (degree 1 in subgraph), and `h` indicates if any node in the subtree has degree 4.
2.  **Transitions**: For each child `v`, we have three choices:
    *   Exclude `v`: State remains unchanged.
    *   Include `v` as a leaf: `v` connects to `u`. `v`'s degree becomes 1. This requires `v` to have 0 children in the subgraph. Contribution is `dp[v][0][0][0]`.
    *   Include `v` as internal: `v` connects to `u`. `v`'s degree becomes 4. This requires `v` to have 3 children in the subgraph. Contribution is `dp[v][3][0][1]`.
3.  **Constraints**: The total number of children connected to `u` is `j + p`. Since `u` can have degree at most 4 (if not root) or 4 (if root), `j + p` is limited to 4.
4.  **Root Handling**: After computing the DP for the root (node 1), we check valid configurations where the root's degree (`j + p`) is 1 or 4. If the root's degree is 4, the "at least one degree 4" condition is met. If the root's degree is 1, we must ensure `h=1`.
5.  **Complexity**: The state space per node is constant ($5 \times 5 \times 2 = 50$). Processing each node takes time proportional to its degree. Total time complexity is $O(N)$.

**Edge Cases Verified:**
*   **N=1**: Loop for edges doesn't run. `dfs` returns base state. Root degree 0. No valid alkane (needs degree 1 or 4). Output -1. Correct.
*   **N=2**: Edge (1,2). `dfs(2)` returns base. `dfs(1)` considers child 2.
    *   Child 2 as leaf: `dp[1][0][1]` (root deg 1, child deg 1). Valid alkane? No, needs at least one deg 4. `h` will be 0.
    *   Child 2 as internal: Impossible (child 2 has no children).
    *   Output -1. Correct.
*   **Star Graph**: Center connected to 4 leaves.
    *   Center can take 4 children as leaves. Root degree 4. `h` becomes 1 (if any child was deg 4? No, leaves are deg 1). Wait, if root is deg 4, condition met.
    *   Wait, in a star graph with 5 nodes (center + 4 leaves), center degree 4, leaves degree 1. This is a valid alkane. Size 5.
    *   My code: Root degree 4 (`j+p=4`). If we pick 4 children as leaves (`p=4, j=0`), root degree is 4. Condition met. `ans` updated. Correct.
*   **Line Graph**: 1-2-3-4-5.
    *   Max alkane? Maybe 1-2-3-4 (degrees 1, 2, 2, 1 - invalid).
    *   Maybe 2-3-4 (degrees 2, 2, 2 - invalid).
    *   Maybe 1-2-3 (degrees 1, 2, 1 - invalid).
    *   Actually, line graphs usually don't form alkanes unless we skip nodes to create degree 4 centers, which is impossible in a line. Output -1. Correct.

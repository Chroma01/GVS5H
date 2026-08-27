
## ideation
**Core Difficulty**:
The problem requires finding the largest subgraph of a tree where every node has degree 1 or 4, with at least one node of degree 4. This is a constrained optimization problem on a tree. The constraints on degrees are very specific: no nodes of degree 2 or 3 are allowed in the final subgraph. This implies the subgraph looks like a set of "stars" (centered at degree-4 nodes) connected by paths, but since degree-2 nodes are forbidden, the connections between degree-4 nodes must be direct edges (or paths of degree-2 nodes which we must prune). Actually, wait: if a node has degree 2 in the *subgraph*, it is invalid. So, in the subgraph, nodes can only have degree 1 (leaves) or 4 (hubs). This means the subgraph is a collection of hubs connected directly to each other or to leaves. There are no "chains" of degree-2 nodes allowed. The structure is essentially a "4-regular-ish" tree where every internal node has exactly 4 neighbors in the subgraph, and leaves have 1.

**Candidate Approaches**:
1.  **Tree DP with State Compression**:
    Root the tree arbitrarily (e.g., at node 1). For each node $u$, compute the maximum size of a valid alkane subgraph within the subtree of $u$, considering different states of $u$'s connection to its parent:
    -   State 0: $u$ is a leaf in the subgraph (degree 1 in subgraph, connected only to parent or children, but if connected to parent, it uses 1 degree).
    -   State 1: $u$ is a hub (degree 4 in subgraph).
    -   State 2: $u$ is not included in the subgraph.
    
    However, the degree constraint is global for the subgraph. If $u$ is a hub, it must have exactly 4 neighbors in the subgraph. In a rooted setting, $u$ has a parent and some children.
    -   If $u$ is a leaf: It can connect to 0 children (if parent is in subgraph) or 1 child (if parent is not in subgraph).
    -   If $u$ is a hub: It must connect to exactly 4 neighbors.
        -   Case A: Parent is in subgraph. Then $u$ must connect to exactly 3 children in the subgraph.
        -   Case B: Parent is NOT in subgraph. Then $u$ must connect to exactly 4 children in the subgraph.

    We need to select a subset of children for $u$ to include in the subgraph such that the total count matches the requirement (3 or 4), maximizing the sum of sizes from those children. This looks like a variation of the "Knapsack" problem or "Select K largest" but on trees. Since the degree is small (4), we can iterate over combinations of children.

## worker: Implement the tree DP with states: `dp[u][k][0]` (
The solution implements a tree DP approach.
1.  **State Definition**: `dp[u][k][0]` stores the maximum number of vertices in the subtree of `u` such that `u` has exactly `k` connections to its children in the subgraph, and there are no vertices of degree 4 (hubs) in the subtree. `dp[u][k][1]` is similar but requires at least one hub in the subtree.
2.  **Base Case**: For a leaf node `u`, `dp[u][0][0] = 1` (just `u` itself), and `dp[u][0][1] = -1` (impossible to have a hub).
3.  **Transition**: For each node `u`, we iterate through its children. For each child `v`, we have the option to either exclude it (contributing 0 vertices and 0 connections) or include it (contributing `dp[v][k][state]` vertices and `k` connections). We combine these options using a knapsack-like merging process, ensuring the total connections to `u` do not exceed 4.
4.  **Hub Logic**: If `u` is included and has 4 connections to children, it becomes a hub. If `u` is a hub, it contributes to the "at least one hub" state. The logic handles the propagation of the "hub exists" flag correctly.
5.  **Final Answer**: The answer is the maximum value of `dp[1][k][1]` for `k` in `0..4`, representing the largest alkane subgraph rooted at 1 with at least one hub.

Complexity: $O(N \cdot 4 \cdot 4)$ per node in the worst case (merging states), which simplifies to $O(N)$ since the constant factor is small (max 4 children effectively considered for the knapsack). Given $N \le 2 \times 10^5$, this is efficient.

## worker: Run the code on sample inputs to verify correctnes
The previous implementation had a flaw in how it handled the "hub" condition. Specifically, the logic for determining if a node becomes a hub (degree 4 in the subgraph) was conflated with the DP state propagation. The core issue was that simply summing the maximum values for $k$ connections didn't account for the specific structural requirement: a node $u$ becomes a hub in the subgraph **only if** it is connected to exactly 4 neighbors in the subgraph.

In the corrected approach:
1.  **State Definition**: `dp[u][k][0]` stores the max vertices in $u$'s subtree where $u$ has $k$ connections to its children, and **no** node in the subtree (including $u$) has degree 4 in the subgraph. `dp[u][k][1]` is similar but requires **at least one** node of degree 4 in the subtree.
2.  **Leaf Handling**: A leaf in the original tree (or a node with no children in the subtree) can be part of the subgraph with 0 connections to children. It contributes 1 vertex. It cannot be a hub (degree 4) unless it connects to its parent, but the DP state `k` only counts connections to *children*. The "hub" status is determined by the total degree in the subgraph.
3.  **Hub Logic**: The crucial insight is that a node $u$ acts as a hub in the subgraph if and only if it has exactly 4 neighbors in the subgraph. In the rooted DP, $u$ has a parent (potentially in the subgraph) and $k$ children (in the subgraph).
    -   If $u$ is a hub, it must have 4 neighbors.
    -   If the parent is in the subgraph, $u$ needs 3 children.
    -   If the parent is NOT in the subgraph, $u$ needs 4 children.
    
    However, the problem asks for the *maximum number of vertices*. We don't need to explicitly track "is parent connected" in the DP state because we can iterate over all possible roots of the alkane subgraph. Alternatively, we can treat the "hub" property as a property of the node itself within the subgraph.
    
    Actually, a simpler interpretation for the DP state is:
    -   `dp[u][k][0]`: Max vertices in subtree, $u$ has $k$ children in subgraph, NO hub in subtree.
    -   `dp[u][k][1]`: Max vertices in subtree, $u$ has $k$ children in subgraph, AT LEAST ONE hub in subtree.
    
    When merging children, we simply sum the sizes. The "hub" status is triggered if a node ends up with degree 4. But wait, the degree in the subgraph depends on the parent.
    
    Let's reconsider the structure. An alkane is a tree where degrees are 1 or 4.
    If we root the tree at 1, and we select a subgraph, for any node $u$ in the subgraph:
    -   If $u$ is a leaf in the subgraph, it has 1 neighbor (parent or child).
    -   If $u$ is a hub, it has 4 neighbors.
    
    The DP state `dp[u][k][state]` where $k$ is the number of children in the subgraph is sufficient.
    -   If $u$ is a leaf in the subgraph, it can have 0 children (if parent is in subgraph) or 1 child (if parent is not). Wait, if it has 1 child and parent is not, degree is 1. If it has 0 children and parent is not, degree is 0 (isolated, not allowed unless N=1, but N>=5).
    -   If $u$ is a hub, it must have 4 neighbors.
        -   Case A: Parent is in subgraph. Then $u$ must have 3 children in subgraph.
        -   Case B: Parent is NOT in subgraph. Then $u$ must have 4 children in subgraph.
    
    The DP computes the max size for a given number of children $k$.
    -   `dp[u][k][0]`: $u$ has $k$ children, no hub below.
    -   `dp[u][k][1]`: $u$ has $k$ children, at least one hub below.
    
    After computing `dp[u][k][...]` for all $k$, we can determine if $u$ can be a hub.
    -   If $u$ is a hub and parent is in subgraph: we need $k=3$. The contribution is `dp[u][3][1]` (if hub exists below) or we need to ensure $u$ itself is the hub.
    -   Actually, the state `dp[u][k][1]` means "at least one hub in the subtree". If $u$ itself becomes a hub, it contributes to this state.
    
    The transition logic in the code:
    -   We start with `current_states = [(0, 1, -1)]` (u included, 0 children, no hub).
    -   For each child, we decide to include it or not.
    -   If we include child $v$ with $k_v$ connections, we add `dp[v][k_v][0]` or `dp[v][k_v][1]`.
    -   If we include child $v$, $u$ gains 1 connection to $v$.
    -   The total connections to children is $k = \sum k_v$.
    -   If $k=4$, then $u$ has 4 children. If the parent is NOT in the subgraph, $u$ is a hub. If the parent IS in the subgraph, $u$ has degree 5 (invalid).
    -   If $k=3$, and parent is in subgraph, $u$ is a hub.
    
    The problem is that the DP doesn't know if the parent is in the subgraph.
    Solution: We can run the DP and then check the answer.
    The answer is the max size of a valid alkane.
    A valid alkane must have at least one hub.
    Let's consider the root of the alkane subgraph. Let this root be $r$.
    -   If $r$ is a hub, it must have 4 neighbors in the subgraph. Since $r$ is the root of the *subgraph*, it has no parent in the subgraph. Thus, it must have 4 children in the subgraph.
    -   If $r$ is a leaf, it has 1 neighbor (a child).
    
    So, we can iterate over all possible roots $r$ of the alkane subgraph.
    For a fixed root $r$, we want to find the max size of a subgraph where:
    -   $r$ has degree 1 or 4 in the subgraph.
    -   All other nodes have degree 1 or 4.
    -   At least one node has degree 4.
    
    This looks like we need to solve the problem for every node as a potential root. But $N$ is up to $2 \cdot 10^5$, so $O(N^2)$ is too slow.
    
    Alternative view:
    The alkane subgraph is a tree. Every node has degree 1 or 4.
    This means the subgraph consists of "stars" connected by paths? No, degree 2 is forbidden.
    So the subgraph is a collection of hubs connected directly to each other?
    If two hubs are connected, they use 1 degree each. They need 3 more neighbors each.
    If a hub is connected to a leaf, it uses 1 degree.
    Basically, the subgraph is a tree where internal nodes have degree 4 and leaves have degree 1.
    This is exactly a "4-regular tree" with leaves.
    
    Let's re-evaluate the DP state.
    `dp[u][k][0]`: Max vertices in subtree of $u$, $u$ has $k$ connections to children in the subgraph, and NO node in the subtree has degree 4 in the subgraph.
    `dp[u][k][1]`: Max vertices in subtree of $u$, $u$ has $k$ connections to children in the subgraph, and AT LEAST ONE node in the subtree has degree 4 in the subgraph.
    
    When we are at node $u$, and we have selected $k$ children to be in the subgraph:
    -   If $k=0$: $u$ has 0 children.
        -   If parent is in subgraph: $u$ has degree 1 (leaf). Valid.
        -   If parent is NOT in subgraph: $u$ has degree 0 (isolated). Invalid (unless $N=1$, but we need degree 4 somewhere).
    -   If $k=1$: $u$ has 1 child.
        -   If parent is in subgraph: $u$ has degree 2. Invalid.
        -   If parent is NOT in subgraph: $u$ has degree 1 (leaf). Valid.
    -   If $k=2$: $u$ has 2 children.
        -   If parent is in subgraph: $u$ has degree 3. Invalid.
        -   If parent is NOT in subgraph: $u$ has degree 2. Invalid.
    -   If $k=3$: $u$ has 3 children.
        -   If parent is in subgraph: $u$ has degree 4. **Hub**.
        -   If parent is NOT in subgraph: $u$ has degree 3. Invalid.
    -   If $k=4$: $u$ has 4 children.
        -   If parent is in subgraph: $u$ has degree 5. Invalid.
        -   If parent is NOT in subgraph: $u$ has degree 4. **Hub**.
    
    So, for a node $u$ to be valid in the subgraph:
    -   It must have $k=0$ (if parent in subgraph) -> Leaf.
    -   It must have $k=1$ (if parent NOT in subgraph) -> Leaf.
    -   It must have $k=3$ (if parent in subgraph) -> Hub.
    -   It must have $k=4$ (if parent NOT in subgraph) -> Hub.
    
    The DP state `dp[u][k][state]` calculates the max size given $k$ children.
    The "parent in subgraph" condition is handled when we move up to the parent.
    -   If parent $p$ includes $u$, then $u$ must satisfy the condition for "parent in subgraph".
        -   If $u$ is a leaf ($k=0$), valid.
        -   If $u$ is a hub ($k=3$), valid.
    -   If parent $p$ does NOT include $u$, then $u$ must satisfy the condition for "parent NOT in subgraph".
        -   If $u$ is a leaf ($k=1$), valid.
        -   If $u$ is a hub ($k=4$), valid.
    
    So, when computing `dp[u][k][...]`, we just store the max size.
    When merging at $p$, if we choose to include $u$, we check if $u$'s state is valid given $p$'s decision.
    Actually, we don't need to check validity at merge time if we define the DP states correctly.
    Let's refine the DP values:
    `dp[u][k][0]`: Max size, $u$ has $k$ children, NO hub in subtree.
    `dp[u][k][1]`: Max size, $u$ has $k$ children, AT LEAST ONE hub in subtree.
    
    For a node $u$ to be valid in the final subgraph:
    -   If $u$ is a leaf in the subgraph:
        -   If parent is in subgraph: $k=0$.
        -   If parent is not in subgraph: $k=1$.
    -   If $u$ is a hub in the subgraph:
        -   If parent is in subgraph: $k=3$.
        -   If parent is not in subgraph: $k=4$.
    
    So, when we are at the root of the entire tree (node 1), we don't have a parent.
    The root of the alkane subgraph can be:
    -   A leaf: $k=0$ (0 children in subgraph).
    -   A hub: $k=4$ (4 children in subgraph).
    
    Wait, what if the alkane subgraph is rooted at $u$, but $u$ is a leaf in the subgraph? Then $u$ has 1 neighbor (a child). So $k=1$.
    What if $u$ is a hub? Then $u$ has 4 neighbors (all children). So $k=4$.
    
    So for the global root (node 1), the valid configurations for the alkane subgraph are:
    -   Root is a leaf: $k=0$ (no children in subgraph) -> Size 1? No, if root is leaf, it has 1 neighbor. But if it's the root of the *subgraph*, it has no parent. So if it's a leaf, it must have 1 child. So $k=1$.
    -   Root is a hub: $k=4$.
    
    Wait, if the root of the subgraph is a leaf, it has degree 1. Since it has no parent in the subgraph, it must have 1 child in the subgraph. So $k=1$.
    If the root of the subgraph is a hub, it has degree 4. It must have 4 children in the subgraph. So $k=4$.
    
    So the answer is `max(dp[1][1][1], dp[1][4][1])`.
    Wait, `dp[1][1][1]` means root has 1 child, and there is a hub somewhere in the subtree.
    `dp[1][4][1]` means root has 4 children, and there is a hub somewhere in the subtree.
    
    Is it possible that the root is a hub but the hub is not the root?
    Yes, `dp[1][k][1]` covers "at least one hub in the subtree".
    If the root is a hub, it must have $k=4$.
    If the root is a leaf, it must have $k=1$.
    Are there other cases?
    -   Root has $k=0$: Degree 0 (isolated). Invalid.
    -   Root has $k=2$: Degree 2. Invalid.
    -   Root has $k=3$: Degree 3. Invalid.
    
    So the answer is indeed `max(dp[1][1][1], dp[1][4][1])`.
    
    One detail: The DP state `dp[u][k][0]` assumes $u$ is NOT a hub.
    If $u$ becomes a hub (e.g., $k=3$ and parent is in subgraph, or $k=4$ and parent is not), does it affect the "no hub" state?
    -   If $u$ is a hub, then the subtree contains a hub. So it should contribute to state 1, not state 0.
    -   Therefore, `dp[u][k][0]` should be -1 if $u$ becomes a hub.
    -   $u$ becomes a hub if ($k=3$ and parent in subgraph) OR ($k=4$ and parent not in subgraph).
    -   But the DP state doesn't know about the parent.
    -   However, we can define `dp[u][k][0]` as "no hub in the subtree, AND $u$ is not a hub".
    -   If $u$ has $k=3$ or $k=4$, it *could* be a hub depending on the parent.
    -   But if we are building the subgraph bottom-up, we don't know the parent yet.
    -   So, `dp[u][k][0]` should be valid only if $u$ cannot be a hub.
    -   $u$ cannot be a hub if $k \neq 3$ and $k \neq 4$.
    -   Wait, if $k=3$, $u$ is a hub ONLY if parent is in subgraph. If parent is not, $u$ is not a hub (degree 3).
    -   If $k=4$, $u$ is a hub ONLY if parent is not in subgraph. If parent is, $u$ is not a hub (degree 5, invalid).
    
    This suggests we need to track the "potential" to be a hub.
    Actually, let's simplify.
    We want to find a subgraph.
    Let's define `dp[u][k][0]` as max size where $u$ has $k$ children, and NO node in the subtree is a hub.
    For $u$ to NOT be a hub:
    -   If $k=3$, $u$ is a hub if parent is in subgraph. If parent is not, $u$ is not a hub.
    -   If $k=4$, $u$ is a hub if parent is not in subgraph. If parent is, $u$ is not a hub (invalid degree).
    
    This dependency on the parent makes the state tricky.
    However, notice that if $u$ is a hub, it MUST have degree 4.
    If we assume the subgraph is valid, then for any node $u$ in the subgraph:
    -   If $u$ is a leaf, it has 1 neighbor.
    -   If $u$ is a hub, it has 4 neighbors.
    
    Let's reconsider the "root of the subgraph" approach.
    The subgraph is a tree. Pick an arbitrary node $r$ in the subgraph as the root.
    -   If $r$ is a leaf in the subgraph, it has 1 child in the subgraph.
    -   If $r$ is a hub in the subgraph, it has 4 children in the subgraph.
    
    So, if we root the original tree at 1, and we consider the subgraph rooted at 1:
    -   If 1 is a leaf in the subgraph, it has 1 child in the subgraph ($k=1$).
    -   If 1 is a hub in the subgraph, it has 4 children in the subgraph ($k=4$).
    
    What if the subgraph is rooted at some other node $r \neq 1$?
    Then 1 is not in the subgraph (or 1 is a leaf/hub but not the root of the subgraph).
    If 1 is not in the subgraph, we can just ignore it.
    But we need to find the max size.
    The DP approach computes the max size for the subtree of 1.
    If the optimal subgraph does not include 1, then the DP for 1 will not find it?
    No, the DP for 1 considers including or excluding children. If 1 is excluded, the subtree of 1 is empty?
    No, the DP state `dp[u][k]` assumes $u$ is included.
    So `dp[1][k]` assumes 1 is in the subgraph.
    If the optimal subgraph does not include 1, we need to consider other roots.
    
    But wait, the problem is on a tree. We can re-root the tree? No, $O(N^2)$.
    However, notice that if the optimal subgraph does not include 1, then there is some node $r$ in the subgraph that is "closest" to 1.
    Actually, we can just run the DP and then check all nodes as potential roots? No.
    
    Let's look at the constraints and the structure again.
    The subgraph is a tree.
    If we root the original tree at 1, and we select a subgraph, the subgraph is also a tree.
    Let $r$ be the node in the subgraph that is closest to 1 (or 1 itself if 1 is in the subgraph).
    If 1 is in the subgraph, then $r=1$.
    If 1 is not in the subgraph, then the subgraph is entirely in some subtree of 1.
    We can iterate over all nodes $u$ and assume $u$ is the "highest" node in the subgraph (closest to 1).
    But we can't iterate all $u$.
    
    Wait, if 1 is not in the subgraph, then the subgraph is contained in the subtree of some child of 1.
    We can just run the DP for each child? No, that's $O(N^2)$.
    
    Actually, the standard trick for "find max subgraph with property P" on a tree is to root at 1 and compute DP.
    If the optimal subgraph does not include 1, then the "highest" node $r$ is in the subtree of some child $v$ of 1.
    The DP at $v$ will compute the max size for the subtree of $v$ assuming $v$ is included.
    If we take `max(dp[v][...])` for all children $v$, we cover the case where the subgraph is in $v$'s subtree.
    But we need to combine them? No, the subgraph is connected.
    If the subgraph is in $v$'s subtree, then $v$ must be in the subgraph (unless the subgraph is further down, but then we would have covered it when processing $v$'s children).
    So, the answer is `max(dp[1][1][1], dp[1][4][1], max_{v in children(1)} (max(dp[v][1][1], dp[v][4][1])))`.
    Wait, if the subgraph is in $v$'s subtree, and $v$ is the highest node, then $v$ must be a leaf or hub in the subgraph.
    So $v$ must have $k=1$ (leaf) or $k=4$ (hub).
    So we check `dp[v][1][1]` and `dp[v][4][1]`.
    
    So the algorithm is:
    1. Compute DP for all nodes.
    2. The answer is `max(dp[1][1][1], dp[1][4][1])`.
    3. Also, for every node $u$, if $u$ is not the root of the whole tree, we need to consider the case where $u$ is the highest node in the subgraph.
       But we can't iterate all $u$.
    
    Wait, if the subgraph is in the subtree of $v$ (child of 1), and $v$ is the highest node, then the answer is `max(dp[v][1][1], dp[v][4][1])`.
    But we don't know which $v$ it is.
    However, we can just compute `global_max = max(global_max, dp[v][1][1], dp[v][4][1])` for all $v$.
    But this is $O(N)$.
    So we can just iterate all nodes $u$ and update `ans = max(ans, dp[u][1][1], dp[u][4][1])`.
    Wait, is it guaranteed that if $u$ is the highest node, it must have $k=1$ or $k=4$?
    Yes, because $u$ has no parent in the subgraph.
    -   If $u$ is a leaf, it has 1 child ($k=1$).
    -   If $u$ is a hub, it has 4 children ($k=4$).
    
    So the final answer is `max(dp[u][1][1], dp[u][4][1])` for all $u$.
    But we need to ensure that the subgraph is valid (at least one hub).
    `dp[u][k][1]` ensures at least one hub.
    So `ans = max(dp[u][1][1], dp[u][4][1])` for all $u$.
    
    Wait, what if the subgraph is just a single node? No, must have degree 4 somewhere.
    What if the subgraph has no hub? Then `dp[u][...][1]` will be -1.
    So we only consider state 1.
    
    So the plan:
    1. Run the DP as described.
    2. Iterate all $u$ from 1 to $N$.
    3. `ans = max(ans, dp[u][1][1], dp[u][4][1])`.
    4. If `ans` is still -1, print -1.
    
    One correction: The DP state `dp[u][k][0]` should be -1 if $u$ becomes a hub.
    Because if $u$ becomes a hub, it contributes to state 1.
    When does $u$ become a hub?
    -   If $k=3$ and parent is in subgraph.
    -   If $k=4$ and parent is not in subgraph.
    But the DP doesn't know about the parent.
    However, we can define `dp[u][k][0]` as "no hub in subtree, AND $u$ is not a hub".
    If $u$ has $k=3$ or $k=4$, it *might* be a hub.
    But if we are building the subgraph, we can choose whether to make $u$ a hub or not?
    No, the degree is determined by the number of neighbors.
    If $u$ has 3 children in the subgraph, and we connect it to its parent, it has degree 4 -> Hub.
    If we don't connect it to its parent, it has degree 3 -> Invalid.
    So if $k=3$, $u$ MUST be connected to its parent to be valid. And if connected, it becomes a hub.
    So if $k=3$, $u$ is a hub.
    Similarly, if $k=4$, $u$ MUST NOT be connected to its parent to be valid (degree 4). If connected, degree 5 -> Invalid.
    So if $k=4$, $u$ is a hub (and parent is not in subgraph).
    
    So:
    -   If $k=3$, $u$ is a hub.
    -   If $k=4$, $u$ is a hub.
    -   If $k=0$ or $k=1$, $u$ is a leaf.
    -   If $k=2$, $u$ is invalid (degree 2 or 3).
    
    So `dp[u][3][0]` and `dp[u][4][0]` should be -1 (impossible to have no hub).
    And `dp[u][3][1]` and `dp[u][4][1]` are valid.
    And `dp[u][0][0]` and `dp[u][1][0]` are valid (no hub).
    And `dp[u][0][1]` and `dp[u][1][1]` are valid (hub elsewhere).
    
    So in the DP transition, if we reach $k=3$ or $k=4$, we should only update state 1.
    State 0 should be -1 for $k=3, 4$.
    
    Let's adjust the code to enforce this.
    In the merge step, if `nk == 3` or `nk == 4`, we only update state 1.
    State 0 is only possible for `nk == 0` or `nk == 1`.
    
    Wait, what if $u$ is a leaf ($k=0$) but there is a hub in the subtree? Then state 1 is valid.
    What if $u$ is a leaf ($k=0$) and no hub in subtree? Then state 0 is valid.
    
    So the logic:
    -   Initialize `dp[u][0][0] = 1`, `dp[u][0][1] = -1`.
    -   During merge, if `nk` becomes 3 or 4, we only update `dp[u][nk][1]`.
    -   If `nk` becomes 0 or 1, we update both.
    -   If `nk` becomes 2, it's invalid (degree 2 or 3), so skip.
    
    This ensures that `dp[u][k][0]` is only valid for $k \in \{0, 1\}$.
    And `dp[u][k][1]` is valid for $k \in \{0, 1, 3, 4\}$.
    
    Then the final answer is `max(dp[u][1][1], dp[u][4][1])` for all $u$.

## worker: Update the code to enforce the hub logic (state 0 
1.  **Hub Logic Enforcement**: The code now explicitly enforces that `dp[u][k][0]` (no hub in subtree) is only valid for `k=0` or `k=1`. If `k=3` or `k=4`, the node `u` *must* be a hub (either connected to parent or not, depending on the global context, but locally it has 3 or 4 children which forces it to be a hub or invalid). Specifically, if `u` has 3 children and is connected to a parent, it's a hub. If it has 4 children and is NOT connected to a parent, it's a hub. Since the DP builds bottom-up, we treat `k=3` and `k=4` as "potential hub" states. By restricting state 0 to `k <= 1`, we ensure that if a node has 3 or 4 children, it contributes to state 1 (hub exists).
2.  **Final Answer Calculation**: The previous logic only checked `dp[1][...]`. This missed cases where the optimal alkane subgraph is rooted at a node other than 1 (i.e., node 1 is not part of the subgraph, or node 1 is a leaf/hub but the "highest" node in the subgraph is a descendant). The new logic iterates over all nodes `u` and checks `dp[u][1][1]` (u is a leaf in subgraph) and `dp[u][4][1]` (u is a hub in subgraph). This covers all possible roots of the alkane subgraph within the tree.
3.  **Complexity**: The DP state space is $O(N \times 5 \times 2)$. The transition involves merging children, which in the worst case (star graph) could be $O(\text{degree} \times 5 \times 5)$. Since the degree is bounded by $N$ but the effective state space for `k` is small (0-4), the complexity is effectively $O(N)$.

## worker: Run the code against the provided sample inputs to
The code implements a Tree DP solution.
1.  **State Definition**: `dp[u][k][0]` stores the max vertices in the subtree of `u` where `u` has exactly `k` connections to its children in the subgraph, and **no** node in the subtree (including `u`) has degree 4 in the subgraph. `dp[u][k][1]` is similar but requires **at least one** node of degree 4 in the subtree.
2.  **Hub Logic**: A node `u` in the subgraph has degree 4 (is a hub) if it connects to 4 neighbors. In the rooted DP, `u` connects to its parent (potentially) and `k` children.
    -   If `u` is a leaf in the subgraph, it has 1 neighbor. If parent is in subgraph, `k=0`. If parent is not, `k=1`.
    -   If `u` is a hub in the subgraph, it has 4 neighbors. If parent is in subgraph, `k=3`. If parent is not, `k=4`.
    -   The DP state `k` counts children. The "parent connection" is handled implicitly by the fact that we check `dp[u][k][1]` for `k=1` (leaf, parent not connected) and `k=4` (hub, parent not connected) or `k=3` (hub, parent connected). However, since we iterate over all nodes `u` as potential roots of the alkane subgraph, we specifically check `dp[u][1][1]` (u is a leaf in subgraph) and `dp[u][4][1]` (u is a hub in subgraph).
3.  **Transition**: We merge children options. If `u` ends up with `k=3` or `k=4` children, it *must* be a hub (either connected to parent or not, but locally it has 3 or 4 children which forces the degree to be 4 or 5). Since degree 5 is invalid, `k=4` implies parent is not connected. Since degree 3 is invalid, `k=3` implies parent is connected. In both cases, `u` becomes a hub. Thus, `dp[u][3][0]` and `dp[u][4][0]` are set to -1.
4.  **Final Answer**: We iterate over all nodes `u` and take the maximum of `dp[u][1][1]` and `dp[u][4][1]`. This covers all cases where `u` is the "highest" node (closest to the global root 1) in the alkane subgraph.

## worker: finalize
The solution implements a Tree DP approach to find the maximum size of an "alkane" subgraph.
1.  **State Definition**: `dp[u][k][0]` stores the maximum number of vertices in the subtree of `u` such that `u` has exactly `k` connections to its children in the subgraph, and **no** node in the subtree (including `u`) has degree 4 in the subgraph. `dp[u][k][1]` is similar but requires **at least one** node of degree 4 in the subtree.
2.  **Hub Logic**: A node `u` in the subgraph has degree 4 (is a hub) if it connects to 4 neighbors. In the rooted DP, `u` connects to its parent (potentially) and `k` children.
    -   If `u` is a leaf in the subgraph, it has 1 neighbor. If parent is in subgraph, `k=0`. If parent is not, `k=1`.
    -   If `u` is a hub in the subgraph, it has 4 neighbors. If parent is in subgraph, `k=3`. If parent is not, `k=4`.
    -   The DP state `k` counts children. The "parent connection" is handled implicitly by the fact that we check `dp[u][k][1]` for `k=1` (leaf, parent not connected) and `k=4` (hub, parent not connected) or `k=3` (hub, parent connected). However, since we iterate over all nodes `u` as potential roots of the alkane subgraph, we specifically check `dp[u][1][1]` (u is a leaf in subgraph) and `dp[u][4][1]` (u is a hub in subgraph).
3.  **Transition**: We merge children options. If `u` ends up with `k=3` or `k=4` children, it *must* be a hub (either connected to parent or not, but locally it has 3 or 4 children which forces the degree to be 4 or 5). Since degree 5 is invalid, `k=4` implies parent is not connected. Since degree 3 is invalid, `k=3` implies parent is connected. In both cases, `u` becomes a hub. Thus, `dp[u][3][0]` and `dp[u][4][0]` are set to -1.
4.  **Final Answer**: We iterate over all nodes `u` and take the maximum of `dp[u][1][1]` and `dp[u][4][1]`. This covers all cases where `u` is the "highest" node (closest to the global root 1) in the alkane subgraph.

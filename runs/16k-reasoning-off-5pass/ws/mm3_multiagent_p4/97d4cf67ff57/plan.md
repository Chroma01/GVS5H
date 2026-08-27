We need to find the maximum-sized induced subgraph (or any subgraph) of a tree that is a tree where every vertex degree is 1 or 4, and at least one vertex has degree 4. This is equivalent to picking a connected subset of edges/vertices in the original tree. Since the original graph is a tree, any connected subgraph is also a tree. So we want the maximum connected subgraph where internal vertices have degree exactly 4, leaves have degree 1, and at least one internal vertex (degree 4) exists.

We can root the tree arbitrarily (say at 1) and run a DP for each node computing best alkane subgraphs within the subtree that are connected and pass through that node. The challenge: a vertex can have up to original degree N-1, but in the subgraph its degree can be 1 or 4. So the DP must consider how many children of the node are included in the subgraph, and whether the node is a leaf (degree 1 in subgraph), a degree-4 node, or not included.

Because edges in a tree form a hierarchy, a connected subgraph containing a node v can only include a subset of v's children subtrees, and possibly the parent side. We can split DP into:
- dp[v][k][t] where k = number of edges from v to chosen children (0..min(4, children)), and t indicates the direction to parent (0 = not connected upward, 1 = connected upward meaning v's degree in the subgraph uses 1 edge to parent).
But degrees must be 1 or 4. So for a node in the subgraph:
- If t=1 (connected to parent), then the number of child edges used plus the parent edge must be either 1 (so v is leaf with only parent edge, meaning k=0) or 4 (so k=3). Because total degree in subgraph = k + (t ? 1 : 0) must be 1 or 4.
- If t=0 (not connected to parent, i.e., v is the root of the alkane subgraph), then total degree = k must be 1 or 4, and we also need overall the subgraph to contain at least one degree-4 node.

Goal: find max total vertices of any such subgraph. We can return -1 if no degree-4 node possible.

We will compute DP that returns the best size given constraints. Complexity O(N * degree^2) naive is too much. We need efficient merging. Since degree max 4, we can try DP states small.

Actually each node can have at most 3 children in a rooted tree (since we can pick one neighbor as parent). For a node to become degree 4, it would need 3 child edges + parent edge, i.e., exactly 3 of its children must be included. So at each node we just need to consider picking up to 3 children, combining their DP values.

Specifically, for each child u of v, we can either:
- Not include the edge (v-u), i.e., child subgraph is irrelevant.
- Include the edge, meaning the child must be connected to v, so the child's DP must have the "connected upward" state (t=1). In that case the child's subgraph must be a valid alkane-subtree with its own root being u, and u is connected to parent v.

Thus for each child we have two options: not include, or include with size f[u][connected]. Let w_u = size of best alkane-subtree in child u's subtree that is connected upward to v (i.e., u is included and its parent edge to v is part of subgraph). If we don't include, we contribute 0 vertices from that child.

Now at node v we need to choose a subset of children to connect, such that the degree constraint is satisfied.

Case 1: t=0 (v not connected to parent). Then degree = number of chosen children. Must be 1 or 4. Since max children = original degree - 1 <= N-1, but to be 4 we need exactly 4 chosen children. That implies v must have at least 4 children (since t=0). However total degree of v in the original tree is deg(v). Since we root it, parent doesn't count; children count = deg(v)-1. So for v to have degree 4 and not connect to parent, it needs at least 4 children. That is possible.

Case 2: t=1 (v connected to parent). Then degree = 1 + chosen children. Must be 1 or 4. So possibilities:
- chosen children = 0, giving degree 1 (leaf attached to parent).
- chosen children = 3, giving degree 4.

Thus for each node v, we can compute:
- best_down0 = maximum total vertices in a valid alkane-subtree that is entirely within v's subtree, connected upward to v, and v has degree 1 (i.e., leaf in subgraph) or degree 4 with t=1? Wait. For t=1, we have two subtypes: leaf (k=0) or degree 4 (k=3). Both are valid. So we need DP[t=1][k=0] and DP[t=1][k=3].

- best_subtree_rooted = best valid alkane-subtree that is fully inside v's subtree and is connected (i.e., t=0, k=1 or 4). This is the candidate for the whole answer (since we can treat v as root of the alkane). But also we might combine across parent side? Since any connected subgraph will have a highest node (closest to root). So the maximal alkane will be captured as some node v with t=0 (no parent edge). So we just need the global max over all v of DP[t=0][valid].

Thus we need to compute DP values for each v:
- f0_leaf[v] = best size for a connected subgraph inside v's subtree that includes v and is connected to parent (t=1) and v's degree is 1 (i.e., k=0, no children). This is simply 1 (just v alone) or maybe we can also not include any child subgraphs, but also we could include some child subgraphs that are detached? No, they must be connected via edges. If we connect to parent, we cannot include any other child subtrees because that would add degree >1. So f0_leaf[v] = 1.

- f1_deep[v] = best size for a connected subgraph inside v's subtree that includes v and is connected to parent, and v's degree is 4 (i.e., k=3). So we need to pick exactly 3 children of v to include, and for each included child we must use its DP with upward connection (f_up[child] defined below). For non-included children, we can ignore them. So we need to compute sum of top 3 values of w[child] (where w[child] is best size of a subgraph in child's subtree that includes child and is connected upward to v). The total size = 1 (v) + sum of w[child_i] for the three chosen children. But we also need the child's subgraph to be valid (must contain at least one degree-4 node somewhere). However we can have child's subgraph that is just child alone (leaf) which has no degree-4 node; that's allowed because overall subgraph may have degree-4 node elsewhere (e.g., v). The condition "there is at least one vertex of degree 4" applies to the whole subgraph. So we don't require each subtree to have a degree-4 node. Thus child can be a leaf-only subgraph (size 1) as long as global subgraph includes some degree-4 node.

Thus w[child] is defined as: the best size of a connected subgraph in child's subtree that includes child and connects upward to v (i.e., t=1). That subgraph can be either leaf (degree 1) or degree 4 (with exactly 3 of child's children). So w[child] = max( f0_leaf[child] (=1), f1_deep[child] ). Because child's degree can be 1 (if we don't include any of its children) or 4 (if we include 3 of its children). So w[child] = max(1, best_deep[child]) where best_deep[child] is the size of subgraph where child is degree 4 and connected upward.

But we also need to consider that child's subgraph may be empty (i.e., not include any vertex) - but we must include child to connect to v, so size >=1. So w[child] = 1 if no valid degree-4 subgraph exists in child's subtree that can be attached to v (i.e., child cannot become degree 4 because it doesn't have enough children with positive w values). However we can always choose the leaf case (size 1) regardless of children.

Thus we can compute for each node v:
- deep_up[v] = size of best subgraph that includes v, connects upward, and v has degree 4. This is:
   deep_up[v] = 1 + sum of largest 3 values of w[child] among children of v.
   If v has fewer than 3 children, deep_up[v] is impossible (i.e., -inf). Because we need exactly 3 children connected.

- leaf_up[v] = 1 (just v alone connecting upward). This is always possible.

- root_degree1[v] = best subgraph that is entirely within v's subtree, includes v, and v's degree is 1 (i.e., not connected to parent, but degree 1). This means we must pick exactly 1 child to connect to v, and the rest not. So root_degree1[v] = 1 + max_{child} w[child]. If no child, then impossible (since we need degree 1, but with no children degree would be 0). Actually if v has no children (leaf in original tree), then degree 1 not possible as root (because we need degree 1 but t=0 means only children contribute, so need at least 1 child). So root_degree1[v] invalid.

- root_degree4[v] = best subgraph that is entirely within v's subtree, includes v, and v's degree is 4. This means we need exactly 4 children connected (since t=0). So we need at least 4 children. So root_degree4[v] = 1 + sum of largest 4 values of w[child]. If v has fewer than 4 children, impossible.

The overall answer is max over all v of (root_degree1[v] or root_degree4[v]) that are valid and have at least one degree-4 vertex somewhere. But root_degree1[v] subgraph may have no degree-4 vertex; however overall we can also have degree-4 vertex somewhere else (in one of the child subgraphs). For root_degree1[v], v itself is degree 1, but we need at least one vertex of degree 4 in the whole subgraph. That could be inside one of the chosen child subgraphs. For root_degree1[v], we only include one child subtree (connected to v). That child subtree could have a degree-4 node (if we pick the child where deep_up[child] is used). Since w[child] = max(1, deep_up[child]), the best option for root_degree1[v] will automatically pick the child with maximal w[child], which could be deep_up[child] (degree 4) if exists, ensuring we have a degree-4 node. So we don't need extra check.

Similarly, for root_degree4[v], we sum top 4 w[child] values. If any of those w[child] come from deep_up[child] (i.e., child degree 4), then overall subgraph has degree-4 node. But it's also possible that none of them are deep_up (all are leaf 1). Then overall subgraph would have only v as degree-4 node (which is fine). So root_degree4[v] is always valid if it exists.

But we also need to consider subgraphs that might not be rooted at a node (i.e., the root of the subgraph could be somewhere in the middle of a tree path). However any connected subgraph of a tree has a unique node that is the "center" when considering parent direction; but if we consider the rooted tree, any connected subgraph that includes a node v and not its parent can be considered as rooted at v. So the DP should capture all possible subgraphs. Indeed any connected subgraph will have a node v such that the parent side is not included (i.e., the edge to parent is not in the subgraph). That node v can be the "root" of the subgraph in the rooted tree. So we only need to consider subgraphs where the root node is not connected to its parent. That's exactly the root_degree1 and root_degree4 cases.

Thus answer = max over v of max(root_degree1[v], root_degree4[v]) (where defined). If no such valid subgraph, output -1.

Now we need to compute w[child] values efficiently. Since w[child] depends on deep_up[child] which depends on w[grandchildren] etc., we can compute in post-order (DFS) from leaves upward. For each node v, we need w values of its children to compute its own deep_up and root_*. So we need to compute deep_up[v] and w[v] = max(1, deep_up[v]) (or maybe just store both). Actually w[v] needed by its parent: w[v] = max(1, deep_up[v]) because parent can either use v as leaf (size 1) or use v as degree-4 (size deep_up[v]) if v has enough children to become degree 4. So we define:
- best_up[v] = max(1, deep_up[v]) if deep_up[v] defined else 1. (If deep_up[v] impossible, best_up[v]=1).
We also need for root_degree1[v] and root_degree4[v] the values of best_up[child] for top 1 or 4 children.

Thus algorithm:
1. Build adjacency list.
2. Root tree at 1 (or any).
3. Perform DFS post-order to compute for each node:
   - Collect list of best_up[child] for all children.
   - Compute deep_up[v] = -inf initially.
     If number of children >= 3, deep_up[v] = 1 + sum of three largest best_up[child].
   - best_up[v] = 1 if deep_up[v] invalid else max(1, deep_up[v]).
   - Compute root1[v] = -inf initially.
     If children exist: root1[v] = 1 + max best_up[child] among children.
   - Compute root4[v] = -inf initially.
     If children >= 4: root4[v] = 1 + sum of four largest best_up[child].
   - Keep global answer = max(answer, root1[v], root4[v]).
4. After DFS, output answer if answer > 0 else -1.

Edge Cases:
- The condition "there is at least one vertex of degree 4" is satisfied if answer corresponds to a subgraph that includes at least one node of degree 4. In our DP, root1[v] uses a single child; if that child's best_up[child] is just 1 (leaf), then subgraph has no degree-4 node. However we could still have a degree-4 node deeper in that child's subtree if child is leaf? No, leaf cannot be degree 4. So root1[v] with child best_up=1 leads to subgraph with only v (degree 1) and the child (leaf). That subgraph has no degree-4 node. So it does not satisfy the condition. Similarly root4[v] might have all children best_up=1, but v itself is degree 4, so condition satisfied. So we need to ensure that we only consider subgraphs that have at least one degree-4 node.

Let's analyze root1[v] more carefully. root1[v] corresponds to a connected subgraph where v is degree 1 (connected to exactly one child). The subgraph includes v and that child's subtree (connected upward to v). For the whole subgraph to have a degree-4 node, we need at least one node of degree 4. This could be:
- v is degree 1, not degree 4.
- The child (call it c) is the connection point; c's degree in the subgraph is: it has edge to v plus maybe its own children. Since c is the root of its own attached subtree (connected upward to v), its degree in the whole subgraph is 1 (to v) + (number of its children included in its own subtree). If we use c's deep_up[c] (i.e., c is degree 4 in its own subtree) then c will have degree 1 (to v) + 3 = 4. That yields a degree-4 node (c). So if we choose child c where best_up[c] is from deep_up[c] (i.e., deep_up[c] exists and > 1), then overall subgraph has a degree-4 node. So root1[v] can be valid only if the max best_up[child] corresponds to a deep_up (i.e., child can be degree 4). However our DP currently selects the child with maximal best_up value, which may be either 1 (if all children have no deep_up) or >1 (if some child has deep_up). But we need to ensure that we only count root1[v] as a valid subgraph if it includes a degree-4 node. That means we should consider root1[v] only if the chosen child's best_up is > 1, i.e., deep_up[child] is valid and >1. But what if v itself can be degree 4? That's root4 case, handled separately.

Thus we need to refine root1[v] computation: we need to know the maximum best_up[child] that is >1 (i.e., deep_up[child] defined). If none, root1[v] is invalid (cannot be used). But could there be a degree-4 node somewhere deeper in child's subtree even if child is leaf? No, because child's subtree only includes child; if child is leaf (no children), deep_up[child] invalid. So the only way to have a degree-4 node in that whole subgraph is for the child to be a degree-4 node itself (connected upward to v). Because any other node deeper than child would be in child's subtree but the edge from child to v is included, so child's degree includes parent edge. That child would need to be degree 4, so it must have 3 other children. So indeed the degree-4 node must be the child (or possibly some node deeper if child's own subtree includes a degree-4 node that is not child). Wait, child's subtree can have a degree-4 node that is not child, e.g., child's child could be degree 4 with its own 3 children, and child's degree would be 2 (connected to v and to that child). That is allowed? Let's examine: Suppose we have a chain v - c - d, where d is degree 4 with three of its own children. If we include edges v-c and c-d and d's children, then degrees:
- v degree 1 (connected to c) -> leaf.
- c degree 2 (connected to v and d) -> not allowed (must be 1 or 4). So c would be degree 2, which violates the alkane condition. So we cannot have a node of degree 2 in the subgraph. Thus any node on the path from the root of the subgraph to a degree-4 node must have degree 1 or 4. If root v is degree 1, then its neighbor c must be either degree 1 (leaf) or degree 4. If c is degree 1, then subgraph ends there (c leaf). So c cannot be degree 2. Therefore the only way to have a degree-4 node deeper than the child is if the child itself is degree 4, because the child would have degree 1 (to v) + 3 = 4. So the degree-4 node must be the immediate neighbor of the root in a degree-1 root scenario. Similarly, if root v is degree 4, v itself is degree-4, or possibly a child could be degree 4? Let's think: root v degree 4, it connects to 4 children. Each child c_i is connected to v and possibly to its own children. For each child c_i, its degree = 1 (to v) + number of its own children included. This must be 1 or 4. So if c_i is not degree 4, it must have degree 1 (i.e., include no further children). So the only way to have a degree-4 node not equal to v is if some child c_i is degree 4. That's fine.

Thus the condition for root1[v] to be valid is that the chosen child c must be able to be degree 4 (i.e., deep_up[c] defined). So we need to compute:
- best_one_child_deep[v] = max (1 + deep_up[child]) over children where deep_up[child] defined.
If none, then root1[v] invalid.

Similarly, for root4[v] (v degree 4), we need to ensure that the subgraph includes a degree-4 node. It could be v itself (always degree 4) or any child being degree 4. Since v is degree 4, condition satisfied. So root4[v] is valid as long as we can select 4 children (i.e., at least 4 children exist). However there is nuance: if v has exactly 4 children and none of them can be degree 4 (i.e., all deep_up invalid), then subgraph includes v (degree 4) and each child leaf (degree 1). That's fine. So root4[v] is valid whenever v has >=4 children.

But also we might have subgraphs where v is degree 4 but we also could have some child also degree 4; that's allowed. So root4[v] valid if at least 4 children.

Now consider root4[v] when v has >4 children: we need to choose exactly 4 children to connect. The others are excluded. The size is 1 + sum of best_up[child] for top 4 children. That's fine. So root4[v] is defined if number of children >= 4. The condition for at least one degree-4 node: v itself is degree 4, so satisfied.

Thus answer = max over v of:
- If v has >=4 children: candidate = 1 + sum of top 4 best_up[child].
- Else candidate from root1: need a child with deep_up defined. Then candidate = 1 + deep_up[child] (size of child's subtree including child as degree 4). But careful: deep_up[child] includes child plus its three children subtrees. However we also include v (the root) which is degree 1 attached to child. The total size = 1 (v) + deep_up[child] (child + its subtrees). That's exactly 1 + deep_up[child]. But deep_up[child] = 1 + sum of top 3 best_up[grandchildren]. So total = 2 + sum of top 3 best_up[grandchildren]. However our earlier formula root1[v] = 1 + best_up[child] where best_up[child] = max(1, deep_up[child]). Since we restrict to child where deep_up[child] defined, best_up[child] = deep_up[child] (since deep_up[child] >= 2). So root1_candidate = 1 + deep_up[child]. So that's correct.

But we need to ensure that the child we pick is indeed the one that yields maximum total size, not necessarily the one with largest best_up, because we need deep_up defined. So we can compute for each node v:
- best_deep_child[v] = max over children of (deep_up[child]) if defined.
Then candidate1[v] = 1 + best_deep_child[v] (if best_deep_child[v] defined).

But also we might consider a subgraph where v is degree 4 and also includes a child that is degree 4 (or not). That's covered by root4.

Thus final answer is max of:
- For each v with at least 4 children: cand4[v] = 1 + sum of top 4 best_up[child].
- For each v where best_deep_child[v] defined: cand1[v] = 1 + best_deep_child[v].

Additionally, could there be a subgraph where the root node v has degree 1 but the child is not degree 4, yet some deeper node in child's subtree is degree 4? As argued earlier, that would create a node of degree 2 on the path (v-c-... ), because c would have degree 2 (connected to v and its child). But if that deeper node is degree 4 and c is degree 2, that's invalid. So not allowed. So the only possible degree-4 node in a degree-1 root scenario is the child.

Thus the DP is correct.

Now we need to compute best_up[child] = max(1, deep_up[child]) (where deep_up is size if child is degree 4 and connected upward). This is used for picking top children for root4.

Now we also need to consider subgraphs where the root is not the original root of the DFS (i.e., the "root" of the alkane is some node that is not the original root of the tree). In our DP, we treat any node v as potential root (t=0). That's fine.

Now complexity: For each node we need to find top 4 values among children best_up. Since degree can be large, we can do this by scanning children and maintaining top 4 using a small loop. O(N) total.

Implementation details:
- Use recursion or iterative stack due to N up to 2e5, recursion depth may cause recursion limit issues. Use sys.setrecursionlimit(1e6) or iterative post-order.

- Build adjacency list, parent array via BFS/DFS.

- Post-order: we can store order list from DFS and then process in reverse order.

- For each node v, iterate over its neighbors, skip parent, collect best_up[child] values into a list child_vals = [best_up[child] for child in children]. Also we need to know deep_up[child] values for best_deep_child.

Compute:
- If len(child_vals) >= 3: compute sum of top 3 values; deep_up[v] = 1 + sum_top3.
- else deep_up[v] = -inf (or None).

- best_up[v] = 1 if deep_up[v] is None else max(1, deep_up[v]) = deep_up[v] (since deep_up >= 4? Actually deep_up includes at least 4 vertices: v + 3 children (each at least 1). So deep_up >= 4. So best_up[v] = deep_up[v] if defined else 1.

- For best_deep_child[v]: we need to consider children where deep_up[child] defined. So we can store deep_up[child] values as we compute them (or we can compute after processing children). Since we process children first, we have deep_up[child] and best_up[child] available.

- best_deep_child_val = max(deep_up[child]) if any; else None.

- candidate1 = 1 + best_deep_child_val if best_deep_child_val defined.

- candidate4: if len(child_vals) >= 4: sum top 4 best_up[child] + 1.

- global answer = max(answer, candidate1, candidate4).

Edge Cases:
- For root of original DFS, parent is None; we treat it as not having a parent, but for computing deep_up and best_up for node v, we only consider children (neighbors except parent). That's correct.

- For leaf node (no children): child_vals empty. deep_up[leaf] = None. best_up[leaf] = 1. best_deep_child[leaf] = None. candidate1 invalid, candidate4 invalid. So leaf alone cannot be a valid alkane (needs degree 4). Good.

- For node with exactly 3 children: deep_up possible (choose all three). candidate4 not possible. candidate1 may be possible if some child has deep_up (i.e., child must have at least 3 grandchildren). That can happen.

- For node with exactly 4 children: both candidate4 and deep_up possible.

- For node with >4 children: candidate4 possible.

- Global answer may be None (no candidate). Then output -1.

Now we should double-check sample cases.

Sample 1:
N=9 edges: 1-2-3-4 chain plus 2-6,2-7,3-8,3-9. Let's compute manually.
Root at 1 maybe. Let's compute DP.

We'll test later.

But trust logic.

Potential issues:
- The DP only considers subgraphs where the root has degree 1 or 4. But what about subgraphs where the root has degree 1 but the child is leaf, and somewhere else (not on the path) there is a degree-4 node? Not possible because the subgraph is connected; if root is degree 1 and child is leaf, the subgraph is just an edge (two vertices). There's no other nodes. So can't have degree-4 node.

- Could there be a subgraph where the root node v has degree 4 but we also include a child that is degree 4, making the overall degree of v be 5? No, v's degree is number of children included, which is exactly the number of child edges we include. If we include a child c, we include edge v-c. v's degree counts that edge. If we also include c's children, v's degree does not increase. So v's degree is just number of child edges. So root4 uses exactly 4 children, each child may have its own subtrees, but v's degree remains 4. So it's fine.

Now we should test on sample 1 manually.

We'll implement a small script later, but for now let's reason.

Sample 1: tree structure:
1-2, 2-3, 3-4, 2-6,2-7,3-8,3-9.
Degrees: deg(1)=1, deg(2)=4 (neighbors 1,3,6,7), deg(3)=4 (neighbors 2,4,8,9), deg(4)=1, deg(6)=1, deg(7)=1, deg(8)=1, deg(9)=1.

The answer is 8, using vertices 1,2,3,4,6,7,8,9 (all except 5? Wait there is no 5). Actually the sample says vertices 1,2,3,4,6,7,8,9 (8 vertices). That's the whole tree except maybe missing something? Actually the tree has 9 vertices, we omitted vertex 5? Wait vertex 5 is not in the list. The edges: there is no vertex 5. Wait the tree has N=9, vertices 1..9. The edges listed: 1-2,2-3,3-4,4-5? No, they have 4-5? Let's check sample input 1:
9
1 2
2 3
3 4
4 5
2 6
2 7
3 8
3 9

Yes, there is an edge 4-5. So the tree is a path 1-2-3-4-5 with branches at 2 (6,7) and at 3 (8,9). So degree of 2 is 4 (neighbors 1,3,6,7). degree of 3 is 4 (neighbors 2,4,8,9). Vertex 5 is leaf attached to 4. The answer includes vertices 1,2,3,4,6,7,8,9 (8 vertices) and excludes vertex 5. That subgraph is a tree where 2 and 3 are degree 4, others degree 1. Indeed that works.

Our DP should capture that: root at 2 maybe. Let's compute.

Root at 1: we can compute.

Better to test after implementing.

But seems plausible.

Now sample 2:
Tree is a full binary tree of height 2: root 1 with children 2,3; 2 has children 4,5; 3 has children 6,7. All internal nodes have degree 3 (except leaves). No node has degree 4. So answer -1. Our DP: For any node to be degree 4, it needs 4 children (or 3 children + parent). Since max degree is 3, impossible. So candidate4 never exists. candidate1 requires a child with deep_up, but deep_up requires node to have 3 children (to be degree 4). No node has 3 children. So answer -1. Good.

Sample 3: answer 11. We'll test later.

Thus algorithm seems correct.

Now we need to be careful about memory and time.

Complexities: O(N) time and O(N) memory.

Now we should consider possible pitfalls:
- The DP definition of best_up[v] = max(1, deep_up[v]) ensures that if deep_up[v] is invalid, best_up[v]=1. This is correct for usage in parent's candidate4 (picking top 4 best_up). However we might also want to consider that best_up[v] could be 1 but maybe there is a better subgraph in v's subtree that is not connected upward (i.e., root at v). But that will be considered when v is the root of alkane (candidate1 or candidate4). For parent, we only need the best upward-connected subgraph (including v). So best_up is correct.

- The candidate1[v] uses best_deep_child[v] = max deep_up[child]. But we also need to ensure that the child's deep_up subgraph includes child as degree 4. That subgraph includes child and three of its children subtrees. However we also need to ensure that the edge from v to child is included, and v is degree 1. That's fine.

But is there any scenario where v has a child c with deep_up defined, but we also want to include some other child subtree that is not connected to c (i.e., as separate component)? No, because the subgraph must be connected. If we include any other child subtree, that would create another edge from v to that child, making v degree >1. So cannot. So candidate1 is correct.

Now we need to verify that candidate1 does not double count something incorrectly: deep_up[child] includes child and its three child subtrees. Adding v yields total vertices = 1 + deep_up[child]. This includes child and its descendants. That's correct.

Now we need to think about the case where v has degree 1 but the child is not degree 4; but the child could be degree 1 and its child (grandchild) is degree 4? That would cause child degree 2, invalid. So not allowed.

Thus candidate1 is correct.

Now we need to ensure that we don't miss subgraphs where the root node v is degree 4 and also includes a child that is degree 4, but we might want to choose a different set of 4 children that includes a child with deep_up to maximize size. Our candidate4 picks top 4 best_up values, which includes deep_up values for children. That's fine.

But there might be a scenario where the root v has degree 4, but one of the children is the parent of a deeper degree-4 node, but that deeper node is not the child itself. That would cause intermediate node of degree 2, invalid. So not allowed. So any degree-4 node must be either the root or one of the immediate children (connected directly to root). Therefore candidate4 covers all possibilities.

Now we need to ensure we didn't miss subgraphs where the root is not the original root but some internal node, and the root's degree is 4, but we might also need to exclude parent side. Our DP for node v excludes parent side (t=0). So if we want to consider subgraphs where the root is v and we don't include parent, we can treat v as root of the alkane. That's what candidate1 and candidate4 compute. So all possibilities covered.

Now we need to think about the case where the alkane subgraph is just a single vertex of degree 4? Not possible because degree 4 requires at least 4 edges, thus at least 5 vertices (including the central node). So minimal alkane is a "star" with central node degree 4 and 4 leaves: 5 vertices. But our DP will capture that: for a node v with at least 4 children (in original tree) and each child is leaf (best_up=1). Then candidate4 = 1 + 4*1 = 5. Good.

Now we should also consider subgraphs that are "chains" where all internal nodes have degree 4? Not possible because a node of degree 4 in a tree must have 4 neighbors; but a tree cannot have a node of degree 4 in a simple chain. So the alkane is a tree where internal nodes have degree 4, leaves degree 1. This is like a "4-regular tree" (except leaves). It's a rooted tree where each internal node has exactly 4 children (or 3 children + parent). In the context of our DP, any internal node (except the root) must have exactly 3 children (since one edge to parent). That's exactly the structure: a rooted tree where each non-root node has either 0 children (leaf) or 3 children (internal). The root has either 1 child (degree 1) or 4 children (degree 4). So the DP is consistent.

Thus the maximum alkane subgraph is essentially the maximum-size "4-ary tree" (each internal node has 4 children) embedded in the original tree.

Now we need to verify that our DP indeed computes the size of the maximum such embedded tree.

We need to ensure that we consider all possible embeddings. Since the original tree is arbitrary, we can choose any node as root of the embedded alkane, and we can choose any subset of children for each node as per degree constraints. The DP chooses the best combination of child subtrees for each node.

Potential issue: The DP might miss configurations where a node is degree 4 (connected to parent) but we also include a child that is degree 1 (leaf) and also another child that is degree 4 (i.e., we pick 3 children, some of which are leaves, some internal). That's allowed. The DP picks top 3 best_up values among children, which may include leaves (size 1) and internal subtrees (size >1). That's fine.

But we also need to ensure that the child subtrees themselves are valid alkane subtrees that are connected upward. For a child c, its best_up includes either leaf (size 1) or a degree-4 subtree (deep_up). That's correct.

Now what about a child c that is degree 4 (connected to v) but also includes its own child subtrees; those subtrees are themselves alkane subtrees with root c (connected upward). That's exactly deep_up.

Thus DP is correct.

Now we need to handle the case where deep_up[v] is defined but we might want to use a different combination of children than top 3 best_up values? Since best_up values are independent across children, picking top 3 yields maximum sum. So optimal.

Similarly for candidate4: pick top 4 best_up values.

Now we also need to consider the case where a node v has degree 1 (connected to parent) and we might want to include a child subtree that is not the best_up but maybe a combination that yields a degree-4 node somewhere else? But as argued, the only possible degree-4 node is the child. So we just need the child with maximum deep_up.

Thus DP yields optimal.

Now we need to ensure we handle large N efficiently.

Implementation steps:
1. Read N.
2. Build adjacency list (list of lists).
3. If N < 5, answer is -1 (since need at least 5 vertices). But we can still compute; DP will produce no candidate.
4. Perform iterative DFS to get parent and order:
   - Use stack = [(1, 0)] (node, parent). While stack: pop, record order, push children (neighbors not parent) with parent=node.
   - Actually for post-order we can do a stack for order: do a BFS/DFS to get parent and children, then process nodes in reverse order.
5. Initialize arrays: deep_up (size N+1) maybe store as -1 (invalid). best_up (size N+1) = 1 initially.
6. Also store list of children for each node? Not necessary; we can iterate adjacency each time, but that would be O(N^2) if we scan all neighbors each time. We need to store children lists: after DFS we can build children list for each node: children[v] = list of neighbors that are not parent[v]. This can be built during DFS.

Implementation details:
- Use recursion with sys.setrecursionlimit(1e6) maybe fine for N=2e5, but recursion depth may be up to N (if tree is a line). That may cause recursion depth error or stack overflow in Python. Safer to use iterative.

We'll do:
parent = [0]*(N+1)
order = []
stack = [1]
parent[1] = -1
while stack:
    v = stack.pop()
    order.append(v)
    for u in adj[v]:
        if u != parent[v]:
            parent[u] = v
            stack.append(u)

Now order is preorder. For post-order we process reversed(order).

Now we also need children list: can build after parent known: for each v (except root), add v to children[parent[v]].

Alternatively, we can just use adjacency and skip parent during DP; but we need to iterate children for each v. Since we have parent array, we can iterate over adj[v] and skip parent[v] each time. That's O(N + total edges) = O(N). Since each edge considered twice (once from each endpoint) total O(N). That's fine.

Thus we can compute DP without storing explicit children list.

Processing reversed order:
Initialize deep_up = [None]*(N+1) (or -inf). best_up = [1]*(N+1). best_deep_child_val = [None]*(N+1) maybe not needed; we can compute on the fly.

We also need to compute candidate1 and candidate4 for each node, update global answer.

Implementation details:
- For each v in reversed(order):
    child_vals = []  # best_up values of children
    deep_child_vals = [] # deep_up values of children (if not None)
    for u in adj[v]:
        if u == parent[v]: continue
        child_vals.append(best_up[u])
        if deep_up[u] is not None:
            deep_child_vals.append(deep_up[u])
    # compute deep_up[v]
    if len(child_vals) >= 3:
        # find top 3 values
        # we can sort or use nlargest from heapq
        # Since N up to 2e5, we can sort child_vals (size deg(v)) but total O(N log N) if we sort each list; that could be O(N log N) overall but still okay for 2e5? In worst case star tree: root has N-1 children, sorting O(N log N). That's fine. But we have many nodes with small degree. Simpler: use nlargest(3, child_vals) which is O(k log 3) ~ O(k). Use heapq.nlargest.
        top3 = sum(heapq.nlargest(3, child_vals))
        deep_up[v] = 1 + top3
        best_up[v] = deep_up[v]  # since deep_up >= 4 > 1
    else:
        deep_up[v] = None
        best_up[v] = 1

    # candidate1: need at least one deep_child_vals
    if deep_child_vals:
        max_deep_child = max(deep_child_vals)
        cand1 = 1 + max_deep_child
        ans = max(ans, cand1)
    # candidate4: need at least 4 child_vals
    if len(child_vals) >= 4:
        top4 = sum(heapq.nlargest(4, child_vals))
        cand4 = 1 + top4
        ans = max(ans, cand4)

After loop, if ans remains -inf (or 0), output -1 else ans.

Edge Cases:
- For candidate1, we used max_deep_child. But is it always optimal to pick the child with maximum deep_up? Yes, because we only include one child (the one that gives degree-4). The total size = 1 + deep_up[child]. Since we can't include any other children, picking the child with max deep_up yields max size. So correct.

- For candidate4, we need to ensure we pick exactly 4 children. If v has >4 children, we can choose any 4. The sum of top 4 best_up values is optimal. So correct.

Now we need to ensure that the DP's best_up for a child is indeed the best size of a subgraph that includes the child and is connected upward to parent. For leaf child, best_up=1 (just the child). For internal child, best_up = deep_up[child] (size of subgraph where child is degree 4). However there might be a scenario where the child can be degree 4 but we might want to not use all its capacity because maybe using a leaf is better for the parent's sum? Since best_up is max of 1 and deep_up, we always pick the larger. That's optimal for maximizing total size when we want to include that child. There's no penalty for including a larger subtree; bigger is better. So best_up is correct.

Now we need to verify with sample 1.

Let's simulate manually or code mentally.

But before that, we need to think about potential missing cases: The subgraph may have degree-4 nodes that are not the root or immediate children of root. For example, consider a node v with degree 4 (root) connecting to children a,b,c,d. Suppose child a is degree 4, connecting to its own three children (a1,a2,a3). In our DP, for child a, best_up[a] = deep_up[a] (size includes a + its three children). That will be included in the sum for root v. So the total includes a1..a3. That's correct.

Thus DP captures nested degree-4 nodes.

Now we need to think about the possibility of a subgraph where the root is degree 4 and one of its children is also degree 4, and that child also has its own children that are degree 4, etc. That's just a tree of branching factor 4. DP captures recursively.

Now we need to think about the case where the root is degree 1, but the child is degree 4, and that child has its own children (three). That's included via deep_up[child] which includes child + its three children. So total size = 1 + (1 + sum of top3 best_up of grandchildren). That's correct.

Now we need to consider the case where the root is degree 1 and the child is degree 4, but we might also want to include a leaf somewhere else? Not possible because root only has one child edge.

Now we need to think about subgraphs where the root is degree 1 and the child is degree 4, but the child's subtrees may also have degree-4 nodes deeper. That's allowed, captured by deep_up[child] (which recursively includes deep_up of grandchildren). So fine.

Now we need to think about subgraphs where the root is degree 4 and one of its children is degree 1 (leaf). That's fine.

Now we need to consider the case where the original tree is a star: central node with many leaves. The maximum alkane subgraph would be the central node plus 4 leaves (size 5). Our DP: For central node v, children are leaves. child_vals = [1]*deg(v). For candidate4: if deg(v) >= 4, pick top 4 = 4*1 = 4, plus v => 5. That's correct. candidate1: deep_child_vals empty (since leaves have deep_up None). So ans = 5.

Now consider a path of length 5: vertices 1-2-3-4-5. No node has degree >=4, answer -1. Our DP: For each node, children <=1, deep_up never defined, candidate4 never, candidate1 never (no deep_child). So ans -1.

Now consider a more complex tree where there is a node with degree 4 and also a child with degree 4, etc. DP will compute.

Now we need to ensure that we didn't miss subgraphs where the root is degree 1 but the child is not degree 4, yet there is a degree-4 node deeper in child's subtree but child's degree becomes 2 (invalid). As argued, not allowed.

Now we need to think about subgraphs where the root is degree 4 but the parent side is included (i.e., the subgraph includes the parent of the root). But that would mean the root is not the root of the subgraph; there is some higher node. In our enumeration, we consider any node as potential root (i.e., we consider subgraphs that do not include its parent). If there is a subgraph that includes the parent of v, then the root of that subgraph (in the sense of the node whose parent side is not included) is some ancestor of v, not v. So it will be considered when we process that ancestor. So we don't need to consider subgraphs where the parent is included but we treat v as root. So DP covers all.

Thus answer is max over all nodes of these candidates.

Now we need to verify sample 3.

But before that, we should think about potential pitfalls: The DP uses best_up[child] = max(1, deep_up[child]) which is monotonic: deeper subtrees larger. However there is a nuance: For candidate1, we require child to be degree 4. But what if the child can be degree 4 but we might also want to include a leaf child of the root to increase size? Not possible because root degree is 1, can't include more than one child. So we cannot add extra leaves.

Now, is there any case where root degree 1 and child is degree 4, but the child's subgraph deep_up[child] might be less than 1+max best_up[grandchild] (i.e., leaf) but we might want to choose leaf instead? But then root would be degree 1, child leaf, subgraph size 2, no degree-4 node, invalid. So we must pick child that can be degree 4. So candidate1 is correct.

Now, could there be a subgraph where root v has degree 4, but we choose 4 children, and one of those children is degree 1 (leaf) and the other three are leaves too, but we also have a degree-4 node somewhere else in the subtree of one of those leaves? Not possible because leaf has no children.

Thus candidate4 is correct.

Now we need to think about the case where the root v has degree 4, but we might want to include only 3 children and exclude the fourth to maybe allow the excluded child to be root of a separate alkane? Not relevant because we want a single connected subgraph.

Now we need to think about subgraphs where the root has degree 4, but we might want to include a child that is degree 4, and also include some grandchildren that are degree 4, etc. That's captured.

Now we need to verify the DP's ability to handle large N and depth.

Now we also need to ensure we treat negative infinite correctly: We'll use ans = -1 initially. When we find a candidate, we update ans = max(ans, cand). Since all candidate sizes are positive, we can just check if ans remains -1.

Implementation details for speed: Use local variables, avoid heavy overhead.

Now we need to think about the possibility that the answer is large (up to N). Since N up to 2e5, fits in int.

Now let's test the algorithm on sample 1 manually to ensure we get 8.

We'll simulate quickly.

Tree: adjacency:
1:2
2:1,3,6,7
3:2,4,8,9
4:3,5
5:4
6:2
7:2
8:3
9:3

Root at 1.

Parent[1] = -1.
DFS order (preorder) maybe: 1,2,3,4,5,8,9,6,7 (depending). But we process reversed.

Let's compute DP bottom-up.

Leaves: 5,6,7,8,9 (all have no children). For each leaf:
- child_vals empty.
- deep_up[leaf] = None.
- best_up[leaf] = 1.
- deep_child_vals empty => candidate1 not possible.
- candidate4 not possible.

Now node 4: children = {5} (since parent is 3). child_vals = [1] (best_up[5]=1). len=1 <3, deep_up[4]=None. best_up[4]=1. deep_child_vals: deep_up[5] is None, so none. candidate1: none. candidate4: len<4, none.

Node 8: leaf, same as above.

Node 9: leaf.

Node 6: leaf.

Node 7: leaf.

Now node 3: children = {4,8,9} (parent 2). child_vals = [best_up[4]=1, best_up[8]=1, best_up[9]=1] => [1,1,1]. len=3 => deep_up[3] = 1 + sum(top3) = 1+1+1+1 = 4? Wait sum of top3 = 1+1+1 =3, plus v => 4. So deep_up[3] = 4. best_up[3] = 4.
deep_child_vals: deep_up[4]=None, deep_up[8]=None, deep_up[9]=None => none.
candidate1: none.
candidate4: len=3 <4, none.

Now node 2: children = {3,6,7} (parent 1). child_vals = [best_up[3]=4, best_up[6]=1, best_up[7]=1] => [4,1,1]. len=3 => deep_up[2] = 1 + sum(top3) = 1+4+1+1 = 7? Wait top3 are 4,1,1 => sum=6, +1 =>7. So deep_up[2] = 7. best_up[2] = 7.
deep_child_vals: deep_up[3]=4 (valid), deep_up[6]=None, deep_up[7]=None => deep_child_vals = [4]. candidate1 = 1 + max_deep_child = 1+4 =5. candidate4: len=3 <4, none.

Now node 1: children = {2} (parent -1). child_vals = [best_up[2]=7]. len=1 <3, deep_up[1]=None. best_up[1]=1. deep_child_vals: deep_up[2]=7 => candidate1 = 1+7 =8. candidate4: len<4.

Thus ans = max(candidate1 across all nodes) = max(5 (node2), 8 (node1)) = 8. That's the answer. Good.

Now sample 2:

Tree: 1-2,1-3,2-4,2-5,3-6,3-7. Root at 1.

Leaves: 4,5,6,7.

Node 2: children 4,5. child_vals [1,1], len=2 <3, deep_up[2]=None, best_up[2]=1. deep_child_vals none. candidate1 none. candidate4 none.

Node 3: similar.

Node 1: children 2,3. child_vals [1,1], len=2 <3, deep_up[1]=None, best_up[1]=1. deep_child_vals: deep_up[2]=None, deep_up[3]=None => none. candidate1 none. candidate4 none. So ans remains -1. Good.

Now sample 3: We'll test after implementing code.

But we should also think about other possible tricky cases.

Potential tricky case: Node v has exactly 3 children, each of which can be degree 4. Then deep_up[v] = 1 + sum of top 3 best_up[child] = 1 + (deep_up[c1] + deep_up[c2] + deep_up[c3]). That's large. That's fine.

Potential tricky case: Node v has many children, but only some have deep_up defined. best_up[child] will be deep_up[child] if defined else 1. So picking top 4 best_up may include some leaves (1) if not enough deep_up children. That's fine.

Now we need to ensure that for candidate1 (v degree 1) we require a child with deep_up defined. But what if a child c has deep_up defined but we might also want to include a leaf from another child? Not allowed because v would have degree 2. So candidate1 only includes one child.

Now we need to think about subgraphs where v is degree 1 and the child is degree 4, but the child may have some children that are leaves and some that are degree 4. That's fine.

Now we also need to think about the possibility that the best alkane subgraph is not rooted at a node with degree 4 (i.e., root degree 1). In that case the root is degree 1 and its child is degree 4. That's candidate1. So we need to consider candidate1 for all nodes.

Now we also need to consider the case where the root is degree 4 and the root is a leaf in the original tree? Not possible because degree 4 requires 4 neighbors.

Now we need to think about the case where the root is degree 4 but the root is not the original root of DFS; we treat it as root for DP (t=0). That's fine.

Now we need to consider the case where the original root (1) may have a parent side (none). Our DP for node 1 will treat it as root (t=0). That's fine.

Now we need to consider the possibility that the best alkane subgraph includes the original root's parent side (which doesn't exist). So no issue.

Now we need to verify that the DP indeed yields the maximum size of any alkane subgraph.

We can attempt to prove correctness more formally:

Define a "good" subgraph (alkane) as a connected subgraph of the original tree where each vertex degree in the subgraph is 1 or 4, and at least one vertex has degree 4.

Observation: In any such subgraph, consider the node v that is farthest from the root of the original tree (or any node) that is not connected to its parent (i.e., the edge to its parent in the original tree is not in the subgraph). Since the subgraph is a tree, there is at least one node whose parent edge is not used; we can pick the one closest to the root (or any). That node v will have degree in the subgraph equal to the number of its children (in the original tree) that are included. Since the edge to parent is not used, the degree of v in the subgraph is exactly the number of incident edges to its children that are part of the subgraph. This must be 1 or 4 (since all vertices have degree 1 or 4). So v is a node where the subgraph is rooted at v (i.e., does not include parent). Conversely, for any node v, we can consider subgraphs that are rooted at v (i.e., include v and some of its descendants, not its parent). The size of the best such subgraph is exactly max(root1[v], root4[v]) as defined.

Thus the global optimum is the max over all v of these values.

Now we need to compute root1[v] and root4[v] efficiently using DP.

Now we need to ensure that root1[v] and root4[v] are correctly computed via DP.

We'll prove by induction on subtree size.

Induction hypothesis: For each node u, we have computed:
- best_up[u] = size of largest alkane-subtree that includes u, is connected to its parent (i.e., uses edge to parent), and satisfies degree constraints (so u's degree in that subgraph is 1 or 4). This subgraph is entirely within u's subtree.
- deep_up[u] = size of largest such subgraph where u has degree 4 (i.e., uses parent edge + exactly 3 child edges). If no such subgraph exists, deep_up[u] = None.

Base case: leaf (no children). Then best_up[leaf] = 1 (just the leaf). deep_up[leaf] = None (cannot have degree 4). This matches the only possible subgraph that includes leaf and connects upward: just the leaf itself (degree 1). This is optimal.

Inductive step: For internal node v with children c1..ck. Consider any alkane-subtree that includes v and connects upward. It must include exactly 0 or 3 of its children (since v's degree in subgraph must be 1 or 4, and one edge goes to parent). If it includes 0 children, then subgraph is just {v} (size 1). If it includes exactly 3 children, then for each included child ci, the edge v-ci must be present, and the subgraph must include a connected alkane-subtree in ci's subtree that includes ci and connects upward to v (i.e., includes edge ci-v). The size contributed by ci is best_up[ci] (the best such subtree). So the total size is 1 + sum_{i in S} best_up[ci] where S is a set of exactly 3 children. To maximize, we pick the 3 children with largest best_up values. So deep_up[v] = 1 + sum of top 3 best_up[ci] if k >= 3, else None. This matches DP.

Now best_up[v] = max(1, deep_up[v]) (if deep_up defined). This is correct because the best subgraph connecting upward either has v degree 1 (size 1) or degree 4 (size deep_up[v]), whichever is larger. Since deep_up[v] >= 4, best_up[v] = deep_up[v] when defined.

Now consider root1[v] (subgraph rooted at v with v degree 1). This means v is not connected to parent, and has exactly one child edge in the subgraph. The child must be connected upward to v, and the subgraph consists of v plus a connected alkane-subtree in that child's subtree that includes the child and connects upward to v. Moreover, to satisfy the global condition of having at least one degree-4 node, the child's subgraph must contain a degree-4 node (unless v itself is degree 4, but v is degree 1 here). As argued, the only possible degree-4 node in this configuration is the child itself (since the child will have degree 1 (to v) plus its own children; if it had degree 1, then no degree-4 node). So we need the child to be able to be degree 4 in its own upward-connected subgraph, i.e., deep_up[child] must be defined. Then the total size is 1 + deep_up[child]. To maximize, pick child with max deep_up[child]. So root1[v] = 1 + max_{child} deep_up[child] if any child has deep_up defined, else undefined.

Now consider root4[v] (subgraph rooted at v with v degree 4). v must have at least 4 children in the original tree (since it cannot use parent). We need to pick exactly 4 children to connect. For each chosen child, we can attach any upward-connected alkane-subtree (size best_up[child]). Since v itself is degree 4, the global condition of having a degree-4 node is satisfied regardless of child choices. So we need to maximize total size: pick 4 children with largest best_up values. So root4[v] = 1 + sum of top 4 best_up[ci] if k >= 4, else undefined.

Thus the DP correctly computes these values.

Now we need to ensure we didn't miss the case where the subgraph has v degree 4, but we also include a child that is degree 4, and that child's subgraph includes its own children, etc. This is captured because best_up[child] may be deep_up[child] which includes child's children.

Now the global optimum is the max over all v of root1[v] and root4[v] (where defined). Because any alkane subgraph has some node v where the edge to its parent is not used; v can be any node. The subgraph is rooted at v, and v's degree in the subgraph is either 1 or 4. So the size is exactly root1[v] or root4[v] (or possibly smaller if we choose suboptimal children, but we want max). So the DP finds the best possible for each v, and overall max is answer.

Thus algorithm is correct.

Now we need to implement efficiently.

Potential performance issues: For each node we need to find top 3 and top 4 values among child best_up. Since degree can be large, we can do this by scanning and maintaining top 4 using a small list.

Implementation approach: For each node, we can iterate over children, keep a list of top up to 4 values using a simple algorithm: maintain a list of size up to 4, insert each value if larger than smallest, etc. Or we can use heapq.nlargest which is O(k log 3) ~ O(k). Since total sum of degrees = 2(N-1), total time O(N log 4) = O(N). That's fine.

But we also need to compute max of deep_up[child] for candidate1. That's just max over children where deep_up[child] is not None. So we can track that.

Now we need to store deep_up as integer or None. Use -1 to indicate invalid. Since sizes are positive, we can use -1.

Initialize deep_up = [ -1 ] * (N+1). best_up = [1] * (N+1). ans = -1.

Processing reversed order:

for v in reversed(order):
    child_best = [] (list of best_up[child])
    max_deep_child = -1
    for u in adj[v]:
        if u == parent[v]: continue
        child_best.append(best_up[u])
        if deep_up[u] != -1:
            if deep_up[u] > max_deep_child:
                max_deep_child = deep_up[u]
    # compute deep_up[v]
    if len(child_best) >= 3:
        # sum of top 3
        # we can get top3 using nlargest
        top3 = sum(heapq.nlargest(3, child_best))
        deep_up[v] = 1 + top3
        best_up[v] = deep_up[v]
    else:
        deep_up[v] = -1
        best_up[v] = 1
    # candidate1
    if max_deep_child != -1:
        cand = 1 + max_deep_child
        if cand > ans:
            ans = cand
    # candidate4
    if len(child_best) >= 4:
        top4 = sum(heapq.nlargest(4, child_best))
        cand = 1 + top4
        if cand > ans:
            ans = cand

After loop, if ans == -1: print(-1) else print(ans).

Check sample 1: we got ans=8. Good.

Now test sample 2: ans stays -1. Good.

Now sample 3: we need to test.

We can also test some custom cases.

Edge Cases:

1. N=5 star: central node 1 connected to 2,3,4,5. Expect answer 5. Let's test:
Root at 1. Leaves have best_up=1. Node 1 child_best = [1,1,1,1]. deep_up[1] = -1 (since <3 children? Actually len>=3, yes 4 >=3, so deep_up[1] = 1 + sum top3 = 1+1+1+1=4. Wait deep_up[1] is size of subgraph where node 1 is degree 4 and connected upward to parent. But node 1 has no parent. So deep_up[1] is not used (since we only consider subgraphs where node connects to parent). However deep_up[1] being defined is okay for best_up[1] (though not used by parent). But candidate4 for node 1: len>=4, top4 sum = 4*1 =4, +1 =5. ans = max(candidate1 (none), candidate4) = 5. Good.

2. N=6: chain 1-2-3-4-5-6. No degree 4, answer -1. DP will produce no candidates.

3. N=7: root 1 with children 2,3,4,5,6,7 (6 children). Node 1 has 6 children. Deep_up[1] = 1 + sum top3 best_up[child] = 1+1+1+1=4? Actually each child best_up=1, top3 sum=3, +1 =4. candidate4 = 1 + sum top4 = 1+4=5. So answer 5. Indeed we can pick any 4 leaves.

4. More complex: A node v with children each having deep_up. For example, a complete 4-ary tree of height 2: root has 4 children, each child has 3 children (leaves). That's a tree where root degree 4, each internal child degree 4 (connected to parent + 3 children). This is a valid alkane. The total vertices = 1 + 4*(1+3) = 1 + 4*4 = 17? Wait each child includes itself + 3 leaves = 4 vertices. So total = 1 + 4*4 = 17. That's the full tree. Our DP should capture that: For each child, best_up = deep_up[child] = 1+3*1 = 4. For root, candidate4 = 1 + sum top4 best_up = 1 + 4*4 = 17. Good.

5. A more complex tree where the best alkane is not the whole tree but a subset. For example, a node v with 5 children, but only 3 of them can support deep_up (i.e., have at least 3 children each). The best may be to pick those 3 children as deep_up and one leaf as the 4th child to make root degree 4. Or maybe root degree 1 with a child that has large deep_up. DP will handle.

Now we need to ensure we correctly compute best_up for children. For child with deep_up, best_up = deep_up. That's fine.

Now consider the case where a node v has 3 children, each with deep_up values large, but we also have a 4th child that is a leaf. The best root4 picks top 4 best_up values; but we only have 3 children. So root4 not possible. However we could have root1 (v degree 1) picking the best child deep_up. That's candidate1. So DP will pick best.

Now we need to think about the case where v has exactly 4 children, but we might want to exclude one child to make root degree 1? That's candidate1. But candidate1 uses max deep_child, which may be less than picking 3 children and a leaf? Actually root4 uses top 4 best_up; root1 uses 1 + deep_up[best_child]. Compare sizes: root4 includes 4 children (including possibly leaf) plus v. root1 includes only one child (which must be deep_up) plus v. Usually root4 will be larger because includes more vertices. So candidate4 will be considered.

Now we also need to consider the case where v has >4 children, but we might want to pick only 3 children that have deep_up and a leaf, but we have to pick exactly 4 children. So we must pick 4 children; picking top 4 best_up yields max.

Now we also need to consider the case where v has exactly 3 children, each with deep_up, and we also want to consider the possibility that the best alkane is rooted at v with v degree 4, but we need 4 children; not possible. So only candidate1.

Thus DP seems correct.

Now we need to test sample 3.

Sample 3 input:

15
8 5
2 9
1 12
6 11
9 3
15 1
7 12
7 13
10 5
6 9
5 1
1 9
4 5
6 14

Let's parse edges:

1: edges: (15,1) => 15-1; (5,1) => 5-1; (1,9) => 1-9; (1,12) => 1-12
2: (2,9) => 2-9
3: (9,3) => 3-9
4: (4,5) => 4-5
5: (8,5),(10,5),(5,1),(4,5) => 5 connected to 8,10,1,4
6: (6,11),(6,9),(6,14) => 6 connected to 11,
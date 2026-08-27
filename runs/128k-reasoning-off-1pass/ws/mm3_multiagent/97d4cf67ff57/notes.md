
## ideation
**Core difficulty**  
We need a connected subgraph of a tree that itself is a tree where every vertex has degree exactly 1 or exactly 4, and there is at least one degree‑4 vertex (i.e. a “branching” vertex). The subgraph can be any induced connected subset, not necessarily a whole rooted subtree of the original tree – we may discard some incident edges. However, because the original graph is a tree, any connected subgraph is also a tree, and once we decide which vertices belong to the subgraph, the edges are forced (the unique path between any two kept vertices lies entirely inside because the original is a tree).

Thus the problem is: choose a connected set of vertices `S` that induces a tree where:
* For every `v ∈ S`, its degree inside the induced subgraph is either 1 (leaf) or 4.
* `S` contains at least one vertex of degree 4.

We want to maximise `|S|`.

**Candidate approaches**

1. **Tree DP with “state” describing how the kept part attaches to the parent.**  
   Root the tree arbitrarily (e.g. at 1). For each node `u`, we compute DP values that describe the best alkane‑shaped connected subgraph *inside* the subtree of `u` that contains `u` and respects certain degree constraints on `u` (0 children attached, 1 child attached, up to 3 children attached, possibly also the parent). The number of possible states is small because the degree of `u` in the subgraph is at most 4, and one incident edge may be the parent edge.  

   Possible states for a node `u`:
   * `leaf[u]` – `u` is a leaf in the subgraph (degree 1) and the edge to its parent is the only incident edge. The children are all excluded.
   * `inner0[u]` – `u` is an internal vertex (degree 4) but the edge to its parent is *not* used. `u` is only connected to up to 3 child branches; we still may or may not use all 3. Actually the degree 4 must be satisfied, so if we don't use the parent edge we need *exactly* 3 child branches.
   * `inner1[u]` – `u` is an internal vertex (degree 4) and the edge to its parent *is* used, so we need exactly 3 child branches as well.
   * `unused[u]` – no subgraph (size 0) – not needed for final answer.

   But the situation is simpler: we only need to know, for a node, the best size of a valid partial alkane that **uses the parent edge** (i.e. the part is attached to the parent) and respects that `u`'s degree in the partial subgraph is either 1 (leaf) or 4 (internal). If we also know the best size when the parent edge is *not* used (i.e. the partial alkane is a complete alkane inside the subtree, not attached upward), we can use that to combine children.

   Let's formalise:  
   For each node `u`, we compute:
   * `dp0[u]` – best size of a connected subgraph `X` contained in the subtree of `u` such that:
        - `X` is a valid alkane *or* a single vertex? Actually `X` may be empty?  
        - The parent edge is **not** included. This subgraph may be a complete alkane (contains at least one degree‑4 vertex) or may be just a single vertex (which is not an alkane). But we need to know this because when we attach `u` as an internal node to its parent, we need children that themselves are complete alkanes (or perhaps just a leaf) and we have to take the best three.
   * `dp1[u]` – best size of a connected subgraph `X` contained in the subtree of `u` such that:
        - `X` is connected, contains `u`.
        - The edge to the parent is part of `X`.
        - Inside `X`, the degree of `u` is 1 (leaf) or 4 (internal), while all other vertices satisfy the degree rules. Moreover, `X` may be a single vertex (just `u`, considered as a leaf for the parent). If `u` is internal (degree 4), then it must have exactly three child sub‑branches (each being a subtree attached to one of its children), and the rest of the tree (other children) must be excluded.

   The DP transition:
   For a node `u` with children `v1, v2, …, vk`. We want to compute `dp1[u]`. There are two possibilities for the degree of `u` in the subgraph:
   * **u is a leaf** (degree 1). Then the parent edge is the only incident edge, and none of the child subtrees can be used. So `dp1[u] = 1`.
   * **u is internal** (degree 4). Then we need exactly three child subtrees, each providing a `dp1[child]` (i.e., the child is connected to `u` via the edge (u, child) and the child's degree in the partial subgraph is 1 or 4). The other children are excluded. The size contributed by the three children is the sum of their `dp1[child]`. Therefore `dp1[u] = 1 + sum of best three `dp1[child]` values among all children. If `u` has fewer than three children, this case is impossible (we cannot have degree 4). So we keep the maximum of the two cases (leaf or internal). If the internal case is impossible, we just have leaf case = 1.

   Now `dp0[u]` – a subgraph not using the parent edge. This subgraph can be:
   * **Empty** (size 0) – we can always take nothing.
   * **A single vertex** (size 1) – just `u` alone, not an alkane but allowed as a building block.
   * **A complete alkane** inside the subtree, which means the whole subgraph is attached to `u` (since `u` is the topmost node) and has at least one degree‑4 vertex somewhere. Because the parent edge is not used, `u`'s degree inside the subgraph is either 1 (if `u` is a leaf of the alkane) or 4 (if `u` is an internal vertex). Both are allowed. So we can think of `dp0[u]` as the best size of a subgraph that is connected, includes `u` (or maybe we allow not to include `u` at all, but we also need the value when we later attach a parent). Actually for the purpose of combining with the parent, we never need a value that does not contain `u` because the edge to the parent is not used. However, we might need a value for the case where we do not use `u` at all (i.e., the best alkane is completely in some child's subtree). That will be captured by taking max over children of their `dp0` when we compute the final answer. So `dp0[u]` can be defined as the best size of a subgraph (alkane or just a vertex) inside the subtree of `u` **that is connected and includes `u`** but does not use the parent edge. Let's call it `best_containing_u_no_parent`. This is what we need when `u` is a child of its parent and we consider the scenario where `u` is a leaf of the alkane attached to the parent: then we need `u` to be a leaf, which corresponds to `dp0[u] = 1`. Wait, if `u` is a leaf in the final alkane, then the edge to its parent is used, so the subgraph attached to the parent must be of type `dp1[u]` with degree 1 at `u`. That's already covered by `dp1[u] = 1` (leaf case). So we never need `dp0[u]` for leaf case.  

   But we need `dp0[u]` to combine as a child of its parent when the parent is internal. In that case the child must be a valid alkane (i.e., a complete alkane) because the parent expects the child's contribution to be a sub‑alkane with its own degree‑4 vertices, not just a chain. Wait, is that correct? Let's check: Suppose we have a parent node `p` that is internal (degree 4) and we attach three child sub‑branches. Each child branch is a subtree that contains that child vertex `c`. Inside that branch, the degree of `c` (with respect to the whole alkane) is 1 (since it connects only to `p`) or maybe 4 (if `c` itself is an internal vertex). But the branch must be a valid alkane **except possibly missing the parent edge**? The whole subgraph after adding `p` and the three branches will be a tree where every vertex satisfies the degree constraints. In particular, inside the branch (excluding the edge to `p`), the vertices other than `c` must already satisfy the constraints. `c` will have degree 1 (just to `p`) or degree 4 (if it also has three child branches). If `c` has degree 4, then it must be an internal node with exactly three child branches, which are sub‑branches that themselves are valid (i.e., each child branch is a valid alkane or just a leaf). So the structure recurses: each child of an internal node must be a valid alkane attached via a leaf of the child.

   Therefore, the DP state `dp1[u]` exactly captures the best size of a partial alkane that includes `u` and uses the edge to its parent (if any). For a leaf `u` in the final alkane, `dp1[u] = 1`. For an internal `u`, `dp1[u] = 1 + sum of best three dp1[child]`. This works recursively because each child that is used will also have its parent edge used, so it uses its own `dp1` value. The recursion stops at leaves of the original tree (or when we don't have enough children to become internal). So we don't need `dp0` at all? Let's examine the condition that the whole alkane must have at least one degree‑4 vertex. In the DP, if a node is internal (degree 4) we count it. If a node is leaf, it doesn't count. So the final answer we need to output is the size of the largest alkane (complete). In the DP, an alkane is a connected subgraph where the topmost node (the one connected to the rest of the original tree via its parent edge) may be either a leaf or internal. But we need to ensure that the whole subgraph contains at least one internal node (degree 4). In our DP definition, `dp1[u]` includes both possibilities (leaf and internal) for the role of `u` in the subgraph. So the final answer should be the maximum `dp1[u]` over all `u` where the chosen configuration is internal somewhere. However, we might accidentally pick a configuration where the whole subgraph is just a single vertex (size 1) or a chain where no vertex is internal. Is a chain allowed? In a chain, the internal vertices have degree 2 in the subgraph, which violates the condition (must be 1 or 4). So any valid alkane must have at least one degree‑4 vertex, which means that the DP must have at least one internal node in the chosen configuration. In our DP, if we pick `dp1[u]` and it corresponds to the leaf case (just size 1), that would be invalid as a final answer unless we have a larger structure with internal nodes somewhere else. But we are taking max over all `u`, and any internal node will have `dp1[u] >= 5` (since it includes itself plus at least three children each of size at least 1). So a chain is not possible because an internal node needs three child branches. But could we have a subtree that is like a "broom" where the central node is internal and all three branches are just leaves? That would be a valid alkane: the central node degree 4, each leaf degree 1. That has size 1 + 3 = 4. Wait, we need at least one degree‑4 vertex, yes. So size 4 is possible. So any DP state where we pick the internal case for some node will produce a valid alkane. However, the DP as described might also produce a "partial" alkane that is attached to a parent (i.e., the root of the DP) where the root node itself is a leaf. That would correspond to a branch that is a chain ending at the root, but that chain would have internal vertices of degree 2, which is not allowed. Wait, our DP's internal case requires the node to have exactly three child branches that are themselves valid partial alkanes (with parent edge used). Those child branches could be just a leaf (size 1). If a child branch is a leaf, that means the child vertex is a leaf in the final alkane. That's fine. So the DP builds trees where every non‑leaf vertex has exactly three child branches (except the root which may have a parent). So the shape is a "full ternary tree" where each internal node has exactly 3 children (ignoring the parent direction). This matches the definition of an alkane: every vertex degree 1 or 4. In a rooted tree, a vertex of degree 4 can have 1 parent + 3 children (if it's not the root) or 4 children (if it's the root). Actually, if the root is internal, it has degree 4, meaning it must have 4 children (since no parent). If the root is a leaf, it has degree 1, meaning it has no children. Wait, careful: In the final alkane (unrooted), each vertex has degree 1 or 4. If we root it arbitrarily, a degree‑4 vertex may have 1 parent edge and 3 child edges (if not the root) or 4 child edges (if it is the root). In our DP, we treat the edge to the parent as a possible connection. For a node that is internal in the alkane, it must have degree 4. In the rooted view, if it is not the overall root, it has exactly 3 children (since the parent edge accounts for one of the 4). If it is the overall root (i.e., we are considering the whole alkane as a subtree not attached to anything), then it has no parent edge, so it must have 4 children. However, our DP `dp1[u]` always assumes the edge to the parent is used (or we are computing a value for a node that is attached to its parent). The final alkane is a connected subgraph that is not attached to any parent; it is the whole thing. So we need a DP state for a node that is the "top" of the alkane and has no parent edge. Let's call it `dpRoot[u]`. Then we can compute the answer as the max of `dpRoot[u]` over all `u`, provided the result is not just a single vertex (i.e., size >= 4? Actually minimum size of an alkane is 4? Let's check: a tree where one vertex has degree 4 and the other 4 vertices are leaves: that's 5 vertices. Wait, the central node degree 4, so it connects to 4 leaves. That's 1 + 4 = 5 vertices. But is there a smaller alkane? Could we have a tree where one vertex has degree 4 and some of the other vertices have degree 4 as well? The smallest possible is 5: the star with one internal node of degree 4 and 4 leaves. Are there any alkanes with fewer than 5 vertices? No, because each vertex has degree 1 or 4, and the sum of degrees is 2*(V-1). If we have I internal vertices (degree 4) and L leaves (degree 1), then V = I + L. The sum of degrees = 4I + L = 2V - 2 = 2(I + L) - 2 = 2I + 2L - 2. So 4I + L = 2I + 2L - 2 => 2I = L - 2 => L = 2I + 2. Then V = I + L = I + 2I + 2 = 3I + 2. For I = 1, V = 5. For I = 2, V = 8, etc. So the smallest alkane has 5 vertices. So any valid alkane has at least 5 vertices. However, note that the problem statement says "Every vertex has degree 1 or 4, and there is at least one vertex of degree 4." So V must be at least 5. So we can safely ignore configurations with size < 5. But our DP might produce a value of 1 (leaf case). That's not a valid alkane. So when we compute the answer, we must ensure that the configuration includes at least one internal node. In the DP, any configuration that picks the internal case for at least one node will have size >= 5 (since internal node needs 3 children, each child at least size 1). So we can just take the maximum over all DP states that correspond to a valid alkane.

But we need a DP that can represent both cases: a node that is the top of the alkane (no parent) and a node that is attached to a parent. For the attached case, we already have `dp1[u]`. For the root case, we need a similar computation but without requiring the parent edge. Let's define:

* `dp0[u]`: best size of a connected subgraph inside the subtree of `u` that **does not use the parent edge** and is a **valid alkane** (i.e., has at least one internal node) **or** is just a single vertex? Actually we need to be careful: when we attach a child to its parent, the child must be a valid alkane (including the possibility that the child is just a leaf? No, if the child is a leaf in the final alkane, then the edge to the parent is the only edge for that child. In the DP for the child, that corresponds to the case where the child is a leaf and the parent edge is used. That's `dp1[child] = 1`. So the child can be a leaf. So when we combine three children to form an internal node, we are picking `dp1[child]` values, not `dp0[child]`. So we don't need `dp0` for the combination. However, for the root of the alkane, if the root is internal, it needs 4 children (since no parent). If the root is a leaf, then the alkane is just a single vertex? But a single vertex has degree 0, which is not allowed (must be 1 or 4). So a leaf root would imply the whole alkane is just that vertex, but that violates the degree condition. Actually, if the root is a leaf, then it has degree 1, meaning it must be connected to something. But since it's the root of the alkane, there is no parent. So a leaf root would be impossible for a connected subgraph with no other vertices. So the root must be internal (degree 4) if the alkane is non‑empty. Wait, could the alkane be a path? No, because internal vertices of a path have degree 2. So the only way to have a leaf root is if the alkane is just a single vertex, which is invalid. So the root of the alkane must be internal (degree 4). Therefore, the minimal alkane is a star with center degree 4 and 4 leaves. So the root must have exactly 4 children in the rooted view (if we root at an internal node). But we can also root at a leaf? If we root at a leaf, then that leaf has degree 1 (its parent is the rest of the tree). The parent must be internal (degree 4) and have 3 other children (since one edge goes to the leaf). So the structure is still the same. So in any rooted representation, the root of the alkane could be a leaf (if we choose the root to be a leaf of the alkane) or an internal node. But for the purpose of DP, it's easier to root the alkane at an internal node. However, we don't know which node is the root. So we need a DP that can handle both possibilities.

One approach: For each node `u`, compute two values:
* `up[u]`: best size of a valid alkane that is entirely inside the subtree of `u` (with respect to the original tree's root) and is attached to `u` via the edge to its parent (i.e., the parent edge is part of the alkane). This is the same as `dp1[u]` defined earlier.
* `down[u]`: best size of a valid alkane that is entirely inside the subtree of `u` and **does not** use the parent edge. This is the best alkane that is a complete alkane inside `u`'s subtree, with `u` possibly being a leaf or internal. Actually, for the purpose of the final answer, we just need the maximum over all `down[u]` where the alkane is entirely within `u`'s subtree (i.e., the root of the alkane is somewhere in that subtree). But we can also get that by taking the max over all `up[child]` for children of `u`? Not exactly. If the alkane is entirely within a child's subtree, then `down[u]` should be at least `down[child]`. But if the alkane includes `u` as a node, then we need to consider the case where `u` is the topmost node (no parent). Let's define `best[u]` as the best size of an alkane that is entirely within the subtree of `u` (including possibly `u` itself). Then we want the answer as `max_{u} best[u]`. And we can compute `best[u]` by considering:
* The best alkane entirely in some child subtree: `max_{v child of u} best[v]`.
* An alkane where `u` is the root (i.e., the alkane includes `u` and possibly some of its descendants). This is like `dpRoot[u]`.

But maybe we don't need to separate `down` and `best`. We can just compute `dp1[u]` (attached to parent) and then also compute `dpRoot[u]` (not attached to parent). Then the answer is the max over all `dpRoot[u]` (and also possibly over `dp1[u]` for the root of the original tree? But `dpRoot` is the natural one). Let's think carefully.

**Detailed DP design**

We root the original tree at 1. For each node `u`, we process its children. We need to compute for each node `u`:
1. `leaf[u]`: the best size of a partial alkane that includes `u` and uses the parent edge, with `u` being a leaf (degree 1). This is simply 1. Actually we don't need to store it separately; it's just 1.
2. `inner[u]`: the best size of a partial alkane that includes `u` and uses the parent edge, with `u` being internal (degree 4). This requires `u` to have at least 3 children, and we pick the best 3 children to attach. For each child `v`, we need the best partial alkane that includes `v` and uses the edge (u,v). That is exactly `dp1[v]` (which we compute recursively). So `inner[u] = 1 + sum of top three dp1[v]` over children. If `u` has fewer than 3 children, `inner[u]` is impossible (or -infinity).
3. `dp1[u] = max(leaf[u], inner[u])`. Since leaf is always 1, `dp1[u]` is at least 1. But we should be careful: if `inner[u]` is impossible, then `dp1[u] = 1`. However, we also need to consider the possibility that `u` is a leaf in the original tree (no children). Then `dp1[u] = 1`.

Now, for a node that is the root of the alkane (no parent), we need a similar computation but without the parent edge. If the root is internal, it must have degree 4, so it needs 4 children. If the root is a leaf, then the alkane is just a single vertex, which is invalid (no internal vertex). So for a valid alkane, the root must be internal. Therefore, for each node `u`, we can compute `dpRoot[u]` = best size of an alkane entirely within the subtree of `u` where `u` is the topmost node (i.e., the edge to its parent is not used). Since `u` is the top, if `u` is internal, it needs 4 children. So `dpRoot[u] = 1 + sum of top four dp1[v]` over children `v`. If `u` has fewer than 4 children, then `dpRoot[u]` is impossible. However, note that `u` could also be a leaf in the alkane? No, as argued, a leaf root would mean the alkane is just `u`, which is invalid. So we only consider the internal case for the root. But wait, is it possible that the alkane is entirely within a child's subtree, and `u` is not included? That would be captured by the max over children of `dpRoot[child]` or something. So for each node `u`, we can compute the best alkane entirely within its subtree as:
   `best[u] = max( dpRoot[u], max_{v child of u} best[v] )`.
   And the final answer is `max_{u} best[u]`.

But is it sufficient to only consider `dpRoot[u]` where `u` is internal? What about the case where the alkane is rooted at a node that is a leaf in the original tree? That node would be a leaf in the alkane as well, but then the alkane would have to extend into its parent (which is not in the subtree). So if we are considering alkanes entirely within the subtree of `u`, then the root of the alkane cannot be a leaf in the original tree unless the alkane is just that leaf (invalid). So yes, the root of the alkane must be an internal node in the original tree (or at least have degree at least 4 in the original tree? Not necessarily; it could have degree 2 in the original tree but we only pick 4 of its children? Wait, in the original tree, a node can have arbitrary degree. For it to be internal in the alkane, it needs exactly 4 incident edges in the alkane. If it has fewer than 4 children in the original tree, it cannot be internal. So `dpRoot[u]` is only possible if `u` has at least 4 children. So that's fine.

But is it correct to only consider `dpRoot[u]` as defined? Let's test with a simple case: a star with center node 1 and leaves 2,3,4,5,6,7 (degree 6). The best alkane is to take the center and any 4 of its leaves, size 5. According to our DP: root at 1. Children are 2..7. For each child leaf, `dp1[child] = 1` (since they have no children). Then `dpRoot[1] = 1 + sum of top four dp1[child] = 1+4 = 5`. `best[1] = 5`. Answer 5. Correct.

What about a path? The DP will not find any internal node with at least 3 children, so all `dp1` values are 1. `dpRoot[u]` will be impossible for all `u` because they have at most 1 child. `best[u]` will be 0 or something. We should output -1. Our DP would produce max 0? But we need to output -1 if no alkane exists. So we need to check if the maximum is at least 5 (or more precisely, at least 5, because the smallest alkane has 5 vertices). So we can set answer = max over all `best[u]`. If answer < 5, print -1. But wait, could there be an alkane of size exactly 4? No, as proven. So we can check if answer >= 5. However, our DP might produce a value like 4 if we consider a node with 3 children and each child is a leaf? That would be `dpRoot[u] = 1 + 3 = 4`? No, `dpRoot` requires 4 children. So 4 is not possible from `dpRoot`. But what about `best[u]` from a child? If a child has 3 children, `dpRoot[child] = 1+3=4`? Wait, if a node has 3 children, it can be internal with 3 children only if it also uses the parent edge. That's `dp1[child] = 1+3=4`. But `dpRoot` requires 4 children. So a node with 3 children cannot be the root of an alkane. However, could there be an alkane where the root has degree 4 but one of its neighbors is also internal and uses the parent edge? Yes, that's fine. But the root of the alkane must have degree 4 in the alkane. If we root the alkane at an internal node, it has 4 children. If we root it at a leaf, that leaf has degree 1, so it must have a parent which is internal. So the root of the alkane (in the rooted sense) could be a leaf. In our DP, we are not considering the case where the alkane is attached to the rest of the tree via a leaf. But we are considering all possible subgraphs, so we need to consider alkanes that are entirely within a subtree, and they could be rooted at any node. If we root the alkane at a leaf, then that leaf is the topmost node in the alkane? Actually, if we consider the alkane as a tree, we can choose any node as root. Our DP `dpRoot[u]` assumes that `u` is the topmost node in the sense that the edge to its parent is not used. That means the alkane does not extend above `u`. So if the alkane is rooted at a leaf, then the parent of that leaf (in the original tree) is not part of the alkane. So that leaf is the topmost node. But then the leaf has degree 1 in the alkane, which is okay. However, as we argued, a leaf topmost node implies the alkane is just a single vertex, because if it had any other nodes, they would have to be connected through the leaf, but the leaf has degree 1. So the alkane would be just the leaf. That's invalid. So the topmost node (the one with no parent in the alkane) must be internal. Wait, is that true? Let's think: In a tree, if we pick a node `r` and consider the tree rooted at `r`, the root has no parent. The degree of `r` in the tree is the number of children. If `r` is a leaf in the tree, its degree is 1, so it has exactly 1 child. But then the tree would be just a path? Actually, if `r` is a leaf, it has exactly one neighbor in the tree. In the rooted tree, that neighbor becomes its child. So the root has one child. But the root's degree in the tree is 1 (since it only connects to that child). So the root is a leaf. That's allowed: a tree can be rooted at a leaf. For example, a path of 2 vertices: root at one leaf, the other is the child. The root has degree 1. So the root can be a leaf. In an alkane, a leaf has degree 1, which is fine. So the topmost node of an alkane (in the rooted sense) could be a leaf. But does that affect our DP? If the alkane is entirely within a subtree, we can choose any node as the root. In our DP, we are not fixing a root; we are just trying to find the largest alkane. The DP `dpRoot[u]` is defined as the best alkane that does not use the parent edge, i.e., the alkane is contained in the subtree of `u` and does not extend to the parent. In that case, `u` is the highest node in the alkane (with respect to the original tree's root). But `u` could be a leaf in the alkane. For example, consider a path: 1-2-3. The largest alkane? None, because internal nodes have degree 2. But if we had a path where one node is internal with degree 4? That's not a path. Let's consider a valid alkane: the star with center 1 and leaves 2,3,4,5. If we root the original tree at 1, then the alkane is entirely within the subtree of 1 (which is the whole tree if 1 is the root). The topmost node is 1, which is internal. That's `dpRoot[1]`. Now consider a different alkane: a longer tree. Suppose we have an alkane that is a "Y" shape: a central node 1 connected to 2,3,4,5, but one of the leaves (say 2) is actually a chain: 1-2-6, where 6 is a leaf? That would give 2 degree 2, not allowed. So to extend, we need to replace leaves with subtrees. So the alkane is a rooted tree where internal nodes have 3 children (plus possibly a parent if not root). So the topmost node (the one with no parent) must have 4 children. If the topmost node is a leaf, then it has 0 children, but then the tree is just that node, invalid. So indeed, the topmost node must be internal. Therefore, in any alkane, the node that is highest in the rooted view (the one that does not use the parent edge) must be internal. So `dpRoot[u]` is only valid when `u` is internal, i.e., it must have at least 4 children. So our DP is correct.

But wait: what if the alkane is not rooted at an internal node in the original tree's rooting? That doesn't matter. The DP explores all possibilities. For a given alkane, there is a unique node that is the highest with respect to the original tree's root (the one whose parent is not in the alkane). That node must be internal. So it will be considered as `dpRoot[u]` for that `u`. So we will find it.

Thus, the algorithm is:
1. Read N and edges.
2. Build adjacency list.
3. Root the tree at 1 (or any node). Do a DFS to compute parent and children.
4. Process nodes in post-order (from leaves upward). For each node `u`, compute:
   - Collect `dp1[v]` for all children `v` of `u`.
   - If `u` has at least 3 children, compute `inner[u] = 1 + sum of top three dp1[v]`. Otherwise, `inner[u] = -infinity`.
   - `dp1[u] = max(1, inner[u])`. (Note: `1` is always possible, meaning `u` is a leaf in the alkane.)
   - If `u` has at least 4 children, compute `dpRoot[u] = 1 + sum of top four dp1[v]`. Otherwise, `dpRoot[u] = -infinity`.
   - Compute `best[u] = max(dpRoot[u], max_{v child of u} best[v])`.
5. The answer is the maximum `best[u]` over all `u`. If the maximum is less than 5 (or if no `dpRoot` is valid), print -1. But careful: the condition "at least one vertex of degree 4" is automatically satisfied if we have a valid `dpRoot` (since the root is internal) or if we have a valid `inner` somewhere. But `best[u]` could be 1 from a leaf? Actually `best[u]` is defined as the best alkane entirely within the subtree. If no alkane exists, `best[u]` might be 0 or negative. We can initialize `best[u]` to 0 (meaning no alkane). Then we take max over `dpRoot[u]` and children's `best`. So if no `dpRoot` is valid and children have no alkane, `best[u]` remains 0. So the final answer is the maximum `best[u]`. If that maximum is 0, print -1. But wait, what about an alkane of size 5? That would give `best[u] = 5`. So we can just check if the maximum is >= 5. However, is it possible that the maximum is 4? Let's see: could we have an alkane of size 4? No, because V = 3I+2, I>=1 => V>=5. So any valid alkane has size at least 5. So we can check if max >= 5. But to be safe, we can just check if max > 0? Actually, if max is 0, it means no alkane. But what about a case where the maximum is 4? That shouldn't happen. However, our DP might produce a value of 4 from `dpRoot[u]`? No, because `dpRoot[u]` requires 4 children, so it's at least 5 (1+4*1=5). But `inner[u]` could be 4? That would be 1 + 1+1+1 = 4, but that requires 3 children, each with `dp1=1`. That gives `inner[u]=4`. But `inner[u]` is not a complete alkane; it's a partial alkane attached to a parent. If we take that as a complete alkane (i.e., if `u` is the root of the alkane and we don't use the parent edge), then `u` would have degree 3 (since it has 3 children and no parent), which is not allowed. So `inner[u]` is not a valid alkane. So we only consider `dpRoot[u]` for complete alkanes. And `best[u]` is the max of `dpRoot[u]` and children's `best`. So `best[u]` will be at least 5 if there is a valid alkane. So we can simply take the maximum over all `best[u]` and if it's 0, print -1, else print the maximum.

But wait: what about the possibility that the alkane is just a single node? That's invalid because no degree 4. So we ignore.

**Pitfalls and edge cases**:
- N=1: no edges, no alkane, answer -1.
- N=2: path, no alkane.
- N=3: star with center degree 2, no.
- N=5: star with center degree 4, answer 5.
- N=6: maybe an alkane of size 5? Or size 6? But size 6 would require I=1, L=4, V=5, so size 6 is impossible. So maximum size is determined by the formula V=3I+2. So possible sizes: 5, 8, 11, 14, ... So we might see 8, 11, etc. as in samples.
- The DP must handle the case where a node has many children, but some children might be excluded. We need to pick the best three (or four) children to maximize the sum. So we need to sort the `dp1[child]` values in descending order and take the top 3 or 4. This is O(N log N) if we sort for each node, but since the sum of degrees is O(N), we can do it efficiently by keeping the top few while iterating. We can collect all `dp1[child]` into a list, sort descending, and take the first 3 or 4. Since the list size is the degree of `u`, and the sum of all degrees is 2(N-1), the total sorting cost is O(N log N) in the worst case if we sort each list, but we can do it in O(N) by using a selection algorithm? Actually, we can just sort each list; the sum of (deg(u) log deg(u)) over all u is O(N log N) because the maximum degree can be O(N), but then it's only one node. For a star, the center has degree N-1, sorting N-1 elements is O(N log N). That's fine for N=2e5. So we can just sort.
- We must be careful with the definition of `dp1[u]`. It is the best size of a partial alkane that includes `u` and uses the edge to its parent. For a leaf in the original tree, `dp1[u] = 1`. For a node with 2 children, `inner[u]` is impossible, so `dp1[u] = 1`. That means the node is used as a leaf. That's fine.
- When we compute `dpRoot[u]`, we require at least 4 children. But what if a node has 4 children, but some of them have `dp1=1`? That's fine, sum = 4, plus 1 = 5.
- We need to ensure that the alkane has at least one degree-4 vertex. In our DP, any `dpRoot[u]` has `u` as internal, so it satisfies that. So we don't need extra checks.
- However, there is a subtlety: what if the alkane is rooted at a node `u` that is internal, but some of its children are not leaves? That's fine because `dp1[child]` will account for the child's internal structure.
- But is it possible that the best alkane is not a "rooted" alkane in the sense that the highest node is not unique? No, in a tree, the highest node with respect to the original root is unique.

**Testing the DP on samples**:

Sample 1:
N=9
Edges:
1-2
2-3
3-4
2-6
2-7
3-8
3-9

Tree:
1: child 2 (if root at 1)
2: children 1,3,6,7. But 1 is parent. So children: 3,6,7.
3: children 2,4,8,9. Parent 2. So children: 4,8,9.
4: child 3 (parent). So no children.
5: not present? Wait, N=9, vertices 1..9. The edges don't include 5. So 5 is isolated? But the problem says it's a tree, so all vertices must be connected. Let's check: edges: 1-2,2-3,3-4,2-6,2-7,3-8,3-9. That's 7 edges. For a tree with 9 vertices, we need 8 edges. So 5 is missing. There must be an edge involving 5. Maybe the sample input is missing a line? Let's look at the sample:
9
1 2
2 3
3 4
4 5
2 6
2 7
3 8
3 9
Ah, there is 4-5. So 5 is connected to 4. So the tree is:
1-2-3-4-5, and 2 connected to 6,7; 3 connected to 8,9.
So the structure: 
1: leaf (only connected to 2)
2: connected to 1,3,6,7 (degree 4)
3: connected to 2,4,8,9 (degree 4)
4: connected to 3,5 (degree 2)
5: leaf (connected to 4)
6,7,8,9: leaves.

Now, the alkane: take vertices 1,2,3,4,6,7,8,9. That's 8 vertices. Let's see the shape: 
2 and 3 are internal (degree 4 in the subgraph: 2 connected to 1,3,6,7; 3 connected to 2,4,8,9). 1,4,6,7,8,9 are leaves. So it's valid. Size 8.
Our DP: root at 1.
Children:
1: children = [2]
2: children = [3,6,7] (parent 1)
3: children = [4,8,9] (parent 2)
4: children = [5] (parent 3)
5: leaf
6,7,8,9: leaves.

Compute dp1 bottom-up:
5: dp1[5] = 1 (no children, so leaf case)
4: children: [5]. dp1[5]=1. inner[4] requires 3 children, not possible. So dp1[4]=1.
3: children: 4,8,9. dp1[4]=1, dp1[8]=1, dp1[9]=1. inner[3] = 1+1+1+1=4. So dp1[3]=max(1,4)=4.
2: children: 3,6,7. dp1[3]=4, dp1[6]=1, dp1[7]=1. inner[2] = 1 + top three: 4,1,1 = 6. So dp1[2]=6.
1: child 2. dp1[2]=6. inner[1] requires 3 children, not possible. dp1[1]=1.
Now compute dpRoot:
For each node, we need 4 children.
1: only 1 child, so dpRoot[1] invalid.
2: children: 3,6,7 (only 3 children, but need 4 for dpRoot). So dpRoot[2] invalid? But wait, if we root at 2, it has only 3 children in the original tree (since 1 is parent). But in the alkane, 2 is internal and has 4 children: 1,3,6,7. So to get the alkane rooted at 2, we need to include the edge to 1 (parent) as a child. But our DP `dpRoot[u]` only considers children, not the parent. So for a node to be the root of an alkane, it must have at least 4 children in the original tree. Here, 2 has degree 4, but one of its neighbors is its parent. So if we root at 2, it has only 3 children (3,6,7) and one parent (1). So to make 2 the root, we would need to not use the parent edge? But in the alkane, 2 is connected to 1. So if we want 2 to be the root, we must include the edge to 1, but that edge goes to the parent. So 2 cannot be the root of the alkane if we are considering the original tree rooted at 1. However, we could choose a different root for the original tree. Our DP as described assumes a fixed root (node 1). So if the alkane is rooted at 2, and 2's parent is 1, then the alkane includes the edge (1,2). In the rooted view (with root 1), 2 is not the topmost node; 1 is. The topmost node is 1. But 1 is a leaf in the alkane. So the alkane's topmost node with respect to root 1 is 1. So we would compute `dpRoot[1]`. But 1 has only one child, so `dpRoot[1]` is invalid. That means our DP would miss this alkane! That's a problem.

So our DP as defined (with `dpRoot` only considering children) is insufficient because it assumes the alkane is rooted at a node that has no parent in the alkane, which corresponds to the node being the highest in the original tree's root. But in this sample, the alkane's highest node with respect to root 1 is node 1, which is a leaf. So we need to consider alkanes that are attached to the rest of the tree via a leaf. In other words, the alkane might not be entirely contained in a subtree rooted at some node; it might span across the root. But we can still capture it by considering the DP from both directions: we need to consider the "upward" direction as well.

This is a classic tree DP problem where the answer can be in any part of the tree, not necessarily a subtree. We need to do a DP that considers both downward and upward contributions. Specifically, we need to compute for each node the best alkane that uses that node as a "attachment point" to the rest of the tree, and also the best alkane that is entirely within the subtree. The sample shows that the alkane includes node 1 (leaf) and node 2 (internal) and goes down. So we need to handle the case where the alkane is attached to the parent via a leaf.

So we need a more general DP: For each node `u`, we need to know the best partial alkane that includes `u` and uses the edge to its parent (if any), but now the parent might be part of the alkane as well. Actually, we can think of the alkane as a tree. If we root the alkane at some node, we can do DP on that alkane. But we need to find the largest such alkane in the original tree. This is similar to finding the largest "subtree" that is an alkane. Because the original graph is a tree, any connected subgraph is a tree. So we are looking for a subtree of the original tree that is an alkane. This is equivalent to: choose a connected set of vertices S, and the induced subgraph on S must be an alkane. Since the original is a tree, the induced subgraph is exactly the minimal tree connecting S. So we can think of it as: we can delete some edges to obtain a forest, and we want a component of that forest that is an alkane. We want the largest such component.

This is a typical "tree DP" where we can decide for each edge whether to keep it or not. The condition is on degrees in the resulting subgraph. So we can think of each vertex having a "state" in the final alkane: it can be a leaf (degree 1) or internal (degree 4). In the final alkane, every vertex must have exactly 1 or 4 incident edges from the original tree that are kept. So we can view it as: we keep some edges, and the kept edges form a tree. For each vertex, the number of kept incident edges must be 1 or 4. And the tree must have at least one vertex with 4 kept edges.

This is a degree-constrained subgraph problem on a tree. Since the tree is undirected, we can root it and do DP that considers the number of kept edges from the node to its children, and also the edge to its parent (which may be kept or not). For each node, we can consider DP states based on the degree of the node in the final subgraph (0,1,4) but since the subgraph is connected and contains the node (if we are considering a component), we can have states: 
- The node is not in the alkane (we don't consider it).
- The node is in the alkane, and the edge to its parent is kept (so the node has at least 1 kept edge from parent). Then the node's degree in the alkane is 1 + (number of kept edges to children). This sum must be 1 or 4. So if the parent edge is kept, then the number of kept child edges can be 0 (making degree 1) or 3 (making degree 4).
- The node is in the alkane, and the edge to its parent is not kept. Then the node's degree in the alkane is exactly the number of kept child edges. This must be 1 or 4. So the number of kept child edges can be 1 (if the node is a leaf) or 4 (if the node is internal). But wait, if the node is a leaf and the parent edge is not kept, then the node is isolated? Actually, if the node is in the alkane and the parent edge is not kept, then the node must have exactly 1 kept child edge to be a leaf, or 4 kept child edges to be internal. But if it's a leaf with 1 child, then that child would have the node as its parent. So the leaf would be the child, not the parent. In other words, if the node is a leaf in the alkane, it has exactly 1 neighbor in the alkane. That neighbor could be its parent or one of its children. So if the parent edge is not kept, the leaf must have exactly 1 kept child edge. So the node's degree is 1 from that child. So that's valid.

Thus, for each node, we can have DP states that describe the best size of an alkane-like subgraph that includes the node and satisfies certain conditions on the edge to the parent. The conditions are: 
- `state 0`: the node is not in the alkane (or we don't care about the alkane containing the node? Actually for the purpose of combining, we need to know the best subgraph that is entirely in the subtree and does not use the parent edge, but may or may not include the node. So we need a state where the node is not included, meaning we don't keep any edges incident to it. That will be useful when a parent decides not to use the edge to this child.
- `state 1`: the node is in the alkane, the parent edge is kept, and the node's degree in the alkane is 1 (so no child edges are kept). This means the node is a leaf attached to its parent.
- `state 4`: the node is in the alkane, the parent edge is kept, and the node's degree is 4 (so exactly 3 child edges are kept, and those children must be in states 1 or 4 with their parent edges kept).
- `state leaf_no_parent`: the node is in the alkane, the parent edge is not kept, and the node's degree is 1 (so exactly 1 child edge is kept, and that child must be in state 1 or 4 with parent edge kept).
- `state internal_no_parent`: the node is in the alkane, the parent edge is not kept, and the node's degree is 4 (so exactly 4 child edges are kept).

But note that `state leaf_no_parent` and `state internal_no_parent` are essentially the same as `state 1` and `state 4` but with the parent edge not used. However, they are different in terms of how they combine with the parent. For the parent, if the parent wants to use the edge to this child, then the child must be in state 1 or 4 (with parent edge kept). If the parent does not use the edge, then the child might be in a state that doesn't require the parent edge, but then the child's subgraph is entirely within its own subtree and might be a complete alkane (if it satisfies the condition). So we need to compute for each node the best value for each of these states, considering the subtree of the node.

Let's define for each node `u` the following DP values, after processing its children:
- `dp0[u]`: best size of an alkane-like subgraph entirely within the subtree of `u` that **does not** include `u` (i.e., `u` is excluded). This is simply the max over children of `best[child]` (where `best[child]` is the best alkane entirely within child's subtree). But we also need to consider that the alkane might be in multiple disconnected components? No, we are looking for a single alkane. So `dp0[u]` is the maximum size of a valid alkane that is completely inside the subtree of `u` but does not include `u`. This will be used when the parent decides not to use the edge to `u`.
- `dp1[u]`: best size of a partial alkane that includes `u`, uses the parent edge, and `u` has degree 1 in the partial alkane (i.e., `u` is a leaf). This means no child edges are used. So `dp1[u] = 1` (just `u`).
- `dp4[u]`: best size of a partial alkane that includes `u`, uses the parent edge, and `u` has degree 4 in the partial alkane. This means exactly 3 child edges are used. For each child, we need to use a state where the child uses the edge to `u` and has degree 1 or 4. So we need the best value for a child when the edge to `u` is used. Let's define for each child `v` a value `f1[v]` which is the best size of a partial alkane that includes `v` and uses the edge to its parent (which is `u`). That is exactly `dp1[v] + dp4[v]?` No, we need to know the best size for `v` given that the edge to `u` is used. That is the maximum of two cases: `v` is a leaf (so the partial alkane is just `v`, size 1) or `v` is internal (so we need to use 3 of its children, etc.). But note that `v`'s state when the edge to `u` is used is exactly the same as the state we are computing for `u` but for the child. So we can compute for each child `v` a value `g[v]` = best size of a partial alkane that includes `v` and uses the edge to its parent. This is analogous to what we want for `u` but from the child's perspective. So we can compute `g[v]` recursively. Let's define:
  * `g[v]` = best size of a partial alkane that includes `v` and uses the edge to its parent.
  * `h[v]` = best size of a complete alkane (i.e., not using the parent edge) that is entirely within the subtree of `v`. This is what we ultimately want for the answer.

But then for `u`, when it wants to use the edge to child `v`, it needs `g[v]`. So we need to compute `g[v]` for all children. And `g[v]` depends on the children of `v`, so we can compute it in a post-order traversal. So we can compute for each node `u`:
- `g[u]` = best size of a partial alkane that includes `u` and uses the parent edge. This can be:
  * `u` is a leaf: size 1.
  * `u` is internal: we need to pick exactly 3 children to attach, and for each such child, we get `g[child]`. So `g[u] = 1 + sum of top three g[child]` if there are at least 3 children, else not possible.
  So `g[u] = max(1, 1 + sum of top three g[child])` but the second term is only valid if there are at least 3 children. Actually, if there are not 3 children, the internal case is impossible, so `g[u] = 1`.

Now, for a complete alkane that is entirely within the subtree of `u` and does not use the parent edge, we have two cases for `u`:
- `u` is a leaf in the alkane: then it must have exactly 1 child edge used. So we pick the best child to attach, and get `g[child]`. So size = 1 + max g[child] over children. But wait, is that correct? If `u` is a leaf, its degree in the alkane is 1. Since the parent edge is not used, the only incident edge is to one child. So that child must use the edge to `u` (i.e., the child is in a state where the parent edge is used). So we take the maximum `g[child]` over all children. So `leaf_alkane[u] = 1 + max_{v child} g[v]`.
- `u` is internal in the alkane: then it must have exactly 4 child edges used. So we pick the top 4 children by `g[child]`. So `internal_alkane[u] = 1 + sum of top four g[v]` if at least 4 children, else not possible.

So the best complete alkane within the subtree of `u` is `best[u] = max( leaf_alkane[u], internal_alkane[u], max_{v child} best[v] )`. But wait, we also need to consider the case where the alkane is rooted at `u` and `u` is a leaf? That is covered by `leaf_alkane[u]`. And `internal_alkane[u]` covers the case where `u` is internal. And the `max_{v child} best[v]` covers the case where the alkane is entirely in a child's subtree.

But is it sufficient to only consider these? What about an alkane that includes `u` and some children, but also goes upward? That would be considered when we compute `g[u]` for the parent. So the final answer is the maximum `best[u]` over all `u`. But note that `best[u]` as defined might include alkanes that are not valid because they might not have any internal vertex. Let's check: `leaf_alkane[u]` has `u` as a leaf, but the child that is attached could be internal. So the alkane could have an internal vertex in the child's subtree. So it's valid. `internal_alkane[u]` has `u` as internal, so valid. And `best[v]` from children are already valid alkanes. So `best[u]` will be valid if it is at least 5? Not necessarily: `leaf_alkane[u]` could be size 2? For example, if `u` has one child, and that child has `g[child]=1` (so the child is just a leaf), then `leaf_alkane[u] = 1+1=2`. That is a tree with two vertices, each degree 1. That is not an alkane because no vertex has degree 4. So we must ensure that the alkane has at least one internal vertex. In the `leaf_alkane[u]` case, the only chance for an internal vertex is in the child's subtree. But if the child is just a leaf (g=1), then the whole subgraph is just an edge, which is invalid. So we need to ensure that the alkane has at least one internal vertex. How can we guarantee that? We can simply check if the resulting subgraph has an internal vertex. In our DP, we can keep track of whether the partial alkane contains an internal vertex. But note that in the definition of an alkane, we require at least one vertex of degree 4. So for a complete alkane (the ones we consider for the answer), we need to ensure that condition. For partial alkanes that are used to build larger ones, we don't care if they have an internal vertex or not, because they might become part of a larger alkane that has an internal vertex. However, when we combine children to form an internal node, we are creating a new internal node, so the resulting alkane will have at least that internal node. So it's fine. For the `leaf_alkane[u]` case, if we take a child that is just a leaf, then the whole alkane would have no internal vertex (since `u` is a leaf and the child is a leaf). So such a configuration should not be considered a valid alkane. But our DP might still consider it as a candidate for `best[u]`. So we need to filter out configurations that do not have any internal vertex. One way is to require that the size of the alkane is at least 5, but that's not sufficient because a tree of size 4 could have an internal vertex? Actually, as argued, the smallest alkane is size 5. So we can simply require that the size is at least 5. But our DP might produce a size of 2,3,4 which are invalid. So we can either filter them out at the end (only consider sizes >= 5) or incorporate a flag in the DP state indicating whether the partial alkane contains an internal vertex. Since the partial alkane might not have an internal vertex yet, we need to be careful. Actually, for the purpose of building larger alkanes, we don't care if the partial alkane has an internal vertex or not. For example, when we attach three children to form an internal node, the children could be just leaves (no internal vertex), and the resulting alkane will have the new internal node. So it's fine. For the `leaf_alkane[u]` case, if the child we attach is a partial alkane that already has an internal vertex, then the whole alkane is valid. If the child does not have an internal vertex, then the whole alkane might still be valid if `u` itself is internal? But in `leaf_alkane[u]`, `u` is a leaf, so it has degree 1. So the only chance for an internal vertex is in the child's subtree. So we need to know for each partial alkane (attached to parent) whether it contains an internal vertex. Let's define for each node `u` two values for `g[u]`:
- `g0[u]`: best size of a partial alkane that includes `u`, uses the parent edge, and has **no** internal vertex (i.e., all vertices in the partial alkane are leaves). This is only possible if `u` is a leaf and all children used are also leaves. But if we use any child, that child must be in a state that uses the parent edge. If that child has no internal vertex, then the child must be a leaf (since if it were internal, it would have degree 4, so it would be an internal vertex). So for `g0[u]`, we can only attach children that are also `g0` (i.e., no internal vertex). But if we attach any child, that child would have degree 1 (since it uses the parent edge and no other edges), so it is a leaf. So the whole partial alkane would be a tree where `u` is internal? Wait, if `u` uses the parent edge and also uses 3 child edges, then `u` has degree 4, so `u` is an internal vertex. So that would introduce an internal vertex. So `g0[u]` is only possible if `u` is a leaf (no child edges used). So `g0[u] = 1` (just `u`). And if we try to make `u` internal, then `u` becomes an internal vertex, so the partial alkane has an internal vertex. So we can define:
- `g_with_internal[u]`: best size of a partial alkane that includes `u`, uses the parent edge, and has at least one internal vertex. This is the same as `g[u]` we defined earlier, but we need to ensure that the configuration actually contains an internal vertex. For `g[u]`, if we take the internal case (3 children), then `u` is internal, so it contains an internal vertex. If we take the leaf case (1 child? no, leaf case is just `u` alone, size 1, which has no internal vertex). So we can separate:
  * `g_leaf[u] = 1` (no internal vertex).
  * `g_internal[u] = 1 + sum of top three g[child]` (but we need to consider that the children themselves might not have internal vertices, but that's okay because `u` is internal). So `g_internal[u]` is valid only if there are at least 3 children. And the size will be at least 4 (1+3*1=4) but that configuration has no internal vertex in the children, but `u` is internal, so the whole has an internal vertex. So `g_internal[u]` is a valid partial alkane with an internal vertex.
  Then we can define `g[u] = max(g_leaf[u], g_internal[u])` for the purpose of combining with parent? Actually, when we combine, we don't care if the child has an internal vertex or not, because if the child doesn't have an internal vertex, it's just a leaf, and that's fine. So we can just use `g[u] = max(1, 1+sum top3)` as before. But for the `leaf_alkane[u]` case, we need to know if the child we attach contains an internal vertex. Because if the child is just a leaf (no internal vertex), and `u` is a leaf, then the whole alkane has no internal vertex. So we need to know for each child `v` whether the partial alkane `g[v]` contains an internal vertex. So we need to compute for each node two values: the best size with internal vertex and the best size without internal vertex. But note that a partial alkane without internal vertex is necessarily just a single vertex? Let's check: If a partial alkane includes `u` and uses the parent edge, and has no internal vertex, then `u` must be a leaf (degree 1), so no child edges are used. So the partial alkane is just `u`. So `g0[u] = 1`. If we try to use any child edges, then `u` would have degree >1. If `u` has degree 4, it's internal. If `u` has degree 2 or 3, that's not allowed. So indeed, the only partial alkane without an internal vertex is the single vertex. So we can define:
- `g_no_int[u] = 1` (just `u`).
- `g_int[u] = 1 + sum of top three g[child]` if at least 3 children, else not possible.
Then `g[u] = max(g_no_int[u], g_int[u])` but we need to know which case gives a larger size. Typically, `g_int[u]` will be larger if possible.

Now, for `leaf_alkane[u]` (complete alkane where `u` is a leaf and parent edge not used), we need to pick one child to attach. That child will be in a state where it uses the edge to `u` (so it's a partial alkane with parent edge used). The resulting alkane will have an internal vertex if and only if the child's partial alkane has an internal vertex. So we need to consider both possibilities: if we pick a child that has an internal vertex, then the whole alkane is valid. If we pick a child that is just a leaf (no internal vertex), then the whole alkane is just two leaves, invalid. So we should only consider children that have an internal vertex. So we need for each child `v` a value `g_int[v]` (the best size of a partial alkane that includes `v` and has an internal vertex). Then `leaf_alkane[u] = 1 + max_{v} g_int[v]` (if such a child exists), else not valid.

Similarly, for `internal_alkane[u]` (complete alkane where `u` is internal and parent edge not used), we need to pick 4 children. Each child will be attached via the edge to `u`, so they are in state using parent edge. They can be either with or without internal vertex. The resulting alkane will have an internal vertex (namely `u`), so it's valid regardless of whether the children have internal vertices. So we can use `g[child]` (which could be 1 if no internal vertex) for the children. So `internal_alkane[u] = 1 + sum of top four g[child]` if at least 4 children.

Now, we also need to consider the case where the alkane is entirely within a child's subtree, which is already covered by `best[child]`.

So the DP becomes:
For each node `u` (processed in post-order):
1. For each child `v`, we have already computed:
   - `g[v]`: best size of a partial alkane that includes `v` and uses the edge to its parent (which is `u`). This is the max of:
        * `g_no_int[v] = 1`
        * `g_int[v] = 1 + sum of top three g[w]` over grandchildren `w` of `v` (i.e., children of `v` except `u`). This is valid only if `v` has at least 3 children (excluding `u`).
   So we can compute `g[v]` as described.
   - `best[v]`: best size of a complete alkane entirely within the subtree of `v`. This is the max of:
        * `leaf_alkane[v] = 1 + max_{w child of v, w != u} g_int[w]` (if any such w with g_int exists)
        * `internal_alkane[v] = 1 + sum of top four g[w]` over children `w` of `v` excluding `u` (if at least 4 such children)
        * `max_{w child of v, w != u} best[w]`
   But note: when computing `best[v]`, we are considering the subtree of `v` excluding `u`. So we need to pass the information that `u` is the parent. So we need to do a rerooting DP? Actually, we can compute everything in a single DFS if we consider the children relative to the root. But the definition of `g[v]` and `best[v]` depends on the parent. So we need to do a DP that takes into account the parent. This is a classic tree DP with two passes: one post-order to compute the "downward" values, and one pre-order to compute the "upward" values. But maybe we can simplify by noting that the alkane is a tree, and we can root it arbitrarily. However, the condition for the alkane to be valid is global. So we need to consider all possible subtrees.

Given the constraints (N up to 2e5), we need an O(N) or O(N log N) solution. The DP described above can be computed in O(N) if we are careful. But we need to handle the fact that `g[v]` and `best[v]` depend on the parent. We can compute for each node the values assuming a certain parent (e.g., for the rooted tree at 1, we compute for each node the values for the subtree rooted at that node, not considering the parent). That is, we compute `g_down[u]` = best size of a partial alkane that includes `u` and uses the edge to its parent (in the rooted tree), considering only the subtree of `u` (excluding the parent). This is exactly what we computed earlier as `g[u]`. And `best_down[u]` = best size of a complete alkane entirely within the subtree of `u` (excluding the parent). This is `best[u]` as computed earlier. But as we saw in the sample, the alkane might include the parent of `u`. So we also need to compute the "upward" values: the best alkane that includes the parent and goes through `u`. That is, for each node `u`, we need to know the best partial alkane that includes `u` and uses the edge to its parent, but now the parent might have other branches (from the rest of the tree). So we need to combine the downward contributions from the children with the upward contribution from the parent.

This is getting complicated. Let's think of an alternative approach.

**Alternative approach: Tree DP with "re-rooting"**

We can compute for each node the best alkane that is entirely within the tree, but we can also think of the problem as: we want to select a connected subgraph S that is an alkane. Since the original graph is a tree, S is a tree. We can root S at some node. The condition on S is that every node has degree 1 or 4 in S. This is similar to a "degree-constrained tree" problem. We can try to find the maximum such S by considering each node as a potential root of the alkane? But the alkane is not necessarily rooted at a node in the original tree in a natural way.

Another idea: Since the degree condition is very restrictive (only 1 or 4), we can think of the alkane as a tree where every internal node has exactly 4 neighbors. In the original tree, each node can have at most its original degree. So we need to choose for each node a subset of its incident edges to keep, such that the kept edges form a tree and the degree in the kept edges is 1 or 4. This is like finding a "subgraph" that is a tree with degree constraints.

We can formulate this as a maximum subgraph problem with degree constraints. Since the graph is a tree, we can use DP on the tree. For each node, we can consider how many kept edges go from the node to its children. Let's denote for each node u, we choose an integer k in {0,1,2,3,4} (but actually the degree must be 1 or 4, so k can be 1 or 4 if the parent edge is kept, or if the parent edge is not kept, then k can be 1 or 4 as well? Actually, if the node is in the alkane, its total degree in the alkane is the number of kept incident edges. That number must be 1 or 4. So if we denote x_u as the number of kept edges from u to its children, and p_u as whether the edge to the parent is kept (0 or 1), then the total degree is p_u + x_u, which must be 1 or 4. So possible (p_u, x_u) pairs: (0,1), (0,4), (1,0), (1,3). Note that (0,0) is not allowed because then u would be isolated (degree 0), which is not allowed. Also (1,1) would give degree 2, not allowed. So the valid states for a node u are:
- p_u=0, x_u=1: u is a leaf, with one child kept.
- p_u=0, x_u=4: u is internal, with four children kept.
- p_u=1, x_u=0: u is a leaf, with parent edge kept.
- p_u=1, x_u=3: u is internal, with three children kept and parent edge kept.

Now, for the tree of the alkane, we need to choose for each node one of these states, and the kept edges must form a connected tree. Also, the alkane must have at least one node with x_u=4 or (p_u=0 and x_u=4) i.e., an internal node.

We can do a DP where for each node u, we compute the best size of a connected subgraph that includes u and satisfies the state conditions, and then take the max over all possible states and all nodes. This is similar to the DP on trees for degree-constrained subgraphs.

Let's define for each node u, and for each of the four states (p=0, x=1), (p=0, x=4), (p=1, x=0), (p=1, x=3), we compute the maximum number of vertices in a subgraph that is entirely within the subtree of u (excluding the parent), satisfies the state for u, and forms a valid partial alkane (i.e., all nodes in the subtree satisfy the degree conditions, and the subgraph is connected). Then we can combine these to get the answer. But we also need to consider that the alkane might extend above u, so we need to consider the parent edge. This is a typical "tree DP with states" problem. We can do a reroot DP: first compute DP values for the subtree (downward), then do a second pass to compute the DP values when considering the parent (upward). But the state space is small (4 states), so we can do O(N) DP.

Let's formalize. Root the tree at 1. For each node u, we consider its children (in the rooted tree). We will compute for each node u the following four values, where the first two are for the case when the edge to the parent is NOT used (p=0), and the last two are for when the edge to the parent IS used (p=1). But we need to be careful: when p=0, the subgraph does not include the parent, so it must be contained in the subtree of u. When p=1, the subgraph includes u and the parent edge, so it extends to the parent. So for the downward DP, we compute values for the subtree. Let's define:
- `down[u][0]`: best size of a valid partial alkane contained in the subtree of u, that includes u, with p_u=0 (i.e., the edge to parent is not used), and u has degree 1 in the alkane (so x_u=1, exactly one child is used). This means we pick exactly one child v, and for that child, we must have p_v=1 (since the edge u-v is used) and the child must satisfy its own state. So we need the best value for a child when the edge to u is used and the child is in state p=1 and x=0 or x=3? Actually, if the child v is attached to u, then from v's perspective, the edge to u is used, so p_v=1. And v's degree in the alkane will be 1 (if x_v=0) or 4 (if x_v=3). So we need for each child v the best value of a partial alkane that includes v and uses the edge to u (p_v=1). Let's denote for each child v a value `use[v]` which is the best size of a partial alkane that includes v and uses the edge to its parent. This is the maximum of two cases: v is a leaf (p=1, x=0) -> size 1; v is internal (p=1, x=3) -> size 1 + sum of top three `use` of its children (excluding u). So we can compute `use[v]` recursively. So for `down[u][0]`, we need to pick one child v and add `use[v]`. So `down[u][0] = 1 + max_{v child} use[v]`. But we must ensure that the child v is used in a way that the edge u-v is kept. So that's fine.
- `down[u][4]`: best size of a valid partial alkane contained in the subtree of u, that includes u, with p_u=0 and u has degree 4 (x_u=4). So we need to pick exactly four children, and for each, we add `use[v]`. So `down[u][4] = 1 + sum of top four use[v]` if at least 4 children, else -infinity.
- `use[u]` (which is p=1): best size of a partial alkane that includes u and uses the edge to its parent. This can be:
  * u is a leaf: `use[u] = 1`.
  * u is internal: `use[u] = 1 + sum of top three use[v]` if at least 3 children, else -infinity.
  So `use[u] = max(1, 1 + sum of top three use[v])` but the second term is only valid if at least 3 children. Actually, we can just compute `use[u] = max(1, 1 + sum_top3)` where sum_top3 is valid only if there are at least 3 children; otherwise, it's -inf.
- We also need a value for the case when the edge to the parent is used and u is internal (p=1, x=3). That is exactly the internal case in `use[u]`. So we can store that separately if needed.

Now, for the answer, we need to consider complete alkanes that are not attached to any parent. That is, a connected subgraph that is a tree and has at least one internal vertex. This can be:
- A subgraph that is entirely within the subtree of some node u, with p_u=0. So we can take the max over u of `down[u][0]` and `down[u][4]`. But wait, `down[u][0]` gives an alkane where u is a leaf. That alkane might have an internal vertex in the child's subtree. So it could be valid. `down[u][4]` gives an alkane where u is internal, so it's valid. So the maximum over all u of max(down[u][0], down[u][4]) should give the best alkane entirely within some subtree (with the root of the alkane being u or in the subtree). But we also need to consider alkanes that are not contained in a single subtree rooted at some node? Actually, any connected subgraph of a tree is contained in the subtree of some node if we root the tree arbitrarily? Not necessarily. For example, in the sample, the alkane includes nodes 1 and 2, where 1 is the parent of 2. If we root the tree at 1, then the alkane is contained in the subtree of 1 (which is the whole tree). So it is contained in a subtree. In fact, for any connected subgraph S, if we root the original tree at an arbitrary node r, then S is contained in the subtree of r (since r is the root of the whole tree, its subtree is the whole tree). So S is always contained in the subtree of r. But we need to find the maximum S. So we can just consider all possible S that are entirely within the subtree of some node u (with respect to the root r). However, if we fix r, then S is contained in the subtree of r (the whole tree). So we can compute the best S within the whole tree by considering the DP values for the root r. But the root r might not be the topmost node of S. In the sample, the topmost node of S is 1, which is the root. So that's fine. But if the topmost node of S is not the root, then S is contained in the subtree of that node? Actually, if S is a connected subgraph, and we consider the original tree rooted at r, then the node in S that is closest to r (i.e., the one with the smallest depth) is the topmost node. That node u has the property that S is contained in the subtree of u (since all nodes in S are descendants of u in the rooted tree). So S is contained in the subtree of u. So we can find S by considering each node u as the topmost node, and computing the best alkane within the subtree of u that does not use the parent edge. That is exactly `down[u][0]` and `down[u][4]`. So the answer should be the maximum over all u of max(down[u][0], down[u][4]). But wait, in the sample, for u=1, down[1][0] and down[1][4]? Let's compute with the new DP.

Root at 1.
Children: 1 has child 2.
For node 2: children: 3,6,7 (since 1 is parent).
For node 3: children: 4,8,9.
For node 4: child 5.
Leaves: 5,6,7,8,9.

Compute use[v] for leaves: use[5]=1, use[6]=1, use[7]=1, use[8]=1, use[9]=1.
For node 4: children: [5]. use[4] = max(1, 1+sum_top3) = max(1, 1+? only 1 child) = 1. (since internal case not possible)
For node 3: children: 4,8,9. use[3] = max(1, 1+sum_top3) = 1 + 1+1+1 = 4. So use[3]=4.
For node 2: children: 3,6,7. use[2] = 1 + 1+4+1 = 6? Wait, sum_top3: 4,1,1 = 6. So use[2]=6.
For node 1: child 2. use[1] = max(1, 1+? only 1 child) = 1.

Now compute down[u][0] and down[u][4] for each node.
For node 5: no children. down[5][0] = 1 + max use? no children, so impossible. down[5][4] = impossible.
For node 6,7,8,9: similar.
For node 4: child 5. down[4][0] = 1 + max use[5] = 1+1=2. down[4][4] = 1 + sum_top4? only 1 child, so impossible.
For node 3: children: 4,8,9. use[4]=1, use[8]=1, use[9]=1. down[3][0] = 1 + max(1,1,1) = 2. down[3][4] = 1 + sum_top4? only 3 children, so impossible.
For node 2: children: 3,6,7. use[3]=4, use[6]=1, use[7]=1. down[2][0] = 1 + max(4,1,1) = 5. down[2][4] = 1 + sum_top4? only 3 children, so impossible.
For node 1: child 2. use[2]=6. down[1][0] = 1 + max(6) = 7. down[1][4] = impossible.

Now, the maximum over u of max(down[u][0], down[u][4]) is: for u=1, down[1][0]=7; for u=2, down[2][0]=5; for u=3, down[3][0]=2; for u=4, down[4][0]=2. So the maximum is 7. But the sample answer is 8. So we are missing the alkane of size 8. The size 8 alkane includes nodes 1,2,3,4,6,7,8,9. In our DP, for u=1, down[1][0] gave 7, which corresponds to attaching one child to 1. That child is 2, and we get use[2]=6. That gives a subgraph of size 1+6=7. But the actual alkane has size 8. Why is there a discrepancy? Because in the alkane, node 1 is a leaf, and node 2 is internal, and node 3 is internal, etc. The total number of vertices is 1+4+3? Let's count: 1 (leaf), 2 (internal with 3 children: 1,3,6,7), 3 (internal with 3 children: 2,4,8,9), 4 (leaf), 6,7,8,9 (leaves). That's 8 vertices. In our DP, use[2] was computed as 6, which is the size of the partial alkane attached to 2 via the edge from 1. That partial alkane includes 2,3,4,6,7,8,9? That's 7 vertices? Actually, use[2] includes 2 and its descendants. Let's see: use[2] = 6. That means 2 plus the best three children. The children are 3,6,7. use[3]=4, use[6]=1, use[7]=1. So use[2] = 1+4+1+1=7? Wait, 1+4+1+1=7, not 6. I miscalculated: 1+4+1+1=7. So use[2] should be 7. But earlier I said 6. Let's recalculate carefully:
use[3] = 1 + use[4] + use[8] + use[9] = 1+1+1+1=4.
use[2] = 1 + use[3] + use[6] + use[7] = 1+4+1+1=7.
So use[2]=7. Then down[1][0] = 1 + max use[2] = 1+7=8. Yes! So down[1][0]=8. That matches the answer. So the maximum is 8. So our DP works.

But wait, in the sample, the alkane includes node 1 as a leaf. In our DP, down[1][0] is the case where u=1 is a leaf (p=0, x=1). That means 1 uses exactly one child. That child is 2, and we add use[2]. That gives size 1+7=8. And the resulting alkane has 1 as a leaf, and the rest is attached via 2. And since use[2] is computed as internal for 2, the alkane has internal vertices. So it's valid. So the answer is 8. Great.

So the algorithm is:
1. Root the tree at 1 (or any node).
2. Do a post-order traversal to compute for each node u:
   - `use[u]`: best size of a partial alkane that includes u and uses the edge to its parent. This is:
        if u has at least 3 children: `use[u] = max(1, 1 + sum of top three use[child])`
        else: `use[u] = 1` (since the internal case is impossible, the best is just u as a leaf).
   Actually, we can compute `use[u] = max(1, 1 + sum_top3)` where sum_top3 is valid only if there are at least 3 children; otherwise, the second option is not considered.
   - `down0[u]`: best size of a valid alkane within the subtree of u where u is a leaf (p=0, x=1). This is:
        if u has at least 1 child: `down0[u] = 1 + max_{v} use[v]`
        else: `down0[u]` is not possible? Actually, if u has no children, then p=0 and x=1 is impossible because x=1 requires one child. So down0[u] should be -infinity. But we can treat it as 0 or not use.
   - `down4[u]`: best size of a valid alkane within the subtree of u where u is internal (p=0, x=4). This is:
        if u has at least 4 children: `down4[u] = 1 + sum of top four use[v]`
        else: not possible.
   - `best[u]`: best size of a valid alkane entirely within the subtree of u. This is:
        `best[u] = max( down0[u], down4[u], max_{v} best[v] )`
        We can initialize `best[u]` to 0, and then take max with children's best.
3. The answer is the maximum over all u of `best[u]`. But note that `best[u]` might include down0 and down4, which are valid alkanes. Also, we need to ensure that the alkane has at least one internal vertex. However, in our computation, down0[u] might be valid even if it doesn't have an internal vertex? For example, if u is a leaf and the child we attach is also a leaf (use=1), then down0[u]=2, which is not a valid alkane. So we need to filter out such cases. How can we ensure that? We can keep track of whether the partial alkane contains an internal vertex. For `use[u]`, we have two cases: leaf (size 1, no internal vertex) and internal (size >=4, has internal vertex). So we can compute two values: `use_no_int[u]` and `use_int[u]`. Then for down0[u], we need to attach a child that has an internal vertex, because otherwise the whole alkane would have no internal vertex. So we need for each child v, the best size of a partial alkane that has an internal vertex. Let's define:
- `use_int[u]`: best size of a partial alkane that includes u, uses the parent edge, and has at least one internal vertex. This is only possible if u is internal (x=3) or if the child we attach has an internal vertex? Actually, if u is a leaf (p=1, x=0), then the partial alkane is just u, which has no internal vertex. So `use_int[u]` is only possible if u is internal. So `use_int[u] = 1 + sum of top three use[child]` (since u is internal, it contributes an internal vertex). So we compute this only if u has at least 3 children.
- `use_no_int[u] = 1` (just u).
Then for down0[u], we need to attach a child v such that the resulting alkane has an internal vertex. That will happen if either v's partial alkane has an internal vertex, or u itself is internal? But u is a leaf in down0, so u is not internal. So we need v to have an internal vertex. So we need `use_int[v]`. So `down0[u] = 1 + max_{v} use_int[v]` if such v exists, else not valid.
For down4[u], u is internal, so the alkane has an internal vertex regardless of children. So we can use `use[v]` (which could be 1). So `down4[u] = 1 + sum of top four use[v]` if at least 4 children.
Then `best[u] = max( down0[u], down4[u], max_{v} best[v] )`.

But we also need to consider the case where the alkane is rooted at u and u is a leaf, but the child we attach is a partial alkane that has an internal vertex. That's covered by down0[u]. And if the child is just a leaf, then down0[u] would be invalid because use_int[v] is not defined (or is -inf). So we need to compute use_int[v] properly.

Let's test this on the sample.
Compute use_int and use_no_int for each node.
Leaves: use_int[5] = impossible, use_no_int[5]=1.
Node 4: children: [5]. use_int[4] = impossible (needs 3 children). use_no_int[4]=1.
Node 3: children: 4,8,9. use_int[3] = 1 + use[4]+use[8]+use[9] = 1+1+1+1=4. (Here, use[4]=1, use[8]=1, use[9]=1) So use_int[3]=4. use_no_int[3]=1.
Node 2: children: 3,6,7. use_int[2] = 1 + use[3]+use[6]+use[7] = 1+4+1+1=7. use_no_int[2]=1.
Node 1: child 2. use_int[1] = impossible, use_no_int[1]=1.

Now down0 and down4:
Node 5: no children. down0[5] = impossible, down4[5] = impossible.
Node 4: child 5. use_int[5] impossible, so down0[4] = impossible. down4[4] = impossible.
Node 3: children: 4,8,9. use_int[4] impossible, use_int[8] impossible, use_int[9] impossible. So down0[3] = impossible. down4[3] = impossible.
Node 2: children: 3,6,7. use_int[3]=4, use_int[6] impossible, use_int[7] impossible. So down0[2] = 1 + max(4, -inf, -inf) = 5. down4[2] = impossible.
Node 1: child 2. use_int[2]=7. down0[1] = 1+7=8. down4[1] = impossible.

best:
best[5]=0, best[4]=0, best[3]=0, best[2]=max(5, 0,0,0)=5, best[1]=max(8,5,0)=8.
Maximum best = 8. Correct.

So this DP works.

Now, we need to implement this efficiently. We need to compute for each node:
- `use_int[u]`: best size with internal vertex.
- `use_no_int[u] = 1`.
- `down0[u]`: if there exists a child v with use_int[v] defined, then down0[u] = 1 + max use_int[v].
- `down4[u]`: if at least 4 children, then down4[u] = 1 + sum of top four use[v] (where use[v] = max(use_int[v], use_no_int[v])? Actually, use[v] is the best size regardless of internal vertex. For down4, we don't care if the child has an internal vertex because u is internal. So we use use[v] = max(use_int[v], 1). But use_int[v] might be -inf if not possible, so we can take the max of use_int[v] and 1? But careful: use[v] should be the best size of a partial alkane that includes v and uses the edge to u. That is exactly what we need. So we can compute a single value `best_use[v] = max(use_int[v], 1)` (since use_no_int[v] is 1). But note that use_int[v] might be larger than 1, so best_use[v] is the maximum. So we can define:
- `g[v] = max(use_int[v], 1)` (since 1 is always possible as a leaf).
Then:
- `use_int[u] = 1 + sum of top three g[child]` if at least 3 children, else -inf.
- `down0[u] = 1 + max use_int[child]` if any child has use_int[child] defined, else -inf.
- `down4[u] = 1 + sum of top four g[child]` if at least 4 children, else -inf.
- `best[u] = max( down0[u], down4[u], max best[child] )`.

We also need to handle the case where a child has use_int[child] defined but is very small. That's fine.

Now, we need to compute these values in a post-order traversal. We need to store for each node its children (excluding parent). We can do a DFS to get the tree structure and parent array.

Complexities: For each node, we need to find the top three or four `g[child]` values. We can do this by collecting all `g[child]` into a list, sort descending, and take the first few. Since the sum of degrees is O(N), the total sorting time is O(N log N) in the worst case (e.g., a star). That's acceptable for N=2e5.

But we can optimize: we can keep the top 4 values while iterating, but we need to sort for use_int? Actually, for use_int, we need the top 3. For down4, we need the top 4. We can compute both by sorting once. So for each node, we create a list of `g[child]` for all children, sort it in descending order, then:
- If len >= 3, sum_top3 = sum of first 3.
- If len >= 4, sum_top4 = sum of first 4.
- Also, max_use_int = maximum of use_int[child] (if any child has use_int[child] > 0, we take the max; otherwise, -inf).

But we need use_int[child] separately. So we need to compute use_int[child] for each child before computing the parent's values. So in the post-order, when we process u, we have already computed use_int[v] and g[v] for all children v. So we can compute use_int[u] based on g[child] (which is max(use_int[child], 1)). So we don't need to sort use_int[child] separately; we can compute g[child] = max(use_int[child], 1). Then for use_int[u], we need the top 3 g[child]. So we can sort the list of g[child]. For down0[u], we need the max use_int[child]. So we need to know use_int[child] separately. So we should store both g[child] and use_int[child] for each child.

Let's define for each node u after processing children:
- `children_g`: list of g[v] for v in children.
- `children_use_int`: list of use_int[v] for v in children.

We can sort children_g to get top3 and top4. And find max of children_use_int.

Now, what about the case where a node has no children? Then g list is empty. use_int[u] is -inf. down0[u] and down4[u] are -inf. best[u] = max(0, max best[child]) but no children, so best[u] = 0.

We also need to initialize best[u] = 0, and then take max with down0, down4, and children's best.

Now, the final answer is the maximum best[u] over all u. If that maximum is 0, print -1. But wait, could the maximum be 0 even if there is a valid alkane? No, because a valid alkane has at least 5 vertices. So if the maximum is 0, it means no alkane exists. If the maximum is between 1 and 4, that would be an error in our DP, but it shouldn't happen. We can still check if the maximum >= 5. However, to be safe, we can just check if the maximum > 0? But what if the maximum is 1? That would correspond to a single vertex, which is not an alkane. So we should require that the alkane has at least one internal vertex. In our DP, down0[u] and down4[u] are only defined if they produce a valid alkane with an internal vertex. down0[u] requires that the child has an internal vertex, so it will be at least 5 (1+4=5? Actually, if use_int[child]=4, then down0=5; if use_int[child]=7, then down0=8, etc. So down0[u] will be at least 5. down4[u] is at least 5 (1+4*1=5). So best[u] will be at least 5 if there is a valid alkane. So we can just take the maximum best[u] and if it is 0, print -1, else print the maximum.

Let's test on sample 2:
7 nodes, edges: 1-2,1-3,2-4,2-5,3-6,3-7.
Root at 1.
Children: 1: 2,3.
2: 4,5.
3: 6,7.
Leaves: 4,5,6,7.
Compute:
g[4]=1, use_int[4]=-inf.
g[5]=1, use_int[5]=-inf.
g[6]=1, use_int[6]=-inf.
g[7]=1, use_int[7]=-inf.
Node 2: children_g: [1,1]. len<3, so use_int[2]=-inf. down0[2]: max use_int[4], use_int[5] both -inf, so -inf. down4[2]: len<4, -inf. best[2]=max(0,0,0)=0.
Node 3: similarly, best[3]=0.
Node 1: children_g: [g[2], g[3]] = [max(-inf,1)=1, max(-inf,1)=1]. So children_g = [1,1]. len=2. use_int[1]=-inf. down0[1]: max use_int[2], use_int[3] both -inf, so -inf. down4[1]: len<4, -inf. best[1]=max(0, best[2], best[3])=0.
So max best = 0. Output -1. Correct.

Sample 3: N=15. We can test after implementing.

So the algorithm seems correct.

**Implementation details**:
- Use adjacency list.
- Do a DFS to set parent and children.
- Process nodes in post-order (using recursion or stack; N=2e5, recursion might hit stack limit, so we should use iterative post-order or set recursion limit high in Python). Python recursion limit can be increased, but iterative is safer.
- For each node, after processing children, compute:
  - `g = max(use_int, 1)` (but use_int might be -inf, so we need to handle that).
  - Store g in an array.
  - Compute use_int: if number of children >= 3, then use_int = 1 + sum of top three g[child]. Else use_int = -inf.
  - Compute down0: if there is any child with use_int[child] > 0 (or defined), then down0 = 1 + max(use_int[child]). Else down0 = -inf.
  - Compute down4: if number of children >= 4, then down4 = 1 + sum of top four g[child]. Else down4 = -inf.
  - Compute best[u] = max(down0, down4, 0, max(best[child])). Actually, we can initialize best[u] to 0, and then update with down0, down4, and iterate over children to take max of best[child].
- Finally, the answer is the maximum over all best[u]. If that maximum is 0, print -1, else print the maximum.

We need to be careful with the sorting: for each node, we need the top 3 and top 4 of g[child]. We can sort the list of g[child] in descending order. But we also need the max of use_int[child]. So we can compute that separately.

Let's write pseudocode:

```
N = read int
adj = [[] for _ in range(N+1)]
for i in range(N-1):
    a,b = read
    adj[a].append(b)
    adj[b].append(a)

parent = [0]*(N+1)
order = []  # for post-order
stack = [1]
parent[1] = -1
while stack:
    u = stack.pop()
    order.append(u)
    for v in adj[u]:
        if v != parent[u]:
            parent[v] = u
            stack.append(v)

# Now process in reverse order (post-order)
g = [0]*(N+1)
use_int = [0]*(N+1)
down0 = [0]*(N+1)
down4 = [0]*(N+1)
best = [0]*(N+1)
ans = 0

for u in reversed(order):
    children = [v for v in adj[u] if v != parent[u]]
    child_g = []
    child_use_int = []
    for v in children:
        child_g.append(g[v])
        child_use_int.append(use_int[v])
    # sort child_g descending
    child_g.sort(reverse=True)
    # compute use_int[u]
    if len(child_g) >= 3:
        use_int[u] = 1 + child_g[0] + child_g[1] + child_g[2]
    else:
        use_int[u] = -10**18  # negative infinity
    # compute g[u]
    g[u] = max(use_int[u], 1)
    # compute down0[u]
    max_use_int_child = -10**18
    for val in child_use_int:
        if val > max_use_int_child:
            max_use_int_child = val
    if max_use_int_child > -10**18:
        down0[u] = 1 + max_use_int_child
    else:
        down0[u] = -10**18
    # compute down4[u]
    if len(child_g) >= 4:
        down4[u] = 1 + child_g[0] + child_g[1] + child_g[2] + child_g[3]
    else:
        down4[u] = -10**18
    # compute best[u]
    best_u = max(0, down0[u], down4[u])
    for v in children:
        if best[v] > best_u:
            best_u = best[v]
    best[u] = best_u
    if best_u > ans:
        ans = best_u

if ans == 0:
    print(-1)
else:
    print(ans)
```

But we need to handle the case where a node has children but use_int[u] is negative infinity. Then g[u] = 1. That's fine.

One more thing: in the sample, the alkane size is 8, which is >=5. So ans will be 8.

Let's test on sample 1 manually with the code.

We'll implement and test.

**Potential issues**:
- The negative infinity value: we can use -1e18.
- The sorting: we need to sort child_g, but we also need to compute max_use_int_child. We can compute that in the same loop.
- We need to ensure that for down0[u], we only consider children that have use_int[child] defined (i.e., > -inf). If a child has use_int[child] = -inf, it means that child cannot be internal when attached to u, so it can only be a leaf. But if we attach such a child to u when u is a leaf, then the whole alkane would have no internal vertex (since u is leaf and child is leaf). So we should not consider that child for down0[u]. So we filter out children with use_int[child] <= 0? Actually, use_int[child] could be positive, but if it's -inf, we ignore. So max_use_int_child should be the maximum among use_int[child] that are not -inf. If all are -inf, then down0[u] is -inf.
- For down4[u], we use child_g, which is max(use_int[child], 1). So even if use_int[child] is -inf, we use 1. That's correct because for an internal node, we can attach a leaf child.

Now, what about the case where the alkane is just a single node? That would be best[u]=1, but we output -1 if ans=0. However, our best[u] will be 0 for such a node because down0 and down4 are -inf, and best[child] are 0. So ans=0. So we output -1. Good.

What about an alkane of size 2? That would require two vertices connected by an edge, both degree 1. That's not allowed. In our DP, could that happen? For two vertices u and v, if u is leaf and v is leaf, then use_int[u] is -inf (since u has no children), g[u]=1. Similarly for v. Then down0[u] would be 1 + max use_int[child] = 1 + (-inf) = -inf. So not valid. So best remains 0. So no false positive.

Thus, the algorithm should work.

**Complexity**: O(N log N) due to sorting at each node. In the worst case, a star graph, the center has N-1 children, sorting takes O(N log N). For other nodes, constant. So total O(N log N). N=2e5, this is fine.

We can optimize the sorting by using nth_element or keeping top 4, but not necessary.

**Space**: O(N) for arrays and adjacency list.

**Implementation notes**:
- Use 0-indexed or 1-indexed? The problem uses 1-indexed. We'll use 1-indexed.
- Use iterative DFS to avoid recursion depth issues.
- Use large negative number for -inf, e.g., -10**18.

Let's write the code accordingly.

We'll also test on the samples.

After implementing, we should run on the samples to verify.

## worker: Implement the tree DP in Python: read input, build
The solution uses a post‑order tree DP with state tracking. For each node we compute:

* `g[u]`: best size of a partial alkane attached to the parent (can be a leaf of size 1 or an internal node with three child branches).
* `use_int[u]`: same as `g[u]` but guaranteed to contain at least one internal vertex (only possible when the node has ≥ 3 children and uses the internal case).
* `down0[u]`: best alkane completely inside the subtree where the topmost node `u` is a leaf (needs one child branch that already has an internal vertex).
* `down4[u]`: best alkane completely inside the subtree where the topmost node `u` is internal (needs four child branches).
* `best[u]`: the maximum alkane size wholly contained in `u`’s subtree, also considering the best from any child.

The answer is the maximum `best[u]` over all nodes. If this maximum is 0, no valid alkane exists and we output ‑1. The DP runs in \(O(N \log N)\) time due to sorting the child values (worst‑case star graph) and uses \(O(N)\) memory. The iterative DFS avoids recursion depth problems for \(N\le2\times10^5\).

## worker: Build the Python program: read input, construct ad
The algorithm uses a post-order tree DP. For each node we compute:
- `g[u]`: best size of a partial alkane attached to its parent (either a leaf of size 1 or an internal node using three child branches).
- `use_int[u]`: same as `g[u]` but guaranteed to contain an internal vertex (only possible when the node has ≥ 3 children and uses the internal case).
- `down0[u]`: best alkane completely inside the subtree where the top node is a leaf (requires one child branch that already has an internal vertex).
- `down4[u]`: best alkane completely inside the subtree where the top node is internal (requires four child branches).
- `best[u]`: the best alkane wholly contained in the subtree, also taking the maximum from any child.

The answer is the maximum `best[u]` over all nodes; if it is 0, no valid alkane exists and we output -1. The DP runs in \(O(N \log N)\) time due to sorting child values (worst‑case star) and uses \(O(N)\) memory. The iterative DFS avoids recursion depth issues for \(N\le2\times10^5\).

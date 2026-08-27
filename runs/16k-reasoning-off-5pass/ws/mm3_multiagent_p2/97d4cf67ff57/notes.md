
## ideation
We need to find a connected subgraph (subtree) of the given tree where every vertex has degree 1 or 4, and at least one vertex has degree 4. This is a maximum size "alkane" subgraph problem.

Key observations:
- The subgraph must be connected.
- Degrees are restricted to 1 (leaves) or 4 (internal).
- At least one degree-4 vertex is required.

We can solve it with tree DP. Root the tree at node 1. For each node `u`, compute DP values for three states:
- `dp[u][0]`: max vertices in a valid component inside `u`'s subtree where `u` is not included.
- `dp[u][1]`: max vertices in a valid component inside `u`'s subtree where `u` is included and has degree 1 (leaf). This component contains `u` and connects to its parent via exactly one edge.
- `dp[u][4]`: max vertices in a valid component inside `u`'s subtree where `u` is included and has degree 4 (internal). This component connects to its parent via exactly one edge (if parent is included) or is the root of the component.

Transitions:
- `dp[u][0] = sum of max(dp[child][0], dp[child][1], dp[child][4])` for all children.
- For `dp[u][1]`: `u` is included as a leaf, so it can have at most 1 child attached. We need to pick the best child to attach (with state 1) and exclude others (state 0). `dp[u][1] = 1 + max over children of (dp[child][1] - max(dp[child][0], dp[child][1], dp[child][4])) + sum of max for all children`. Actually, simpler: try all children, for the chosen child use `dp[child][1]`, for others use `dp[child][0]`. Take the best.
- For `dp[u][4]`: `u` is included as internal, so it can have up to 4 children attached. But if `u` is the root of the component (no parent), it can have 4 children. If `u` is attached to its parent (parent uses degree 1 on `u`), then `u` can have up to 3 more children (total degree 4). To handle this uniformly, we can treat the parent edge as a "virtual child" that uses one degree slot. For `dp[u][4]`, if the parent is included and uses one degree on `u`, we can only attach 3 children. If `u` is the root of the component, we can attach 4 children. We can compute two values: `dp[u][4][free]` (can attach 4 children) and `dp[u][4][used]` (can attach 3 children because parent takes one slot). But we can simplify: we need to know how many slots are available.

Actually, we need to be careful: the state `dp[u][1]` means `u` has degree 1 in the component, so it connects to exactly one neighbor (its parent if it's not the root, or one child if it's the root). State `dp[u][4]` means `u` has degree 4, so it connects to exactly 4 neighbors. Since it's a tree, `u` can have at most 4 neighbors in the component. If `u` is attached to its parent, then it can have at most 3 children attached. If `u` is the root of the component (not attached to parent), it can have up to 4 children attached.

So we need DP values that also consider whether the parent edge is used. Let's define:
- `dp0[u]`: `u` not included.
- `dp1[u]`: `u` included, degree 1, so it has exactly one neighbor in the component. This neighbor could be its parent (if `u` is not the root of the component) or one of its children (if `u` is the root). In both cases, `u` uses exactly one of its incident edges in the component.
- `dp4[u]`: `u` included, degree 4, so it has exactly four neighbors. It uses all its incident edges up to 4. If the parent is also included, then the parent uses one slot, so `u` can attach at most 3 children. If the parent is not included, `u` can attach up to 4 children.

To avoid passing the "parent used" flag down, we can compute two versions for degree 4:
- `dp4_root[u]`: `u` is included as degree 4 and the parent edge is NOT used (so `u` is the top of the component). It can have up to 4 children attached.
- `dp4_child[u]`: `u` is included as degree 4 and the parent edge IS used. It can have up to 3 children attached.

For degree 1:
- `dp1_root[u]`: `u` is included as degree 1 and parent edge is NOT used. It must have exactly one child attached.
- `dp1_child[u]`: `u` is included as degree 1 and parent edge IS used. It has no children attached (since degree is 1 and parent already used it).

Then the answer is the maximum over all `u` of `dp1_root[u]` and `dp4_root[u]` (and possibly `dp4_child[u]`? No, because if parent is used, the component is not rooted at `u`. The root of the component is some node where the parent edge is not used. So we only consider roots: `dp1_root` and `dp4_root`. But also we could have a component where the root has degree 1 (so it's a leaf) and has no parent. That's fine. But we must have at least one degree-4 vertex. So we only consider `dp4_root[u]` for the answer, unless there is a component that is a single edge? That would have two vertices of degree 1, no degree 4, invalid. So indeed we need a degree-4 vertex. So we only care about components with at least one degree-4 vertex. That means the root could be degree 1 or degree 4. But if the root is degree 1, then the component must contain some degree-4 vertex deeper. So we need to consider both `dp1_root` and `dp4_root` as candidate answers, but we must ensure that the component actually contains a degree-4 vertex. However, our DP for `dp1_root` will naturally build a component that might not have any degree-4 vertex (e.g., a path of length 1). We need to check validity. But if the component has no degree-4 vertex, it's invalid. So we need to either:
- Only consider `dp4_root` as the answer (since any valid alkane has at least one degree-4 vertex, and that vertex could be the root).
- Or for `dp1_root`, ensure that the component contains a degree-4 vertex.

But wait: in a valid alkane, the root (the node where the parent edge is not used) could be a leaf. For example, a star with center degree 4 and 4 leaves: the root could be one of the leaves. In that case, the component has a degree-4 vertex (the center). So we do need to consider `dp1_root` as a candidate, but we must ensure that somewhere in the component there is a degree-4 vertex. This is tricky to track in DP because the state at `u` doesn't tell us if a degree-4 vertex exists deeper.

Alternative: We can compute DP values that also track a boolean: whether the component contains at least one degree-4 vertex. Let's define:
- `dp0[u]`: max vertices in a valid component in subtree of `u` where `u` is excluded.
- `dp1[u]`: max vertices in a valid component in subtree of `u` where `u` is included with degree 1, and the component has a degree-4 vertex (or we can store two values: with/without degree-4).
- `dp4[u]`: max vertices in a valid component in subtree of `u` where `u` is included with degree 4, and the component has a degree-4 vertex.

Actually, since degree-4 vertices are required, and the component is a tree, we can think of the DP as building subtrees. For a node `u` with degree 4, it automatically has a degree-4 vertex (itself). For a node `u` with degree 1, the degree-4 vertex must be in one of the child subcomponents that are attached (or there is none, in which case the component is just a path of length 1, which is invalid because no degree-4).

So for `dp1[u]`, we can compute two values:
- `dp1_no4[u]`: max vertices in a valid component rooted at `u` (degree 1, parent not used) that has NO degree-4 vertex.
- `dp1_yes4[u]`: max vertices in a valid component rooted at `u` (degree 1, parent not used) that has AT LEAST one degree-4 vertex.

Similarly, for `dp4[u]` (degree 4, parent not used), since `u` itself is degree 4, the component always has a degree-4 vertex. So we only need one value: `dp4_root[u]`.

For the child version (parent used):
- For degree 1 child: since it has no children, it cannot have a degree-4 vertex in its subtree unless it is itself degree 4, but it's degree 1. So `dp1_child[u]` is just 1 (itself) and it has no degree-4. But wait, if `u` is a leaf in the component, it has no children attached, so the component is just `{u}`. That has no degree-4 vertex. So if we attach a degree-1 child, that child contributes no degree-4 vertex.
- For degree 4 child: `u` is degree 4 and has parent used, so it can have up to 3 children. It automatically has a degree-4 vertex. But we might need to know if it has one (it does). So we don't need to track it separately.

But we also need to know when we attach children, whether the resulting component has a degree-4 vertex. For `dp1_root[u]`, we attach exactly one child. That child could be:
- degree 1 root: then no degree-4 (unless the child's subtree has one, but that child is degree 1 and has exactly one child attached, so it propagates the question down).
- degree 4 root: then the child itself is degree 4, so we have a degree-4.

So we need to propagate the "has degree-4" flag through the chain. This is doable with DP with two states (has4 / no4) for degree 1 components, and for degree 4 components we only care about the max size (since they always have a degree-4).

Let's define:
- `dp0[u]`: max vertices in a valid component in subtree of `u` where `u` is excluded.
- For degree 1, parent not used (root of component):
  - `dp1_root0[u]`: max size, no degree-4 vertex in component.
  - `dp1_root1[u]`: max size, at least one degree-4 vertex in component.
- For degree 1, parent used (attached to parent as leaf):
  - `dp1_child[u]`: max size of the component (which is just `{u}` since no children can be attached, because degree is 1 and parent takes the only edge). It has no degree-4. Size = 1.
- For degree 4, parent not used (root of component):
  - `dp4_root[u]`: max size. Always has degree-4 (at u).
- For degree 4, parent used (internal node attached to parent):
  - `dp4_child[u]`: max size. Always has degree-4 (at u). Can attach up to 3 children.

But wait, for `dp1_child[u]`, since `u` is a leaf in the component, it has no children attached. So the component is just the single vertex. Size = 1. No degree-4.

For `dp4_child[u]`, `u` is degree 4, one edge goes to parent, so it can have up to 3 children. It is itself degree 4, so the component has a degree-4 vertex.

Now, for the root states:
- `dp1_root0[u]`: `u` is degree 1, parent not used. It must attach exactly one child. The child can be:
  - `dp1_root0[child]`: contributes no degree-4.
  - `dp1_root1[child]`: contributes degree-4.
  - `dp4_root[child]`: contributes degree-4.
  - `dp4_child[child]`: but wait, if we attach a child as `dp4_child`, that means the child's parent edge is used. But the child's parent is `u`, so yes, that's exactly when we attach a degree-4 child. So `dp4_child[child]` is valid.
  - `dp1_child[child]`: if we attach a child as `dp1_child`, that means the child is a leaf attached to `u`. That child would have degree 1 (used by parent `u`), so it cannot have its own children. That's fine.
  - `dp0[child]`: child not included.

We want to pick the best child to attach. The rest of the children are excluded (`dp0`). So we need to compute for each child the "gain" of attaching it vs excluding it. For `dp1_root0`, we want the child that gives the best size, but we need to combine with the "has degree-4" flag. If we pick a child that gives no degree-4, the whole component has no degree-4. If we pick a child that gives degree-4, the whole component has degree-4.

So for `dp1_root0[u]` (no degree-4), we need to pick a child such that the child's component has no degree-4. The candidates are children that themselves can provide a component with no degree-4. That includes `dp1_child[child]` (size 1, no degree-4), `dp1_root0[child]` (if it exists), and maybe `dp0` (but that's excluding, not attaching). Also, if the child is attached as `dp4_root` or `dp4_child`, that would introduce a degree-4, so not allowed for `dp1_root0`.

Similarly, for `dp1_root1[u]`, we need to pick a child such that the child's component has at least one degree-4. Candidates: `dp1_root1[child]`, `dp4_root[child]`, `dp4_child[child]`. Or we could pick a child that is excluded, but then the component has only `u`, which has no degree-4. So we must attach a child that brings a degree-4.

This seems complicated. Maybe we can simplify by noting that the answer is just the maximum over all nodes of `dp4_root[u]` and `dp1_root1[u]`. And we can compute `dp1_root1[u]` by considering the best child that brings a degree-4, and the rest excluded. For `dp1_root0[u]`, we don't really care about it for the final answer, because we only care about components with at least one degree-4. However, we might need `dp1_root0` as a candidate for the child of a degree-1 node that is looking for a degree-4. Wait, if a degree-1 node is looking for a child that brings a degree-4, it will only consider children with degree-4. So it doesn't need to consider `dp1_root0` children for the "has4" case. But for the "no4" case, it might need `dp1_root0` to propagate the "no degree-4" flag when building a path. But again, for the final answer we only care about "has4". So maybe we can simplify: we only need to compute DP values for components that are "valid" (have at least one degree-4) and components that are "invalid" (no degree-4) but might be needed as subcomponents? Actually, if a component has no degree-4, it can only be used as a subcomponent of a larger component that eventually gets a degree-4. But the only way a degree-1 node can attach to a child without degree-4 and still have the whole component have a degree-4 is if some other child (or itself) has degree-4. But a degree-1 node only attaches one child. So if it attaches a child without degree-4, the whole component has no degree-4 (unless `u` itself is degree-4, but it's degree 1). So for a degree-1 node to be part of a valid alkane, the single child it attaches must contain a degree-4 vertex. So we only care about the "has4" case for degree-1 nodes. For degree-4 nodes, they always have degree-4, so any component rooted at a degree-4 node is valid (has at least one degree-4). So we don't need to track the "has4" flag at all for degree-4 nodes, and for degree-1 nodes we only care about the case where the attached child brings a degree-4. The "no4" case for degree-1 is never useful for building a valid alkane, because if a degree-1 node is attached as a leaf to a degree-4 parent, it contributes no children and no degree-4, which is fine. But if a degree-1 node is the root, it must have a child with degree-4. So we only need to compute the maximum size of a degree-1 root component that contains a degree-4 vertex. And for degree-4, we just compute the maximum size.

But we also need to consider that a degree-1 node could be attached as a child to a degree-4 parent. In that case, the degree-1 child is just a leaf, size 1, no children. So `dp1_child` is trivial: size 1, no children.

So the DP states we need:
- `dp0[u]`: max size of a valid component in subtree of `u` where `u` is excluded. (This can be used as "child not included")
- For `u` included:
  - As degree 1, parent edge used: `dp1_leaf[u] = 1`. (u is a leaf, no children attached)
  - As degree 1, parent edge not used: we need to attach exactly one child. The child must be attached in a way that the resulting component has a degree-4 vertex. So the child must be either:
    - degree 4 (root or child) -> provides degree-4
    - degree 1 (root) that itself attaches to a degree-4 somewhere -> provides degree-4
  So we need to compute `dp1_root[u]`: max size of a component rooted at `u` (degree 1, parent not used) that contains at least one degree-4 vertex.
  - As degree 4, parent edge used: `dp4_child[u]`. u has degree 4, one edge to parent, up to 3 children. It contains a degree-4 vertex (itself).
  - As degree 4, parent edge not used: `dp4_root[u]`. u has degree 4, up to 4 children. Contains a degree-4 vertex.

The answer is the maximum over all `u` of `dp1_root[u]` and `dp4_root[u]`. (Note: `dp1_root[u]` requires that the component has a degree-4, so it's already filtered. `dp4_root[u]` automatically has degree-4.)

Now, transitions:
For a node `u` with children `v1, v2, ..., vk`:
- `dp0[u] = sum over children of max(dp0[v], dp1_leaf[v], dp1_root[v], dp4_root[v], dp4_child[v])`. But wait, can a child be included in a way that doesn't connect to `u`? Yes, `dp0` means the child's component is entirely in the child's subtree and does not connect to `u`. So we can take the best of all possibilities for each child independently.
- `dp1_leaf[u] = 1`. (No children attached, because degree is 1 and parent already uses the edge.)
- `dp1_root[u]`: we need to pick exactly one child to attach. The attached child must provide a component that contains a degree-4 vertex and connects to `u`. The other children are excluded. The size is 1 (for `u`) + size of the attached child's component. The child's component can be:
  - `dp1_root[v]`: child is degree 1 root, its component has degree-4 somewhere.
  - `dp4_root[v]`: child is degree 4 root, has degree-4.
  - `dp4_child[v]`: child is degree 4 attached to `u` (parent used), has degree-4.
  Note: `dp1_leaf[v]` is a leaf attached to its parent, but here `u` would be the parent. So if we attach `v` as a leaf, `v` would have degree 1 and its parent edge used. That is exactly `dp1_leaf[v] = 1`. But that child would not bring a degree-4. So we cannot use `dp1_leaf` for `dp1_root` because then the whole component would have no degree-4 (since `u` is degree 1 and the only child is a leaf with no degree-4). So for `dp1_root`, we must use a child state that guarantees a degree-4 in that child's component. The states that guarantee a degree-4 are: `dp1_root` (if it is valid, i.e., the child's component has degree-4), `dp4_root`, `dp4_child`. So we need to compute the best gain for each child as: `gain[v] = max(dp1_root[v], dp4_root[v], dp4_child[v]) - max(dp0[v], dp1_leaf[v], dp1_root[v], dp4_root[v], dp4_child[v])`. Actually, we need to pick the best child to attach, and the others are excluded. So we compute the "value if attached" for each child (only those that have degree-4) and "value if excluded" (which is `dp0[v]` or any of the other states, but we want the best excluded value, which is the max over all states for that child). Wait, if we exclude a child, we can still have a component in its subtree, as long as it doesn't connect to `u`. So the best excluded value is `best_excluded[v] = max(dp0[v], dp1_leaf[v], dp1_root[v], dp4_root[v], dp4_child[v])`. But note that `dp1_leaf[v]` means `v` is a leaf attached to `u`, so it connects to `u`. If we exclude `v`, we cannot use `dp1_leaf[v]` because that would mean `v` is attached to `u`. So actually, if we want to exclude `v`, the component in `v`'s subtree must not connect to `u`. The states that do not connect to `u` are: `dp0[v]`. The states that connect to `u` are: `dp1_leaf[v]` (attached to `u` as leaf), `dp1_root[v]` (attached to `u` as parent? Wait, `dp1_root[v]` means `v` is degree 1 and its parent edge is not used. So if we attach it to `u`, `u` is the parent. So `dp1_root[v]` connects to `u` if we choose to attach it. So it is a "connected" state. `dp4_root[v]` connects to `u` if attached. `dp4_child[v]` connects to `u` (parent used). So for exclusion, we can only use `dp0[v]`. For inclusion (attaching), we can use `dp1_leaf[v]`, `dp1_root[v]`, `dp4_root[v]`, `dp4_child[v]`. But for `dp1_root[u]`, we need to attach exactly one child, and that child must provide a degree-4. So we consider attaching a child with a state that has a degree-4: `dp1_root[v]` (if it has degree-4), `dp4_root[v]`, `dp4_child[v]`. The other children are excluded (state `dp0`). So `dp1_root[u] = 1 + max over children of (best_with4[v] - dp0[v]) + sum over children of dp0[v]`, where `best_with4[v] = max(dp1_root[v], dp4_root[v], dp4_child[v])`. We take the maximum gain. If no child provides a degree-4, then `dp1_root[u]` is invalid (or we could say it's -inf). But actually, we could also consider that the degree-4 might be in `u`? No, `u` is degree 1. So if no child brings a degree-4, the component is just `u` and a leaf, which is a path of length 1, no degree-4. So invalid.

- `dp4_child[u]`: `u` is degree 4, parent edge used. So `u` can attach up to 3 children. The children can be in any state that connects to `u` (i.e., `dp1_leaf`, `dp1_root`, `dp4_root`, `dp4_child`) as long as the total number of attached children ≤ 3. The rest are excluded (`dp0`). Also, we need to ensure that the component is valid (has at least one degree-4). Since `u` is degree 4, it always has a degree-4. So we just need to maximize the total size: 1 (for `u`) + sum over children of (best_including[v] or dp0[v]). For each child, we have a "gain" if we attach it: `gain_attach[v] = max(dp1_leaf[v], dp1_root[v], dp4_root[v], dp4_child[v]) - dp0[v]`. Note: `dp1_leaf[v]` is allowed. We can attach up to 3 children. So we need to pick the top 3 gains (positive or negative? Actually, we can attach fewer than 3. If we attach a child, we use one of the 3 slots. If we don't attach, we use 0 slots. The best is to take the top 3 positive gains? Actually, we can attach any subset of children, up to 3. The optimal is to take the children with the highest gains, but we can take at most 3. So we sort gains descending and take the first 3 (or fewer if not enough positive). But we must also consider that some gains might be negative (attaching the child reduces total size compared to excluding it). In that case, we might not want to attach it. But we can attach 0, 1, 2, or 3 children. The maximum will be obtained by taking the top 3 gains that are positive, or all available if less than 3. Actually, if a gain is negative, attaching that child is worse than excluding it. So we should only attach children with positive gain. But wait, what if all gains are negative? Then we attach 0 children, and `dp4_child[u] = 1 + sum dp0[v]`. That's fine.
  However, there is a catch: for `dp1_root[v]`, it requires that the child's component has a degree-4. But in the context of `dp4_child[u]`, if we attach a child as `dp1_root`, that child is a degree-1 root. But its parent is `u`, so the child is attached to `u`. The child's parent edge is used, so the child is actually `dp1_child`? No, `dp1_root` means the child's parent edge is not used. But if we attach it to `u`, then the child's parent edge is used. So we cannot use `dp1_root` when the child is attached to a parent. We need a state for the child where the parent edge is used. So for attaching a child, we need to use the child's state where the edge to `u` is used. That is:
  - For child degree 1: `dp1_child[v]` (which is just 1, leaf attached to parent).
  - For child degree 4: `dp4_child[v]` (parent edge used).
  What about `dp1_root`? If we attach a child as `dp1_root`, that means the child's parent edge is not used. But if we are attaching it to `u`, then the edge to `u` is used. Contradiction. So we cannot use `dp1_root` when the child is attached to a parent. Similarly, `dp4_root` cannot be used when attached to a parent.
  Ah! This is a crucial point. The state must reflect whether the edge to the parent is used or not. So when we attach a child to `u`, the child must be in a state where the parent edge is used. The only such states are `dp1_child` and `dp4_child`. For exclusion, the child is in `dp0` (no connection to `u`).
  But then, how do we get a degree-4 vertex in a component that is rooted at some node? If the root is degree 1, it must attach a child. That child is attached to the root, so the child's parent edge is used. So the child must be in a state that has parent used. So the child must be either `dp1_child` or `dp4_child`. If the child is `dp1_child`, it's a leaf, no degree-4. If the child is `dp4_child`, it is degree 4, so we have a degree-4. So for a degree-1 root, the only way to get a degree-4 is to attach a child that is `dp4_child`. And that child can further attach grandchildren, but those grandchildren would be attached to the `dp4_child` node, so they would use the parent edge (the edge to the `dp4_child` node). So the states propagate.
  Therefore, the "root" state (parent not used) can only be at the top of the component. All other nodes in the component have their parent edge used. So the component is a tree rooted at some node (the root of the component). The root has no parent. Its children have parent used. So we only need two sets of DP values:
  - For a node `u` when the edge to its parent is NOT used (i.e., `u` is the root of a component): `root1[u]` and `root4[u]`.
  - For a node `u` when the edge to its parent IS used (i.e., `u` is attached to its parent in the component): `child1[u]` and `child4[u]`.
  This is much cleaner! And we don't need `dp0` for the "excluded" case in the same way? Actually, we still need a way to say that a child is not included in the component. But if the child is not included, then there is no connection to `u`. So we need a DP for "not included". Let's call it `none[u]`. This is the best we can do in the subtree of `u` if `u` is not connected to its parent. It can be any valid component (or empty) that doesn't use the edge to the parent. But wait, if `u` is not included, then its children might be included in components that don't connect to `u`. So we need to define `none[u]` as the maximum size of a valid alkane subgraph in the subtree of `u` that does not include `u` and does not use the edge (u, parent). Actually, if `u` is not included, then the edge to parent is not used. So `none[u]` is simply the sum over children of the maximum of their "not connected to parent" states. But the children can be in any state that doesn't connect to `u`. If a child is not connected to `u`, then the child is effectively in its own component, and the edge to `u` is not used. So for the child, this is exactly the "parent not used" case. But wait, if the child is in a state where the parent is not used, that means the child is the root of its own component. And that component does not connect to `u`. So the child's state is either `root1`, `root4`, or the child is not included (which is `none` for the child). So actually, we can unify: the "parent not used" states are: `root1[u]`, `root4[u]`, and `none[u]`. But `none[u]` is just the sum of the best "parent not used" states of its children. So we can compute `none[u] = sum over children of max(root1[v], root4[v], none[v])`. And we can use that as the base.

So the DP states are:
- `root1[u]`: max size of a valid alkane component in the subtree of `u` such that `u` is the root, has degree 1, and the component contains at least one degree-4 vertex. (Invalid if no such component.)
- `root4[u]`: max size of a valid alkane component in the subtree of `u` such that `u` is the root, has degree 4. (Automatically has degree-4.)
- `child1[u]`: max size of a valid alkane component in the subtree of `u` such that `u` is attached to its parent (edge used), `u` has degree 1. Since the edge to parent is used, `u` has no other edges in the component. So `u` is a leaf. The component is just `{u}`. Size = 1. It has no degree-4 vertex (unless the rest of the component has one, but `u` is a leaf, so the rest of the component is above `u`, not in its subtree). So `child1[u] = 1`. It is always valid? But if we attach `u` as a child1 to a parent, the parent might be degree-4, so the whole component has a degree-4. So `child1[u]` is just the size 1, and it doesn't affect the "has degree-4" flag because the parent is the one that has the degree-4 or not. Actually, from the perspective of the parent's DP, when it attaches a child, it doesn't need to know if the child's subtree has a degree-4, because the parent (if degree-4) already provides one. If the parent is degree-1, then it needs the child to provide a degree-4. But in that case, the child cannot be `child1` because that would not provide a degree-4. So `child1` is only useful when attached to a degree-4 parent. So we can just define `child1[u] = 1` (size).
- `child4[u]`: max size of a valid alkane component in the subtree of `u` such that `u` is attached to its parent (edge used), `u` has degree 4. It can attach up to 3 children (since one edge is used by parent). The component always has a degree-4 (at `u`). So we just compute the max size: 1 + best sum of up to 3 children attached. The children can be in states: `child1`, `child4`, or `none` (excluded). Note: they cannot be `root1` or `root4` because those assume the parent edge is not used. If we attach a child, the edge to `u` is used, so the child must be in a "parent used" state. So the valid states for a child attached to `u` are: `child1` and `child4`. And for excluded children, they are in `none`.

So transitions:
For a node `u` with children `v1..vk` (in the rooted tree):
- `none[u] = sum_i max(root1[vi], root4[vi], none[vi])`. (Each child independently can form a component in its subtree that doesn't connect to `u`.)
- `child1[u] = 1`. (Leaf, no children attached.)
- `child4[u] = 1 + sum_i none[vi] + sum of top 3 gains, where gain_i = max(child1[vi], child4[vi]) - none[vi]`. We can attach up to 3 children. We take the best 3 children to attach (those with positive gain). If a gain is negative, we don't attach that child. So we sort gains descending, take the first 3 (or fewer if there are less than 3 children), and add to the base sum of `none[vi]`.
- `root1[u]`: `u` is degree 1, root. It must attach exactly 1 child. The child must be attached, so it must be in a "parent used" state. The only such state that can provide a degree-4 is `child4[vi]` (since `child1` provides no degree-4). So we need to pick exactly one child to attach as `child4`, and the other children must be `none`. So `root1[u] = 1 + max_i (child4[vi] - none[vi]) + sum_i none[vi]`. We take the child with the maximum `child4[vi] - none[vi]`. If no child has `child4[vi]` valid (i.e., no child can form a degree-4 component), then `root1[u]` is invalid (-inf). Note: `child4[vi]` is always valid (since `u` is degree 4, we can always form a component with just `u` and no children? Wait, if `vi` is a child, `child4[vi]` means `vi` is degree 4 and has parent used. But can `child4[vi]` be just `vi` alone? Yes, if `vi` has no children attached, then `child4[vi] = 1 + sum none[grandchildren]`. But wait, if `vi` is a leaf in the original tree, then it has no children. `none[vi] = 0` (since no children). `child1[vi] = 1`. `child4[vi]`: `vi` can attach up to 3 children, but it has none. So `child4[vi] = 1 + 0 = 1`. So a leaf can be `child4`? That would mean the leaf is degree 4 in the component, but it has no children. That's impossible because degree 4 means it must have 4 neighbors. If it's a leaf in the original tree, it only has one neighbor (its parent). So it cannot have degree 4. So `child4[vi]` for a leaf should be invalid! We missed this.
  Indeed, the degree in the subgraph cannot exceed the degree in the original tree. For a node `u` to have degree 4, it must have at least 4 neighbors in the original tree. So if `deg(u) < 4`, then `root4[u]` and `child4[u]` are invalid. For degree 1, we need at least 1 neighbor (always true except isolated, but it's a tree). So we must check the original degree.
  Also, for `root1[u]`, `u` must have at least 1 neighbor to attach a child. So if `u` is a leaf in the original tree, `root1[u]` is invalid (cannot attach a child because it has no children in the rooted tree? Wait, in the rooted tree, a leaf has no children. But it has a parent. If `u` is the root of the component, the parent is not used. So `u` must attach a child to have degree 1. But it has no children. So it would have degree 0. So `root1[u]` is invalid. However, `u` could be attached as `child1` to its parent. That's fine.
  So we need to incorporate the original degree constraint.
  - `root4[u]` is valid only if `deg(u) >= 4`. And we can attach up to 4 children.
  - `child4[u]` is valid only if `deg(u) >= 4`. And we can attach up to 3 children (since one is used by parent).
  - `root1[u]` is valid only if `deg(u) >= 1` (which is always true for N>=1) and it has at least one child in the rooted tree to attach. If `u` is a leaf in the rooted tree (no children), then it cannot attach any child, so `root1[u]` is invalid. But it could be `child1` (attached to parent).
  Also, for `child1[u]`, it's always valid (size 1), but it requires that `u` has degree at least 1? Actually, if `u` is a leaf, it can be `child1` (attached to parent). That's fine.

So let's add original degree checks:
- `root4[u]`: if `deg(u) < 4`, then `root4[u] = -inf`. Else compute: `root4[u] = 1 + sum none[vi] + sum of top 4 gains`, where gains are `max(child1[vi], child4[vi]) - none[vi]`. We can attach up to 4 children. (Note: `child1` is allowed, `child4` is allowed. But wait, can we attach a child as `child1`? That child would have degree 1 and parent used. That's fine. But does `child1` require the child to have at least 1 neighbor? Yes, but it's a tree, so it has at least the parent. So `child1` is always valid for any child (size 1). However, if we attach a child as `child4`, that child must have `deg >= 4`. So the gain for attaching as `child4` is only available if `deg(vi) >= 4`. We should take the max over available states. So `gain_i = max(child1[vi], (child4[vi] if deg(vi)>=4 else -inf)) - none[vi]`. Actually, we can just precompute for each child the best attached value, and compare to none. But we must be careful: if `deg(vi) < 4`, then `child4[vi]` is invalid, so we can only use `child1[vi]` (which is 1). So the gain is `1 - none[vi]`. That's fine.
- `child4[u]`: if `deg(u) < 4`, then `child4[u] = -inf`. Else compute: `child4[u] = 1 + sum none[vi] + sum of top 3 gains`. Same gains.
- `root1[u]`: if `u` has no children in the rooted tree (i.e., `u` is a leaf), then `root1[u] = -inf`. Else, we need to attach exactly one child. The child must be attached in a way that provides a degree-4. That means the child must be `child4` (since `child1` provides no degree-4). And `child4` requires `deg(child) >= 4`. So we pick the best child that has `deg >= 4` and `child4[vi]` is valid. So `gain_i = child4[vi] - none[vi]`. We take the max over children of this gain. If no such child, `root1[u] = -inf`. So `root1[u] = 1 + sum none[vi] + max_i (child4[vi] - none[vi])`.

Wait, is it correct that for `root1[u]`, the only way to get a degree-4 is if the attached child is `child4`? What if the attached child is `root1`? No, because the child is attached to `u`, so the child's parent edge is used. So the child must be in a "parent used" state. The only "parent used" states are `child1` and `child4`. `child1` has no degree-4. So yes, it must be `child4`.

What about the case where the root is degree 4 and has 4 children, one of which is degree 1 and that degree 1 child attaches a degree 4 grandchild? That's handled: the degree 1 child is `root1` (or `child1`? Wait, if the degree 1 child is attached to the root, then the child's parent edge is used. So the child is `child1` if it is a leaf, or if it has its own children, it would be `root1`? No, if the child has its own children, then the child is not a leaf. The child has degree 1 in the component, and its parent is the root. So the child's parent edge is used. So the child is in a "parent used" state. But we don't have a state for "parent used, degree 1, but has children". Because if a node has degree 1 and the parent edge is used, it has no other edges. So it cannot have children. So a degree-1 node with children must be the root of the component (parent not used). So in a valid alkane, the degree-1 nodes are either leaves (no children) or roots (no parent). So the only degree-1 nodes with children are roots. So in the DP, a node with children can only be degree 4 or degree 1 root. So if a degree-1 node is attached to a parent, it must be a leaf. So our states are correct: `child1` is a leaf, no children. `root1` has exactly one child. So in the tree, if we see a degree-1 node in the component that has children in the original tree, it must be the root of the component. So our DP captures that.

So the DP seems correct. Let's test on a simple example.
Sample 1:
Tree:
1-2, 2-3, 3-4, 2-6, 2-7, 3-8, 3-9
Root at 1.
Degrees:
1:1, 2:4, 3:4, 4:1, 6:1, 7:1, 8:1, 9:1
We expect answer 8.

Let's compute bottom-up.
Leaves: 4,6,7,8,9. deg=1.
For a leaf (say 4): no children (except parent 3). In rooted tree, 4 has no children.
none[4] = 0.
child1[4] = 1.
child4[4] = -inf (deg<4).
root1[4] = -inf (no children to attach).
root4[4] = -inf.
Now node 3: children 4,8,9. deg(3)=4.
none[3] = sum max(root1, root4, none) for 4,8,9. All are -inf or 0? For 4: max(-inf, -inf, 0) = 0. So none[3] = 0.
child1[3] = 1.
child4[3]: deg>=4. Gains for 4,8,9: each child: child1=1, none=0. So gain=1-0=1. We can attach up to 3 children. So we take top 3 gains: 1+1+1=3. So child4[3] = 1 + sum none (0) + 3 = 4. (This is the star: center 3, leaves 4,8,9. Size 4.)
root1[3]: has children. Need to attach one child as child4. But child4[4] is -inf. So no child can be child4. So root1[3] = -inf.
root4[3]: deg>=4. Gains: 1 each, take top 4: but only 3 children, so gain sum = 3. root4[3] = 1 + 0 + 3 = 4.
Now node 2: children 3,6,7. deg(2)=4.
none[2] = max for 3: max(-inf, 4, 0) = 4. For 6,7: 0. So none[2] = 4+0+0=4.
child1[2] = 1.
child4[2]: gains: for 3: child4[3]=4, none[3]=0, gain=4. child1[3]=1, gain=1. So max is 4. For 6,7: gain=1. So gains: 4,1,1. Top 3: 4+1+1=6. child4[2] = 1 + sum none (4) + 6 = 11? Wait, sum none is 4. So child4[2] = 1+4+6=11. But we can't attach all three children because child4 can only attach up to 3 children. We have 3 children, so we can attach all. The total size would be 1 (node 2) + size of child 3's component (4) + 1+1=7? Actually, child4[3] is 4 (star at 3). If we attach 3, we get 1 (2) + 4 (3) = 5. Then attach 6 and 7 as child1 (leaves), we get 2 more, total 7. So child4[2] should be 1 + none[3] (0? no, none[3]=0) + child4[3] (4) + child1[6] (1) + child1[7] (1) = 1+0+4+1+1=7. Wait, my sum none was 4, which is max of root4[3] (4) and none[3] (0). But if we attach 3, we use child4[3]=4, not none[3]. So the base sum should be sum of none[vi] for excluded children, and for attached children we add the gain. So for child4[2], we consider attaching 3,6,7. The base sum is sum none[vi] = none[3] + none[6] + none[7] = 0+0+0=0. Then we add gains for attached children. We can attach up to 3. The gains: for 3: max(child1, child4) - none = max(1,4)-0=4. For 6: 1-0=1. For 7: 1-0=1. Top 3: 4+1+1=6. So child4[2] = 1 + 0 + 6 = 7. That is correct.
root1[2]: has children. Attach one child as child4. The child4 values: for 3: 4, gain 4. For 6: -inf, for 7: -inf. So best child4 is 3 with gain 4. So root1[2] = 1 + sum none[vi] + 4 = 1+0+4=5. (This is 2 attached to 3, and 3 is star with 4,8,9. But 2 is root1, so it has degree 1. It attaches 3. 3 is child4, so it can have up to 3 children. 3 attaches 4,8,9. Total vertices: 2,3,4,8,9 = 5. But we also have 6 and 7 excluded. So size 5.)
root4[2]: deg>=4. Gains: for 3: 4, for 6:1, for 7:1. Top 4: we have 3 children, so sum=6. root4[2] = 1 + sum none (0) + 6 = 7. This is the whole star centered at 2: 2,3,4,6,7,8,9? Wait, 2 is root4, can attach up to 4 children. It attaches 3,6,7. But 3 is child4, which already includes its children 4,8,9. So total: 2,3,4,6,7,8,9 = 7 vertices. But sample answer is 8. The sample subgraph has 1,2,3,4,6,7,8,9. That's 8 vertices. How do we get 8? That subgraph has 2 as degree 4, 3 as degree 4, and leaves 1,4,6,7,8,9. So 2 and 3 are both internal. In our DP, 2 is root4, and it attaches 3 as child4. But 3 as child4 can have up to 3 children. In the sample, 3 has children 4,8,9 (3 children) and also connects to 2? Wait, in the sample subgraph, 2 and 3 are connected. So 3's degree is 4: it connects to 2,4,8,9. So 3 has parent 2, and children 4,8,9. That's exactly child4: parent used, can attach up to 3 children. So child4[3] with children 4,8,9 attached: size = 1 (3) + 3 (leaves) = 4. Then root4[2] attaches 3 (child4, size 4) and also attaches 1,6,7. But wait, 1 is the parent of 2 in our rooted tree! In our rooted tree, 2's parent is 1. So 1 is not a child of 2. In the sample, 1 is a leaf attached to 2. But in our rooted tree, 1 is the parent. So to get 1 in the component, 2 must be attached to 1, or 1 must be attached to 2? Since 1 is the parent, if we want 1 in the component, we can either make 2 the root and attach 1 as a child? But 1 is the parent, so if 2 is the root, the edge to 1 is the parent edge, which is not used. So we cannot attach 1 as a child if 2 is root. Alternatively, we can make 1 the root. Let's see: if we root at 1, then 1 is the root. 1 has child 2. In the sample, 1 is a leaf, so it should be degree 1. So 1 could be root1, attaching 2 as child4. Then 2 is child4, attaching 3,6,7. 3 is child4, attaching 4,8,9. So the component is rooted at 1. That would be root1[1] = 1 + sum none[2] + max child4[2] - none[2]. Let's compute that.

We need to compute node 1: children: only 2. deg(1)=1.
none[1] = max(root1[2], root4[2], none[2]) = max(5,7,4) = 7.
child1[1] = 1.
child4[1] = -inf.
root1[1]: has child 2. Attach one child as child4. child4[2]=7. none[2]=4. Gain = 7-4=3. So root1[1] = 1 + none[2] + 3 = 1+4+3=8.
root4[1] = -inf.
So the answer is max over all root states: root1[1]=8, root4[2]=7, etc. So max is 8. That matches sample 1.

So the DP works. We just need to implement it carefully.

Complexities:
- For each node, we need to sort the gains to pick top 3 or 4. Since the number of children can be large, we can do this in O(deg log deg) per node, total O(N log N). N=2e5, that's fine.
- We need to handle invalid states. We can use -infinity for invalid. Since sizes are at most N, we can use -1e9 or -10**9.
- We need to compute original degrees. We can do that by counting edges.

Implementation details:
- Root the tree at 1 (or 0-indexed). Use adjacency list.
- Do a DFS post-order.
- For each node, compute:
  - `none[u]`: sum of `max(root1[v], root4[v], none[v])` for children v.
  - `child1[u] = 1`.
  - `child4[u]`: if `deg(u) < 4` then -inf else:
      - For each child, compute `best_attached = max(child1[v], child4[v])` (child4[v] might be -inf).
      - `gain = best_attached - none[v]`.
      - Sort gains descending, take first 3.
      - `child4[u] = 1 + sum_none + sum(top 3 gains)`.
  - `root1[u]`: if no children, -inf. Else:
      - For each child, if `child4[v]` is valid (i.e., not -inf), `gain = child4[v] - none[v]`.
      - Take max gain.
      - If no such child, -inf.
      - `root1[u] = 1 + sum_none + max_gain`.
  - `root4[u]`: if `deg(u) < 4` then -inf else:
      - Similar to child4 but take top 4 gains.
      - `root4[u] = 1 + sum_none + sum(top 4 gains)`.

Note: For `root1[u]`, we only consider children that can be `child4`. But what if the child is `root1`? No, because the child is attached to `u`, so it must be in "parent used" state. So `child4` is correct.
But wait: what if the child is `root4`? That would mean the child's parent edge is not used. But if we attach it to `u`, the edge to `u` is used. So we cannot use `root4` when the child is attached. So we must use the "parent used" version. So the child must be `child4`. And `child4` requires `deg(child) >= 4`. So the child must have degree at least 4 in the original tree. So only those children can be used to provide the degree-4 for a degree-1 root. That makes sense: a degree-1 node must attach to a degree-4 node, because the only way to have a degree-4 in the component is if some node has degree 4. If the root is degree 1, the degree-4 must be in the subtree. The immediate child of the root is the only node that can have degree 4? Not necessarily: the degree-4 could be deeper. For example, a chain: root (deg1) - A (deg1) - B (deg4) - ... But in that case, the root attaches A. A is degree 1. A attaches B. B is degree 4. So the immediate child of the root is A, which is degree 1. So the root's child is not degree 4. In our DP, for `root1[u]`, we require the immediate child to be `child4`. That would only work if the immediate child is degree 4. But in the chain example, the immediate child is degree 1, not degree 4. So our DP would fail to capture that! Let's check: root u (deg1), child v (deg1), v has child w (deg4). In the component, u is root1, v is child1? No, v is degree 1 and has a child w. So v cannot be child1 because child1 has no children. v must be root1? But v is attached to u, so v's parent edge is used. So v must be in a "parent used" state. But v has a child. The only "parent used" state that allows children is `child4` (since `child1` is a leaf). So v must be `child4`. But v is degree 1! So v cannot be `child4`. So this configuration is impossible in our DP. But is it possible in reality? Let's think: a degree-1 node with a child in the component. That means the degree-1 node has two incident edges in the component: one to its parent, one to its child. That would make its degree 2, not 1. So it's impossible! In a tree, the sum of degrees is 2*(V-1). A vertex with degree 1 is a leaf. A leaf has exactly one incident edge. So if a vertex has degree 1 in the subgraph, it cannot have any other edges. So it cannot have children. So the chain example is invalid: if u is degree 1, it has exactly one neighbor. That neighbor cannot be degree 1 and have another neighbor, because that would give the middle vertex degree 2. So indeed, in an alkane, the degree-1 vertices are leaves. They have no children in the component. So our DP is correct: a degree-1 node with a parent (child1) has no children. A degree-1 node without a parent (root1) has exactly one child, and that child must be degree 4 (since the child has the parent edge used, so it must be in a "parent used" state; and to have children, it must be degree 4, because degree 1 with parent used is a leaf). So the only way to have a degree-4 vertex in a component with a degree-1 root is that the child of the root is degree 4. That degree 4 node can then have its own children, which can be degree 1 leaves or degree 4 nodes, etc. So the structure is: a degree-1 root can only attach to a degree-4 node. That degree-4 node can attach to degree-1 leaves or further degree-4 nodes. So our DP correctly enforces that.

Let's verify with a path: 1-2-3-4. No degree-4, so invalid. Our DP: leaves: child1=1, child4=-inf, root1=-inf, root4=-inf. Node 2: children 3,4. none[2] = 0+0=0. child4: -inf. root1: needs child4, but none have child4. So -inf. So no valid alkane. Correct.

What about a star: center 1, leaves 2,3,4,5. deg(1)=4. Leaves: child1=1, root1=-inf. Node 1: none=0. child4: -inf. root1: -inf. root4: deg>=4, gains: 1 each, top 4: 4. root4[1]=1+0+4=5. Correct.

What about two degree-4 nodes connected: 1-2, with 1 having leaves 3,4,5 and 2 having leaves 6,7,8. deg(1)=4, deg(2)=4. Root at 1. Leaves: child1=1. Node 2: children 6,7,8. none[2]=0. child4[2] = 1+0+3=4. root4[2] = 1+0+3=4. Node 1: children 2,3,4,5. none[1] = max(root4[2], none[2]) = 4. child4[1]: gains: for 2: child4[2]=4, none[2]=0, gain=4. For 3,4,5: gain=1. Top 3: 4+1+1=6. child4[1]=1+0+6=7? Wait, sum none is 0? But we have 4 children. none[1] is sum of max for each child. For 2: max(root1[2], root4[2], none[2]) = 4. For 3,4,5: 0. So sum none = 4+0+0+0=4. Then child4[1] = 1 + 4 + top 3 gains. The gains: for 2: 4-0=4. For 3: 1-0=1. For 4:1. For 5:1. Top 3: 4+1+1=6. So child4[1] = 1+4+6=11. But we can only attach up to 3 children. The base sum includes the best excluded value for all children. If we attach 2, we add its gain (4). The base sum already includes the best excluded value for 2, which is none[2]=0? Wait, in the sum none, we used the best of root1, root4, none for each child. For child 2, the best excluded value is root4[2]=4. So none[1] includes 4 from child 2. But if we attach child 2 as child4, we are not using the excluded value; we are using the attached value. So we should not add the excluded value for attached children to the base sum. The correct way: base sum = sum of none[vi] for all children. Then for each child we attach, we add the gain (attached - none). So base sum should be sum of none[vi]. For child 2, none[2]=0. For 3,4,5, none=0. So base sum = 0. Then we add gains: for 2: child4[2] - none[2] = 4-0=4. For 3: 1-0=1, etc. Then child4[1] = 1 + 0 + sum of top 3 gains = 1+4+1+1=7. That is correct: the component is 1,2,3,4,5,6,7,8? Wait, 1 attaches 2,3,4,5. 2 is child4, so it can have up to 3 children. It attaches 6,7,8. So total: 1,2,3,4,5,6,7,8 = 8 vertices. But child4[1] = 7? That's 1 (node 1) + child4[2] (4) + child1[3] (1) + child1[4] (1) + child1[5] (1) = 7? Wait, 1+4+1+1+1=8. But my sum was 1+0+4+1+1=7. I forgot to add the 1 for node 1? The formula is `1 + sum_none + sum_gains`. Here `1` is for node 1. `sum_none` is 0. `sum_gains` is top 3 gains: for 2: 4, for 3:1, for 4:1 (we take top 3). So sum_gains=6. Total = 1+0+6=7. But we have 4 children, and we are attaching 3 of them. The gains are attached - none. The attached values: for 2: child4[2]=4, for 3: child1[3]=1, for 4: child1[4]=1. The none values: for 2: none[2]=0, for 3: none[3]=0, for 4: none[4]=0, for 5: none[5]=0. So total = 1 + (none[2]+none[3]+none[4]+none[5]) + (child4[2]-none[2]) + (child1[3]-none[3]) + (child1[4]-none[4]) = 1 + 0 + 4-0 + 1-0 + 1-0 = 7. But that misses the node 5? Because we are only attaching 3 children. The 4th child (5) is excluded, so it contributes none[5]=0. So total vertices = 1 (node1) + 4 (subtree of 2) + 1 (node3) + 1 (node4) = 7. But we have 8 vertices in the component: nodes 1,2,3,4,5,6,7,8. That's 8. Why is the DP giving 7? Because we only attached 3 children, but we have 4 children. We attached 2,3,4. Node 5 is excluded. But in the real component, we can attach 4 children. Our `child4[1]` can attach up to 3 children? Wait! `child4[1]` means node 1 is degree 4 and has parent used. So it can attach up to 3 children. It has 4 children in the original tree. It can only use 3 of them. So if we want to include node 5, we would have to not use one of the others. But the maximum size might be achieved by using 3 children, or maybe using a different child? But we have 4 children. The sum of gains: for 2: 4, for 3,4,5: 1. The top 3 gains are 4,1,1. That gives 6. Total 7. If we attach all 4, we can't because we only have 3 slots. So the maximum is indeed 7? But the component with 8 vertices has node 1 connecting to 2,3,4,5. That's 4 children. So node 1 has degree 4. But node 1 has a parent? In our rooted tree, node 1 is the root, so it has no parent. So node 1 is `root4`, not `child4`. For `root4`, we can attach up to 4 children. So we need to check `root4[1]`. Let's compute `root4[1]`: deg(1)=4. Base sum = sum none[vi] = 0. Gains: for 2: 4, for 3:1, 4:1, 5:1. Top 4: 4+1+1+1=7. root4[1] = 1 + 0 + 7 = 8. That gives 8. So the maximum is 8, from `root4[1]`. So the answer is 8. That matches the component.

So the DP works: we must consider both `root1` and `root4` for the answer. And for `child4` we only have 3 slots.

So the algorithm is:
1. Read N and edges.
2. Build adjacency list.
3. Compute degree of each node.
4. Root the tree at 1 (or 0). Do a DFS to get parent and children order.
5. Process nodes in post-order.
6. For each node u:
   - `sum_none = 0`
   - For each child v:
     - `sum_none += none[v]`
   - `none[u] = sum_none + sum over children of (max(root1[v], root4[v]) - none[v])`? Wait, earlier we said `none[u] = sum max(root1[v], root4[v], none[v])`. But `max(root1[v], root4[v], none[v]) = none[v] + max(0, root1[v]-none[v], root4[v]-none[v])`. So we can compute that. But we can just compute it directly.
   - For `child1[u] = 1`.
   - For `child4[u]`:
     - if `deg[u] < 4`: `-inf`
     - else:
       - For each child v: `gain = max(child1[v], child4[v]) - none[v]`
       - Sort gains descending, take first 3 (or all if less than 3).
       - `child4[u] = 1 + sum_none + sum(top 3 gains)`
   - For `root1[u]`:
     - if no children: `-inf`
     - else:
       - best_gain = max over children

## worker: Implement the tree DP to compute the maximum alkan
The solution uses tree DP with four states per node:
- `none[u]`: best size in subtree if `u` is excluded.
- `child1[u]`: `u` is included as a leaf attached to its parent (size 1).
- `child4[u]`: `u` is included with degree 4 and its parent edge is used (can attach up to 3 children).
- `root1[u]`: `u` is the component root with degree 1 (must attach exactly one child which must be `child4` to provide a degree-4 vertex).
- `root4[u]`: `u` is the component root with degree 4 (can attach up to 4 children).

The DP is computed in post-order. For each node, we compute the best "gain" of attaching a child vs. excluding it, sort the gains, and take the top 3 or 4 depending on the state. The original degree constraint ensures that degree 4 states are only valid if the node has at least 4 neighbors in the original tree.

The final answer is the maximum over all nodes of `root1[u]` and `root4[u]`, which represent valid alkane subgraphs (they contain at least one degree-4 vertex by construction). If no valid state yields a positive size, output -1.

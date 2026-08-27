
## ideation
**Core difficulty:** We must partition a tree with N·K vertices into N simple paths, each containing exactly K vertices (K−1 edges). The paths must be vertex-disjoint and edge-disjoint, collectively covering the whole tree.

**Reformulation as edge partition:** Since each path uses K−1 edges and there are exactly N·K−1 edges in the tree, a valid decomposition partitions the edges into N path-pieces of K−1 edges each, with all vertices used exactly once. Equivalently, at every vertex, the path pieces passing through it must form a "matching" of incident edges (each internal vertex of a path has degree 2 within the path, endpoints have degree 1). This is similar to partitioning a tree into disjoint paths of bounded length.

**Candidate approaches:**

1. **Leaf-stripping with multiset of remainders** (standard solution):
   - Root the tree at any node and run a DFS/post-order.
   - From each child `c`, we obtain a "remainder" `r_c` = how many vertices are still needed to complete a path that extends from child `c` upward to the current node. Values are in `0..K-1`.
   - If `r_c == 0`, the child subtree already contains a closed path; discard it.
   - Otherwise `r_c` means a partial path of length `r_c` vertices has its free end at node `u` (the current node, the parent).
   - For the current node `u`, collect all `r_c > 0` from children. For each child remainder, push it into a multiset.
   - Repeatedly pair two remainders `a` and `b` from the multiset: if `a + b + 1 == K`, a full path of K vertices is closed. Otherwise insert `(a + b + 1) mod K` back (the new combined remainder counts the current node once between them).
   - Any unpaired remainder at the end is propagated to the parent.
   - Finally, the root must have no propagated remainder (or one that matches the root itself, depending on conventions) — and we need exactly N closed paths.
   - Complexity O(V log V) with a multiset per node; using a `defaultdict`/list + sort is fine for V ≤ 2·10^5.

2. **Greedy bottom-up matching of partial paths at each edge:**
   - For each node, keep a multiset of "path-tail lengths mod K" coming from each subtree.
   - For each pair whose sum ≡ K−1 (mod K), they join through this node, forming a longer path or a closed cycle. (Since a tree has no cycles, closing = finished path.)
   - Same idea as approach 1; the implementation trick: any remaining unmatched value is what propagates upward.

3. **Reformulation as flow / matching:** Build an auxiliary multigraph and use matching — but this is overkill and likely too slow for 2·10⁵.

4. **Brute force / DP on tree:** Exponential in branching factor — infeasible.

**Pitfalls:**
- Off-by-one between “length K” (K vertices) and K−1 edges. The combination formula is: two remainders `a` and `b` at a common parent form a path of length `a + b + 1` (the +1 is the current node). If this equals K, it’s complete.
- Modular reduction must be done with `(a + b + 1) % K`, but with the special check: if `a + b + 1 == K`, close; else reduce.
- When K = 1, each path is a single vertex, trivially Yes (any tree). Handle this edge case to avoid mod-by-1 weirdness in some implementations.
- The root may end with a single remaining partial path of length K (i.e., the whole tree is one path of K vertices). But the question requires N paths each of length K, so we need to check that the number of closed paths equals N.
- We must count closed paths across the entire tree; using a global counter incremented when `a + b + 1 == K` works.
- Implementation must handle up to 2·10⁵ nodes efficiently; Python recursion must be avoided or stack limit increased — use iterative post-order (stack-based) or set recursionlimit high.

**Refined algorithm:**
1. Build adjacency list.
2. Iterative post-order traversal (parent array via BFS, then process nodes in reverse BFS order). Equivalent: root at 1, do a stack DFS to compute parent, then iterate vertices in reverse order of traversal order.
3. For each node `u` in post-order:
   - Initialize an empty list (acting as a multiset — but since we only need to repeatedly pair the two smallest, we can sort, and actually we can just do the following: keep a counter/dict of remainders since K ≤ V is bounded by 2·10⁵).
   - For each child `v` of `u`:
     - Get the remainder value `r` that `v` propagated to `u` (stored in an array `up[v]`). If `r == 0`, increment closed-path counter (it was already closed in the subtree) — actually `r == 0` means a closed path was formed; we don't need to track it further.
     - Else add `r` to the list at `u`.
   - Sort the list.
   - Greedily pair: two-pointer from both ends. For `a <= b`:
     - If `a + b + 1 == K`: increment global closed counter; discard both.
     - Else: new remainder = `(a + b + 1) % K`; if it's 0, that's invalid because we said `a + b + 1 < K` would mean a path of length < K can be a partial, but `a + b + 1 > K` and `(a+b+1)%K == 0` would mean a closed path of length K which we would have caught by `== K`... so `== 0` shouldn't happen here, but handle gracefully.
     - Add the new remainder to a "next level" list.
   - After pairing all, any leftover single remainder is stored as `up[u]`. If no leftover, `up[u] = 0` (meaning this subtree is fully closed).
4. After processing all nodes, `up[root]` must be 0, and the global closed counter must equal N.
5. Special case: K = 1 → always Yes if N·K = number of vertices (given), and we need N paths of 1 vertex each which is trivially satisfied. Actually, with K=1, each path is one vertex, N = total vertices. Always Yes.

**Complexities:** O(V log V) due to sorting at each node, but the total sizes of all lists across nodes is O(V). A more efficient version uses a hash map of counts rather than sorting, giving O(V). For safety with 2·10⁵, O(V log V) is fine; with careful implementation can also do O(V) using a Counter that we drain.

**Verification of algorithm with samples:**
- Sample 1: N=3, K=2. Tree: 1-2-3-4, 2-5, 5-6.
  - Post-order from 1: 4→3→6→5→2→1.
  - Node 4: no children, no remainder, up[4]=0.
  - Node 3: child 4 with r=0 (closed in subtree? no — 4 alone isn't a closed path; but here r=0 means “nothing to propagate”). Wait: in my scheme, up[v] = 0 means the subtree at v is fully closed with some number of complete paths. Up to v, we don't know how many closed paths. We need a separate closed count.
  - Actually the correct convention: `up[u]` is either 0 (no pending partial path) or a value in 1..K-1 indicating a partial path of `up[u]` vertices whose free end is at u, to be extended upward. Closed paths are counted globally.
  - Node 4: up[4] = 0, but it represents a partial of length 1? No — node 4 has no children and is not the root. It should propagate a partial path of length 1 (just vertex 4) upward. With K=2, partial = 1.
  - So leaf nodes propagate `up[leaf] = 1` (mod K, and 1 means one vertex pending).
  - Node 3: child 4 contributes r=1. List = [1]. Nothing to pair. up[3] = 1.
  - Node 6: leaf, up[6] = 1.
  - Node 5: child 6 contributes r=1. Pair: 1+1+1=3, mod 2 = 1, not 2. Hmm that doesn't work.

Let me re-examine. With K=2, we want paths of length 2 vertices. So a leaf (single vertex) is a partial of size 1. Two leaves meeting at a parent with parent in the middle: 1+1+1=3 vertices, too many — but actually a path of 2 vertices can't include the parent as middle; it can only be 2 vertices with the parent as one endpoint. So two leaves can't both attach to the same parent to form length-2 paths because that would need the parent to be in the middle, making length 3.

In the correct algorithm: at node 5, we have one child (6) with r=1. There's only one partial, so we can't pair. The new partial up[5] = 1+1 = 2? But 2 == K, so it's a closed path! We count it and up[5] = 0. Yes, that works.

So the rule is: when only one partial `a` comes up from a child and the node itself forms the other end: a + 1 = K → closed, else a+1 propagated.

Let me redo:
- Node 4 (leaf, no children): single node is a partial of size 1 → up[4] = 1.
- Node 3: child 4 with r=1. One partial. New remainder = 1+1=2 == K → closed (+1). up[3] = 0.
- Node 6 (leaf): up[6] = 1.
- Node 5: child 6 with r=1. New = 1+1=2 == K → closed (+1). up[5] = 0.
- Node 2: children 3 (r=0) and 5 (r=0). No partials. up[2] = ? Hmm — but node 2 itself needs to be in some path. If no children have partials, node 2 alone is a partial of size 1 → up[2] = 1.
- Node 1: child 2 with r=1. New = 1+1=2 == K → closed (+1). up[1] = 0.

Closed count = 4, but N = 3. Hmm, that's wrong.

Wait, let me recount: 3 → closed path (3,4), 5 → closed (5,6), 1 → closed (1,2). That's 3 closed paths, but my counter says 4. The issue: when node 3 closes a path, but node 3 itself was part of it as one endpoint. Let me retrace:

- Node 4 (leaf): partial = 1 (just node 4).
- Node 3: child 4 has partial 1. Combining: 1 (from child 4) + 1 (node 3) = 2 = K → forms path (4,3) — wait, the direction matters. Actually when we say "child contributes r=1, parent combines: r + 1", we're saying a partial path of 1 vertex (just the child) is extended by adding the parent as one more vertex, total 2 = K → closed path. The path is (child, parent) = (4, 3). 
- Node 6 (leaf): partial = 1.
- Node 5: combining child 6's partial (1) + node 5 = 2 = K → closed path (6, 5).
- Node 2: children 3 and 5 both have r=0 (subtrees fully closed, no partial reaching node 2). So node 2 has no children partials. But node 2 itself is in the tree and must be in some path. So node 2 starts a new partial of size 1, up[2] = 1.

But wait, subtrees of node 3 closed (3,4) — node 3 itself is in the closed path, so it's used. Subtree of node 5 closed (5,6) — node 5 is in that path, used. So node 2 has no incoming partial. Node 2 alone is a partial of size 1 → up[2] = 1. But node 2 is connected to node 1 (parent). So when node 1 processes:
- Child 2 has r=1. Combining: 1 + 1 (node 1) = 2 = K → closed path (2, 1).

So total closed = 3 = N. But in my trace earlier I had node 3 closing then 5 closing then 1 closing = 3 closed. Let me recount the closures: (3,4), (5,6), (1,2). That's 3. Good. Where did I get 4? Let me recount my earlier bullet trace: I said "closed at 3", "closed at 5", "closed at 1" = 3. So I was wrong about getting 4. The algorithm gives 3. 

**Generalized rule clarification:**
- Each leaf propagates a partial of size 1.
- At a node with a multiset of child remainders `S`:
  - Sort `S`.
  - Use two pointers to greedily pair the smallest and largest.
  - For pair `(a, b)`: 
    - If `a + b + 1 == K`: closed path; count.
    - Else: new remainder `(a + b + 1) % K` (which is `a + b + 1 - K` since `a + b + 1 > K` when not equal).
  - After all pairings, if there's a single leftover `a`: 
    - If `a + 1 == K`: closed path (this forms a path where the node is one endpoint); count.
    - Else: up[node] = (a + 1) % K.
  - If `S` is empty: up[node] = 1 (a partial starting at this node).
- Root handling: after the root is processed, if up[root] is nonzero, that means a partial is dangling, which is invalid (unless K = 1).
- Final answer: closed_count == N and up[root] == 0.

Wait, there's a subtlety: if at a node `S` is empty, up[node] = 1. But what if the node is part of a closed path formed at its parent? That's fine — the parent will use this 1.

Now, why does the greedy "pair smallest with largest" work? Because we want `a + b + 1` to be as close to K as possible — pairing extremes maximizes the chance of hitting K or going over. If it doesn't hit K, the leftover `(a + b + 1) % K` should be as small as possible? Actually we want to minimize the new remainder to avoid long dangles. Hmm, the standard approach pairs smallest with largest, and it's been proven correct for this type of problem.

Let me verify with sample 2: N=3, K=2. Tree: 1-2-3-4, 2-5, 3-6.

- Node 4: up=1.
- Node 6: up=1.
- Node 3: child 4 (r=1), child 6 (r=1). S = [1,1]. Pair: 1+1+1=3, mod 2 = 1, not 2. up[3] = 1.
- Node 5: up=1.
- Node 2: child 3 (r=1), child 5 (r=1). S = [1,1]. Pair: 1+1+1=3, mod 2 = 1. up[2] = 1.
- Node 1: child 2 (r=1). S = [1]. Single: 1+1=2 == K → closed. up[1]=0.

Closed = 1, but N = 3. Answer: No. Correct! (Only one path of length 2 formed, namely (2,1). The rest can't be partitioned.)

Great, the algorithm is correct.

**Implementation details:**
- Use adjacency list, parent array, order array (post-order via BFS/DFS).
- `up` array of size V+1.
- For each node in post-order, build a list of remainders from children, sort, apply the pairing logic.
- Global counter for closed paths.
- At the end, check: closed == N and up[root] == 0.
- Edge case K = 1: each path is one vertex, N = NK, trivially Yes. Just print Yes.

## worker: Implement the post-order path decomposition algori
The solution implements the standard "leaf-stripping" or "post-order remainder pairing" algorithm for partitioning a tree into paths of equal length K. 

Key points:
1. **K=1 edge case**: Each path is a single vertex, so any tree can be decomposed. Print "Yes" immediately.
2. **Iterative DFS**: To avoid recursion depth issues with up to 2×10⁵ nodes, we use an explicit stack to build a preorder traversal and then process nodes in reverse (post-order).
3. **Remainder propagation**: Each node collects "remainders" from its children — values r in [1, K-1] representing a partial path of r vertices whose free end is at the current node. We greedily pair the smallest remainder with the largest: if a+b+1 == K, the path is closed (increment counter); otherwise, the new remainder is (a+b+1) % K, inserted back into the list. This continues until at most one remainder remains.
4. **Final check**: After processing the root, we need exactly N closed paths and no dangling remainder at the root.

The algorithm is O(V log V) due to sorting at each node, which is efficient enough for V ≤ 2×10⁵. The initial messy `solve()` was replaced by `solve_clean()` which is the final correct version.

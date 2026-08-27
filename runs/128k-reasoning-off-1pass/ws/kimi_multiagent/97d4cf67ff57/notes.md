
## ideation
Core difficulty: a valid subgraph must be a connected subtree where every included vertex has kept-degree exactly 1 or 4, with at least one degree-4 vertex. This is a local degree-constraint optimization on a tree, so tree DP is natural, but the “exactly 4” branching makes naive merging expensive if not bounded carefully.

Key observations:
- Any connected subgraph of a tree that is a tree is a subtree (connected vertex subset with induced edges).
- For a chosen vertex subset S, each v in S must have |N(v) ∩ S| in {1,4}.
- Root T arbitrarily. For each node, only the number of selected children matters, plus whether the parent is selected.
- If parent is not selected, node needs selected-child-count in {1,4}. If parent is selected, node needs selected-child-count in {0,3}.
- We need maximum size of a connected selected set. A rooted DP can return best values for states depending on parent selection and selected-child count, then combine children with a small DP over counts 0..4.
- Pitfall: connectivity. If we simply take best child subtrees independently, we may combine pieces that are valid only when connected through the current node. That is fine if each child state assumes current node is selected. But we must ensure child states are compatible with the edge to current node.
- Pitfall: leaves. A selected leaf in the final alkane has degree 1, so in rooted terms it either selects parent and no children, or (if root) selects exactly one child.
- Pitfall: at least one degree-4 vertex required. A single edge subtree (two degree-1 vertices) is not valid. Need to track whether a degree-4 vertex exists, or compute max valid with/without and only accept with.
- Pitfall: answer may not include the arbitrary root, so DP must consider best subtree anywhere, not only rooted at 1.

Candidate DP:
Root tree at 1. For each node u, compute DP over:
- p ∈ {0,1}: whether parent of u is selected.
- k ∈ {0..4}: number of selected children of u.
- h ∈ {0,1}: whether the selected subtree in u's descendant component (including u if selected) already contains a degree-4 vertex.
Value = max selected vertices in the part of the subtree rooted at u that is connected to u, assuming u is selected, with exactly k selected children, and parent selected status p. If u is not selected, nothing in this branch can connect upward, so for child merging we only need states where child is selected and connected.

When merging children, each child v can either be excluded (contributes 0 selected vertices and count 0), or included, in which case v must be in a state with parent selected (p=1) and some child-count c such that its total degree is valid: since parent edge selected, v needs c ∈ {0,3}. Its contribution is dp[v][p=1][c][h] + 1? Better define dp value including v itself, then contribution is that value. Excluding child contributes 0 and h=0. Merge with small knapsack over total selected children up to 4 and h flag.

After computing dp[u], derive best valid subtree whose highest node (closest to root) is u:
- If parent not selected (p=0), u can be final with child-count k ∈ {1,4}; if k=4 then h automatically true, else need h=1 from descendants.
- If parent selected (p=1), u can be final with child-count k ∈ {0,3}; validity of u degree okay, and h indicates degree-4 somewhere.
But for global answer, a valid alkane has a unique highest node r (closest to root). Its parent is not selected, so it corresponds to state p=0 at r with k∈{1,4}, and h=1 or k=4. Max over all r. This avoids needing rerooting.

Need careful initialization: for a leaf u (no children in rooted tree):
- p=0: u selected, needs k∈{1,4}; impossible with k=0, so no valid state as highest node. But dp[u][0][0][0]=1 may still be useful? If parent not selected and u selected with k=0, u is isolated invalid, and cannot be part of a larger valid subtree upward because parent not selected. So such state is useless for merging upward (parent edge not selected). For merging into parent, only p=1 states matter.
- p=1: u selected with parent edge, needs k∈{0,3}; with k=0 valid (degree 1), dp=1,h=0.

Thus for merging children, from child v we only use dp[v][1][0 or 3][h], since edge u-v selected implies v's parent selected. Good.

At node u, to compute dp[u][p][k][h], merge children options. Since k only up to 4, and each included child contributes count 1, this is just: choose up to 4 children to include, each with best value for c∈{0,3} and h flag, but h combination needs max over whether any included child has h=1. Since all child contributions are positive? dp values positive, but excluding may be better if including forces count constraints. We can compute for each child two best options: include with h=0 best value, include with h=1 best value. Then for each total count m and h flag, max sum. Number of children large, but m≤4 so O(deg*4*2*2) fine.

However, subtlety: for a child included, its state c=0 or c=3 both valid when parent selected. We should take max over c for each h. Yes.

Then dp[u][p][k][h] = 1 + best_merge[k][h] if the total degree condition relative to p is satisfiable eventually? Actually dp states can store all k 0..4 regardless of final validity, because when u is merged into its parent, only certain k are acceptable depending on p. So compute all k 0..4. Validity checked when used:
- As child of its parent (p=1): acceptable k∈{0,3}.
- As highest node (p=0): acceptable k∈{1,4}, plus h condition for answer.

This works.

Alternative approach: rerooting / DP on edges with states, but rooted highest-node method seems sufficient.

Need to confirm sample 1: root 1; likely answer 8.

Complexity O(N * constant). Use iterative postorder to avoid recursion limits, or set recursionlimit high. N=2e5, recursion risky; use iterative stack order.

Implementation detail:
- Build adjacency.
- Root at 1, produce parent and order via stack.
- Process nodes in reverse order.
- For each node, gather children (neighbors except parent).
- For each child, compute inc0 = max(dp[child][1][0][0], dp[child][1][3][0]) (h=0), inc1 = max(... h=1). Use -inf for impossible.
- Merge: initialize cur[m][h] = -inf, cur[0][0]=0. For each child, new = -inf; option exclude: same; option include h0: cur[m-1][0]+inc0 -> h0, cur[m-1][1]+inc0 -> h1; include h1: cur[m-1][0]+inc1 -> h1, cur[m-1][1]+inc1 -> h1. m from 1..4.
- After merging all children, for k in 0..4, h in 0..1: dp[u][p][k][h] = 1 + cur[k][h] for both p=0 and p=1 (same, since p only affects validity not merging). Actually dp doesn't depend on p in value; only usability. So we can store dp[u][k][h] and interpret. Simpler.
- Answer: for each u, as highest node (parent not selected), k=1 requires h=1 (since u degree 1, need a degree-4 below), value dp[u][1][1]; k=4 valid regardless h? If k=4, u itself degree 4, so h can be 0 or 1; value dp[u][4][0/1]. Take max. Note dp[u][k][h] includes u and selected descendants connected. For k=1,h=1, the degree-4 vertex is in descendant subtree; connectivity holds because child included is connected to u. Good.
- Edge case: what about valid alkane consisting of a degree-4 vertex with 4 leaves: highest node has k=4 (if root of alkane is the degree-4 vertex) or k=3 with parent selected (then highest node is a leaf with k=1? Let's see: alkane with center c and leaves a,b,d,e. Root tree at some node. Highest node of the selected set is the selected vertex closest to root. If root is outside, highest could be a leaf or center depending on shape. In any case highest node has parent not selected and must have final degree 1 or 4 using only children, so k∈{1,4}. For center-with-4-leaves, if center is highest, k=4 OK. If a leaf is highest (tree rooted inside that leaf's side?), the leaf's parent (center) is selected, contradiction because highest means parent not selected. Actually highest node is unique: the selected vertex closest to root; its parent is not selected. If root is at a leaf of the alkane, then that leaf is highest with k=1 (child center), and h must be 1 (center is degree 4) — captured by dp[leaf][1][1]. Good.

So answer = max over u of dp[u][1][1], dp[u][4][0], dp[u][4][1]. If none, -1.

Check sample 2 mentally: tree is two degree-3 nodes connected; max degree 3 so no vertex can have degree 4 in any subtree (subtree degree ≤ original degree). Answer -1. Our DP: no node can have k=4 or k=3 with parent (needs 3 children + parent = 4) — node 1 has children 2,3 (2 children) if rooted at 1; nodes 2,3 have 2 children each. dp[2] as highest: k=1 possible? children 4,5 leaves. dp[4] p=1 k=0 =1. Merge at 2: k=1 value 2 (2+leaf), h=0. k=... dp[2][1][1]=2. As highest k=1 needs h=1, none. k=4 impossible. Similarly no answer. Good.

But wait: degree-4 vertex in subtree needs original degree ≥4. Fine.

One more subtlety: when child included with c=3 (child has 3 selected children + parent = degree 4), that child's h flag: child itself is degree 4, so even if its descendants have no degree-4, the state should be h=1. Our dp definition: h = whether subtree (including u) contains degree-4 vertex. When computing dp[u][k][h], we set h based on merged children h flags OR (u itself has total degree 4). But total degree depends on p (parent selected?) which is unknown at computation time. Hmm. For states used as child (p=1), u degree = k+1; degree 4 iff k=3. For states used as highest (p=0), degree = k; degree 4 iff k=4.

So h should incorporate u's own degree-4 status depending on context. Options:
- Store dp[u][k][h] where h refers only to descendants (children subtrees), and when using the state, check u itself: for answer (p=0): valid if k∈{1,4} and (h==1 or k==4). For child usage (p=1): acceptable k∈{0,3}; when parent merges child with k=3, the child itself is degree 4, so contribution's h should be treated as 1 regardless of stored h. So in parent merging, inc0/inc1 computation: for child states with k=3, add to h=1 category with value dp[child][3][h] for both h (take max). For k=0, child degree 1, h stays as stored.

Let's define dp[u][k][h] = max vertices in selected connected set within u's subtree including u, with exactly k selected children, and h indicates whether any selected vertex among u's descendants (excluding u) has degree 4 in the final selected set... but degree of descendants is fully determined within subtree (their parent is u, selected, so their degree = their k +1). Yes, descendants' final degrees are determined by their own states (since their parent u is selected). So h for descendants is well-defined: child state (k_c, h_c) contributes a degree-4 vertex if k_c==3 (child itself degree 4) or h_c==1.

Thus when merging child, for each child compute:
- best value for option "contributes h=0": child k_c=0 with h_c=0 only (k_c=0 means child degree 1; h_c=0 means no degree-4 in its descendants). Also k_c=3 cannot be h=0 because child itself degree 4. So h0 option = dp[child][0][0].
- best value for option "contributes h=1": max over dp[child][0][1], dp[child][3][0], dp[child][3][1].
Then dp[u][k][h] = 1 + merge result, where h refers to degree-4 among descendants (children and below), not counting u.

Answer at u as highest (p=0): u degree = k. Valid if k∈{1,4}. Alkane needs some degree-4: if k==4, u itself qualifies → value dp[u][4][h] for h∈{0,1}. If k==1, need h==1 → dp[u][1][1].

Also, could the highest node have k=... what about k=0? Single vertex degree 0 invalid. k=2,3 invalid degrees. Right.

Also need to consider valid alkane where highest node has degree 1 and the degree-4 vertex is deeper — covered.

Also, what about the possibility that u's parent is selected but u is the "top" because parent edge not in subgraph — that's exactly p=0 case. Covered by considering every u as highest.

Now compute sample 1 roughly to validate: root 1.
Tree: 1-2,2-3,3-4,4-5,2-6,2-7,3-8,3-9.
Root 1: child 2. 2's children 3,6,7. 3's children 4,8,9. 4 child 5. Leaves 5,6,7,8,9: dp[k=0][h0]=1.
Node 4: child 5. Merge: k=0: 1 (just 4), k=1: 1+1=2 h0. dp[4][1][0]=2.
Node 3: children 4,8,9. Child options: 4: h0: dp[4][0][0]=1 (exclude 5, just 4? wait dp[4][0][0]=1 means select 4 with 0 children; as child of 3, 4's degree = 1 (parent) + 0 = 1 OK), h1: dp[4][3][*] impossible, dp[4][0][1] impossible → -inf. So child 4: inc0=1, inc1=-inf. But also dp[4][0][0]=1 vs including 5? For child state k_c can be 0 or 3 only (since parent selected). k_c=0 gives value 1. So including child 4 contributes only 1 (vertex 4 alone, not 5). Hmm but in the optimal alkane, 4 is excluded and 5 excluded. Fine.
Children 8,9: inc0=1 each.
Merge at 3: best k=3: include 4,8,9 → value 1+ (1+1+1)=4, h=0. dp[3][3][0]=4. Also k=1: best 2 (3+one child) h0. k=4 impossible (3 children max).
Node 2: children 3,6,7. Child 3 options: h0: dp[3][0][0]=1; h1: dp[3][3][0]=4 (3 itself degree 4), dp[3][0][1] none → inc1=4. Children 6,7: inc0=1.
Merge: k=3: choose 3(h1,4),6,7 → sum 6, h1 → dp[2][3][1]=7. k=1 with h1: 1+4=5 → dp[2][1][1]=5. k=4 impossible (3 children).
Node 1: child 2. dp[1][1][1] = 1 + inc1(2). inc1 for child 2: max(dp[2][0][1], dp[2][3][0], dp[2][3][1]) = 7. So dp[1][1][1]=8. Answer candidate: u=1,k=1,h=1 → 8. Also u=2 as highest: k=... dp[2][4] impossible; dp[2][1][1]=5. u=3 highest: dp[3][4] impossible (only 3 children), dp[3][1][1]? k=1 h1: include child with h1 — none, so no. Answer 8. Matches.

Sample 3 answer 11 — trust.

Complexities fine.

Now code structure:
- Read N, edges.
- adjacency list.
- parent = [0]*(N+1), order via stack from 1.
- dp as list per node: we need dp[u][k][h] for k 0..4, h 0..1. Store as list of 5x2 ints, or two arrays of size 5. Use -10**9 as -inf.
- Process reversed order: children = neighbors except parent.
- For each child, precompute inc0 = dp[child][0][0]; inc1 = max(dp[child][0][1], dp[child][3][0], dp[child][3][1]).
- Merge with cur arrays size 5x2.
- After merge, dp[u][k][h] = 1 + cur[k][h] where cur > -inf.
- Update answer: ans = max(ans, dp[u][1][1], dp[u][4][0], dp[u][4][1]).
- Print ans if > -inf else -1. Since valid alkane has at least 5 vertices? Actually smallest alkane: one degree-4 vertex + 4 leaves = 5 vertices. So ans ≥5 if exists. If ans stays -inf print -1.

Wait: is a graph with one degree-4 vertex and four degree-1 vertices a tree? Yes, star K1,4, 5 vertices. Minimum alkane size 5.

Double-check merging loops: for each child, iterate m from high to low or use new array. Use new array each child: O(5*2*4) per child.

Edge case N=1: no edges, no alkane → -1.

Also confirm: dp[u][0][0] = 1 always (select u alone, no children). As child with p=1, degree 1 valid. Good.

Potential issue: when child inc0 = dp[child][0][0], that's child selected with no selected children — degree 1 (parent edge). Valid. inc1 includes dp[child][3][*] where child has 3 selected children — degree 4 valid, and dp[child][0][1] where child degree 1 but a deeper degree-4 exists. Good.

What about child state k_c=... could child have k_c such that child degree is 4 via parent+3 children only; k_c=0 or 3 are the only valid ones. Yes.

Answer condition: highest node u, parent not selected, degree = k must be 1 or 4. k=1 → need h=1. k=4 → any h. Also k=... could highest node have degree 4 with k=4 only (no parent). Yes.

I think solution is correct. Let me also consider whether a valid alkane's highest node could have k=1 but the degree-4 vertex is... must be in descendants, h=1 captures. Good.

Now write code.

def solve():
    import sys
    sys.setrecursionlimit(...)
    data = sys.stdin.buffer.read().split()
    ...

Iterative DFS:
parent = [0]*(N+1)
order = []
stack = [1]
parent[1] = -1
while stack:
    u = stack.pop()
    order.append(u)
    for v in adj[u]:
        if v != parent[u]:
            parent[v] = u
            stack.append(v)

Then process reversed(order).

NEG = -10**9
dp = [None]*(N+1)
ans = NEG
for u in reversed(order):
    cur0 = [NEG]*5; cur1 = [NEG]*5  # or 2D
    cur[0][0]=0
    for v in adj[u]:
        if v == parent[u]: continue
        d = dp[v]
        inc0 = d[0][0]
        inc1 = max(d[0][1], d[3][0], d[3][1])
        nxt = [[NEG]*2 for _ in range(5)]
        for m in range(5):
            for h in range(2):
                val = cur[m][h]
                if val == NEG: continue

## worker: Implement the full Python solution: iterative post
- A connected subgraph of a tree that is itself a tree is a subtree (connected vertex subset with induced edges). Each selected vertex must keep exactly 1 or 4 selected neighbors, with at least one degree-4 vertex.
- Rooted the tree at 1 (iterative DFS to avoid recursion limits) and processed nodes in reverse order (post-order).
- State `dp[u][k][h]`: best size of a selected connected set inside u's subtree containing u, with exactly k selected children; h tracks whether a degree-4 vertex exists among selected descendants (u's own degree depends on whether its parent is selected, so it's accounted for at usage time).
- When u selects a child v, v's parent edge is used, so v must have selected-child-count 0 (degree 1) or 3 (degree 4). Thus child merge options: `inc0 = dp[v][0][0]` (no degree-4 contributed), `inc1 = max(dp[v][0][1], dp[v][3][0], dp[v][3][1])` (degree-4 at v itself when k=3, or deeper). Merged with a small knapsack over counts 0..4 and h∈{0,1}, O(deg·5·2) per node.
- Every valid alkane has a unique highest (closest-to-root) vertex u whose parent is unselected; u's degree equals its selected-child count k, so valid cases are k=1 with h=1 (degree-4 lies below) or k=4 (u itself is degree 4). Answer = max of `dp[u][1][1]`, `dp[u][4][0]`, `dp[u][4][1]` over all u; -1 if unreachable.
- Verified logic against samples: sample 1 yields 8 (root 1 with child 2 in state k=3,h=1 giving 7, plus root = 8); sample 2 has max degree 3 so no state qualifies → -1.
- Complexity: O(N) time and O(N) memory (constant 5×2 states per node).

We need to compute, for each query (u, v), the sum over all permutations P of the distance in the random rooted tree T(P) between u and v, modulo MOD=998244353.

Key observation: In a random rooted tree where each node i (i≥2) independently chooses a parent uniformly from {1,…,i-1}, the structure is equivalent to a random recursive tree. For such trees, the probability that the unique path between u and v passes through edge (x, parent(x)) equals: for u<v, when considering the pair (min, max) = (u,v), the path uses edge (k, parent(k)) iff parent(k) lies on the path already, which occurs exactly when parent(k) is in the set {u, parent(u), parent(parent(u)), …, v} under the recursive tree dynamics. In a random recursive tree, the probability that edge (k, parent(k)) lies on the path between u and v (with u<v) is 2/(max - min + 2). More precisely, for a random recursive tree on {1..N} (where each node attaches to a uniformly random earlier node), the probability that the path between u and v goes through the edge connecting k to its parent is 2/(v - u + 1) for u<k≤v, and 0 otherwise. Wait — let me verify with small N.

For N=3, all (N-1)!=2 trees:
- P=(1,1): parents are 2→1, 3→1. Path 1-2 uses edge (2,1). Path 1-3 uses edge (3,1). Path 2-3 uses both edges, length A2+A3.
- P=(1,2): parents are 2→1, 3→2. Path 1-2 uses edge (2,1). Path 1-3 uses edges (3,2) and (2,1). Path 2-3 uses edge (3,2).

For query (1,2): u=1, v=2. Sum of distances = A2 + A2 = 2·A2. Probability that edge (2,1) is on path = 2/2 = 1. ✓

For query (1,3): u=1, v=3. Sum = A3 + (A2+A3) = A2+2·A3. Probability that edge (2,1) is on path: in first tree yes, in second yes → 1. Probability edge (3, parent(3)) on path: in first yes, in second yes → 1. So formula giving prob = 2/(v-u+1) = 2/3 doesn't match. Hmm.

Let me reconsider. The claim might be that for each edge (k, parent(k)) with u < k ≤ v, the probability it lies on the path between u and v is 2/((v-u)(v-u+1))? No.

Actually I recall: in a random recursive tree, the probability that node k (u<k≤v) is an ancestor of v AND on the path from u to v is... Let me think differently.

Path from u to v in rooted tree: u goes up to LCA(u,v), then down to v. Edge (k, parent(k)) is on this path iff either (k is on path from u to LCA including u's edge upward) or (k is on path from LCA to v including v's edge upward toward root... wait, v to LCA is going up).

Equivalently, the path from u to v is the set of edges that connect nodes in the interval [u,v] (in the recursive tree sense) to their parents. In a random recursive tree, the probability that parent(k) ∈ [u, v] for k ∈ [u, v] is... Hmm.

Let me just compute directly. In a random recursive tree with N nodes labeled 1..N (node i attaches to uniform random node in {1..i-1}), the probability that parent(k) = j (j<k) is 1/(k-1).

For the path between u and v (u<v), it consists of edges (k, parent(k)) where k is on the "u-branch" going up from u to LCA(u,v), and on the "v-branch" going up from v to LCA(u,v). Equivalently, these are edges where k ∈ [u, v] and parent(k) is the "next node" on the path.

Alternative: There's a known result that in a random recursive tree, for any u<v, the sum of A_k for k in [u,v] times the probability that edge (k, parent(k)) is on the path from u to v equals... Let me think.

Actually here's a clean formulation. In a random recursive tree on {1,...,N}, consider the "Cartesian tree" or "heap" structure. The tree's structure is determined by: for each k from 2 to N, parent(k) is uniform on {1,...,k-1}. So P_i is uniform on {1,...,i-1}.

Claim: The path from u to v (u<v) goes through edge (k, parent(k)) iff parent(k) ∈ {u, u+1, ..., k-1} ∩ {some ancestor structure}... Hmm complicated.

Let me try a different approach. Sample N=4, all 6 trees. Compute sum of distances (1,4):
- P=(1,1,1): path 1-4: 4→1, edges (4,1),(3,1),(2,1) all on path. Distance A2+A3+A4.
- P=(1,1,2): parents 2→1, 3→1, 4→2. Path 1-4: 4→2→1, edges (4,2),(2,1). Distance A4+A2.
- P=(1,1,3): parents 2→1, 3→1, 4→3. Path 1-4: 4→3→1, edges (4,3),(3,1). Distance A4+A3.
- P=(1,2,1): 2→1, 3→2, 4→1. Path 1-4: 4→1, 2→1, edges (4,1),(2,1). Distance A4+A2.
- P=(1,2,2): 2→1, 3→2, 4→2. Path 1-4: 4→2→1, edges (4,2),(2,1). Distance A4+A2.
- P=(1,2,3): 2→1, 3→2, 4→3. Path 1-4: 4→3→2→1, edges (4,3),(3,2),(2,1). Distance A4+A3+A2.

Sum = (A2+A3+A4) + (A4+A2) + (A4+A3) + (A4+A2) + (A4+A2) + (A4+A3+A2)
    = A2: 1+1+0+1+1+1 = 5
    = A3: 1+0+1+0+0+1 = 3
    = A4: 1+1+1+1+1+1 = 6

So coefficient of A2 is 5, of A3 is 3, of A4 is 6. Total trees = 6.

Hmm interesting. Notice: for k=v=4, coefficient is 6 = 6/1. For k=3, coefficient is 3 = 6/2. For k=2, coefficient is 5... not 6/3=2.

So the formula isn't simply 2/(v-u+1) for k between u and v.

Let me reconsider. Actually coefficient for k=2 in query (1,4):
Edge (2,1) is on path 1-4 in: tree 1 (yes, since 1-2-...-4 all chain through), tree 2 (yes), tree 3 (yes, 4-3-1, 2 is not on path actually wait, 2 is child of 1, and path is 1-3-4, so edge (2,1) is NOT on path). Let me recheck tree 3: P=(1,1,3). So parent(2)=1, parent(3)=1, parent(4)=3. Tree: 1 has children 2,3; 3 has child 4. Path from 1 to 4: 1→3→4. Edges used: (3,1), (4,3). Edge (2,1) NOT used. So tree 3 doesn't count. I made an error above. Let me redo:

Tree 1: P=(1,1,1). 1-2,1-3,1-4. Path 1-4: edges (4,1),(3,1),(2,1) all NOT used actually only (4,1). Hmm wait path from 1 to 4 is just edge (4,1). Edge (2,1) and (3,1) are NOT on this path (1-2-3-4 doesn't exist as path, the tree is a star). So actually only edge (4,1) on path. Let me redo.

Distance 1-4 in each tree = sum of A_k for k on path = A4 for tree 1.
Tree 1: P=(1,1,1). Distance 1-4: A4. Edge (4,1) yes. Edge (3,1) no. Edge (2,1) no.
Tree 2: P=(1,1,2). Path 4-2-1. Distance A4+A2. Edges: (4,2) yes, (2,1) yes.
Tree 3: P=(1,1,3). Path 4-3-1. Distance A4+A3. Edges: (4,3) yes, (3,1) yes.
Tree 4: P=(1,2,1). Path 4-1, 2-1. Distance 1-4: just A4 (direct). Edges: (4,1) yes. (2,1) no (since 2 not on path from 1 to 4 which is just 1-4).
   Wait, parent(2)=1, parent(3)=2, parent(4)=1. Tree: 1→{2,4}, 2→3. Path 1-4: edge (4,1). So A4 only. Edge (2,1) not on path.
Tree 5: P=(1,2,2). 1→{2,4}, 2→3,4. Path 1-4: 1-2-4, distance A2+A4. Edges (2,1) and (4,2).
Tree 6: P=(1,2,3). 1→{2,4}, 2→3, 3→4. Path 1-4: 1-2-3-4. Distance A2+A3+A4. All three edges.

Sum:
A2: tree 2(1) + tree 5(1) + tree 6(1) = 3
A3: tree 3(1) + tree 6(1) = 2
A4: tree 1 + tree 2 + tree 3 + tree 4 + tree 5 + tree 6 = 6

Hmm. So coefficient of A2 = 3, A3 = 2, A4 = 6. Total 11. Total trees = 6.

Total of N=4: 6 trees, sum of distances 1-4 = 11. So average ~ 1.83.

For k=2, coefficient is 3, not following a simple pattern with v-u=3.

Let me think again. Maybe the formula is based on Catalan-like numbers? Hmm.

Wait, perhaps a different characterization. The number of trees where edge (k, parent(k)) is on path from u to v...

For k=v (the larger endpoint), edge (v, parent(v)) is always on the path from u to v (since v is an endpoint). So coefficient of A_v is always (N-1)!.

For k=u (u is smaller endpoint), edge (u, parent(u)) is on path from u to v iff u is not the root of the tree (i.e., u≠1) AND parent(u) is an ancestor of v via going up... Hmm.

Actually for u=1, parent(1) doesn't exist, so edge (1, parent(1)) is never on path. So coefficient of A_1 = 0 (but A_1 isn't even defined in problem; A is indexed from 2). 

For k in (u, v], edge (k, parent(k)) is on path from u to v iff parent(k) is in the set of nodes on the path from k to v, going toward root, but stopping at u or before... Hmm.

Let me think recursively. The random recursive tree has the property: conditional on the tree restricted to {1,...,k}, the edge (k+1, parent(k+1)) connects k+1 to a uniform random node in {1,...,k}.

For query (u,v) with u<v, the path from u to v uses edge (k, parent(k)) for k ∈ (u, v] such that... 

Claim: edge (k, parent(k)) is on path from u to v iff parent(k) is in the same "recursive subtree" as v when restricted to [u, k-1] and some condition.

This is getting complex. Let me look for a different approach.

Approach via symmetry / linearity: We can compute the probability p(u, v, k) that edge (k, parent(k)) lies on path from u to v, summed over all P (where each P is equally likely with (N-1)! choices).

p(u, v, k) = P(parent(k) is on path from u to v in T(P) AND k is on path from u to v) 
But k is on path from u to v iff... hmm.

Actually edge (k, parent(k)) is on path from u to v iff removing this edge disconnects u and v, which happens iff exactly one of u, v is in the subtree rooted at k.

Subtree rooted at k in random recursive tree: k is the root, descendants are nodes that attached to k (directly or transitively). 

P(exactly one of u, v in subtree of k) = P(u in subtree of k, v not) + P(u not, v in).

For k > v: v is not in subtree of k (since v < k and subtree of k only contains nodes ≥ k with parent in subtree). Actually wait, in recursive tree, node j's descendants are all nodes attached to j (directly or transitively), and these must be > j (since each node attaches to a smaller one). So subtree of k = {k} ∪ {nodes > k attached to k's subtree}. So for k > v, v ∉ subtree(k). For k ≤ u, u ∉ subtree(k). For u < k < v, both u and v are < k, so neither in subtree. For k = v, v ∈ subtree(v), u ∉ subtree(v) (since u < v and subtree of v only has nodes ≥ v). So edge (v, parent(v)) is always on path from u to v when u < v. ✓

For u < k < v, we need parent(k) to be such that k's subtree contains exactly one of {u,v}, but both u,v < k, so neither is in subtree of k. So edge (k, parent(k)) is NOT on path from u to v for u < k < v.

Wait that contradicts my earlier calculation! For k=2, u=1, v=4, I had coefficient 3, meaning edge (2, parent(2)) is on path in 3 of 6 trees. But u=1 < k=2 < v=4. According to my reasoning, since u<k<v, neither u nor v is in subtree(2) (subtree(2) ⊆ {2,3,4,...}), so edge (2, parent(2)) is never on path. Contradiction!

Wait I messed up. Let me recheck tree 2: P=(1,1,2). Path from 1 to 4: 1→2→4. Edge (2,1) is on this path. Subtree of 2: {2, 4} (since 4 attached to 2). v=4 ∈ subtree(2). u=1 ∉ subtree(2). So exactly one of {u,v} in subtree(2). ✓

So my claim "for u<k<v, neither in subtree" is wrong because subtree can include v if v attached to k. Let me reconsider: subtree of k includes all descendants, which are nodes j > k with parent(j) in subtree(k). So if k < v, v might or might not be in subtree(k) depending on whether v attached (directly or transitively) to k.

OK so my analysis was wrong. Let me redo.

Subtree(k) = {k} ∪ descendants of k in T(P). Descendants of k are nodes j > k with parent chain reaching k. So v ∈ subtree(k) iff v attached to k (directly or transitively). 

For u<v:
- If k > v: v ∉ subtree(k) (descendants > k), u ∉ subtree(k) (u < k). Edge (k,parent(k)) not on path.
- If k = v: v ∈ subtree(k), u ∉ subtree(k) (u<v<k, u not descendant of k since descendants>k=v). Edge on path. ✓ Always.
- If u < k < v: u ∉ subtree(k) (u<k), v ∈ subtree(k) iff v attached to k's subtree. So edge on path iff v attached to k's subtree.
- If k = u: u ∈ subtree(k) (k is its own subtree root), v ∈ subtree(u) iff v attached to u. Edge on path iff v not attached to u's subtree (i.e., v not descendant of u).
- If k < u: u ∉ subtree(k) (descendants > k), v ∉ subtree(k). Edge not on path.

So the only k that can have edge (k, parent(k)) on path from u to v are k = u and k = v, and u < k < v where v is a descendant of k.

Wait, also for k = v, always yes. For u < k < v, edge on path iff v is descendant of k. For k = u, edge on path iff v is NOT descendant of u (since u is in its own subtree, we need v not in subtree).

So sum = (probability v descendant of u, summed over k in (u, v], contributes A_k for k where v descendant of k) + A_v (always) + A_u · P(v not descendant of u).

Hmm wait for k=u: edge (u, parent(u)) on path iff v not in subtree(u). But for k=u, the edge is (u, parent(u)) and removing it separates {subtree(u)} from rest. u is in subtree(u), v is in subtree(u) iff v descendant of u. So path u-v uses edge (u,parent(u)) iff v not in subtree(u). ✓

Let me re-examine N=4, u=1, v=4:
- k=4: always contributes A4. Count: 6.
- k=3: contributes A3 iff 4 descendant of 3. Trees where parent(3) is ancestor of 4 going down... 4's parent is 3 means 4 descendant of 3. Trees 3 (P=(1,1,3)) and 6 (P=(1,2,3)). Count: 2. ✓
- k=2: contributes A2 iff 4 descendant of 2. Trees where parent chain of 4 reaches 2: tree 2 (P=(1,1,2), parent(4)=2), tree 5 (P=(1,2,2), parent(4)=2). Count: 2. But I calculated 3 earlier. Discrepancy!

Let me recheck. Tree 6: P=(1,2,3). parent(4)=3. Is 4 descendant of 2? parent(4)=3, parent(3)=2, so 4's parent chain is 4→3→2→1. Yes, 4 is descendant of 2. So tree 6 should count for k=2.

Tree 1: P=(1,1,1). parent(4)=1, not descendant of 2. No.
Tree 2: parent(4)=2. Yes, descendant of 2.
Tree 3: parent(4)=3, parent(3)=1. 4→3→1, not through 2. No.
Tree 4: P=(1,2,1). parent(4)=1. No.
Tree 5: parent(4)=2. Yes.
Tree 6: parent(4)=3, parent(3)=2. 4→3→2→1. Yes.

Count: 3. ✓ Matches.

So formula: 
- A_v contributes (N-1)! (always).
- For u < k < v, A_k contributes (N-1)! · P(v descendant of k).
- A_u contributes (N-1)! · P(v not descendant of u).

P(v descendant of k) in random recursive tree: v attached to k's subtree. 

Known result: In random recursive tree on [N], the probability that the path from 1 to v passes through a specific node... or probability that v's ancestor at a specific level is k...

Actually, for random recursive tree, the "ancestor chain" of v going up to root is determined. The probability that v's parent is k (for k < v) is 1/(v-1). The probability that v's grandparent is k (k < v-1) requires parent(v)=j with j>k, then parent(j)=k. Hmm.

But we want P(v descendant of k), which is the probability that in the path from v to root (1), node k appears. Equivalently, k is an ancestor of v.

In random recursive tree, the set of ancestors of v is some random subset. The probability that k is an ancestor of v...

Actually there's a neat result: in random recursive tree on [N], for u < v, the probability that the path from u to v contains k (for u < k ≤ v) is... 

Hmm, let me think. The path from v to root goes through some ancestors. For k to be on path from u to v, we need... 

Alternative formulation: In random recursive tree, conditional on parent choices for nodes ≤ v, the structure restricted to [v] is a random recursive tree on [v]. So we can consider v and ancestors within [v].

For u < v, ancestor chain of v: v = a_0, parent(v)=a_1, parent(a_1)=a_2, ..., until 1. Each a_i < a_{i-1}.

P(k is ancestor of v) = P(parent of v in chain reaches k) = ?

In random recursive tree on [v], v attaches to uniform random in [v-1]. Its parent attaches to uniform random in [parent-1], etc. The chain is: v, parent(v), parent(parent(v)), ..., 1.

Actually here's a key fact: in random recursive tree, for any v, the ancestors of v form a uniformly random subset of {1, ..., v-1} ∪ {v}, but with specific distribution. Hmm, not quite.

Let me think recursively. Let f(v, k) = P(k is ancestor of v in random recursive tree on [v]) for 1 ≤ k < v.

f(v, v) = 1 (v is its own ancestor).
For k < v: f(v, k) = P(parent(v) is k, or parent(v) is j and k is ancestor of j) = sum over j ∈ [v-1] of P(parent(v)=j) · f(j, k) = (1/(v-1)) · sum_{j=k+1}^{v-1} f(j, k).

So f(v, k) · (v-1) = sum_{j=k+1}^{v-1} f(j, k).

Let g(v) = f(v, k) for fixed k. Then g(v)(v-1) = sum_{j=k+1}^{v-1} g(j), and g(k)=1 (k is ancestor of itself... wait, k isn't ancestor of k unless we count k as ancestor. In our problem, ancestor of v means proper ancestor going up to root. Hmm, let me redefine.

Let A(v, k) = P(k is on path from v to root in random recursive tree on [v]). For k = v, A(v,v) = 1. For k < v, A(v, k) = probability k appears in ancestor chain of v.

Recurrence: A(v, k) = (1/(v-1)) · sum_{j=k}^{v-1} A(j, k) for k < v. With A(k, k) = 1.

Let's compute: A(2, 1) = 1/1 · A(1,1) = 1. (Parent of 2 must be 1.)
A(3, 1) = (1/2)(A(1,1)+A(2,1)) = (1/2)(1+1) = 1. (1 always ancestor of any v ≥ 1.)
A(3, 2) = (1/2) A(2,2) = 1/2.
A(4, 1) = (1/3)(1+1+1) = 1.
A(4, 2) = (1/3)(1 + 1 + 1/2) = (1/3)(5/2) = 5/6.
A(4, 3) = (1/3) · A(3,3) = 1/3.

Let me verify with enumeration (N=4, 6 trees, query (1,4), k=2 should have coefficient 3, so probability 1/2, not 5/6).

Hmm discrepancy. Let me recheck enumeration.

For k=2, v=4, A(4, 2) = probability 2 is ancestor of 4.
Tree 1 (P=(1,1,1)): 4→1, ancestors of 4: {4,1}. 2 not ancestor. ✗
Tree 2 (P=(1,1,2)): 4→2→1. 2 is ancestor. ✓
Tree 3 (P=(1,1,3)): 4→3→1. 2 not ancestor. ✗
Tree 4 (P=(1,2,1)): 4→1. 2 not ancestor. ✗
Tree 5 (P=(1,2,2)): 4→2→1. 2 is ancestor. ✓
Tree 6 (P=(1,2,3)): 4→3→2→1. 2 is ancestor. ✓

So 3/6 = 1/2. But my formula gave 5/6. Error in recurrence.

Oh I see the issue: the recurrence should be A(v, k) = (1/(v-1)) · sum_{j=k}^{v-1} A(j, k) for k < v. But this counts A(v, v) as well? No, for k<v, sum is over j from k to v-1, not v.

Wait, A(v,k) = P(k is ancestor of v) where ancestor means in the chain v, parent(v), parent(parent(v)), ..., 1. So k is ancestor of v iff either parent(v)=k (probability 1/(v-1)) or parent(v)=j>k and k is ancestor of j.

But if parent(v) = j and k is ancestor of j, we need to be careful: in random recursive tree, the choice of parent(v) is independent of the tree structure on [v-1]? Actually the tree on [v] is built by: first random tree on [v-1], then v attaches to uniform random node in [v-1]. So yes, independent. So A(v, k) = sum_{j=k}^{v-1} (1/(v-1)) · A(j, k).

For v=4, k=2: A(4,2) = (1/3)(A(2,2)+A(3,2)) = (1/3)(1 + 1/2) = 1/2. ✓

I had an error. Let me redo: A(4, 2) = (1/3) · sum_{j=2}^{3} A(j, 2) = (1/3)(A(2,2) + A(3,2)) = (1/3)(1 + 1/2) = 1/2. ✓

Great. So A(v, k) for k < v satisfies:
A(k, k) = 1, and A(v, k) = (1/(v-1)) · sum_{j=k}^{v-1} A(j, k) for v > k.

Let h(v, k) = (v-1) · A(v, k) = sum_{j=k}^{v-1} A(j, k). Then h(v+1, k) - h(v, k) = A(v, k), and (v)·A(v+1,k) - (v-1)·A(v,k) = A(v,k), so v·A(v+1, k) = v · A(v, k). So A(v+1, k) = A(v, k) for v > k.

Wait! A(v+1, k) = A(v, k)? Let me verify: A(3,2) = 1/2, A(4,2) = 1/2. ✓ A(4,3) = 1/3, A(5,3) = ?

A(5,3) = (1/4)(A(3,3)+A(4,3)) = (1/4)(1 + 1/3) = 1/3. ✓

So A(v, k) = A(k+1, k) for all v > k. And A(k+1, k) = (1/k) · A(k, k) = 1/k.

So A(v, k) = 1/k for all v > k. 

Let me verify: A(4, 2) = 1/2 ✓. A(4, 3) = 1/3 ✓. A(3, 2) = 1/2 ✓.

So P(k is ancestor of v in random recursive tree on [v]) = 1/k for v > k.

Wait but this is on [v], not [N]. Does it matter? The tree on [N] restricted to [v] is a random recursive tree on [v] (since edges from nodes > v don't affect tree on [v]). So yes, A_N(v, k) = 1/k for v > k. ✓

Now back to our problem. P(v descendant of k) for u < k < v: v is descendant of k means k is ancestor of v. P = 1/k. 

P(v not descendant of u): v is descendant of u means u is ancestor of v. P(u ancestor of v) = 1/u. So P(v not descendant of u) = 1 - 1/u.

Wait, but for u=1, 1/u = 1, so P(v not descendant of 1) = 0. Indeed, 1 is always ancestor of every node, so v is always "descendant" of 1 in the trivial sense. Hmm, but 1 is the root, so v is always in subtree(1). The edge (1, parent(1)) doesn't exist. For our problem, when k=u=1, edge (1, parent(1)) doesn't exist (since parent is only defined for i≥2), so A_1 isn't a thing. The coefficient of A_1 in the sum is 0 by definition (A_1 not defined, and edge (1,parent(1)) doesn't exist).

Hmm but my formula says: for k=u, edge contributes A_u · P(v not descendant of u). For u=1, P(v not descendant of 1) = 0, so A_1 contributes 0. ✓ (A_1 not defined.)

For k=u>1: contributes A_u · (1 - 1/u) = A_u · (u-1)/u.

Wait, but for k=v, always contributes A_v · 1 = A_v.

Hmm, let me re-derive. We have:
- k = v: contributes A_v (always, (N-1)! trees).
- u < k < v: contributes A_k · (N-1)! · P(k ancestor of v) = A_k · (N-1)! · (1/k).
- k = u: contributes A_u · (N-1)! · P(v not descendant of u) = A_u · (N-1)! · (1 - 1/u) = A_u · (N-1)! · (u-1)/u.

Total sum (mod MOD) = (N-1)! · [A_v + sum_{k=u+1}^{v-1} A_k / k + A_u · (u-1)/u].

For u=1: A_1 doesn't exist, so just A_v + sum_{k=2}^{v-1} A_k / k.

Let me verify with N=4, u=1, v=4:
Sum = (4-1)! · [A_4 + A_3/3 + A_2/2] = 6 · [A4 + A3/3 + A2/2].

If A2=A3=A4=1: 6 · [1 + 1/3 + 1/2] = 6 · 11/6 = 11. ✓

For N=3, u=1, v=3, A2=A3=1:
Sum = 2 · [A3 + A2/2] = 2 · [1 + 1/2] = 3. ✓

For N=3, u=1, v=2, A2=1:
Sum = 2 · A2 = 2. ✓

For N=3, u=2, v=3, A3=1:
Sum = 2 · [A3 + A2 · (2-1)/2] = 2 · [1 + 1/2] = 3.
Let me verify: 2 trees, query (2,3).
Tree 1: P=(1,1). Path 2-3: 2→1→3, edges (2,1),(3,1). Distance A2+A3=2.
Tree 2: P=(1,2). Path 2-3: 2→1, then 3→2. So 2 and 3: 3→2, edge (3,2). Distance A3=1.
Sum = 3. ✓

Great, the formula works.

So the answer to query (u, v) (u < v) is:
(N-1)! · [A_v + A_u · (u-1)/u + sum_{k=u+1}^{v-1} A_k / k] mod MOD.

We can precompute prefix sums of A_k / k modulo MOD. Let S[t] = sum_{k=2}^{t} A_k / k. Then sum_{k=u+1}^{v-1} A_k / k = S[v-1] - S[u]. And A_v and A_u · (u-1)/u are separate.

Answer = (N-1)! · [A_v + A_u · (u-1) / u + S[v-1] - S[u]] mod MOD.

For u=1, A_u doesn't exist, and A_u · (u-1)/u = 0, and S[u] = S[1] = 0. So formula becomes (N-1)! · [A_v + S[v-1]].

Also, we need to compute A_k / k mod MOD, i.e., A_k · k^{-1} mod MOD.

Compute (N-1)! mod MOD, then for each query compute the answer.
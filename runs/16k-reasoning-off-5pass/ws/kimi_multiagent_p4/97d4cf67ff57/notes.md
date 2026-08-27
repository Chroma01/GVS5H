
## ideation
Core difficulty: maximizing the size of a connected induced subtree where every kept vertex has induced-degree exactly 1 or 4, with at least one degree-4 vertex. Since T is a tree, any connected vertex subset induces a subtree, and "subgraph" can be WLOG the induced subtree on its vertices (adding available edges never creates invalid degrees as long as the degree condition is defined on the subgraph itself — careful: degrees must be 1 or 4 in the subgraph, so we choose which incident edges to include; but including an edge requires including its endpoint, so the subgraph is determined by a connected vertex set S together with a subset of induced edges that keeps it connected and degrees in {1,4}. Since induced subtree on S has well-defined degrees, and dropping edges would disconnect or change degrees, the cleanest model: choose connected S; the subgraph = induced tree on S; require every vertex's induced degree ∈ {1,4}).

Wait — subtlety: could a subgraph use vertex set S but omit some induced edge while staying connected? In a tree the induced graph on connected S is itself a tree (unique paths), and removing any edge disconnects it. So subgraph ⇔ connected vertex subset S, degrees = induced degrees. Good.

So problem = largest connected S ⊆ V with deg_S(v) ∈ {1,4} ∀v∈S, and ∃v with deg_S(v)=4. Equivalent: a subtree where internal branching vertices have exactly 3 kept children (degree 4 with parent) or 4 kept children (degree 4, no parent / root), and leaves have degree 1.

Candidate approach: rooted tree DP. Root T at arbitrary node. For each node u, compute DP over states:
- f[u] = best value of a valid configuration within u's subtree where the edge (u, parent) is NOT used, and the whole kept part inside subtree is either empty or a valid alkane-fragment... but fragments need not be complete alkanes — a vertex may have degree 4 only when combined with parent edge.

Better: think of it as each kept vertex must end with total degree 1 or 4. For node u with parent edge possibly kept, let k = number of kept children. Constraints:
- If parent edge kept: k+1 ∈ {1,4} → k ∈ {0,3}.
- If parent edge not kept and u kept: k ∈ {1,4} (u is leaf of the alkane if k=1? no — if parent not kept and u kept, u is the "top" of the component; its degree = k must be 1 or 4, so k ∈ {1,4}; k=0 would make u isolated degree 0 — invalid unless component is a single vertex, but single vertex has degree 0, not allowed).

So DP states per node:
- A[u] = max kept vertices in u's subtree, with u kept, parent edge kept, and all constraints satisfied inside subtree except u's own degree is not yet finalized (u will get +1 from parent). Then u needs k ∈ {0,3} kept children. Value = 1 + sum of child contributions.
- B[u] = max kept vertices in u's subtree forming a valid complete alkane entirely within subtree (edge to parent cut), possibly empty. This is the "free" state used when the parent cuts the edge.

For combining children: each child v contributes either:
- cut: B[v] (a self-contained valid alkane in v's subtree, or 0 = nothing kept), or
- kept: A[v] + ... where A[v] means v kept connected to u.

For A[u] (u will have parent edge): choose exactly k ∈ {0,3} children to keep (contribute A-child values), others contribute B values. So A[u] = 1 + Σ B[v] + max over choosing k∈{0,3} children of Σ (keptContrib[v] − B[v]) where keptContrib[v] = value when v kept and connected to u. Let me define: for child v, base = B[v] (cut), gain[v] = (value of v kept with edge to u) − B[v]. Then A[u] = 1 + Σ B[v] + max(top k gains with k∈{0,3}, gains can be negative — but we must pick exactly k, so take k largest gains even if negative; k=0 option gives 0).

Value of "v kept with edge to u": v's parent edge kept, so v needs 0 or 3 kept children — that's exactly A[v]. So gain[v] = A[v] − B[v].

For B[u] (free state, parent edge cut): possibilities:
1. Nothing kept in subtree: value 0.
2. u not kept: then children are independent free states: Σ B[v].
3. u kept as part of an alkane whose top is u (no parent edge): u needs k ∈ {1,4} kept children: value 1 + Σ B[v] + max(top k gains, k∈{1,4}).
B[u] = max of these.

Answer = max over u of B-rooted... actually answer = max B[root] if we also require the alkane to have a degree-4 vertex. Hmm — does every valid configuration automatically have a degree-4 vertex? A connected set where all degrees are 1: that's a single edge (2 vertices, both degree 1) — a path can only have 2 vertices if all degrees are 1 (path with ≥3 vertices has degree-2 internal vertices). So the all-degree-1 case is exactly a single edge (2 vertices). Also single vertex (degree 0) is invalid. So we must exclude the 2-vertex single-edge configuration.

Track this: in the DP, configurations where u is kept with k=1 child and that child-subtree is all-degree-1... simplest: compute answer as max valid alkane with a degree-4 vertex. Add a flag dimension, or note: the only forbidden valid configuration is a single edge. So compute the max over all valid configurations (allowing degree-1-only), and separately track whether the max config has a degree-4 vertex. Cleaner: DP values as pairs, or run DP tracking two values per state: best with a degree-4 vertex present, best overall. Since states A and B combine via sums and top-k selections, carrying a flag doubles the state but is straightforward: e.g., A[u] and A4[u] (with a deg-4 vertex somewhere in kept part). Combination: when summing child contributions, "has4" = any child has4 OR (u itself has degree 4 — but u's degree finalizes only when parent decision known; for A[u], u's degree = k+1 ∈ {1,4}, so u has degree 4 iff k=3). So:
- A[u] (k∈{0,3}): has4 if k==3 or any kept child has4 or any cut child's B-part has4... careful: cut children contribute B[v] which may contain an alkane with deg-4 vertex. But if u is kept and connected to parent, the whole thing is one component — cut children are separate components. That's fine for B (free state = best alkane anywhere in subtree, components independent). But for A[u], the state means "u kept, connected upward" — the cut children's alkanes are disjoint bonus components. Is that allowed? In the final answer we need ONE alkane subgraph; extra disjoint alkanes in the subtree would be a separate subgraph — we can't count them in the same subgraph's vertex count!

Critical pitfall: B[v] as "best alkane anywhere in v's subtree" cannot be ADDED to a kept component through a cut edge, because the final answer must be a single connected alkane. But wait — when u is kept and edge (u,v) is cut, can we still keep an alkane inside v's subtree as part of the answer? The answer is one subgraph (connected tree). So no — the total answer counts vertices of one alkane only. However, in DP, B[u] = "best alkane fully inside u's subtree" is a valid standalone candidate for the answer. When u is kept and connected, children that are cut must contribute 0 kept vertices (nothing kept in that child's subtree), NOT B[v].

Revised model: for a child v of a kept node u, either edge kept (contribute A[v], v kept) or edge cut AND nothing kept in v's subtree (contribute 0). Because any kept vertices in v's subtree disconnected from u's component would be a different subgraph.

But then where does the answer come from? Answer = max over u of C[u] where C[u] = best valid alkane whose highest vertex (closest to root) is u, i.e., u kept, parent edge cut, u's degree ∈ {1,4} (k ∈ {1,4} kept children), all kept descendants valid. Plus the single-edge case handled/excluded. Also B[u] = max answer within u's subtree = max(B[children]..., C[u]) — used only for answer propagation, not added into kept components.

So DP:
- A[u]: u kept, edge to parent kept, u's subtree kept-part is exactly u's component (connected through u). u needs k ∈ {0,3} kept children. Each child: kept → A[v], cut → 0. So A[u] = 1 + max over k∈{0,3} of sum of k largest values among A[v] (only positive? must pick exactly k, so pick k largest even if negative... but A[v] ≥ 1 always since v kept alone with k=0 children gives A[v]=1. A[v] ≥ 1 > 0, so picking k largest is fine and they're positive). Actually A[v] ≥ 1 always (v kept with 0 kept children = degree 1 from parent — valid). So gains positive; A[u] = 1 + sum of top-k of {A[v]} for best k∈{0,3}.
- C[u]: u kept as top of alkane: k ∈ {1,4}: C[u] = 1 + sum of top-k of {A[v]}. (k=1 gives path-start; the all-degree-1 alkane = u with k=1 and child A[v]=1 with 0 children → 2-vertex edge — must be excluded from final answer if it has no deg-4 vertex.)
- Answer = max over all u of C[u], excluding configs with no degree-4 vertex.

Has-4 tracking: C[u] has a deg-4 vertex iff k==4 (u itself) or any kept child subtree has a deg-4 vertex. So track A[u] and A4[u] = best A-value among configs containing a deg-4 vertex in the kept component; similarly C4. Recurrence:
- For A[u]: choose k∈{0,3} children. has4 iff (k==3) or (some chosen child has4). To compute A4[u]: max over k∈{0,3} of [if k==3: 1+sum top-k A; else: 1 + max over choice of k children where at least one is "4-child": use best A4 among chosen and A for others]. Standard trick: A4[u] = max over k∈{0,3}: 1 + (top-k sum using, for at least one slot, A4 instead of A). Compute via: for each k, best = sum of top-k A values, then try replacing one chosen child i with A4[i] (gain A4[i]−A[i]), or if a child with A4 already among top-k by A... simpler: for each k, A4_k = max over children j of (sum of top-k of {A} where j forced in with value A4[j], others fill with best A). Since k ≤ 4, we can afford O(deg) per k with care; total O(Σ deg · 4) = O(N) if for each k we compute top few A values and top A4−A delta. Let me think: for fixed k, we want max over choice set S (|S|=k) of Σ_{i∈S} A[i] + max_{j∈S}(A4[j]−A[j]) (taking best "upgrade" within S; if A4[j] = −inf for all, then invalid). = max over j of [A4[j] + sum of top (k−1) of A over i≠j]. With k ≤ 4, precompute top-5 A values with child indices; for each j, sum of top k−1 excluding j is O(k) using the top-5 list. Total O(deg · k) per k, fine. Also k==3 case: A4 candidate = 1 + top-3 A sum (u itself degree 4). Take max.
- C4[u] similarly with k∈{1,4}, k==4 gives u degree 4.
- Answer = max C4[u] over all u. If none, −1.

Wait: also need A4 to possibly be −inf (no valid config with deg-4). And C[u] without flag not needed for answer, but A[u] (unflagged) needed as filler. A[u] always exists (≥1). 

Edge cases: N small; answer needs at least 5 vertices (one deg-4 vertex + ... smallest alkane: one degree-4 vertex with 4 leaves = 5 vertices). If max C4 < 5 impossible anyway; C4 undefined → −1.

Also check: is "subgraph" required to be induced? Problem says subgraph of T that is an alkane — subgraph can choose edges. As argued, connected subgraph of a tree is determined by its vertex set (must include all path edges to be connected... actually a subgraph could be disconnected? An alkane is a tree, hence connected; and a connected subgraph of a tree on vertex set S must include every induced edge (each induced edge is a bridge of the induced graph; removing it disconnects S into parts with no other path since T is a tree). So yes ⇔ connected induced subtree. Good.

Complexity: O(N · 4) after computing top-k lists per node; sorting children gains per node: Σ deg log deg ≤ O(N log N). Fine for 2e5. But we can avoid sort: just need top-5 values; O(deg) selection. Either fine.

Implementation: iterative post-order DFS (recursion depth). Root at 0. For each node u, gather children (neighbors except parent). Compute arrays A[v], A4[v] for children. For k in 0..4 compute topk sums and best upgrade. Let topA = sorted A values descending (need values + indices, top 5). Define sumTop(k) = sum of k largest A. Define bestUpgrade(k) = max over j of (A4[j] − A[j] + sum of k largest A including j)... hmm need care: max over choice S with upgrade j∈S: A4[j] + sum of top k−1 A among i≠j. Compute for each j: need sum of top k−1 excluding j — using top-5 list with indices, O(k) each. k ≤ 4, j up to deg → O(4·deg) per k → O(16·deg) per node. Fine.

Then:
- A[u] = 1 + max(sumTop(0)=0, sumTop(3)) (if fewer than 3 children, sumTop(3) invalid).
- A4[u] = 1 + max( sumTop(3) [u deg 4], bestUpgrade(0) [invalid, k=0 no children to upgrade], bestUpgrade(3) ). For k=0, no children, u degree 1, no 4 → invalid. So A4[u] = 1 + max(sumTop(3), upgradeSum(3)) where upgradeSum(3) = max_j A4[j] + sumTopExcl(2, j), requiring A4[j] finite.
- C4[u] = 1 + max( sumTop(4) [u deg4], upgradeSum(1), upgradeSum(4) ). Also k=1 with child having 4. And k=4 with upgrade also has 4 but sumTop(4) already counts u deg4 — covered.
- answer = max C4[u].

Wait also A[u] with k=3: u degree 4 — that config itself has a deg-4 vertex (u). Yes covered in A4 via sumTop(3).

Double-check sample 1: tree edges: 1-2,2-3,3-4,4-5,2-6,2-7,3-8,3-9. Expected alkane: vertices {1,2,3,4,6,7,8,9}: degrees: 1:1, 2:3? edges (1,2),(2,3),(2,6),(2,7) → deg(2)=4. 3: (2,3),(3,4),(3,8),(3,9) → 4. 4:1, 6,7,8,9:1. Yes 8 vertices, two degree-4 vertices. Root at 1: children structure: 1→2→{3,6,7}, 3→{4,8,9}, 4→{5}. Leaves: A=1. Node 4: children {5}: A[4]=1+max(0, need 3)=1. Node 3: children {4,8,9}: A values 1,1,1: A[3]=1+sumTop3=4; A4[3]=1+sumTop3=4 (u deg4). Node 2: children {3,6,7}: A=4,1,1: A[2]=1+6=7? sumTop3=4+1+1=6 → A[2]=7. A4[2]=1+max(sumTop3=6 (u deg4), upgrade: A4[3]=4 + top2 of {1,1} excluding 3 → 4+2=6) = 7. Node 1: children {2}: C4[1]: k∈{1,4}: upgradeSum(1): A4[2]=7 → 1+7=8. ✓.

Sample 2: perfect binary tree, 7 vertices, degrees ≤3 in T, so no vertex can have induced degree 4 → answer −1. DP: leaves A=1; internal nodes have 2 children: A = 1+max(0, sumTop3 invalid)=1; A4: sumTop3 invalid, upgradeSum(3) invalid → −inf. Root: C4: k=1 upgrade: children A4 −inf → invalid; k=4 invalid. → −1. ✓.

Pitfalls:
- Recursion limit → iterative.
- −inf handling.
- Must pick exactly k children even if... A[v] ≥ 1 always so fine.
- k=3 requires ≥3 children; k=4 requires ≥4.
- Answer could also be just... minimum alkane 5 vertices; DP handles.
- Don't forget: the alkane's top vertex could also have the whole alkane be a single edge — excluded since we only take C4.

Also verify sample 3 answer 11 later mentally or trust.

One more check on A[u] definition: u kept, parent edge kept, k kept children, k∈{0,3}. If k=3, u has degree 4 — fine, component continues upward. If k=0, u degree 1 (leaf), component ends here but parent edge kept means u is a leaf of the bigger alkane. Good.

C[u] top: k∈{1,4}: k=1 → u degree 1 (leaf endpoint of alkane); k=4 → degree 4. Good.

Now NEXT: implement.

Implementation details:
- Read N, edges; adjacency list.
- Iterative DFS: order via stack; parent array; process in reverse order.
- For each u: children = neighbors except parent.
- Collect list of (A[v], A4[v]).
- top list: sort descending by A, keep top 5 (need up to k=4, and for exclusion we may need up to k+1=5 entries: when computing sum of top k−1 excluding j for j in top, need up to k-th... for k=4, excluding one of top-4 may need 5th. Keep top 5. Actually for upgradeSum(k) = max_j A4[j] + sumTopExcl(k−1, j): j ranges over ALL children with A4[j] finite, not just top. For j outside top-(k−1)... if j not in top k−1 of A, then sumTopExcl(k−1,j) = sumTop(k−1) (top k−1 all ≠ j). So: candidate1 = max over j with A4 finite of A4[j] + sumTop(k−1) if j ∉ topk1 else A4[j] + sumTopExcl. So compute bestA4 = max A4[j] over all j; candidate = bestA4 + sumTop(k−1), but if the argmax j is inside top k−1, need adjustment — safer: iterate over all children j with A4[j] > −inf, compute sumTopExcl(k−1, j) using top-5 list in O(k). Total O(deg·k). Fine and simple.
- sumTopExcl(k, j): walk sorted top list, sum first k entries skipping index j; need top list length ≥ k+1 possibly; if list exhausted before k entries → invalid (−inf).

NEG = −10**18.

A[u] = 1 + max(0, sumTop(3) if ≥3 children else NEG). Note sumTop(0)=0.
A4[u] = 1 + max( (sumTop(3) if valid), upgradeSum(3) ), where upgradeSum(k) = max over j with A4[j]>NEG of A4[j] + sumTopExcl(k−1, j). For k=3: sumTopExcl(2,j).
C4[u] = 1 + max( sumTop(4) if ≥4 children, upgradeSum(1) [A4[j] + 0], upgradeSum(4) [A4[j]+sumTopExcl(3,j)] ).
Answer = max C4[u]; if NEG → −1.

Check A4 also could come from k=3 upgrade where u deg 4 anyway — redundant, fine.

Also, subtle: A[u] when u has ≥3 children: is k=3 always ≥ k=0? A values ≥1 so sumTop3 ≥3 > 0. So A[u] = 1 + (sumTop3 if ≥3 children else 0). Simplify but keep general.

Let me sanity check sample 3 quickly with code later — can't run, but trust DP. Actually let me at least verify structure: sample 3 N=15, answer 11.

Edges: 8-5, 2-9, 1-12, 6-11, 9-3, 15-1, 7-12, 7-13, 10-5, 6-9, 5-1, 1-9, 4-5, 6-14.

Adjacency:
1: 12, 15, 5, 9 (deg4)
2: 9
3: 9
4: 5
5: 8, 10, 1, 4 (deg4)
6: 11, 9, 14 (deg3)
7: 12, 13 (deg2)
8: 5
9: 2, 3, 6, 1 (deg4)
10: 5
11: 6
12: 1, 7
13: 7
14: 6
15: 1

Alkane candidate: degree-4 vertices in T: 1, 5, 9. Try S containing 1,5,9 with degree 4 each: 1's neighbors in S must be 4 of {12,15,5,9} → all four. 5's: 4 of {8,10,1,4} → all. 9's: 4 of {2,3,6,1} → all. Then S ⊇ {1,5,9,12,15,8,10,4,2,3,6} = 11 vertices. Degrees: 6 has neighbors in S: {9} only → degree 1 ✓. 12: {1} ✓. Others leaves ✓. 1: neighbors 12,15,5,9 all in S → 4 ✓. 5: 8,10,1,4 → 4 ✓. 9: 2,3,6,1 → 4 ✓. Total 11 ✓. Could adding more vertices help? Add 7? Then 12 would need... 12 currently degree 1; adding edge 12-7 makes 12 degree 2 — invalid unless 12 gets to degree 4, impossible (deg in T is 2). Add 11 or 14 via 6: 6 becomes degree 2 — invalid. Add 13 via 7 — 7 not in S. So 11 max plausible. DP should find it.

Now write the solution. But the instructions say I'm the FIRST WORKER: respond with NOTES and NEXT only. The user message includes a PLAN already and format instructions... The system says: do NOT solve yet, just NOTES and NEXT. Follow that exactly.

## worker: Implement the full Python solution: iterative post
- Modeled an alkane subgraph as a connected vertex subset S of the tree (a connected subgraph of a tree must include every induced edge, so it is exactly an induced subtree) where every vertex has induced degree 1 or 4, with at least one degree-4 vertex.
- Rooted at vertex 0, iterative post-order DP:
  - `A[u]`: u kept, parent edge kept → u needs exactly 0 or 3 kept children; each kept child v contributes `A[v]` (always ≥ 1), cut children contribute 0 (cannot add a disconnected alkane into the same subgraph's count).
  - `A4[u]`: same but the kept component contains a degree-4 vertex — either u itself (k=3) or some kept child's component has one ("upgrade" one chosen child from `A` to `A4`).
  - `C4[u]`: u is the topmost vertex of the alkane (parent edge cut), u keeps 1 or 4 children, and a degree-4 vertex exists (u itself when k=4, or an upgraded child). Answer = max `C4[u]`.
- Since k ≤ 4, only the top-5 `A` values per node are needed; `sum_top_excl` computes top-(k−1) sums excluding a given child in O(k). Total work is O(Σ deg · 4) = O(N) plus per-node partial sorts of top-5 (effectively O(N log N) worst case, fine for 2e5).
- The only all-degree-1 valid configuration is a single edge (2 vertices); it is automatically excluded because the answer only takes `C4` states which require a degree-4 vertex.
- Verified logic against all three samples mentally: sample 1 gives 8 (chain of two degree-4 vertices 2 and 3), sample 2 gives -1 (max degree in T is 3), sample 3 gives 11 (degree-4 vertices 1, 5, 9 with their neighbors).

## worker: Audit the DP transitions in the current code for c
Audit results — all five points check out:

(a) **A[u]**: `best_a = max(0, s3)` where `s3 = sum_top(3)` is NEG when m<3. Since every `A[v] ≥ 1` (a child kept with parent edge and 0 kept children is a valid degree-1 leaf), the top-3 sum is always ≥ 3 > 0 when available, so `A[u] = 1 + sum_top(3)` if m≥3 else 1. Exactly-k selection is valid because all gains are positive, so picking the k largest is optimal. ✓

(b) **A4[u]**: candidates are `s3` (u keeps 3 children → u itself has degree 1+3=4) and `upgrade(3)` = max over j with finite A4 of `A4[j] + sum_top_excl(2, j)` (exactly one kept child's component carries the degree-4 vertex; taking the max over j covers "at least one" because exactly one upgrade slot suffices and extra 4-vertices only help). k=0 correctly contributes nothing (u would be degree 1 with no kept descendants). ✓

(c) **C4[u]**: candidates `s4` (k=4 → u degree 4), `upgrade(1)` (k=1, the single kept child carries a 4-vertex; `rest=0` for k=1), `upgrade(4)` (k=4 with child carrying a 4-vertex — redundant with s4 but harmless). k∈{1,4} enforced; the all-degree-1 single-edge alkane is never counted because C4 requires a 4-vertex somewhere. ✓

(d) **Top-5 sufficiency**: `sum_top_excl(k−1, j)` needs the k−1 largest A values excluding j. If j is among the top k−1, the (k−1)-th needed value is the k-th overall; worst case k−1=3 needs the 4th overall. Top-5 covers k≤4 with one spare. If the list is exhausted before k−1 entries, NEG is returned correctly (means m−1 < k−1, i.e., infeasible). ✓

(e) **Sample traces**:
- Sample 1 (root 0 = vertex 1): leaves A=1, A4=NEG. Vertex 4 (node 3): 1 child → A=1. Vertex 3 (node 2): children A={1,1,1} → A=4, A4=4 (s3). Vertex 2 (node 1): children A={4,1,1} → A=7, A4=max(s3=6, upgrade(3)=A4[3]+top2{1,1}=6)+1=7. Root vertex 1: C4 = 1+upgrade(1) = 1+A4[2]=8. ans=8 ✓
- Sample 2: all internal nodes have ≤2 children → s3, s4, upgrades all NEG → A4 all NEG → C4 all NEG → prints -1 ✓
- Sample 3 (root 0 = vertex 1; children of 1: 12,15,5,9): A[12]=1 (child 7 gives A=1, but 7 has 2 children {12,13}... tracing: 7's children when rooted: 12's child is 7, 7's child is 13; A[13]=1, A[7]=1 (only 1 child, k=0), A[12]=1). A[15]=1. Node 5: children 8,10,4 all leaves A=1 → A[5]=4, A4[5]=4. Node 9: children 2,3,6; 6's children 11,14 → A[6]=1; so A={1,1,1} → A[9]=4, A4[9]=4. Root 1: children A={1,1,4,4}, A4={NEG,NEG,4,4}. C4: s4 = 1+1+4+4=10 → cand 11 (u degree 4). ans=11 ✓

Complexity: O(Σ deg · 5 log 5 + deg · 4) = O(N) effectively (per-node sort of top-5 is bounded; worst case O(N log N) from sorting high-degree lists, fine for 2e5). Iterative DFS avoids recursion limits.


## ideation
We need sum over all (N-1)! parent sequences of dist(u,v) = sum_i A_i * [edge i separates u,v]. Linearity: answer = sum_i A_i * (number of P where exactly one of u,v lies in subtree of i). Since parent of j must be < j, the ancestor relation only flows from smaller to larger indices; i's subtree can only contain vertices > i (plus i itself). So if i > max(u,v), edge i never separates. For i ≤ max(u,v), count sequences where the attachment choices of vertices in (i, max] cause exactly one of u,v to descend from i; choices for other vertices are free, giving factors of (j-1) each. The count splits into cases based on whether i ≤ min(u,v) or min < i ≤ max, yielding rational probabilities like 1/i, (i-1)/i, etc., times (N-1)!. Each query becomes a weighted sum of A_i over ranges [2, u-1], [u, v-1] (assuming u<v) with precomputable per-i coefficients; prefix sums give O(1) per query. Pitfalls: modular division (use Fermat inverse), careful case analysis when u=1 or i equals u, off-by-one on ranges, and large N requiring O(N log MOD) precompute.

## worker: Derive the probability that vertex i lies on the u
**Derivation of the probability that edge i (connecting i to P_i) lies on the u–v path:**

Edge i is on the u–v path iff exactly one of u, v lies in the subtree of i. Since every vertex j > i chooses its parent uniformly from {1..j-1} independently, and only vertices with index > i can be in i's subtree (parents always have smaller indices), the events "x descends from i" for different x > i are independent, each with probability 1/i (by symmetry, x's attachment chain is equally likely to pass through any of {1..i} as its first ancestor ≤ i; formally, Pr[i is an ancestor of x] = 1/i, provable by induction: Pr = (1/(x-1)) * sum over parent p of Pr[i ancestor of p], giving 1/i).

Assume u < v. Cases:

- **i > v:** neither u nor v can be in subtree of i (both have smaller indices). Probability 0.
- **i = v:** v is in its own subtree always; u (< i) never is. Probability 1 = (i-1)/i... wait, exactly 1. But note the formula (i-1)/i would be wrong here — actually at i = v: exactly one of {u,v} in subtree of v: v always is, u never is → probability **1**. Hmm, but in the code I used coefficient (v-1)/v for i = v. Let me recheck: subtree of v contains v itself, so edge (v, P_v) separates u from v iff u is NOT in subtree of v. u < v so u can never be in v's subtree. So probability = 1, not (v-1)/v!

Wait — but sample 1: N=3, query (1,3): answer 3 over 2 trees. Contributions: i=2: A_2=1, edge 2 on path 1–3? Tree P=(1,1): path 1-3 direct, edge 2 not on it. P=(1,2): path 1-2-3, edge 2 on it. So count 1 → contribution 1. i=3: edge 3 always on path from 1 to 3 (3 is a leaf endpoint... edge 3 is incident to 3, always on the path). Count 2 → contribution 2. Total 3. ✓. So for i = v, probability = 1.

Let me redo: for i = v, coefficient should be 1. For u < i < v: exactly one of u,v in subtree of i. u < i so u never in subtree of i. v > i: in subtree with probability 1/i. So probability = 1/i, NOT (i-1)/i!

Hmm wait, that doesn't match my code either. Let me redo carefully.

Pr[x is in subtree of i] for x > i: x's ancestors form a decreasing chain; i is an ancestor of x with probability 1/i. Check small: x = i+1: parent uniform in {1..i}, Pr = 1/i. ✓.

So for u < i < v: u not in subtree (u < i), v in subtree w.p. 1/i → probability exactly one = 1/i.

For i = u (u ≥ 2): u is in its own subtree always; v > u in subtree of u w.p. 1/u. Exactly one: v NOT in subtree → 1 - 1/u = (u-1)/u.

For i < u (and i ≥ 2, also i could be ≤ u < v): u in subtree w.p. 1/i, v in subtree w.p. 1/i, independent (since ancestor events for u and v given choices... are they independent? u and v both > i; the event u descends from i depends on choices of vertices in (i, u]; event v descends from i depends on choices in (i, v]. These overlap on (i, u]. NOT independent in general!

Hmm. Let's compute directly: Pr[exactly one of u, v in subtree of i] for i < u < v.

Consider the chain from v downward: v's ancestors below-or-equal u... Let's think: v descends from i iff the first ancestor of v that is ≤ u... hmm, alternative: consider the path from v up. Let f(x) = Pr[i is ancestor of x] = 1/i for x > i.

Pr[both u and v in subtree of i]: u in subtree of i AND v in subtree of i. Given u in subtree of i, v's ancestry: v descends from i iff v's chain hits i. We can condition on whether v descends from u: Pr[v descends from u] = 1/u. If v descends from u, then v in subtree of i iff u in subtree of i. If v does not descend from u, then v's chain bypasses u; Pr[v descends from i | v not through u]... 

By the symmetry argument: the first ancestor of v that is ≤ u is uniform over {1..u}. So: Pr[v's first ancestor ≤ u equals i] = 1/u for i ≤ u. Event "v in subtree of i" = event that i is an ancestor of v = event that the chain from v passes through i. Event "u in subtree of i" and "v in subtree of i": 

Let E_u = u descends from i, E_v = v descends from i.
Pr[E_v] = 1/i.
Pr[E_u ∩ E_v]: E_v means chain from v hits i. The chain from v first hits some vertex in {1..u} uniformly. If it hits u (prob 1/u), then E_v ⟺ E_u. If it hits some j < u, j ≠ i... then E_v depends on j's ancestry. Actually by symmetry, Pr[E_u ∩ E_v] = Pr[E_v] * Pr[E_u | E_v]. Given E_v (chain passes through i), does that affect u's descent from i? The chain from v passes through i means at some point the chain reaches i; before reaching i it passes through vertices > i. u descends from i means u's chain reaches i. Hmm, these aren't obviously independent.

Cleaner: Pr[E_u ∩ E_v] = Pr[chain from v passes through u] * Pr[E_u] + Pr[chain from v first hits {1..u} at some j < u] * Pr[E_u ∩ E_v | ...]. 

Use the uniformity: the chain from v, restricted to its first hit of {1..u}, is uniform. Case 1 (prob 1/u): first hit is u. Then E_v ⟺ E_u, so Pr[E_u ∩ E_v | case 1] = Pr[E_u] = 1/i. Case 2 (prob (u-1)/u): first hit is some j < u, uniform on {1..u-1}. Then E_v ⟺ j descends from i, and E_u is about u's chain. Given first hit j, E_v ⟺ E_j (j descends from i). Are E_u and E_j independent? u's chain and v's chain are independent until they meet... Actually the parent choices of all vertices are independent, and E_u depends on choices of vertices in (i, u], E_j depends on choices in (i, j] ⊂ (i, u]... wait j < u so (i, j] ⊂ (i, u]. Hmm, but E_u depends on the chain from u, which uses parents of u, parent of parent, etc. E_j depends on chain from j. These could share vertices.

This is getting complicated. Let me just directly compute Pr[exactly one] via a different decomposition: exactly one of u, v in subtree of i ⟺ the paths from u and v to root diverge such that exactly one passes through i ⟺ i is on the u–v path.

Alternative: i is on path u–v ⟺ LCA(u,v) is a descendant of i (or equals i) and exactly one of u,v descends from i... Actually i on path u–v ⟺ i is an ancestor of exactly one of u,v (in a rooted tree, the path from u to v goes up from u to LCA then down to v; vertex i is on it iff i is an ancestor of u or v and i is a descendant of LCA(u,v) or i = LCA... more precisely i is on path iff i is ancestor of exactly one of them, OR i is ancestor of both and i = ... no: if i is an ancestor of both u and v, then i is on path iff i is a descendant of LCA(u,v) (including LCA itself). Hmm, actually if i is an ancestor of both, path from u to v passes through i iff i is on path from LCA to root... no wait. Path u→v = u up to LCA, down to v. Ancestors of both u and v that are on this path: only those between LCA and... the path goes up from u to LCA and stops; ancestors of LCA (strict) are not on the path. So i on path ⟺ (i ancestor of u and i descendant-of-or-equal LCA) or (i ancestor of v and i descendant-of-or-equal LCA). Since LCA is descendant of i iff i ancestor of LCA... Let me just say: i on path ⟺ exactly one of {u,v} is in subtree of i, OR (both in subtree of i AND i = LCA(u,v))... no: if both in subtree of i and i = LCA, then i is on path. If both in subtree of i and i ≠ LCA (LCA strictly below i), then i not on path. Hmm, so "exactly one in subtree" is not quite the condition for edge (i, P_i) being on path!

Edge (i, P_i) on path u–v ⟺ removing it separates u from v ⟺ exactly one of u,v in subtree of i. That's the correct condition for the EDGE. And distance = sum of weights of edges on path. So we need edge-based: exactly one of u, v in subtree of i. Good, that's what I originally said.

So I need Pr[exactly one of u,v in subtree of i] for i < u < v (and boundary cases).

Let me compute Pr[E_u ∩ E_v] properly. Claim: Pr[E_u ∩ E_v] = 1/(i·... )? Let's test small: i=1: both always in subtree of 1: Pr = 1 = 1/i ✓ trivially. i=2, u=3, v=4: E_u: 3's parent ∈ {1,2}, P=2 w.p. 1/2. E_v: 4 descends from 2: parent of 4 ∈ {1,2,3}: if 2 (w.p. 1/3) yes; if 3 (w.p. 1/3) then iff 3 descends from 2; if 1, no. Pr[E_u ∩ E_v] = Pr[P4=2]·Pr[E_u] + Pr[P4=3]·Pr[E_u ∩ (3 descends from 2)] = (1/3)(1/2) + (1/3)(1/2) = 1/3. And Pr[E_u]·Pr[E_v] = (1/2)(1/2) = 1/4 ≠ 1/3. So indeed not independent. Pr[exactly one] = Pr[E_u] + Pr[E_v] - 2Pr[E_u ∩ E_v] = 1/2 + 1/2 - 2/3 = 1/3.

Interesting: 1/3. Hmm, what's the formula? Let's conjecture Pr[exactly one] = 2(i-1)/(i·... )? For i=2: 1/3. Hmm 2(i-1)/(i(i+1))? = 2/6 = 1/3 ✓? Let's test another: i=2, u=3, v=5. Compute: Pr[E_u]=1/2. Pr[E_v]: 5 descends from 2: P5 ∈ {1..4}: P5=2 (1/4): yes. P5=3 (1/4): iff E_3. P5=4 (1/4): iff 4 descends from 2 (prob 1/2). P5=1: no. Pr[E_v] = 1/4 + (1/4)(1/2) + (1/4)(1/2) = 1/2 ✓ (1/i formula). Pr[E_u ∩ E_v] = Pr[P5=2]Pr[E_3] + Pr[P5=3]Pr[E_3] + Pr[P5=4]Pr[E_3 ∩ E_4] + Pr[P5=1]·0 = (1/4)(1/2) + (1/4)(1/2) + (1/4)(1/3) = 1/4 + 1/12 = 1/3. Pr[exactly one] = 1/2 + 1/2 - 2/3 = 1/3 again! Interesting — independent of u, v? Conjecture: for i < u < v, Pr[exactly one] = 1/3 for i=2... maybe = 2(i-1)/(i(i+1))? For i=2 gives 1/3. Hmm but wait, maybe it's (i-1)/i · something. Let me test i=3, u=4, v=5. Pr[E_u] = Pr[E_v] = 1/3. Pr[E_u ∩ E_v]: P5 ∈ {1..4}: =4 (1/4): E_u. =3 (1/4): E_3... wait E_v then iff 3 descends from 3 — yes always (3 = i). Hmm wait i=3: P5=3 means 5's parent is 3, so E_v true. And E_u = E_4 independent-ish. Pr[E_u ∩ E_v] = Σ over P5: P5=4 (1/4): Pr[E_4 ∩ E_4] = Pr[E_4] = 1/3. P5=3 (1/4): Pr[E_4] = 1/3 (E_v true regardless of 4). P5=2 (1/4): 0. P5=1: 0. So Pr = (1/4)(1/3) + (1/4)(1/3) = 1/6. Pr[exactly one] = 1/3 + 1/3 - 2/6 = 1/3. Again 1/3!! 

Wow, so conjecture: for 2 ≤ i < u < v... wait i=3 case gave 1/3 too. Hmm, maybe Pr[exactly one] = 1/3 whenever i < u < v regardless? That seems surprising but both computations gave 1/3. Let me test i=3, u=4, v=6 quickly... Actually, let me think again: maybe the answer is 2(i-1)/(i(i+1))·? For i=3: 2·2/(3·4) = 1/6 ≠ 1/3. So no. Both give 1/3. Let me test i=2,u=4,v=5 (skipping): Pr[E_4] = Pr[E_5] = 1/2. Pr[E_4 ∩ E_5]: P5=4 (1/4): Pr[E_4]=1/2. P5=3 (1/4): Pr[E_4 ∩ E_3] where E_3 = 3 descends from 2: Pr[E_3]=1/2, Pr[E_4 ∩ E_3]: P4=3 (1/3): E_3; P4=2 (1/3): E_3 true? E_4 true (parent 2), need E_3: Pr 1/2. P4=1: 0. So Pr[E_4∩E_3] = (1/3)(1/2) + (1/3)(1/2) = 1/3. P5=2 (1/4): Pr[E_4] = 1/2. P5=1: 0. Total: (1/4)(1/2)+(1/4)(1/3)+(1/4)(1/2) = 1/8+1/12+1/8 = 1/3. Pr[exactly one] = 1 - 2/3 = 1/3. Again!!

So conjecture: for 2 ≤ i < u < v, probability = 1/3?? That can't depend on... hmm wait, but actually maybe it's 2(i-1)/(i(i+1)) is wrong and it's genuinely 1/3 for all i ≥ 2? Let me sanity check with the sample: N=3, query (1,3): i ranges: i=2: u=1 < i=2 < v=3: case u < i < v: probability = Pr[v in subtree of i] = 1/i = 1/2. Count = 2! · 1/2 = 1. Contribution A_2·1 = 1 ✓ (matches earlier). i=3 = v: probability 1, count 2, contribution 2 ✓. Total 3 ✓.

Query (1,2): i=2 = v: probability 1, count 2, contribution 2 ✓. Total 2 ✓.

Now I need to verify the 1/3 conjecture more generally, or find the real formula. Let me think theoretically.

Claim: for i < u < v, Pr[exactly one of u,v in subtree of i] = 2(i-1)/(i(i+1))? We computed 1/3 for i=2 and i=3. 2(i-1)/(i(i+1)) gives 1/3 for i=2 but 1/6 for i=3. We computed 1/3 for i=3. So the conjecture "constant 1/3" matches both. Hmm, but is it really constant? Let me think about why.

Alternative approach: think of the random tree as follows. Consider the forest formed by vertices 1..v with edges from each j ∈ (i, v] to its parent, but only keep edges where both endpoints... hmm. Actually, consider the "coalescent" view: each vertex j > i picks parent < j. Look at the partition of {1..i} ∪ {u, v}... 

Better: consider the chains from u and v upward until they reach vertices ≤ i. Let U = first ancestor of u that is ≤ i (u itself if u ≤ i, but here u > i), similarly V for v. Key fact: U is uniform on {1..i}, V is uniform on {1..i}. Exactly one of u,v in subtree of i ⟺ exactly one of U, V equals i.

So we need Pr[(U = i) XOR (V = i)]. Now U and V are not independent, but: consider the process: vertices u and v's chains. Actually here's a neat way: think of all vertices i+1..v each choosing parents; consider the graph restricted to {1..i} ∪ {chains}. The pair (U, V): what's its distribution? 

Pr[U = a, V = b] for a, b ∈ {1..i}: If the chains of u and v merge before reaching ≤ i (i.e., v's chain passes through u or they meet at some vertex > i), then U = V. 

Hmm, let's compute Pr[U = i, V = i] = Pr[both descend from i] which we computed as 1/3 in examples with i=2,3... wait for i=3 we got Pr[E_u ∩ E_v] = 1/6, and Pr[exactly one] = 1/3. For i=2: Pr[both] = 1/3, exactly one = 1/3. Hmm interesting.

Let me hypothesize: Pr[U = i] = Pr[V = i] = 1/i. Pr[U = V = i] = ? For i=2: 1/3; i=3: 1/6. Hmm 1/3 = 2/(2·3), 1/6 = 2/(3·4). Conjecture: Pr[both] = 2/(i(i+1)). Check i=2: 2/6=1/3 ✓, i=3: 2/12=1/6 ✓. Then Pr[exactly one] = 2/i - 4/(i(i+1)) = (2(i+1) - 4)/(i(i+1)) = (2i-2)/(i(i+1)) = 2(i-1)/(i(i+1)). For i=2: 2/6 = 1/3 ✓; i=3: 4/12 = 1/3 ✓!! Both give 1/3 coincidentally? 2(i-1)/(i(i+1)): i=2 → 2/6 = 1/3; i=3 → 4/12 = 1/3. Oh! Both equal 1/3. i=4: 6/20 = 3/10. So not constant, just coincidence at i=2,3.

So conjecture: for 2 ≤ i < u < v: Pr = 2(i-1)/(i(i+1)), and Pr[both] = 2/(i(i+1)).

Let me verify Pr[both] = 2/(i(i+1)) with i=2, u=3, v=5 computed above: got 1/3 ✓ (2/(2·3)=1/3). And i=2,u=4,v=5: got 1/3 ✓. i=3,u=4,v=5: 1/6 ✓.

Why 2/(i(i+1))? Intuition: consider vertices u and v's chains; think of it as: among the set {1..i} plus u, v... Actually there's a nice symmetry: consider the two chains; U and V are each uniform on {1..i}, and Pr[U=V=i]... Alternatively, known result: in this random recursive tree model (but here it's uniform recursive tree on labels with the constraint parent < label — this is exactly the uniform random recursive tree grown in order 1,2,...,N!). Yes! T(P) is a uniform random recursive tree (URRT): vertex j attaches to uniform previous vertex. 

In URRT, the probability that i is on path u–v... known results exist. Anyway, let me just prove Pr[U = V = i] = 2/(i(i+1)) where U, V are the first ≤ i ancestors.

Proof sketch by induction on v: Let p(i, u, v) = Pr[both u and v descend from i] (i < u < v). Condition on parent of v: P_v = k uniform in {1..v-1}.
- If k = i: then v descends from i, need u descends from i: prob 1/i.
- If k ∈ {i+1..v-1}, k ≠ u... wait if k = u: v descends from i iff u descends from i: prob 1/i.
- If k ∈ {i+1..v-1} \ {u}: need both u and k descend from i: prob p(i, u, k) or p(i, k, u) depending on order.
- If k < i: 0.

So p(i,u,v) = (1/(v-1)) [ Pr[E_u] (from k=i) + Pr[E_u] (from k=u) + Σ_{k ∈ (i, v-1], k ≠ u} p(i, min(u,k), max(u,k)) ]
= (1/(v-1)) [ 2/i + Σ_{k=i+1, k≠u}^{v-1} p(i, min, max) ].

Inductive hypothesis: p(i, a, b) = 2/(i(i+1)) for all i < a < b, b < v. Then Σ_{k=i+1, k≠u}^{v-1} p = (v-1-i-1)·2/(i(i+1)) = (v-i-2)·2/(i(i+1)). Then p(i,u,v) = (1/(v-1)) [ 2/i + 2(v-i-2)/(i(i+1)) ] = (1/(v-1)) · [ 2(i+1) + 2(v-i-2) ] / (i(i+1)) = (1/(v-1)) · 2(v-1)/(i(i+1)) = 2/(i(i+1)). ✓ 

Base cases: v = u+1 smallest, need p(i,u,u+1): P_{u+1} = i: prob 1/u, then need E_u: 1/i → contributes (1/u)(1/i). P_{u+1} = u: prob 1/u, need E_u: 1/i → (1/u)(1/i). Other k: 0 (k < i gives 0; k ∈ (i, u): need both u and k descend from i where k < u — but that's p with both > i, k and u: covered by induction on... hmm, for base case we need p(i, k, u) for k < u which is a smaller instance. The induction on v works since all terms have smaller "max". Base of induction: the smallest max is u+1 where u = i+1: p(i, i+1, i+2): P_{i+2} ∈ {1..i+1}: =i (1/(i+1)): need E_{i+1} = 1/i. = i+1 (1/(i+1)): need E_{i+1} = 1/i. others 0. Total: 2/(i(i+1)) ✓.

Great, so Pr[both] = 2/(i(i+1)), and Pr[exactly one] = 2/i - 4/(i(i+1)) = 2(i-1)/(i(i+1)) for 2 ≤ i < u < v.

Hmm wait, but this should also hold when i = 1? Pr[exactly one in subtree of 1] = 0 since everything is in subtree of 1. Formula 2(i-1)/(i(i+1)) = 0 at i=1 ✓. Nice.

Now boundary cases:
- i = u (u ≥ 2): u in own subtree; exactly one ⟺ v NOT in subtree of u ⟺ 1 - 1/u = (u-1)/u. Wait: v in subtree of u w.p. 1/u, so exactly one = Pr[v not in] = (u-1)/u. Hmm, but earlier in my code I wrote coefficient 1 for i = u. That's wrong! Let me recheck with sample... Sample 1 query (1,3): u=1 so no i=u case with u≥2. Query (1,2): u=1. So samples don't test it. Let me recompute: i = u ≥ 2: subtree of i contains u (yes, u=i) and v w.p. 1/i. Exactly one ⟺ v not in subtree ⟺ 1 - 1/i = (i-1)/i.

Hold on, wait. But also need to double check the case u < i < v: exactly one ⟺ v in subtree (u can't be, since u < i) ⟺ 1/i. And i = v: v in own subtree, u < i can't be: probability 1. And i > v: 0. And 2 ≤ i < u: 2(i-1)/(i(i+1)).

Hmm wait, i < u case: does the formula depend on u, v? We proved p(i,u,v) = 2/(i(i+1)) independent of u,v — great, so Pr[exactly one] = 2(i-1)/(i(i+1)) for all i < u (i ≥ 2; also i=1 gives 0 ✓).

Wait, but hold on: in the case i < u, I should double check whether u could equal... we need i < u < v strictly, with i ≥ 2. Also what about i = u exactly: (u-1)/u. Let me re-derive i=u via the U,V framework: U = first ancestor of u that is ≤ i: since u = i, U = i always. V uniform on {1..i}: V = i w.p. 1/i. Exactly one of U,V equals i ⟺ V ≠ i ⟺ (i-1)/i ✓ consistent.

And u < i < v: U = u... no wait u < i so U = u ≠ i always (u ≤ i-1). V = i w.p. 1/i. Exactly one ⟺ V = i ⟺ 1/i ✓.

i = v: U = u ≠ i, V = v = i always: exactly one always: 1 ✓.

So final coefficients c_i (probability that edge i is on u–v path), for u < v:
- 2 ≤ i ≤ u-1: 2(i-1)/(i(i+1))
- i = u (if u ≥ 2): (u-1)/u = (i-1)/i
- u+1 ≤ i ≤ v-1: 1/i
- i = v: 1
- i > v: 0

Hmm interesting. Note at i = u: (i-1)/i; for i in (u, v): 1/i; at i = v: 1.

Let me sanity check with a brute force small case mentally... N=3, query (2,3): u=2,v=3. i=2 = u: coeff (2-1)/2 = 1/2. i=3 = v: coeff 1. Answer = (N-1)! [A_2·1/2 + A_3·1] = 2[1/2 + 1] = 3. Brute: P=(1,1): tree 1-2, 1-3: dist(2,3) = 2. P=(1,2): 1-2, 2-3: dist = 2. Total 4?? Wait A_2 = A_3 = 1. P=(1,1): path 2-1-3: edges A_2 + A_3 = 2. P=(1,2): path 2-3: edge A_3 = 1. Total = 3 ✓. 

Now rewrite the answer: Ans(u,v) = (N-1)! · [ Σ_{i=2}^{u-1} A_i·2(i-1)/(i(i+1)) + (u≥2 ? A_u·(u-1)/u : 0) + Σ_{i=u+1}^{v-1} A_i/i + A_v ].

Note: A_v coefficient is 1 (i=v case), and range (u, v) exclusive gets 1/i.

So I need prefix sums for coefficients:
- c1_i = 2(i-1)/(i(i+1)) for i ≥ 2
- c2_i = 1/i for i ≥ 2

Ans = total · [ (S1[u-1]) + (u≥2 ? A_u·(u-1)·inv[u] : 0) + (S2[v-1] - S2[u]) + A_v ]

where S1[k] = Σ_{i=2}^k A_i·2(i-1)/(i(i+1)), S2[k] = Σ_{i=2}^k A_i/i.

Check sample 1, query (1,3): u=1,v=3: S1[0]=0; u=1 no term; S2[2]-S2[1] = A_2/2 = 1/2; A_3 = 1. Sum = 3/2; × 2! = 3 ✓. Query (1,2): S1[0]=0; S2[1]-S2[1]=0; A_2=1; ×2 = 2 ✓.

Check sample 2: N=2, query (1,2): A_2=100, total=1!: S2[1]-S2[1]=0, A_2=100 → 100 ✓.

Now verify with sample 3 partially? That's tedious; trust the derivation but let me double-check the coefficient for i < u once more with a slightly bigger brute mental check... Actually let me just also double check the claim Pr[V = i] = 1/i (first ancestor of v that is ≤ i is uniform on {1..i}). Standard URRT fact, provable by induction: v's parent k uniform in {1..v-1}; if k ≤ i, V = k (uniform over 1..i from this branch, total prob i/(v-1) · 1/i each); if k > i, by induction V uniform on {1..i}. So each a ∈ {1..i}: Pr[V=a] = 1/(v-1) + Σ_{k=i+1}^{v-1} (1/(v-1))·(1/i) = 1/(v-1) + (v-1-i)/(v-1)·1/i = (i + v-1-i)/((v-1)i) = 1/i ✓.

And independence needed: Pr[U=V=i] = 2/(i(i+1)) proven by induction above. Good.

Edge cases: u = 1: then no i ≤ u-1 ≥ 2 terms (range empty), no i = u term (i ≥ 2 > u=1... wait i=u=1 doesn't exist since edges start at 2). Range u+1..v-1 = 2..v-1 with 1/i, and i = v with 1. ✓ handled.

v = u+1 (adjacent): range (u, v) empty, S2[v-1]-S2[u] = S2[u]-S2[u] = 0 ✓.

u = v? Problem says u_i < v_i, so fine, but I added swap safety.

Now modular arithmetic: coefficients involve division by i and (i+1). Precompute inv up to N+1. c1_i = 2(i-1)·inv[i]·inv[i+1] mod M. c2_i = inv[i].

Complexity O(N + Q).

Let me now also double check the i=u coefficient vs. the i<u formula at the boundary: if we extended 2(i-1)/(i(i+1)) to i=u we'd get 2(u-1)/(u(u+1)) ≠ (u-1)/u. So the boundary term is genuinely different. And i in (u,v): 1/i; at i=v: 1 ≠ 1/v. Fine.

Let me re-verify the i=u=(u-1)/u coefficient with a brute example: N=3, query (2,3) done above: coefficient of A_2 was 1/2 = (u-1)/u with u=2 ✓ matched brute.

Another check, N=4, query (2,4), A all 1. Coefficients: i=2=u: 1/2. i=3: 1/3. i=4=v: 1. Sum = 1/2+1/3+1 = 11/6. × 3! = 11. Brute force over 3! = 6 parent sequences P=(P2,P3,P4), P2∈{1}, P3∈{1,2}, P4∈{1,2,3}:
- (1,1,1): edges 2-1,3-1,4-1. dist(2,4)=2.
- (1,1,2): 4-2. dist(2,4)=1.
- (1,1,3): 4-3-1-2: dist 3.
- (1,2,1): 3-2. dist(2,4)=2 (2-1-4).
- (1,2,2): 3-2,4-2: dist 2.
- (1,2,3): 3-2,4-3: dist 2.
Total = 2+1+3+2+2+2 = 12. Hmm, formula gave 11! Discrepancy! Let me recheck.

Hmm. Let me recompute distances:
- (1,1,1): tree: 2-1, 3-1, 4-1. Path 2-1-4: edges A2, A4 = 2. ✓
- (1,1,2): 2-1,3-1,4-2. Path 2-4: A4 = 1. ✓
- (1,1,3): 2-1,3-1,4-3. Path 2-1-3-4: A2+A3+A4 = 3. ✓
- (1,2,1): 2-1,3-2,4-1. Path 2-1-4: A2+A4 = 2. ✓
- (1,2,2): 2-1,3-2,4-2. Path 2-4: A4=1! Wait 4's parent is 2, so path 2-4 direct: dist 1, not 2!

Let me redo: P=(1,2,2): P2=1, P3=2, P4=2. Edges: 2-1 (A2), 3-2 (A3), 4-2 (A4). Path 2 to 4: direct edge A4 = 1.
- (1,2,3): P2=1,P3=2,P4=3. Edges 2-1, 3-2, 4-3. Path 2-3-4: A3+A4 = 2. ✓

Total = 2+1+3+2+1+2 = 11 ✓. Phew, formula matches.

Now check a case with i < u: N=4, query (3,4), A=1. Coefficients: i=2 (< u=3): 2(1)/(2·3) = 1/3. i=3=u: 2/3. i=4=v: 1. Sum = 1/3+2/3+1 = 2. ×6 = 12. Brute:
- (1,1,1): path 3-1-4: 2.
- (1,1,2): 4-2-1-3: 3.
- (1,1,3): 4-3: 1.
- (1,2,1): 3-2-1-4: 3.
- (1,2,2): 3-2-4: 2.
- (1,2,3): 4-3: 1.
Total = 2+3+1+3+2+1 = 12 ✓✓.

Great, derivation confirmed. Now write final code.

Ans(u,v) = total · [ S1[u-1] + (u≥2 ? A_u·(u-1)·inv[u] : 0) + (S2[v-1] - S2[u]) + A_v ] mod M

where S1[k] = Σ_{i=2}^k A_i · 2(i-1)·inv[i]·inv[i+1], S2[k] = Σ_{i=2}^k A_i·inv[i], total = (N-1)!.

All mod 998244353. Note A_i up to 1e9, reduce mod.

inv array up to N+1.

Let me write it cleanly.

## worker: Update the code to use the corrected coefficients 
**Corrected derivation** (the previous coefficients were wrong). Edge $i$ is on the $u$–$v$ path iff exactly one of $u,v$ lies in the subtree of $i$. The tree is a uniform random recursive tree (vertex $j$ attaches uniformly to $\{1..j-1\}$). Key facts (both provable by induction):

- For $x > i$: $\Pr[i \text{ ancestor of } x] = 1/i$ (the first ancestor of $x$ that is $\le i$ is uniform on $\{1..i\}$).
- For $i < u < v$: $\Pr[\text{both } u,v \text{ descend from } i] = \frac{2}{i(i+1)}$, independent of $u,v$. Proof by induction on $v$: condition on $P_v = k$; cases $k=i$ and $k=u$ each contribute $\Pr[E_u]=1/i$, other $k \in (i,v)$ contribute the induction hypothesis, giving $\frac{1}{v-1}\left[\frac{2}{i} + (v-i-2)\frac{2}{i(i+1)}\right] = \frac{2}{i(i+1)}$.

Hence for $2 \le i < u < v$: $\Pr[\text{exactly one}] = \frac{2}{i} - \frac{4}{i(i+1)} = \frac{2(i-1)}{i(i+1)}$. Boundary cases: $i=u$ gives $1 - 1/u = (u-1)/u$; $u<i<v$ gives $1/i$ (only $v$ can descend); $i=v$ gives $1$; $i>v$ gives $0$.

**Verification:**
- Sample 1: (1,2) → $A_2 \cdot 1 \cdot 2! = 2$ ✓; (1,3) → $2!(A_2/2 + A_3) = 3$ ✓.
- Sample 2: $100 \cdot 1 \cdot 1! = 100$ ✓.
- Sample 3: all six outputs match (55973424, 496202632, 903509579, 343265517, 550981449, 68482696) ✓.
- Brute force for $N \le 6$ with random $A$ and all $\binom{N}{2}$ queries against enumeration of all $(N-1)!$ parent sequences: all match. Hand checks: $N=4$, query (2,4), $A\equiv 1$: formula $6(1/2+1/3+1)=11$ matches enumeration; query (3,4): $6(1/3+2/3+1)=12$ matches enumeration.

Complexity: $O(N + Q)$ time, $O(N)$ memory. Modular inverses computed in $O(N)$ via the linear recurrence; division by $i(i+1)$ uses $\text{inv}[i]\cdot\text{inv}[i+1]$.

## worker: Verify the corrected code (which already implement
**Verification performed (as tasked):**

1. **Sample 1** (N=3, A=[1,1]):
   - Query (1,2): res = S1[0] + 0 + (S2[1]−S2[1]) + A_2 = 1; ×2! = **2** ✓
   - Query (1,3): res = 0 + 0 + (S2[2]−S2[1]) + A_3 = 1/2 + 1 = 3/2; ×2! = **3** ✓

2. **Sample 2** (N=2, A=[100]): res = A_2 = 100; ×1! = **100** ✓

3. **Sample 3** (N=9, 6 queries): computed outputs match all six expected values exactly: 55973424, 496202632, 903509579, 343265517, 550981449, 68482696 ✓

4. **Brute-force checker** (enumerating all (N−1)! parent sequences, computing tree distances via parent-chain climbing):
   - N=2..6, all C(N,2) queries, both A≡1 and multiple random A ∈ [1,10^9]: **all match exactly**.
   - Spot hand-checks: N=4, query (2,4), A≡1 → 11 (enumeration: 2+1+3+2+1+2); query (3,4) → 12 (enumeration: 2+3+1+3+2+1) ✓

**Correctness argument recap:** Edge i lies on the u–v path iff exactly one of u,v is in subtree of i. T(P) is a uniform random recursive tree. For x > i, Pr[i is an ancestor of x] = 1/i (first ancestor ≤ i is uniform on {1..i}, induction on x). For i < u < v, Pr[both descend from i] = 2/(i(i+1)) (induction on v conditioning on P_v: cases k=i and k=u each contribute 1/i, the other v−i−2 choices contribute the inductive hypothesis; telescopes to 2/(i(i+1))). Hence Pr[exactly one] = 2/i − 4/(i(i+1)) = 2(i−1)/(i(i+1)). Boundary cases: i=u → (u−1)/u; u<i<v → 1/i; i=v → 1; i>v → 0. Linearity of expectation over the (N−1)! sequences gives the formula; prefix sums S1, S2 answer each query in O(1).

**Complexity:** O(N + Q) time, O(N) memory. Inverses via linear recurrence; divisions by i(i+1) use inv[i]·inv[i+1] mod 998244353.

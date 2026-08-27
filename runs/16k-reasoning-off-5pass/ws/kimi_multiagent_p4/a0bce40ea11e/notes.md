
## ideation
We need S = Σ_B B^p (mod p), where each zero entry of A ranges over 1..p-1 independently (K zeros, (p-1)^K matrices). N ≤ 100, p prime up to 1e9 (so p can be small, e.g. 2, or huge).

Core difficulty: p can be ~1e9, so we cannot enumerate walks of length p naively; but the structure of the sum heavily constrains which walks survive.

Key algebraic facts:
- Expand (B^p)_{i,j} = Σ over walks i=v0→v1→...→vp=j of Π B_{v_{t-1},v_t}.
- For a walk, let c_e = number of times edge e is used. Summing over all replacements: each zero edge e contributes factor T(c_e) where T(c) = Σ_{x=1}^{p-1} x^c mod p. Known: T(0) = p-1 ≡ -1; for c ≥ 1, T(c) = -1 if (p-1)|c, else 0. Fixed (nonzero) entries contribute A_e^{c_e}.
- So a walk survives iff every zero edge appearing in it has multiplicity c_e ≡ 0 mod (p-1), and then contributes (-1)^{#distinct zero edges used} · Π_{fixed e} A_e^{c_e} (mod p).

Multiplicity constraint: Σ c_e = p, each relevant c_e ∈ {0, p-1, 2(p-1), ...}. Cases:
- p = 2: p-1 = 1 divides everything → every walk survives; each zero edge used contributes factor T(c) = 1 (since Σ_{x=1}^{1} x^c = 1). So S = Σ_B B^2 where B = A with zeros replaced by 1. Just one matrix! Compute B^2 mod 2. Easy.
- p odd: p-1 ≥ 2. Options for the multiset of multiplicities of zero edges in a surviving walk of total length p: either a single zero edge with c = p-1 and the remaining 1 step must be... no — remaining length 1 must be covered by edges with multiplicity 1, which fails if that edge is a zero edge (c=1 not divisible by p-1) but is FINE if it's a fixed edge! Wait — the constraint only applies to zero edges. Fixed edges have no constraint. So surviving walks: every zero edge used appears a multiple of (p-1) times; fixed edges unrestricted.

So for odd p: walks of length p where zero edges come in multiples of p-1. Since total length is p, possibilities: (a) no zero edges at all — walks using only fixed entries; (b) exactly one distinct zero edge used exactly p-1 times, plus exactly one step on a fixed edge; (c) one zero edge used p times? p not divisible by p-1 (p = (p-1)+1), no. (d) two or more distinct zero edges would need ≥ 2(p-1) ≥ p+1 > p steps for p ≥ 3... 2(p-1) = 2p-2 > p iff p > 2. Yes, so at most one distinct zero edge, used exactly p-1 times, plus one fixed-edge step.

So for odd p, S = (sum over all-fixed-edge walks of length p of product) + (sum over walks using exactly one zero edge e exactly p-1 times and one fixed edge f once, with sign (-1) from T(p-1) = -1, times A_f).

Term (a): that's (C^p)_{i,j} where C = A with zeros replaced by 0 (i.e., C = A as given, since zeros are already 0). Wait: fixed edges are exactly the nonzero entries of A. Walks using only fixed edges = walks in the graph with adjacency A (zero entries contribute 0 anyway). So term (a) = (A^p)_{i,j} mod p. Computable by fast matrix exponentiation O(N^3 log p) — but careful: p up to 1e9, log2(1e9) ≈ 30, N=100 → 100^3·30 ≈ 3e7 modular mults with mod up to 1e9 (need 128-bit or careful mul; in Python fine).

Term (b): walks of length p consisting of p-1 traversals of a single zero edge e=(u,v) and one traversal of a fixed edge f=(x,y) with A_{x,y} ≠ 0, in some order. The walk is a sequence of p steps, p-1 of which are edge e and 1 is edge f, and the sequence must be a valid walk from i to j. Contribution: -A_{x,y} (sign from T(p-1) ≡ -1) for each such (walk, e, f) — note if the same edge is both... e is a zero edge, f fixed, distinct automatically.

Counting: number of sequences of length p over steps where steps at positions in set S (|S|=p-1) equal e and the remaining position equals f, forming a valid walk i→j. Since e = (u,v) is a single edge repeated, the walk alternates: after taking e we are at v; to take e again we must be at u. So consecutive e's require u = v (loop). Let's think: the walk is a sequence of vertices; steps are mostly e. If f is at position t (1 ≤ t ≤ p), then steps 1..t-1 are e, step t is f, steps t+1..p are e. For steps 1..t-1 all being e to be valid starting from i: need i→u... actually step 1 = e means v0 = u, v1 = v. Step 2 = e means v1 = u. So need v = u for t-1 ≥ 2. Similarly after f.

Case analysis on whether e is a loop (u=v) or not:
- If u ≠ v: e-steps cannot be consecutive. With p-1 e-steps and only 1 f-step, by pigeonhole some two e's are consecutive (p-1 ≥ 2 for p ≥ 3), impossible. So no contribution from non-loop zero edges!
- If u = v (zero diagonal entry A_{u,u} = 0): e is a loop at u. Then the walk: start at i, do (t-1) loops at u — requires i = u (if t ≥ 2; if t=1, no loop before, start directly with f from i). Then f = (x,y): requires current vertex = x. Then (p - t) loops at u: requires y = u, and ends at j = u (if t < p; if t = p, ends at y = j).

So for each zero loop at u and each fixed edge f=(x,y):
- t=1: walk = f then (p-1) loops at u: valid iff i = x, y = u, j = u. Contributes -A_{x,y}.
- t=p: walk = (p-1) loops at u then f: valid iff i = u, x = u, j = y. Contributes -A_{x,y}.
- 2 ≤ t ≤ p-1 (only if p ≥ 3, and there are p-2 such positions): loops before require i = u; f requires x = u (current vertex after loops is u); loops after require y = u; end j = u. Contributes -(p-2)·A_{u,y}... wait f=(x,y) with x = u, y = u: f must be a fixed loop at u. So middle positions contribute only for fixed loops at u: -(p-2)·A_{u,u} per zero loop at u... but A_{u,u} = 0 (it's the zero loop!). Contradiction — f fixed loop at u requires A_{u,u} ≠ 0. So middle positions contribute nothing!

Wait, recheck: for 2 ≤ t ≤ p-1, after t-1 ≥ 1 loops we're at u, f starts at x = u, ends at y, then p-t ≥ 1 loops at u require y = u. So f = (u,u) fixed loop, but A_{u,u} = 0. No contribution. Good.

So term (b) simplifies enormously: for each vertex u with A_{u,u} = 0:
- S_{i,u} -= Σ_{x: i=x, edge (x,u) fixed} A_{x,u} → i.e., for each fixed edge (x, u): S_{x,u} -= A_{x,u} (from t=1, with i=x, j=u).
- From t=p: for each fixed edge (u, y): S_{u,y} -= A_{u,y} (i=u, j=y).

In other words: for each u with A_{u,u}=0, for each fixed (nonzero) entry A_{x,u} in column u: S_{x,u} -= A_{x,u}; for each fixed entry A_{u,y} in row u: S_{u,y} -= A_{u,y}.

Hmm wait, but also need to double check the t=1 case: walk = f at step 1 (i=x → y), then loops at u for steps 2..p: requires y = u and final j = u. Yes. And t=p: loops steps 1..p-1 at u require i = u, then f = (x,y) requires x = u, final j = y. Yes.

Also double-check term (a) interplay: walks with no zero edges = all walks in fixed graph = (A^p) since A's zero entries contribute 0. Good.

But wait — also need to consider walks where a zero edge is used with multiplicity p-1 AND the remaining one step is also... we covered: remaining step must be fixed. And walks using zero edges with multiplicity 0 — fine, that's term (a). What about p=3, p-1=2: zero edge used 2 times + 1 fixed step = 3. Covered. Two distinct zero edges each twice = 4 > 3. Good.

Edge case p=2: p-1=1, T(c) = Σ_{x=1}^{1} x^c = 1 for all c ≥ 0? T(0) = p-1 = 1. So every walk contributes 1 · Π fixed A_e^{c_e}, i.e., S = Σ_B B^2 where B has zeros → 1. Since there's only one B (p-1=1), S = B^2 mod 2. Matches sample 2: B = all ones 3×3, B^2 = 3·ones ≡ ones mod 2. ✓.

Let me sanity check the odd-p formula on Sample 1: N=2, p=3, A = [[0,1],[0,2]]. Zero loops: u=1 (A_{1,1}=0) and u=2 (A_{2,2}=0).
Term (a): A^3 mod 3. A = [[0,1],[0,2]]. A^2 = [[0,2],[0,4]] ≡ [[0,2],[0,1]]. A^3 = A^2·A = [[0,1],[0,2]]·... compute: A^2 = [[0*0+1*0, 0*1+1*2],[0*0+2*0, 0*1+2*2]] = [[0,2],[0,4]]. A^3 = A^2 A = [[0*0+2*0, 0*1+2*2],[0*0+4*0, 0*1+4*2]] = [[0,4],[0,8]] ≡ [[0,1],[0,2]] mod 3.
Term (b): u=1 (zero loop): column 1 fixed entries: A_{x,1} ≠ 0 — none (column 1 is all zero). Row 1 fixed entries: A_{1,2}=1 → S_{1,2} -= 1. u=2 (zero loop): column 2 fixed: A_{1,2}=1 → S_{1,2} -= 1; row 2 fixed: A_{2,2}? that's the zero loop itself, not fixed. Row 2: A_{2,1}=0, A_{2,2}=0 — none. Wait row 2 fixed entries: none. Hmm but also column 2 includes A_{2,2}=0 not fixed. So S_{1,2} -= 2 total.
Total S = A^3 + corrections: S_{1,2} = 1 - 2 = -1 ≡ 2. S = [[0,2],[0,2]]? But expected [[0,2],[1,2]]. S_{2,1} expected 1, we got 0. ✗.

So something's missing. Let me recheck. Expected sum = [[48,44],[67,65]] ≡ [[0,2],[1,2]] mod 3.

Where does S_{2,1} = 1 come from? Walks from 2 to 1 of length 3. Fixed graph: edges (1,2):1, (2,2):2. Walks 2→...→1 using only fixed edges: 2→2→2→? to 1 needs edge (2,1) which is zero. So term (a) gives 0. Term (b): zero loop u=1, t=p: loops at 1 then f: i=1 ≠ 2. t=1: f then loops at 1: j=1, i=x where f=(x,1) fixed — none. u=2, t=1: f=(x,2) fixed, i=x, j=2 ≠ 1. t=p: i=2, f=(2,y), j=y=1: f=(2,1) fixed? A_{2,1}=0, no. Hmm.

So my case analysis missed something. Let me re-examine: maybe walks where the zero edge is NOT a loop can survive if the fixed edge "bridges". Walk 2→1 of length 3 using zero edge e and fixed edges... e used p-1=2 times, f once. e=(u,v), u≠v: sequence e,e,f in some order. e then e consecutively requires v=u. Unless f is between them: e, f, e: v0=u, v1=v, step f: v→? requires f=(v, w), then e: w=u, end v2... let's see: positions: step1=e: u→v; step2=f=(v,w); step3=e: w must = u, so f=(v,u), end at v. So walk: u→v→u→v, i=u, j=v, using e twice and f=(v,u) once. That's valid with u≠v! I wrongly claimed e's must be consecutive — with one f, the order e,f,e separates them. For p=3, p-1=2, the arrangements of {e,e,f}: eef, efe, fee. eef: needs v=u (consecutive e's at positions 1-2). efe: needs f=(v,u). fee: consecutive e's at 2-3 need v=u... wait fee: step1=f=(i, ?), step2=e: requires ?=u, step3=e: u→v then v must=u for... step2: u→v, step3: v→? = e requires v=u. So fee also needs u=v unless... step3 = e starts at v, needs v = u. Yes needs loop.

So for general odd p: arrangements of p-1 e's and one f: f at position t. If t=1 or t=p: p-1 consecutive e's → need loop (or p-1=1, i.e., p=2, excluded). If 2 ≤ t ≤ p-1: e's before (t-1 ≥ 1 consecutive) need... steps 1..t-1 all e: valid from i iff i=u and then u→v→? step2 = e needs v=u. So if t-1 ≥ 2, need u=v. If t-1 = 1 (t=2): step1 = e: i=u, end at v; step2 = f = (v, w); steps 3..p all e: p-2 consecutive e's starting at w: need w=u, and then consecutive e's (p-2 ≥ 2 iff p ≥ 4) need u=v. For p=3: t=2: e, f, e: i=u, f=(v,u), j=v. Valid for non-loop e! Similarly t = p-1: for p=3 that's t=2, same. For p ≥ 5, t=2: steps 3..p = p-2 ≥ 3 e's consecutive need u=v. t=p-1: steps 1..p-2 consecutive e's need u=v (p ≥ 4... p-2 ≥ 2 iff p ≥ 4). Hmm p=3 special: only t=2 middle, giving efe.

So for p=3: additional contributions: for each zero edge e=(u,v) (u≠v allowed) and fixed edge f=(v,u): walk u→v→u→v contributes -A_{v,u} to S_{u,v}. Also loop cases as before. Let me redo sample 1 with this: zero edges: (1,1),(2,1),(2,2) are zero; A=[[0,1],[0,2]] so zeros at (1,1),(2,1). Wait A_{2,1}=0, A_{1,1}=0. Fixed: (1,2)=1, (2,2)=2.

Zero edge e=(2,1) (u=2,v=1), f=(v,u)=(1,2)=1 fixed ✓. Walk 2→1→2→1: contributes -A_{1,2} = -1 to S_{2,1}. So S_{2,1} = 0 - 1 ≡ 2? But expected 1. Hmm. Also e=(1,1) loop, u=1: t=1: f=(x,1) fixed: none. t=p: f=(1,y) fixed: (1,2)=1 → S_{1,2} -= 1. e=(2,1) non-loop, p=3 middle: S_{2,1} -= A_{1,2} = 1 → S_{2,1} = -1 ≡ 2. Expected S_{2,1} = 1. ✗ still.

Hmm. Let me recompute expected: total sum [[48,44],[67,65]] mod 3 = [[0, 2],[1, 2]]. 67 mod 3 = 1. So S_{2,1} = 1.

Let me enumerate walks 2→1 length 3 over all B and sum. B = [[a,1],[b,2]], a,b ∈ {1,2}. (B^3)_{2,1}: walks 2→x→y→1: B_{2,x} B_{x,y} B_{y,1}. Possibilities: x∈{1,2}, y∈{1,2}: terms: B_{2,1}B_{1,1}B_{1,1} = b·a·a; B_{2,1}B_{1,2}B_{2,1} = b·1·b; B_{2,2}B_{2,1}B_{1,1} = 2·b·a; B_{2,2}B_{2,2}B_{2,1} = 2·2·b. Sum over a,b ∈{1,2}: Σ b a^2 = (Σa^2)(Σb) = 5·3=15; Σ b^2 = 3·5=15... wait Σ_{a,b} b^2 = (Σ_a 1)(Σ_b b^2) = 2·5 = 10; Σ 2ab = 2·3·3=18; Σ 4b = 4·2·3=24. Total = 15+10+18+24 = 67. ✓.

Now my formula: walk b·a·a uses zero edges (2,1) once and (1,1) twice: multiplicities: (1,1):2 = p-1 ✓, (2,1):1 ✗ → killed. Walk b·1·b: edge (2,1) twice, (1,2) once: (2,1) mult 2 ✓ survives, contribution T(2)·1 = -1 per (a,b)... summed over a: a doesn't appear, so factor (p-1)=2 choices for a? Wait — the sum over B includes sum over a even when a doesn't appear in the walk. Each walk's sum over all replacements = Π over zero edges of T(c_e), but zero edges not used have c=0, T(0)=p-1≡-1. I forgot the T(0) factors! Every zero edge e not used in the walk contributes T(0) = p-1 ≡ -1. So each surviving walk contributes (-1)^{K} · Π fixed A^{c} where K = total number of zeros? No: (-1)^{#zero edges with c_e ≥ 1} · (p-1)^{#zero edges with c_e = 0} ≡ (-1)^{#used} · (-1)^{#unused} = (-1)^K. So every surviving walk contributes (-1)^K Π_{fixed} A_e^{c_e}. Constant sign! Great simplification.

Check sample 1: K=2, sign (+1). Surviving walks 2→1: b·1·b (edge (2,1) twice, (1,2) once): contribution A_{1,2}=1. Any others? b·a·a killed ((2,1) once). 2·b·a: edges (2,2),(2,1),(1,1) each once — killed. 4b: (2,2) twice? walk 2→2→2→1: edges (2,2),(2,2),(2,1): (2,1) once killed. So only one surviving walk, contribution +1 → S_{2,1}=1 ✓.

Recheck S_{1,2}: expected 2. Walks 1→x→y→2: terms: a·a·1 (edges (1,1)²,(1,2)): (1,1) mult 2 ✓ → contributes A_{1,2}=1, sign +. a·1·b? walk 1→1→2→2: edges (1,1),(1,2),(2,2) each once — killed. 1·b·a: walk 1→2→1→1: edges (1,2),(2,1),(1,1) once each — killed. 1·2·1? walk 1→2→2→2: edges (1,2),(2,2)²: (2,2) mult 2 ✓ → contributes A_{1,2}·A_{2,2}² = 1·4 = 4 ≡ 1. So S_{1,2} = 1 + 4 = 5 ≡ 2 ✓. 

So corrected framework: S_{i,j} = (-1)^K · Σ over walks i→j of length p where every zero edge used has multiplicity ≡ 0 mod (p-1), of Π_{fixed edges} A_e^{c_e} (mod p).

Now redo the structural analysis with the global sign (-1)^K pulled out. Surviving walks (odd p): zero edges used with multiplicity in {p-1} (can't be p since p ≢ 0 mod p-1; can't be ≥ 2(p-1) > p for p > 2... 2(p-1) = 2p-2 > p iff p>2 ✓). At most one zero edge used (two would need ≥ 2(p-1) > p steps... unless p=3: 2(p-1)=4 > 3 ✓). So: either (a) no zero edges — all-fixed walks, contributes (A^p)_{i,j}; or (b) exactly one zero edge e used exactly p-1 times, plus exactly one fixed-edge step f.

Arrangements for (b): f at position t ∈ {1,...,p}, e elsewhere.
- t=1: f=(i, y), then p-1 consecutive e's from y: need y = u, and consecutive e's: p-1 ≥ 2 (p≥3) → need u = v. So e loop at u, f=(i,u), j=u. Contribution: A_{i,u} for fixed (i,u), added to (i, u).
- t=p: p-1 consecutive e's from i: need i = u, u=v (loop), then f=(u, j). Contribution A_{u,j} to (u, j).
- 2 ≤ t ≤ p-1: steps 1..t-1 consecutive e's from i. If t ≥ 3: need u=v and i=u. Steps t+1..p consecutive e's: if t ≤ p-2: need u=v and start w=u. So for p ≥ 5 with 3 ≤ t ≤ p-2: e loop at u, i=u, f=(u,u) — but f fixed loop at u contradicts A_{u,u}=0. For boundary middle t=2: steps 3..p: p-2 consecutive e's after f. p=3: t=2 is the only middle; walk e,f,e: i=u, f=(v, u), j=v: contribution A_{v,u} to (u,v) — e may be non-loop! For p ≥ 5, t=2: steps 3..p = p-2 ≥ 3 consecutive e's need u=v and f=(v,u); then also steps 1..1: single e, i=u fine. So e loop, f=(u,u) contradiction again. Similarly t=p-1 symmetric. So non-loop contributions exist ONLY for p=3, t=2: walk u→v→u→v with e=(u,v) zero, f=(v,u) fixed, contributing A_{v,u} to S_{u,v}.

Wait, also for p=3, are t=1 and t=3 subsumed? t=1: f then 2 e's: need u=v... for p=3, p-1=2 consecutive e's need u=v. Yes loop required, as stated. But hold on, for p=3 t=1: f=(i,y), steps 2,3 = e,e: y=u, u→v→? step3 needs v=u. Loop. ✓. And the middle case t=2 with e a loop gives f=(u,u) contradiction, fine.

So final formula for odd p:
S = (-1)^K · [ A^p + C1 + C2 (+ C3 if p=3) ] mod p, where:
- C1: for each zero loop u (A_{u,u}=0), for each fixed entry A_{i,u} (i any, A_{i,u}≠0): add A_{i,u} to position (i, u). Note i=u excluded since A_{u,u}=0.
- C2: for each zero loop u, for each fixed A_{u,j}: add A_{u,j} to (u, j).
- C3 (p=3 only): for each zero edge (u,v) with u≠v... actually also u=v? If e loop and p=3, t=2 gives f=(u,u) contradiction, so only u≠v: for each zero (u,v), fixed (v,u): add A_{v,u} to (u,v).

Hmm wait, but for p=3, does C3 also apply when e is a loop? Covered — no. Also, should C3 include the case where (v,u) is... f must be fixed: A_{v,u} ≠ 0. Yes.

But wait, one more check for p=3: in case (b), could the zero edge be used p-1=2 times and f also... we need f fixed. What if f is also a zero edge? Then two distinct zero edges each with multiplicity... e twice, f once: f multiplicity 1 not divisible by 2 → killed. Unless f = e. Covered. ✓.

Also for odd p, what about walks using one zero edge with multiplicity p-1 where the walk has length p but... we need EXACTLY p steps; p-1 + 1 = p ✓ only one extra step. ✓.

Now verify sample 1 fully: K=2, sign +1. A^3 ≡ [[0,1],[0,2]] (computed). C1: zero loops u=1: fixed column-1 entries: none. u=2: fixed entries in column 2: A_{1,2}=1 → add 1 to (1,2). C2: u=1: fixed row-1: A_{1,2}=1 → add to (1,2). u=2: fixed row-2: none. C3 (p=3): zero non-loop edges: (2,1): check A_{1,2}=1 fixed → add 1 to (2,1). Zero (1,2)? A_{1,2}=1 not zero. So C3: (2,1) += 1.
S = [[0, 1+1+1],[0+1, 2]] = [[0,3],[1,2]] ≡ [[0,0],[1,2]]? Expected [[0,2],[1,2]]. S_{1,2}: A^3 gives 1, C1 gives 1, C2 gives 1 → 3 ≡ 0, but expected 2! ✗.

Hmm. Let me recompute A^3 mod 3. A=[[0,1],[0,2]]. A^2: row1: [0·0+1·0, 0·1+1·2] = [0,2]; row2: [0·0+2·0, 0·1+2·2]=[0,4]. A^3 = A^2·A: row1: [0·0+2·0, 0·1+2·2]=[0,4]; row2: [0·0+4·0, 0·1+4·2]=[0,8]. mod 3: [[0,1],[0,2]]. (1,2) entry = 1.

Direct enumeration for S_{1,2}: expected 44 mod 3 = 2. Walks 1→x→y→2 summed over a,b ∈ {1,2}: terms: a·a·1? walk 1→1→1→2: B11·B11·B12 = a²·1. walk 1→1→2→2: a·1·2 = 2a. walk 1→2→1→2: 1·b·1 = b. walk 1→2→2→2: 1·2·2 = 4. Σ over a,b∈{1,2}: Σa² = 2·5=10 (sum over a of a² times 2 choices of b) = 10; Σ2a = 2·3·2=12; Σb = 2·3=6... wait Σ_{a,b} b = 2·3 = 6; Σ4 = 4·4=16. Total = 10+12+6+16 = 44 ✓.

Surviving walks with sign (-1)^K = +1: walk a²·1: edges (1,1)×2, (1,2)×1: zero edge (1,1) mult 2 ✓ → contribution A_{1,2} = 1. walk 2a: edges (1,1),(1,2),(2,2) each once → killed. walk b: edges (1,2),(2,1),(1,2): (2,1) mult 1 killed. walk 4: edges (1,2),(2,2)×2: zero edge? (2,2) is FIXED (A_{2,2}=2). (1,2) fixed. No zero edges! Survives in term (a): contribution 1·2² = 4. So S_{1,2} = 1 + 4 = 5 ≡ 2 ✓.

So where does my decomposition go wrong? Term (a) = all-fixed walks = A^p includes walk 1→2→2→2 giving 4 ≡ 1 ✓ (A^3[1,2] = 4 ≡ 1). Walk a²·1: zero loop (1,1) twice + fixed (1,2) once, f at position t=3=p: C2 case: u=1, f=(1,2): add A_{1,2}=1 to (1,2) ✓. So C2 gives 1. But I ALSO added C1 (u=2, column 2 fixed A_{1,2}: add to (1,2)) and C3? No C3 to (1,2). C1 u=2: zero loop at 2? A_{2,2}=2 ≠ 0! Not a zero loop! I made an error: zero loops are u=1 only (A_{1,1}=0; A_{2,2}=2 fixed). Redo: C1: u=1: fixed entries in column 1: A_{x,1}≠0: none. C2: u=1: fixed row 1: A_{1,2}=1 → (1,2) += 1. C3: zero non-loop edges: (2,1): A_{1,2}=1 fixed → (2,1) += 1. Total: S = [[0, 1+1],[1, 2]] = [[0,2],[1,2]] ✓✓. 

Now the formula works for sample 1. Let me also sanity check sample 2 (p=2): handled separately, B = A with zeros→1, S=B^2 mod 2. ✓ (matches).

Now, is the formula complete for general odd p? Let me re-derive carefully. Surviving walks: zero edges used with multiplicity divisible by p-1; total length p; multiplicities ≤ p. Options per zero edge: 0 or p-1 (p itself not divisible by p-1; 2(p-1) > p for p>2). At most one zero edge with p-1 (two would exceed p). Remaining steps: p - (p-1) = 1 fixed step, or 0 zero edges used → all p steps fixed.

Case (a): all-fixed walks: (A^p)_{i,j}. ✓ (zero entries of A contribute 0 to walks anyway).

Case (b): one zero edge e=(u,v) used p-1 times, one fixed edge f used once. Walk structure: sequence of p steps; p-1 are e, 1 is f. Since e's are identical, the walk is determined by position t of f and validity constraints:
- All e-steps before f (t-1 of them) form a walk from i using only edge e: i → u requires... step1=e: v0=i=u. Then each subsequent e requires returning to u: v=u. So: if t-1 = 0: no constraint from prefix (i free, f starts at i). If t-1 = 1: i = u. If t-1 ≥ 2: i = u and u = v.
- Similarly suffix after f: p-t e-steps: if 0: j = endpoint of f. If 1: f ends at u, j = v. If ≥ 2: f ends at u, u = v, j = v = u.

Subcases (p ≥ 5):
- t=1: suffix p-1 ≥ 2: u=v, f=(i, u), j=u. Contribution: for zero loop u, fixed (i,u): S_{i,u} += A_{i,u}.
- t=p: prefix ≥ 2: i=u, u=v, f=(u, j): S_{u,j} += A_{u,j}.
- t=2: prefix 1: i=u. suffix p-2 ≥ 3 ≥ 2: f ends at u, u=v, j=u: f=(v,u)=(u,u) fixed loop — contradiction (A_{u,u}=0). None.
- t=p-1: symmetric: f=(u,u) contradiction. None.
- 3 ≤ t ≤ p-2 (exist for p ≥ 7... p=5: t=3: prefix 2, suffix 2): need u=v, i=u, f=(u,u): contradiction. None.

p=3: t=2: prefix 1 (i=u), suffix 1 (f ends at u, j=v): f=(v,u) fixed. e=(u,v) zero, any u,v (if u=v, f=(u,u) contradiction, so u≠v effectively). Contribution: S_{u,v} += A_{v,u}.

Great, formula confirmed:
For odd p:
M = A^p mod p.
For each u with A_{u,u} = 0:
  for each i with A_{i,u} ≠ 0: M_{i,u} += A_{i,u}
  for each j with A_{u,j} ≠ 0: M_{u,j} += A_{u,j}
If p = 3:
  for each (u,v) with A_{u,v} = 0 and A_{v,u} ≠ 0 (u≠v implied... if u=v then A_{v,u}=A_{u,v}=0, so condition A_{v,u}≠0 auto-excludes loops): M_{u,v} += A_{v,u}
S = (-1)^K · M mod p.

Wait, double check C1/C2 for double counting when both apply — they're different positions generally, fine. Also note in C1, i can equal u? A_{u,u}=0 so A_{i,u}≠0 excludes i=u. Good.

Hmm, wait: also should we consider p=3 C3 overlap with C1/C2? C3 adds to (u,v) where A_{u,v}=0; C1 adds to (i,u) at positions where A_{i,u}≠0 — different positions (C1 targets fixed entries, C3 targets zero entries). C2 targets fixed entries in row u. No overlap. ✓.

Now verify sample 3 (p=13, N=4) mentally? That's heavy; trust the derivation but workers should verify by brute force in code during development (we can't run, but the next worker writes code; include a brute-force self-check on small random cases in testing — though final submission shouldn't test samples, we can reason).

Let me partially check sample 3: p=13, K = number of zeros in A:
Row1: 0 1 2 0 → zeros at (1,1),(1,4)
Row2: 3 4 0 5 → zero (2,3)
Row3: 0 6 0 7 → zeros (3,1),(3,3)
Row4: 8 9 0 0 → zeros (4,3),(4,4)
K=7, sign (-1)^7 = -1.
Zero loops: u=1 (A11=0), u=3 (A33=0), u=4 (A44=0). u=2: A22=4 fixed.
C1 (column u fixed entries, add to (i,u)):
 u=1: column 1: A21=3, A41=8 (A11=0, A31=0): M[2,1]+=3, M[4,1]+=8.
 u=3: column 3: all zero (A13=2? wait A_{1,3}=2! Row1: 0 1 2 0, so A13=2. Column 3 entries: A13=2, A23=0, A33=0, A43=0. So M[1,3] += 2.
 u=4: column 4: A14=0, A24=5, A34=7, A44=0: M[2,4]+=5, M[3,4]+=7.
C2 (row u fixed entries, add to (u,j)):
 u=1: row1: A12=1, A13=2: M[1,2]+=1, M[1,3]+=2.
 u=3: row3: A32=6, A34=7: M[3,2]+=6, M[3,4]+=7.
 u=4: row4: A41=8, A42=9: M[4,1]+=8, M[4,2]+=9.
p=13 ≠ 3, no C3.
S = -(A^13 + corrections) mod 13.

Expected output:
8 0 6 5
11 1 8 5
8 0 4 12
8 0 1 9

So M = -S mod 13:
M[1] = [5, 0, 7, 8]; M[2] = [2, 12, 5, 8]; M[3] = [5, 0, 9, 1]; M[4] = [5, 0, 12, 4].
Check corrections: M[2,1] should = A^13[2,1] + 3; M[4,1] = A^13[4,1] + 8 + 8 = A^13[4,1]+16 ≡ +3; M[1,3] = A^13[1,3] + 2 + 2 = +4; M[2,4] = A^13[2,4] + 5; M[3,4] = A^13[3,4] + 7 + 7 = +14 ≡ +1; M[1,2] = A^13[1,2]+1; M[3,2] = A^13[3,2]+6; M[4,2] = A^13[4,2]+9.

We can't easily compute A^13 by hand, but the structure is plausible. The next worker should verify with a brute-force implementation over small cases (e.g., random N≤4, p∈{3,5,7}, enumerate all (p-1)^K with K small) against the formula. Since we can't run code here, the plan: implement formula + matrix fast power, and mentally trust derivation; also include derivation cross-check via the alternative "polynomial/trace" method? Not needed.

Complexity: O(N^3 log p) for A^p with mod p (p up to 1e9, products up to ~1e18 — Python handles big ints natively, fine). N=100, log p ≤ 30 → ~3e7 ops worst case in Python... might be slow (~30-60s?). Optimization: since we only need A^p mod p, note by Fermat/matrix Frobenius? There's no cheap "A^p mod p" shortcut for general matrices (unlike scalars). Hmm — actually in characteristic p, (A+B)^p ≠ A^p + B^p in general (noncommutative), but for a single matrix, A^p is just power. Use fast exponentiation: ~2·log2(p) ≈ 60 matrix multiplications of 100×100 → 6e7 modular multiplications. In Python with pure loops that's too slow (~60s+). Need speed: use numpy with object dtype? No — use numpy with int64? Products up to (p-1)^2 · N ≈ 1e18 · 100 = 1e20 overflows int64. Options: mod p ≤ 1e9, use float64-based matmul trick (like for convolution)? Risky. Alternative: numpy with dtype=object is slow. Better: reduce mod p each step; values < p ≤ 1e9; products < 1e18 < 2^63 ≈ 9.2e18. Sum of 100 products < 1e20 overflows. But we can accumulate with periodic mod: numpy dot with int64 overflows silently. Trick: split matrices or use the "mod after each 2^? additions" — can't control numpy's accumulation.

Alternative: use the fact that we can do matmul mod p via numpy float64 when p^2·N < 2^53: p^2·N ≈ 1e18·100 = 1e20 > 9e15. No.

Standard trick: decompose A = A (values < p ≤ 1e9 < 2^30). Use int64 dot but mod inside: do dot in chunks? Or use Python's built-in pow for matrix? Not available.

Better idea: we don't need full A^p via generic exponentiation — we can use binary exponentiation but implement matmul with numpy using the "split into low/high 15-bit parts" trick: A = A0 + 2^15 A1 + 2^30 A2 (values < 2^30 need 2 parts of 15 bits: A = A_lo + 2^15 A_hi, A_lo, A_hi < 2^15). Then A·B = A_lo·B_lo + 2^15(A_lo·B_hi + A_hi·B_lo) + 2^30 A_hi·B_hi. Each product matrix entries: sums of 100 terms each < 2^15·2^15 = 2^30, total < 100·2^30 ≈ 1.6e11 < 2^53 — safe in float64? float64 exact for integers < 2^53 ≈ 9e15 ✓. But float64 matmul then convert to int64 — rounding exact since values < 2^53 ✓. Then combine and mod p. That's ~4-6 float matmuls per mod-matmul, each ~1e6 flops → fast (numpy 100×100 matmul ~ microseconds). Total 60 matmuls × ~6 = 360 numpy matmuls — trivial.

Alternatively simpler: use int64 numpy with mod reduction every iteration via `np.dot` on int64 — overflow risk as computed (1e20 > 9.2e18). Could reduce p... no. Use the float trick or pure Python with `pow`-based... Actually simplest robust: pure Python triple loop with mod, 3e7 ops — likely 20-40s, too slow for typical 2s limit. Go with numpy float-split trick, or use int64 with accumulation splitting: dot(A.astype(np.int64), B) where we pre-reduce... no.

Alternative cleaner: since p < 2^30, values < 2^30. Products < 2^60. Sum of 100 < 100·2^60 ≈ 1.15e20 > int64 max 9.2e18. Overflow by factor ~12. If we mod the operand matrices to < p and also... we could do the dot in two halves (50 columns each) with mod between: each half sum < 50·2^60 ≈ 5.76e19 still > 9.2e18. Quarters: 25·2^60 ≈ 2.88e19 > 9.2e18. Hmm 2^60 = 1.15e18; 8 terms = 9.2e18 borderline. So chunk size 4: messy. Use float-split trick — standard and clean.

Actually even simpler: use numpy with `dtype=np.float64` directly is unsafe; the 15-bit split with float64 matmul is safe as shown (max intermediate 100·(2^15)² = 100·2^30 ≈ 1.07e11 ≪ 2^53). Then result = (M00 + (M01+M10)·2^15 + M11·2^30) mod p, computed in int64/Python ints: M values ≤ 1.07e11 fit int64; multiply by 2^30 → ~1e20 overflow int64! So do mod in Python: convert to Python int or do mod via int64 with care: (M00 + ((M01+M10) % p)·2^15 % p ...). Better: compute r = (M00 % p) + ((M01+M10) % p)·(2^15 % p) + (M11 % p)·(2^30 % p), all mod p — use Python ints via `.astype(object)`? Slow-ish but only 1e4 elements × 360 = 3.6e6 ops, fine. Or use int64: values after % p are < 1e9; times 2^15 < 3.3e13; sum of three such < 1e14 < 9.2e18 ✓ int64 safe! Great: keep everything int64 numpy: M00 % p etc. all int64, combine with precomputed 2^15 % p, 2^30 % p. All int64-safe.

Even simpler alternative: represent each matrix mod p as int64, and do matmul via splitting ONE operand: C = A·B mod p. Split A = A0 + 2^15 A1 (A0 = A & 32767, A1 = A >> 15 < 2^15 since A < 2^30). C = A0·B + 2^15·A1·B. But A0·B entries: sum of 100 × (2^15 · 2^30) = 100·2^45 ≈ 3.5e15 < 2^53 ✓ float-safe, and also < int64 max! 3.5e15 ≪ 9.2e18 ✓. So int64 dot works directly if one operand is < 2^15: A0·B and A1·B each ≤ 100·2^15·(p-1) < 100·2^15·2^30 = 100·2^45 ≈ 3.5e15 ✓ int64 SAFE. So: C = (A0 @ B + (A1 @ B) · (2^15 % p)) % p — wait need mod: A0@B ≤ 3.5e15, (A1@B)·2^15 ≤ 3.5e15·32768 ≈ 1.15e20 overflow! So mod first: C = (A0@B % p + (A1@B % p)·(2^15 % p)) % p — (A1@B % p) < 1e9, ×2^15 < 3.3e13, + A0@B%p < 1e9 → sum < 3.4e13 ✓ int64 safe. Two int64 matmuls per multiply. numpy int64 matmul 100×100: fast (~50µs). Total ~120 matmuls → milliseconds. 

So implementation:
def matmul(X, Y, p): X0 = X % 32768; X1 = X // 32768 (X already < p < 2^30, so X1 < 2^15); return (X0@Y % p + (X1@Y % p)·(2^15 % p)) % p. Wait X0@Y: X0 < 2^15, Y < p < 2^30 → entries ≤ 100·2^15·(2^30-1) ≈ 3.5e15 ✓. Good. All numpy int64.

Then matpow via binary exponentiation, ~2·30 = 60 matmuls.

Edge cases:
- p=2: separate handling: B = A with zeros→1 (mod 2 everything is 0/1; A entries are 0 or 1 since ≤ p-1=1). S = B^2 mod 2. Note K can be anything; only one B. Compute with numpy mod 2. Actually also could the general formula work for p=2? p-1=1 divides all multiplicities, so ALL walks survive with sign (-1)^K and T(c)=1... Σ over all walks of Π fixed A^c × 1^{zero stuff} = (B^2) where B has 1s — yes consistent but the structural formula (cases) assumed odd p. Just handle p=2 separately. Note for p=2, N up to 100, B^2 mod 2 easy.
- p=3: add C3.
- K=0: sign +1, no corrections (no zero loops), answer = A^p mod p. ✓ consistent.
- p odd but p-1 > p? impossible. p=3 boundary handled.

Wait, one more subtle check for p=3, C3: e=(u,v) zero, f=(v,u) fixed. What if u=v? Then A_{v,u}=A_{u,u}=0, not fixed — excluded automatically by requiring A_{v,u}≠0. ✓. And C3 walk u→v→u→v: i=u, j=v ✓. Also for p=3, are there walks where zero edge used p-1=2 times and it's a loop, f at t=2? f=(u,u) needed fixed — excluded. ✓.

Also double-check C1 for p=3: t=1: f=(i,y), then 2 e's: y=u, e twice: u→v→? need v=u. So loop, f=(i,u), j=u ✓ same as general. C2 t=3: ✓.

Another subtlety: in case (b), could the single fixed step f be on an edge that is ALSO... f fixed means A_{f} ≠ 0. e zero means A_e = 0. Distinct edges. ✓. And what if the walk uses zero edge e with multiplicity p-1 but ALSO the fixed step is on the same edge? Impossible since A_e=0 vs fixed. ✓.

Also: walks where a zero edge is used with multiplicity 0 — fine. Walks using fixed edges with any multiplicity — fine, contribute A_e^{c_e} mod p (note A_e^{c} mod p with c up to p — just compute as pow or as part of A^p; in corrections C1/C2/C3 the fixed edge appears exactly once, contributing A_e^1). ✓.

Sign: (-1)^K overall. Let me double-check the sign derivation: for a surviving walk, sum over replacements = Π_{zero edges e} T(c_e) where T(0)=p-1≡-1 (for unused zero edges) and T(p-1)≡-1 (used). So each of the K zero edges contributes -1 regardless! Sign = (-1)^K ✓. Fixed edges contribute A_e^{c_e} exactly (sum over nothing). ✓.

But wait — T(c) for c≥1: Σ_{x=1}^{p-1} x^c ≡ -1 if (p-1)|c else 0 (mod p). For c = p-1: -1 ✓.

Also confirm there's no surviving walk type we missed for odd p where zero edge multiplicity = p-1 and total length p but the walk uses the zero edge p-1 times and one fixed edge — yes that's case (b) fully. And multiplicity must be exactly 0 mod (p-1): possible values 0, p-1 (since 2(p-1) ≥ p+1 for p ≥ 3: 2p-2 ≥ p+1 ⟺ p ≥ 3 ✓; and p ≢ 0 mod (p-1)). ✓.

Now also verify C1/C2 don't need multiplicity factors: the zero loop appears p-1 times, T(p-1) = -1, absorbed in global sign. Fixed edge once: factor A. Number of walks for given (u, i, f=(i,u)): exactly 1 (position t=1 forced). ✓. So C1: M[i,u] += A[i,u] for each zero loop u and fixed A[i,u]. ✓.

Let me also re-examine: in C1, is it required that i ≠ u? If i = u: A[u,u] = 0, not fixed, excluded. ✓. In C2, j ≠ u similarly. ✓.

Now sample 3 partial verification: let's compute A^13 mod 13... too heavy by hand. Alternative: verify one entry via expected output. M = -S: M[1,1] = -8 ≡ 5. Corrections don't touch (1,1) (C1 touches column u at rows i with A[i,u]≠0, i≠u; C2 touches row u at j≠u; (1,1) untouched). So A^13[1,1] ≡ 5 mod 13. Can't verify by hand easily. The next worker should brute-force check the formula on tiny random cases (N ≤ 3, p ∈ {3,5}, K ≤ 4) by enumerating all B — as a self-test during development (not in final code). Since we cannot execute, the plan should emphasize careful re-derivation + a brute-force cross-check function included optionally... The instructions say don't test on samples; but self-tests on random tiny cases during development are fine conceptually — however we can't run anything. The final worker must just submit. Risk: formula error. Mitigation: re-derive once more below and cross-check sample 3 entries that are "untouched" by corrections via a different method? Can't compute A^13 by hand realistically.

Let me at least verify the sign and corrections structure against sample 3's zero pattern: positions where corrections apply: (2,1):+3, (4,1):+8+8=16≡3, (1,3):+2+2=4, (2,4):+5, (3,4):+7+7=14≡1, (1,2):+1, (3,2):+6, (4,2):+9. p=13 no C3. M = A^13 + corr, S = -M.

Expected S row1: 8 0 6 5 → M row1: 5 0 7 8. So A^13[1,1]=5, A^13[1,2]=M[1,2]-1= -1 ≡ 12, A^13[1,3]=7-4=3, A^13[1,4]=8.
Row2: S: 11 1 8 5 → M: 2 12 5 8 → A^13[2,1]=2-3=-1≡12, [2,2]=12, [2,3]=5, [2,4]=8-5=3.
Row3: S: 8 0 4 12 → M: 5 0 9 1 → A^13[3,1]=5, [3,2]=0-6=7, [3,3]=9, [3,4]=1-1=0.
Row4: S: 8 0 1 9 → M: 5 0 12 4 → A^13[4,1]=5-3=2, [4,2]=0-9=4, [4,3]=12, [4,4]=4.

Plausibility check: A^13 mod 13 — note for any matrix over F_p, the Frobenius map doesn't simplify A^p entrywise, but there's a known fact: A^p ≡ ... no general simple form. However, we can sanity check via trace: tr(A^p) ≡ tr(A)^p ≡ tr(A) (mod p)? In char p, tr(A^p) ≡ (tr A)^p? For a matrix over F_p, eigenvalues in algebraic closure: tr(A^p) = Σ λ_i^p = (Σ λ_i)^p = tr(A)^p ≡ tr(A). tr(A) = 0+4+0+0 = 4. Our A^13 diagonal: 5+12+9+4 = 30 ≡ 4 mod 13 ✓!! Great consistency check passed.

Another check: det(A^p) = det(A)^p ≡ det(A) mod p. Hard by hand. The trace check is reassuring.

Also check sample 3 S has zeros at (1,2),(3,2),(4,2): S[i,2] = -(A^13[i,2] + corr). Column 2 of A: 1,4,6,9 — all nonzero. Interesting but no contradiction.

Now, p=2 case: also note p=2 with the general approach: B = A with 0→1; answer B^2 mod 2. But wait — is it (B^p) summed over all B, and there's exactly one B since (p-1)^K = 1. ✓.

Implementation plan:
1. Read N, p, matrix A.
2. If p == 2: B = (A == 0 ? 1 : A) mod 2; compute B^2 mod 2 (numpy int64 fine: entries ≤ 100); print.
3. Else:
   - K = count zeros.
   - Compute M = A^p mod p via binary exponentiation with numpy int64 split matmul (values < p ≤ 1e9 < 2^30; split at 2^15).
   - Corrections: for each u with A[u,u] % p == 0 (A entries already in [0,p-1]): col = A[:,u]; for i where col[i] != 0: M[i,u] += col[i]; row = A[u]; for j where row[j] != 0: M[u,j] += row[j]. Mod p after.
   - If p == 3: for each (u,v) with A[u,v]==0 and A[v,u]!=0: M[u,v] += A[v,u]. (u≠v automatic.)
   - If K odd: M = -M mod p.
   - Print M.

Complexity: O(N^3 log p) with numpy — fast.

Wait, p up to 1e9 but constraints say prime p with 1 ≤ p ≤ 1e9 — p=1 isn't prime; smallest prime 2. Fine. Also note p could be as small as 2 or 3 — handled. p=3, N=1: A=[0]: K=1, M = A^3 = 0; zero loop u=0: col/row fixed entries none; C3: A[0,0]=0, A[0,0]≠0 false; sign -: M=0. Brute: B=[x], x∈{1,2}, B^3 = x^3 ≡ x (mod 3): sum = 1+2 = 3 ≡ 0 ✓.

N=1, p=3, A=[a≠0]: K=0, M = a^3 ≡ a. Brute: single B=A, B^3 = a^3 ≡ a ✓.

N=1, p=5, A=[0]: K=1, M = 0^5 = 0; corrections none; sign - → 0. Brute: Σ_{x=1}^4 x^5 ≡ Σ x = 10 ≡ 0 mod 5 ✓ (x^5 ≡ x).

N=2, p=5, A = [[0,1],[1,0]]: K=2, sign +. A^5: A^2 = I, A^5 = A. So M = A = [[0,1],[1,0]]. Zero loops: u=1: col1 fixed: A[2,1]=1 → M[2,1] += 1 → 2; row1 fixed: A[1,2]=1 → M[1,2] += 1 → 2. u=2: col2: A[1,2]=1 → M[1,2] += 1 → 3; row2: A[2,1]=1 → M[2,1] += 1 → 3. M = [[0,3],[3,0]]. Brute check: B = [[a,1],[1,b]], a,b ∈ 1..4. Compute (B^5)_{1,2} summed over a,b. Walks 1→...→2 length 5. Surviving: all-fixed (no zero edges): walks using edges (1,2),(2,1) only: 1→2→1→2→1→2: product 1 → contributes 1 (A^5[1,2]=1 ✓). Zero loop (1,1) ×4 + 1 fixed step: t=1: f=(1,1)? f must end at u=1: f=(i,1) fixed: (2,1): walk 2→1 then loops at 1 — but i=1 for S_{1,2}: t=1 requires i=x where f=(x,u): f=(2,1) means i=2. Not for (1,2). t=p: i=u=1, f=(1,j): f=(1,2), j=2 ✓: walk 1→1→1→1→1→2: contributes A[1,2]=1. Zero loop (2,2)×4: t=1: f=(x,2), i=x: f=(1,2): i=1 ✓, then loops at 2, j=2 ✓: contributes 1. t=p: i=2 ✗. So S_{1,2} = 1+1+1 = 3 ✓ matches M[1,2]=3. 

The formula seems solid. Now think about implementation details for speed and correctness:
- numpy int64 matmul safety: X, Y < p ≤ 1e9. X0 = X & 32767 (< 2^15), X1 = X >> 15 (< 2^15 since X < 2^30). X0@Y: ≤ N·(2^15-1)·(p-1) ≤ 100·32767·1e9 ≈ 3.28e15 < 9.2e18 ✓. Then C = (X0@Y % p + ((X1@Y % p) · (32768 % p))) % p: (X1@Y % p) < p ≤ 1e9, ×32768 ≤ 3.3e13, + < 1e9 → < 3.4e13 ✓.
- Binary exponentiation: result = I; base = A % p; e = p; while e: if e&1: R = mul(R, base); base = mul(base, base); e >>= 1. ~60 muls.
- Memory/time trivial.

Potential pitfall: reading input fast (N=100, trivial). Output formatting: N lines, space-separated.

One more consideration: p=2 case could also just fall through general code? The structural derivation assumed odd p. For p=2, p-1=1, every walk survives, sign (-1)^K, T(c)=1 for all c (Σ_{x=1}^{1} x^c = 1). Sum over all walks i→j length 2 of Π fixed A^c · 1 = (B^2)_{i,j} where B = A with zeros→1. And sign? T(c) = 1 = (-1)? mod 2, -1 ≡ 1, so sign irrelevant. So p=2: answer = B^2 mod 2 with B = A + (A==0). Just implement separately.

Also p=3 C3 condition: "A[u,v]==0 and A[v,u]!=0" — includes u==v? A[v,u]=A[u,v]=0 fails second condition. ✓ excluded.

Also think: do C1/C2 corrections need to use original A (yes, fixed = nonzero in A). ✓.

Double-check the claim T(0) = p-1: zero edge unused means its replacement variable x doesn't appear in the walk product; summing over x ∈ 1..p-1 gives factor (p-1) ≡ -1. ✓. This is where the global sign comes from — every zero edge contributes -1 whether used (mult p-1) or not. Clean.

Now also confirm no missing factor for the used zero edge: T(p-1) = Σ x^{p-1} = Σ 1 = p-1 ≡ -1 ✓ (x^{p-1} ≡ 1 by Fermat).

Everything checks. Remaining risk: subtle mistake in case analysis for larger p (e.g., p=5, t=2 with suffix p-2=3 consecutive e's — needs u=v and f ends at u; prefix t-1=1: i=u; f=(v,u)=(u,u) contradiction ✓ none). p=5, t=4 (t=p-1): symmetric none. t=3: prefix 2 needs u=v, i=u; suffix 2: f ends u, j=u; f=(u,u) contradiction ✓. So only t=1, t=p for p ≥ 5. ✓.

Also p=3: t=1: suffix 2 consecutive e's needs u=v ✓ loop; t=3: prefix 2 needs loop ✓; t=2: efe, no loop requirement ✓. Good.

Alternative approach (for robustness cross-check): none needed; trace check on sample 3 passed.

Plan for next worker: implement as above; include careful numpy mod-matmul; handle p=2; p=3 extra term; global sign (-1)^K. Also mention fallback pure-Python if numpy unavailable? AtCoder (this looks like AtCoder) allows numpy. Provide code with numpy; optionally pure python matmul fallback might TLE. Use numpy.

Also note: A^p where p is huge exponent — binary lifting with exponent p (the integer). ✓.

Edge: p=2 and K anything: B entries: A_{ij} ∈ {0,1}; zeros→1. B^2 mod 2: entries ≤ 100, numpy fine.

Let me also double check sample 2 with p=2 handling: A = identity 3×3, zeros→1 gives all-ones J. J^2 = 3J ≡ J mod 2 → output all 1s ✓.

Final answer structure: S = (-1)^K (A^p + C1 + C2 + [p=3] C3) mod p for odd p; B^2 for p=2.

Write-up for NEXT: implement formula, numpy int64 split matmul, handle cases, verify trace invariant tr(A^p) ≡ tr(A) as internal assert (optional, remove for speed — it's cheap: just diagonal sums; could keep as sanity but not necessary).

## worker: Implement the full Python solution based on the co
Implemented the derived closed form. Summary of the math (verified against all three samples structurally, plus a trace invariant check on sample 3):

- Expanding $(B^p)_{i,j}$ into walks and summing each zero entry over $x \in \{1,\dots,p-1\}$ gives per-zero-edge factors $T(c) = \sum_x x^c$, with $T(0) = p-1 \equiv -1$ and $T(c) \equiv -1$ iff $(p-1) \mid c$, else $0$ (for $c \ge 1$). Hence every zero edge contributes a factor $-1$ regardless of use, giving the global sign $(-1)^K$, and a walk survives iff every zero edge it uses has multiplicity divisible by $p-1$.
- For odd $p$, multiplicities sum to $p$, so a surviving walk uses either no zero edges (giving $A^p \bmod p$) or exactly one zero edge exactly $p-1$ times plus one fixed edge once. Positional analysis of the single fixed step shows only placements $t=1$ and $t=p$ survive for $p \ge 5$ (requiring the zero edge to be a loop), yielding C1/C2; for $p=3$ the middle placement $t=2$ additionally allows a non-loop zero edge $(u,v)$ with fixed reverse edge $(v,u)$, yielding C3.
- $p=2$: $p-1=1$ divides everything, there is exactly one $B$ (zeros $\to 1$), answer is $B^2 \bmod 2$.

Implementation details:
- $A^p \bmod p$ via binary exponentiation with numpy int64 matmul. Since entries $< p \le 10^9 < 2^{30}$, the left operand is split as $X = X_0 + 2^{15}X_1$ with $X_0, X_1 < 2^{15}$; each partial dot product is $\le 100 \cdot 2^{15} \cdot (p-1) < 3.5 \times 10^{15} \ll 2^{63}$, so int64 is overflow-safe. Combination is done mod $p$ before multiplying by $2^{15} \bmod p$, keeping all values $< 3.4 \times 10^{13}$.
- Corrections C1/C2/C3 applied from the original matrix, then mod $p$, then the sign $(-1)^K$.
- Sanity checks performed during derivation: sample 1 fully by hand ($S_{2,1}=1$ requires the global $(-1)^K$ sign and the $p=3$ C3 term), sample 2 via the $p=2$ path, sample 3 via $\operatorname{tr}(A^{13}) \equiv \operatorname{tr}(A) \equiv 4 \pmod{13}$ which matched the implied $A^{13}$ diagonal from the expected output.

Complexity: $O(N^3 \log p)$ with small constants (numpy), trivially fast for $N \le 100$, $p \le 10^9$.

## worker: Review the implementation for edge cases (N=1, K=0
Review of the requested edge cases:

- **N=1**: Works. `matpow` handles 1×1 matrices; corrections loops run over single entries. Manually verified: `p=3, A=[0]` → 0 (Σ_{x=1}^{2} x³ ≡ 1+2 ≡ 0); `p=3, A=[a≠0]` → a³ ≡ a; `p=5, A=[0]` → Σ x⁵ ≡ Σ x = 10 ≡ 0. All match the formula.
- **K=0** (no zeros): Corrections C1/C2 require zero diagonal entries and C3 requires zero entries, so none apply; sign is +1; answer is A^p mod p, which is correct since the sum is over a single B = A.
- **p=2**: Handled by the separate path. p−1 = 1 divides every multiplicity, so all walks survive with T(c) = 1; there is exactly one B (zeros→1), answer B² mod 2. Matches sample 2 (all-ones squared = 3·J ≡ J). Entries of B@B ≤ 100, no overflow.
- **p=3**: C3 term included. Verified by hand on sample 1: the (2,1) entry gets +A[1,2] = 1 from zero edge (2,1) with fixed reverse (1,2), and the (1,2) entry gets A³ (=1) + C2 from zero loop u=1 (=1), giving [[0,2],[1,2]] ✓. The u=v case in C3 is auto-excluded because A[v,u]≠0 contradicts A[u,v]=0.
- **p near 1e9**: p < 2³⁰, so after splitting X = X0 + 2¹⁵X1 with X0, X1 < 2¹⁵, partial dots satisfy entries ≤ 100·(2¹⁵−1)·(p−1) < 3.3e15 ≪ 2⁶³−1 ≈ 9.2e18 — int64-safe. The combination step keeps values < p + p·2¹⁵ < 3.3e13 — safe. Exponentiation does ≤ 2·⌈log₂ p⌉ ≈ 60 matmuls, each ~2 numpy int64 dots of 100×100 — runs in milliseconds.
- **Overflow in corrections**: M entries < p ≤ 1e9; each correction adds at most (p−1) per entry at most twice before the `%` (C1 and C2 can both hit the same entry? C1 hits (i,u) with i≠u, C2 hits (u,j) with j≠u — disjoint positions; C3 hits zero entries while C1/C2 hit nonzero entries — disjoint). Values stay < 3p < 2⁶³. Safe.
- **Sign**: K counted from Amod == 0; since input guarantees 0 ≤ A_ij ≤ p−1, Amod == A, but the `% p` makes it robust anyway.
- **Output format**: N lines, space-separated values in [0, p−1], trailing newline. Matches the required format. Values are cast to Python int for printing (avoids numpy formatting quirks).
- **Trace cross-check on sample 3**: From the expected output and corrections, the implied A¹³ diagonal is (5, 12, 9, 4), summing to 30 ≡ 4 ≡ tr(A) mod 13, consistent with tr(A^p) ≡ tr(A)^p ≡ tr(A) in characteristic p. Strong evidence the formula and implementation are correct.

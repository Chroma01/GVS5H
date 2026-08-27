
## ideation
The core difficulty is reducing the 2D Manhattan geometry to something searchable, then doing a max-min selection (classic "aggressive cows" on a ring).

Key claim to verify: for two points on the boundary of a square, Manhattan distance = shorter arc length along the perimeter. Check: points on the same edge — Manhattan distance equals edge distance, matches arc. Points on adjacent edges, e.g. (a,0) and (side,b): Manhattan = (side-a)+b; boundary path via corner (side,0) = (side-a)+b; the other way around the perimeter is longer (perimeter is 4·side, other path = 4·side − that ≥ it since each is at most 2·side... need care: adjacent-edge path via shared corner is ≤ side+side = 2·side = half perimeter, so it IS the shorter arc, and it equals Manhattan). Points on opposite edges, e.g. (a,0) and (b,side): Manhattan = |a−b|+side. Shorter arc = min over going via left side (a + side + b) or right side ((side−a)+side+(side−b)) = side + min(a+b, 2·side−a−b) = side + (side − |a−b|)... wait: min(a+b, 2side−a−b) = side − |a−b| when... a+b vs 2side−a−b: difference is 2(a+b)−2side. If a+b ≤ side, min = a+b, and |a−b| ≤ a+b ≤ side, so side+arc_min = side+a+b ≥ |a−b|+side = Manhattan. Hmm, that gives arc ≥ Manhattan, not equal! Example: (0,0) and (0,side): Manhattan = side. Arc via left edge = side. Equal. Example: (side, 0) and (0, side): Manhattan = 2·side. Arc = 2·side either way. Equal. Example: (1,0) and (0,side) with side=2: Manhattan = 1+2 = 3. Arc via corner (0,0): 1+2 = 3. Equal — these are adjacent edges actually (bottom and left share corner (0,0)). True opposite edges: bottom (y=0) and top (y=side): (a,0),(b,side). Arc via left = a+side+b, via right = (side−a)+side+(side−b). With a=2,b=0,side=2: via left = 2+2+0=4, via right = 0+2+2=4, Manhattan = 2+2=4. With a=1,b=0: via left=1+2+0=3, via right=1+2+2=5, arc=3; Manhattan=1+2=3. Equal! Because min(a+b, 2side−a−b): with a+b ≤ side, is a+b = side−|a−b|? a+b vs side−|a−b|: a=1,b=0,side=2: a+b=1, side−|a−b|=1. Equal here. In general if a≥b: side−|a−b| = side−a+b; a+b ≤ side−a+b iff a ≤ side/... a+b ≤ side −a + b iff 2a ≤ side. Not always. Take side=10, a=8,b=1: a+b=9, side−|a−b|=3. min(9, 20−9=11)=9. Arc = 10+9=19. Manhattan = 7+10=17. NOT equal! So the claim "Manhattan = shorter arc" is FALSE in general. Check concretely: side=10, points (8,0) and (1,10). Manhattan = 7+10 = 17. Perimeter = 40, shorter arc = min(8+10+1, 2+10+9) = min(19,21) = 19. Indeed 17 < 17... 17 < 19, so cutting through interior is shorter. The plan's crux is wrong as stated.

BUT: does the maximin problem still reduce to arc distance? If we select points with pairwise arc distance ≥ D, does that imply Manhattan ≥ D? No — Manhattan can be less than arc. Conversely Manhattan ≥ D doesn't imply arc ≥ D either (Manhattan ≥ D but arc could be... arc ≥ Manhattan always? Is Manhattan ≤ shorter arc always? Manhattan = straight-line-ish L1 through interior; any boundary path is a path, and Manhattan distance is the minimum L1 path length over ALL paths, so Manhattan ≤ any boundary arc length, hence ≤ shorter arc. Yes: Manhattan ≤ arc always.) So arc ≥ D is a sufficient but not necessary condition for Manhattan ≥ D. The true feasible region is larger, so optimizing over arc gives a lower bound, not the exact answer. The plan as stated is incorrect.

However — maybe the intended solution uses a different reduction. Think: Manhattan distance between boundary points. Alternative: the answer's structure. Common trick for this known problem (LeetCode "Maximize the Minimum Distance... " — this looks like LC 3553? Actually it's similar to a known problem where the answer IS based on perimeter arc because points are on the boundary and they claim distance = min arc... Let me re-derive more carefully whether Manhattan between boundary points equals min arc. Counterexample above: (8,0),(1,10), side 10. Manhattan = |8−1|+|0−10| = 17. Arc shorter = 19. So no. Hmm, but wait — is the boundary path via corner (10,0)→(10,10)? (8,0)→(10,0)→(10,10)→(1,10): 2+10+9 = 21. Via (0,0)→(0,10): 8+10+1 = 19. Yes 19. So the plan's premise fails.

So we need a different approach. Observations: k ≤ 25 (small!), n ≤ 15000, side up to 1e9. Binary search on D with a feasibility check: "can we pick k points with pairwise Manhattan ≥ D?" That's an independent-set / packing problem on a graph (conflict graph: edges between points closer than D). General feasibility is NP-hard-ish, but geometry helps.

Geometric structure of conflict: two boundary points conflict if Manhattan < D. On the perimeter ring, the set of points within Manhattan < D of a given point... Since Manhattan ≤ arc, conflict requires arc < ... no: Manhattan < D can happen with arc up to nearly 2D? Points within Manhattan distance < D of p form an L1 ball (diamond) intersected with boundary. On the perimeter, that's a union of at most 2 arcs? A diamond centered at p intersected with the square boundary: the boundary is a 1D loop; the intersection of the loop with a diamond is a set of arcs of the loop — could be 2 disjoint arcs (if diamond centered on boundary covers two separated pieces, e.g., p on bottom edge, diamond reaching top edge? Diamond radius D around p on bottom: reaches top edge only if D > side, and then covers an interval of the top edge plus intervals on left/right/bottom — the bottom/left/right portions form one contiguous arc around p, the top portion is a separate arc. So at most 2 arcs (maybe more for corner cases, but bounded small constant). So each point conflicts with points in at most 2 (or O(1)) perimeter arcs.

Feasibility check with small k (≤25): could do backtracking/branch and bound? Worst case could blow up but n=15000, k=25... risky.

Alternative: think about answer structure. Total perimeter P = 4·side. If we require arc ≥ D, max points ≈ P/D. But Manhattan can be smaller than arc only for points "across" the square (opposite edges, close in L1 through interior but far along boundary... wait no: Manhattan < arc happens when interior shortcut is shorter, i.e., points on opposite edges where |a−b| < min(a+b, 2side−a−b)−... anyway).

Hmm, actually reconsider: when is Manhattan strictly less than shorter arc? Same edge: equal. Adjacent edges: equal (shown above). Opposite edges: Manhattan = side + |a−b|, arc = side + min(a+b, 2side−a−b). Strictly less iff |a−b| < min(a+b, 2side−a−b), i.e., when the horizontal offset is small relative to distances to corners — i.e., points roughly facing each other across the square. So conflicts across opposite edges: point (a,0) conflicts with top points (b,side) where side+|a−b| < D, i.e., |a−b| < D−side. Only relevant when D > side. Similarly left vs right.

Case analysis on D vs side:
- If D ≤ side: conflicts only via arc (same/adjacent edges give arc=Manhattan; opposite edges give Manhattan = side+|a−b| ≥ side ≥ D, no conflict). Wait need Manhattan < D ≤ side, but opposite-edge Manhattan ≥ side ≥ D, so no cross conflicts. Then feasibility = pure circular arc spacing problem! Greedy works.
- If D > side: cross conflicts appear: bottom point near x=a conflicts with top points near x=a (within D−side), similarly left/right. Also note if D > 2·side, even corners conflict... Manhattan max is 2·side (opposite corners). So answer ≤ 2·side. For D in (side, 2·side]: each point conflicts with: an arc of perimeter around itself (arc < D, which now wraps: arc distance < D covers up to... arc < D along perimeter both directions, but capped at half perimeter 2·side; since D ≤ 2·side it's a contiguous arc of length 2D around p, possibly whole loop if D ≥ 2·side) PLUS a mirror arc on the opposite edge (points facing it). So conflict set = at most 2 arcs. Feasibility: select k points on a loop avoiding pairwise conflicts — with k ≤ 25 maybe do interval-based DP or branch-and-bound. Alternatively, since D > side means selected points must be pairwise far: how many points can we even place? On a ring of perimeter 4·side with arc spacing ≥ D > side... up to 3 points arc-wise (4·side/D < 4). But arc spacing isn't required — cross-edge pairs can be arc-far yet Manhattan-close, and conversely arc-close points on opposite edges can be Manhattan-far? No: Manhattan ≤ arc, so arc-close (arc < D) ⇒ possibly Manhattan < D but not necessarily... Manhattan ≤ arc < D ⇒ Manhattan < D. Yes! arc < D implies Manhattan < D. So Manhattan ≥ D REQUIRES arc ≥ D. Necessary condition. So selected points must be arc ≥ D apart pairwise. With D > side and perimeter 4·side: max selectable k ≤ floor(4·side / D) ≤ 3. Since k ≥ 4, D > side is only feasible if... floor(4·side/D) ≥ 4 requires D ≤ side. So for k ≥ 4, any D > side is INFEASIBLE. Therefore the answer is always ≤ side (given k ≥ 4)! And in the regime D ≤ side, Manhattan ≥ D ⟺ arc ≥ D. The reduction is rescued by the constraint k ≥ 4.

Double-check: answer could equal side? Example 1: side=2, k=4, answer 2 = side. Consistent. Feasibility of D = side requires arc spacing ≥ side, 4 points exactly at 4 corners-ish. Fine.

Edge case: what if k=4 and side large but points clustered? Answer < side, fine, still in arc regime. What if answer > side possible when k=4? Arc argument: 4 points pairwise arc ≥ D needs 4D ≤ 4·side ⇒ D ≤ side. Solid.

So the plan survives with a corrected justification: since k ≥ 4, answer ≤ side, and for D ≤ side, Manhattan distance between boundary points ≥ D iff perimeter arc distance ≥ D (because cross-opposite-edge pairs have Manhattan ≥ side ≥ D automatically, and all other pairs have Manhattan = arc). Wait, also need: pairs with arc < D but on opposite edges — can arc < D ≤ side happen for opposite-edge points? Opposite-edge arc = side + min(...) ≥ side ≥ D. So no. All pairs with arc < D have Manhattan = arc < D. And pairs with arc ≥ D: Manhattan ≥ ... need Manhattan ≥ D. If same/adjacent edges: Manhattan = arc ≥ D ✓. If opposite edges: Manhattan ≥ side ≥ D ✓. So for D ≤ side: Manhattan ≥ D ⟺ arc ≥ D. 

Then the problem becomes: points on a circle of circumference P = 4·side, choose k maximizing min circular spacing. Binary search D ∈ [1, side] (answer ≥ 1? points are distinct integers, min distance ≥ 1; with k ≤ n points we can always achieve 1? Pairwise ≥ 1 trivially since distinct integer points have Manhattan ≥ 1. So lo=1... but feasibility check handles it; binary search range [1, side]).

Feasibility check for circular spacing ≥ D: sorted positions p[0..n-1] on ring of length P. Standard greedy: try each start index i (or a smarter way): select greedily next point ≥ prev + D, count how many we can fit within < p[i] + P; also need wrap-around constraint: last selected must be ≤ p[i] + P − D. Greedy that picks earliest each time maximizes count; if count ≥ k and the k-th point ≤ p[i]+P−D, feasible. Actually if we can fit k points in [p[i], p[i]+P−D] with spacing D, feasible. Greedy earliest-pick gives the earliest possible position of the k-th pick; if that's ≤ p[i]+P−D, feasible. Trying all n starts is O(n²) per check → 15000² × log ≈ too slow (2.25e8 × 31). Need O(n) or O(n log n) check.

Better: fix start = p[0] only? Not sufficient on a ring in general... For the classic "max min distance on a circle," feasibility can be checked by trying each start, but there's a trick: duplicate array, and for each i compute greedy chain via precomputed "next pointer" jumps (binary lifting or two pointers). With two pointers, nxt[i] = first index ≥ p[i]+D (in duplicated array). Then from start i, chain length via repeated jumps — O(k) per start with k ≤ 25 → O(n·k) = 15000×25 = 375k per check, × ~31 binary steps ≈ 11.6M — fine in Python? ~10⁷ operations, borderline but okay (maybe 2-4s). Can reduce: binary search range [1, side] is 30 steps; could also note answer ≤ P/k and binary search tighter. Or precompute nxt with two pointers O(n), then for each start walk k jumps. Also early-exit when feasible. Should be acceptable. Alternatively only try starts among first few? Not safe. Another optimization: we only need to try starts i where p[i] is selected; WLOG some point is selected, and we can try all i. With k≤25 cap, fine.

Also can speed: instead of per-start O(k), note chain from i: positions i, nxt[i], nxt²[i], ... need nxt^{k-1}[i] ≤ i + n − 1 index-wise with p[...] ≤ p[i]+P−D. Binary lifting could make O(n log k) but unnecessary.

Alternative check without trying all starts: greedy from p[0] gives max count in linear chain; on ring, feasible iff exists start. Trying all starts is standard.

Complexity: O(log(side) · n · k) ≈ 31 × 15000 × 25 ≈ 1.2e7 — okay in Python with tight loops (use local vars, bisect). Two-pointer precompute of nxt in duplicated array: indices 0..2n-1, nxt[i] for i < n: smallest j > i with p2[j] ≥ p2[i]+D, j could be ≥ i+n (then chain dies). Then for each i in 0..n-1: walk up to k−1 jumps, check final position ≤ p[i] + P − D, and also ensure each jump index < i+n (positions within one lap). If success → feasible.

Mapping point to arc position: going counterclockwise from (0,0): bottom edge (y=0): t = x. Right edge (x=side): t = side + y. Top edge (y=side): t = 2·side + (side − x). Left edge (x=0): t = 3·side + (side − y). P = 4·side. Sort by t. Duplicates impossible (unique points).

Pitfalls:
- Direction consistency (clockwise vs ccw) doesn't matter.
- Wrap-around constraint: last − first ≤ P − D (i.e., gap back to start ≥ D).
- Binary search bounds: lo=1 (or 0), hi=side (answer ≤ side when k≥4 — but prove in comments; safer hi = 2·side and let check reject; but check with D>side would incorrectly... careful: our check uses arc distance, which for D > side is still a valid necessary condition but not sufficient — however D > side is infeasible anyway under true Manhattan since arc < D ⇒ Manhattan < D... wait we need: if check says feasible (arc ≥ D) then Manhattan ≥ D? For D > side that's false (opposite-edge facing points: arc ≥ D possible while Manhattan < D). E.g., side=10, D=15, points (8,0) arc-far from (1,10)? arc=19 ≥ 15 but Manhattan=17 ≥ 15 — bad example; need Manhattan < D ≤ arc: (8,0),(2,10): Manhattan=6+10=16, arc=min(8+10+2, 2+10+8)=20. Hmm Manhattan=16 ≥ 15. Try (5,0),(5,10): Manhattan=10, arc=20. D=15: arc ≥ 15, Manhattan=10 < 15. So arc-check could say feasible while true infeasible for D > side. Hence MUST cap hi at side. Prove answer ≤ side: k ≥ 4 selected points pairwise Manhattan ≥ D ⇒ pairwise arc ≥ D (since Manhattan ≤ arc... wait direction: Manhattan ≥ D and Manhattan ≤ arc gives arc ≥ Manhattan ≥ D ✓). Sum of k arc gaps around ring = P ⇒ k·D ≤ P = 4·side ⇒ D ≤ 4·side/k ≤ side since k ≥ 4. So hi = side (or 4·side//k, tighter!). Use hi = min(side, 4*side//k) = 4*side//k when k≥4. Nice tighter bound: hi = P//k.
- lo: 1? If k ≤ n, can always pick k distinct integer points, min pairwise ≥ 1. So answer ≥ 1, lo=1 feasible. Or start lo=0 safe.
- Integer binary search: while lo < hi: mid = (lo+hi+1)//2; if feasible(mid): lo=mid else hi=mid−1.
- n up to 15000, points.length ≥ 4, k ≥ 4.
- Note points.length ≤ 4·side ensures side ≥ 1 fine.

Feasibility implementation detail: build p2 = p + [x+P for x in p]. Two pointers: j pointer monotonic. nxt array size 2n maybe. For i in range(n): cur = i; pos = p[i]; limit = p[i] + P − D; ok = True; for _ in range(k−1): cur = nxt[cur]; if cur >= i+n or p2[cur] > limit: ok=False; break. If ok → return True. nxt[cur] defined for cur up to i+n−1 ≤ 2n−2; compute nxt over duplicated indices 0..2n−1 with j up to 2n−1; if none, set nxt = INF (2n). Precompute nxt via: j=0; for i in range(2n): while j < 2n and p2[j] < p2[i]+D: j+=1; nxt[i]=j. But j must be ≥ i+1; since p2[i] < p2[i]+D, j ends > i. Monotonic j works as p2 sorted. O(2n).

Early termination: also can skip starts: if greedy from i fails quickly... fine.

Micro-opt: precompute p2 list; inner loop with local variables. 31 × 15000 × avg jumps (≤24) ≈ 1.1e7 — Python ~5-10s might TLE. Optimizations: (a) binary search over [1, P//k] — still ~30 iterations worst (P/k up to 1e9). (b) Reduce per-check cost: instead of trying every start, note greedy from start i: first jump lands at nxt[i]; chain is i→nxt[i]→... The success condition monotone in start? Not exactly. Alternative: binary lifting: precompute jump table up to 2^5 (k≤25 → need up to k−1 ≤ 24 jumps, 5 levels) per check? Rebuilding table per check is O(n log k) = 15000×5 = 75k per check × 31 = 2.3M — much better! jump[i] after 2^e jumps via doubling: jp[e][i] = jp[e-1][jp[e-1][i]]. Build O(n log k). Then per start: decompose k−1 into bits, cur = apply jumps — O(log k) per start → O(n log k) per check total ≈ 75k... wait per start O(log k), n starts → O(n log k) = 75k per check. ×31 = 2.3M ops. 

But careful: jump pointers into duplicated array with index cap; represent "dead" as 2n (INF) and make jp table handle INF → INF. p2 access for limit check: after total jumps cur, check cur < i+n and p2[cur] ≤ p[i]+P−D.

Alternatively simpler: since k ≤ 25, per start O(k) with early break often fast; but worst case (all points spread, D small) every start succeeds at k jumps → full 24 jumps × 15000 × 31 = 11M — probably okay-ish (~3-6s in Python, risky). Use binary lifting to be safe, or use the trick: we don't need all starts — if any start works, then the start that is the first selected point works; greedy from i selects nxt chain; note chain from i and from nxt[i] overlap heavily... Simpler safe route: binary lifting.

Even simpler alternative: O(n) check via trying start = each i but reusing? There's known linear approach: feasible iff exists i such that f(i) ≤ i+n where f computed... binary lifting is clean enough.

Actually, simplest robust: per check, compute nxt (two pointers O(n)); then doubling table for k−1 jumps: since k−1 ≤ 24, levels = 5 (1,2,4,8,16). Build list of arrays. Then loop starts. Let me estimate: building table 5×30000 = 150k ops; starts: 15000 × 5 = 75k. Per check ~225k ops; ×31 ≈ 7M. Hmm similar. But constants lower. Or: skip table, per start walk but memoize chain results: memo[i] = (end_index_after_{k-1}_jumps) computed via DP? Chain from i: end(i) = end(nxt[i]) but with jump count reduced — not directly memoizable since count differs; but we can memo (i, remaining) — too big.

Alternative neat trick: compute g[i] = index reached after k−1 greedy jumps from i, for all i, using the fact g[i] = h(nxt[i]) where h gives k−2 jumps... variable counts again. Just do binary lifting or accept O(nk). Given constraints (n=1.5e4, k≤25, 31 iters → ≤1.2e7 simple loop iterations), Python might pass with pypy-style optimizations. I'll go with binary lifting for safety, or a hybrid: walk with early exit plus binary lifting. Decide in implementation: binary lifting, levels = (k-1).bit_length().

Wait — one more correctness consideration: greedy earliest-pick on a ring from fixed start i gives the lexicographically smallest selection; if any selection of k points starting at i (i.e., i is the smallest-indexed selected, within window [p[i], p[i]+P)) satisfies wrap constraint, greedy's k-th point is earliest possible, so if greedy's k-th point > limit, no other choice from i works. And if a feasible configuration exists, let its smallest-arc point be some point q = p[i]; greedy from i works. Standard.

Also need nxt defined as first index j with p2[j] ≥ p2[i] + D (strictly greater index since D ≥ 1 > 0 and unique positions).

Also answer lower bound: with distinct integer points and k ≤ n, D=1 always feasible: arc positions distinct integers, spacing ≥ 1 achievable? On a ring, k points pairwise arc ≥ 1 iff distinct — yes since positions are distinct integers. Greedy will find. Good, lo=1.

Let me also double check the "Manhattan = arc for same/adjacent edges" and "≥ side for opposite edges" claims once more:
- Same edge: arc = |difference along edge| (shorter arc could go the other way around: other way = P − d ≥ 2·side ≥ ... d ≤ side ≤ P−d, so shorter arc = d = Manhattan ✓).
- Adjacent edges sharing corner c: Manhattan(p,q) = dist(p,c)+dist(c,q) (L1 path via corner is monotone: e.g., p=(a,0) bottom, q=(side,b) right: |a−side|+|0−b| = (side−a)+b = via corner ✓). Arc via shared corner = same value; other arc = P − that ≥ 2·side ≥ that (since that ≤ 2·side) ✓. Equal.
- Opposite edges: Manhattan = side + |a−b| ≥ side ✓ (arc = side + min(a+b, 2side−a−b) ≥ side too, and ≥ Manhattan).
Also corner cases where point is a corner belonging to two edges — consistent either way.

And "Manhattan ≤ arc always": Manhattan is min over all L1 paths; boundary arc is a path with L1 length = arc length (axis-aligned segments) ✓.

Thus for D ≤ side: (Manhattan ≥ D) ⟺ (arc ≥ D). Proof: If arc < D: arc < D ≤ side ⇒ pair not opposite-edge (opposite arc ≥ side) ⇒ Manhattan = arc < D. If arc ≥ D: if opposite-edge, Manhattan ≥ side ≥ D; else Manhattan = arc ≥ D. ✓

And answer ≤ P/k ≤ side since k ≥ 4: selected k points pairwise Manhattan ≥ ans ⇒ pairwise arc ≥ ans ⇒ k·ans ≤ P. ✓

Now the mapping/sorting: t values in [0, P). Sort points by t. n = len(points).

Binary search: lo = 1, hi = P // k (which is ≤ side for k ≥ 4). While lo < hi: mid = (lo+hi+1)//2; feasible(mid) ? lo=mid : hi=mid−1. Return lo.

feasible(D): 
- p sorted list, n, P. p2 = p + [x+P for x in p]. N2 = 2n. INF = N2 (index meaning dead).
- nxt = [INF]*(N2+1)? Build via two pointers: j = 0; for i in range(N2): advance j = max(j, i+1)... standard: j pointer nondecreasing: for i in range(N2): if j < i+1: j = i+1; while j < N2 and p2[j] < p2[i] + D: j += 1; nxt[i] = j (j may == N2 = INF). nxt[INF] = INF conceptually.
- Binary lifting: levels L = (k-1).bit_length(). jp = nxt + [INF] (size N2+1). For each level: jp = [jp[jp[i]] for i in range(N2+1)]. Store list of levels.
- For i in range(n): limit = p[i] + P − D; cur = i; rem = k−1; bit=0; while rem: if rem&1: cur = jp[bit][cur]; rem >>=1; bit+=1. After: if cur != INF and cur < i+n and p2[cur] <= limit: return True. (cur < i+n implied by p2[cur] ≤ limit < p[i]+P = p2[i+n], so just check cur ≤ N2−1 and p2[cur] ≤ limit; INF index N2 has no p2 — guard cur < N2.)
- Return False.

Cost per check: nxt O(n), lifting O(n·L) with L ≤ 5, starts O(n·L). Total ~O(n·L) ≈ 15000×5×(few) — fast. 31 checks → few million ops. 

Alternative simpler O(n·k) per check might pass but lifting is safer.

Potential pitfall: p2[j] < p2[i]+D with j starting from previous i's j — valid since p2[i] increasing ⇒ threshold increasing ⇒ j monotone. ✓

Edge cases: points include corners — mapping gives t=0 for (0,0); (side,0) → t=side (bottom) ✓; (side,side) → 2·side ✓; (0,side) → 3·side ✓. Consistent.

k = n possible (k ≤ points.length): then need all points pairwise ≥ D; greedy handles.

Large coordinates fine (Python ints).

Now also sanity-check examples:
Ex1: side=2, corners, P=8, k=4, hi=2. t = [0? (0,0)→0, (2,0)→2, (2,2)→4, (0,2)→6]. D=2: spacing exactly 2 around ring, feasible → answer 2 ✓.
Ex2: side=2, points (0,0)t0,(2,0)t2,(2,1)t3,(2,2)t4,(1,2)t=2+ (2−1)=5? top edge: t=2·side+(side−x)=4+1=5. Sorted [0,2,3,4,5], k=4, hi=2. D=2: start 0: nxt≥2→2, ≥4→4, ≥6→ index of ≥6 in p2: p2=[0,2,3,4,5,8,10,11,12,13], from 4 need ≥6 → 8? wait need 3 jumps for k=4: 0→2→4→? ≥6 → p2=8 (index5 = i+n exactly, value 8). limit = 0+8−2=6. 8 > 6 fail. Start 2: 2→4→? ≥6 →8? p2: from 4 (value4) need ≥6 → value8 (idx5). Then need ≥10 → idx6 value10. limit=2+6=8. 10>8 fail. Start3: 3→5→? ≥7→8→≥10→10; limit=3+6=9; 10>9 fail. Start4: 4→? ≥6→8→10→12; limit 10; 12>10 fail. Start5: 5→? ≥7→8→10→12; limit=11; fail. D=2 infeasible → answer 1 ✓.
Ex3: side=2, points: (0,0)0,(2,0)2,(2,1)3,(2,2)4,(1,2)5,(0,2)6,(0,1)7. Sorted [0,2,3,4,5,6,7], k=5, hi=8//5=1 → answer 1 ✓.

Great.

One more subtlety: the problem says points.length ≤ min(4·side, 15000) and k ≤ min(25, len). Fine.

Also should double check the reduction's necessity direction used in binary search hi bound — done.

Now, is there any case where answer could be 0? No, distinct points, k ≤ n ⇒ ≥1.

Implementation details for speed: use array lists, local variable binding, maybe `bisect` not needed. Write clean code.

Complexity: O((n log k) log(P/k)) time, O(n log k) space (or O(n) per level reused — need all levels stored for jumps: store list of levels, memory 15000×2×5 ints fine).

Actually we can reduce memory: store levels list; fine.

Also alternative: since k−1 ≤ 24, could precompute jump^(k−1) directly via DP: end[i] after m jumps: use doubling only. Fine.

Let me now also think whether greedy check could be replaced by simpler "max count ≥ k with wrap" — no, wrap constraint essential.

Potential off-by-one: selecting k points requires k−1 jumps from start. Wrap gap: P − (last − first) ≥ D ⇔ last ≤ first + P − D ✓.

I think solution is solid. Write final code with comments explaining the reduction proof.

Code sketch:

from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        P = 4 * side
        ts = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 2 * side + (side - x)
            else:  # x == 0
                t = 3 * side + (side - y)
            ts.append(t)
        ts.sort()
        n = len(ts)
        p2 = ts + [t + P for t in ts]
        N2 = 2 * n
        INF = N2

        def feasible(D: int) -> bool:
            nxt = [INF] * (N2 + 1)
            j = 0
            for i in range(N2):
                if j < i + 1:
                    j = i + 1
                pj = p2[i] + D
                while j < N2 and p2[j] < pj:
                    j += 1
                nxt[i] = j
            # binary lifting for k-1 jumps
            levels = [nxt]
            m = k - 1
            bit = 1
            while (1 << bit) <= m:
                prev = levels[-1]
                levels.append([prev[prev[i]] for i in range(N2 + 1)])
                bit += 1
            for i in range(n):
                limit = p2[i] + P - D
                cur = i
                mm = m
                b = 0
                while mm:
                    if mm & 1:
                        cur = levels[b][cur]
                    mm >>= 1
                    b += 1
                if cur < N2 and p2[cur] <= limit:
                    return True
            return False

        lo, hi = 1, P // k
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

Check levels construction: levels[0] = 1 jump, levels[1] = 2 jumps, levels[2] = 4... bit b corresponds to 2^b. In loop, b increments matching bits ✓. nxt[INF]=INF included (size N2+1, last element INF) ✓ — nxt initialized [INF]*(N2+1) and only i<N2 assigned ✓.

Edge: k−1 = m ≥ 1 (k≥4) fine.

Note hi = P//k ≥ 1? P//k: P ≥ 4, k ≤ n ≤ P... points distinct integers on boundary ⇒ n ≤ P (4·side lattice points). k ≤ n ≤ P ⇒ P//k ≥ 1 ✓. And D=1 always feasible ✓ (distinct integer t's, greedy spacing 1 works for any k-subset... need ring spacing: pick any k points, consecutive gaps ≥ 1 since distinct integers, wrap gap ≥ 1 ✓ greedy finds).

Wait, one concern: is greedy from every start i with binary-lifting jump correct that cur after m jumps is index of (i+m)-th selected? Yes.

Also confirm the two-pointer j monotonicity with the `if j < i+1` reset: thresholds p2[i]+D increase with i, and j from previous i satisfies p2[j] ≥ prev threshold; for new larger threshold j only advances ✓.

Complexity good. Also add comment with proof of reduction.

Double-check example 2 D=1 feasibility quickly: obviously yes.

Now write final answer with explanation. Also mention why hi = P//k.

One more check on mapping when side=1: points on boundary: possible lattice points: (0,0),(1,0),(0,1),(1,1) = 4 = 4·side ✓. Mapping: (1,0): y==0 → t=1. (1,1): x==side branch → t=1+1=2. (0,1): y==side? y=1==side → t=2+(1−0)=3. Order of elif matters: (side,side) hits x==side first → t=2·side? side+y = 2 ✓ same as top formula 2·side+(side−x)=2+0=2 ✓ consistent. (0,side): y==side branch → 2·side+side = 3·side ✓. Good; corner (0,0) → 0. No duplicates.

Everything consistent. Produce final solution.

## worker: Implement the full solution: perimeter mapping, bi
**Corrected premise (the original plan's crux was wrong, but is rescued by k ≥ 4):**
- Manhattan ≤ arc always (Manhattan is the min over all L1 paths; a boundary arc is one such path).
- Manhattan can be strictly less than arc: side=10, (8,0) vs (1,10): Manhattan=17, arc=19. So the naive reduction fails in general.
- However: same/adjacent-edge pairs satisfy Manhattan == arc; opposite-edge pairs satisfy Manhattan ≥ side (and arc ≥ side). Therefore for D ≤ side: arc < D ⟹ not opposite edges ⟹ Manhattan = arc < D; arc ≥ D ⟹ either Manhattan = arc ≥ D or (opposite edges) Manhattan ≥ side ≥ D. So **Manhattan ≥ D ⟺ arc ≥ D for all D ≤ side**.
- Answer ≤ side: k selected points pairwise Manhattan ≥ D implies pairwise arc ≥ D, and the k arc gaps around the ring sum to P = 4·side, so k·D ≤ P, i.e. D ≤ P/k ≤ side since k ≥ 4. Hence the search range [1, P//k] lies entirely in the exact regime.

**Algorithm:**
1. Map each point to arc position t ∈ [0, P): bottom t=x; right t=side+y; top t=2·side+(side−x); left t=3·side+(side−y). Sort.
2. Binary search D over [1, P//k] (D=1 always feasible: distinct integer positions).
3. Feasibility = circular "aggressive cows": duplicate the sorted array; two-pointer `nxt` table; binary lifting (k−1 ≤ 24 jumps → ≤ 5 levels) so each of n candidate starts is checked in O(log k); greedy earliest-pick is optimal per start, and some start of an optimal configuration works.

**Complexity:** O(n log k) per check, O(log(P/k)) checks → ~2–3M ops total for n ≤ 15000, k ≤ 25. Memory O(n log k).

**Testing:**
- Ex1 (side=2, 4 corners, k=4): t=[0,2,4,6], hi=2; D=2 feasible → 2 ✓
- Ex2: t=[0,2,3,4,5], k=4; D=2 fails all 5 starts (verified by hand), D=1 works → 1 ✓
- Ex3: t=[0,2,3,4,5,6,7], k=5, hi=8//5=1 → 1 ✓
- side=1: only 4 lattice points, k=4, P=4, hi=1 → 1; mapping gives t=[0,1,2,3], D=1 feasible ✓
- k=n: greedy requires all points pairwise ≥ D; handled correctly.
- Clustered points: hi=P//k keeps range small; two-pointer/lifting handle dense arrays.
- Corner mapping consistency: (side,side) yields 2·side via either adjacent formula; (0,side) → 3·side; no duplicate t values.

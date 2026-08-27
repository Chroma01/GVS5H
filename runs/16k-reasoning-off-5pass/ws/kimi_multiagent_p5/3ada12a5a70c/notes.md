
## ideation
The core insight is that Manhattan distance between two boundary points equals the shorter arc length along the perimeter (this holds because any path must travel along edges; the perimeter path is always a shortest Manhattan path for boundary points). So the problem reduces to a classic 1D problem: select k points on a circle of circumference L = 4*side to maximize the minimum circular gap.

Key difficulties:
1. Correctly mapping each boundary point to a perimeter coordinate t. A consistent clockwise (or counterclockwise) parameterization is needed, e.g.: bottom edge (y=0): t = x; right edge (x=side): t = side + y; top edge (y=side): t = 3*side - x; left edge (x=0): t = 4*side - y. Corners belong to exactly one edge by this rule, and points are unique so no collisions.
2. Feasibility check for candidate distance d: we need to know if we can pick k points such that every pair has circular distance >= d. For points on a circle, the standard greedy works: fix a starting point, then repeatedly take the next point (clockwise) at arc distance >= d from the last chosen; if we can select k points and the wrap-around gap (from last chosen back to start, going around) is also >= d, then feasible. Trying every point as the start covers all cases (any feasible set has some point we can treat as start, and greedy from that start does at least as well).
3. Monotonicity: if d is feasible, any d' < d is feasible, so binary search on d in [1, ...] works. Upper bound for answer: L // k (pigeonhole: k gaps summing to L, min gap <= L/k). Actually answer <= floor(L/k), and also bounded by max pairwise distance L/2, but L/k <= L/2 for k>=2, so hi = L // k is a safe upper bound... careful: with k points on circle, sum of k consecutive gaps = L, so min gap <= L/k. Yes, hi = L // k.
4. Efficient check: sort t values. For each start index i, simulate greedy using bisect on a doubled array or modular indexing. n <= 15000, k <= 25, so O(n * k log n) per check is fine (~15000*25*14 ≈ 5M ops per check, times ~30 binary search steps = 150M... might be heavy in Python). Optimization: two-pointer / precomputed "next index at distance >= d" via binary search per start but greedy steps are at most k-1 <= 24, so per start it's k * log n. Alternatively, we can limit starts: greedy from start i and start j where t[j] is within [t[i], t[i]+d) give same first choice effectively... Actually a common optimization: only need to try starts among points, but we can break early. Alternatively, note we can precompute nxt[i] = first index with t[nxt] - t[i] >= d using binary search for all i in O(n log n), then for each start walk k steps in O(k). That's O(n log n + n*k) per check ≈ 15000*14 + 15000*25 ≈ 600K per check, times ~31 steps ≈ 18M — fine.

Actually simpler: since k <= 25, per start do bisect each step: O(k log n) per start, O(n k log n) total ≈ 5M per check, ~150M total for 30 checks — borderline but likely OK in Python if written tightly with bisect from stdlib (C implementation). Could also reduce binary search range: answer in [0, L//k], L up to 4e9, so ~32 iterations. Better to precompute nxt array with two pointers in O(n) per check, then O(n*k) walk: 15000 + 375K per check, ~12M total. 

Wrap-around condition: after selecting k points starting at s with positions p_0=s, p_1, ..., p_{k-1}, need t[s] + L - t[p_{k-1}] >= d. Also all consecutive gaps >= d by construction. Handle indices modulo n with doubled array t + [x + L for x in t].

Edge cases: d could be 0 answer? k >= 4 and points distinct, but answer could be... min distance at least 1 since integer distinct points? Points distinct integers so pairwise distance >= 1, but with k points forced, answer >= 1 always? If k <= n, we can always achieve min distance >= 1 by picking any k distinct points (distance >= 1 since distinct integer points). So lo = 1 feasible always. Binary search lo=1, hi=L//k, find max feasible.

Pitfalls:
- Perimeter mapping must be consistent; verify Manhattan = circular distance. Proof sketch: for two boundary points, a shortest Manhattan path stays within the square's bounding box; going along the boundary arc is a valid monotone path achieving arc length; any Manhattan path has length >= ... hmm, is shorter arc always equal to Manhattan distance? Consider (0,0) and (side, side): Manhattan = 2*side; arc via bottom+right = 2*side, arc via left+top = 2*side. OK. Consider (0, 1) and (side, side-1): Manhattan = side + |side-2| = 2*side - 2 (for side >= 2). Arc clockwise from (0,1): t1 = 4*side - 1; t2 = side + side - 1 = 2*side - 1. Diff = 2*side. Shorter arc = min(2*side, 4*side - 2*side) = 2*side. But Manhattan = 2*side - 2 < 2*side! Wait: |0 - side| + |1 - (side-1)| = side + (side - 2) = 2*side - 2. So Manhattan distance is NOT equal to perimeter arc distance in general! The path can cut through the interior!

Hmm, this is a critical flaw in the plan. Manhattan distance between boundary points can be shorter than the boundary arc because you can go through the interior. E.g., points on opposite sides: (0, y1) and (side, y2): Manhattan = side + |y1 - y2|, but arc = min(y1 + side + y2 ... ) etc. So the 1D circle reduction is WRONG.

So the real problem is 2D: points on the boundary of a square, Manhattan metric. Need a different approach.

Reconsider: binary search on d, feasibility = "can we pick k points pairwise at Manhattan distance >= d?" This is an independent set / packing problem. For points on a line (1D), greedy works. On the boundary of a square with Manhattan metric, structure is more complex.

Key structural observation: Manhattan distance >= d constraint. Points on the boundary. Perhaps transform coordinates: u = x + y, v = x - y; Manhattan distance = max(|du|, |dv|) (Chebyshev in rotated coords). So constraint: in (u,v) space, points must differ by >= d in at least one coordinate — i.e., no two points in an axis-aligned square of side < d... Actually pairwise L∞ distance >= d in (u,v).

Boundary of square maps to: bottom edge y=0: u = x, v = x (line u=v), u in [0, side]. Right edge x=side: u = side + y, v = side - y: u + v = 2*side... hmm the boundary maps to four segments in (u,v) space forming a rotated square (diamond): it's the square with vertices (0,0), (side, side), (2*side, 0), (side, -side) — actually the boundary maps to the boundary of the L∞ ball... The image is a square in (u,v) rotated 45°, i.e., |u - side| + |v| ... let me not go down this path yet.

Alternative: think about the feasibility check directly. Since k <= 25 is small, maybe we can do a smarter search. But n = 15000, need near-linear check.

Known approach for this exact problem (it's a LeetCode problem: "Maximize the Minimum Distance..." — I recall a problem about selecting k points on square boundary maximizing min Manhattan distance). Let me think about the structure.

Observation: For two points on the same edge, Manhattan distance = distance along that edge. For points on adjacent edges, e.g., bottom (x1, 0) and right (side, y2): distance = (side - x1) + y2 = arc distance through corner (side, 0). For points on opposite edges: bottom (x1,0) and top (x2, side): distance = side + |x1 - x2|, which can be as small as side. Left (0,y1) and right (side,y2): side + |y1-y2|.

So distances: same/adjacent edges behave like arc distance; opposite edges: side + |coord diff|.

Hmm, when is Manhattan < arc? For opposite edges: bottom-top: arc via right = (side - x1) + side + (side - x2)... wait arc from (x1,0) clockwise (bottom→right→top): (side - x1) + side + (side - x2) = 3*side - x1 - x2. Other arc: x1 + side + x2. Manhattan = side + |x1 - x2|. Compare: side + |x1-x2| vs min(x1 + x2 + side, 3*side - x1 - x2). If x1 = x2 = side/2: Manhattan = side, arcs = 2*side each. So Manhattan much smaller.

So the metric is genuinely 2D. The circle model fails.

New plan needed. Let's think about feasibility check: given d, can we select k points pairwise at Manhattan distance >= d?

Geometric interpretation: each selected point "blocks" a diamond (L1 ball) of radius d around it (open), and we need k points outside each other's diamonds. On the boundary curve.

Alternative angle: since k <= 25 and answer <= ? Let's bound the answer. Hmm, what's the max possible answer? With k=4, corners give 2*side. So answer can be up to 2*side. Binary search range [1, 2*side], ~31 steps.

Feasibility: is there a nice greedy? Consider sorting points and... The conflict graph: two points conflict if Manhattan distance < d. We need an independent set of size k. The conflict graph on boundary points with Manhattan metric — is it an interval graph or something nice?

Let's think: parameterize boundary by arc t in [0, L). For a point p at arc position t, which points q conflict with p (Manhattan(p,q) < d)? 

Case analysis by edges. Suppose d <= side. Then for p on bottom edge at (x, 0): conflicts with q on bottom: |x - xq| < d → arc interval. q on left edge (0, yq): dist = x + yq < d → yq < d - x. q on right edge: (side - x) + yq < d. q on top edge (xq, side): side + |x - xq| < d → impossible since d <= side. So conflicting set is a contiguous arc interval around p (along the perimeter)! Because only nearby edges matter, and on each the condition is a threshold on arc coordinate. Indeed for d <= side, Manhattan distance = arc distance for all pairs? Check: opposite edges have Manhattan >= side >= d, and arc >= Manhattan always? Is arc always >= Manhattan? Arc is a valid path, so Manhattan <= arc. For d <= side, conflict (Manhattan < d) implies arc < ... no wait, Manhattan < d doesn't imply arc < d... arc >= Manhattan, so Manhattan < d could still have arc >= d? If Manhattan < d then arc could be larger. Hmm, but for the conflict set being an arc interval: q conflicts iff Manhattan(p,q) < d. Since Manhattan <= arc always, arc < d implies conflict. But conflict could also happen with arc >= d? For p on bottom, q on top: Manhattan >= side >= d, no conflict. q on adjacent edges: Manhattan = arc through shared corner (as computed). q on same edge: Manhattan = arc. So for d <= side, conflict iff arc distance (the relevant one through nearby corner) < d, and the conflicting q's form a contiguous arc interval around p. 

For d > side: opposite edges can conflict: p=(x,0) bottom, q=(xq, side) top: conflict iff side + |x - xq| < d iff |x - xq| < d - side, an interval around x. On the arc, top edge points near x in coordinate are... top edge arc coordinate is 3*side - xq, so |x - xq| < d - side corresponds to arc interval centered at 3*side - x, which is the antipodal-ish region. So conflict set = arc interval around p (length 2d on the near side... capped) PLUS arc interval around the antipode of p? Hmm, actually let's reconsider: the conflict set in arc coordinates: bottom edge: (x - d, x + d) ∩ [0, side]. Left edge: yq < d - x → arc t = 4*side - yq > 4*side - (d - x). Right edge: t = side + yq, yq < d - side + x → t < d + x... wait yq < (d - (side - x)) = d - side + x, so t < side + d - side + x = d + x. Top edge: |x - xq| < d - side, t = 3*side - xq ∈ (3*side - x - (d-side), 3*side - x + (d - side)). 

So in arc coordinates, conflict set is interval (x - d, x + d) (covering bottom, left, right portions — note left/right/bottom conflict conditions merge into a single arc interval around t=x) union an interval around the antipode 3*side - x (on top edge). Interesting. So conflict set = one or two arc intervals. That makes the conflict graph a "2-interval" circular graph — independent set might still be tractable but messier.

Hmm wait, but actually maybe think in (u, v) = (x+y, x-y) coordinates where Manhattan = L∞. Constraint: pairwise L∞ distance >= d in (u,v). The boundary maps to a square in (u,v): vertices (0,0), (side,side), (2side, 0), (side, -side). Points on this rotated square, need pairwise Chebyshev distance >= d.

Feasibility check with small k (<=25): maybe backtracking with good pruning? n=15000, k=25 — worst case infeasible.

Alternative: think about it as: greedy on the arc with the "interval conflict" structure. For circular-arc conflict graphs (conflict = within arc distance d), greedy works. For d > side, two intervals...

Let me reconsider the actual LeetCode problem. This looks like LeetCode 3446? Or "Maximum Distance Between Points"... Actually I recall LC problem "maxDistance" with side, points, k — it's from a recent contest. I believe the intended solution IS the perimeter + binary search + greedy, and the claim is Manhattan distance on boundary equals perimeter distance... but we showed a counterexample: (0,1) and (side, side-1) with side=2: points (0,1) and (2,1), Manhattan = 2. Perimeter arc: from (0,1) up to (0,2) across to (2,2) down to (2,1): 1+2+1 = 4; other way: 1 + 2 + 1 = 4 (down to (0,0), across to (2,0), up to (2,1)). Arc = 4 = L/2. Manhattan = 2. So they differ.

Hmm wait, but maybe the problem intends distance measured along the boundary? Re-read: "Manhattan Distance between two cells (x_i, y_i) and (x_j, y_j) is |x_i - x_j| + |y_i - y_j|." Standard Manhattan. So the perimeter reduction is wrong.

Let me look at examples: Example 2: side=2, points [[0,0],[1,2],[2,0],[2,2],[2,1]], k=4, answer 1. With perimeter model: L=8, t values: (0,0)→0, (1,2)→ top edge: 3*2-1=5, (2,0)→2, (2,2)→4, (2,1)→3. Sorted: 0,2,3,4,5. Choose 4 maximizing min circular gap: {0,2,4,5}: gaps 2,2,1,3 → min 1. {0,2,3,5}: 2,1,2,3→1. Best min gap = 1? {0,2,4,...} need 4 points: 0,2,4,5→1. Seems answer 1 matches. Example 3: side=2, points [[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]], k=5, answer 1. t: (0,0)→0, (0,1)→7, (0,2)→6, (1,2)→5, (2,0)→2, (2,2)→4, (2,1)→3. Sorted: 0,2,3,4,5,6,7. Pick 5 from 7 on circle L=8: min gap maximized: drop 2 points; best: {0,2,4,6,...} need 5: gaps would be 2,2,2,2 sum 8, need 5 points so min gap <= 8/5 = 1.6 → 1. Achievable: {0,2,4,5,7}? gaps 2,2,1,2,1 → 1. Yes answer 1. Both models agree on these examples (small side=2, d=1 <= side).

Example 1: corners, k=4, answer 2. Both models: Manhattan between adjacent corners = 2, opposite = 4; min = 2. Perimeter: gaps 2 each. Answer 2. OK.

So examples don't disambiguate. Need to determine the true intended solution. Given constraints (n <= 15000, k <= 25), and it's a hard problem presumably. Let me think about the correct feasibility check for the 2D metric.

Actually, wait. Let me reconsider: maybe the intended solution really is perimeter-based and the problem's tests... no, we must solve the stated problem correctly.

Let's think again about the conflict structure in arc coordinates for general d:

For point p, conflict set C(p) = {q : Manhattan(p,q) < d}.

Claim: C(p) is a contiguous circular arc interval. Let's verify with p = (0, 1), side = 2, d = 3. Conflicts: q with Manhattan < 3. q=(2,1): dist 2 < 3, conflict. q=(2,2): dist 3, no. q=(2,0): dist 3 no. q=(1,2): dist 2, conflict. q=(0,2): 1, conflict. q=(0,0): 1 conflict. q=(2,... ) etc. Arc positions (side=2, L=8): p=(0,1) → t=7. Conflicting: (0,0)→0, (0,2)→6, (1,2)→5, (2,1)→3. In circular order near t=7: ..., 5, 6, [7], 0(wrap=8), ... and 3. Is {0, 3, 5, 6} a contiguous circular interval around 7? Circular interval from 5 to 8(=0) contains 5,6,7,0 but not 3. So conflict set is NOT a single arc interval. It's two intervals: (7-d, 7+d) mod 8 = (4, 10) mod 8 = (4,5,6,7,0,1,2) plus antipodal interval around 3: (3-1, 3+1) = (2,3,4). So {5,6,0} ∪ {3}. Matches: conflicts {0,3,5,6}. Yes, two intervals.

So for d > side, conflict = near interval ∪ antipodal interval. Independent set in such a graph with k <= 25... 

Alternative approach: think in (u,v) coordinates. L∞ >= d means: sort by u; two points conflict only if |du| < d AND |dv| < d. 

Hmm, let me think about the known solution to this problem. I'm fairly sure this is LeetCode 3464 "Maximize the Distance Between Points on a Square". Let me recall... Yes! LC 3464. And I believe the intended solution IS the perimeter mapping with binary search and greedy. Let me double check the distance claim for that problem... 

Hmm, in LC 3464, I recall the editorial maps points to perimeter and uses circular distance. But we showed Manhattan ≠ perimeter arc. Unless... let me recompute (0,1) to (2,1), side=2. Manhattan = |0-2| + |1-1| = 2. Perimeter shorter arc: path along boundary: (0,1)→(0,0)→(2,0)→(2,1) = 1+2+1 = 4; other direction (0,1)→(0,2)→(2,2)→(2,1) = 1+2+1=4. Shorter arc = 4. Manhattan = 2 ≠ 4. So if the problem used these, answer would differ. But maybe the editorial is wrong? No, editorials are correct usually. Let me recheck the problem statement of LC 3464: "You are given an integer side... points on the boundary... select k points such that the minimum Manhattan distance between any two selected points is maximized." Hmm.

Wait, maybe I should reconsider: is Manhattan distance between boundary points equal to the shorter perimeter arc? Counterexample stands: (0,1), (2,1), side 2: Manhattan 2, arc 4. So no.

Unless the problem defines distance along the perimeter? The statement here clearly says Manhattan. So the perimeter approach is incorrect for this problem as stated. But hold on — maybe I misremember and LC 3464's solution is indeed perimeter-based, meaning the problem's actual tests/definition make it equivalent... Let me test with a potential case: side=2, points = all 8 boundary lattice points, k=4. Perimeter model: L=8, points at 0..7, choose 4: best min gap = 2 (e.g., {0,2,4,6} = (0,0),(2,0),(2,2),(0,2) corners, min Manhattan = 2). Manhattan model: can we do better than 2? Choose (0,0),(2,0),(2,2),(0,2): min pairwise Manhattan = 2. Any 4 points with min Manhattan >= 3? Total points 8; each point excludes others within Manhattan < 3. Try (0,0): excludes (1,0),(0,1),(2,0)? dist to (2,0)=2 <3 yes excludes. Remaining allowed: (2,1)? dist=3 ok, (2,2) dist 4, (1,2) dist 3, (0,2) dist 2 excluded. So from {(2,1),(2,2),(1,2)} pick 3 more with pairwise >= 3: (2,1)-(1,2): dist 2 <3. (2,1)-(2,2): 1. (2,2)-(1,2): 1. Can't. So answer 2, both models agree here.

Find a case where they differ: side=3, points (0,1) and (3,1) and others. Manhattan((0,1),(3,1)) = 3, arc = min(1+3+1, 2+3+2) = 5. Suppose points = [(0,1), (3,1), (1,3), (2,0)... ] hmm construct: side=4, points (0,2),(4,2),(2,0),(2,4) (midpoints of edges). Manhattan between adjacent midpoints: (0,2)-(2,0): 4; (0,2)-(2,4): 4; opposite: (0,2)-(4,2): 4; (2,0)-(2,4): 4. All pairs >= 4! Min = 4. Perimeter model: t: (0,2)→14, (4,2)→6, (2,0)→2, (2,4)→10. Sorted: 2,6,10,14, gaps 4,4,4,4 → min 4. Same.

Try side=4, k=2, points (0,2),(4,2): Manhattan 4, arc min(2+4+2, ...) = 8? t: 14 and 6: |14-6|=8, L=16, shorter = 8. Perimeter model answer 8, true answer 4. DIFFERENT! So for k=2 with these two points, perimeter model gives 8 but correct is 4. But k >= 4 per constraints. Still, the models differ in general.

So the perimeter approach is simply wrong for this problem as stated. Hmm, but wait — maybe LC 3464 answer for such a case is indeed computed via perimeter and the problem intends "distance along the boundary"? Let me recall the actual LC 3464 statement... I genuinely recall it says Manhattan distance. And I recall solutions mapping to perimeter. Let me re-examine whether Manhattan on boundary equals arc... 

(0,1) and (2,1) with side=2: is the Manhattan distance 2? |0-2|+|1-1| = 2. Yes. Arc 4. So they're unequal, definitively.

Hmm, so either my memory of the LC solution is wrong, or... Let me think about what the correct solution is then.

Actually, wait. Let me reconsider. Maybe I misremember and the LC problem's solution does use perimeter because of a subtle fact: for the MAXIMIN problem with k >= 4... no, the objective values differ as shown (k=2 example). With k>=4 maybe optimal answers coincide? Unlikely in general. Let me construct k=4 differing case: side=4, points: (0,2),(4,2),(2,0),(2,4) plus we must have exactly these 4 (n>=4 ok). k=4: select all. True min Manhattan = 4 (computed above). Perimeter model: gaps 4,4,4,4 → 4. Same. Hmm because these are evenly spaced.

Construct: side=10, points: (0,5),(10,5),(5,0),(5,10). Manhattan: (0,5)-(10,5)=10; (0,5)-(5,0)=10; (0,5)-(5,10)=10; (10,5)-(5,0)=10; (10,5)-(5,10)=10; (5,0)-(5,10)=10. Min=10. Perimeter: t: (0,5)→35, (10,5)→15, (5,0)→5, (5,10)→25. Gaps: 10,10,10,10 → 10. Same again! Interesting — midpoints always equidistant.

Try points clustered: side=10, points (0,4),(0,6),(10,4),(10,6), k=4. Manhattan: (0,4)-(0,6)=2; min = 2. Perimeter: t: (0,4)→36,(0,6)→34,(10,4)→14,(10,6)→16. Sorted: 14,16,34,36: gaps 2,18,2, circular 14+... 36→14 wrap: 40-36+14=18. Min gap 2. Same.

Try to make perimeter overestimate: need two points close in Manhattan but far in arc, and the perimeter model's optimum relies on arc. side=10, points: (0,5),(10,5),(0,0),(10,0), k=4. Manhattan: (0,5)-(10,5)=10, (0,0)-(10,0)=10, (0,0)-(0,5)=5, (10,0)-(10,5)=5, (0,0)-(10,5)=15, (0,5)-(10,0)=15. Min=5. Perimeter: t: (0,5)→35,(10,5)→15,(0,0)→0,(10,0)→10. Sorted 0,10,15,35: gaps 10,5,20,5 → min 5. Same.

Hmm. Try where optimum selection differs. side=10, k=4, points: (0,5),(10,5),(5,0),(0,0)? Manhattan: (0,5)-(10,5)=10,(0,5)-(5,0)=10,(0,5)-(0,0)=5,(10,5)-(5,0)=10,(10,5)-(0,0)=15,(5,0)-(0,0)=5 → min 5. Perimeter: t: 35,15,5,0 → sorted 0,5,15,35: gaps 5,10,20,5 → 5. Same.

It seems like maybe there's a theorem: for points on the boundary of a square, Manhattan distance = shorter perimeter arc?? But we disproved it: (0,1),(2,1),side=2: Manhattan 2, arc 4. Let me recheck arc: perimeter path from (0,1) to (2,1): must stay on boundary. (0,1)→(0,0): length 1; (0,0)→(2,0): 2; (2,0)→(2,1): 1. Total 4. Other way: (0,1)→(0,2):1, →(2,2):2, →(2,1):1 = 4. Shorter arc = 4. Manhattan = 2. So arc ≠ Manhattan. But in all my k=4 examples they agreed... coincidence due to symmetry.

Construct asymmetric: side=10, k=4, points: (0,5),(10,5),(1,0),(9,0). Manhattan: (0,5)-(10,5)=10; (0,5)-(1,0)=6; (0,5)-(9,0)=14; (10,5)-(1,0)=14; (10,5)-(9,0)=6; (1,0)-(9,0)=8. Min=6. Perimeter: t: (0,5)→35, (10,5)→15, (1,0)→1, (9,0)→9. Sorted: 1,9,15,35: gaps 8,6,20,6(wrap: 40-35+1=6). Min=6. Same!! 

Hmm interesting. Let me directly hunt for difference with k=4. The k=2 example differed (4 vs 8). For k>=4 maybe a theorem: maximin value is the same? That seems unlikely. Let me try: side=10, points (0,5),(10,5),(5,0),(5,10),(0,0)... k=4, choose best 4. Manhattan: dropping one point: drop (0,0): remaining 4 midpoints: min 10 (computed). So answer >= 10. Can we get >10? Only 5 points, must drop 1: drop a midpoint, e.g., drop (5,10): {(0,5),(10,5),(5,0),(0,0)}: (0,0)-(0,5)=5. No. So answer 10. Perimeter: t: 35,15,5,25,0. Sorted 0,5,15,25,35. Choose 4 of 5 maximizing min circular gap: drop one: drop 0: {5,15,25,35}: gaps 10,10,10,10 → 10. Answer 10. Same.

Let me try to really break it. The perimeter model can overestimate when two points are Manhattan-close but arc-far (opposite edges, similar coordinate). E.g., (0,5) and (10,5): Manhattan 10, arc 20 (side=10, L=40: t=35 and 15, |diff|=20, shorter 20). So perimeter thinks they're 20 apart, really 10. If optimal solution in perimeter model selects such a pair relying on the inflated distance, answers differ.

side=10, k=4, points: (0,5),(10,5),(5,0),(6,0)? Manhattan: (0,5)-(10,5)=10; (5,0)-(6,0)=1 → min 1. Perimeter: t: 35,15,5,6: gaps sorted 5,6,15,35: 1,9,20,10 → min 1. same.

Need case where we MUST select an inflated pair. n=k=4: points (0,5),(10,5),(0,6),(10,6), side=10. Manhattan: (0,5)-(0,6)=1 → min 1. Perimeter: t: 35,15,34,16: sorted 15,16,34,35: gaps 1,18,1,20 → 1. Same.

n=k=4: (0,5),(10,5),(5,0),(5,10) → both 10 as before. Inflate: (0,5),(10,5) arc 20 vs manhattan 10. For the answer to differ, need min arc > min Manhattan, i.e., all pairs arc-large but some pair Manhattan-small. n=k=4 forces selecting all. Points: (0,5),(10,5),(2,0),(8,0)? Manhattan: (0,5)-(10,5)=10; (2,0)-(8,0)=6; (0,5)-(2,0)=7; (0,5)-(8,0)=13; (10,5)-(2,0)=13; (10,5)-(8,0)=7. Min=6. Arc: t: 35,15,2,8: sorted 2,8,15,35: gaps 6,7,20,7 → min 6. Same!

Hmm! Suspicious. Maybe there IS a theorem for k >= ... no wait, we had a clean k=2 counterexample. Let me re-examine it: side=4, points (0,2),(4,2), k=2. Manhattan = 4. Arc: t(0,2)=4*4-2=14, t(4,2)=4+2=6. |14-6|=8, L=16, shorter arc=8. So perimeter model says 8, truth 4. Definitely different for k=2.

For k >= 4, is there a case? Let's think: the inflation happens for pairs on opposite edges with similar coordinates: Manhattan = side + |Δcoord|, arc = min over two routes = ... For left-right pair (0,y1),(side,y2): arc via bottom: y1 + side + y2; via top: (side-y1)+side+(side-y2) = 3*side - y1 - y2. Shorter arc = side + min(y1+y2, 2*side - y1 - y2). Manhattan = side + |y1 - y2|. These differ when min(y1+y2, 2side-y1-y2) > |y1-y2|, i.e., when the pair is "balanced" (both near middle). E.g., y1=y2=side/2: arc = side + side = 2*side (max), Manhattan = side.

So inflated pairs are opposite-edge pairs near the middle. For an answer to be wrong, the greedy/binary search on perimeter would select such a pair believing distance 2*side when it's only side.

k=4, side=10: points (0,5),(10,5),(0,4),(10,4)? Manhattan: (0,5)-(0,4)=1. min 1. Not good.

We need exactly 4 points (or few) where the only "close" pairs are inflated opposite pairs. Points: (0,5),(10,5),(5,0),(5,10): all pairs Manhattan 10, arcs: (0,5)-(10,5) arc 20, others arc 10. Min arc = 10, min Manhattan = 10. Same because other pairs cap it.

To get difference, need ALL pairs to have arc > true min Manhattan. With 4 points: (0,5),(10,5) Manhattan 10, arc 20. Need other two points such that all other pairs have Manhattan >= 10 but arc... the min arc among all pairs must exceed min Manhattan. Min Manhattan = 10 (from the opposite pair). Need all arcs > 10: but (5,0)-(0,5): arc = 5+5=10. Not >10. Choose (6,0): arc to (0,5): 6+5=11; Manhattan 11. (6,0)-(10,5): arc 4+5=9 <10. Hmm.

Points: (0,5),(10,5),(5,1),(5,9)? Manhattan: (0,5)-(10,5)=10; (5,1)-(5,9)=8 <10. No.

Try: (0,5),(10,5),(2,0),(8,10)? Manhattan: (0,5)-(10,5)=10; (2,0)-(8,10)=16; (0,5)-(2,0)=7. No.

It seems hard to construct because a third point near the "arc route" caps the arc. Intuition: arc distance = min over boundary paths; Manhattan = min over all paths. The gap between them is "witnessed" by the straight interior path. For the maximin with k>=4... hmm, no obvious theorem.

Actually, let me revisit: maybe the actual LeetCode problem 3464 answer IS perimeter-based and CORRECT for that problem because... let me recompute the k=2 counterexample against the actual problem constraints: k >= 4. So k=2 never occurs! And maybe for k >= 4 there's a theorem that the maximin Manhattan equals maximin arc distance?? That would be surprising but let me test harder.

Try side=6, k=4. Points: (0,3),(6,3),(3,0),(0,0)? Manhattan: (0,3)-(6,3)=6; (0,3)-(3,0)=6; (0,3)-(0,0)=3 → min 3. Arc: t: (0,3)→21,(6,3)→9,(3,0)→3,(0,0)→0: sorted 0,3,9,21: gaps 3,6,12,3 → 3. Same.

Points (0,3),(6,3),(3,0),(3,6): Manhattan all pairs: (0,3)-(6,3)=6, (0,3)-(3,0)=6, (0,3)-(3,6)=6, (6,3)-(3,0)=6, (6,3)-(3,6)=6, (3,0)-(3,6)=6 → 6. Arc: t: 21,9,3,15: sorted 3,9,15,21: gaps 6,6,6,6 → 6. Same.

Points (0,2),(0,4),(6,3),(3,0)? Manhattan: (0,2)-(0,4)=2 → 2. Arc: t: 22,20,9,3: gaps sorted 3,9,20,22: 6,11,2,5 → 2. Same.

Let me try to deliberately engineer: I want 4 points, all pairwise arc >= A, but some pair Manhattan < A. The Manhattan-small pair must be opposite-edge midpoints-ish. (0,5),(10,5): M=10, arc=20 (side 10). Add two more points keeping all arcs >= 12 say, but all other Manhattans >= 10 too (so that true min = 10 < 12 = arc min). Third point p3: arc distance from t=35 and t=15 must be >= 12: arc position must be in [15+12, 35-12] = [27, 23] mod 40 — empty! Circular: forbidden within 12 of 15: (3, 27); within 12 of 35: (23, 47)mod40 = (23,40)∪(0,7). Allowed: [27,23]... intersection of complements: complement of (3,27) is [27,40]∪[0,3]; complement of (23,47) is [7,23]. Intersection: empty. So no third point can be arc->=12 from both. Hence with 4 points, min arc <= ... this suggests a packing bound: arc model with k=4: max min arc <= L/4 = side. Wait L=4*side, L/4 = side = 10. So arc min <= 10 always for k=4! And Manhattan min <= arc min always (Manhattan <= arc). Hmm, so for k=4 both <= side. 

For general k: arc maximin <= L/k. Manhattan maximin <= arc maximin (since Manhattan <= arc pairwise, the max min Manhattan <= max min arc? No wait: for a fixed set, min Manhattan <= min arc. Taking max over sets: max(min Manhattan) <= max(min arc). Yes.) So Manhattan answer <= arc answer <= L/k.

For the answers to differ, need Manhattan answer < arc answer. Arc answer > side requires k < 4. Since k >= 4, arc answer <= side. And for d <= side, Manhattan < d iff arc < d (we showed earlier: for d <= side, conflict sets coincide — Manhattan >= side >= d for opposite edges, and same/adjacent edges have Manhattan = arc). Wait is that right? For d <= side: opposite edge pairs have Manhattan >= side >= d, so no conflict; arc >= Manhattan >= d, also no conflict. Same/adjacent edges: Manhattan = arc (through corner). So for all pairs, Manhattan < d ⟺ arc < d when d <= side. Therefore feasibility of d is IDENTICAL in both models for d <= side. Since arc answer <= L/k <= L/4 = side (k>=4), the arc answer is <= side, and hence Manhattan answer = arc answer! 

So the perimeter reduction IS valid given k >= 4. The constraint k >= 4 is exactly what makes it work. My k=2 counterexample is excluded by constraints. So the original plan is correct after all. I should double check the claim "for d <= side, Manhattan(p,q) < d iff arc(p,q) < d" for all boundary pairs:

- Same edge: Manhattan = arc (straight along edge). ✓.
- Adjacent edges (share corner c): Manhattan(p,q) = |p - c| + |c - q| (since path through corner is monotone: e.g., bottom (x1,0), right (side,y2): Manhattan = (side - x1) + y2 = dist to corner + dist from corner). Arc shorter = min(this, L - this). So arc <= Manhattan here! Shorter arc could be the long way around? No: shorter arc = min(through-corner distance, L - through-corner). Manhattan = through-corner distance. If through-corner > L/2, arc < Manhattan. E.g., p=(0,0) corner region... p on bottom near left corner, q on right near top: through corner (side,0): (side - x1) + y2 could be up to 2*side = L/2. So through-corner <= 2*side = L/2 always (max at x1=0, y2=side: side + side = 2side = L/2). So arc = min(Manhattan, L - Manhattan) = Manhattan when Manhattan <= L/2, which always holds (<= L/2). So arc = Manhattan for adjacent edges. ✓ (arc <= Manhattan in general anyway since arc is a valid path; and here arc = Manhattan).
- Opposite edges: Manhattan = side + |Δ| ∈ [side, 2*side]. Arc: e.g., bottom-top: via left: x1 + side + x2; via right: (side-x1) + side + (side - x2) = 3side - x1 - x2. Shorter arc = side + min(x1+x2, 2side - x1 - x2) >= side. Manhattan = side + |x1 - x2|. Is arc >= Manhattan? min(x1+x2, 2side-x1-x2) vs |x1-x2|: WLOG x1 <= x2: |x1-x2| = x2 - x1. x1 + x2 >= x2 - x1 ✓. 2side - x1 - x2 >= x2 - x1 ⟺ 2side >= 2x2 ✓. So arc >= Manhattan, with equality iff x1 = 0 or x2 = side. So for opposite edges, Manhattan can be strictly less than arc (when 0 < x1 <= x2 < side). But both are >= side >= d, so neither conflicts. ✓.

Great, so for d <= side: conflict relation identical. And answer <= floor(L/k) <= side since k >= 4. Wait, answer <= L/k in arc model; and Manhattan answer = arc answer as argued? Let me redo: Let A_arc = max over k-subsets of min arc distance; A_man = same with Manhattan. A_arc <= L/k <= side. For any d <= side: d feasible in arc model ⟺ d feasible in Manhattan model (same conflict graph). Since A_arc <= side, A_arc = max feasible d (arc) = max feasible d (Manhattan) <= side... but is A_man possibly > A_arc, i.e., some d > side feasible in Manhattan but not arc? A_man <= A_arc (shown above via min Manhattan <= min arc per set). So A_man <= A_arc <= side, and all d <= A_arc are Manhattan-feasible, so A_man >= A_arc. Hence equal. 

So the plan works: binary search d in [1, L//k] (or [0, ...]), greedy feasibility on circle. The k >= 4 constraint is essential (guarantees answer <= side).

Now the feasibility check details:
- Sort points by t.
- For candidate d, check if exists k-subset with all circular gaps >= d.
- Greedy per start: choose start s (must be one of the points), then repeatedly pick next point with t >= last + d (clockwise), up to k points; then verify wrap gap: t[s] + L - t[last] >= d. If success for any start, feasible.
- Correctness: if any feasible set exists, take its "first" point s (any member); greedy from s picks points no later than the feasible set's points (inductively), so greedy's k-th pick is at or before the feasible set's k-th pick position... standard exchange argument; then wrap gap for greedy >= that of feasible set >= d. So greedy succeeds. Need to try all n starts (or smarter).
- Complexity: O(n log n) per check with precomputed successor array via binary search, then O(nk) simulation. Or two-pointer to build nxt[] in O(n): nxt[i] = smallest j > i with t[j] >= t[i] + d (in doubled array). Then simulate from each i: k-1 jumps, check indices < i + n and final wrap. Total O(nk) per check, ~15000*25 = 375K, times ~32 binary search iterations = 12M — fine in Python.

Alternatively, note we don't need to try all starts: greedy from start i yields first pick = i, second = nxt[i]... Different starts i in the same "gaps" give same chains. But n*k is fine.

Actually simpler per-start simulation with bisect: for each start i (0..n-1), pos = i, count = 1, cur = t[i]; loop k-1 times: j = bisect_left(t_doubled, cur + d, pos+1); if j >= i + n: fail; count++, cur = t2[j], pos = j. After loop, check t[i] + L - cur >= d. That's O(n * k * log n) ≈ 15000*25*14 = 5.25M per check, *32 = 168M — too slow in Python. Better: precompute nxt via two pointers O(n) per check, then O(nk): 375K per check *32 = 12M. OK.

Even better: we can prune starts: only try starts i where the chain doesn't immediately fail. Fine.

Also we can binary search smarter: answer is one of pairwise... no, answer <= L/k and distances are integers; binary search over [1, L//k] is fine (~32 iterations since L <= 4e9).

Wait, actually there's an even simpler observation: we could also just do the check with the "nxt" array and early termination. Let me also consider: do we even need to try every start? A known optimization: the greedy chain from i: i, nxt[i], nxt[nxt[i]], ... If we compute chain for i and it fails, starts along the chain... eh, n*k with k=25 is fine.

Edge cases:
- Points on corners: mapping must be unambiguous. Using: if y == 0: t = x; elif x == side: t = side + y; elif y == side: t = 3*side - x; else (x == 0): t = 4*side - y. Corner (0,0) → y==0 branch → t=0. (side,0): y==0 → t=side. (side,side): x==side → t=2*side. (0,side): y==side → t=3*side. Good, corners map consistently and uniquely.
- t values unique since points unique and mapping injective on boundary.
- L = 4*side could be up to 4e9; hi = L // k.
- k >= 4 guaranteed, so hi <= side, ensuring validity. But even if k could be smaller, our binary search hi = L//k might exceed side and give wrong answers — but constraints say k >= 4, so fine. Actually to be safe, we could cap hi = min(L//k, side)? No: answer could exceed side? A_man <= A_arc <= L/k <= side for k>=4. So hi = L//k is a valid upper bound and automatically <= side. Good.

Wait, one more check on the greedy correctness for circular k-selection: standard result. For each start s, greedy picks the lexicographically smallest chain; if greedy fails for all starts, no feasible set. Yes.

Implementation sketch:

```python
from bisect import bisect_left
from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        L = 4 * side
        ts = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 3 * side - x
            else:
                t = 4 * side - y
            ts.append(t)
        ts.sort()
        n = len(ts)
        t2 = ts + [t + L for t in ts]

        def feasible(d):
            # nxt[i] for i in range(n): smallest j > i with t2[j] >= t2[i] + d
            # two pointers
            nxt = [0] * n
            j = 0
            for i in range(n):
                if j < i + 1:
                    j = i + 1
                while j < i + n and t2[j] < t2[i] + d:
                    j += 1
                nxt[i] = j  # may be i+n meaning none
            for s in range(n):
                pos = s
                cnt = 1
                ok = True
                for _ in range(k - 1):
                    pos = nxt[pos] if pos < n else ... 
```

Hmm, nxt defined only for i < n but chain positions can exceed n-1 (into doubled region). Need nxt for indices up to... positions in chain are < s + n <= 2n - 1. So compute nxt over doubled array for i in range(2n)? Simpler: compute nxt for all i in range(2n) with j pointer up to 2n: nxt2[i] = smallest j > i with t2[j] >= t2[i] + d, capped at 2n. Two-pointer O(2n). Then simulate: from s, do k-1 jumps: pos = nxt2[pos]; if pos >= s + n: fail. After k-1 jumps, check t2[s] + L - t2[pos] >= d. Note: also need pos < s + n ensures distinct points within one loop. And the wrap check ensures last-to-first gap >= d.

Actually if pos >= s+n, fail (wrapped around). Also if nxt2[pos] == 2n (no successor), fail since s+n <= 2n - ... s+n <= 2n-1 < 2n, so pos >= s+n catches it? If nxt2[pos] = 2n then pos_new = 2n >= s+n ✓ fail. Good.

Simulation cost: O(n*k). With early break when fail.

Alternatively, we can accelerate: precompute jump pointers via binary lifting? Overkill; k=25.

Binary search: lo = 1 (always feasible? need k distinct points, pairwise distance >= 1: distinct integer points have distance >= 1, so any k-subset works; k <= n given). hi = L // k. Invariant: lo feasible, hi maybe infeasible. Standard: while lo < hi: mid = (lo + hi + 1)//2; if feasible(mid): lo = mid else hi = mid - 1. Return lo.

Check hi >= lo: L//k >= L/n; n <= 4*side = L so L//k >= 1 since k <= n <= L. ✓.

Let me sanity check with examples.

Example 1: side=2, points corners, k=4. t: (0,2)→ y==side → 6-0=6; (2,0)→2; (2,2)→ x==side → 4; (0,0)→0. Sorted: 0,2,4,6. L=8, hi=2. feasible(2): start 0: nxt: t>=2 →2, t>=4→4, t>=6→6; wrap: 0+8-6=2>=2 ✓. Answer 2. ✓

Example 2: side=2, points [[0,0],[1,2],[2,0],[2,2],[2,1]], k=4. t: 0, (1,2)→6-1=5, 2, 4, (2,1)→3. Sorted: 0,2,3,4,5. L=8, hi=2. feasible(2)? start 0: next >=2: 2; >=4: 4; >=6: none within < 0+5=5 indices... t2 = [0,2,3,4,5,8,10,11,12,13]. start s=0: pos0=0(t=0); nxt: first j with t2[j]>=2 → j=1 (t=2); then >=4 → j=3 (t=4); then >=6 → j=5 (t=8) but s+n=5, j=5 >= 5 → fail. s=1 (t=2): >=4 → t=4 (j=3); >=6 → t=8 (j=5); >=10 → j=6 (t=10); s+n = 1+5=6, j=6>=6 fail. s=2 (t=3): >=5→t=5(j=4); >=7→t=8(j=5); >=10→t=10(j=6); s+n=7, j=6<7 ok; cnt=4; wrap: t[s]+L - t_last = 3+8-10=1 < 2 fail. s=3 (t=4): >=6→8(j5); >=10→10(j6); >=12→12(j8)? t2: indices: 0:0,1:2,2:3,3:4,4:5,5:8,6:10,7:11,8:12,9:13. From j6(t=10): >=12 → j8 (t=12); s+n=8, j8>=8 fail. s=4 (t=5): >=7→8(j5); >=10→10(j6); >=12→12(j8); s+n=9; j8<9 ok; wrap: 5+8-12=1<2 fail. So 2 infeasible → answer 1. ✓ (matches expected 1).

Example 3: side=2, k=5, points [[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]]. t: 0, (0,1)→8-1=7, (0,2)→6, 5, 2, 4, 3. Sorted: 0,2,3,4,5,6,7. n=7, L=8, hi = 8//5=1. So answer <= 1, and >= 1 → 1. ✓.

Great.

Complexity: O(log(L/k) * (n + n*k)) ≈ 32 * (15000 + 375000) ≈ 12.5M operations. Fine.

Potential pitfall: two-pointer nxt computation must be O(n) carefully; or just use bisect for each i: O(n log n) = 15000*14 = 210K per check, *32 = 6.7M — also fine and simpler. Then simulation O(nk) with array jumps. Let me just use bisect for building nxt (simpler, less bug-prone), or even skip nxt and bisect during simulation: O(n*k*log n) = 5.25M per check * 32 = 168M — too slow. So build nxt array first (O(n log n) via bisect or O(n) two-pointer), then O(nk) simulation.

Actually, we can reduce further: simulation from each start s does k-1 jumps; total n*(k-1) = 360K per check. Fine.

One more optimization for the simulation: if chain from s visits positions, and we fail, we could skip, but not needed.

Let me also double-check the greedy correctness more carefully, because the wrap condition matters. Claim: d is feasible iff exists start s such that greedy chain c_0=s, c_{i+1}=nxt(c_i) reaches k points with all positions < s+n and t2[c_{k-1}] + d <= t2[s] + L.

Proof: (⇒) Suppose feasible set S with points at positions p_0 < p_1 < ... < p_{k-1} (in doubled array, choose p_0 = some point of S, others the next ones clockwise, all < p_0 + n, and wrap gap t2[p_0] + L - t2[p_{k-1}] >= d). Greedy from s=p_0: c_0 = p_0. Inductively, c_i <= p_i: c_1 = nxt[p_0] is the smallest index > p_0 with t >= t[p_0]+d; p_1 qualifies (gap >= d), so c_1 <= p_1. Then c_2 = nxt[c_1]: p_2 has t[p_2] >= t[p_1] + d >= t[c_1] + d, and p_2 > p_1 >= c_1, so c_2 <= p_2. Etc. So c_{k-1} <= p_{k-1} < p_0 + n, and wrap: t[c_{k-1}] + d <= t[p_{k-1}] + d <= t[p_0] + L. ✓. (⇐) greedy chain itself is a valid selection (indices mod n distinct since positions < s+n). ✓.

Good.

Also confirm answer lower bound: lo=1 always feasible as argued (any k distinct points, pairwise Manhattan >= 1 since distinct integer coordinates; and in arc model, distinct t's differ by >= 1? t values are integers, distinct, but circular gap could be... t distinct integers in [0, L), consecutive differ >= 1, wrap gap = L - (max-min) >= 1 since max-min <= L-1. So yes any k points have all gaps >= 1, d=1 feasible). ✓.

Now, the response format: I'm the FIRST WORKER, must respond with ### NOTES and ### NEXT. The user message already includes a PLAN (the perimeter approach). My job: analyze, note pitfalls. The critical pitfall I found: Manhattan ≠ perimeter arc in general, BUT the reduction is saved by k >= 4 ensuring answer <= side, under which the two metrics' threshold graphs coincide. This is a subtle but crucial correctness point that the plan glosses over. I should document this, plus implementation details and complexity.

Let me write concise but complete notes.

Also mention alternative: since k <= 25 small, could also consider DP/other, but binary search + greedy is the way.

Pitfalls list:
1. Manhattan ≠ arc in general (counterexample (0,1)-(2,1) side 2: 2 vs 4); reduction valid only because k>=4 → answer <= L/k <= side, and for d <= side, "Manhattan < d" ⟺ "arc < d" (verify per edge-pair case). Must cap binary search hi = L//k (<= side) — this is both an upper bound on the answer and keeps us in the regime where the models agree.
2. Corner mapping consistency (each corner satisfies two edge conditions; use if/elif chain).
3. Greedy needs wrap-around gap check and trying all starts.
4. Use doubled array; indices < s+n to avoid reselecting.
5. Integer binary search boundaries: lo=1 feasible always; hi=L//k.
6. Complexity: build nxt with two pointers O(n) or bisect O(n log n) per check; simulate O(nk).

NEXT tasks: implement mapping, feasibility with doubled array + nxt + greedy per start, binary search; test on examples plus edge cases (points only on one edge? possible — points just need boundary; e.g., all on bottom edge: then it's 1D line problem, greedy still works on circle; d > side cases never reached since hi <= side... wait if all points on one edge, answer could be up to side/(k-1) roughly, still <= side fine).

Let me also double check hi = L//k >= 1: k <= n <= min(4*side, 15000), L = 4*side >= n >= k, so L//k >= 1. ✓.

Write the response now. Format: exactly ### NOTES then ### NEXT with bullets.

## worker: Implement mapping from (x, y) to perimeter coordin
- **Mapping** (clockwise from (0,0), exactly as specified): bottom `t=x`; right `t=side+y`; top `t=2*side+(side-x)`; left `t=3*side+(side-y)`. The if/elif chain assigns each corner to exactly one edge: (0,0)→0, (side,0)→side, (side,side)→2·side, (0,side)→3·side. The map is injective on the boundary, so all `t` are distinct.
- **Critical correctness subtlety**: Manhattan distance does **NOT** equal circular arc distance in general. Counterexample: side=2, points (0,1) and (2,1): Manhattan = 2, but shorter boundary arc = 4. The reduction is saved by the constraint **k ≥ 4**:
  - For any k-subset, min Manhattan ≤ min arc ≤ L/k (k circular gaps sum to L). With k ≥ 4, the answer is ≤ L/4 = side.
  - For any threshold d ≤ side, the conflict relations coincide: `Manhattan(p,q) < d ⟺ arc(p,q) < d`. Proof by edge-pair case analysis:
    - Same edge: Manhattan = arc (straight along the edge).
    - Adjacent edges (share corner c): Manhattan = dist(p,c)+dist(c,q) ≤ 2·side = L/2, so shorter arc = that same value.
    - Opposite edges: Manhattan = side + |Δcoord| ≥ side ≥ d, and arc ≥ Manhattan (e.g., bottom-top: arc = side + min(x1+x2, 2·side−x1−x2) ≥ side + |x1−x2| = Manhattan), so neither side conflicts.
  - Hence for all d ≤ side, feasibility is identical in both metrics; since the arc-model answer ≤ side, the two maximin answers are equal. (A k=2 counterexample exists — side=4, points (0,2),(4,2): true answer 4, arc answer 8 — but k ≥ 4 is guaranteed.)
- **Feasibility check** (standard circular greedy): for candidate d, build successor array `nxt[i]` = first index j>i with `t2[j] ≥ t2[i]+d` via two pointers in O(n) on the doubled array. For each start s, follow k−1 successor jumps; fail if an index ≥ s+n (reselected a point) or if the wrap gap `t2[s]+L−t2[pos] < d`. Correctness: if any feasible set exists, greedy started at its first point picks each subsequent point no later (exchange argument), so it succeeds.
- **Binary search**: lo=1 (always feasible: distinct integer points have pairwise distance ≥ 1), hi=L//k (pigeonhole upper bound, and ≤ side which keeps us in the valid regime). ~32 iterations.
- **Complexity**: O(n + n·k) per check ≈ 15000 + 375000 ops; ×32 iterations ≈ 12.5M — fast in Python. Verified against all three examples (2, 1, 1).

## worker: Validate the solution against the three provided e
I validated the solution mentally and via hand-computation against the three provided examples and the targeted edge cases:

**Provided examples**
- Ex1 (side=2, 4 corners, k=4): t = [0,2,4,6], L=8, hi=2. feasible(2): start 0 → chain 0,2,4,6, wrap gap 8−6=2 ≥ 2 ✓. Returns 2. ✓
- Ex2 (side=2, k=4): t sorted = [0,2,3,4,5], hi=2. feasible(2) fails for all 5 starts (traced each: chains either hit index ≥ s+n or wrap gap = 1 < 2). feasible(1) trivially passes. Returns 1. ✓
- Ex3 (side=2, k=5, n=7): hi = 8//5 = 1, so answer forced to 1. Returns 1. ✓

**Targeted edge cases**
- All points on one edge (e.g., side=10, points (0,0),(3,0),(6,0),(9,0), k=4): t=[0,3,6,9], hi=40//4=10. feasible(3): start 0 → 0,3,6,9, wrap = 40−9=31 ≥ 3 ✓; feasible(4): best chain 0,?,... gaps of 3 < 4 fail for all starts (wrap check also fails). Answer 3 — correct, since on a line the maximin spacing of {0,3,6,9} is 3.
- k = n (must select all): e.g., side=4, points (0,2),(4,2),(2,0),(2,4), k=4: t=[2,6,10,14], gaps all 4, hi=16//4=4, feasible(4) ✓ (wrap = 16−14+2=4). Answer 4 = true min Manhattan (all pairs = 4). ✓
- side = 1: boundary lattice points are only the 4 corners, so n=4, k=4, L=4, hi=1. t=[0,1,2,3], feasible(1) ✓. Answer 1 = true min Manhattan between adjacent corners. ✓ (hi = 4//4 = 1 ≥ 1 holds.)
- Clustered points, answer 1: covered by Ex2/Ex3; any k distinct integer points give d=1 feasible since distinct sorted integer t's have all gaps ≥ 1 and wrap gap = L − (max−min) ≥ 1.
- d near side, opposite-edge pairs: side=10, points (0,5),(10,5),(5,0),(5,10), k=4: t=[5,15,25,35], hi=40//4=10. feasible(10): start 5 → 5,15,25,35, wrap = 40−35+5=10 ✓. Answer 10. True Manhattan: all 6 pairs = 10 (including the opposite-edge pair (0,5)-(10,5) with Manhattan 10 but arc 20 — the arc model's inflation never matters because d=10 ≤ side and the other pairs cap the answer). ✓ This confirms the k≥4 regime argument: hi = L//k ≤ side, and for d ≤ side the conflict relations coincide.

**Upper bound check**: hi = L//k ≥ 1 because k ≤ n ≤ 4·side = L (constraint n ≤ min(4·side, 15000)). hi ≤ side because k ≥ 4 ⇒ L//k = 4·side//k ≤ side. Both bounds confirmed; lo=1 ≤ hi always, so binary search is well-defined.

**Complexity**: per feasible() call O(2n) two-pointer + O(n·k) simulation ≈ 15000·25 = 375K ops; ≤ 32 binary-search iterations ⇒ ~12M ops total, well within limits.

The code is unchanged from the current work — it is correct as written.

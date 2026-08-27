
## ideation
We need to count monotone (right/up) lattice paths of any length (including single points) on the rectangle [0,W]×[0,H] with the closed rectangular hole L≤x≤R, D≤y≤U removed. Total over all start/end pairs (s,t), s≤t coordinatewise, both allowed, of the number of monotone paths from s to t that avoid the hole.

Core difficulty: the hole forces paths to route either below-then-right of the hole, or left-then-above it. A monotone path from s to t passes through the hole region only if s is "southwest" of the hole (x≤R, y≤U with the path entering) and t is "northeast". Standard trick: paths from s to t avoiding the hole = total paths − paths through hole. Paths through the hole can be decomposed via the first hole point hit, or via inclusion-exclusion using the hole's corners: number of monotone paths from s to t hitting the forbidden rectangle equals paths through corner decomposition: paths s→(L..R, D..U) region. A clean known approach for this AtCoder problem (typical "Kyoto" problem): answer = sum over all pairs of C(dx+dy, dx) minus pairs whose rectangle path passes through the hole, where the "bad" count can be computed by splitting at the hole boundary: any bad path crosses from region x<L or y<D into region x>R or y>U through the hole... Actually a monotone path from s to t intersects the hole iff s.x ≤ R, s.y ≤ U, t.x ≥ L, t.y ≥ D, and the path enters the rectangle. Equivalent: paths from s to t that pass through at least one hole point. Using the standard decomposition: bad paths = paths that go through the hole = (paths from s to any point on the hole's bottom/left entry edges staying outside) × ... This gets complicated; alternative: count directly by classifying paths into: (1) paths entirely in the "SW-feasible" region that never cross both barriers, (2) paths going around the hole via the bottom-right corridor (pass below hole then right of it), (3) via the top-left corridor. A path can use at most one of the two corridors (monotone). So total = paths avoiding the "NE of hole" conflict = sum over pairs where NOT(s.x≤R and s.y≤U and t.x≥L and t.y≥D) of C(dx+dy,dx), plus for the conflicting pairs, paths that route around: those must pass through either the segment {(x, D-1)→(R+1... )} hmm — a path from SW to NE avoiding the hole must at some point be either at y<D while x crosses from ≤R to >R... precisely it must contain an edge crossing the line x=R+0.5 at y<D, or an edge crossing y=U+0.5 at x<L. These two events are disjoint. So bad-avoiding count = sum over crossing edges. This suggests an O((W+H)) convolution approach: for each edge e = (R, y)→(R+1, y) with y<D, count pairs (s,t) with s ≤ (R,y), t ≥ (R+1,y), s,t allowed, summed paths s→(R,y) × paths (R+1,y)→t. Similarly for edges (x, U)→(x, U+1) with x<L. Plus all pairs not in conflict. Each of these is a 2D prefix-sum of binomial coefficients, computable via precomputed factorials and 2D prefix sums over the grid? Grid is up to 1e6×1e6 — too big for 2D arrays. Need closed-form sums: sum over s in a rectangle of C((a-s.x)+(b-s.y), a-s.x) has hockey-stick-like closed forms. Indeed sum over s.x≤a, s.y≤b of C((a-s.x)+(b-s.y), ...) = C(a+b+2, a+1) style identities (number of paths from any point in rectangle to (a,b) equals paths from (-1,-1)-ish... known identity: Σ_{i=0..a} Σ_{j=0..b} C(i+j, i) = C(a+b+2, a+1) − 1). So many terms reduce to O(1) binomial evaluations. The plan: derive answer = Σ over allowed pairs C(dx+dy,dx) − Σ over conflicting pairs (paths through hole). And paths through hole from s to t: by the entry-point argument, paths through hole = total − around-bottom − around-top where around-bottom paths cross some edge (R,y)→(R+1,y), y<D... but careful: a path from s (SW region) to t (NE region) avoiding hole crosses exactly one of those edge sets; summing over edges with product of path counts works because each path crosses exactly one such edge. So answer = Σ_{all allowed pairs, not conflicting} C + Σ_{conflicting pairs} [Σ_{bottom edges} + Σ_{top edges} products]. The first term: total over all allowed pairs minus conflicting pairs' totals. Conflicting pairs: s in [0,R]×[0,U] allowed (i.e., s.x<L or s.y<D), t in [L,W]×[D,H] allowed (t.x>R or t.y>U). Hmm, but also s must be ≤ t coordinatewise for any path to exist; if s.x≤R and t.x≥L etc. it's automatic? Not quite: conflict condition for hole passage possibility is s.x ≤ R, s.y ≤ U, t.x ≥ L, t.y ≥ D AND s ≤ t. If s.x ≤ R and t.x ≥ L but s.x > t.x possible (e.g., s.x=R, t.x=L with L<R). Then no path. So need care.

Pitfalls: (1) double counting paths that could cross both edge sets — impossible for monotone paths, but must verify: crossing bottom edge set requires y<D at x=R+1; crossing top edge set requires x<L at y=U+1; a monotone path could do both? To cross x=R+0.5 at y<D and y=U+0.5 at x<L: after crossing x=R+1 at y<D, x≥R+1≥L forever, so cannot later cross y=U+0.5 at x<L. Before crossing, y<D≤U so cannot have crossed y=U+0.5 earlier. Disjoint. Good. (2) Single-point paths (length 0) count = number of blocks; included in Σ pairs with s=t, C(0,0)=1. (3) The "not conflicting" total must be computed with rectangle-sum identities with careful bounds, many cases — error-prone. Alternative cleaner formulation: answer = Σ over all monotone paths = Σ over paths classified by their relation to hole. Maybe simpler: total paths in full grid minus paths that use at least one hole point. Paths using a hole point: decompose by first hole point? Or: paths whose vertex set intersects hole = Σ over pairs s≤t, paths s→t hitting hole. Hitting-hole paths from s to t: nonzero only if s SW-ish and t NE-ish. Count = total(s,t) − around(s,t) where around = bottom-route + top-route as above. Then answer = Σ_{s,t allowed} total(s,t) − Σ_{conflicting} [total − bottom − top]. Equivalently answer = Σ_{s,t} total − Σ_{conflicting} total + Σ bottom-route + Σ top-route, where the first Σ is over allowed pairs with s≤t.

Each piece is a sum of binomials over rectangles/products of sums, all reducible to O(1) binomial computations via the identity S(a,b) = Σ_{i=0}^{a}Σ_{j=0}^{b} C(i+j,i) = C(a+b+2, a+1) − 1, and product-convolution sums like Σ_{y=0}^{D-1} [Σ_{s≤(R,y)} paths] × [Σ_{t≥(R+1,y)} paths] where the inner sums are S-type and the outer sum over y of products of two binomials in y — that's a 1D convolution sum: Σ_y C(y + c1, k1) · C((D-1-y) + c2, k2)-type, which has closed form via Vandermonde: Σ_y C(y+a, m) C(b−y, n) = C(a+b+1, m+n+1)-type identities. So everything O(1) with factorials up to 2e6+something. Need to derive carefully.

Let me define: paths from s to t: C(dx+dy, dx), dx=t.x−s.x, dy=t.y−s.y ≥ 0.

Term A = Σ over allowed s, allowed t, s≤t of C(dx+dy,dx). Equivalent: total over all pairs in full rectangle minus pairs where s in hole or t in hole. Full rectangle total: Σ_{s≤t} C = Σ_{dx,dy} (W−dx+1)(H−dy+1) C(dx+dy,dx). Subtract pairs with s in hole (t any ≥ s within grid), and t in hole (s any ≤ t), add back both in hole. Each is a sum over an anchor point in the hole times rectangle sums — computable with S-identity and its weighted variants? Σ_{s in hole} Σ_{t≥s} C(dx+dy,dx) = Σ_{s in hole} [S(W−s.x, H−s.y) + 1]... S(a,b) = Σ_{i=0..a, j=0..b} C(i+j,i) − includes (0,0). Σ_{t≥s} C = S(W−s.x, H−s.y) where S includes the t=s term. Then Σ over s in hole of S(W−s.x, H−s.y) = Σ C(W−s.x+H−s.y+2, W−s.x+1) − 1 over hole — a 2D sum of binomial over rectangle, which again has closed form: Σ_{i=p..q, j=r..s} C(i+j+2, i+1)? Substituting i=W−s.x etc., it's Σ over rectangle of C(i+j+2, i+1), and Σ_{i=0..a,j=0..b} C(i+j+2, i+1) = C(a+b+4, a+2) − (b+1) − (a+1) − 1? There's an identity: Σ_{i,j} C(i+j+k, i+k') reduces to single binomial plus lower-order corrections. Doable but messy with rectangle offsets; use inclusion-exclusion with prefix function F(a,b) = Σ_{i=0..a}Σ_{j=0..b} C(i+j+2, i+1). Need closed form for F. C(i+j+2, i+1) = C(i+j+2, j+1). Σ_{i=0..a} C(i+j+2, j+1) = C(a+j+3, j+2) − C(j+2, j+2)?? Hockey stick: Σ_{i=0..a} C((j+2)+i, j+1) = C(j+3+a, j+2) − C(j+2, j+2) = C(a+j+3, j+2) − 1. Then Σ_{j=0..b} [C(a+j+3, j+2) − 1] = Σ_j C((a+3)+j − ... hmm C(a+j+3, j+2) = C(a+j+3, a+1). Σ_{j=0..b} C(a+1 + (j+2)... let me write C(a+j+3, a+1): Σ_{j=0..b} C((a+1)+(j+2), a+1) = Σ_{k=a+3}^{a+b+3} C(k, a+1) = C(a+b+4, a+2) − C(a+3, a+2) = C(a+b+4, a+2) − (a+3). So F(a,b) = C(a+b+4, a+2) − (a+3) − (b+1). Check small: a=b=0: F = C(0+0+2, 1) = 2. Formula: C(4,2) − 3 − 1 = 6−4 = 2. ✓.

So with a few such identities everything reduces to O(1) binomials. The conflicting-pair total and route sums similarly decompose. This is very fiddly; many cases. Must be extremely careful with bounds and off-by-ones.

Alternative simpler mental model: answer = Σ over all "gaps"/edges? Another known solution approach for this exact AtCoder problem (ABC/ARC? — it's from AGC? "Snuke" Kyoto — likely ARC111 or similar... Actually this is AtCoder "Ex - Directed Substring"? no. It's likely typical: answer = (paths in whole grid) − (paths passing through hole), and paths passing through hole counted by entry edge into hole: a path enters the hole through bottom edge (y=D−1→D, L≤x≤R) or left edge (x=L−1→L, D≤y≤U), first entry unique. Count paths by (start, entry point, exit...) — paths through hole = Σ over entry edge e and over start s ≤ e.tail, end t ≥ e.head with t allowed... but the path after entering may wander inside hole and exit; counting via entry edge: paths s→entry avoiding hole before, then any path from entry to t (which may stay in hole or exit — but once inside, monotone path to t with t outside NE is fine and automatically avoids re-entry issues; but t could be such that path exits and... any monotone path from entry point to t stays within x≥L... it could go below? No, y only increases, entry at y≥D, so stays y≥D; x≥ entry.x ≥ L; so it stays in the column strip; if t is right of hole, path crosses x=R+0.5 at some y≥D — fine, allowed region for x>R any y. So all continuations valid!). And paths from s to entry tail avoiding hole: s with s ≤ (x, D−1) (bottom entry): any monotone path to (x, D−1) has y ≤ D−1 < D, so never in hole — automatically valid! Similarly left entry (L−1, y): x ≤ L−1 < L always valid. So paths through hole = Σ_{x=L..R} Σ_{s ≤ (x,D−1)} Σ_{t ≥ (x,D)} C(s→(x,D−1)) · C((x,D)→t) + Σ_{y=D..U} Σ_{s ≤ (L−1,y)} Σ_{t ≥ (L,y)} C(s→(L−1,y)) · C((L,y)→t). Wait but entry edge decomposition: each path through hole has a unique first hole vertex; the edge into it comes from below (from (x, D−1) to (x,D), requiring first hole vertex has y=D) or from the left (from (L−1,y) to (L,y), first hole vertex at x=L, y>D? if y=D it could come from below or left — assign: first hole vertex (x,y): if y=D and x=L, edge could be from left or below; uniqueness: classify by the edge taken into the first hole vertex: it's either from (x, y−1) with y=D (from below, since y−1=D−1<D means outside) — but if x=L, (x, y−1)=(L, D−1) is outside hole (y<D) ✓; or from (x−1, y) with x=L. For first hole vertex (L, D), the entering edge is from (L−1, D) or (L, D−1) — both outside; a path has exactly one entering edge, so summing over edges (not vertices) keeps uniqueness: edges into hole from outside are exactly: bottom edges (x, D−1)→(x, D) for L≤x≤R, and left edges (L−1, y)→(L, y) for D≤y≤U. Each path through the hole uses exactly one such edge (the first time it enters). 

So: Answer = T_total − T_hole, where T_total = Σ_{s≤t, both allowed} C(s→t)... wait no! T_total should be over allowed endpoints only, and T_hole = paths (with allowed endpoints) that pass through hole. But in the entry-edge sum, s ranges over allowed points ≤ tail: any s ≤ (x, D−1) has y ≤ D−1 < D hence allowed automatically. Similarly s ≤ (L−1, y) allowed automatically. And t ≥ (x, D): t must be allowed: t ≥ (x,D) with x≤R: t in hole if t.x ≤ R and t.y ≤ U. So restrict t to allowed: t.x > R or t.y > U. Hmm, but the continuation path from (x,D) to t: if t is in the hole, endpoint not allowed — exclude. So T_hole = Σ_{entry edges} A(tail) · B(head) where A(p) = Σ_{s≤p} C(s→p) = S(p.x, p.y) (with s ranging over all lattice points ≥ (0,0) — all allowed as shown), and B(p) = Σ_{t ≥ p, t allowed} C(p→t). For head p=(x, D): B = Σ_{t≥p} C − Σ_{t≥p, t in hole} C = S(W−x, H−D) − Σ_{t: x≤t.x≤R... wait t≥p means t.x≥x, t.y≥D; hole condition t.x≤R, t.y≤U, and t.x≥L automatically since t.x≥x≥L. So subtract Σ_{t.x=x..R, t.y=D..U} C((t.x−x)+(t.y−D), t.x−x) = S(R−x, U−D). So B((x,D)) = S(W−x, H−D) − S(R−x, U−D). Similarly for head (L, y): B = S(W−L, H−y) − S(R−L, U−y).

And A((x, D−1)) = S(x, D−1) = C(x+D+1, x+1) − 1. A((L−1, y)) = S(L−1, y) = C(L+y+1, L) − 1.

Then T_hole = Σ_{x=L}^{R} [C(x+D+1, x+1) − 1] · [S(W−x, H−D) − S(R−x, U−D)] + Σ_{y=D}^{U} [C(L+y+1, L) − 1] · [S(W−L, H−y) − S(R−L, U−y)].

These are 1D sums of products of binomials — need closed forms. S(a,b) = C(a+b+2, a+1) − 1. So terms like [C(x+D+1, x+1) − 1]·[C(W−x+H−D+2, W−x+1) − 1 − C(R−x+U−D+2, R−x+1) + 1]. Products of two binomials summed over x: Σ_x C(x + a, p) · C(b − x, q) — Vandermonde gives C(a+b+1, p+q+1) if the sum ranges over all valid x; with restricted range L..R it's a partial Vandermonde — no simple closed form in general! Hmm. That's a problem. Σ_{x=L}^{R} C(x+D+1, D) · C(W−x+H−D+2, H−D+1): let u = x+D+1; terms C(u, D)·C((W+H−D+2+D+1) − u − ... , ...) — partial sum over u in an interval. Partial Vandermonde doesn't simplify. So T_hole as stated needs O(R−L + U−D) = O(1e6) evaluation — that's fine! O(W+H) with precomputed factorials is totally fine (constraints 1e6). We don't need closed forms, just O(N) per term with O(1) binomial each. 

So the algorithm: precompute factorials/inv factorials up to 2e6+10 (max n: W+H+4 ≤ 2e6+4; also arguments like x+D+1 ≤ W+H+1 fine). Compute:
- T_total = Σ over allowed endpoint pairs. Compute as: (all pairs in full grid) − (s in hole) − (t in hole) + (both in hole). Where "pairs" means s≤t and count C(s→t).
  - All pairs: G(W,H) = Σ_{dx=0..W} Σ_{dy=0..H} (W−dx+1)(H−dy+1) C(dx+dy, dx). Closed form? Σ over s,t = Σ_s S(W−s.x, H−s.y) = Σ_{i=0..W}Σ_{j=0..H} S(i,j) where S(i,j) = C(i+j+2, i+1) − 1. Σ_{i,j} C(i+j+2, i+1) = F(W,H) = C(W+H+4, W+2) − (W+3) − (H+1) (derived above). Then G = F(W,H) − (W+1)(H+1). Let me double check F derivation later. Alternatively just compute G via O(W) sum: fix dx, inner over dy: Σ_{dy} (H−dy+1) C(dx+dy, dx) — has closed form C(dx+H+2, dx+... ) — Σ_{dy=0..H} (H+1−dy) C(dx+dy, dy). Σ_{dy=0..H} C(dx+dy, dx) = C(dx+H+1, dx+1). Σ_{dy} dy·C(dx+dy, dx) = ? Identity: Σ_{dy=0..H} dy C(dx+dy, dy) = (dx+1)·C(dx+H+1, dx+2)? Something like that. Could just do O(W+H) loops with O(1) each — simplest: iterate dx 0..W, maintain running sums? Each term needs C(dx+dy, dx) for all dy — O(W·H) too big. Use closed forms or O(W) with recurrence. Easiest: G = Σ_s S(W−s.x, H−s.y), and use F-identity for 2D sum of binomial — verify F carefully, then G is O(1). Similarly s-in-hole sum = Σ_{s in hole} S(W−s.x, H−s.y) = Σ_{i=L..R, j=D..U} [C((W−i)+(H−j)+2, W−i+1) − 1] = rectangle sum of C((W+H+2) − (i+j), W−i+1). Substitute a = W−i (ranges W−R..W−L), b = H−j (H−U..H−D): Σ C(a+b+2, a+1) over rectangle = F(W−L, H−D) − F(W−R−1, H−D) − F(W−L, H−U−1) + F(W−R−1, H−U−1) with F(a,b) = Σ_{i=0..a}Σ_{j=0..b} C(i+j+2, i+1) = C(a+b+4, a+2) − (a+3) − (b+1) (to verify). Minus count of hole points (R−L+1)(U−D+1) for the "−1" in S. Similarly t-in-hole: Σ_{t in hole} S(t.x, t.y) (paths from any s≤t to t; s automatically... wait s must be allowed! If t in hole and s≤t, s could also be in hole — but that's the inclusion-exclusion: pairs where t in hole regardless of s. Fine, s ranges over all ≤t: S(t.x, t.y).) = Σ_{i=L..R, j=D..U} [C(i+j+2, i+1) − 1] = [F(R,U) − F(L−1,U) − F(R,D−1) + F(L−1,D−1)] − (R−L+1)(U−D+1). Both-in-hole: Σ_{s,t in hole, s≤t} C = G(R−L, U−D) (translation-invariant). 

  So T_total = G(W,H) − HoleSumS − HoleSumT + G(R−L, U−D), where HoleSumS = Σ_{s∈hole} S(W−s.x, H−s.y), HoleSumT = Σ_{t∈hole} S(t.x, t.y).

  Wait — careful: "all pairs in full grid" includes pairs where s or t in hole; subtracting s∈hole (all t≥s) and t∈hole (all s≤t) and adding back both-in-hole pairs counted twice. But pairs where s∈hole, t≥s with t also... inclusion-exclusion on the set of pairs: allowed pairs = all − (s∈hole) − (t∈hole) + (s∈hole ∧ t∈hole). ✓.

- T_hole = Σ_{x=L}^{R} A1(x)·B1(x) + Σ_{y=D}^{U} A2(y)·B2(y) with:
  - A1(x) = S(x, D−1) = C(x+D+1, x+1) − 1 (if D=0, no bottom edges; skip — S(x, −1)=0; handle by skipping when D==0).
  - B1(x) = S(W−x, H−D) − S(R−x, U−D) = [C(W−x+H−D+2, W−x+1) − 1] − [C(R−x+U−D+2, R−x+1) − 1] = C(W−x+H−D+2, W−x+1) − C(R−x+U−D+2, R−x+1). Note when x=R... fine. Edge case: if D>H? no, D≤U≤H. If D=H? then head (x, D) has H−D=0 fine.
  - A2(y) = S(L−1, y) = C(L+y+1, L) − 1 (skip if L=0).
  - B2(y) = S(W−L, H−y) − S(R−L, U−y) = C(W−L+H−y+2, W−L+1) − C(R−L+U−y+2, R−L+1).
  
  Wait B2: t ≥ (L, y), t allowed: subtract t in hole: t.x ∈ [L, R], t.y ∈ [y, U]: Σ C((t.x−L)+(t.y−y), t.x−L) = S(R−L, U−y). ✓. And B1: t ≥ (x, D), subtract t.x∈[x,R], t.y∈[D,U]: S(R−x, U−D). ✓.

  Hmm wait, but there's subtlety in T_hole: the continuation from head to t might pass... it's fine as argued. But also: does the path from s to tail possibly already... s ≤ tail=(x, D−1): path stays y ≤ D−1, never enters hole ✓. For left edges: s ≤ (L−1, y): x ≤ L−1 ✓.

  But hold on: is it true that every path from allowed s to allowed t that passes through the hole has s ≤ some entry tail and the entry edge decomposition counts each such path exactly once? Yes: first hole vertex, the edge used to reach it is unique and is one of the listed edges. ✓.

  Also T_hole counts paths whose endpoints are allowed and which visit ≥1 hole point. Answer = T_total − T_hole. 

Complexity: O(R−L + U−D) binomial evaluations = O(1e6), fine. Factorials up to max n: W+H+4 (for G) and x+D+1 ≤ W+H+1, W−x+H−D+2 ≤ W+H+2, etc. Max is W+H+4 ≤ 2·10^6+4. Precompute up to 2e6+10.

Now verify F identity: F(a,b) = Σ_{i=0}^{a} Σ_{j=0}^{b} C(i+j+2, i+1).
Inner: Σ_{i=0}^{a} C(i+j+2, i+1). Write C(i+j+2, j+1). Σ_{i=0}^{a} C((j+2)+i, j+1) = C(j+2+a+1, j+2) − C(j+2, j+2) [hockey stick: Σ_{i=0}^{a} C(r+i, r) with r=j+1... C(j+1+i, j+1)? But we have C(j+2+i, j+1) = C(j+2+i, i+1). Hmm hockey stick: Σ_{i=0}^{a} C(j+2+i, j+1) = Σ_{k=j+2}^{j+2+a} C(k, j+1) = C(j+a+3, j+2) − C(j+2, j+2) = C(a+j+3, j+2) − 1. ✓ (using Σ_{k=0}^{n} C(k, m) = C(n+1, m+1), subtract k<j+2 terms which are zero except... C(k, j+1)=0 for k<j+1, and k=j+1 term C(j+1, j+1)=1; so Σ_{k=j+2}^{j+2+a} C(k,j+1) = C(j+a+3, j+2) − C(j+2, j+2)·... let me just: Σ_{k=0}^{N} C(k, m) = C(N+1, m+1). Σ_{k=j+2}^{j+2+a} C(k, j+1) = C(j+a+3, j+2) − C(j+2, j+2) = C(a+j+3, j+2) − 1. ✓)
Outer: Σ_{j=0}^{b} [C(a+j+3, j+2) − 1] = Σ_{j=0}^{b} C(a+j+3, a+1) − (b+1) = [C(a+b+4, a+2) − C(a+3, a+2)] − (b+1) = C(a+b+4, a+2) − (a+3) − (b+1). ✓ (Σ_{j=0}^{b} C(a+3+j, a+1) = Σ_{k=a+3}^{a+3+b} C(k, a+1) = C(a+b+4, a+2) − C(a+3, a+2); C(a+3, a+2) = a+3.)
Check a=b=0: F = C(2,1)=2; formula C(4,2)−3−1 = 6−4=2 ✓. a=1,b=0: terms i=0..1,j=0: C(2,1)+C(3,2)=2+3=5; formula C(5,3)−4−1=10−5=5 ✓.

G(W,H) = Σ_{i=0..W}Σ_{j=0..H} S(i,j) where S(i,j) = C(i+j+2, i+1) − 1. So G = F(W,H) − (W+1)(H+1) = C(W+H+4, W+2) − (W+3) − (H+1) − (W+1)(H+1).
Sanity: W=H=0: single point, 1 path. G = C(4,2) − 3 − 1 − 1 = 6−5 = 1 ✓.
W=1,H=0: points (0,0),(1,0); paths: (0,0),(1,0),(0,0)→(1,0) = 3. G = C(5,3) − 4 − 1 − 2 = 10−7 = 3 ✓.

HoleSumS = Σ_{i=L..R, j=D..U} S(W−i, H−j) = Σ_{a=W−R..W−L, b=H−U..H−D} [C(a+b+2, a+1) − 1] = rectF(W−L, H−D) − rectF(W−R−1, H−D) − rectF(W−L, H−U−1) + rectF(W−R−1, H−U−1) − (R−L+1)(U−D+1), where rectF(a,b) = F(a,b) for a,b ≥ 0 else 0.

HoleSumT = Σ_{i=L..R, j=D..U} S(i, j) = [F(R,U) − F(L−1,U) − F(R,D−1) + F(L−1,D−1)] − (R−L+1)(U−D+1).

BothInHole = G(R−L, U−D).

T_hole sums: O(1e6) loop each. Note B1(x) when D=0: skip bottom edges entirely (no y=D−1). When L=0 skip left edges. Also note: if D=0 then bottom entry edges don't exist; left edges still exist if L>0. Also careful: what if the hole touches boundary such that head=(x,D) has B1 possibly... B1 formula fine.

Also note A1(x) = C(x+D+1, x+1) − 1 = C(x+D+1, D) − 1. B1(x) = C((W−x)+(H−D)+2, W−x+1) − C((R−x)+(U−D)+2, R−x+1).

Edge: R−x+U−D+2 choose R−x+1: when x=R: C(U−D+2, 1) = U−D+2; S(0, U−D) = C(U−D+2, 1) − 1 = U−D+1 ✓ (points along column).

Let me sanity check T_hole on a tiny example later via brute force in my head or trust derivation; better to plan a brute-force verification during development (but final code must not test samples — we just write the code; we can reason).

Wait, one more check on T_total: "all pairs in full grid" G(W,H) counts s≤t both in [0,W]×[0,H]. ✓.

Also the problem says at least one block exists. Mod 998244353.

Now sample 1: W=4,H=3,L=1,R=2,D=2,U=3. Hole: x∈{1,2}, y∈{2,3}. Let me compute answer via formula roughly? That's a lot; trust and verify with brute force mentally maybe small case instead: W=1,H=1,L=0,R=0,D=0,U=0: hole = {(0,0)}. Blocks: (1,0),(0,1),(1,1). Paths: 3 singletons + (1,0)→(1,1) + (0,1)→(1,1) = 5.
Formula: G(1,1) = C(6,3) − 4 − 2 − 4 = 20−10 = 10. HoleSumS: hole single point (0,0): S(W−0, H−0) = S(1,1) = C(4,2)−1 = 5. HoleSumT: S(0,0) = C(2,1)−1 = 1. BothInHole = G(0,0) = 1. T_total = 10 − 5 − 1 + 1 = 5. T_hole: bottom edges: D=0 → none. Left edges: L=0 → none. T_hole = 0. Answer 5 ✓. (Paths through hole impossible since hole point (0,0) can only be a start... wait (0,0) is in hole, not a block, so no path includes it. ✓)

Another check: W=2,H=2, hole L=1,R=1,D=1,U=1 (center point (1,1) removed). Blocks: 8 points. Total paths in full grid G(2,2) = C(8,4) − 5 − 3 − 9 = 70 − 17 = 53. HoleSumS = S(W−1, H−1) = S(1,1) = 5. HoleSumT = S(1,1) = 5. BothInHole = G(0,0) = 1. T_total = 53 − 5 − 5 + 1 = 44. T_hole: bottom edges: x=1: A1(1) = C(1+1+1, 1) − 1 = C(3,1)−1 = 2. B1(1) = C((1)+(1)+2, 2) − C(0+0+2, 1) = C(4,2) − C(2,1) = 6 − 2 = 4. Contribution 8. Left edges: y=1: A2(1) = C(1+1+1, 1) − 1 = 2. B2(1) = C(1+1+2, 2) − C(0+0+2,1) = 6−2 = 4. Contribution 8. T_hole = 16. Answer = 44 − 16 = 28.
Brute check: paths through hole point (1,1): s ≤ (1,1) allowed s: (0,0),(1,0),(0,1) (not (1,1)); t ≥ (1,1) allowed: (1,2),(2,1),(2,2). Paths through (1,1): Σ_{s} C(s→(1,1)) × Σ_{t} C((1,1)→t): s counts: (0,0):2, (1,0):1, (0,1):1 → 4. t counts: (1,2):1, (2,1):1, (2,2):2 → 4. Total 16 ✓. And answer 28: total allowed-endpoint pairs paths 44 minus 16 = 28. Plausible ✓.

Great, formula works on this sanity check.

Now also double-check T_total's "all pairs" includes pairs where path from s to t passes through hole — yes, T_total counts all monotone paths between allowed endpoints regardless of hole; then subtract T_hole. ✓.

Max factorial argument: W+H+4 ≤ 2,000,004. Also x+D+1 ≤ W+H+1 fine. Precompute fact/invfact up to 2_000_005 + safety.

Negative-argument guards: F(a,b) valid only a,b ≥ 0; define rectF returning 0 if a<0 or b<0. G(a,b) for a,b≥0. S(a,b) for a,b≥0; in T_hole, D≥1 for bottom (else skip), L≥1 for left (else skip).

Modulo handling for subtraction.

Complexity O(W+H+U−D+R−L) ~ 2e6+ precompute 2e6 → fine in Python? 2e6 factorial loop plus up to 1e6 term loop with a few modular multiplications each — Python might be ~2-4 seconds. AtCoder typical TL 2s... risky but likely OK in PyPy. Optimize: precompute fact and invfact arrays; each binomial = fact[n]*ifac[k]%M*ifac[n-k]%M — 3 lookups, 2 mults. Loop up to (R−L+1)+(U−D+1) ≤ 1e6+1e6? R−L ≤ 1e6, U−D ≤ 1e6, total ≤ 2e6 iterations × ~2 binomials each ≈ 4e6 binomial evaluations ≈ 12e6 mults — might be ~5-8s in Python. Hmm. Can optimize using recurrence: consecutive terms in x: A1(x) = C(x+D+1, D) − 1 — recurrence in x: multiply by (x+D+2)/(x+1)... modular division via precomputed inverses — still mults. Alternatively note we can compute each binomial with fact table; 2 mults each. Let's estimate: 2e6 iterations, each ~2 binomials = 6 array accesses + 4 mults + adds. Python ~50-100ns per simple op... realistically ~0.3µs per binomial → 2e6 × 2 × 0.3µs ≈ 1.2s. Plus factorial precompute 2e6 × 2 loops ≈ 1s. Total ~2.5-3s. Acceptable-ish; can micro-optimize with local variable binding. Alternatively reduce: B1(x) has two binomials, A1 one → 3 binomials per x. Still fine.

Actually we can halve: iterate and use multiplicative recurrence with precomputed modular inverses (inv array) — same cost roughly. Just write clean code with locals.

Let me now also double check the T_hole formula handles the case where head's B includes t values that are ≥ head but the path from head to t could go... already argued fine.

One more subtlety: In T_hole bottom edges, s ranges over ALL points ≤ tail (all allowed since y ≤ D−1). But wait, s must also satisfy x ≤ W etc. — yes s in grid. S(x, D−1) counts s ∈ [0,x]×[0,D−1]. ✓. Also need s itself allowed: y ≤ D−1 < D ✓ always allowed.

Also: are there paths through the hole whose start s is in the hole? No—s must be a block. Our T_hole only counts allowed s. ✓. And T_total − T_hole: T_total counts paths between allowed endpoints (including those through hole), T_hole subtracts exactly those passing through hole. ✓.

Now write the solution summary and code plan:

```
import sys
def main():
    W,H,L,R,D,U = map(int, sys.stdin.read().split())
    MOD = 998244353
    N = W + H + 5
    fact = [1]*(N+1); ...
    def C(n,k): return 0 if k<0 or k>n else fact[n]*ifac[k]%MOD*ifac[n-k]%MOD
    def S(a,b): # a,b>=0
        return (C(a+b+2, a+1) - 1) % MOD
    def F(a,b):
        if a<0 or b<0: return 0
        return (C(a+b+4, a+2) - (a+3) - (b+1)) % MOD
    def G(a,b):
        return (F(a,b) - (a+1)*(b+1)) % MOD
    hole_pts = (R-L+1)*(U-D+1) % MOD
    HoleSumS = (F(W-L, H-D) - F(W-R-1, H-D) - F(W-L, H-U-1) + F(W-R-1, H-U-1) - hole_pts) % MOD
    HoleSumT = (F(R, U) - F(L-1, U) - F(R, D-1) + F(L-1, D-1) - hole_pts) % MOD
    T_total = (G(W,H) - HoleSumS - HoleSumT + G(R-L, U-D)) % MOD
    T_hole = 0
    if D >= 1:
        for x in range(L, R+1):
            A1 = C(x+D+1, D) - 1
            B1 = (C(W-x+H-D+2, W-x+1) - C(R-x+U-D+2, R-x+1)) % MOD
            T_hole = (T_hole + A1 * B1) % MOD
    if L >= 1:
        for y in range(D, U+1):
            A2 = C(L+y+1, L) - 1
            B2 = (C(W-L+H-y+2, W-L+1) - C(R-L+U-y+2, R-L+1)) % MOD
            T_hole = (T_hole + A2 * B2) % MOD
    print((T_total - T_hole) % MOD)
```

Wait G(a,b) = F(a,b) − (a+1)(b+1): check G(0,0) = F(0,0) − 1 = 2−1 = 1 ✓.

Hmm wait, G = Σ_{i,j} S(i,j) = Σ [C(i+j+2,i+1) − 1] = F − (W+1)(H+1) ✓.

Double-check HoleSumS substitution: s=(i,j) ∈ [L,R]×[D,U]; a = W−i ∈ [W−R, W−L]; b = H−j ∈ [H−U, H−D]. Σ_{a=W−R}^{W−L} Σ_{b=H−U}^{H−D} C(a+b+2, a+1) = F(W−L, H−D) − F(W−R−1, H−D) − F(W−L, H−U−1) + F(W−R−1, H−U−1) ✓ (F is prefix over a,b from 0). Then minus hole_pts for the "−1" per point ✓.

HoleSumT = Σ_{i=L}^{R}Σ_{j=D}^{U} [C(i+j+2, i+1) − 1] = F(R,U) − F(L−1,U) − F(R,D−1) + F(L−1,D−1) − hole_pts ✓.

Check sample1 quickly? Tedious; trust the earlier verification + plan to mentally test more. Actually let me partially verify sample 1 with quick computations where feasible... maybe skip; the derivation was verified on two tiny cases.

One concern: T_hole bottom loop when D≥1 but also note if D−1 > H? impossible. If U=H, B1's second term C(R−x+U−D+2, R−x+1) still fine.

Also possible edge: W−x+1 could be... x ≤ R ≤ W so W−x ≥ 0 ✓. n = W−x+H−D+2 ≥ k ✓.

Factorial max n: C(a+b+4, ...) with a+b ≤ W+H → n ≤ W+H+4. Set N = W+H+4.

Now, is the answer for sample 1 = 192? Let me try to verify with a slightly different approach mentally... maybe compute T_total and T_hole for sample 1 numerically. W=4,H=3,L=1,R=2,D=2,U=3.

G(4,3) = F(4,3) − 5·4. F(4,3) = C(11,6) − 7 − 4 = 462 − 11 = 451. G = 451 − 20 = 431.
HoleSumS: F(W−L,H−D) = F(3,1) = C(8,5) − 6 − 2 = 56−8 = 48. F(W−R−1, H−D) = F(1,1) = C(6,3) − 4 − 2 = 20−6 = 14. F(W−L, H−U−1) = F(3, −1) = 0. F(1,−1) = 0. hole_pts = 2·2 = 4. HoleSumS = 48 − 14 − 4 = 30.
HoleSumT: F(R,U) = F(2,3) = C(9,4) − 5 − 4 = 126 − 9 = 117. F(L−1,U) = F(0,3) = C(7,2) − 3 − 4 = 21 − 7 = 14. F(R, D−1) = F(2,1) = C(7,4) − 5 − 2 = 35 − 7 = 28. F(L−1, D−1) = F(0,1) = C(5,2) − 3 − 2 = 10 − 5 = 5. HoleSumT = 117 − 14 − 28 + 5 − 4 = 76.
BothInHole = G(1,1) = F(1,1) − 4 = 14 − 4 = 10.
T_total = 431 − 30 − 76 + 10 = 335.

T_hole: D=2 ≥ 1. x from 1 to 2:
A1(x) = C(x+3, 2) − 1. x=1: C(4,2)−1 = 5. x=2: C(5,2)−1 = 9.
B1(x) = C(4−x+3−2+2, 4−x+1) − C(2−x+3−2+2, 2−x+1) = C(7−x, 5−x) − C(5−x, 3−x).
x=1: C(6,4) − C(4,2) = 15 − 6 = 9. x=2: C(5,3) − C(3,1) = 10 − 3 = 7.
Bottom contribution: 5·9 + 9·7 = 45 + 63 = 108.
L=1 ≥ 1. y from 2 to 3:
A2(y) = C(1+y+1, 1) − 1 = (y+2) − 1 = y+1. y=2: 3; y=3: 4.
B2(y) = C(4−1+3−y+2, 4−1+1) − C(2−1+3−y+2, 2−1+1) = C(8−y, 4) − C(6−y, 2).
y=2: C(6,4) − C(4,2) = 15 − 6 = 9. y=3: C(5,4) − C(3,2) = 5 − 3 = 2.
Left contribution: 3·9 + 4·2 = 27 + 8 = 35.
T_hole = 108 + 35 = 143.
Answer = 335 − 143 = 192 ✓✓ Matches sample 1!

Excellent. The formula is verified against sample 1.

Implementation considerations: precompute factorials up to N = W+H+4. Use list comprehensions / loops. For speed, bind locals in loops. Also handle mod-negatives with % MOD at the end of each expression.

Potential pitfalls recap:
- D=0 → skip bottom loop; L=0 → skip left loop.
- F with negative args → 0.
- G(R−L, U−D) fine (≥0).
- Large N arrays: N+1 up to 2,000,005 — two lists of ints ~ 32MB each in Python (int objects ~28 bytes → actually 2e6 Python ints ≈ 56MB each!). Memory concern: Python ints in list: each ~28 bytes + list pointer 8 bytes → ~72MB per list of 2e6. Two lists = 144MB. AtCoder Python memory limit usually 256MB (or 512MB). Should be OK but tight-ish. Could use array('I') or... values < 998244353 fit in 32-bit unsigned? 998244353 < 2^32 ✓. Use `array('I')` or `list` of ints — list of ints in CPython: small ints are objects; computed values are full objects ~28B each + 8B pointer = 36B × 2e6 × 2 arrays ≈ 144MB. Risky but typically accepted; many AtCoder Python solutions use list factorials of 2e6. Alternatively use a single fact array and compute inverse factorial via pow per query — too slow. Keep two lists; should fit in 256MB? 144MB + overhead — okay. Or use `array('q')`? Slower access maybe. I'll use lists; it's standard.

Actually, to be safe on speed, precompute inv (modular inverses) too? Not needed with invfact approach.

Time: factorial loop 2e6, invfact loop 2e6, main loops ≤ 2e6 with ~3 binomials (9 accesses, 6 mults). Total maybe 3-4s in CPython, ~1.5s in PyPy. AtCoder TL for this problem (it's AGC? Actually this is "HHKB2020"? no—it's likely typical 2s). Hmm. Could optimize the T_hole loops using recurrence relations to avoid binomial computations:

A1(x+1)/A1(x): C(x+D+2, D) = C(x+D+1, D) · (x+D+2)/(x+2). With precomputed inv array (O(N) precompute), each step 2 mults. B1 has two binomials each with recurrence: C(W−x+H−D+2, W−x+1) as x increases by 1: n decreases by 1, k decreases by 1: C(n−1, k−1) = C(n,k) · k / n. So 2 mults each. Total per iteration ~6 mults vs binomial approach 6 mults + more accesses. Roughly same. Just keep binomials via fact table — simpler, less error-prone. I'll write it straightforwardly with local variable optimization.

Alternatively, reduce constant: compute both loops with local references to fact, invf, MOD.

I think the solution is solid. Let me also double check B1 for x such that W−x+H−D+2 choose W−x+1: k = W−x+1 ≥ 1, n = k + (H−D+1) ≥ k ✓.

Also A1 = C(x+D+1, D) − 1: check S(x, D−1) = C(x + D−1 + 2, x+1) − 1 = C(x+D+1, x+1) − 1 = C(x+D+1, D) − 1 ✓.
A2 = S(L−1, y) = C(L−1+y+2, L) − 1 = C(L+y+1, L) − 1 ✓.
B2 = S(W−L, H−y) − S(R−L, U−y) = C(W−L+H−y+2, W−L+1) − C(R−L+U−y+2, R−L+1) ✓.

Everything checks. Now write final answer with code.

Also note: result of B1 could be negative before mod — apply % MOD. A1 − 1 could be... C ≥ 1 always so A1 ≥ 0; but mod fine.

Edge case: hole covers everything? "There is at least one block" guaranteed. If hole = whole grid... not possible then. Fine.

Edge: R−L, U−D could be 0 (hole is a line/point) — formulas still fine (verified with point-hole test above).

Let me also consider: T_hole when D≥1 but the bottom edge tail (x, D−1) — s ranges over [0,x]×[0,D−1]; all such s allowed ✓ regardless of L.

One more: in T_total, "all pairs" G(W,H) includes pairs s=t in hole etc. — handled by inclusion-exclusion ✓.

Write-up: explain derivation concisely, then code.

For the response format: provide explanation and the code block. The user asked to enclose code within delimiters as follows... they showed "PLAN:" — presumably they want the solution. I'll give a brief explanation and the Python code in a ```python block reading stdin writing stdout.

Final code:

```python
import sys

def main():
    MOD = 998244353
    W, H, L, R, D, U = map(int, sys.stdin.read().split())
    N = W + H + 4
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    invf = [1] * (N + 1)
    invf[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invf[i-1] = invf[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invf[k] % MOD * invf[n-k] % MOD

    def F(a, b):
        # sum_{i=0..a} sum_{j=0..b} C(i+j+2, i+1)
        if a < 0 or b < 0:
            return 0
        return (C(a+b+4, a+2) - (a+3) - (b+1)) % MOD

    def G(a, b):
        # sum over all pairs s<=t in [0,a]x[0,b] of path counts
        return (F(a, b) - (a+1) * (b+1)) % MOD

    hole = (R - L + 1) * (U - D + 1) % MOD
    sumS = (F(W-L, H-D) - F(W-R-1, H-D) - F(W-L, H-U-1) + F(W-R-1, H-U-1) - hole) % MOD
    sumT = (F(R, U) - F(L-1, U) - F(R, D-1) + F(L-1, D-1) - hole) % MOD
    total = (G(W, H) - sumS - sumT + G(R-L, U-D)) % MOD

    through = 0
    f = fact; iv = invf; M = MOD
    if D >= 1:
        for x in range(L, R+1):
            a1 = f[x+D+1] * iv[D] % M * iv[x+1] % M - 1
            b1 = (f[W-x+H-D+2] * iv[W-x+1] % M * iv[H-D+1] % M
                  - f[R-x+U-D+2] * iv[R-x+1] % M * iv[U-D+1] % M) % M
            through = (through + a1 * b1) % M
    if L >= 1:
        for y in range(D, U+1):
            a2 = f[L+y+1] * iv[L] % M * iv[y+1] % M - 1
            b2 = (f[W-L+H-y+2] * iv[W-L+1] % M * iv[H-y+1] % M
                  - f[R-L+U-y+2] * iv[R-L+1] % M * iv[U-y+1] % M) % M
            through = (through + a2 * b2) % M

    print((total - through) % MOD)

main()
```

Check C(R−x+U−D+2, R−x+1): n−k = U−D+1 ✓ matches invf[U−D+1]. C(W−x+H−D+2, W−x+1): n−k = H−D+1 ✓. C(x+D+1, D): n−k = x+1 ✓. C(L+y+1, L): n−k = y+1 ✓. C(W−L+H−y+2, W−L+1): n−k = H−y+1 ✓. C(R−L+U−y+2, R−L+1): n−k = U−y+1 ✓.

All indices ≤ W+H+4? W−x+H−D+2 ≤ W+H+2 ✓; x+D+1 ≤ W+H+1 ✓; a+b+4 ≤ W+H+4 ✓. Good.

I'm confident. Pro

## worker: Write the final solution: implement the derived O(
- **Model**: Count all monotone (right/up) paths of any length ≥ 0 on the grid [0,W]×[0,H] with the closed rectangular hole L≤x≤R, D≤y≤U removed. Answer = (paths between allowed endpoint pairs, hole ignored) − (paths that actually enter the hole).
- **Key identities** (verified by hand on small cases):
  - S(a,b) = Σ_{i≤a,j≤b} C(i+j, i) = C(a+b+2, a+1) − 1.
  - F(a,b) = Σ_{i≤a,j≤b} C(i+j+2, i+1) = C(a+b+4, a+2) − (a+3) − (b+1) (double hockey stick; checked F(0,0)=2, F(1,0)=5).
  - G(a,b) = total paths over all endpoint pairs in an (a+1)×(b+1) grid = F(a,b) − (a+1)(b+1) (checked G(0,0)=1, G(1,0)=3).
- **T_total** (allowed endpoints, hole ignored) by inclusion–exclusion: G(W,H) − Σ_{s∈hole} S(W−s.x, H−s.y) − Σ_{t∈hole} S(t.x, t.y) + G(R−L, U−D), where the hole sums are rectangle sums evaluated with F (prefix form, 0 for negative args).
- **T_hole**: every path entering the hole has a unique entry edge: a bottom edge (x,D−1)→(x,D), L≤x≤R, or a left edge (L−1,y)→(L,y), D≤y≤U. Starts s ≤ tail are automatically hole-free (y<D or x<L), so the start side is S(x, D−1) / S(L−1, y). The end side from the head allows any continuation but the endpoint must be a block: S(W−x, H−D) − S(R−x, U−D) (subtract endpoints inside the hole), analogously for left edges. Summed in O(R−L + U−D).
- **Verification**: brute-checked by hand on W=H=1 with point hole (answer 5 ✓), W=H=2 with center hole (T_hole=16, answer 28 ✓), and fully computed Sample 1: T_total=335, T_hole=143, answer=192 ✓.
- Factorials/inv-factorials up to W+H+4 ≤ 2·10⁶+4; all binomial arguments bounded accordingly. Edge cases D=0 / L=0 skip the respective entry-edge loops; negative F args return 0.

## worker: Final review of code for off-by-one errors, index 
Final review performed; the code is unchanged because it already handles all the checked cases correctly.

**Off-by-one verification:**
- `S(a,b) = C(a+b+2, a+1) − 1`: counts all (i,j) with 0≤i≤a, 0≤j≤b including (0,0) → C(0,0)=1 per pair, so single-point paths are included. ✓
- `F(a,b) = C(a+b+4, a+2) − (a+3) − (b+1)`: re-derived via double hockey stick; spot-checked F(0,0)=2, F(1,0)=5, F(1,1)=14 (used in sample-1 hand computation giving exactly 192). ✓
- `G(a,b) = F(a,b) − (a+1)(b+1)`: the subtracted term is exactly the number of grid points, matching the "−1" in each S. G(0,0)=1, G(1,0)=3 ✓.
- Hole sums use prefix inclusion–exclusion with correct boundary shifts: `W−R−1`, `H−U−1`, `L−1`, `D−1`, each guarded to return 0 when negative. ✓
- Entry-edge decomposition: bottom edges `(x,D−1)→(x,D)` for L≤x≤R (requires D≥1), left edges `(L−1,y)→(L,y)` for D≤y≤U (requires L≥1). Each path through the hole uses exactly one such edge (its first hole vertex), so no double counting; the two edge families are disjoint for monotone paths. ✓
- B1/B2 subtract exactly the in-hole endpoints: `S(R−x, U−D)` covers t∈[x,R]×[D,U]; `S(R−L, U−y)` covers t∈[L,R]×[y,U]. ✓

**Index bounds (all ≤ N = W+H+4):**
- F: n = a+b+4 ≤ W+H+4 ✓ (largest case).
- Bottom loop: n₁ = x+D+1 ≤ R+D ≤ W+H; n₂ = W−x+H−D+2 ≤ W+H+2; n₃ = R−x+U−D+2 ≤ W+H+2. ✓
- Left loop: n₁ = L+y+1 ≤ L+U ≤ W+H; n₂ = W−L+H−y+2 ≤ W+H+2; n₃ = R−L+U−y+2 ≤ W+H+2. ✓
- All k satisfy 0 ≤ k ≤ n (e.g., W−x+1 ≥ 1 since x ≤ R ≤ W; H−D+1 ≥ 1). ✓

**Edge cases:**
- D=0 → bottom loop skipped (no points below the hole); L=0 → left loop skipped. ✓
- Degenerate hole (R=L or U=D, even a single point): formulas verified by hand on W=H=1, hole={(0,0)} (answer 5 ✓) and W=H=2, hole={(1,1)} (T_hole=16, answer 28 ✓).
- Hole touching boundary (U=H, R=W, etc.): all binomial arguments remain valid; B-terms reduce correctly (e.g., U−D+1 ≥ 1).
- Sample 1 fully recomputed by hand: total=335, through=143, answer=192 ✓.

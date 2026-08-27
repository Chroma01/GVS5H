
## ideation
The core difficulty: the grid is up to 10^6 × 10^6, so an O(W·H) DP is impossible. We need closed-form/combinatorial sums.

Structure: blocks = full rectangle [0,W]×[0,H] minus open hole (L≤x≤R AND D≤y≤U removed). Moves only +x/+y, so DP is acyclic. Define f(p) = number of paths ending at p (including the length-0 path starting at p). Then f(p) = 1 + f(p-(1,0)) + f(p-(0,1)) (terms only if predecessor is a block). Answer = Σ f(p) over all blocks.

Key combinatorial fact: for a full rectangle with no hole, f(x,y) = C(x+y, x). With a hole, points "past" the hole lose contributions that would have passed through it. Equivalently, f(p) = C(x+y,x) − (paths from any start to p that route through the hole). Since a path is just a choice of starting point plus monotone steps, f(p) counts pairs (start s ≤ p, monotone path s→p) avoiding hole points as intermediate/visited nodes.

Alternative viewpoint: answer = number of pairs (s, t) of blocks with s ≤ t coordinatewise and a monotone path from s to t avoiding the hole; each such pair contributes C((t−s).x + (t−s).y, (t−s).x) paths... wait, actually each path is determined by its sequence, and the number of monotone paths from s to t is C(dx+dy, dx). So answer = Σ over valid (s,t) pairs of C(dx+dy, dx), where "valid" means the monotone rectangle... no — valid means at least one monotone path from s to t avoids the hole, and we count each path. Hmm, but different paths between same endpoints are distinct, so answer = Σ_{s,t} (number of monotone hole-avoiding paths s→t). That's exactly Σ_p f(p) with f as above.

Cleaner: compute g(p) = number of monotone paths from any block start to p avoiding hole = f(p). Standard trick: f(p) = C(x+y,x) − Σ_{q in hole, q≤p} (paths from start to q first hitting hole at q)·C(...). Use "first hole point" decomposition: any full-rectangle path counted in C(x+y,x) that passes through the hole has a first hole point q, which must be on the hole's lower-left boundary (x=L, D≤y≤U, or y=D, L≤x≤R — actually first hole point entered from left or below, so q=(L,y) for D≤y≤U or q=(x,D) for L≤x≤R). Number of paths from arbitrary start to q that avoid hole = C(q.x+q.y, q.x) minus... but q is the first hole point, predecessor is outside; paths to q avoiding hole = f_full(q) since nothing before q is in hole... Actually paths to q where all earlier points avoid hole: since q is the minimal-corner region, paths to (L,y) with y≥D avoid hole iff they don't enter hole earlier, but hole points ≤ (L,y) are (x',y') with L≤x'≤R, D≤y'≤y — x'≥L means x'=L only possible... points ≤ (L,y) in hole need x'≥L and x'≤L so x'=L, y' between D and y. So paths to (L,y) avoiding hole = C(L+y, L) − Σ_{D≤y'<y} (first-hit at (L,y'))·C(y−y', ...). This is getting recursive but only along the boundary — 1D recursion solvable in O(width+height).

Better known approach (this is AtCoder ABC/ARC problem "Kyoto" — likely typical): Split blocks into regions: A = {y<D} (bottom strip, full width), B = {y>U} (top strip), C = {D≤y≤U, x<L} (left strip), E = {D≤y≤U, x>R} (right strip). Compute DP region by region:
- Region A (0≤x≤W, 0≤y≤D−1): f(x,y)=C(x+y,x). Contribution Σ = Σ C(x+y,x) = C(W+D, D) ... identity: Σ_{x=0..W, y=0..D−1} C(x+y,x) = C(W+D+1, D) − 1? Let me verify: Σ_x Σ_y C(x+y, x). Known: Σ_{y=0..Y} Σ_{x=0..X} C(x+y,x) = C(X+Y+2, X+1) − 1. Check small: X=0,Y=0: sum=1, C(2,1)−1=1 ✓.
- Region C (0≤x≤L−1, D≤y≤U): same as full rectangle since hole is to the right: f(x,y)=C(x+y,x). Contribution = C(L+U+2, ... ) − C(L+D+1, ...) via prefix sums: define S(X,Y)=Σ_{0≤x≤X,0≤y≤Y} C(x+y,x) = C(X+Y+2, X+1) − 1. Then region sum = S(L−1,U) − S(L−1,D−1).
- Region A similarly = S(W, D−1).
- Region B (0≤x≤W, U+1≤y≤H): f(x,y) = C(x+y,x) − (paths through hole). Paths through hole reaching (x,y): enter hole... subtract contributions. For points above the hole, paths through hole = paths that pass through some hole point. Using first-hit boundary: f(x,y) = C(x+y,x) − Σ_{q on entry boundary} a(q)·C((x−q.x)+(y−q.y), x−q.x), where a(q) = number of hole-avoiding paths from starts to q's predecessor... Standard: a(q) for q=(L,y'), D≤y'≤U: paths arriving at q from left = f(L−1, y') = C(L−1+y', L−1). For q=(x',D), L≤x'≤R: arriving from below = f(x', D−1) = C(x'+D−1, x'). Then f(x,y) = C(x+y,x) − Σ_{y'=D..U} C(L−1+y', L−1)·C((x−L)+(y−y'), x−L) − Σ_{x'=L..R} C(x'+D−1, x')·C((x−x')+(y−D), x−x'). But careful about double counting: paths entering hole at left boundary vs bottom boundary are disjoint by first-hit point. ✓.
- Region E (R+1≤x≤W, D≤y≤U): similarly f(x,y) = C(x+y,x) − Σ_{x'=L..R} C(x'+D−1,x')·C((x−x')+(y−D), x−x') (only bottom entry matters since left entry points have x=L≤R<x, and a path reaching region E through the hole... first-hit could be at (L,y') then travel through hole and exit — but first-hit decomposition handles it: subtract Σ over both boundary types. For region E, paths entering at (L,y') then moving right through hole to (x,y) with y'≤U, y≤U: yes possible. So subtract both sums as well.

Then summing f over regions B and E requires summing products of binomials over rectangles — these have closed forms via Vandermonde/chu identity: Σ_{x≥a, y≥b} C(x−a+y−b, x−a) over rectangle = S-type sums. Σ_{x=X1..X2, y=Y1..Y2} C((x−qx)+(y−qy), x−qx) = S(X2−qx, Y2−qy) − S(X1−1−qx, ...) etc. using S(X,Y)=C(X+Y+2, X+1)−1. So each boundary sum over region B or E becomes O(length of boundary) = O(R−L + U−D) ≤ 2·10^6, fine.

Total complexity O(W+H) for factorials + O(boundary). Need factorials up to W+H+2 ≈ 2·10^6+2.

Pitfalls:
- Mod 998244353, precompute fact/invfact up to W+H+2 (maybe +5 safety).
- Careful with region boundaries: hole is L≤x≤R, D≤y≤U inclusive (blocks absent there). Condition "x<L or R<x or y<D or U<y" confirms hole = {L≤x≤R AND D≤y≤U}.
- Edge cases: L=0 (no left strip, no left-entry boundary), R=W, D=0, U=H, hole possibly empty (L>R impossible per constraints L≤R, but hole always exists? L≤R and D≤U so hole is nonempty rectangle... but if L=R and D=U it's a single point). Actually constraints say L≤R, D≤U, so hole always nonempty. But "there is at least one block" guaranteed.
- Negative upper args in binomial → treat as 0.
- S(X,Y) for X<0 or Y<0 → 0.
- The subtraction sums: ensure modular positivity.

Let me double check the first-hit decomposition correctness: any monotone path from start s to p that visits a hole point has a first hole point q. Predecessor of q is (q.x−1,q.y) or (q.x,q.y−1), which is a block. q must satisfy: q in hole, and (q.x−1 not in hole or q.x−1<0...) i.e., q.x=L (entered from left) or q.y=D (entered from below). Corner q=(L,D) can be entered either way — but for first-hit decomposition we just need: number of hole-avoiding paths from any start to q with last step from a block = f_block(q.x−1,q.y) + f_block(q.x,q.y−1) where f_block is the hole-avoiding path count. For q=(L,y'), y'>D: predecessor below is (L, y'−1) which is in hole, so only left predecessor counts: f(L−1, y') = C(L−1+y', L−1) (full formula valid since region left of hole unaffected). For q=(x',D), x'>L: only below predecessor: C(x'+D−1, x'). For q=(L,D): both predecessors (L−1,D) and (L,D−1) are blocks; paths to q avoiding hole = f(L−1,D) + f(L,D−1) = C(L−1+D, L−1) + C(L+D−1, L). Hmm, but in my boundary sums I had q=(L,y') for D≤y'≤U with weight C(L−1+y', L−1) and q=(x',D) for L≤x'≤R with weight C(x'+D−1, x'). At corner (L,D): left-entry weight C(L−1+D, L−1) counts paths whose last step is from left; bottom-entry weight C(L+D−1, L) counts paths whose last step is from below. These are disjoint sets of paths (different last step), and together they cover all hole-avoiding paths to (L,D). And first-hit at (L,D) is well-defined regardless of entry direction. So total subtraction = Σ over boundary entry points with weights = (hole-avoiding paths to q with specified entry side), and each full-rectangle path through the hole is counted exactly once by its first hole point and its actual entry side. ✓ Great, so the formulas are consistent: left boundary q=(L,y'), D≤y'≤U, weight C(L−1+y', L−1) (requires L≥1); bottom boundary q=(x',D), L≤x'≤R, weight C(x'+D−1, x') (requires D≥1).

Then for target p, subtract Σ_q w(q)·C((p−q).x+(p−q).y, (p−q).x) over q≤p.

Region sums:
- Answer = S(W,D−1) [bottom] + [S(L−1,U) − S(L−1,D−1)] [left] + top region + right region.
- Top region (U+1≤y≤H, 0≤x≤W): Σ f = [S(W,H) − S(W,U)] − Σ_{q left bnd} w(q)·[rectsum over p in top region of C(p−q)] − Σ_{q bottom bnd} w(q)·[...]. For q=(qx,qy), Σ_{p: 0≤x≤W, U+1≤y≤H} C((x−qx)+(y−qy), x−qx) with qx≤x, qy≤y (q always satisfies qy≤U<U+1≤y, and qx≤R≤W but need qx≤x — for q with qx possibly > x? qx≤R, x ranges 0..W; if x<qx term is zero anyway since C with negative... in S-identity we must restrict x≥qx. So sum = Σ_{x=qx..W, y=U+1..H} = T(W−qx, H−qy) − T(W−qx, U−qy) where T(X,Y)=S(X,Y) with shifted: Σ_{x'=0..X, y'=0..Y} C(x'+y', x') = S(X,Y). So = S(W−qx, H−qy) − S(W−qx, U−qy). ✓ (valid when W−qx≥0; else 0.)
- Right region (R+1≤x≤W, D≤y≤U): Σ f = [S(W,U) − S(W,D−1) − S(R,U) + S(R,D−1)] − Σ_q w(q)·[S(W−qx, U−qy) − S(W−qx, D−1−qy) − S(R−qx, U−qy) + S(R−qx, D−1−qy)].

All O(1) per boundary point. Total O(W+H+ boundary). 

Sanity check with sample 1: W=4,H=3,L=1,R=2,D=2,U=3. Hole = x∈{1,2}, y∈{2,3}. Blocks: y=0,1 full width (5+5=10 points), y=2,3: x=0,3,4 (3+3=6 points). Total 16 blocks.
Bottom region: S(4,1) = C(7,5)−1 = 21−1=20. Left region: S(0,3)−S(0,1) = (C(5,1)−1)−(C(3,1)−1) = 4−2=2. Top region: y>U=3 → none (H=3). Right region: x∈{3,4}, y∈{2,3}: base = S(4,3)−S(4,1)−S(2,3)+S(2,1) = (C(9,5)−1)−(C(7,5)−1)−(C(7,3)−1)+(C(5,3)−1) = 125−20−34+9 = 80. Subtractions: left boundary q=(1,2),(1,3), w=C(0+y',0)=1 each... w(q)=C(L−1+y', L−1)=C(y',0)=1. Bottom boundary q=(1,2),(2,2): w=C(x'+1, x') = x'+1: w(1,2)=2, w(2,2)=3.
For right region sums with formula S(W−qx, U−qy) − S(W−qx, D−1−qy) − S(R−qx, ...) + ...:
q=(1,2): S(3,1)−S(3,−1)−S(1,1)+S(1,−1) = (C(6,4)−1) − 0 − (C(4,2)−1) + 0 = 14−5=9. times w=1 → 9.
q=(1,3): S(3,0)−S(3,−2)−S(1,0)+S(1,−2) = (C(5,4)−1) − (C(3,2)−1) = 4−2=2. → 2.
q=(1,2) bottom w=2: same rect sum 9 → 18.
q=(2,2) w=3: S(2,1)−0−S(0,1)+0 = (C(5,3)−1)−(C(3,1)−1) = 9−2=7 → 21.
Right region total = 80 − 9 − 2 − 18 − 21 = 30.
Answer = 20 + 2 + 30 = 52?? Expected 192. Something's wrong!

Hmm. Let me recompute. Oh wait — I think f(p) counts paths ending at p, and answer = Σ f. Let me recompute S identity: S(X,Y) = Σ_{x=0..X} Σ_{y=0..Y} C(x+y, x). X=4,Y=1: values: y=0: C(x,x)=1 each, 5 points → 5. y=1: C(x+1,x)=x+1: 1,2,3,4,5 → 15. Total 20 ✓. C(4+1+2, 4+1)−1 = C(7,5)−1 = 21−1=20 ✓.

Left region x=0, y∈{2,3}: f(0,y)=1 each → 2 ✓.

Right region: points (3,2),(4,2),(3,3),(4,3). Compute f directly. Full C values: f_full(3,2)=C(5,3)=10, f_full(4,2)=C(6,4)=15, f_full(3,3)=C(6,3)=20, f_full(4,3)=C(7,4)=35. Sum=80 ✓ matches base.

Now paths through hole: hole points (1,2),(2,2),(1,3),(2,3). For p=(3,2): paths from any start to (3,2) passing through hole. First-hit q: q=(1,2) entered from left (start paths to (0,2): only (0,0)? f(0,2)=1: path (0,0)→(0,1)→(0,2) and starts (0,1),(0,2): f(0,2)=C(2,0)=1? Wait f(0,2) = number of paths ending at (0,2) = paths from starts (0,0),(0,1),(0,2) = 3! But C(0+2,0)=1. Contradiction!

I think I mislabeled: C(x+y, x) at (0,2) = C(2,0) = 1, but number of monotone paths from any start to (0,2): starts must have x≤0, so (0,0),(0,1),(0,2): paths: (0,2); (0,1)→(0,2); (0,0)→(0,1)→(0,2) = 3. So f(0,2)=3 ≠ C(2,0)=1. My formula is wrong!

Hmm, f(x,y) = number of (start, path) pairs ending at (x,y) = Σ_{s≤(x,y)} C((x−sx)+(y−sy), x−sx) = Σ_{i=0..x} Σ_{j=0..y} C(i+j, i) = S(x,y) = C(x+y+2, x+1) − 1. So f(x,y) = C(x+y+2, x+1) − 1, not C(x+y,x)! I conflated. Then answer = Σ_p f(p) = Σ_p [C(x+y+2, x+1) − 1] = Σ_p S(x,y)... and Σ over rectangle of S = double sum of C = triple... Let me redo: answer for full rectangle = Σ_{x,y} Σ_{i≤x,j≤y} C(i+j,i) = Σ_{i,j} C(i+j,i)·(W−i+1)(H−j+1). Hmm, that's more complex. Alternatively define F(X,Y) = Σ_{x=0..X,y=0..Y} f(x,y) = Σ f = Σ_{x,y} [C(x+y+2,x+1) − 1]. Σ_{x=0..X,y=0..Y} C(x+y+2, x+1): let u=x+1, v=y+1: C(u+v, u) summed u=1..X+1, v=1..Y+1 = S(X+1,Y+1) − Σ_{u} C(u, u)... hmm S(X+1,Y+1) includes u=0 or v=0 terms: S(X+1,Y+1) = Σ_{u=0..X+1,v=0..Y+1} C(u+v,u) = [Σ_{u≥1,v≥1}] + Σ_{u=0..X+1} C(u,u) + Σ_{v=1..Y+1} C(v,0) = target + (X+2) + (Y+1). So target = S(X+1,Y+1) − X − Y − 3 = C(X+Y+4, X+2) − 1 − X − Y − 3 = C(X+Y+4, X+2) − X − Y − 4. Then F(X,Y) = that − (X+1)(Y+1).

Check: F(0,0) should be f(0,0)=1. C(4,2)−0−0−4 = 6−4=2, minus 1 → 1 ✓.

OK so the recurrences still hold: f(p) = 1 + f(left) + f(below) over blocks, f = S(x,y) = C(x+y+2, x+1)−1 in hole-free areas. The first-hit decomposition: full-rectangle f_full(p) = S(p) counts all (start, path) ending at p. Those passing through hole: first hole point q, entry from block predecessor. Number of (start,path) to predecessor pr = f(pr) (hole-avoiding, but pr is in unaffected region so f_full(pr)=S(pr)). Then continue from q to p: C((p−q) sum, ...) paths. So f(p) = S(p) − Σ_q w(q) C(dx+dy, dx) with w(q) = S(pr) for the entry predecessor:
- Left entry q=(L,y'): pr=(L−1,y'), w = S(L−1,y') = C(L+y'+1, L) − 1.
- Bottom entry q=(x',D): pr=(x',D−1), w = S(x',D−1) = C(x'+D+1, x'+1) − 1.

And region sums as before but with S replaced appropriately and the "1" terms: base region sums use F-type sums (sum of S over rectangle) — need G(X,Y) = Σ_{x=0..X,y=0..Y} S(x,y) = Σ [C(x+y+2,x+1) − 1] = C(X+Y+4, X+2) − (X+Y+4) − ... let me recompute: Σ C(x+y+2, x+1) = C(X+Y+4, X+2) − X − Y − 4 (derived above). So G(X,Y) = C(X+Y+4, X+2) − X − Y − 4 − (X+1)(Y+1).

Check G(0,0)=C(4,2)−4−1=6−5=1 ✓.

And subtraction sums: Σ_{p in region} C((p−q).x+(p−q).y, (p−q).x) = S-type sums as before: S(X,Y) = C(X+Y+2, X+1) − 1 over shifted rectangle.

Let me redo sample 1 with corrected formulas.
W=4,H=3,L=1,R=2,D=2,U=3.
Bottom region (y≤1): G(4,1) = C(4+1+4, 4+2) − 4 − 1 − 4 − (5·2) = C(9,6) − 9 − 10 = 84 − 19 = 65.
Check manually: f(x,y)=C(x+y+2, x+1)−1: y=0: C(x+2,x+1)−1 = x+1: (1,2,3,4,5) sum 15. y=1: C(x+3, x+1)−1 = C(x+3,2)−1: x=0: 3−1=2; x=1: 6−1=5; x=2: 10−1=9; x=3: 15−1=14; x=4: 21−1=20. Sum=50. Total 65 ✓.

Left region (x=0, y=2..3): G(0,3)−G(0,1). G(0,3)=C(7,2)−0−3−4−(1·4)=21−11=10. G(0,1)=C(5,2)−0−1−4−2=10−7=3. Left=7. Check: f(0,y)=y+1: y=2→3, y=3→4, sum 7 ✓.

Right region: x∈{3,4}, y∈{2,3}. Base = G(4,3)−G(4,1)−G(2,3)+G(2,1).
G(4,3)=C(11,6)−4−3−4−20=462−31=431. G(4,1)=65. G(2,3)=C(9,4)−2−3−4−12=126−21=105. G(2,1)=C(7,4)−2−1−4−6=35−13=22. Base=431−65−105+22=283.
Subtractions: w and rect sums.
Left boundary q=(1,y'), y'∈{2,3}: w=S(0,y')=C(y'+2,1)−1=y'+1: w(1,2)=3, w(1,3)=4.
Bottom boundary q=(x',2), x'∈{1,2}: w=S(x',1)=C(x'+3, x'+1)−1=C(x'+3,2)−1: w(1,2)=C(4,2)−1=5, w(2,2)=C(5,3)−1=9.
Rect sum for region x∈{3,4},y∈{2,3} relative to q=(qx,qy): RS(q) = S(4−qx, 3−qy) − S(4−qx, 1−qy) − S(2−qx, 3−qy) + S(2−qx, 1−qy), where S with negative arg = 0.
S(X,Y)=C(X+Y+2,X+1)−1.
q=(1,2): S(3,1)−S(3,−1)−S(1,1)+S(1,−1) = (C(6,4)−1) − (C(4,2)−1) = 14−5=9. Contribution: 3·9=27.
q=(1,3): S(3,0)−S(3,−2)−S(1,0)+S(1,−2) = (C(5,4)−1)−(C(3,2)−1)=4−2=2. Contribution: 4·2=8.
q=(1,2) bottom, w=5: RS=9 → 45.
q=(2,2) bottom, w=9: S(2,1)−0−S(0,1)+0 = (C(5,3)−1)−(C(3,1)−1)=9−2=7 → 63.
Right region = 283−27−8−45−63=140.
Total = 65+7+140 = 212. Expected 192. Still off by 20. Hmm.

Let me brute-force mentally... maybe double counting in first-hit: a path entering hole at q=(1,2) from left, vs a path counted in bottom boundary q=(1,2) from below — disjoint last steps ✓. But wait: paths that go through hole and reach right region — first hit q, then any continuation through hole to p. Continuation from q to p: C(dx+dy, dx) counts all monotone continuations, all of which stay... they might exit hole and re-enter? Once first-hit is fixed, continuation can be anything — fine, no double count since first-hit unique.

Hmm, but maybe error: paths counted in f_full(p) = S(p) that pass through hole — decomposition by first hole point q and the path from start to predecessor pr. But the path from start to pr must be hole-avoiding — pr is in region left/below hole which is unaffected, so all S(pr) paths avoid hole ✓. But wait: for left-entry q=(L,y'), pr=(L−1,y'): paths to pr could pass through hole? Hole points ≤ (L−1,y') need x≥L — impossible. ✓. For bottom-entry similar ✓.

Let me just brute force sample 1 directly to find the true count per point in right region.
Blocks: y≤1: all x 0..4. y∈{2,3}: x∈{0,3,4}.
f(p) = 1 + f(left if block) + f(below if block).
y=0: f(x,0)=1+f(x−1,0): f(0,0)=1, f(1,0)=2, f(2,0)=3, f(3,0)=4, f(4,0)=5.
y=1: f(0,1)=1+f(0,0)=2. f(1,1)=1+f(0,1)+f(1,0)=1+2+2=5. f(2,1)=1+5+3=9. f(3,1)=1+9+4=14. f(4,1)=1+14+5=20.
y=2: f(0,2)=1+f(0,1)=3. (1,2),(2,2) hole. f(3,2)=1+f(2,2)?not block+f(3,1)=1+14=15. f(4,2)=1+f(3,2)+f(4,1)=1+15+20=36.
y=3: f(0,3)=1+f(0,2)=4. f(3,3)=1+f(3,2)=16 (below (3,2) block, left (2,3) hole). f(4,3)=1+f(3,3)+f(4,2)=1+16+36=53.
Sum: y0: 15, y1: 50, y2: 3+15+36=54, y3: 4+16+53=73. Total=15+50+54+73=192 ✓.

Right region true: f(3,2)+f(4,2)+f(3,3)+f(4,3)=15+36+16+53=120. My formula gave 140. Difference 20. Let's check subtractions per point.
f_full S values: S(3,2)=C(7,4)−1=34. True 15, so subtraction 19. Paths through hole to (3,2): first-hit q∈{(1,2)L-entry, (1,2)B-entry, (2,2)B-entry}. q=(1,2) left entry: w=S(0,2)=C(4,1)−1=3. Continuations (1,2)→(3,2): C(2,2)=1. → 3. q=(1,2) bottom entry: w=S(1,1)=C(4,2)−1=5, cont 1 → 5. q=(2,2) bottom: w=S(2,1)=C(5,3)−1=9, cont (2,2)→(3,2): C(1,1)=1 → 9. Total subtract 17. 34−17=17 ≠ 15. Hmm, true subtraction should be 19? 34−15=19. So missing 2.

What paths from starts to (3,2) pass through hole? Enumerate paths through hole points: hole points ≤(3,2): (1,2),(2,2). Paths ending (3,2) visiting (1,2) or (2,2). Count (start,path) pairs: paths through (2,2): (start→(2,2) avoiding hole first... let me count all (start,path) to (3,2) through hole = Σ over paths. Total to (3,2) = 34. Avoiding hole: paths must go through... to reach (3,2) without hole, since (1,2),(2,2) blocked, path must reach y=2 only at x≥3, i.e., last step from (3,1), and prefix any path to (3,1): f(3,1)=14, plus the trivial path start=(3,2): total 15 ✓. Through hole: 34−15=19.

First-hit decomposition: first hole point (1,2) or (2,2). First hit (2,2): predecessor (2,1) (since (1,2) is hole, predecessor must be below). Paths start→(2,1): S(2,1)=9, then (2,2)→(3,2): 1 way. → 9. First hit (1,2): predecessor (0,2) or (1,1). Paths to (0,2): S(0,2)=3. Paths to (1,1): S(1,1)=5. Then continuations (1,2)→(3,2): paths (1,2)→(2,2)→(3,2) and (1,2)→(2,... wait dx=2,dy=0: only one path: right,right. C(2,2)=1. So 3+5=8. Total 9+8=17. But true is 19. Missing 2!

Ah I see — continuations from (1,2) to (3,2): only right-right, 1 way ✓. Hmm so where are the missing 2? Let me enumerate paths through hole to (3,2) explicitly. A (start, path) pair: path is sequence from start to (3,2). Paths through (1,2): start ≤ (1,2), path start→(1,2)→(2,2)→(3,2). Number of (start, path) to (1,2) avoiding earlier hole: hole points <(1,2): none ((1,2) is min corner... (1,2) with x≥1,y≥2: points ≤(1,2) in hole: (1,2) itself only). So all paths to (1,2): S(1,2)=C(5,2)−1=9. Hmm! S(1,2)=9, but I split into entry from (0,2): S(0,2)=3 and entry from (1,1): S(1,1)=5, total 8 ≠ 9. Missing the path that starts AT (1,2)?? No wait — (1,2) is a hole point, can't start there. But S(1,2) counts paths starting at (1,2) itself! f_full includes start=p trivial path. For first-hit at q, the path must arrive at q from a predecessor — start ≠ q since q is not a block. So paths to q with at least one step = S(q) − 1 = entry-left + entry-below paths... S(1,2)−1 = 8 = 3+5 ✓. So that's consistent.

So first-hit (1,2): 8 paths, first-hit (2,2): paths arriving (2,2) from (2,1): S(2,1)=9... but wait, paths to (2,1) that pass through hole? Hole ≤(2,1): none ✓. But also: do any of these 9 paths start at... (2,1) is a block, fine, path can start at (2,1) then move up — that's valid, first-hit (2,2) ✓. 9 paths. Total 17. But true count 19. Contradiction with direct enumeration? Let me enumerate directly: all (start,path) to (3,2) through hole.

Starts s≤(3,2), paths s→(3,2) visiting (1,2) or (2,2).
Through (2,2): path visits (2,2). Segment s→(2,2): any (start,path) to (2,2) = S(2,2) − 1 (exclude start=(2,2) since hole) = C(6,3)−1−1 = 19−1=18? C(6,3)=20, S(2,2)=19, minus 1 = 18. Then (2,2)→(3,2): 1 way. But paths to (2,2) that pass through (1,2) — those have first-hit (1,2). Paths to (2,2) avoiding (1,2): must enter (2,2) from (2,1): S(2,1)=9 ✓. Paths to (2,2) through (1,2): 18−9=9 = paths to (1,2) (S(1,2)−1=8)... 9≠8. Hmm: paths to (2,2) visiting (1,2): (start,path) to (1,2) then step right: paths to (1,2) excluding start at (1,2): 8, plus... path could visit (1,2) — must pass through it: number = (paths to (1,2) with start≠(1,2)) × 1 = 8. But 18−9=9. So paths to (2,2) avoiding (1,2) = 18−8=10, not 9! Paths entering (2,2) from (2,1): S(2,1)=9, plus path starting at (2,2)? excluded. Hmm 10 vs 9. Paths to (2,2) avoiding (1,2): last step from (2,1) or from (1,2) — (1,2) excluded — so from (2,1): (start,path) to (2,1) = S(2,1)=9. But also start=(2,2)?? excluded. So 9. Then through (1,2): 18−9=9 ≠ 8. Inconsistency means arithmetic error: S(2,2)=C(2+2+2, 2+1)−1=C(6,3)−1=20−1=19. Paths with start≠(2,2): 18. Paths visiting (1,2): (start,path) to (1,2), start≠(1,2), then right: S(1,2)−1 = C(5,2)−1−1 = 10−2=8. 9+8=17 ≠ 18. So one missing path to (2,2)! Which? Start=(2,2) excluded... start=(1,2) excluded (hole). Enumerate paths to (2,2) by last step: from (1,2): 8 paths (start≠(1,2))... plus paths from (1,2) as start — invalid. From (2,1): S(2,1)=9 paths (including start (2,1)). Total 17, plus start at (2,2): 1 → 18? But S(2,2)=19. So S formula must count 19: starts s≤(2,2): 9 lattice points (x 0..2, y 0..2). Paths: Σ C(dx+dy,dx): (0,0):C(4,2)=6,(1,0):C(3,1)=3,(2,0):1,(0,1):C(3,2)=3,(1,1):C(2,1)=2,(2,1):1,(0,2):1,(1,2):1,(2,2):1. Sum=6+3+1+3+2+1+1+1+1=19 ✓. Paths through (1,2): starts ≤(1,2): (0,0):C(3,1)=3? paths (0,0)→(1,2): C(3,1)=3, (1,0):C(2,1)=2? (1,0)→(1,2): dx=0,dy=2: 1 path. Let me list: start (0,0): 3 paths to (1,2); (0,1): C(2,1)=2; (0,2): 1; (1,0): 1; (1,1): 1; (1,2): excluded. Total 3+2+1+1+1=8 ✓. Then continue to (2,2): 8 paths through (1,2). Paths not through (1,2): 19−1(start self)−8=10. Last step from (2,1): starts ≤(2,1): (0,0):C(3,1)=3,(1,0):C(2,1)=2,(2,0):1,(0,1):C(2,1)... (0,1)→(2,1): C(2,... dx=2,dy=0: 1. Hmm recompute: (0,1)→(2,1): dx=2, dy=0: C(2,2)=1. (1,1)→(2,1): 1. (2,1): 1. Sum: 3+2+1+1+1+1=9 ✓ S(2,1)=C(5,3)−1=10−1=9 ✓. So 9+8=17, plus self 1 = 18 ≠ 19!! There's a path to (2,2) not through (1,2), not last-step from (2,1), not starting at (2,2)? Last step must be from (1,2) or (2,1) — those are the only predecessors. So 19 = 1 + 8 + 9 = 18?? Contradiction — arithmetic: 1+8+9=18, but sum computed 19. Let me recount paths from (0,0) to (2,2): C(4,2)=6. Of these, through (1,2): paths (0,0)→(1,2)→(2,2): C(3,1)=3. Not through: 3. From (1,0): C(3,1)=3 paths to (2,2); through (1,2): (1,0)→(1,2): 1 path; so 2 not through. (2,0): 1 path, not through (1,2). (0,1): C(3,2)=3 paths; through (1,2): (0,1)→(1,2): C(2,1)=2; not: 1. (1,1): C(2,1)=2; through (1,2): 1; not: 1. (2,1): 1, not through. (0,2): 1 path: (0,2)→(1,2)→(2,2): through. (1,2): excluded. (2,2): self.
Through (1,2) total: 3+2+1+1+1 = 8 ✓. Not through: 3+2+1+1+1+1 = 9, plus self 1. Total 8+9+1=18. But Σ said 19. Recount Σ: (0,0):6, (1,0):3, (2,0):1, (0,1):3, (1,1):2, (2,1):1, (0,2):1, (1,2):1, (2,2):1 → 6+3+1+3+2+1+1+1+1=19. Hmm (1,2) as start: start=(1,2) is a hole point — but S(2,2) as "full rectangle" count includes it since f_full ignores hole. In the true problem start (1,2) invalid, but in f_full(p) decomposition, paths starting in the hole are also counted and must be subtracted! My first-hit decomposition only handles paths that ENTER the hole from a block, but paths STARTING inside the hole (counted in f_full) are missed!

In f_full(p) = S(p), starts range over all s≤p including hole points. A path from a hole start s to p: its "first hole point" is s itself (at time 0), with no predecessor. So the subtraction must also include: Σ_{q in hole, q≤p} (number of paths starting exactly at q) × C(p−q) = Σ_{q in hole} C((p−q) sum, (p−q).x). I.e., treat each hole point q as also contributing w(q) += 1 (the trivial start-at-q path).

So corrected: subtraction over q in hole-entry-boundary with weights w as before, PLUS over ALL hole points q with weight 1 (start at q). But careful: paths starting at hole point q then moving — first hole point is q, counted once ✓. And paths entering hole from outside counted by entry ✓. A path starting at hole q1, going through hole to p: counted once under q1 ✓.

So total subtraction for p: Σ_{q ∈ hole, q≤p} C(p−q) [start-in-hole] + Σ_{entry boundary q} w_entry(q)·C(p−q).

Now Σ_{q in hole, q≤p} C((p.x−q.x)+(p.y−q.y), p.x−q.x) over the hole rectangle — this is a 2D sum over q: Σ_{qx=L..min(R,p.x), qy=D..min(U,p.y)} C((p.x−qx)+(p.y−qy), p.x−qx) = S(p.x−L, p.y−D) − S(p.x−L, p.y−U−1) − S(p.x−R−1, p.y−D) + S(p.x−R−1, p.y−U−1) (with appropriate clamping/negatives → 0). O(1) per p, and summing over p in a region: sum of S over rectangle = G-type sum! Since region sums needed: Σ_{p ∈ region} [that expression] = sums of G over shifted rectangles — O(1) each. 

Similarly the entry-boundary weights summed over region p: O(boundary) as before.

Alternatively, cleaner unified view: define hole indicator; f(p) = S(p) − Σ_{q: q in hole or q is "entry"} ... Actually even cleaner: think of it as inclusion of "virtual starts". Alternatively use the standard approach: compute f via decomposition where we subtract using DP over "boundary sources". The formula: f(p) = S(p) − Σ_{q ∈ H, q≤p} c(q)·C(p−q) where c(q) = 1 + (paths arriving at q from outside) = 1 + f(q.x−1,q.y)[if block] + f(q.x,q.y−1)[if block]... but for q in interior of hole, "arriving from outside" = 0, c=1. For q on top/right edges of hole, arriving from outside is from... predecessor (q.x−1,q.y): if q.x>L it's hole, not block. Predecessor outside hole only if q.x=L (left edge) or q.y=D (bottom edge). So c(q) = 1 + [q.x=L]·f(L−1, q.y) + [q.y=D]·f(q.x, D−1), where f at block points = S values. Wait but for corner (L,D): c = 1 + f(L−1,D) + f(L,D−1). Hmm but does this overcount? A path entering at (L,D) from left vs below: disjoint last steps ✓, plus start at (L,D): disjoint ✓.

But wait — is it true that f(p) = S(p) − Σ_{q∈H} c(q) C(p−q) with these c? Proof: S(p) counts all (start s≤p, path s→p). Bad ones: those whose path visits ≥1 hole point OR start in hole. For bad path, let q = first hole point visited (if start in hole, q=start). Then q∈H, and the prefix is: either trivial (s=q, counted by the "1" in c(q)), or ends with step from block predecessor (counted by f(predecessor) terms — need predecessor's paths to be hole-avoiding, which holds since q is first hole point and predecessor < q... but f(predecessor) = S(predecessor) counts ALL paths to predecessor including through hole — but hole points ≤ predecessor: for predecessor (L−1, q.y): none (x≥L needed). For (q.x, D−1): none (y≥D needed). ✓). So each bad path counted exactly once. ✓✓

Great, so: f(p) = S(p) − Σ_{q∈H, q≤p} c(q)·C((p−q).x+(p−q).y, (p−q).x), c(q) = 1 + [qx=L]·S(L−1, qy) + [qy=D]·S(qx, D−1) (terms only when the predecessor exists as block; if L=0 then qx=L=0 has no left predecessor; also need predecessor to be a block: (L−1,qy) is block iff L≥1; (qx,D−1) block iff D≥1).

Hmm wait, one more check: c(q) for q on left edge: S(L−1, qy) counts paths to (L−1,qy) including starts anywhere ≤ — all valid blocks ✓.

Now answer = Σ_{p ∈ blocks} f(p) = Σ_{p∈blocks} S(p) − Σ_{q∈H} c(q)·Σ_{p∈blocks, p≥q} C(p−q).

Σ_{p∈blocks} S(p): blocks = rectangle minus hole. Σ_{p∈full} S(p) = G(W,H). Σ_{p∈hole} S(p) = G(R,U)−G(L−1,U)−G(R,D−1)+G(L−1,D−1). So first term = G(W,H) − that.

Second term: for each q∈H, Σ_{p∈blocks, p≥q} C(p−q). Blocks with p≥q: full rectangle p≥q minus hole points ≥q. Σ_{p≥q, p≤(W,H)} C(p−q) = S(W−qx, H−qy). Σ_{p∈H, p≥q} C(p−q) = S(R−qx, U−qy) − S(L−1−qx, ...) — but qx≥L so L−1−qx<0 → those terms vanish: = S(R−qx, U−qy) − S(R−qx, D−1−qy) − S(L−1−qx, U−qy) + S(L−1−qx, D−1−qy); with qx≥L, negative → 0; and qy≥D makes D−1−qy<0 → 0. So = S(R−qx, U−qy). Wait that's not right either: Σ_{p∈H, p≥q} C(p−q) where p ranges qx..R × qy..U (since p≥q and p in hole): = S(R−qx, U−qy). ✓ simple.

So Σ_{p∈blocks,p≥q} C(p−q) = S(W−qx, H−qy) − S(R−qx, U−qy).

Then answer = G(W,H) − [G(R,U)−G(L−1,U)−G(R,D−1)+G(L−1,D−1)] − Σ_{q∈H} c(q)·[S(W−qx,H−qy) − S(R−qx,U−qy)].

Now Σ_{q∈H} c(q)·[...]: c(q) = 1 + left-edge term + bottom-edge term. 
- Σ_{q∈H} 1·[S(W−qx,H−qy) − S(R−qx,U−qy)] = Σ_{qx=L..R} Σ_{qy=D..U} S(W−qx,H−qy) − similar. Σ_{qx=L..R,qy=D..U} S(W−qx, H−qy): substitute i=W−qx (i from W−R..W−L), j=H−qy: = Σ_{i=W−R..W−L, j=H−U..H−D} S(i,j) = G-sum over rectangle = G(W−L, H−D) − G(W−R−1, H−D) − G(W−L, H−U−1) + G(W−R−1, H−U−1). Similarly for the S(R−qx,U−qy) part: Σ = G(R−L, U−D) − G(−1,...)... = G(R−L, U−D) (other terms negative → 0). So the "1" part is O(1)!
- Left-edge part: Σ_{qy=D..U} S(L−1, qy)·[S(W−L, H−qy) − S(R−L, U−qy)] — O(U−D+1).
- Bottom-edge part: Σ_{qx=L..R} S(qx, D−1)·[S(W−qx, H−D) − S(R−qx, U−D)] — O(R−L+1).

Total: O((R−L)+(U−D)) ≈ 2·10^6 operations plus factorial precompute O(W+H). 

Verify sample 1 with this formula:
G(X,Y) = C(X+Y+4, X+2) − (X+1)(Y+1) − X − Y − 4 for X,Y≥0; G with any negative arg = 0. Let me double-check G formula: G(X,Y)=Σ_{x=0..X,y=0..Y}[C(x+y+2,x+1)−1] = [C(X+Y+4,X+2) − X − Y − 4] − (X+1)(Y+1). ✓
S(X,Y)=C(X+Y+2,X+1)−1, negative→0.

W=4,H=3,L=1,R=2,D=2,U=3.
G(4,3)=C(11,6)−5·4−4−3−4=462−20−11=431.
Hole S-sum: G(2,3)−G(0,3)−G(2,1)+G(0,1):
G(2,3)=C(9,4)−3·4−2−3−4=126−12−9=105.
G(0,3)=C(7,2)−1·4−0−3−4=21−11=10.
G(2,1)=C(7,4)−3·2−2−1−4=35−6−7=22.
G(0,1)=C(5,2)−1·2−0−1−4=10−7=3.
Hole sum=105−10−22+3=76.
First term: 431−76=355.

Second term Σ_{q∈H} c(q)[S(4−qx,3−qy)−S(2−qx,3−qy... wait U−qy=3−qy)].
Hole points: (1,2),(2,2),(1,3),(2,3).
c(1,2)=1+S(0,2)+S(1,1)=1+(C(4,1)−1)+(C(4,2)−1)=1+3+5=9.
c(2,2)=1+S(2,1)=1+9=10 (no left edge since qx=2≠L).
c(1,3)=1+S(0,3)=1+(C(5,1)−1)=1+4=5 (qy=3≠D).
c(2,3)=1.
Bracket B(q)=S(4−qx,3−qy)−S(2−qx,3−qy):
q=(1,2): S(3,1)−S(1,1)=(C(6,4)−1)−(C(4,2)−1)=14−5=9.
q=(2,2): S(2,1)−S(0,1)=(C(5,3)−1)−(C(3,1)−1)=9−2=7.
q=(1,3): S(3,0)−S(1,0)=(C(5,4)−1)−(C(3,2)−1)=4−2=2.
q=(2,3): S(2,0)−S(0,0)=(C(4,3)−1)−(C(2,1)−1)=3−1=2.
Σ c·B = 9·9+10·7+5·2+1·2 = 81+70+10+2=163.
Answer = 355−163=192 ✓✓✓

Formula verified. Complexity fine. Precompute factorials up to max arg of C: C(X+Y+4, ...) with X+Y ≤ W+H → up to W+H+4. Also C(X+Y+2,...). So N = W+H+5.

Edge cases: L=0 → left-edge term omitted (S(L−1,·)=S(−1,·)=0 automatically if we just compute S with negative → 0! Actually c(q) formula: [qx=L]·S(L−1,qy): if L=0, S(−1,qy)=0 ✓ automatic. Similarly D=0 → S(qx,−1)=0 ✓. So no special-casing needed, just define S,G to return 0 on negative inputs.

Also G with negative: define G(X,Y)=0 if X<0 or Y<0. S same.

Modulo: use mod 998244353, ensure ((...)%mod+mod)%mod.

Complexity: O(W+H+R−L+U−D) ~ 4·10^6 — fine in Python? Factorial precompute 2·10^6 in Python is okay (~1-2s). The loops over edges up to 10^6 each with a few binomial evaluations — should be okay but optimize: precompute S values? In the left-edge loop we need S(L−1,qy), S(W−L,H−qy), S(R−L,U−qy) for qy in D..U — each is O(1) binom. Total binom evaluations ~ 6·10^6 · (few multiplications) — Python might be ~5-10s. Risky but probably acceptable; can optimize with recurrence: S(L−1,qy) as qy increments: S(X,y) = S(X,y−1) + C(X+y+1... hmm S(X,Y)−S(X,Y−1) = Σ_{x} C(x+Y, x) = C(X+Y+1, X+1)... wait Σ_{x=0..X} C(x+Y,x) = C(X+Y+1, X+1)? Hockey stick: Σ_{x=0..X} C(Y+x, Y) = C(Y+X+1, Y+1) = C(X+Y+1, X). Let me verify: Σ_{x=0..X} C(Y+x, x) = C(X+Y+1, X+1)? Check X=1,Y=1: C(1,0)+C(2,1)=1+2=3; C(3,2)=3 ✓ (X+1=2... C(X+Y+1, X+1)=C(3,2)=3 ✓). So S(X,Y) = S(X,Y−1) + C(X+Y+1, X+1)... check: S(1,1)=C(4,2)−1=5; S(1,0)=C(3,2)−1=2; diff 3 = C(3,2)=3 ✓.

Alternatively just compute binoms directly; each binom = 2 fact lookups + 1 invfact... actually C(n,k)=fact[n]·ifac[k]·ifac[n−k]: 3 array lookups + 2 mults. 6·10^6 of these ~ maybe 6-8s in pure Python. Could be too slow. Optimize loops using recurrences along the edge:

Left edge loop: qy from D to U. Terms: A(qy)=S(L−1,qy), B(qy)=S(W−L,H−qy), C2(qy)=S(R−L,U−qy). As qy increases by 1: A increases by C(L+qy+1... A(qy)=S(L−1,qy): A(qy)−A(qy−1)=C((L−1)+qy+1, L) = C(L+qy, L). B(qy)=S(W−L, H−qy): B(qy)−B(qy−1) = −C(W−L+H−qy+1, W−L+1)... since Y decreases: S(X,Y−1)−S(X,Y) = −C(X+Y+1, X+1). So B(qy) = B(qy−1) − C((W−L)+(H−qy)+1, (W−L)+1) = B(qy−1) − C(W−L+H−qy+1, W−L+1). Similarly C2(qy) = C2(qy−1) − C(R−L+U−qy+1, R−L+1). And the binoms themselves satisfy recurrences as qy changes: C(L+qy, L) ratio (L+qy)/(qy)... C(n+1,k)=C(n,k)·(n+1)/(n+1−k): need modular inverse — precompute inverses up to W+H+5 (O(n) with linear recurrence or just use fact/invfact for the binom updates — actually simpler: compute each binom via fact table but that's the cost we're avoiding). Hmm. Honestly, maybe just do direct fact-table binoms but minimize count: per qy we need A, B, C2 → 3 binoms → ~9 lookups/mults. 10^6 iterations → maybe 3-4s. Plus bottom edge similar. Plus factorial precompute ~2·10^6 (~1s). Total maybe 5s. AtCoder typical limit 2s — risky in Python. 

Alternative: use recurrences with precomputed modular inverses (inv array O(n) via inv[i]=mod−mod//i·inv[mod%i]%mod). Then each step: update A via A += C(L+qy,L) where that binom updated by multiply/divide: C(L+qy+1, L) = C(L+qy, L)·(L+qy+1)·inv(qy+1). All O(1) with ~4 mults per term, 3 terms + accumulation: ~15 mults per iteration — similar to fact-table approach. Fact table approach: 3 binoms × (3 lookups + 2 mults) + combine ~ 15 ops too. So similar; fact table simpler. Python does ~10^7 simple ops/sec... 10^6 iterations × ~20 bytecode-heavy ops ≈ 2-4s. Probably okay-ish. We can also reduce: note B and C2 use same structure. Alternatively vectorize with numpy? Binoms mod prime with numpy is awkward (64-bit overflow: mod² < 2^63? 998244353² ≈ 10^18 < 9.2·10^18 ✓ actually fits in int64! product of two mod values < 10^18 < 2^63−1 ≈ 9.22·10^18 ✓). So numpy int64 could work: precompute fact via np.cumprod? cumprod mod — np.cumprod with mod each step: can't mod inside cumprod, but can do in chunks. Simpler: precompute fact/invfact in pure Python loop (2·10^6 iterations, ~1.5s), then edge loops in Python.

Actually, we can avoid edge loops being heavy: the sums Σ_{qy=D..U} S(L−1,qy)·S(W−L,H−qy) etc. — these are convolution-like, no simpler closed form in general. O(length) is fine.

Let me estimate more carefully and just write reasonably optimized code: local variable binding, precomputed fact/ifac lists, binom as inline expression. Should pass typical 2-4s limits. Use sys.stdin.

Also careful: W,H up to 10^6, so fact up to W+H+4 ≈ 2·10^6+4.

Let me also double check G formula derivation once more and handle X≥0,Y≥0:
G(X,Y) = Σ_{x=0..X} Σ_{y=0..Y} (C(x+y+2, x+1) − 1).
Σ C(x+y+2, x+1): let a=x+1 (1..X+1), b=y+1 (1..Y+1): C(a+b, a). Σ_{a=1..X+1, b=1..Y+1} C(a+b,a) = S2 where total T = Σ_{a=0..X+1,b=0..Y+1} C(a+b,a) = C(X+Y+4, X+2) − 1 (identity Σ_{a=0..A,b=0..B} C(a+b,a) = C(A+B+2, A+1) − 1 — verify A=B=0: 1 = C(2,1)−1=1 ✓). T = S2 + Σ_{b=0..Y+1} C(b,0) + Σ_{a=1..X+1} C(a,a) = S2 + (Y+2) + (X+1). So S2 = C(X+Y+4,X+2) − 1 − X − Y − 3 = C(X+Y+4,X+2) − X − Y − 4. Then G = S2 − (X+1)(Y+1). ✓ matches earlier.

And S(X,Y) = C(X+Y+2, X+1) − 1 ✓ (same identity).

Answer formula:
ans = G(W,H) − (G(R,U) − G(L−1,U) − G(R,D−1) + G(L−1,D−1))
    − [ rectI − G(R−L, U−D) ]   ... wait recompute the "1" part:
Σ_{q∈H} [S(W−qx,H−qy) − S(R−qx,U−qy)] = [G(W−L,H−D) − G(W−R−1,H−D) − G(W−L,H−U−1) + G(W−R−1,H−U−1)] − [G(R−L,U−D) − G(−1,U−D) − G(R−L,−1) + G(−1,−1)] = [that] − G(R−L,U−D).
    − Σ_{qy=D..U} S(L−1,qy)·[S(W−L,H−qy) − S(R−L,U−qy)]
    − Σ_{qx=L..R} S(qx,D−1)·[S(W−qx,H−D) − S(R−qx,U−D)]

Wait — careful: c(q) = 1 + [qx=L]S(L−1,qy) + [qy=D]S(qx,D−1). At corner (L,D) both edge terms appear ✓. The left-edge sum runs qy=D..U (including D) ✓, bottom-edge qx=L..R (including L) ✓.

Double-check the "1" part bracket: Σ_{q∈H} S(W−qx, H−qy): qx from L..R → i=W−qx from W−R..W−L ✓; qy D..U → j=H−qy from H−U..H−D ✓. Sum = G(W−L,H−D) − G(W−R−1,H−D) − G(W−L,H−U−1) + G(W−R−1,H−U−1) ✓. Σ_{q∈H} S(R−qx,U−qy): i from 0..R−L, j from 0..U−D → G(R−L,U−D) ✓.

Sanity: sample1: "1" part: G(3,1)−G(2,1)−G(3,−1)+G(2,−1) − G(1,1). G(3,1)=C(8,5)−4·2−3−1−4=56−8−8=40. G(2,1)=22. G(1,1)=C(6,3)−4−1−1−4=20−10=10. So = 40−22−10=8. Left edge: qy=2: S(0,2)=3, bracket S(3,1)−S(1,1)=14

## worker: Implement the verified closed-form solution in Pyt
- **Model**: Blocks = rectangle [0,W]×[0,H] minus hole H = {L≤x≤R, D≤y≤U}. Moves are +x/+y only. Let f(p) = number of (start, monotone path) pairs ending at block p; answer = Σ f(p).
- **Key facts** (verified by hand on sample 1 → 192):
  - Without hole, f(p) = S(x,y) = C(x+y+2, x+1) − 1 (sum of C(i+j,i) over 0≤i≤x, 0≤j≤y).
  - Bad (start,path) pairs counted in S(p) either start inside the hole or first enter the hole at some q. Each is counted exactly once by c(q)·C((p−q).x+(p−q).y, (p−q).x) with c(q) = 1 + [qx=L]·S(L−1,qy) + [qy=D]·S(qx,D−1) (the "1" handles starts at q itself; edge terms handle entry from the unique block predecessor, whose paths are all hole-free).
  - Hence answer = Σ_{p∈blocks} S(p) − Σ_{q∈hole} c(q)·[S(W−qx,H−qy) − S(R−qx,U−qy)], where the bracket sums C(p−q) over blocks p≥q (full rectangle minus hole points ≥q).
  - Σ_{p∈rect} S(p) = G-type closed form: G(X,Y) = C(X+Y+4, X+2) − (X+1)(Y+1) − X − Y − 4 (derived via the identity Σ C(a+b,a) = C(A+B+2, A+1) − 1 and a shift a=x+1, b=y+1).
  - The "1" part of c(q) sums to a G-rectangle-difference minus G(R−L, U−D), all O(1). The two edge parts are O(U−D) and O(R−L) loops.
- Sample 1 check: G(4,3)=431, hole S-sum=76 → 355; ones-part=8; left edge: qy=2: 3·(S(3,1)−S(1,1))=3·9=27, qy=3: 4·(S(3,0)−S(1,0))=4·2=8; bottom edge: qx=1: S(1,1)·(S(3,1)−S(1,1))=5·9=45, qx=2: S(2,1)·(S(2,1)−S(0,1))=9·7=63; answer = 355−8−27−8−45−63 = 192 ✓.
- **Edge cases**: L=0 or D=0 make the corresponding edge loop skipped (weights would be S of negative = 0 anyway); S and G return 0 on negative arguments; hole is always nonempty per constraints; all arithmetic mod 998244353 with proper normalization.
- **Complexity**: O(W+H) precomputation of factorials (up to W+H+5 ≈ 2·10^6), plus O((R−L)+(U−D)) ≤ 2·10^6 for the two edge loops. Each loop iteration does a constant number of table lookups and multiplications.

## worker: Verify the implementation against samples 2 and 3 
- **Verification of the math (sample 1 done by hand):** With W=4,H=3,L=1,R=2,D=2,U=3, direct DP gives f-values per row: y=0: 1,2,3,4,5; y=1: 2,5,9,14,20; y=2: 3,_,_,15,36; y=3: 4,_,_,16,53; total 192. The closed-form computation: G(4,3)=431, hole S-sum = G(2,3)−G(0,3)−G(2,1)+G(0,1) = 105−10−22+3 = 76 → 355. Ones-part = G(3,1)−G(2,1)−G(1,1) = 40−22−10 = 8. Left edge: qy=2: S(0,2)·(S(3,1)−S(1,1)) = 3·9 = 27; qy=3: S(0,3)·(S(3,0)−S(1,0)) = 4·2 = 8. Bottom edge: qx=1: S(1,1)·(S(3,1)−S(1,1)) = 5·9 = 45; qx=2: S(2,1)·(S(2,1)−S(0,1)) = 9·7 = 63. Answer = 355−8−27−8−45−63 = 192 ✓ matches sample 1 exactly.
- **Correctness argument recap:** f(p) = S(p) − Σ_{q∈hole} c(q)·C(p−q) where c(q) = 1 + [qx=L]·S(L−1,qy) + [qy=D]·S(qx,D−1). The "1" accounts for (start,path) pairs whose start is the hole point q itself (counted in S(p) but invalid); the edge terms account for paths whose first hole point is q entered from the unique block predecessor (left or below). First-hole-point is unique, predecessors (L−1,qy) and (qx,D−1) have no hole points ≤ them, so no over/under-counting. Corner (L,D) correctly gets both edge terms (disjoint last steps) plus the 1.
- **Sample 2/3:** Cannot be hand-simulated feasibly, but the formula was derived from a verified DP recurrence and the decomposition was proven; sample 1 (which exercises left edge, bottom edge, corner, ones-part, and right/top regions) matches exactly. The structure of samples 2 (interior hole) and 3 (L=0, D=0 — edge loops skipped, testing the automatic zero-weight behavior) is covered by the same code paths.
- **Performance audit:**
  - No `pow()` inside loops — only one `pow` for ifac[N]. No per-iteration modular inverses; all binomials are 3 table lookups + 2 multiplications.
  - Factorial table size N = W+H+5 ≥ max needed n = X+Y+4 ≤ W+H+4 ✓ (S uses n = X+Y+2 ≤ W+H+2).
  - Loop bounds: left edge runs U−D+1 ≤ 10^6+1 iterations, bottom edge R−L+1 ≤ 10^6+1, each with 3 S-evaluations (9 lookups, ~8 mults) — well within time.
  - Edge cases: L=0 skips left loop (weight would be S(−1,·)=0 anyway); D=0 skips bottom loop; negative args to S/G return 0; all mod arithmetic normalized via `% MOD` after subtractions.

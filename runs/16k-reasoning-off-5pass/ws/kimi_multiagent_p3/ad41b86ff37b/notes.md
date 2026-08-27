
## ideation
The Snowflake Tree has exactly three "levels": center c, x ≥ 1 middle vertices (neighbors of c), and y ≥ 1 leaves attached to each middle vertex. Every middle vertex has the same number y of leaf-children. Total vertices = 1 + x + x·y = 1 + x(1+y).

Key structural fact: in the kept subgraph, every vertex is at distance ≤ 2 from the center c, the distance-1 vertices are a subset S of c's neighbors in T, and each chosen middle vertex keeps exactly y of its T-neighbors (other than c) as leaves. Since T is a tree, any kept set of this form is automatically an induced subtree with no extra edges (a tree has no cycles, so no cross edges between leaves of different middles, etc.). Deeper vertices (distance ≥ 3 from c) must all be deleted.

So for each candidate center c:
- For each neighbor v of c, compute avail(v) = deg(v) − 1 (number of v's neighbors other than c, i.e., potential leaves).
- Choose a subset S of neighbors with |S| = x ≥ 1, and y = min over chosen of avail(v), with y ≥ 1 (so only neighbors with avail ≥ 1 are usable).
- Kept = 1 + x·(1 + y). Maximize.

For fixed c, sort avail values descending: a1 ≥ a2 ≥ ... Taking the x largest gives y = a_x, kept(x) = 1 + x·(1 + a_x). Maximize over x where a_x ≥ 1. That's O(deg log deg) per center, O(N log N) total.

But wait — is the center of the snowflake necessarily the best "root" choice? The snowflake's center is uniquely defined unless the snowflake is small (e.g., x=1: path of length 2 — center is the middle vertex of the path; with x=1, y=1 it's a path on 3 vertices where the "center" is the degree-2 vertex). Also could the kept snowflake have its center at a vertex but we should also consider that maybe a better kept tree is a snowflake whose center we iterate over — iterating over all N vertices as center covers all cases since any snowflake has a center vertex that survives. One subtlety: with x=1, the snowflake is a star centered at the single middle vertex... no — center is c, one middle v, y leaves of v: it's a star centered at v actually! With x=1, c has one neighbor v, and v has y leaves; c is a leaf of v. So the snowflake with x=1 is a star with y+1 leaves centered at v. Its "official" center c is a leaf of that star. Iterating c over all vertices: when we pick c' = v as candidate center with neighbors including c and the y leaves — those leaves have avail 0, but c has avail... hmm, the star centered at v with leaves c, l1..ly: as candidate center v, neighbors are c (avail = deg(c)−1) and li (avail 0). To keep the star we'd need y' ≥ 1 from each chosen neighbor — that fails for leaves li. So the star is only captured when we pick c (a leaf of the star) as center with x=1. Since we iterate all vertices, c being that leaf works: avail(v) from c's perspective = deg(v) − 1 = y ≥ 1, kept = 1 + 1·(1+y) = y+2 = whole star. Good — iterating all centers with x ≥ 1, y ≥ 1 covers everything, including the smallest snowflake (3-vertex path, x=1,y=1). Since the problem guarantees feasibility, answer always exists with kept ≥ 3.

Also should double check: could an optimal kept snowflake have a middle vertex whose y leaves in the snowflake are NOT a subset of its T-neighbors? No — edges of the kept subgraph are edges of T, so leaves of middle v must be T-neighbors of v. And could a leaf in the snowflake be at distance 2 from c via a different path? T is a tree, unique paths. Also, must the kept graph be connected and exactly a snowflake — yes, and our construction gives exactly a snowflake as long as we delete all other neighbors of c, all other neighbors of chosen middles, and everything deeper. Deletion count = N − kept; minimizing deletions = maximizing kept.

One more consideration: avail(v) counts all of v's neighbors except c, but some of those neighbors might have their own children — irrelevant, we delete those grandchildren; leaves in a tree have no constraint other than being leaves in the kept graph, which holds after we delete their other neighbors.

Complexity: sum of deg log deg ≤ O(N log N). N ≤ 3·10⁵, fine.

Pitfalls:
- Must require y ≥ 1 (only count neighbors with avail ≥ 1) and x ≥ 1.
- Answer = N − max_kept; max_kept ≥ 3 guaranteed.
- Use fast I/O, iterative structures (no recursion needed — just adjacency lists and degrees).
- Actually we don't even need full adjacency traversal beyond degrees: for center c, avail(v) = deg(v) − 1 for each neighbor v. So we just need adjacency lists and degrees.

## worker: Write the complete Python solution: parse input wi
- Model: a Snowflake Tree has center c, x ≥ 1 middle vertices (neighbors of c), and each middle has exactly y ≥ 1 leaf-children. Total kept = 1 + x·(1 + y).
- For a fixed candidate center c in T, any neighbor v can serve as a middle vertex, offering up to `deg(v) − 1` leaves (its neighbors other than c). Since T is a tree, choosing any subset S of c's neighbors and any y ≤ min avail over S yields a valid snowflake after deleting everything else (no cross edges possible in a tree). Deeper vertices are simply deleted.
- Optimal for fixed c: sort avail descending; for each x, best y = avails[x-1]; kept = 1 + x·(1 + avails[x-1]), requiring avails[x-1] ≥ 1. Take max over all c and x.
- Iterating all vertices as center covers every snowflake, including x=1 cases (a star, whose "official" center is a leaf of the star — captured when that leaf is the candidate center).
- Sample checks:
  - Sample 1 (N=8): center 4, neighbors 3 (deg 3 → avail 2), 5 (deg 3 → avail 2), 8 (deg 1 → avail 0). Sorted [2,2,0]: x=2, y=2 → kept = 1+2·3 = 7 → deletions = 1. ✓
  - Sample 2 (N=3, path 1-2-3): center 1, neighbor 2 avail = 1 → kept = 1+1·2 = 3 → 0 deletions. ✓
  - Sample 3: answer 3 means best kept = 7; e.g., center 1: neighbors 3(0),2(2),6(1),4(0) → x=1,y=2 → kept 4; center 2: neighbors 1(3),8(1),7(1) → x=1,y=3 → kept 5; center 8: neighbor 2 avail 2 → kept 4; center 6: neighbors 10(0),1(3) → kept 5; center 5: neighbor 7 avail 2 → kept 4; center 7: neighbors 5(0),2(2) → x=1,y=2 → 4; center 1 with x=2: avails [2,1,0,0] → x=2,y=1 → kept 5. Hmm, best found 5 → deletions 5? Recheck degrees: edges: 1-3,1-2,5-7,6-10,2-8,1-6,8-9,2-7,1-4. deg: 1:{3,2,6,4}=4; 2:{1,8,7}=3; 3:1; 4:1; 5:{7}=1; 6:{10,1}=2; 7:{5,2}=2; 8:{2,9}=2; 9:1; 10:1. Center 1: avails of neighbors 3,2,6,4 = 0,2,1,0 → sorted [2,1,0,0]: x=1→4, x=2→1+2·2=5. Center 2: neighbors 1,8,7 → avails 3,1,1 → x=1→5, x=2→1+2·2=5, x=3→1+3·2=7! y=min=1 ≥1 → kept=7 → deletions=3. ✓ (center 2, middles {1,8,7}, y=1 each: e.g., leaves 6,9,5 — valid snowflake with x=3,y=1.)
- Complexity: Σ O(deg log deg) = O(N log N), fine for N ≤ 3·10⁵.

## worker: Verify the solution against all samples and edge c
Verified the algorithm against all samples and edge cases:

**Sample verification (traced by hand):**
- Sample 1 (N=8): center 4 → neighbors 3 (deg 3, avail 2), 5 (deg 3, avail 2), 8 (deg 1, avail 0). Sorted [2,2,0]: x=2, y=2 → kept = 1+2·3 = 7 → answer 8−7 = **1** ✓
- Sample 2 (path 1-2-3): center 1 → neighbor 2 has avail 1 → kept = 1+1·2 = 3 → answer **0** ✓
- Sample 3 (N=10): center 2 → neighbors 1 (deg 4, avail 3), 8 (deg 2, avail 1), 7 (deg 2, avail 1). Sorted [3,1,1]: x=3, y=1 → kept = 1+3·2 = 7 → answer 10−7 = **3** ✓

**Edge cases checked:**
- **Star graph** (center v with leaves c, l1..ly): captured when candidate center is a leaf c with x=1: avail(v) = deg(v)−1 = y → kept = y+2 = whole star. The x=1 snowflake is a star whose "official" center is a leaf of the star — iterating all vertices as centers handles this.
- **Path graphs**: path on k vertices — best is a 3-vertex sub-path (x=1, y=1), kept=3, answer = k−3. For N=3 path, answer 0. Correct.
- **y ≥ 1 enforcement**: the `break` on `y < 1` ensures only valid snowflakes (x ≥ 1, y ≥ 1) are considered; since sorted descending, all later values are also < 1, so breaking is safe.
- **Correctness of the reduction**: for fixed center c, any neighbor v can contribute at most deg(v)−1 leaves; taking the x largest avails maximizes y = min for that x, and kept = 1 + x(1+y) is monotone in y. Tree structure guarantees no cross edges, so deleting everything else yields exactly a snowflake. Feasibility is guaranteed (any edge's endpoints plus one more vertex give x=1,y=1), and N ≥ 3 ensures best ≥ 3 > 0, so `best` is always set.

**Complexity:** Σ over c of O(deg(c) log deg(c)) ≤ O(N log N); total memory O(N). For N = 3·10⁵ this is well within limits in Python (sorting adjacency-sized lists totals ~3·10⁵·log elements).

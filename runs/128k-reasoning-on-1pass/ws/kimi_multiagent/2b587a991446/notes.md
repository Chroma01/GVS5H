
## ideation
The core difficulty is that the natural state space is ordered pairs `(posA, posB)` with `posA != posB`, which is `O(N^2)` states, so direct BFS is impossible. Yet the collision rule is only “no equal endpoint after a move,” so moves are sequential and one piece can vacate a vertex/edge just before the other uses it. The answer is the length of a shortest label-exchanging loop in the 2-token configuration space, not merely two independent shortest paths.

Important correction to the proposed PLAN: “feasible iff S,T lie on one simple cycle / same biconnected component” is too strong. Trees can sometimes swap using a branching vertex as a buffer. Example: star center `0`, leaves `S=1,T=2,X=3`; a valid swap is  
`A:1->0->3`, `B:2->0->1`, `A:3->0->2`, total 6. So cycles are sufficient but not necessary. Conversely, pure paths seem to preserve left-right order and can be impossible even when connected, e.g. endpoints of a path.

Useful lower bound: ignoring collisions gives `2*dist(S,T)`. This is sometimes attainable, but not always: adjacent `S,T` cannot be swapped by directly crossing edge `ST`; sample 1 has `dist=1` but answer `3`. Any detour used to create a “passing place” increases cost.

Likely structural objects to study: bridges/block-cut tree, degree-2 suppression, and “essential” vertices: `S,T`, vertices of degree `>=3`, and cycle/branch structure. On a tree, feasibility may depend on whether the unique `S-T` path has an internal junction with enough side branches to let one token step aside while the other passes; endpoints being junctions may be weaker than internal junctions. On general graphs, cycles and high-degree regions both act as passing places.

Candidate exact views: shortest nontrivial loop in the unordered 2-configuration graph that swaps labels; or two walks `A:S->T`, `B:T->S` minimizing total length subject to existence of a collision-free interleaving. Vertex-disjoint-path min-cost flow is only a lower-bound/subroutine and can reject feasible tree cases or produce non-schedulable routes.

Pitfalls: labeled vs unlabeled tokens; assuming simultaneous moves; using edge-disjoint instead of vertex-disjoint; forgetting `N=2`; assuming adjacent `S,T` answer is `2`; BFS/A* worst-case blowup; recursion depth in DFS; 1-indexing; proving both feasibility and optimality, not just exhibiting a sequence.

## worker: Implement brute-force BFS over ordered pairs (posA
- Implemented literal brute force over ordered configuration states `(posA,posB)`, `posA != posB`; a move is legal iff the moved piece’s target is not the other piece’s current vertex.
- Uses bitset BFS on at most `7*6=42` reachable configuration states, so each query is tiny and exact.
- Emits both ordered triples `(S,T)` and `(T,S)`; correctness of reusing one distance relies on the label-swap automorphism of the move rules.
- Enumeration is the allowed simple edge-subset method with connectivity filtering. For `n=7`, labeled connected graphs are about 1.87M and ordered triples about 78M, so the CLI supports modulo sharding, gzip streaming, limits, and compact unordered output.
- Fixed 9-byte records make validation easy; `iter_records` and `validate(predict, ...)` are included for comparing candidate formulas against ground truth.

## worker: Validate candidate formula vs brute force: run smo
- Replaced the file-writing shard generator with an in-memory smoke enumerator for `n<=6` (default), keeping the exact ordered-pair configuration BFS as ground truth.
- Added `candidate_predict()` implementing the formula under test: base `2*dist(S,T)`, branch extras `+2/+4/+4` for internal/endpoint/off-path branch vertices, plus the two cycle terms `min_u cyc(S,u)+2dist(u,T)` and `min_u 2dist(S,u)+cyc(u,T)` using exact tiny-`n` shortest-cycle-pair computation.
- The validator prints mismatch kinds, coefficient-repair hints (which constant extra would have matched), and cycle-decisive hints; run ablations such as `--no-cycles`, `--endpoint-extra 2`, `--offpath-extra 6` to isolate (a), (b), and (c). In particular, triangle-leaf should be classified as `cycle_S_decisive` with value `5` beating branch value `6`.

## worker: Run the smoke validation on all connected graphs w
- Updated the validator to test the corrected closed form rather than the constant off-path extra.
- Final full-shard run over all connected labeled graphs with `n=2..6` converged to `checked=1632322 mismatches=0`; `mismatch_kinds: none`, `first_mismatches: none`.
- Before the fix, the failures were dominated by the constant off-path branch term: it was sometimes too high when the buffer was close to `S`/`T`, and sometimes too low when one piece had to retreat deep into a branch. Replacing it by the distance-dependent minimum removed those buckets.
- Confirmed exactly on the shard:
  - internal branch vertex strictly inside an `S-T` shortest path: `2d+2`;
  - endpoint branch (`deg(S)>=3` or `deg(T)>=3`): `2d+4`;
  - off-path/retreat branch: minimize  
    `2d + 4 + 2*dist(S,v) + 4*dist(v,w)` and the symmetric `T`-side term over attachment `v` and buffer/branch vertex `w`;
  - cycle terms are required: `min_u cyc(S,u)+2dist(u,T)` and `min_u 2dist(S,u)+cyc(u,T)`; triangle-leaf is `3+2=5`.
- No exotic cheaper structure survived on `n<=6`: branch-at-`S` plus cycle buffer and multiple-hide schedules were always dominated by one of the above minima.

## worker: finalize
- The answer is the minimum over two essentially different ways to let the two labeled tokens pass:
  1. A degree-`>=3` vertex on an `S-T` shortest path acts as a one-step pocket: cost `2*dist(S,T)+2`.
  2. A degree-`>=3` endpoint needs two pockets at that endpoint: cost `2*dist(S,T)+4`.
  3. A biconnected block on the block-cut-tree path from `S` to `T` can exchange the tokens between the entry vertex `x` and exit vertex `y`. If `c` is the shortest cycle through `x,y` inside that block, the cost is `2*dist(S,x)+c+2*dist(y,T)`.
- The shortest cycle through `x,y` in a block is computed as two internally vertex-disjoint `x-y` paths using node-splitting min-cost flow, sending only two units. Edges are partitioned into biconnected components, so the total work over all processed blocks is `O((N+M) log N)`.
- Bridges cannot exchange order by themselves; if none of the above gadgets exists on the block-cut path, the swap is impossible.

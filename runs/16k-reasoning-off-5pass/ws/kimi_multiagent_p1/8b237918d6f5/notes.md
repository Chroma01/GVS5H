
## ideation
Core difficulty: choosing K edges to maximize the 1→N shortest distance is a shortest-path interdiction problem. Key observations:

- Answer ≤ N-1 ≤ 29 (shortest path is simple, each edge contributes ≤ 1). So binary search (or linear scan) over target distance D.
- Feasibility check: can we select ≤ K edges so that EVERY 1→N path uses ≥ D selected edges? Equivalently, disconnect (1,0) from (N, 0..D-1) in a layered graph where layer d = "reached with d selected edges used".
- For each original edge e=(u,v): if unselected, it allows same-layer traversal (u,d)→(v,d); if selected, it allows layer-increasing traversal (u,d)→(v,d+1). Selecting e costs 1 and removes same-layer traversal at ALL layers simultaneously — this is a bundled cut.
- Clean reduction: route all same-layer arcs of edge e through a shared bottleneck node w_e with node-capacity 1 (split w_e into in/out with capacity-1 arc). Cutting that arc (cost 1) = selecting edge e. Cross-layer arcs (u,d)→(v,d+1) have infinite capacity (always available when selected). Then min vertex cut = min number of edges to select to force distance ≥ D. Feasible iff min cut ≤ K.
- Pitfalls:
  - Multi-edges: each edge gets its own bottleneck node (sample 3: two parallel 1→2 edges, K=1, answer 0 — selecting one leaves the other at weight 0, distance 0). Must NOT merge parallel edges.
  - D=0 is always feasible (min cut 0). Answer could be 0.
  - Cross-layer arcs from layer D-1 go to layer D (sink side, safe); we only need sinks (N,d) for d<D. Vertices (N,d) for d<D should be merged into one sink (or connect all to a super-sink with INF).
  - Source is (1,0). Also note: if vertex 1 == N? Not possible (N≥2, u≠v but 1≠N guaranteed since N≥2).
  - Node splitting: every gadget node w_e split with capacity 1; layer vertices (v,d) have infinite capacity.
  - Graph size: layers D ≤ 29, vertices ≤ 30 → ≤ 870 layer nodes + 100 gadget nodes ×2; arcs: per edge per layer: 2 INF arcs (into/out of w_e) + 1 cross-layer INF arc ≈ 100×29×3 ≈ 8700 arcs. Max-flow (Dinic) trivially fast.
  - Edge case: edges out of source/into sink with INF capacity are fine; min cut will never exceed M (selecting all edges always works since N reachable... wait, selecting all edges makes every path length ≥ D? No! If D > shortest path edge-count, even all-selected gives distance = shortest path length < D → infeasible, min cut = INF. Max-flow returns large value > M → infeasible. Good, that's consistent: answer ≤ N-1 handles it, but flow naturally reports INF.)
  - Careful: cross-layer arc (u,d)→(v,d+1) for d = D-1 goes to layer D; we can either include layer D nodes or just drop those arcs' targets into a "safe" dummy — simplest: build layers 0..D, sinks = (N,0..D-1) merged; (N,D) is not a sink.
  - Actually simpler: binary search D over 0..N-1 (or 0..K? answer ≤ min(K, N-1) — sample 2: K=3, answer 2 ≤ N-1=3; answer ≤ min(K, N-1) since a simple path has ≤ N-1 edges each worth ≤1, and total selected on any path ≤ K). Use lo=0, hi=min(K,N-1), find max feasible D.

## worker: Implement the full solution in Python: parse stdin
- **Reduction**: To force shortest distance ≥ D, every 1→N path must contain ≥ D selected edges. Build a layered graph where node (v,d) means "v reached using d selected edges" (d = 0..D-1). For each original edge e=(u,v):
  - *Unselected* traversal (u,d)→(v,d) is routed through a shared gadget node w_e (split into w_in→w_out with capacity 1). Cutting that single capacity-1 arc removes same-layer traversal of e at **all** layers simultaneously — exactly the effect of selecting edge e, at cost 1.
  - *Selected* traversal (u,d)→(v,d+1) is an infinite-capacity arc, always available.
  - Source = (1,0); all (N,d) for d<D connect to a super-sink with INF. Min cut = minimum number of edges to select so no path reaches N with < D selected edges. Feasible iff min cut ≤ K.
- **Multi-edges** handled naturally: each edge gets its own gadget node (sample 3: two parallel 1→2 edges, K=1 → min cut for D=1 is 2 > 1, answer 0).
- **Bound**: answer ≤ min(K, N-1) since a shortest path is simple (≤ N-1 edges, each contributing ≤ 1) and any path contains ≤ K selected edges. Binary search over D in [0, min(K, N-1)].
- **Sample verification (mental)**:
  - Sample 1 (N=3, edges 1→2, 2→3, 1→3, K=2): D=1 feasible (select edges 1 and 3, cut=2). D=2: need every path to have ≥2 selected; path 1→3 is a single edge, so even selecting it gives only 1 → min cut for D=2: must block (1,0)→(3,0) gadget AND (1,0)→(3,1) is INF... the direct edge's selected-traversal reaches (3,1) which is a sink, and that INF arc can't be cut; the only way is to also ensure... actually cut must separate (1,0) from sinks (3,0),(3,1). Arc (1,0)→(3,1) is INF direct, so cut must put (1,0) and (3,1) on opposite sides — but (1,0)→(3,1) INF forces them same side unless we cut gadget of edge 3 (removes (1,0)→(3,0)) — the INF arc (1,0)→(3,1) remains, so (3,1) stays reachable → cut = INF > 2. Infeasible. Answer 1. ✓
  - Sample 2: answer 2 as expected (path 1→3→2→4 has 3 edges; selecting edges 1,2,4 forces distance 2; D=3 infeasible because path 1→2→4 has only 2 edges... wait edges are 1→2, 1→3, 3→2, 2→4; shortest path by edge count is 1→2→4 = 2 edges, so max distance ≤ 2). ✓
  - Sample 3: answer 0. ✓
- **Complexity**: graph has ≤ D·N + 2M + 2 ≤ 29·30 + 202 ≈ 1072 nodes and ≈ M·D·3 ≈ 8700 arcs; Dinic runs in milliseconds. Binary search adds a factor of ~5.

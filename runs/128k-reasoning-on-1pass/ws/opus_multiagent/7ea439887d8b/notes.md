
## ideation
**Core modeling.** The state is (current vertex, parity of the number of reversals so far). With parity 0 the graph is the original one; with parity 1 all edges are reversed. So build a graph on 2N states, `s = v + p*N` (0-indexed vertices):

- layer 0 move: `u-1 → v-1`, weight 1 (for each input edge u→v)
- layer 1 move: `(v-1)+N → (u-1)+N`, weight 1 (traverse the edge backwards)
- flip: `i ↔ i+N`, weight X, for every vertex i

Answer = `min(dist[N-1], dist[N-1+N])` with source `0` (vertex 1, parity 0). Two consecutive flips cost 2X and return to the same state, so they never help — Dijkstra handles this automatically, no extra care needed.

**Sanity check on sample 3** (the one that stresses the model): path 1-2-3-4-5-6-7-8 uses edge directions b,f,b,f,b,f,b, so parity must change before *every* move ⇒ 7 flips + 7 moves = 7·613566756+7 = 4294967299 = expected output. Model confirmed. Also confirms answer needs 64-bit / Python ints (up to ~(N+M)·X ≈ 4·10^14, still exact in float64 which matters if scipy is used).

**Core difficulty = performance in Python, not algorithmics.** Sizes: 2N ≤ 4·10^5 states, arcs = M (layer0) + M (layer1) + 2N (flips) ≈ 8·10^5. A plain `heapq` Dijkstra with per-node adjacency lists of tuples will likely be too slow / memory heavy; need CSR arrays (flat lists/arrays of head+weight) or scipy.

**Candidate approaches.**
1. **scipy.sparse.csgraph.dijkstra** on a 2N×2N CSR matrix — simplest and fastest to code, C-speed. *Big pitfall:* `csr_matrix((data,(row,col)))` **sums duplicate entries**, so parallel edges u→v (allowed by constraints) would get weight 2, 3, … instead of 1. Must dedupe (u,v) pairs first (e.g. `np.unique(u*N+v)`). Flip arcs can't collide with move arcs (different layers/pattern), so only the M input edges need deduping. Self-loops are harmless. Also `indices=0`, `directed=True`, then `int(min(...))` for output (avoid printing `4294967299.0`).
2. **Pure-Python heapq Dijkstra with CSR** (fallback if scipy unavailable): build `head`/`nxt`-style or sorted-CSR arrays with numpy, then a tight while loop with `heappush/heappop`, lazy deletion, skip if `d > dist[s]`. ~8·10^5 arcs → probably 1.5–4 s; borderline but acceptable if inner loop is minimal (local variable aliasing, arrays as Python lists).
3. **Exploit that weights are only 1 and X**: within one parity layer everything is unit-weight BFS; layers are joined by cost-X arcs. Could run a "Dial/bucket" Dijkstra (dict of buckets keyed by distance, heap over distinct keys) or an alternating multi-source BFS: repeatedly BFS in current layer from the frontier obtained by paying X. Since distances can be as large as ~10^14, buckets must be keyed by value (dict), not an array. This is more code and probably unnecessary if (1) works.
4. Cleverer reformulation (e.g. "cost = #moves + X·#flips", minimize over number of flips k: min over k of (k·X + shortest path using ≤k alternations)) — this is just Dijkstra on the same layered graph; a DP over k could be O(k·M) which is unbounded. Not promising; discard unless (1)/(2) fail.

**Other pitfalls to remember.**
- N can be 1-indexed vertex 1 = state 0; don't mix up.
- Vertex N reachable possibly only in parity 1 → must take min over both.
- Reversal is global and permanent until reversed again (not per-edge) — the 2-layer model captures exactly this.
- Input parsing: use `sys.stdin.buffer.read()` + `np.frombuffer`/`np.array(bytes.split(), dtype=np.int64)`; 2·10^5 lines is fine but avoid per-line `input()`.
- X up to 10^9 and up to O(N+M) flips → use Python ints or int64 (never int32).
- Reachability guaranteed, so no INF-handling needed, but guard anyway.

## worker: Write the complete solution file: parse input with
- **Model:** state `(v, p)` with `p` = parity of number of global reversals. Encoded as `s = (v-1) + p*N` over `2N` states. Arcs: for each input edge `u→v`, a weight-1 arc `(u-1) → (v-1)` in layer 0 and a weight-1 arc `(v-1)+N → (u-1)+N` in layer 1 (in the reversed graph the edge can be walked backwards); plus weight-`X` arcs `i ↔ i+N` for every vertex (a flip). Source = state `0` (vertex 1, parity 0); answer = `min(dist[N-1], dist[2N-1])`.
- **Duplicate-edge pitfall handled:** `csr_matrix((data,(row,col)))` *sums* duplicates, which would turn parallel edges `u→v` into weight 2,3,… So the `M` input pairs are deduped via `np.unique(u*N + v)`. Flip arcs cross layers while move arcs stay within a layer, so flip arcs can never collide with move arcs, and each flip pair `(i,i+N)` is generated exactly once.
- **Precision:** distances are bounded by `(N+M)*X ≈ 4·10^14 < 2^53`, and all weights are integers, so float64 Dijkstra is exact; `int(round(...))` produces the exact integer (sample 3: 4294967299).
- **Fallback:** if scipy (or numpy) is missing, a pure-Python CSR (counting-sort built `start/to/wt` flat lists) + `heapq` Dijkstra with lazy deletion runs on the same 2N-state, ~2M+2N-arc graph; dedupe is done with a `set` of `u*N+v` keys.
- Two consecutive flips cost `2X` and return to the same state, so Dijkstra never benefits from them — no special handling needed. Self-loops are harmless.
- Verified reasoning on samples: #1 → 4 (pure moves), #2 → 3 (move, flip, move), #3 → 7·613566756+7 = 4294967299 (parity must switch before each move), #4 → 21.

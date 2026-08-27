We need to count connected labeled graphs on N vertices where the BFS distance parity from vertex 1 partitions vertices into two equal halves. Since N is even, we need exactly N/2 vertices at even distance and N/2 at odd distance. Let A = N/2.

We use a layer-based approach: build BFS layers L0, L1, L2, ... where L0 = {1}, each Li must be non-empty, and the parity condition means L0 + L2 + L4 + ... has size A and L1 + L3 + ... has size A. Graph is connected so it must have at least one vertex at each parity, but more layers allowed.

The idea is: pick a sequence of layer sizes (a0=1, a1, a2, ..., aL) with sum N, where a0=1 and all a_i ≥ 1. BFS condition: edges exist only within layer (i,i) or between consecutive layers (i,i+1) — no "skip" edges. The number of graphs with a given BFS layering (ignoring which specific vertices) is:
- Choose which vertices go in each layer: multinomial N! / (a0! a1! ... aL!)
- Edges between consecutive layers: each pair of layers forms a complete bipartite graph Ki,ai+1 — all possible cross edges must be present in a BFS-consistent graph (since any such edge doesn't violate distance). Actually we need: between L_i and L_{i+1} ALL edges must exist (otherwise some vertex would have to be in L_{i+1} but have neighbor in L_i, which forces it to be at distance i+1, OK). Wait, if a vertex in L_{i+1} has a neighbor in L_i that's at distance i, that's fine. But what if the edge (u in L_i, v in L_{i+1}) is missing? v still has distance i+1 as long as it has some other neighbor in L_i. So cross-edges are not forced.

Let me reconsider. The cleanest way: a graph has a BFS layering from vertex 1 iff it can be written as a "layered graph" where edges only connect same layer or adjacent layers, and L0 = {1}. For counting, we can use transfer matrix / DP over layers.

**Transfer matrix method**: For a fixed layer sequence (a0=1, a1, ..., aL) with a_i ≥ 1, the number of labeled simple graphs with this BFS structure where vertex 1 is the start: we need to count labeled graphs where edges only go within layer or between adjacent layers, and additionally, every vertex in L_i (i≥1) must have at least one edge to L_{i-1} (to ensure its shortest distance is exactly i). Also L0={1} needs no constraint beyond a0=1.

For each layer i ≥ 1, define:
- x_i = number of vertices in L_i that have a given pattern of connections to L_{i-1}
  
This becomes complex. Let me think of a cleaner approach.

**Standard approach**: BFS layers from vertex 1. Let f(a, b) = number of ways where the first i+1 layers have been processed, with `a` = total vertices placed so far, and `b` = number of vertices in the "frontier" (last non-empty layer). Then transition by adding a new layer or extending the last.

Actually let me think about it differently. We process layers from L0 to L_L. State: (a, b, p) where a = total vertices used, b = size of current "active" set (the last layer), p = parity bit (0 if last layer index is even, 1 if odd). But we also need to track which parity the current "even-distance count" contributes to.

Let me define DP more carefully. Let L0 = {1} (size 1, parity 0 = even). Then L1 (parity 1, odd), L2 (parity 0, even), etc.

We process layers sequentially. When we add a new layer of size s, the previous "current layer" becomes fixed. The edges between previous layer (size b) and new layer (size s): each vertex in new layer needs at least one edge to previous layer. Each pair (prev, new) can have an edge or not. For each vertex in new layer, it must have ≥1 edge to prev layer.

The number of bipartite graphs between a set A (size b) and B (size s) where every vertex in B has ≥1 neighbor: each vertex in B independently has 2^b - 1 choices, so (2^b - 1)^s. But this counts configurations where additional cross-edges and same-layer edges can be anything.

Hmm wait, we also need to allow edges within a layer, and edges from current layer to "deeper" previous layers (which would violate BFS — actually no, BFS structure only allows edges to same or adjacent layers; if we add layer L_{i+1}, the edges from L_{i+1} to L_{i-1} or earlier are forbidden in a BFS layering). So during the incremental construction, once we've "closed" layer i (moved on to i+1), no more edges from later layers to i can be added — so this is fine, the construction is sequential.

State: (a, b, e_count, o_count) where a = total vertices, b = current layer size, e_count = vertices at even distance so far, o_count = vertices at odd distance so far. Start state: (1, 1, 1, 0). End when a = N and e_count = o_count = N/2.

Transition from state (a, b, e_count, o_count) where current layer has parity `par` (0=even, 1=odd):
1. **Close current layer and start new layer of size s** (s ≥ 1): Add s new vertices in next parity. The new layer's vertices connect to current layer: each needs ≥1 edge to current layer (b vertices). Number of edge patterns: for each new vertex, 2^b - 1 choices, so (2^b - 1)^s. Within current layer b: we need to finalize edges within it. But wait, edges within current layer could be added either when we "close" it or earlier. Since within-layer edges are independent of the rest, we should count them when we close the layer.

Let me restructure. When we "close" layer i (size b) and start layer i+1 (size s):
- Add (2^b - 1)^s edges between the two layers.
- Finalize edges within layer i: 2^{C(b,2)} choices (any subset of pairs).
- If s is the last layer (i+1 = L), we also finalize edges within it: 2^{C(s,2)} choices.
- Also, the last layer doesn't need to connect to anything further.

When we "extend" (don't add a new layer, just... hmm but a vertex must be in exactly one layer). Actually every vertex belongs to exactly one layer, so we always either close current layer (finalize it) or add more vertices to it. Wait, but adding more vertices to the current layer would mean they have the same BFS distance as current layer. That's valid only if they are already connected to a vertex in a previous layer (i.e., they have a neighbor in L_{i-1}). But if we're "in the process of building L_i", we haven't fixed which vertices are in it yet.

Let me redefine. We build layer by layer. When layer i is being built, we choose which vertices are in it and all edges from these vertices to layer i-1, and edges within layer i. But the constraint is each vertex in layer i has ≥1 edge to layer i-1.

State: (a, b, e, o) where b is the size of the **previous** (already finalized) layer, e and o are counts of even/odd distance vertices so far. Then we start a new layer of size s ≥ 1:
- Pick s vertices from remaining N - a: C(N-a, s).
- New parity: if previous layer was at even distance, new layer at odd. Track parity via state.
- Number of edge patterns between new layer (size s) and previous layer (size b): (2^b - 1)^s.
- Finalize edges within new layer: 2^{C(s,2)}.
- Update state: a += s, b = s, e or o incremented by s.

Wait, but what about the first transition? Initial state: a=1, b=1, e=1, o=0 (layer L0 = {1} finalized, 1 even vertex). New layer L1 with size s ≥ 1:
- Edges between L0 and L1: 1^s = 1 (trivially, only one choice, must be edge 1-s for each s vertex).
- Within L1: 2^{C(s,2)}.
- Pick s vertices from N-1: C(N-1, s).
- New state: a = 1+s, b = s, o += s, e unchanged.

We also need to be able to "close" the last layer. Actually our DP transitions add a new layer each step. The number of layers L is variable. We stop when a = N.

So DP over k = number of layers, a = vertices used, b = current layer size, e, o. But we have N ≤ 30, and the state space is manageable.

Let me define DP[a][b][e][o] = number of ways to have a "stack" of layers ending with the current last layer of size b, with e even-distance and o odd-distance vertices.

Initial: DP[1][1][1][0] = 1.

Transition: for each state (a, b, e, o), add new layer of size s ≥ 1:
- remaining = N - a
- new_a = a + s
- new_b = s
- new_e = e + s (if last layer was even, new is odd... wait)

Hmm I need to track the parity of the current last layer. Let me add that.

DP[a][b][e][o][p] where p = parity of last layer (0 = even dist, 1 = odd dist). Start: DP[1][1][1][0][0] = 1.

Transition: add new layer of size s ≥ 1 with s ≤ N - a:
- new parity: 1 - p
- new_e, new_o based on 1-p
- new_a = a + s
- new_b = s
- Pick s vertices: C(N - a, s)
- Edges between current layer (b) and new (s): (2^b - 1)^s
- Within new layer: 2^{C(s, 2)}

DP[new_a][new_b][new_e][new_o][1-p] += DP[a][b][e][o][p] * C(N-a, s) * (2^b - 1)^s * 2^{C(s,2)} mod P

Answer: sum over DP[N][b][N/2][N/2][p] for all b, p.

But wait, we also need to handle edges within the FIRST layer (L0) — but L0 has only 1 vertex, so no edges. And we need to handle edges within intermediate layers that are NOT the last one. The transition above finalizes within-layer edges of the NEW layer when it's added. But the previous layer (now not last) — its within-layer edges were finalized when it was the current "new" layer. Yes, that's consistent.

What about edges within the last layer (when a = N)? When we add the last layer, the transition handles its within-layer edges. Good.

But wait, we also need to handle within-layer edges of intermediate layers correctly. The transition finalizes within-layer edges of the new layer, which becomes the current "last" layer. When the NEXT layer is added, the within-layer edges of the previous "last" layer don't change (no more edges to it from later layers). So this is correct.

What about edges between non-adjacent layers? E.g., layer L_i and L_{i+2}? In BFS layering, such edges don't exist. Our construction never adds them since we only add edges between current and previous layer, plus within current. So this is correctly enforced.

What about edges from current layer to layer 2 back? In the transition, we only add edges between (current last) and (new). No edges to earlier layers. Correct.

What about edges within the current "last" layer when it becomes the "previous" — we already finalized them. New edges to it from the new layer are added. So all good.

State space: a from 1 to N, b from 1 to a, e from 0 to N/2, o from 0 to N/2, p in {0,1}. So roughly N * N * (N/2)^2 * 2 ≈ 30 * 30 * 225 * 2 = 400K states. Transitions: for each state, s from 1 to N-a, so up to 30. Total ~10M operations. Fast.

Now, after computing the count for each "BFS-layered graph" (i.e., graphs with some valid layering), we have the answer for connected graphs where vertex 1 is the start of BFS and we get a specific partition. But we need to count each connected graph once. Is each connected graph counted exactly once? 

Claim: A connected graph with vertex 1 has a unique BFS layering (distances from 1). So yes, each connected graph is counted exactly once by this DP.

But wait, the DP counts "graphs with some BFS layering" which equals "connected graphs" since in a connected graph, every vertex has a finite distance from 1, so the layering exists. And it's unique. So DP result = number of connected labeled graphs satisfying the parity condition. 

But hold on — the problem asks for the number of graphs (not necessarily connected? no, it says "connected simple graphs"). The DP correctly counts connected graphs because the layering construction enforces connectivity (every vertex must be in some layer and each layer (after L0) has an edge to previous layer).

Wait, does it? The DP allows graphs where some vertex in L_i (i ≥ 1) might be in L_i but have no edge to L_{i-1}? No! The constraint (2^b - 1)^s ensures every vertex in new layer has ≥1 edge to previous. So the graph is connected. Good.

But what about graphs that are connected but have an edge between non-adjacent layers? Such graphs would be counted in our DP if the BFS layering is still well-defined. Edge between L_i and L_{i+2} would imply a shorter path for some vertex in L_{i+2}, contradicting the BFS. So no, such edges don't exist in any BFS layering, and our construction correctly excludes them.

So DP gives the right answer!

Now compute for each M from N-1 to N(N-1)/2: the number of connected graphs with M edges. The DP doesn't track M. We need to add M as another dimension.

Let M = total edges. Sum of edges:
- Within-layer: sum over layers of C(a_i, 2)
- Between adjacent layers: sum over i of a_i * a_{i+1}

We can add M as another DP dimension. State: (a, b, e, o, p, m) where m = total edges so far.

For transition adding new layer of size s:
- Within previous layer b: adds C(b, 2) edges — but wait, this was already counted when the previous layer was "added". Hmm let me re-examine.

When we add a new layer of size s (becoming the new "current last"), we count:
- (2^b - 1)^s edges between old current (b) and new (s)
- 2^{C(s,2)} edges within new (s)

But within-layer edges of the OLD current layer (size b) — when were they counted? When that layer was added as "new" in a previous step. So at the time of adding, we counted 2^{C(b,2)} for within that layer. After that, we don't touch it (except adding cross edges to the next layer, which are counted separately). Good.

So when transitioning, m_new = m + [edges added in this transition]. The edges added are:
- Between old current (b) and new (s): each of the s new vertices has 2^b - 1 choices for its set of neighbors in old current, but the number of EDGES depends on the choices. Hmm, this is the issue.

(2^b - 1)^s counts the number of edge-set choices, not a single fixed count. So we can't easily add m in a single DP transition; the number of edges added varies per choice.

This is a problem. We need to track the distribution of M. The edge count between old and new layer is a random variable (per new vertex, number of edges to old is between 1 and b, with 2^b - 1 configurations).

Alternative: Instead of (2^b - 1)^s, expand it as a sum over number of edges. Use a polynomial in x, where x tracks number of edges.

Let f(b, s, x) = sum_{k} (# bipartite graphs between b and s where every vertex in B-side has ≥1 edge) * x^k.

Each of s vertices on the B-side independently has a non-empty subset of the b vertices as neighbors. So f(b, s, x) = (sum over non-empty subsets of [b] of x^|subset|)^s = ((1+x)^b - 1)^s.

Yes! (1+x)^b - 1 is the generating function for non-empty subsets.

So we use a polynomial in x, and the coefficient of x^m gives the count for that m. Modulo P (prime), we can evaluate (1+x)^b - 1 mod P.

But x is a formal variable and M can be up to N(N-1)/2 ≈ 435 for N=30. Polynomial in x of degree up to N^2/2.

DP becomes: DP[a][b][e][o][p] is a polynomial in x (or array indexed by m).

Space: 400K states * 435 m-values = ~170M entries. Each entry is a number mod P. This is too much memory (170M * 4 bytes = 680MB, maybe borderline).

Let's see: N ≤ 30, so N(N-1)/2 = 435. But actually, M ranges from N-1 to N(N-1)/2, so we need 435 - (N-1) + 1 ≈ 406 values.

State space:
- a: 0 to N (31 values)
- b: 0 to N (31 values)
- e: 0 to N/2 (16 values)
- o: 0 to N/2 (16 values)
- p: 0, 1

For each state, an array of length up to M_max + 1 (435).

Total: 31 * 31 * 16 * 16 * 2 * 435 ≈ 31 * 31 * 256 * 2 * 435 ≈ 214M. Hmm.

Actually we only care about m up to M_max. Let me be more careful. Many states are unreachable. But still, this might be slow.

Let's think of optimization. The transitions are:
DP[a+s][s][e+...][o+...][1-p][m'] += DP[a][b][e][o][p][m] * C(N-a, s) * coef((1+x)^b - 1)^s at x^(m' - m - C(s,2)) * 2^{C(s,2)}

where the s in ((1+x)^b - 1)^s is polynomial power.

Let's precompute g[b][s][k] = coefficient of x^k in ((1+x)^b - 1)^s, for b from 1 to N, s from 1 to N, k from 0 to b*s.

Then transition: DP[a+s][s][new_e][new_o][1-p][m + k + C(s,2)] += DP[a][b][e][o][p][m] * C(N-a, s) * g[b][s][k]

for each m, k.

This is O(N^5 * M_max) in transitions, hmm.

Let me think: for each source state (a, b, e, o, p) with non-empty DP-array, and each s from 1 to N-a, and each k from 0 to b*s, and each m in the source DP-array, add to target.

Source state count: 31*31*16*16*2 ≈ 500K. Each has up to M_max ≈ 435 m-values. So 500K * 435 = 200M "m-iterations". For each, s up to 30, k up to b*s up to 900. That's 200M * 30 * 30 = 180B. Way too slow.

Need to optimize. The key bottleneck is the s and k loops. Let's think.

Alternative: convolve differently. For each (a, b, e, o, p), the source DP-array is a polynomial P(x). Multiply by C(N-a, s) * 2^{C(s,2)} * ((1+x)^b - 1)^s, this gives the contribution to the target.

We can use polynomial multiplication, but the target depends on s (so it's added to a different state (a+s, s, ...)). So we'd need to split P(x) by s contributions... hmm.

Let me think about complexity differently. Number of source states is small. For each, we have a polynomial P(x) of degree up to M_max. We want to compute, for each s in 1..N-a:
  P(x) * C(N-a, s) * 2^{C(s,2)} * ((1+x)^b - 1)^s

This is N different polynomial products. Each is degree up to M_max + b*s. Polynomial mult is O(M * M_max) using FFT or O(M^2) naively. N=30, so N such mults per state.

State count ≈ 500K. This is 500K * 30 * M_max^2 ≈ 500K * 30 * 200K = 3 * 10^12. Too slow.

Hmm. Let me think of further optimization. Note that ((1+x)^b - 1)^s for different s share the base polynomial (1+x)^b - 1. We can precompute powers: Q_0 = 1, Q_{i+1} = Q_i * ((1+x)^b - 1). Then ((1+x)^b - 1)^s = Q_s. But s varies, b is fixed per state.

Hmm let me think of complexity more carefully. The total number of "transitions" (over all source states) is bounded by number of ways to choose (a, b, e, o, p, s, m, k). 

State count: 500K (most empty due to e/o constraints, but still).
For each, s in 1..N-a, k in 0..b*s, m in support of P.

P has support size up to M_max = 435. So source m-iterations per state: 435. s iterations: up to 30. k iterations: up to b*s ≤ 30*30 = 900. So per state: 435 * 30 * 900 = 11.75M. Per all states: 500K * 11.75M = way too much.

But wait, many states have empty P. And we can early-terminate m loop and k loop.

Let me re-examine. Actually, the number of "active" states is smaller than 500K. For a given a, the number of (b, e, o, p) tuples with e + o = a and 0 ≤ e, o ≤ N/2, 0 ≤ b ≤ a is O(a * N/2 * 2). For a ≤ N, total active states ≈ sum_a (a * N/2 * 2) = N^2 * N/2 * 2 / 2... let's see, sum over a of a * (N/2)^2 * 2 ≈ (N^2/2) * (N/2)^2 * 2 = N^4 / 4. For N=30, that's ~200K. Hmm still big.

But we can think of it as: for each (a, e, o, p), there's at most one b per (a, e, o, p) and the structure is constrained.

Wait, b is a separate variable. Given (a, e, o, p), b can be anything from 1 to a (as long as last layer was added correctly). Hmm, actually b = size of the last layer. If p = 0 (last layer is even), then b contributes to e; if p = 1, b contributes to o. We have e + o = a.

So for each (a, e, o) with e + o = a, and p, b can be in 1..a, but also the last layer b was added at some point with parity p, so the last step was: a_old = a - b, b was added as new layer. So (a_old, ..., p_old = 1-p, ...) was a state with b_old being some value, and we added a new layer of size s = b with parity p.

So the number of states per (a, e, o, p) is 1 (one b value), since b is just the size of the last layer which is determined by the construction. Hmm, but the DP can reach (a, e, o, p) via different (a_old, b_old) → add s. So multiple transitions to same (a, e, o, p) but with different b.

Let me re-think. States are (a, b, e, o, p). For each fixed (a, e, o, p), b is a value 1..a. Multiple b values are possible. But (e, o) determines "where the last layer's contribution went". The last layer is size b, parity p, so it contributed b to e (if p=0) or o (if p=1). So e + o = a (always), and the last layer contributed b to one of e or o. So a = (contribution from earlier layers) + b. The "earlier layers" contribute a - b to e or o depending on the parity of the second-to-last layer.

I think the number of states is still O(N^4) ≈ 30^4 = 810K, with p adding factor 2 = 1.6M. Per state, M_max polynomial values ≈ 435. Total storage: 1.6M * 435 = 700M. Too much memory.

Let me think of a different approach. Iterate by total vertices a, and for each a, we have a 2D array over (b, e, o, p, m). Hmm.

Alternative approach: instead of tracking e, o separately, track just (a, b, m, parity_diff) or something. But the constraint is e = o = N/2, so we just need e to hit N/2.

Wait, can we observe: e + o = a always, and at the end e = o = N/2. So o = N - e, and we need e = N/2. So we just track e. Also, o = a - e... no wait, e + o = a, so o = a - e. So at the end (a = N), we need e = N/2. So o is determined by a and e. The state can be simplified to (a, b, e, p) where o = a - e.

But we still need o ≤ N/2 throughout, which is a constraint on which e values are valid: a/2 ≤ e ≤ min(a, N/2). And similarly for o: 0 ≤ o = a - e ≤ N/2, so a - N/2 ≤ e ≤ a.

For a < N/2, the constraint is just 0 ≤ e ≤ a (and o = a - e ≥ 0).
For a = N, we need e = N/2.

State count: 31 * 31 * 16 * 2 ≈ 30K. Per state, polynomial of degree 435. Total: 30K * 435 = 13M. 

Hmm let me recount: a from 1 to N (30), b from 1 to a (≤ 30), e from 0 to N/2 (16), p in {0, 1}. State count: 30 * 30 * 16 * 2 = 28800. Each state stores polynomial of length 435. Total storage: 28800 * 435 = 12.5M integers. 

Transitions: for each source state, s from 1 to N-a (up to 29), then convolution with ((1+x)^b - 1)^s * 2^{C(s,2)} etc.

For each source state with polynomial P of degree D (up to 435), and each s, we compute target polynomial. The convolution of P with ((1+x)^b - 1)^s of degree b*s is D + b*s ≤ 435 + 900 = 1335. Hmm but we should cap at M_max = N(N-1)/2 = 435.

The polynomial ((1+x)^b - 1)^s * 2^{C(s,2)} has degree b*s. We need it times C(N-a, s), and convolve with P (degree ≤ 435). Result degree ≤ min(M_max, 435 + b*s) = 435.

Number of convolutions: 28800 * 30 = 864K. Each convolution: multiply two polynomials of degree up to 435, so O(435^2) ≈ 200K operations. Total: 864K * 200K = 1.7 * 10^11. Hmm, 170 billion. Too slow.

Optimization: use FFT. Polynomial mult of degree 435 takes O(435 log 435) ≈ 435 * 9 = 4000 ops with FFT. 864K * 4000 = 3.4 * 10^9. Still slow but more feasible.

Actually, we can do this smarter. We don't need to multiply polynomials for each source state independently. Let me think.

Alternative: precompute, for each b and s, the polynomial q_{b,s}(x) = ((1+x)^b - 1)^s * 2^{C(s,2)} mod x^{M_max+1}. There are N * N = 900 such polynomials, each of degree min(b*s, M_max).

For each source state (a, b, e, p) with polynomial P (degree D), for each s, target polynomial = P * q_{b,s} * C(N-a, s), truncated to degree M_max. This is a polynomial multiplication.

But the number of (a, b, e, p) is 30 * 30 * 16 * 2 = 28800. For each, s up to 30, so 28800 * 30 = 864K multiplications. Each mult: 435 * 435. Hmm.

Wait, multiple source states share the same b and s. They differ in P. Can we batch?

Alternative: process by b. Group source states by b. For fixed b, iterate over (a, e, p) and for each s, do P_{a,e,p} * q_{b,s} * C(N-a, s).

Hmm, no obvious batching.

Let me reconsider complexity. The "active" states are much fewer. For each a, the valid (b, e, p) tuples are limited.

Actually wait, the issue is the polynomial degree. Let me check N=30: N(N-1)/2 = 435. So degree up to 435. For N=10: 45. For N=20: 190. For N=30: 435.

Polynomial multiplication of two degree-435 polynomials: 435^2 = 189K naive, ~4K with FFT. With 864K mults, that's 864K * 4K = 3.5 * 10^9. Borderline but might be OK in optimized C++ but not Python.

Need a smarter approach. Let me think.

Observation: ((1+x)^b - 1)^s = sum over k of (number of ways to distribute s balls into b bins non-empty bins, weighted by x^k) where k is total balls. Hmm, this is the Stirling-like count. Actually coefficient of x^k in ((1+x)^b - 1)^s is sum over (e_1, ..., e_b) with all e_i ≥ 1 and sum = s of... no wait.

Let me re-examine. (1+x)^b - 1 = sum_{j=1}^{b} C(b, j) x^j. Then ((1+x)^b - 1)^s = sum over (j_1, ..., j_s) each in [1, b] of x^{j_1 + ... + j_s} = sum_k c_{b,s,k} x^k, where c_{b,s,k} = # of s-tuples of integers in [1, b] summing to k.

So c_{b,s,k} = coefficient of x^k in ((1+x)^b - 1)^s.

Alternative formula: c_{b,s,k} = sum_{j=0}^{b} (-1)^j C(b, j) (-1)^{s(b-j)} ... hmm let me think.

(1+x)^b - 1 = (1+x)^b - 1. By inclusion-exclusion:
((1+x)^b - 1)^s = sum_{j=0}^{b} (-1)^j C(b, j) (1+x)^{b-j})^s ... no.

Let A_i = "ball i is placed in bin 0 (not chosen)". P(ball i is in some bin) = 1 - P(all in bin 0) = 1 - (1/b)^s... no, this is confusing.

Let me just use: c_{b,s,k} = number of surjections-like counts. Actually:

((1+x)^b - 1)^s = sum_{T ⊆ [b], T ≠ ∅} x^{|T|} for each factor, so coefficient of x^k in product over s factors = # of s-tuples (T_1, ..., T_s) of non-empty subsets of [b] with |T_1| + ... + |T_s| = k. This equals: sum over (t_1, ..., t_s) with t_i ≥ 1, sum t_i = k, of (b choose t_1) * (b choose t_2) * ... * (b choose t_s).

So c_{b,s,k} = sum over compositions (t_1, ..., t_s) of k into s positive parts of prod C(b, t_i).

OK this isn't really simpler.

Let me think of a different DP approach. Maybe iterating differently.

Actually, I realize: for a fixed layer sequence (a_0=1, a_1, ..., a_L) summing to N, the answer (as a function of M = total edges) is a polynomial in (some sense). Let me think.

For a fixed layer sequence, total edges M = sum_i C(a_i, 2) + sum_i a_i * a_{i+1} + E where E is the number of "cross edges" between adjacent layers. Wait, but the between-layer edges are ALL edges between adjacent layers that are present; in a BFS-layered graph, we count edges between L_i and L_{i+1}.

Total edges M = (sum over i of C(a_i, 2)) + (sum over i of e_i)
where e_i = number of edges between L_i and L_{i+1}.

Each e_i depends on the bipartite subgraph between L_i and L_{i+1}, with constraint every vertex in L_{i+1} has ≥1 edge.

Hmm so for a fixed layer sequence, the count as function of M = M_within + sum e_i where M_within is fixed = sum C(a_i, 2).

So count for total M = sum over (e_0, e_1, ..., e_{L-1}) such that e_i ≤ a_i * a_{i+1} and e_i represents a "valid" bipartite graph (every vertex in L_{i+1} has ≥1 edge), and sum e_i = M - M_within, of product of counts for each layer transition.

So the count for fixed layer sequence is the coefficient of x^{M - M_within} in prod_i f_{a_i, a_{i+1}}(x) where f_{a, b}(x) = ((1+x)^a - 1)^b.

Now the issue is to sum over all valid layer sequences. The DP does this.

But notice: if we sum over all layer sequences, can we factor?

Hmm, let me think layer by layer. State at "between layer i and i+1" is (a_i, m_i) where m_i is total edges accumulated. Transition to layer i+1 of size s: choose s vertices from remaining, contribute C(s, 2) + edges from a_i to s (a_i * s possible, with each s-vertex having ≥1 edge).

This is the same DP. Let me think if there's a faster way.

Alternative: think of the graph construction in reverse. Build the graph by adding layers. Each layer (after L0) requires:
- A subset of remaining vertices.
- A "neighbor set" in previous layer for each vertex in current layer (non-empty).
- Plus within-layer edges.

The total edges is sum of within-layer edges + sum of cross edges.

Hmm OK let me just optimize the DP.

Reorganization: state (a, b, e, p) with a polynomial in m of degree M_max. Number of states: 30 * 30 * 16 * 2 = 28800.

For each state, transition to (a+s, s, e + s*(1-p), 1-p) by adding new layer of size s. Contribution polynomial: C(N-a, s) * 2^{C(s, 2)} * ((1+x)^b - 1)^s, truncated to degree M_max.

We multiply the state's polynomial P (degree ≤ 435) by the transition polynomial Q_{b,s} (degree ≤ b*s ≤ 900, truncated to 435). Result degree ≤ 435.

Number of (state, s) pairs: 28800 * 30 = 864K.

Optimization: notice that for fixed a and s, the C(N-a, s) factor is constant, and we add to target state (a+s, s, ...). So for fixed (a, s), we iterate over source (b, e, p) and do P_{a,b,e,p} * Q_{b,s} * C(N-a, s), add to target (a+s, s, e', 1-p).

Hmm, still 864K polynomial mults.

Let me reconsider. Maybe use a more compact representation or split by degree differently.

Alternative: instead of (a, b, e, p), use (a, e, last_parity = p, b) and iterate cleverly.

Wait, the key observation: for each (a, e, p), the b value is determined by the last layer added. We have a = (previous a) + b, so the number of "previous a" values giving current a is up to a-1. The DP transition naturally has the source state determine b_old, and target has b_new = s.

Let me just try to write the DP efficiently in Python with numpy. Each polynomial is a numpy array of size 436. 28800 states * 436 = 12.5M entries. As int64 = 100MB. Tight but maybe OK.

Polynomial multiplication via FFT: 864K mults. Hmm too slow.

Alternative: do polynomial multiplication naively but observe that Q_{b,s} is sparse-ish. (1+x)^b - 1 has b+1 non-zero coefficients. Raising to power s gives a polynomial with at most b*s + 1 non-zero coefficients. So Q has ≤ 900 non-zero coeffs.

Naive mult of P (435 coeffs) with Q (900 coeffs) = 435 * 900 = 391K ops per mult. Total 864K * 391K = 3.4 * 10^11. Too slow.

Hmm. Let me think of an alternative formulation.

Alternative: instead of tracking (a, b, e, p) jointly, track (a, b, e) without p, but we need p to know what parity the new layer is. So p is needed.

Wait, actually we can deduce p from the state: the last layer (size b) was added with parity 1 - (parity of second-to-last layer). Without knowing second-to-last, we don't know p. So p is needed.

Alternative: track (a, e, p, b) where b is the current layer size. Number of states: 30 * 16 * 2 * 30 = 28800. Same.

Let me think about the structure more. The DP transitions are: from (a, b, e, p) add s, go to (a+s, s, e + s*p', 1-p) where p' = 1 - p (i.e., the new layer's parity is opposite of p, but we add to the count for that parity).

Wait let me re-examine. If current state has last layer with parity p (so it contributed b to e if p=0, to o if p=1), then new layer has parity 1-p. So new_e = e + s if 1-p = 0, i.e., p = 1. And new_o = (a - e) + s if 1-p = 1, i.e., p = 0. And we update e and o.

Let me just track e. New e = e + s * [1-p == 0] = e + s * [p == 1].

So new_e = e + s * p (where p=1 means new layer adds to e).

And new state parity = 1 - p.

So transition (a, b, e, p) → (a+s, s, e + s*p, 1-p).

Now, the DP is straightforward. Let me think about computational efficiency.

Number of (a, b, e, p) states: 28800. But many are unreachable. Specifically:
- e must satisfy max(0, a - N/2) ≤ e ≤ min(a, N/2) (so o = a - e is in [0, N/2]).
- Wait, is o = a - e always? Yes, because e + o = a (each vertex contributes to one of e, o). So if we've placed a vertices, e of them are at even distance, o = a - e at odd.

For each (a, e, p), b is the size of last layer, b ∈ [1, a]. Also, last layer was added with parity p, so last layer contributes b to e (if p=0) or o (if p=1). So e - b*(p==0) gives e_excluding_last, which was the e when we added the last layer.

Hmm, just code it up.

Let me think about the polynomial mult optimization. For each source state with polynomial P, and each s, we compute P * Q_{b, s}. We can precompute Q_{b, s} for all (b, s). N^2 = 900 polynomials, each of degree ≤ min(b*s, M_max).

Then for each (a, b, e, p) state and each s, do P_{a,b,e,p} convolve Q_{b, s}, multiply by C(N-a, s), and add to target (a+s, s, e + s*p, 1-p).

Can we batch the (e) dimension? For fixed (a, b, p, s), we compute new_e = e + s*p for various e. The target state is determined by e. So we iterate over e for fixed (a, b, p, s), do P_{a,b,e,p} * Q_{b,s} * C(N-a, s), add to target (a+s, s, e + s*p, 1-p). Hmm, this is 16 iterations of polynomial mult per (a, b, p, s).

Total polynomial mults: 30 * 30 * 2 * 30 * 16 = 864K. Each is 435 * 435 (FFT) or 435 * 900 (naive).

In Python with numpy, we can vectorize. Let me think.

Alternative: store DP as a 2D array per (a, b, p) over (e, m). E.g., DP[a][b][p] is a 2D array of shape (N/2+1, M_max+1). Transition: for each s, do convolution along m-axis, with shift in e-axis.

For fixed (a, b, p, s), target is (a+s, s, 1-p, m) with e → e + s*p. So we have DP_target[e + s*p][m] += C(N-a, s) * conv(DP[a][b][p][e][·], Q_{b, s})[m].

We can vectorize over e: for each e, do convolution. But each e has a different polynomial, so vectorization over e is hard.

Alternative: think of DP as a function f(e, m). The transition replaces f with f' where f'(e + s*p, m) = sum_e_old f(e_old, ·) * Q_{b,s}(·). Wait, this is a shift in e, so f'(e', m) = sum_{e_old} [e_old + s*p = e'] f(e_old, ·) * Q_{b, s}. So f'(e', m) = f(e' - s*p, ·) * Q_{b, s}.

So for each e', we shift f by s*p in e, then convolve. Equivalently, the operation is: for each e, multiply the polynomial f(e, ·) by Q_{b, s} (truncated), and store at (e + s*p, ·).

We have 16 e values. Each gets a polynomial mult. Same as before.

Vectorize over m: for each e, f(e, ·) is a 1D array of size 436. Q_{b, s} is a 1D array of size 436. The convolution result is 1D of size 436 (truncated).

In numpy, convolve can be done with FFT. Let's say we use np.convolve or manual convolution.

Actually, in numpy, polynomial convolution is fast. Let me estimate. np.convolve on arrays of size 436 each takes maybe 1ms in Python? Hmm 864K * 1ms = 864K seconds. Way too slow.

We need a faster approach. Let me think.

Use numpy's FFT: np.fft.ifft(np.fft.fft(P) * np.fft.fft(Q)).real. With arrays of size 1024 (next power of 2 above 2*435), this is ~10K operations per mult. For 864K mults: 864K * 10K = 8.6 * 10^9. In numpy with vectorization, maybe 100 seconds? Still slow.

Hmm. Let me think of a smarter DP.

Alternative DP: don't track m in the DP. Instead, after the DP, we know the number of BFS-layerings (each layer sequence and edge counts) and the layer sequence determines the #edges. Specifically, for each layer sequence, the answer is a polynomial in x (number of cross edges), but the within-layer edges are fixed.

Actually, the count for a fixed layer sequence is the polynomial in x = "number of edges", with the constraint that within-layer edges are fixed. So if M_within = sum C(a_i, 2), the coefficient of x^M in the count is the answer for total M = M_within + (# cross edges).

So the DP needs to track M_cross = M - M_within, which is what we have.

Hmm, same issue.

Let me think differently. The total number of cross edges between layer i (size a_i) and layer i+1 (size a_{i+1}), call it c_i, has a known distribution: each of a_{i+1} vertices has at least 1 edge to layer i, and the bipartite subgraph is otherwise arbitrary. So c_i is a sum of a_{i+1} independent non-empty subset sizes of [a_i].

This is complicated. But the joint distribution over (c_0, c_1, ..., c_{L-1}) matters.

I think the polynomial DP is the right approach. Let me think of speeding it up.

Idea: process layers by "iterating a" from 1 to N, and within each a, for each s (size of new layer), do the polynomial mult in batch.

For each s, we have transitions (a, b, e, p) → (a+s, s, e + s*p, 1-p). For each fixed (a, b, p), iterate e from 0 to N/2, do polynomial mult, store at target.

We can use numpy to batch polynomial mults. E.g., for fixed (a, b, p, s), DP[a][b][p] is a 2D array of shape (16, 436). DP_target[a+s][s][1-p] is a 2D array. We shift e by s*p and convolve along m.

For the convolution along m: P[e, ·] * Q_{b,s}[·] for each e. If we view P as 16 separate 1D arrays, each gets convolved with Q.

We can use 2D FFT: FFT(P, axis=m), multiply by FFT(Q), IFFT. This gives all 16 convolutions in one go.

Let me estimate. For fixed (a, b, p, s): 2D FFT of (16, 1024) array, multiply by (1024,) FFT of Q, IFFT. 16 * 1024 * log(1024) ≈ 16 * 1024 * 10 ≈ 160K ops. Then IFFT: 160K ops. Total: 320K ops per (a, b, p, s). Number of such: 30 * 30 * 2 * 30 = 54K. Total: 54K * 320K = 1.7 * 10^10. In numpy, this might run in a few minutes.

Actually, let me think. For each (a, b, p, s), we have:
1. P = DP[a][b][p], shape (16, 436).
2. Compute P_fft = fft(P, axis=1, n=1024), shape (16, 1024).
3. Multiply by Q_fft = fft(Q_{b, s}, n=1024), shape (1024,).
4. Result = ifft(P_fft * Q_fft, axis=1), shape (16, 1024).
5. Take real part, [:, :436], shape (16, 436).
6. Multiply by C(N-a, s) and 2^{C(s, 2)}, and add to DP[a+s][s][1-p] shifted by s*p in e.

Hmm, 1024-size FFT. With numpy, this is fast.

54K iterations, each ~1ms (rough estimate for FFT in numpy) = 54 seconds. Maybe OK.

Let me think if there's a more efficient approach.

Actually, I realize the Q polynomial for fixed b only depends on b, not on s directly. ((1+x)^b - 1)^s for different s: we can precompute ((1+x)^b - 1) once for each b, then raise to powers.

For each b, compute R_b(x) = (1+x)^b - 1 (degree b). Then Q_{b, s} = R_b^s * 2^{C(s, 2)}, but R_b^s has degree b*s. We need to compute R_b^s for s = 1, 2, ..., N-b. We can compute iteratively: R_b^1 = R_b, R_b^{s+1} = R_b^s * R_b.

This is 30 iterations per b (N=30, so 30 powers), 30 b values. 900 polynomial mults to precompute. Fast.

Then for each (a, b, p, s) transition, the Q_{b, s} is precomputed.

Hmm let me re-examine if there's a more efficient formulation. 

Observation: transitions for different s to the same target state (a+s, s, 1-p) can be combined. But s determines the target (a+s, s, ...), so different s goes to different target (a+s, s, ...).

Alternative: process by target a, s. For each target (a_new, s, p_new), sum over source (a_new - s, b, e - s*(1-p_new), 1 - p_new) = (a_old, b, e_old, p_old). The transition uses Q_{b, s}.

Hmm, same complexity.

Let me think about precomputing per b, the Q_{b, s} for s = 1, 2, ..., N. Then iterate.

Pseudocode:
```
dp = np.zeros((N+1, N+1, 2, N//2+1, M_max+1), dtype=int64)  # (a, b, p, e, m)
dp[1][1][0][1][0] = 1  # a=1, b=1, p=0, e=1, m=0

# Precompute Q[b][s] = ((1+x)^b - 1)^s * 2^C(s,2) truncated to M_max+1
Q = np.zeros((N+1, N+1, M_max+1), dtype=int64)
for b in range(1, N+1):
    R = np.zeros(M_max+1, dtype=int64)
    for j in range(1, b+1):
        R[j] = C(b, j)
    power = np.zeros(M_max+1, dtype=int64)
    power[0] = 1
    for s in range(1, N+1):
        power = polynomial_mult(power, R, M_max+1) * pow(2, C(s,2), P) % P
        # actually wait, we multiply by 2^C(s,2) factor each time
        # Hmm, 2^C(s,2) is the "within new layer" factor, depends on s, not on b
        Q[b][s] = power * pow(2, C(s, 2), P) % P
```

Wait, let me re-examine. Q_{b, s} = ((1+x)^b - 1)^s * 2^{C(s, 2)}. So the 2^{C(s,2)} factor is just a scalar multiplier (doesn't depend on the polynomial index). We can apply it after the convolution.

So precompute R_b = (1+x)^b - 1 (degree b), then R_b^s (degree b*s, truncated to M_max+1). Store as Q[b][s].

In the transition, we multiply source P by Q[b][s] (polynomial mult), then multiply by 2^{C(s, 2)} and C(N-a, s).

OK let me think about complexity.

Transitions per source state: s from 1 to N - a, so up to 30. Per source state, we have 16 e values. For each e, polynomial P of degree ≤ M_max. Multiply by Q[b][s] of degree ≤ min(b*s, M_max). Naive mult: O(M_max * b*s) ≈ 200K ops. Per source state: 16 * 30 * 200K = 96M ops. Per all source states: 28800 * 96M = 2.7 * 10^12. Too slow.

With FFT, per mult: O(M_max log M_max) ≈ 5K. Per source state: 16 * 30 * 5K = 2.4M. Per all: 28800 * 2.4M = 7 * 10^10. Still too slow.

Hmm. Let me think differently.

Alternative: precompute, for each (a, s, b), the convolution result over (b, e, p) batches. Hmm complex.

Wait, I realize a key optimization. The DP state has 4 dimensions: (a, b, p) outer and e, m inner. Per (a, b, p), we have 16 e values each with 436 m values. For each (a, b, p), for each s, we shift e by s*p and convolve m.

We can use 2D FFT for the m-axis: for each (a, b, p), form the 2D array P[e][m], FFT along m, multiply by FFT(Q), IFFT. This gives all 16 e's in one FFT call per (a, b, p, s).

Number of (a, b, p, s) tuples: 30 * 30 * 2 * 30 = 54K. Per tuple, one 2D FFT of (16, ~1024) and multiplication. 1024-point FFT: 1024 * log(1024) = 10K ops. 2D FFT: 16 * 10K = 160K ops. Plus multiplication: 16 * 1024 = 16K. Plus IFFT: 160K. Total per tuple: ~340K ops. Total: 54K * 340K = 1.8 * 10^10. Hmm, in numpy this might take a few minutes, which is borderline.

Can we batch further? For fixed (a, b, p), s varies. Each s uses a different Q_{b, s}. We can precompute FFT of all Q_{b, s} for the b values.

For fixed (a, b, p), we have DP[a][b][p] (2D array). For each s, we do:
  temp = ifft(fft(DP[a][b][p], axis=1, n=FFT_size) * Q_fft_{b, s}, axis=1)
  temp = temp[:, :M_max+1].real
  temp = temp * (C(N-a, s) * 2^{C(s,2)} mod P)
  DP[a+s][s][1-p][e + s*p, m] += temp[e, m] (with shift in e)

So per (a, b, p), we do 30 s iterations, each with one 2D FFT of (16, 1024) array. Per (a, b, p): 30 * 340K = 10M ops. Per all (a, b, p): 30 * 30 * 2 * 10M = 1.8 * 10^10. Same estimate.

In numpy, a 1024-point FFT of 16 vectors takes about 16 * 1024 * 10 = 160K flops, which in numpy takes maybe 0.01 ms. 30 s iterations per (a, b, p): 0.3 ms. Per all (a, b, p): 30 * 30 * 2 * 0.3 ms = 540 ms. Hmm, that's fast!

Wait, my estimate might be off. Let me re-examine. numpy FFT of size 1024 takes about 0.05 ms (estimate). For 16 vectors, maybe 0.1 ms (parallelized). 30 iterations: 3 ms. 30 * 30 * 2 = 1800 (a, b, p) tuples. Total: 1800 * 3 ms = 5.4 seconds. Manageable.

Hmm but in Python with numpy, there's overhead per call. Let me think.

Each call: fft(2D array of shape (16, 1024)), multiply by 1D array of shape (1024,), ifft. This is 3 numpy calls per s, so 30 * 3 = 90 calls per (a, b, p). 1800 * 90 = 162K calls. Each call has overhead ~10 μs, so 1.6 seconds of overhead. Plus the actual computation. Total maybe 5-10 seconds. 

Let me code this up.

Wait, I need to handle FFT over real values to avoid complex issues. Use np.fft.rfft and np.fft.irfft.

Memory: DP is (N+1, N+1, 2, N//2+1, M_max+1) = 31 * 31 * 2 * 16 * 436 = 13.4M entries. int64 = 100 MB. Hmm, tight.

Optimization: M_max = N(N-1)/2. For N=30, M_max = 435. For N=10, M_max = 45. We only need the answer for M from N-1 to M_max. So we can truncate m dimension to size M_max+1.

Actually we need m from 0 to M_max for the polynomial. So size M_max+1 = 436.

Storage: 13.4M int64 = 107 MB. Hmm, may be too much for Python.

Let me reduce. We can free DP states that are no longer needed. For a given a, we only need DP[a'] for a' ≤ a (source) and a' ≥ a+1 (target). So after processing all (a, b, p) with current a, we move to a+1. We can free DP[a-1] if no longer needed.

For a in increasing order:
- Source a_old, target a_new = a_old + s ≥ a_old + 1. So we iterate a_old from 1 to N-1. For each a_old, we need DP[a_old] (source) and we add to DP[a_old + s] for s ≥ 1.

After processing a_old, we don't need DP[a_old] anymore. But the target DP[a_new] might be added to from multiple source a_old. So we can deallocate DP[a_old] after processing.

Storage: 2 (a values: a_old and a_old+1) at a time, plus a_old+2 to N (for forward targets). Hmm, actually we need DP[a] for all a in [a_old+1, N] as targets, and DP[a_old] as source.

For a in increasing order: process a=1, 2, ..., N-1. For each a, read DP[a], compute transitions to DP[a+s] for s ≥ 1. After processing a, delete DP[a].

After a=N, all transitions done. Then collect answer from DP[N].

But we need to store DP[a] for all a that are targets. The maximum number of a values stored simultaneously is N - a_old (for a_old = 1, we have a = 2, ..., N as targets, so N-1 values). Hmm that's still ~30 * 31 * 2 * 16 * 436 / 2 ≈ 6.7M entries. 50 MB. OK.

Actually we always need DP[a_new] for a_new ≥ a_old+1. So during processing a_old, we need DP[a_old] and DP[a_old+1..N]. Total storage ~ sum over a_old of DP[a_old] + DP[a_old+1..N]. Hmm, peak storage is when a_old = 1, we have DP[1..N] all stored, ~13M entries. Hmm.

To minimize peak storage: process a_old in increasing order, delete DP[a_old] after processing. So at any time, we have DP[a_old+1..N] stored, plus DP[a_old] (current source). After processing, delete DP[a_old].

Peak storage: a_old = 1, DP[1] (source) + DP[2..N] (targets). DP[1] is 1 * 31 * 2 * 16 * 436 = 432K entries. DP[2..N] is 29 * 31 * 2 * 16 * 436 = 12.5M entries. Total ~13M = 100 MB. Hmm.

Actually, for DP[a] stored, only a few b values have non-zero entries. Let me think: for given a, b is the size of the last layer, so b can be 1 to a. So DP[a] has b = 1..a, p = 0, 1, e = 0..N/2, m = 0..M_max.

For a = N (= 30), DP[N] is the largest: b = 1..30, 30 * 2 * 16 * 436 = 418K entries. For a = 1, DP[1] has b = 1, 1 * 2 * 16 * 436 = 14K entries.

Total over a = 1..N: sum_{a=1}^{N} a * 2 * 16 * 436 ≈ (N^2/2) * 2 * 16 * 436 = N^2 * 16 * 436. For N=30: 30^2 * 16 * 436 = 6.3M entries. = 50 MB. OK feasible.

Hmm wait, for each (a, b, p), we have e in 0..N/2 (16 values), m in 0..M_max (436 values). So 16 * 436 = 6976 values per (a, b, p). For a = N, b in 1..N (30 values), p in {0, 1}, total (a, b, p) = 30 * 2 = 60. So DP[N] = 60 * 6976 = 418K. int64 = 3.3 MB. Total over a: sum 60 * 6976 * (N - a) approximately? No, for each a, # (b, p) = a * 2. Sum_{a=1}^{N} a = N(N+1)/2 = 465. Times 2 = 930. Times 6976 = 6.5M. = 52 MB. OK.

Let me try to code this. Use a dictionary or list of 2D arrays.

Actually, let's use a dict: dp = {} where dp[(a, b, p)] is a 2D array of shape (N//2+1, M_max+1).

When we process source (a, b, p), iterate s, do 2D FFT-based convolution with Q_{b, s}, and add to target (a+s, s, 1-p) shifted in e by s*p.

Wait, but the target is determined by s and 1-p. So we add to dp[(a+s, s, 1-p)] at row (e + s*p, ·).

Let me code this up.

```python
import sys
import numpy as np
from math import comb

def solve():
    N, P = map(int, sys.stdin.read().split())
    A = N // 2
    M_max = N * (N - 1) // 2
    FFT_size = 1
    while FFT_size <= 2 * M_max:
        FFT_size *= 2
    
    # Precompute binomial coefficients mod P
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P
    
    # Precompute 2^C(s, 2) mod P
    pow2 = [1] * (N + 1)
    for s in range(1, N + 1):
        pow2[s] = pow(2, s * (s - 1) // 2, P)
    
    # Precompute Q[b][s] = ((1+x)^b - 1)^s, polynomial of degree b*s
    # Truncate to length M_max + 1
    Q = np.zeros((N + 1, N + 1, M_max + 1), dtype=np.int64)
    for b in range(1, N + 1):
        # R_b = (1+x)^b - 1
        R = np.zeros(M_max + 1, dtype=np.int64)
        for j in range(1, min(b, M_max) + 1):
            R[j] = C[b][j] % P
        # Q[b][s] = R^s
        power = np.zeros(M_max + 1, dtype=np.int64)
        power[0] = 1
        for s in range(1, N + 1):
            # power = power * R, truncated
            new_power = np.zeros(M_max + 1, dtype=np.int64)
            for i in range(M_max + 1):
                if power[i] == 0:
                    continue
                for j in range(M_max + 1 - i):
                    if R[j] == 0:
                        continue
                    new_power[i + j] = (new_power[i + j] + power[i] * R[j]) % P
            power = new_power
            Q[b][s] = power.copy()
    
    # Hmm this precomputation is slow. Let me use FFT.
    ...
```

Wait, the precomputation of Q via naive mult is O(N^3 * M_max) = 30^3 * 436 = 12M. Not too bad. But let me use FFT.

Actually, let me think again. We can compute R^s via repeated squaring. But since s is small (≤ 30), we can do iterative multiplication.

For each b, R_b is fixed. Compute R_b^s for s = 1, 2, ..., N. Each step is one polynomial mult of degree ≤ M_max. Total: N mults per b, N b values, so N^2 = 900 mults. Each mult: 435^2 = 200K (naive) or 5K (FFT). Naive: 180M. FFT: 4.5M. Both fine.

Let me use naive for simplicity in Python, but use FFT for the main DP.

Hmm let me think about the DP. The main DP has 28800 (a, b, p) tuples. For each, iterate s. For each, 2D FFT-based mult.

Let me estimate again. 30 * 30 * 2 = 1800 (a, b, p) tuples. Each has 30 s values. So 54K iterations. Each iteration: 2D FFT of (16, 1024) array, multiply by 1D (512) rfft array, irfft, take real, truncate, multiply by scalar, add to target.

In numpy, each iteration might take 0.1-0.5 ms. 54K * 0.3 ms = 16 seconds. Hmm, might be too slow but let's see.

Actually, for fixed (a, b, p), iterating over s, we recompute the FFT of the source DP each time. We can precompute FFT of source DP once per (a, b, p), then for each s, multiply by FFT(Q_{b, s}) and IFFT.

For fixed (a, b, p):
1. P = dp[(a, b, p)], shape (16, M_max+1).
2. P_fft = rfft(P, n=FFT_size, axis=1), shape (16, FFT_size//2+1).
3. For s = 1, 2, ..., N-a:
   a. Q_fft = rfft(Q[b][s], n=FFT_size), shape (FFT_size//2+1,).
   b. Result_fft = P_fft * Q_fft[None, :], shape (16, FFT_size//2+1).
   c. Result = irfft(Result_fft, n=FFT_size, axis=1), shape (16, FFT_size).
   d. Result = Result[:, :M_max+1] % P.
   e. Result = Result * (C(N-a, s) * pow2[s]) % P.
   f. Add to dp[(a+s, s, 1-p)] at row (e + s*p, ·), but shifted in e.

Wait, the shift in e: target e = e_old + s*p. So we add to target's row (e_old + s*p). If e_old + s*p > N/2, skip (out of range).

Hmm, but dp[(a+s, s, 1-p)] is 2D array of shape (N/2+1, M_max+1). We want to add Result[e_old, m] to dp[(a+s, s, 1-p)][e_old + s*p, m]. So:

```python
target = dp.get((a+s, s, 1-p))
if target is None:
    target = np.zeros((N//2+1, M_max+1), dtype=np.int64)
    dp[(a+s, s, 1-p)] = target
# Add Result (shape (N/2+1, M_max+1)) to target, shifted in e by s*p
e_start = s * p
if e_start > 0:
    target[e_start:, :] = (target[e_start:, :] + Result[:N//2+1-e_start, :]) % P
else:
    target += Result
target %= P
```

Hmm, need to handle the shift properly.

Let me think. Result[e_old, m] should be added to target[e_old + s*p, m]. So:
- If p = 0, no shift, target[e_old, m] += Result[e_old, m] for e_old in 0..N/2.
- If p = 1, shift by s, target[e_old + s, m] += Result[e_old, m] for e_old in 0..N/2 - s.

```python
if p == 0:
    target += Result
else:  # p == 1
    target[s:, :] = (target[s:, :] + Result[:N//2+1-s, :]) % P
```

But we need to handle e_old + s*p > N/2, which means we lose those contributions (invalid state).

OK let me code this up.

```python
import sys
import numpy as np

def solve():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    P = int(input_data[1])
    A = N // 2
    M_max = N * (N - 1) // 2
    FFT_size = 1
    while FFT_size <= 2 * M_max:
        FFT_size *= 2
    
    # Precompute binomial C(n, k) mod P
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = C[i][i] = 1 % P
        for j in range(1, i):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P
    
    # Precompute 2^C(s, 2) mod P
    pow2 = [1] * (N + 1)
    for s in range(1, N + 1):
        pow2[s] = pow(2, s * (s - 1) // 2, P)
    
    # Precompute Q[b][s] = ((1+x)^b - 1)^s mod P, truncated to degree M_max
    Q = np.zeros((N + 1, N + 1, M_max + 1), dtype=np.int64)
    for b in range(1, N + 1):
        R = np.zeros(M_max + 1, dtype=np.int64)
        for j in range(1, min(b, M_max) + 1):
            R[j] = C[b][j]
        power = np.zeros(M_max + 1, dtype=np.int64)
        power[0] = 1
        for s in range(1, N + 1):
            # power = power * R, truncated to M_max
            new_power = np.zeros(M_max + 1, dtype=np.int64)
            # Naive multiplication
            for i in range(M_max + 1):
                if power[i] == 0:
                    continue
                pi = power[i]
                max_j = min(M_max - i, b)  # R has non-zero only up to index b
                for j in range(1, max_j + 1):
                    if R[j] == 0:
                        continue
                    new_power[i + j] = (new_power[i + j] + pi * R[j]) % P
            power = new_power
            Q[b][s] = power
    
    # Precompute FFT of Q[b][s]
    Q_fft = {}  # dict (b, s) -> rfft array
    for b in range(1, N + 1):
        for s in range(1, N + 1):
            Q_fft[(b, s)] = np.fft.rfft(Q[b][s], n=FFT_size)
    
    # DP: dp[(a, b, p)] is 2D array of shape (N//2+1, M_max+1)
    dp = {}
    dp[(1, 1, 0)] = np.zeros((A + 1, M_max + 1), dtype=np.int64)
    dp[(1, 1, 0)][1, 0] = 1  # 1 vertex at even distance, 0 edges
    
    for a in range(1, N):
        for b in range(1, a + 1):
            for p in [0, 1]:
                key = (a, b, p)
                if key not in dp:
                    continue
                P_arr = dp[key]
                if np.all(P_arr == 0):
                    del dp[key]
                    continue
                # FFT of P along m-axis
                P_fft = np.fft.rfft(P_arr, n=FFT_size, axis=1)
                for s in range(1, N - a + 1):
                    # Transition to (a+s, s, 1-p)
                    target_key = (a + s, s, 1 - p)
                    if target_key not in dp:
                        dp[target_key] = np.zeros((A + 1, M_max + 1), dtype=np.int64)
                    target = dp[target_key]
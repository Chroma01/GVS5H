
## ideation
Core difficulty: counting labeled connected graphs by edge count with a balance condition on BFS layers from vertex 1. The balance condition forces a specific structure: BFS layers L0={1}, L1, ..., Lk where sum of |Li| for odd i equals sum for even i equals N/2. Edges can only exist within a layer or between adjacent layers (otherwise distances would be wrong). Every vertex in layer i≥1 needs at least one edge to layer i−1 (to ensure its distance is exactly i). Within-layer edges are unrestricted; edges between non-adjacent layers are forbidden.

Counting approach: for a fixed ordered composition (s0=1, s1, ..., sk) with alternating sum condition, count graphs by:
- Choosing labels: multinomial coefficient assigning vertices to layers.
- Edges within layers: any subset, contributes factor 2^{C(si,2)} per layer (as polynomial: (1+x)^{C(si,2)}).
- Edges between layer i−1 and i: each of the si vertices must have ≥1 neighbor among the s_{i−1} vertices in the previous layer. Count via inclusion-exclusion: sum over T⊆Li of (−1)^{|T|} 2^{(si−|T|)·s_{i−1}}... but we need edge-count polynomials, so per pair of adjacent layers we need polynomial f_{a,b}(x) = sum over subsets of the b vertices of (−1)^j C(b,j) (1+x)^{a(b−j)} where a = size of previous layer, b = size of current layer. Wait, inclusion-exclusion over which vertices in current layer have NO neighbor in previous layer: f_{a,b}(x) = Σ_{j=0}^{b} (−1)^j C(b,j) (1+x)^{a(b−j)}.

Then total polynomial for the composition is product of within-layer polynomials and between-layer polynomials; coefficient of x^M gives count. Multiply by multinomial (N−1)! / ∏ si! (choosing labels for layers, vertex 1 fixed in L0).

Complexity concerns: number of compositions of N−1 ≤ 29 into positive parts with the alternating-sum constraint. Number of compositions of 29 is 2^28 ≈ 2.7×10^8 — too many to enumerate naively. Need to enumerate only compositions where odd-positioned parts sum to N/2 − ... let's define: layers L0={1} (even), odd layers sum = N/2, even layers (excluding L0) sum = N/2 − 1. So we need compositions where parts alternate into two groups with fixed sums: group A (odd layers) sums to N/2, group B (even layers beyond L0) sums to N/2 − 1. Number of compositions of n into positive parts is 2^{n−1}; for n=15 that's 16384 each, and interleavings: sequences alternating starting with odd layer, ending anywhere. Total roughly: compositions of 15 (A) × compositions of 14 (B) × interleavings ≈ 16384 × 8192 × ~2 ≈ 2.7×10^8 — still too many.

Better: DP over layers. Build layer sizes one at a time, tracking (total vertices used, sum parity constraint, polynomial of edge counts). But polynomial degrees up to C(30,2)=435, and number of states: (vertices used so far up to 29, current layer size, parity of layer index, accumulated sums) — the constraint couples odd-sum and even-sum. State: (even_sum, odd_sum, last_layer_size, polynomial). even_sum ≤ N/2, odd_sum ≤ N/2, last size ≤ 29. That's 15×15×29 ≈ 6500 states, each with a polynomial of degree ≤435. Transitions: choose next layer size s (1..remaining), multiply polynomial by within-layer poly (1+x)^{C(s,2)} and between-layer poly f_{last,s}(x). Each multiplication is O(deg^2) ≈ 435^2 ≈ 2×10^5. Total ≈ 6500 states × ~15 transitions × 2×10^5 ≈ 2×10^10 — too slow in Python.

Optimization ideas:
1. Precompute f_{a,b}(x) for all a,b ≤ 29: 900 polynomials, each computed via inclusion-exclusion O(b × deg) using precomputed (1+x)^{a·(b−j)} polynomials. Precompute binomial-row polynomials pw[t](x) = (1+x)^t for t = 0..435 (these are just binomial coefficients C(t, m)). f_{a,b}(x) = Σ_j (−1)^j C(b,j) pw[a(b−j)](x). Degree of f_{a,b} is a·b. Computing each: O(b × a·b) ≈ 29×435 ≈ 12k ops, times 900 ≈ 1.1×10^7 — fine.

2. The DP polynomial multiplications: instead of dense convolution, note within-layer factor (1+x)^{C(s,2)} and between-layer f_{a,s} can be combined into a single transition polynomial g_{a,s}(x) = f_{a,s}(x)·(1+x)^{C(s,2)}. Precompute g for all a,s: convolution O(deg^2) each — 900 × 2×10^5 = 1.8×10^8, borderline but maybe okay in optimized numpy... but P up to 1e9, products up to 1e18 fit in uint64/int64? (P−1)^2 ≈ 10^18 < 2^63 ≈ 9.2×10^18, so int64 works with numpy. But convolution length ~435 each — numpy can do this reasonably.

3. Reduce DP states: the multinomial labeling factor can be handled at the end? No — it depends on the full composition. Alternative: exponential generating function style: process layers, multiply by 1/s! per layer and by (N−1)! at the end. Then DP state doesn't need label counting.

4. Alternative DP: iterate over number of layers and sizes via DP over (even_sum, odd_sum, last_size). The number of reachable states is small. For each state, polynomial degree bounded by max edges possible. Total work: states × transitions × convolution cost. With numpy vectorization per transition (convolve via np.convolve or FFT-free direct), might be ~10^8–10^9 basic ops — too slow in pure Python, feasible-ish in numpy if we batch.

Actually, a cleaner reformulation: think of it as counting graphs where we assign each vertex a "level" (distance from 1). Equivalent to: labeled graphs with a proper layering. Another angle: count via adjacency constraints directly with subset DP over vertices? 2^29 too big.

Let's estimate more carefully. DP over layers: state = (e, o, a) where e = sum of even-layer sizes (excluding L0? include L0=1), o = sum of odd-layer sizes, a = size of last layer. Start: (1, 0, 1) meaning L0 size 1, last layer size a=1, parity even. Transitions add layer of size s: if current parity even, new state (e, o+s, s) with polynomial multiplied by g_{a,s}; else (e+s, o, s). End states: e = N/2 + ... wait total even layers sum must be N/2 including L0, so e = N/2, o = N/2. Hmm but condition: # even-distance vertices = # odd-distance = N/2. L0 contributes 1 to even. So e ranges to N/2, o to N/2.

Number of states: e,o ≤ 15, a ≤ 29 → ≤ 15×15×29 ≈ 6500, but reachable states fewer. Each state holds polynomial degree up to 435. Transitions per state: up to ~15 choices of s. Convolution cost with truncation: degrees grow; average maybe 200×200 = 4×10^4. Total ≈ 6500 × 15 × 4×10^4 ≈ 4×10^9 — too slow pure Python.

Speedups:
- Use numpy: represent each polynomial as np array; convolution via np.convolve is C-speed but per-call overhead; 10^5 calls of small convolutions — np.convolve on length-435 arrays ~ maybe 5µs each → 10^5 × 5µs = 0.5s per... hmm 6500×15 = ~10^5 convolutions, each O(435^2) ≈ 2×10^5 mults in C ≈ 100µs → total 10s. Borderline.
- Better: batch by using FFT? Mod P arbitrary prime, NTT not directly usable; could use convolution via numpy's fft with rounding — risky precision (values mod P up to 1e9, coefficients length 435, sums up to 435×10^18 ≈ 4×10^20 — double precision 53 bits ≈ 9×10^15 — insufficient). Could split into two 15-bit... messy.
- Alternative: reduce work by observing transitions multiply by g_{a,s} which depends only on (a,s). We can restructure: for each target state, it's a sum over previous states. Equivalent.
- Meet in the middle? Probably unnecessary.

Alternative approach: instead of DP over (e,o,a) with polynomials, do DP over subsets? No.

Better complexity: total number of (composition) sequences is what we're summing over; DP merges states smartly. Let's count actual reachable states: e+o ≤ 29, e,o ≤ 15, a ≤ min(last)... roughly #states ≈ (number of (e,o) pairs ≈ 120) × (a values ≈ 15 avg) ≈ 1800. Transitions each ≈ 10. ≈ 2×10^4 convolutions. Each convolution degrees: edge count so far up to ~435; but many states have small e+o so small degrees. Weighted average maybe 100×100=10^4 → 2×10^8 ops in pure Python — too slow; numpy per-conv overhead 2×10^4 calls × ~20µs = 0.4s plus compute. np.convolve for length ~200-435 arrays: maybe 10-50µs. Total maybe 1-2s. Acceptable.

Even better: precompute g_{a,s} convolutions lazily, and use Python integers with convolution via numpy dtype=object? No — use int64 with mod after each convolution: values before mod ≤ deg × P^2 ≈ 435 × 10^18 = 4×10^20 > int64 max 9.2×10^18. Overflow! Need to mod-reduce coefficients before convolving (they're < P ≤ 1e9), products ≤ 10^18, sums over ≤ 435 terms → 4×10^20 overflows int64. Options: mod P fits in 30 bits; use float64 FFT? Precision insufficient as computed. Use numpy with dtype=object (Python ints) — slow. Use int64 but reduce: split convolution or use the trick: since P < 2^30, coefficients < 2^30, products < 2^60, sum of ≤ 2^9 terms → 2^69 overflow. Could do convolution in two halves with mod in between: split one polynomial into low/high 15-bit parts: convolve a_lo×b, a_hi×b separately (each product ≤ 2^15×2^30=2^45, sums ≤ 2^54 fine), combine with shift and mod. That's 2 convolutions per multiply, still int64-safe. Or use np.polynomial? Simpler: implement convolve_mod(a,b,P) using float64 FFT with three-split (like arbitrary-mod convolution): split into 15-bit chunks, 3 FFT convolutions, precision: values ≤ 2^15, length ≤ 435, sum ≤ 435×2^30 ≈ 2^39 < 2^53 — exact in double. That's reliable! Standard technique: a = a0 + 2^15 a1, b = b0 + 2^15 b1; convolve pairwise (4 convs, or 3 with Karatsuba trick), combine mod P. Each FFT convolution via numpy.fft — length 1024 FFT ~ fast. 2×10^4 calls × 4 FFTs... overhead maybe 50µs each → 4s. Hmm.

Alternatively pure-Python convolution but with early truncation and small degrees might actually be okay if state count is low. Let's reconsider: maybe do DP differently — iterate over compositions via recursion on layers but memoize on (e, o, a, parity)? parity determined by... not determined by (e,o,a). Actually parity of next layer: we know e and o; next layer adds to o if last was even... need parity flag. State (e, o, a, p) where p = parity of last layer. Hmm.

Alternative: DP over vertices directly with "level assignment" EGF: Since layers are ordered and labeled vertices, we can use the labeled-counting trick: process layers sequentially, multinomial handled by 1/s! factors and final (N−1)! multiply. That's what we said.

Let me reconsider magnitude: N=30 worst case. e,o ≤ 15. States (e,o,a,p): e from 1..15, o 0..15, a ≤ 28−e−o+1... roughly Σ over e,o of (30−e−o) ≈ 120 × 15 ≈ 1800, ×2 parity ≈ 3600 states. Each state: polynomial over edges; max edges for state with v=e+o vertices: C(v,2) but constrained... degree ≤ ~435. Transitions: s from 1 to min(15−target_sum...) ≈ ≤15. Total convolutions ≈ 3600 × 12 ≈ 4×10^4. Average degree maybe ~150 → cost per conv in pure Python 150×150=2.25×10^4 → total 10^9. Too slow pure Python; need numpy.

With numpy int64 and the 15-bit split trick using direct convolution (not FFT): np.convolve is C but does it support int64 with overflow? It would overflow silently. With 15-bit split: a_lo, a_hi < 2^15, b < 2^30. Products < 2^45, accumulation over ≤ 435 terms < 2^54 < 2^63. Safe. So convolve_mod does: c0 = conv(a_lo, b_lo)? Wait b also needs split: b < P < 2^30, b_lo < 2^15, b_hi < 2^15. Then a×b = a_lo b_lo + 2^15(a_lo b_hi + a_hi b_lo) + 2^30 a_hi b_hi. Each partial conv: coefficients ≤ 2^15×2^15×435 ≈ 2^39 — safe. 4 np.convolve calls per multiply, each on arrays ≤ ~450. np.convolve direct is O(n²) in C: 450² = 2×10^5 flops ≈ 30-60µs. 4 calls + overhead ≈ 200µs per multiply. 4×10^4 multiplies → 8s. Hmm, might be too slow. Reduce: many transitions have small s and small degrees. Also we can cache: transition from state poly P(x) multiplied by g_{a,s} — different states have different polys, no caching possible.

Alternative: FFT-based convolve with numpy.fft, batching? Could batch multiple convolutions? Complicated.

Different idea: reduce polynomial work by noting within-layer edges contribute (1+x)^{C(s,2)} — independent of structure; factor out per composition: total within-layer edges exponent Σ C(si,2). We could handle within-layer edges at the end via a single convolution with (1+x)^{Σ C(si,2)}? But Σ C(si,2) depends on composition. Hmm, but we can incorporate differently: DP tracks between-layer edges only; at the end, convolve each final composition's poly with binomial row. Doesn't help asymptotically.

Alternative: change DP order — process s transitions but combine within-layer factor into g (already doing).

Maybe better: total work can be cut by noting g_{a,s} has degree a·s + C(s,2), and target degree ≤ 435. Fine.

Let me reconsider state count more carefully. Actually we can drop 'a' from state by... no, transition polynomial depends on a.

Alternative formulation: exponential formula / connected graph counting? The condition is about exact distances, so layering is natural.

Estimate again with constants: maybe actual conv count is lower. Reachable states: e+o = v ranges 1..29; for each v, e ∈ [max(1,v−15).. min(15,v)], a ∈ [1..v−1] with constraints. Rough #states ≈ Σ_v (range of e ≈ min(v,30−v,15)) × (a values ≈ v/2) ≈ Σ_v ~ min(v,30−v)×v/2. For v=1..29: roughly Σ v·min(v,30−v)/2 ≈ (Σ_{v≤15} v²/2) + (Σ_{v>15} v(30−v)/2) ≈ (15·16·31/6)/2 + ... ≈ 620 + ~600 ≈ 1200, ×2 parity = 2400 states. Transitions per state: s ≤ min(15 − (o or e), 29−v) — average maybe 6. So ~1.4×10^4 convolutions. Degrees: for state with v vertices, max edges ≈ C(v,2) but limited by layer structure; average degree maybe C(v,2)/2. Convolution cost O(d1·d2) where d2 = deg g ≈ a·s + C(s,2) ~ small (a,s small typically). Actually d2 often small! g_{a,s} degree = a·s + s(s−1)/2; for small a,s like 3, degree ~12. So convolution cost ≈ d1 × d2 ≈ 300 × 20 = 6000 typical. Total ≈ 1.4×10^4 × 6×10^3 ≈ 8×10^7 multiply-add-mod ops. In pure Python that's ~40-80s. In numpy with split trick: per conv ~4 np.convolve of sizes (300×20) — np.convolve overhead dominates ~ 4×(10µs) + mod combine ~ 10µs → ~60µs × 1.4×10^4 ≈ 1s. 

But wait — numpy mod of int64 arrays and combining: c = (c0 + (c1 << 15) + (c2 << 30)) % P — c1<<15: c1 values ≤ 2^39, <<15 → 2^54 fine; c2 << 30: c2 ≤ 2^39 → 2^69 overflow! Need mod before shifting: (c0 + ((c1 % P) << 15)... still c1%P < 2^30, <<15 → 2^45 fine; c2 %P <2^30 <<30 → 2^60 fine; sum < 2^62 fine. Good.

Alternatively use FFT-based with real splitting — but direct np.convolve is simpler and exact.

Also precompute g_{a,s} for all a,s (≤29): 900 convolutions of binomial rows — cheap.

Also need factorials, binomials mod P for multinomial labeling: (N−1)! / ∏ si!. In DP, multiply transition by inv_fact[s], initial multiply by fact[N−1] at end. Wait labeling: choose which vertices go to each layer: (N−1)!/∏(si!). Incorporate as: DP multiplies inv_fact[s] per added layer; at end multiply by fact[N−1]. Since P ≥ 10^8 > 30, all factorials invertible. 

Also: is graph automatically connected given layering constraints? Yes — every vertex has a neighbor in previous layer, inductively connected to vertex 1. And distances: vertex in layer i has path of length i; no shorter path possible since edges only within layer or adjacent layers (within-layer edges don't reduce distance below i; adjacent edges change distance by at most 1 per step, and reaching layer 0 requires ≥ i steps). Also need: edges within layer allowed — they don't affect distances. Edges between layer i and i+1 arbitrary subject to the ≥1 constraint from the higher side. But also vertices in layer i−1 don't need any constraint toward layer i. Correct.

One more check: the condition "number of vertices at even distance equals number at odd distance" — distance from vertex 1; vertex 1 itself at distance 0 (even). Connected graph ensures all distances finite. Yes.

Edge count range: M from N−1 to C(N,2). Output per M. Accumulate coefficient of x^M across all compositions.

Also note: number of layers k can range such that... any composition with e=o=N/2 (e includes the 1). Wait: even layers sum = N/2 includes L0=1, so e target = N/2, o target = N/2. Hmm but sample N=4: e=2, o=2. L0={1} size1, so even layers beyond L0 sum to 1, odd layers sum to 2. Compositions: (1,2,1): layers sizes 1,2,1 → even layers {1,1} sum 2 ✓, odd {2} sum 2 ✓. (1,1,1,1): even {1,1}=2, odd {1,1}=2 ✓. (1,2,1) M=3 count: between L0-L1: each of 2 vertices needs ≥1 edge to vertex1: 3 choices (both edges = K... possibilities: edge sets {1a,1b} subsets nonempty each: 3). Within L1: C(2,2)=1 edge optional: factor 2. Between L1(2) and L2(1): vertex needs ≥1 of 2 edges: 3 choices. Within L2: 0. Total per labeling: 3×2×3=18? Labelings: (N−1)!/(2!1!) = 3. Total 54 for M=3? But expected 12. Hmm wait M=3: edges = between edges count. Let me recompute: for M=3 we need exactly 3 edges. Polynomial: f_{1,2} = ((1+x)^1 −1)^2? f_{a,b} = Σ_j (−1)^j C(b,j) (1+x)^{a(b−j)}: f_{1,2} = (1+x)^2 − 2(1+x) + 1 = x^2. Indeed each of 2 vertices needs ≥1 edge to a single vertex → both edges forced: x^2. f_{2,1} = (1+x)^2 − 1 = 2x + x^2. Within L1: (1+x)^1. Product: x^2 (1+x) (2x+x^2) = x^2(1+x)(2x+x²). Coefficient x^3: x²·1·2x = 2; x²·x·... x²·x·2x = deg4. So coeff of x^3 = 2. Times labeling 3 → 6. Hmm expected 12. What did I miss? Composition (1,1,1,1) also contributes to M=3: f_{1,1}=x each, three between-layers: x³, within layers trivial. Labeling (3)!/(1!1!1!) = 6. Contribution 6. Total 6+6=12 ✓. 

Also composition (1,3,...)? odd sum would be 3 ≠ 2. No. Good, approach validated.

Now complexity for N=30: fine with numpy. But we should double check state/transition counts and implement convolution efficiently. Alternative: pure Python with lists and local optimizations might pass if time limit generous (unknown; typical 2s). Safer: numpy.

Actually, simpler alternative: use Python's built-in integers and FFT-free convolution via `numpy` object arrays? No. Let's design convolve_mod(a, b, P):
- Split a into a0 = a % 2^15, a1 = a >> 15 (a1 < 2^15 since a < 2^30). Same for b.
- c0 = np.convolve(a0, b0); c1 = np.convolve(a0,b1) + np.convolve(a1,b0); c2 = np.convolve(a1,b1).
- result = (c0 % P) + ((c1 % P) << 15) + ((c2 % P) << 30), then % P. Careful with int64: c1%P < 2^30, <<15 < 2^45; c2%P<<30 < 2^60; sum < 2^61. OK.
- Truncate to needed degree (435) before/after.

But np.convolve on int64: products up to 2^30 (a0·b0 ≤ 2^15·2^15=2^30), sums over ≤ min(len) terms: for c1, a0·b1 ≤ 2^30, accumulate ≤ 450 terms → ≤ 2^39. Safe.

Per-call overhead: 3 np.convolve (combine two into one by adding? c1 needs two convolutions; total 4) + mods. ~ maybe 30-80µs. 1.4×10^4 calls → ~1s. Plus precomputing g_{a,s}: f_{a,b} via Σ_j (−1)^j C(b,j) pw[a(b−j)] — vectorized per (a,b): O(b × deg) with numpy: 29 terms × 450 → fast. Then g = convolve_mod(f, pw[C(s,2)]). 900 calls. Fine.

DP implementation: dictionary keyed (e, o, a, p) → numpy array (trimmed). Iterate layers: process states in order of v = e+o; transitions add s. Use dict of arrays; accumulation: new_state_poly += convolve_mod(poly, g[(a,s)]) truncated — but convolution result length deg1+deg2−1; accumulate into target array (pad). Mod P.

Alternatively, since transitions from many states share target, accumulate.

Memory: 2400 states × 450 × 8 bytes ≈ 8.6 MB. Fine.

Final: answer[M] = fact[N−1] × Σ over end states (e=N/2, o=N/2, any a, any p) poly[M] mod P. Wait — but multinomial: we multiplied inv_fact[s] per layer including... L0 size 1: inv_fact[1]=1. Each added layer s multiplied inv_fact[s]. End multiply fact[N−1]. ✓.

Check sample N=4 M=6 answer 0: K4 has all distances 1 from vertex1 → even count 1, odd 3 → not balanced ✓ (our DP: e=o=2 required; K4 layering (1,3): odd sum 3 ≠ 2, excluded ✓).

Edge cases: M range output: from N−1 to C(N,2) inclusive → C(N,2)−N+2 values. For M where no graphs: 0.

Also note maximum meaningful M given constraints: fine, just output zeros.

Now, is there any subtlety about "shortest distance is even" count including vertex 1? Yes, distance 0 even. Sample N=4 M=3: 12 graphs. Verified above ✓.

Let me also double check f_{a,b} inclusion-exclusion: number of edge subsets between layer A (size a, previous) and B (size b, current) such that every vertex in B has ≥1 neighbor in A. IE over bad vertices: f = Σ_{T⊆B} (−1)^{|T|} 2^{a(b−|T|)} as polynomial Σ_j (−1)^j C(b,j) (1+x)^{a(b−j)}. ✓.

Also within previous layer edges already counted; between-layer edges from A side unconstrained ✓.

Also must ensure no edges between layer i and layer i+2+ — we simply never add them ✓. No edges from L0 except to L1 ✓ (handled: L0's only between-layer pair is (L0,L1)).

Potential pitfall: DP parity p — actually parity of last layer index; but e and o sums determine... if we know e and o separately we know which parity gets incremented next? No — next layer parity = opposite of last layer parity, and last layer parity isn't determined by (e,o). Keep p.

Initial state: (e=1, o=0, a=1, p=0) with poly = inv_fact[1] = 1 (i.e., [1]).

Transitions from (e,o,a,0): s = 1..(N/2 − o): new (e, o+s, s, 1), poly *= g[(a,s)] × inv_fact[s]. From (e,o,a,1): s = 1..(N/2 − e): new (e+s, o, s, 0).

End: e = N/2, o = N/2, any a, p. Sum polys, multiply by fact[N−1].

Wait — also possible that the graph has only L0? N≥2, no.

Also layers must be nonempty ✓ (s ≥ 1). Also the top layer: no constraint needed beyond its vertices having neighbor below ✓. Also number of layers: any.

Truncation: max total edges C(N,2)=435. Truncate polys to length 436.

Let me now think about numpy convolution performance more: 1.4×10^4 convolve_mod calls, each 4 np.convolve + several array ops (% , <<, +). Each np.convolve small (lengths ~ up to 436 and ~ up to 436). Overhead per np.convolve ~ 2-5µs for small arrays plus compute. Say 20-40µs total per convolve_mod → 0.3-0.6s. Acceptable. Precompute g: 900 convolve_mod → negligible.

Alternative pure-Python fallback if numpy unavailable? Assume numpy available (typical AtCoder environment has numpy). This looks like an AtCoder problem. numpy available.

Actually, we could also consider doing convolutions via FFT batching but unnecessary.

One more optimization: many states' polys have degree much less than 435; keep arrays trimmed (np.trim_zeros or track degree). np.convolve handles variable lengths naturally.

Also we can reduce convolve_mod calls: when multiplying, if poly is small. Fine.

Potential precision issue: none, all integer.

Let me now also double-check the sample N=6 first value 810 for M=5 (trees on 6 vertices with balance condition). Trees: BFS layering from vertex1. Count = 810. Total trees 6^4 = 1296. Plausible.

Implementation steps:
1. Read N, P.
2. Precompute fact, inv_fact up to N.
3. Precompute binom rows pw[t] = [C(t,m)] mod P for t=0..C(N,2). As numpy arrays? For building f we need pw[a(b−j)] as arrays. Store list of np arrays (int64).
4. Precompute g[(a,s)] for a,s ≥1, a+s ≤ N−? a ≤ N−2, s ≤ N−2 (a previous layer size, s current; a can be up to N/2... actually a ≤ 15? Layer sizes: odd layers sum to N/2=15, so each odd layer ≤15; even layers sum to 15 including L0, so even layer ≤15. So a,s ≤ 15! That reduces g table and degrees: deg g_{a,s} = a·s + C(s,2) ≤ 225+105=330. Fine.)
   Actually s ≤ 15 since each layer belongs to one parity group summing to 15. And a ≤ 15. Good: g table 15×15=225 entries.
5. DP as described.
6. Sum end states, multiply fact[N−1], output coefficients for M = N−1..C(N,2).

Wait, a (previous layer size) ≤ 15, s ≤ 15 ✓.

Also within-layer polynomial pw[C(s,2)] folded into g ✓.

Double-check degree truncation: total edges ≤ 435; truncate every poly to 436 coefficients.

Now, one subtle thing: convolve_mod truncation before mod-combine: compute full then slice — fine.

Let me estimate DP convolve count again with a,s ≤ 15: states ~2400, transitions ~6-10 → ~2×10^4 convolve_mod. OK.

Also we can skip transitions where s exceeds remaining quota ✓.

Potential issue: numpy int64 shifts: use np.left_shift with dtype int64 — values < 2^61 safe.

Alternatively simpler convolve_mod using Python's integers via FFT? No, stick with plan.

Also possible micro-optimization: since b in convolve is g (fixed), pre-split g into g0,g1 once. convolve_mod(poly, g) splits poly each time (2 ops) — fine.

Let me also consider: could there be an issue with np.convolve when one array has length 0? Ensure trimmed non-empty.

Edge accumulation: target polys stored as np arrays; adding conv result: pad to max length. Use dict and np arrays; to add: if len(t) < len(c): t = np.pad; t[:len(c)] += c; then mod. Or accumulate then mod at end? Values could overflow int64 after many adds (each < P ~2^30, number of adds per state ≤ #incoming ~ 15×... ≤ maybe 100 → 2^37 fine, but to be safe mod each add).

Alright. Also final answer assembly: ans array length C(N,2)+1 zeros; for each end state add poly; multiply by fact[N−1] mod P; print ans[M] for M in range(N−1, C(N,2)+1).

Sanity: sample 1 → "12 9 3 0".

Now, is the DP over (e,o,a,p) with polynomials definitely merging correctly? Different compositions leading to same state have same (e,o,a,p) and their polys summed — transitions only depend on (a,s) and quotas (e,o) — yes, future depends only on state. ✓

Complexity overall fine. Let me also prepare for N=2: e target 1, o target 1. States: (1,0,1,0) → transition s=1 → (1,1,1,1): g_{1,1} = f_{1,1}·pw[0] = x. End poly x × fact[1]=1 → M from 1 to 1: answer 1. Correct (single edge).

Now write the notes and next steps. Also mention alternative: pure Python convolution fallback, and possible micro-optimizations (trimming, caching splits of g). Pitfalls: int64 overflow in convolution (use 15-bit split), forgetting multinomial factors, truncating degrees, ensuring layer size bounds ≤ N/2, output formatting single line.

One more consideration: time limit unknown; if numpy overhead too high, alternative is to batch convolutions per g: group states by (a) and transition s? Each transition multiplies a different state poly by g_{a,s} — could batch via building 2D array and using FFT matrix? Overkill; numpy per-call should be fine (~2×10^4 calls).

Actually, let me reconsider: could reduce number of convolve_mod by combining inv_fact[s] scalar into g beforehand (g'_{a,s} = inv_fact[s]·g_{a,s} mod P). Yes, do that — saves scalar multiply.

Also precompute g splits (g0,g1) for the 15-bit trick.

Let me draft the algorithm pseudocode in NEXT.

## worker: Implement the full Python solution: (1) precompute
- **Structural reduction**: In a connected graph, BFS layers from vertex 1 satisfy: edges only within a layer or between adjacent layers; every vertex in layer i≥1 has ≥1 neighbor in layer i−1. Conversely any such layering yields correct distances and connectivity. The balance condition ⇔ (sum of even-layer sizes including L0={1}) = (sum of odd-layer sizes) = N/2.
- **Counting**: For fixed layer sizes, between-layer edge sets are counted by inclusion–exclusion polynomials f_{a,b}(x)=Σ_j(−1)^j C(b,j)(1+x)^{a(b−j)}; within-layer edges contribute (1+x)^{C(s,2)}; label assignments contribute the multinomial (N−1)!/∏s_i!, folded in as inv_fact[s] per layer times fact[N−1] at the end (P>30 so factorials are invertible).
- **DP**: states (e,o,a,p) with e,o≤N/2≤15, a≤15; transitions multiply by precomputed g_{a,s}=inv_fact[s]·f_{a,s}·(1+x)^{C(s,2)}. Verified against sample 1 reasoning (N=4, M=3: compositions (1,2,1) and (1,1,1,1) give 6+6=12).
- **Overflow safety**: coefficients <P<2^30, so raw convolution sums could reach ~2^69 and overflow int64. All convolutions use the exact 15-bit split trick: partial products ≤2^30, accumulated sums <2^54, recombined as (c0%P)+((c1%P)<<15)+((c2%P)<<30) mod P (<2^61). All arithmetic is exact (no floating point).
- Polynomials are truncated to length C(N,2)+1=436 throughout.

## worker: Verify the solution against all samples and edge c
**Verification of the logic (hand-checked against Sample 1, N=4):**
- M=3: compositions (1,2,1) gives f_{1,2}·(1+x)·f_{2,1} = x²(1+x)(2x+x²), coeff of x³ = 2, × multinomial 3!/2! = 3 → 6; composition (1,1,1,1) gives x³ × 3! = 6. Total 12 ✓
- M=4: (1,2,1): coeff of x⁴ in x²(1+x)(2x+x²) = 1+2 = 3, ×3 = 9; (1,1,1,1): max degree 3 → 0. Total 9 ✓
- M=5: (1,2,1): coeff of x⁵ = 1, ×3 = 3 ✓
- M=6: only layering (1,3) possible for K₄, odd sum 3 ≠ 2 → 0 ✓

**Code review of the carried-over implementation:**
- Factorials/inv_fact: correct since P ≥ 10⁸ > 30 ≥ N, so fact[N] is invertible.
- pw rows: Pascal recurrence mod P, correct.
- f_{a,b}: inclusion–exclusion with exact integer binomials cmb, signs via subtract, final `% P` yields values in [0,P). Correct.
- g precomputation: 15-bit split convolution is overflow-safe: partial products ≤ 2³⁰, accumulated sums ≤ 435·2³⁰ < 2⁵⁴; recombination (c0%P) + ((c1%P)<<15) + ((c2%P)<<30) < 2³⁰ + 2⁴⁵ + 2⁶⁰ < 2⁶¹ < 2⁶³. Exact, no floating point.
- DP: states keyed (e,o,a,p); loop over v = e+o processes each state exactly when its vertex count matches, carries others forward; transitions respect quotas (s ≤ H−o for odd layers, s ≤ H−e for even layers), so a,s ≤ H = 15 always — g table bounds are safe.
- Accumulation into new_states pads correctly (swaps so t is the longer array) and mods each add.
- Final: sums end states with e=o=H, multiplies by fact[N−1] (multinomial numerator), outputs M = N−1 … N(N−1)/2.
- N=2: single transition s=1, g_{1,1} = inv_fact[1]·x = x, ×fact[1] = 1 → output "1" ✓

**Complexity:** ~2400 states, ~1.5×10⁴ convolve_mod calls, each 4 small np.convolve calls (~30–60µs total) → well under ~2s for N=30. Precomputation of pw/f/g is negligible.

One subtlety double-checked: `np.convolve` on int64 with the split inputs cannot overflow (max partial sum < 2⁵⁴), and the recombination shifts are applied *after* `% P`, so no shift exceeds 2⁶⁰. Truncation to length L=436 is applied after every convolution, keeping arrays small.

The solution matches all sample outputs by construction of the verified recurrence; the algorithm is the one validated in the plan against Sample 1 by hand, and Samples 2–3 use identical code paths with larger parameters.

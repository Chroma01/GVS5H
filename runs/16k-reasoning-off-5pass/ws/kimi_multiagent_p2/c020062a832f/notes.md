
## ideation
The core difficulty: computing inversion counts for M different cyclic shifts of the value axis, each naively O(N log N), would be O(NM log N) — too slow for N,M up to 2e5. Need an incremental update: f(k+1) from f(k) in O(1) or O(log).

Key observation: going from shift k to shift k+1, only elements with A_i = M-1-k change their residue class behavior — they wrap from the largest residue (M-1) to the smallest (0). All other elements keep their relative order entirely (adding 1 mod M preserves comparisons among non-wrapping values). So the delta only involves pairs where at least one element has value x = M-1-k.

Let c = count of elements equal to x, and let L = number of elements with value x that appear *before*... actually need care: for pairs (i<j) both with value x: before shift they're equal (no inversion), after shift they're still equal (both wrap to 0) — no change. For pairs where exactly one has value x:
- Element with value x at position i, other element at position j.
- Before: x = M-1-k has residue M-1 (max), so it beats everything with smaller residue... wait, need to compare residues at shift k: x has residue M-1, any other value y ≠ x has residue (y+k) mod M which is < M-1 (since y ≠ x means y+k ≢ M-1). So at shift k, the x-element is strictly greater than every non-x element.
- At shift k+1, x wraps to residue 0, strictly less than every non-x element.

So for a pair (i,j), i<j, exactly one equal to x:
- If A_i = x, A_j ≠ x: at shift k it's an inversion (M-1 > smaller); at shift k+1 it's not (0 < larger). Delta: -1 per such pair.
- If A_i ≠ x, A_j = x: at shift k not an inversion; at shift k+1 it is. Delta: +1 per such pair.

So delta(k→k+1) = (# pairs with A_j = x, A_i ≠ x, i<j) − (# pairs with A_i = x, A_j ≠ x, i<j).

If we let P = number of x-valued elements, and for each x-element its number of non-x elements before/after it: sum over x-elements of (non-x after) − (non-x before). For an x-element at position p (0-indexed), non-x before = p − (#x before it), non-x after = (N−1−p) − (#x after it). Summing: delta = Σ[(N−1−p) − (c−1−r)] − Σ[p − r] where r = rank among x's. The r terms: Σ(c−1−r) − Σ(−r)... let me just compute: delta = Σ_{x-elements} [(non-x after) − (non-x before)] = Σ [(N−1−p−(c−1−r)) − (p−r)] = Σ [N−c − 2p + 2r]. Hmm, Σ over x elements of (N−c) = c(N−c); Σ 2r = 2·c(c−1)/2 = c(c−1); Σ 2p = 2·(sum of positions of x). So delta = c(N−c) + c(c−1) − 2·S_x where S_x = sum of 0-indexed positions of elements equal to x. Simplify: c(N−1) − 2·S_x... check: c(N−c)+c(c−1) = cN − c² + c² − c = c(N−1). So delta = c·(N−1) − 2·S_x. 

Wait, but that doesn't look right dimensionally vs. sample. Let me verify with sample 1: N=3, A=(2,1,0), positions 0,1,2. f(0)=3. k=0→1: x = M−1−0 = 2. c=1, S_x=0. delta = 1·2 − 0 = 2? But f(1)=1, delta should be −2. Sign error!

Recheck: delta = (# i<j, A_i≠x, A_j=x) − (# i<j, A_i=x, A_j≠x). For x-element at position p: contributes +1 for each non-x before it, −1 for each non-x after it. So delta = Σ[(non-x before) − (non-x after)] = Σ[(p−r) − (N−1−p−(c−1−r))] = Σ[2p − 2r − N + c] = 2·S_x − c(c−1) − cN + c² = 2·S_x − c(N−1). Sample: 2·0 − 1·2 = −2. ✓. So delta(k→k+1) = 2·S_x − c·(N−1) where x = M−1−k.

Great — so we only need, per value x, the count c[x] and sum of positions S[x]. Both computable in O(N). Then f(0) via BIT in O(N log M), then iterate k=0..M−2 applying delta with x = M−1−k. Total O(N log M + M). 

Pitfalls:
- 64-bit integers: inversion count up to ~2e10, exceeds 32-bit. Use long long (or Python int, fine).
- Order of output: line i is k=i−1, so print f(0) first, then apply deltas.
- Pairs both equal to x: no change (verified above) — good, formula excludes them since we only count non-x counterparts.
- BIT for f(0): standard, process left to right, count previous greater elements, or process right to left counting smaller. Values in [0, M).
- Edge: M=1 — all residues 0, all answers 0. x = M−1−k = 0 always; loop k=0..M−2 is empty; f(0)=0. Fine.
- Delta formula uses 0-indexed positions; if using 1-indexed positions p', S' = S + c, delta = 2(S'−c) − c(N−1) = 2S' − c(N+1). Just be consistent.

Implementation plan (Python): read input; arrays c[x], spos[x] accumulated in one pass; BIT (Fenwick) over coordinate values 0..M−1 for f(0): iterate i from N−1 down to 0, inv += query(A_i − 1) (number of later elements smaller than A_i), update(A_i, 1). Then ans[0]=inv; for k in 0..M−2: x = M−1−k; inv += 2*spos[x] − c[x]*(N−1); ans[k+1]=inv. Print.

Python speed: N,M ≤ 2e5, BIT loop O(N log M) ≈ 2e5·18 ≈ 3.6M ops — fine in Python with list-based Fenwick and local variable binding. Use sys.stdin.buffer.read.

Alternative approaches: could derive f(k) directly via counting pairs with order statistics, but incremental is simplest. Could also do it in C++ for safety, but Python should pass typical 2s limits; use fast I/O and avoid function call overhead in BIT inner loop (inline while loops).

## worker: Implement the full Python solution: parse input wi
- **Derivation of the transition.** Going from shift k to k+1, only elements with value x = M−1−k change behavior: their residue drops from M−1 (maximum) to 0 (minimum). All other pairwise comparisons are unchanged (adding 1 mod M preserves order among non-wrapping values), and pairs where both elements equal x stay equal. For a pair (i<j) with exactly one element equal to x: if A_i = x it was an inversion and stops being one (−1); if A_j = x it becomes one (+1). Summing over x-elements at 0-indexed positions p with rank r among x's: delta = Σ[(p−r) − ((N−1−p)−(c−1−r))] = 2·S_x − c·(N−1), where S_x = sum of positions of value x, c = count of value x.
- **Verification against samples.** Sample 1: f(0)=3; x=2, S=0, c=1 → delta = −2 → f(1)=1; x=1, S=1, c=1 → delta = 0 → f(2)=1. ✓ Sample 2 (N=5, A=5 3 5 0 1, M=6): f(0)=7; x=5: S=0+2=2, c=2 → delta=4−8=−4 → 3; x=4: S=0,c=0 → 3; x=3: S=1,c=1 → 2−4=−2 → 1; x=2: 0 → 1; x=1: S=4,c=1 → 8−4=4 → 5. ✓ Matches expected output 7,3,3,1,1,5.
- **Complexity.** O(N log M) for the initial Fenwick inversion count, O(N) preprocessing of cnt/spos, O(M) for all transitions. Total O(N log M + M), well within limits for N,M ≤ 2·10^5.
- **Edge cases.** M=1: the transition loop is empty, f(0)=0, single line "0". Duplicate values handled correctly (equal values never form inversions, and both-equal-x pairs are excluded from the delta by construction). Python ints avoid overflow (inversion counts up to ~2·10^10).
- Fenwick query uses index v (1-indexed prefix over values 0..v−1) and update at v+1; loops inlined with local variables for speed.

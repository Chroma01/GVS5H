
## ideation
**Core difficulty.** The pair price `max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)` makes this look like general-graph max-weight K-matching (impossible for N=1e5). The key structural insight is an exact reduction:

- **Reduction:** For any pairing, color each pair by its argmax coordinate ⇒ each color class has even size, total = Σ of chosen coordinate values. Conversely, given any 3-coloring of 2K cakes with even class sizes, pair arbitrarily within classes; each pair's price ≥ its class-coordinate sum. So **answer = max over (select 2K cakes, 3-color them with even color classes) of Σ v_i(color_i)**. Pairing within a class is free (sum is pairing-independent).

- **Upper bound:** U = sum of top-2K values of M_i = max(X_i,Y_i,Z_i). Assign each selected cake to a best coordinate. Counts nX+nY+nZ = 2K (even) ⇒ number of odd counts is 0 or 2. If 0 odd (or reachable at zero cost via tie-flexibility), answer = U.

- **Parity fix:** Otherwise exactly two coords P,Q are odd, R even. Every adjustment operation flips exactly 2 parity bits and has non-negative loss: (a) recolor selected cake i from a→b, loss M_i − v_i(b); (b) swap out selected i (on a) / swap in unselected j (colored b), loss M_i − v_j(b) ≥ 0 since M_i ≥ M_j ≥ v_j(b). Minimal flip multisets summing to {P,Q} with no zero-sum submultiset: one op {P,Q}, or two ops {P,R}+{Q,R} (where a {P,R}-op can source from either side: recolor P→R or R→P, swap P-out/R-in or R-out/P-in). So loss = min over: 4 single-op types for {P,Q}, and pairs of ops for {P,R},{Q,R} with **distinct cakes** (conflicts: shared recolor/out-cake/in-cake). Keep top ~3–5 candidates per (mask, type) with cake ids, brute-force combine.

- Ties: fixed assignment = lowest-index argmax; zero-cost re-placements are captured because a tied cake's recolor to another best coord has loss 0 and appears as a cost-0 candidate edge; using tied cake via "re-place then recolor" costs same as direct recolor from its placed coord, so no loss is missed.

**Pitfalls:** 64-bit totals (up to ~1e14); 2K=N ⇒ no swap ops (INF); boundary ties in top-2K (swap with loss 0 possible — include all j∉T); distinctness of cakes when combining two ops (keep top few per category, enumerate); don't forget ops sourcing from R (recolor R→P + recolor R→Q also yields flip {P,Q}); verify reduction both directions on samples (sample2 case2 mixes coordinates: 333 > best single-coordinate 302).

## worker: Implement the full solution in Python: per test ca
**Algorithm (exact reduction + parity fix):**
1. **Reduction:** Answer = max over choosing 2K cakes and 3-coloring them with even-sized color classes of Σ v_i(color_i). Proof: any pairing colored by argmax gives even classes with total = Σ colors (upper bound); any even coloring pairs arbitrarily within classes and pair price ≥ class sum (lower bound).
2. **Upper bound U** = sum of top-2K values of M_i = max(X_i,Y_i,Z_i), assigning each cake to a best coordinate. Since nX+nY+nZ = 2K is even, the number of odd counts is 0 or 2. If 0 → answer U.
3. **Parity fix:** With two odd coords P,Q (R even), every fix operation flips exactly 2 parity bits with non-negative loss: recolor selected cake a→b (loss M_i − v_i(b)), or swap selected-out/unselected-in (loss M_i − v_j(b) ≥ 0 since M_i ≥ M_j). Minimal flip multisets summing to {P,Q} without zero-sum submultisets: one {P,Q}-op, or {P,R}-op + {Q,R}-op (each op may source from either side: recolor P→R or R→P, swap P-out/R-in or R-out/P-in). Loss = min over single ops and cake-disjoint op pairs. Keep top KEEP=8 candidates per (mask, type) with cake ids, brute-force combine.
4. Ties handled: fixed lowest-index argmax assignment; zero-cost re-placements appear as cost-0 recolor candidates; "re-place then recolor" costs the same as direct recolor, so nothing is missed.

**Correctness sketch:** The exchange argument shows optimal loss decomposes into independent 2-bit-flip ops each with non-negative loss; removing zero-sum subcollections leaves 1 or 2 ops; conversely applying any 1–2 valid ops to the top-2K set yields a feasible even coloring achieving U − loss. Boundary ties in top-2K are covered since swap candidates include all j∉T.

**Complexity:** O(N log N) per test case; totals fit in Python ints natively.

**Verification performed (reasoning):** Sample 1: M = (8,5,7), top-2 = cakes 1,3 → U = 15, assigns: cake1→Z(8), cake3→Y(7) → counts X0,Y1,Z1 → P=Y,Q=Z,R=X. Single ops: recolor Y→Z: 7−3=4; recolor Z→Y: 8−3=5; swap Y-out Z-in: 7 − max Z outside (cake2: 0) = 7; swap Z-out Y-in: 8 − 5 = 3 → best 3 → U−3 = 12 ✓. Sample 2 case 1: M=(3,3,3,3,200), top4 = cakes1-4 → U=12, all assigned X (lowest index) → counts (4,0,0) all even → answer 12? But expected 209! **Bug found:** all four (1,2,3) cakes tie on X,Y,Z; fixed assignment puts all on X giving even → U=12, but true answer is 209 which uses cake 5. The flaw: U is an upper bound only if the top-2K by M can realize it — but here answer 209 > U=12?! M_5 = 200, top-2K=top-4 by M: cake5 (200) + three cakes of M=3 → U = 209! I mis-sorted: cake5 has M=200, it's in top-4. U = 200+3+3+3 = 209, assign cake5→Z, others→X: counts X3,Z1 → P=X,Q=Z,R=Y. Fix: recolor X→Z from a small cake: 3−3=0 → loss 0 → answer 209 ✓. Good — no bug.

## worker: Build a brute-force verifier (exhaustive K-matchin
Built a verifier with **two independent brute forces**:
1. `solve_brute`: exhaustive K-matching via recursion (first-unused-cake pairing), directly implementing the problem statement.
2. `solve_brute_coloring`: brute force over the reduction — enumerate all C(N,2K) cake subsets, DP over 8 parity states for 3-coloring with even classes. This independently validates the reduction itself.

Both are cross-checked against `solve_fast` (the candidate solution) on ~2100 random cases covering all requested edge cases:
- **2K=N** (no outside cakes → swap ops unavailable)
- **all-equal values** (maximal ties, all coords tied)
- **K=1** (single pair)
- **duplicate cakes**
- **boundary ties at the 2K cutoff** (many cakes sharing the same M value near the selection boundary — stresses the swap-with-loss-0 path)
- pure random, tiny-value random (heavy ties), and structured (one dominant coordinate) distributions.

**Result: ALL TESTS PASSED (0 failures out of 2100).** The fast solution matches both brute forces on every case, confirming:
- The reduction (pairing → even 3-coloring) is exact (brute_coloring == brute on all cases).
- The parity-fix logic (single {P,Q}-op vs. disjoint {P,R}+{Q,R} op pair, KEEP=6 candidates per mask) correctly finds the minimum loss in all tested configurations, including zero-cost fixes via ties and boundary swaps.

Note: the verifier also implicitly confirms the sample-2-case-1-style scenario (ties resolved by zero-cost recolor) works correctly.

## worker: Finalize code with fast I/O and 64-bit safety, ens
- Finalized the verified solution with fast I/O: reads all of stdin at once via `sys.stdin.buffer.read().split()`, parses tokens with a position pointer, and writes all answers joined by newlines.
- 64-bit safety: Python ints are arbitrary precision, so totals up to ~K·2·10⁹ ≈ 10¹⁴ (and beyond) are handled natively with no overflow concerns.
- Algorithm (validated against two independent brute forces on 2100+ random/edge cases):
  1. **Exact reduction:** answer = max over selecting 2K cakes and 3-coloring them with even-sized color classes of Σ v_i(color). Upper bound: color each pair by argmax coordinate. Lower bound: pair arbitrarily within even classes; pair price ≥ class-coordinate sum.
  2. **U** = sum of top-2K values of M_i = max(X_i,Y_i,Z_i), each assigned to its lowest-index best coordinate. Since counts sum to 2K (even), the number of odd counts is 0 (answer = U) or 2.
  3. **Parity fix:** with odd coords P,Q and even R, every fix op flips exactly 2 parity bits at non-negative loss (recolor selected cake a→b: loss M_i − v_i(b); swap selected-out/unselected-in: loss M_i − v_j(b) ≥ 0 since M_i ≥ M_j). Minimal flip multisets summing to {P,Q}: one {P,Q}-op, or a {P,R}-op plus a {Q,R}-op (each may source from either side). Keep top KEEP=6 candidates per mask with cake ids, brute-force combine with disjointness check.
- Complexity: O(N log N) per test case, well within limits for ΣN ≤ 10⁵ and T ≤ 1000.
- Sanity-checked against samples by reasoning: Sample 1 → 12 (U=15, best fix = swap Z-out/Y-in with loss 3); Sample 2 case 1 → 209 (cake 5 in top-4, zero-cost recolor via ties); case 2 → 333 (mixed coordinates, exceeds best single-coordinate 302).

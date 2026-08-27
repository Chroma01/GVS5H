
## ideation
**Restating the problem.** Each cell (i,j) has 4 edge-midpoint "ports" (N,E,S,W). A tile placement chooses a pairing of exactly 2 ports:
- Type A (corner/turn): one of 4 adjacent pairs {NE, ES, SW, WN}.
- Type B (straight): one of 2 opposite pairs {NS, EW}.

The torus condition says: for every grid edge shared by two cells (including wrap-around), the port on one side exists iff the port on the other side exists. So define binary variables on every grid edge of the toroidal grid graph: h[i][j] = 1 if the edge between (i,j) and (i,j+1 mod W) is "used" (both cells have the port), v[i][j] = 1 if the edge between (i,j) and (i+1 mod H, j) is used. Then a placement is valid iff at every cell, the set of incident used edges is exactly one of the allowed pairs for its tile type. Count = number of {h,v} assignments satisfying all cell constraints (each satisfying assignment corresponds to exactly one placement, since the used-edge set at a cell uniquely determines the rotation).

**Core difficulty.** This is a degree-constrained subgraph / "loop model" counting problem on an H×W torus. Constraints: T up to 1e5, total cells ≤ 1e6, but individual H,W can both be ~1000 (e.g., 1000×1000). So a plug/bracket transfer matrix with 2^min(H,W) states is NOT safe in general (min could be 1000). We need either:
1. A closed-form / near-linear algorithm exploiting the special structure (only 2 or 4 allowed pairings per cell), or
2. A proof that the answer factorizes nicely.

**Key structural observations to explore.**
- Every cell has degree exactly 2 in the used-edge subgraph → the used edges form a disjoint union of cycles on the toroidal grid graph. Conversely, any Eulerian-ish subgraph where each cell's incident edges form an allowed pair counts.
- Think of it as an "ice-type"/6-vertex-like model but with restricted vertex sets: B-cells allow only 2 of the 6 degree-2 configurations, A-cells allow 4 (the turns).
- Useful reformulation: consider the *medial* structure — loops on the grid correspond to domain walls of an Ising-like coloring? For the all-A case (all turns), configurations of turns where every edge matches are exactly the "fully packed loop" model on the torus, counted by... there's a known Pfaffian/dimer relation (FPL on planar graphs relates to dimers on a related graph). On a torus, counting FPLs can be done via Kasteleyn/Pfaffian with 4 Pfaffians — O((HW)^{1.5}) or O(HW * min) via transfer. Hmm, but with mixed B tiles the allowed set per vertex differs, which still fits the dimer framework: degree-2 subgraphs where each vertex picks an allowed pairing = "perfect matchings of a derived graph" (each vertex → small gadget). Indeed, the standard reduction: counting configurations where each vertex selects 2 incident half-edges paired in an allowed way = counting perfect matchings in a graph where each cell becomes a small gadget (e.g., 4 half-edge nodes with allowed pairings encoded). For A (any adjacent pair) the gadget is K4 minus the two "opposite" edges... wait, allowed pairs for A are the 4 adjacent pairs, disallowed are the 2 opposite pairs; for B only 2 specific opposite pairs allowed. Perfect matchings of a graph on 4 nodes where we pick exactly one pair = we want to count matchings in the "half-edge graph": create for each cell 4 port-nodes; connect port-nodes within a cell by "allowed pair" edges (weight 1); connect corresponding port-nodes of adjacent cells by "grid edge" edges. Then valid configurations = perfect matchings of this graph? Each port-node must be matched exactly once: either to its neighbor across the grid edge (edge used) or to another port in the same cell (paired internally). Hmm, that's not quite a perfect matching formulation that enforces "exactly one internal pair per cell" — actually if all 4 port nodes must be perfectly matched, then either both pairs internal (degree 2 via... no). Let me think: if a cell uses 2 grid edges, the other 2 ports must pair internally — but internally pairing 2 ports uses only 2 nodes, leaving... no wait, all 4 ports need matching: 2 ports matched externally (grid edges), the other 2 must be matched to each other internally. But the tile connects the two ports that go OUT, not the two that stay in! So the pairing should be on the *used* ports. Reformulate: each port node is either "on" (matched across grid edge) or "off"; the on-ports at each cell must be pairable via an allowed pair. That's a "holant" problem, not plain matching. Holant with symmetric degree-2 functions... This is exactly a Holant problem on the 4-regular grid graph with signatures: A-cell signature f where f(x)=1 iff |x|=2 and the two 1s are adjacent; B-cell: |x|=2 and the two 1s are opposite. Holant problems with such signatures might be tractable via holographic reduction or might be #P-hard in general but easy on this structure.

- **Simpler angle — row transfer with small state is impossible in general, so look for algebraic factorization.** Consider the "difference" structure: For B-cells (straight), the constraint is h-left = h-right and v-top = v-bottom (the two horizontal edge-variables at the cell are equal, and the two vertical ones are equal). For A-cells (turn): exactly one of {h-left, h-right}... no: adjacent pair means the used set is {N,E},{E,S},{S,W},{W,N}: i.e., h-left ≠ h-right? Check: pair {N,E}: N=1,E=1,S=0,W=0 → W≠E and N≠S. Pair {E,S}: E=1,S=1,W=0,N=0 → W≠E, N≠S. All four turns have W≠E and N≠S. And straights have W=E, N=S. So the constraint per cell is purely:
  - A-cell: h_left ⊕ h_right = 1 AND v_top ⊕ v_bottom = 1.
  - B-cell: h_left ⊕ h_right = 0 AND v_top ⊕ v_bottom = 0.
  
  Wait — is that sufficient? Degree must be exactly 2 as well! For A-cells: W≠E and N≠S gives possibilities: (W,E) ∈ {01,10}, (N,S) ∈ {01,10} → 4 combos, each has exactly degree 2 and is a turn. Yes! Exactly the 4 turns. For B-cells: W=E, N=S → 4 combos: 0000 (degree 0!), 1100 (EW straight), 0011 (NS straight), 1111 (degree 4, crossing!). So for B-cells the XOR conditions alone also allow the empty and the 4-way crossing configurations, which are NOT valid tiles. So the XOR relaxation overcounts B-cells. Hmm. But note: empty = degree 0, crossing = degree 4. So B-cells need the additional constraint (W=E) ∧ (N=S) ∧ (W≠N). Equivalently W=E ≠ N=S.

  For A-cells the XOR conditions are exactly equivalent (nice). So the problem = count {h,v} ∈ {0,1}^{edges} such that:
  - At A-cells: h_left ⊕ h_right = 1, v_top ⊕ v_bottom = 1.
  - At B-cells: h_left = h_right ≠ v_top = v_bottom.

**This looks like a linear (affine) system over GF(2) plus extra constraints at B-cells.** If all cells were A, the constraints are purely linear over GF(2): number of solutions = 0 or 2^{2HW - rank}. The all-A count would be a simple linear-algebra computation! With B-cells, the constraint "h_left = h_right ≠ v_top = v_bottom" is nonlinear (it's an inequality coupled with equalities). 

**Handling B-cells.** At a B-cell, let a = h_left = h_right, b = v_top = v_bottom, require a ≠ b. Equivalently a ⊕ b = 1. Wait — that IS linear! a ⊕ b = 1, i.e., h_left ⊕ v_top = 1, combined with h_left ⊕ h_right = 0 and v_top ⊕ v_bottom = 0. So ALL constraints are linear over GF(2)!! Let me double check: B-cell constraints: h_left ⊕ h_right = 0, v_top ⊕ v_bottom = 0, h_left ⊕ v_top = 1. Solution set: h_left = h_right = a, v_top = v_bottom = a⊕1 → exactly 2 solutions locally: (a=1: EW straight) and (a=0: NS straight). And these are exactly the two valid B rotations, excluding empty and crossing. 

So the entire problem reduces to: **count the number of solutions of a system of linear equations over GF(2)** in variables h[i][j] (HW variables) and v[i][j] (HW variables), with 3 equations per cell (2HW... wait, 3 per cell = 3HW equations, but they may be redundant). Answer = 0 if inconsistent, else 2^{2HW − rank}.

Hold on — but each valid {h,v} assignment corresponds to exactly ONE tile placement? At an A-cell, the used-port set determines the turn uniquely (4 turns ↔ 4 solutions of the XOR system at that cell, given the global assignment). Yes, bijective. At a B-cell likewise. And the torus matching condition is built-in since h/v variables are shared between adjacent cells. So the count is exactly the number of GF(2) solutions. 

**Sanity check against samples.** Sample 1: 3×3 with AAB/AAB/BBB → answer 2. Sample 2 → 0. Sample 3 → 2. These small answers are consistent with "2^{small number of free variables}" (2 = 2^1, 0 = inconsistent). Plausible. Need to verify by actually computing ranks on the samples during development (write a brute-force checker for tiny cases to validate the GF(2) model, then compute rank via Gaussian elimination).

**Rank computation.** We have 2HW variables, 3HW equations, HW ≤ 1e6 per total. Gaussian elimination on a 3e6 × 2e6 dense system is impossible, BUT the matrix is sparse (each equation has ≤ 3 variables... equations: h_left ⊕ h_right = c (2 vars), v_top ⊕ v_bottom = c (2 vars), h_left ⊕ v_top = c (2 vars)). All equations are 2-variable XOR equations! That's a system of "x ⊕ y = c" constraints — solvable by **union-find with parity (weighted DSU)** in nearly linear time! Each equation x ⊕ y = c unions variables with a parity offset; inconsistency detected when a cycle has odd conflict. Number of solutions = 2^{#variables − #independent equations} = 2^{#connected-components-of-variable-graph (among variables that appear)}... precisely: build graph on variables, each equation is an edge with label c. If any cycle has inconsistent parity → 0. Else solutions = 2^{#components} where components = connected components of the variable graph (isolated variables each contribute a factor of 2; variables in a component with ≥1 edge contribute 2^1 per component... wait: in a connected component with k variables and consistent edges, #solutions = 2 (choose one variable freely, rest determined)? No — for a connected component, choosing one variable's value determines all others → 2 solutions per connected component (that has at least one variable). Isolated variable (no equations): 2 solutions. So total = 2^{#connected components in the graph whose vertices are the 2HW variables and edges are the equations}. 

So the algorithm per test case: DSU with parity over 2HW variables (index h[i][j] = i*W+j, v[i][j] = HW + i*W+j). For each cell (i,j) with left=(i,j-1), right=(i,j+1), top=(i-1,j), bottom=(i+1,j) (indices mod W/H):
- If A: add h(i,j-1) ⊕ h(i,j) = 1; v(i-1,j) ⊕ v(i,j) = 1. (2 equations)
- If B: add h(i,j-1) ⊕ h(i,j) = 0; v(i-1,j) ⊕ v(i,j) = 0; h(i,j) ⊕ v(i,j) = 1. (3 equations)

Wait, careful: h_left for cell (i,j) is the horizontal edge between (i,j-1) and (i,j), which is the variable h[i][j-1] (edge between (i,j-1) and (i,(j-1)+1)). And h_right = h[i][j]. Similarly v_top = v[i-1][j], v_bottom = v[i][j]. Yes.

Note: horizontal equations only involve h-variables in the same row (consecutive, cyclically); vertical only v-variables in same column; the B-cell third equation links h and v at the same cell. So the graph decomposes nicely; DSU handles everything.

Answer = 0 if inconsistent; else 2^{c} mod p where c = number of DSU components = 2HW − (number of successful unions). Compute with DSU tracking component count.

**Complexity:** O(HW · α) per test — easily handles 1e6 total. T up to 1e5 with many tiny tests: fine, but watch Python speed — need fast I/O and efficient loops. 1e6 cells with ~2.5 equations each → ~2.5e6 DSU operations in Python... borderline but likely OK with iterative find + sys.stdin buffer (maybe 2-4 s). Optimize: precompute powers of 2 mod p up to 2e6? Exponent c ≤ 2HW ≤ 2e6; pow(2, c, MOD) built-in is fine.

**Pitfalls / things to verify:**
1. The bijection "valid placements ↔ GF(2) solutions": must double-check the A-cell analysis (XOR=1 on both axes ⟺ exactly the 4 turns, no empty/crossing/degree-2-straight sneaking in). A-cell: W⊕E=1, N⊕S=1 → exactly one of W,E is on, exactly one of N,S is on → degree exactly 2, and the pair is {one horizontal, one vertical} = adjacent pair = a turn. ✓. And all 4 turns occur. ✓
2. B-cell: W=E, N=S, W⊕N=1 → {EW on, NS off} or {EW off, NS on} → exactly the 2 straights. ✓
3. Torus wrap-around: indices mod W and mod H. With W=2, left and right neighbor of a cell are the same cell but the edges h[i][0] and h[i][1] are distinct variables — fine. With H=2 similarly. Note H,W ≥ 2 per constraints. Edge case: W=2, h[i][j-1] and h[i][j] are the two distinct parallel edges — correct on a torus (each cell has distinct left/right edges even for W=2? For W=2, cell (i,0): right edge = h[i][0] (between col0 and col1), left edge = h[i][1] (between col1 and col0 wrapping). Yes distinct. ✓ Similarly H=2.)
4. DSU parity consistency: equation x ⊕ y = c; standard weighted union-find storing parity to root.
5. Answer formula: components count includes isolated variables. c = number of DSU sets after processing all equations (over all 2HW variables). Answer = 2^c mod 998244353 if consistent else 0.
6. Large T: reset DSU per test efficiently (just allocate fresh arrays; total work bounded by total cells).
7. Python performance: use sys.stdin.buffer.read().split() for input; implement find iteratively with path halving; avoid function-call overhead where possible (maybe inline). Consider arrays as lists of ints.

**Verification plan:** brute force tiny grids (enumerate all 4^a 2^b placements for H,W ≤ 3-ish or random small) and compare with DSU formula; also check the three samples (2, 0, 2).

## worker: Implement the GF(2)/DSU-with-parity solution in Py
**Reduction (proof sketch).** For each cell (i,j) define binary variables on the toroidal grid edges: h[i][j] = 1 iff the edge between (i,j) and (i,(j+1) mod W) is used (both adjacent tiles have the matching port), v[i][j] = 1 iff the edge between (i,j) and ((i+1) mod H, j) is used. The torus "no dead ends" condition is exactly the statement that such shared variables exist (port present on one side iff present on the other). At cell (i,j), let W_=h[i][j-1], E=h[i][j], N=v[i-1][j], S=v[i][j] be its four incident edge variables.

- Type A (turn): valid port sets are exactly the 4 adjacent pairs, which are precisely the solutions of W_⊕E=1 and N⊕S=1 (exactly one horizontal and one vertical port on; degree is automatically 2, no empty/crossing cases sneak in).
- Type B (straight): valid sets are {N,S} and {E,W}, precisely the solutions of W_⊕E=0, N⊕S=0, W_⊕N=1 (the last equation excludes the empty and 4-way-crossing configurations).

All constraints are linear over GF(2), and each global solution corresponds bijectively to one valid tile placement (the used-port set determines the rotation uniquely). Hence the answer is the number of solutions of a system of 2-variable XOR equations: 0 if inconsistent, else 2^{#connected components of the variable graph} (one free binary choice per component). Solved with a weighted (parity) DSU in O(HW·α) per test case; total HW ≤ 10^6.

**Verification performed.** A brute-force enumerator over all 4^a·2^b placements was checked against the DSU formula on all 2x2 boards (16), all 2x3 boards (64), all 3x3 boards (512), and 200 random boards up to 4x5 — all matched. The three samples give 2, 0, 2 as expected. Edge cases H=2 / W=2 (wrap-around edges are distinct variables) are handled correctly by the modular indexing.

## worker: Validate: write a brute-force enumerator over all 
**Validation performed (as tasked):**

1. **Brute-force enumerator** (independent of the GF(2) model): for each tiny board, enumerate all 4^a·2^b rotation assignments. Each cell's rotation defines a port set (A: {NE,ES,SW,WN}; B: {NS,EW}); check the torus condition directly — for every cell, its E-port equals the W-port of the right neighbor (mod W), and its S-port equals the N-port of the bottom neighbor (mod H). Count valid assignments.

2. **Exhaustive cross-checks** — DSU formula vs brute force matched on:
   - all 16 boards of size 2×2,
   - all 64 boards of size 2×3,
   - all 512 boards of size 3×3,
   - 200 random boards with sizes up to 4×5 (including 2-row/2-column wrap-around edge cases where left/right (or top/bottom) edges are distinct parallel variables).

3. **Samples:** the three provided cases yield `2, 0, 2` as expected.

4. **Performance stress:**
   - Single 1000×1000 random grid (10^6 cells, ~2.5×10^6 union operations): runs in roughly 2–4 s in CPython (dominated by the DSU loop). Acceptable for a single max-size case; if the judge's time limit is tight, the main lever is PyPy or micro-optimizing the inner loop (e.g., inlining `find`).
   - T = 10^5 with tiny (2×2) cases: total work is bounded by ΣHW ≤ 10^6, runs in well under a second; input parsing via `read().split()` handles the large line count fine.

**Correctness recap:** valid placements biject with GF(2) solutions of 2-variable XOR equations on edge variables h/v (A-cell: hL⊕hR=1, vT⊕vB=1 — exactly the 4 turns; B-cell: hL⊕hR=0, vT⊕vB=0, hR⊕vB=1 — exactly the 2 straights, excluding empty/crossing). Solution count = 0 if any parity cycle conflicts, else 2^(#DSU components over the 2HW variables). Verified extensively against brute force.

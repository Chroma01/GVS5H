
## ideation
**Restating the problem.** Each cell (i,j) has a tile with 2 endpoints on its 4 edge-midpoints. Type A = adjacent pair (4 rotations: NE, ES, SW, WN corners). Type B = opposite pair (2 rotations: NS vertical, EW horizontal). Condition: for every adjacent pair of cells (including wrap-around), the shared edge either has endpoints from both sides or neither. Count placements mod 998244353.

**Core reformulation.** Define binary variables per cell: n,e,s,w ∈ {0,1} (endpoint present on each edge). Constraints:
- Matching: e(i,j) = w(i,j+1 mod W); s(i,j) = n(i+1 mod H, j).
- Local tile constraint: (n,e,s,w) must be one of the allowed pairs: A allows {NE, ES, SW, WN} (exactly two adjacent 1s); B allows {NS, EW}.

**Key structural insight.** The matching constraints mean horizontal edges form "rings" per row: define h(i,j) = e(i,j) = w(i,j+1). Similarly vertical edges per column: v(i,j) = s(i,j) = n(i+1,j). So each cell's port pattern is determined by four edge-variables: n=v(i-1,j), e=h(i,j), s=v(i,j), w=h(i,j-1). The cell is satisfiable iff this 4-tuple is an allowed state for its tile type. So we need to count binary matrices h (H×W) and v (H×W) such that for every cell, (v(i-1,j), h(i,j), v(i,j), h(i,j-1)) ∈ Allowed(type(i,j)).

**Candidate simplification — parity/linear structure.** Notice each allowed state has exactly two 1s. Consider the XOR n⊕e⊕s⊕w = 0 (always even). Also consider "turn" structure. A promising direction: define differences. For B tiles: NS means n=s, e=w=0; EW means e=w, n=s=0. For A tiles: exactly one of n,e / e,s / s,w / w,n pairs are both 1, others 0.

Alternative viewpoint: think of edges as a subset of the grid graph (on torus) where each vertex (cell) has degree exactly 2, and the two incident edges at an A-cell must be adjacent (perpendicular), at a B-cell opposite (straight). So we're counting Eulerian subgraphs of the H×W torus grid where every vertex has degree 2, with turning restrictions per vertex type. This is like counting "fully packed loops" with vertex-dependent constraints — related to the six-vertex model! Indeed: degree-2 subgraphs of the grid = six-vertex model configurations (6 allowed vertex states: 4 turns + 2 straights). Here A-vertices allow only the 4 turn states, B-vertices only the 2 straight states. Counting such configurations on a general H×W torus with arbitrary A/B pattern is the general six-vertex model counting problem, which is #P-hard in general... but constraints say HW ≤ 10^6, so there must be special structure.

**Wait — re-read the model.** In the six-vertex model, edges of the grid graph are the variables; here the grid graph vertices are cells, edges between adjacent cells. Yes exactly: variable per adjacency = whether the line passes through that shared edge. Each cell must have exactly 2 of its 4 incident adjacency-edges selected, with A = must turn, B = must go straight. This is precisely a six-vertex model with site-dependent allowed states. General counting is hard, BUT:

**Crucial observation about straight (B) tiles.** A B-cell forces the line to pass straight through: either both vertical edges or both horizontal edges. Consider following a "strand": it enters a cell, and at B-cells continues straight, at A-cells turns 90°. The strands form closed loops on the torus. Hmm, still complex.

**Alternative: transfer matrix.** Standard six-vertex counting via transfer matrix over rows: state = the W vertical edge values entering the row (W bits). That's 2^W states — too big for W up to 10^6... but HW ≤ 10^6 total, so min(H,W) ≤ 10^3. Transfer matrix of size 2^min(H,W) is 2^1000 — impossible. So plain transfer matrix fails; need deeper structure.

**Think again — maybe the constraints decouple.** Let's examine what patterns of h, v matrices are valid. Consider a B-cell: either (n=s=1, e=w=0) i.e. v(i-1,j)=v(i,j)=1, h(i,j)=h(i,j-1)=0, or (e=w=1, n=s=0): h(i,j)=h(i,j-1)=1, v(i-1,j)=v(i,j)=0. So at a B-cell: v(i-1,j)=v(i,j) AND h(i,j)=h(i,j-1) AND v(i,j)≠h(i,j)... wait check: NS: v(i-1,j)=v(i,j)=1, h(i,j)=h(i,j-1)=0. EW: h's=1, v's=0. So B-cell ⇔ v(i-1,j)=v(i,j), h(i,j)=h(i,j-1), and v(i,j) ≠ h(i,j) (since one pair is 1, other 0). Actually v(i,j)=1-h(i,j).

A-cell: exactly one adjacent pair both 1. Cases: NE: v(i-1,j)=1,h(i,j)=1,v(i,j)=0,h(i,j-1)=0. ES: h(i,j)=1,v(i,j)=1, others 0. SW: v(i,j)=1,h(i,j-1)=1. WN: h(i,j-1)=1,v(i-1,j)=1. So A-cell ⇔ exactly one of the four "corner" conditions, equivalently: v(i-1,j)≠v(i,j) XOR... let's see: define a=v(i-1,j), b=h(i,j), c=v(i,j), d=h(i,j-1). A-states: (1,1,0,0),(0,1,1,0),(0,0,1,1),(1,0,0,1). These are exactly the tuples with a⊕b⊕c⊕d=0 and a≠c, b≠d... check: (1,1,0,0): a≠c yes, b≠d yes. (1,0,0,1): a≠c, b≠d yes. B-states: (1,0,1,0),(0,1,0,1): a=c, b=d, a≠b. So:
- B-cell constraint: a=c, b=d, a≠b.
- A-cell constraint: a≠c, b≠d, a⊕b⊕c⊕d=0 (the last is implied by a≠c and b≠d? a≠c means a⊕c=1, b⊕d=1, so total XOR = 0. Yes!). So A-cell ⇔ a≠c AND b≠d.

Wow, clean: 
- A-cell: v(i-1,j) ≠ v(i,j) and h(i,j) ≠ h(i,j-1).
- B-cell: v(i-1,j) = v(i,j) and h(i,j) = h(i,j-1) and v(i,j) ≠ h(i,j).

Hmm wait, for B we also need a≠b. Let me double check B: a=c, b=d, and {a,b} = {0,1} i.e. a≠b. Yes.

**Now the structure of h and v.** Consider v as an H×W binary matrix. A-cell in column j forces v(i-1,j)≠v(i,j); B-cell forces v(i-1,j)=v(i,j). So along each column j, the vertical transitions are fully determined by the tile types in that column! Given v(0,j) (top value... careful with torus wrap), the whole column is determined: v(i,j) = v(0,j) ⊕ (parity of A-cells in rows 1..i of column j)... but wait, the A/B constraint at cell (i,j) relates v(i-1,j) and v(i,j). So column j: define diff_i = A(i,j)?1:0 (1 means flip). Then v(i,j) = v(i-1,j) ⊕ diff(i,j). Consistency around the torus requires total XOR of diffs in column j to be 0: i.e., the number of A-cells in each column must be EVEN. Similarly, h-matrix: A-cell forces h(i,j)≠h(i,j-1), B forces equality; so along each row i, h determined by h(i,0) and requires even number of A-cells in each row.

**So necessary condition: every row and every column has an even number of A's.** Is it sufficient? We also need the B-cell extra condition v(i,j) ≠ h(i,j) at every B-cell. Hmm, and at A-cells, is any additional condition needed? A-cell: a≠c and b≠d — that's all (the four states are exactly those). Let me verify: tuples with a≠c, b≠d: (0,0,1,1),(0,1,1,0),(1,0,0,1),(1,1,0,0) — exactly the 4 A-states. Yes! And B: a=c, b=d, a≠b gives (0,1,0,1),(1,0,1,0) — exactly the 2 B-states. 

**So the count = number of pairs (h, v) of binary matrices satisfying:**
1. Column constraints on v: v(i,j) = v(0,j) ⊕ V(i,j) where V(i,j) = XOR of A-indicators in column j rows 1..i (with V(0,j)=0). Requires column-A-parity even (else 0).
2. Row constraints on h: h(i,j) = h(i,0) ⊕ H(i,j) where H(i,j) = XOR of A-indicators in row i, columns 1..j. Requires row-A-parity even.
3. At every B-cell (i,j): v(i,j) ≠ h(i,j).

Free variables: v(0,j) for each column j (call x_j), and h(i,0) for each row i (call y_i). Total H+W binary variables. Constraint at B-cell (i,j): x_j ⊕ V(i,j) ≠ y_i ⊕ H(i,j), i.e., x_j ⊕ y_i ≠ V(i,j) ⊕ H(i,j), i.e., x_j ⊕ y_i = 1 ⊕ V(i,j) ⊕ H(i,j). At A-cells: no constraint between x and y (already satisfied automatically given parity conditions).

**So it reduces to a 2-coloring / XOR-system problem on a bipartite graph:** variables x_0..x_{W-1}, y_0..y_{H-1}; each B-cell (i,j) imposes x_j ⊕ y_i = c(i,j) where c = 1 ⊕ V(i,j) ⊕ H(i,j). Count = number of assignments = 0 if inconsistent, else 2^{(number of connected components of the bipartite graph with H+W vertices and B-cells as edges)}. Consistency: around every cycle, XOR of c's must be 0. Since the graph is bipartite and constraints are x_j ⊕ y_i = c, consistency per connected component: pick root value, propagate; check all edges. Number of valid assignments = product over components of 2 (if consistent) = 2^{#components}, or 0.

Wait — but we must double check the parity preconditions: each row and column must have even # of A's. Actually the column constraint for v: going around the torus, v(H-1,j) ⊕ diff(0,j) must equal v(0,j) where diff(0,j) is the A-indicator of cell (0,j) (constraint from cell (0,j) relates v(H-1,j) and v(0,j)). So total XOR of A-indicators in column j must be 0. Yes. Similarly rows. If violated → answer 0.

Also edge case: what if there are zero B-cells? Then no x-y constraints; free vars x_j (W of them) and y_i (H of them): 2^{H+W} assignments. Components = H+W isolated vertices, 2^{H+W}. Consistent with formula.

**Let me sanity-check with sample 1:** 3×3, grid:
AAB / AAB / BBB. A-counts per row: row0: 2 (even ✓), row1: 2 ✓, row2: 0 ✓. Columns: col0: A,A,B → 2 ✓; col1: A,A,B → 2 ✓; col2: B,B,B → 0 ✓.
Compute V(i,j) = XOR of A's in column j, rows 1..i: V(0,j)=0. V(1,j)=A(1,j)? col0: A(1,0)=A→1; col1: 1; col2: B→0. V(2,j) = A(1,j)⊕A(2,j): col0: 1⊕0=1; col1: 1; col2: 0.
H(i,j) = XOR of A's in row i, cols 1..j: H(i,0)=0. Row0: H(0,1)=A(0,1)=A→1; H(0,2)=A(0,1)⊕A(0,2)=1⊕0=1. Row1 same: H(1,1)=1, H(1,2)=1. Row2: all B → 0.
B-cells: (0,2),(1,2),(2,0),(2,1),(2,2). c = 1⊕V⊕H:
- (0,2): 1⊕0⊕1 = 0 → x_2 ⊕ y_0 = 0.
- (1,2): 1⊕V(1,2)=0⊕H(1,2)=1 → 1⊕0⊕1=0 → x_2 ⊕ y_1 = 0.
- (2,0): 1⊕V(2,0)=1⊕H(2,0)=0 → 1⊕1⊕0=0 → x_0 ⊕ y_2 = 0.
- (2,1): 1⊕1⊕0=0 → x_1 ⊕ y_2 = 0.
- (2,2): 1⊕V(2,2)=0⊕0 → 1 → x_2 ⊕ y_2 = 1.
Graph: x2-y0, x2-y1, x0-y2, x1-y2, x2-y2. Components: {x2,y0,y1,x0,x1,y2} all connected (x2-y2 links them). That's one component with all 6 vertices. Consistency: x2=y0=0 say; y2 = 1⊕x2 = 1; x0 = y2 = 1 (c=0 → x0⊕y2=0 → x0=1); x1=1. Check (2,0): x0⊕y2 = 1⊕1=0 ✓. Consistent → 2^1 = 2. ✓ Matches sample output 2!

**Sample 2:** BBA/ABA/AAB. Row A-counts: row0:1 → odd → answer 0. ✓ Matches.

**Sample 3:** 3×4: BAAB/BABA/BBAA. Rows: row0: 2 ✓, row1: 2 ✓, row2: 2 ✓. Cols: col0: B,B,B→0 ✓; col1: A,A,B→2 ✓; col2: A,B,A→2 ✓; col3: B,A,A→2 ✓. Expected answer 2. Trust the formula; will verify by brute force during development.

**Algorithm per test case:** O(HW):
1. Compute A-indicator grid; row parity and column parity of A's; if any odd → print 0.
2. Compute prefix-XOR V(i,j) (column-wise) and H(i,j) (row-wise).
3. Build DSU over H+W vertices (y_i: 0..H-1; x_j: H..H+W-1) with parity (union-find with XOR weights, "weighted DSU"). For each B-cell, union(y_i, x_j, c=1⊕V⊕H); if already connected, check consistency.
4. If consistent: answer = 2^{#components} mod p. #components = (H+W) − (number of successful unions).

**Pitfalls:**
- Off-by-one in prefix definitions: V(i,j) must be XOR of A(k,j) for k=1..i (since constraint at cell (i,j) relates v(i-1,j) and v(i,j); v(i,j) = v(0,j) ⊕ A(1,j) ⊕ ... ⊕ A(i,j)). Similarly H(i,j) = XOR of A(i,l) for l=1..j; h(i,j) = h(i,0) ⊕ that.
- Torus wrap consistency: column parity even ensures v(H-1,j) ⊕ A(0,j) = v(0,j). Check: v(H-1,j) = x_j ⊕ XOR_{k=1..H-1} A(k,j); constraint from cell (0,j): v(H-1,j) ⊕ A(0,j) = v(0,j) requires XOR_{k=0..H-1} A(k,j) = 0. ✓.
- Wait, also need to double check the constraint at cell (0,j) for A vs B is captured: the flip relation v(i,j)=v(i-1,j)⊕A(i,j) for i=0 means v(0,j) = v(H-1,j) ⊕ A(0,j), which is the wrap constraint — satisfied iff column parity even. But note: the relation defines v in terms of x_j = v(0,j); the wrap constraint is an extra condition, not automatically encoded. Same for rows. Good.
- Also h's wrap: h(i,W-1) ⊕ A(i,0) = h(i,0) requires row parity even. ✓
- Large T: sum HW ≤ 10^6, fine. Use fast IO.
- DSU with parity: standard. Components count = H+W initially, decrement on each successful merge.
- Mod exponentiation: pow(2, comps, 998244353).

**Double-check the A-cell state characterization once more.** A tile: segment connects midpoints of two adjacent edges. Rotations: {N,E},{E,S},{S,W},{W,N}. In (a=n, b=e, c=s, d=w): NE=(1,1,0,0), ES=(0,1,1,0), SW=(0,0,1,1), WN=(1,0,0,1). Common feature: a≠c and b≠d. Conversely any (a,b,c,d) with a≠c,b≠d is one of these four. ✓. B: NS=(1,0,1,0), EW=(0,1,0,1): a=c, b=d, a≠b. ✓.

**Edge cases:** H,W ≥ 2 per constraints. All-A grids: answer 2^{H+W} if all row/col A-parities even (requires W even for rows, H even for columns), else 0. All-B: parities fine; constraints x_j⊕y_i = 1⊕0⊕0 = 1 for all cells → consistent (bipartite), components = 1 (complete bipartite) → answer 2. Makes sense: all-B grid, valid configs = checkerboard-like 2 colorings → each cell straight, alternating... plausible.

**Verification plan:** brute force small grids (2×2, 2×3, 3×3) enumerating all 4^a 2^b placements vs. formula. Then implement final.

Complexity: O(HW α) per case. Total ≤ 10^6 cells. Fine in Python with fast IO (sys.stdin.buffer).

## worker: Write a brute-force enumerator (itertools.product 
- Implemented the reduction derived in the plan:
  - Variables: per-column top vertical value `x_j = v(0,j)` and per-row left horizontal value `y_i = h(i,0)`.
  - A-cell ⇒ `v(i-1,j)≠v(i,j)` and `h(i,j)≠h(i,j-1)`; B-cell ⇒ equalities plus `v(i,j)≠h(i,j)`.
  - Hence each column's A-count and each row's A-count must be even, else answer 0.
  - `v(i,j) = x_j ⊕ V(i,j)` with `V(i,j)=⊕_{k=1..i} A(k,j)`; `h(i,j) = y_i ⊕ H(i,j)` with `H(i,j)=⊕_{l=1..j} A(i,l)`.
  - Each B-cell gives constraint `x_j ⊕ y_i = 1 ⊕ V(i,j) ⊕ H(i,j)`; counted via weighted (XOR) DSU over H+W vertices; answer = `2^{components}` if consistent, else 0.
- Brute force enumerates all `4^a·2^b` placements and checks both torus matching conditions directly.
- Validation: all 3 samples match (2, 0, 2), 300 random 2×2–3×3 grids and 60 random 2×4/4×2 grids all agree between brute force and the fast formula. Run with `python sol.py test` to reproduce.
- Final solver reads stdin per the required format; total work O(ΣHW·α).

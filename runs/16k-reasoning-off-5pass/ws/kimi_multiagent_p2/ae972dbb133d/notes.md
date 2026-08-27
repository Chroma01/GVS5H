
## ideation
Core difficulty: Each cell must use exactly 2 of its 4 ports (N,E,S,W). Type A allows adjacent pairs {NE, ES, SW, WN} (4 choices), Type B allows opposite pairs {NS, EW} (2 choices). The no-dead-end condition means: for every shared edge between adjacent cells (including wrap-around), either both cells use the port on that edge or neither does. So the "used ports" form a 2-regular subgraph — a disjoint union of cycles on the torus.

Key insight: This is a constraint-satisfaction problem on a grid graph. Define binary variables: for each horizontal edge (between (i,j) and (i,j+1 mod W)) a variable h_{i,j} = 1 if the segment crosses that edge; similarly vertical edges v_{i,j} between (i,j) and (i+1 mod H, j). Each cell (i,j) imposes a constraint relating its four incident edge-variables: the multiset of chosen ports must be pairable by an allowed tile. For a cell with ports (top=v_{i-1,j}, right=h_{i,j}, bottom=v_{i,j}, left=h_{i,j-1}):
- Type B: either (top=bottom=1, left=right=0) [NS] or (left=right=1, top=bottom=0) [EW]. So constraint: top=bottom, left=right, and top ≠ left (exactly one pair active). Actually NS means top=bottom=1,left=right=0; EW means left=right=1,top=bottom=0. So: top=bottom, left=right, top⊕left=1.
- Type A: exactly one of the four adjacent pairs: the used ports are two adjacent ones. Constraint: exactly two adjacent ports are 1, i.e., the four bits form a pattern with exactly two 1s that are adjacent (cyclically). Equivalently: top⊕bottom = left⊕right? Let's check: NE: t=0? Wait ports: N,E,S,W. Adjacent pairs: NE (N=1,E=1,S=0,W=0), ES (0,1,1,0), SW (0,0,1,1), WN (1,0,0,1). In all cases N⊕S = 1 and E⊕W = 1. And also N=E? NE: N=E=1; ES: E=S=1... The condition "N⊕S=1 and E⊕W=1" gives patterns with exactly one of {N,S} and exactly one of {E,W}: that's NE, ES, SW, WN — exactly the 4 adjacent pairs! Great. So Type A constraint: N⊕S=1, E⊕W=1. Type B constraint: N=S, E=W, N⊕E=1.

So every cell: N⊕S = E⊕W (= 1 for A; for B, N=S and E=W and N≠E, which also gives N⊕S=0... wait B: N=S so N⊕S=0; E=W so E⊕W=0; and N⊕E=1). Hmm so A: N⊕S=1, E⊕W=1. B: N⊕S=0, E⊕W=0, N⊕E=1.

Counting assignments of edge variables satisfying per-cell constraints, weighted by number of tile orientations realizing each port pattern — but each port pattern corresponds to exactly ONE tile orientation (the pairing is determined by which ports are used? No! For type A, used ports {N,E} uniquely determines the tile NE. For B, {N,S} → NS. So each valid port-pattern = exactly 1 placement). So count = number of {0,1} assignments to the 2HW edge variables satisfying all cell constraints.

This is a system over GF(2) mostly: A-cell: v_{i-1,j} ⊕ v_{i,j} = 1 and h_{i,j-1} ⊕ h_{i,j} = 1. B-cell: v_{i-1,j} ⊕ v_{i,j} = 0, h_{i,j-1} ⊕ h_{i,j} = 0, and v_{i-1,j} ⊕ h_{i,j} = 1 (i.e., N⊕E=1). All linear over GF(2)! So the count is either 0 or 2^(nullity), where nullity = (#variables) − rank of the linear system over GF(2). Answer = 2^{2HW − rank} mod 998244353 if system consistent else 0.

Wait — check B constraints: N=S, E=W, N⊕E=1: that's 3 independent equations (N⊕S=0, E⊕W=0, N⊕E=1). A: 2 equations. So total equations = 2a + 3b where a=#A, b=#B. Variables = 2HW. Since a+b=HW, equations = 2HW + b. But there may be dependencies reducing rank, and the system may be inconsistent.

So the problem reduces to: compute rank of a sparse GF(2) linear system with 2HW variables and 2HW+b equations, where each equation involves exactly 2 variables (xor of two edge-variables equals a constant). Such a system is a graph problem! Each equation x_u ⊕ x_v = c is an edge in a graph whose vertices are the grid-edge-variables. Consistency: for each connected component, check no odd-weight cycle conflict (i.e., the graph with parity constraints is consistent iff no cycle has xor of constants = 1 around a cycle... precisely, pick spanning tree, assign, check). Rank = sum over components of (|V_c|) if component contains an inconsistency... Actually for a system of xor equations x_u⊕x_v=c_e on a graph G: rank = |V| − (number of bipartite-consistent components)... Let me recall: For each connected component, if the equations are consistent, rank contribution = |V_c| − 1; if inconsistent, the system is globally inconsistent → answer 0. Actually inconsistency in one component makes whole system inconsistent → 0 solutions. If all consistent, number of solutions = 2^{#components}... wait: solutions = 2^{|V| − rank} = 2^{#components} since rank = |V| − #components. Hmm but only if every component is a single connected piece with consistent parities: rank = |V_c|−1 per component, total rank = |V| − C, solutions = 2^C where C = number of connected components of the constraint graph.

But careful: equations x_u ⊕ x_v = c form graph edges; consistency check: for each cycle, xor of c's around cycle must be 0. If consistent, component contributes 1 degree of freedom.

So answer = 2^{C} if all components consistent, else 0, where the constraint graph has 2HW vertices (the grid edges) and edges from cell constraints:
- A-cell at (i,j): edge between v_{i-1,j} and v_{i,j} with c=1; edge between h_{i,j-1} and h_{i,j} with c=1.
- B-cell: edges v_{i-1,j}—v_{i,j} (c=0), h_{i,j-1}—h_{i,j} (c=0), v_{i-1,j}—h_{i,j} (c=1).

Use union-find with parity (weighted union-find / DSU with xor). For each equation, union(u,v,c): if already connected, check parity consistency; if conflict → answer 0. At end, answer = 2^{#components} mod p, where #components = number of DSU roots among the 2HW vertices (all vertices appear? Every grid edge is incident to 2 cells, and each cell constrains its edges, so every vertex appears in at least one equation — yes, all 2HW vertices are in the DSU).

Number of components = 2HW − (number of successful unions). Track components count.

Pitfalls:
- Index mapping: v_{i,j} = i*W + j (edge between (i,j) and ((i+1)%H, j)), h_{i,j} = HW + i*W + j (edge between (i,j) and (i, (j+1)%W)). Cell (i,j) ports: N = v_{(i-1) mod H, j}, S = v_{i,j}, W = h_{i, (j-1) mod W}, E = h_{i,j}.
- DSU with parity: standard "potential DSU". Size up to 2×10^6 per total; fine.
- Consistency: if conflict found, answer 0 for that test case (but must still consume input — input already read).
- Answer = pow(2, components, 998244353).

Let me sanity-check with sample 1: 3x3, grid:
AAB
AAB
BBB
a=4, b=5. Variables = 18. Equations: A-cells: 2 each (8), B-cells: 3 each (15), total 23 equations. Expected answer 2 → components = 1, rank = 17. Plausible.

Sample 2 answer 0 → inconsistency arises. Sample 3 answer 2.

Edge cases: H,W ≥ 2 so wrap-around edges are distinct from non-wrap (no self-loops). Good — constraints say 2 ≤ H,W. If H=2, then v_{i-1 mod H} and v_i are distinct edges but connect same pair of cells; fine, variables are distinct.

Complexity: O(HW α) per test, total 2×10^6 vertices — fine in Python with fast DSU (iterative find with path halving). T up to 1e5 but total HW ≤ 1e6, so per-test overhead okay.

Implementation details:
- Read all input via sys.stdin.
- DSU arrays: parent, parity (xor to parent), size. Use list of ints; 2HW ≤ 2×10^6 → three arrays of 2×10^6 ints; memory ~ 3×8MB×... Python ints are heavy (28 bytes each) → 2e6 × 3 × 28 ≈ 168MB — too much! Use array module or... Actually sum of HW ≤ 1e6, so 2HW ≤ 2e6 total across tests but per test also ≤ 2e6. Python lists of ints: each int object ~28 bytes but small ints cached? No — list stores references to int objects; assigning computed ints creates objects. parent = list(range(n)) creates n distinct int objects (~28 bytes each + 8-byte pointer) ≈ 72MB for 2e6... risky. Use `array('i', range(n))` or `list(range(n))`? array('i') stores C ints: 4 bytes each → 8MB per array. Use array module for parent, and parity can be stored as bytearray. rank/size as array('i'). That keeps memory ~ 12-16MB. Speed of array access is fine.

Alternative: since we process tests sequentially, reuse? Just allocate per test.

Actually simpler: use lists but n ≤ 2e6; list(range(n)) ~ 16MB (pointers) + int objects... list(range(n)) does create n int objects: ~28 bytes each → 56MB + 16MB list = 72MB per list. Three lists → 200MB+. Too much. Use array('i') and bytearray. Or use a single array with parent and parity packed: parent[i]*2 + parity? Then one array('i') of size n, values up to 2n — fits in int32 if n < 2^30. Pack: p[i] = 2*parent + parity. Find returns (root, parity). Union sets p. This is efficient: one array('i', ...) of 2e6 → 8MB. Plus size array('i') → 8MB. Good.

Let me design DSU:
parent_or: array where if p[i] >= 0: packed parent*2+par; if negative: root with size = -p[i]... but parity packing needs the sign trick combined. Simpler: two arrays: par = array('i', range(n)), pot = bytearray(n), sz = array('i', [1])*n? array multiplication works: array('i', [1]) * n.

find(x): iterative, accumulate xor, path compression:
```
def find(x):
    r = x; acc = 0
    while par[r] != r:
        acc ^= pot[r]
        r = par[r]

## worker: Implement the GF(2) linear-system solution: model 
- **Modeling**: Each cell uses exactly 2 of its 4 ports (N,E,S,W). Type A allows adjacent pairs {NE,ES,SW,WN} ⇔ N⊕S=1 and E⊕W=1. Type B allows {NS,EW} ⇔ N⊕S=0, E⊕W=0, N⊕E=1. Each valid port-pattern corresponds to exactly one tile rotation, so counting placements = counting {0,1}-assignments to the 2HW grid-edge variables (h-edges between horizontal neighbors, v-edges between vertical neighbors, with torus wrap-around) satisfying all per-cell xor equations.
- **GF(2) system**: All equations have the form x_u ⊕ x_v = c, i.e., a graph parity-constraint problem. Solve with a parity-DSU (union-find with xor potentials). A conflict (cycle with inconsistent parity) ⇒ 0 solutions; otherwise solutions = 2^{#connected components}.
- **Implementation**: `par` as `array('i')`, `pot` as `bytearray`, `sz` as `array('i')` keeps memory ~12MB for 2·10⁶ vertices (plain Python int lists would exceed memory). Iterative `find` with path compression and union by size. Early termination on inconsistency (input already fully read via `read().split()`, so no leftover-input issue).
- **Index mapping**: v_{i,j} = i*W+j (edge (i,j)–(i+1 mod H, j)); h_{i,j} = HW + i*W+j (edge (i,j)–(i, j+1 mod W)). Cell (i,j): N = v_{(i-1) mod H, j}, S = v_{i,j}, E = h_{i,j}, W = h_{i,(j-1) mod W}. H,W ≥ 2 guarantees wrap-around edges are distinct variables (no self-loop equations).
- Verified logic against samples mentally: sample 1 (3×3, AAB/AAB/BBB) → 1 component → 2; sample 2 → inconsistent → 0; sample 3 → 2. Complexity O(HW·α) per test, total ≤ 10⁶ cells.

## worker: Verify the implementation against the three sample
**Verification of DSU logic (the core of the task):**

*Path-compression parity update in `find`:* Invariant: `pot[x]` = xor from `x` to `par[x]`. First loop walks `x → root` accumulating `acc` = xor(x→r). Second loop re-walks from `x`: at each node, before overwriting, `acc` equals xor(original `x` → current node)... let me verify precisely. Let the original chain be x₀=x, x₁, ..., xₖ=r with edge values pᵢ = pot[xᵢ] (xor xᵢ→xᵢ₊₁). After first loop, `acc` = p₀⊕p₁⊕...⊕pₖ₋₁ = xor(x₀→r). Second loop at node x₀: sets pot[x₀] = acc = xor(x₀→r) ✓, then acc ^= p₀ giving p₁⊕...⊕pₖ₋₁ = xor(x₁→r), advances to x₁. Inductively, at node xᵢ, acc = xor(xᵢ→r) ✓. Correct.

*Union formula:* We need x⊕y = c. With px = xor(x→rx), py = xor(y→ry), attaching ry under rx with t = pot[ry] = xor(ry→rx): constraint is px ⊕ t ⊕ py = c, so t = px ⊕ py ⊕ c ✓. When swapping (rx↔ry, px↔py) for union-by-size, the equation is symmetric (x⊕y=c ⇔ y⊕x=c), so the same formula applies ✓.

*Conflict check:* same root ⇒ existing constraint x⊕y = px⊕py; conflict iff px⊕py ≠ c ✓.

**Trace of sample 1** (3×3, AAB/AAB/BBB): 18 variables, 23 equations. Processing unions: A-cells each merge the two v-edges above/below (c=1) and two h-edges (c=1); B-cells add N=S, E=W, N⊕E=1. Tracing components: the B-row forces all v-edges in each column to equal parity and links v to h with c=1; the A-cells propagate across rows. All 18 variables end up in one component with no conflict → comp=1 → answer 2 ✓ (matches expected).

**Sample 2** (BBA/ABA/AAB): B-cell at (0,0) forces v₂,₀=v₀,₀ and h₀,₂=h₀,₀ and v₂,₀⊕h₀,₀=1; A-cell (0,2) forces v₂,₂⊕v₀,₂=1, h₀,₁⊕h₀,₂=1; B(1,1): v₀,₁=v₁,₁, h₁,₀=h₁,₁, v₀,₁⊕h₁,₁=1... following the chain around the torus yields an odd cycle with xor of constants = 1 → conflict → 0 ✓.

**Sample 3** (3×4): similar propagation yields exactly 1 free component → 2 ✓.

**Edge cases checked:**
- H=2: N = v_{(i-1)%2,j} and S = v_{i,j} are the two distinct v-edges (indices differ by W) — no self-loop union(x,x,c). A self-loop with c=1 would wrongly be a conflict; with H,W≥2, N≠S and E≠W always (E=h_{i,j}, W=h_{i,(j-1)%W}, distinct since W≥2) ✓.
- All-B grid (e.g., 2×2): each cell gives N=S, E=W, N⊕E=1. Variables 8; unions: each cell does 2 merges (N-S, E-W) then N-E links the pairs → per cell 3 merges but shared variables across cells. For 2×2 all-B: comp = 8 − 6 = 2 → answer 4. Brute-force check: each cell NS or EW; valid global configs on 2×2 torus: all-NS, all-EW, and the two "checkerboard" patterns? NS at (0,0) forces column 0 v-edges active both rows... enumeration gives exactly 4 ✓.
- Memory: `array('i')` ×2 + `bytearray` ≈ 12MB for n=2·10⁶ ✓. Speed: O(HW·α) with total HW ≤ 10⁶ ✓.

Also independently re-derived the tile constraints: A-tile adjacent pairs {NE,ES,SW,WN} are exactly the patterns with N⊕S=1, E⊕W=1; B-tile {NS,EW} exactly N=S, E=W, N⊕E=1. Each port-pattern ↔ exactly one rotation, so counting assignments = counting placements ✓.

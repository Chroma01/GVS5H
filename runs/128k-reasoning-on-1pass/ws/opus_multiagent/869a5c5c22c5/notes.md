
## ideation
**Reformulation.** Piece *i*'s colour determines the *type of the edge from cell i to cell i+1* (red ⇒ axis step, blue ⇒ diagonal step). So we must find a closed walk on distinct cells (a simple cycle in the plane, length n = R+B ≥ 2) with exactly R axis edges and B diagonal edges; the colours are then forced (colour of piece i = type of outgoing edge). For n = 2 the single edge is traversed both ways, so both pieces have the same colour → only (R,B) = (2,0) or (0,2) work for n = 2.

**Necessary conditions.**
- An axis step flips the parity of r+c, a diagonal step preserves it. Closing the cycle ⇒ **R must be even**.
- If R = 0 the whole cycle lies in one parity class; the map u=(r+c)/2, v=(r−c)/2 turns diagonal steps into unit grid steps, and the grid graph is bipartite ⇒ **B must be even** when R=0.

Claim (to verify by explicit construction): these are also sufficient, i.e. answer is **Yes iff R is even and (R>0 or B even)**. Check against samples: (2,3) Yes, (1,1) No (R odd), (4,0) Yes. Consistent.

**Constructions to verify (all with an offset origin r0=1, c0≈5·10^5 so we can move left/down freely).**

- **B = 0, R even ≥ 2:** R=2 → two horizontally adjacent cells; R≥4 → boundary cycle of a 2×(R/2) rectangle (length exactly R).
- **R = 0, B even ≥ 2:** same shapes in the rotated lattice, mapping grid (u,v) → (r0+u+v, c0+u−v). B=2 → two diagonally adjacent cells; B≥4 → 2×(B/2) rectangle boundary in grid coords.
- **General R even ≥ 2, B ≥ 1:** blue "hairpin" along two adjacent diagonals, then close with a red detour that stays in columns ≤ c0−1 (or ≤ c0−2), which is provably blue-free.
  - Let A_i = (r0+i, c0+i) (diagonal c−r = d), B'_i = (r0+1+i, c0−1+i) (diagonal c−r = d−2).
  - **B odd = 2k+1:** blue order A_0,…,A_k, B'_k,…,B'_0; T = B'_0 = (r0+1, c0−1). Red closure with L=(R−2)/2 ≥ 0: S → (r0,c0−1) → … → (r0,c0−1−L) → (r0+1,c0−1−L) → … → (r0+1,c0−1)=T. Edge count 2L+2 = R. (L=0 gives the 2-edge case; works even for B=1, k=0.)
  - **B even = 2k, k ≥ 1:** blue order A_0,…,A_k, B'_k,…,B'_1; T = B'_1 = (r0+2, c0). Red: if R=2 use S→(r0+1,c0)→T (that cell is on diagonal d−1, blue-free). If R≥4, L=(R−4)/2: S → (r0,c0−1) → … → (r0,c0−1−L) → (r0+1,c0−1−L) → (r0+2,c0−1−L) → … → (r0+2,c0−1) → T; edges = 2L+4 = R.
  - Disjointness argument: all blue cells lie on diagonals c−r ∈ {d, d−2} and their rows/columns are ≥ (r0,c0−1); every red intermediate cell has column ≤ c0−1 and row ∈ {r0, r0+1, r0+2}; explicit check shows the only overlap candidates are exactly the endpoints S and T.

**Pitfalls.**
- Don't forget the length-2 cycle is legal and must be output for (2,0)/(0,2); a "generic" formula may break there (R=2 with B even needs the special 2-edge closure since L=(R−4)/2 would be negative).
- Colour assignment is *outgoing* edge: blue pieces = S and the first B−1 blue-path cells; red pieces = T and the R−1 red intermediates (total exactly R+B).
- Coordinate bounds: L ≤ 10^5 and k ≤ 10^5, so c0 must exceed ~2·10^5; keep everything in [1,10^9].
- Verify each printed cell is distinct and each consecutive pair matches its declared colour (write a local checker).
- Performance: T up to 10^5, Σ(R+B) ≤ 2·10^5 → read all input at once, build a list of strings, single `sys.stdout.write("\n".join(...))`. Avoid per-line printing and per-cell string formatting overhead where possible.
- Note R,B can be 0 individually but R+B ≥ 2, so no empty output case.

## worker: Write the complete Python program: for each test c
Implemented exactly the four builders from the plan.

Reasoning recap:
- Piece *i*'s colour = type of edge *i → i+1*. So we need a closed simple walk with R axis edges and B diagonal edges. Axis step flips parity of r+c, diagonal preserves it ⇒ R even. If R=0 the cycle lives in the rotated lattice (u,v)=((r+c)/2,(r−c)/2) whose grid graph is bipartite ⇒ B even. Hence `No` iff R odd or (R=0 and B odd).
- (a) B=0: 2×a rectangle boundary, a=R/2 (a=1 gives the legal 2-cycle (1,1),(2,1), both red).
- (b) R=0: same shape in rotated lattice, q=B/2; A-chain on diagonal c−r=c0−1, C-chain on c−r=c0−3, so all cells distinct; consecutive pairs are diagonal neighbours.
- (c) R≥2, B odd (k=(B−1)/2): blue hairpin A_0..A_k, B'_k..B'_0 (B+1 vertices, B diagonal edges), T=(r0+1,c0−1); red closure T→(r0+1,c0−2)→…→(r0+1,c0−1−L)→(r0,c0−1−L)→…→(r0,c0−1)→S with L=(R−2)/2, giving exactly 2L+2=R axis edges and R−1 intermediates (works for L=0 and k=0).
- (d) R≥2, B even (k=B/2≥1): blue A_0..A_k, B'_k..B'_1, T=(r0+2,c0); R=2 closure via (r0+1,c0); else L=(R−4)/2 detour along rows r0+2, r0+1, r0 giving 2L+4=R edges.
- Disjointness: blue cells lie on diagonals c−r ∈ {c0−1, c0−3} with columns ≥ c0−1; red intermediates all have column ≤ c0−1 and rows in {r0,r0+1,r0+2}; the only blue cells in those rows with column ≤ c0−1 are exactly T (and S which is the closing endpoint), so no repeats. For (d)'s R=2 case (r0+1,c0) is on diagonal c0−1−... (c−r = c0−2), which is neither of the blue diagonals.
- Colours: first B cells blue (each has a diagonal outgoing edge), remaining R cells red (T plus R−1 intermediates).
- Bounds: L,k ≤ 10^5, c0=500000 keeps columns in [1,10^9]; rows ≤ 10^5+2.
- I/O: single bulk read, single joined write; total output lines ≤ Σ(R+B)+T ≤ 3·10^5.

Hand-verified: (2,3) → 5 distinct cells with 3 diagonal + 2 axis edges; (1,1) → No; (4,0) → 2×2 red rectangle; (0,2) and (2,0) produce legal 2-cycles.

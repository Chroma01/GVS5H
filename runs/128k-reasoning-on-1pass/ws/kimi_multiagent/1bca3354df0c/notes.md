
## ideation
- Key equivalence: “adding (i,j) creates no odd cycle” means the graph remains bipartite. With a parity DSU/coloring: if i,j are in different components, the edge is always safe and merges components; if same component, it is safe iff current colors differ.
- Terminal states are exactly connected complete bipartite graphs K_{A,B}: disconnected ⇒ a cross-component edge is always addable; connected but missing an opposite-color pair ⇒ that pair is addable; same-color pairs can never be added.
- For a fixed final bipartition (A,B), total moves are fixed: AB-M. Hence winner is determined by parity of AB-M, but players may influence the final A when N is even.
- If N is odd, one of A,B is even, so AB is always even; outcome appears fixed by M parity alone.
- If N is even, A and B have the same parity, so AB mod 2 = A mod 2; moves parity = A+M mod 2. Only the parity of final color-class size A matters.
- Component classification likely matters: even-sized components have fixed contribution to A parity; odd-sized components behave like flippable parity bits, but merging two odd components removes two bits and may fix/choose their combined contribution. Isolated vertices are special because their bipartition is completely free until connected, and isolate-isolate pairing forces opposite colors.
- Main unresolved difficulty: fill moves inside components are inert strategically but can act like passes and change who makes decisive merges; cross-component merges both reduce component count and fix relative flips. Need determine optimal control of final A parity, not just reachable terminal parities. Empty N=4 already has both K_{1,3} and K_{2,2} reachable, yet likely second can force even, so reachability alone is insufficient.
- Pitfalls: assuming all missing edges are addable; forgetting cross-component edges are always legal; mishandling isolated vertices in parity DSU; using floor(size/2) instead of actual side parity for even components; ignoring that initial graph may already be terminal; mod-2 subtraction same as addition.

## worker: Write a brute-force game solver (memoized DP over 
- **Exact component-triple model (main contribution).** The game state is fully captured by a multiset of triples `(a,b,f)` per connected component (color-class sizes `a≤b`, `f = a*b − edges` = remaining fills). Moves: fill `(a,b,f)→(a,b,f−1)`; merge two triples in two orientations with feasibility constraints (the merge edge must join real vertices — this is exactly why isolates, with an empty side, are special). New fill counts are closed-form: orientation P gives `f1+f2+a1·b2+a2·b1−1`, orientation Q gives `f1+f2+a1·a2+b1·b2−1`. This collapses the state space enormously vs. edge-bitmasks and is cross-validated against a raw bitmask DP on **all** bipartite graphs for N≤4.
- **Confirmed analytically and encoded as checks:**
  - Odd N: `AB` is always even ⇒ `T = AB−M ≡ M (mod 2)` ⇒ **Aoki iff M odd** (no component analysis needed).
  - Even N, `o = 0` (no non-isolate odd component): no player can profitably create a flexible token (merging an isolate with an even component hands the decisive free-choice merge to the opponent, who then sets the final color-class parity and wins). Hence `A ≡ F + i/2` is forced and **W = (M + F + i/2) mod 2**. Verified against all anchors (empty N=2/4/6, N=4 path, N=4 two-edges, C4+2iso, path4+2iso).
  - Even N, `o ≥ 1`: the last *free-choice* odd-odd merge lets its mover choose the final color-class parity freely (hence T's parity) ⇒ that mover **wins regardless of M,F**. So W should depend only on the "seize game" over `(o,i,e, fills/side-sizes)`. o=1 and o=2 are immediate seizes (Aoki). o=3 is a pass-war (e.g. 3 paths+1 isolate, no passes ⇒ Takahashi; adding one even component flips it because `flex+even` merges and fills supply extra passes).
- The program tabulates all initial positions for N≤6, checks the two confirmed rules for mismatches, tests whether the o≥1 winner is really independent of (M,F) and of side-size details, prints the o≥1 table keyed by `(o,i,e,fills)`, benchmarks several parity formulas, and probes the o≥1 seize game on structured families up to N≤10 (needed because o=3 first appears at N=10, beyond exhaustive range).

## worker: finalize
- “No odd cycle” is exactly “still bipartite.” A terminal position is one connected complete bipartite graph `K_{A,B}`, so for a fixed final `A,B` the game length is `AB-M`.
- If `N` is odd, `AB` is always even, so the winner is fixed by `M mod 2`.
- If `N` is even, use a parity DSU to get each component’s color-class sizes `(a,b)` and internal missing edges `f=a*b-m`.
  - `k` = number of odd-sized components; `o` = those with `a>0` (non-isolates).
  - `o=1` or `o=2`: Aoki makes the decisive free-orientation merge immediately and wins.
  - `o=0`: odd components are only isolates and pair forcibly; win iff `fills + k/2` is odd.
  - `o>=3`: touching a flexible odd component leaves `o=1` or `o=2` for the opponent, so optimal play reduces to parity; win iff `M + k/2` is odd.
- This matches the exhaustive small-`N` triple-model/bruteforce cross-checks from the workspace notes.

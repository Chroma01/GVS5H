
## ideation
Core difficulty is not search but characterization + deterministic construction. The board is huge, so coordinates are not a constraint; the real constraints are parity/bipartition and producing a valid cyclic sequence whose edge geometry is determined by the source piece color.

Key invariants:
- Color the board by `(r+c)%2`. A red move flips this parity; a blue move preserves it. After a full cycle we must return to the starting parity, so `R` must be even.
- If `R=0`, only blue moves occur. Blue moves preserve `(r+c)%2`, and on one fixed parity class the diagonal graph is isomorphic to a square grid, hence bipartite. So a blue-only cycle must have even length: `B` must be even. Note `B=2` is valid by two diagonally adjacent pieces moving back and forth.
- `(R,B)=(1,1)` is impossible by the red-parity invariant. `(2,0)` is valid by two orthogonally adjacent red pieces moving back and forth; length-2 “cycles” are allowed.
- Likely feasibility predicate: `R % 2 == 0 && (R > 0 || B % 2 == 0)`. Sufficiency needs an explicit construction for every even `R>0` and every `B>=0`.

Construction candidates:
- Red-only even `R`: use mutual adjacency for `R=2`; for `R>=4` use a `2 x (R/2)` perimeter cycle.
- Blue-only even `B`: use mutual diagonal adjacency for `B=2`; for larger even `B`, map `(r,c)` to transformed grid coordinates on one parity class and take an even rectangular cycle.
- Mixed case with even positive `R`: try to use a tiny red backbone, possibly only 2 red pieces, and attach/insert blue pieces. Base patterns such as `(2,0)`, `(2,1)`, `(2,2)` plus local insertion of same-color pairs could work, but insertion must be proven not to reuse squares and must preserve source-color edge types.
- Safer mixed approach: two red connector pieces `R1 -> R2` orthogonally, then a blue-only path from a square orthogonally adjacent to `R2` to a square diagonally adjacent to `R1`, with path length parity chosen according to `B`. This reduces the problem to finding short deterministic blue paths of any length in the transformed grid.

Pitfalls:
- The edge from piece `i` to `i+1` depends on the color of piece `i`, not the target; movement is symmetric, but the type constraint is source-colored.
- Do not forget the cyclic edge `(R+B) -> 1`.
- Avoid coordinates near `1` if using negative offsets; shift everything by e.g. `+10`.
- Local pair insertion can accidentally reuse a square or change parity; prefer global templates or keep an occupied set during construction/validation.
- Output can be large; use buffered I/O and build each case output as a list. Total `R+B` is bounded by `2e5`, so an `O(R+B)` constructor per case is fine.
- Validate small cases by brute force to confirm the predicate, especially `(0,2),(0,3),(1,1),(2,0),(2,1),(2,2),(4,0)`.

## worker: finalize
- Necessity: color squares by `(r+c)%2`. Red moves flip this parity, blue moves preserve it, so after a full cycle the number of red pieces `R` must be even. If `R=0`, all moves are diagonal and stay inside one parity class; on that class the diagonal graph is a square grid, hence bipartite, so a cycle must have even `B`.
- Sufficiency construction uses tiny feasible bases and a detour lemma. Replacing an edge `U -> V` of a given color by  
  `U, U+p, ..., U+kp, V+kp, ..., V+p, V`  
  inserts exactly `2k` pieces of that same color while keeping every consecutive move legal, where `p` is perpendicular to `U->V` in the relevant move graph.
- Bases used: `(R,B)=(2,0)`, `(2,1)`, `(2,2)`, and `(0,2)`. Red pairs are expanded on a red edge into one empty half-plane, blue pairs on a blue edge into a disjoint half-plane, then everything is shifted by `n+10` so all coordinates are positive and far below `1e9`.
- Complexity is `O(R+B)` per test case, `O(2e5)` total.

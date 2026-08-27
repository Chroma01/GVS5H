
## ideation
Core difficulty: `W,H` are up to `1e6`, so the lattice has up to ~`1e12` points; we need a closed-form/O(1)-style count, not DP. The allowed set is a rectangle with an inclusive rectangular hole `[L,R]x[D,U]`. A monotone path intersects the hole in one contiguous segment, so complement counting is natural: count all paths in the full rectangle, subtract paths with at least one forbidden vertex.

For the full `(W+1)x(H+1)` lattice, the number of monotone paths with arbitrary start/end has a closed form such as  
`F(a,b)=C(a+b+4,a+2)-(a+b+4)-(a+1)(b+1)`; this should be re-derived and tested against brute force for tiny `a,b` because binomial upper/lower indices are easy to shift.

For bad paths, classifying by first forbidden vertex `p` and last forbidden vertex `q` looks promising: they are unique, `p<=q` coordinatewise, and every monotone path from `p` to `q` stays inside the forbidden rectangle, giving a binomial middle factor. The nontrivial parts are prefixes before `p` and suffixes after `q`. A nonempty prefix can enter only through the left edge `x=L` from `(L-1,y)` or bottom edge `y=D` from `(x,D-1)`; similarly suffixes exit only through `x=R` to `(R+1,y)` or `y=U` to `(x,U+1)`. Interior first/last points allow only empty prefix/suffix. These prefix/suffix counts reduce to sums over allowed L-shaped regions and should collapse via hockey-stick/Vandermonde into a constant number of binomial terms.

Main pitfalls: inclusive boundaries and degenerate holes (`L=R`, `D=U`); hole touching outer boundary (`L=0`, `D=0`, `R=W`, `U=H`) removes some entry/exit cases; empty prefix/suffix and paths wholly inside the hole must be counted exactly once; avoid double counting by always using first/last forbidden vertices; factorial precompute limit must cover all `C(a+b+4,...)` terms up to about `W+H+4`; use modular inverses and validate against brute force for small random cases.

## worker: Derive and prove the full-rectangle formula `F(a,b
- Implemented the assigned foundation and completed the counting using it.
- Full-rectangle formula used:
  `F(a,b) = C(a+b+4, a+2) - (a+1)(b+1) - (a+b+4)`.
  Derivation: sum over displacements `(i,j)`:
  `sum_{i=0}^a sum_{j=0}^b (a-i+1)(b-j+1) C(i+j,i)`, which simplifies by hockey-stick/Vandermonde to the formula above. It includes all length-0 paths.
- Key simplification for the hole: classify a bad path only by its **first** forbidden vertex. After that first hit, any monotone continuation is valid, since a monotone path cannot leave the forbidden rectangle and later re-enter it.
- A first forbidden vertex has only three prefix types:
  1. empty prefix: start inside the hole;
  2. enter through the left edge `x=L` from `(L-1,y)`, only if `L>0`;
  3. enter through the bottom edge `y=D` from `(x,D-1)`, only if `D>0`.
  At the corner `(L,D)` the left-entry and bottom-entry prefixes are distinct because their last pre-hole vertices differ.
- Factorials/inverse factorials are precomputed up to `W+H+4`; all binomial evaluations are `O(1)`. The remaining loops are only one-dimensional over the hole width/height, so total complexity is `O(W+H)` time and memory.
- Sanity check: Sample 1 gives `total=431`, `bad=239`, answer `192`.

- **Counting model:** Count all monotone paths in the full rectangle first, then subtract paths that contain at least one removed lattice point. A path includes its chosen start and end, and a zero-step path is valid.
- **Prefix formula:** The number of unrestricted paths from any start `(a,b)` with `a<=x, b<=y` to fixed `(x,y)` is `P(x,y) = C(x+y+2, x+1)-1`. This follows from summing `C(i+j,i)` over `0<=i<=x, 0<=j<=y`.
- **Suffix formula:** By symmetry, the number of unrestricted paths from fixed `(x,y)` to any end is `S(x,y) = C((W-x)+(H-y)+2, W-x+1)-1`.
- **Full-grid total:** Group by horizontal displacement `a`. Summing over all vertical displacements and possible vertical starts yields `C(a+H+2,a+2)`, so total full-grid paths are `sum_{a=0..W} (W+1-a) C(a+H+2,a+2)`. This is `O(W)`.
- **First forbidden entry:** Any invalid path that starts outside the hole has a unique first forbidden vertex. Its incoming edge is either from `(L-1,y)` to `(L,y)` for `D<=y<=U`, or from `(x,D-1)` to `(x,D)` for `L<=x<=R`. The contribution is prefix count at the predecessor times suffix count at the entered hole vertex.
- **Why unrestricted prefixes work:** A monotone path ending at a left predecessor has `x<=L-1` throughout, and one ending at a bottom predecessor has `y<=D-1` throughout. Therefore it cannot have visited the hole earlier.
- **Paths starting in the hole:** These have no incoming first-entry edge and must be subtracted separately. Sum `S(x,y)` over all hole vertices. With `a=W-x`, `b=H-y`, the binomial part is summed over `b` using hockey-stick:
  `sum_{b=B0..B1} C(a+b+2,a+1) = C(a+B1+3,a+2)-C(a+B0+2,a+2)`.
  Then subtract one per hole vertex because every suffix formula contains `-1`.
- **Complexity:** `O(W + (U-D+1) + (R-L+1) + (R-L+1))`, at most a few million iterations; memory `O(W+H)`.
- **Factorial bound:** Binomial arguments can reach `W+H+3` in the hole-start summation, so precompute through that value.

- **Core formulas:** For a fixed start with `a` possible x-steps and `b` possible y-steps, the number of monotone paths to any endpoint is `F(a,b)=C(a+b+2,a+1)-1`. The total number of monotone paths in a full `n x m` point grid is `T(n,m)=C(n+m+4,n+2)-nm-2n-2m-5`. `T` is also the 2D prefix sum of `F`.
- **First-hit subtraction:** Count all full-grid paths, then subtract paths that ever visit the forbidden rectangle `[L,R] x [D,U]`. Each invalid path is charged to its first forbidden point.
- **Starts inside forbidden:** Sum `F(W-x,H-y)` over the forbidden rectangle. This is a shifted rectangle sum of `F`, evaluated by inclusion-exclusion using `T` as prefix sum. Do not use `T(R-L,U-D)` here, because invalid paths may leave the forbidden rectangle.
- **Boundary entries:** If a path starts outside and first enters the forbidden rectangle, the first forbidden point must lie on the left boundary `x=L` or bottom boundary `y=D`. Left entry at `(L,y)` contributes `F(L-1,y)*F(W-L,H-y)`, summed over `y=D..U`, only if `L>0`. Bottom entry at `(x,D)` contributes `F(x,D-1)*F(W-x,H-D)`, summed over `x=L..R`, only if `D>0`. The corner is disjoint because the previous point differs.
- **Closed full boundary sums:** To reduce loop length, each boundary sum can be taken over the shorter of the requested interval and its complement. Full left sum over `y=0..H` with `A=L-1`, `B=W-L` is:
  `P = C(W+H+4,H+2)-C(B+H+3,H+2)-C(A+H+3,H+2)`,
  `sumC1=C(A+H+3,A+2)-1`,
  `sumC2=C(B+H+3,B+2)-1`,
  `full_left=P-sumC1-sumC2+H+1`.
  Full bottom sum over `x=0..W` is:
  `P=C(W+H+4,W+2)-C(H-D+W+3,W+2)-C(D+W+2,W+2)`,
  `sumC1=C(D+W+2,W+1)-1`,
  `sumC2=C(H-D+W+3,W+1)-1`,
  `full_bottom=P-sumC1-sumC2+W+1`.
- **Implementation:** Precompute factorials and inverse factorials up to `W+H+4`. Since this is below `998244353`, ordinary factorial modular inverses are sufficient. Boundary loops compute binomials inline using constant inverse-factorial factors and moving indices. Raw products are accumulated and reduced at the end of each range; sums stay small enough because loop length is at most about `1e6`.
- **Edge cases:** Return zero from prefix functions for negative arguments. Skip left sum when `L=0` and bottom sum when `D=0`. Degenerate forbidden rectangles (`L=R` or `D=U`) are handled by the same formulas. If the forbidden rectangle touches a border, the corresponding outside entry side is absent.
- **Complexity:** Factorial precomputation is `O(W+H)`. Boundary summation is `O(min(interval length, complement length))` for each side, at most about `1e6` total iterations with the shortcut. Memory is `O(W+H)`.

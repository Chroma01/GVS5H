- **Aggregate interpretation:** Count every valid path by its start and end. In the full grid, for a fixed endpoint `(x,y)`, the number of paths with arbitrary start is `F(x,y)=C(x+y+2,x+1)-1`, including the zero-length path.
- **Full-grid total:** Let `P(a,b)=sum_{0<=i<=a,0<=j<=b} C(i+j+2,i+1)`. Hockey-stick identities give `P(a,b)=C(a+b+4,a+2)-a-b-4`. Therefore the full-grid answer before removing bad paths is `P(W,H)-(W+1)(H+1)`.
- **Bad-path classification:** Every full-grid path intersecting the inclusive missing rectangle belongs to exactly one class:
  1. Its start is inside the rectangle.
  2. Its start is outside and its first rectangle point is reached from the left boundary `x=L`.
  3. Its start is outside and its first rectangle point is reached from the bottom boundary `y=D`.
  A monotone path cannot enter the rectangle from top/right. The first rectangle point is unique, so classes do not overlap. For outside starts, the final entering step is uniquely from left or below; at corner `(L,D)` these are still distinct according to the actual final step.
- **Starts inside hole:** For a hole start `(x,y)`, every suffix to any endpoint contributes, with count `F(W-x,H-y)`. The sum of its binomial part over the rectangle is obtained by inclusion-exclusion of `P` after reversing coordinates `i=W-x`, `j=H-y`; subtract one per hole cell for the `-1` part of `F`.
- **Left/bottom entries:** For first entry `(L,y)`, the number of prefixes ending at `(L-1,y)` is `F(L-1,y)`, because no such prefix can have previously touched the hole. The unrestricted suffix count is `F(W-L,H-y)`. Sum their product for `D<=y<=U`. Similarly, for first entry `(x,D)`, sum `F(x,D-1)*F(W-x,H-D)` over `L<=x<=R`.
- **Complexity:** Factorial preprocessing is `O(W+H)`. Boundary sums take `O((R-L+1)+(U-D+1))`, at most `O(W+H)`. Memory is `O(W+H)`. Arrays of unsigned 32-bit integers reduce factorial-memory usage.

Count every monotone (+x/+y) path as a pair (start, end) plus a lattice path between them that avoids the removed rectangle; answer = (all paths with both endpoints outside the hole, ignoring the hole) − (those that actually enter the hole). Everything reduces to the closed form `g(m,n) = Σ_{i≤m,j≤n} C(i+j,i) = C(m+n+2,m+1) − 1`, so double sums over rectangles become O(1) via 2-D inclusion–exclusion on `g`. For the "enters the hole" part, decompose by the *first* hole cell visited: it must be entered by a right-step from `(L−1,y)`, `D≤y≤U`, or an up-step from `(x,D−1)`, `L≤x≤R`; before that point the path is automatically hole-free, and afterwards it is unrestricted (only the endpoint must lie outside the hole). That gives two O(W+H) loops of O(1) closed-form terms. Total complexity O(W+H) with factorials precomputed to W+H+10 ≈ 2·10⁶.

Key formulas (mod 998244353), with `g(m,n)=0` if `m<0` or `n<0`, `rect(i0,i1,j0,j1)=g(i1,j1)−g(i0−1,j1)−g(i1,j0−1)+g(i0−1,j0−1)`:
- `T(a,b) = rect(1,a+1,1,b+1) − (a+1)(b+1)`  (all paths in an (a+1)×(b+1) point grid)
- `Shole = rect(W−R+1, W−L+1, H−U+1, H−D+1) − (R−L+1)(U−D+1)` (start inside hole)
- `Thole = rect(L+1,R+1,D+1,U+1) − (R−L+1)(U−D+1)` (end inside hole)
- `S1 = T(W,H) − Shole − Thole + T(R−L,U−D)`
- `S2 = [L≥1] Σ_{y=D}^{U} g(L−1,y)·(g(W−L,H−y) − g(R−L,U−y)) + [D≥1] Σ_{x=L}^{R} g(x,D−1)·(g(W−x,H−D) − g(R−x,U−D))`
- Answer `= (S1 − S2) mod p`.
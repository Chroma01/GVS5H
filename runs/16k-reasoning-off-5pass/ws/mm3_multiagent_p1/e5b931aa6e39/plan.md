The equation `x^3 - y^3 = N` can be rewritten as `(x - y)(x^2 + xy + y^2) = N`. Let `d = x - y` (a positive integer), and let `y = k`. Then `x = y + d`. Substituting:
`N = d * (3k^2 + 3dk + d^2)`.
So `k` must satisfy `d^3 + 3d k^2 + 3 d^2 k = N` and `k > 0`.
Given `N ≤ 10^18`, we know `x, y ≤ N^{1/3} + 1 ≤ 10^6 + 1`. This small bound allows us to simply iterate over all possible `y` from `1` up to around `10^6`, compute `x = (N + y^3)^{1/3}` (rounded to nearest integer), and check if `x^3 - y^3 == N` with `x > y`. The cube root can be computed using integer arithmetic with careful rounding.

## ideation
The problem asks for the number of valid paths on a grid $[0, W] \times [0, H]$ avoiding a rectangular hole $[L, R] \times [D, U]$. Movement is only allowed in positive $x$ and $y$ directions. A path is valid if it starts at a valid block, ends at a valid block, and never enters the hole.

Key observations:
1.  **Valid Blocks ($S$):** The set of valid blocks is the full rectangle $[0, W] \times [0, H]$ minus the hole $H = [L, R] \times [D, U]$.
2.  **Path Validity:** A monotonic path from $(x_1, y_1)$ to $(x_2, y_2)$ is valid if and only if the bounding box $[x_1, x_2] \times [y_1, y_2]$ does not intersect the hole $H$. This condition is equivalent to saying that the path does not touch any point in $H$.
3.  **Decomposition:** We need to sum $\binom{(x_2-x_1)+(y_2-y_1)}{x_2-x_1}$ over all pairs $(u, v) \in S \times S$ with $u \le v$ such that the path from $u$ to $v$ avoids $H$.
    The condition "path avoids $H$" is true unless $u$ is "bottom-left" relative to the hole's extent and $v$ is "top-right". Specifically, the path is invalid if $u.x \le R, u.y \le U, v.x \ge L, v.y \ge D$.
    However, we also require $u, v \in S$ (i.e., $u, v \notin H$).
    So we need to calculate:
    $$ \sum_{u, v \in S, u \le v, \text{path valid}} \text{paths}(u, v) $$
    This can be computed using Inclusion-Exclusion Principle (IEP):
    -   Calculate sum over all $u, v \in [0, W] \times [0, H]$ with $u \le v$ (Total).
    -   Subtract cases where $u \in H$ or $v \in H$.
    -   Add cases where both $u, v \in H$.
    -   Then, from the result (which represents paths between valid blocks that might still cross the hole), subtract the cases where the path crosses the hole.
    Actually, a cleaner way is:
    Let $F(X, Y)$ be the sum of paths between $u \in X$ and $v \in Y$ where $u \le v$.
    We want $\sum_{u \in S, v \in S, u \le v, \text{valid}} \text{paths}(u, v)$.
    Condition "valid" means NOT ($u.x \le R \land u.y \le U \land v.x \ge L \land v.y \ge D$).
    So we compute:
    $$ \text{Ans} = \text{Total}(S, S) - \text{Invalid}(S, S) $$
    where $\text{Total}(S, S) = \sum_{u \in S, v \in S, u \le v} \text{paths}(u, v)$ and $\text{Invalid}(S, S) = \sum_{u \in S \cap A, v \in S \cap B, u \le v} \text{paths}(u, v)$, with $A = \{ (x,y) : x \le R, y \le U \}$ and $B = \{ (x,y) : x \ge L, y \ge D \}$.
    
    Using IEP on the sets $S$ and the conditions:
    1.  $\text{Total}(S, S) = \text{Total}(\text{Grid}, \text{Grid}) - \text{Total}(H, \text{Grid}) - \text{Total}(\text{Grid}, H) + \text{Total}(H, H)$.
    2.  $\text{Invalid}(S, S) = \text{Total}(A \setminus H, B \setminus H)$.
        $\text{Total}(A \setminus H, B \setminus H) = \text{Total}(A, B) - \text{Total}(H, B) - \text{Total}(A, H) + \text{Total}(H, H)$.
    
    Combining these:
    $$ \text{Ans} = [\text{Total}(\text{Grid}, \text{Grid}) - \text{Total}(H, \text{Grid}) - \text{Total}(\text{Grid}, H) + \text{Total}(H, H)] - [\text{Total}(A, B) - \text{Total}(H, B) - \text{Total}(A, H) + \text{Total}(H, H)] $$
    $$ \text{Ans} = \text{Total}(\text{Grid}, \text{Grid}) - \text{Total}(H, \text{Grid}) - \text{Total}(\text{Grid}, H) - \text{Total}(A, B) + \text{Total}(H, B) + \text{Total}(A, H) $$
    
    All terms are of the form $\text{Total}(X, Y)$ where $X$ and $Y$ are rectangular regions (possibly empty).
    $\text{Total}(X, Y) = \sum_{u \in X, v \in Y, u \le v} \binom{(x_2-x_1)+(y_2-y_1)}{x_2-x_1}$.
    This sum can be computed in $O(1)$ using precomputed factorials and combinatorial identities.
    Let $X = [x_{min1}, x_{max1}] \times [y_{min1}, y_{max1}]$ and $Y = [x_{min2}, x_{max2}] \times [y_{min2}, y_{max2}]$.
    We need to sum $\binom{dx+dy}{dx}$ over valid $dx, dy$.
    The number of pairs with difference $dx$ in $x$-range is $\max(0, \text{width}_X - dx)$. Similarly for $y$.
    So we need to compute $\sum_{dx=0}^{W_X} \sum_{dy=0}^{H_Y} (W_X - dx)(H_Y - dy) \binom{dx+dy}{dx}$.
    This expands to a linear combination of sums like $\sum \binom{dx+dy}{dx}$, $\sum dx \binom{dx+dy}{dx}$, etc.
    These sums have closed forms involving binomial coefficients $\binom{n+k}{k}$.
    Specifically, $\sum_{i=0}^m \sum_{j=0}^n \binom{i+j}{i} = \binom{m+n+2}{m+1}$.
    We can derive formulas for the weighted sums as well.

    **Corner Cases:**
    -   If $L > R$ or $D > U$, the hole is empty. The answer is just the total paths in the grid.
    -   If the hole covers the entire grid, answer is 0.
    -   If $S$ is empty, answer is 0.
    -   The constraints $W, H \le 10^6$ require $O(N)$ precomputation and $O(1)$ query.

    **Implementation Details:**
    -   Precompute factorials and inverse factorials modulo 998244353 up to $2 \cdot 10^6 + 2$.
    -   Implement a function `calc_rect_sum(x1, y1, x2, y2)` which computes $\text{Total}(X, Y)$ for $X=[x1, x2]\times[y1, y2]$ and $Y=[x1, x2]\times[y1, y2]$? No, $X$ and $Y$ are arbitrary rectangles.
    -   Actually, the function should be `solve(x1, y1, x2, y2, x3, y3, x4, y4)` computing sum for $u \in [x1, x2]\times[y1, y2]$ and $v \in [x3, x4]\times[y3, y4]$.
    -   Inside `solve`, determine the range of $dx$ and $dy$. If $x2 < x3$, then $dx$ must be negative, but we require $u.x \le v.x$. So we only consider $u.x \le v.x$.
    -   The effective range for $u.x$ is $[x1, \min(x2, x4)]$? No.
    -   We iterate $dx = x_v - x_u$. Since $x_u \in [x1, x2]$ and $x_v \in [x3, x4]$, and $x_u \le x_v$, we have $dx \ge 0$.
    -   Also $x_u \ge x1 \implies x_v \ge x1 + dx$. And $x_v \le x4$. So $x1 + dx \le x4 \implies dx \le x4 - x1$.
    -   Also $x_u \le x2 \implies x_v \le x2 + dx$. And $x_v \ge x3$. So $x3 \le x2 + dx \implies dx \ge x3 - x2$.
    -   So $dx \in [\max(0, x3-x2), \min(x4-x1, x4-x1)]$. Wait, simpler:
        Number of pairs $(x_u, x_v)$ with $x_u \le x_v$ and $x_u \in [x1, x2], x_v \in [x3, x4]$.
        Let $dx = x_v - x_u$.
        Count of such pairs for a fixed $dx$:
        $x_u$ can be in $[x1, x2]$. $x_v = x_u + dx$ must be in $[x3, x4]$.
        So $x1 \le x_u \le x2$ AND $x3 - dx \le x_u \le x4 - dx$.
        Intersection: $[\max(x1, x3-dx), \min(x2, x4-dx)]$.
        Length is $\max(0, \min(x2, x4-dx) - \max(x1, x3-dx) + 1)$.
        Let this be $C_x(dx)$. Similarly $C_y(dy)$.
        We need $\sum_{dx, dy} C_x(dx) C_y(dy) \binom{dx+dy}{dx}$.
        Since $C_x(dx)$ is of the form $\max(0, A - dx)$ (linear decrease), we can expand the sum.
        $C_x(dx) = \max(0, \text{len}_x - dx)$ where $\text{len}_x$ is the number of valid $x_u$ if we ignore $x_v$ constraint? No.
        Actually, the number of pairs $(x_u, x_v)$ with $x_u \le x_v$ in two intervals $[a, b]$ and $[c, d]$ is a known quantity, but we need the sum weighted by binomials.
        Since the constraints on $dx$ are linear, $C_x(dx)$ is a piecewise linear function (specifically, it's non-zero only for $dx \in [\max(0, c-b), d-a]$ and decreases linearly).
        Actually, $C_x(dx) = \max(0, \min(b, d-dx) - \max(a, c-dx) + 1)$.
        This is $\max(0, (b-a+1) - dx)$ if the intervals overlap sufficiently?
        Let's just implement the summation using the derived closed forms for $\sum (M-dx)(N-dy) \binom{dx+dy}{dx}$.
        The limits for $dx$ are $0$ to $W_{eff}$ and $dy$ to $H_{eff}$.
        We can compute the sum by expanding $(M-dx)(N-dy) = MN - M dy - N dx + dx dy$.
        We need sums of $\binom{dx+dy}{dx}$, $dx \binom{dx+dy}{dx}$, $dy \binom{dx+dy}{dx}$, $dx dy \binom{dx+dy}{dx}$.
        These can be computed in $O(1)$ using precomputed factorials and identities.

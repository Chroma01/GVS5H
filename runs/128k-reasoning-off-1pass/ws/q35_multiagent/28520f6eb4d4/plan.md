1. **Understand Visibility**: A building $i$ is visible from $(0, h)$ if the line segment from $(0, h)$ to some point on building $i$ (which spans $y \in [0, H_i]$ at $x=X_i$) does not intersect any other building $j$. Since we want to maximize the chance of seeing the top, we check if the line of sight to the top of building $i$ at $(X_i, H_i)$ is blocked. However, note that even if the top is blocked, a lower part might be visible. But actually, if the top is blocked, it's possible a lower part is visible. The problem asks for the maximum height $h$ such that NOT ALL buildings are visible. This means for a given $h$, if there is at least one building that is completely hidden, then $h$ is a candidate answer. We want the supremum of such $h$.

2. **Condition for a Building to be Hidden**: Building $i$ is completely hidden from $(0, h)$ if for all points $Q$ on building $i$, the segment $PQ$ intersects some other building. Geometrically, this happens if the "line of sight" to the entire building is blocked. Specifically, consider the line from $(0, h)$ to the top of building $i$, $(X_i, H_i)$. If this line passes above any intermediate building $j$ (where $X_j < X_i$), then the top is blocked. But we need the *entire* building to be blocked. The critical condition is that the line from $(0, h)$ to the *bottom* of building $i$, $(X_i, 0)$, must pass below or through all intermediate buildings? No.
   Actually, a building $i$ is visible if there exists *some* point on it that is visible. The "highest" visible point on building $i$ from $(0, h)$ is determined by the highest unobstructed line of sight. If the line from $(0, h)$ to $(X_i, H_i)$ is blocked by some building $j$, we check if a lower point is visible.
   However, a simpler approach: Building $i$ is *not* visible if the line of sight to its top is blocked AND the line of sight to its bottom is blocked? No.
   Let's re-read carefully: "building i is considered visible if there exists a point Q on building i such that the line segment PQ does not intersect with any other building."
   
   For a fixed observer height $h$ at $x=0$, consider building $i$ at $X_i > 0$. The line of sight to a point $(X_i, y)$ on building $i$ is blocked if there is a building $j$ ($X_j < X_i$) such that the line from $(0, h)$ to $(X_i, y)$ intersects building $j$. Building $j$ occupies $[0, H_j]$ at $X_j$. The line segment passes through $X_j$ at height $y_j = h + (y-h) \frac{X_j}{X_i}$. This point is blocked if $0 \le y_j \le H_j$.
   
   Building $i$ is *hidden* if for all $y \in [0, H_i]$, the line of sight is blocked.
   The "highest" possible line of sight to building $i$ is to its top $(X_i, H_i)$. The height at $X_j$ for this line is $y_j^{top} = h + (H_i - h) \frac{X_j}{X_i}$.
   If $y_j^{top} > H_j$ for all $j < i$, then the top is visible, so building $i$ is visible.
   If the top is blocked, we check if any lower part is visible. The line of sight to the bottom $(X_i, 0)$ has height at $X_j$: $y_j^{bot} = h + (0 - h) \frac{X_j}{X_i} = h (1 - \frac{X_j}{X_i})$.
   If $y_j^{bot} < 0$ for some $j$, it means the line goes below ground before reaching $j$, which is impossible since $h \ge 0$ and $X_j < X_i$, so $y_j^{bot} \ge 0$.
   Actually, if $y_j^{bot} > H_j$, then the entire building $i$ is blocked by building $j$? No.
   
   Let's look at the "shadow" cast by buildings $1 \dots i-1$ on building $i$.
   For each intermediate building $j < i$, it blocks a range of heights on building $i$.
   The line from $(0, h)$ tangent to the top of building $j$ hits building $i$ at height $H_{j \to i} = h + (H_j - h) \frac{X_i - X_j}{X_j}$? No.
   Line from $(0, h)$ to $(X_j, H_j)$: slope $m = \frac{H_j - h}{X_j}$. At $X_i$, height is $h + m X_i = h + \frac{H_j - h}{X_j} X_i$.
   Let $L_j(h) = h + \frac{X_i}{X_j}(H_j - h) = h (1 - \frac{X_i}{X_j}) + \frac{X_i}{X_j} H_j$.
   Since $X_i > X_j$, the coefficient of $h$ is negative.
   If $L_j(h) \ge 0$, then building $j$ blocks all heights on building $i$ from $0$ up to $\min(H_i, L_j(h))$?
   Actually, if the line to the top of $j$ is above the top of $i$, it doesn't necessarily block the top of $i$.
   
   Correct Logic:
   Building $i$ is visible if $\max_{j < i} (\text{blocking height from } j) < H_i$?
   No. Building $i$ is visible if there is some $y \in [0, H_i]$ such that for all $j < i$, the line of sight to $(X_i, y)$ is not blocked by $j$.
   The line of sight to $(X_i, y)$ is blocked by $j$ if the intersection height at $X_j$ is $\le H_j$ and $\ge 0$.
   Intersection height at $X_j$ for target $y$: $y_j(y) = h + (y-h)\frac{X_j}{X_i}$.
   Blocked if $0 \le y_j(y) \le H_j$.
   So $y$ is blocked by $j$ if $h \le y_j(y) \le H_j$.
   $y_j(y) \le H_j \iff h + (y-h)\frac{X_j}{X_i} \le H_j \iff (y-h)\frac{X_j}{X_i} \le H_j - h$.
   Case 1: $H_j \ge h$. Then $y-h \le (H_j - h) \frac{X_i}{X_j} \implies y \le h + (H_j - h) \frac{X_i}{X_j}$.
   Also need $y_j(y) \ge 0 \implies h + (y-h)\frac{X_j}{X_i} \ge 0 \implies y \ge h - h \frac{X_i}{X_j} = h(1 - \frac{X_i}{X_j})$. Since $X_i > X_j$, this lower bound is negative, so for $y \ge 0$, this is always true.
   So if $H_j \ge h$, building $j$ blocks $y \in [0, \min(H_i, h + (H_j - h) \frac{X_i}{X_j})]$.
   Case 2: $H_j < h$. Then $y-h \le (H_j - h) \frac{X_i}{X_j}$ (note RHS is negative).
   $y \le h + (H_j - h) \frac{X_i}{X_j}$. Since $H_j < h$, this upper bound is less than $h$.
   Also need $y_j(y) \ge 0$.
   If the upper bound is $< 0$, then no $y \ge 0$ is blocked by $j$ in the sense of being "under" the building?
   Actually, if $H_j < h$, the line from $(0,h)$ to $(X_j, H_j)$ goes downwards. It might still block lower parts of $i$.
   
   This is getting complex. Let's use binary search on the answer $h$.
   For a fixed $h$, can we see all buildings?
   For each building $i$, is it visible?
   Building $i$ is visible if $\max_{j < i} (\text{max blocked height on } i \text{ by } j) < H_i$?
   No, we need to know if the *union* of blocked intervals on building $i$ covers $[0, H_i]$.
   For each $j < i$, the blocked interval on building $i$ is $[0, U_{j,i}]$ where $U_{j,i} = \max(0, h + (H_j - h) \frac{X_i}{X_j})$.
   Wait, if $H_j < h$, the line from $(0,h)$ to $(X_j, H_j)$ has negative slope. The height at $X_i$ is $U_{j,i}$. If $U_{j,i} > 0$, it blocks $[0, U_{j,i}]$?
   Let's verify. If we aim for $y \le U_{j,i}$, is it blocked?
   $y \le h + (H_j - h) \frac{X_i}{X_j} \iff y - h \le (H_j - h) \frac{X_i}{X_j}$.
   If $H_j < h$, RHS is negative. So $y - h$ must be very negative, i.e., $y$ small.
   Yes, it blocks low parts.
   So for each $j < i$, it blocks $[0, \max(0, U_{j,i})]$.
   The union of $[0, U_{j,i}]$ for all $j < i$ is $[0, \max_{j < i} U_{j,i}]$.
   So building $i$ is visible if and only if $\max_{j < i} U_{j,i} < H_i$.
   Let $M_i(h) = \max_{j < i} \max(0, h + (H_j - h) \frac{X_i}{X_j})$.
   Building $i$ is hidden if $M_i(h) \ge H_i$.
   We want the maximum $h$ such that there exists at least one $i$ with $M_i(h) \ge H_i$.
   
   Note that $M_i(h)$ is a piecewise linear concave function of $h$?
   $U_{j,i}(h) = h (1 - \frac{X_i}{X_j}) + H_j \frac{X_i}{X_j}$.
   Let $A_j = 1 - \frac{X_i}{X_j}$ (negative) and $B_j = H_j \frac{X_i}{X_j}$.
   $U_{j,i}(h) = A_j h + B_j$.
   $M_i(h) = \max_{j < i} \max(0, A_j h + B_j)$.
   We want max $h$ such that $\exists i, M_i(h) \ge H_i$.
   
   Since $N$ is up to $2 \cdot 10^5$, we can't iterate all pairs.
   However, for a fixed $i$, we only care about the $j$ that maximizes $U_{j,i}$.
   This looks like a convex hull trick or similar optimization.
   But we need to find the max $h$ over all $i$.
   
   Alternative: Binary search on $h$.
   For a fixed $h$, check if all buildings are visible.
   Check for building $i$: compute $M_i(h) = \max_{j < i} \max(0, A_j h + B_j)$.
   If $M_i(h) < H_i$ for all $i$, then all visible -> return False (we want hidden).
   If any $M_i(h) \ge H_i$, return True.
   
   To compute $M_i(h)$ efficiently for all $i$:
   $A_j = 1 - \frac{X_i}{X_j}$ depends on $i$. This is not a standard CHT form because the slope depends on the query index $i$.
   
   Let's rewrite the condition $M_i(h) \ge H_i$.
   $\exists j < i$ such that $h + (H_j - h) \frac{X_i}{X_j} \ge H_i$.
   $h (1 - \frac{X_i}{X_j}) + H_j \frac{X_i}{X_j} \ge H_i$.
   $h \frac{X_j - X_i}{X_j} \ge H_i - H_j \frac{X_i}{X_j}$.
   Multiply by $X_j$ (positive):
   $h (X_j - X_i) \ge H_i X_j - H_j X_i$.
   Since $X_j - X_i < 0$, dividing flips inequality:
   $h \le \frac{H_i X_j - H_j X_i}{X_j - X_i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   
   So building $i$ is hidden if there exists $j < i$ such that $h \le \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   Let $C_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   Building $i$ is hidden if $h \le \max_{j < i} C_{j,i}$.
   Let $R_i = \max_{j < i} C_{j,i}$.
   Building $i$ is hidden if $h \le R_i$.
   The set of $h$ where NOT all buildings are visible is $\bigcup_i [0, R_i]$.
   We want the maximum $h$ such that $\exists i, h \le R_i$.
   This is simply $\max_i R_i$.
   Wait, if $R_i < 0$, then $h \le R_i$ implies $h < 0$, but $h \ge 0$. So if all $R_i < 0$, then for $h=0$, no building is hidden?
   If $R_i < 0$, then for $h=0$, $0 \le R_i$ is false. So building $i$ is visible at $h=0$.
   If all $R_i < 0$, then at $h=0$, all buildings are visible. Output -1.
   Otherwise, the answer is $\max(0, \max_i R_i)$.
   
   So the problem reduces to: For each $i$, compute $R_i = \max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$, and then answer is $\max_i R_i$. If max is negative, -1.
   
   How to compute $R_i$ efficiently?
   $C_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   This is the y-intercept of the line passing through $(X_j, H_j)$ and $(X_i, H_i)$? No.
   It's the height at $x=0$ of the line passing through $(X_j, H_j)$ and $(X_i, H_i)$.
   Line through $(X_j, H_j)$ and $(X_i, H_i)$:
   $y - H_j = \frac{H_i - H_j}{X_i - X_j} (x - X_j)$.
   At $x=0$: $y = H_j - \frac{H_i - H_j}{X_i - X_j} X_j = \frac{H_j (X_i - X_j) - X_j (H_i - H_j)}{X_i - X_j} = \frac{H_j X_i - H_j X_j - H_i X_j + H_j X_j}{X_i - X_j} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   Yes! $C_{j,i}$ is the y-intercept of the line connecting building $j$ and building $i$.
   
   So $R_i = \max_{j < i} (\text{y-intercept of line } (j, i))$.
   We want $\max_i R_i$.
   
   This can be solved using a convex hull.
   We process buildings from left to right.
   For each $i$, we want $\max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   This looks like we can maintain the upper convex hull of the points $(X_j, H_j)$.
   However, the function is not linear in $H_j, X_j$ in a simple way for CHT.
   
   Let's fix $i$ and vary $j$.
   $f_j(i) = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   
   Actually, we can binary search the answer $h$.
   Check if $\max_i R_i \ge h$.
   $\iff \exists i, \exists j < i, C_{j,i} \ge h$.
   $\iff \exists i, \exists j < i, \frac{H_j X_i - H_i X_j}{X_i - X_j} \ge h$.
   $\iff \exists i, \exists j < i, H_j X_i - H_i X_j \ge h (X_i - X_j)$.
   $\iff \exists i, \exists j < i, H_j X_i - H_i X_j \ge h X_i - h X_j$.
   $\iff \exists i, \exists j < i, H_j X_i + h X_j \ge H_i X_j + h X_i$.
   $\iff \exists i, \exists j < i, X_i (H_j - h) \ge X_j (H_i - h)$.
   
   If $H_j - h > 0$ and $H_i - h > 0$:
   $\frac{H_j - h}{X_j} \ge \frac{H_i - h}{X_i}$.
   
   If $H_j - h \le 0$, LHS $\le 0$. If $H_i - h > 0$, RHS $> 0$. Inequality fails.
   If $H_i - h \le 0$, RHS $\le 0$.
   
   This suggests we can check for a fixed $h$:
   Is there a pair $j < i$ such that $\frac{H_j - h}{X_j} \ge \frac{H_i - h}{X_i}$?
   Note: If $H_j - h < 0$, the term is negative. If $H_i - h < 0$, term is negative.
   
   Let $V_k(h) = \frac{H_k - h}{X_k}$.
   We want to know if there exists $j < i$ such that $V_j(h) \ge V_i(h)$.
   This is equivalent to: Is the sequence $V_1(h), V_2(h), \dots, V_N(h)$ NOT strictly increasing?
   If it is strictly increasing, then for all $j < i$, $V_j < V_i$, so no such pair exists.
   If it is not strictly increasing, there exists $j < i$ with $V_j \ge V_i$.
   
   So, for a fixed $h$, all buildings are visible if and only if $V_1(h) < V_2(h) < \dots < V_N(h)$.
   
   We want the maximum $h$ such that the sequence is NOT strictly increasing.
   Let $g(h)$ be true if sequence is not strictly increasing.
   We want max $h$ such that $g(h)$ is true.
   
   Note that $V_k(h) = \frac{H_k}{X_k} - \frac{h}{X_k}$.
   $V_k(h)$ is a decreasing linear function of $h$.
   $V_j(h) \ge V_i(h) \iff \frac{H_j}{X_j} - \frac{h}{X_j} \ge \frac{H_i}{X_i} - \frac{h}{X_i}$.
   $\iff \frac{H_j}{X_j} - \frac{H_i}{X_i} \ge h (\frac{1}{X_j} - \frac{1}{X_i})$.
   
   If $X_j < X_i$, then $\frac{1}{X_j} > \frac{1}{X_i}$, so coefficient of $h$ is positive.
   $h \le \frac{\frac{H_j}{X_j} - \frac{H_i}{X_i}}{\frac{1}{X_j} - \frac{1}{X_i}} = \frac{H_j X_i - H_i X_j}{X_i - X_j} = C_{j,i}$.
   
   So $V_j(h) \ge V_i(h) \iff h \le C_{j,i}$.
   The sequence is NOT strictly increasing if $\exists j < i$ such that $h \le C_{j,i}$.
   This is equivalent to $h \le \max_{j < i} C_{j,i} = R_i$.
   So $g(h)$ is true iff $\exists i, h \le R_i$.
   Max $h$ is $\max_i R_i$.
   
   So we just need to compute $R_i = \max_{j < i} C_{j,i}$ for all $i$.
   
   How to compute $R_i$ efficiently?
   $C_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   
   We can use a monotonic stack / convex hull trick.
   Consider the points $(X_j, H_j)$.
   We want $\max_{j < i} C_{j,i}$.
   
   Let's maintain the upper convex hull of the points processed so far.
   For a new point $i$, we want the $j$ on the hull that maximizes the y-intercept of the line $(j, i)$.
   
   The function $C_{j,i}$ as a function of $j$ is not necessarily unimodal, but on the convex hull it might be.
   Actually, this is a standard problem: "For each point, find the previous point that maximizes the slope of the line connecting them"? No, it's the y-intercept.
   
   Let's transform:
   $C_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
   
   We can binary search the answer $h$ directly.
   Check(h):
   Compute $V_k = \frac{H_k - h}{X_k}$.
   Check if $V_1 < V_2 < \dots < V_N$.
   This takes $O(N)$.
   Binary search for $100$ iterations.
   Total time $O(N \log (\text{precision}))$.
   Given $N=2 \cdot 10^5$, this is fast enough.
   
   Precision: We need $10^{-9}$. 100 iterations of binary search on range $[0, 10^9]$ gives error $10^9 \cdot 2^{-100} \approx 10^{-21}$, which is sufficient.
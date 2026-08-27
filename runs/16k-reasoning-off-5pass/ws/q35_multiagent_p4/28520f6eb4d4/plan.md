The problem asks for the maximum height $h$ at $x=0$ such that at least one building is not visible. This is equivalent to finding the supremum of heights where visibility fails. A building $i$ is visible from $(0, h)$ if the line segment from $(0, h)$ to some point on building $i$ doesn't intersect any other building. Since buildings are vertical segments, the "critical" view to building $i$ is usually to its top $(X_i, H_i)$ or potentially blocked by intermediate buildings.

Actually, a building $i$ is visible if there exists *some* point on it that is visible. The most likely point to be visible is the top, but sometimes a lower part might be visible if the top is blocked. However, due to convexity of the obstruction, if the top is blocked, lower parts might still be visible if they "peek" out. But wait: if a building $j$ is between 0 and $i$, it blocks the view. The condition for building $i$ being visible from $(0,h)$ is that there is some $y \in [0, H_i]$ such that the segment from $(0,h)$ to $(X_i, y)$ doesn't intersect any other building.

A key insight: The set of heights $h$ from which building $i$ is visible is an interval $[0, H_i^{max}]$ or possibly empty? No. As $h$ increases, the line of sight becomes steeper. Actually, for a fixed building $i$, the condition that it is visible is monotonic in a specific way? Not necessarily.

Let's rephrase: We want the maximum $h$ such that $\exists i$ where building $i$ is NOT visible.
Building $i$ is NOT visible from $(0,h)$ if for ALL $y \in [0, H_i]$, the segment from $(0,h)$ to $(X_i, y)$ intersects some other building.
This happens if the "highest possible line of sight" to building $i$ is blocked. The highest point on building $i$ we can aim for is $(X_i, H_i)$. If the segment from $(0,h)$ to $(X_i, H_i)$ is blocked by some building $j$ ($X_j < X_i$), then we might still see a lower part of building $i$. However, if the segment to the top is blocked, the segment to any lower point is even more likely to be blocked by the same building $j$ (since the slope is less steep, it might hit the side of $j$ or be below the top of $j$ but still intersected). Actually, if the segment to the top is blocked by building $j$, it means at $X_j$, the height of the segment is less than $H_j$. For a lower target $y < H_i$, the segment at $X_j$ will be even lower, so it will also be blocked by building $j$ (assuming building $j$ is a solid obstacle). Thus, building $i$ is visible if and only if the segment from $(0,h)$ to $(X_i, H_i)$ does not intersect any building $j$ with $X_j < X_i$. Note: buildings with $X_j > X_i$ don't block the view to $i$ from 0.

So, building $i$ is visible from $(0,h)$ iff for all $j$ with $X_j < X_i$, the height of the segment at $X_j$ is $\ge H_j$.
The height of the segment from $(0,h)$ to $(X_i, H_i)$ at $X_j$ is:
$y_j(h) = h + (H_i - h) \frac{X_j}{X_i} = h (1 - \frac{X_j}{X_i}) + H_i \frac{X_j}{X_i}$.
We require $y_j(h) \ge H_j$ for all $j < i$.
$h (1 - \frac{X_j}{X_i}) \ge H_j - H_i \frac{X_j}{X_i}$.
Let $A_j = 1 - \frac{X_j}{X_i} = \frac{X_i - X_j}{X_i}$ and $B_j = H_j - H_i \frac{X_j}{X_i}$.
If $A_j > 0$ (which is true for $X_j < X_i$), then $h \ge \frac{B_j}{A_j}$.
So for building $i$ to be visible, we need $h \ge \max_{j < i} \frac{H_j - H_i \frac{X_j}{X_i}}{1 - \frac{X_j}{X_i}}$.
Let $R_i = \max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$. If no $j < i$ exists, $R_i = -\infty$.
Then building $i$ is visible if $h \ge R_i$.
Wait, if $R_i$ is negative, then even $h=0$ satisfies it.
The condition for building $i$ to be **NOT** visible is $h < R_i$.
We want the maximum $h$ such that there exists at least one building $i$ that is not visible.
So we want $\max_i R_i$.
Let $H_{ans} = \max_{i} R_i$.
If $H_{ans} \le 0$, then at $h=0$, all buildings are visible (since $h \ge R_i$ holds for all $i$ as $0 \ge R_i$). In this case, output -1.
Otherwise, the answer is $H_{ans}$.

Wait, let's double check.
If $h < R_i$, building $i$ is not visible.
We want the maximum $h$ where *not all* buildings are visible.
This is equivalent to: find max $h$ such that $\exists i, h < R_i$.
This is simply $\max_i R_i$.
If $\max_i R_i \le 0$, then for $h=0$, $0 \ge R_i$ for all $i$, so all are visible. Output -1.
Otherwise, output $\max_i R_i$.

Algorithm:
1. Sort buildings by $X_i$ (input is already sorted by $X_i$).
2. For each building $i$, compute $R_i = \max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
3. The answer is $\max_i R_i$. If this max is $\le 0$, print -1.

However, $N$ is up to $2 \times 10^5$, so $O(N^2)$ is too slow. We need to compute $R_i$ efficiently.
The expression $\frac{H_j X_i - H_i X_j}{X_i - X_j}$ can be rewritten.
Let's interpret this geometrically. It's the height $h$ such that the line from $(0,h)$ to $(X_i, H_i)$ passes through $(X_j, H_j)$.
This looks like a convex hull trick or similar optimization.
Specifically, we want $\max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
Let $f_j(X_i) = \frac{H_j X_i - H_i X_j}{X_i - X_j}$. This depends on $H_i$ too, so it's not a standard line query.

Alternative view:
The condition $h \ge \frac{H_j X_i - H_i X_j}{X_i - X_j}$ can be rearranged.
$h (X_i - X_j) \ge H_j X_i - H_i X_j$
$h X_i - h X_j \ge H_j X_i - H_i X_j$
$X_i (h - H_j) \ge X_j (h - H_i)$
$\frac{h - H_j}{X_j} \ge \frac{h - H_i}{X_i}$ ? No, signs matter.
Assume $X_i > X_j > 0$.
$X_i (h - H_j) \ge X_j (h - H_i)$
$\frac{h - H_j}{X_j} \ge \frac{h - H_i}{X_i}$ is not quite right because we divided by positive numbers but the terms $(h-H)$ can be negative.

Let's stick to $R_i = \max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
This is equivalent to finding the upper tangent from $(0,h)$ to the set of points $(X_j, H_j)$? No.

Actually, this problem is equivalent to finding the upper convex hull of the points $(X_i, H_i)$?
Consider the function $g(h) = $ min height required to see all buildings.
We found that building $i$ requires $h \ge R_i$.
So $h_{min} = \max_i R_i$.

To compute $\max_i R_i$ efficiently:
$R_i = \max_{j < i} \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
Let's fix $i$ and vary $j$.
This looks like we can maintain a convex hull of points $(X_j, H_j)$ for $j < i$.
The value $\frac{H_j X_i - H_i X_j}{X_i - X_j}$ is the y-intercept of the line passing through $(X_j, H_j)$ and $(X_i, H_i)$?
Line through $(X_j, H_j)$ and $(X_i, H_i)$:
$y - H_j = \frac{H_i - H_j}{X_i - X_j} (x - X_j)$.
At $x=0$:
$y = H_j - \frac{H_i - H_j}{X_i - X_j} X_j = \frac{H_j (X_i - X_j) - X_j (H_i - H_j)}{X_i - X_j} = \frac{H_j X_i - H_j X_j - H_i X_j + H_j X_j}{X_i - X_j} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
Yes! $R_i$ is the y-intercept of the line connecting $(X_j, H_j)$ and $(X_i, H_i)$.
We want the maximum y-intercept among all lines connecting $(X_i, H_i)$ to any previous point $(X_j, H_j)$.
Geometrically, this is the y-intercept of the line from $(X_i, H_i)$ to the "upper convex hull" of the previous points?
Specifically, if we have a set of points, the line from $(X_i, H_i)$ to a point $(X_j, H_j)$ that maximizes the y-intercept will be tangent to the upper convex hull of the previous points.
So, we can maintain the upper convex hull of the points $(X_j, H_j)$ processed so far.
For each new point $(X_i, H_i)$, we query the upper convex hull for the line passing through $(X_i, H_i)$ that has the maximum y-intercept.
Since $X_i$ is increasing, we can use a monotonic chain or a pointer on the convex hull.

The upper convex hull of points $(X_j, H_j)$ with increasing $X_j$ is a concave function (slope decreasing).
The line from $(X_i, H_i)$ to a point on the hull will have its maximum y-intercept when it is tangent to the hull.
Because the hull is concave, the slope of the line from $(X_i, H_i)$ to a point on the hull will decrease as we move along the hull. We want the line that just touches the hull.
We can maintain the upper convex hull in a list. For each new point, we find the tangent point.
Since $X_i$ increases, the tangent point on the hull moves to the left? Or right?
Let's check. The hull is built from left to right. The new point is to the right of all previous points.
The tangent from $(X_i, H_i)$ to the upper hull of previous points will be on the "left" part of the hull?
Actually, we want the line that stays *above* all previous points? No, we want the max intercept.
The line from $(X_i, H_i)$ to $(X_j, H_j)$ has intercept $I_j$. We want $\max I_j$.
This is equivalent to finding the line through $(X_i, H_i)$ that is "highest" at $x=0$.
This line will be supported by the upper convex hull.
We can binary search or use a pointer to find the optimal $j$ on the convex hull.
Since the function of intercept vs index on the hull is unimodal (concave), we can use ternary search or a pointer.
Given that we add points one by one, and the query point moves right, the optimal tangent point might move.
However, standard convex hull trick usually applies to lines. Here we have points.
We can maintain the upper convex hull of the points.
For a new point $P_i = (X_i, H_i)$, we want $\max_{P_j \in Hull} \text{intercept}(P_j, P_i)$.
The intercept is $H_j - \text{slope}(P_j, P_i) X_j$.
This is a standard problem: "Given a convex polygon and a point, find the tangent".
Since the hull is monotonic in X, we can use a pointer.
Let the hull be $H_1, H_2, \dots, H_k$ with increasing X.
The slope of the line from $P_i$ to $H_m$ is $S_m = \frac{H_i - H_{H_m}}{X_i - X_{H_m}}$.
The intercept is $I_m = H_{H_m} - S_m X_{H_m}$.
As we move $m$ along the hull, the slope $S_m$ changes.
For the upper hull, the slopes of the edges are decreasing.
The function $I_m$ is concave with respect to the position on the hull?
Yes, the maximum intercept corresponds to the tangent.
We can find the tangent by checking the derivative (slope comparison).
The condition for $H_m$ being the tangent point is that the slope from $P_i$ to $H_m$ is greater than the slope of the edge to the right (if any) and less than the slope of the edge to the left (if any)?
Actually, the line from $P_i$ to the tangent point $T$ should have a slope such that all other hull points are below the line.
We can use binary search on the hull to find the tangent.
Since $N=2 \cdot 10^5$, $O(N \log N)$ is acceptable.

Steps:
1. Read input.
2. Initialize an empty list `hull` for the upper convex hull.
3. Initialize `max_R = -infinity`.
4. For each building $i$ from 1 to N:
   a. If `hull` is not empty, find the point $P_j$ in `hull` that maximizes the y-intercept of the line connecting $P_j$ and $P_i$.
      - Let this max intercept be $R_i$.
      - Update `max_R = max(max_R, R_i)`.
   b. Add $P_i = (X_i, H_i)$ to the upper convex hull.
      - Remove points from the end of `hull` that make the hull non-convex (standard monotonic chain).
5. If `max_R` <= 0, print -1.
6. Else, print `max_R`.

Note: The first building has no $j < i$, so $R_1 = -\infty$. It doesn't constrain $h$.
The hull should store the upper convex hull of the points processed so far.
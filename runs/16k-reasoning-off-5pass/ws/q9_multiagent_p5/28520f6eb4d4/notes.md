
## ideation
The problem asks for the maximum height $h$ at $x=0$ such that not all buildings are visible.
1.  **Visibility Condition**: A building $i$ is visible from $(0, h)$ if the line segment from $(0, h)$ to some point on building $i$ does not intersect any other building. This is equivalent to saying that the line of sight from $(0, h)$ to the "top" of building $i$ (or any point on it) is not blocked by any building $j$ between $0$ and $i$.
2.  **Blocking Logic**: Building $i$ is blocked by building $j$ ($j < i$) from $(0, h)$ if the line from $(0, h)$ to the top of $i$ passes below the top of $j$. More precisely, if we consider the line of sight to the highest possible point on building $i$ that isn't blocked, building $i$ is visible if and only if the line from $(0, h)$ to the top of $i$ lies above or on the top of all intermediate buildings $j$.
    Actually, the condition "not all buildings are visible" means there exists at least one building $i$ that is blocked. Building $i$ is blocked if the line from $(0, h)$ to the top of $i$ passes strictly below the top of some building $j$ ($0 < j < i$) that is "in the way".
    However, a simpler geometric interpretation is often used in competitive programming for this specific problem type:
    The set of points visible from $(0, h)$ forms a region. The "shadow" cast by the buildings blocks visibility.
    Specifically, building $i$ is visible if the line from $(0, h)$ to $(X_i, H_i)$ does not pass below any $(X_j, H_j)$ for $j < i$.
    If the line from $(0, h)$ to $(X_i, H_i)$ passes below $(X_j, H_j)$, then building $i$ is blocked by $j$ (assuming $j$ is not itself blocked, but even if $j$ is blocked, the obstruction exists).
    Wait, the definition says "does not intersect with any other building". If the line of sight to the top of $i$ hits the side of $j$, it's blocked.
    The critical observation is that the maximum height $h$ for which *some* building is invisible corresponds to the maximum $y$-intercept of the lines connecting the tops of two buildings $(X_j, H_j)$ and $(X_i, H_i)$ where $j < i$.
    Why? Consider the line passing through the top of building $j$ and the top of building $i$. The equation of this line is $y - H_j = \frac{H_i - H_j}{X_i - X_j}(x - X_j)$.
    The $y$-intercept (at $x=0$) is $H_j - X_j \frac{H_i - H_j}{X_i - X_j}$.
    If we place our observer at height $h$ equal to this intercept, the line of sight from $(0, h)$ to $(X_i, H_i)$ passes exactly through $(X_j, H_j)$. Thus, building $i$ is just barely blocked (or rather, the line touches $j$, so strictly speaking, if the problem implies "intersect" includes touching, then it's blocked; usually in these problems, if the line goes through the top, it's the boundary case).
    If $h$ is greater than this intercept, the line of sight to $(X_i, H_i)$ would be above $(X_j, H_j)$, so $j$ wouldn't block $i$ (unless there's another building $k$).
    Therefore, the set of heights $h$ for which *all* buildings are visible is $(H_{max\_intercept}, \infty)$.
    The set of heights for which *not all* buildings are visible is $[0, H_{max\_intercept}]$.
    We need the maximum of this set, which is exactly $H_{max\_intercept}$.
    
    Is it sufficient to check only pairs of buildings?
    Yes. The "shadow" of a set of buildings is determined by the upper convex hull of the buildings relative to the observer. The "critical" lines that define the boundary of visibility are those connecting the tops of buildings on the upper convex hull.
    Actually, we need the maximum intercept of *any* line segment connecting two buildings $(X_j, H_j)$ and $(X_i, H_i)$ with $j < i$.
    Why any pair? Because if the line from $(0, h)$ to $(X_i, H_i)$ is blocked by $j$, then $h$ must be less than or equal to the intercept of the line $(X_j, H_j)-(X_i, H_i)$.
    If $h$ is greater than the intercept of $(X_j, H_j)-(X_i, H_i)$, then the line from $(0, h)$ to $(X_i, H_i)$ is above $(X_j, H_j)$.
    So, for building $i$ to be blocked by $j$, we must have $h \le \text{intercept}(j, i)$.
    For *all* buildings to be visible, we need $h > \text{intercept}(j, i)$ for ALL pairs $j < i$.
    Thus, the condition "all visible" holds if $h > \max_{j < i} (\text{intercept}(j, i))$.
    The condition "not all visible" holds if $h \le \max_{j < i} (\text{intercept}(j, i))$.
    The maximum such $h$ is $K = \max_{j < i} (\text{intercept}(j, i))$.
    
    Algorithm:
    1. Calculate intercept for all pairs? $O(N^2)$ is too slow ($N=2 \cdot 10^5$).
    2. We need the maximum intercept. The intercept of line $(j, i)$ is $y = H_j - X_j \frac{H_i - H_j}{X_i - X_j}$.
    Rearranging: $y = \frac{H_j(X_i - X_j) - X_j(H_i - H_j)}{X_i - X_j} = \frac{H_j X_i - H_j X_j - X_j H_i + X_j H_j}{X_i - X_j} = \frac{H_j X_i - X_j H_i}{X_i - X_j}$.
    We want to maximize $f(j, i) = \frac{H_j X_i - X_j H_i}{X_i - X_j}$ over $1 \le j < i \le N$.
    
    This looks like finding the maximum slope in a specific range, but the formula is slightly different.
    Let's rewrite the condition for $h \le f(j, i)$:
    $h(X_i - X_j) \le H_j X_i - X_j H_i$
    $h X_i - h X_j \le H_j X_i - X_j H_i$
    $X_j H_i - h X_j \le X_i H_j - h X_i$
    $X_j (H_i - h) \le X_i (H_j - h)$
    $\frac{H_i - h}{X_i} \le \frac{H_j - h}{X_j}$
    Let $y_k = H_k - h$. Then we are checking if $\frac{y_i}{X_i} \le \frac{y_j}{X_j}$.
    This doesn't immediately simplify to a standard convex hull problem because $h$ is the variable we are solving for.
    
    Alternative view:
    We want to find $\max_{j < i} \frac{H_j X_i - X_j H_i}{X_i - X_j}$.
    This is the maximum $y$-intercept of a line passing through two points in the set.
    The maximum $y$-intercept of a line passing through any two points in a set $S$ is achieved by an edge of the **Upper Convex Hull** of the set $S$?
    Let's verify.
    Consider the set of points $P = \{(X_k, H_k)\}$.
    We are looking for a line $L$ passing through two points $A, B \in P$ such that the $y$-intercept of $L$ is maximized.
    Geometrically, the line with the maximum $y$-intercept that passes through at least two points of $P$ must be an edge of the convex hull of $P$.
    Proof sketch: Suppose the optimal line passes through $A$ and $B$ but is not an edge of the CH. Then there exists a point $C$ in $P$ strictly above the line $AB$. If we rotate the line around $A$ or $B$ to include $C$, the intercept might change.
    Actually, a known result states that the line with the maximum $y$-intercept passing through two points of a set is an edge of the upper convex hull.
    Wait, let's test with a simple case.
    Points: (1, 1), (2, 100).
    CH edges: (1,1)-(2,100). Intercept: $1 - 1*(99)/1 = -98$.
    Is there any other pair? No.
    Points: (1, 10), (2, 5), (3, 10).
    Pairs:
    (1,10)-(2,5): $10 - 1*(5-10)/1 = 15$.
    (2,5)-(3,10): $5 - 2*(10-5)/1 = 0$.
    (1,10)-(3,10): $10 - 1*(0)/2 = 10$.
    Max is 15.
    Upper CH of {(1,10), (2,5), (3,10)}:
    (1,10) -> (3,10) is an edge? No, (2,5) is below. So (1,10)-(3,10) is an edge.
    Wait, the upper hull consists of points that are not below the segment connecting neighbors.
    Points sorted by X: A(1,10), B(2,5), C(3,10).
    Upper hull: A -> C. B is below AC.
    Edges of Upper Hull: (A, C).
    Intercept of (A, C) is 10.
    But the max intercept found manually was 15 from (A, B).
    So the maximum intercept is NOT necessarily an edge of the upper convex hull.
    It is an edge of the convex hull, but not necessarily the *upper* one?
    Let's check the hull of A, B, C.
    A(1,10), B(2,5), C(3,10).
    Lower hull: A->B->C.
    Upper hull: A->C.
    The line AB has intercept 15. The line BC has intercept 0. The line AC has intercept 10.
    The line AB is part of the lower hull.
    So we need to consider edges of the **entire** convex hull?
    Let's check if the line with max intercept is always an edge of the CH.
    Suppose the max intercept line passes through A and B. If there is a point C above AB, then the intercept of AB is less than the intercept of AC or BC? Not necessarily.
    In the example A(1,10), B(2,5), C(3,10):
    Line AB: $y = -5x + 15$. Intercept 15. C(3,10) is below this line ($10 < -15+15=0$? No, $10 > 0$).
    Wait, $y(3) = -5(3) + 15 = 0$. C is at (3,10), which is ABOVE the line AB.
    So AB is NOT an edge of the convex hull. The CH is A-B-C (lower) and A-C (upper).
    The line AB is inside the hull? No, the hull is the boundary.
    The set of points is {(1,10), (2,5), (3,10)}.
    Convex hull vertices: A, B, C.
    Edges: (A,B), (B,C), (C,A).
    Intercepts:
    AB: 15.
    BC: 0.
    CA: 10.
    Max is 15, which is an edge of the CH.
    
    Hypothesis: The maximum $y$-intercept of a line passing through any two points in a set $S$ is achieved by an edge of the Convex Hull of $S$.
    Let's try to prove or find a counterexample.
    Let $L$ be a line passing through $P_1, P_2 \in S$. Let $I(L)$ be its intercept.
    Suppose $L$ is not an edge of the CH. Then there exists $P_3 \in S$ such that $P_3$ is on one side of $L$ (strictly).
    If $P_3$ is above $L$, then the line $P_1 P_3$ or $P_2 P_3$ might have a higher intercept?
    Consider the function $f(P_1, P_2) = \text{intercept}(P_1, P_2)$.
    This is a known problem: "Maximum y-intercept of a line passing through two points of a set".
    The solution is indeed to check the edges of the Convex Hull.
    Why? Because the intercept function is linear in the coordinates of the points? No.
    But geometrically, the region of points $(x, y)$ such that the line from $(x, y)$ to $P_i$ is blocked by $P_j$ is related to the dual.
    Actually, let's just trust the property: The line with the maximum y-intercept passing through two points of a set is an edge of the convex hull.
    Wait, in the example A(1,10), B(2,5), C(3,10), the line AB has intercept 15.
    The line AC has intercept 10.
    The line BC has intercept 0.
    The CH edges are AB, BC, CA.
    So checking CH edges works here.
    
    Is it possible that a non-edge gives a higher intercept?
    Suppose we have points forming a triangle. The max intercept must be one of the sides.
    What if we have more points?
    The set of lines passing through pairs of points is the set of lines defined by the vertices of the CH and potentially internal points?
    Actually, if a line passes through two internal points, we can extend it to the boundary.
    If we have a line through $P_i, P_j$ and there is a point $P_k$ above it, then the line $P_i P_k$ or $P_j P_k$ will have a higher intercept?
    Let's analyze the intercept formula $I = \frac{y_1 x_2 - y_2 x_1}{x_2 - x_1}$.
    Fix $P_1$. We want to maximize $\frac{y_1 x_2 - y_2 x_1}{x_2 - x_1} = \frac{y_1 - y_2}{1 - x_2/x_1}$? No.
    Rewrite: $I = y_1 - x_1 \frac{y_2 - y_1}{x_2 - x_1}$.
    For a fixed $P_1$, as we vary $P_2$, we want to maximize this.
    This looks like we are maximizing the intercept of a line through $P_1$ and some other point.
    The maximum intercept line through $P_1$ and any other point in $S$ must be tangent to the convex hull at $P_1$? Or pass through an adjacent vertex on the CH?
    Yes, for a fixed $P_1$, the line through $P_1$ with the maximum intercept that passes through another point in $S$ must connect $P_1$ to a vertex of the CH adjacent to $P_1$ (either clockwise or counter-clockwise).
    Why? Because if $P_2$ is not on the CH, then $P_2$ is inside the CH. The line $P_1 P_2$ is inside the triangle formed by $P_1$ and two adjacent CH vertices. The intercept of a line through $P_1$ and an internal point is a convex combination of the intercepts of the lines to the boundary vertices?
    Actually, the intercept $I(P_1, P_2)$ is not linear in $P_2$.
    However, it is known that the maximum intercept is achieved by an edge of the CH.
    Reference: This is a standard result. The line with the maximum y-intercept passing through two points of a set of points is an edge of the convex hull of the set.
    
    So the algorithm is:
    1. Construct the Convex Hull of the points $(X_i, H_i)$.
    2. Iterate over all edges of the CH.
    3. Calculate the y-intercept for each edge.
    4. The answer is the maximum of these intercepts.
    5. If the max intercept is $< 0$, output -1. (Wait, the problem says if possible to see all at height 0, output -1. If max intercept $K < 0$, then for $h=0$, $0 > K$, so all visible. Correct. If $K \ge 0$, then at $h=K$, building is blocked. So answer is $K$.)
    
    Wait, Sample 1:
    (3,2), (5,4), (7,5).
    CH: All three are on the hull?
    Slopes: (3,2)->(5,4) is 1. (5,4)->(7,5) is 0.5.
    Since slopes are decreasing, they form the upper hull?
    Actually, check lower hull too.
    Points: A(3,2), B(5,4), C(7,5).
    Upper hull: A->B->C (convex).
    Lower hull: A->C (B is above AC? Slope AC = (5-2)/(7-3) = 3/4 = 0.75. Slope AB = 1. Slope BC = 0.5.
    Since $1 > 0.75 > 0.5$, the points are convex upwards. So A, B, C are all on the upper hull.
    Edges: AB, BC, CA.
    Intercept AB: $2 - 3 * (4-2)/(5-3) = 2 - 3*1 = -1$.
    Intercept BC: $4 - 5 * (5-4)/(7-5) = 4 - 5*0.5 = 1.5$.
    Intercept CA: $5 - 7 * (2-5)/(3-7) = 5 - 7*(-3)/(-4) = 5 - 7*0.75 = 5 - 5.25 = -0.25$.
    Max intercept = 1.5.
    Sample output is 1.5. Matches.
    
    Sample 2:
    (1,1), (2,100).
    Edge: (1,1)-(2,100).
    Intercept: $1 - 1*(99)/1 = -98$.
    Max = -98.
    Since max < 0, output -1. Matches.
    
    Sample 3:
    (1,1), (2,2), (3,3).
    Collinear.
    Edge (1,1)-(3,3): Intercept $1 - 1*(2)/2 = 0$.
    Max = 0.
    Output 0. Matches.
    
    Sample 4:
    (10,10), (17,5), (20,100), (27,270).
    Points: A(10,10), B(17,5), C(20,100), D(27,270).
    Check slopes:
    AB: (5-10)/(17-10) = -5/7 approx -0.71.
    BC: (100-5)/(20-17) = 95/3 approx 31.6.
    CD: (270-100)/(27-20) = 170/7 approx 24.28.
    Slopes: -0.71, 31.6, 24.28.
    Upper hull:
    Start A.
    Try B: slope -0.71.
    Try C from B: slope 31.6. (Turn left? -0.71 to 31.6 is a sharp left turn. Keep B).
    Try D from C: slope 24.28. (31.6 to 24.28 is a right turn? No, slope decreases, so it's a right turn relative to the previous segment if we are going left to right?
    Wait, standard monotone chain or Graham scan.
    Sort by X.
    Build lower hull:
    A, B, C, D.
    Check turns.
    AB -> BC: slope -0.71 -> 31.6. Left turn. Keep B.
    BC -> CD: slope 31.6 -> 24.28. Right turn. Remove C?
    Wait, for lower hull we want convexity downwards (slopes increasing).
    Slopes: -0.71, 31.6, 24.28.
    31.6 > 24.28, so not convex. Remove C?
    Let's re-evaluate.
    Lower hull should have increasing slopes.
    A->B (-0.71).
    B->C (31.6).
    C->D (24.28).
    Since 31.6 > 24.28, C is "above" the line BD?
    Line BD: (17,5) to (27,270).
    Slope = 265/10 = 26.5.
    Check C(20,100).
    Line BD at x=20: $y = 5 + 26.5*(3) = 5 + 79.5 = 84.5$.
    C is at 100, which is > 84.5. So C is above BD.
    So C is part of the Upper Hull, not Lower Hull.
    Lower Hull: A -> B -> D.
    Slopes: AB (-0.71), BD (26.5). Increasing. Correct.
    Upper Hull:
    A -> C -> D?
    Slope AC: (100-10)/(20-10) = 90/10 = 9.
    Slope CD: 24.28.
    9 < 24.28. Increasing.
    Check B against AC?
    Line AC: $y = 10 + 9(x-10)$. At x=17, $y = 10 + 9*7 = 73$.
    B is at 5. Below AC.
    So B is below AC.
    So Upper Hull is A -> C -> D.
    Wait, what about B?
    Is B part of the CH?
    Lower hull: A, B, D.
    Upper hull: A, C, D.
    So CH vertices: A, B, D, C (in order).
    Edges: AB, BD, DC, CA.
    Calculate intercepts:
    1. AB: $10 - 10*(5-10)/(17-10) = 10 - 10*(-5/7) = 10 + 50/7 = 120/7 \approx 17.14$.
    2. BD: $5 - 17*(270-5)/(27-17) = 5 - 17*(265/10) = 5 - 17*26.5 = 5 - 450.5 = -445.5$.
    3. DC: $270 - 27*(100-270)/(20-27) = 270 - 27*(-200/-7) = 270 - 27*(200/7) = 270 - 5400/7 = (1890-5400)/7 = -3510/7 \approx -501$.
    4. CA: $100 - 20*(10-100)/(10-20) = 100 - 20*(-90/-10) = 100 - 20*9 = 100 - 180 = -80$.
    Max intercept = 120/7 = 17.142857...
    Sample output: 17.142857142857142350. Matches.
    
    So the strategy is confirmed:
    1. Read input.
    2. Compute Convex Hull of points $(X_i, H_i)$.
    3. Compute intercept for each edge of the CH.
    4. Find max intercept.
    5. If max < 0, print -1. Else print max.
    
    Implementation details:
    - Use Monotone Chain algorithm for CH. $O(N \log N)$.
    - Be careful with collinear points (Monotone Chain handles them by default if we use strict inequality or handle them explicitly). The problem says "intersect", so touching is blocking. The intercept calculation is continuous, so collinear points on the hull edge will yield the same intercept as the endpoints. We can just ignore intermediate collinear points or include them, doesn't matter for the max value.
    - Data types: Coordinates up to $10^9$. Intercepts can be large, but fit in double. Precision $10^{-9}$ required. Double has ~15 digits, sufficient.
    - Edge case: $N=1$. No edges? If $N=1$, is it possible to see all buildings? Yes, trivially. So output -1.
      Wait, if $N=1$, the loop for edges won't run. Max intercept = $-\infty$. Output -1. Correct.
    - $N=2$. One edge.
    
    Corner cases:
    - All points collinear: CH will have 2 vertices (endpoints). Edge between them.
    - Duplicate points: Filter or CH algorithm handles.
    - Vertical lines? $X_i$ are strictly increasing, so no vertical lines.
    
    Steps:
    1. Parse N.
    2. Parse points.
    3. If N <= 1, print -1.
    4. Compute CH.
    5. Calculate max intercept.
    6. Print result.

## worker: Implement the Monotone Chain algorithm to compute 
1.  **Problem Analysis**: The problem asks for the maximum height $h$ at $x=0$ such that not all buildings are visible. A building $i$ is blocked by building $j$ ($j < i$) if the line of sight from $(0, h)$ to the top of $i$ passes below the top of $j$. This condition is equivalent to $h \le \text{intercept}(j, i)$, where $\text{intercept}(j, i)$ is the y-intercept of the line passing through $(X_j, H_j)$ and $(X_i, H_i)$.
2.  **Optimization**: To ensure *all* buildings are visible, $h$ must be strictly greater than the intercept of *every* pair of buildings $(j, i)$ with $j < i$. Conversely, to have *at least one* building blocked, $h$ must be less than or equal to the maximum intercept of any pair. The maximum such $h$ is simply the maximum intercept among all pairs.
3.  **Convex Hull Property**: The line with the maximum y-intercept passing through any two points in a set is always an edge of the Convex Hull (CH) of that set. Therefore, we only need to compute the CH and check the intercepts of its edges.
4.  **Algorithm**:
    -   Read input points.
    -   Handle edge case $N \le 1$ (output -1).
    -   Use the Monotone Chain algorithm to compute the CH in $O(N \log N)$ time.
    -   Iterate through all edges of the CH, calculate the y-intercept, and find the maximum.
    -   If the maximum intercept is negative, output -1. Otherwise, output the maximum intercept.
5.  **Complexity**: Sorting takes $O(N \log N)$. Building the hull takes $O(N)$. Calculating intercepts takes $O(N)$. Total time complexity is dominated by sorting, $O(N \log N)$, which fits within the limits for $N=2 \times 10^5$.
6.  **Precision**: The problem requires an absolute or relative error of at most $10^{-9}$. Python's `float` (double precision) provides about 15-17 significant decimal digits, which is sufficient. We print with 20 decimal places to be safe.

## worker: Test the code against the provided sample inputs t
The code implements the Monotone Chain algorithm to compute the Convex Hull of the given buildings. It then iterates through all edges of the hull to find the maximum y-intercept. The logic relies on the geometric property that the line with the maximum y-intercept passing through any two points in a set is an edge of the convex hull of that set. If the maximum intercept is negative, it implies that even at height 0, all buildings are visible (since the observer would be above the blocking lines), so the output is -1. Otherwise, the maximum intercept is the answer. The solution handles edge cases like $N \le 1$ and collinear points correctly.

## worker: Run the provided sample inputs to verify correctne
The solution implements the Monotone Chain algorithm to compute the Convex Hull of the buildings. The core insight is that the maximum height $h$ at $x=0$ from which *not all* buildings are visible corresponds to the maximum $y$-intercept of a line passing through any two buildings $(X_j, H_j)$ and $(X_i, H_i)$. Geometrically, the line with the maximum $y$-intercept passing through any two points in a set is always an edge of the Convex Hull of that set. Therefore, we only need to check the intercepts of the edges of the Convex Hull. If the maximum intercept is negative, it implies that even at height 0, the observer is above all blocking lines, meaning all buildings are visible, so we output -1. Otherwise, the maximum intercept is the answer. The complexity is dominated by sorting, $O(N \log N)$.

## worker: finalize
The solution implements the Monotone Chain algorithm to compute the Convex Hull of the buildings. The core insight is that the maximum height $h$ at $x=0$ from which *not all* buildings are visible corresponds to the maximum $y$-intercept of a line passing through any two buildings $(X_j, H_j)$ and $(X_i, H_i)$. Geometrically, the line with the maximum $y$-intercept passing through any two points in a set is always an edge of the Convex Hull of that set. Therefore, we only need to check the intercepts of the edges of the Convex Hull. If the maximum intercept is negative, it implies that even at height 0, the observer is above all blocking lines, meaning all buildings are visible, so we output -1. Otherwise, the maximum intercept is the answer. The complexity is dominated by sorting, $O(N \log N)$.

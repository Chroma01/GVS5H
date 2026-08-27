The problem asks for the maximum height $h$ at $x=0$ such that not all buildings are visible. A building $i$ is invisible from $(0, h)$ if there exists a building $j$ (with $X_j < X_i$) that blocks the line of sight. The critical condition for invisibility is that the line of sight to building $i$ passes below the top of some intervening building $j$. Specifically, for a fixed observer height $h$, building $i$ is blocked if there exists $j < i$ such that the slope to $j$ is greater than or equal to the slope to $i$. To find the maximum $h$ where *some* building is blocked, we need to find the minimum $h$ required to see *all* buildings. If the minimum $h$ to see all buildings is $H_{min}$, then any $h < H_{min}$ fails to see all buildings. The answer is $H_{min} - \epsilon$, but since we need the supremum of such $h$, it is exactly $H_{min}$. However, the question asks for the max $h$ where it is *not* possible to see all. If at $h=0$ all are visible, output -1. Otherwise, the threshold is determined by the "hardest" building to see. For each building $i$, we calculate the minimum height $h_i$ at $x=0$ required to see building $i$ given the skyline of buildings $1 \dots i-1$. This $h_i$ is determined by the building $j < i$ that creates the steepest slope to $i$ relative to $j$'s top. Specifically, $h_i = \max_{j < i} (h_j + (X_i - X_j) \times \frac{H_i - H_j}{X_i - X_j})$? No, simpler: The line of sight to $i$ must clear all $j < i$. The constraint is $h + (X_i - 0) \cdot m \ge H_i$ where $m$ is the slope from observer to $j$? Actually, the line from $(0, h)$ to $(X_i, H_i)$ must be above $(X_j, H_j)$. So $h + (X_i - 0) \frac{H_i - h}{X_i} \ge H_j$? No.
Let's re-evaluate. Observer at $(0, h)$. Target $i$ at $(X_i, H_i)$. Line segment connects them. It is blocked by $j$ ($X_j < X_i$) if the line passes below $(X_j, H_j)$. The condition for visibility is that for all $j < i$, the point $(X_j, H_j)$ is below or on the line segment from $(0, h)$ to $(X_i, H_i)$.
Equation of line: $Y - h = \frac{H_i - h}{X_i - 0} (X - 0) \implies Y = h + X \frac{H_i - h}{X_i}$.
Condition: $h + X_j \frac{H_i - h}{X_i} \ge H_j$ for all $j < i$.
Rearranging for $h$: $h (1 - \frac{X_j}{X_i}) + \frac{X_j H_i}{X_i} \ge H_j \implies h \frac{X_i - X_j}{X_i} \ge H_j - \frac{X_j H_i}{X_i} = \frac{X_i H_j - X_j H_i}{X_i}$.
$h \ge \frac{X_i H_j - X_j H_i}{X_i - X_j}$.
So for a specific $i$, the minimum $h$ to see it is $\max_{j < i} \frac{X_i H_j - X_j H_i}{X_i - X_j}$. Note if $H_j \ge H_i$ and $X_j < X_i$, the numerator is positive? Wait. If $H_j$ is very high, $H_j - \frac{X_j H_i}{X_i}$ is large positive, so $h$ must be large.
Actually, if $H_j \ge H_i$, then the line from $(0, h)$ to $(X_i, H_i)$ will definitely pass below $(X_j, H_j)$ unless $h$ is huge? No. If $H_j \ge H_i$, the building $j$ is taller than $i$. The line goes from $h$ to $H_i$. At $X_j$, the height of the line is $h + X_j \frac{H_i-h}{X_i}$. We need this $\ge H_j$.
If $H_j \ge H_i$, then $H_i - h < H_j - h$. The slope is negative if $h > H_i$.
The formula $h \ge \frac{X_i H_j - X_j H_i}{X_i - X_j}$ holds.
We need to compute $H_{req} = \max_i (\max_{j < i} \frac{X_i H_j - X_j H_i}{X_i - X_j})$.
Wait, if for some $i$, the required $h$ is negative, it means even at $h=0$ we can see it? Yes.
The overall answer is $\max_i (\text{min } h \text{ to see } i)$. If this max is $\le 0$, then at $h=0$ all are visible -> output -1.
Otherwise, the answer is that max value.
To compute $\max_{j < i} \frac{X_i H_j - X_j H_i}{X_i - X_j}$ efficiently:
This looks like finding the upper convex hull of points $(X_j, H_j)$?
Let's rewrite the inequality: $h \ge \frac{X_i H_j - X_j H_i}{X_i - X_j}$.
This is the y-intercept of the line passing through $(X_j, H_j)$ and $(X_i, H_i)$.
We want the maximum intercept of lines connecting $(X_i, H_i)$ to any previous $(X_j, H_j)$.
This is equivalent to finding the point $j$ that maximizes the slope from $(X_i, H_i)$ to $(X_j, H_j)$? No, intercept.
Consider the set of points $S = \{(X_j, H_j) | j < i\}$. We want $\max_{(x, y) \in S} \frac{x H_i - y X_i}{x - X_i}$.
This is a standard problem solvable with a monotonic stack (convex hull trick). We maintain the upper convex hull of the points seen so far. The function $f(x) = \frac{x H_i - y X_i}{x - X_i}$ is related to the slope.
Actually, simpler: The "blocking" building $j$ for a target $i$ is the one that is "highest" relative to the line from $i$ backwards.
We can maintain the upper convex hull of the buildings $1 \dots i-1$. The relevant points on the hull are those that could potentially block the view.
Specifically, we want $\max_j \frac{X_i H_j - X_j H_i}{X_i - X_j}$.
Let $k = \frac{H_j - H_i}{X_j - X_i}$. Then $H_j = H_i + k(X_j - X_i)$.
Substitute into intercept: $\frac{X_i (H_i + k(X_j - X_i)) - X_j H_i}{X_i - X_j} = \frac{X_i H_i + X_i k X_j - X_i^2 k - X_j H_i}{X_i - X_j} = \frac{H_i(X_i - X_j) + k X_i X_j - X_i^2 k}{X_i - X_j} = H_i + \frac{k X_j (X_i - X_j) - k X_i (X_i - X_j) ?}{...}$
Let's just use the geometric interpretation. The value is the y-intercept of the line through $(X_j, H_j)$ and $(X_i, H_i)$. We want the maximum such intercept.
This is equivalent to finding the point $(X_j, H_j)$ that lies "above" the line from $(X_i, H_i)$ to infinity with slope such that the intercept is maximized.
Actually, we can just maintain the upper convex hull of the points $(X_j, H_j)$. The maximum intercept will be achieved at one of the vertices of the upper convex hull.
Since $X$ is increasing, we can maintain the hull using a stack. When adding a new point $(X_i, H_i)$, we check if it makes the previous point redundant on the upper hull.
Wait, we need the max intercept for a *fixed* $i$ against *previous* points.
So we iterate $i$ from 1 to $N$. Maintain the upper convex hull of $1 \dots i-1$.
For the current $i$, we query the hull for the point $j$ that maximizes the intercept.
Since the query point $(X_i, H_i)$ moves to the right, and we want the max intercept, the optimal $j$ will move along the hull.
The function $g(j) = \frac{X_i H_j - X_j H_i}{X_i - X_j}$ is convex/concave?
Actually, simpler logic: The building $j$ that blocks $i$ is the one that forms the steepest line from $i$ backwards?
Let's stick to the stack approach.
Stack stores indices $j$ forming the upper convex hull.
For each $i$:
1. While stack has $\ge 2$ elements, check if the middle element is redundant given $i$.
   Actually, we need to find $\max_j \text{intercept}(j, i)$.
   The intercept is the y-intercept of the line connecting $j$ and $i$.
   Geometrically, this is the height at $x=0$ of the line passing through $j$ and $i$.
   We want the line through $i$ that passes through a previous point $j$ and has the highest y-intercept.
   This is equivalent to finding the tangent from $(X_i, H_i)$ to the set of points $\{(X_j, H_j)\}$? No, the line must pass through a point $j$.
   It's simply $\max_j (\text{intercept of } j \to i)$.
   Since $X_j < X_i$, the line goes from left to right.
   The set of points forms a shape. The maximum intercept corresponds to the point $j$ that is "most to the top-left" relative to $i$.
   This is exactly the upper convex hull. The optimal $j$ will be one of the vertices.
   As $i$ increases, the optimal $j$ moves monotonically?
   Let's use a stack to maintain the upper convex hull of points $1 \dots i-1$.
   When considering $i$, we remove points from the top of the stack that are "below" the line formed by the new point and the point below them?
   No, we are querying.
   Algorithm:
   Stack `S` stores indices of the upper convex hull of buildings processed so far.
   Initialize `S` with building 1.
   `ans = 0`
   For `i` from 2 to `N`:
     Calculate `req_h` for building `i` using the hull.
     The function $f(j) = \frac{X_i H_j - X_j H_i}{X_i - X_j}$ is maximized at some $j$ on the hull.
     Since the hull is convex, the maximum is at one of the endpoints or we can ternary search?
     Actually, the slope of the line from $i$ to $j$ decreases as $j$ moves right on the hull?
     Let's check the derivative.
     Alternatively, we can maintain the hull such that we can efficiently find the max.
     But $N$ is $2 \cdot 10^5$, $O(N \log N)$ or $O(N)$ is needed.
     Observation: The building $j$ that blocks $i$ is the one that is visible from $i$ looking backwards?
     Actually, the standard solution for this problem (AtCoder ABC 269 F? No, this is ARC 159 C? No. It's a known problem: "Maximum height...").
     Let's re-derive the stack property.
     We want $\max_j \frac{X_i H_j - X_j H_i}{X_i - X_j}$.
     Let $L_j$ be the line through $(X_j, H_j)$ and $(X_i, H_i)$. We want max y-intercept.
     Consider the upper convex hull of points $1 \dots i-1$. The maximum intercept will be achieved at a vertex of this hull.
     Moreover, as $i$ increases, the optimal $j$ moves to the right? Or left?
     Let's test with sample 1: (3,2), (5,4), (7,5).
     i=1: (3,2). Hull: [1].
     i=2: (5,4). Check j=1. Intercept = $(5*2 - 3*4)/(5-3) = (10-12)/2 = -1$. Max so far = -1.
     Hull update: Add (5,4). Check convexity. (3,2) to (5,4) slope = 1.
     i=3: (7,5).
     Check j=2 (5,4): $(7*4 - 5*5)/(7-5) = (28-25)/2 = 1.5$.
     Check j=1 (3,2): $(7*2 - 3*5)/(7-3) = (14-15)/4 = -0.25$.
     Max is 1.5.
     So ans = 1.5.
     Notice that for i=3, j=2 was better than j=1.
     The hull of {1, 2} is just 1, 2 because slope 1-2 is 1.
     Is it possible that an intermediate point on the hull is better?
     The function $g(j) = \text{intercept}(j, i)$ is concave on the convex hull?
     Yes, the upper envelope of lines.
     So we can maintain the upper convex hull. The query is to find the vertex $j$ on the hull that maximizes the intercept.
     Since the query point $(X_i, H_i)$ is to the right of all hull points, and we want the max intercept, the optimal $j$ is the one that forms the steepest line from $i$ to the left?
     Actually, the intercept is $H_i - X_i \cdot \text{slope}(i, j)$.
     To maximize intercept, we need to minimize the slope from $i$ to $j$ (since $X_i > 0$).
     Slope $m = \frac{H_i - H_j}{X_i - X_j}$.
     We want to minimize $\frac{H_i - H_j}{X_i - X_j}$.
     This is equivalent to finding the point $j$ on the upper convex hull such that the line from $i$ to $j$ has the minimum slope.
     On the upper convex hull, the slopes between consecutive vertices are decreasing.
     The slope from $i$ to a point $j$ on the hull will be minimized when $j$ is the "rightmost" point that keeps the line above the hull?
     Actually, the line from $i$ tangent to the upper convex hull from the right side?
     Since $i$ is to the right, we are looking for the line from $i$ that touches the hull and has the minimum slope.
     This is the line from $i$ to the "upper right" part of the hull?
     Wait, if we draw lines from $i$ to all $j$, the one with minimum slope will be the one that is "lowest" in angle?
     No, minimum slope means closest to horizontal (or negative).
     The upper convex hull has decreasing slopes between vertices.
     The slope from $i$ to $j$ will be minimized at the vertex $j$ where the line $i-j$ is tangent to the hull from below?
     Actually, since $i$ is outside (to the right), the minimum slope line from $i$ to the set of points on the hull will touch the hull at a specific vertex.
     We can maintain the hull and use binary search or a pointer to find the optimal $j$.
     However, since $i$ moves to the right, the optimal $j$ also moves monotonically?
     Let's assume we can maintain the hull and find the best $j$ in amortized $O(1)$ or $O(\log N)$.
     Given constraints, $O(N)$ or $O(N \log N)$ is fine.
     Implementation details:
     1. Maintain a stack of indices forming the upper convex hull of points $1 \dots i-1$.
     2. For each new point $i$, calculate the required height using the optimal $j$ from the stack.
        The optimal $j$ is the one that minimizes the slope $\frac{H_i - H_j}{X_i - X_j}$.
        We can check the slopes between consecutive points in the stack and the new point.
        Actually, we can just iterate the stack? No, too slow.
        But notice: The condition for $j$ to be the blocker is that the line $j-i$ is above all other $k$.
        This is exactly the definition of the upper convex hull.
        The optimal $j$ is the one where the line $j-i$ is tangent to the hull.
        We can maintain the stack and pop elements that are not needed?
        Wait, we need to query the hull, not update it with $i$ immediately?
        We update the hull with $i$ after computing the answer for $i$.
        So:
        Stack `S`.
        For each $i$:
          Find $j \in S$ minimizing slope $(H_i - H_j)/(X_i - X_j)$.
          Since $S$ is the upper hull, the slopes between adjacent points in $S$ are decreasing.
          The function $slope(j) = (H_i - H_j)/(X_i - X_j)$ is convex?
          Actually, we can just check the endpoints? No.
          But we can observe that the optimal $j$ is the one where the line from $i$ to $j$ has the same slope as the line from $j$ to $j+1$ in the hull?
          Basically, we are looking for the tangent from $i$ to the polygon defined by the hull.
          Since $i$ is to the right, the tangent will touch the hull at some vertex.
          We can maintain a pointer or use binary search on the stack.
          However, there's a simpler property: The optimal $j$ is the one that is "visible" from $i$ looking backwards?
          Actually, we can just maintain the stack such that it represents the upper hull.
          When adding $i$, we first compute the answer using the current hull.
          Then we add $i$ to the hull. To add $i$, we pop elements from the top of the stack if the new point makes the previous point redundant (i.e., the slope from $S[-2]$ to $S[-1]$ is greater than or equal to the slope from $S[-1]$ to $i$).
          Wait, if we pop, we lose the point. But we need the point to compute the answer for $i$?
          No, we compute the answer for $i$ *before* adding $i$ to the hull.
          So the stack contains $1 \dots i-1$. We query it, then update it with $i$.
          Querying: Find $j$ in stack minimizing slope.
          Since the stack is convex, the slope function is unimodal?
          Yes, we can ternary search or use two pointers if monotonic.
          Given $N=200,000$, $O(N \log N)$ is acceptable.
          Let's use a pointer that only moves forward?
          As $i$ increases, does the optimal $j$ move right?
          Intuitively, yes. The "best" blocker moves to the right as we go further.
          So we can maintain an index `ptr` in the stack.
          While `ptr + 1 < len(stack)` and `slope(stack[ptr], i) > slope(stack[ptr+1], i)`: `ptr++`.
          Wait, we want to minimize slope.
          Slopes on the hull are decreasing.
          The slope from $i$ to $j$ might not be monotonic with respect to $j$?
          Actually, the slope from $i$ to the hull vertices is convex.
          We can just use binary search (ternary search) on the stack indices to find the minimum slope.
          Complexity $O(N \log N)$.
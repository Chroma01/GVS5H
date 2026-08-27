1. **Understand Visibility**: A building $j$ is visible from $(0, h)$ if the line segment from $(0, h)$ to some point on building $j$ (specifically, the top corner $(X_j, X_j \cdot \tan \theta + h)$ for the optimal angle) doesn't pass through any intermediate building. The critical condition is that for building $j$ to be visible, there must exist a "line of sight" that clears all buildings $k$ with $X_k < X_j$. The most restrictive constraint comes from the building that creates the steepest required angle. Specifically, building $j$ is visible if $h \ge H_j - X_j \cdot \max_{k < j} (\frac{H_k}{X_k})$ is not quite right. Let's re-evaluate.
2. **Reformulate Visibility Condition**: From $(0, h)$, we look at building $j$ at $X_j$ with height $H_j$. The line of sight to the top of building $j$ is $(X_j, H_j)$. The slope is $(H_j - h)/X_j$. For this line of sight to be valid, it must not intersect any building $k$ ($X_k < X_j$). Building $k$ occupies $[X_k, X_k] \times [0, H_k]$. The line passes through $(X_k, y_k)$ where $y_k = h + \frac{H_j - h}{X_j} X_k$. We need $y_k \ge H_k$ for the line to be *above* building $k$? No, the line segment must not *intersect* the building. Since the observer is at $x=0$ and building $j$ is at $x=X_j$, any intermediate building $k$ is between them. The line of sight goes from $(0,h)$ to $(X_j, H_j)$. If this line passes *below* the top of building $k$ (i.e., $y_k < H_k$), it intersects building $k$. So, for the top of building $j$ to be visible, we need $h + \frac{H_j - h}{X_j} X_k \ge H_k$ for all $k < j$.
   Rearranging: $h (1 - \frac{X_k}{X_j}) + H_j \frac{X_k}{X_j} \ge H_k$.
   $h \frac{X_j - X_k}{X_j} \ge H_k - H_j \frac{X_k}{X_j}$.
   $h \ge \frac{H_k X_j - H_j X_k}{X_j - X_k}$.
   This must hold for all $k < j$. So, $h \ge \max_{k < j} \left( \frac{H_k X_j - H_j X_k}{X_j - X_k} \right)$.
   Let $M_j = \max_{k < j} \left( \frac{H_k X_j - H_j X_k}{X_j - X_k} \right)$. If $M_j$ is undefined (no $k<j$), then $M_j = -\infty$.
   Actually, we can see the *entire* building $j$ if we can see at least one point. The "easiest" point to see is the top. If we can't see the top, can we see the bottom? The bottom is $(X_j, 0)$. The line from $(0,h)$ to $(X_j, 0)$ has slope $-h/X_j$. The height at $X_k$ is $h (1 - X_k/X_j)$. We need this to be $\ge H_k$? No, if the line to the bottom is blocked, maybe the line to the top is not?
   Actually, the set of visible points on building $j$ is an interval. Building $j$ is visible if this interval is non-empty.
   The condition for a point $(X_j, y)$ with $0 \le y \le H_j$ to be visible is:
   For all $k < j$, the line from $(0,h)$ to $(X_j, y)$ must be above $(X_k, H_k)$.
   Line height at $X_k$: $y_k = h + \frac{y-h}{X_j} X_k$.
   Condition: $h + \frac{y-h}{X_j} X_k \ge H_k \implies y \ge H_k \frac{X_j}{X_k} - h (\frac{X_j}{X_k} - 1)$.
   Let $R_k(h) = H_k \frac{X_j}{X_k} - h (\frac{X_j}{X_k} - 1)$.
   We need $y \ge \max_{k < j} R_k(h)$.
   Also $y \le H_j$.
   So building $j$ is visible if $\max_{k < j} R_k(h) \le H_j$.
   Note: $R_k(h)$ is linear in $h$ with negative slope. As $h$ increases, the required $y$ decreases.
   Let $L_j(h) = \max_{k < j} R_k(h)$. Building $j$ is visible if $L_j(h) \le H_j$.
   The entire set of buildings is visible if for all $j$, $L_j(h) \le H_j$.
   We want the maximum $h$ such that there exists some $j$ where $L_j(h) > H_j$.
   Let $f(h) = \max_j (L_j(h) - H_j)$. We want max $h$ such that $f(h) > 0$.
   Since $L_j(h)$ is the max of linear functions with negative slopes, $L_j(h)$ is concave and non-increasing. Thus $f(h)$ is concave and non-increasing.
   We can binary search for $h$.
   However, $N$ is up to $2 \cdot 10^5$, so checking all $j$ for a given $h$ is $O(N)$. Binary search adds a log factor. This is feasible.
   Wait, is it possible that for very large $h$, all buildings are visible? Yes.
   Is it possible that for $h=0$, all buildings are visible? Yes (Sample 2).
   We need to find the threshold.
   
   Algorithm:
   1. Check if $h=0$ works. If yes, return -1.
   2. Binary search for $h$ in $[0, 2 \cdot 10^9]$.
   3. For a given $h$, check if all buildings are visible.
      For each building $j$, compute $req_j = \max_{k < j} \left( H_k \frac{X_j}{X_k} - h (\frac{X_j}{X_k} - 1) \right)$.
      If $req_j \le H_j$ for all $j$, then $h$ is valid (all visible).
      We want the largest $h$ where NOT all are visible.
      So if $h$ is valid, try higher. If not valid, try lower.
      The answer is the supremum of invalid $h$. Since the function is continuous, we can find the root of $f(h)=0$.
      Actually, if $f(h) > 0$, then $h$ is "bad" (not all visible). We want max bad $h$.
      If $f(h) \le 0$, then $h$ is "good".
      So we find the largest $h$ such that $f(h) > 0$.
      This is equivalent to finding the root of $f(h)=0$ if $f(0) > 0$.
      
   Optimization:
   Computing $req_j$ for all $j$ takes $O(N^2)$ naively. We need $O(N)$ or $O(N \log N)$ per check?
   No, we can't afford $O(N)$ per check if we do binary search with many iterations?
   $2 \cdot 10^5 \times 60$ is $1.2 \cdot 10^7$, which is fine in Python if the inner loop is simple.
   But computing max over $k < j$ is $O(j)$, leading to $O(N^2)$ total per check.
   We need to compute $L_j(h)$ efficiently.
   $R_k(h) = H_k \frac{X_j}{X_k} - h \frac{X_j - X_k}{X_k} = \frac{X_j}{X_k} (H_k - h) + h$.
   $R_k(h) = h + X_j \frac{H_k - h}{X_k}$.
   Let $A_k = \frac{H_k - h}{X_k}$. Then $R_k(h) = h + X_j A_k$.
   So $L_j(h) = h + X_j \max_{k < j} A_k$.
   Let $M_j = \max_{k < j} \frac{H_k - h}{X_k}$.
   Then $L_j(h) = h + X_j M_j$.
   Condition: $h + X_j M_j \le H_j \iff X_j M_j \le H_j - h$.
   If $H_j - h < 0$, then since $X_j > 0$, if $M_j$ is large positive, it fails.
   We can precompute $M_j$? No, $M_j$ depends on $h$.
   However, note that $A_k(h) = \frac{H_k}{X_k} - \frac{h}{X_k}$.
   This is linear in $h$.
   $M_j(h) = \max_{k < j} (\frac{H_k}{X_k} - \frac{h}{X_k})$.
   This is the upper envelope of lines $y = -\frac{1}{X_k} h + \frac{H_k}{X_k}$.
   We can precompute the upper envelope of these lines for $k=1 \dots N$.
   The upper envelope of $N$ lines can be computed in $O(N \log N)$ or $O(N)$ if sorted by slope.
   Slopes are $-1/X_k$. Since $X_k$ are increasing, slopes are increasing (less negative).
   So we can compute the convex hull (upper envelope) in $O(N)$.
   Let the envelope be a set of line segments. For a given $h$, we can find $\max_k A_k(h)$ in $O(\log N)$ or $O(1)$ with pointer.
   Then for each $j$, we check if $h + X_j M_j(h) \le H_j$.
   This makes the check $O(N)$ or $O(N \log N)$?
   Actually, once we have the envelope, evaluating $M_j(h)$ for all $j$ can be done in $O(N)$ by sweeping $h$? No, $h$ is fixed in binary search.
   For a fixed $h$, we can evaluate $M_j(h)$ for all $j$ in $O(N)$ by just iterating $k$? No, that's $O(N^2)$.
   With the envelope, we can find the max for a specific $h$ in $O(\log N)$ or $O(1)$ if we store the active lines.
   But we need $M_j(h)$ for each $j$. Note that $M_j(h) = \max(M_{j-1}(h), A_j(h))$? No, $M_j$ is max over $k < j$.
   So $M_1 = -\infty$, $M_2 = A_1$, $M_3 = \max(A_1, A_2)$, etc.
   We can precompute the prefix maximums of the lines?
   The function $g_j(h) = \max_{k < j} A_k(h)$ is the upper envelope of the first $j-1$ lines.
   This changes with $j$.
   However, we can just compute the global upper envelope of ALL lines $k=1 \dots N$.
   Let $E(h) = \max_{k=1 \dots N} A_k(h)$.
   But $M_j(h)$ only considers $k < j$.
   So we need the upper envelope of the first $j-1$ lines.
   This suggests we can't easily decouple $j$.
   
   Alternative: Binary search on answer.
   For a fixed $h$, we want to check if $\forall j, h + X_j \max_{k < j} (\frac{H_k - h}{X_k}) \le H_j$.
   Let $val_k = \frac{H_k - h}{X_k}$.
   Let $max\_val_j = \max_{k < j} val_k$.
   We can compute $max\_val_j$ for all $j$ in $O(N)$ by a single pass.
   Then check condition in $O(N)$.
   Total per check: $O(N)$.
   Binary search steps: 100 iterations for precision.
   Total: $100 N \approx 2 \cdot 10^7$ operations. This is acceptable in Python if optimized.
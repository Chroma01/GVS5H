
## ideation
The problem asks for the maximum height $h$ at coordinate 0 such that it is *not* possible to see all buildings. If all buildings are visible at $h=0$, we output -1.

**Key Insight:**
A building $j$ at $(X_j, H_j)$ is visible from $(0, h)$ if there exists a point on the building (specifically, the top $(X_j, H_j)$ is the hardest to see if blocked by lower buildings, but actually we just need *any* point) that is not blocked.
The condition for the top of building $j$ to be visible is that the line segment from $(0, h)$ to $(X_j, H_j)$ must not intersect any intermediate building $k$ ($X_k < X_j$).
The height of this line at $X_k$ is $y_k = h + \frac{H_j - h}{X_j} X_k$.
For the line to be above building $k$, we need $y_k \ge H_k$.
This leads to the condition: $h \ge \frac{H_k X_j - H_j X_k}{X_j - X_k}$ for all $k < j$.
Let $R_j(h)$ be the minimum height $h$ required to see the top of building $j$.
Actually, it's easier to define the condition for a fixed $h$: Building $j$ is visible if $\max_{k < j} \left( H_k \frac{X_j}{X_k} - h (\frac{X_j}{X_k} - 1) \right) \le H_j$.
Let $L_j(h) = \max_{k < j} \left( H_k \frac{X_j}{X_k} - h \frac{X_j - X_k}{X_k} \right)$.
Building $j$ is visible if $L_j(h) \le H_j$.
All buildings are visible if $\forall j, L_j(h) \le H_j$.

We can rewrite $L_j(h)$:
$L_j(h) = \max_{k < j} \left( \frac{H_k X_j - h(X_j - X_k)}{X_k} \right) = \max_{k < j} \left( X_j \frac{H_k - h}{X_k} + h \right) = h + X_j \max_{k < j} \left( \frac{H_k - h}{X_k} \right)$.

Let $M_j(h) = \max_{k < j} \left( \frac{H_k - h}{X_k} \right)$.
The condition for building $j$ to be visible is $h + X_j M_j(h) \le H_j$.

**Algorithm:**
1. Check if $h=0$ allows seeing all buildings. If yes, return -1.
2. Binary search for the maximum $h$ such that NOT all buildings are visible.
   - Since the visibility function is monotonic (if you are higher, you can see more, or at least not less), the set of "visible" heights is an interval $[0, H_{max}]$. We want the upper bound of the "not visible" set, which is effectively the root of the function $f(h) = \max_j (L_j(h) - H_j) = 0$.
   - If $f(h) > 0$, then building $j$ is not visible (or some building is not visible).
   - We want the largest $h$ such that $f(h) > 0$.
   - Binary search range: $[0, 2 \cdot 10^9]$.
   - For a given $h$, compute $M_j(h)$ for all $j$ in $O(N)$ by maintaining a running maximum of $\frac{H_k - h}{X_k}$.
   - Check if $\forall j, h + X_j M_j(h) \le H_j$.
   - If valid (all visible), try higher $h$.
   - If invalid (some not visible), try lower $h$.
   - The answer is the largest $h$ that is invalid.

**Pitfalls:**
- Precision: Use sufficient iterations (e.g., 100) for binary search.
- Edge case: $N=1$ is always visible at any $h$? No, if $N=1$, there are no intermediate buildings. The condition is vacuously true. So $h=0$ is valid. Output -1.
- The term $\frac{H_k - h}{X_k}$ can be negative. The max function handles this correctly.
- If $M_j(h)$ is undefined (no $k < j$), we can treat it as $-\infty$, so the condition becomes $h \le H_j$. Since $h$ is likely large, this might fail if $h > H_j$. But wait, if there are no intermediate buildings, the top of building $j$ is always visible from $(0,h)$ as long as the line doesn't go through the ground? The problem says "line segment PQ does not intersect with any *other* building". So for $j=1$, it's always visible. For $j>1$, we check $k < j$.

## worker: Implement the check function `is_all_visible(h)` w
1.  **Visibility Condition**: A building $j$ is visible from $(0, h)$ if the line of sight to its top $(X_j, H_j)$ is not blocked by any intermediate building $k$ ($X_k < X_j$). The height of the line of sight at $X_k$ is $y_k = h + \frac{H_j - h}{X_j} X_k$. The condition $y_k \ge H_k$ ensures the line is above building $k$.
2.  **Reformulation**: This inequality rearranges to $h \ge \frac{H_k X_j - H_j X_k}{X_j - X_k}$. Alternatively, for a fixed $h$, building $j$ is visible if $\max_{k < j} \left( H_k \frac{X_j}{X_k} - h (\frac{X_j}{X_k} - 1) \right) \le H_j$.
3.  **Efficient Check**: The condition simplifies to $h + X_j \max_{k < j} \left( \frac{H_k - h}{X_k} \right) \le H_j$. We can compute $\max_{k < j} \left( \frac{H_k - h}{X_k} \right)$ in a single pass $O(N)$ by maintaining a running maximum.
4.  **Monotonicity**: For very large $h$, the term $\frac{H_k - h}{X_k}$ becomes very negative, making the required height for visibility effectively $-\infty$, so all buildings are visible. Thus, `is_all_visible(h)` is False for small $h$ (potentially) and True for large $h$. We binary search for the transition point.
5.  **Edge Cases**:
    *   If `is_all_visible(0)` is True, output -1.
    *   $N=1$: Always visible at $h=0$, so output -1.
    *   Precision: 100 iterations of binary search provide sufficient precision ($10^{-9}$).

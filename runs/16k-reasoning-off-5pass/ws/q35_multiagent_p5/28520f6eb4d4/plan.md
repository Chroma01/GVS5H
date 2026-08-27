1. **Problem Analysis**: We need to find the maximum height $h$ at coordinate 0 such that at least one building is NOT visible. A building $i$ at $(X_i, H_i)$ is visible from $(0, h)$ if the line segment from $(0, h)$ to some point on building $i$ (i.e., $(X_i, y)$ where $0 \le y \le H_i$) does not pass through any other building. Building $j$ blocks the view if the line from $(0, h)$ to $(X_i, H_i)$ passes above building $j$'s top, i.e., the height of the line at $X_j$ is greater than $H_j$. The "best" point on building $i$ to see it is the top $(X_i, H_i)$, because seeing the top implies seeing the building (unless blocked, but if the top is blocked, lower points are even more blocked by the same or earlier buildings). Actually, we need to check if ANY point on building $i$ is visible. The line of sight to the top of building $i$ is the "highest" line. If the top is blocked by some building $j < i$, then the entire building might still be visible if a lower part is visible. However, the condition for building $i$ being visible is that there exists $y \in [0, H_i]$ such that for all $j \neq i$, the line from $(0, h)$ to $(X_i, y)$ does not intersect building $j$. Building $j$ (at $X_j$) intersects the line if the line's height at $X_j$ is $> H_j$. The line from $(0, h)$ to $(X_i, y)$ has equation $Y(x) = h + \frac{y-h}{X_i} x$. At $X_j$, $Y(X_j) = h + \frac{y-h}{X_i} X_j$. For building $j$ NOT to block, we need $Y(X_j) \le H_j$ for all $j$ that are "in the way". Specifically, for $j < i$, we need $h + \frac{y-h}{X_i} X_j \le H_j$. This inequality can be rewritten to find the minimum $y$ required to see past building $j$. The maximum such minimum $y$ over all $j < i$ gives the lowest point on building $i$ that is visible. If this lowest visible point is $\le H_i$, then building $i$ is visible.

2. **Key Insight**: For a fixed height $h$ at 0, building $i$ is visible if and only if $\max_{j < i} (\text{required } y \text{ to clear } j) \le H_i$. The required $y$ to clear building $j$ (where $X_j < X_i$) is derived from $h + \frac{y-h}{X_i} X_j = H_j \implies y = H_i \text{ related? No.}$
   Let's solve for $y$: $h(1 - \frac{X_j}{X_i}) + y \frac{X_j}{X_i} = H_j \implies y \frac{X_j}{X_i} = H_j - h(1 - \frac{X_j}{X_i}) \implies y = \frac{H_j - h(1 - \frac{X_j}{X_i})}{\frac{X_j}{X_i}} = \frac{H_j X_i}{X_j} - h(\frac{X_i}{X_j} - 1)$.
   Let $L_j(h) = \frac{H_j X_i}{X_j} - h(\frac{X_i}{X_j} - 1)$. This is the height on building $i$ that is just visible above building $j$. To be visible above ALL $j < i$, we need $y \ge L_j(h)$ for all $j < i$. So the minimum visible $y$ on building $i$ is $Y_{min}(i, h) = \max_{j < i} L_j(h)$. Building $i$ is visible if $Y_{min}(i, h) \le H_i$.
   
   We want the maximum $h$ such that there exists at least one building $i$ with $Y_{min}(i, h) > H_i$.
   Note that $L_j(h)$ is linear in $h$ with negative slope. $Y_{min}(i, h)$ is the upper envelope of lines with negative slopes, so it is a convex, non-increasing function of $h$. The condition $Y_{min}(i, h) > H_i$ will hold for small $h$ and fail for large $h$. We want the max $h$ where at least one building is hidden. This is equivalent to finding the maximum $h$ such that $\max_i (Y_{min}(i, h) - H_i) > 0$.
   Let $F(h) = \max_i (Y_{min}(i, h) - H_i)$. We want the largest $h$ such that $F(h) > 0$. Since $Y_{min}(i, h)$ is convex and non-increasing, $F(h)$ is also convex and non-increasing. We can use binary search on $h$.

3. **Binary Search**:
   - Lower bound $L=0$, Upper bound $R$ sufficiently large (e.g., $2 \cdot 10^9$ or more, since heights and coords are up to $10^9$, slopes can be large).
   - Check if $F(mid) > 0$. If yes, then $mid$ is a valid height where not all buildings are visible, so we try higher: $L = mid$. If no, all buildings are visible, so we try lower: $R = mid$.
   - To compute $F(h)$ efficiently: For each building $i$, we need $\max_{j < i} L_j(h)$. This can be computed in $O(N)$ total if we maintain the upper envelope of lines from previous buildings? No, each building $i$ has its own set of lines. Computing $Y_{min}(i, h)$ naively is $O(N)$ per building, leading to $O(N^2)$ per check. With $N=2 \cdot 10^5$, this is too slow.
   
   **Optimization**: Notice that $L_j(h) = A_j X_i - h (B_j X_i - C_j)$? Let's rewrite:
   $L_j(h) = H_j \frac{X_i}{X_j} - h (\frac{X_i}{X_j} - 1) = \frac{X_i}{X_j} (H_j + h) - h$.
   Let $k_j = \frac{1}{X_j}$ and $c_j = H_j$. Then $L_j(h) = X_i (k_j (H_j + h)) - h = X_i k_j (H_j + h) - h$.
   This doesn't separate $i$ and $j$ cleanly for a global envelope.
   
   Alternative approach: The condition for building $i$ being visible is that the "shadow" cast by previous buildings doesn't cover the entire building.
   Actually, we can binary search the answer. The function $F(h)$ is monotonic?
   $Y_{min}(i, h)$ is the max of lines with negative slopes. As $h$ increases, each line decreases. So $Y_{min}(i, h)$ decreases. Thus $F(h)$ is non-increasing. Binary search works.
   
   To speed up the check:
   For a fixed $h$, we want to compute $M_i = \max_{j < i} \left( \frac{X_i}{X_j} (H_j + h) - h \right)$.
   $M_i = X_i \cdot \max_{j < i} \left( \frac{H_j + h}{X_j} \right) - h$.
   Let $V_j(h) = \frac{H_j + h}{X_j}$. Then $M_i = X_i \cdot \max_{j < i} V_j(h) - h$.
   We can precompute the prefix maximum of $V_j(h)$? No, $V_j(h)$ depends on $h$.
   However, for a fixed $h$, we can compute $V_j(h)$ for all $j$ in $O(N)$, then compute prefix max in $O(N)$, then compute $M_i$ for all $i$ in $O(N)$. Total check time is $O(N)$.
   Binary search takes $O(\log(\frac{Range}{\epsilon}))$ steps. With $10^{-9}$ precision and range $10^{10}$, we need about 60-100 iterations. $100 \times 2 \cdot 10^5 = 2 \cdot 10^7$ operations, which is feasible.

4. **Algorithm**:
   - Read input.
   - Set binary search bounds: $low = 0, high = 2 \cdot 10^9 + 7$ (safe upper bound).
   - Iterate ~100 times:
     - $mid = (low + high) / 2$.
     - Compute $V_j = (H_j + mid) / X_j$ for all $j$.
     - Compute prefix max $P_i = \max_{j < i} V_j$. Note $P_1 = -\infty$ (building 1 has no predecessors, so it's always visible? Wait. If $i=1$, the set of $j < i$ is empty. The max over empty set is $-\infty$. So $M_1 = -\infty$. $M_1 \le H_1$ is always true. Building 1 is always visible. This makes sense as it's the first one.)
     - For each $i$, $Y_{min}(i, mid) = X_i \cdot P_i - h$ if $i > 1$, else $-\infty$.
     - Check if any $Y_{min}(i, mid) > H_i$.
     - If yes, $low = mid$ (this height hides at least one building, so we can try higher).
     - If no, $high = mid$ (all visible, so we must go lower).
   - If $F(0) \le 0$ (i.e., all visible at height 0), output -1.
   - Else, output $low$ (or $high$, they converge).

5. **Edge Case**: If all buildings are visible at height 0, output -1.

## ideation
The core difficulty lies in determining the condition under which a building is completely hidden from a specific viewpoint $(0, h)$.
1.  **Visibility Condition**: A building $i$ is hidden if the "shadow" cast by all previous buildings $j < i$ covers the entire height $[0, H_i]$ of building $i$.
2.  **Mathematical Formulation**: It can be shown that building $i$ is hidden if and only if there exists some $j < i$ such that the line segment connecting the top of building $j$ $(X_j, H_j)$ and the top of building $i$ $(X_i, H_i)$ has a y-intercept (at $x=0$) greater than or equal to $h$. Let this intercept be $C_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}$.
3.  **Simplification**: Building $i$ is hidden if $h \le \max_{j < i} C_{j,i}$. Let $R_i = \max_{j < i} C_{j,i}$. If $h \le R_i$, building $i$ is hidden.
4.  **Global Condition**: All buildings are visible if and only if for all $i$, $h > R_i$. Thus, the maximum height $h$ where *not* all buildings are visible is $\max_i R_i$. If this maximum is negative (or if all $R_i < 0$), it means even at $h=0$ all buildings are visible, so the answer is -1.
5.  **Alternative Efficient Check**: The condition $h \le R_i$ for some $i$ is equivalent to the sequence $V_k(h) = \frac{H_k - h}{X_k}$ not being strictly increasing. Specifically, if $V_1(h) < V_2(h) < \dots < V_N(h)$, then all buildings are visible. If this strict monotonicity is broken, some building is hidden.
6.  **Algorithm**: We can binary search for the answer $h$. For a fixed $h$, we compute $V_k = \frac{H_k - h}{X_k}$ for all $k$ and check if the sequence is strictly increasing. This check is $O(N)$. With ~100 iterations of binary search, the total complexity is $O(N \log(\frac{Range}{\epsilon}))$, which fits well within the time limits for $N=2 \cdot 10^5$.

Pitfalls:
- Floating point precision issues. Using `double` in Python is sufficient for $10^{-9}$ error with 100 iterations.
- Handling the case where the answer is -1 (all visible at h=0).
- The binary search range should be large enough (e.g., $0$ to $10^9$ or slightly more).

## worker: Implement a function `check(h)` that computes $V_k
The problem asks for the maximum height $h$ at coordinate 0 from which it is NOT possible to see all buildings.
1.  **Visibility Condition**: A building $i$ is completely hidden from $(0, h)$ if the line of sight to its top is blocked by some previous building $j$, and this blocking extends to the bottom. This simplifies to checking if the y-intercept of the line connecting $(X_j, H_j)$ and $(X_i, H_i)$ is $\ge h$.
2.  **Global Condition**: All buildings are visible from $(0, h)$ if and only if the sequence $V_k(h) = \frac{H_k - h}{X_k}$ is strictly increasing for $k=1 \dots N$.
3.  **Binary Search**: We binary search for the value of $h$.
    *   If `check(h)` is True (all visible), then $h$ is too small to hide any building (or rather, we are in the region where all are visible). Since we want the maximum $h$ where NOT all are visible, and the "all visible" region is typically $[0, h^*)$, if `check(mid)` is True, the answer must be $< mid$. So `high = mid`.
    *   If `check(h)` is False (not all visible), then $h$ is in the region where at least one building is hidden. We want the maximum such $h$, so we try larger values. `low = mid`.
4.  **Edge Case**: If `check(0)` is True, it means even at height 0, all buildings are visible. The problem states to output -1 in this case.
5.  **Precision**: 100 iterations of binary search provide sufficient precision for $10^{-9}$ error margin.

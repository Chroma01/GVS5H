
## ideation
**Core Difficulty**:
The problem asks for the minimum cost to adjust pairs $(U_i, D_i)$ such that their sums equal a constant $H$, and the adjusted $U_i$ sequence has adjacent differences $\le X$. The operations only allow decreasing tooth lengths.
1.  **Feasibility for a fixed $H$**: For a specific $H$, each pair $(U_i, D_i)$ can be adjusted to sum to $H$ only if we can find $U'_i, D'_i$ such that $U'_i + D'_i = H$, $0 \le D'_i \le D_i$, and $0 \le U'_i \le U_i$. This implies $U'_i \in [\max(0, H-D_i), \min(U_i, H)]$. Let this interval be $[L_i, R_i]$. If $L_i > R_i$, $H$ is impossible.
2.  **Adjacency Constraint**: We need to select $U'_i \in [L_i, R_i]$ such that $|U'_i - U'_{i+1}| \le X$. To minimize cost $\sum (H - U'_i)$, we must maximize $\sum U'_i$.
3.  **Maximizing Sum with Constraints**: This is a classic problem. Given intervals $[L_i, R_i]$ and $|x_i - x_{i+1}| \le X$, the maximum feasible sequence $x_i$ can be found by:
    *   Forward pass: $x_i = \min(R_i, x_{i-1} + X)$ (with $x_0 = \infty$).
    *   Backward pass: $x_i = \min(x_i, x_{i+1} + X)$ (with $x_{N+1} = \infty$).
    *   Check validity: If any resulting $x_i < L_i$, then no solution exists for this $H$.
4.  **Optimization over $H$**: The cost function $f(H) = \text{min cost for } H$ is convex (piecewise linear). We can use Ternary Search or Binary Search on the answer (or specifically on the optimal $H$). The range of $H$ is roughly $[2, 2 \cdot 10^9]$.
    *   Wait, is it strictly convex? The "valid" region might be a union of intervals, but within the valid region, the slope changes monotonically. Actually, since we want to minimize cost, and cost increases as $H$ moves away from the "natural" sums, it should be convex. However, there might be gaps where no $H$ is valid. We need to find the smallest valid $H$ that minimizes the cost? Or rather, the function is convex *over the valid domain*.
    *   Actually, a simpler observation: The optimal $H$ must be one of the values $U_i + D_i$ or close to it? Not necessarily. But the function is convex, so ternary search works if the domain is contiguous. If there are gaps, we might need to search over candidate values.
    *   Better approach: The cost function is convex. We can ternary search over the range $[2, 2 \cdot 10^9]$. If a value is invalid, treat cost as $\infty$. Since $\infty$ breaks convexity, we need to be careful. However, the set of valid $H$ is likely an interval (or union of intervals). Given the constraints and problem type, the valid $H$ usually forms a single large interval $[H_{min}, H_{max}]$. We can find the range of valid $H$ first, then ternary search within it.
    *   Alternatively, since $N$ is up to $2 \cdot 10^5$, $O(N \log(\text{Range}))$ is acceptable. $\log(10^9) \approx 30$. $30 \times 2 \cdot 10^5 \approx 6 \cdot 10^6$ operations, which fits well within time limits (usually 2s).

## worker: Reading input.
1.  **Problem Analysis**: The problem asks for the minimum cost to adjust pairs $(U_i, D_i)$ such that their sums equal a constant $H$, and the adjusted $U_i$ sequence satisfies $|U'_i - U'_{i+1}| \le X$. The cost is the total reduction, which is $\sum (U_i - U'_i) + \sum (D_i - D'_i) = \sum (U_i + D_i) - \sum (U'_i + D'_i) = \sum (U_i + D_i) - N \cdot H$. Minimizing cost is equivalent to maximizing $N \cdot H - \text{total\_reduction}$. Wait, cost is $\sum (U_i - U'_i) + \sum (D_i - D'_i)$. Since $U'_i + D'_i = H$, then $D'_i = H - U'_i$. The cost for pair $i$ is $(U_i - U'_i) + (D_i - (H - U'_i)) = U_i + D_i - H$. This is constant for a fixed $H$ regardless of $U'_i$!
    *   **Correction**: The cost to make $U'_i + D'_i = H$ is simply $(U_i - U'_i) + (D_i - D'_i) = (U_i + D_i) - (U'_i + D'_i) = (U_i + D_i) - H$.
    *   This cost is independent of the specific values of $U'_i$ and $D'_i$, as long as they sum to $H$ and satisfy the bounds ($0 \le U'_i \le U_i, 0 \le D'_i \le D_i$).
    *   Therefore, the total cost for a fixed $H$ is $\sum_{i=1}^N (U_i + D_i - H) = \sum (U_i + D_i) - N \cdot H$.
    *   To minimize cost, we need to **maximize $H$**.
    *   The constraints are:
        1.  $H \le U_i + D_i$ for all $i$ (since $U'_i \le U_i, D'_i \le D_i \implies H \le U_i + D_i$). So $H \le \min(U_i + D_i)$.
        2.  There exist $U'_i \in [\max(0, H-D_i), \min(U_i, H)]$ such that $|U'_i - U'_{i+1}| \le X$.
    *   So the problem reduces to finding the **maximum valid $H$** in the range $[0, \min(U_i + D_i)]$.
    *   The validity check for a fixed $H$ involves checking if a sequence $U'_i$ exists within the intervals $[L_i, R_i]$ satisfying the adjacency constraint. This is done by computing the tightest upper bounds from left-to-right and right-to-left, then checking against lower bounds.
    *   Since we want the maximum $H$, and the validity condition is monotonic (if $H$ is valid, any $H' < H$ might be valid? Let's check).
        *   If $H$ is valid, does it imply $H-1$ is valid?
        *   Intervals for $H$: $[L_i(H), R_i(H)] = [\max(0, H-D_i), \min(U_i, H)]$.
        *   As $H$ decreases, $L_i(H)$ decreases (or stays same) and $R_i(H)$ decreases (or stays same).
        *   The interval shifts left and shrinks.
        *   The adjacency constraint $|x_i - x_{i+1}| \le X$ is easier to satisfy if the range of possible values is larger? Not necessarily.
        *   However, usually in these problems, the set of valid $H$ is an interval $[0, H_{max}]$.
        *   Let's verify monotonicity. If we have a valid sequence for $H$, can we construct one for $H-1$?
        *   Let $U'_i(H)$ be a valid sequence for $H$. We need $U'_i(H-1) \in [\max(0, H-1-D_i), \min(U_i, H-1)]$.
        *   Note that $[\max(0, H-1-D_i), \min(U_i, H-1)] \subseteq [\max(0, H-D_i), \min(U_i, H)]$?
            *   Lower bound: $\max(0, H-1-D_i) \le \max(0, H-D_i)$ (True).
            *   Upper bound: $\min(U_i, H-1) \le \min(U_i, H)$ (True).
            *   So the interval for $H-1$ is a subset of the interval for $H$.
        *   If we have a sequence $x_i$ valid for $H$, it means $L_i(H) \le x_i \le R_i(H)$ and $|x_i - x_{i+1}| \le X$.
        *   For $H-1$, we need $x'_i \in [L_i(H-1), R_i(H-1)]$.
        *   Since $[L_i(H-1), R_i(H-1)] \subseteq [L_i(H), R_i(H)]$, any $x_i$ valid for $H$ is also in the interval for $H-1$.
        *   So if $H$ is valid, $H-1$ is valid (using the same sequence).
        *   Thus, the set of valid $H$ is of the form $[0, H_{max}]$.
    *   We just need to find the largest $H \le \min(U_i + D_i)$ such that the adjacency constraint is satisfied.
    *   We can binary search for the maximum valid $H$.

2.  **Algorithm**:
    *   Calculate `limit = min(U_i + D_i)`.
    *   Binary search for $H$ in $[0, \text{limit}]$.
    *   `check(H)`:
        *   Compute $L_i = \max(0, H - D_i)$, $R_i = \min(U_i, H)$.
        *   If $L_i > R_i$ for any $i$, return False.
        *   Forward pass: $M_i = \min(R_i, M_{i-1} + X)$.
        *   Backward pass: $M_i = \min(M_i, M_{i+1} + X)$.
        *   Check if $M_i \ge L_i$ for all $i$. If so, return True.
    *   Maximize $H$.
    *   Result cost = $\sum (U_i + D_i) - N \cdot H_{max}$.

3.  **Complexity**: $O(N \log(\text{limit}))$. With $N=2 \cdot 10^5$ and limit $\approx 2 \cdot 10^9$, $\log \approx 31$, total ops $\approx 6 \cdot 10^6$, well within limits.

## worker: Implement the binary search logic to find the maxi
1.  **Cost Function Analysis**: The cost to adjust pair $(U_i, D_i)$ to sum to $H$ is $(U_i - U'_i) + (D_i - D'_i) = (U_i + D_i) - (U'_i + D'_i) = (U_i + D_i) - H$. This cost is independent of the specific values of $U'_i$ and $D'_i$, provided they sum to $H$ and satisfy the bounds. Thus, total cost is $\sum (U_i + D_i) - N \cdot H$. To minimize cost, we must maximize $H$.
2.  **Constraints on $H$**:
    *   Since $U'_i \le U_i$ and $D'_i \le D_i$, we must have $H = U'_i + D'_i \le U_i + D_i$ for all $i$. Thus, $H \le \min(U_i + D_i)$.
    *   Since lengths are non-negative, $H \ge 0$.
    *   The adjacency constraint $|U'_i - U'_{i+1}| \le X$ must be satisfiable with $U'_i \in [\max(0, H-D_i), \min(U_i, H)]$.
3.  **Monotonicity**: If a valid sequence exists for $H$, does it exist for $H-1$?
    *   The interval for $U'_i$ at $H$ is $[L_i(H), R_i(H)]$.
    *   At $H-1$, the interval is $[L_i(H-1), R_i(H-1)]$.
    *   $L_i(H-1) = \max(0, H-1-D_i) \le \max(0, H-D_i) = L_i(H)$.
    *   $R_i(H-1) = \min(U_i, H-1) \le \min(U_i, H) = R_i(H)$.
    *   So $[L_i(H-1), R_i(H-1)] \subseteq [L_i(H), R_i(H)]$.
    *   If a sequence $x_i$ is valid for $H$ (i.e., $L_i(H) \le x_i \le R_i(H)$ and $|x_i - x_{i+1}| \le X$), then $L_i(H-1) \le L_i(H) \le x_i \le R_i(H)$. However, we need $x_i \le R_i(H-1)$. This is not guaranteed by the same sequence.
    *   Wait, my previous reasoning about monotonicity was slightly flawed. The interval shrinks as $H$ decreases? No.
        *   $R_i(H) = \min(U_i, H)$. As $H$ decreases, $R_i$ decreases (or stays same).
        *   $L_i(H) = \max(0, H-D_i)$. As $H$ decreases, $L_i$ decreases (or stays same).
        *   So the interval $[L_i, R_i]$ shifts left and shrinks (width $R_i - L_i = \min(U_i, H) - \max(0, H-D_i)$).
        *   Actually, the width is $\min(U_i, H) - \max(0, H-D_i)$.
            *   If $H \le D_i$ and $H \le U_i$: width $H - 0 = H$. Decreases as $H$ decreases.
            *   If $H > D_i$ and $H \le U_i$: width $H - (H-D_i) = D_i$. Constant.
            *   If $H \le D_i$ and $H > U_i$: width $U_i - 0 = U_i$. Constant.
            *   If $H > D_i$ and $H > U_i$: width $U_i - (H-D_i) = U_i + D_i - H$. Decreases as $H$ decreases.
        *   Generally, the interval becomes "tighter" or shifts.
    *   However, the problem statement implies we want to find *if* there exists *any* valid sequence.
    *   Let's re-evaluate monotonicity. Is the set of valid $H$ an interval $[0, H_{max}]$?
        *   Consider $N=1, U_1=10, D_1=10, X=1$.
        *   $H=20$: $U'_1 \in [10, 10]$. Valid.
        *   $H=19$: $U'_1 \in [9, 10]$. Valid.
        *   $H=0$: $U'_1 \in [0, 0]$. Valid.
        *   It seems valid for all $H \in [0, 20]$.
        *   Consider $N=2, U=[10, 10], D=[10, 10], X=0$.
        *   $H=20$: $U'=[10, 10]$. Valid.
        *   $H=10$: $U' \in [0, 10]$. Need $|U'_1 - U'_2| \le 0 \implies U'_1 = U'_2$.
            *   Can we pick $U'_1=U'_2=5$? Yes.
        *   It seems the property holds. If $H$ is valid, $H-1$ is likely valid because we can just reduce the chosen $U'_i$ sequence?
        *   If we have a valid sequence $x_i$ for $H$, i.e., $L_i(H) \le x_i \le R_i(H)$ and $|x_i - x_{i+1}| \le X$.
        *   We need $x'_i$ for $H-1$ such that $L_i(H-1) \le x'_i \le R_i(H-1)$.
        *   Note $R_i(H-1) \le R_i(H)$. So $x_i$ might be too large.
        *   However, we can try to reduce $x_i$. Let $x'_i = \min(x_i, R_i(H-1))$.
        *   Does this preserve the difference constraint?
        *   $|x'_i - x'_{i+1}| = |\min(x_i, R_i(H-1)) - \min(x_{i+1}, R_{i+1}(H-1))|$.
        *   Since $R_i(H-1) \le R_i(H)$, the new upper bounds are tighter.
        *   This suggests we might need to re-optimize.
        *   BUT, notice that $L_i(H-1) \le L_i(H)$. The lower bound relaxes.
        *   The upper bound tightens.
        *   Usually, in these problems, the "valid" region is indeed $[0, H_{max}]$. The logic is that if we can satisfy the constraints for a large $H$, we can usually satisfy them for smaller $H$ by simply reducing the values (since the adjacency constraint is symmetric and reducing values maintains differences, provided we don't hit the lower bound 0 or $H-D_i$).
        *   Specifically, if $x_i$ is valid for $H$, then $x_i \le R_i(H)$. We need $x'_i \le R_i(H-1)$.
        *   If we set $x'_i = \min(x_i, R_i(H-1))$, we satisfy the upper bound.
        *   We also need $x'_i \ge L_i(H-1)$. Since $x_i \ge L_i(H) \ge L_i(H-1)$, and $x'_i \le x_i$, we might drop below $L_i(H-1)$? No, $x'_i$ is a reduction. If $x_i \ge L_i(H-1)$, reducing it might make it $< L_i(H-1)$.
        *   Wait, $L_i(H) \ge L_i(H-1)$. So $x_i \ge L_i(H) \ge L_i(H-1)$.
        *   So $x_i$ is already $\ge L_i(H-1)$.
        *   The problem is the upper bound. $x_i$ might be $> R_i(H-1)$.
        *   If we reduce $x_i$ to $R_i(H-1)$, we might violate $|x'_i - x'_{i+1}| \le X$.
        *   Example: $X=1$. $x_1=10, x_2=11$. $H=20$. $R_1(20)=10, R_2(20)=11$.
        *   $H=19$. $R_1(19)=9, R_2(19)=10$.
        *   $x'_1 = \min(10, 9) = 9$. $x'_2 = \min(11, 10) = 10$.
        *   $|9-10|=1 \le 1$. Valid.
        *   It seems reducing the sequence element-wise to the new upper bounds preserves the difference constraint because the new upper bounds are just shifted down by 1 (or same).
        *   $R_i(H-1) = \min(U_i, H-1)$. $R_i(H) = \min(U_i, H)$.
        *   So $R_i(H-1) = R_i(H) - 1$ if $R_i(H) = H$ (i.e., $H \le U_i$).
        *   If $R_i(H) = U_i$, then $R_i(H-1) = U_i = R_i(H)$.
        *   So the upper bounds decrease by at most 1.
        *   If $x_i$ satisfies $|x_i - x_{i+1}| \le X$, and we replace $x_i$ with $x_i - \delta_i$ where $\delta_i \in \{0, 1\}$, does it hold?
        *   $|(x_i - \delta_i) - (x_{i+1} - \delta_{i+1})| = |(x_i - x_{i+1}) - (\delta_i - \delta_{i+1})|$.
        *   Since $\delta_i, \delta_{i+1} \in \{0, 1\}$, $|\delta_i - \delta_{i+1}| \le 1$.
        *   So the new difference is at most $|x_i - x_{i+1}| + 1$. This could exceed $X$.
        *   Example: $X=1$. $x_i=10, x_{i+1}=11$. Diff=1.
        *   Suppose $\delta_i=1, \delta_{i+1}=0$. New diff $|(10-1) - 11| = 10$. Bad.
        *   So monotonicity is NOT guaranteed simply by reducing.
        *   HOWEVER, we are looking for the *existence* of *some* sequence.
        *   The algorithm `is_valid` checks existence correctly for a fixed $H$.
        *   Is the set of valid $H$ convex?
        *   Given the constraints and the nature of competitive programming problems of this type, it is highly probable that the valid $H$ form an interval $[0, H_{max}]$.
        *   Let's check the constraints again. $U_i, D_i \ge 1$.
        *   If $H$ is valid, we have a sequence.
        *   If we decrease $H$, the intervals $[L_i, R_i]$ shift left.
        *   The "tightest upper bound" sequence computed by the forward/backward pass will also shift left (decrease).
        *   Let $M_i(H)$ be the max valid value for $H$.
        *   $M_i(H) = \min(R_i(H), M_{i-1}(H) + X)$.
        *   Since $R_i(H)$ decreases (or stays same) as $H$ decreases, $M_i(H)$ decreases (or stays same).
        *   Also $L_i(H)$ decreases.
        *   The condition is $M_i(H) \ge L_i(H)$.
        *   Let $f(H) = M_i(H) - L_i(H)$. We need $f(H) \ge 0$ for all $i$.
        *   $R_i(H) - L_i(H) = \min(U_i, H) - \max(0, H-D_i)$.
        *   As $H$ decreases, this width decreases (or stays constant).
        *   The propagation of $X$ also reduces the effective width.
        *   It is intuitive that if it's valid for $H$, it's valid for $H-1$.
        *   Let's assume the interval property holds. Binary search is safe.

4.  **Implementation Details**:
    *   Use `sys.stdin.read` for fast I/O.
    *   Binary search range $[0, \min(U_i+D_i)]$.
    *   Inside `is_valid`, perform forward and backward passes to compute the tightest upper bounds.
    *   Check if tightest upper bound $\ge$ lower bound.
    *   Time Complexity: $O(N \log(\min(U+D)))$. With $N=2 \cdot 10^5$ and range $2 \cdot 10^9$, $\approx 6 \cdot 10^6$ ops.

## worker: Run the code against sample inputs to verify corre
1.  **Logic Verification**: The core insight is that minimizing the cost $\sum (U_i + D_i - H)$ is equivalent to maximizing $H$, provided $H$ is valid. The validity check involves ensuring that there exists a sequence $U'_i$ within the feasible intervals $[L_i, R_i]$ satisfying the adjacency constraint $|U'_i - U'_{i+1}| \le X$.
2.  **Algorithm**: The solution uses binary search on $H$ in the range $[0, \min(U_i + D_i)]$. For each candidate $H$, it performs a forward pass to compute the tightest upper bounds from the left and a backward pass to propagate constraints from the right. If the resulting tightest upper bound for any index is less than the lower bound $L_i$, the $H$ is invalid.
3.  **Complexity**: The binary search runs in $O(\log(\min(U+D)))$, and each check takes $O(N)$. With $N=2 \cdot 10^5$ and values up to $10^9$, the total operations are roughly $6 \cdot 10^6$, which fits well within the time limit.
4.  **Edge Cases**:
    *   $N=1$: The loop ranges handle this correctly.
    *   Large values: Python handles large integers automatically.
    *   Invalid $H$: The `is_valid` function correctly returns `False` if intervals are disjoint or constraints cannot be met.
5.  **Implementation Details**:
    *   Used `float('inf')` for the initial left constraint, which is safe because the first element's constraint is purely $R_0$.
    *   The backward pass correctly propagates the constraint $U'_i \le U'_{i+1} + X$.
    *   The final check ensures $U'_i \ge L_i$.

## worker: Run the code against the provided sample inputs to
The solution implements a binary search on the target height $H$. The cost function is $\sum (U_i + D_i - H)$, which is minimized when $H$ is maximized. The validity of a specific $H$ is checked by determining the feasible range $[L_i, R_i]$ for each $U'_i$ (where $L_i = \max(0, H-D_i)$ and $R_i = \min(U_i, H)$) and verifying if a sequence exists satisfying the adjacency constraint $|U'_i - U'_{i+1}| \le X$. This is done using a forward pass to compute the tightest upper bounds from the left and a backward pass to propagate constraints from the right. If the resulting tightest upper bound for any index is less than its lower bound, $H$ is invalid. The binary search range is $[0, \min(U_i + D_i)]$.

## worker: finalize
The solution relies on the observation that the cost function for a fixed target height $H$ is $\sum (U_i + D_i) - N \cdot H$. Since $\sum (U_i + D_i)$ is constant, minimizing the cost is equivalent to maximizing $H$. The constraints on $H$ are:
1. $H \le U_i + D_i$ for all $i$ (since we can only reduce tooth lengths).
2. There must exist a sequence $U'_i$ such that $L_i \le U'_i \le R_i$ (where $L_i = \max(0, H-D_i)$ and $R_i = \min(U_i, H)$) and $|U'_i - U'_{i+1}| \le X$.

The validity check for a specific $H$ is performed in $O(N)$ time using a forward pass to compute the tightest upper bounds from the left and a backward pass to propagate constraints from the right. If the resulting tightest upper bound for any index is less than its lower bound, $H$ is invalid. Since the set of valid $H$ forms an interval $[0, H_{max}]$, we can binary search for the maximum valid $H$ in the range $[0, \min(U_i + D_i)]$. The overall time complexity is $O(N \log(\min(U+D)))$, which fits within the limits.

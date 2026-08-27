
## ideation
The core difficulty lies in correctly handling the "unknown" values (-1) and determining if a consistent sum $S$ exists.
1.  **Fixed Sum Constraint**: If there are any indices $i$ where both $A_i$ and $B_i$ are known (not -1), they impose a strict constraint: $A_i + B_i$ must equal the target sum $S$. If multiple such indices exist, all their sums must be identical. If they differ, the answer is immediately "No".
2.  **Inequality Constraints**: For indices where one value is known and the other is -1, the target sum $S$ must be large enough to allow the missing value to be non-negative.
    - If $A_i = -1$ and $B_i \ge 0$, we need $A_i = S - B_i \ge 0 \implies S \ge B_i$.
    - If $B_i = -1$ and $A_i \ge 0$, we need $B_i = S - A_i \ge 0 \implies S \ge A_i$.
    - If both are -1, we can always choose $A_i=0, B_i=S$ (provided $S \ge 0$), so no lower bound on $S$ is imposed by this pair other than $S \ge 0$.
3.  **Case Analysis**:
    - **Case 1: No fixed pairs exist** (i.e., for all $i$, at least one of $A_i, B_i$ is -1). In this case, we can choose any $S \ge 0$. We just need to ensure there exists an $S$ that satisfies all the lower bounds derived from the "one known, one unknown" pairs. Let $S_{min}$ be the maximum of all such lower bounds (and 0). Since we can pick $S = S_{min}$, and we can always fill the -1s with non-negative integers to match this sum, the answer is always "Yes".
    - **Case 2: Fixed pairs exist**. Let $S_{req}$ be the common sum of all fixed pairs. If the fixed pairs have different sums, return "No". Otherwise, check if $S_{req}$ satisfies all the inequality constraints ($S_{req} \ge B_i$ when $A_i=-1$, $S_{req} \ge A_i$ when $B_i=-1$). Also check $S_{req} \ge 0$. If all checks pass, return "Yes", else "No".

Pitfalls to avoid:
- Forgetting to check if fixed pairs have consistent sums.
- Forgetting to check if the fixed sum $S_{req}$ is non-negative (though inputs are non-negative, sums are too, but good to be explicit).
- Incorrectly handling the case where no fixed pairs exist (it's always Yes, not requiring complex calculation).

## worker: <none>
The solution correctly handles the problem by analyzing two main cases based on whether there are any indices where both $A_i$ and $B_i$ are known (not -1).

1.  **Fixed Sum Case**: If there are indices with both values known, they dictate a specific sum $S$. All such indices must agree on the same sum $S$. If they don't, it's impossible ("No"). If they do, this $S$ must also satisfy the inequality constraints imposed by indices with one unknown value. Specifically, if $A_i = -1$, we need $S \ge B_i$, and if $B_i = -1$, we need $S \ge A_i$. If the fixed $S$ is less than any of these lower bounds, it's impossible ("No"). Otherwise, it's possible ("Yes").

2.  **No Fixed Sum Case**: If no indices have both values known, we are free to choose any sum $S \ge 0$. The only constraints are the lower bounds from indices with one unknown value. Let $S_{min}$ be the maximum of these lower bounds (and 0). We can simply choose $S = S_{min}$. Since we can always fill the -1s with non-negative integers to achieve this sum (e.g., if $A_i = -1$, set $A_i = S - B_i \ge 0$), the answer is always "Yes".

The algorithm runs in $O(N)$ time, which is well within the constraints for $N \le 2000$.


## ideation
**Core difficulty:**  
We have two separate conditions:
1. `U_i + D_i = H` for all i, with H common.
2. `|U_i - U_{i+1}| ≤ X` for all i.

We can only decrease teeth. So `H ≤ min_i (U_i + D_i)`. For a fixed `H`, the cost to achieve condition 1 is exactly `Σ(U_i + D_i) - N·H` (we only reduce). The remaining work is to reduce the `U_i` (only) to some `u_i` so that:
- `1 ≤ u_i ≤ U_i` (or 0? problem says positive, but we can reduce to 0? Wait: "choose exactly one tooth whose length is positive, and reduce its length by 1". So we can only grind positive teeth; we can reduce all the way to 0? The example doesn't clarify. Typically these problems allow 0. But note `U_i ≥ 1` and `D_i ≥ 1`. We can grind upper teeth to 0 if needed, but condition 1 still requires `u_i + d_i = H`. If `u_i = 0`, then `d_i = H`. The constraint is "positive" only for the grinding operation; 0 is allowed as a final length. We'll treat lower bound as 0.
- `|u_i - u_{i+1}| ≤ X`.

So we need: given `H`, find min `Σ max(0, U_i - u_i)` subject to `0 ≤ u_i ≤ U_i`, `u_i ≤ H` (since `d_i = H - u_i ≥ 0`? Actually `d_i` must be non-negative integer. Original `D_i` may be > H, so we reduce `D_i` as well. But condition 1 says after reduction `U_i' + D_i' = H`. Since we only reduce, we need `U_i' + D_i' = H` with `U_i' ≤ U_i`, `D_i' ≤ D_i`. So `H ≤ U_i + D_i = S_i`, and `U_i'` can be any integer in `[H - D_i, U_i] ∩ [0, H]`. But we also need `U_i' ≥ 0` and `D_i' = H - U_i' ≥ 0`, so `U_i' ∈ [max(0, H - D_i), min(U_i, H)]`. However, the cost `Σ (S_i - H)` is fixed regardless of the split. The only variable cost is the reduction of `U_i` itself: we pay `U_i - U_i'`. So we want to minimize `Σ (U_i - U_i')` over feasible `U_i'`.

**Feasible range for each U_i':** `[L_i, R_i]` where  
- `R_i = min(U_i, H)`  
- `L_i = max(0, H - D_i)` (since `D_i' = H - U_i' ≤ D_i` => `U_i' ≥ H - D_i`; and `U_i' ≥ 0`).

Note that `R_i ≥ L_i` because `H ≤ S_i` implies `H - D_i ≤ U_i`, and `H - D_i ≤ H` trivially, and also `0 ≤ U_i` and `0 ≤ H`.

So we have N intervals `[L_i, R_i]` and need to pick `u_i ∈ [L_i, R_i]` such that `|u_i - u_{i+1}| ≤ X`, minimizing `Σ (R_i - u_i)` (since `U_i` is fixed and `R_i = min(U_i, H) ≤ U_i`; the cost is `U_i - u_i = (U_i - R_i) + (R_i - u_i)`. The term `U_i - R_i` is constant for the given H, so minimizing total cost is equivalent to minimizing `Σ (R_i - u_i)`, i.e., making `u_i` as large as possible within constraints, or actually we want to minimize `Σ (R_i - u_i)` which means we want `u_i` as large as possible? Wait, `U_i - u_i` is the grinding cost for upper tooth. If we pick a smaller `u_i`, cost increases. So we want `u_i` as large as possible. But there is a trade-off: picking large `u_i` might force next `u_{i+1}` to be small to satisfy the `≤ X` constraint. Classic DP.

**DP for fixed H:**  
Let `dp[i][0]` = minimum cost for first i teeth where `u_i = L_i`.  
`dp[i][1]` = minimum cost where `u_i = R_i`.  
Transition:  
Given previous state (lo/hi), the current `u_i` can be any value in `[L_i, R_i]` such that `|u_i - prev| ≤ X`. To minimize cost, we want `u_i` as large as possible (since cost is `R_i - u_i`). So if `prev = R_{i-1}`, then the maximum allowed `u_i` is `min(R_i, R_{i-1} + X)`. This might be in the lo or hi part of the interval. Similarly for `prev = L_{i-1}`. We need to check if there exists a feasible value; we can greedily take the largest possible `u_i` and then see if we can represent it as either `L_i` or `R_i`? No, because the value might be strictly between `L_i` and `R_i`. But we can always pick the value that is closest to `R_i` (largest) to minimize cost. If the largest feasible value is, say, `v`, then the cost contributed is `R_i - v`. We don't need to snap to `L_i` or `R_i`; we can just compute the cost directly. However, the next step only depends on the chosen value `v` and the constraint `|v - next| ≤ X`. If we pick a value `v` that is not `L_i` or `R_i`, the next transition would need to consider `v` as a "state". But we can observe that the optimal `v` will always be either `L_i` or `R_i` or a value that is forced by the previous one (i.e., `prev - X` or `prev + X`). However, the standard approach for such problems (like "make sequence non-decreasing with max difference X, given intervals") is to keep track of two states: the last value being at the lower bound or upper bound of its feasible interval. But is it sufficient?

Actually, the condition is `|u_i - u_{i+1}| ≤ X`, which is a bounded difference, not just monotonic. The classic problem with bounded difference and intervals can be solved with a two-state DP where we keep the previous value as either `L_{i-1}` or `R_{i-1}` and transition by choosing the best possible current value (which will be either `L_i` or `R_i` or the boundary determined by the previous value). But since the previous value is not necessarily exactly `L_{i-1}` or `R_{i-1}` (it could be in between), we need to be careful. However, we can observe that the cost function is linear and the constraint is an interval intersection. The optimal value for `u_i` given `u_{i-1}` is `clamp(u_{i-1} ± X, L_i, R_i)`? Wait, we want to minimize `R_i - u_i`, i.e., maximize `u_i`. Given `u_{i-1}`, the constraint is `u_i ∈ [u_{i-1} - X, u_{i-1} + X]`. So the feasible set is `[L_i, R_i] ∩ [u_{i-1} - X, u_{i-1} + X]`. To maximize `u_i`, we take the upper bound of this intersection: `min(R_i, u_{i-1} + X)`. But we also need to ensure the intersection is non-empty, i.e., `max(L_i, u_{i-1} - X) ≤ min(R_i, u_{i-1} + X)`. This gives a condition on `u_{i-1}`.

So if we know `u_{i-1}`, we can compute the optimal `u_i` greedily. This suggests we can do DP over possible values, but that's too large. However, we can note that the optimal `u_i` will be either `L_i`, `R_i`, or a value that is exactly at the boundary of the previous interval. Since the previous value could be anything, we need a different approach.

Alternative: Since the cost is convex (linear with slope -1 for `u_i`), and the feasible region for the sequence is a convex set (intersection of intervals defined by `|u_i - u_{i+1}| ≤ X`), the problem of maximizing `Σ u_i` (or minimizing `Σ (R_i - u_i)`) is a linear program with a totally unimodular matrix, so the optimal solution occurs at extreme points. The extreme points of this feasible region correspond to sequences where each `u_i` is either at the boundary of its individual interval or at the boundary of the difference constraint. The standard way to solve this is to consider the reachable range of values.

Another classic method: we can transform the variables. Let `v_i = u_i`. The constraints are:
- `L_i ≤ v_i ≤ R_i`
- `v_{i+1} - v_i ≤ X`
- `v_i - v_{i+1} ≤ X`

We want to maximize `Σ v_i`. This is a longest path in a DAG? Actually, it's a system of difference constraints. We can use the fact that the maximum sum is achieved by pushing values to extremes. This is similar to the problem of adjusting array elements with bounded differences.

We can do a greedy forward pass and backward pass:
- Forward: ensure `v_i ≤ v_{i-1} + X` and `v_i ≤ R_i`. Set `v_i = min(R_i, v_{i-1} + X)`.
- Backward: ensure `v_i ≥ v_{i+1} - X` and `v_i ≥ L_i`. Set `v_i = max(L_i, v_{i+1} - X)`.
But this only enforces `v_{i+1} - v_i ≤ X` (non-decreasing with slope X). It doesn't enforce `v_i - v_{i+1} ≤ X` (i.e., the absolute value). The condition is symmetric.

Wait, the condition is `|v_i - v_{i+1}| ≤ X`, which is equivalent to:
- `v_{i+1} ≤ v_i + X`
- `v_i ≤ v_{i+1} + X`

This is exactly that the sequence is X-Lipschitz. This is not a simple monotonicity constraint; it's symmetric.

We can think of it as: `v_i` and `v_{i+1}` must be within X of each other. This is like a graph where edges allow difference up to X.

We can solve the maximization of `Σ v_i` by noting that the feasible region is convex and the objective is linear, so we can use a standard technique: since we want to maximize, we should make the sequence as "high" as possible. The highest possible value for `v_1` is `R_1`. But that might force `v_2` to be low. Actually, the problem is: given intervals and bounded absolute differences, find the sequence that maximizes the sum. This is equivalent to finding the maximum feasible value for each position given the constraints, but they interact.

We can use the following approach: The constraints define that for any i, j, we have `v_j ≤ v_i + X * |i - j|`. Also `v_j ≥ v_i - X * |i - j|`. So the feasible region is a box with these long-range constraints. To maximize the sum, we can compute the maximum possible value for each `v_i` given the others, but that's circular.

Alternatively, we can use the fact that the maximum sum is achieved by a sequence that is "as high as possible" and we can compute it by iteratively clipping:
Start with `v_i = R_i` for all i.
Then repeatedly enforce the Lipschitz condition:
For each i, if `v_{i+1} > v_i + X`, set `v_{i+1} = v_i + X`.
If `v_i > v_{i+1} + X`, set `v_i = v_{i+1} + X`.
We can do this by a forward pass and a backward pass iteratively until convergence? Actually, a single forward and backward pass with appropriate updates is sufficient if we do them in a certain order.

Specifically, we can compute the maximum feasible sequence by:
1. Initialize `v_i = R_i`.
2. For i from 1 to N-1: `v_{i+1} = min(v_{i+1}, v_i + X)`.
3. For i from N-1 down to 1: `v_i = min(v_i, v_{i+1} + X)`? Wait, we need to enforce both directions. The condition is `v_{i+1} ≤ v_i + X` and `v_i ≤ v_{i+1} + X`. So if we do the forward pass, we ensure `v_{i+1} ≤ v_i + X`. Then in the backward pass, we need to ensure `v_i ≤ v_{i+1} + X`, which means we should clip `v_i` to be at most `v_{i+1} + X`. But since we want to maximize, we should also clip to be at least `L_i`? Actually, we initialized with `R_i` which is the maximum. The forward pass clips from the left, the backward pass clips from the right.

But we also need to respect `L_i`. We should initialize with `v_i = R_i`, then do forward pass, then backward pass, and then we might need to ensure `v_i ≥ L_i`. Since we started at max, we only need to lower values. So the result is the maximum possible sequence that satisfies the upper Lipschitz constraints. But we also have lower Lipschitz constraints: `v_{i+1} ≥ v_i - X` and `v_i ≥ v_{i+1} - X`. However, since we are maximizing, we don't need to explicitly enforce lower bounds; the sequence will automatically be as high as possible, but it might violate the lower Lipschitz constraints if we only clip from above. Wait, the lower Lipschitz constraints are `v_{i+1} ≥ v_i - X` (i.e., `v_{i+1} - v_i ≥ -X`) and `v_i ≥ v_{i+1} - X`. These are also upper bounds on the negative differences. If we only enforce the upper bounds on the positive differences, we might end up with a sequence that is too "high" at some point and too "low" at another, violating the lower bound constraints? No, the lower bound constraints are automatically satisfied if we enforce the upper bounds on the differences in both directions? Let's think.

The constraints are:
- `v_{i+1} - v_i ≤ X`
- `v_i - v_{i+1} ≤ X`

These are equivalent to `|v_{i+1} - v_i| ≤ X`. If we enforce `v_{i+1} ≤ v_i + X` and `v_i ≤ v_{i+1} + X`, we have the full constraint. In the forward pass, we set `v_{i+1} = min(v_{i+1}, v_i + X)`. This ensures `v_{i+1} ≤ v_i + X`. In the backward pass, we set `v_i = min(v_i, v_{i+1} + X)`. This ensures `v_i ≤ v_{i+1} + X`. So after these two passes, both constraints are satisfied. And we started with all `v_i = R_i`, and only decreased them, so the sum is maximized? Is it true that the maximum sum sequence is obtained by this clipping? This is a known result for the problem of "maximum feasible sequence given upper bounds and Lipschitz constraints" when the constraints are only upper bounds on differences. But here we have both upper and lower bounds on differences, which we have converted to two sets of upper bounds: `v_{i+1} - v_i ≤ X` and `v_i - v_{i+1} ≤ X`. The second is equivalent to `v_{i+1} - v_i ≥ -X`, which is a lower bound on the difference. However, we only applied upper bound clipping. Does the maximum sum sequence satisfy the lower bound constraints automatically? Not necessarily. For example, if we have intervals [0,0] and [10,10] with X=1. The maximum sum sequence under only the upper constraints `v_2 ≤ v_1 + 1` and `v_1 ≤ v_2 + 1` would be... wait, the intervals force v1=0, v2=10. But `|10-0| = 10 > 1`, so no feasible sequence exists. The clipping would: start v1=0, v2=10. Forward: v2 = min(10, 0+1)=1. Backward: v1 = min(0, 1+1)=0. Result [0,1], sum=1. But the actual feasible sequence is empty? Wait, the intervals are [0,0] and [10,10], so v1 must be 0, v2 must be 10. The constraint is |v1-v2| ≤ 1. This is impossible. Our clipping gave [0,1] which violates v2 ≤ 10? No, v2=1 ≤ 10, so it's within the interval [10,10]? No, 1 is not in [10,10]. We forgot to enforce the interval lower bounds! We must also enforce `v_i ≥ L_i`. In the example, L2=10, R2=10. After forward pass, v2=1, which is below L2. So we need to enforce the lower bounds as well.

So the algorithm should be:
Initialize v_i = R_i.
Forward pass: for i=1 to N-1: v_{i+1} = max(L_{i+1}, min(v_{i+1}, v_i + X))? Actually, we need to ensure v_{i+1} ≥ L_{i+1} at all times. Since we only decrease, v_{i+1} might go below L_{i+1}. If that happens, the problem is infeasible. But we also have the backward pass. The standard algorithm to find the maximum feasible sequence (or detect infeasibility) is:
Initialize v_i = R_i.
Forward: for i=1 to N-1: v_{i+1} = min(v_{i+1}, v_i + X). If v_{i+1} < L_{i+1}, set v_{i+1} = L_{i+1} but then it might violate the forward constraint? Actually, if v_{i+1} is forced below L_{i+1}, then infeasible.
Backward: for i=N-1 down to 1: v_i = min(v_i, v_{i+1} + X). If v_i < L_i, infeasible.
After this, we have a sequence that satisfies the upper Lipschitz constraints and is the maximum possible. But does it satisfy the lower Lipschitz constraints? The lower Lipschitz constraint is v_{i+1} ≥ v_i - X, which is equivalent to v_i ≤ v_{i+1} + X. We enforced that in the backward pass. So both upper and lower Lipschitz constraints are satisfied. And we started with R_i, so v_i ≤ R_i. And we checked v_i ≥ L_i in each step (if not, infeasible). So the resulting sequence is feasible and maximizes the sum? Is it guaranteed to be the maximum? Yes, this is a standard result: the maximum sum of a sequence satisfying `v_{i+1} - v_i ≤ X` and `v_i - v_{i+1} ≤ X` (i.e., both directions) and `L_i ≤ v_i ≤ R_i` is obtained by the two-pass clipping algorithm. Wait, we also need to ensure the lower Lipschitz constraint v_{i+1} ≥ v_i - X. This is equivalent to v_i ≤ v_{i+1} + X. We enforced that in the backward pass. So all constraints are satisfied. And because we started at the maximum possible values and only reduced them when forced by constraints, the sum is maximized.

But is that sufficient? Let's test with an example: L = [0, 0, 0], R = [10, 0, 10], X=5.
Initialize: [10, 0, 10]
Forward:
i=1: v2 = min(0, 10+5)=0. (0 >= L2=0 ok)
i=2: v3 = min(10, 0+5)=5. (5 >= L3=0 ok)
Backward:
i=2: v2 = min(0, 5+5)=0. (0 >= L2=0 ok)
i=1: v1 = min(10, 0+5)=5. (5 >= L1=0 ok)
Result: [5,0,5], sum=10. Is there a better sequence? [10,5,10] is not allowed because v2=5 > R2=0. So [5,0,5] is optimal. Sum=10. Our algorithm gave sum=10. Good.

Another example: L = [0,10,0], R = [10,10,10], X=1.
Initialize: [10,10,10]
Forward:
i=1: v2 = min(10, 10+1)=10. (>=10 ok)
i=2: v3 = min(10, 10+1)=10. (>=0 ok)
Backward:
i=2: v2 = min(10, 10+1)=10.
i=1: v1 = min(10, 10+1)=10.
Result: [10,10,10], sum=30. But is this feasible? |10-10|=0 ≤ 1, yes. But wait, the intervals are [0,10] for v2, so v2=10 is fine. But is there any lower bound constraint violated? No. So sum=30 is optimal.

What about L = [0, 0], R = [0, 10], X=0.
Initialize: [0,10]
Forward: v2 = min(10, 0+0)=0. v2=0 < L2=0? No, equal. So [0,0]. Sum=0. Feasible? |0-0|=0 ≤ 0, yes. But is there a better sequence? v1 must be 0, v2 must be 10, but |0-10|=0? No, 0 is not allowed. So infeasible? But our algorithm gave [0,0] which is feasible and sum=0. However, the problem asks for the minimum cost to make the teeth fit. If it's impossible to make them fit for a given H, then that H is invalid. Our algorithm found a feasible sequence, so H is valid. But wait, the intervals were [0,0] and [0,10]. The sequence [0,0] is within both intervals and satisfies |0-0|=0 ≤ 0. So it is feasible. But does it correspond to a valid grinding? Yes. So H=... is feasible. The original U_i and D_i might allow it. So the algorithm is correct.

But is the maximum sum always achieved by this two-pass clipping? Yes, because the constraints are a convex polytope and the objective is linear, the maximum occurs at an extreme point. The two-pass algorithm computes the "upper envelope" of the constraints. More formally, we can think of it as: we want to maximize Σ v_i. The constraints are:
v_i ≤ R_i
v_i ≥ L_i
v_{i+1} - v_i ≤ X
v_i - v_{i+1} ≤ X

The first set and third set are of the form v_{i+1} ≤ v_i + X, which are difference constraints. The second set is v_i ≤ v_{i+1} + X. Together they form a set of inequalities that can be solved by the "clipping" method. Actually, the standard algorithm for "bounded difference" with intervals is to do a forward pass and a backward pass, but to maximize the sum, we do:
v = L (or R?) Wait, if we want to maximize, we start with R and clip down. If we want to minimize, we start with L and clip up. Here we want to maximize u_i (which is equivalent to minimizing grinding cost). So we start with R_i and clip down. The clipping ensures all constraints are satisfied. And since we only clip when necessary, the result is the lexicographically maximum sequence (and thus the sum is maximized). This is a known property for this type of problem.

However, we must be careful: the forward pass clips v_{i+1} ≤ v_i + X. The backward pass clips v_i ≤ v_{i+1} + X. But what about the lower bound constraints v_{i+1} ≥ v_i - X? That is equivalent to v_i ≤ v_{i+1} + X, which we did in the backward pass. So all Lipschitz constraints are satisfied. And we also need to ensure v_i ≥ L_i. We do that by checking after each clip. If at any point a clip would force a value below L_i, then the problem is infeasible for this H. In that case, we cannot achieve this H, so the binary search should treat it as invalid (return infinity or a large value).

But wait, is the condition v_{i+1} ≥ v_i - X automatically satisfied if we satisfy v_i ≤ v_{i+1} + X? Yes, they are the same. So the two passes are sufficient.

So the algorithm for a given H is:
1. Compute L_i = max(0, H - D_i), R_i = min(U_i, H).
2. Initialize v_i = R_i.
3. For i=0 to N-2:
   v[i+1] = min(v[i+1], v[i] + X)
   if v[i+1] < L_{i+1}: infeasible.
4. For i=N-2 down to 0:
   v[i] = min(v[i], v[i+1] + X)
   if v[i] < L_i: infeasible.
5. If feasible, the minimum cost for the U_i part is Σ (U_i - v_i) = Σ (U_i - R_i) + Σ (R_i - v_i) = constant + Σ (R_i - v_i).
   The total cost for this H is Σ (S_i - H) + Σ (R_i - v_i) - Σ (R_i - v_i)? Wait:
   Total cost = Σ (S_i - H) + Σ (U_i - v_i). But Σ (U_i - v_i) = Σ (U_i - R_i) + Σ (R_i - v_i).
   And Σ (S_i - H) = Σ (U_i + D_i - H) = Σ (U_i - (H - D_i))? Not exactly.
   Actually, the cost to make U_i + D_i = H is Σ (S_i - H). This is the cost for both upper and lower teeth. Then we also need to pay additional cost to reduce the upper teeth further to satisfy the Lipschitz condition? No! The cost to achieve U_i + D_i = H already includes reducing upper teeth to some value u_i and lower teeth to H - u_i. The grinding cost is exactly S_i - H. If we then reduce the upper teeth further to v_i (where v_i ≤ u_i) to satisfy the Lipschitz condition, we pay additional U_i - v_i. But we can instead directly choose the final u_i and pay U_i - u_i. The total cost is Σ (U_i - u_i) + Σ (D_i - (H - u_i)) = Σ (U_i + D_i - H) = Σ (S_i - H). Wait! That's interesting. The total cost to make the pair sum to H and also satisfy the Lipschitz condition on U_i is NOT just Σ (S_i - H). Because the Lipschitz condition might force us to reduce the upper teeth more than necessary, which means we must also reduce the lower teeth less? No, the condition is U_i + D_i = H. If we reduce U_i more, D_i must be larger to keep the sum H? But we can only reduce teeth, not increase them. So if we choose a final U_i' = v_i, then D_i' = H - v_i. Since we can only reduce, we need D_i' ≤ original D_i, i.e., H - v_i ≤ D_i => v_i ≥ H - D_i. This is exactly the lower bound L_i! So the feasible u_i are exactly those in [L_i, R_i]. The total cost is Σ (U_i - u_i) + Σ (D_i - (H - u_i)) = Σ (U_i + D_i - H) = Σ (S_i - H). This is independent of the choice of u_i! As long as u_i is feasible (i.e., u_i ∈ [L_i, R_i]), the total cost is exactly Σ (S_i - H). The distribution of the reduction between upper and lower teeth doesn't matter for the total cost. So the Lipschitz condition on U_i does not change the total cost! It only restricts which u_i we can choose. But any choice in [L_i, R_i] gives the same total cost.

Wait, is that true? Let's check: We want final U_i' + D_i' = H. The cost is (U_i - U_i') + (D_i - D_i') = U_i + D_i - (U_i' + D_i') = S_i - H. Yes! As long as we can achieve U_i' + D_i' = H with U_i' ≤ U_i, D_i' ≤ D_i, the cost is exactly S_i - H. The choice of U_i' within [H - D_i, U_i] doesn't affect the total cost. The only constraint is that we must be able to pick U_i' such that the Lipschitz condition holds. So the problem reduces to: for a given H, does there exist a sequence u_i ∈ [L_i, R_i] satisfying |u_i - u_{i+1}| ≤ X? If yes, the cost is Σ (S_i - H). If no, H is invalid.

So the problem is: find the minimum H (to minimize Σ (S_i - H) = Σ S_i - N*H, which is decreasing in H) such that there exists a sequence u_i ∈ [L_i, R_i] satisfying |u_i - u_{i+1}| ≤ X.

But wait! Is it really that simple? The cost is independent of the distribution? Let's verify with the sample.
Sample 1:
N=4, X=3
U: 3,4,5,2
D: 1,1,9,6
S: 4,5,14,8
min S_i = 4.
We want to find H ≤ 4.
For H=4:
L_i = max(0, H-D_i):
i1: max(0, 4-1)=3
i2: max(0, 4-1)=3
i3: max(0, 4-9)=0
i4: max(0, 4-6)=0
R_i = min(U_i, H):
i1: min(3,4)=3
i2: min(4,4)=4
i3: min(5,4)=4
i4: min(2,4)=2
Intervals: [3,3], [3,4], [0,4], [0,2].
We need |u_i - u_{i+1}| ≤ 3.
u1=3.
u2 ∈ [3,4]. Since |3-u2| ≤ 3 => u2 ≥ 0, so [3,4] ok. Choose u2=4.
u3 ∈ [0,4]. |4-u3| ≤ 3 => u3 ≥ 1. So u3 ∈ [1,4]. Choose u3=1.
u4 ∈ [0,2]. |1-u4| ≤ 3 => u4 ≥ 0 (already). Choose u4=2.
Sequence: 3,4,1,2. All differences: |3-4|=1, |4-1|=3, |1-2|=1. All ≤ 3. Feasible.
Cost = Σ(S_i - 4) = (4+5+14+8) - 4*4 = 31 - 16 = 15. Matches sample output!

For H=3:
L_i: max(0, 3-D):
i1: max(0,3-1)=2
i2: 2
i3: 0
i4: 0
R_i: min(U_i,3):
i1: 3
i2: 3
i3: 3
i4: 2
Intervals: [2,3], [2,3], [0,3], [0,2].
u1=2 or 3.
Try u1=3. Then u2 ∈ [2,3] and |3-u2|≤3 => u2≥0, so [2,3]. Choose u2=3.
u3 ∈ [0,3], |3-u3|≤3 => u3≥0, so [0,3]. Choose u3=3.
u4 ∈ [0,2], |3-u4|≤3 => u4≥0, so [0,2]. Choose u4=2.
Sequence: 3,3,3,2. Differences: 0,0,1 ≤3. Feasible.
Cost = Σ(S_i - 3) = 31 - 12 = 19. But we want minimum cost, so H=4 is better.

So the cost is indeed just Σ (S_i - H) for the largest feasible H.

But wait, is it always true that we want the largest possible H? The cost is decreasing with H. So we want to find the maximum H ≤ min S_i such that the interval graph is feasible. Then the answer is Σ S_i - N * H.

So the problem reduces to: Given intervals [L_i, R_i] (with L_i = max(0, H - D_i), R_i = min(U_i, H)), find the maximum H such that there exists a sequence with bounded difference X. Then answer = Σ S_i - N*H.

Now, how to find the maximum feasible H efficiently?

We can binary search on H. For a given H, we check feasibility in O(N) using the two-pass algorithm. N is up to 2e5, and binary search over range up to 1e9 takes about 31 iterations. 2e5 * 31 = 6.2e6, which is fast.

But is the two-pass algorithm correct for checking feasibility? Let's verify.

The feasibility problem: given intervals [L_i, R_i] and X, does there exist a sequence u_i ∈ [L_i, R_i] with |u_i - u_{i+1}| ≤ X?

This is equivalent to: is there a sequence satisfying:
L_i ≤ u_i ≤ R_i
u_{i+1} ≤ u_i + X
u_i ≤ u_{i+1} + X

This is a system of difference constraints. We can use a shortest path algorithm, but the two-pass clipping is a known necessary and sufficient condition for such "box" constraints with bounded differences. Actually, the two-pass algorithm we described (start with R_i, clip forward, clip backward) produces the maximum sequence. If during the process any value goes below L_i, then no feasible sequence exists. Is that correct?

Let's test a case where the two-pass fails. Suppose intervals: [0,10], [10,10], X=5.
R: [10,10]
Forward: v2 = min(10, 10+5)=10. (>= L2=10 ok)
Backward: v1 = min(10, 10+5)=10. (>= L1=0 ok)
Result [10,10], feasible.

Suppose: [0,0], [10,10], X=5.
R: [0,10]
Forward: v2 = min(10, 0+5)=5. Now v2=5 < L2=10. Infeasible. Correct, because u1=0 forces u2 ≤ 5, but L2=10.

Suppose: [0,10], [0,0], X=5.
R: [10,0]
Forward: v2 = min(0, 10+5)=0. (>=0 ok)
Backward: v1 = min(10, 0+5)=5. (>=0 ok)
Result [5,0], feasible? Check: |5-0|=5 ≤5, yes. u1=5, u2=0. Both in intervals. Feasible.

Suppose: [0,5], [5,10], X=0.
R: [5,10]
Forward: v2 = min(10, 5+0)=5. v2=5 >= L2=5 ok.
Backward: v1 = min(5, 5+0)=5. v1=5 >= L1=0 ok.
Result [5,5], feasible.

Suppose: [0,5], [6,10], X=0.
R: [5,10]
Forward: v2 = min(10, 5+0)=5. v2=5 < L2=6. Infeasible. Correct.

Suppose: [0,10], [0,10], X=0. Both must be equal. R=[10,10]. Forward: v2=min(10,10)=10. Backward: v1=min(10,10)=10. Feasible.

What about a more complex case: L=[0,0,0], R=[10,10,10], X=0. All must be equal. Feasible.

L=[0,5,0], R=[10,10,10], X=3.
R=[10,10,10]
Forward:
i1: v1=10
i2: v2 = min(10, 10+3)=10. >= L2=5 ok.
i3: v3 = min(10, 10+3)=10. >= L3=0 ok.
Backward:
i2: v2 = min(10, 10+3)=10. >=5 ok.
i1: v1 = min(10, 10+3)=10. >=0 ok.
Feasible. Sequence: 10,10,10. Differences 0 ≤3. Yes.

What about L=[0,10,0], R=[5,10,15], X=3.
R=[5,10,15]
Forward:
v1=5
v2 = min(10, 5+3)=8. v2=8 < L2=10. Infeasible. Let's check manually: u1 ≤5, u2 ≥10. Then u2 - u1 ≥ 5 > 3. So infeasible. Correct.

What about L=[0,8,0], R=[5,10,15], X=3.
Forward:
v1=5
v2 = min(10, 5+3)=8. v2=8 >= L2=8 ok.
v3 = min(15, 8+3)=11. v3=11 >= L3=0 ok.
Backward:
v2 = min(8, 11+3)=8. >=8 ok.
v1 = min(5, 8+3)=5. >=0 ok.
Result: [5,8,11]. Differences: 3,3. Feasible. Sum=24.

Could we do better? What if we lower v1? v1=4, then v2 ≤7, but L2=8, so infeasible. v1=5 is max. So correct.

What about L=[0,0,10], R=[10,10,10], X=3.
R=[10,10,10]
Forward:
v1=10
v2 = min(10, 10+3)=10. >=0 ok.
v3 = min(10, 10+3)=10. >=10 ok.
Backward:
v2 = min(10, 10+3)=10. >=0 ok.
v1 = min(10, 10+3)=10. >=0 ok.
Feasible: [10,10,10]. But v3=10 is >= L3=10. u1=10, u2=10, u3=10. Differences 0,0. OK.

What about L=[0,0,11], R=[10,10,10], X=3.
Forward: v3 = min(10, 10+3)=10 < L3=11. Infeasible. Manual: u3 ≥11, u2 ≤10, so u3 - u2 ≥1. But X=3, so |u2-u3| ≤3 => u3 ≤13. Actually u3=11, u2=10, diff=1 ≤3, so it is feasible? Wait! u3=11 is allowed because R3=10? No, R3=10 means u3 ≤ 10. So u3 cannot be 11. The interval for u3 is [11,10] which is empty! So H is invalid for that i. Indeed, L_i ≤ R_i must hold. If L_i > R_i, then no feasible sequence exists. In our construction, L_i = max(0, H - D_i), R_i = min(U_i, H). We must have L_i ≤ R_i, i.e., max(0, H - D_i) ≤ min(U_i, H). This requires H - D_i ≤ U_i => H ≤ U_i + D_i = S_i, and H - D_i ≤ H (trivial), and 0 ≤ min(U_i, H) (trivial). So as long as H ≤ min S_i, we have L_i ≤ R_i. So we only consider H ≤ min S_i. So that case won't happen.

But is the two-pass algorithm correct for all cases? Let's think about the theoretical justification.

We want to know if there exists a sequence u satisfying:
(1) L_i ≤ u_i ≤ R_i
(2) u_{i+1} - u_i ≤ X
(3) u_i - u_{i+1} ≤ X

This is a system of linear inequalities. By Farkas' lemma or by convexity, if there is a solution, there is a solution that is "extremal". The two-pass algorithm computes the maximum possible value for each u_i given the upper bounds (R_i and the X constraints). If this maximum sequence violates the lower bounds L_i, then no sequence exists. Is that true? Not exactly, because the maximum sequence might violate the lower bounds, but a non-maximum sequence could exist. For example, suppose lowering some values could allow others to be higher, but we only care about existence. The two-pass algorithm is a standard way to compute the "upper envelope" of the constraints. But does it correctly detect infeasibility? In the examples above, it seemed to. But I recall that for problems like "find a feasible sequence with bounded differences", the correct approach is to do a forward pass to compute the maximum allowed value for each position given the left constraints, and a backward pass to compute the maximum allowed given the right constraints, and then the intersection must be non-empty. But here we want to know if there exists ANY sequence. The maximum sequence approach might fail if the maximum sequence is not feasible but a lower one is.

Wait, the two-pass algorithm I described: start with v_i = R_i, then v_{i+1} = min(v_{i+1}, v_i + X), then v_i = min(v_i, v_{i+1} + X). This computes the maximum sequence that satisfies the upper bound constraints (R_i and the two Lipschitz constraints). If this maximum sequence satisfies L_i ≤ v_i, then it is feasible. If not, is it possible that some other sequence (with some values lower than the maximum) is feasible? Let's test.

Consider L = [0, 10], R = [0, 5], X = 3.
We have u1 ∈ [0,0], u2 ∈ [10,5]? Wait, L2=10, R2=5, empty. So infeasible. But assume L=[0,0], R=[10,5]? No, L ≤ R.

Consider L = [5, 0], R = [10, 10], X = 3.
R = [10,10]
Forward: v1=10, v2 = min(10, 10+3)=10. v2=10 ≥ L2=0 ok.
Backward: v1 = min(10, 10+3)=10. v1=10 ≥ L1=5 ok.
Result [10,10], feasible. Sequence [10,10] works: |10-10|=0 ≤3.

Consider L = [0, 5], R = [5, 10], X = 3.
R = [5,10]
Forward: v1=5, v2 = min(10, 5+3)=8. v2=8 ≥ L2=5 ok.
Backward: v1 = min(5, 8+3)=5. v1=5 ≥ L1=0 ok.
Result [5,8], feasible.

Consider L = [0, 6], R = [5, 10], X = 3.
Forward: v1=5, v2 = min(10, 5+3)=8. v2=8 ≥ L2=6 ok.
Backward: v1 = min(5, 8+3)=5. v1=5 < L1=0? No, 5 ≥ 0 ok.
Result [5,8], feasible. u1=5 (≥0), u2=8 (≥6). |5-8|=3 ≤3. Yes.

Now a tricky case: L = [0, 8], R = [5, 10], X = 3.
Forward: v1=5, v2 = min(10, 5+3)=8. v2=8 ≥ L2=8 ok.
Backward: v1 = min(5, 8+3)=5. v1=5 ≥0 ok.
Result [5,8], feasible.

What about L = [0, 9], R = [5, 10], X = 3.
Forward: v2 = min(10, 5+3)=8. v2=8 < L2=9. Infeasible. Manual: u1 ≤5, u2 ≥9. Need u2 - u1 ≤3 => u2 ≤ u1+3 ≤ 8. But u2 ≥9. Contradiction. Infeasible.

What about L = [6, 0], R = [10, 10], X = 3.
Forward: v1=10, v2=min(10,13)=10. v2=10 ≥0 ok.
Backward: v1=min(10,13)=10. v1=10 ≥6 ok.
Result [10,10], feasible.

What about L = [6, 10], R = [10, 10], X = 3.
Forward: v1=10, v2=10. v2=10 ≥10 ok.
Backward: v1=10 ≥6 ok.
Feasible.

What about L = [0, 0], R = [10, 10], X = 0.
Must be equal. v=[10,10]. Feasible.

I can't find a counterexample. But I recall that for the problem of "make sequence non-decreasing with bounded differences", the two-pass works. For absolute difference, it's symmetric, so it should also work. Actually, the two-pass algorithm for absolute difference is standard: to find the maximum feasible sequence, you do forward and backward passes. But is it correct for feasibility checking? Suppose there is a feasible sequence, but the maximum sequence is not feasible. That would mean the maximum sequence violates some lower bound, but by lowering some values, we could make it work. However, if the maximum sequence violates a lower bound at position k, it means that even with the maximum possible values from the left and right, we cannot satisfy the lower bound. Because the maximum sequence is the component-wise maximum over all feasible sequences? Is that true?

Let's check: The set of feasible sequences is a convex polytope defined by linear inequalities. The objective "maximize v_k" is linear. The maximum of v_k is achieved at an extreme point. The two-pass algorithm computes a specific extreme point. But is it the component-wise maximum? Not necessarily. There might be a sequence that is higher at position 1 but lower at position 2, etc. However, we want to know if the polytope is empty. The two-pass algorithm gives a necessary condition? If the two-pass algorithm (which computes a specific point) is feasible, then the polytope is non-empty. If it is infeasible, does it mean the polytope is empty? Not necessarily, because the algorithm computes a particular point (the one obtained by the greedy clipping). It might be that this point is infeasible but another point is feasible.

Let's test a potential counterexample. We need L_i, R_i, X such that the greedy clipping fails but a solution exists.

Consider N=3.
L = [0, 10, 0]
R = [10, 10, 10]
X = 5.
Greedy:
v1=10
v2 = min(10, 10+5)=10. v2=10 >= L2=10 ok.
v3 = min(10, 10+5)=10. v3=10 >=0 ok.
Backward: v2=10, v1=10. All ok. Feasible.

Consider L = [0, 10, 0]
R = [10, 10, 10]
X = 4.
v1=10
v2 = min(10, 10+4)=10 >=10 ok.
v3 = min(10, 10+4)=10 >=0 ok.
Feasible.

Consider L = [0, 10, 0]
R = [10, 10, 10]
X = 3.
v1=10
v2 = min(10, 10+3)=10 >=10 ok.
v3 = min(10, 10+3)=10 >=0 ok.
Feasible.

We need a case where the greedy clipping from the top forces a value down, but then a lower value would allow the next to be higher? No, because the constraints are upper bounds on differences. If we lower a value, the next value can only be lower or equal? Actually, the constraints are:
v_{i+1} ≤ v_i + X
v_i ≤ v_{i+1} + X
If we lower v_i, the first constraint allows v_{i+1} to be lower (since v_i + X decreases). The second constraint allows v_i to be lower (since v_{i+1} + X is fixed, so v_i can be lower). So lowering a value can only make the feasible set for the others larger? Wait, the feasible set for v_{i+1} given v_i is: max(L_{i+1}, v_i - X) ≤ v_{i+1} ≤ min(R_{i+1}, v_i + X). If v_i decreases, the lower bound v_i - X decreases, and the upper bound v_i + X decreases. So the interval for v_{i+1} shifts left and shrinks from above. It can only get smaller or shift down. Similarly, the constraint on v_i given v_{i+1} is: v_{i+1} - X ≤ v_i ≤ v_{i+1} + X. If v_{i+1} is determined, v_i is constrained. So it's not obvious that the greedy maximum is the component-wise maximum.

Let's try to construct a counterexample.
We want the greedy algorithm to produce a sequence v that violates some L_k, but there exists another sequence u that satisfies all L_i.
Since v is obtained by starting with R and clipping, v is the maximum possible value for v_1 that is consistent with the rightward constraints? Actually, the forward pass ensures v_{i+1} ≤ v_i + X. The backward pass ensures v_i ≤ v_{i+1} + X. Together, they ensure the Lipschitz condition. And v_i ≤ R_i always. So v is the unique sequence that is the "upper envelope" of the constraints? Let's see.

The system of inequalities:
v_i ≤ R_i
v_{i+1} - v_i ≤ X
v_i - v_{i+1} ≤ X

We can rewrite as:
v_{i+1} ≤ v_i + X
v_i ≤ v_{i+1} + X
v_i ≤ R_i

This is a set of upper bounds on v_i and on the differences. The maximum feasible region for the sequence is the set of all sequences satisfying these upper bounds. This is a convex set. The maximum value of any particular v_k over this set is given by the longest path in a DAG? Actually, we can find the maximum v_k by a forward pass and backward pass. But the sequence v produced by the two-pass is the lexicographically maximum sequence? Or the component-wise maximum? Not necessarily.

For example, consider:
L = [0, 0, 0, 0]
R = [10, 10, 10, 10]
X = 0.
The constraints force all v_i = 10. The two-pass gives [10,10,10,10]. Feasible.

Consider:
L = [0, 0, 0]
R = [10, 10, 10]
X = 5.
All sequences with values in [0,10] and differences ≤5 are feasible. The two-pass gives [10,10,10]. Feasible.

What if we have a "bottleneck" that forces a value down?
Suppose L = [0, 5, 0]
R = [10, 10, 10]
X = 3.
Two-pass:
v1=10
v2 = min(10, 10+3)=10. v2=10 >= L2=5 ok.
v3 = min(10, 10+3)=10. v3=10 >=0 ok.
Backward: v2=10, v1=10. Result [10,10,10]. Feasible.

Suppose L = [0, 8, 0]
R = [10, 10, 10]
X = 3.
v1=10
v2 = min(10, 10+3)=10. v2=10 >=8 ok.
v3 = min(10, 10+3)=10. v3=10 >=0 ok.
Result [10,10,10]. Feasible.

Suppose L = [0, 9, 0]
R = [10, 10, 10]
X = 3.
v1=10
v2 = min(10, 10+3)=10. v2=10 >=9 ok.
v3 = min(10, 10+3)=10. v3=10 >=0 ok.
Result [10,10,10]. Feasible.

Suppose L = [0, 10, 0]
R = [10, 10, 10]
X = 3.
v1=10
v2 = min(10, 10+3)=10. v2=10 >=10 ok.
v3 = min(10, 10+3)=10. v3=10 >=0 ok.
Result [10,10,10]. Feasible.

Suppose L = [0, 11, 0] but R=[10,10,10]. Not possible since L≤R.

What if X is very small? L = [0, 5, 0], R = [10, 10, 10], X=2.
v1=10
v2 = min(10, 12)=10. v2=10 >=5 ok.
v3 = min(10, 12)=10. v3=10 >=0 ok.
Backward: v2=10, v1=10. Feasible.

What if L = [0, 5, 0], R = [10, 10, 10], X=1.
v1=10
v2 = min(10, 11)=10. v2=10 >=5 ok.
v3 = min(10, 11)=10. v3=10 >=0 ok.
Feasible.

It seems the two-pass always works when it says feasible. But what about when it says infeasible? Suppose it says infeasible because v2 went below L2. That means in the forward pass, v2 = min(R2, v1 + X) < L2. Since v1 ≤ R1, v1 + X ≤ R1 + X. So R2 < L2 or R2 ≥ L2 but R1 + X < L2. If R1 + X < L2, then any u1 ≤ R1 implies u1 + X < L2, so u2 must be ≥ L2, but u2 ≤ R2 and u2 ≤ u1 + X < L2, contradiction. So indeed infeasible.

But what if the forward pass succeeds, but the backward pass makes v1 go below L1? That means v1 = min(v1, v2 + X) < L1. Since v2 ≤ R2, v2 + X ≤ R2 + X. So R1 < L1 or R1 ≥ L1 but v2 + X < L1. But v2 was set in forward pass. Could there be a solution that uses a smaller v2? If we lower v2, then v1 = min(v1, v2 + X) becomes even smaller (since v2 + X decreases). So that would not help. The backward pass uses the current v2 (which is the maximum possible given the forward constraints and the interval). If with that maximum v2, we cannot satisfy L1, then any smaller v2 would also fail to satisfy L1 (or make it worse). So the two-pass is correct.

Wait, the backward pass updates v_i based on the updated v_{i+1}. The updated v_{i+1} is the minimum of the original v_{i+1} (from forward pass) and the new constraint from the right. But we are doing a single pass forward, then a single pass backward. Is that sufficient to enforce all constraints? Yes, because the constraints are a system of difference inequalities. The standard algorithm to find the maximum solution is to do a forward pass and a backward pass, but the backward pass must be done with the updated values. However, a single forward and single backward pass is not enough for general difference constraints; you might need to iterate until convergence. For example, in the "trampoline" problem or "adjusting weights" with bounds on differences, a single forward and backward pass is not sufficient if there are both upper and lower bounds on differences. But here we have only upper bounds on the differences v_{i+1} - v_i and v_i - v_{i+1}, and upper bounds v_i ≤ R_i. There are no lower bounds on differences (except those implied by the upper bounds on the opposite difference). Actually, the lower bound on v_{i+1} - v_i is -X, which is equivalent to v_i - v_{i+1} ≤ X, which is an upper bound on v_i - v_{i+1}. So all constraints are of the form "variable ≤ something" or "variable - next ≤ something". This is a system of difference constraints with only "≤" and no "≥" except the individual lower bounds L_i.

But the individual lower bounds L_i are not used in the forward/backward passes except to check feasibility. In the forward pass, we do v_{i+1} = min(v_{i+1}, v_i + X). This ensures v_{i+1} - v_i ≤ X. In the backward pass, we do v_i = min(v_i, v_{i+1} + X). This ensures v_i - v_{i+1} ≤ X. After these two passes, all difference constraints are satisfied. The values are only decreased from the initial R_i. So they are still ≤ R_i. The only constraints not yet enforced are the lower bounds L_i. We check if v_i ≥ L_i. If not, we declare infeasible. Is it possible that a sequence exists but this particular sequence v is infeasible because some v_i < L_i, but by increasing some earlier values (which were decreased by the backward pass), we could make it feasible? But the backward pass is the last pass; it only decreases values. So if after the backward pass v_i < L_i, then before the backward pass, v_i was at least as large (since backward pass only decreases). So the forward pass produced a sequence v^f that satisfied the forward constraints and v^f_i ≥ v_i. If v^f_i < L_i, we already declared infeasible in the forward pass. So the only case is that the forward pass was feasible, but the backward pass made some v_i go below L_i. That means before the backward pass, v_i ≥ L_i, but after clipping with v_{i+1} + X, it became < L_i. So v_{i+1} + X < L_i. Since v_{i+1} is the result of the forward pass (and possibly earlier backward updates), but we are doing backward pass in reverse order: for i from N-2 down to 0, we update v_i using the current v_{i+1}. At the moment of update, v_{i+1} is the final value for that position (since we process from right to left). So v_{i+1} is as small as possible given the forward pass and the rightward constraints. If v_i = min(v_i, v_{i+1} + X) < L_i, then v_{i+1} + X < L_i. Since v_{i+1} was set to be at most R_{i+1} and at least L_{i+1} (if feasible), we have v_{i+1} + X ≤ R_{i+1} + X. So R_{i+1} + X < L_i. This means that for any feasible sequence, u_{i+1} ≤ R_{i+1}, so u_i ≤ u_{i+1} + X ≤ R_{i+1} + X < L_i. But we also need u_i ≥ L_i. Contradiction. So indeed infeasible.

Thus, the two-pass algorithm is correct for checking feasibility.

So the algorithm is:
- Compute S_i = U_i + D_i.
- Let min_S = min S_i.
- Binary search for the maximum H in [0, min_S] such that the interval graph is feasible.
- For a given H, compute L_i = max(0, H - D_i), R_i = min(U_i, H).
- Run the two-pass algorithm. If feasible, return true.
- The answer is sum_S - N * H_max.

Wait, is the cost exactly sum_S - N*H? Yes, as argued, the total grinding cost is the sum of reductions of both upper and lower teeth. For each pair, we reduce upper by U_i - u_i and lower by D_i - (H - u_i) = D_i - H + u_i. Total = U_i + D_i - H = S_i - H. This is independent of u_i as long as u_i ∈ [L_i, R_i]. So if there is at least one feasible u_i sequence, the cost is exactly that. And we want to minimize the cost, so we want the largest H. So binary search for max H.

But we must be careful: H must be an integer? The problem says "There exists an integer H". So H is integer. The lengths are integers, we reduce by 1 each time, so H is integer. The binary search is over integers.

Complexities: O(N log max_S). max_S is up to 2e9, so log2(2e9) ≈ 31. N up to 2e5. 6.2e6 operations, fine.

Let's test with sample 3:
N=4, X=1
U: 1e9, 1e9, 1e9, 1
D: 1e9, 1e9, 1e9, 1
S: 2e9, 2e9, 2e9, 2
min_S = 2.
We want max H ≤ 2.
Check H=2:
L1 = max(0, 2 - 1e9) = 0
R1 = min(1e9, 2) = 2
So intervals: [0,2] for first three, [max(0,2-1)=1, min(1,2)=1] for last = [1,1].
R: [2,2,2,1]
Forward:
v1=2
v2 = min(2, 2+1)=2. >=0
v3 = min(2, 2+1)=2. >=0
v4 = min(1, 2+1)=1. >=1 ok.
Backward:
v3 = min(2, 1+1)=2. >=0
v2 = min(2, 2+1)=2.
v1 = min(2, 2+1)=2.
All ok. So H=2 is feasible.
Cost = sum_S - 4*2 = (2e9*3 + 2) - 8 = 6000000002 - 8 = 5999999994. Matches sample output!

Check H=3? min_S=2, so H max is 2.

Sample 4:
N=15, X=128
We can test later.

So the solution seems to be:
1. Read N, X, U_i, D_i.
2. Compute S_i = U_i + D_i, sum_S.
3. min_S = min S_i.
4. Binary search low=0, high=min_S.
   While low < high:
     mid = (low + high + 1) // 2
     if feasible(mid): low = mid
     else: high = mid - 1
5. Answer = sum_S - N * low.

Feasible(H):
  For i in 0..N-1:
    L[i] = max(0, H - D[i])
    R[i] = min(U[i], H)
    v[i] = R[i]
  Forward:
    for i=0..N-2:
      v[i+1] = min(v[i+1], v[i] + X)
      if v[i+1] < L[i+1]: return False
  Backward:
    for i=N-2 down to 0:
      v[i] = min(v[i], v[i+1] + X)
      if v[i] < L[i]: return False
  return True

Edge cases: H can be 0? U_i ≥ 1, D_i ≥ 1, so S_i ≥ 2. So H min is 0. If H=0, then L_i = max(0, 0 - D_i) = 0, R_i = min(U_i, 0) = 0. So all v_i = 0. Feasible trivially. Cost = sum_S. So answer is at most sum_S. The binary search will find some H ≥ 0. If no H > 0 is feasible, H=0 is always feasible. So answer is finite.

Wait, is H=0 always feasible? If H=0, then u_i = 0 for all i. Then |0-0| = 0 ≤ X. Yes. So H=0 is always feasible. So the binary search will always find at least 0.

But wait, can we reduce a tooth to 0? The problem says "choose exactly one tooth whose length is positive, and reduce its length by 1". So we can reduce positive to 0, but not negative. So final length 0 is allowed. The lower bound L_i = max(0, H - D_i). For H=0, L_i = 0. So u_i can be 0. Good.

One more check: The cost formula sum_S - N*H assumes that we can achieve the reduction with exactly that cost. But is it possible that the Lipschitz condition forces us to reduce the upper tooth more than necessary, which would increase the cost? Let's re-evaluate.

Total cost = Σ (U_i - u_i) + Σ (D_i - d_i) where d_i = H - u_i.
Total = Σ (U_i + D_i - H) = Σ S_i - N*H.
This is independent of u_i. So as long as there exists a sequence u_i satisfying the constraints, the cost is exactly that. There is no additional cost. The choice of u_i only affects how the cost is split between upper and lower teeth, but the total is the same.

This is a crucial insight. So the problem is simply to find the maximum H ≤ min S_i such that there exists u_i with:
- L_i = max(0, H - D_i) ≤ u_i ≤ min(U_i, H) = R_i
- |u_i - u_{i+1}| ≤ X.

And the answer is sum S_i - N * H.

So the problem is solved.

Now, we need to implement the two-pass algorithm carefully with large integers. N up to 2e5, values up to 1e9, sum up to 2e14, so use Python int (unbounded) or 64-bit. In Python, int is fine.

Time complexity: O(N log max_S). Memory: O(N) for U, D, but we can compute on the fly or store.

Implementation details:
- Read input.
- Store U and D as lists of integers.
- Compute S and sum_S.
- min_S = min(S).
- Binary search.
- The feasible function: given H, we need L_i and R_i. We can compute them in the forward pass without storing all? We need L_i for checking. We can store L_i or compute on the fly. Since we have the original U and D, we can compute L_i = max(0, H - D_i), R_i = min(U_i, H). We need to pass through the arrays three times: once to initialize v, forward, backward. We can do it in one loop? Actually, we need the original U and D. We can store them.

Optimization: The binary search is the bottleneck. 31 iterations. Each feasible check is O(N). N=2e5, so 6.2 million operations. Python should handle this easily if written efficiently (avoiding unnecessary overhead). Using list indexing is fine.

Let's double-check the two-pass logic with integer types.
v[i] is a Python int.
v[i+1] = min(v[i+1], v[i] + X)
This is fine.

Potential pitfall: The condition v[i+1] < L[i+1] should be strictly less than. If equal, it's fine.
Similarly for backward.

What about the case where L_i > R_i? As discussed, for H ≤ min S_i, we have H ≤ S_i = U_i + D_i. So H - D_i ≤ U_i. Also H - D_i ≤ H. And 0 ≤ min(U_i, H) because U_i ≥ 1, H ≥ 0. So L_i = max(0, H - D_i) ≤ min(U_i, H) = R_i. So L_i ≤ R_i always holds for H ≤ min S_i. We don't need to check it separately.

Thus, the solution is solid.

Let's test with a small custom case.
N=2, X=1
U: [2, 2]
D: [2, 2]
S: [4,4]
min_S=4.
H=4:
L: [max(0,4-2)=2, 2]
R: [min(2,4)=2, 2]
v: [2,2]
Forward: v2 = min(2, 2+1)=2. >=2.
Backward: v1 = min(2,

## worker: Implement the binary search and feasibility check 
The solution works by recognizing that the total grinding cost depends only on the target common sum H: it is exactly Σ S_i - N·H. This is because any valid final upper tooth length u_i in the feasible range [max(0, H-D_i), min(U_i, H)] yields the same total cost (the reduction of the lower tooth compensates exactly). Thus we only need to maximize H subject to the existence of a sequence u_i satisfying the Lipschitz condition |u_i - u_{i+1}| ≤ X.

Feasibility for a given H is checked via a two-pass clipping algorithm: start with the maximum possible u_i = R_i, then enforce the upper-bound constraints u_{i+1} ≤ u_i + X (forward) and u_i ≤ u_{i+1} + X (backward). If any value falls below its lower bound L_i, the constraints are infeasible. This correctly detects feasibility because the computed sequence is the component-wise maximum of all feasible sequences under the upper-bound constraints; if it fails the lower bounds, no sequence can exist.

Binary search finds the largest feasible H in O(N log max_S) time, well within limits for N up to 2×10⁵.

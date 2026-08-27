We need each `target[i]` to have at least one multiple present in `nums` after we increment elements (never decrement). For each target, the valid values it can "cover" are its multiples (including itself). An element of `nums` can be increased to any number ≥ its current value, so it can cover any target whose multiple is ≥ the element's current value.

Since `target.length ≤ 4`, we can enumerate all subsets of `nums` assigned to cover a target. For each assignment (a function mapping each `t` to one `nums[i]`), the cost is sum over `t` of `ceil(needed_multiple / t) * t - nums[i]`, where `needed_multiple` is the smallest multiple of `t` that is ≥ `nums[i]`. If `nums[i]` is already a multiple, cost is 0.

We can search over assignments using DP over subsets of `nums`. State: subset mask of used `nums`; value: min cost to cover processed targets. For each next target, try every unused `nums[i]`. Since `n ≤ 5e4` and `|target| ≤ 4`, the number of states is manageable only if we use meet-in-the-middle: split `nums` into two halves and for each target generate a list of (cost, used-mask-in-half) pairs, then DP combine. Actually, simpler: iterate over subsets of `nums` of size `|target|`, but n=5e4 is too large for subset enumeration.

Better: since |target| is tiny (≤4), we can pick one distinct nums element per target. For each target, independently sort nums by cost to make it a multiple (cost = (ceil(num/t)*t - num)), and consider combinations using recursion. But n=5e4, |target|=4 → O(n^4)=6.25e18 impossible.

Use meet-in-the-middle on `nums`: split into left/right halves of size ~n/2. For each target, compute an array of (cost, mask) for each half where mask is a single bit index within the half (or no element). Then for each target, we have a multiset of possible single-element assignments per half. We need to pick one element per target, all distinct. This is exactly: for each half, enumerate all ways to assign up to k=|target| distinct elements to the k targets. We can generate all valid assignments per half using backtracking (since n/2 ~ 25000 and k≤4, still large).

But there is a smarter way: for each target, we can keep the best (smallest cost) element in each half, and also second-best, etc. Since k≤4, we can just take for each target the best few elements. However different targets might pick the same element, causing conflict. We can handle conflicts by considering that at most |target| elements are chosen total, so the optimal solution likely uses the globally best |target| candidate elements across all target options. We can compute the top (|target| + small margin) cheapest "candidate" elements per target, then try combinations.

A robust approach: since |target| ≤ 4, the answer is at most sum of (max(nums) * target[i] / target[i])... but we can do exponential in n only via a limited candidate set. Generate all "useful" nums per target: an element is useful only if its cost to become a multiple of t is "small" relative to alternatives. But we can't rely on that.

Alternative simpler approach: For each target t, we want the minimal total increment. This is essentially a minimum weight matching in a bipartite graph where left side = targets (≤4), right side = nums (≤5e4), and we need a matching covering all targets. Edge weight from t to nums[i] = (ceil(nums[i]/t)*t - nums[i]). Since left side is tiny, we can run Hungarian or just brute force assignments: for each target, sort nums by weight, take top K candidates (e.g., K=50), then DFS assign targets to distinct candidates. K=50^4=6.25e6 feasible.

Take K = min(n, 50) cheapest (or just take all if n small). For n=5e4, 50^4=6.25e6 worst case, OK. We can early prune by minimum possible remaining cost.

Better: since n=5e4, we can actually for each target, compute all costs and just take the best 20 or so. With pruning (branch & bound), 20^4=160k, easily fast.

Thus algorithm:
- For each target t in target, compute list `cands[t]` of (cost, idx) for all nums, sort by cost, keep top L (L=30).
- Recursive DFS assigning each target a distinct candidate (by idx). Maintain best answer. Prune when current cost + lower bound on remaining >= best. Lower bound = sum of minimum cost of remaining targets (ignoring conflicts) since we can reuse an element in lower bound (optimistic).
- Return best.

Edge: a target may already be covered by a nums element with cost 0 (already multiple). In that case cost=0 candidate will appear; algorithm will naturally find 0.

Complexity: O(|target| * n log n + L^|target|). With L=30, |target|≤4, this is at most 810k recursive states, fine.
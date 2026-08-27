We need to maximize the minimum of the three vitamin totals, subject to total calories ≤ X, where each item gives A_i units of a single vitamin V_i and costs C_i calories. This is a classic 3-type knapsack with an objective on the balanced minimum.

We'll group items by vitamin type (1, 2, 3). For each type, we compute a DP over calories: the maximum total vitamin units obtainable with exactly `c` calories using items of that type (standard 0/1 knapsack, N up to 5000, X up to 5000 → O(N·X) is feasible). Let `dp1[c], dp2[c], dp3[c]` be these maximums (0 if not achievable; for unreachable calories we keep -∞).

Then we iterate over calorie splits: for `c1 + c2 + c3 ≤ X`, the value is `min(dp1[c1], dp2[c2], dp3[c3])`. We take the maximum over all splits. Complexity O(X³) is too much (125 billion), so we need optimization.

We can fix `c3` (0..X) and want the maximum of `min( best1, best2 )` where `best1 = max_{c1 ≤ X-c3} dp1[c1]`, `best2 = max_{c2 ≤ X-c3-c1}` … still O(X²) per `c3`. Better: for each remaining budget `B`, precompute `M1[B] = max_{c1 ≤ B} dp1[c1]` (prefix maximum), and similarly `M2[B]`. Then the best two-type allocation with combined budget `B` is `min(M1[B], M2[B])` (use all of B split arbitrarily, but we need exactly c1 + c2 ≤ B; since M1, M2 are non-decreasing in budget, the min is attained at some split giving at most B each — actually we can think: for budget B split into c1, c2 with c1+c2 ≤ B, we can move unspent calories to either side increasing the prefix maxes, so the best is `min(M1[B], M2[B])`). More rigorously: the optimal pair is achieved when we spend exactly B calories total (since M1 and M2 are non-decreasing), and then we want to maximize `min(dp1[c1], dp2[c2])` with c1+c2 = B. This is equivalent to finding the best `k` such that we can achieve at least `k` from both, i.e., there exists c1 with dp1[c1] ≥ k and c2 with dp2[c2] ≥ k and c1+c2 ≤ B. The maximum such k is exactly `min(M1[B], M2[B])`? Not quite — it's the maximum k such that there exist c1, c2 with c1+c2 ≤ B, dp1[c1] ≥ k, dp2[c2] ≥ k. Since M1[B] is the max over c1 ≤ B of dp1[c1], similarly M2[B], but we need c1+c2 ≤ B, so we can't use B for both. The right quantity is: for each `c1`, value is `min(dp1[c1], M2[B-c1])`. Iterate c1 over 0..B → O(X²) total. But we can do better with two-pointer or just accept O(X²) ≈ 25M, fine. Actually we have outer loop over c3 (0..X) and inner over c1 (0..X-c3) → O(X²/2) = 12.5M, fine.

Simpler: for each `c1` and `c2`, if `c1 + c2 + c3 ≤ X`, compute `min(dp1[c1], dp2[c2], dp3[c3])`. We can do nested loops c1, c2, then compute max feasible c3 = X - c1 - c2, take `dp3[max_c3_prefix]`. That's O(X²) = 25M, fine.

Algorithm:
1. Read N, X.
2. Group items by V_i into three lists: costs and values.
3. Run 0/1 knapsack for each type: `dp[t][c]` = max vitamin units using exactly c calories (or ≤c). Use -1 for unreachable. Initialize dp[0]=0. For each item (cost w, value v), iterate c from X down to w: dp[c] = max(dp[c], dp[c-w] + v). After each type, convert to prefix max: `for c in 1..X: dp[c] = max(dp[c], dp[c-1])`. So `dp1[c]` = max vitamin1 with ≤c calories.
4. Now iterate `c1` from 0 to X, `c2` from 0 to X - c1:
   - `budget3 = X - c1 - c2`
   - candidate = min(dp1[c1], dp2[c2], dp3[budget3])
   - track maximum.
5. Print answer.

This is O(N·X + X²) ≈ 25M + 25M = 50M, fast.

Edge cases: unreachable states (dp values stay 0 or -1?). Since all A_i ≥ 1, but we might have 0 calories spent on a type giving 0 vitamins — that's valid (0 is the minimum possible). The answer can be 0 (sample 2). Our dp initialized with 0 at cost 0, and unreachable costs keep -1. But since we do prefix max, we need unreachable to not pollute. Initialize dp = [-1]*(X+1), dp[0]=0. After processing items, do prefix max only over non-negative entries, or treat -1 as -inf. Let's do: for c from 0..X: if dp[c] < 0 and c>0, set to -1; then for c from 1..X: dp[c] = max(dp[c], dp[c-1]). This way dp[c] = max vitamin achievable with ≤c calories (or 0 if nothing achievable, but 0 is correct baseline — we can always "choose" 0 items of a type, giving 0 vitamins, with 0 calories).

Wait, we must be careful: the item set for each type is independent. For a type, we either pick some subset of that type's items (possibly none) costing some calories, giving sum of A_i. We want to consider all possible calorie allocations to each type independently. So dp1[c] = maximum vitamin1 from items of type 1 using at most c calories. Using 0 items gives 0 vitamins and 0 calories. With prefix max, dp1[0]=0, dp1[c]≥0 always. Similarly for others. Then the triple min handles the balance.

Time/space: three arrays of size X+1 ≈ 5001, fine. Knapsack is 0/1 per type. N=5000, but items are split; total still N.

Let's verify on sample 1:
- Type1: one item (5 cal, 8 vit) → dp1: [0,0,0,0,0,8,8,...]
- Type2: items (5,3) and (10,7) → dp2: [0,0,0,0,0,3,3,3,3,3,10,...] prefix max: 0,0,0,0,0,3,3,3,3,3,10,10,...
- Type3: items (5,2) and (10,3) → dp3: [0,0,0,0,0,2,2,2,2,2,3,3,...]
- Iterate c1,c2: best is c1=5, c2=5, c3=15 → min(8,3,3)=3. Output 3. ✓

Sample 2: type1 (1 cal, 200000), type2 (1 cal, 200000), type3 empty → dp3 all 0.
- c1=1, c2=1, c3=4998 → min(200000, 200000, 0) = 0. Answer 0. ✓

Looks good.
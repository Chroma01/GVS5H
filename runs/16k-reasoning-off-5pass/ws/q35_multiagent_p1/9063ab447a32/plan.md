1. **Binary Search on Answer**: Since the maximum total units we can buy is monotonic with respect to cost (buying more units always costs more or equal), we can binary search on the total number of units `T`.
2. **Check Function**: For a given total unit count `T`, we need to determine if it's possible to buy exactly `T` units (or at most `T` units, but since we want max, we check feasibility of `T`) with cost ≤ M. To minimize cost for exactly `T` units, we should distribute the units among products such that the marginal cost of each additional unit is balanced. The cost function for product `i` is `k^2 * P_i`. The marginal cost of the `k`-th unit of product `i` is `k^2 * P_i - (k-1)^2 * P_i = (2k-1) * P_i`.
3. **Greedy Distribution via Binary Search on Marginal Cost**: For a fixed total `T`, we can find the optimal distribution by finding a threshold marginal cost `C` such that the sum of units bought with marginal cost ≤ C is at least `T`. Specifically, for each product `i`, the maximum number of units `k_i` we can buy such that the marginal cost of the last unit is ≤ C is determined by `(2k_i - 1) * P_i ≤ C` => `k_i ≤ (C + 1) / (2 * P_i)`. So `k_i = min(T, floor((C + 1) / (2 * P_i)))` but we also need the sum to be exactly `T`.
4. **Refined Check**: Actually, a simpler approach for the check function: Given `T`, we want to minimize `sum(k_i^2 * P_i)` subject to `sum(k_i) = T` and `k_i >= 0`. This is a convex optimization problem. We can use Lagrange multipliers or binary search on the "price" of a unit. Let `lambda` be the Lagrange multiplier. For each product, we choose `k_i` to minimize `k_i^2 * P_i - lambda * k_i`. The optimal `k_i` is approximately `lambda / (2 * P_i)`. More precisely, we binary search on `lambda` (or a related value) to find the distribution that sums to `T` with minimum cost.
5. **Alternative Check via Binary Search on Threshold**: Binary search on a value `X` such that we buy all units of product `i` whose marginal cost is less than `X`. The marginal cost of the `k`-th unit of product `i` is `(2k-1)*P_i`. So for product `i`, we buy `k_i` units where `(2k_i - 1) * P_i < X` and `(2(k_i+1) - 1) * P_i >= X`. This gives `k_i = floor((X - 1) / (2 * P_i) + 1)` if `X > P_i`, else 0. Wait, let's derive: `(2k-1)P_i < X` => `2k-1 < X/P_i` => `k < (X/P_i + 1)/2` => `k_i = floor((X - 1) / (2 * P_i)) + 1` if `X > P_i`? Let's check: if `X = P_i`, then `(2k-1)P_i < P_i` => `2k-1 < 1` => `k < 1` => `k=0`. Formula: `floor((P_i - 1)/(2*P_i)) + 1 = floor(<0.5) + 1 = 0 + 1 = 1`. Incorrect. Let's use `k_i = max(0, floor((X - 1) / (2 * P_i)) + 1)` is wrong. 
   Correct derivation: We want largest `k` such that `(2k-1)P_i < X`. 
   `2k - 1 < X / P_i`
   `2k < X / P_i + 1`
   `k < (X / P_i + 1) / 2`
   `k_i = floor((X - 1) / (2 * P_i))` if we use integer arithmetic carefully? 
   Let's just use: `k_i = 0` if `X <= P_i`. Otherwise, `k_i = floor((X - 1) // (2 * P_i)) + 1`? 
   Test: `P_i=1, X=1`. `k_i=0`. Correct (marginal cost of 1st unit is 1, which is not < 1).
   `P_i=1, X=2`. `k_i = floor(1/2) + 1 = 0 + 1 = 1`. Marginal cost of 1st unit is 1 < 2. Correct.
   `P_i=1, X=3`. `k_i = floor(2/2) + 1 = 1 + 1 = 2`. Marginal costs: 1st=1, 2nd=3. 1<3, 3 not < 3. So k=1? No, we want strictly less? If we define threshold as "buy if marginal cost <= X", then `(2k-1)P_i <= X`.
   Let's stick to: buy `k_i` units if `(2k_i - 1) * P_i <= X`.
   `2k_i - 1 <= X / P_i`
   `2k_i <= X / P_i + 1`
   `k_i <= (X / P_i + 1) / 2`
   `k_i = floor((X + P_i) / (2 * P_i))`? 
   Let's test `P_i=1, X=1`. `(1+1)/2 = 1`. k=1. Marginal cost 1 <= 1. Correct.
   `P_i=1, X=2`. `(2+1)/2 = 1.5` -> 1. k=1. Marginal cost 1 <= 2. Next unit marginal cost 3 > 2. Correct.
   `P_i=1, X=3`. `(3+1)/2 = 2`. k=2. Marginal costs 1, 3. Both <= 3. Correct.
   So `k_i = (X + P_i) // (2 * P_i)`.
   Sum `k_i` might exceed `T`. If sum > T, we bought too many. If sum < T, we bought too few.
   We binary search `X` to get sum close to `T`. Then calculate exact cost.
   Actually, we can binary search `X` such that `sum(k_i) >= T` and `sum(k_i') < T` for `X-1`. Then we take all units with marginal cost < X, and fill the remaining needed units with those having marginal cost == X (which have the same P_i, so we pick the cheapest ones? No, all units at the same marginal cost threshold for a specific product are identical in cost structure, but different products have different P_i. However, at the threshold X, the "marginal cost" is exactly X for some units. We just need to pick `T - sum_{marginal < X} k_i` more units from the set of units with marginal cost == X. Since all these units have marginal cost X, their "value" is the same in terms of cost efficiency? No, we just need to minimize total cost. The units with marginal cost < X are definitely bought. The units with marginal cost > X are not. The units with marginal cost == X are candidates. We need to pick enough of them to reach T. Since they all have the same marginal cost X, it doesn't matter which ones we pick? Wait, the cost is `k^2 P_i`. The marginal cost is `(2k-1)P_i`. If `(2k-1)P_i = X`, then the cost of that specific unit is effectively X. So yes, we just pick any `rem` units from the pool of units with marginal cost exactly X.
   
   Algorithm:
   1. Binary search `T` in `[0, M]` (upper bound: since min P_i >= 1, max units <= M). Actually max units is M (if P_i=1, k^2 <= M => k <= sqrt(M), but we have N products. Max units is when we buy 1 unit of each cheap product. Upper bound: M is 10^18, so T can be up to 10^18? No, if P_i=1, cost of k units is k^2. If we buy T units all of one product, cost T^2 <= M => T <= sqrt(M) = 10^9. If we spread across N products, T can be larger. Max T is when we buy 1 unit of each of N products with P_i=1. Cost N. If M=10^18, N=2*10^5, we can buy many more. 
   Actually, the maximum possible units is bounded by M (since each unit costs at least 1). So T in `[0, M]`.
   
   2. For a fixed T, we want to check if min cost <= M.
      Use binary search on X to find the threshold such that sum of k_i(X) >= T.
      Let `S(X) = sum_i floor((X + P_i) / (2 * P_i))`.
      Find smallest X such that `S(X) >= T`.
      Let this be `X*`.
      Calculate `base_units = S(X* - 1)`.
      `rem = T - base_units`.
      The cost is `sum_i cost_i(k_i(X*-1)) + rem * X*`.
      Why `rem * X*`? Because each additional unit at the threshold has marginal cost X*.
      Check if this total cost <= M.
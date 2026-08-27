
## ideation
**Core difficulty:** Maximize the minimum of three independent vitamin totals subject to a single shared calorie budget. This is a max‑min / bottleneck optimization, naturally solved by binary search on the answer and a feasibility test.

**Candidate approaches:**
1. **Binary search + DP per vitamin:**  
   - For each vitamin type `t = 1,2,3`, build a DP `dp[t][v] = min calories to get at least v units of vitamin t`.  
   - DP is a 0/1 knapsack on the items of that type: weight = calories, value = vitamin amount.  
   - `mid` is feasible iff there exist calorie splits `c1,c2,c3` (one per DP) such that `c1 + c2 + c3 ≤ X` and each `dp[t][mid] ≤ c_t` is achievable.  
   - Since we only need the minimum calories for each possible total, we can keep a 1‑D array of size `mid` and after DP take the suffix minimum.  
2. **Triple nested enumeration:**  
   - Enumerate `c1` over achievable calories for vitamin 1 (from its DP), and for each, binary search in vitamin 2's achievable calories to see if the remaining budget can cover vitamin 3.  
3. **Treat as a multi‑constraint knapsack** directly – would be 3‑dimensional DP, too heavy.

**Why the DP‑per‑vitamin + binary search is chosen:**  
- `N,X ≤ 5000`, but vitamin amounts go up to `2·10⁵`. A DP over calorie budget (≤ 5000) per vitamin is cheap.  
- For a given `mid`, we only need DP up to `mid` per type, costing `O(N·mid)` per type, `O(N·mid)` total per check.  
- With `mid` binary searched over `[0, 2·10⁵]`, worst case ~18 checks → ~ `18·N·2e5` operations, which in Python can be heavy but is manageable because the inner DP only iterates over the items of that specific vitamin type and stops at `mid`.  
- N is small (5000), so the constant factor is okay.

**Pitfalls to watch out for:**
- **Large `mid` leading to huge DP arrays:** Need to cap the DP array size to `mid` (not full vitamin sum).
- **DP initialization:** `dp[0] = 0`, others = `INF` (e.g., `X+1` or a large int).
- **Suffix minimum:** After DP, for any required total `mid`, we need the minimum calories among all totals ≥ `mid`. Compute suffix min: `for v from mid-1 down to 0: dp[v] = min(dp[v], dp[v+1])`.
- **Triple loop / nested search efficiency:**  
  - The naive `O(mid²)` loop over `c1,c2` per check is too slow.  
  - Instead, for each achievable calorie `c1` for vitamin 1, we need the smallest `c2` for vitamin 2 such that `c1 + c2 ≤ X - c3_min`, where `c3_min = dp3[mid]`.  
  - We can precompute a boolean or min‑calorie array for each vitamin (e.g., `min_cal1[v] = min calories to get exactly v` or at least v). For vitamin 2, we need for each total calorie budget the minimum vitamin achievable, or vice versa.  
  - A simpler route: For each vitamin, keep a sorted list of pairs `(calories_spent, min_vitamin_at_least_mid)`? Actually, for a given `mid`, `dp[t][v]` for `v ≥ mid` after suffix becomes non‑increasing. We only need the set of possible calorie expenditures that achieve at least `mid` for that vitamin.  
  - The classic solution (used in many editorial solutions) does a triple loop: iterate `c1` over all `0..X`, if `c1` can achieve ≥ mid for vitamin 1, then iterate `c2` over `0..X-c1`, if achievable for vitamin 2, then check if the remaining calories `X - c1 - c2` is ≥ the minimum calories needed for vitamin 3 to reach `mid`.  
  - To make the inner loop fast, we can precompute for each calorie `c` whether vitamin 2 can achieve ≥ mid. That's just a boolean array `ok2[c]`. Then the total check per `mid` is `O(X²)` in worst case (25 million), which is okay because `X ≤ 5000` → 25M per check, times ~18 checks = 450M, borderline but might pass in PyPy with optimizations.  
  - However, we can do better: since `N ≤ 5000`, the number of distinct calorie values achievable for each vitamin is at most `N_t` (items of that type). So we can enumerate only achievable calorie pairs. For each achievable calorie `c1` in the set of vitamin 1 DP results, for each achievable `c2` in vitamin 2 DP results, check the remaining budget. The number of such pairs is at most `N1 * N2` ≤ 25M, but in practice much less. Still, using boolean arrays and iterating `c1` from 0..X and `c2` from 0..X-c1 is simpler and likely fast enough.

**Better feasibility test (chosen approach):**
1. For each vitamin `t`, compute `dp_t[0..mid]` where `dp_t[v]` = min calories to get exactly `v` (or at least v). Initialize `dp_t[0] = 0`, others = INF.
2. For each item of type `t` with vitamin `a` and calorie `c`:
   - For `v` from `mid` down to `a`: `dp_t[v] = min(dp_t[v], dp_t[v-a] + c)`.
3. After processing all items of type `t`, compute suffix minimum: for `v = mid-1 ... 0`: `dp_t[v] = min(dp_t[v], dp_t[v+1])`.
4. Now `dp_t[mid]` is the minimum calories needed to get at least `mid` of vitamin `t`. (After suffix, `dp_t[v]` means min calories to get at least `v`.)
5. Feasibility: if `dp_1[mid] + dp_2[mid] + dp_3[mid] ≤ X`, then certainly feasible (just take the optimal sub‑solution for each). But this is a **necessary** condition, not sufficient, because we could spend more on one vitamin to allow less on another, but the minimum sum test is actually sufficient if we can freely combine? Wait—careful: The DP for each vitamin is independent, so the total minimum calories to get `mid` of each is exactly `sum(dp_t[mid])`. If that sum ≤ X, then we can simply take the optimal subset for each vitamin (they are disjoint sets of items? No, items have a unique vitamin type, so the subsets for different vitamins are disjoint! Because each item gives exactly one vitamin. So there is no conflict!  
   - Indeed, since each item belongs to exactly one vitamin type, the three subproblems are on disjoint item sets. Therefore, the minimum total calories to achieve at least `mid` for all three is exactly the sum of the three individual minima. There is no trade‑off between vitamins; we just pick optimal subsets for each independently.  
   - This means the feasibility check simplifies dramatically: compute `need_t = dp_t[mid]` for each type (after suffix). If `need_1 + need_2 + need_3 ≤ X`, then `mid` is achievable; otherwise not.

**Why is this correct?**  
Because items are partitioned by vitamin type. The decision for vitamin 1 does not affect what is available for vitamins 2 or 3. The total calories is the sum of calories used by the chosen subset for each type. To minimize total calories while achieving `mid` for each, we independently minimize calories for each type. The sum of independent minima is the global minimum. So the binary search check is just a sum check.

**Wait—double check with sample 1:**  
- mid = 3.  
- Vitamin 1: items: (8,5). To get ≥3, need 5 calories.  
- Vitamin 2: items: (3,5), (7,10). To get ≥3, need 5 calories.  
- Vitamin 3: items: (2,5), (3,10). To get ≥3, need 10 calories.  
- Sum = 5+5+10 = 20 ≤ 25 → feasible. Answer at least 3.  
- mid = 4:  
  - Vitamin 1: need 5.  
  - Vitamin 2: min calories to get ≥4? Items give 3 and 7. To get 7 need 10. Sum 7 ≥ 4, so 10. Or 3+? Only two items, total 10, gives 10 units. So need 10.  
  - Vitamin 3: items 2 and 3, total 5, max 5 ≥ 4, need 15 calories (both).  
  - Sum = 5+10+15 = 30 > 25 → infeasible. Answer 3. Matches sample.

**Great—this simplifies everything to three independent knapsacks per check.**

**Complexities:**  
- For a given `mid`, we do 3 DPs, each over `mid` capacity and processing items of that type.  
- Time per check: `O(N * mid)` (since each item is processed once and we loop up to `mid`).  
- With `N ≤ 5000`, `mid` up to `2e5`, worst case per check `10^9`? No, because we only loop `v` from `mid` down to `a` for each item, and `a` could be large, but still each item may touch up to `mid` states. In worst case `5000 * 2e5 = 10^9`, which is too much.  
- However, we can early stop: `mid` is binary searched, and the DP per vitamin only needs to consider totals up to `mid`. The number of items per vitamin is at most `N`, and the vitamin amount per item is up to `2e5`. The DP inner loop is over `v` from `mid` down to `a_i`. In the worst case, if many items have small `a_i`, the total work is `O(N * mid)`. With `mid` around `1e5` and `N=5000`, that's `5e8`, which is too slow.  
- **Optimization:** We can cap the DP size per vitamin to the total sum of vitamins of that type, but that's what `mid` is. Actually, since `mid` could be up to `2e5`, and N is 5000, the average vitamin per item is large? Not necessarily.  
- **Alternative DP dimension:** Since calories `C_i ≤ X ≤ 5000`, we can do DP on calories instead of vitamin! For each vitamin type, we want the maximum vitamin achievable with at most `c` calories. Then for a given `mid`, we need the minimum calories `c` such that `max_vitamin[c] ≥ mid`. This DP is over calorie budget (≤ 5000) and processes N items, total `O(N * X) = 5000 * 5000 = 2.5e7` per check, times 18 checks = 4.5e8, still a bit high but manageable in PyPy with optimizations (using array of size X+1).  
- **Even better:** Precompute the full DP for each vitamin type once (not per mid). Compute `max_vit[t][c]` = maximum vitamin of type `t` achievable with ≤ c calories. This DP is independent of `mid`. Then for binary search, for a given `mid`, we just need the minimum `c` such that `max_vit[t][c] ≥ mid`. This is a simple scan over `c` from 0 to X, or we can precompute for each `t` a list of (calorie, vitamin) pairs and binary search.  
- This precomputation costs `O(N * X)` total (3 * 5000 * 5000 = 7.5e7), which is fine. Then each binary search step is O(X) per vitamin (3*X = 15000), times log(2e5) ~ 18 → ~ 270k operations. Excellent.

**Refined plan:**
1. Read input.  
2. Partition items into three lists: `items[t] = list of (vitamin_amount, calories)`.  
3. For each `t` in 1..3, compute `max_vit[t]` as an array of size `X+1` (indices 0..X).  
   - Initialize `max_vit[t][c] = 0` for all c.  
   - For each item (a, c) in items[t]: for `budget` from `X` down to `c`: `max_vit[t][budget] = max(max_vit[t][budget], max_vit[t][budget - c] + a)`.  
   - After processing all items, make it non‑decreasing: for `c` from 1 to X: `max_vit[t][c] = max(max_vit[t][c], max_vit[t][c-1])`.  
   - This gives: with calorie budget exactly `c`, the max vitamin you can get is `max_vit[t][c]`; with ≤ c, also `max_vit[t][c]` after the prefix max.  
4. For a given candidate `mid`, find `need_t` = the smallest `c` in `0..X` such that `max_vit[t][c] ≥ mid`. If none, set `need_t = X+1` (infeasible).  
5. If `need_1 + need_2 + need_3 ≤ X`, then `mid` is feasible.  
6. Binary search `mid` over `[0, 2e5]` (or higher, but `2e5` is safe upper bound). Return the largest feasible `mid`.

**Edge cases:**
- If no items of a certain vitamin type exist, then `max_vit[t][c] = 0` for all c. So the minimum intake is capped at 0. The answer could be 0 (as in sample 2, no vitamin 3).  
- The binary search upper bound can be the maximum possible minimum vitamin. Since each vitamin amount ≤ 2e5, and we can take all items, the max vitamin per type is sum of its items' vitamins. The minimum of the three sums is an upper bound. Or simply use `2e5` as a safe constant.

**Complexity:**  
- Precomputation: `O(3 * N * X) = O(N*X) = 2.5e7` operations, each is a simple max assignment. In Python, this might be near the limit but with PyPy and using built‑in lists should be okay. We can micro‑optimize by using local variables and maybe `array` or just list.  
- Binary search: `O(log(M) * 3 * X)` = `O(18 * 15000)` = 270k, negligible.  
- Total ~2.5e7 + small. Should run in under 2 seconds in PyPy.

**Potential micro‑optimizations:**  
- For each vitamin type, we can break early in the inner DP loop if the calorie `c_i > X`? No, `c_i ≤ X` guaranteed.  
- We can store items per type and iterate.  
- Use `range(X, c-1, -1)` for the inner loop.  
- The DP arrays can be lists of ints. We can reuse the same array for each type? No, need separate results.

**Memory:**  
- Three arrays of size X+1 (≤ 5001) each → trivial.

**Final algorithm outline:**
```
read N, X
items = {1:[], 2:[], 3:[]}
for i in range(N):
    read V, A, C
    items[V].append((A, C))

max_vit = [None, arr1, arr2, arr3]  # 1-indexed
for t in [1,2,3]:
    dp = [0]*(X+1)
    for a, c in items[t]:
        for b in range(X, c-1, -1):
            val = dp[b-c] + a
            if val > dp[b]:
                dp[b] = val
    # prefix max
    for c in range(1, X+1):
        if dp[c] < dp[c-1]:
            dp[c] = dp[c-1]
    max_vit[t] = dp

def feasible(mid):
    total_need = 0
    for t in [1,2,3]:
        # find min c s.t. max_vit[t][c] >= mid
        # max_vit[t] is non-decreasing
        # can use bisect_left on a list of (c, vit) but it's an array
        # linear scan is fine (X=5000)
        need = X+1
        # simple loop
        for c in range(X+1):
            if max_vit[t][c] >= mid:
                need = c
                break
        total_need += need
        if total_need > X:
            return False
    return total_need <= X

lo, hi = 0, 200000  # or sum of vitamins
while lo < hi:
    mid = (lo + hi + 1) // 2
    if feasible(mid):
        lo = mid
    else:
        hi = mid - 1
print(lo)
```

**Potential improvement for `feasible`:**  
- Precompute for each `t` the minimal calorie needed for each `mid`? No, we don't know `mid` in advance. But we can make the inner scan faster by precomputing a list of (calorie, vitamin) frontier? The DP array is size 5000, scanning 5000 three times is 15000 per check, times 18 = 270k, trivial. So linear scan is fine.

**Testing with sample 1:**
- N=5, X=25.  
- After DP:
  - t=1: items [(8,5)]. dp[5]=8, others 0. Prefix: dp[0..4]=0, dp[5..25]=8.  
  - t=2: items [(3,5),(7,10)]. dp:  
    - init 0.  
    - item (3,5): for b=25..5: dp[b]=3.  
    - item (7,10): for b=25..10: val = dp[b-10]+7. If b-10 ≥5, dp[b-10]=3 → val=10. If b-10<5, dp[b-10]=0 → val=7. So dp[10..14]=7, dp[15..25]=10.  
    - Prefix: dp[0..4]=0, dp[5..9]=3, dp[10..14]=7, dp[15..25]=10.  
  - t=3: items [(2,5),(3,10)]. dp:  
    - item (2,5): for b=25..5: dp[b]=2.  
    - item (3,10): for b=25..10: val = dp[b-10]+3. b-10≥5 → dp=2 → val=5. b-10<5 → 0+3=3. So dp[10..14]=3, dp[15..25]=5.  
    - Prefix: dp[0..4]=0, dp[5..9]=2, dp[10..14]=3, dp[15..25]=5.  
- feasible(3): t1: c=5 (vit=8≥3). t2: c=5 (vit=3≥3). t3: c=15 (vit=5≥3). sum=5+5+15=25 ≤ 25 → true.  
- feasible(4): t1: c=5 (8≥4). t2: c=15 (10≥4). t3: c=20 (5≥4? dp[20]=5≥4 yes). sum=5+15+20=40 > 25 → false.  
- Answer 3. Good.

**Sample 2:**  
- N=2, X=5000. items 1: [(200000,1)], 2: [(200000,1)], 3: [].  
- max_vit[3] = all zeros.  
- feasible(mid) for mid>0: t1 need=1, t2 need=1, t3 need=5001 (since never ≥ mid). total >5000 → false. So answer 0. Good.

**Edge case:** What if `mid` is larger than any achievable vitamin for a type? Then `need = X+1`, total > X, infeasible. The linear scan will fall through the loop without finding, so `need` stays `X+1`. Correct.

**Upper bound for binary search:**  
- We can compute the total vitamin per type. Let `sum_vit[t]` = sum of `A` for items of type `t`. The maximum possible minimum is `min(sum_vit[1], sum_vit[2], sum_vit[3])`. But we also need to respect calorie limit. So upper bound is `min(sum_vit[t])` and also not exceeding the max vitamin achievable with X calories. Actually, the DP already gives the max vitamin with X calories: `max_vit[t][X]`. So the global upper bound is `min(max_vit[t][X])`. Using this as `hi` makes binary search tighter. But `2e5` is small enough anyway.

**Final check on time:**  
- `N*X = 5000*5000 = 2.5e7`. In Python, a loop of 25 million with simple operations is fine (usually < 1 sec in PyPy). We have 3 types, so 75 million operations. Might be around 2-3 seconds. Acceptable.  
- We can micro-opt: convert items to separate lists of calories and vitamins for each type, and use local variable references. Or use `array('i')`? Not needed.  
- We can also note that we only need DP up to the smallest calorie that can achieve the max? No, the DP must be over full X because we need the prefix max. But the inner loop `for b in range(X, c-1, -1)` is necessary for 0/1 knapsack.

**Alternative to speed up:**  
- Since we only care about the maximum vitamin for each calorie budget, and items have unique types, we can do the DP for all items together but track three separate vitamins? That would be 3D DP, too big. So separate is fine.

**One more optimization:**  
- The DP for each type can be done with a list of length X+1. The inner loop is `for b in range(X, c-1, -1): new = dp[b-c] + a; if new > dp[b]: dp[b] = new`.  
- In Python, we can write it as:  
  ```
  for b in range(X, c-1, -1):
      v = dp[b-c] + a
      if v > dp[b]:
          dp[b] = v
  ```
  This is standard.

**Memory layout:**  
- `max_vit` is a list of 3 lists (index 0 unused).  
- `items` is a list of 3 lists.

**Potential bug:**  
- The prefix max step ensures that `max_vit[t][c]` = max vitamin achievable with ≤ c calories. But in the inner loop we update `dp[b]` for exact budget b. After processing all items, `dp[b]` is the max vitamin with exact calorie b (or unused calories? No, in knapsack with calorie as weight, `dp[b]` is the max value with total weight exactly b? Actually, if we use `dp[b] = max(dp[b], dp[b-c] + a)`, and we initialize `dp[0]=0` and others 0, then `dp[b]` will be the max vitamin achievable with total calories exactly b? No, it can be ≤ b if we don't use all calories. Wait, in standard 0/1 knapsack with weight = calories, `dp[b]` is the max value with total weight exactly b if we consider all combinations, but we can also choose not to fill exactly. The standard initialization with `dp = [0]*(X+1)` and then for each item: for b from X down to c: dp[b] = max(dp[b], dp[b-c]+a) results in `dp[b]` being the max value with total weight exactly b? Actually, no. Because we only update `dp[b]` from `dp[b-c]`, which could be from a partial fill. The standard knapsack DP for "max value with weight at most W" uses exactly this recurrence with `dp[0..W]` and `dp[b]` meaning the max value with total weight exactly b? Let's recall:  
  - In the 0/1 knapsack, we often define `dp[w]` = max value with total weight exactly w, or at most w?  
  - The recurrence `dp[w] = max(dp[w], dp[w - weight] + value)` with initialization `dp[0..W] = 0` and processing items in 0/1 manner results in `dp[w]` being the maximum value achievable with total weight **at most** w? No, that's not right. The standard interpretation: after processing all items, `dp[w]` is the max value with total weight exactly w if we can leave some items unused. But the recurrence only builds exact totals. However, because we initialize all `dp[w] = 0`, and an empty set gives value 0 for weight 0, but for `w > 0` the empty set gives 0 only if we consider weight exactly 0. For `w > 0`, `dp[w]` will be 0 if no combination sums to exactly w. To get "at most w", we need to take `max(dp[0..w])`. That's why we do the prefix max: after DP, we take `dp[w] = max(dp[w], dp[w-1])` to make it the best with weight ≤ w. So the prefix max is necessary.

**So the algorithm is solid.**

**Let's double-check the DP correctness for "exact" vs "at most":**  
- Example: X=10, one item (vitamin 5, calorie 3).  
- After processing: dp[3]=5, others 0.  
- Prefix max: dp[0..2]=0, dp[3..10]=5.  
- Correct: with 10 calories, we can spend 3 and get 5 vitamins. So max vitamin with ≤10 calories is 5. Good.  
- Another: two items (5,3) and (7,4). X=10.  
- Process (5,3): dp[3]=5, dp[4..10] still 0.  
- Process (7,4): for b=10..4: dp[b] = max(dp[b], dp[b-4]+7).  
  - b=4: dp[0]+7=7 > 0 → dp[4]=7.  
  - b=5: dp[1]+7=7 > 0 → dp[5]=7.  
  - b=6: dp[2]+7=7 > 0 → dp[6]=7.  
  - b=7: dp[3]+7=5+7=12 > 0 → dp[7]=12.  
  - b=8: dp[4]+7=7+7=14 → dp[8]=14.  
  - b=9: dp[5]+7=7+7=14 → dp[9]=14.  
  - b=10: dp[6]+7=7+7=14 → dp[10]=14.  
- Prefix max: dp[0..2]=0, dp[3]=5, dp[4..6]=7, dp[7]=12, dp[8..10]=14.  
- Check: with 10 calories, we can take both (3+4=7 calories, 12 vitamins) and have 3 calories left unused. The DP gives 14? Wait, 5+7=12, not 14. Why did dp[8..10] become 14? Because dp[4]=7 (from the second item alone), then dp[8] = dp[4]+7 = 7+7=14? That's using the second item twice! That's a bug in the 0/1 knapsack logic if we process items in a way that allows reuse.  
- Ah! In 0/1 knapsack, we must iterate `b` from high to low to prevent reusing the same item. I did `for b in range(X, c-1, -1)`, which is correct (high to low). Let's re-evaluate:  
  - Process (5,3) first: dp[3]=5, dp[4..10]=0.  
  - Process (7,4): for b from 10 down to 4: dp[b] = max(dp[b], dp[b-4] + 7).  
  - At b=4: dp[0]=0 → 0+7=7. dp[4] becomes 7.  
  - At b=5: dp[1]=0 → 7. dp[5]=7.  
  - At b=6: dp[2]=0 → 7. dp[6]=7.  
  - At b=7: dp[3]=5 (from first item) → 5+7=12. dp[7]=12.  
  - At b=8: dp[4] is now 7 (updated at this step? But we are iterating downwards. At b=8, we look at dp[8-4]=dp[4]. dp[4] was just updated to 7 in the same item processing? No, because we are going from high to low: b=10,9,8,...,4. So at b=8, we look at dp[4]. But dp[4] has already been updated to 7 at b=4? Wait, the order is b=10, then 9, then 8, then 7, then 6, then 5, then 4. So when we are at b=8, we haven't yet processed b=4. dp[4] is still 0 from initialization (before this item) or from previous items? After processing the first item (5,3), dp[3]=5, others 0. So dp[4]=0. So at b=8, dp[4] is 0, so dp[8] becomes 0+7=7.  
  - Let's re-evaluate step by step for b=8:  
    - b=10: dp[6]=0 → 7. dp[10]=7.  
    - b=9: dp[5]=0 → 7. dp[9]=7.  
    - b=8: dp[4]=0 → 7. dp[8]=7.  
    - b=7: dp[3]=5 → 12. dp[7]=12.  
    - b=6: dp[2]=0 → 7. dp[6]=7.  
    - b=5: dp[1]=0 → 7. dp[5]=7.  
    - b=4: dp[0]=0 → 7. dp[4]=7.  
  - So dp becomes: dp[0..2]=0, dp[3]=5, dp[4]=7, dp[5]=7, dp[6]=7, dp[7]=12, dp[8]=7, dp[9]=7, dp[10]=7.  
  - Prefix max: dp[0..2]=0, dp[3]=5, dp[4]=7, dp[5]=7, dp[6]=7, dp[7]=12, dp[8]=12, dp[9]=12, dp[10]=12.  
  - Correct! The maximum vitamin with ≤10 calories is 12 (items 1+2). Good. The 0/1 knapsack with descending loop is correct.

**My earlier mistake was thinking dp[4] was already updated when computing dp[8], but descending order ensures it's not.**

**So the DP is correct.**

**Now, finalizing the solution:**

**Steps:**
1. Read `N, X`.
2. Initialize `items = [[], [], [], []]` (index 1..3).
3. Loop `N` times, read `V, A, C`, append `(A, C)` to `items[V]`.
4. For each `t` in 1..3:
   - `dp = [0] * (X + 1)`
   - For `(a, c)` in `items[t]`:
     - For `b` in `range(X, c - 1, -1)`:
       - `val = dp[b - c] + a`
       - If `val > dp[b]`: `dp[b] = val`
   - For `c` in `range(1, X + 1)`:
     - If `dp[c] < dp[c-1]`: `dp[c] = dp[c-1]`
   - Store `dp` in a list `max_vit[t]`.
5. Define function `can(mid)`:
   - `total = 0`
   - For `t` in 1..3:
     - `need = X + 1`
     - Iterate `c` from 0 to X:
       - If `max_vit[t][c] >= mid`: `need = c`; break
     - `total += need`
     - If `total > X`: return False
   - Return `total <= X`
6. Binary search:
   - `lo = 0`, `hi = 0`
   - For `t` in 1..3: `hi = max(hi, max_vit[t][X])` (or just a large number like 200000)
   - Actually, we can set `hi = min(max_vit[t][X] for t in 1..3)`.
   - While `lo < hi`:
     - `mid = (lo + hi + 1) // 2`
     - If `can(mid)`: `lo = mid`
     - else: `hi = mid - 1`
   - Print `lo`.

**Complexity summary:**
- Precomputation: 3 * (N * X) operations. With N,X ≤ 5000, max 75 million simple operations. Might be a bit slow in CPython but fine in PyPy. We can micro-opt by using local variables and maybe a single combined DP? No, separate is fine.
- Each `can(mid)`: 3 * (X+1) scans, ~15000 ops.
- Binary search: ~18 steps → ~270k ops.
- Total: ~75M + 270k. Should be okay.

**Potential further optimization:**  
- We can compute the DP for all three types in one pass? Not really, because they are disjoint. We can just do them sequentially. The constant factor is small. We can also unroll the inner loop? Not needed.  
- We can use `array('i')` from the `array` module for the DP to reduce memory overhead and maybe speed up? `array` is slower for random access than list in CPython, but in PyPy list is fine.  
- We can break early in the DP for a type if the maximum possible vitamin sum is less than the current `mid`? No, the DP is precomputed once, independent of `mid`.

**Edge Cases & Validation:**
- N=0? The constraints say N ≥ 1. So no empty input.
- Items may have `C_i = X` (single item uses all calories). DP handles it.
- Vitamin amounts large, but DP only cares about max achievable, not individual values.
- Binary search `lo, hi` initialization: `hi` can be `max_vit[1][X]`, but we need the global upper bound as the minimum across types. So `hi = min(max_vit[t][X] for t in 1..3)`. This is tight and correct. If a type has no items, `max_vit[t][X] = 0`, so `hi = 0`, answer 0. Good.
- What if `hi` is 0 initially? Then loop doesn't run, print 0. Correct.

**Testing more cases:**
- Case: N=1, X=5, item (1,10,5). max_vit[1][5]=10, others 0. hi = min(10,0,0)=0. Answer 0. Correct because no vitamins 2 and 3.
- Case: N=3, each type one item with vitamin 5, calorie 5. X=15. max_vit[t][5]=5, [10]=5? No, only one item per type, so max_vit[t][10]=5, [15]=5. For mid=5, need_t: t1: c=5, t2:5, t3:5, sum=15 ≤15 → feasible. Answer 5. For mid=6, need_t: for t1, max is 5, so need=X+1=16 > X, infeasible. Answer 5. Correct.
- Case: multiple items to combine. Should work.

**Potential integer overflow:** A_i up to 2e5, N=5000, sum up to 1e9. Fits in Python int (arbitrary precision). dp values can be up to 1e9. No problem.

**Final code structure:**
```python
import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[] for _ in range(4)]
    for _ in range(N):
        V, A, C = map(int, input().split())
        items[V].append((A, C))
    
    max_vit = [None] * 4
    for t in range(1, 4):
        dp = [0] * (X + 1)
        for a, c in items[t]:
            # loop descending
            for b in range(X, c - 1, -1):
                val = dp[b - c] + a
                if val > dp[b]:
                    dp[b] = val
        # prefix max to make it "at most"
        for c in range(1, X + 1):
            if dp[c] < dp[c - 1]:
                dp[c] = dp[c - 1]
        max_vit[t] = dp
    
    # binary search
    lo = 0
    hi = min(max_vit[t][X] for t in range(1, 4))
    # hi could be 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        feasible = True
        for t in range(1, 4):
            # find min c s.t. max_vit[t][c] >= mid
            # max_vit[t] is non-decreasing, so linear scan
            # we can speed up by storing the first index for each value? Not needed.
            # but we can precompute an array 'min_cal_for_vit' for each t? No.
            # We can use a while loop.
            need = X + 1
            # manual unroll? not needed
            arr = max_vit[t]
            # linear scan
            # For speed, we can use a for loop with break
            for c in range(X + 1):
                if arr[c] >= mid:
                    need = c
                    break
            total += need
            if total > X:
                feasible = False
                break
        if feasible:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

**Micro-optimizations for the inner scan in `can`:**  
- The DP arrays are small (5001). A Python for loop with range and break is fast. But we call it ~18 * 3 = 54 times, each scanning up to 5000 → 270k iterations. Negligible.  
- We could precompute a dictionary or list of (mid, min_cal) but not needed.

**Potential improvement for the DP precomputation:**  
- The inner loop `for b in range(X, c-1, -1)` is the main cost. We can try to vectorize with numpy? Not allowed in standard AtCoder.  
- We can combine the three DPs? No.  
- We can note that if `items[t]` is empty, skip the loop (dp remains all zeros). Good.  
- We can also break early if `c > X`? Already guaranteed `C_i ≤ X`.  
- We can use local variables to avoid attribute lookups: `dp_local = dp; for b in range...: val = dp_local[b-c] + a; if val > dp_local[b]: dp_local[b] = val`. This is a known micro-opt.

**Let's write the final code with these micro-opts:**
```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    items = [[] for _ in range(4)]
    for _ in range(N):
        V = int(next(it))
        A = int(next(it))
        C = int(next(it))
        items[V].append((A, C))
    
    max_vit = [None] * 4
    for t in range(1, 4):
        dp = [0] * (X + 1)
        item_list = items[t]
        for a, c in item_list:
            # c is calories, must be <= X
            for b in range(X, c - 1, -1):
                val = dp[b - c] + a
                if val > dp[b]:
                    dp[b] = val
        # prefix max
        for c in range(1, X + 1):
            if dp[c] < dp[c - 1]:
                dp[c] = dp[c - 1]
        max_vit[t] = dp
    
    lo = 0
    hi = min(max_vit[t][X] for t in range(1, 4))
    # If hi is 0, loop skipped
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        feasible = True
        for t in range(1, 4):
            arr = max_vit[t]
            # find first index where arr[c] >= mid
            # arr is non-decreasing
            # Use a simple loop
            need = X + 1
            # we can iterate from 0 to X
            # but we know arr[X] < mid might happen, then need stays X+1
            for c in range(X + 1):
                if arr[c] >= mid:
                    need = c
                    break
            total += need
            if total > X:
                feasible = False
                break
        if feasible:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

**Using `sys.stdin.buffer.read()` is faster for large N.**  
**Check the DP logic with the earlier tricky example:**  
- X=10, items (5,3) and (7,4).  
- Code:  
  - t=2: item_list = [(5,3), (7,4)]  
  - First (5,3): for b=10..3: dp[7]=5, dp[8]=5, dp[9]=5, dp[10]=5.  
  - Second (7,4): for b=10..4:  
    - b=10: dp[6]=0 → val=7, dp[10]=max(5,7)=7.  
    - b=9: dp[5]=0 → 7, dp[9]=7.  
    - b=8: dp[4]=0 → 7, dp[8]=7.  
    - b=7: dp[3]=5 → 12, dp[7]=12.  
    - b=6: dp[2]=0 → 7, dp[6]=7.  
    - b=5: dp[1]=0 → 7, dp[5]=7.  
    - b=4: dp[0]=0 → 7, dp[4]=7.  
  - Prefix: dp[0..2]=0, dp[3]=5, dp[4]=7, dp[5]=7, dp[6]=7, dp[7]=12, dp[8]=12, dp[9]=12, dp[10]=12.  
- Correct.

**One more check: What if there are multiple items of the same type with the same calories?**  
- Fine, 0/1 knapsack handles it.

**What if the same item appears multiple times?** Not in input.

**Time complexity re-evaluation:**  
- The DP inner loop is `X - c + 1` for each item. Sum over items is roughly `N * X` in worst case. With N=5000, X=5000, that's 25 million per type, 75 million total. In Python, 75 million simple operations (a few integer additions and comparisons) might take around 1-2 seconds in PyPy. AtCoder's time limit is usually 2 sec. This should be okay, but we need to be careful.  
- We can optimize by noting that we only need DP up to the sum of vitamins? No, the DP is over calories, not vitamins. The calorie limit X is small (5000), so the DP size is small. The number of items is 5000, but the inner loop length is X. So total operations = N * X = 25M per type? Wait, per type the number of items is at most N, but the inner loop is over X, not over the number of items. So for each item, we do X iterations. So it's indeed N * X per type.  
- If N=5000, X=5000, that's 25,000,000 iterations per type. Each iteration does a couple of operations. 75M iterations total. In PyPy, this is typically around 1.5 seconds. In CPython, maybe 3-4 seconds. The problem likely expects PyPy. We can try to reduce the constant factor.  
- One idea: The DP is a standard 0/1 knapsack. We can process items in groups? No.  
- We can use the `array` module with type 'i' or 'l'? Not faster.  
- We can use Cython? No.  
- We can observe that the DP only depends on the maximum calorie. Since X ≤ 5000, we can use a list of length X+1. The inner loop is the bottleneck.  
- We can unroll the loop or use `while` with manual decrement? Not much difference.  
- We can skip the DP for types with no items (already do).  
- We can skip items with `c > X`? Not possible.  
- We can note that the total number of items is 5000, but distributed among 3 types. The worst case is all 5000 in one type, then DP for that type is 5000*5000=25M, the others 0. So 25M total. That's very fast! 25M iterations in Python is about 0.5-1 sec. If items are spread, say 1666 each, then 3 * 1666 * 5000 = 25M as well. So the total is always bounded by N * X = 25M. Wait, is it? For each type, it's (number of items of that type) * X. Sum over types = (N1+N2+N3)*X = N*X = 25M. Yes! Because each item belongs to exactly one type, and the inner loop length is always X (since we iterate over all possible calorie budgets for that item). So the total work across all three DPs is exactly N * X. N=5000, X=5000 → 25 million iterations. Each iteration is a few integer ops. In Python, 25M iterations is very fast (under 1 second) in PyPy. I mistakenly thought it was N*X per type, but it's N_t * X per type, sum N_t = N. So total 25M. Excellent! This is definitely fast enough.

**Thus the solution is efficient and correct.**

**One final check:**  
- The binary search upper bound `hi = min(max_vit[t][X] for t in 1..3)`. If a type has no items, `max_vit[t][X] = 0`, so `hi = 0`. Then while loop doesn't execute, answer 0. Good.  
- If `hi` is 0, the loop `while lo < hi` is false, print 0. Good.  
- The feasible function: if `mid = 0`, then `need = 0` for all (since `arr[0] = 0 >= 0`). So total = 0 ≤ X, always feasible. So answer at least 0. Binary search will work.

**All good.**

**Let's write the final code.**</mm:think>### NOTES
**Core difficulty:** Maximize the minimum of three independent vitamin totals under a shared calorie limit. This is a max‑min / bottleneck optimization.

**Key insight:** Because each food provides exactly one vitamin type, the three subproblems (choosing foods for vitamin 1, 2, 3) are on **disjoint** item sets. Thus the total calories used is the sum of the calories used for each vitamin, and the minimum total calories to reach a target `mid` for all three is simply the sum of the three independent minima. There is no trade‑off between vitamins.

**Candidate approaches:**
1. **Binary search on the answer + per‑vitamin 0/1 knapsack on calories:**  
   - For each vitamin type, compute the maximum vitamin achievable with exactly `c` calories (0/1 knapsack, weight = calories, value = vitamin). Convert to “at most `c`” with a prefix max.  
   - For a candidate `mid`, find the minimum calories needed for each type to reach `mid` (linear scan over the DP array). Sum them. If the sum ≤ X, `mid` is feasible.  
   - This works because items are disjoint, so independent minima sum to the global minimum.
2. **DP over vitamin amounts:** Would need large arrays (vitamin sum up to 10⁹) and is unnecessary.
3. **Triple‑nested enumeration of calorie splits:** Works but O(X²) per check and more complex.

**Why approach 1 is chosen:**  
- N, X ≤ 5000, so the per‑vitamin knapsack DP on calorie budget costs O(N·X) total across the three types (each item is processed once, inner loop over X). With N=5000, X=5000, that's 25 million simple operations — easily fast enough in PyPy.  
- The feasibility check per `mid` is just three linear scans over size X (≈ 5000), negligible.  
- Binary search adds a log factor (~18).

**Pitfalls to watch:**
- The knapsack DP gives the max vitamin for **exact** calorie usage; must take a prefix max to get “at most”.
- The DP must use a descending loop to enforce 0/1 (no item reuse).
- If a vitamin type has no items, the DP stays all zeros → minimum intake is 0.
- The binary search upper bound can be the minimum across the three types of the max vitamin achievable with X calories (tight bound).

**Correctness sketch:**  
- For a fixed `mid`, the minimum calories to get at least `mid` of vitamin `t` is `need_t`. Because item sets are disjoint, any feasible selection of foods is a union of selections for each vitamin, with total calories = sum of per‑vitamin calories. The minimum total calories is therefore `need_1 + need_2 + need_3`. If this sum ≤ X, we can simply take the optimal subset for each vitamin independently and meet the budget. Conversely, if the sum > X, no selection can beat the sum of independent lower bounds, so `mid` is infeasible.

## worker: Implement the final Python solution according to t
- Partitioned foods by vitamin type; each type's items are disjoint, so the three subproblems are independent.
- For each vitamin type, ran a 0/1 knapsack on calorie budget (weight = calories, value = vitamin amount) to get the maximum vitamin achievable with exactly `c` calories, then took a prefix max to obtain the maximum with **at most** `c` calories.
- The feasibility check for a candidate `mid` finds, for each type, the smallest calorie budget that yields at least `mid` vitamin (linear scan over the size‑X array). Because the item sets are disjoint, the global minimum total calories is the sum of the three independent minima. If that sum ≤ X, `mid` is achievable.
- Binary searched `mid` over `[0, min_t max_vit[t][X]]`. The upper bound is tight and handles cases where some vitamin type has no items (answer 0).
- Complexity: precomputation O(N·X) ≤ 25 M operations; each feasibility check O(X); binary search adds a log factor. Easily fits within limits.

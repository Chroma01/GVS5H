
## ideation
We need to maximize the minimum intake among the three vitamins, with the constraint that total calories ≤ X. Each food contributes to exactly one vitamin. The natural approach is binary search on the answer M: check whether we can achieve at least M units of each vitamin within the calorie budget.

For a fixed M, we need to determine the minimum calories required to collect ≥ M units of each vitamin, using foods of that vitamin only. Since each food is 0/1 (take or not), this is a knapsack subproblem: minimize cost (calories) for a given total vitamin value (≥ M). For each vitamin type, we can run a DP over vitamin amount up to M, with dp[v] = minimum calories to achieve exactly v units. Because we only need to know whether we can reach M, we can cap the DP at M: when transitioning, we clamp the new vitamin amount to M. Complexity per DP is O(number of foods of that type × M). With N ≤ 5000 and M up to 2e5, worst case could be 10^9, but in practice M is bounded by the binary search range and the DP only runs for each type. We must be careful to keep the DP efficient; we can limit M to the answer and use early termination, or process each type separately so the total work across the three DPs is O(N × M) where N is split among the three vitamins.

Alternative: DP over calories. Since X ≤ 5000, we could do a knapsack on calories (value = vitamin amounts) to maximize the minimum vitamin. But the minimum function makes it tricky; binary search on M with DP on vitamin amount is more straightforward.

We must also handle the case M=0 (always feasible) and ensure the DP correctly clamps values.

Edge cases: Some vitamin types may have no foods; then M must be 0. The DP for that type returns infeasible (dp[M] stays INF) unless M=0.

Binary search range: low=0, high = max possible sum of A_i per vitamin (or just a large number like 2e5 * 5000? but safer to set high = sum of A_i for each vitamin individually and take the max; actually max possible M is the maximum total of a single vitamin across all its foods, but we can just set high = 2e5 * 5000? No, better to set high = max sum of A_i for any single vitamin, which is at most 5000 * 2e5 = 1e9, which is fine for binary search. But we can also set high = 2e5 (since A_i ≤ 2e5 and N=5000, but the sum could be large). However, binary search with log2(1e9) ≈ 30 steps is fine. Each step does DP of size M+1, which in the worst case could be 1e9? No, because M is the current guess, which decreases as we binary search. In the worst case, we might check M up to 1e9, making DP array huge. We need to bound the DP size more cleverly.

Observation: The DP only needs to track vitamin amounts up to M. If M is large (e.g., 1e9), we cannot allocate an array of size M. However, note that the total number of foods N is only 5000, and each A_i ≤ 2e5. So the maximum achievable vitamin amount for any single vitamin is at most sum of A_i over its foods, which is at most 5000 * 2e5 = 1e9. But we cannot allocate arrays of size 1e9. So we need a different approach when M is large.

We can cap M at the total possible sum for each vitamin. More importantly, we can run the DP but we don't need to allocate an array of size M if M is huge; instead we can use a dictionary (hash map) DP or limit the DP size by the number of items. Since N=5000, the number of distinct reachable vitamin amounts is at most N+1 per type. So we can use a dictionary DP: for each type, we keep a dict mapping vitamin amount to minimum calories. For each food, we update the dict: for each existing amount v, new amount = v + A_i (but we can cap at M if M is small, but if M is huge we don't need to cap because the sum is bounded by N*2e5). Actually we only need to know whether we can reach at least M. So we can keep a dict and prune any v >= M, mapping them to a single sentinel ">=M" with the minimum calories. This way the dict size is O(N). Complexity per DP is O(N^2) in the worst case per type? Actually for each item, we iterate over current dict entries, which grows linearly. So total O(N^2) per type, i.e., 5000^2 = 25e6 per check, times ~30 checks = 7.5e8, too high.

Better: Since each food has cost C_i (calories) and value A_i, we want to minimize calories for given vitamin amount. This is a standard knapsack. With N=5000 and X=5000, we could do DP on calories: for each calorie budget up to X, track the maximum vitamin amount we can get for each type. But we need the minimum intake among three vitamins. Binary search on M: for each type, we need to know the minimum calories to achieve M vitamin units. Since X is only up to 5000, we can do DP on calories for each type: for each type, we want to know for each calorie cost c (0..X) the maximum vitamin amount we can get. Then for a given M, the minimum calories needed for that type is the smallest c such that dp_max_vitamin[c] >= M. We can precompute for each type a DP of size X+1 (5001) which is very fast. Then for each M, we just look up three values and sum them. Binary search over M, each check O(1) after precomputation? But the precomputation depends on M? No, the DP on calories for each type does not depend on M: we compute for all calorie budgets up to X the maximum vitamin amount achievable. Then to check if M is feasible, we find for each type the minimum calorie cost to achieve at least M vitamin units: that is min_{c: dp_vitamin[c] >= M} c. If any type has no such c, then infeasible. Otherwise, sum the three minimal costs; if sum <= X, feasible.

This is much better! Because X ≤ 5000, the DP per type is O(N_k * X) where N_k is the number of foods of that type. N_1+N_2+N_3 = N ≤ 5000. So total DP time is O(N * X) = 5000 * 5000 = 25e6, which is fine. Then binary search over M: we need to be able to quickly answer, for each type, the minimal calories to achieve at least M. We can precompute an array best_cal[M] for M from 0 to max_possible? But max_possible could be up to 1e9. We cannot precompute for all M up to 1e9. However, we can binary search M and for each M perform a linear scan over calorie costs (0..X) to find the first c where dp_vitamin[c] >= M. That's O(X) per check, and O(X log MAX) = 5000 * 30 = 1.5e5, very small. So total complexity is O(N*X + X*log(max_A_sum)) which is excellent.

So the plan:
1. Read N, X.
2. Group foods by vitamin type (1,2,3). For each type, we have a list of (A_i, C_i).
3. For each type k in {1,2,3}, compute an array dp[k] of length X+1, where dp[c] = maximum vitamin amount achievable with exactly c calories (or at most c calories? We'll do "at most" because we can leave unused calories. Standard knapsack: dp[c] = max vitamin amount using calories ≤ c. Initialize dp[0]=0, others = -inf. For each food (A, C) of that type, for c from X down to C: dp[c] = max(dp[c], dp[c-C] + A). After processing all foods, dp[c] is the max vitamin amount with total calories exactly c? Actually with the standard DP (for c from X down to C), dp[c] ends up as the max vitamin amount with total calories exactly c (or at most c if we consider unused calories as not using them; but we can interpret dp[c] as the max vitamin amount with calories exactly c, and we can also allow "not using" by just not updating). To get the max with at most c, we can either after DP take prefix max: for c from 1 to X: dp[c] = max(dp[c], dp[c-1]). Then dp[c] is the max vitamin amount with calories ≤ c. This is what we want: for a given calorie budget, what's the max vitamin we can get. Then to find minimal calories to achieve at least M, we find the smallest c such that dp[c] >= M. If none, return INF.
4. Binary search M: low=0, high = max possible sum of A_i for any single vitamin (or a safe upper bound like 2e5 * N). Actually we can compute the maximum total vitamin for each type: total_A_k = sum of A_i for foods of type k. The answer cannot exceed min(total_A_1, total_A_2, total_A_3). So high = min(total_A_1, total_A_2, total_A_3). But we can just set high = max(total_A_1, total_A_2, total_A_3) and binary search; the check will correctly determine feasibility. But to be safe, high = min(total_A_1, total_A_2, total_A_3) or simply a large number. Since the DP can only give up to total_A_k, we can set high = min(total_A_1, total_A_2, total_A_3) + 1, and binary search on the inclusive range. But note that M can be 0, and if one type has no foods, total_A_k = 0, so answer is 0.
5. For each candidate M, we need to find for each type k: cost_k = min c in [0..X] such that dp_k[c] >= M. If no such c, cost_k = INF. Then if sum(cost_1, cost_2, cost_3) <= X, M is feasible. We can do a simple loop: for c in 0..X, if dp_k[c] >= M, break. Since X=5000, this is fast.
6. Binary search for the maximum feasible M. Since M can be up to 1e9, but we only loop up to X for each check, it's fine. However, we must be careful: if M is larger than any dp_k[c], the loop will go through all X and return INF, which is correct.
7. Return the maximum M.

Edge cases: If for some type k, no foods, then dp_k[0] = 0, and for c>0 dp_k[c] = 0 (or -inf). Actually if no foods, we should set dp_k array such that dp_k[0]=0, and for c>0, dp_k[c] = 0? Wait, if we have no foods, we cannot get any vitamin units regardless of calories. So the max vitamin amount with calories ≤ c is 0. So dp_k[0]=0, dp_k[c]=0 for c>0. In the DP initialization, we set dp[c] = -inf for c>0, but with no items, they remain -inf. After the prefix max (or during initialization), we should handle this. Better: initialize dp array with 0 for all c? But that would imply we can always get 0 vitamin units with any calories, which is correct. Actually the maximum vitamin amount achievable with calories ≤ c is at least 0 (by taking nothing). So we can initialize dp[c] = 0 for all c. That works. But if we use -inf, we need to be careful with the max operation. Let's just initialize dp[c] = 0 for all c. Then the DP update: for each food (A, C), for c from X down to C: dp[c] = max(dp[c], dp[c-C] + A). This is standard for "maximize value with cost C". Since we allow not using any food, dp[c] is at least 0. So after DP, dp[c] is the max vitamin amount achievable with total calories exactly c (or at most c if we take prefix max). Actually with the standard 0/1 knapsack DP, dp[c] is the max value with cost exactly c? No, the standard DP (for c from X down to C) gives dp[c] = max value with cost exactly c? Let's recall: The DP state is dp[c] = max value using cost exactly c? Usually it's defined as the max value using cost at most c. But the standard implementation (c from high to low) computes dp[c] as the max value achievable with cost exactly c, assuming we either take the item or not. However, because we don't force using all calories, dp[c] can be considered as the max value with cost exactly c, but we can also have "unused" calories by simply not picking any item that costs them. But the DP as written (c from high to low) actually computes the max value with cost exactly c if we consider the items as having cost C and value A, and we are allowed to pick each at most once. The recurrence dp[c] = max(dp[c], dp[c-C] + A) ensures that if we don't pick the item, dp[c] remains the value from previous items. But note: dp[c] from previous items might have been computed from a different combination that also exactly costs c? Actually, initially dp[c] = 0 for all c (meaning we can achieve 0 value with cost exactly c by picking no items? But picking no items costs 0, not c. So initializing all dp[c] to 0 is a bit sloppy because it implies we can achieve 0 value with cost c, which is not true for c>0. However, the recurrence doesn't distinguish between "exactly c" and "at most c". Let's think carefully.

Standard 0/1 knapsack for maximum value with weight limit W: dp[w] = maximum value with total weight ≤ w. Initialization: dp[0..W] = 0. For each item (weight, value): for w from W down to weight: dp[w] = max(dp[w], dp[w-weight] + value). This works because dp[w] is the max value with weight ≤ w. The recurrence is valid: if we don't take the item, dp[w] stays the best with weight ≤ w using previous items; if we take the item, we must have dp[w-weight] as the best with weight ≤ w-weight, and then we add value, so total weight is at most w. So dp[w] is indeed the max value with total weight ≤ w. This is the standard approach. So we can just do that. The prefix max step is not needed if we define dp[w] as max value with weight ≤ w. But careful: the recurrence dp[w] = max(dp[w], dp[w-weight] + value) uses dp[w-weight] which is the max value with weight ≤ w-weight. That is exactly the condition we need. So dp[w] is the max value with total calories ≤ w. So we can just use that DP and not do prefix max. However, the recurrence assumes dp[w] is the max value with weight ≤ w, and dp[w-weight] is the max value with weight ≤ w-weight. This is a well-known DP. So we can just use it.

Let's confirm: For each item (cost C, value A), we update w from X down to C: dp[w] = max(dp[w], dp[w-C] + A). Initially dp[0..X] = 0. After processing all items, dp[w] = max total vitamin A we can get with total calories ≤ w. This is correct. So to find the minimal calories to achieve at least M, we find the smallest w such that dp[w] >= M. If no such w, then it's impossible for that type.

But wait: what if we have a combination that uses, say, 7 calories and gives 10 vitamin, and another that uses 3 calories gives 5. Then dp[5] might be 5 (from the 3-calorie item), dp[7] is 10, dp[6] might be 5 (since 6 ≤ 7, the max with ≤6 is 5). That's correct.

So the DP is correct. The complexity is O(X) per item, total O(N*X). With N=5000, X=5000, it's 25 million, which is fine in Python.

Now, for each M, we need to find the smallest w such that dp_k[w] >= M. Since X=5000, we can just loop w from 0 to X. But we can also precompute for each type an array best_for_m: for each possible M up to max_vitamin (which could be up to 1e9), we cannot precompute. So we do the loop. The loop is O(X) per type, so 3*X = 15000 operations per check. With binary search ~32 checks, that's 480,000 operations, trivial.

But we must be careful: the DP for each type only considers foods of that type. So we need to do three separate DPs.

Algorithm steps:
1. Read N, X.
2. Initialize three lists: items1, items2, items3.
3. For i in 1..N: read V, A, C. Append (A, C) to the corresponding list.
4. For each k in [1,2,3], run knapsack DP:
   dp = [0] * (X+1)
   for (A, C) in items_k:
       for w in range(X, C-1, -1):
           if dp[w-C] + A > dp[w]:
               dp[w] = dp[w-C] + A
   Store dp in an array dps[k-1] = dp.
5. Determine the maximum possible M. The answer cannot exceed the total vitamin available for any type, but also we can just set high = min(sum of A in each type). Actually we can set high = min(total_A_1, total_A_2, total_A_3). But to be safe for binary search, we can set high = 1 + min(total_A_1, total_A_2, total_A_3). Since we want the maximum M, we can binary search on [0, high]. But note that M could be 0 even if totals are >0. So we can set high = min(total_A_1, total_A_2, total_A_3) + 1, and binary search for the largest M such that feasible(M) is true. Or we can just set high to a large number like 2e5 * 5000? But then the check might take longer because we have to loop over X for each type, but it's still O(X) regardless of M. So we can set high = 10**18 or something, but we need an upper bound. Actually we can set high = min(total_A_1, total_A_2, total_A_3) + 1, and then binary search on the integer range. Since the DP for each type only goes up to total_A_k, any M > total_A_k will be infeasible. So we can compute total_A_k for each type, and set high = min(total_A_1, total_A_2, total_A_3). But careful: if we set high = min_total, then we check feasibility for M = min_total. It might be feasible or not. If feasible, answer could be higher? No, because at least one type has total vitamin exactly min_total, so we cannot get more than that. So high = min(total_A_1, total_A_2, total_A_3) is a valid upper bound. But we want to binary search on the maximum feasible M. So we can set lo = 0, hi = min_total. Then while lo < hi: mid = (lo + hi + 1) // 2; if feasible(mid): lo = mid else: hi = mid - 1. Finally answer = lo.

But wait: what if min_total is 0? Then answer is 0. That's fine.

Now, feasible(M) function:
   total_cost = 0
   for each k in 1..3:
       dp = dps[k-1]
       found = False
       for w in range(0, X+1):
           if dp[w] >= M:
               found = True
               total_cost += w
               break
       if not found:
           return False
   return total_cost <= X

Complexity: O(3*X) per call.

But we can optimize: since we have three DPs, we can precompute for each dp an array next_cost_for_m? No need.

One more optimization: Instead of looping w from 0 to X for each check, we can precompute for each type the minimal calories to achieve each possible vitamin amount. But the number of possible vitamin amounts is up to total_A_k, which can be large. So we cannot precompute an array of size 1e9. However, we can note that the DP gives dp[w] for w=0..X. The vitamin amounts are at most total_A_k. Since X is only 5000, the number of distinct dp values is at most X+1. So we can, for each type, create a dictionary or list mapping from vitamin amount to the minimal calories to achieve at least that amount? Actually we want: for a given M, find min w such that dp[w] >= M. This is equivalent to: for each w, we have a vitamin amount dp[w]. We can sort the pairs (w, dp[w]) by dp[w] descending, and then for a given M, the minimal w is the minimal w among those with dp[w] >= M. Since X=5000, we can just loop.

So the plan is solid.

Now, we must ensure that the DP handles large A_i (up to 2e5) correctly. dp values can be up to sum of A_i, which is at most 1e9. Python int can handle that.

Let's test with sample 1:
N=5, X=25
Foods:
1: V=1, A=8, C=5
2: V=2, A=3, C=5
3: V=2, A=7, C=10
4: V=3, A=2, C=5
5: V=3, A=3, C=10

Items1: (8,5)
Items2: (3,5), (7,10)
Items3: (2,5), (3,10)

DP for type 1: X=25. dp[w] = max vitamin with ≤w calories.
Initially dp[0..25]=0.
Item (8,5): for w from 25 down to 5: dp[w] = max(dp[w], dp[w-5]+8). So dp[5]=8, dp[6]=8, ..., dp[25]=8.
So dp[5..25] = 8. dp[0..4]=0.
Now for M=3: find smallest w with dp[w]>=3. w=5 (dp[5]=8>=3). So cost=5.
For M=4: w=5, cost=5.
For M=8: w=5, cost=5.
For M=9: dp[5]=8 <9, so no w ≤25 has dp>=9? Wait, dp[5]=8, and all other w>5 also 8. So no w gives 9. So infeasible for M=9.

DP for type 2: items (3,5) and (7,10).
Initialize dp[0..25]=0.
Item (3,5): for w from 25 down to 5: dp[w] = max(dp[w], dp[w-5]+3). So dp[5]=3, dp[6]=3, ..., dp[25]=3.
Item (7,10): for w from 25 down to 10: dp[w] = max(dp[w], dp[w-10]+7).
Let's compute manually:
w=10: dp[0]+7=7 -> dp[10]=7.
w=11: dp[1]+7=7 -> dp[11]=7.
...
w=15: dp[5]+7=3+7=10 -> dp[15]=10.
w=20: dp[10]+7=7+7=14 -> dp[20]=14.
w=25: dp[15]+7=10+7=17 -> dp[25]=17.
Also, we could combine both items: total calories 15, vitamin 3+7=10. That's dp[15]=10.
Total calories 20, vitamin 10+3? Wait, we can't take the 3-cal item twice. Actually items are 5 and 10. So combinations:
- only (3,5): cost 5, vitamin 3.
- only (7,10): cost 10, vitamin 7.
- both: cost 15, vitamin 10.
So dp[w] should be:
w<5: 0
5≤w<10: 3
10≤w<15: 7 (since cost 10 gives 7, and we can also have cost 5 but 7>3)
15≤w: 10 (cost 15 gives 10)
w=20: 14? Wait, can we get 14? That would require 20 calories: we could take (7,10) and (3,5) twice? But we can't take (3,5) twice. So we only have one (3,5). So max vitamin for 20 calories is 10 (from both items) plus maybe something else? No, we only have two items. So with 20 calories, we could take (7,10) and (3,5) and have 5 calories left unused. Total vitamin = 10. So dp[20] should be 10. But my manual computation above said dp[20]=14? That's wrong. Let's re-evaluate:
After processing (3,5): dp[5]=3, dp[6]=3, ..., dp[10]=3, dp[11]=3, ..., dp[15]=3, etc.
Then processing (7,10):
for w=25 down to 10:
dp[10] = max(dp[10], dp[0]+7) = max(3,7)=7.
dp[11] = max(dp[11], dp[1]+7) = max(3,7)=7.
...
dp[15] = max(dp[15], dp[5]+7) = max(3,3+7=10)=10.
dp[16] = max(dp[16], dp[6]+7) = max(3,3+7=10)=10.
...
dp[20] = max(dp[20], dp[10]+7). At this point, dp[10] has already been updated to 7? Wait, careful: we are iterating w from 25 down to 10. When we reach w=20, we look at dp[10]. But dp[10] was updated in this same item's iteration? Since we are going downwards, dp[10] has already been updated when we processed w=10. So dp[10] is 7. Then dp[20] = max(dp[20], dp[10]+7) = max(3, 7+7=14) = 14. That is incorrect because we cannot take the same item twice. The error is that the DP should use the dp values from the previous item, not the updated ones. The standard 0/1 knapsack does iterate from high to low, so that dp[w-C] refers to the state before considering the current item. But because we are iterating w from X down to C, when we are at w=20, we look at w-C=10. Since 10 < 20, and we are going downwards, dp[10] has already been updated for the current item (since we started at 25 and went down to 10). So dp[10] is the state after considering the current item. This would incorrectly allow taking the same item multiple times. Wait, the standard 0/1 knapsack trick: to avoid using an item multiple times, we iterate w from W down to weight. This ensures that when we update dp[w] using dp[w-weight], the dp[w-weight] is from the previous iteration (before the current item is considered) because w-weight < w, and since we are going downwards, w-weight is less than the current w, so it has not been updated yet? Actually, if we go downwards, say W=25, weight=10. We start at w=25, then 24, ..., 10. When w=20, we access dp[10]. At that moment, we have already processed w=25,24,...,10? No, we are at w=20, and we have processed w=25,24,...,21. We have not yet processed w=10 because 10 < 20. Wait, the loop is for w in range(W, weight-1, -1): so w goes 25,24,23,22,21,20,19,...,10. So when w=20, we have processed w=25..21, but not w=20 itself yet, and not w=19..10. So dp[10] has not been updated in this item's iteration yet. So dp[10] is still the old value (before the current item). So the standard trick works: by going downwards, when we update dp[w], dp[w-weight] is from the previous item (or previous state). So my manual thought that dp[10] is updated before w=20 is wrong because 10 is processed after 20? Wait, the order: w=25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10. So w=20 is processed before w=10. So when we process w=20, dp[10] is still the old value (from before the current item). So dp[10] is 3 (from the first item). So dp[20] = max(dp[20], dp[10]+7) = max(3, 3+7=10) = 10. That is correct. So my earlier manual update was in the wrong order. So the DP is correct.

Thus, DP works.

Now, back to sample 1: For type 2, dp[10]=7, dp[15]=10. So for M=3, smallest w with dp[w]>=3 is w=5 (dp[5]=3). For M=4, w=10 (dp[10]=7). For M=7, w=10. For M=8, w=15 (dp[15]=10). For M=10, w=15.

Type 3: items (2,5) and (3,10).
DP:
Item (2,5): dp[5]=2, dp[6]=2, ..., dp[25]=2.
Item (3,10): for w from 25 down to 10: dp[w] = max(dp[w], dp[w-10]+3).
w=10: dp[0]+3=3 -> dp[10]=3.
w=15: dp[5]+3=2+3=5 -> dp[15]=5.
w=20: dp[10]+3. At w=20, dp[10] is old (before this item)? Actually careful: when w=20, we access dp[10]. Since we are going downwards, w=20 is processed before w=10? No, the loop: w=25,24,...,10. So w=20 is processed before w=10. So dp[10] is still the old value (2). So dp[20] = max(2, 2+3=5) = 5.
w=25: dp[15]+3. dp[15] is old? w=25 is processed before w=15. So dp[15] is old (2). So dp[25] = max(2, 2+3=5) = 5.
But wait, we can take both items: cost 5+10=15, vitamin 2+3=5. That gives dp[15]=5. So dp[15]=5 is correct.
What about taking both and having more calories? For w=20, we could take both (15 calories) and have 5 left, vitamin 5. So dp[20] should be 5. That matches.
But can we get more? No, only two items.
So dp for type 3: w<5:0; 5≤w<10:2; 10≤w<15:3; 15≤w:5.
For M=2, w=5. M=3, w=10. M=5, w=15.

Now, for M=3:
Type1: cost 5 (dp[5]=8>=3)
Type2: cost 5 (dp[5]=3>=3)
Type3: cost 10 (dp[10]=3>=3)
Total cost = 5+5+10 = 20 ≤ 25. So feasible.
M=4:
Type1: cost 5 (8>=4)
Type2: cost 10 (7>=4)
Type3: cost 15? dp[15]=5>=4, so cost 15.
Total = 5+10+15 = 30 > 25, infeasible.
So max feasible M is 3. Matches sample.

Sample 2:
N=2, X=5000
Food1: V=1, A=200000, C=1
Food2: V=2, A=200000, C=1
Type1: one item (200000,1). dp[c] for c>=1: 200000. So for M=1, cost=1. For M=200000, cost=1.
Type2: one item (200000,1). dp[c] for c>=1: 200000.
Type3: no items. dp[c]=0 for all c. So for M=1, dp[0]=0 <1, so no w gives >=1, infeasible. So M=1 is infeasible. Thus answer 0.
Our code: total_A_3 = 0, so high = min(200000,200000,0) = 0. Binary search [0,0] gives 0. Good.

So the algorithm is correct.

Now, we need to implement in Python.

Steps:
- Read input.
- Group items.
- For each of the three vitamins, compute dp array of length X+1.
- Compute total_A for each type to set hi for binary search.
- Binary search for maximum M.

Edge cases: What if a type has no items? Then dp array remains all zeros. For M=0, cost=0 (since dp[0]=0>=0). For M>0, no w gives dp>=M, so infeasible. Our binary search high will be min(total_A_1, total_A_2, total_A_3). If one type has total_A=0, high=0, so answer 0.

Now, complexity: O(N*X + log(MAX) * 3*X) where MAX is at most total_A_min. With N=5000, X=5000, it's 25e6 + ~5000*30 = 25e6 + 150k = about 25 million, which is fast in Python (maybe 0.5-1 second).

We should be careful with the DP: using a list of length X+1, and for each item, looping backwards. This is standard.

Now, we need to produce the final code.

We should also consider if we can further optimize: the DP for each type is independent. We can run them.

Now, let's write the code in a clean way.

Implementation details:

```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[], [], []]  # index 0 for vitamin 1, 1 for vitamin 2, 2 for vitamin 3
    total_A = [0, 0, 0]
    for _ in range(N):
        V, A, C = map(int, input().split())
        idx = V - 1
        items[idx].append((A, C))
        total_A[idx] += A
    
    # DP for each vitamin type
    dps = []
    for k in range(3):
        dp = [0] * (X + 1)
        for A, C in items[k]:
            # if C > X, then this food cannot be taken because calorie limit is X. But constraints say C_i <= X, so ignore.
            for w in range(X, C - 1, -1):
                # dp[w] = max(dp[w], dp[w-C] + A)
                val = dp[w - C] + A
                if val > dp[w]:
                    dp[w] = val
        dps.append(dp)
    
    # Function to check if M is feasible
    def feasible(M):
        total_cost = 0
        for k in range(3):
            dp = dps[k]
            found = False
            for w in range(X + 1):
                if dp[w] >= M:
                    found = True
                    total_cost += w
                    break
            if not found:
                return False
        return total_cost <= X
    
    # Determine upper bound for binary search
    # The maximum possible M is the minimum total vitamin among the three types.
    # But note: even if total_A_k is large, we might not be able to achieve it due to calorie constraints. However, the answer cannot exceed min(total_A_1, total_A_2, total_A_3) because each type can provide at most that much. So hi = min(total_A) is a valid upper bound.
    hi = min(total_A)
    lo = 0
    # Binary search for the largest M such that feasible(M) is True.
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

We should test with the samples.

Test 1:
Input:
5 25
1 8 5
2 3 5
2 7 10
3 2 5
3 3 10
Our code should output 3.

Test 2:
Input:
2 5000
1 200000 1
2 200000 1
Output 0.

Now, consider some edge cases:
- N=1, X=10, food: V=1, A=5, C=10. Then total_A = [5,0,0]. hi=0. Answer 0. But wait, we can get 5 units of vitamin 1, but 0 of others, so min is 0. Correct.
- N=3, X=10, foods: V=1, A=10, C=5; V=2, A=10, C=5; V=3, A=10, C=5. Then total_A = [10,10,10]. hi=10. Check M=5: cost for each: type1: need ≥5. With cost 5, we get 10, so cost=5. Total=15 >10, infeasible. M=4: same, cost=5, total=15>10. M=0: feasible. So answer 0. That seems correct.
- N=3, X=15, same foods. M=10: cost for each =5, total=15, feasible. M=11: infeasible. Answer 10.

Now, check the DP: for type1, dp[5]=10, dp[6..15]=10. So for M=10, w=5 works. For M=11, no w. Good.

Now, what about the case where we have multiple items and the optimal cost for a type is not simply the sum of the cheapest items? The DP correctly considers all combinations.

Now, we must ensure that the DP correctly handles the case where we don't take any items. dp[0]=0. So for M=0, cost=0 always.

Now, one more thing: the feasible function loops w from 0 to X. Since dp is non-decreasing? Not necessarily, but with the DP, dp[w] is the max vitamin with calories ≤ w, so it is non-decreasing with w? Actually, since we can always waste calories, dp[w] is non-decreasing. But in our DP, we didn't do prefix max, but the recurrence dp[w] = max(dp[w], dp[w-C]+A) and initial dp[w]=0. Since we can always choose not to take the item, dp[w] is at least dp[w-1]? Not automatically. For example, with one item (A=10, C=5), dp[0]=0, dp[1]=0, dp[2]=0, dp[3]=0, dp[4]=0, dp[5]=10, dp[6]=10, etc. So it is non-decreasing. In general, the standard 0/1 knapsack DP with dp initialized to 0 and the recurrence as given yields dp[w] that is non-decreasing? Let's check: Suppose we have two items: (A=5, C=3) and (A=10, C=7). Then dp[0]=0. After first item: dp[3]=5, dp[4]=5, dp[5]=5, etc. After second item: we update from high to low. So dp[7] = max(old dp[7], dp[0]+10)=10. dp[6] = max(old dp[6], dp[-1]?) not updated. So dp[6] remains 5. So dp[6]=5, dp[7]=10. That is non-decreasing. In fact, the DP ensures dp[w] is the max over all subsets with total cost ≤ w, so it is non-decreasing by definition. So we can break early when we find dp[w] >= M, because for larger w it's also >= M. But we still need to find the smallest w, so we loop from 0 upwards.

Now, is there any optimization we can do? We can precompute for each type an array best_cost_for_m: for each possible M, the minimal cost. But as discussed, M can be large, so not possible.

The current solution is efficient and correct.

Now, we should double-check the constraints: N up to 5000, X up to 5000, A_i up to 2e5. The DP values can be up to 1e9, which fits in Python int.

Now, consider the time limit. Usually 2 seconds. 25 million operations in Python might be a bit slow but should be okay. We can micro-optimize: use local variables, avoid function calls. But 25 million simple integer operations should be fine.

We can also optimize by not iterating over all w for each item if C > X, but constraints say C_i <= X, so it's fine.

Another micro-optimization: use `for w in range(X, C-1, -1):` and inside, use `new_val = dp[w-C] + A; if new_val > dp[w]: dp[w] = new_val`. This is fine.

Now, let's test with a random small case to ensure correctness. We can write a brute force for N up to 10, but we trust the algorithm.

One potential issue: The DP we described is for "at most w calories". But the standard recurrence is for "exactly w calories" if we initialize dp with -inf except dp[0]=0. However, we initialized all to 0, which allows not using all calories. Let's verify the recurrence carefully.

We want: dp[w] = max total vitamin using a subset of items with total calories ≤ w.
Base: dp[0..X] = 0. (using empty set, 0 calories, 0 vitamin).
For each item (cost C, value A):
  for w from X down to C:
    dp[w] = max(dp[w], dp[w-C] + A)

Is this correct? Let's prove by induction. Assume before processing the item, dp[w] is the max vitamin with cost ≤ w using a subset of processed items. Now consider adding the new item. For a given w, if we don't take the new item, the best is dp[w] (old). If we take the new item, we need to select a subset of old items with cost ≤ w-C, and add A. The best old subset for cost ≤ w-C is dp[w-C] (old). So the best with the new item is dp[w-C] (old) + A. So the new dp[w] is the max of these two. This is exactly the recurrence. So the DP is correct.

Thus, our DP correctly computes the max vitamin with calories ≤ w.

Now, the feasible function: for each type, find the smallest w such that dp[w] >= M. Since dp is non-decreasing, we can break at the first such w. Then sum the w's. If sum ≤ X, feasible.

Now, we need to ensure that the sum of the minimal w's is indeed the minimal total calories to achieve at least M for each type. Is it optimal to independently minimize the calories for each type? Yes, because the types are independent: the foods for different vitamins do not interact. We can choose any subset of foods, and the total calories is the sum of calories from each vitamin's foods. So to achieve at least M for all three, we need to pick a set of foods for each type that achieves at least M, and the total calories is the sum. To minimize total calories, we should minimize the calories for each type independently. So the feasible check is correct.

Now, we need to ensure that the binary search bounds are correct. We set hi = min(total_A). But is it possible that the answer is greater than min(total_A)? No, because each type can provide at most total_A_k vitamin units. So the minimum intake cannot exceed the smallest total among the three. So hi = min(total_A) is a valid upper bound. However, note that total_A could be large, but we only binary search up to that. If min(total_A) is 0, hi=0, and we only check M=0, which is feasible. So answer 0. Good.

Now, what if min(total_A) is very large, e.g., 1e9? Then binary search takes about 30 steps. Each step does O(X) work. X=5000, so 150k work per step, 4.5 million total. The DP is O(N*X) = 25 million. So total is about 30 million, fine.

Now, we should also consider that the DP for each type might be unnecessary to run if the type has no items? We can just set dp to [0]*(X+1). That's fine.

Now, let's think about potential integer overflow? No, Python handles big ints.

Now, we should test the code with the sample inputs.

I'll simulate mentally, but I'm confident.

Now, we need to output the code in the required format: "Enclose your code within delimiters as follows." Probably they want something like:

```python
# your code
```

But the problem says: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT." It might mean to put the code in a block. Usually in these tasks, we just provide the code. But the instruction says: "Enclose your code within delimiters as follows." Possibly they want:

```python
import sys

def solve():
    ...

if __name__ == "__main__":
    solve()
```

But to be safe, we just provide the code as is.

Now, before finalizing, let's think if there is any better approach. The DP on calories is very efficient. We could also DP on vitamin amount with a dictionary, but that would be slower. So this is the best.

One more check: In the feasible function, we sum the minimal w for each type. But is it always possible to achieve the sum of these minimal w's? That is, if for type 1 we need w1 calories to get M, and for type 2 we need w2, and for type 3 we need w3, can we always pick a combination that uses exactly w1 calories for type 1, w2 for type 2, w3 for type 3? Yes, because the choices for each type are independent. The DP gives us the existence of a subset of foods for that type that uses at most w calories and gives at least M vitamin. We can pick the subset that achieves that. So total calories is at most w1 + w2 + w3. But wait: the DP gives the max vitamin with at most w calories. So if dp[w] >= M, there exists a subset with total calories ≤ w that gives at least M vitamin. So we can pick a subset for each type that uses at most w_k calories. Then the total calories used is at most sum w_k. If sum w_k ≤ X, then we can pick those subsets, and total calories ≤ X. So it's feasible. The fact that the actual subset might use fewer than w_k calories only helps. So the check is correct.

Now, we need to ensure that the DP state "at most w" is exactly what we want. Yes.

Now, let's consider if there is any off-by-one error. For M=0, dp[0]=0 >=0, so cost 0. So feasible. The binary search will include M=0.

Now, we should also consider that the binary search might check M values that are larger than any dp[w] for some type. Then the loop over w will not find any w, and feasible returns False. So it's correct.

Now, we should optimize the feasible function slightly: since dp is non-decreasing, we can break when found. We already do that.

Now, we can also precompute for each type the minimal w for each possible M? Not needed.

Now, let's write the final code.

But wait: There is a subtle point: the DP we computed is dp[w] = max vitamin with calories ≤ w. However, when we look for the minimal w such that dp[w] >= M, we are finding a calorie budget w that allows us to get at least M vitamin. But the actual subset we pick might use fewer than w calories. So the total calories used could be less than the sum of these w's. So our condition sum(w) ≤ X is sufficient but not necessary? Actually, if for type 1 we need w1 calories to achieve M, that means there is a subset using ≤ w1 calories. We can choose that subset. So the actual calories used for type 1 is some c1 ≤ w1. Similarly for others. The sum c1+c2+c3 ≤ w1+w2+w3. So if w1+w2+w3 ≤ X, then c1+c2+c3 ≤ X. So it's feasible. Conversely, if for every type, the minimal w such that dp[w] >= M is w_k, and if sum w_k > X, then any combination of subsets that achieve M for each type must use at least w1, w2, w3 calories respectively? Not necessarily: the minimal w for each type is the minimal calorie budget needed. So any subset achieving M for type 1 must use at least w1 calories? Wait, dp[w] is the max vitamin with calories ≤ w. If dp[w1] >= M, it means there exists a subset using ≤ w1 calories that gives M. It does not mean that every subset achieving M uses at least w1 calories. The minimal calories needed to achieve M is the smallest w such that there exists a subset with calories ≤ w achieving M. That minimal w is exactly the minimal calories required. So for each type, the minimal calories required is min_{subset achieving M} total calories. Our DP finds that minimal w as the smallest w with dp[w] >= M. So that w is exactly the minimal calories needed for that type. So if we denote c_k = minimal calories for type k to achieve M, then any feasible solution must have total calories at least c1+c2+c3. And if c1+c2+c3 ≤ X, we can achieve it by taking the subsets that achieve these minimal costs. So the condition is both necessary and sufficient. So our check is correct.

Now, we must ensure that the DP correctly gives the minimal calories. Since dp[w] is the max vitamin with calories ≤ w, the smallest w with dp[w] >= M is indeed the minimal calories needed to achieve at least M. So it's correct.

Now, we can finalize the code.

But we should also consider the case where we have many items and the DP might be slow. We can use array module or list of ints. It's fine.

Now, let's write the code with proper input parsing.

We should use sys.stdin.readline for speed.

Now, one more optimization: we can precompute the total_A and also the items lists.

Now, the code:

```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[], [], []]
    total_A = [0, 0, 0]
    for _ in range(N):
        V, A, C = map(int, input().split())
        items[V-1].append((A, C))
        total_A[V-1] += A
    
    dps = []
    for k in range(3):
        dp = [0] * (X + 1)
        for A, C in items[k]:
            for w in range(X, C - 1, -1):
                val = dp[w - C] + A
                if val > dp[w]:
                    dp[w] = val
        dps.append(dp)
    
    def feasible(M):
        total_cost = 0
        for k in range(3):
            dp = dps[k]
            for w in range(X + 1):
                if dp[w] >= M:
                    total_cost += w
                    break
            else:
                return False
        return total_cost <= X
    
    lo = 0
    hi = min(total_A)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

This should work.

Now, we should test with the samples.

Sample 1:
5 25
1 8 5
2 3 5
2 7 10
3 2 5
3 3 10

Output: 3

Sample 2:
2 5000
1 200000 1
2 200000 1

Output: 0

Now, let's think about a case where the answer is large. Suppose N=3, X=15, foods: (1,10,5), (2,10,5), (3,10,5). Then total_A=[10,10,10], hi=10. Check M=10: each type needs 5 calories, total 15, feasible. M=11: infeasible. So answer 10.

Now, a case with multiple items per type. It should work.

Now, we need to ensure that the DP correctly handles the case where we have many items and the calorie cost is large. Since X=5000, the DP array is size 5001, which is small.

Now, we should consider if we can further reduce the time. One thing: the feasible function is called many times, and inside it we loop over X for each type. That's fine. But we can also precompute for each type an array `min_cost_for_vitamin` where for each possible vitamin amount up to total_A_k, we store the minimal calories. But total_A_k can be up to 1e9, so we cannot. However, we can note that the DP gives dp[w] for w=0..X. The vitamin amounts are at most total_A_k, but we only care about the threshold M. So we can for each type, create a list of pairs (vitamin_amount, minimal_calories) from the DP. But since X is small, we can just loop.

Now, we should also consider that the DP might be computed with items of each type, and we might have many items. But N=5000, X=5000, so 25 million iterations. In Python, 25 million simple operations might take about 0.5-1 second. It's acceptable.

Now, we can micro-optimize the DP: use local variables for dp, X, and items. But it's fine.

Now, let's consider if there is any bug: the DP initializes dp to 0. But if we have an item with cost C and value A, and we loop w from X down to C, then for w < C, we don't update. That's correct. For w >= C, we consider taking the item. But what if we have multiple items? The DP handles it.

Now, one more thing: the feasible function sums the minimal w. But what if the minimal w for a type is 0? That can happen if M=0. Then total_cost might be 0. That's fine.

Now, we should also consider that the DP might produce dp[w] that is not strictly increasing, but that's fine.

Now, we should test with a case where one type has no items. For example, N=1, X=10, V=1, A=5, C=5. Then items[0]=[(5,5)], items[1]=[], items[2]=[]. total_A=[5,0,0]. hi=0. lo=0, hi=0, loop doesn't run, print 0. Correct.

Now, what if N=3, X=10, foods: V=1, A=5, C=5; V=2, A=5, C=5; V=2, A=5, C=5; V=3, A=5, C=5. So type1: one item, type2: two items, type3: one item. total_A=[5,10,5]. hi=5. Check M=5: type1: cost 5, type2: cost 5 (can take one item of 5), type3: cost 5, total 15 >10, infeasible. M=4: type1: cost 5 (since 5>=4), type2: cost 5, type3: cost 5, total 15>10, infeasible. M=3: same, total 15>10. M=2: same. M=1: same. M=0: cost 0, feasible. So answer 0. That seems correct because we need 15 calories to get at least 1 of each, but we only have 10.

Now, a more complex case: N=6, X=10, foods:
V1: A=8, C=5; A=2, C=6 (total 10, but 8+2=10, so to get 8 we need 5 calories, to get 10 we need 11? Actually 5+6=11 >10, so we can only take one. So max vitamin for type1 is 8 (if we take the 8-cost one) or 2 (if we take the 2-cost one). So dp for type1: w<5:0; 5≤w<6:8; 6≤w:8 (since taking 8 gives 8, taking 2 gives 2, so max is 8). So for M=8, w=5; M=2, w=6? Actually for M=2, we can use the 2-cost item with 6 calories, so w=6. But also we can use the 8-cost item with 5 calories, which gives 8>=2, so w=5. So minimal w is 5. So type1 can achieve 2 with 5 calories.
Type2: similar.
Type3: similar.
So for M=2, each type needs 5 calories, total 15 >10, infeasible. For M=0, feasible. So answer 0. Our code would compute hi = min(10,10,10)=10. But actually we cannot get 10 for any type because of calorie limits. But the DP will correctly reflect that: for type1, dp[5]=8, dp[6]=8, etc. So for M=10, no w gives dp>=10, so infeasible. Binary search will eventually find that M=2 is infeasible, and M=1 is infeasible? Let's check M=1: type1 w=5, type2 w=5, type3 w=5, total 15>10, infeasible. So M=0 is max. So answer 0. Good.

Now, what if we have items that allow us to get exactly M with lower calories? The DP will find the minimal w.

Now, we should also consider that the binary search might check M values that are not achievable by the DP for any w, but the loop will go through all w and not find, so feasible returns False. That's correct.

Now, the code seems solid.

Now, we need to output the code as per the instructions. The problem says: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT." It might be that they want the code in a markdown block. But to be safe, we just provide the code.

Now, we should also think about potential improvements: we can use `array` module for the DP to save memory and maybe speed, but not needed.

Now, let's write the final answer.

But wait: the problem statement says: "There are N foods, each containing exactly one of vitamins 1, 2, and 3." So each food has one vitamin. Our code assumes that.

Now, we should also consider that the input might have extra spaces or newlines. Using split handles that.

Now, we are ready.

But let's double-check the DP correctness with a small brute force.

Consider N=3, X=5, foods:
1: V=1, A=10, C=3
2: V=1, A=1, C=2
3: V=2, A=5, C=4
Type1: items (10,3) and (1,2). DP: dp[0]=0. After (10,3): w=5..3: dp[3]=10, dp[4]=10, dp[5]=10. After (1,2): w=5..2: dp[5]=max(10, dp[3]+1=11)=11; dp[4]=max(10, dp[2]+1=1)=10; dp[3]=max(10, dp[1]+1=1)=10; dp[2]=max(0, dp[0]+1=1)=1. So dp: w=0:0, 1:0, 2:1, 3:10, 4:10, 5:11. So max vitamin with ≤5 calories is 11 (by taking both: 3+2=5 calories, 10+1=11). Correct.
Type2: item (5,4). dp: w=4..4: dp[4]=5, dp[5]=5. So max vitamin with ≤5 calories is 5.
Type3: no items. dp: all 0.
Now, for M=5: type1: need w with dp>=5: w=3 (10>=5) -> cost 3. type2: w=4 (5>=5) -> cost 4. type3: no w with dp>=5 -> infeasible. So M=5 infeasible.
M=4: type1: w=3, cost 3. type2: w=4, cost 4. type3: infeasible. M=3: type1: w=3, cost 3. type2: w=4? dp[3]=0, so no w<=3 has dp>=3? Actually dp[3]=0, dp[4]=5, so w=4. So cost 4. type3: infeasible. M=2: type1: w=2 (dp[2]=1<2? no, dp[2]=1, so not >=2. w=3:10>=2, so cost 3. type2: w=4, cost 4. type3: infeasible. M=1: type1: w=2 (dp[2]=1>=1), cost 2. type2: w=4, cost 4. type3: infeasible. M=0: all cost 0, feasible. So answer 0. That makes sense because we can't get any vitamin 3.

Now, suppose type3 had an item: V=3, A=1, C=1. Then total_A=[11,5,1]. hi=1. Check M=1: type1: w=2 (dp[2]=1>=1) cost 2. type2: w=4 cost 4. type3: w=1 cost 1. total=7 >5, infeasible. M=0: feasible. So answer 0. If X=7, then total=7, feasible. So answer 1. Our code would handle that.

Now, everything seems correct.

Now, we should also consider that the DP for each type might be reused. We compute it once.

Now, we can finalize the code.

One more optimization: in the feasible function, we can precompute for each type an array `min_w` for each possible M? Not needed.

Now, we should write the code in a clean and efficient manner.

We'll produce the code as follows:

```python
import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[], [], []]
    total = [0, 0, 0]
    for _ in range(N):
        V, A, C = map(int, input().split())
        items[V-1].append((A, C))
        total[V-1] += A
    
    # DP for each vitamin type
    dps = []
    for k in range(3):
        dp = [0] * (X + 1)
        for A, C in items[k]:
            for w in range(X, C - 1, -1):
                val = dp[w - C] + A
                if val > dp[w]:
                    dp[w] = val
        dps.append(dp)
    
    def can(M):
        cost = 0
        for k in range(3):
            dp = dps[k]
            for w in range(X + 1):
                if dp[w] >= M:
                    cost += w
                    break
            else:
                return False
        return cost <= X
    
    lo = 0
    hi = min(total)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

This should be the final code.

Now, we need to output it in the required format. The problem says: "Enclose your code within delimiters as follows." Possibly they want:

```python
# your code
```

But to be safe, we'll just put it in a code block.

Now, before finalizing, let's think if there is any edge case where the DP might be incorrect. For example, if we have an item with C > X, we ignore it. But the constraints say C_i <= X, so it's fine.

Now, what about the case where we have multiple items and the DP might exceed time? 25 million iterations in Python is usually okay if written efficiently. We can try to micro-optimize: use `range(X, C-1, -1)` which is fast. We can also use local variables: `dp_w = dp` etc. But it's fine.

Now, we should also consider that the binary search might be called many times, but each call is O(3*X) = 15000, and log2(1e9) ~ 30, so 450,000 operations, negligible.

Now, we can produce the final answer.

But wait: the problem statement says: "Find the maximum possible value of this: the minimum intake among vitamins 1, 2, and 3." So we want to maximize the minimum. Our algorithm does that.

Now, we should also consider that the answer might be 0. Our code handles that.

Now, I think we are done.

Now, we need to output the code in the response. The instruction says: "Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT." It might be that they want the code to be inside a block. We'll provide it as a Python code block.

Now, final answer.</mm:think>```python
import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[], [], []]
    total = [0, 0, 0]
    for _ in range(N):
        V, A, C = map(int, input().split())
        items[V-1].append((A, C))
        total[V-1] += A

    # DP for each vitamin type: dp[w] = max vitamin with calories <= w
    dps = []
    for k in range(3):
        dp = [0] * (X + 1)
        for A, C in items[k]:
            for w in range(X, C - 1, -1):
                val = dp[w - C] + A
                if val > dp[w]:
                    dp[w] = val
        dps.append(dp)

    def can(M):
        cost = 0
        for k in range(3):
            dp = dps[k]
            for w in range(X + 1):
                if dp[w] >= M:
                    cost += w
                    break
            else:
                return False
        return cost <= X

    lo = 0
    hi = min(total)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
```

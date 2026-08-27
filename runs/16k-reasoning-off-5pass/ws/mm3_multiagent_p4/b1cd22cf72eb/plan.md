We need to choose a common target height `H` and reduce each upper tooth `U_i` and lower tooth `D_i` down to some `h_i, k_i` with `h_i + k_i = H`. The cost is the total reduction: `sum (U_i - h_i) + (D_i - k_i)`. Given `h_i + k_i = H`, minimizing per tooth cost yields `h_i = min(U_i, H)` and `k_i = min(D_i, H - h_i) = min(D_i, max(0, H - U_i))`, which is equivalent to the standard formula: cost for tooth i with height H is `max(0, U_i + D_i - 2*H)` when `H` is small, but more directly: we must reduce each tooth to at most H/2, paying `(U_i - min(U_i, H/2))` etc. Actually the optimal split: h_i = min(U_i, H/2), k_i = H - h_i, and we must ensure k_i ≤ D_i so we never need to reduce k_i below D_i — this is equivalent to ensuring H - min(U_i, H/2) ≤ D_i, i.e., H ≤ U_i + D_i. So H must be ≤ min_i (U_i + D_i), and cost for that i is (U_i + D_i - H) when H ≤ U_i + D_i (and split optimally). So total cost is `sum_i max(0, U_i + D_i - H)`.

But we also have the adjacency constraint: after grinding, final upper lengths `u_i' = min(U_i, H/2)`? Wait — the upper tooth length after grinding is `h_i = min(U_i, H - h_i)`. The solution is: set h_i = min(U_i, H/2) (since choosing a larger h_i would make k_i smaller and we might violate D_i). Actually for a given H, the optimal h_i is `min(U_i, H)` as long as H - h_i ≤ D_i, which holds if H ≤ U_i + D_i. So h_i = min(U_i, H). But that can exceed H/2; then k_i = H - h_i, and we need D_i ≥ H - h_i, i.e., D_i + U_i ≥ H. Yes this is always satisfied if H ≤ U_i + D_i. So u_i' = min(U_i, H), d_i' = min(D_i, H - u_i')? Actually d_i' = H - u_i' = max(0, H - U_i). And we need d_i' ≤ D_i, i.e., max(0, H - U_i) ≤ D_i, i.e., H ≤ U_i + D_i. So given H ≤ min_i (U_i + D_i), valid splits exist with cost `sum_i (U_i - min(U_i, H)) + (D_i - min(D_i, H - min(U_i, H)))`. This simplifies to:
- If U_i ≤ H: u_i' = U_i, d_i' = H - U_i, cost_i = D_i - (H - U_i) = U_i + D_i - H (only if H - U_i ≤ D_i, true).
- If U_i > H: then d_i' = 0, but d_i' must be 0 ≤ D_i, valid. Cost_i = U_i - H + D_i = U_i + D_i - H.

Wait, in both cases cost_i = U_i + D_i - H? No, if U_i ≤ H, we don't grind upper at all (cost U_i - U_i = 0), and we grind lower to H - U_i, costing D_i - (H - U_i) = U_i + D_i - H. If U_i > H, we grind upper to H, cost U_i - H, and lower stays at D_i ≥ 0 (d_i' = 0, cost 0). Total = U_i - H + 0. Hmm, this is different.

Let me re-derive. After grinding, u_i' + d_i' = H, with 0 ≤ u_i' ≤ U_i, 0 ≤ d_i' ≤ D_i. We want to minimize U_i - u_i' + D_i - d_i' = (U_i + D_i) - H. This is constant! So for any H ≤ U_i + D_i, the cost for that tooth is exactly U_i + D_i - H. So total cost for given H is `sum_i max(0, U_i + D_i - H)` where H can be at most `min_i (U_i + D_i)`? Actually we need H ≥ 1 (teeth have positive length? The problem says "whose length is positive" to grind, implying we can't make length 0, or can we? "choose exactly one tooth whose length is positive, and reduce its length by 1" — so we can only reduce to 0? No, "whose length is positive" means we pick a tooth with length ≥ 1 to reduce. So we can reduce to 0. But the final lengths must be such that u_i' + d_i' = H, with u_i', d_i' ≥ 0, and also the resulting u_i' must equal min(U_i, H) and d_i' = H - min(U_i, H) = max(0, H-U_i), provided max(0, H-U_i) ≤ D_i. So H ≤ U_i + D_i.

Wait, but if U_i ≤ H, we set u_i' = U_i (no grinding of upper, cost 0), d_i' = H - U_i, cost = D_i - (H-U_i) = U_i + D_i - H. If U_i > H, u_i' = H, cost = U_i - H, d_i' = 0, cost = D_i. Total = U_i - H + D_i = U_i + D_i - H. Yes! So cost is always U_i + D_i - H as long as H ≤ U_i + D_i.

Now the second condition: |u_i' - u_{i+1}'| ≤ X, where u_i' = min(U_i, H). We can choose H to be any integer ≥ 0 (or ≥ 1?). Since we need u_i' ≥ 0, and we only grind positive teeth, but final u_i' can be 0. The problem says "choose exactly one tooth whose length is positive, and reduce its length by 1" — so to make a tooth 0, we reduce from 1 to 0, which is allowed. So H can be 0, giving u_i' = 0 for all i, cost = sum U_i + sum D_i. But teeth fitting together with H=0? The condition says "U_i + D_i = H for every i", so H=0 would require U_i + D_i = 0, impossible since U_i, D_i ≥ 1. So actually H must be at least 1? Wait, the final u_i' and d_i' must satisfy u_i' + d_i' = H, and u_i' ≤ U_i, d_i' ≤ D_i, u_i', d_i' ≥ 0. If H=0, then u_i' = d_i' = 0, but we need 0 ≤ U_i (true) and 0 ≤ D_i (true). But the operation requires reducing teeth whose length is positive. To make U_i = 0, we must reduce U_i times, which is allowed. However, the condition "U_i + D_i = H" with H=0 means after grinding, the new upper length plus new lower length = 0, so both must be 0. But the condition is about the final lengths? "There exists an integer H such that U_i + D_i = H for every integer i" — this likely refers to the final lengths, let's call them u_i' and d_i'. So u_i' + d_i' = H. With H=0, u_i' = d_i' = 0 for all i. Is that valid? The problem says "Takahashi has 2N teeth: N upper teeth and N lower teeth. The length of the i-th upper tooth ... is U_i". So initially lengths are U_i, D_i. After operations, lengths become some values. The conditions are on the final state. So yes, H=0 is technically allowed, but then u_i' = 0 for all i, so |u_i' - u_{i+1}'| = 0 ≤ X, always satisfied. Cost = sum U_i + sum D_i. But we can do better by choosing larger H. The maximum useful H is min_i (U_i + D_i) because if H > U_i + D_i for some i, we cannot achieve u_i' + d_i' = H with u_i' ≤ U_i, d_i' ≤ D_i (both non-negative), since max sum is U_i + D_i.

So the problem reduces to: choose integer H with 0 ≤ H ≤ M = min_i (U_i + D_i) to minimize:
1. Total cost: C(H) = sum_i (U_i + D_i - H) = sum_i (U_i + D_i) - N*H. This is linear decreasing in H. So larger H is better for cost.
2. Adjacency constraint: |u_i' - u_{i+1}'| ≤ X for all i, where u_i' = min(U_i, H). Note: u_i' is a non-decreasing function of H? It's min(U_i, H), which is non-decreasing and piecewise linear: 0 for H=0,...,H=U_i, then H for H>U_i.

We need to find the maximum H ≤ M such that for all i, |min(U_i, H) - min(U_{i+1}, H)| ≤ X.

Since C(H) decreases with H, we want the maximum feasible H. Let H* be the maximum H in [0, M] satisfying the constraint. Then answer is sum(U_i + D_i) - N * H*.

We need to compute H* efficiently. N up to 2e5.

Let f_i(H) = min(U_i, H). We need |f_i(H) - f_{i+1}(H)| ≤ X for all i.

Consider each i. The constraint |f_i(H) - f_{i+1}(H)| ≤ X is violated when f_i(H) - f_{i+1}(H) > X or f_{i+1}(H) - f_i(H) > X.

Case 1: f_i(H) - f_{i+1}(H) > X.
f_i(H) = min(U_i, H), f_{i+1}(H) = min(U_{i+1}, H).
This is violated when min(U_i, H) - min(U_{i+1}, H) > X.
We can think of this as: for a given H, the left tooth is much taller than the right.
Subcase 1a: H ≤ U_{i+1}. Then f_{i+1} = H. We need min(U_i, H) - H > X. If U_i ≤ H, then 0 > X, impossible. If U_i > H, then H - H = 0 > X? No, min(U_i, H) = H, so H - H = 0 > X false. So if H ≤ min(U_i, U_{i+1}), f_i = f_{i+1} = H, diff = 0. No violation.
Subcase 1b: H > U_{i+1} and H ≤ U_i. Then f_{i+1} = U_{i+1}, f_i = H. Condition: H - U_{i+1} > X => H > U_{i+1} + X. So for H in (U_{i+1}, U_{i+1} + X], it's okay. For H > U_{i+1} + X, violated. Also need H ≤ U_i.
Subcase 1c: H > U_i and H > U_{i+1}. Then f_i = U_i, f_{i+1} = U_{i+1}. Condition: U_i - U_{i+1} > X. This is a constant condition on U_i and U_{i+1} that doesn't depend on H. If U_i - U_{i+1} > X, then no H > max(U_i, U_{i+1}) can satisfy. But if H ≤ max(U_i, U_{i+1}), we are in previous subcases. So if U_i - U_{i+1} > X, we need H ≤ something.

More systematically: For each adjacent pair (i, i+1), define the set of H where |f_i - f_{i+1}| ≤ X.
Let a = U_i, b = U_{i+1}. WLOG a ≤ b. Then f_i = min(a, H), f_{i+1} = min(b, H).
- For H ≤ a: both = H, diff = 0 ≤ X. OK.
- For a < H ≤ b: f_i = a, f_{i+1} = H. diff = H - a. Need H - a ≤ X => H ≤ a + X. So OK for H ∈ [a, min(b, a+X)].
- For H > b: f_i = a, f_{i+1} = b. diff = b - a. Need b - a ≤ X. This is a condition on inputs. If b - a > X, then no H > b works. But for H ∈ (b, ∞), it's violated if b - a > X.

So the allowed H for this pair are:
- H ∈ [0, min(b, a+X)] always.
- If b - a ≤ X, then H ∈ [0, b] is all allowed? Wait: for H > b, diff = b - a ≤ X, so allowed. Actually if b - a ≤ X, then for H > b, diff = b - a ≤ X, allowed. So the entire [0, ∞) is allowed? No, we also have the M bound. And we need H ≤ M. So if b - a ≤ X, the pair imposes no upper bound beyond M? Let's check: for H > b, diff = b - a ≤ X, yes allowed. For H between a and b, H - a ≤ X => H ≤ a + X. If b ≤ a + X, then for all H ∈ [a, b], H ≤ a + X, so allowed. And for H > b, allowed since b - a ≤ X. So yes, if b - a ≤ X, any H is allowed for this pair. Wait, what about H very large? It doesn't matter. So only the global M matters.

If b - a > X, then:
- For H ≤ a: allowed.
- For a < H ≤ b: need H ≤ a + X, so H ∈ [a, a+X] (if a+X < b) or [a, b] (if a+X ≥ b).
- For H > b: diff = b - a > X, not allowed. So H must be ≤ b.

So in summary, the pair (a,b) with a ≤ b imposes an upper bound on H:
- If b - a ≤ X: H ≤ M (no additional constraint).
- If b - a > X: H ≤ a + X. (Because if H > a+X, then if H ≤ b, diff > X; if H > b, diff = b-a > X. So H must be ≤ a+X.)

So for each adjacent pair, let L_i = min(U_i, U_{i+1}), and if |U_i - U_{i+1}| > X, then we require H ≤ L_i + X. Otherwise no constraint from this pair.

Thus the maximum feasible H is:
H* = min( M, min_{i: |U_i - U_{i+1}| > X} (min(U_i, U_{i+1}) + X) )

where M = min_i (U_i + D_i).

Then total cost = sum_i (U_i + D_i) - N * H*.

Let's verify with sample 1.
N=4, X=3.
U: 3,4,5,2
D: 1,1,9,6
M = min(3+1,4+1,5+9,2+6) = min(4,5,14,8) = 4.

Adjacent pairs:
(3,4): diff=1 ≤ 3, no constraint.
(4,5): diff=1 ≤ 3, no constraint.
(5,2): diff=3 ≤ 3, no constraint.
So H* = min(4) = 4.
Total sum = (3+1)+(4+1)+(5+9)+(2+6) = 4+5+14+8 = 31.
Cost = 31 - 4*4 = 31 - 16 = 15. Matches sample output 1!

Sample 2:
N=4, X=1e9. All U_i=3, D_i=3.
M = min(3+3)=6.
All diffs 0 ≤ X, so H* = 6.
Sum = 24. Cost = 24 - 4*6 = 0. Matches.

Sample 3:
N=4, X=1.
U: 1e9, 1e9, 1e9, 1
D: 1e9, 1e9, 1e9, 1
M = min(2e9, 2e9, 2e9, 2) = 2.
Pairs:
(1e9,1e9): diff=0 ≤1, no constraint.
(1e9,1e9): no.
(1e9,1): diff=1e9-1 > 1. min=1, so H ≤ 1+1=2. So H ≤ 2.
M=2, so H* = min(2,2) = 2.
Sum = 2e9+2e9+2e9+2 = 6e9+2.
Cost = (6e9+2) - 4*2 = 6e9+2 - 8 = 5999999994. Matches sample!

Sample 4:
N=15, X=128.
Let's compute quickly.
U: 748,586,972,432,408,138,656,632,984,404,155,832,353,387,567
D: 169,329,529,519,587,249,114,299,755,772,506,854,465,374,385
M = min of sums.
Sums:
748+169=917
586+329=915
972+529=1501
432+519=951
408+587=995
138+249=387
656+114=770
632+299=931
984+755=1739
404+772=1176
155+506=661
832+854=1686
353+465=818
387+374=761
567+385=952
M = 387.

Check pairs where |U_i - U_{i+1}| > 128.
(748,586): diff=162 >128. min=586. H ≤ 586+128=714.
(586,972): diff=386 >128. min=586. H ≤ 714.
(972,432): diff=540 >128. min=432. H ≤ 560.
(432,408): diff=24 ≤128.
(408,138): diff=270 >128. min=138. H ≤ 266.
(138,656): diff=518 >128. min=138. H ≤ 266.
(656,632): diff=24.
(632,984): diff=352 >128. min=632. H ≤ 760.
(984,404): diff=580 >128. min=404. H ≤ 532.
(404,155): diff=249 >128. min=155. H ≤ 283.
(155,832): diff=677 >128. min=155. H ≤ 283.
(832,353): diff=479 >128. min=353. H ≤ 481.
(353,387): diff=34.
(387,567): diff=180 >128. min=387. H ≤ 515.

So min of these upper bounds: 266 (from 138+128). Also M=387, so H* = min(266, 387) = 266.
Total sum of U+D = 917+915+1501+951+995+387+770+931+1739+1176+661+1686+818+761+952 = let's sum:
917+915=1832
+1501=3333
+951=4284
+995=5279
+387=5666
+770=6436
+931=7367
+1739=9106
+1176=10282
+661=10943
+1686=12629
+818=13447
+761=14208
+952=15160
Cost = 15160 - 15*266 = 15160 - 3990 = 11170. But sample output is 9460. Hmm, mismatch.

Wait, sample 4 output is 9460. My calculation gives 11170. Let me re-check.

Did I miss something? Let's recalculate M = min of sums.
138+249=387. That's the smallest? Check others:
748+169=917
586+329=915
972+529=1501
432+519=951
408+587=995
138+249=387
656+114=770
632+299=931
984+755=1739
404+772=1176
155+506=661
832+854=1686
353+465=818
387+374=761
567+385=952
Yes, 387 is the minimum. So M=387.

But if H* = 266, then cost = 15160 - 15*266 = 15160 - 3990 = 11170. Sample says 9460. So my formula is wrong.

Let me reconsider. The cost formula: we need to reduce each tooth. But is it always possible to achieve H with cost U_i + D_i - H? Let's verify with the constraints. We set u_i' = min(U_i, H). Then d_i' = H - u_i'. We need d_i' ≤ D_i, i.e., H - min(U_i, H) ≤ D_i.
If U_i ≥ H, then min(U_i, H) = H, d_i' = 0 ≤ D_i, OK.
If U_i < H, then min(U_i, H) = U_i, d_i' = H - U_i. Need H - U_i ≤ D_i => H ≤ U_i + D_i.
So for a given H, it is feasible for tooth i iff H ≤ U_i + D_i. And the cost is indeed U_i + D_i - H.
But we also need to be able to grind the teeth. The operation reduces a tooth by 1. To get u_i' = U_i (no grinding of upper), and d_i' = H - U_i, we need to grind D_i down to H - U_i. That's D_i - (H - U_i) = U_i + D_i - H operations. Yes.

So why sample 4 gives 9460? Let me check if I can find a better H* or if my bound is wrong.

Maybe H can be larger than my min bound? Let's check the pair (138, 656). I said H ≤ 138+128=266 because |656-138|=518 > 128. But let's examine the function more carefully.
For pair (a,b) = (138, 656) with X=128.
- H ≤ 138: f_i=H, f_{i+1}=H, diff=0 ≤ 128. OK.
- 138 < H ≤ 656: f_i=138, f_{i+1}=H. diff = H - 138. Need H - 138 ≤ 128 => H ≤ 266. So for H ∈ (138, 266], OK. For H > 266, violated.
- H > 656: f_i=138, f_{i+1}=656. diff = 518 > 128. Violated.
So H must be ≤ 266. That's correct.

But wait, in sample 4, is there a way to choose H larger than 266 by not using the optimal split for some teeth? The cost formula assumed we can always achieve the minimum cost U_i + D_i - H. But is there any other constraint? We need to ensure that after grinding, the final upper teeth satisfy |u_i' - u_{i+1}'| ≤ X. We chose u_i' = min(U_i, H). But could we choose a different u_i' (not equal to min(U_i, H)) to satisfy the constraint? Yes! The condition is that there exists some choice of u_i', d_i' ≥ 0 with u_i' + d_i' = H, u_i' ≤ U_i, d_i' ≤ D_i, and |u_i' - u_{i+1}'| ≤ X. The cost would be (U_i - u_i') + (D_i - d_i') = U_i + D_i - H. So any valid choice gives the same cost! Therefore, for a fixed H, if there exists any valid assignment, the cost is exactly sum (U_i + D_i - H) = sum(U_i+D_i) - N*H. So we just need to check feasibility of H.

My feasibility analysis for a pair (U_i, U_{i+1}) is: we need to choose u_i' ∈ [0, U_i] and u_{i+1}' ∈ [0, U_{i+1}] such that u_i' + (H - u_i') = H (automatically), similarly for i+1, and |u_i' - u_{i+1}'| ≤ X. Actually, we need to choose u_i' and u_{i+1}' such that there exist d_i', d_{i+1}' with d_i' = H - u_i' ≤ D_i and d_{i+1}' = H - u_{i+1}' ≤ D_{i+1}. That is, we need u_i' ≥ H - D_i, and u_i' ≤ U_i. So u_i' ∈ [max(0, H - D_i), min(U_i, H)]. Similarly for u_{i+1}'.

Thus the constraint is: there exist u_i' ∈ [L_i, R_i] and u_{i+1}' ∈ [L_{i+1}, R_{i+1}] such that |u_i' - u_{i+1}'| ≤ X, where L_i = max(0, H - D_i), R_i = min(U_i, H).

We need to find if for a given H, there exists a sequence u_i' satisfying these interval constraints and adjacency constraints. This is a constraint satisfaction problem.

My earlier simplification assumed u_i' = R_i (i.e., min(U_i, H)). But maybe we can choose smaller u_i' to satisfy the adjacency constraint? For example, if U_i is large, we set u_i' = H (max possible). But if H is large and U_{i+1} is small, we might need to set u_{i+1}' = U_{i+1} (max possible for it), and the diff is H - U_{i+1} which could be large. But we could instead set u_i' smaller? No, because u_i' ≤ H. If U_i > H, we can set u_i' to any value in [max(0, H - D_i), H]. To reduce diff, we could set u_i' smaller. So the earlier necessary condition (H ≤ min(U_i, U_{i+1}) + X) might not be sufficient, or rather, the actual feasible set might be larger!

In my example, for pair (138, 656) with H=300, X=128.
i=1: U=138, D=249. L_1 = max(0, 300-249)=51, R_1 = min(138, 300)=138.
i=2: U=656, D=114. L_2 = max(0, 300-114)=186, R_2 = min(656, 300)=300.
We need u_1' ∈ [51,138], u_2' ∈ [186,300], and |u_1' - u_2'| ≤ 128.
Max possible u_1' is 138. Min possible u_2' is 186. Diff = 186 - 138 = 48 ≤ 128. So we can pick u_1'=138, u_2'=186. Diff 48 ≤ 128. So H=300 is feasible for this pair!

But my earlier bound said H ≤ 266. So indeed, we can choose a smaller u_2' (not equal to H) to satisfy the constraint. This is the key insight.

So the problem is: given intervals [L_i, R_i] for each i, where L_i = max(0, H - D_i), R_i = min(U_i, H), we need to find if there exists a sequence a_i with L_i ≤ a_i ≤ R_i and |a_i - a_{i+1}| ≤ X.

This is a classic reachability problem. We can process from left to right. Let the possible range for a_i be [low_i, high_i]. Initially low_1 = L_1, high_1 = R_1. For i > 1, given a_{i-1} ∈ [low_{i-1}, high_{i-1}], we need a_i ∈ [L_i, R_i] and |a_i - a_{i-1}| ≤ X. So a_i must be in [L_i, R_i] ∩ [low_{i-1} - X, high_{i-1} + X]. If this intersection is non-empty, we can set low_i = max(L_i, low_{i-1} - X), high_i = min(R_i, high_{i-1} + X). We continue. If at any point low_i > high_i, infeasible.

Since we want to maximize H, and the total cost decreases with H, we can binary search on H. For each H, we run the feasibility check in O(N). N is 2e5, so binary search with O(N log V) is fine. V can be up to 2e9, so about 31 steps. O(N log V) = 2e5 * 31 = 6.2e6, fine.

Alternatively, we can find the maximum H by some monotonicity argument. The feasibility is monotonic in H? If H is feasible, is a larger H also feasible? Not necessarily! Because increasing H increases R_i (until H > U_i) and increases L_i (since H - D_i increases). The intervals change. Let's check. If H increases, R_i = min(U_i, H) is non-decreasing. L_i = max(0, H - D_i) is non-decreasing. So the interval [L_i, R_i] might shift. The adjacency constraint might become harder or easier. Is feasibility monotonic? Not obviously. For example, if U_i are very different, increasing H might force both to be close to H, making diff large. If we decrease H, maybe we can set them to smaller values. Actually, let's test: H small, say H=0. L_i=0, R_i=0. So a_i=0 for all. Diff=0 ≤ X. Feasible. As H increases, it might become infeasible at some point, then feasible again? Unlikely. Usually these problems have the property that if H is feasible, then any H' ≤ H is also feasible? Not necessarily. Consider pair with U_1=10, U_2=0, D_1=0, D_2=10, X=1. For H=5: L1=5, R1=5; L2=0, R2=0. a1=5, a2=0, diff=5>1. Infeasible. For H=1: L1=1,R1=1; L2=0,R2=0. diff=1 ≤1. Feasible. So feasibility is not monotonic in general. So binary search might not work directly.

But we want the maximum H. We need to find the largest H such that the constraint is satisfied. Since N is 2e5, we can use ternary search? No, not convex.

Maybe we can solve directly without binary search. The condition is a system of constraints. We can think of it as: for each i, a_i ∈ [L_i, R_i], and a_{i+1} ∈ [a_i - X, a_i + X]. This is like a chain of intervals. The feasible set for a_i is an interval that propagates.

Actually, we can compute the feasible range for a_1 backward or forward. But since L_i and R_i depend on H, we need to find H such that the final feasible set is non-empty.

Alternatively, we can rephrase: We need to find H such that there exist a_i with:
max(0, H - D_i) ≤ a_i ≤ min(U_i, H)
and a_i - a_{i+1} ≤ X, a_{i+1} - a_i ≤ X.

This is equivalent to: there exists a sequence a_i such that the constraints hold. This is a linear programming feasibility problem with 2 variables per i and constraints. But since it's a chain, we can solve it efficiently.

We can think of it as: we want to choose a_i to satisfy the constraints. For a fixed H, we can run the forward propagation. The propagation gives intervals [low_i, high_i] for a_i. If at the end low_N ≤ high_N, feasible.

We need to find the maximum H. Since the intervals are piecewise linear in H, maybe we can find the critical points. The constraints are:
L_i(H) = max(0, H - D_i)
R_i(H) = min(U_i, H)

These are piecewise linear with breakpoints at H = U_i and H = D_i (for the L_i part). The L_i increases from 0 to H when H > D_i? Actually L_i = 0 for H ≤ D_i, and H - D_i for H > D_i. R_i = H for H ≤ U_i, and U_i for H > U_i.

So there are O(N) breakpoints. The maximum H is the largest integer H such that the propagation is feasible. We could binary search and check, but as noted, feasibility is not monotonic. However, maybe the maximum H is the minimum of some bounds? Let's think.

We want to minimize cost, i.e., maximize H. The constraints are linear inequalities. The set of H for which the system is feasible is a union of intervals? But we want the maximum H in the feasible set. We can find the maximum H by considering that the system is feasible if and only if certain inequalities hold. Because it's a chain, the feasibility condition can be written as: for all i, j, something. But maybe we can derive an upper bound on H similar to before but taking into account the ability to choose a_i not at the extremes.

Actually, the problem might have a simpler solution. Let's think about the dual or the tightest constraints.

We have a_i ≤ U_i, a_i ≤ H, a_i ≥ H - D_i, a_i ≥ 0.
And a_i - a_{i+1} ≤ X, a_{i+1} - a_i ≤ X.

We can try to bound H. Consider any two indices i and j. The difference |a_i - a_j| ≤ (j-i)X. Also a_i ∈ [max(0, H-D_i), min(U_i, H)].

If H is very large, say H > U_i for many i, then R_i = U_i. So a_i ∈ [max(0, H-D_i), U_i]. For this to be non-empty, we need H - D_i ≤ U_i => H ≤ U_i + D_i. This is the same as before. So H ≤ M = min_i (U_i + D_i).

Also, if H is large, L_i = H - D_i (assuming H > D_i). Then a_i ≥ H - D_i. So a_i is at least H - D_i. The difference between a_i and a_{i+1} is at most X. So (H - D_i) - U_{i+1} ≤ X? Not necessarily, because a_{i+1} can be as low as H - D_{i+1} and as high as U_{i+1}. Actually, to satisfy a_i - a_{i+1} ≤ X, we need that there exist values. The tightest constraint comes from the worst-case values.

We can think of the problem as: we need to find if there exists a sequence a_i such that:
L_i ≤ a_i ≤ R_i
a_i - a_{i+1} ≤ X
a_{i+1} - a_i ≤ X

This is equivalent to: for all i, max(L_i, L_{i+1} - X) ≤ min(R_i, R_{i+1} + X). But that's local. For the whole chain, we need to check the propagation.

The propagation can be done in O(N) for a given H. To find the maximum H, we can binary search on H if the feasibility is monotonic. Is it monotonic? Let's test the earlier counterexample: U=(10,0), D=(0,10), X=1.
H=1: L1=1,R1=1; L2=0,R2=0. Feasible.
H=2: L1=2,R1=2; L2=0,R2=0. diff=2>1. Infeasible.
H=3: L1=3,R1=3; L2=0,R2=0. Infeasible.
H=10: L1=10,R1=10; L2=0,R2=0. Infeasible.
H=11: L1=10,R1=10; L2=1,R2=0? Wait U2=0, so R2=0. L2=max(0,11-10)=1. So L2=1 > R2=0. Infeasible immediately.
So feasible for H=1, infeasible for H=2,3,4,... So the set of feasible H is {1} maybe also 0. It's not monotonic. So binary search for the maximum feasible H would fail if we assume monotonicity.

But in that example, the maximum H is 1. We could find it by checking H from M downwards? M = min(10+0, 0+10) = 10. For H=10: L1=10,R1=10; L2=0,R2=0. Infeasible. H=9: similar. So we need to check each H from M down? That's O(N * M) too big.

But maybe the maximum H is actually the minimum of some set of upper bounds. Let's analyze the constraints more carefully.

We need a_i ∈ [L_i, R_i]. The adjacency constraint means that the sequence a_i must be "X-smooth". This is like we have a path. The set of feasible a_i is an interval that can be computed by forward/backward propagation. The propagation gives the range of possible a_i values. At the end, we need the intersection of forward and backward ranges to be non-empty.

Alternatively, we can think of it as: we need to find if there exists a_i such that all constraints hold. This is a difference constraints system. We can write it as:
a_i - a_{i+1} ≤ X
a_{i+1} - a_i ≤ X
a_i ≤ R_i
-a_i ≤ -L_i

This is a system of inequalities. The feasibility can be checked by Bellman-Ford or by topological order since it's a chain. But here L_i and R_i depend on H. We can treat H as a variable and find the maximum H such that the system is feasible.

The system is feasible iff for all i, the range [L_i, R_i] intersects the X-neighborhood of the next range. More precisely, we can compute the set of possible values for a_1 by working backwards or forwards.

Let's try to find an explicit formula for the maximum H. Perhaps the problem has a known solution: the answer is sum(U_i + D_i) - N * H_max, and H_max is the minimum over i of some function.

Let's consider the constraints in terms of H. For each i, a_i must be at least H - D_i (if H > D_i) and at most U_i (if H > U_i) or H (if H ≤ U_i). And a_i must be within X of a_{i+1}.

We can think of the "tightest" constraints on H. Suppose we want H large. Then for each i, a_i is roughly H - D_i (if we set a_i as small as possible to help the adjacency). Actually, to allow a_i to be close to a_{i+1}, we might want a_i to be as small as possible or as large as possible depending on the differences.

Let's define b_i = H - a_i. Then d_i' = b_i. The constraints become:
b_i = H - a_i.
a_i ∈ [max(0, H-D_i), min(U_i, H)] => b_i ∈ [max(0, H - min(U_i, H)), max(0, H - max(0, H-D_i))]? Messy.

Better: a_i ≤ U_i, a_i ≤ H, a_i ≥ H - D_i, a_i ≥ 0.
And |a_i - a_{i+1}| ≤ X.

We can try to find the maximum H by considering that for each i, a_i must be chosen. The worst-case for the adjacency is when U_i and U_{i+1} are very different, but we can compensate by using the D_i.

Let's look at the sample 4 again to see what H* should be. Sample output 9460.
Sum = 15160. N=15. So N*H* = 15160 - 9460 = 5700. H* = 5700 / 15 = 380.
So the maximum H is 380. But M = 387. And my bound gave 266. So H* = 380.

Let's check if H=380 is feasible. We need to find a_i for H=380.
Compute L_i and R_i for H=380:
i=1: U=748, D=169. R1 = min(748,380)=380. L1 = max(0, 380-169)=211. So a1 ∈ [211,380].
i=2: U=586, D=329. R2 = min(586,380)=380. L2 = max(0,380-329)=51. a2 ∈ [51,380].
i=3: U=972, D=529. R3=380, L3=0 (380-529<0). a3 ∈ [0,380].
i=4: U=432, D=519. R4=380, L4=0. a4 ∈ [0,380].
i=5: U=408, D=587. R5=380, L5=0. a5 ∈ [0,380].
i=6: U=138, D=249. R6 = min(138,380)=138. L6 = max(0,380-249)=131. a6 ∈ [131,138].
i=7: U=656, D=114. R7=380, L7=266 (380-114=266). a7 ∈ [266,380].
i=8: U=632, D=299. R8=380, L8=81. a8 ∈ [81,380].
i=9: U=984, D=755. R9=380, L9=0. a9 ∈ [0,380].
i=10: U=404, D=772. R10=380, L10=0. a10 ∈ [0,380].
i=11: U=155, D=506. R11=155, L11=0. a11 ∈ [0,155].
i=12: U=832, D=854. R12=380, L12=0. a12 ∈ [0,380].
i=13: U=353, D=465. R13=353, L13=0. a13 ∈ [0,353].
i=14: U=387, D=374. R14=380? min(387,380)=380. L14=6. a14 ∈ [6,380].
i=15: U=567, D=385. R15=380, L15=0. a15 ∈ [0,380].

Now we need to choose a_i in these intervals with |a_i - a_{i+1}| ≤ 128.
Let's try to see if feasible.
Start with a1 ∈ [211,380].
a2 ∈ [51,380] and |a1-a2| ≤128 => a2 ∈ [a1-128, a1+128] ∩ [51,380].
If we pick a1=211, a2 ∈ [83,339] ∩ [51,380] = [83,339]. So a2 can be 83.
Then a3 ∈ [0,380] and |a2-a3| ≤128. If a2=83, a3 ∈ [0,211] ∩ [0,380] = [0,211]. So a3 can be 0.
a4: a3=0, a4 ∈ [0,128] ∩ [0,380] = [0,128].
a5: a4=0, a5 ∈ [0,128].
a6: a5=0, a6 ∈ [131,138] but a5=0 so a6 must be in [0,128] ∩ [131,138] = empty! So a5 cannot be 0 if a6 must be ≥131.
We need a5 to be at least 131-128=3? Actually a6 ∈ [131,138], so a5 must be in [131-128, 138+128] = [3,266] intersected with a5's range [0,380] and previous constraints.
Let's propagate properly.

We can do forward propagation:
i=1: [211, 380]
i=2: intersect [51,380] with [211-128, 380+128] = [83, 339]? Wait: a2 must be in [51,380] and [a1-128, a1+128]. Since a1 can be up to 380, the union over a1 is [211-128, 380+128] = [83, 508]. Intersect with [51,380] gives [83, 380]. But we also need to track the possible range. Actually, we can compute the range of possible a_i values given the past.
Start: lo=211, hi=380.
i=2: lo = max(51, 211-128) = max(51,83)=83. hi = min(380, 380+128)=380. So [83,380].
i=3: L3=0, R3=380. lo = max(0, 83-128)=0. hi = min(380, 380+128)=380. So [0,380].
i=4: L4=0, R4=380. lo = max(0, 0-128)=0. hi = min(380, 380+128)=380. [0,380].
i=5: L5=0, R5=380. lo = max(0, 0-128)=0. hi = 380. [0,380].
i=6: L6=131, R6=138. lo = max(131, 0-128) = 131. hi = min(138, 380+128)=138. [131,138].
i=7: L7=266, R7=380. lo = max(266, 131-128)=266. hi = min(380, 138+128)=266. So lo=266, hi=266. Forced to 266.
i=8: L8=81, R8=380. lo = max(81, 266-128)=138. hi = min(380, 266+128)=380. [138,380].
i=9: L9=0, R9=380. lo = max(0, 138-128)=10. hi = min(380, 380+128)=380. [10,380].
i=10: L10=0, R10=380. lo = max(0, 10-128)=0. hi = 380. [0,380].
i=11: L11=0, R11=155. lo = max(0, 0-128)=0. hi = min(155, 380+128)=155. [0,155].
i=12: L12=0, R12=380. lo = max(0, 0-128)=0. hi = min(380, 155+128)=283. [0,283].
i=13: L13=0, R13=353. lo = max(0, 0-128)=0. hi = min(353, 283+128)=353. [0,353].
i=14: L14=6, R14=380. lo = max(6, 0-128)=6. hi = min(380, 353+128)=380. [6,380].
i=15: L15=0, R15=380. lo = max(0, 6-128)=0. hi = min(380, 380+128)=380. [0,380].
Final lo=0 ≤ hi=380. Feasible! So H=380 works.

Now, is H=381 feasible? Let's check M=387, so H=381.
Compute L_i for H=381:
i=1: L1 = max(0,381-169)=212. R1=380? min(748,381)=380. So [212,380].
i=2: L2 = max(0,381-329)=52. R2=380. [52,380].
i=3: L3=0, R3=380. [0,380].
i=4: L4=0, R4=380. [0,380].
i=5: L5=0, R5=380. [0,380].
i=6: L6 = max(0,381-249)=132. R6=138. [132,138].
i=7: L7 = 381-114=267. R7=380. [267,380].
i=8: L8=82, R8=380.
i=9: L9=0, R9=380.
i=10: L10=0, R10=380.
i=11: L11=0, R11=155.
i=12: L12=0, R12=380.
i=13: L13=0, R13=353.
i=14: L14=7, R14=380.
i=15: L15=0, R15=380.

Now forward:
i=1: [212,380]
i=2: lo=max(52,212-128=84)=84, hi=min(380,380+128)=380. [84,380]
i=3: lo=max(0,84-128)=0, hi=380. [0,380]
i=4: lo=0, hi=380. [0,380]
i=5: lo=0, hi=380. [0,380]
i=6: lo=max(132,0-128)=132, hi=min(138,380+128)=138. [132,138]
i=7: lo=max(267,132-128=4)=267, hi=min(380,138+128=266)=266. lo=267 > hi=266. Infeasible! So H=381 is not feasible.

Thus H* = 380. And the answer is 15160 - 15*380 = 15160 - 5700 = 9460. Perfect.

So the problem is: find the maximum integer H such that the forward propagation (or equivalently, the existence of a_i) is feasible. Since the feasibility check is O(N) and we need to find the maximum H, we can do a binary search if the feasibility is monotonic. But we saw a counterexample where feasibility is not monotonic. However, in that counterexample, H was small. For the maximum H, maybe it is monotonic in the sense that if H is feasible, then all H' < H are also feasible? Let's check: if H=380 is feasible, is H=379 feasible? Likely yes. Is it possible that H is feasible but H+1 is not, but H+2 is feasible again? Let's think.

The constraints are: a_i ∈ [L_i(H), R_i(H)], where L_i(H) = max(0, H - D_i), R_i(H) = min(U_i, H). As H increases, L_i(H) increases (weakly) and R_i(H) increases (weakly). The set of allowed a_i shifts to the right and possibly shrinks or expands. The adjacency constraint is a_i - a_{i+1} ≤ X and a_{i+1} - a_i ≤ X. If we have a feasible assignment for H, can we always get one for H+1? Not necessarily. But for the purpose of finding the maximum H, we can note that the condition is equivalent to: there exists a sequence a_i such that for all i:
a_i ≤ U_i
a_i ≤ H
a_i ≥ H - D_i
a_i ≥ 0
a_i - a_{i+1} ≤ X
a_{i+1} - a_i ≤ X.

This is a system of linear inequalities. The set of H for which the system is feasible is an interval [0, H_max]? Or is it a union of intervals? Let's test with the counterexample: U=(10,0), D=(0,10), X=1.
H=0: L1=0,R1=0; L2=0,R2=0. a1=a2=0. Feasible.
H=1: L1=1,R1=1; L2=0,R2=0. a1=1,a2=0. |1-0|=1≤1. Feasible.
H=2: L1=2,R1=2; L2=0,R2=0. a1=2,a2=0. |2-0|=2>1. Infeasible.
H=3 to 10: similarly infeasible.
H=11: L1=10,R1=10; L2=1,R2=0. L2>R2, infeasible.
So feasible for H=0,1. Infeasible for H≥2. So the set of feasible H is {0,1}, which is an interval [0,1] (if we consider integers, it's contiguous). Is it always a prefix? That is, if H is feasible, is every H' < H feasible? In this example, yes. Let's test another: U=(5,0), D=(0,5), X=1.
H=0: feasible.
H=1: L1=1,R1=1; L2=0,R2=0. a1=1,a2=0. diff=1. Feasible.
H=2: L1=2,R1=2; L2=0,R2=0. diff=2>1. Infeasible.
H=3: L1=3,R1=3; L2=0,R2=0. Infeasible.
H=4: L1=4,R1=4; L2=0,R2=0. Infeasible.
H=5: L1=5,R1=5; L2=0,R2=0. Infeasible.
H=6: L1=5,R1=5; L2=1,R2=0. Infeasible.
So feasible for H=0,1. Again prefix.

What about U=(0,10), D=(10,0), X=1.
H=0: feasible.
H=1: L1=0,R1=0; L2=1,R2=1. a1=0,a2=1. diff=1. Feasible.
H=2: L1=0,R1=0; L2=2,R2=2. diff=2>1. Infeasible.
H=3: L1=0,R1=0; L2=3,R2=3. Infeasible.
...
H=10: L1=0,R1=0; L2=10,R2=10. Infeasible.
H=11: L1=1,R1=0? U1=0 so R1=0. L1=1>0. Infeasible.
So feasible for H=0,1. Prefix.

Can we have a case where H is feasible, H+1 is not, but H+2 is feasible? Suppose U=(10,0,10), D=(0,10,0), X=1.
Indices: 1,2,3.
We need |a1-a2|≤1, |a2-a3|≤1.
H=1: a1∈[1,1], a2∈[0,0], a3∈[1,1]. a1=1,a2=0,a3=1. |1-0|=1, |0-1|=1. Feasible.
H=2: a1∈[2,2], a2∈[0,0], a3∈[2,2]. a1=2,a2=0,a3=2. |2-0|=2>1. Infeasible.
H=3: a1=3,a2=0,a3=3. Infeasible.
H=4: a1=4,a2=0,a3=4. Infeasible.
H=10: a1=10,a2=0,a3=10. Infeasible.
H=11: a1: U1=10,D1=0 => L1=11, R1=10. Infeasible.
So still prefix.

What if we have more teeth? The constraints are like a path. The feasible set of a_i is an interval. As H increases, the intervals [L_i, R_i] shift. The propagation is essentially: we maintain a range [lo, hi] for the current a_i. At each step, we intersect with [L_i, R_i] and shift by X. The condition lo ≤ hi must hold. As H increases, L_i and R_i change. The intersection and shift are monotone? Let's analyze the recurrence:
Let I_i(H) = [L_i(H), R_i(H)]. The feasible set for a_i is F_i(H) = I_i(H) ∩ (F_{i-1}(H) + [-X, X]), where F_1(H) = I_1(H). We want F_N(H) non-empty.
The operations are: intersection and Minkowski sum with [-X, X]. Both are monotone with respect to set inclusion. If H1 < H2, is I_i(H1) ⊆ I_i(H2)? Not necessarily. L_i(H) = max(0, H - D_i). This is non-decreasing in H. R_i(H) = min(U_i, H) is non-decreasing in H. So both endpoints are non-decreasing. Thus I_i(H) is shifting right or staying. However, the length R_i - L_i might decrease. For example, if H increases past U_i, R_i becomes constant at U_i, while L_i continues to increase. So the interval shrinks from the left. So I_i(H) is not necessarily contained in I_i(H') for H > H'. So the feasible set might not be monotone.

But can F_N(H) be empty, F_N(H+1) empty, but F_N(H+2) non-empty? That would require that increasing H somehow helps. Intuitively, increasing H tightens the constraints because it forces a_i to be larger (L_i increases) but also allows larger a_i (R_i increases). The adjacency constraint limits differences. If H is too large, the lower bounds L_i are too high and differ too much. If we increase H, the lower bounds increase, potentially making differences larger. So it seems that if H is too large, it becomes infeasible, and increasing H further only makes it worse. So the set of feasible H is a prefix [0, H_max]. Let's try to prove or find a counterexample.

Suppose H is infeasible. Then for some i, the interval becomes empty. The emptiness is due to lo > hi. lo = max(L_i, lo_prev - X), hi = min(R_i, hi_prev + X). As H increases, L_i increases, R_i increases (or stays). lo_prev might increase or stay, hi_prev might increase or stay. The new lo = max(L_i, lo_prev - X). Since L_i increases and lo_prev - X increases (if lo_prev increases), lo is non-decreasing. Similarly, hi = min(R_i, hi_prev + X). R_i is non-decreasing, hi_prev + X is non-decreasing, so hi is non-decreasing? Actually, min of two non-decreasing functions is non-decreasing. So lo is non-decreasing with H, and hi is non-decreasing with H. The condition lo ≤ hi. Since both lo and hi are non-decreasing in H, the set of H where lo ≤ hi is a union of intervals, but since lo and hi are integer-valued piecewise constant or increasing, once lo > hi, can it become lo ≤ hi again? For lo to decrease, it would need that max(L_i, lo_prev - X) decreases. L_i is non-decreasing, so it never decreases. lo_prev - X: if lo_prev is non-decreasing, then lo_prev - X is non-decreasing. So lo is non-decreasing. Similarly, hi is non-decreasing. So the difference hi - lo is not necessarily monotone, but lo is non-decreasing and hi is non-decreasing. The condition lo ≤ hi: if at some H we have lo > hi, then for any H' > H, lo(H') ≥ lo(H) > hi(H) and hi(H') ≥ hi(H). But we could have hi(H') increasing faster? However, lo(H') ≥ lo(H) and hi(H') ≥ hi(H). It's possible that hi(H') - lo(H') becomes positive again? For that, we need hi(H') to increase more than lo(H'). But since both are bounded, it's theoretically possible? Let's see.

We need lo(H) = max(L_i(H), lo_{i-1}(H) - X). Since L_i is non-decreasing, the only way lo could decrease is if lo_{i-1} - X decreases. But lo_{i-1} is also non-decreasing. So by induction, all lo_i and hi_i are non-decreasing in H. Because base: lo_1 = L_1, hi_1 = R_1, both non-decreasing. Assume lo_{i-1}, hi_{i-1} are non-decreasing. Then lo_i = max(L_i, lo_{i-1} - X). Both arguments are non-decreasing, so max is non-decreasing. hi_i = min(R_i, hi_{i-1} + X). Both arguments are non-decreasing, so min is non-decreasing. Therefore, lo_i and hi_i are non-decreasing functions of H. The condition lo_N ≤ hi_N. Since both are non-decreasing, the set of H where lo_N ≤ hi_N is of the form [0, H_max] for integers? Not necessarily: if lo_N and hi_N are non-decreasing, lo_N - hi_N is not necessarily monotone. But we can have lo_N > hi_N at H, and lo_N stays > hi_N, or could it cross? Since lo_N is non-decreasing and hi_N is non-decreasing, the difference could be anything. But note that lo_N and hi_N are piecewise constant or linearly increasing. Actually, L_i and R_i are piecewise linear with slope 0 or 1. The operations max, min, and adding X preserve this. So lo_N and hi_N are piecewise linear non-decreasing functions. The condition lo_N ≤ hi_N. If at some H0, lo_N(H0) > hi_N(H0), then since both are non-decreasing, for H > H0, lo_N(H) ≥ lo_N(H0) > hi_N(H0) and hi_N(H) ≥ hi_N(H0). But could hi_N(H) become larger than lo_N(H)? For that, we need hi_N(H) - lo_N(H) > 0. At H0, it's negative. The derivative (slope) of hi_N and lo_N are either 0 or 1 (since max of non-decreasing functions, etc.). Actually, the slope of max is the max of slopes where they are equal? Not exactly, but the slope of max of two functions with slopes 0 or 1 is 0 or 1. Similarly for min. So the slopes are 0 or 1. The difference hi_N - lo_N has slope in {-1,0,1}. It can go up and down. So it is possible that lo_N > hi_N at H0, but at H1 > H0, lo_N increases by 0, hi_N increases by 1, so lo_N = hi_N? But we need lo_N ≤ hi_N. If lo_N > hi_N at H0, then at H0+1, lo_N could stay same, hi_N increase by 1, so they could become equal. So the set of feasible H is not necessarily a prefix. Example: lo(H) = H, hi(H) = H+1? Then lo ≤ hi always. To have lo > hi, we need lo >= hi+1. Suppose lo(H) = H, hi(H) = H-1 for H≥1. Then lo > hi. But at H=0, lo=0, hi=-1? Not possible. Let's try to construct a case.

We need lo and hi piecewise linear with slopes 0 or 1. Let's design lo and hi directly. lo(H) = 0 for H<5, then H-5 for H≥5. hi(H) = H for H<3, then 3 for H≥3? Wait, hi is non-decreasing. hi(H) = H for H≤3, then 3 for H>3? That's not non-decreasing? H increases, then drops to 3. No, hi must be non-decreasing. So hi cannot drop. So hi is non-decreasing, lo is non-decreasing. If lo > hi at H0, then lo(H0) > hi(H0). For H > H0, lo(H) ≥ lo(H0) and hi(H) ≥ hi(H0). It's possible that hi(H) increases while lo(H) stays constant. For example, lo(H) = 10 for all H ≥ 5. hi(H) = H for H ≤ 10, then 10 for H > 10. Then at H=9, lo=10, hi=9 => lo>hi. At H=10, lo=10, hi=10 => lo=hi. So feasible at H=10 but not at H=9. So the feasible set is not a prefix: feasible for H=10, but not for H=9. But wait, is that possible in our propagation? lo and hi come from specific functions. But in our problem, H is the parameter. If H=9 is infeasible, can H=10 be feasible? Let's test if such a scenario can occur.

Suppose we have a single tooth: N=1. Then condition is just that L1 ≤ R1. L1 = max(0, H-D1), R1 = min(U1, H). We need L1 ≤ R1. This is equivalent to H ≤ U1 + D1. So feasible for H ≤ U1+D1. That's a prefix.

For N>1, could we have a non-prefix feasible set? Let's try to construct. We need lo_N > hi_N at H, but lo_N ≤ hi_N at H+1. Since lo_N and hi_N are non-decreasing, this means that at H, lo_N > hi_N. At H+1, either lo_N stays same and hi_N increases, or lo_N increases and hi_N increases more, or both increase but hi_N increases more.

Consider a simple case N=2. lo_2 = max(L2, lo_1 - X). hi_2 = min(R2, hi_1 + X). lo_1 = L1, hi_1 = R1.
All functions are non-decreasing.
Suppose at H, lo_2 > hi_2. At H+1, we need lo_2 ≤ hi_2.
Since lo_2 and hi_2 are integers, and their slopes are 0 or 1, the difference hi_2 - lo_2 can increase by at most 1 when H increases by 1 (if lo slope 0, hi slope 1) or stay same (if both 0 or both 1), or decrease (if lo slope 1, hi slope 0). So if at H we have hi - lo = -1, at H+1 it could be 0. So feasible set could be like: infeasible at H, feasible at H+1. But then what about H+2? It could be infeasible again? If at H+1, lo and hi have slopes? Once feasible, can it become infeasible again? If hi - lo becomes negative again, that means lo increases and hi doesn't, or lo increases more. But since both are non-decreasing, if at some point hi - lo > 0, can it become negative again? For that, we need lo to increase and hi to stay same. That is possible. For example, lo(H) = H, hi(H) = H. Then hi - lo = 0 always. Not negative. To have hi - lo negative then positive then negative, we need the difference to change sign multiple times. Since the difference has slope in {-1,0,1}, it can oscillate. So the feasible set is a union of intervals. However, we are looking for the maximum feasible H. So we can't just binary search for the largest H in a prefix. We need to find the maximum H that is feasible. Since the feasible set is a union of intervals, the maximum H is the right endpoint of the last interval.

But we can find the maximum H by noting that the total cost is minimized at the maximum H, and we can use a "reverse" argument or a different approach.

Wait, is the cost function C(H) = sum(U_i+D_i) - N*H? This is linear decreasing in H. So to minimize cost, we want the maximum feasible H. So we need the maximum H such that the system is feasible.

We can solve this by finding the maximum H directly. Since the feasibility condition can be checked in O(N), and H is in [0, M] where M = min(U_i+D_i), we can find the maximum H by iterating H from M downwards until feasible? That's O(N * M) too big.

But we can use the fact that the feasible set is a union of intervals, and we want the maximum H. We can do a binary search on H, but we need a way to check if there exists any feasible H' ≥ H. That is, we need to check if the maximum feasible H is ≥ H. This is a monotonic property: if there exists a feasible H' ≥ H, then the answer is ≥ H. So we can binary search on H to find the maximum H such that there exists a feasible H' ≥ H. This is a different check: we need to know if the system is feasible for some H' ≥ H, not necessarily exactly H. But we want the maximum feasible H, so we can binary search on H and for each H, check if the system is feasible for some H' in [H, M]? That might be complicated.

Alternatively, we can use the fact that the condition is equivalent to: there exists a sequence a_i such that for all i:
a_i ≤ U_i
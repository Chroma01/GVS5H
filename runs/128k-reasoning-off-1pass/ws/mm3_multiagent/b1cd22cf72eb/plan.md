We need to choose a target sum H and reduce upper and lower tooth lengths (only decreasing) so that for every i, U_i' + D_i' = H, and the resulting U_i' sequence is X‑Lipschitz (|U_i' - U_{i+1}'| ≤ X). The cost equals total reduction = Σ (U_i + D_i - H). Since D_i' = H - U_i', we just decide final U_i' (≤ U_i) and set D_i' = H - U_i' (which must be ≤ D_i, i.e., U_i' ≥ U_i + D_i - H, so U_i' ≥ max(0, U_i + D_i - H)). To minimize cost, we want U_i' as large as possible, so U_i' = max(0, U_i + D_i - H). So total cost for a given H is Σ (U_i + D_i - H) over i with H > U_i + D_i, i.e., Σ max(0, S_i - H) where S_i = U_i + D_i.

Now we also need the Lipschitz constraint. Since U_i' = max(0, S_i - H) is non‑increasing in H, we can binary search the optimal H. The remaining problem: for a fixed H, is there a way to pick upper lengths U_i' (≤ U_i) with lower bound L_i = max(0, S_i - H) and sum constraint Σ U_i' = N*H - total_reduction? Actually we just need to check if we can pick U_i' satisfying bounds and Lipschitz, and also the implied D_i' = H - U_i' ≤ D_i (which is equivalent to U_i' ≥ S_i - H, already in L_i). So we need to check feasibility of a sequence A_i with L_i ≤ A_i ≤ U_i, |A_i - A_{i+1}| ≤ X. The cost then is Σ (U_i - A_i) + Σ (D_i - (H - A_i)) = Σ (U_i + D_i) - N*H, which depends only on H, not on the A_i choice! So feasibility is just about existence.

Feasibility check can be done with interval DP: maintain a range [low, high] of possible A_i values after processing i teeth. Initialize low=high=0 (A_0 = 0 reference). For i from 1..N: new_low = max(L_i, low - X), new_high = min(U_i, high + X). If new_low > new_high, infeasible. After processing all, any value in [low, high] works. This is O(N). Then binary search H in [0, max(S_i) + max(U_i) maybe], but H is bounded by S_i + U_i (max possible after reducing D to 0). Actually upper bound for H can be max(S_i) + max possible extra (U_i can be up to 1e9, but H can be up to S_i + U_i? No, we can only decrease teeth, so U_i' ≤ U_i, D_i' ≤ D_i, and U_i' + D_i' = H, so H ≤ U_i + D_i = S_i for all i where we reduce? Actually H can be larger than S_i: we can't increase teeth, so if H > S_i, we cannot make U_i' + D_i' = H because sum of max possible values is S_i. Wait, U_i' ≤ U_i, D_i' ≤ D_i, so U_i' + D_i' ≤ S_i. Thus H ≤ min_i S_i. So H must be ≤ min S_i. Lower bound is 0 (or maybe 1 since lengths positive? But we can grind to 0). So H ∈ [0, min_S].

Cost(H) = Σ max(0, S_i - H). This is a convex decreasing function. We binary search the largest H that is feasible. Since feasibility is monotonic in H (larger H makes L_i larger and U_i unchanged, harder to fit), we can find the maximum feasible H via binary search, then answer = Σ max(0, S_i - H). Complexity O(N log C).

Let's verify with sample 1: N=4, X=3, pairs (3,1),(4,1),(5,9),(2,6) → S=[4,5,14,8]. min_S=4. Feasibility at H=4: L_i = max(0, S_i-4) = [0,1,10,4]. U_i = [3,4,5,2]. Process:
i=1: [0,0]∩X→ new=[0,0] ∩ U=[0,3] → [0,0]
i=2: L=1, U=4, low=0,high=0 → [max(1,0-3), min(4,0+3)] = [1,3]
i=3: L=10, U=5 → [max(10,1-3), min(5,3+3)] = [10,5] infeasible.
So H=4 not feasible. Try H=5: L=[0,0,9,3] U=[3,4,5,2].
i=1: [0,0]
i=2: L=0, U=4 → [max(0,0-3), min(4,0+3)] = [0,3]
i=3: L=9, U=5 → infeasible. H=5 not feasible.
H=6: L=[0,0,8,2] U=[3,4,5,2]
i=1: [0,0]
i=2: [0,3]
i=3: L=8, U=5 infeasible.
...
We need H larger to reduce L_i? Wait, larger H means L_i = S_i - H becomes negative → 0, so constraints relax! I had it backwards: L_i = max(0, S_i - H). As H increases, S_i - H decreases, so L_i decreases (or stays 0). So feasibility improves with larger H. So we want the maximum feasible H, which is min_S = 14? Let's check H=14: L = [0,0,0,0] U=[3,4,5,2]. Lipschitz with X=3: sequence 3,4,5,2 has |3-4|=1, |4-5|=1, |5-2|=3 ≤3, feasible. Cost = Σ max(0,S_i-14) = max(0,4-14)+max(0,5-14)+max(0,14-14)+max(0,8-14) = 0. But sample answer is 15, not 0. Wait, the problem says we can only decrease teeth. But we need U_i' + D_i' = H. If H=14, U_i' ≤ U_i, D_i' ≤ D_i. S_3 = 5+9=14, so U_3' ≤5, D_3' ≤9, U_3'+D_3'=14 possible (e.g., 5+9). S_4 = 2+6=8, but H=14 > 8, impossible! Because we cannot increase sum. So H ≤ S_i for all i, i.e., H ≤ min S_i = 4. I confused min and max. Indeed, H must be ≤ S_i for every i, so H ≤ min S_i. For sample 1, min S_i = 4. So H ∈ [0,4]. Feasibility monotonic decreasing in H? Let's check: H=4 was infeasible. H=3: L=[1,2,11,5]? Wait S_i-H: 4-3=1, 5-3=2, 14-3=11, 8-3=5. L_i = [1,2,11,5] but U_i = [3,4,5,2]. L_3=11 > U_3=5 infeasible. H=2: L=[2,3,12,6] even worse. H=0: L=[4,5,14,8] impossible. So no H ≤4 feasible? But sample says 15 is answer. Let's re‑examine.

Wait, I made an error: U_i' + D_i' = H. We can only decrease teeth. So U_i' ≤ U_i, D_i' ≤ D_i. We choose U_i' freely ≤ U_i, and D_i' = H - U_i'. For D_i' ≤ D_i, we need H - U_i' ≤ D_i → U_i' ≥ H - D_i. Also U_i' ≤ U_i. So U_i' ∈ [max(0, H - D_i), U_i]. Also U_i' ≥ 0. Additionally, D_i' ≥ 0 → H - U_i' ≥ 0 → U_i' ≤ H. So overall U_i' ∈ [max(0, H - D_i), min(U_i, H)]. For this to be non‑empty, we need max(0, H - D_i) ≤ min(U_i, H), i.e., H - D_i ≤ U_i and H - D_i ≤ H (always) and 0 ≤ U_i and 0 ≤ H. So H ≤ U_i + D_i = S_i for all i. So H ≤ min S_i = 4. And for each i, the feasible interval for U_i' is [L_i, R_i] where L_i = max(0, H - D_i), R_i = min(U_i, H).

For H=4:
i=1: U=3, D=1 → L=max(0,4-1)=3, R=min(3,4)=3 → {3}
i=2: U=4, D=1 → L=3, R=min(4,4)=4 → [3,4]
i=3: U=5, D=9 → L=0, R=4 → [0,4]
i=4: U=2, D=6 → L=0, R=2 → [0,2]
Now check Lipschitz feasibility with X=3:
i=1: interval [3,3] (low=3, high=3)
i=2: L=3, R=4, X=3 → new_low=max(3,3-3)=3, new_high=min(4,3+3)=4 → [3,4]
i=3: L=0, R=4 → new_low=max(0,3-3)=0, new_high=min(4,4+3)=4 → [0,4]
i=4: L=0, R=2 → new_low=max(0,0-3)=0, new_high=min(2,4+3)=2 → [0,2] non‑empty → feasible.
So H=4 is feasible! My earlier L_i formula was wrong. The lower bound is not S_i - H, but max(0, H - D_i). And the cost is: for each i, we can choose U_i' in [L_i, R_i] to minimize total reduction. The total reduction cost = Σ (U_i - U_i') + Σ (D_i - D_i') = Σ (U_i - U_i') + Σ (D_i - (H - U_i')) = Σ (U_i + D_i) - N*H, which is independent of U_i'! Wait, that means cost depends only on H, not on the specific U_i' chosen. So for any feasible H, the cost is Σ (U_i + D_i) - N*H. Since H ≤ min S_i, and we want to minimize cost, we want H as large as possible. So the problem reduces to finding the maximum H ≤ min S_i such that the Lipschitz feasibility holds with intervals [max(0, H-D_i), min(U_i, H)].

Feasibility is monotonic in H: as H increases, L_i = max(0, H-D_i) increases (if H > D_i) or stays 0, and R_i = min(U_i, H) increases until H > U_i then stays U_i. So intervals expand, making it easier? Actually both bounds increase, so the feasible set for U_i' grows. But the Lipschitz constraint couples them. Intuitively, larger H gives more flexibility, so feasibility is monotonic non‑decreasing in H. Let's verify: H=3:
i=1: U=3,D=1 → L=2,R=3
i=2: U=4,D=1 → L=2,R=3
i=3: U=5,D=9 → L=0,R=3
i=4: U=2,D=6 → L=0,R=2
Feasibility: i1 [2,3], i2 new=[max(2,2-3), min(3,3+3)] = [2,3], i3 new=[max(0,2-3), min(3,3+3)] = [0,3], i4 new=[max(0,0-3), min(2,3+3)] = [0,2] feasible.
H=2: i1 L=1,R=2; i2 L=1,R=2; i3 L=0,R=2; i4 L=0,R=2. Feasible.
H=1: i1 L=0,R=1; i2 L=0,R=1; i3 L=0,R=1; i4 L=0,R=1. Feasible.
H=0: L=0,R=0 for all. Feasible (all zero).
So all H in [0,4] are feasible? But sample answer is 15. Let's compute cost for H=4: Σ (U_i+D_i) = (3+1)+(4+1)+(5+9)+(2+6) = 4+5+14+8 = 31. N*H = 4*4=16. Cost = 31-16=15. That matches sample output! So H=4 gives cost 15. But we could pick H=3, cost = 31-12=19. H=2: 31-8=23. H=1: 31-4=27. H=0: 31. So indeed H=4 is optimal. My earlier statement that H ≤ min S_i is correct, and we want the maximum feasible H. In this case H=4 is feasible and is min S_i, so answer is 15.

Now the algorithm: binary search H in [0, min_S] for the maximum feasible H. Feasibility check O(N) as described. Then answer = Σ (U_i + D_i) - N * H_max. Complexity O(N log max_S). N up to 2e5, log(1e9) ~ 30, fine.

Edge cases: H can be 0. Need to handle large sums (up to 2e5 * 2e9 = 4e14, need 64-bit).

Let's test sample 3: N=4, X=1. Pairs: (1e9,1e9) three times, then (1,1). S = [2e9, 2e9, 2e9, 2]. min_S = 2. H ≤ 2. Check feasibility for H=2:
i=1,2,3: U=1e9, D=1e9 → L=2-1e9? max(0, 2-1e9) = 0, R=min(1e9,2)=2. So [0,2].
i=4: U=1, D=1 → L=max(0,2-1)=1, R=min(1,2)=1 → {1}.
X=1.
i1: [0,2], low=0, high=2.
i2: L=0,R=2 → [max(0,0-1), min(2,2+1)] = [0,2]
i3: same → [0,2]
i4: L=1,R=1 → [max(1,0-1), min(1,2+1)] = [1,1] feasible.
So H=2 feasible. Cost = Σ S_i - 4*2 = (2e9+2e9+2e9+2) - 8 = 6000000002 - 8 = 5999999994. Matches sample.

Sample 2: all S_i=6. H can be up to 6. U_i=D_i=3. For H=6: L=3,R=3. Sequence 3,3,3,3 Lipschitz with X=1e9. Feasible. Cost = 24 - 24 = 0. Matches.

Sample 4: need to trust.

Binary search details: We want max H in [0, min_S] such that feasible(H) is true. Since feasible is monotonic non‑decreasing in H, we can binary search for the largest true. Or simply linear search? Binary search is fine.

Feasibility check:
low = 0, high = 0  # represents possible A_i value
for i in range(N):
    L = max(0, H - D[i])
    R = min(U[i], H)
    low = max(L, low - X)
    high = min(R, high + X)
    if low > high: return False
return True

Need to be careful: low and high are the range of possible values for A_i (the chosen U_i'). The recurrence: A_i must be in [L,R] and |A_i - A_{i-1}| ≤ X. So A_{i-1} ∈ [A_i - X, A_i + X] ∩ [prev_low, prev_high]. Equivalently, A_i ∈ [L,R] ∩ [prev_low - X, prev_high + X]. So new_low = max(L, prev_low - X), new_high = min(R, prev_high + X). This matches.

Initially, before any tooth, we can think of A_0 as a variable with no constraint? Actually the constraint is only between consecutive teeth. The first tooth has no left neighbor constraint except its own bounds. So we can set initial low = high = 0? Wait, if we set initial low=high=0, that forces A_1 to be within X of 0. But A_1 is only constrained by its own bounds and A_2. There's no constraint on A_1 relative to 0. So we should start with low = -infinity, high = +infinity? Actually the first tooth just needs to be in [L_1, R_1]. There is no previous tooth to constrain it. So we should set low = L_1, high = R_1 for i=1, or equivalently start with low = -inf, high = +inf and then for i=1 do new_low = max(L_1, low - X) = L_1 (since low = -inf), new_high = min(R_1, high + X) = R_1. So starting with low = -10^18, high = 10^18 works. Or simply handle first tooth separately. Using large bounds is fine.

Let's verify with H=4 sample 1:
low=-inf, high=+inf.
i=1: L=3, R=3 → low=3, high=3.
i=2: L=3, R=4, X=3 → low=max(3,3-3)=3, high=min(4,3+3)=4.
i=3: L=0, R=4 → low=max(0,3-3)=0, high=min(4,4+3)=4.
i=4: L=0, R=2 → low=max(0,0-3)=0, high=min(2,4+3)=2. OK.

Implementation in Python:
- Read N, X.
- Read arrays U, D.
- Compute S = [u+d for u,d in zip(U,D)].
- min_S = min(S).
- total = sum(S).
- Binary search lo=0, hi=min_S (inclusive). We want max feasible H.
  while lo < hi:
    mid = (lo + hi + 1) // 2
    if feasible(mid): lo = mid
    else: hi = mid - 1
- ans = total - N * lo.
- Print ans.

Feasible function with H:
  low = -10**19  # or some very small number
  high = 10**19
  for i in range(N):
      L = H - D[i] if H > D[i] else 0  # max(0, H - D[i])
      if L < 0: L = 0
      R = U[i] if U[i] < H else H  # min(U[i], H)
      if L > R: return False
      low = max(L, low - X)
      high = min(R, high + X)
      if low > high: return False
  return True

Need to ensure low - X doesn't underflow Python int? Python ints are arbitrary precision, so fine. But we can use -10**18 or just float('-inf')? Better to use integer bounds: since lengths up to 1e9, N up to 2e5, max possible value for A_i is at most max(U_i) ≤ 1e9, and min is 0. So we can bound low and high to [0, 1e9] safely. Actually low can be negative due to low - X, but we can clamp. But Python handles it. To be safe, we can use low = -10**18, high = 10**18.

Let's test with H > min_S: not allowed, we restrict hi = min_S.

Test sample 1: total=31, N=4. Binary search:
lo=0, hi=4.
mid=2: feasible? check. H=2: i1 L=1,R=2; i2 L=1,R=2; i3 L=0,R=2; i4 L=0,R=2. low starts -inf. i1: [1,2]. i2: low=max(1,1-3)=1, high=min(2,2+3)=2. i3: low=max(0,1-3)=0, high=min(2,2+3)=2. i4: low=max(0,0-3)=0, high=min(2,2+3)=2. Feasible. lo=2.
lo=2, hi=4. mid=3: feasible? H=3: i1 L=2,R=3; i2 L=2,R=3; i3 L=0,R=3; i4 L=0,R=2. Process: i1 [2,3]; i2 low=max(2,2-3)=2, high=min(3,3+3)=3; i3 low=max(0,2-3)=0, high=min(3,3+3)=3; i4 low=max(0,0-3)=0, high=min(2,3+3)=2. Feasible. lo=3.
lo=3, hi=4. mid=4: feasible? Yes as checked. lo=4. Loop ends. ans = 31 - 4*4 = 15. Good.

Sample 3: N=4, X=1, S=[2e9]*3 + [2], total=6000000002, min_S=2.
lo=0, hi=2.
mid=1: H=1. i1: U=1e9,D=1e9 → L=0,R=1. i2: L=0,R=1. i3: L=0,R=1. i4: U=1,D=1 → L=0,R=1. X=1. Process: i1 [0,1]; i2 low=max(0,0-1)=0, high=min(1,1+1)=1; i3 low=0, high=1; i4 low=0, high=1. Feasible. lo=1.
lo=1, hi=2. mid=2: feasible? H=2. i1: L=0,R=2; i2: L=0,R=2; i3: L=0,R=2; i4: L=1,R=1. i1 [0,2]; i2 low=max(0,0-1)=0, high=min(2,2+1)=2; i3 low=0, high=2; i4 low=max(1,0-1)=1, high=min(1,2+1)=1. Feasible. lo=2. ans = total - 4*2 = 6000000002 - 8 = 5999999994. Good.

Edge case: what if H is very small but intervals are tight? The algorithm should handle.

Complexity: O(N log min_S) where min_S up to 2e9, log2(2e9) ~ 31. So O(2e5 * 31) ~ 6e6, fine.

One more check: The condition |U_i - U_{i+1}| ≤ X applies to the final upper teeth. Our feasibility check enforces exactly that.

Thus the solution is correct.
We need to find the minimum total cost to reduce lengths (only decreasing) so that:
1. All pairs (U_i, D_i) sum to the same H.
2. Consecutive U_i differ by at most X.

Let S_i = U_i + D_i. The final H must be ≤ min_i S_i (since we can only decrease). For a fixed H, the cost to make U_i + D_i = H is exactly Σ (S_i - H) = Σ S_i - N·H. The second condition is independent of D_i: we need to reduce U_i's (only) so that |U_i - U_{i+1}| ≤ X.

So for each H ≤ min S_i, we compute the minimum cost to make the sequence U_i (decreased to some u_i ≤ original U_i, with u_i ≤ H) satisfy the X-difference constraint, plus Σ S_i - N·H. We can binary search on H.

For a given H, we need minimum Σ (U_i - u_i) over non-increasing (or non-decreasing? we can choose any direction) sequences u_i with u_i ≤ min(U_i, H) and |u_i - u_{i+1}| ≤ X. This is a classic DP: dp[i][0/1] = minimum cost for first i teeth where u_i is at its "low bound" (0) or "high bound" (1) of feasible range. Standard interval DP with two states tracks whether the last value was chosen as low or high of its feasible range.

The feasible range for u_i is [L_i, R_i] where L_i = max(1, R_{i-1,low} - X) and R_i = min(U_i, H) with a similar update. Complexity O(N) per check. N up to 2e5 and 60+ iterations → fine.
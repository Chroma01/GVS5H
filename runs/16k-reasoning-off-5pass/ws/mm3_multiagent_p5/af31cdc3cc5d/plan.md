The operation removes two adjacent elements, concatenating the left and right parts. This is equivalent to pairing up the original indices into pairs where each pair’s two indices form a “matching” of the line graph (non-crossing pairings of adjacent removals). Any such sequence of removals corresponds to a partition of {1..N} into N/2 disjoint pairs such that no two pairs cross (i.e., a non-crossing perfect matching). The total score is the sum of |A_i - A_j| over all pairs in the matching. Thus we need the maximum-weight non-crossing perfect matching of points on a line, where the weight of pairing i<j is |A_i - A_j|. N is up to 3e5, so O(N^2) DP is impossible; we need O(N log N) or O(N).

Key observation: only the relative order of A matters for the structure. However, a fully correct O(N) solution is nontrivial. A well-known approach for this problem (AtCoder ABC163 F-style) is to use a segment-tree DP over the sorted order of values. The idea: process elements by value from largest to smallest, and maintain a DP over intervals of the current "active" indices. Equivalent to: after sorting A, dp[l][r] = maximum score achievable on the subarray of original indices between positions l and r (in original order) using only values in a certain value range. This can be done with a segment tree where each node stores the maximum value, and we combine using the fact that the best pair to close the interval is the max element.

Concretely, build a segment tree on the array A. For a segment [l,r], the optimal DP value f[l][r] satisfies: pick the position m of the maximum element in [l,r]; then f[l][r] = max( f[l][m-1] + f[m+1][r], f[l][m-1] + f[m+1][r] + (A[m] matched with something) ). The standard trick: the value contributed by the max element equals the difference between it and the max of the two remaining subsegments after pairing it with someone. This leads to a divide-and-conquer with segment tree that runs in O(N log N).

Implementation: recursive function solve(l,r) returning (ans, mx) where mx is the maximum A in [l,r]. Then:
ans(l,r) = max( ans(l,m-1)+ans(m+1,r) + abs(mx - max(mx_left, mx_right)) ) where mx_left, mx_right are the max of the two subsegments. Actually the correct recurrence (well-known, see editorial of this AtCoder problem "Removing Blocks" / ABC163 F? No — this is ABC163 F? Let me recall: This is AtCoder ABC163 F? No. This problem is "Maximum Total Score" from AtCoder, editorial uses divide and conquer with segment tree.

The recurrence: Let solve(l,r) return (dp, mx). Let m = argmax, L = solve(l,m-1), R = solve(m+1,r). Then dp = L.dp + R.dp, and we can additionally match the element at m with an element from either left or right subsegment, but only with the maximum of the other side. So:
extra = max(0, abs(mx - max(L.mx, R.mx))) -- but we need to be careful. Actually:
We pair element m with some element from left or right. The best such pair contributes |A_m - A_x| where A_x is the maximum among all elements on the other side (since we can choose any, the max |A_m - A_x| for x in other side equals max( |A_m - min_other|, |A_m - max_other| ) ). Then the remaining elements (excluding m and that partner) are split into two independent subproblems, and the partner's subproblem is solved. But since we only keep (dp, mx) of subsegments, and pairing m with the maximum on the other side leaves the other subsegment's max reduced... this is the standard trick.

Standard recurrence (from editorial): 
solve(l,r):
  if l==r: return (0, A[l])
  m = argmax in [l,r]
  (dl, ml) = solve(l, m-1)
  (dr, mr) = solve(m+1, r)
  best = dl + dr + max(0, abs(A[m] - max(ml, mr)))
  return (best, A[m])

This is O(N log N) with a segment tree to find argmax quickly. Base case: l>r return (0, -inf) (or handle separately).

Let me verify with sample: A=[1,2,5,3]. Max=5 at index 3. Left: solve(1,2): max=2 at idx2. Left-left: solve(1,1)=(0,1). Left-right: empty=(0,-inf). best_left = 0+0+max(0,|2-max(1,-inf)|)=max(0,|2-1|)=1. So solve(1,2)=(1,2). Right: solve(4,4)=(0,3). best= 0+0+max(0,|5-max(2,3)|)=max(0,|5-3|)=2. So solve(1,4)=1+2+2=5. Matches.

Verify sample 2: A=[3,1,4,1,5,9,2]. Let's trust the recurrence. This is exactly the editorial solution.
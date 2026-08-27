
## ideation
The core difficulty is that N (length of S) is small (≤10) but M (length of T) is large (≤100). We need to count, for each k=0..N, the number of strings T of length M over 26 letters such that LCS(S, T) = k. The order of T matters, so we cannot just consider multisets. However, we can process T left-to-right, maintaining the DP state of the LCS computation. The standard LCS DP can be space-optimized to O(N) by keeping an array dp[0..N] where dp[i] is the LCS of S[0..i-1] and the processed prefix of T. The update for a new character ch is: for i from N down to 1: if S[i-1] == ch: dp[i] = max(dp[i], dp[i-1] + 1) else: dp[i] = max(dp[i], dp[i-1]). The key observation is that dp[i] - dp[i-1] is always 0 or 1 (LCS can increase by at most 1 when extending S). Therefore the entire dp array is uniquely represented by a bitmask of length N where bit i-1 is 1 iff dp[i] > dp[i-1]. The number of such masks is at most 2^N ≤ 1024. This allows us to do a DP over M steps, where each step we transition from one mask to another based on the chosen character. We can precompute the transition for all 2^N masks and 26 characters. Then we run a simple DP over the M positions: cur[mask] = number of strings resulting in that mask. After M steps, the answer for k is the sum of cur[mask] over masks with popcount k.

Pitfalls:
- The 1D LCS update must use the *old* dp[i-1] when processing from right to left, but we must also handle the case of no match by taking max with dp[i-1] to propagate the maximum from the cell above. Without the else clause, the DP is incorrect (as shown with S="abc", T="bac").
- The mask representation is valid because dp is non-decreasing and differences are 0 or 1. We must correctly reconstruct the dp array from the mask and the new mask from the updated dp array.
- M can be up to 100, so we need modular arithmetic (mod 998244353) for the counts.

## worker: Enumerate all 2^N masks (0..(1<<N)-1). For each ma
The solution uses a state compression DP over the LCS computation. The key insight is that the LCS DP array `dp[0..N]` (where `dp[i]` is the LCS of S[0..i-1] with the processed prefix of T) has the property that `dp[i] - dp[i-1] ∈ {0,1}`. This allows representing the state as a bitmask of length N, where bit i-1 is set iff `dp[i] > dp[i-1]`. Since N ≤ 10, there are at most 2^10 = 1024 states.

For each state and each of the 26 possible characters, we precompute the next state by simulating the 1D LCS update. The update is: for i from N down to 1, if S[i-1] == ch: new_dp[i] = max(old_dp[i], old_dp[i-1] + 1); else: new_dp[i] = max(old_dp[i], old_dp[i-1]). This correctly handles both match and no-match cases (the max with old_dp[i-1] propagates the LCS value from the previous row).

Then we run a simple DP over the M positions of T: for each step, we multiply the counts by the transition matrix. Finally, the answer for each k is the sum of counts for masks with popcount k.

The code is self-contained, reads from stdin, and writes to stdout. It runs in O(M * 2^N * 26) time, which is about 2.6 million operations for the worst case, easily fast enough.

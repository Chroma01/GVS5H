The problem asks if we can transform string S into string T using at most K edit operations (insert, delete, replace). This is exactly the Levenshtein distance (edit distance) problem. However, since K is very small (≤ 20) and the strings can be long (up to 500,000), a standard O(|S|*|T|) DP is too slow. We need an optimized approach.

Key insight: If the edit distance is ≤ K, then the length difference | |S| - |T| | must be ≤ K. If | |S| - |T| | > K, output "No" immediately.

Otherwise, we can use a bounded DP approach. Since K is small, we only need to track a band of width 2K+1 around the diagonal in the DP table. Specifically, for computing dp[i][j] (edit distance between S[0..i-1] and T[0..j-1]), we know that if |i-j| > K, the distance cannot be ≤ K. So we only compute dp[i][j] where |i-j| ≤ K.

We can optimize space by using only two rows (current and previous) and iterating i from 0 to |S|, and for each i, j ranges from max(0, i-K) to min(|T|, i+K). The base cases are dp[0][j] = j and dp[i][0] = i, but we only care about values ≤ K.

If the final dp[|S|][|T|] ≤ K, output "Yes", else "No".
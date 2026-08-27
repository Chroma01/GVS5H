1. Define prefix sums for `nums` and `cost` to allow O(1) calculation of subarray sums.
2. Use dynamic programming where `dp[i]` represents the minimum cost to partition the first `i` elements (`nums[0..i-1]`).
3. The recurrence relation is: `dp[i] = min(dp[j] + cost_of_subarray(j, i))` for all `0 <= j < i`, where the subarray is `nums[j..i-1]` and its order index is `i - j`.
4. The cost of subarray `nums[j..i-1]` (which is the `(i-j)`-th subarray) is calculated using the prefix sums and the formula provided.
5. Initialize `dp[0] = 0` and `dp[i] = infinity` for `i > 0`.
6. Return `dp[n]` where `n` is the length of `nums`.
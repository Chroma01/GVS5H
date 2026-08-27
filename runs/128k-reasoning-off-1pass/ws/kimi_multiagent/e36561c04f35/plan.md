We need to find the minimum number of operations to empty the sequence. The operations are:
1. Swap adjacent elements.
2. Delete a prefix if all elements in the prefix are equal.

To solve this, we can use dynamic programming where `dp[i]` represents the minimum operations to delete the prefix of length `i`. We can transition from `dp[j]` to `dp[i]` if we can make the subarray `A[j+1...i]` consist of a single value `v` using swaps, and then delete it. The cost to make `A[j+1...i]` all `v` is the number of elements in `A[j+1...i]` that are not `v`. We can optimize this by iterating through the array and keeping track of the last occurrence of each value.
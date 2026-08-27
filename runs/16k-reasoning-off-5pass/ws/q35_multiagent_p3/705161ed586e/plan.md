1. Use dynamic programming where `dp[i][j][k]` represents the minimum cost to make the prefix `caption[0:i]` valid, ending with character `j` (0-25) having a current run length of `k` (1, 2, or 3+).
2. For each position `i`, iterate over all possible previous characters `prev_char` and run lengths `prev_len`. Calculate the cost to change `caption[i]` to the current character `curr_char`.
3. If `curr_char == prev_char`, increment the run length; if `curr_char != prev_char`, reset the run length to 1.
4. Only allow states where run length is at least 3 when transitioning to a new character (i.e., a block is complete).
5. Track the actual string by storing parent pointers or reconstructing the solution from DP states, ensuring lexicographically smallest result by iterating characters in order and breaking ties appropriately.
6. Return the lexicographically smallest valid string with minimum cost, or empty string if no solution exists.
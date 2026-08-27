We need to decide if `S` can be turned into `T` with at most `K` (≤20) edit operations (insert/delete/replace). Standard edit-distance (Levenshtein) is O(|S|·|T|), but strings can be up to 500k, so we can't use the full DP.

Key observation: if the edit distance is ≤ K and K ≤ 20, then the two strings must be very similar. We can bound how far we need to look around each position. Use a banded DP (Ukkonen's algorithm) that only computes cells where `|i - j| ≤ K`. Since K ≤ 20 and lengths can be large, the banded DP runs in O(K·min(|S|,|T|)) ≈ O(20·500k) = 10M, which is fine.

Algorithm:
- Let n = len(S), m = len(T).
- If |n - m| > K → impossible (No).
- Otherwise, run banded DP with band width K.
- The band is rows where `j ∈ [i-K, i+K]`.
- Process rows from 0 to n, tracking `prev` and `cur` arrays of size up to 2K+1.
- At the end, if `dp[n][m] ≤ K` → Yes, else No.

Edge handling: offset = K to index into the band array. We must guard against out-of-range j values.
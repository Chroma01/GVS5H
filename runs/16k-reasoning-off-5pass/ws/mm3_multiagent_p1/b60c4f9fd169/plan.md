We need to decide if `S` can be transformed into `T` using at most `K` edit operations (insert, delete, replace). Since `K ≤ 20`, we can use a bounded edit‑distance DP (Ukkonen’s algorithm) that runs in `O(|S| * |T| * K)` time, which is fine because `|S|,|T| ≤ 500000` but `K` is tiny. The DP state `dp[i][j]` is the minimum number of operations to convert the first `i` characters of `S` to the first `j` characters of `T`. Transitions:
- If `i>0`: `dp[i-1][j] + 1` (delete)
- If `j>0`: `dp[i][j-1] + 1` (insert)
- If `i>0` and `j>0`: `dp[i-1][j-1] + (S[i-1]!=T[j-1])` (replace or keep)

We only keep rows within `K` of the current column index to prune, implementing the classic “k‑band” technique. The answer is `Yes` if the final `dp[|S|][|T|] ≤ K`.

Because strings are large, we cannot store the full `O(|S|*K)` table naively for both dimensions; we store the previous column and compute the current column in place, using a deque‑like sliding window only for the “delete” transition when needed. A simple `O(|S|*K)` memory and `O(|S|*K)` time per column is acceptable: `|S| ≤ 5e5`, `K ≤ 20` → about 10 million operations per column, times 5e5 columns = 5e12 – too much. We need a faster approach.

Better: use Ukkonen’s algorithm, which computes the edit distance limited by `K` in `O((K+1) * min(|S|,|T|))` time by only exploring cells `dp[i][j]` where `|i-j| ≤ K` and `dp[i][j] ≤ K`. This works in about `O(K * min(n,m))`, i.e., at most `20 * 5e5 = 1e7` operations – easily fast enough.

Implementation steps for Ukkonen:
1. Ensure `len(S) ≤ len(T)` (swap if needed; remember original lengths for output).
2. `n = len(S)`, `m = len(T)`.
3. Maintain an array `prev[0..K+1]`, `curr[0..K+1]` storing `dp[i][j]` for the current `i` within the band.
4. For each column `j` from `0..m`:
   - Compute the valid row range `[lo, hi]` where `lo = max(0, j-K)`, `hi = min(n, j+K)`.
   - Iterate `i` over that range, applying the three transitions, but only keeping values `≤ K`.
5. If at any point `dp[n][m] ≤ K`, we can answer `Yes` early.
6. After the loop, check `prev` (which holds the last column) for `dp[n][m] ≤ K`.

Because we need only to know whether distance ≤ K, we can cap all values at `K+1`.

Edge case: if `abs(n-m) > K` → answer `No` immediately.
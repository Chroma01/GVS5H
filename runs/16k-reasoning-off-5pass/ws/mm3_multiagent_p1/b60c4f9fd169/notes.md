
## ideation
We need to decide if string `S` can be transformed into string `T` using at most `K` edit operations (insert, delete, replace), where `1 ≤ K ≤ 20` and both strings have length up to 500,000.

The classic edit‑distance DP is `O(|S|·|T|)` time and memory, which is infeasible for 500k characters. However, because `K` is tiny, we can use **Ukkonen’s algorithm** (the “k‑band” or “bounded edit distance” algorithm) that runs in `O(K·min(|S|,|T|))` time and memory.

Key points:
- We only need to know whether the edit distance is `≤ K`, not the exact distance.
- The DP only needs cells where `|i‑j| ≤ K` and `dp[i][j] ≤ K`.
- If `| |S| - |T| | > K` we can immediately answer `No`.
- Store the DP column‑by‑column using two 1‑D arrays of size `2K+1` (or slightly larger) to keep memory small.
- A simple implementation iterates each column `j` from `0` to `m`, and for each valid row `i` computes:
  - deletion: `prev[i] + 1` (where `prev` is the previous column)
  - insertion: `curr[i-1] + 1` (current column, previous row)
  - replace/match: `prev[i-1] + (S[i-1] != T[j-1])`
  - take the minimum, but cap at `K+1`.
- We need to be careful with indices because the band slides. It is easiest to always store the whole column of length `n+1` and only update the cells inside the band; values outside the band are set to a sentinel `K+1`.

Given the constraints (`K ≤ 20`, strings ≤ 500k), the algorithm will run in at most about `20 * 500k = 1e7` operations – easily fast enough.

Pitfalls:
- Swapping `S` and `T` if `|S| > |T|` so the inner loop is over the shorter string; this keeps the band width small.
- Initializing `dp[0][j] = j` (cost of inserting `j` characters), but we only need to keep the first `K+1` columns if we process row‑by‑row? Actually it's easier to process column‑by‑column and initialize `dp[0][0] = 0`, `dp[i][0] = i` (cost of deleting `i` chars), but we only store up to row `K` initially.
- When `j` increases, the valid row window `[lo, hi]` moves down by at most 1 per column; we can maintain it explicitly.
- Early termination: if the cell `(n, m)` becomes `≤ K`, we can output `Yes` immediately.

After processing all columns, check if `dp[n][m] ≤ K`.

## worker: Implement the bounded edit‑distance DP in Python a
The solution uses Ukkonen’s bounded edit‑distance algorithm.  
Key points:
- Quick reject if `| |S| - |T| | > K`.
- Swap strings so the DP iterates over the shorter string (`S`) to keep the band small.
- Maintain two 1‑D arrays (`prev`, `curr`) of size `|S|+1`.  
  For each column `j` of `T` we only compute rows `i` in the band `[max(0, j-K), min(|S|, j+K)]`.
- Values are capped at `K+1` (treated as INF) to ignore useless large distances.
- Early termination when the cell `(n,m)` becomes `≤ K`.
- Complexity: `O(K * min(|S|,|T|))` time and `O(min(|S|,|T|))` memory.  
  With `K ≤ 20` and lengths up to 500 000 this is about 10⁷ operations – easily within limits.

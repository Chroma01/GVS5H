
## ideation
- **Core difficulty**:  
  Transform the binary string into one where all `1`s form a single contiguous block using the minimum number of adjacent swaps.  
- **Key observation**:  
  Adjacent swaps preserve the relative order of the `1`s. After reordering, the *i*-th original `1` (in left‑to‑right order) must become the *i*-th `1` in the final block.  
- **Mathematical formulation**:  
  Let `pos[0 … K‑1]` be the (0‑based) indices of the `1`s (`K` = number of `1`s).  
  If the final block starts at index `l` (0‑based) and ends at `l+K‑1`, then the target index of the *i*-th `1` is `l + i`.  
  The number of swaps needed for a given `l` is  
  \[
  f(l) = \sum_{i=0}^{K-1} |\,pos[i] - (l + i)\,|.
  \]  
  The block must fit inside the string, so `l` must satisfy `0 ≤ l ≤ N‑K`.  
- **Minimising the L1 sum**:  
  The expression `|pos[i] - (l + i)|` is minimised in `l` when `l` is a median of the shifted positions  
  \[
  d_i = pos[i] - i \quad (i = 0 … K-1).
  \]  
  Hence we take the median of `d`, then clamp it to the feasible interval `[0, N‑K]`.  
- **Algorithm steps**:  
  1. Read `N` and `S`.  
  2. Collect all indices `pos` where `S[i] == '1'`.  
  3. Compute `d = [pos[i] - i for i in range(K)]`.  
  4. Sort `d` and pick `median = d[K // 2]` (0‑based median).  
  5. Clamp `start = median` to the range `[0, N‑K]`.  
  6. Answer = `sum(abs(x - start) for x in d)`.  
- **Complexity**:  
  - Time: `O(N)` to scan the string + `O(K log K)` to sort `d` (`K ≤ N ≤ 5·10⁵`, well within limits).  
  - Memory: `O(K)` for `pos` and `d`.  
- **Pitfalls**:  
  - Off‑by‑one errors (use 0‑based indices consistently).  
  - Forgetting to clamp the median, which could lie outside the feasible start range.  
  - Using 1‑based indices for the block length would misplace the targets.  
  - The answer can be as large as ~\(2.5·10^{11}\); Python’s arbitrary‑precision integers handle this safely.  
- **Edge cases**:  
  - `K = 1` → answer is `0` (any single `1` is already contiguous).  
  - All `1`s already form a contiguous segment → median yields `start` equal to the first `1` index, and the sum of absolute differences is `0`.  
  - `N = 2` with `S = "01"` → positions `[1]`, `K=1`, answer `0`.

## worker: finalize
- The relative order of the `1`s cannot change; the *i*-th `1` (in left‑to‑right order) must end up at index `l + i` where `l` is the leftmost position of the final block.
- The total number of adjacent swaps needed for a given `l` is `∑ |pos[i] - (l + i)|`.
- Setting `d_i = pos[i] - i` reduces the problem to minimizing `∑ |d_i - l|`, which is achieved when `l` is a median of the `d_i`.
- The median may lie outside the feasible interval `[0, N‑K]`, so we clamp it.
- The algorithm runs in `O(N + K log K)` time (dominant sorting) and `O(K)` memory, well within the limits (`N ≤ 5·10⁵`).

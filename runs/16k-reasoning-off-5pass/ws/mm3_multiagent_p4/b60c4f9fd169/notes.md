
## ideation
The problem asks whether the edit distance between S and T is ≤ K, where K ≤ 20. Strings are huge (≤ 5e5), so a full O(n·m) DP is impossible. The standard approach for tiny K is **A\* search** on the edit distance DAG, with a strong admissible heuristic like the number of mismatched characters (h = (|S|-i - common prefix) + (|T|-j - common suffix) or just max(missing1, missing2) or using character frequency differences). However, for up to length 5e5 and K=20, even a naive A\* might explore many states. 

A better deterministic approach: **Ukkonen's banded edit distance** (only compute DP cells where |i - j| ≤ K). Since the true distance d ≤ K, any optimal path from (0,0) to (n,m) stays within a diagonal band of width 2K+1. This gives O(K·min(n,m)) time. If the banded DP finds a distance d ≤ K, output Yes; else No. This is the standard AtCoder problem C / full version solution.

We must be careful: the banded DP works by maintaining the current column's DP values for rows i where |i - j| ≤ K. We iteratively increase j and slide a window. The algorithm must handle the case where the distance exceeds K (we can return early). For n,m up to 5e5 and K=20, the O(K·min(n,m)) ≤ 2e7 operations is fine.

Algorithm details:
- Let f(i,j) be edit distance. We only compute f(i,j) for |i - j| ≤ K.
- Initialize f(0,0) = 0, f(i,0) = i, f(0,j) = j.
- For j = 1..m:
  - Determine the range of i: max(0, j-K) to min(n, j+K).
  - For i in that range:
    - if i>0 and j>0: f(i,j) = min( f(i-1,j)+1, f(i,j-1)+1, f(i-1,j-1)+(S[i-1]!=T[j-1]) )
    - if i==0: f(0,j) = j
    - if j==0: f(i,0) = i
  - After processing column j, we only need to keep rows in a window. But the straightforward O(K) per column method: for j from 1 to m, we compute a contiguous block of f(i,j) for i in [lo, hi] where lo = max(0, j-K) and hi = min(n, j+K). But we must read f(i-1,j) which is the previously computed value in the same column? Wait, standard DP uses f(i-1,j) from same column j (left neighbor in the matrix? Actually rows increase downward, columns increase rightward. f(i-1,j) is above, f(i,j-1) is left, f(i-1,j-1) is diagonal). So we need to store the column j-1 fully, and we only need the part of column j-1 within the band. 

Standard efficient implementation: Keep a list/array of current column values. We iterate j from 1 to m. For each j, we know the valid i range. We can compute f(i,j) using f(i-1,j-1), f(i-1,j), f(i,j-1). But f(i-1,j) is from the column we are currently building? Actually, if we process i from low to high, we need the previously computed f(i-1,j) which we have just computed in the same column. So we can compute column j in order of i. This is a standard DP.

We also need to early terminate: if at any point f(i,j) > K and we can prove that the optimal distance is > K, we can stop. For banded DP, if the minimum value in the current column exceeds K + (m - j), we can break, but simpler: if we find a cell where f(i,j) > K and we cannot go down, we can prune. Actually, the standard early termination: while computing column j, if the minimum value in the column (for allowed i) is > K, then distance > K (since we still need at least m-j insertions and n-i deletions). But because K is small, we can just run the full min(n,m)*K DP and at the end check f(n,m) ≤ K. If f(n,m) > K, answer No.

Wait, careful: In Ukkonen's algorithm, the band width is 2K+1, so if we fix K, we compute DP only where |i - j| ≤ K. But this only works if the actual distance d ≤ K. If d > K, the optimal path leaves the band, so the DP restricted to the band will give a distance > K (or might be wrong because it forces a path inside the band). Actually, the standard edit distance DP restricted to the band is a lower bound on the true distance, and if d ≤ K, the true distance equals the banded DP distance. So we can safely compute the banded DP. If the result > K, we can conclude d > K. However, if the banded DP exceeds K at some cell, we can stop early.

Implementation specifics for Python:
- n, m = len(S), len(T). If abs(n - m) > K, answer is No immediately.
- Initialize prev column array for i from 0 to min(n, K). Actually, the band at j=0: i in [0, min(n, K)] (since j=0, |i-0|≤K → i≤K). For j=0, f(i,0)=i.
- For j in 1..m:
  - Determine i range: i_min = max(0, j - K), i_max = min(n, j + K).
  - Allocate a new array cur of size i_max - i_min + 1 (index 0 corresponds to i_min).
  - For i in i_min..i_max:
    - if i == 0: cur[0] = j (since f(0,j)=j)
    - else: 
      - sub = prev[i - (i_min-1) - 1]? Need careful indexing. 
      - Let's map index properly. Let prev store f values for i from i_min_prev to i_max_prev. i_min_prev = max(0, (j-1)-K) = max(0, j-K-1), i_max_prev = min(n, (j-1)+K) = min(n, j+K-1).
      - We need f(i-1, j-1): that's in prev at index (i-1) - i_min_prev.
      - f(i, j-1): in prev at index i - i_min_prev (if i in prev range).
      - f(i-1, j): this is cur at index (i-1) - i_min. We compute i in increasing order, so we have it.
    - Compute f(i,j) = min of the three, but careful: if i-1 < i_min_prev, f(i-1,j-1) is not computed, but actually i-1 ≥ i_min? Since i_min = max(0, j-K), i_min-1 = max(-1, j-K-1). If j-K-1 >= 0, then i_min_prev = j-K-1, so i-1 = j-K? If i = i_min = j-K, then i-1 = j-K-1 = i_min_prev, which is valid. If j-K-1 < 0 (i.e., j ≤ K), then i_min=0, and i-1 could be -1, which is out of bounds. In that case, f(i-1,j-1) is f(-1, j-1) = infinity.
    - Similarly for f(i, j-1): if i < i_min_prev, it's infinity.

To simplify, we can pad the prev array with infinities at the ends. But K ≤ 20, n,m up to 5e5, the arrays are small per column (at most 2K+1 = 41 elements). The overhead of Python arrays is small. We can just use a list and manually handle out-of-range as a large number (e.g., K+1 or INF). Since we only care about values up to K, we can use INF = K+1.

Simplified implementation using two arrays of length 2K+1, centered around the diagonal:
- We keep an array `cur` of size 2K+1 representing the column j. Index d corresponds to i = j + d, where d ranges from -K to K.
- For j=0, the valid d are such that i = 0 + d is between 0 and n, and |d| ≤ K. So d in [max(-j, -K), min(K, n-j)]. For j=0, d in [0, min(K, n)].
- For each j, we compute cur[d] for d in valid range. The recurrence in terms of d:
  - i = j + d.
  - f(i,j) = f(j+d, j).
  - f(i-1,j) = f(j+d-1, j) = cur_prev[d-1] (if d-1 in previous valid range).
  - f(i,j-1) = f(j+d, j-1) = cur[d] from previous column? Wait, f(i, j-1) is in the previous column at row i. In the d representation, previous column index d' satisfies i = (j-1) + d' => d' = i - (j-1) = d+1. So f(i, j-1) = prev[d+1].
  - f(i-1, j-1) = f(j+d-1, j-1) = prev[d] (since row = j+d-1, col = j-1, so d' = (j+d-1) - (j-1) = d).
- So recurrence: cur[d] = min( prev[d-1] + 1,  # delete
                           prev[d+1] + 1,  # insert (from i, j-1)
                           prev[d] + (S[i-1] != T[j-1]) )  # match/replace
  where prev is the array for column j-1.
- But careful: prev is the array for column j-1, which has its own valid d range. So we need to index prev with d-1, d, d+1, and if out of valid range, treat as INF (or a large number). Also, the valid range for cur is d_min = max(-j, -K), d_max = min(K, n-j). For prev (col j-1), d_min_prev = max(-(j-1), -K), d_max_prev = min(K, n-(j-1)).

We can implement this with a fixed-size array of size 2K+1 (indices 0..2K corresponding to d = -K..K). For each j, we compute cur and then swap cur and prev.

This is very efficient: O(m * (2K+1)) time, O(K) space.

Edge cases:
- n or m can be 0? Problem says length ≥ 1.
- If abs(n - m) > K, immediate No.
- After full DP, if f(n,m) ≤ K, Yes else No. f(n,m) is at d = n-m. We need to ensure that d is within [-K, K] in the final array. Since we already checked abs(n-m) ≤ K, it will be.

Early termination: As we compute, if all cur[d] > K, we can stop and return No. Also, if j reaches m but we haven't reached d = n-m? Actually, we need to compute all columns. But we can stop if the minimum of cur is > K + (m - j) because we need at least that many more operations? But given the tiny K, we can just run full. The total operations: m * (2K+1) ≤ 5e5 * 41 = 2e7, which is fine in Python if optimized (avoid bounds checks inside the inner loop, maybe use local variables).

However, 2e7 in Python might be a bit slow (maybe 2-3 seconds). We can optimize by:
- Precomputing the mismatch cost: a list of booleans or using ord values.
- Using `while` loops with local variables.
- Actually, we only need to compute the d range for each j. The number of valid d is at most 2K+1, but often less near the ends. We can compute the slice.

Let's write the code carefully.

## worker: Implement the banded edit distance (Ukkonen's algo
The solution uses Ukkonen's banded edit distance algorithm. Since the true edit distance \(d \le K \le 20\), any optimal path lies within the diagonal band \(|i - j| \le K\). The DP is restricted to this band, giving \(O(m \cdot (2K+1))\) time and \(O(K)\) space. We maintain two fixed-size arrays of length \(2K+1\) representing the current and previous columns, indexed by diagonal offset \(d = i - j\). Out-of-band cells are treated as \(K+1\), which is effectively infinity for our purpose. We also add an early termination if the minimum value in a column exceeds \(K\). An immediate check \(|n-m| > K\) handles trivial cases.

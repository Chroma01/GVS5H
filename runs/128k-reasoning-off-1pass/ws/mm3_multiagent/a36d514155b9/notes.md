
## ideation
We need to compute, over all subsets of size k from an m×n grid, the sum of pairwise Manhattan distances. Because Manhattan distance separates into row distance + column distance, the total sum = (sum over row pairs) + (sum over column pairs). By linearity of expectation (or double counting), each pair of cells contributes to many subsets.

Number of cells N = m·n ≤ 1e5, k ≤ N. For a fixed unordered pair of cells, the number of subsets of size k containing that pair is C(N-2, k-2). So:

Total = C(N-2, k-2) · Σ_{unordered pairs} ManhattanDist(pair)

Σ_{pairs} ManhattanDist = Σ_{pairs} |r_i - r_j| + Σ_{pairs} |c_i - c_j|

Each row has exactly n cells, each column has exactly m cells.

**Row contribution**: Σ_{i<j} n·n·(j - i) = n² Σ_{i<j} (j - i). This is O(m²) naively, but we can compute it in O(m) using a running prefix sum:

For row index i (0-indexed) with value v = n:
   contribution from pairs (i, j>i) is v * (v·i - prefix) summed over i
   = v·v·i - v·prefix; add to total. Maintain `prefix` = sum of v's seen so far (i.e., n·i).

**Column contribution** is symmetric with m instead of n.

So:
- row_sum = n² · (sum over 1 ≤ i < j ≤ m of (j-i))
- col_sum = m² · (sum over 1 ≤ i < j ≤ n of (j-i))

Closed form for Σ_{0 ≤ i < j ≤ M-1} (j - i) = M(M² - 1)/6. Verify: it's the sum of all pairwise distances in a 1D line of M points.

Therefore:
row_sum = n² · m(m² - 1)/6
col_sum = m² · n(n² - 1)/6

Total pair sum = row_sum + col_sum.
Answer = C(N-2, k-2) · (row_sum + col_sum) mod (1e9+7).

Precompute factorials up to N = 1e5 and inverse factorials mod M (M is prime). Compute C(n,r) as fact[n]·invfact[r]·invfact[n-r] mod M.

We must divide by 6 mod M, i.e., multiply by inv(6) = inv(6) mod M (166666668).

Edge cases: None special, but ensure modular division by 6 (or equivalently precompute inv6). All arithmetic mod 1e9+7.

## worker: Re-evaluate and correct the formula for sum of Man
**Derivation:**

For an m×n grid, the total sum of Manhattan distances over all **unordered pairs** of cells is:
$$\sum_{\text{pairs}} (|r_i - r_j| + |c_i - c_j|) = \text{row\_sum} + \text{col\_sum}$$

**Row part:** For two distinct rows i and j, there are n cells in each, giving n² pairs with row distance |i-j|. So:
$$\text{row\_sum} = n^2 \sum_{0 \le i < j \le m-1} (j - i) = n^2 \cdot \frac{m(m^2-1)}{6}$$

**Column part:** By symmetry:
$$\text{col\_sum} = m^2 \cdot \frac{n(n^2-1)}{6}$$

**Verification with examples:**
- m=2, n=2: row_sum = 4·(2·3/6) = 4, col_sum = 4·(2·3/6) = 4, total = 8 ✓
- m=1, n=4: row_sum = 0, col_sum = 1·(4·15/6) = 10, total = 10 ✓

**Total over all arrangements:** Each unordered pair appears in C(N-2, k-2) subsets of size k, so:
$$\text{answer} = C(N-2, k-2) \cdot (\text{row\_sum} + \text{col\_sum}) \bmod (10^9+7)$$

For example 1: C(2,0)=1, total=8·1=8 ✓
For example 2: C(2,1)=2, total=10·2=20 ✓

The factor k(k-1) is **not** needed because we already summed over all unordered pairs (each pair counted once), and C(N-2, k-2) directly counts how many k-subsets contain a given pair.

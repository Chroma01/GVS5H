For every arrangement we have a set of `k` distinct cells.  
For a fixed unordered pair of cells `{u,v}` the distance `d(u,v)` contributes to the total sum once for every arrangement that contains both cells.  
The number of such arrangements is the number of ways to choose the remaining `k‑2` cells from the other `N‑2` cells, i.e. `C(N‑2, k‑2)`, where `N = m·n`.  

Hence the required sum is  

\[
S = \binom{N-2}{k-2}\; \times\; T,
\]

where `T` is the sum of Manhattan distances over **all** unordered cell pairs of the `m × n` grid.

`T` can be split into row and column contributions.  
For rows: a pair of rows `i < j` contributes `j‑i` for every pair of columns, i.e. `n²` times.  
Thus the row part is `n² * Σ_{i<j} (j‑i)`.  

\[
\sum_{0\le i<j<m}(j-i) = \frac{m(m-1)(m+1)}{6}.
\]

The column part is symmetric, giving  

\[
T = \frac{n^{2}\,m(m-1)(m+1) + m^{2}\,n(n-1)(n+1)}{6}.
\]

All values fit easily in Python’s integers, and division by `6` is exact because the numerator is a multiple of `6`.  
Finally we compute `C(N‑2, k‑2)` modulo `10⁹+7` using pre‑computed factorials and modular inverses (MOD is prime).  

The algorithm runs in `O(N)` time for factorial pre‑computation and `O(1)` for the final calculation, well within the limits (`N ≤ 10⁵`).
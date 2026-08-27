
## ideation
The core difficulty is avoiding explicit consideration of all pairs, since the graph can have quadratic many edges. The threshold gives the crucial restriction: if either value exceeds the threshold, its LCM with every positive value also exceeds the threshold, so that vertex is isolated. For values at most the threshold, connectivity can be represented through shared multiples no greater than the threshold. A careful implementation must also handle duplicate-related indexing assumptions, although the stated constraints guarantee distinct values, and must avoid accidentally merging values merely because they divide a common multiple above the threshold.

The proposed multiples-based DSU idea is valid: for every present value `x`, scan its multiples up to the threshold and connect `x` to another present divisor associated with each multiple. Every genuine edge is captured at its LCM, while unions at other multiples only establish valid paths because the multiple itself is within the threshold. The component count can start at `n`, with values above the threshold remaining singleton components.

## worker: Implement the multiples-representative DSU solutio
For every value `x <= threshold`, all multiples of `x` up to `threshold` are scanned. If two values divide the same multiple `m <= threshold`, their LCM also divides `m`, so their LCM is at most the threshold and they belong to the same connected component.

At each multiple, the current value is unioned with one previously seen divisor. Any genuine edge `(a, b)` is captured when processing the multiple `lcm(a, b)`, ensuring all adjacent vertices become connected in the DSU. Values greater than the threshold are isolated because every LCM involving them is greater than the threshold.

The total scanning cost is:

\[
\sum_{x \le threshold} \frac{threshold}{x} = O(threshold \log threshold)
\]

with near-constant amortized DSU operations.

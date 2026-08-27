
## ideation
The core difficulty is answering sums of absolute differences over two arbitrary prefixes without explicitly processing all \(X_kY_k\) pairs. For a value \(a\), its contribution against a prefix of \(B\) can be obtained from the count and sum of \(B\)-values below and above \(a\). However, both the queried prefix length and the queried values vary, so the data structure must support prefix-restricted order-statistics and sum queries efficiently. The target complexity should be around \(O((N+K)\log N)\) or \(O((N+K)\log^2 N)\), with 64-bit answers.

## worker: Implement a sqrt-decomposition solution: partition
The A-prefix is split into blocks of size 300. For each block boundary, all queries with that boundary share the contribution of the complete boundary prefix. The sorted boundary prefix is maintained by merging in the next sorted block, and its interaction with all B-values is computed by a linear sweep in sorted B order.

The remaining at most 300 A-elements of each query are handled individually. A persistent segment tree over B-prefixes provides the count and sum of B-values smaller than a given A-value, allowing each absolute-difference sum in \(O(\log N)\).

Overall complexity is approximately \(O(N^2/S + K S \log N + N\log N)\), with \(S=300\), and all answers use 64-bit integer arithmetic.

## worker: Fix the `less_than` persistent-segment-tree query:
Fixed `less_than` by adding the final leaf’s count and sum when `lo < pos`. This correctly includes all compressed values strictly smaller than the queried position, including the leaf where the descent terminates. The boundary-zero case remains handled by the initial zero contribution table.

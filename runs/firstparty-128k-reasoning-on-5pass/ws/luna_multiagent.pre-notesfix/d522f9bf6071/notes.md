
## ideation
The core difficulty is combining weighted interval scheduling with a strict lexicographic tie-break on the original interval indices. Intervals must be considered compatible only when the next interval starts strictly after the previous interval ends, so equal boundaries are incompatible. The scheduling order used internally will generally differ from original-index order, while the returned list must be sorted by original indices before lexicographic comparison. Since at most four intervals may be chosen, storing or comparing short index lists is feasible, but tie handling must be applied consistently at every dynamic-programming state. The empty choice and “at most four” requirement also need explicit consideration.

## worker: Implement and test a Fenwick-tree weighted interva
The intervals are processed in nondecreasing order of right endpoint. For each exact selection count, a Fenwick tree stores the best state for every prefix of right endpoints.

For an interval starting at `l`, querying only Fenwick positions whose right endpoint is strictly less than `l` enforces the non-overlap condition, including the rule that shared boundaries overlap.

States are compared by:
1. larger total weight;
2. lexicographically smaller sorted tuple of original indices.

Counts are processed in descending order, so the current interval cannot be reused during the same iteration. The total complexity is `O(n log n)` with a constant factor of at most four, and memory usage is `O(n)`.

## worker: Run the provided examples and randomized brute-for
The Fenwick trees store the best state for each exact selection count over processed intervals. Querying with `bisect_left(ends, l)` includes only endpoints strictly less than `l`, so intervals sharing a boundary are correctly treated as overlapping.

States are compared first by maximum weight and then by the lexicographically smallest sorted tuple of original indices. Processing counts in descending order prevents selecting the same interval more than once.

The approach runs in `O(n log n)` time with a constant factor of four and uses `O(n)` memory. It handles fewer than four selected intervals by comparing the best states for all counts from zero through four.

## worker: Run the implementation on both provided examples a
The implementation was validated against both provided examples and exhaustive/randomized brute-force cases on small interval sets.

The brute-force comparison covered:
- Endpoint-sharing intervals, which must be treated as overlapping.
- Equal-score choices requiring lexicographically smallest original indices.
- Solutions using fewer than four intervals.
- Empty-choice handling.
- Duplicate boundaries and arbitrary original index order.

For an interval starting at `left`, `bisect_left(ends, left)` queries only previously selected intervals whose right endpoint is strictly less than `left`, enforcing the required strict non-overlap rule.

Each Fenwick tree stores the best state for an exact selection count. States are compared by maximum weight first and lexicographically smallest sorted index tuple second. The complexity is `O(n log n)` with a constant factor of four, and memory usage is `O(n)`.

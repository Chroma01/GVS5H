
## ideation
The core difficulty is that deleting a value affects every occurrence of that value simultaneously, while the desired subarray is contiguous only after those occurrences are removed. For a fixed deleted value, the problem is an ordinary maximum-subarray computation on a filtered sequence, but evaluating every distinct value independently would be quadratic.

A correct implementation must also distinguish deleting an element from replacing it with zero. Deleted elements disappear and therefore can concatenate neighboring portions. Treating them as zero can incorrectly produce a zero-valued subarray when every remaining element is negative. The empty filtered array must likewise be rejected.

## worker: Implement the repeated point-deletion segment tree
The segment tree stores the standard concatenation monoid for a sequence:

- `total`: sum of the sequence
- `pref`: maximum non-empty prefix sum
- `suff`: maximum non-empty suffix sum
- `best`: maximum non-empty subarray sum

A deleted position is represented by the true empty-sequence identity:
`(0, -inf, -inf, -inf)`. Thus deleted elements disappear and neighboring values concatenate correctly, while empty subarrays are never selected.

For every distinct value, all of its positions are temporarily replaced by the identity, the root's `best` is queried, and the positions are restored. Each position is updated at most twice, giving `O(n log n)` time and `O(n)` memory.

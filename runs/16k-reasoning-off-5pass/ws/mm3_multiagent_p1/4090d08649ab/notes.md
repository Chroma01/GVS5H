
## ideation
The problem asks for the sum over all subarrays of the minimum number of operations to erase all numbers, where each operation can erase all occurrences of a contiguous integer interval that appears in the subarray. This is equivalent to the number of connected components of the set of distinct values in the subarray on the integer line. For a subarray, if we let `distinct` be the number of distinct values and `adj` be the number of adjacent integer pairs `(v, v+1)` both present, then the number of components is `distinct - adj`. Thus the answer is `sum_distinct - sum_adjacent`, where `sum_distinct` is the total number of distinct occurrences over all subarrays, and `sum_adjacent` is the total number of subarrays containing at least one occurrence of both `v` and `v+1` for each `v`.

We can compute `sum_distinct` by, for each value `v`, counting subarrays containing `v`. Using the positions of `v`, the number of subarrays missing `v` is the sum over gaps of `len*(len+1)//2`. Then `cnt_v = total - miss_v`, and `sum_distinct = sum_v cnt_v`.

For `sum_adjacent`, for each `v` from 1 to N-1, we need the number of subarrays containing both `v` and `v+1`. By inclusion-exclusion, this is `total - miss_v - miss_{v+1} + miss_both`, where `miss_both` is the number of subarrays containing neither `v` nor `v+1`. To compute `miss_both`, we merge the sorted position lists of `v` and `v+1` and sum `len*(len+1)//2` over the gaps between merged positions. Since each position belongs to exactly two lists (for `v = A_i-1` and `v = A_i`), the total work across all merges is O(N).

The constraints allow O(N) time and memory.

## worker: Implement the solution in Python: read N and A, bu
We derived that for a subarray the minimum number of operations equals the number of connected components of its distinct values on the integer line. This equals `distinct - adjacent`, where `distinct` is the number of distinct values and `adjacent` counts pairs of consecutive integers both present. Summing over all subarrays gives `sum_distinct - sum_adjacent`.

- `sum_distinct` is computed by, for each value `v`, counting subarrays containing `v` via `total - miss_v`, where `miss_v` is the number of subarrays missing `v` (obtained from gaps between positions of `v`).
- `sum_adjacent` requires, for each `v`, the number of subarrays containing both `v` and `v+1`. By inclusion–exclusion this is `total - miss_v - miss_{v+1} + miss_both`, where `miss_both` is the number of subarrays containing neither `v` nor `v+1`. `miss_both` is computed by merging the two sorted position lists and summing over gaps.

Each position appears in at most two pairs, so the total merging work is O(N). All other steps are linear, yielding an O(N) solution.

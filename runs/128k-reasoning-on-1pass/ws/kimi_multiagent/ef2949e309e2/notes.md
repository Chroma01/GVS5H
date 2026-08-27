
## ideation
Core difficulty is not enumerating 5-subsequences, but counting by the fixed middle index `p`: every valid subsequence is uniquely partitioned by its third element, so we need exactly 2 choices from left of `p` and 2 from right of `p`. For middle value `v = nums[p]`, if `a`/`b` are the numbers of chosen left/right elements equal to `v`, then middle frequency is `1+a+b`. Cases split cleanly: `a+b >= 2` is always valid because at most two non-`v` elements remain; `a+b = 0` is never valid; the only delicate case is `a+b = 1`, where the three non-`v` picks must be pairwise distinct, including cross-side collisions. Values are large, so compress or use hash maps. With `n <= 1000`, an `O(n^2)` solution is acceptable, so correctness should be prioritized over a fragile `O(n)` sweep. Main pitfalls: treating subsequences as subarrays, overcounting arrangements within left/right pairs, missing tie cases when middle frequency is 2, double-counting across different middles, and inclusion-exclusion errors when one non-`v` is from the left and two are from the right or vice versa.

## worker: Implement a minimal brute-force oracle and a first
- Fixed the middle index `i`; every 5-subsequence is counted once by choosing 2 indices left of `i` and 2 right of `i`.
- For middle value `v`, classified left/right pairs by how many chosen side elements equal `v`: `L0/L1/L2` and `R0/R1/R2`.
- Cases with at least two side `v`s are always valid. Cases with zero side `v`s are invalid. Exactly one side `v` requires the three non-`v` side values to be pairwise distinct.
- Maintained side `Counter`s plus sums of squared frequencies to compute distinct-valued non-`v` pairs and exclusions in O(1) per distinct opposite value.
- Included a combination brute-force oracle and randomized small-array cross-checks under `if __name__ == "__main__":`; examples and random tests pass.

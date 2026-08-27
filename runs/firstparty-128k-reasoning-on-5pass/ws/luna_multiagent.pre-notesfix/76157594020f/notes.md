
## ideation
The core difficulty is checking whether a target maximum run length can be achieved with at most `numOps` flips. A flip changes both the character and potentially the boundaries of neighboring runs, so greedy choices can fail. The natural monotonicity is that if a maximum run length `L` is feasible, every larger limit is feasible, enabling binary search over `L`. Any feasibility method must account for the last chosen character and the length of its current run, while minimizing flips.

## worker: Implement and test a binary-search feasibility hel
The feasibility check uses dynamic programming on the ending bit and current run length. Keeping the same bit extends a run, while changing the bit starts a run of length one. The minimum flip count for each state is maintained, and feasibility is monotonic in the candidate maximum run length, allowing binary search.

## worker: Run the provided examples and edge cases against t
The feasibility DP correctly tracks the ending bit and the length of the final run. For each character, it either extends the existing run or starts a new run with the opposite bit, adding one flip whenever the chosen bit differs from the original character.

Feasibility is monotonic: if a maximum run length `L` is achievable, every larger limit is also achievable. Therefore, binary search returns the smallest feasible limit.

The implementation produces:
- `minLength("000001", 1) == 2`
- `minLength("0000", 2) == 1`
- `minLength("0101", 0) == 1`

It also handles edge cases such as a one-character string, zero operations, and strings already alternating.

Complexity is `O(n^2 log n)` in the worst case and `O(n)` auxiliary space for each feasibility check.

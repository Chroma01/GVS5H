
## ideation
The core difficulty is counting the number of valid completions after fixing a prefix, so lexicographic blocks can be skipped without generating permutations. Once the parity of the last chosen value is known, every subsequent position must use the opposite parity. Therefore, the parity pattern is forced, and a completion count is the product of factorials of the remaining odd and even values, provided their counts exactly match the required future parity slots.

The initial position is special because either parity may be possible, subject to the total counts of odd and even numbers. For odd `n`, there is one more odd number, so every valid permutation must start with an odd value. For even `n`, either starting parity is possible. The total count should be checked before construction.

Since `k` can be as large as `10^15`, counts only need to be computed up to a cap slightly above `k`; capped factorials and capped products prevent oversized arithmetic while preserving all comparisons. Candidate values must be considered in increasing numerical order, and each candidate’s completion count determines whether to skip its entire lexicographic block or select it. If all candidates are exhausted before locating the requested block, return an empty list.

Potential pitfalls include using the wrong completion count when no prefix has yet been selected, failing to enforce the required parity of the next position, and overlooking that a candidate is feasible only when the remaining odd/even counts match the forced parity slots. The values themselves are distinct, so after parity feasibility is established, the remaining odd and even values can be arranged independently.

## worker: Implement and validate the greedy lexicographic co
The parity of every position after the first is forced by the previously chosen value. For a candidate value, the remaining odd and even counts must exactly match the required alternating parity slots; otherwise its lexicographic block is empty.

When feasible, the remaining odd values and even values can be arranged independently, giving `remaining_odd! * remaining_even!` completions. Factorials and products are capped at `k`, since larger values are indistinguishable for all needed comparisons.

The construction scans unused values in increasing order, skips complete lexicographic blocks when `k` exceeds their size, and selects the candidate containing the requested permutation. The total count is checked first to handle out-of-range `k`.

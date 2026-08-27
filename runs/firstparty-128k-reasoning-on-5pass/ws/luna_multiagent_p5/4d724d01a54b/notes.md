- **Optimal swap order:** Among all currently available adjacent inversions, swapping the leftmost one is optimal. Any sorting sequence can be represented by a reduced word in adjacent transpositions. Commuting independent swaps does not affect cost. The only relevant braid replacement is `i+1, i, i+1` to `i, i+1, i`; both perform the same permutation, while their costs change from `3i+2` to `3i+1`, so the latter is never worse. Repeatedly applying these exchanges yields the lexicographically smallest reduced sequence, which always chooses the leftmost available inversion.
- **Insertion-sort interpretation:** Choosing the leftmost inversion is exactly insertion sort. When processing the original element `P_j`, the prefix `P_1...P_{j-1}` is already sorted. If the current value is greater than `k` prefix elements, it moves left across exactly those `k` elements.
- **Exact cost:** The element starts at position `j` and crosses boundaries `j-1, j-2, ..., j-k`. Their sum is
  `k * ((j-k) + (j-1)) / 2 = k * (2j-k-1) / 2`.
- **Fenwick computation:** After processing the first `j-1` values, the number of prior values greater than `P_j` is
  `k = (j-1) - count(values <= P_j)`. A Fenwick tree over values supports this count in `O(log N)`.
- **Complexity:** The algorithm uses `O(N log N)` time and `O(N)` memory. Python integers safely handle the potentially cubic-sized total cost.
- **Edge cases:** Already sorted input has `k=0` for every element and answer `0`. The formula uses current positions and automatically handles all inversion patterns.

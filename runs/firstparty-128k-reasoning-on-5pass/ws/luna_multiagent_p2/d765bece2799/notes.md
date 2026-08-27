- **Contribution model:** For each index, count subarrays in which that element is the uniquely assigned representative of the maximum or minimum. If there are `L` valid left extensions and `R` valid right extensions, choose positive lengths `a <= L` and `b <= R`; the subarray length is `a + b - 1`, which must be at most `k`.

- **Counting formula:** Let `P(t)` be the number of positive pairs `(a, b)` with `a + b <= t`. Then `P(t) = t(t-1)/2` for `t > 1`, otherwise zero. Without extension limits, the count is `P(k+1)`. Inclusion-exclusion gives:
  `P(k+1) - P(k+1-L) - P(k+1-R) + P(k+1-L-R)`.

- **Maximum boundaries:** Previous boundary is the nearest strictly greater element, obtained by popping values `<= current`. Next boundary is the nearest greater-or-equal element, obtained by popping values `< current`.

- **Minimum boundaries:** Previous boundary is the nearest strictly smaller element, obtained by popping values `>= current`. Next boundary is the nearest smaller-or-equal element, obtained by popping values `> current`.

- **Duplicate handling:** The asymmetric strictness assigns each subarray to exactly one equal extremum. For maxima, equal values are represented by the rightmost occurrence; minima use the same tie convention. Thus no subarray is counted twice.

- **Complexity:** Each monotonic stack processes every index at most once per operation. Time complexity is `O(n)` and space complexity is `O(n)`. Python integers safely provide the required 64-bit-or-more arithmetic.

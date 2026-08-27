
## ideation
The core difficulty is updating the inversion count when every residue is shifted cyclically, without recomputing inversions for all \(M\) shifts. Between consecutive shifts, the relative order of all values stays unchanged except for elements currently equal to \(M-1\), which wrap to \(0\). All such elements must be handled as a group, because pairs consisting of two wrapping elements do not change their mutual inversion status.

A natural baseline is to compute the inversion count for \(k=0\) with a Fenwick tree over values. For each subsequent shift, identify the original residue class whose elements currently equal \(M-1\), and calculate the total change caused by moving that class from the maximum residue to zero. The change for each position depends on the number of non-wrapping elements to its left and right. Grouping positions by original residue allows these quantities to be aggregated efficiently, using position sums and ranks within each group. This gives linear preprocessing after the initial inversion computation and then constant-time transitions between answers.

Important pitfalls include:
- Equal values never form inversions, including pairs of elements that wrap simultaneously.
- The wrapping group for shift \(k\) consists of original values congruent to \(M-1-k\) modulo \(M\).
- All elements in the wrapping group should conceptually be moved together, or their mutual pairs may be counted incorrectly.
- Use sufficiently wide integer arithmetic because the inversion count can be \(N(N-1)/2\).
- The case \(M=1\) should naturally produce zero for every shift.

## worker: Derive and verify the exact aggregate delta for sh
For a shift from `k` to `k+1`, only elements whose current value is `M-1` wrap to `0`. These are exactly the elements of one original residue class `x`.

For an element of this class at position `i`, pairs with another element of the same class remain non-inversions because both values change together. Every element of a different class changes the pair status:

- each non-class element to the left creates one inversion;
- each non-class element to the right removes one inversion.

If the class has `c` elements and their zero-based position sum is `s`, the total change is:

\[
\Delta_x = 2s - (N-1)c.
\]

The initial inversion count is computed with a Fenwick tree in `O(N log M)`. Class counts and position sums are collected in `O(N)`, and all `M` answers are generated in `O(M)`.

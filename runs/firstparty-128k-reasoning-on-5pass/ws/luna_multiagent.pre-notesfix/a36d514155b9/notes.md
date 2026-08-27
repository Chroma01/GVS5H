
## ideation
The core difficulty is aggregating Manhattan distances over all subsets of \(k\) occupied cells without enumerating either arrangements or cell pairs. Linearity of summation reduces the problem to determining how often each unordered pair of cells occurs, then efficiently summing distances over the entire grid. The large dimensions require an \(O(1)\) or \(O(m+n)\) computation with modular arithmetic, including careful handling of factorials, inverses, and the case \(k=mn\).

## worker: Derive and implement the complete \(O(mn)\)-time s
For every unordered pair of cells, the pair occurs in exactly \(\binom{mn-2}{k-2}\) arrangements. Thus, by linearity, compute the sum of Manhattan distances over all cell pairs and multiply by this common factor.

The total horizontal contribution is:
\[
m^2 \sum_{0 \le i < j < n}(j-i),
\]
and the total vertical contribution is:
\[
n^2 \sum_{0 \le i < j < m}(j-i).
\]
Using
\[
\sum_{0 \le i < j < q}(j-i)=\frac{q(q-1)(q+1)}{6},
\]
the result is computed in \(O(mn)\) time and \(O(mn)\) memory for factorials.

## worker: Run the provided examples and edge cases (`k=2`, `
For every unordered pair of cells, the number of arrangements containing both cells is `C(m*n-2, k-2)`. The sum of Manhattan distances over all cell pairs is:

- `m² * n(n-1)(n+1)/6` for horizontal distances
- `n² * m(m-1)(m+1)/6` for vertical distances

The implementation multiplies this total by the common number of arrangements containing each pair. It handles `k = 2`, `k = m*n`, and one-dimensional grids. It produces `8` for `(2, 2, 2)` and `20` for `(1, 4, 3)`.

- **Core counting:** Every arrangement is a size-\(k\) subset of the \(mn\) grid cells. Any fixed unordered pair of cells is present in exactly \(\binom{mn-2}{k-2}\) arrangements.
- **Distance summation:** By linearity, multiply the total Manhattan distance over all unordered grid-cell pairs by \(\binom{mn-2}{k-2}\).
- **Geometric formula:** The sum of distances over unordered pairs of positions on a line of length \(L\) is \(L(L^2-1)/6\). Therefore, row-distance contribution is \(n^2m(m^2-1)/6\), and column-distance contribution is \(m^2n(n^2-1)/6\).
- **Final formula:** \[
  \left(\frac{n^2m(m^2-1)+m^2n(n^2-1)}{6}\right)\binom{mn-2}{k-2}\pmod{10^9+7}.
  \]
- **Validation run:** All sample tests pass: `(m,n,k) = (2,2,2)` returns `8`; `(1,4,3)` returns `20`.
- **Additional validation run:** All listed small and boundary cases pass: `(1,2,2) -> 1`; `(1,4,2) -> 10`; `(1,4,4) -> 10`; `(2,3,2) -> 25`; `(2,3,6) -> 25`.
- **Complexity:** Factorial precomputation takes \(O(mn)\) time and memory; remaining calculations are \(O(1)\). Since \(mn \le 10^5\), this fits comfortably.

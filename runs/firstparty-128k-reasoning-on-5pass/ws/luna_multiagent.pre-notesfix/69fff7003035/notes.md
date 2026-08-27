
## ideation
The core difficulty is that each element’s contribution depends on the total number of decimal digits in all elements placed after it, not merely on its position. For a fixed value \(i\), choosing the set of elements after it determines the power of 10, while the remaining elements can be arranged before and after \(i\) in factorially many ways. The useful symmetry is that this count depends only on the digit lengths of the chosen elements, and every integer with the same digit length has the same positional coefficient.

Since \(N \le 2\times 10^5\), directly enumerating subsets or permutations is impossible. There are only six possible digit lengths, so the state can be compressed by digit-length groups. All calculations involving factorials, powers of 10, subset counts, and sums of values should be performed modulo 998244353.

## worker: Derive the complete contribution formula and an ef
For a fixed element \(i\), choose the subset of elements appearing after it. If the subset has size \(k\), its arrangements contribute \(k!(N-1-k)!\), and its total digit length determines the power of \(10\).

Numbers with equal digit length are interchangeable for this positional factor. The generating polynomial is
\[
F(y)=\prod_{x=1}^N (1+10^{d(x)}y).
\]
For an element of digit length \(d\), removing one factor \((1+10^d y)\) gives the subset polynomial for elements after that element.

The coefficients of \(F\) are computed in \(O(ND)\), where \(D\le 6\), using
\[
Q(y)F'(y)=R(y)F(y),
\]
with
\[
Q(y)=\prod_d(1+10^d y),\qquad
R(y)=\sum_d c_d10^d\prod_{e\ne d}(1+10^e y).
\]
Each excluded-group polynomial is then obtained by linear division in \(O(N)\). Overall complexity is \(O(ND)\), with \(O(N)\) memory.


## ideation
The core difficulty is proving the correct shape of an optimal pairing and then answering many interval queries without examining every mochi in each interval. For a fixed interval and a fixed number \(K\), an exchange argument shows that it is sufficient to use the \(K\) smallest mochi as tops and the \(K\) largest as bottoms, pairing them in sorted order. The feasibility test therefore consists of \(K\) inequalities, not an arbitrary matching search.

Define, for each position \(x\), the first position \(p_x\) whose mochi is at least twice \(A_x\). Equivalently, \(p_x\) can be found by lower bound on \(2A_x\). If \(C_x=p_x-x\), then \(K\) pairs in \([L,R]\) are feasible exactly when \(K\) does not exceed half the interval length and every position \(x\) from \(L\) through \(L+K-1\) satisfies \(C_x\le R-L+1-K\). The values \(C_x\) are not necessarily monotone, so checking only the last position is unsafe.

Feasibility is monotone in \(K\): if \(K\) pairs can be formed, then any smaller number can also be formed. Thus a binary search over \(K\), combined with a range-maximum query for \(C_L,\ldots,C_{L+K-1}\), is a natural solution. A sparse table gives constant-time range maxima after linearithmic preprocessing, leading to roughly \(O((N+Q)\log N)\) time. A segment tree also works but makes each feasibility check logarithmic.

Important pitfalls are:
- Use the exact condition \(2a\le b\), avoiding floating-point division.
- The selected tops and bottoms must be disjoint, so always enforce \(K\le\lfloor (R-L+1)/2\rfloor\).
- Duplicate sizes are allowed and should be handled by lower bound.
- The first valid bottom position may lie outside the array; use a sentinel larger than \(N\).
- The range-max condition must cover all \(K\) candidate tops; relying only on an endpoint comparison is incorrect because \(p_x-x\) need not be monotone.

## worker: Derive and verify the greedy feasibility character
For a query interval of length \(m\), if \(K\) pairs are possible, it is sufficient to use the \(K\) smallest mochi as tops and the \(K\) largest as bottoms. Pairing them in sorted order is optimal.

For each position \(i\), `c[i] = bisect_left(A, 2*A[i]) - i` is the minimum distance from that mochi to a valid bottom. Thus \(K\) pairs are feasible exactly when

\[
\max(c[L],\ldots,c[L+K-1]) \le m-K.
\]

The predicate is monotone in \(K\), so binary search finds the maximum value. A sparse table answers each range maximum in \(O(1)\), giving total complexity \(O(N\log N + Q\log N)\) and \(O(N\log N)\) memory.

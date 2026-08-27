- **Structural model:** Every removal sequence corresponds to a noncrossing matching of the indices. Each removed adjacent pair becomes an edge; the reverse order of removals shows that every noncrossing matching is realizable. For odd \(N\), exactly one index remains unmatched.

- **Uncrossing principle:** For four positions \(i<j<k<l\), consider crossing edges \((i,k)\) and \((j,l)\). Among the three pairings of these four endpoints, the crossing pairing is never strictly better than both noncrossing pairings:
  \[
  |A_i-A_k|+|A_j-A_l|
  \le \max\bigl(
  |A_i-A_j|+|A_k-A_l|,
  |A_i-A_l|+|A_j-A_k|
  \bigr).
  \]
  This follows by sorting the four numerical values and comparing the three possible pair-sum weights. Therefore crossing edges can be repeatedly uncrossed without decreasing the total score. Hence the optimal noncrossing matching has the same value as the unrestricted maximum-weight matching.

- **Unrestricted matching:** After sorting values \(b_1\le\cdots\le b_N\), an even-size maximum matching pairs the lower half with the upper half, giving
  \[
  \sum_{i=N/2+1}^{N} b_i-\sum_{i=1}^{N/2}b_i.
  \]
  This is optimal by the exchange argument that pairing larger values with smaller values maximizes the sum of absolute differences.

- **Odd size:** One value remains unmatched. The optimal choice is the median \(b_{(N+1)/2}\): removing anything below it reduces the lower-half contribution less favorably, while removing anything above it reduces the upper-half contribution. Thus pair the smallest \(N//2\) values with the largest \(N//2\) values and leave the median unused.

- **Complexity:** Sorting costs \(O(N\log N)\), and the final sums cost \(O(N)\). Python integers safely handle the answer range.

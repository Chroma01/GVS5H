
## ideation
The operation on indices i..i+3 (1-indexed) reflects the two middle pieces across the midpoint of the outer two. If outer positions are a and d (with a < d), and inner positions are b and c (a < b < c < d), then after the operation the inner pieces become a+d-b and a+d-c. Note:
- The sum of the four pieces is preserved: a + (a+d-b) + (a+d-c) + d = 2(a+d).
- The two middle pieces swap their order (since b < c implies a+d-b > a+d-c).

Thus the operation is essentially a swap of the two adjacent middle pieces. By composing operations, we can swap any adjacent pair (i, i+1) for i = 1, 2, ..., N-2, because pair (i, i+1) can be made the middle two of a 4-tuple (using i-1 and i+2 as the outer pieces). The only adjacent pair we cannot swap is (N-1, N), since there is no piece at position N+1 to serve as the right outer piece.

Therefore, the last piece X_N stays fixed at the rightmost position, while the first N-1 pieces can be arbitrarily permuted. To minimize the total sum, we sort the first N-1 pieces in ascending order and keep X_N at the end.

## worker: finalize
The operation on indices i, i+1, i+2, i+3 reflects the two middle pieces across the midpoint of the outer two. This preserves the sum of the four positions and effectively swaps the two middle pieces. By chaining such operations, any adjacent pair among the first N-1 pieces can be swapped, so their order is completely flexible. The N-th piece is never the inner piece of any valid operation, so it stays fixed at the rightmost position. Hence the minimum sum is achieved by sorting the first N-1 coordinates and keeping the last one unchanged.

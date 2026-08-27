We can flip any row or any column any number of times. Since flipping twice cancels, each row and each column is either flipped (1) or not (0). Let `r[i]` be 0/1 for row i, `c[j]` be 0/1 for column j. The final value at cell (i,j) is `A[i][j] XOR r[i] XOR c[j]`. We want to minimize the total number of 1s.

Fix the column flips `c`. Then for each row i, the row's contribution is the number of 1s in `A[i] XOR c`. We can choose `r[i]` to flip the row if that reduces the count. So for a fixed `c`, the optimal row flips give row i contribution `min(popcount(A[i] XOR c), W - popcount(A[i] XOR c))`. Sum over rows gives the total for that `c`.

Since W ≤ 18, we can enumerate all 2^W possible column flip masks (up to 262144). For each mask, compute the sum of `min(popcount(row XOR mask), W - popcount(row XOR mask))` over all rows, and take the minimum.

Complexity: O(H * 2^W) which is fine for H up to 2e5 and W ≤ 18.
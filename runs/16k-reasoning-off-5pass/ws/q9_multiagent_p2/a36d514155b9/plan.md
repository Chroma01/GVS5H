The problem asks for the sum of Manhattan distances between all pairs of pieces over all valid arrangements. By linearity of expectation (or summation), we can separate the Manhattan distance into row differences and column differences. The total sum is the sum of (row distance contribution) + (column distance contribution). For rows, we treat the grid as having `m` positions with `n` slots each, and we need to place `k` pieces. The number of ways to choose which rows contain pieces and how many pieces go into each row determines the row distance. However, a more efficient approach is to realize that the row and column problems are independent in terms of counting combinations. Specifically, the total sum is `Total_Ways * E[Distance]`. Alternatively, we can iterate over the distance `d` for rows and `d'` for columns. A better combinatorial approach: The total sum is the sum over all pairs of cells (u, v) of (Manhattan(u, v) * Number of ways to place k-2 other pieces such that one piece is at u and one is at v). Since pieces are identical, we fix two distinct cells u and v, calculate the distance, and multiply by the number of ways to choose the remaining k-2 pieces from the remaining mn-2 cells. Summing this over all pairs is O((mn)^2) which is too slow.
Instead, we use the linearity of expectation on the contribution of each coordinate difference. The total sum = (Sum of |r1 - r2| over all pairs of occupied rows weighted by counts) * (Ways to choose columns) + (Sum of |c1 - c2| over all pairs of occupied columns weighted by counts) * (Ways to choose rows).
Actually, the standard trick for "sum of distances over all subsets of size k" is:
Total Sum = Sum_{i<j} (Count of arrangements where piece i and piece j are at specific rows r_i, r_j and cols c_i, c_j) * (|r_i - r_j| + |c_i - c_j|).
Since the choice of rows and columns are independent, the number of ways to pick rows for k pieces is C(m, k_rows) * ... wait, pieces are identical, so we just choose k cells.
Let's reframe: We are choosing k cells out of M*N.
Total Sum = Sum_{all pairs of cells (u, v)} (|u.r - v.r| + |u.c - v.c|) * C(MN - 2, k - 2).
This simplifies to: C(MN-2, k-2) * [ Sum_{u,v} |u.r - v.r| + Sum_{u,v} |u.c - v.c| ].
The term Sum_{u,v} |u.r - v.r| can be calculated by iterating over all pairs of rows (r1, r2) and counting how many cells are in those rows.
For a fixed pair of rows r1 and r2, the number of pairs of cells (u, v) with u in row r1 and v in row r2 is n * n. The distance is |r1 - r2|.
Also, we must consider u and v in the same row? No, if u and v are in the same row, |u.r - v.r| = 0, so they don't contribute to the row part.
So, Row Contribution = C(MN-2, k-2) * Sum_{r1 < r2} ( |r1 - r2| * n^2 ).
Similarly, Col Contribution = C(MN-2, k-2) * Sum_{c1 < c2} ( |c1 - c2| * m^2 ).
We need to compute Sum_{r1 < r2} |r1 - r2| efficiently. This is a standard problem: sum of distances between all pairs in a line of length m.
Sum_{i=1 to m} Sum_{j=i+1 to m} (j-i) = Sum_{d=1 to m-1} d * (m-d).
This can be computed in O(1) or O(m). Given constraints m, n <= 10^5, O(m+n) is fine.
Finally, multiply by C(MN-2, k-2) modulo 10^9+7.
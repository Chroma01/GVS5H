We precompute prefix sums `SA` and `SB` for arrays `A` and `B`.  
The answer for a query `(X,Y)` is  

\[
S = X\cdot SB[Y] - Y\cdot SA[X] - 2\cdot F_1 + 2\cdot F_2
\]

where  

\[
F_1 = \sum_{i=1}^{X} \sum_{\substack{j\le Y \\ B_j\le A_i}} B_j ,\qquad 
F_2 = \sum_{i=1}^{X} A_i\cdot\bigl|\{j\le Y\mid B_j\le A_i\}\bigr|.
\]

For a fixed `Y`, when we insert a new `B_y = b` we must add `b` to `F_1` and `A_i` to `F_2` for every index `i` with `A_i \ge b`.  
We maintain two dynamic arrays `val1[i]` (the inner sum) and `val2[i]` (the inner count) over the original index order, supporting:

* **range update on a set** `{ i | A_i \ge b }`:
  * `val1[i] += b`
  * `val2[i] += A_i`
* **prefix sum query** `sum_{i=1}^{X} val1[i]` and `sum_{i=1}^{X} val2[i]`.

This is done with a segment tree over the index interval `[1,N]`.  
Each node stores the minimum and maximum `A_i` in its range, the static sum of `A_i`, and lazy values representing fully covered updates (the node is completely inside the set).  
When a node is fully covered we only touch the node (O(1)); otherwise we push lazy values to children and recurse.  
Each `B_y` update costs `O(log N)` amortised, and each query needs two prefix sums (`O(log N)`).  

We sort the `K` queries by `Y`, process `B` values in increasing order, answer all queries with the current `Y`, and finally output the answers in the original order.
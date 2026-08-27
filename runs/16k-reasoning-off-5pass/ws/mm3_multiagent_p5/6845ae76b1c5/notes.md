
## ideation
We need to answer K queries of the form: given prefix lengths X_k of A and Y_k of B, compute
S(X_k, Y_k) = Σ_{i≤X_k} Σ_{j≤Y_k} |A_i - B_j|.

N ≤ 1e5, K ≤ 1e4. Direct O(N²) per query is impossible.

Key observation: The sum is over a Cartesian product of two index‑prefix sets. If we process queries in increasing order of Y, we can incrementally add B elements one by one, maintaining the total contribution of all processed B’s to the current set of eligible A’s. Similarly, we can maintain the set of eligible A’s (indices ≤ X) by adding A elements as X grows.

Thus we need a data structure that supports:
- Insert an A value (with its original integer value) into a multiset.
- Query: given a new B value v, compute Σ_{a in multiset} |a - v|.

This can be done with two Fenwick trees (BIT) over coordinate‑compressed values of A:
- `cnt` BIT: number of inserted A’s with a given compressed value.
- `sum` BIT: sum of original A values for those inserted.

For a new B_j with compressed index `idx`, let:
- `cntL = query(cnt, idx)`, `sumL = query(sum, idx)`.
- `cntR = total_cnt - cntL`, `sumR = total_sum - sumL`.

Then contribution = (cntL * B_j - sumL) + (sumR - cntR * B_j).

We also need to know the compressed index of B_j to query the BITs. Since B values may not be in the compression set of A, we can compress the union of A and B values, or simply binary‑search the compressed coordinate of B_j in the sorted list of A values (using `bisect_right`).

Processing order:
- Sort queries by Y ascending.
- Keep pointers `bj` (current number of B elements processed) and `ai` (current number of A elements inserted into BITs).
- Maintain a running total `cur` = sum over all processed B’s and all inserted A’s of |A_i - B_j|.
- For each query (X_k, Y_k) in sorted order:
  1. While `bj < Y_k`: add B_{bj+1} to `cur` using the BIT contribution formula.
  2. While `ai < X_k`: insert A_{ai+1} into the BITs (update `cnt` and `sum`).
  3. Record `cur` as answer for this query.

Complexities:
- Sorting queries: O(K log K).
- Each A and B element is processed once: O(N log N).
- Each query does O(1) extra work.
- Total: O((N+K) log N) time, O(N) memory.

Pitfalls:
- Use 64‑bit integers (Python int is fine).
- Coordinate compression: sort unique values of A (or union of A and B). Since we only need to query BITs at positions corresponding to B values, we can compress only A values and use binary search to find the index for B values (the BIT query up to that index gives counts of A ≤ B_j).
- When B_j is smaller than all A values, `cntL = 0`, `sumL = 0`. When larger than all, `cntL = total_cnt`, `sumL = total_sum`.
- Ensure we add A elements before answering the query? Actually the order matters: we need A_i with i ≤ X_k and B_j with j ≤ Y_k. Since we process B first then A, the BITs contain exactly the A’s with index ≤ current X_k, and `cur` contains contributions from all B’s with index ≤ Y_k. So the order of adding A after B is correct.

## worker: Implement the solution in Python: read input, coor
- The algorithm processes queries in order of increasing `Y_k`. For each query, it first adds all `B_j` with `j ≤ Y_k` to a running total `cur_total`, then adds all `A_i` with `i ≤ X_k` into two Fenwick trees (one for counts, one for value sums).  
- The contribution of a new `B_j` to the current set of `A` values is computed using prefix counts and sums from the BITs:  
  `Σ |a - B_j| = (cntL * B_j - sumL) + (sumR - cntR * B_j)`, where `cntL`/`sumL` are the number/sum of `A` values `≤ B_j`.  
- Coordinate compression is applied only to `A` values; `B` values are mapped via `bisect_right` to find the appropriate prefix in the BITs.  
- Complexity: `O((N+K) log N)` time, `O(N)` memory.  
- Edge cases (e.g., `B_j` smaller/larger than all `A` values) are handled automatically by the BIT prefix sums.

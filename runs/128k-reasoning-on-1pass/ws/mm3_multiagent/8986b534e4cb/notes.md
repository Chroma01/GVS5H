
## ideation
- **Encoding with prefix sums**  
  Let `A[0]=0` and `A[i]=w[1]+…+w[i]`. A person travelling from `L` to `R` (`L<R`) needs `A[L‑1]=A[R]` (stamina 0 at both ends) and `A[x] > A[L‑1]` for every intermediate town `x` (mountain). If `L>R` the same holds with `<` (valley).  
  Hence each person is equivalent to an interval `[a,b] = [L‑1,R]` and a direction (`0` = mountain, `1` = valley).  
- **When do constraints conflict?**  
  For two persons of the **same direction** with intervals `[a1,b1]` and `[a2,b2]`, the constraints become contradictory exactly when the intervals **cross**: `a1 < a2 < b1 < b2`.  
  - Proof: For mountains we get `A[a2] > A[a1]` and `A[b1] > A[a2]` while `A[a1]=A[b1]`, impossible. Valleys give the symmetric contradiction.  
  - Intervals of opposite directions never cause a problem (they only give consistent inequalities).  
- **Feasibility condition**  
  A set of persons is satisfiable **iff** no two intervals of the same direction cross.  
- **Query reduction**  
  For a query `[L,R]` we must check whether the sub‑array `L..R` contains a crossing pair of the same direction.  
  - Compute for each person `i` the smallest index `j>i` that forms a crossing pair with `i` (same direction); call it `next[i]` (`INF` if none).  
  - In a query, if `min_{i∈[L,R]} next[i] ≤ R` then a crossing pair exists → answer **No**, otherwise answer **Yes**.  
- **Computing `next[i]`**  
  Process intervals of one direction together:  
  1. Sort by right endpoint `b` decreasing.  
  2. Scan groups with equal `b`.  
  3. For each interval `(a,b,i)` in the group, we need the smallest index `> i` among already inserted intervals whose left endpoint `a'` satisfies `a < a' < b`. This is a 2‑D range query (coordinate `a` and index `> i`).  
  4. Use a segment tree over the `a`‑axis. Each node stores a sorted list of indices that have been inserted.  
     - Query visits `O(log N)` nodes, binary‑searches the list (`O(log M)`) → `O(log N log M)`.  
     - Insertion also costs `O(log N log M)`.  
  5. After answering queries for the group, insert all its intervals into the segment tree.  
  Overall `O(M log N log M)` time and `O(M log N)` memory, performed twice (mountains, valleys).  
- **Answering queries**  
  Build a range‑minimum structure (sparse table or segment tree) on the two `next` arrays. Each query then needs two `O(1)` (or `O(log M)`) minima and a comparison with `R`.  
- **Pitfalls**  
  - Indexing: `a = min(S,T)-1`, `b = max(S,T)-1`. Use 0‑based for the answer array, 1‑based for the segment tree (insert at `a+1`).  
  - Crossing requires strict inequalities; touching (`a2 = b1`) is allowed.  
  - The answer condition is **inverted** in the original description: `min next[i] ≤ R` means a crossing exists → answer **No**.  
  - `|S−T|>1` guarantees `b−a ≥ 2`, so the interior range `[a+1, b-1]` is non‑empty.  
  - Large `N` (4·10⁵) forces the segment tree size to be a power of two; memory for `O(M log N)` sorted lists must be handled carefully in Python (use `bisect` on lists).  
  - Time: `M log N log M ≈ 2·10⁵·19·18 ≈ 7·10⁷` operations – need fast I/O and efficient code.  
  - Edge cases: `M=1` always “Yes”; opposite‑direction crossings are harmless.

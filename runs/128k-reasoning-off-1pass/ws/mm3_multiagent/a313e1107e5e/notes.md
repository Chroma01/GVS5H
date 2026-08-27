
## ideation
The problem asks for the length of the longest strictly increasing subsequence of the prefix `A[1..R]` that uses only elements `≤ X`.  
Constraints: `N, Q ≤ 2·10⁵`, values up to `10⁹`.

**Core difficulty** – We need many queries, each with a different prefix length and a different bound `X`. Recomputing LIS for each query is too slow.

**Key observation** – The classic O(N log N) LIS algorithm can be implemented with a Fenwick tree (BIT) where we maintain, for each possible value `v`, the maximum length of an increasing subsequence ending with value `v` after processing some prefix. When we process an element `a`:
```
best = max length among values < a
new length = best + 1
update position of a with new length (keeping the maximum)
```
The answer for a query `(R, X)` after processing the first `R` elements is simply the maximum stored value among positions corresponding to values `≤ X`.

Thus we can process queries offline:
1. Coordinate‑compress all `A[i]` and all `X_i`.
2. Sort queries by `R` ascending.
3. Sweep `i = 1..N`, updating the BIT with `A[i]`.
4. When the current index reaches a query’s `R`, answer it with `BIT.query(index_of_X)`.

Complexities: `O((N+Q) log (N+Q))` time, `O(N+Q)` memory.

## worker: Implement the coordinate compression and BIT-based
- Used coordinate compression of all `A[i]` and all `X_i` into a 1‑based index.
- A Fenwick tree (BIT) maintains the maximum length of an increasing subsequence ending at each compressed value.
- For each element `A[i]` we query the maximum among values `< A[i]` (strictly increasing), add 1, and update its position.
- Queries are processed in order of `R`; when the sweep reaches a query's `R`, the BIT already represents the prefix `A[1..R]`. The answer is the maximum over all values `≤ X`, which is exactly `bit.query(x_idx)`.
- Strictly increasing is handled by querying `v-1`; the bound `≤ X` includes equal values because we query up to `x_idx`.
- Complexity: `O((N+Q) log (N+Q))` time, `O(N+Q)` memory.
- Verified against the sample inputs (both produce the expected output).

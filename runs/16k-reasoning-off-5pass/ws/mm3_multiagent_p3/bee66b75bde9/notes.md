
## ideation
The problem asks whether a binary N×N matrix can be filled such that each row is a prefix of B’s followed by W’s, and each column is also a prefix of B’s followed by W’s, consistent with M precolored cells.

**Key reformulation:**
- There exist row thresholds `r[i] ∈ [0,N]` and column thresholds `c[j] ∈ [0,N]`.
- Cell `(i,j)` is B iff `i ≤ r[i]` **and** `j ≤ c[j]`, otherwise W.
- For a precolored B at `(i,j)`: need `r[i] ≥ i` and `c[j] ≥ j`.
- For a precolored W at `(i,j)`: need `r[i] < i` **or** `c[j] < j`.

**Sufficient and necessary condition:**
- Let `R_has_B[i] = True` if row i has at least one B cell, else False.
- Let `C_has_B[j] = True` if column j has at least one B cell, else False.
- If we set `r[i] = i` for rows with a B, else `0`; similarly for columns, then:
  - Any B cell becomes B (good).
  - A W cell `(i,j)` becomes B only if `R_has_B[i]` and `C_has_B[j]` both hold. So it is invalid to have a W cell where both the row and column have at least one B.

Thus the check is:
- For every W cell, it is NOT the case that (its row has a B) AND (its column has a B).

**Algorithm:**
1. Read N, M (N up to 1e9, M up to 2e5).
2. Maintain two hash sets: `rows_with_B` and `cols_with_B`.
3. Also collect all W cells in a list.
4. For each precolored cell:
   - If color is B, add its row to `rows_with_B` and its column to `cols_with_B`.
   - If color is W, store its (row, col).
5. For each stored W cell `(i,j)`:
   - If `i` is in `rows_with_B` **and** `j` is in `cols_with_B`, output `No`.
6. If no conflict, output `Yes`.

**Correctness:**
- The constructed thresholds `r[i] = i if rows_with_B else 0` and `c[j] = j if cols_with_B else 0` satisfy all B cells.
- Any W cell violating the condition would become B under these thresholds, so conflict implies impossibility.
- If no conflict, the thresholds work for all cells, so the answer is Yes.

**Complexity:**
- Time: O(M) average (hash set operations).
- Space: O(M) for storing W cells + O(M) for sets.

**Pitfalls:**
- N is huge (1e9) but we only care about rows/columns that appear in the M precolored cells, so hash sets are fine.
- M can be up to 2e5, which is fine for Python.
- Make sure to read input efficiently (use sys.stdin).

## worker: Implement the `solve()` function in Python: read N
The algorithm follows the derived necessary and sufficient condition: a W cell forces that either its row or its column cannot have any B cell (otherwise the cell would become B under the minimal valid thresholds). The implementation uses hash sets for the rows/columns that contain at least one B cell, then checks each W cell for a conflict. Complexity is O(M) time and O(M) space, which easily handles the constraints (M up to 2·10⁵, N up to 10⁹).

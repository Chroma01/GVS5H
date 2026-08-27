
## ideation
**Solution Explanation**

For each row we must choose a number `a[i]` (`0 ≤ a[i] ≤ N`) – the length of the black
prefix of that row.  
All rows together form a Young diagram, therefore the sequence `a[1]…a[N]`
must be non‑increasing:

```
a[1] ≥ a[2] ≥ … ≥ a[N]
```

For a coloured cell `(x , y , c)` we get a simple inequality for `a[x]`:

* `c = B` (black) → `a[x] ≥ y`
* `c = W` (white) → `a[x] ≤ y‑1`

Thus for each row we obtain an interval

```
L[x] = max column of a black cell in the row   (0 if none)
R[x] = min column of a white cell – 1            (N if none)

L[x] ≤ a[x] ≤ R[x]
```

If a row has `L[x] > R[x]` the instance is impossible.

Only rows that appear in the input give non‑trivial intervals; the other rows can
always be filled later.  
Let the constrained rows be `p1 < p2 < … < pK` with intervals `[L[p_k] , R[p_k]]`.

--------------------------------------------------------------------
**Greedy construction (top to bottom)**  

```
cur = N                     # biggest value we may put into the current row
for rows in increasing order:
        allowed = min(R[row] , cur)   # largest value respecting both constraints
        if allowed < L[row]: impossible
        cur = allowed                 # use this value
```

Why is it correct?  
For the current row we may choose any value in  
`[L[row] , min(R[row], cur)]`.  
Choosing the largest possible one makes `cur` as large as possible for all
later rows. If even this largest choice is smaller than `L[row]`,
no feasible value exists – the instance is impossible.
If the loop finishes, we can set the remaining unrestricted rows to `cur`
and obtain a non‑increasing sequence satisfying all intervals,
hence a valid coloring exists (the columns are then automatically correct).

The algorithm runs in `O(M log M)` time (sorting the distinct rows) and
`O(M)` memory.

--------------------------------------------------------------------
**Reference Implementation (Python 3)**

```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # per row: [max_black, min_white] (None for missing)
    row_info = {}

    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it).decode()          # 'B' or 'W'
        if x not in row_info:
            row_info[x] = [0, None]    # max_black, min_white
        if c == 'B':
            if y > row_info[x][0]:
                row_info[x][0] = y
        else:  # 'W'
            wm = row_info[x][1]
            if wm is None or y < wm:
                row_info[x][1] = y

    # Build list of constrained rows with their intervals [L, R]
    rows = []
    for x, (bm, wm) in row_info.items():
        L = bm                         # at least 0 if no black cell
        if wm is not None:
            R = wm - 1                 # a[x] ≤ wm‑1
        else:
            R = N
        if L > R:                      # contradictory requirements
            print("No")
            return
        rows.append((x, L, R))

    rows.sort()                        # increasing row index

    cur = N                            # maximal value we may use
    for _, L, R in rows:
        allowed = R if R < cur else cur   # min(R, cur)
        if allowed < L:
            print("No")
            return
        cur = allowed

    print("Yes")

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.

## worker: (Omitted because the solution is complete and corr
The solution models the problem as choosing for each row `i` a value `a[i]` (length of black prefix). The column condition forces `a[1] ≥ a[2] ≥ ... ≥ a[N]`. Each pre-colored cell gives a linear inequality on `a[x]`, yielding per-row intervals `[L[i], R[i]]`. A greedy top-to-bottom pass picks the largest feasible value for each row, which is optimal because maximizing `a[i]` never harms feasibility for later rows. Time complexity is `O(M log M)`, memory `O(M)`.

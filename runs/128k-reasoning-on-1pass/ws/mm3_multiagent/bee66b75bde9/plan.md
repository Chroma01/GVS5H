**Solution Explanation**

For every row we have to choose an integer `a[i] ( 0 ≤ a[i] ≤ N )`

* columns `1 … a[i]` are black, columns `a[i]+1 … N` are white  

For every column we have to choose an integer `b[j] ( 0 ≤ b[j] ≤ N )`

* rows `1 … b[j]` are black, rows `b[j]+1 … N` are white  

The two families of numbers are not independent.  
If we know the row numbers `a[1] , a[2] , … , a[N]` then the column numbers are forced:

```
b[j] = max { i | a[i] ≥ j }          (the highest row whose black part reaches column j)
```

`a[ ]` must be **non‑increasing** (`a[1] ≥ a[2] ≥ … ≥ a[N]`), otherwise the set of black cells would
not be a Young diagram and a column would contain a white cell above a black cell,
contradicting the column condition.

--------------------------------------------------------------------

#### 1.   From the given cells to inequalities for `a[i]`

Consider one already coloured cell `(x , y , colour)`.

* colour = **B** (black)  
  The cell belongs to the black prefix of its row, therefore `a[x] ≥ y`.  
  (The column condition is automatically satisfied, because `a[x] ≥ y` implies
  `b[y] ≥ x`.)

* colour = **W** (white)  
  The cell is not black in its row, therefore `a[x] < y`,
  i.e. `a[x] ≤ y-1`.  
  (Again the column condition gives the same inequality,
  because `a[x] < y` is equivalent to `b[y] < x`.)

So every pre‑coloured cell yields one **linear inequality** for the
corresponding row:

```
   black cell (x , y)   →   a[x] ≥ y
   white cell (x , y)   →   a[x] ≤ y-1
```

--------------------------------------------------------------------

#### 2.   Interval for each row

For a fixed row `i`

* let `L[i]` = the largest column of a black cell in this row  
  (`L[i] = 0` if the row has no black cell)
* let `R[i]` = the smallest column of a white cell in this row,
  then `a[i] ≤ R[i]-1`  
  (`R[i] = N+1` – i.e. we use `R[i] = N` – if the row has no white cell)

Hence the row must satisfy  

```
L[i] ≤ a[i] ≤ R[i]                (0 ≤ L[i] ≤ R[i] ≤ N)
```

If for some row `L[i] > R[i]` the instance is impossible.

Rows that never appear in the input have `L[i]=0 , R[i]=N`,
so they never restrict the solution.

--------------------------------------------------------------------

#### 3.   Feasibility of a non‑increasing sequence with given intervals

We have to choose integers `a[1] … a[N]`

```
L[i] ≤ a[i] ≤ R[i]      for all i
a[i] ≥ a[i+1]           for all i      (non‑increasing)
```

Only rows that really appear in the input can have a non‑trivial interval.
Let those rows be `p1 < p2 < … < pK` with intervals `[L[p_k] , R[p_k]]`.

Rows without constraints can always be filled with any decreasing values,
therefore they do not influence the feasibility.

--------------------------------------------------------------------
**Greedy construction (top to bottom)**  

```
cur = N                         // the biggest value we may still put into a row
for rows in increasing order:
        // we are allowed to put at most cur (because of non‑increase)
        // and at most R[row]
        allowed = min( R[row] , cur )
        if allowed < L[row]:   impossible
        cur = allowed           // use the biggest possible value
```

Why is the greedy choice correct?
*For a fixed previous value `cur` the current row can take any value in
`[max(L[row],0) , min(R[row],cur)]`.  
Choosing the largest possible value (`min(R[row],cur)`) makes `cur` as large
as possible for all later rows.  
If even this largest value is smaller than the required lower bound,
no other choice can work, because any smaller value would make `cur`
even smaller for the following rows.*

The algorithm works in `O(K log K)` (sorting) time and `O(K)` memory,
`K ≤ M ≤ 2·10⁵`.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm prints “Yes” iff a valid coloring exists.

---

##### Lemma 1  
For a coloring that satisfies the row and column conditions,
let `a[i]` be the number of black cells in row `i`.  
Then `a[1] ≥ a[2] ≥ … ≥ a[N]`.

**Proof.**  
If a cell `(i , j)` is black, all cells `(i' , j')` with `i' ≤ i , j' ≤ j`
must be black (otherwise the column or the row would contain a white
cell above/left of a black one).  
Consequently the black part of a lower row can never be longer than the
black part of a higher row. ∎



##### Lemma 2  
For a fixed row `i`

* a black pre‑coloured cell `(i , y)` is equivalent to the inequality `a[i] ≥ y`;
* a white pre‑coloured cell `(i , y)` is equivalent to the inequality `a[i] ≤ y‑1`.

**Proof.**  
*Black* : the row condition forces the leftmost `a[i]` cells of the row to be
black, therefore column `y ≤ a[i]` is necessary and sufficient.
*White* : the cell must lie in the white suffix, i.e. `a[i] < y`,
equivalently `a[i] ≤ y‑1`. ∎



##### Lemma 3  
A coloring satisfying all conditions exists **iff** there are integers
`a[1] … a[N]` such that  

* `L[i] ≤ a[i] ≤ R[i]` for every row `i` (intervals defined in Section&nbsp;2);
* `a[1] ≥ a[2] ≥ … ≥ a[N]`.

**Proof.**  
*If* a coloring exists, Lemma&nbsp;1 gives a non‑increasing sequence `a[ ]`.
Lemma&nbsp;2 shows that each pre‑coloured cell yields exactly the corresponding
inequality, therefore `a[i]` lies in `[L[i],R[i]]`.

*Only‑if* : given such a sequence, define a coloring by making exactly the
first `a[i]` cells of each row black.  
Because `a[ ]` is non‑increasing, the set of black cells is a Young diagram,
hence the column condition also holds (the column black count is
`b[j]=max{i | a[i] ≥ j}`, which is automatically non‑increasing). ∎



##### Lemma 4  
The greedy algorithm described in Section&nbsp;3 succeeds
(i.e. never meets `allowed < L[row]`) **iff** a sequence `a[ ]`
satisfying Lemma&nbsp;3 exists.

**Proof.**  
*If the algorithm fails* at some row `r`, we have
`allowed = min(R[r] , cur) < L[r]`.  
Any feasible sequence must use a value `a[r] ≤ cur` (non‑increase) and also
`a[r] ≥ L[r]`. Since even the largest possible value (`min(R[r],cur)`) is
already smaller than `L[r]`, no such `a[r]` exists – the instance is infeasible.

*If the algorithm succeeds*, let `a[i]` be the value it stores for every
constrained row (the value `allowed` that is never smaller than the lower
bound). For all other rows set `a[i]=cur` (the current maximum), which is
non‑increasing and inside `[0,N]`.  
By construction `L[i] ≤ a[i] ≤ R[i]` for every row, and the sequence is
non‑increasing, therefore Lemma&nbsp;3 is satisfied. ∎



##### Lemma 5  
The algorithm prints “Yes” exactly when a feasible coloring exists.

**Proof.**  
The algorithm first builds the intervals `[L[i],R[i]]` and rejects rows with
`L[i] > R[i]`.  
If it proceeds, Lemma&nbsp;4 shows that the greedy check succeeds exactly
when a non‑increasing sequence respecting all intervals exists.
By Lemma&nbsp;3 this is equivalent to the existence of a valid coloring. ∎



##### Theorem  
The program outputs “Yes” if and only if Takahashi can colour the whole
grid so that every row and every column consists of a black prefix followed
by a white suffix.

**Proof.**  
Directly from Lemma&nbsp;5. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*`M`* – number of pre‑coloured cells, `M ≤ 2·10⁵`.

* building the per‑row data: `O(M)`
* sorting the distinct rows: `O(K log K)` with `K ≤ M`
* greedy scan: `O(K)`

Memory consumption: `O(K)` for the rows that appear in the input.

Both limits easily satisfy the constraints (`N` can be as large as `10⁹`
but does not affect the complexity).

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # per row: [max_black, min_white]  (None for missing)
    row_info = {}

    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it).decode()          # 'B' or 'W'
        if x not in row_info:
            row_info[x] = [0, None]    # black_max, white_min
        if c == 'B':
            if y > row_info[x][0]:
                row_info[x][0] = y
        else:  # 'W'
            wm = row_info[x][1]
            if wm is None or y < wm:
                row_info[x][1] = y

    # build list of constrained rows with their intervals
    rows = []
    for x, (bm, wm) in row_info.items():
        L = bm                         # at least 0 if no black cell
        if wm is not None:
            R = wm - 1                  # a[i] <= wm-1
        else:
            R = N
        if L > R:                      # contradictory requirements
            print("No")
            return
        rows.append((x, L, R))

    rows.sort()                       # increasing row index

    cur = N                           # maximal value we may put into the current row
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
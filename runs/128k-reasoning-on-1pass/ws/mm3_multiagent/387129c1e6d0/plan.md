**Solution Explanation**

For every move Santa goes from the current point `(x , y)` to a new point

```
U : (x , y + C)        D : (x , y - C)
R : (x + C , y)        L : (x - C , y)
```

The whole walk consists of `M` axis–parallel segments.
A house `H = (hx , hy)` is *visited* iff it lies on at least one of those
segments (the segment endpoints are included).

The required output is

* the final position of Santa,
* the number of different visited houses.



--------------------------------------------------------------------

#### 1.   Geometry of a segment

* a *horizontal* segment has a fixed `y = y₀` and `x` runs in a closed interval
  `[x₁ , x₂]`.
* a *vertical*   segment has a fixed `x = x₀` and `y` runs in a closed interval
  `[y₁ , y₂]`.

So a house is visited **iff**

```
( hy == y₀  and  hx in [x₁ , x₂] )   for some horizontal segment,
or
( hx == x₀  and  hy in [y₁ , y₂] )   for some   vertical segment.
```

--------------------------------------------------------------------

#### 2.   Storing the segments

For fast queries we store the segments in two dictionaries

```
y_intervals[y] : list of (x_left , x_right)   (all horizontal segments with this y)
x_intervals[x] : list of (y_low  , y_high)    (all   vertical segments with this x)
```

While reading the moves we also update Santa’s position, therefore the final
coordinates are known after the loop.

The total number of stored intervals is exactly `M` ( ≤ 2·10⁵ ).

--------------------------------------------------------------------

#### 3.   From intervals to “does a point belong to any of them ?”

For a fixed `y` all horizontal intervals are known.
If they are **sorted by their left endpoint** we can answer the question  

```
does there exist an interval with left ≤ hx ≤ right ?
```

by a binary search:

```
starts = [ left of each interval ]          # sorted
idx    = rightmost index with starts[idx] ≤ hx   (bisect_right - 1)
if idx ≥ 0 and hx ≤ ends[idx]      →   yes
else                                 →   no
```

The same works for the vertical side.
Complexities per query: `O(log k)` where `k` is the number of intervals for that
fixed coordinate.

To obtain the two sorted lists for every key we sort each list once
(`O(k log k)`), the sum over all keys is `O(M log M)`.  
After sorting we keep only the two parallel arrays

```
starts = [left]   ,   ends = [right]
```

which are exactly what the binary search needs.

--------------------------------------------------------------------

#### 4.   Counting visited houses

For every house `(hx , hy)`

```
if hy in y_data:
        if hx lies in one of the horizontal intervals → visited = True
if not visited and hx in x_data:
        if hy lies in one of the   vertical intervals → visited = True
if visited:  answer += 1
```

Each house is examined once → `O(N log M)`.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints the correct final position and the correct
number of distinct visited houses.

---

##### Lemma 1  
For a horizontal segment from `(x₁ , y)` to `(x₂ , y)` the algorithm stores the
interval `[min(x₁,x₂) , max(x₁,x₂)]` in `y_intervals[y]`.

**Proof.**  
During processing a horizontal move the code computes the new `x` coordinate
(`x₂`), then `x_left = min(cur_x , new_x)`, `x_right = max(cur_x , new_x)` and
appends the pair `(x_left , x_right)` to the list belonging to the fixed `y`.
Both endpoints are included because the interval is closed. ∎



##### Lemma 2  
For a vertical segment from `(x , y₁)` to `(x , y₂)` the algorithm stores the
interval `[min(y₁,y₂) , max(y₁,y₂)]` in `x_intervals[x]`.

**Proof.**   Identical to Lemma&nbsp;1, using the fixed `x` coordinate. ∎



##### Lemma 3  
For a fixed `y` and a point `hx` the binary‑search test
(`bisect_right` on the sorted left ends) returns *true*  
iff there exists a stored horizontal segment with this `y` that contains `hx`.

**Proof.**  
All intervals are sorted by their left end `L`.  
`idx = max { i | L_i ≤ hx }` is exactly the rightmost interval whose left
endpoint is not larger than `hx`.  

*If* the algorithm reports *true*, then `hx ≤ R_idx`, therefore the interval
`[L_idx , R_idx]` contains `hx`.  

*Conversely*, if some interval `I` contains `hx`, let `j` be the index of `I`.
Because `L_j ≤ hx`, we have `idx ≥ j`. Since intervals are sorted,
`R_j ≤ R_idx` (or `j = idx`). In any case `hx ≤ R_idx`, so the test succeeds.
∎



##### Lemma 4  
A house `H = (hx , hy)` is counted by the algorithm **iff** it lies on at least
one segment of Santa’s walk.

**Proof.**  

*If part* – assume the algorithm counts `H`.  
There are two possibilities:

1. `hy` is a key of `y_data` and the binary search on the horizontal
   intervals reports *true*.  
   By Lemma&nbsp;3 there exists a stored horizontal interval with this `y`
   that contains `hx`. By Lemma&nbsp;1 this interval is exactly a segment of
   the walk, therefore `H` lies on that segment.

2. Otherwise `hx` is a key of `x_data` and the binary search on the vertical
   intervals reports *true*.  
   By Lemma&nbsp;3 (applied to the vertical side) a stored vertical interval
   with this `x` contains `hy`. By Lemma&nbsp;2 this interval is a segment of
   the walk, hence `H` lies on it.

*Only‑if part* – assume `H` lies on a segment of the walk.

* If the segment is horizontal, its `y` equals `hy`. By Lemma&nbsp;1 the
  algorithm stored the corresponding interval in `y_intervals[hy]`.  
  Since `hx` belongs to that interval, Lemma&nbsp;3 makes the binary search
  succeed, therefore the algorithm marks `H` visited.

* If the segment is vertical, the symmetric argument with `x_intervals` shows
  that the algorithm also marks `H` visited.

Thus `H` is counted. ∎



##### Lemma 5  
The final coordinates printed by the program are exactly the coordinates of
Santa after all moves.

**Proof.**  
The program updates `cur_x , cur_y` after reading each move according to the
definition of the four possible directions. After the last move the variables
contain the position after the last segment, which is precisely Santa’s final
position. ∎



##### Theorem  
The program outputs

* the correct final position of Santa, and
* the correct number of distinct houses that are passed through or arrived at
  during the whole walk.

**Proof.**  

*Final position* – Lemma&nbsp;5.  

*Number of visited houses* – by Lemma&nbsp;4 a house contributes `+1` to the
counter exactly when it lies on at least one segment, i.e. when it is visited.
The counter is increased at most once per house, therefore it equals the number
of *distinct* visited houses. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

*Building the segment lists* : `O(M)`  

*Sorting all interval lists*  : `O(M log M)`  

*Sorting overhead for the two parallel arrays* (same as above)

*Processing the houses*      : each house needs at most two binary searches  
                              `O(N log M)`

Overall  

```
Time   :  O( (N + M) log M )   ≤  about 4·10⁶ elementary operations
Memory :  O(N + M)              (houses + all intervals + auxiliary arrays)
```

Both limits easily satisfy the given constraints (`N, M ≤ 2·10⁵`).

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys
import bisect
from collections import defaultdict

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))

    houses = [(int(next(it)), int(next(it))) for _ in range(N)]

    # dictionaries: key -> list of intervals
    y_intervals = defaultdict(list)   # y -> [(x_left, x_right), ...]   horizontal
    x_intervals = defaultdict(list)   # x -> [(y_low,  y_high ), ...]   vertical

    cur_x, cur_y = Sx, Sy

    for _ in range(M):
        d = next(it)                # direction as bytes
        c = int(next(it))

        if d == b'L':
            new_x = cur_x - c
            new_y = cur_y
            xl = cur_x if cur_x < new_x else new_x
            xr = new_x if cur_x < new_x else cur_x
            y_intervals[cur_y].append((xl, xr))
        elif d == b'R':
            new_x = cur_x + c
            new_y = cur_y
            xl = cur_x if cur_x < new_x else new_x
            xr = new_x if cur_x < new_x else cur_x
            y_intervals[cur_y].append((xl, xr))
        elif d == b'U':
            new_y = cur_y + c
            new_x = cur_x
            yl = cur_y if cur_y < new_y else new_y
            yr = new_y if cur_y < new_y else cur_y
            x_intervals[cur_x].append((yl, yr))
        else:                     # d == b'D'
            new_y = cur_y - c
            new_x = cur_x
            yl = cur_y if cur_y < new_y else new_y
            yr = new_y if cur_y < new_y else cur_y
            x_intervals[cur_x].append((yl, yr))

        cur_x, cur_y = new_x, new_y

    final_x, final_y = cur_x, cur_y

    # ----- transform interval lists into sorted (starts, ends) ----------
    y_data = {}   # y -> (starts list, ends list)
    for y, lst in y_intervals.items():
        if not lst:
            continue
        lst.sort(key=lambda p: p[0])          # sort by left endpoint
        starts = [iv[0] for iv in lst]
        ends   = [iv[1] for iv in lst]
        y_data[y] = (starts, ends)

    x_data = {}
    for x, lst in x_intervals.items():
        if not lst:
            continue
        lst.sort(key=lambda p: p[0])
        starts = [iv[0] for iv in lst]
        ends   = [iv[1] for iv in lst]
        x_data[x] = (starts, ends)

    # ----- count distinct visited houses -------------------------------
    visited_cnt = 0
    for hx, hy in houses:
        visited = False

        # horizontal test
        if hy in y_data:
            starts, ends = y_data[hy]
            idx = bisect.bisect_right(starts, hx) - 1
            if idx >= 0 and hx <= ends[idx]:
                visited = True

        # vertical test (only if not already visited)
        if not visited and hx in x_data:
            starts, ends = x_data[hx]
            idx = bisect.bisect_right(starts, hy) - 1
            if idx >= 0 and hy <= ends[idx]:
                visited = True

        if visited:
            visited_cnt += 1

    # ----- output -------------------------------------------------------
    sys.stdout.write(f"{final_x} {final_y} {visited_cnt}")

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above and conforms to
the required input‑output format.
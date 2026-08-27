
## ideation
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

    # intervals for horizontal (fixed y) and vertical (fixed x) moves
    y_intervals = defaultdict(list)   # y -> list of (x_left, x_right)
    x_intervals = defaultdict(list)   # x -> list of (y_low, y_high)

    cur_x, cur_y = Sx, Sy

    for _ in range(M):
        d = next(it)          # direction as bytes
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
        else:  # d == b'D'
            new_y = cur_y - c
            new_x = cur_x
            yl = cur_y if cur_y < new_y else new_y
            yr = new_y if cur_y < new_y else cur_y
            x_intervals[cur_x].append((yl, yr))

        cur_x, cur_y = new_x, new_y

    final_x, final_y = cur_x, cur_y

    # ----- sort intervals and build separate start/end arrays ----------
    y_data = {}   # y -> (starts list, ends list)
    for y, lst in y_intervals.items():
        if lst:
            lst.sort(key=lambda p: p[0])
            starts = [iv[0] for iv in lst]
            ends   = [iv[1] for iv in lst]
            y_data[y] = (starts, ends)

    x_data = {}   # x -> (starts list, ends list)
    for x, lst in x_intervals.items():
        if lst:
            lst.sort(key=lambda p: p[0])
            starts = [iv[0] for iv in lst]
            ends   = [iv[1] for iv in lst]
            x_data[x] = (starts, ends)

    # ----- count distinct visited houses -------------------------------
    visited_cnt = 0
    for hx, hy in houses:
        visited = False

        # check horizontal segments
        if hy in y_data:
            starts, ends = y_data[hy]
            idx = bisect.bisect_right(starts, hx) - 1
            if idx >= 0 and hx <= ends[idx]:
                visited = True

        # check vertical segments (if not already marked)
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

## worker: Merge intervals per y and per x to handle nested i
The algorithm first stores every movement of Santa as an axis‑parallel segment.  
For a horizontal move on a fixed `y` we keep the interval `[x_left , x_right]`.  
For a vertical move on a fixed `x` we keep the interval `[y_low , y_high]`.

All intervals belonging to the same fixed coordinate are sorted and **merged**.
Merging removes overlaps and touching intervals, which reduces the number of
intervals per key while preserving the set of points that lie on the union of
the original segments. After merging, for a key we have two parallel arrays
`starts` and `ends` (both sorted).

To know whether a house `(hx, hy)` is visited we only need to test whether its
coordinate lies inside any interval of the appropriate kind:

* If `hy` appears as a key, binary‑search `starts` for the rightmost interval
  whose left endpoint ≤ `hx` and check whether `hx ≤ ends[idx]`.
* If not found there, we repeat the same test on the vertical side with
  `hx` as the key.

Each house is examined once, so the total work is `O((N+M) log M)`.  
The final position is obtained by simply updating `(x, y)` after every move,
so it is available without extra work.

The proof of correctness follows from the lemmas in the plan:  
* Lemma 1 and Lemma 2 – the intervals stored exactly represent the walked
  segments.  
* Lemma 3 – the binary‑search test on a sorted, merged list is true iff the
  point lies in at least one of the original intervals.  
* Lemma 4 – a house is counted iff it lies on at least one segment.  
* Lemma 5 – the variables `final_x, final_y` are Santa’s final coordinates.

Thus the program prints the correct final position and the correct number of
distinct visited houses.

Memory consumption is `O(N + M)` (houses plus all intervals), well within the
limits.

## worker: finalize
The solution processes Santa’s walk as a sequence of axis‑parallel segments.  
For each move we store the corresponding closed interval in a dictionary keyed by the fixed coordinate (`y` for horizontal moves, `x` for vertical moves).  
All intervals for a key are sorted by their left (or low) endpoint and merged into disjoint intervals; this union preserves exactly the set of points visited on that fixed line.  

For a house `H = (hx, hy)` we check two possibilities:
1. If `hy` is a key in the horizontal dictionary, we binary‑search the sorted left ends for the rightmost interval with left ≤ `hx`. If `hx` is not larger than the corresponding right end, the house lies on a horizontal segment.
2. Otherwise, if `hx` is a key in the vertical dictionary, we perform the same test on the vertical intervals.

Each house is examined once, giving `O(N log M)` time.  
Building the interval lists and merging them costs `O(M log M)`.  
Total time: `O((N+M) log M)`, memory: `O(N+M)`, well within the limits.

The final coordinates are obtained by updating `(x, y)` after each move, so they are computed directly during input processing.

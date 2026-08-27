
## ideation
```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # ---------- 1. total number of distinct values over all subarrays ----------
    last_pos = [0] * (N + 2)            # last occurrence of each value (1..N)
    total_distinct = 0
    for i, v in enumerate(A):
        prev = last_pos[v]              # previous occurrence of v (0 if none)
        # i is 0‑based, so position = i+1
        total_distinct += (i + 1 - prev) * (N - i)
        last_pos[v] = i + 1

    # ---------- 2. total number of adjacent value pairs over all subarrays ----------
    last = [0] * (N + 2)                # last occurrence of each value while scanning
    cur = 0                             # Σ_{v=1}^{N-1} min(last[v], last[v+1]) for current R
    total_adj = 0

    for i, a in enumerate(A):
        # Only the pairs (a-1, a) and (a, a+1) can change their minima
        vs = []
        if a > 1:
            vs.append(a - 1)
        if a < N:
            vs.append(a)

        # remember old minima before updating last[a]
        old_mins = [min(last[v], last[v + 1]) for v in vs]

        # update the last occurrence of a
        last[a] = i + 1

        # recompute minima for the affected pairs and update cur
        for v, old in zip(vs, old_mins):
            new = min(last[v], last[v + 1])
            cur += new - old

        total_adj += cur

    # ---------- 3. final answer ----------
    ans = total_distinct - total_adj
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
```

## worker: finalize
We transform the problem: for any subarray, the minimal number of operations equals the number of connected components of the set of distinct values, where two values are linked if they are consecutive integers. This is `d(L,R) - e(L,R)`, where `d` is the number of distinct values and `e` is the number of present adjacent pairs. Hence the required sum splits into two independent sums.  
The sum of distinct values is obtained by counting for each position `i` the number of subarrays where `i` is the first occurrence of `A[i]`, giving `(i - prev[i])·(N-i+1)`.  
The sum of adjacent pairs is computed by scanning from left to right, maintaining for each right end `R` the quantity `cur = Σ_v min(last[v], last[v+1])`. Only the two pairs involving the new element change, so we update `cur` in O(1) per step. The total `cur` over all `R` yields the sum of `e(L,R)`.  
Both parts are O(N) time and O(N) memory, well within the limits.

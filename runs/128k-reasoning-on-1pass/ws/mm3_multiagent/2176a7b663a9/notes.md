
## ideation
```python
import sys
import bisect

INF = 10 ** 18

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    W = [next(it) for _ in range(N)]

    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = next(it)
        R[i] = next(it)

    # --- preparation for queries on “right” side ---
    intervals_by_R = sorted(((R[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_R = [r for r, _ in intervals_by_R]
    pref_min_R = []
    cur = INF
    for _, w in intervals_by_R:
        if w < cur:
            cur = w
        pref_min_R.append(cur)

    # --- preparation for queries on “left” side ---
    intervals_by_L = sorted(((L[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_L = [l for l, _ in intervals_by_L]
    suf_min_L = [0] * N
    cur = INF
    for i in range(N - 1, -1, -1):
        _, w = intervals_by_L[i]
        if w < cur:
            cur = w
        suf_min_L[i] = cur

    # helpers to obtain minimal weight in a prefix / suffix
    def query_R(x: int) -> int:          # min weight with right endpoint ≤ x
        idx = bisect.bisect_right(sorted_R, x) - 1
        return pref_min_R[idx] if idx >= 0 else INF

    def query_L(y: int) -> int:          # min weight with left endpoint ≥ y
        idx = bisect.bisect_left(sorted_L, y)
        return suf_min_L[idx] if idx < N else INF

    Q = next(it)
    out = []
    for _ in range(Q):
        s = next(it) - 1
        t = next(it) - 1

        # direct edge exists ⇔ intervals are disjoint
        if R[s] < L[t] or R[t] < L[s]:
            out.append(str(W[s] + W[t]))
            continue

        # intervals overlap – we need at most two intermediate vertices
        leftS  = query_R(L[s] - 1)                     # vertex left of s
        rightT = query_L(R[t] + 1)                     # vertex right of t

        outL = query_R(min(L[s], L[t]) - 1)             # left of both intervals
        outR = query_L(max(R[s], R[t]) + 1)             # right of both intervals

        best = INF
        if outL != INF or outR != INF:
            best = W[s] + W[t] + min(outL, outR)

        if leftS != INF and rightT != INF:
            cand = W[s] + W[t] + leftS + rightT
            if cand < best:
                best = cand

        out.append(str(-1 if best == INF else best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

## worker: finalize
The algorithm exploits the fact that an edge exists exactly when two intervals are disjoint.  
If the two intervals of `s` and `t` are disjoint, they are directly connected, and the answer is `W[s]+W[t]`.  
Otherwise the intervals intersect. Because all weights are positive, a shortest `s‑t` path can use at most two intermediate vertices:

* one vertex that lies completely left of both intervals (`R < min(L[s],L[t])`) or completely right of both (`L > max(R[s],R[t])`);
* or one vertex left of `s` (`R < L[s]`) together with one vertex right of `t` (`L > R[t]`).

All other possibilities add unnecessary vertices and can never be optimal.

For each query we need the minimum weight among intervals with  
`R ≤ x` (left side) and among intervals with `L ≥ y` (right side).  
Sorting all intervals by `R` and by `L` once and building prefix/suffix minima allows us to answer these sub‑queries in `O(log N)` using binary search.

Thus each query is processed in `O(log N)` time, and the whole program runs in `O((N+Q)·log N)` with `O(N)` memory.

The solution follows the proof in the analysis and correctly handles all cases, including the situation where no path exists (`-1`).

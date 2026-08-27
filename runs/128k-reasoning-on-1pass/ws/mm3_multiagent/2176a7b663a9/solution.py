import sys
import bisect

INF = 10**18

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

    # sort by right endpoint
    intervals_by_R = sorted(((R[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_R = [r for r, _ in intervals_by_R]
    pref_min_R = []
    cur = INF
    for _, w in intervals_by_R:
        if w < cur:
            cur = w
        pref_min_R.append(cur)

    # sort by left endpoint
    intervals_by_L = sorted(((L[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_L = [l for l, _ in intervals_by_L]
    suf_min_L = [0] * N
    cur = INF
    for i in range(N - 1, -1, -1):
        _, w = intervals_by_L[i]
        if w < cur:
            cur = w
        suf_min_L[i] = cur

    # helpers
    def query_R(x: int) -> int:
        """minimum weight among vertices with right endpoint <= x"""
        idx = bisect.bisect_right(sorted_R, x) - 1
        return pref_min_R[idx] if idx >= 0 else INF

    def query_L(y: int) -> int:
        """minimum weight among vertices with left endpoint >= y"""
        idx = bisect.bisect_left(sorted_L, y)
        return suf_min_L[idx] if idx < N else INF

    Q = next(it)
    out = []
    for _ in range(Q):
        s = next(it) - 1
        t = next(it) - 1

        # direct edge if intervals are disjoint
        if R[s] < L[t] or R[t] < L[s]:
            out.append(str(W[s] + W[t]))
            continue

        # intervals overlap – need at most two intermediate vertices
        leftS = query_R(L[s] - 1)          # vertex left of s
        rightT = query_L(R[t] + 1)         # vertex right of t

        outL = query_R(min(L[s], L[t]) - 1)   # left of both intervals
        outR = query_L(max(R[s], R[t]) + 1)   # right of both intervals

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
import sys


def solve():
    it = map(int, sys.stdin.buffer.read().split())
    try:
        N = next(it)
    except StopIteration:
        return

    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = next(it)

    L = [0] * (N + 1)
    R = [0] * (N + 1)

    M = 2 * N + 2
    INF = 10**30

    # leftMin[x] will become min W_i over R_i < x
    # rightMin[x] will become min W_i over L_i > x
    leftMin = [INF] * (M + 1)
    rightMin = [INF] * (M + 1)

    for i in range(1, N + 1):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        w = W[i]
        if w < leftMin[r]:
            leftMin[r] = w
        if w < rightMin[l]:
            rightMin[l] = w

    cur = INF
    for x in range(M + 1):
        val = leftMin[x]
        leftMin[x] = cur
        if val < cur:
            cur = val

    cur = INF
    for x in range(M, -1, -1):
        val = rightMin[x]
        rightMin[x] = cur
        if val < cur:
            cur = val

    Q = next(it)
    out = []
    append = out.append

    Wloc = W
    Lloc = L
    Rloc = R
    left = leftMin
    right = rightMin
    inf = INF

    for _ in range(Q):
        s = next(it)
        t = next(it)

        ls = Lloc[s]
        rs = Rloc[s]
        lt = Lloc[t]
        rt = Rloc[t]
        base = Wloc[s] + Wloc[t]

        # Direct edge.
        if rs < lt or rt < ls:
            append(str(base))
            continue

        # Overlapping endpoints.
        # x is the endpoint with smaller L, y is the other endpoint.
        if ls <= lt:
            rx = rs
            ly = lt
        else:
            rx = rt
            ly = ls

        minL = ls if ls < lt else lt
        maxR = rs if rs > rt else rt

        # Two-edge paths: middle vertex left of both or right of both.
        best = left[minL]
        v = right[maxR]
        if v < best:
            best = v

        # Three-edge path: one middle vertex right of x, one left of y.
        a = right[rx]
        b = left[ly]
        if a < inf and b < inf:
            v = a + b
            if v < best:
                best = v

        if best >= inf:
            append("-1")
        else:
            append(str(base + best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
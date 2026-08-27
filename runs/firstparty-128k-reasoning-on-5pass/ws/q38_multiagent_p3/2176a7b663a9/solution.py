import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    INF = 10**30

    # Coordinates are in [1, 2N].  A little extra space is harmless.
    size = 2 * N + 4

    # minR[x] will become min weight with R < x.
    # minL[x] will become min weight with L > x.
    minR = [INF] * size
    minL = [INF] * size

    w_off = 1
    int_off = 1 + N

    for i in range(N):
        base = int_off + 2 * i
        l = data[base]
        r = data[base + 1]
        w = data[w_off + i]

        if w < minR[r]:
            minR[r] = w
        if w < minL[l]:
            minL[l] = w

    # Forward scan: strict prefix minimum over R.
    cur = INF
    for x in range(size):
        val = minR[x]
        minR[x] = cur
        if val < cur:
            cur = val

    # Backward scan: strict suffix minimum over L.
    cur = INF
    for x in range(size - 1, -1, -1):
        val = minL[x]
        minL[x] = cur
        if val < cur:
            cur = val

    pref = minR
    suff = minL

    q_off = int_off + 2 * N
    Q = data[q_off]
    idx = q_off + 1

    out = []
    append = out.append

    d = data
    w_off_local = w_off
    int_off_local = int_off
    pref_local = pref
    suff_local = suff
    INF_local = INF

    for _ in range(Q):
        s = d[idx] - 1
        t = d[idx + 1] - 1
        idx += 2

        ws = d[w_off_local + s]
        wt = d[w_off_local + t]

        bs = int_off_local + 2 * s
        bt = int_off_local + 2 * t

        ls = d[bs]
        rs = d[bs + 1]
        lt = d[bt]
        rt = d[bt + 1]

        # If the two query intervals are disjoint, the direct edge is optimal.
        if rs < lt or rt < ls:
            append(str(ws + wt))
            continue

        # Intersecting case: only 2-edge or 3-edge paths can be optimal.
        min_l = ls if ls < lt else lt
        max_r = rs if rs > rt else rt

        best = pref_local[min_l]

        v = suff_local[max_r]
        if v < best:
            best = v

        v = suff_local[rs] + pref_local[lt]
        if v < best:
            best = v

        v = suff_local[rt] + pref_local[ls]
        if v < best:
            best = v

        if best >= INF_local:
            append("-1")
        else:
            append(str(ws + wt + best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
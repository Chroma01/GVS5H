import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    N = int(data[idx])
    idx += 1

    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(data[idx])
        idx += 1

    L = [0] * (N + 1)
    R = [0] * (N + 1)

    maxc = 2 * N + 5
    INF = 10**30

    pref_at = [INF] * maxc
    suff_at = [INF] * maxc

    for i in range(1, N + 1):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        L[i] = l
        R[i] = r
        w = W[i]
        if w < pref_at[r]:
            pref_at[r] = w
        if w < suff_at[l]:
            suff_at[l] = w

    # pref[c] = minimum W_i such that R_i <= c
    pref = [INF] * maxc
    cur = INF
    for c in range(maxc):
        v = pref_at[c]
        if v < cur:
            cur = v
        pref[c] = cur

    # suff[c] = minimum W_i such that L_i >= c
    suff = [INF] * maxc
    cur = INF
    for c in range(maxc - 1, -1, -1):
        v = suff_at[c]
        if v < cur:
            cur = v
        suff[c] = cur

    del pref_at, suff_at

    Q = int(data[idx])
    idx += 1

    out = []
    append = out.append

    for _ in range(Q):
        s = int(data[idx])
        t = int(data[idx + 1])
        idx += 2

        ws = W[s]
        wt = W[t]
        ls = L[s]
        lt = L[t]
        rs = R[s]
        rt = R[t]

        # Direct edge: intervals are disjoint.
        if rs < lt or rt < ls:
            append(str(ws + wt))
            continue

        base = ws + wt

        min_l = ls if ls < lt else lt
        max_r = rs if rs > rt else rt

        # Two-edge candidate: one vertex disjoint from both endpoints.
        best = pref[min_l - 1]
        v = suff[max_r + 1]
        if v < best:
            best = v

        # Three-edge candidate: only when the two intervals cross.
        if ls < lt and rs < rt:
            # first middle: L > rs, second middle: R < lt
            x = suff[rs + 1]
            y = pref[lt - 1]
            if x < INF and y < INF:
                cand = x + y
                if cand < best:
                    best = cand
        elif lt < ls and rt < rs:
            # first middle: R < ls, second middle: L > rt
            x = pref[ls - 1]
            y = suff[rt + 1]
            if x < INF and y < INF:
                cand = x + y
                if cand < best:
                    best = cand

        if best >= INF:
            append("-1")
        else:
            append(str(base + best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
import sys

def main():
    read = sys.stdin.buffer.readline
    N = int(read())
    W = list(map(int, read().split()))

    M = 2 * N
    INF = 10 ** 30
    size = 1 << (M - 1).bit_length()
    base = size

    segL = [INF] * (2 * size)
    segR = [INF] * (2 * size)
    L = [0] * N
    R = [0] * N

    for i in range(N):
        l, r = map(int, read().split())
        L[i] = l
        R[i] = r
        w = W[i]

        p = base + l - 1
        if w < segL[p]:
            segL[p] = w

        p = base + r - 1
        if w < segR[p]:
            segR[p] = w

    for p in range(base - 1, 0, -1):
        p2 = p << 1

        left = segL[p2]
        right = segL[p2 | 1]
        segL[p] = left if left < right else right

        left = segR[p2]
        right = segR[p2 | 1]
        segR[p] = left if left < right else right

    prefR = [INF] * (M + 2)
    cur = INF
    for x in range(1, M + 1):
        v = segR[base + x - 1]
        if v < cur:
            cur = v
        prefR[x] = cur

    suffL = [INF] * (M + 2)
    cur = INF
    for x in range(M, 0, -1):
        v = segL[base + x - 1]
        if v < cur:
            cur = v
        suffL[x] = cur

    def query(tree, l, r, size=base, INF=INF):
        l += size
        r += size
        res = INF
        while l < r:
            if l & 1:
                v = tree[l]
                if v < res:
                    res = v
                l += 1
            if r & 1:
                r -= 1
                v = tree[r]
                if v < res:
                    res = v
            l >>= 1
            r >>= 1
        return res

    Q = int(read())
    out = []
    append = out.append

    q = query
    inf = INF
    L_arr = L
    R_arr = R
    W_arr = W
    pref = prefR
    suff = suffL
    segL_arr = segL
    segR_arr = segR

    for _ in range(Q):
        s, t = map(int, read().split())
        s -= 1
        t -= 1

        ls = L_arr[s]
        rs = R_arr[s]
        lt = L_arr[t]
        rt = R_arr[t]
        wsum = W_arr[s] + W_arr[t]

        if rs < lt or rt < ls:
            append(str(wsum))
            continue

        best = inf

        minl = ls if ls < lt else lt
        maxr = rs if rs > rt else rt

        m = pref[minl - 1]
        v = suff[maxr + 1]
        if v < m:
            m = v
        if m < inf:
            best = wsum + m

        if ls < lt <= rs < rt:
            a = q(segL_arr, rs, rt)
            if a < inf:
                b = q(segR_arr, ls - 1, lt - 1)
                if b < inf:
                    cand = wsum + a + b
                    if cand < best:
                        best = cand
        elif lt < ls <= rt < rs:
            a = q(segL_arr, rt, rs)
            if a < inf:
                b = q(segR_arr, lt - 1, ls - 1)
                if b < inf:
                    cand = wsum + a + b
                    if cand < best:
                        best = cand

        if best < inf:
            append(str(best))
        else:
            append("-1")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
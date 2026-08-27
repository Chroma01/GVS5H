import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, Q = data[0], data[1], data[2]
    idx = 3

    ls = [0] * M
    rs = [0] * M
    sg = [0] * M

    for i in range(M):
        S = data[idx]
        T = data[idx + 1]
        idx += 2
        if S < T:
            ls[i] = S - 1
            rs[i] = T - 1
            sg[i] = 0          # strict minimum
        else:
            ls[i] = T - 1
            rs[i] = S - 1
            sg[i] = 1          # strict maximum

    qdata = data[idx:]
    del data

    size = 1
    while size < N:
        size <<= 1

    INF = N + 1
    NEG = -1

    # For each sign:
    # min tree: position = right endpoint, value = left endpoint
    # max tree: position = left endpoint,  value = right endpoint
    min0 = [INF] * (2 * size)
    min1 = [INF] * (2 * size)
    max0 = [NEG] * (2 * size)
    max1 = [NEG] * (2 * size)

    left_cnt = [0] * N
    right_cnt = [0] * N
    limit = [0] * M

    def try_add(i, ls=ls, rs=rs, sg=sg, left_cnt=left_cnt, right_cnt=right_cnt,
                min0=min0, min1=min1, max0=max0, max1=max1,
                size=size, INF=INF, NEG=NEG):
        l = ls[i]
        r = rs[i]
        s = sg[i]

        # Same-side endpoint conflicts are forbidden for both signs.
        if left_cnt[l] or right_cnt[r]:
            return False

        ql = l + 1
        qr = r

        mt = min1 if s else min0
        xt = max1 if s else max0

        # One traversal gives:
        #   min left endpoint among active right endpoints in (l, r)
        #   max right endpoint among active left endpoints in (l, r)
        a0 = ql + size
        b0 = qr + size
        a = a0
        b = b0
        res_min = INF
        res_max = NEG

        while a < b:
            if a & 1:
                v = mt[a]
                if v < res_min:
                    res_min = v
                w = xt[a]
                if w > res_max:
                    res_max = w
                a += 1
            if b & 1:
                b -= 1
                v = mt[b]
                if v < res_min:
                    res_min = v
                w = xt[b]
                if w > res_max:
                    res_max = w
            a >>= 1
            b >>= 1

        # Same-sign crossing exists iff one of these holds.
        if res_min < l or res_max > r:
            return False

        left_cnt[l] = 1
        right_cnt[r] = 1

        # Update min tree at right endpoint r with left endpoint l.
        p = r + size
        mt[p] = l
        p >>= 1
        while p:
            c = p << 1
            left = mt[c]
            right = mt[c | 1]
            mt[p] = left if left < right else right
            p >>= 1

        # Update max tree at left endpoint l with right endpoint r.
        p = l + size
        xt[p] = r
        p >>= 1
        while p:
            c = p << 1
            left = xt[c]
            right = xt[c | 1]
            xt[p] = left if left > right else right
            p >>= 1

        return True

    def remove(i, ls=ls, rs=rs, sg=sg, left_cnt=left_cnt, right_cnt=right_cnt,
               min0=min0, min1=min1, max0=max0, max1=max1,
               size=size, INF=INF, NEG=NEG):
        l = ls[i]
        r = rs[i]
        s = sg[i]

        left_cnt[l] = 0
        right_cnt[r] = 0

        mt = min1 if s else min0
        p = r + size
        mt[p] = INF
        p >>= 1
        while p:
            c = p << 1
            left = mt[c]
            right = mt[c | 1]
            mt[p] = left if left < right else right
            p >>= 1

        xt = max1 if s else max0
        p = l + size
        xt[p] = NEG
        p >>= 1
        while p:
            c = p << 1
            left = xt[c]
            right = xt[c | 1]
            xt[p] = left if left > right else right
            p >>= 1

    R = 0
    ta = try_add
    rm = remove

    for L in range(M):
        while R < M and ta(R):
            R += 1
        limit[L] = R
        if R > L:
            rm(L)

    out = []
    append = out.append
    j = 0
    for _ in range(Q):
        Lq = qdata[j]
        Rq = qdata[j + 1]
        j += 2
        if Rq <= limit[Lq - 1]:
            append("Yes")
        else:
            append("No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    w_base = 1
    lr_base = 1 + n
    q = data[lr_base + 2 * n]

    max_c = 2 * n
    INF = 10**18
    INF_HALF = INF // 2

    min_r = [INF] * (max_c + 2)
    min_l = [INF] * (max_c + 2)

    for i in range(n):
        w = data[w_base + i]
        l = data[lr_base + 2 * i]
        r = data[lr_base + 2 * i + 1]
        if w < min_r[r]:
            min_r[r] = w
        if w < min_l[l]:
            min_l[l] = w

    # pref[x] = minimum weight of an interval with R < x
    pref = [INF] * (max_c + 2)
    cur = INF
    for x in range(1, max_c + 2):
        v = min_r[x - 1]
        if v < cur:
            cur = v
        pref[x] = cur

    # suff[x] = minimum weight of an interval with L > x
    suff = [INF] * (max_c + 2)
    cur = INF
    for x in range(max_c, -1, -1):
        v = min_l[x + 1]
        if v < cur:
            cur = v
        suff[x] = cur

    del min_r, min_l

    out = []
    append = out.append
    idx = lr_base + 2 * n + 1

    d = data
    p_arr = pref
    s_arr = suff

    for _ in range(q):
        s = d[idx] - 1
        t = d[idx + 1] - 1
        idx += 2

        b1 = lr_base + (s << 1)
        b2 = lr_base + (t << 1)

        w1 = d[w_base + s]
        l1 = d[b1]
        r1 = d[b1 + 1]

        w2 = d[w_base + t]
        l2 = d[b2]
        r2 = d[b2 + 1]

        # Disjoint intervals: direct edge is optimal.
        if r1 < l2 or r2 < l1:
            append(str(w1 + w2))
            continue

        # One interval contains the other.
        if l1 <= l2 and r2 <= r1:
            extra = p_arr[l1]
            v = s_arr[r1]
            if v < extra:
                extra = v
            if extra >= INF_HALF:
                append("-1")
            else:
                append(str(w1 + w2 + extra))
        elif l2 <= l1 and r1 <= r2:
            extra = p_arr[l2]
            v = s_arr[r2]
            if v < extra:
                extra = v
            if extra >= INF_HALF:
                append("-1")
            else:
                append(str(w1 + w2 + extra))
        else:
            # Crossing intervals.
            if l1 < l2:
                le = l1
                re = r1
                ll = l2
                rl = r2
            else:
                le = l2
                re = r2
                ll = l1
                rl = r1

            # Length-2 path through a common disjoint interval.
            common = p_arr[le]
            v = s_arr[rl]
            if v < common:
                common = v

            # Length-3 path: right of early, then left of late.
            p = p_arr[ll]
            sm = s_arr[re]
            if p >= INF_HALF or sm >= INF_HALF:
                two = INF
            else:
                two = p + sm

            extra = common if common < two else two
            if extra >= INF_HALF:
                append("-1")
            else:
                append(str(w1 + w2 + extra))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
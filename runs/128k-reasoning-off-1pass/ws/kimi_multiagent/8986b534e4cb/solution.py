import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    Q = int(data[2])

    # Person i -> interval on prefix positions [p, q] (p = a-1, q = b-1,
    # a = min(S,T), b = max(S,T)); type 0 = "U" (S<T, interior above),
    # type 1 = "D" (S>T, interior below).
    P = [0] * (M + 1)
    Qm = [0] * (M + 1)
    T = [0] * (M + 1)
    k = 3
    for i in range(1, M + 1):
        s = int(data[k]); t2 = int(data[k + 1]); k += 2
        if s < t2:
            P[i] = s - 1; Qm[i] = t2 - 1; T[i] = 0
        else:
            P[i] = t2 - 1; Qm[i] = s - 1; T[i] = 1

    SZ = 1
    while SZ < N:
        SZ <<= 1
    INF = N + 1
    B = N + 2

    # Per type:
    #   segQ[t]: segment tree over position x holding max q_i among window
    #            intervals of type t with p_i = x  (range max query)
    #   segP[t]: segment tree over position x holding min p_i among window
    #            intervals of type t with q_i = x  (range min query)
    segQ = [[-1] * (2 * SZ) for _ in range(2)]
    segP = [[INF] * (2 * SZ) for _ in range(2)]
    # Leaf occupant packs (at most 2 occupants per leaf in a valid window
    # plus the transient newcomer): two slots of (value+1), base B.
    packQ = [[0] * N for _ in range(2)]
    packP = [[0] * N for _ in range(2)]
    cntP = [0] * N   # global (both types) count of intervals with p = x
    cntQ = [0] * N   # global count of intervals with q = x

    def upd_max(seg, pos, val):
        i = pos + SZ
        seg[i] = val
        i >>= 1
        while i:
            x = seg[i + i]; y = seg[i + i + 1]
            seg[i] = x if x > y else y
            i >>= 1

    def upd_min(seg, pos, val):
        i = pos + SZ
        seg[i] = val
        i >>= 1
        while i:
            x = seg[i + i]; y = seg[i + i + 1]
            seg[i] = x if x < y else y
            i >>= 1

    def range_query(segq, segp, l, r):
        # inclusive [l, r]; returns (max over segq, min over segp)
        l += SZ
        r += SZ + 1
        mq = -1
        mp = INF
        while l < r:
            if l & 1:
                v = segq[l]
                if v > mq:
                    mq = v
                v = segp[l]
                if v < mp:
                    mp = v
                l += 1
            if r & 1:
                r -= 1
                v = segq[r]
                if v > mq:
                    mq = v
                v = segp[r]
                if v < mp:
                    mp = v
            l >>= 1
            r >>= 1
        return mq, mp

    left = [0] * (M + 1)
    l = 1
    for r in range(1, M + 1):
        # ---- insert person r ----
        p = P[r]; q = Qm[r]; t = T[r]
        cntP[p] += 1
        cntQ[q] += 1
        pk = packQ[t][p]
        s1 = pk % B
        v = q + 1
        if s1 == 0:
            packQ[t][p] = v
            mq = v
        else:
            packQ[t][p] = s1 + v * B
            mq = v if v > s1 else s1
        upd_max(segQ[t], p, mq - 1)
        pk = packP[t][q]
        s1 = pk % B
        v = p + 1
        if s1 == 0:
            packP[t][q] = v
            mp = v
        else:
            packP[t][q] = s1 + v * B
            mp = v if v < s1 else s1
        upd_min(segP[t], q, mp - 1)

        segqt = segQ[t]
        segpt = segP[t]
        # ---- shrink window until person r has no conflict ----
        while True:
            bad = False
            if cntP[p] >= 2 or cntQ[q] >= 2:
                bad = True
            else:
                mqq, mpp = range_query(segqt, segpt, p + 1, q - 1)
                if mqq > q or mpp < p:
                    bad = True
            if not bad:
                break
            # ---- delete person l ----
            dp = P[l]; dq = Qm[l]; dt = T[l]
            cntP[dp] -= 1
            cntQ[dq] -= 1
            pk = packQ[dt][dp]
            s1 = pk % B; s2 = pk // B
            v = dq + 1
            if s1 == v:
                s1 = 0
            else:
                s2 = 0
            packQ[dt][dp] = s1 + s2 * B
            upd_max(segQ[dt], dp, (s1 if s1 > s2 else s2) - 1)
            pk = packP[dt][dq]
            s1 = pk % B; s2 = pk // B
            v = dp + 1
            if s1 == v:
                s1 = 0
            else:
                s2 = 0
            packP[dt][dq] = s1 + s2 * B
            if s1 == 0:
                mp = s2
            elif s2 == 0:
                mp = s1
            else:
                mp = s1 if s1 < s2 else s2
            upd_min(segP[dt], dq, mp - 1 if mp else INF)
            l += 1
        left[r] = l

    out = []
    for _ in range(Q):
        L = int(data[k]); R = int(data[k + 1]); k += 2
        out.append("Yes" if L >= left[R] else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
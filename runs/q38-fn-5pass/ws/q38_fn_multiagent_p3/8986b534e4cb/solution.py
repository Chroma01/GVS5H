import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    M = data[p + 1]
    Q = data[p + 2]
    p += 3

    # 2^20 > max(N, M) under the constraints.
    SH = 20
    MASK = (1 << SH) - 1

    l = [0] * (M + 1)
    r = [0] * (M + 1)
    bad = [0] * (M + 1)

    idx_plus = []
    idx_minus = []

    # Endpoint-conflict structures.
    left_i1 = [0] * (N + 1)
    left_v1 = [0] * (N + 1)
    left_i2 = [0] * (N + 1)

    right_i1 = [0] * (N + 1)
    right_v1 = [0] * (N + 1)
    right_i2 = [0] * (N + 1)

    last_interval = {}

    # Read people and compute all non-crossing conflicts online.
    for i in range(1, M + 1):
        S = data[p]
        T = data[p + 1]
        p += 2

        if S < T:
            li, ri, s = S, T, 1
            idx_plus.append(i)
        else:
            li, ri, s = T, S, -1
            idx_minus.append(i)

        l[i] = li
        r[i] = ri

        b = 0

        # Same interval, opposite direction.
        base = (li << SH) | ri
        if s == 1:
            key = (base << 1) | 1
            opp = base << 1
        else:
            key = base << 1
            opp = (base << 1) | 1

        cand = last_interval.get(opp, 0)
        if cand > b:
            b = cand
        last_interval[key] = i

        # Same left endpoint, different right endpoint.
        i1 = left_i1[li]
        if i1:
            if left_v1[li] != ri:
                cand = i1
            else:
                cand = left_i2[li]
            if cand > b:
                b = cand

            if left_v1[li] == ri:
                left_i1[li] = i
            else:
                left_i2[li] = i1
                left_i1[li] = i
                left_v1[li] = ri
        else:
            left_i1[li] = i
            left_v1[li] = ri

        # Same right endpoint, different left endpoint.
        i1 = right_i1[ri]
        if i1:
            if right_v1[ri] != li:
                cand = i1
            else:
                cand = right_i2[ri]
            if cand > b:
                b = cand

            if right_v1[ri] == li:
                right_i1[ri] = i
            else:
                right_i2[ri] = i1
                right_i1[ri] = i
                right_v1[ri] = li
        else:
            right_i1[ri] = i
            right_v1[ri] = li

        bad[i] = b

    Lq = [0] * Q
    Rq = [0] * Q
    for k in range(Q):
        Lq[k] = data[p]
        Rq[k] = data[p + 1]
        p += 2

    del data
    del left_i1, left_v1, left_i2
    del right_i1, right_v1, right_i2
    del last_interval

    def run_cross(idxs, rev):
        """Add same-sign crossing conflicts for one sign.

        If rev == False, detects:
            l_i < l_j < r_i < r_j
        If rev == True, coordinates are reversed, detecting:
            l_j < l_i < r_j < r_i
        """
        if len(idxs) < 2:
            return

        ll = l
        rr = r
        NN = N

        if not rev:
            coords = sorted({ll[i] for i in idxs})
        else:
            coords = sorted({NN - rr[i] + 1 for i in idxs})

        K = len(coords)
        size = 1
        while size < K:
            size <<= 1

        pos = [-1] * (N + 1)
        for j, x in enumerate(coords):
            pos[x] = j

        tree = [None] * (2 * size)

        bl = bisect_left
        tr = tree
        sz = size
        badl = bad
        sh = SH
        mask = MASK
        posl = pos
        coord = coords
        last_real = K - 1
        last_tree = sz - 1

        if not rev:
            for i in idxs:
                li = ll[i]
                ri = rr[i]
                thresh = ri << sh

                bi = badl[i]
                if bi < i - 1:
                    node = posl[li] + sz
                    res = 0
                    while node:
                        lst = tr[node]
                        if lst:
                            if lst[-1] < thresh:
                                cand = lst[-1] & mask
                            elif lst[0] >= thresh:
                                cand = 0
                            else:
                                cand = lst[bl(lst, thresh) - 1] & mask
                            if cand > res:
                                res = cand
                        node >>= 1

                    if res > bi:
                        badl[i] = res

                a = bl(coord, li + 1)
                b = bl(coord, ri) - 1
                if a <= b:
                    if b == last_real:
                        b = last_tree

                    val = thresh + i
                    limit = thresh
                    ln = a + sz
                    rn = b + sz

                    while ln <= rn:
                        if ln & 1:
                            lst = tr[ln]
                            if lst is None:
                                tr[ln] = [val]
                            else:
                                while lst and lst[-1] >= limit:
                                    lst.pop()
                                lst.append(val)
                            ln += 1

                        if not (rn & 1):
                            lst = tr[rn]
                            if lst is None:
                                tr[rn] = [val]
                            else:
                                while lst and lst[-1] >= limit:
                                    lst.pop()
                                lst.append(val)
                            rn -= 1

                        ln >>= 1
                        rn >>= 1

        else:
            for i in idxs:
                lrev = NN - rr[i] + 1
                rrev = NN - ll[i] + 1
                thresh = rrev << sh

                bi = badl[i]
                if bi < i - 1:
                    node = posl[lrev] + sz
                    res = 0
                    while node:
                        lst = tr[node]
                        if lst:
                            if lst[-1] < thresh:
                                cand = lst[-1] & mask
                            elif lst[0] >= thresh:
                                cand = 0
                            else:
                                cand = lst[bl(lst, thresh) - 1] & mask
                            if cand > res:
                                res = cand
                        node >>= 1

                    if res > bi:
                        badl[i] = res

                a = bl(coord, lrev + 1)
                b = bl(coord, rrev) - 1
                if a <= b:
                    if b == last_real:
                        b = last_tree

                    val = thresh + i
                    limit = thresh
                    ln = a + sz
                    rn = b + sz

                    while ln <= rn:
                        if ln & 1:
                            lst = tr[ln]
                            if lst is None:
                                tr[ln] = [val]
                            else:
                                while lst and lst[-1] >= limit:
                                    lst.pop()
                                lst.append(val)
                            ln += 1

                        if not (rn & 1):
                            lst = tr[rn]
                            if lst is None:
                                tr[rn] = [val]
                            else:
                                while lst and lst[-1] >= limit:
                                    lst.pop()
                                lst.append(val)
                            rn -= 1

                        ln >>= 1
                        rn >>= 1

    run_cross(idx_plus, False)
    run_cross(idx_plus, True)
    run_cross(idx_minus, False)
    run_cross(idx_minus, True)

    del l, r, idx_plus, idx_minus, run_cross

    # Prefix maximum of bad[j].
    mx = 0
    for i in range(1, M + 1):
        if bad[i] > mx:
            mx = bad[i]
        bad[i] = mx

    out = []
    app = out.append
    for k in range(Q):
        if bad[Rq[k]] < Lq[k]:
            app("Yes")
        else:
            app("No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
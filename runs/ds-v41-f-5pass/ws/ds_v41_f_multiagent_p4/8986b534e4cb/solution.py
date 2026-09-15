import sys

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    M = int(data[p]); p += 1
    Q = int(data[p]); p += 1

    PL = [0] * (M + 1)
    PR = [0] * (M + 1)
    plus = []
    minus = []
    for i in range(1, M + 1):
        s = int(data[p]); t = int(data[p + 1]); p += 2
        if s < t:
            PL[i] = s; PR[i] = t
            plus.append(i)
        else:
            PL[i] = t; PR[i] = s
            minus.append(i)

    g2 = [0] * (M + 1)

    # same left endpoint conflicts
    lastl = {}
    for i in range(1, M + 1):
        li = PL[i]
        prev = lastl.get(li, 0)
        if prev > g2[i]:
            g2[i] = prev
        lastl[li] = i
    # same right endpoint conflicts
    lastr = {}
    for i in range(1, M + 1):
        ri = PR[i]
        prev = lastr.get(ri, 0)
        if prev > g2[i]:
            g2[i] = prev
        lastr[ri] = i

    # segment tree for range-max-update / point-query with lazy versioning
    sz = 1
    while sz < N + 1:
        sz <<= 1
    tree = [-1] * (2 * sz)
    ver = [0] * (2 * sz)
    vc_box = [0]

    def process(ids, tree, ver, vc_box, sz):
        n = len(ids)
        if n < 2:
            return
        vc = vc_box[0]
        PLoc = PL
        PRoc = PR
        # positions 0..n-1 correspond to person ids (sorted by original index)
        segs_r = [[k] for k in range(n)]
        segs_l = [[k] for k in range(n)]

        while len(segs_r) > 1:
            m = len(segs_r)
            new_r = []
            new_l = []
            t = 0
            while t + 1 < m:
                Lr = segs_r[t]; Rr = segs_r[t + 1]
                Ll = segs_l[t]; Rl = segs_l[t + 1]

                # ---- Type 1: i<j, l_i < l_j < r_i < r_j ----
                vc += 1
                v = vc
                ptr = 0
                Lrlen = len(Lr)
                for j in Rr:
                    rj = PRoc[ids[j]]
                    while ptr < Lrlen and PRoc[ids[Lr[ptr]]] < rj:
                        ii = ids[Lr[ptr]]
                        a = PLoc[ii] + 1
                        b = PRoc[ii] - 1
                        if a <= b:
                            a += sz; b += sz
                            val = ii
                            while a <= b:
                                if a & 1:
                                    if ver[a] != v:
                                        ver[a] = v; tree[a] = val
                                    elif tree[a] < val:
                                        tree[a] = val
                                    a += 1
                                if not (b & 1):
                                    if ver[b] != v:
                                        ver[b] = v; tree[b] = val
                                    elif tree[b] < val:
                                        tree[b] = val
                                    b -= 1
                                a >>= 1; b >>= 1
                        ptr += 1
                    q = PLoc[ids[j]] + sz
                    res = -1
                    while q:
                        if ver[q] == v and tree[q] > res:
                            res = tree[q]
                        q >>= 1
                    if res > g2[ids[j]]:
                        g2[ids[j]] = res

                # ---- Type 2: i<j, l_j < l_i < r_j < r_i ----
                vc += 1
                v = vc
                ptr = len(Ll) - 1
                for j in reversed(Rl):
                    lj = PLoc[ids[j]]
                    while ptr >= 0 and PLoc[ids[Ll[ptr]]] > lj:
                        ii = ids[Ll[ptr]]
                        a = PLoc[ii] + 1
                        b = PRoc[ii] - 1
                        if a <= b:
                            a += sz; b += sz
                            val = ii
                            while a <= b:
                                if a & 1:
                                    if ver[a] != v:
                                        ver[a] = v; tree[a] = val
                                    elif tree[a] < val:
                                        tree[a] = val
                                    a += 1
                                if not (b & 1):
                                    if ver[b] != v:
                                        ver[b] = v; tree[b] = val
                                    elif tree[b] < val:
                                        tree[b] = val
                                    b -= 1
                                a >>= 1; b >>= 1
                        ptr -= 1
                    q = PRoc[ids[j]] + sz
                    res = -1
                    while q:
                        if ver[q] == v and tree[q] > res:
                            res = tree[q]
                        q >>= 1
                    if res > g2[ids[j]]:
                        g2[ids[j]] = res

                # merge sorted lists
                la = len(Lr); lb = len(Rr)
                mr = [0] * (la + lb)
                i1 = i2 = k = 0
                while i1 < la and i2 < lb:
                    if PRoc[ids[Lr[i1]]] <= PRoc[ids[Rr[i2]]]:
                        mr[k] = Lr[i1]; i1 += 1
                    else:
                        mr[k] = Rr[i2]; i2 += 1
                    k += 1
                while i1 < la:
                    mr[k] = Lr[i1]; i1 += 1; k += 1
                while i2 < lb:
                    mr[k] = Rr[i2]; i2 += 1; k += 1

                la = len(Ll); lb = len(Rl)
                ml = [0] * (la + lb)
                i1 = i2 = k = 0
                while i1 < la and i2 < lb:
                    if PLoc[ids[Ll[i1]]] <= PLoc[ids[Rl[i2]]]:
                        ml[k] = Ll[i1]; i1 += 1
                    else:
                        ml[k] = Rl[i2]; i2 += 1
                    k += 1
                while i1 < la:
                    ml[k] = Ll[i1]; i1 += 1; k += 1
                while i2 < lb:
                    ml[k] = Rl[i2]; i2 += 1; k += 1

                new_r.append(mr)
                new_l.append(ml)
                t += 2

            if m & 1:
                new_r.append(segs_r[-1])
                new_l.append(segs_l[-1])
            segs_r = new_r
            segs_l = new_l

        vc_box[0] = vc

    if plus:
        process(plus, tree, ver, vc_box, sz)
    if minus:
        process(minus, tree, ver, vc_box, sz)

    # prefix maximum of g2
    G = [0] * (M + 1)
    mx = 0
    for i in range(1, M + 1):
        if g2[i] > mx:
            mx = g2[i]
        G[i] = mx

    out = []
    for _ in range(Q):
        Lq = int(data[p]); Rq = int(data[p + 1]); p += 2
        if G[Rq] < Lq:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")

main()
import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q_pos = 1 + 2 * n
    q = int(data[q_pos])
    Xs = list(map(int, data[q_pos + 1: q_pos + 1 + q]))
    Ls = list(map(int, data[1:q_pos:2]))
    Rs = list(map(int, data[2:q_pos:2]))

    vals = sorted(set(Xs))
    M = len(vals)

    LOG = M.bit_length()
    size2 = 1 << LOG            # size2 > M always
    HALF = size2 >> 1
    INF = 1 << 50

    tree = [0] * (size2 + 2)
    prev = 0
    for k in range(M):
        v = vals[k]
        tree[k + 1] = v - prev
        prev = v
    # build fenwick over [1..M] in O(M)
    for i in range(1, M + 1):
        j = i + (i & -i)
        if j <= M:
            tree[j] += tree[i]
    for i in range(M + 1, size2 + 2):
        tree[i] = INF

    pows = [1 << k for k in range(LOG - 1, -1, -1)]

    glob = 0                    # global offset: V[p] = glob + prefix(p)
    vmin = vals[0]
    vmax = vals[-1]

    for L, R in zip(Ls, Rs):
        if R < vmin or L > vmax:
            continue
        if L <= vmin:
            if R >= vmax:
                glob += 1
                vmin += 1
                vmax += 1
                continue
            # i = 1 ; find j = last index with V <= R
            pos = 0
            rem = R - glob
            for pw in pows:
                t = tree[pos + pw]
                if t <= rem:
                    pos += pw
                    rem -= t
            j = pos
            glob += 1
            vmin += 1
            p = j + 1
            while p <= M:
                tree[p] -= 1
                p += p & -p
            continue
        if R >= vmax:
            # j = M ; find i = first index with V >= L
            pos = 0
            rem = L - 1 - glob
            for pw in pows:
                t = tree[pos + pw]
                if t <= rem:
                    pos += pw
                    rem -= t
            i = pos + 1
            vmax += 1
            p = i
            while p <= M:
                tree[p] += 1
                p += p & -p
            continue
        # fused descent (shared prefix), both boundaries strictly inside
        pos = 0
        r1 = L - 1 - glob
        r2 = R - glob
        pw = HALF
        while pw:
            t = tree[pos + pw]
            if t <= r1:
                pos += pw
                r1 -= t
                r2 -= t
            elif t <= r2:
                break
            pw >>= 1
        if not pw:
            continue            # empty range
        p1 = pos
        p2 = pos + pw
        r2 -= t
        w = pw >> 1
        while w:
            t = tree[p1 + w]
            if t <= r1:
                p1 += w
                r1 -= t
            w >>= 1
        w = pw >> 1
        while w:
            t = tree[p2 + w]
            if t <= r2:
                p2 += w
                r2 -= t
            w >>= 1
        p = p1 + 1
        while p <= M:
            tree[p] += 1
            p += p & -p
        p = p2 + 1
        while p <= M:
            tree[p] -= 1
            p += p & -p

    # invert fenwick to recover difference array
    for i in range(M, 0, -1):
        j = i + (i & -i)
        if j <= M:
            tree[j] -= tree[i]

    fin = {}
    s = glob
    for k in range(M):
        s += tree[k + 1]
        fin[vals[k]] = s

    sys.stdout.write('\n'.join([str(fin[x]) for x in Xs]))
    sys.stdout.write('\n')

main()
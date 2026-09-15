import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    N = data[0]; M = data[1]; Q = data[2]
    a = [0] * (M + 1)
    b = [0] * (M + 1)
    sg = [0] * (M + 1)
    p = 3
    for i in range(1, M + 1):
        s = data[p]; t = data[p + 1]; p += 2
        if s < t:
            a[i] = s; b[i] = t; sg[i] = 1
        else:
            a[i] = t; b[i] = s; sg[i] = 0

    INF = 1 << 62
    K = M + 1

    def cross_next(a, b, sg, M, N):
        # nxt[i] = min j>i with same sign and a_i<a_j<b_i<b_j
        size = 1
        while size < N:
            size <<= 1
        T = size << 1
        tree1 = [INF] * T
        tree0 = [INF] * T
        hps1 = [None] * (N + 1)
        hps0 = [None] * (N + 1)
        nxt = [INF] * (M + 2)
        removed = bytearray(M + 1)
        heappush = heapq.heappush
        heappop = heapq.heappop
        for j in range(1, M + 1):
            aj = a[j]; bj = b[j]
            if sg[j]:
                tree = tree1; hps = hps1
            else:
                tree = tree0; hps = hps0
            th = aj * K
            l = aj + size
            r = bj + size - 2
            while True:
                mp = INF
                ll = l; rr = r
                while ll <= rr:
                    if ll & 1:
                        v = tree[ll]
                        if v < mp: mp = v
                        ll += 1
                    if not (rr & 1):
                        v = tree[rr]
                        if v < mp: mp = v
                        rr -= 1
                    ll >>= 1; rr >>= 1
                if mp >= th:
                    break
                i = mp % K
                nxt[i] = j
                removed[i] = 1
                hp = hps[b[i]]
                while hp and removed[hp[0] % K]:
                    heappop(hp)
                val = hp[0] if hp else INF
                pos = b[i] + size - 1
                tree[pos] = val
                pos >>= 1
                while pos:
                    x = tree[pos + pos]; y = tree[pos + pos + 1]
                    nv = x if x < y else y
                    if tree[pos] == nv:
                        break
                    tree[pos] = nv
                    pos >>= 1
            hp = hps[bj]
            if hp is None:
                hp = []
                hps[bj] = hp
            heappush(hp, aj * K + j)
            val = hp[0]
            pos = bj + size - 1
            if tree[pos] != val:
                tree[pos] = val
                pos >>= 1
                while pos:
                    x = tree[pos + pos]; y = tree[pos + pos + 1]
                    nv = x if x < y else y
                    if tree[pos] == nv:
                        break
                    tree[pos] = nv
                    pos >>= 1
        return nxt

    # same a / same b (any sign conflict)
    last_a = [INF] * (N + 2)
    last_b = [INF] * (N + 2)
    next_same = [INF] * (M + 2)
    for i in range(M, 0, -1):
        ai = a[i]; bi = b[i]
        la = last_a[ai]; lb = last_b[bi]
        next_same[i] = la if la < lb else lb
        last_a[ai] = i; last_b[bi] = i

    nxt1 = cross_next(a, b, sg, M, N)          # a_i<a_j<b_i<b_j

    a2 = [0] * (M + 1)
    b2 = [0] * (M + 1)
    for i in range(1, M + 1):
        a2[i] = N + 1 - b[i]
        b2[i] = N + 1 - a[i]
    nxt2 = cross_next(a2, b2, sg, M, N)        # a_j<a_i<b_j<b_i

    boundary = [INF] * (M + 2)
    for i in range(M, 0, -1):
        v = next_same[i]
        w = nxt1[i]
        if w < v: v = w
        w = nxt2[i]
        if w < v: v = w
        w = boundary[i + 1]
        if w < v: v = w
        boundary[i] = v

    out = []
    for _ in range(Q):
        L = data[p]; R = data[p + 1]; p += 2
        out.append("Yes" if boundary[L] > R else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
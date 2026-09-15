import sys
from heapq import heappush, heappop


def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    M = int(data[ptr]); ptr += 1
    Q = int(data[ptr]); ptr += 1

    l = [0] * M
    r = [0] * M
    poss = []
    negs = []
    for i in range(M):
        s = int(data[ptr]); ptr += 1
        t = int(data[ptr]); ptr += 1
        if s < t:
            l[i] = s - 1
            r[i] = t - 1
            poss.append(i)
        else:
            l[i] = t - 1
            r[i] = s - 1
            negs.append(i)

    INF_I = M  # sentinel larger than any valid index
    nextA = [INF_I] * M
    nextB = [INF_I] * M

    size = 1
    while size < N:
        size <<= 1

    def process(indices):
        INF_C = 1 << 30
        treeA = [INF_C] * (2 * size)   # keyed by r, stores min l
        heapsA = {}
        treeB = [-1] * (2 * size)      # keyed by l, stores max r
        heapsB = {}

        for j in indices:
            lj = l[j]
            rj = r[j]
            ql = lj + 1
            qr = rj - 1
            if ql <= qr:
                # ---- structure A: earlier i with r_i in (lj,rj), l_i < lj
                x = ql + size
                y = qr + size + 1
                nodes = []
                while x < y:
                    if x & 1:
                        nodes.append(x); x += 1
                    if y & 1:
                        y -= 1; nodes.append(y)
                    x >>= 1; y >>= 1
                for c in nodes:
                    if treeA[c] >= lj:
                        continue
                    st = [c]
                    while st:
                        node = st.pop()
                        if treeA[node] >= lj:
                            continue
                        if node >= size:
                            h = heapsA.get(node - size)
                            if h is not None:
                                while h and h[0][0] < lj:
                                    _, idx = heappop(h)
                                    nextA[idx] = j
                                treeA[node] = h[0][0] if h else INF_C
                            else:
                                treeA[node] = INF_C
                            p = node >> 1
                            while p:
                                a = treeA[p << 1]; b = treeA[p << 1 | 1]
                                treeA[p] = a if a < b else b
                                p >>= 1
                        else:
                            st.append(node << 1)
                            st.append(node << 1 | 1)

                # ---- structure B: earlier i with l_i in (lj,rj), r_i > rj
                x = ql + size
                y = qr + size + 1
                nodes = []
                while x < y:
                    if x & 1:
                        nodes.append(x); x += 1
                    if y & 1:
                        y -= 1; nodes.append(y)
                    x >>= 1; y >>= 1
                for c in nodes:
                    if treeB[c] <= rj:
                        continue
                    st = [c]
                    while st:
                        node = st.pop()
                        if treeB[node] <= rj:
                            continue
                        if node >= size:
                            h = heapsB.get(node - size)
                            if h is not None:
                                while h and -h[0][0] > rj:
                                    _, idx = heappop(h)
                                    nextB[idx] = j
                                treeB[node] = -h[0][0] if h else -1
                            else:
                                treeB[node] = -1
                            p = node >> 1
                            while p:
                                a = treeB[p << 1]; b = treeB[p << 1 | 1]
                                treeB[p] = a if a > b else b
                                p >>= 1
                        else:
                            st.append(node << 1)
                            st.append(node << 1 | 1)

            # insert j into structure A (key rj, value lj)
            h = heapsA.get(rj)
            if h is None:
                heapsA[rj] = [(lj, j)]
            else:
                heappush(h, (lj, j))
            p = rj + size
            if lj < treeA[p]:
                treeA[p] = lj
                p >>= 1
                while p:
                    a = treeA[p << 1]; b = treeA[p << 1 | 1]
                    treeA[p] = a if a < b else b
                    p >>= 1

            # insert j into structure B (key lj, value -rj)
            h = heapsB.get(lj)
            if h is None:
                heapsB[lj] = [(-rj, j)]
            else:
                heappush(h, (-rj, j))
            p = lj + size
            if rj > treeB[p]:
                treeB[p] = rj
                p >>= 1
                while p:
                    a = treeB[p << 1]; b = treeB[p << 1 | 1]
                    treeB[p] = a if a > b else b
                    p >>= 1

    if poss:
        process(poss)
    if negs:
        process(negs)

    # same-left / same-right conflicts
    next_end = [INF_I] * M
    dl = {}
    dr = {}
    for i in range(M - 1, -1, -1):
        best = INF_I
        li = l[i]
        ri = r[i]
        v = dl.get(li)
        if v is not None and v < best:
            best = v
        v = dr.get(ri)
        if v is not None and v < best:
            best = v
        next_end[i] = best
        dl[li] = i
        dr[ri] = i

    nc = [0] * M
    for i in range(M):
        a = nextA[i]; b = nextB[i]; c = next_end[i]
        m = a if a < b else b
        if c < m:
            m = c
        nc[i] = m

    # range-min segment tree over nc
    s2 = 1
    while s2 < M:
        s2 <<= 1
    seg = [INF_I] * (2 * s2)
    for i in range(M):
        seg[s2 + i] = nc[i]
    for i in range(s2 - 1, 0, -1):
        a = seg[i << 1]; b = seg[i << 1 | 1]
        seg[i] = a if a < b else b

    out = []
    for _ in range(Q):
        L = int(data[ptr]); ptr += 1
        R = int(data[ptr]); ptr += 1
        lo = L - 1
        hi = R - 1
        res = INF_I
        x = lo + s2
        y = hi + s2 + 1
        while x < y:
            if x & 1:
                if seg[x] < res:
                    res = seg[x]
                x += 1
            if y & 1:
                y -= 1
                if seg[y] < res:
                    res = seg[y]
            x >>= 1; y >>= 1
        out.append("No" if res <= hi else "Yes")

    sys.stdout.write("\n".join(out))
    sys.stdout.write("\n")


main()
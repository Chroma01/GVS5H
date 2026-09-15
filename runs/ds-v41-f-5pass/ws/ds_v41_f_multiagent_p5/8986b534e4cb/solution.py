import sys
from bisect import bisect_left, bisect_right
from heapq import heappush, heappop

INF = 1 << 60


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Q = int(next(it))

    Ls = [0] * (M + 1)
    Rs = [0] * (M + 1)
    idx0 = []  # S < T  (up)
    idx1 = []  # S > T  (down)

    for i in range(1, M + 1):
        s = int(next(it))
        t = int(next(it))
        if s < t:
            Ls[i] = s
            Rs[i] = t
            idx0.append(i)
        else:
            Ls[i] = t
            Rs[i] = s
            idx1.append(i)

    qL = [0] * Q
    qR = [0] * Q
    for k in range(Q):
        qL[k] = int(next(it))
        qR[k] = int(next(it))

    BIG = M + 1

    # same left endpoint conflicts
    nsl = [INF] * (M + 1)
    nsr = [INF] * (M + 1)
    lastL = {}
    lastR = {}
    for i in range(1, M + 1):
        l = Ls[i]
        prev = lastL.get(l)
        if prev is not None:
            nsl[prev] = i
        lastL[l] = i

        r = Rs[i]
        prev = lastR.get(r)
        if prev is not None:
            nsr[prev] = i
        lastR[r] = i

    crossed = [INF] * (M + 1)

    push = heappush
    pop = heappop
    bl = bisect_left
    br = bisect_right

    for idxs in (idx0, idx1):
        n = len(idxs)
        if n < 2:
            continue

        rvals = sorted(set(Rs[i] for i in idxs))
        lvals = sorted(set(Ls[i] for i in idxs))
        rmap = {v: k for k, v in enumerate(rvals)}
        lmap = {v: k for k, v in enumerate(lvals)}

        nr = len(rvals)
        nl = len(lvals)
        sizeA = 1
        while sizeA < nr:
            sizeA <<= 1
        sizeB = 1
        while sizeB < nl:
            sizeB <<= 1

        segA = [INF] * (2 * sizeA)
        segB = [0] * (2 * sizeB)
        heapA = [None] * sizeA
        heapB = [None] * sizeB
        deleted = bytearray(M + 1)
        leafA_of = [0] * (M + 1)
        leafB_of = [0] * (M + 1)

        for i in idxs:
            leafA_of[i] = rmap[Rs[i]]
            leafB_of[i] = lmap[Ls[i]]

        for j in idxs:
            lj = Ls[j]
            rj = Rs[j]

            # region A: l_i < l_j < r_i < r_j
            lo = br(rvals, lj)
            hi = bl(rvals, rj) - 1
            th = lj * BIG
            while lo <= hi:
                x = lo + sizeA
                y = hi + 1 + sizeA
                node = -1
                while x < y:
                    if x & 1:
                        if segA[x] < th:
                            node = x
                            break
                        x += 1
                    if y & 1:
                        y -= 1
                        if segA[y] < th:
                            node = y
                            break
                    x >>= 1
                    y >>= 1
                if node < 0:
                    break
                while node < sizeA:
                    lc = node << 1
                    node = lc if segA[lc] < th else lc + 1
                leaf = node - sizeA
                h = heapA[leaf]
                i = h[0] % BIG
                if j < crossed[i]:
                    crossed[i] = j
                deleted[i] = 1
                while h and deleted[h[0] % BIG]:
                    pop(h)
                nv = h[0] if h else INF
                p = sizeA + leaf
                segA[p] = nv
                p >>= 1
                while p:
                    a = segA[p << 1]
                    b = segA[(p << 1) | 1]
                    nvv = a if a < b else b
                    if segA[p] == nvv:
                        break
                    segA[p] = nvv
                    p >>= 1

                lb = leafB_of[i]
                h2 = heapB[lb]
                while h2 and deleted[(-h2[0]) % BIG]:
                    pop(h2)
                nv2 = (-h2[0]) if h2 else 0
                p = sizeB + lb
                segB[p] = nv2
                p >>= 1
                while p:
                    a = segB[p << 1]
                    b = segB[(p << 1) | 1]
                    nvv = a if a > b else b
                    if segB[p] == nvv:
                        break
                    segB[p] = nvv
                    p >>= 1

            # region B: l_j < l_i < r_j < r_i
            lo = br(lvals, lj)
            hi = bl(lvals, rj) - 1
            th2 = (rj + 1) * BIG
            while lo <= hi:
                x = lo + sizeB
                y = hi + 1 + sizeB
                node = -1
                while x < y:
                    if x & 1:
                        if segB[x] >= th2:
                            node = x
                            break
                        x += 1
                    if y & 1:
                        y -= 1
                        if segB[y] >= th2:
                            node = y
                            break
                    x >>= 1
                    y >>= 1
                if node < 0:
                    break
                while node < sizeB:
                    lc = node << 1
                    node = lc if segB[lc] >= th2 else lc + 1
                leaf = node - sizeB
                h = heapB[leaf]
                i = (-h[0]) % BIG
                if j < crossed[i]:
                    crossed[i] = j
                deleted[i] = 1
                while h and deleted[(-h[0]) % BIG]:
                    pop(h)
                nv2 = (-h[0]) if h else 0
                p = sizeB + leaf
                segB[p] = nv2
                p >>= 1
                while p:
                    a = segB[p << 1]
                    b = segB[(p << 1) | 1]
                    nvv = a if a > b else b
                    if segB[p] == nvv:
                        break
                    segB[p] = nvv
                    p >>= 1

                la = leafA_of[i]
                hA = heapA[la]
                while hA and deleted[hA[0] % BIG]:
                    pop(hA)
                nv = hA[0] if hA else INF
                p = sizeA + la
                segA[p] = nv
                p >>= 1
                while p:
                    a = segA[p << 1]
                    b = segA[(p << 1) | 1]
                    nvv = a if a < b else b
                    if segA[p] == nvv:
                        break
                    segA[p] = nvv
                    p >>= 1

            # insert j into A
            la = leafA_of[j]
            hA = heapA[la]
            if hA is None:
                hA = []
                heapA[la] = hA
            push(hA, lj * BIG + j)
            nv = hA[0]
            p = sizeA + la
            segA[p] = nv
            p >>= 1
            while p:
                a = segA[p << 1]
                b = segA[(p << 1) | 1]
                nvv = a if a < b else b
                if segA[p] == nvv:
                    break
                segA[p] = nvv
                p >>= 1

            # insert j into B
            lb = leafB_of[j]
            hB = heapB[lb]
            if hB is None:
                hB = []
                heapB[lb] = hB
            push(hB, -(rj * BIG + j))
            nv = -hB[0]
            p = sizeB + lb
            segB[p] = nv
            p >>= 1
            while p:
                a = segB[p << 1]
                b = segB[(p << 1) | 1]
                nvv = a if a > b else b
                if segB[p] == nvv:
                    break
                segB[p] = nvv
                p >>= 1

    nc = [INF] * (M + 1)
    for i in range(1, M + 1):
        v = nsl[i]
        if nsr[i] < v:
            v = nsr[i]
        if crossed[i] < v:
            v = crossed[i]
        nc[i] = v

    suf = [INF] * (M + 2)
    for i in range(M, 0, -1):
        v = nc[i]
        if suf[i + 1] < v:
            v = suf[i + 1]
        suf[i] = v

    out = []
    for k in range(Q):
        out.append("Yes" if suf[qL[k]] > qR[k] else "No")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()
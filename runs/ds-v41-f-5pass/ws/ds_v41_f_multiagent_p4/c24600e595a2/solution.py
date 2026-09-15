import sys


def solve(n, A, B, C):
    D = []
    U = []
    E = []
    for i in range(n):
        if A[i]:
            if B[i]:
                E.append(C[i])
            else:
                D.append(C[i])
        elif B[i]:
            U.append(C[i])

    allc = D + U + E
    vals = sorted(set(allc))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)

    cntR = [0] * (m + 1)
    sumR = [0] * (m + 1)
    cntS = [0] * (m + 1)
    sumS = [0] * (m + 1)

    totalR = 0
    totalS = 0
    costR = 0
    costS = 0

    # Build removal set R = D
    for c in D:
        j = comp[c]
        cl = sl = 0
        i = j - 1
        while i > 0:
            cl += cntR[i]
            sl += sumR[i]
            i -= i & (-i)
        costR += c * (totalR - cl) + sl
        i = j
        while i <= m:
            cntR[i] += 1
            sumR[i] += c
            i += i & (-i)
        totalR += 1

    # Build addition set S = U
    for c in U:
        j = comp[c]
        cle = sle = 0
        i = j
        while i > 0:
            cle += cntS[i]
            sle += sumS[i]
            i -= i & (-i)
        costS += c * (totalS - cle + 1) + sle
        i = j
        while i <= m:
            cntS[i] += 1
            sumS[i] += c
            i += i & (-i)
        totalS += 1

    M = len(D) + len(U)
    Esum = sum(E)
    best = costR + costS + M * Esum

    E.sort(reverse=True)
    for c in E:
        j = comp[c]
        # insert c into R (removal pair-cost delta)
        cl = sl = 0
        i = j - 1
        while i > 0:
            cl += cntR[i]
            sl += sumR[i]
            i -= i & (-i)
        costR += c * (totalR - cl) + sl
        i = j
        while i <= m:
            cntR[i] += 1
            sumR[i] += c
            i += i & (-i)
        totalR += 1

        # insert c into S (addition cost delta incl. own C term)
        cle = sle = 0
        i = j
        while i > 0:
            cle += cntS[i]
            sle += sumS[i]
            i -= i & (-i)
        costS += c * (totalS - cle + 1) + sle
        i = j
        while i <= m:
            cntS[i] += 1
            sumS[i] += c
            i += i & (-i)
        totalS += 1

        M += 2
        Esum -= c
        t = costR + costS + M * Esum
        if t < best:
            best = t

    return best


def brute(A, B, C):
    """Exact shortest-path over all flip sequences (state = bitmask of 1s)."""
    import heapq
    n = len(A)
    start = 0
    target = 0
    for i in range(n):
        if A[i]:
            start |= 1 << i
        if B[i]:
            target |= 1 << i
    INF = float("inf")
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist.get(s, INF):
            continue
        if s == target:
            return d
        for i in range(n):
            ns = s ^ (1 << i)
            w = 0
            for j in range(n):
                if (ns >> j) & 1:
                    w += C[j]
            nd = d + w
            if nd < dist.get(ns, INF):
                dist[ns] = nd
                heapq.heappush(pq, (nd, ns))
    return dist.get(target, 0)


def verify():
    import random
    random.seed(20240607)
    for _ in range(5000):
        n = random.randint(1, 7)
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        if random.random() < 0.6:
            C = [random.randint(1, 4) for _ in range(n)]   # many ties
        else:
            C = [random.randint(1, 12) for _ in range(n)]
        e = brute(A, B, C)
        g = solve(n, A, B, C)
        if e != g:
            print("MISMATCH", n, A, B, C, "expected", e, "got", g)
            return
    print("all ok")


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [1 if x == b'1' else 0 for x in data[1:1 + n]]
    B = [1 if x == b'1' else 0 for x in data[1 + n:1 + 2 * n]]
    C = [int(x) for x in data[1 + 2 * n:1 + 3 * n]]
    sys.stdout.write(str(solve(n, A, B, C)) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify()
    else:
        main()
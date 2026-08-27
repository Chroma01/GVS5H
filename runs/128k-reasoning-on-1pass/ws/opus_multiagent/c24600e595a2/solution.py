import sys
from bisect import bisect_left
from itertools import accumulate


def solve(n, A, B, C):
    """Closed-form O(N log N) solution."""
    P = []   # A=1, B=0  -> exactly one 'off' flip
    Q = []   # A=0, B=1  -> exactly one 'on' flip
    R = []   # A=1, B=1  -> optionally an 'off' then 'on' pair
    for a, b, c in zip(A, B, C):
        if a:
            if b:
                R.append(c)
            else:
                P.append(c)
        elif b:
            Q.append(c)
        # A=B=0 : never touched

    P.sort()
    Q.sort()
    R.sort(reverse=True)

    nP = len(P)
    nQ = len(Q)
    nR = len(R)

    prefP = [0] + list(accumulate(P))
    prefQ = [0] + list(accumulate(Q))
    SumQ = prefQ[nQ]
    SumR = sum(R)

    # mp(X) = sum over unordered pairs of min(x,y)
    mpP = 0
    for i, x in enumerate(P):
        mpP += x * (nP - 1 - i)
    mpQ = 0
    for i, x in enumerate(Q):
        mpQ += x * (nQ - 1 - i)

    sumT = 0
    m = nP + nQ
    best = m * SumR + mpP + mpQ + SumQ          # t = 0

    for t in range(1, nR + 1):
        c = R[t - 1]                            # descending, so c <= all added before
        i = bisect_left(P, c)
        mpP += prefP[i] + c * (nP - i) + c * (t - 1)
        j = bisect_left(Q, c)
        mpQ += prefQ[j] + c * (nQ - j) + c * (t - 1)
        sumT += c
        m = nP + nQ + 2 * t
        cost = m * (SumR - sumT) + mpP + mpQ + SumQ + sumT
        if cost < best:
            best = cost

    return best


# ----------------------------------------------------------------------
# self test (only when run with the argument 'selftest'); never touched
# during normal judging, which just reads stdin.
# ----------------------------------------------------------------------
def _brute(n, A, B, C):
    import heapq
    start = 0
    goal = 0
    for k in range(n):
        if A[k]:
            start |= 1 << k
        if B[k]:
            goal |= 1 << k
    w = [0] * (1 << n)
    for s in range(1 << n):
        t = 0
        for k in range(n):
            if s >> k & 1:
                t += C[k]
        w[s] = t
    INF = float('inf')
    dist = [INF] * (1 << n)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist[s]:
            continue
        if s == goal:
            return d
        for k in range(n):
            ns = s ^ (1 << k)
            nd = d + w[ns]
            if nd < dist[ns]:
                dist[ns] = nd
                heapq.heappush(pq, (nd, ns))
    return dist[goal]


def _selftest():
    import random
    # samples
    samples = [
        (4, [0, 1, 1, 1], [1, 0, 1, 0], [4, 6, 2, 9], 16),
        (5, [1] * 5, [1] * 5, [1] * 5, 0),
        (20,
         [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
         [52, 73, 97, 72, 54, 15, 79, 67, 13, 55, 65, 22, 36, 90, 84, 46, 1, 2, 27, 8],
         2867),
    ]
    for n, A, B, C, exp in samples:
        got = solve(n, A, B, C)
        assert got == exp, ("sample fail", n, A, B, C, got, exp)
    random.seed(12345)
    for it in range(400):
        n = random.randint(1, 8)
        mode = it % 6
        A = [random.randint(0, 1) for _ in range(n)]
        if mode == 1:
            B = A[:]                       # A == B
        elif mode == 2:
            B = [1 - x for x in A]         # R empty, and one of P/Q by structure
        elif mode == 3:
            A = [0] * n
            B = [random.randint(0, 1) for _ in range(n)]   # P, R empty
        elif mode == 4:
            A = [1] * n
            B = [random.randint(0, 1) for _ in range(n)]   # Q empty
        else:
            B = [random.randint(0, 1) for _ in range(n)]
        if mode == 5:
            v = random.randint(1, 5)
            C = [v] * n                    # all equal C
        else:
            C = [random.randint(1, 5) for _ in range(n)]
        f = solve(n, A, B, C)
        b = _brute(n, A, B, C)
        if f != b:
            print("MISMATCH", n, A, B, C, "fast", f, "brute", b)
            return
    print("all tests passed")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        _selftest()
        return
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    B = list(map(int, data[1 + n:1 + 2 * n]))
    C = list(map(int, data[1 + 2 * n:1 + 3 * n]))
    sys.stdout.write(str(solve(n, A, B, C)) + "\n")


main()
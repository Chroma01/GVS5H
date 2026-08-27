import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    pos = [[] for _ in range(n + 2)]
    for i, a in enumerate(A, start=1):
        pos[a].append(i)

    def contain(P):
        # number of subarrays containing at least one position from P
        total = 0
        prev = 0
        for p in P:
            total += (p - prev) * (n - p + 1)
            prev = p
        return total

    def both(P, Q):
        # number of subarrays containing at least one position from P and one from Q
        if not P or not Q:
            return 0
        i = j = 0
        lp = len(P)
        lq = len(Q)
        total = 0
        L = 1
        while L <= n:
            while i < lp and P[i] < L:
                i += 1
            while j < lq and Q[j] < L:
                j += 1
            if i == lp or j == lq:
                break
            m = P[i] if P[i] > Q[j] else Q[j]
            # addend (n - m + 1) stays constant for L in [L, min(P[i], Q[j])]
            nxt = (P[i] if P[i] < Q[j] else Q[j]) + 1
            total += (nxt - L) * (n - m + 1)
            L = nxt
        return total

    ans = 0
    for v in range(1, n + 1):
        P = pos[v]
        if not P:
            continue
        ans += contain(P) - both(P, pos[v - 1])
    print(ans)

solve()
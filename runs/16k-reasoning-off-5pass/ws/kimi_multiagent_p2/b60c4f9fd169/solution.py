import sys


def solve():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = bytes(data[1])
    T = bytes(data[2])
    N, M = len(S), len(T)

    out = sys.stdout.write

    if abs(N - M) > K:
        out("No\n")
        return

    def lce(x, y):
        # Longest common prefix length of S[x:] and T[y:] via binary search
        # on bytes slices (C-speed memcpy + memcmp).
        lo = 0
        hi = min(N - x, M - y)
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if S[x:x + mid] == T[y:y + mid]:
                lo = mid
            else:
                hi = mid - 1
        return lo

    # Myers O(ND) greedy furthest-reaching algorithm, capped at d = K.
    # V[k] = furthest x reachable on diagonal k (y = x - k) with d edits.
    NEG = -10 ** 18

    # d = 0: single snake along diagonal 0.
    x = lce(0, 0)
    if x >= N and x >= M:  # y = x - 0 = x, so this means (N, M) reached
        out("Yes\n")
        return
    V = {0: x}

    for d in range(1, K + 1):
        newV = {}
        get = V.get
        for k in range(-d, d + 1, 2):
            # Predecessors: diagonal k+1 via insertion (x unchanged),
            # diagonal k-1 via deletion (x + 1).
            if k == -d:
                x = get(k + 1, NEG)
            elif k == d:
                x = get(k - 1, NEG) + 1
            else:
                a = get(k - 1, NEG) + 1
                b = get(k + 1, NEG)
                x = a if a > b else b
            if x < 0:
                x = 0
            elif x > N:
                x = N
            y = x - k
            if 0 <= y <= M:
                if x < N and y < M:
                    x += lce(x, y)
                newV[k] = x
                if x >= N and y >= M:
                    out("Yes\n")
                    return
            else:
                newV[k] = NEG  # off-grid diagonal; keep it unusable
        V = newV

    out("No\n")


solve()
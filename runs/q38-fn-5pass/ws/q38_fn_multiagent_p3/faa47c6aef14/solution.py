import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1] - 1
    idx = 2

    A = data[idx:idx + N]
    idx += N
    B = data[idx:idx + N]
    idx += N
    P = [x - 1 for x in data[idx:idx + N]]
    idx += N
    Q = [x - 1 for x in data[idx:idx + N]]
    del data

    def get_required(perm, balls):
        cycle = []
        cur = X
        while True:
            cycle.append(cur)
            cur = perm[cur]
            if cur == X:
                break

        in_cycle = bytearray(N)
        for v in cycle:
            in_cycle[v] = 1

        for i, val in enumerate(balls):
            if val and not in_cycle[i]:
                return None

        L = len(cycle)
        start = -1
        for j in range(1, L):
            if balls[cycle[j]]:
                start = j
                break

        if start == -1:
            return []
        return cycle[start:]

    red_req = get_required(P, A)
    if red_req is None:
        print(-1)
        return

    blue_req = get_required(Q, B)
    if blue_req is None:
        print(-1)
        return

    if not red_req or not blue_req:
        print(len(red_req) + len(blue_req))
        return

    del A, B, P, Q

    # LCS of two sequences with distinct elements.
    # Map the longer sequence to positions, then LIS on the shorter one.
    if len(red_req) >= len(blue_req):
        s1, s2 = red_req, blue_req
    else:
        s1, s2 = blue_req, red_req

    pos = [-1] * N
    for i, v in enumerate(s1):
        pos[v] = i

    tails = []
    for v in s2:
        p = pos[v]
        if p != -1:
            k = bisect_left(tails, p)
            if k == len(tails):
                tails.append(p)
            else:
                tails[k] = p

    lcs = len(tails)
    print(len(red_req) + len(blue_req) - lcs)


if __name__ == "__main__":
    solve()
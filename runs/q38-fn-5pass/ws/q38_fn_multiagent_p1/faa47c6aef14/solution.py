import sys
from bisect import bisect_left


def build_path(perm, balls, x, n):
    in_cycle = bytearray(n + 1)
    in_cycle[x] = 1

    cycle = []
    cur = perm[x]
    while cur != x:
        cycle.append(cur)
        in_cycle[cur] = 1
        cur = perm[cur]

    for i in range(1, n + 1):
        if balls[i] and not in_cycle[i]:
            return None

    start = -1
    for i, v in enumerate(cycle):
        if balls[v]:
            start = i
            break

    if start == -1:
        return []
    if start == 0:
        return cycle
    return cycle[start:]


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    idx = 2

    A = [0] + data[idx:idx + n]
    idx += n
    B = [0] + data[idx:idx + n]
    idx += n
    P = [0] + data[idx:idx + n]
    idx += n
    Q = [0] + data[idx:idx + n]
    del data

    red = build_path(P, A, x, n)
    if red is None:
        print(-1)
        return

    blue = build_path(Q, B, x, n)
    if blue is None:
        print(-1)
        return

    if not red:
        print(len(blue))
        return
    if not blue:
        print(len(red))
        return

    pos = [-1] * (n + 1)
    for i, v in enumerate(red):
        pos[v] = i

    tails = []
    bl = bisect_left
    for v in blue:
        p = pos[v]
        if p != -1:
            j = bl(tails, p)
            if j == len(tails):
                tails.append(p)
            else:
                tails[j] = p

    print(len(red) + len(blue) - len(tails))


if __name__ == "__main__":
    solve()
import sys
from bisect import bisect_left


def make_route(n, x, perm, balls):
    inv = [0] * n
    for i, to in enumerate(perm):
        inv[to] = i

    dist = [-1] * n
    dist[x] = 0
    near_to_far = []

    cur = x
    d = 0
    while True:
        cur = inv[cur]
        if cur == x:
            break
        d += 1
        dist[cur] = d
        near_to_far.append(cur)

    farthest = 0
    for i, value in enumerate(balls):
        if value:
            if dist[i] == -1:
                return None
            if dist[i] > farthest:
                farthest = dist[i]

    # Operations for this color must be done from farthest toward X.
    return near_to_far[farthest - 1::-1] if farthest else []


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    red_route = make_route(n, x, p, a)
    blue_route = make_route(n, x, q, b)

    if red_route is None or blue_route is None:
        print(-1)
        return

    pos_in_red = {v: i for i, v in enumerate(red_route)}

    # LCS of two sequences with distinct elements is LIS of positions.
    lis = []
    for v in blue_route:
        if v in pos_in_red:
            value = pos_in_red[v]
            idx = bisect_left(lis, value)
            if idx == len(lis):
                lis.append(value)
            else:
                lis[idx] = value

    lcs = len(lis)
    print(len(red_route) + len(blue_route) - lcs)


if __name__ == "__main__":
    main()
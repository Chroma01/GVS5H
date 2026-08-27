import sys
from bisect import bisect_left


def required_route(perm, occupied, target):
    n = len(perm)
    cycle = []
    pos = [-1] * n

    v = target
    while pos[v] == -1:
        pos[v] = len(cycle)
        cycle.append(v)
        v = perm[v]

    first = n
    for i, has_ball in enumerate(occupied):
        if has_ball:
            if pos[i] == -1:
                return None
            if pos[i] > 0:
                first = min(first, pos[i])

    if first == n:
        return []

    return cycle[len(cycle) - 1:first - 1:-1]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    red_route = required_route(p, a, x)
    if red_route is None:
        print(-1)
        return

    blue_route = required_route(q, b, x)
    if blue_route is None:
        print(-1)
        return

    positions = {v: i for i, v in enumerate(red_route)}
    sequence = [positions[v] for v in blue_route if v in positions]

    lis = []
    for v in sequence:
        i = bisect_left(lis, v)
        if i == len(lis):
            lis.append(v)
        else:
            lis[i] = v

    lcs = len(lis)
    print(len(red_route) + len(blue_route) - lcs)


if __name__ == "__main__":
    main()
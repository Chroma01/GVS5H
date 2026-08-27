import sys
from bisect import bisect_left


def build_required_sequence(perm, balls, x, n):
    cycle = []
    cur = x
    while True:
        cycle.append(cur)
        cur = perm[cur]
        if cur == x:
            break

    pos = [-1] * n
    for i, v in enumerate(cycle):
        pos[v] = i

    first = len(cycle)
    for i, has_ball in enumerate(balls):
        if has_ball:
            if pos[i] == -1:
                return None
            if pos[i] != 0:
                first = min(first, pos[i])

    if first == len(cycle):
        return []

    return cycle[first:]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    red = build_required_sequence(p, a, x, n)
    if red is None:
        print(-1)
        return

    blue = build_required_sequence(q, b, x, n)
    if blue is None:
        print(-1)
        return

    blue_pos = [-1] * n
    for i, v in enumerate(blue):
        blue_pos[v] = i

    tails = []
    for v in red:
        z = blue_pos[v]
        if z != -1:
            k = bisect_left(tails, z)
            if k == len(tails):
                tails.append(z)
            else:
                tails[k] = z

    lcs = len(tails)
    print(len(red) + len(blue) - lcs)


if __name__ == "__main__":
    main()
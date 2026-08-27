import sys
from bisect import bisect_left


def required_sequence(n, x, balls, perm):
    inv = [0] * n
    for i, to in enumerate(perm):
        inv[to] = i

    # back[k] is the k+1-th vertex before X on the permutation cycle.
    back = []
    in_cycle = [False] * n
    in_cycle[x] = True

    v = inv[x]
    while v != x:
        back.append(v)
        in_cycle[v] = True
        v = inv[v]

    farthest = -1
    for i, value in enumerate(balls):
        if value:
            if not in_cycle[i]:
                return None
            if i != x:
                # Find distance from X backwards. Build positions lazily below.
                pass

    back_pos = [-1] * n
    for i, v in enumerate(back):
        back_pos[v] = i

    for i, value in enumerate(balls):
        if value and i != x:
            farthest = max(farthest, back_pos[i])

    # The required firing order for this color is from farthest source toward X.
    return list(reversed(back[:farthest + 1]))


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1

    a = list(it)
    a = a[:n]
    b = data[2 + n:2 + 2 * n]
    p = [v - 1 for v in data[2 + 2 * n:2 + 3 * n]]
    q = [v - 1 for v in data[2 + 3 * n:2 + 4 * n]]

    red = required_sequence(n, x, a, p)
    blue = required_sequence(n, x, b, q)

    if red is None or blue is None:
        print(-1)
        return

    blue_pos = [-1] * n
    for i, v in enumerate(blue):
        blue_pos[v] = i

    # LCS of two sequences with distinct elements becomes LIS of mapped positions.
    lis = []
    for v in red:
        pos = blue_pos[v]
        if pos != -1:
            j = bisect_left(lis, pos)
            if j == len(lis):
                lis.append(pos)
            else:
                lis[j] = pos

    # Each common-order pairing lets one operation forward both colors.
    print(len(red) + len(blue) - len(lis))


if __name__ == "__main__":
    main()
import sys
from bisect import bisect_left


def active_sequence(n, x, balls, perm):
    """Return the required firing sequence, or None if infeasible."""
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
    for v, has_ball in enumerate(balls):
        if not has_ball:
            continue
        if pos[v] == -1:
            return None
        if pos[v] > 0:
            first = min(first, pos[v])

    if first == len(cycle):
        return []

    # Balls move forward along the permutation toward X.
    # A ball at cycle position k requires firings k, k+1, ..., before X.
    return cycle[first:]


def main():
    input = sys.stdin.readline

    n, x = map(int, input().split())
    x -= 1

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    p = [v - 1 for v in map(int, input().split())]
    q = [v - 1 for v in map(int, input().split())]

    red = active_sequence(n, x, a, p)
    if red is None:
        print(-1)
        return

    blue = active_sequence(n, x, b, q)
    if blue is None:
        print(-1)
        return

    blue_pos = {v: i for i, v in enumerate(blue)}
    common_positions = [blue_pos[v] for v in red if v in blue_pos]

    lis = []
    for value in common_positions:
        i = bisect_left(lis, value)
        if i == len(lis):
            lis.append(value)
        else:
            lis[i] = value

    print(len(red) + len(blue) - len(lis))


if __name__ == "__main__":
    main()
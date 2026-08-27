import sys
from bisect import bisect_left


def build_chain(balls, perm, x):
    n = len(perm)

    # inverse permutation: inv[v] is the box whose perm-edge enters v
    inv = [0] * n
    for i, v in enumerate(perm):
        inv[v] = i

    # Boxes on the cycle of x, ordered by distance from x when moving
    # backwards along perm: distance 1, 2, ..., up to the predecessor of x.
    near = []
    cur = inv[x]
    while cur != x:
        near.append(cur)
        cur = inv[cur]

    distance = [-1] * n
    for d, v in enumerate(near, 1):
        distance[v] = d

    farthest = 0
    for i, has_ball in enumerate(balls):
        if not has_ball or i == x:
            continue
        if distance[i] == -1:
            return None
        farthest = max(farthest, distance[i])

    if farthest == 0:
        return []

    # Required operation order: farthest from x toward nearest.
    return near[farthest - 1::-1]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    n = next(it)
    x = next(it) - 1

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    red_chain = build_chain(a, p, x)
    blue_chain = build_chain(b, q, x)

    if red_chain is None or blue_chain is None:
        print(-1)
        return

    # Compute LCS of the two chains as LIS after mapping blue vertices
    # to their positions.
    blue_pos = [-1] * n
    for i, v in enumerate(blue_chain):
        blue_pos[v] = i

    mapped = [blue_pos[v] for v in red_chain if blue_pos[v] != -1]

    tails = []
    for value in mapped:
        pos = bisect_left(tails, value)
        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value

    lcs = len(tails)
    print(len(red_chain) + len(blue_chain) - lcs)


if __name__ == "__main__":
    main()
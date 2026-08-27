import sys
from bisect import bisect_left


def build_sequence(n, x, balls, perm):
    """Return the required operation vertices in forward ball-movement order.

    The sequence is empty if there are no balls outside x.
    Return None if some ball is not on the permutation cycle containing x.
    """
    inv = [0] * n
    for i, v in enumerate(perm):
        inv[v] = i

    # Find the cycle containing x and distances toward x.
    dist = [-1] * n
    cur = x
    d = 0
    while dist[cur] == -1:
        dist[cur] = d
        d += 1
        cur = inv[cur]

    max_dist = 0
    for i, has_ball in enumerate(balls):
        if has_ball:
            if dist[i] == -1:
                return None
            if i != x and dist[i] > max_dist:
                max_dist = dist[i]

    if max_dist == 0:
        return []

    # Vertices at distances max_dist, ..., 1 from x.
    seq = []
    cur = x
    for _ in range(max_dist):
        cur = inv[cur]
        seq.append(cur)
    seq.reverse()
    return seq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    red = build_sequence(n, x, a, p)
    blue = build_sequence(n, x, b, q)

    if red is None or blue is None:
        print(-1)
        return

    # Maximum number of red/blue tasks that can be performed together.
    blue_pos = {v: i for i, v in enumerate(blue)}
    tails = []

    for v in red:
        pos = blue_pos.get(v)
        if pos is None:
            continue
        k = bisect_left(tails, pos)
        if k == len(tails):
            tails.append(pos)
        else:
            tails[k] = pos

    paired = len(tails)
    print(len(red) + len(blue) - paired)


if __name__ == "__main__":
    main()
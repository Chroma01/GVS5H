import sys
from bisect import bisect_left


def build_path(perm, balls, x):
    n = len(perm)
    pos = [-1] * n

    cur = x
    length = 0
    while pos[cur] == -1:
        pos[cur] = length
        length += 1
        cur = perm[cur]

    max_dist = 0
    farthest = -1

    for v, has in enumerate(balls):
        if has:
            p = pos[v]
            if p == -1:
                return None

            dist = length - p
            if dist == length:
                dist = 0

            if dist > max_dist:
                max_dist = dist
                farthest = v

    if max_dist == 0:
        return []

    path = []
    cur = farthest
    for _ in range(max_dist):
        path.append(cur)
        cur = perm[cur]

    return path


def lcs_len(a, b, n):
    if not a or not b:
        return 0

    if len(a) > len(b):
        a, b = b, a

    pos = [-1] * n
    for i, v in enumerate(a):
        pos[v] = i

    tails = []
    bl = bisect_left

    for v in b:
        p = pos[v]
        if p != -1:
            i = bl(tails, p)
            if i == len(tails):
                tails.append(p)
            else:
                tails[i] = p

    return len(tails)


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    n = data[idx]
    x = data[idx + 1] - 1
    idx += 2

    red = data[idx:idx + n]
    idx += n

    blue = data[idx:idx + n]
    idx += n

    p = [v - 1 for v in data[idx:idx + n]]
    idx += n

    q = [v - 1 for v in data[idx:idx + n]]
    del data

    red_path = build_path(p, red, x)
    if red_path is None:
        print(-1)
        return
    del red, p

    blue_path = build_path(q, blue, x)
    if blue_path is None:
        print(-1)
        return
    del blue, q

    common = lcs_len(red_path, blue_path, n)
    print(len(red_path) + len(blue_path) - common)


if __name__ == "__main__":
    solve()
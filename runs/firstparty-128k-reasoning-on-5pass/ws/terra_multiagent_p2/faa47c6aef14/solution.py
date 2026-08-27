import sys
from bisect import bisect_left

def build_path_and_check(n, x, initial, perm):
    inv = [0] * (n + 1)
    for i in range(1, n + 1):
        inv[perm[i]] = i

    dist = [-1] * (n + 1)
    node_at_dist = [x]
    dist[x] = 0

    cur = x
    d = 0
    while True:
        cur = inv[cur]
        if cur == x:
            break
        d += 1
        dist[cur] = d
        node_at_dist.append(cur)

    farthest = 0
    for i in range(1, n + 1):
        if initial[i]:
            if dist[i] == -1:
                return None
            if dist[i] > farthest:
                farthest = dist[i]

    path = []
    if farthest > 0:
        cur = node_at_dist[farthest]
        while cur != x:
            path.append(cur)
            cur = perm[cur]

    return path

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it)

    a = [0] + [next(it) for _ in range(n)]
    b = [0] + [next(it) for _ in range(n)]
    p = [0] + [next(it) for _ in range(n)]
    q = [0] + [next(it) for _ in range(n)]

    red_path = build_path_and_check(n, x, a, p)
    blue_path = build_path_and_check(n, x, b, q)

    if red_path is None or blue_path is None:
        print(-1)
        return

    pos_blue = {v: i for i, v in enumerate(blue_path)}
    lis = []

    for v in red_path:
        if v in pos_blue:
            z = pos_blue[v]
            k = bisect_left(lis, z)
            if k == len(lis):
                lis.append(z)
            else:
                lis[k] = z

    lcs = len(lis)
    print(len(red_path) + len(blue_path) - lcs)

if __name__ == "__main__":
    main()
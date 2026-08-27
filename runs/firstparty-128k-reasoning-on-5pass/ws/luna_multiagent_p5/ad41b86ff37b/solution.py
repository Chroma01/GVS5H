import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]
    deg = [0] * n

    pos = 1
    for _ in range(n - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    max_cap = max(deg) - 1
    buckets = [[] for _ in range(max_cap + 1)]

    for v in range(n):
        cap = deg[v] - 1
        if cap >= 1:
            buckets[cap].append(v)

    eligible = [0] * n
    best_x = 0
    best_size = 0

    # At threshold y, active vertices are exactly those with capacity >= y.
    for y in range(max_cap, 0, -1):
        for v in buckets[y]:
            for center in adj[v]:
                eligible[center] += 1
                if eligible[center] > best_x:
                    best_x = eligible[center]

        if best_x > 0:
            retained = 1 + best_x * (y + 1)
            if retained > best_size:
                best_size = retained

    print(n - best_size)


if __name__ == "__main__":
    solve()
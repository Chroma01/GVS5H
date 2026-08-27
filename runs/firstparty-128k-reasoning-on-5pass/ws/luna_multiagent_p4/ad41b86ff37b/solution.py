import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]

    p = 1
    for _ in range(n - 1):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        adj[u].append(v)
        adj[v].append(u)

    best = 0

    for u in range(n):
        capacities = [len(adj[v]) - 1 for v in adj[u]]
        capacities.sort(reverse=True)

        for i, capacity in enumerate(capacities, 1):
            if capacity <= 0:
                break
            retained = 1 + i * (capacity + 1)
            if retained > best:
                best = retained

    print(n - best)


if __name__ == "__main__":
    solve()
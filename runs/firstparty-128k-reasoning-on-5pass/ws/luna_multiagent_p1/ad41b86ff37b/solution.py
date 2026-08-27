import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]
    degree = [0] * n

    p = 1
    for _ in range(n - 1):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    best = 0

    for center in range(n):
        capacities = [degree[neighbor] - 1 for neighbor in adj[center]]
        capacities.sort(reverse=True)

        k = 0
        for capacity in capacities:
            if capacity <= 0:
                break
            k += 1
            retained = 1 + k * (capacity + 1)
            if retained > best:
                best = retained

    print(n - best)


if __name__ == "__main__":
    solve()
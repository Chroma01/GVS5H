import sys


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())

    adj = [[] for _ in range(n)]
    deg = [0] * n

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    best = 0

    for center in range(n):
        capacities = [deg[v] - 1 for v in adj[center]]
        capacities.sort(reverse=True)

        for i, cap in enumerate(capacities, 1):
            if cap == 0:
                break
            best = max(best, 1 + i * (cap + 1))

    print(n - best)


if __name__ == "__main__":
    solve()
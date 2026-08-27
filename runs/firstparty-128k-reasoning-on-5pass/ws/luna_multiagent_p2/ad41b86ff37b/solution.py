import sys


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    adj = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    best = 0

    for center in range(n):
        capacities = sorted(len(adj[neighbor]) - 1 for neighbor in adj[center])
        d = len(capacities)

        i = 0
        while i < d:
            y = capacities[i]
            j = i + 1
            while j < d and capacities[j] == y:
                j += 1

            if y > 0:
                x = d - i
                size = 1 + x * (y + 1)
                if size > best:
                    best = size

            i = j

    print(n - best)


if __name__ == "__main__":
    solve()
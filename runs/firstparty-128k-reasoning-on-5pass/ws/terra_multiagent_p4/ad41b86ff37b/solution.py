import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    graph = [[] for _ in range(n)]

    p = 1
    for _ in range(n - 1):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        graph[u].append(v)
        graph[v].append(u)

    deg = [len(adj) for adj in graph]
    best = 0

    for center in range(n):
        capacities = [deg[branch] - 1 for branch in graph[center]]
        capacities.sort(reverse=True)

        i = 0
        while i < len(capacities):
            y = capacities[i]
            j = i + 1
            while j < len(capacities) and capacities[j] == y:
                j += 1

            if y >= 1:
                x = j
                best = max(best, 1 + x * (y + 1))

            i = j

    print(n - best)


if __name__ == "__main__":
    solve()
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]

    adj = [[] for _ in range(n)]
    for i in range(1, 2 * n - 1, 2):
        u = data[i] - 1
        v = data[i + 1] - 1
        adj[u].append(v)
        adj[v].append(u)

    deg = [len(neighbors) for neighbors in adj]
    best = 0

    for center in range(n):
        capacities = [deg[v] - 1 for v in adj[center] if deg[v] >= 2]
        if not capacities:
            continue

        capacities.sort(reverse=True)

        k = 0
        i = 0
        m = len(capacities)

        while i < m:
            y = capacities[i]
            j = i
            while j < m and capacities[j] == y:
                j += 1

            k = j
            kept = 1 + (y + 1) * k
            if kept > best:
                best = kept

            i = j

    print(n - best)


if __name__ == "__main__":
    solve()
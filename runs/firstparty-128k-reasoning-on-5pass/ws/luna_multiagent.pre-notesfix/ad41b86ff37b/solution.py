import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]
    degree = [0] * n

    pos = 1
    for _ in range(n - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    order = list(range(n))
    order.sort(key=lambda v: degree[v], reverse=True)

    eligible_count = [0] * n
    max_x = 0
    best_size = 0

    i = 0
    while i < n:
        y = degree[order[i]] - 1
        if y < 1:
            break

        j = i
        while j < n and degree[order[j]] - 1 == y:
            j += 1

        for k in range(i, j):
            v = order[k]
            for center in adj[v]:
                eligible_count[center] += 1
                if eligible_count[center] > max_x:
                    max_x = eligible_count[center]

        if max_x > 0:
            size = 1 + (y + 1) * max_x
            if size > best_size:
                best_size = size

        i = j

    print(n - best_size)


if __name__ == "__main__":
    solve()
import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    total = n * k

    if k == 1:
        print("Yes")
        return

    graph = [[] for _ in range(total)]
    pos = 2
    for _ in range(total - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * total
    order = [0]
    parent[0] = total
    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    residual = [0] * total

    for u in reversed(order):
        active = []
        for v in graph[u]:
            if parent[v] == u and residual[v] != 0:
                active.append(residual[v])

        if len(active) >= 3:
            print("No")
            return

        if len(active) == 0:
            residual[u] = 1
        elif len(active) == 1:
            length = active[0] + 1
            if length == k:
                residual[u] = 0
            else:
                residual[u] = length
        else:
            if active[0] + active[1] + 1 != k:
                print("No")
                return
            residual[u] = 0

    print("Yes" if residual[0] == 0 else "No")


if __name__ == "__main__":
    solve()
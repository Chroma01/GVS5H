import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    total = n * k

    graph = [[] for _ in range(total)]
    p = 2
    for _ in range(total - 1):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * total
    parent[0] = total
    order = [0]

    for v in order:
        for to in graph[v]:
            if parent[to] == -1:
                parent[to] = v
                order.append(to)

    rem = [0] * total

    for v in reversed(order):
        value = 1
        for to in graph[v]:
            if parent[to] == v:
                value += rem[to]
        rem[v] = value % k

    used_degree = [0] * total
    for v in range(1, total):
        if rem[v] != 0:
            par = parent[v]
            used_degree[v] += 1
            used_degree[par] += 1

    print("Yes" if max(used_degree) <= 2 else "No")


if __name__ == "__main__":
    solve()
import sys


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    eligible = [len(graph[v]) >= 4 for v in range(n)]

    parent = [-2] * n
    order = []

    for start in range(n):
        if not eligible[start] or parent[start] != -2:
            continue
        parent[start] = -1
        stack = [start]
        while stack:
            v = stack.pop()
            order.append(v)
            for to in graph[v]:
                if eligible[to] and parent[to] == -2:
                    parent[to] = v
                    stack.append(to)

    if not order:
        print(-1)
        return

    down = [0] * n

    for v in reversed(order):
        values = []
        for to in graph[v]:
            if eligible[to] and parent[to] == v:
                values.append(down[to])
        values.sort(reverse=True)
        down[v] = 1 + sum(values[:3])

    best_k = 0
    for v in order:
        values = []
        for to in graph[v]:
            if eligible[to] and parent[to] == v:
                values.append(down[to])
        values.sort(reverse=True)
        best_k = max(best_k, 1 + sum(values[:4]))

    print(3 * best_k + 2)


if __name__ == "__main__":
    solve()
import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    m = n * k

    graph = [[] for _ in range(m)]
    idx = 2
    for _ in range(m - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-2] * m
    parent[0] = -1
    order = []
    stack = [0]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    open_len = [0] * m

    for v in reversed(order):
        count = 0
        total = 0

        for to in graph[v]:
            if parent[to] == v and open_len[to] != 0:
                count += 1
                total += open_len[to]

        if count > 2:
            print("No")
            return

        if count == 2:
            if total + 1 != k:
                print("No")
                return
            open_len[v] = 0
        else:
            length = total + 1
            if length == k:
                open_len[v] = 0
            elif length < k:
                open_len[v] = length
            else:
                print("No")
                return

    print("Yes" if open_len[0] == 0 else "No")


if __name__ == "__main__":
    solve()
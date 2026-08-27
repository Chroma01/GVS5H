import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    m = n * k

    graph = [[] for _ in range(m)]
    pos = 2
    for _ in range(m - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-2] * m
    parent[0] = -1
    order = [0]

    for v in order:
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            order.append(to)

    valid = [True] * m
    residual = [0] * m

    for v in reversed(order):
        child_count = 0
        first = 0
        second = 0
        ok = True

        for to in graph[v]:
            if parent[to] != v:
                continue

            if not valid[to]:
                ok = False
                continue

            length = residual[to]
            if length != 0:
                child_count += 1
                if child_count == 1:
                    first = length
                elif child_count == 2:
                    second = length
                else:
                    ok = False

        if not ok or child_count > 2:
            valid[v] = False
            continue

        if child_count == 0:
            if k == 1:
                residual[v] = 0
            else:
                residual[v] = 1

        elif child_count == 1:
            length = first + 1
            if length > k:
                valid[v] = False
            elif length == k:
                residual[v] = 0
            else:
                residual[v] = length

        else:
            if first + second + 1 != k:
                valid[v] = False
            else:
                residual[v] = 0

    print("Yes" if valid[0] and residual[0] == 0 else "No")


if __name__ == "__main__":
    solve()
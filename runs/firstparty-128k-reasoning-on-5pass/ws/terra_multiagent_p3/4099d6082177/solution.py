import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    V = N * K

    if K == 1:
        print("Yes")
        return

    graph = [[] for _ in range(V)]
    idx = 2
    for _ in range(V - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-2] * V
    parent[0] = -1
    order = [0]

    for v in order:
        for to in graph[v]:
            if parent[to] == -2:
                parent[to] = v
                order.append(to)

    residual = [0] * V
    possible = True

    for v in reversed(order):
        count = 0
        a = 0
        b = 0

        for to in graph[v]:
            if parent[to] != v:
                continue
            r = residual[to]
            if r != 0:
                count += 1
                if count == 1:
                    a = r
                elif count == 2:
                    b = r
                else:
                    possible = False
                    break

        if not possible:
            break

        if count == 0:
            residual[v] = 1
        elif count == 1:
            if a + 1 == K:
                residual[v] = 0
            else:
                residual[v] = a + 1
        else:
            if a + b + 1 == K:
                residual[v] = 0
            else:
                possible = False
                break

    print("Yes" if possible and residual[0] == 0 else "No")


if __name__ == "__main__":
    solve()
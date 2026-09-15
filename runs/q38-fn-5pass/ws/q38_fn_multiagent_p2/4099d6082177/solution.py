import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])

    # A path of one vertex is always possible.
    if K == 1:
        print("Yes")
        return

    M = N * K
    adj = [[] for _ in range(M)]

    idx = 2
    for _ in range(M - 1):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    # Iterative DFS to root the tree at vertex 0.
    parent = [-1] * M
    parent[0] = 0
    order = []
    stack = [0]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            if parent[to] != -1:
                continue
            parent[to] = v
            stack.append(to)

    if len(order) != M:
        print("No")
        return

    # sub[v] = size of subtree of v modulo K.
    sub = [1] * M
    for v in reversed(order):
        p = parent[v]
        if p != v:  # not the root
            sub[p] += sub[v]
            if sub[p] >= K:
                sub[p] %= K

    sub[0] %= K

    # An edge parent[v]-v is forced to be used iff sub[v] != 0.
    deg = [0] * M
    for v in range(1, M):
        if sub[v] != 0:
            p = parent[v]
            deg[v] += 1
            deg[p] += 1
            if deg[v] > 2 or deg[p] > 2:
                print("No")
                return

    # Verify every forced-edge component has exactly K vertices.
    visited = bytearray(M)

    for i in range(M):
        if visited[i]:
            continue

        count = 0
        stack = [i]
        visited[i] = 1

        while stack:
            v = stack.pop()
            count += 1
            pv = parent[v]

            for to in adj[v]:
                if visited[to]:
                    continue

                if parent[to] == v:
                    if sub[to] != 0:
                        visited[to] = 1
                        stack.append(to)
                elif pv == to:
                    if sub[v] != 0:
                        visited[to] = 1
                        stack.append(to)

        if count != K:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()
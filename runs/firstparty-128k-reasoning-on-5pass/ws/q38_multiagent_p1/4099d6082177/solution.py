import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    M = N * K

    if K == 1:
        print("Yes")
        return

    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    parent = [0] * (M + 1)
    parent[1] = -1
    order = [1]
    i = 0
    while i < len(order):
        v = order[i]
        i += 1
        pv = parent[v]
        for to in adj[v]:
            if to == pv or parent[to] != 0:
                continue
            parent[to] = v
            order.append(to)

    if len(order) != M:
        print("No")
        return

    sub = [0] * (M + 1)
    for v in reversed(order):
        s = 1
        for to in adj[v]:
            if parent[to] == v:
                s += sub[to]
                if s >= K:
                    s -= K
        sub[v] = s

    visited = bytearray(M + 1)

    for start in range(1, M + 1):
        if visited[start]:
            continue

        visited[start] = 1
        stack = [start]
        cnt = 0

        while stack:
            v = stack.pop()
            cnt += 1

            if cnt > K:
                print("No")
                return

            deg = 0
            for to in adj[v]:
                if parent[to] == v:
                    kept = sub[to] != 0
                elif parent[v] == to:
                    kept = sub[v] != 0
                else:
                    kept = False

                if kept:
                    deg += 1
                    if deg > 2:
                        print("No")
                        return
                    if not visited[to]:
                        visited[to] = 1
                        stack.append(to)

        if cnt != K:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()
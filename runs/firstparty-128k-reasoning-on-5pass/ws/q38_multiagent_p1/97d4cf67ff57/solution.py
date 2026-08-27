import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]

    for i in range(1, len(data), 2):
        a = data[i] - 1
        b = data[i + 1] - 1
        adj[a].append(b)
        adj[b].append(a)

    is_h = [False] * n
    has_h = False
    for i in range(n):
        if len(adj[i]) >= 4:
            is_h[i] = True
            has_h = True

    if not has_h:
        print(-1)
        return

    parent = [-1] * n
    parent[0] = 0
    order = []
    stack = [0]

    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v == parent[u]:
                continue
            if parent[v] != -1:
                continue
            parent[v] = u
            stack.append(v)

    g = [0] * n
    max_f = 0

    for u in reversed(order):
        if not is_h[u]:
            continue

        m1 = m2 = m3 = m4 = 0

        for v in adj[u]:
            if parent[v] == u and is_h[v]:
                val = g[v]
                if val > m1:
                    m4 = m3
                    m3 = m2
                    m2 = m1
                    m1 = val
                elif val > m2:
                    m4 = m3
                    m3 = m2
                    m2 = val
                elif val > m3:
                    m4 = m3
                    m3 = val
                elif val > m4:
                    m4 = val

        g[u] = 1 + m1 + m2 + m3
        f = 1 + m1 + m2 + m3 + m4

        if f > max_f:
            max_f = f

    print(3 * max_f + 2)

if __name__ == "__main__":
    main()
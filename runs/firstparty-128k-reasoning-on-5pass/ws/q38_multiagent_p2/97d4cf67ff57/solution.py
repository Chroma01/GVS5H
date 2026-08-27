import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    for _ in range(n - 1):
        a = int(next(it))
        b = int(next(it))
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1
    del data, it

    elig = bytearray(n + 1)
    has = False
    for i in range(1, n + 1):
        if deg[i] >= 4:
            elig[i] = 1
            has = True
    del deg
    if not has:
        print(-1)
        return

    parent = [-1] * (n + 1)
    order = []
    for i in range(1, n + 1):
        if elig[i] and parent[i] == -1:
            parent[i] = 0
            stack = [i]
            while stack:
                u = stack.pop()
                order.append(u)
                for v in adj[u]:
                    if elig[v] and parent[v] == -1:
                        parent[v] = u
                        stack.append(v)

    f = [0] * (n + 1)
    ans = 0
    for u in reversed(order):
        a = b = c = d = 0
        for v in adj[u]:
            if parent[v] == u:
                val = f[v]
                if val > a:
                    d = c
                    c = b
                    b = a
                    a = val
                elif val > b:
                    d = c
                    c = b
                    b = val
                elif val > c:
                    d = c
                    c = val
                elif val > d:
                    d = val
        f[u] = 1 + a + b + c
        total = f[u] + d
        if total > ans:
            ans = total

    print((3 * ans + 2) if ans > 0 else -1)

if __name__ == "__main__":
    main()
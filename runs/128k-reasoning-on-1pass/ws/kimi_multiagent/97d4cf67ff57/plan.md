```python
import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    adj = [[] for _ in range(n + 1)]
    p = 1
    for _ in range(n - 1):
        a = data[p]; b = data[p + 1]; p += 2
        adj[a].append(b)
        adj[b].append(a)

    eligible = [False] * (n + 1)
    for i in range(1, n + 1):
        eligible[i] = len(adj[i]) >= 4

    visited = [False] * (n + 1)
    parent = [0] * (n + 1)
    g = [0] * (n + 1)  # parent included: at most 3 children
    best_core = 0

    for s in range(1, n + 1):
        if not eligible[s] or visited[s]:
            continue

        order = []
        stack = [s]
        visited[s] = True
        parent[s] = 0

        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if eligible[v] and not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    stack.append(v)

        for u in reversed(order):
            t1 = t2 = t3 = t4 = 0
            for v in adj[u]:
                if eligible[v] and parent[v] == u:
                    x = g[v]
                    if x > t1:
                        t4 = t3; t3 = t2; t2 = t1; t1 = x
                    elif x > t2:
                        t4 = t3; t3 = t2; t2 = x
                    elif x > t3:
                        t4 = t3; t3 = x
                    elif x > t4:
                        t4 = x
            g[u] = 1 + t1 + t2 + t3          # parent edge uses one degree slot
            h = 1 + t1 + t2 + t3 + t4        # u is the highest vertex of the core
            if h > best_core:
                best_core = h

    print(3 * best_core + 2 if best_core > 0 else -1)

if __name__ == "__main__":
    solve()
```
import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)

    idx = 1
    for _ in range(n - 1):
        a = data[idx]
        b = data[idx + 1]
        idx += 2
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1

    parent = [0] * (n + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    dp = [0] * (n + 1)
    best = 0

    for v in reversed(order):
        if deg[v] >= 4:
            m1 = m2 = m3 = m4 = 0

            for to in adj[v]:
                if parent[to] == v:
                    val = dp[to]
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

            dp[v] = 1 + m1 + m2 + m3
            cand = dp[v] + m4
            if cand > best:
                best = cand

    if best == 0:
        print(-1)
    else:
        print(3 * best + 2)

if __name__ == "__main__":
    solve()
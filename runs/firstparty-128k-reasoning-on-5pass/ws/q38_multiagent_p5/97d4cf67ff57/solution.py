import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    adj = [[] for _ in range(n)]
    idx = 1
    for _ in range(n - 1):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)
    del data

    parent = [-1] * n
    parent[0] = 0
    order = [0]
    i = 0
    while i < len(order):
        v = order[i]
        i += 1
        pv = parent[v]
        for to in adj[v]:
            if to == pv:
                continue
            if parent[to] != -1:
                continue
            parent[to] = v
            order.append(to)

    dp = [0] * n
    max_core = 0

    for v in reversed(order):
        if len(adj[v]) < 4:
            continue
        t0 = t1 = t2 = t3 = 0
        for to in adj[v]:
            if parent[to] == v:
                val = dp[to]
                if val > t0:
                    t3 = t2
                    t2 = t1
                    t1 = t0
                    t0 = val
                elif val > t1:
                    t3 = t2
                    t2 = t1
                    t1 = val
                elif val > t2:
                    t3 = t2
                    t2 = val
                elif val > t3:
                    t3 = val
        dp[v] = 1 + t0 + t1 + t2
        best = 1 + t0 + t1 + t2 + t3
        if best > max_core:
            max_core = best

    if max_core == 0:
        print(-1)
    else:
        print(3 * max_core + 2)

if __name__ == "__main__":
    solve()
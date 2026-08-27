import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]
    deg = [0] * n

    idx = 1
    for _ in range(n - 1):
        a = data[idx] - 1
        b = data[idx + 1] - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1

    del data

    marked = [d >= 4 for d in deg]
    del deg

    if not any(marked):
        print(-1)
        return

    parent = [-2] * n
    order = []
    stack = []

    for i in range(n):
        if marked[i] and parent[i] == -2:
            parent[i] = -1
            stack.append(i)
            while stack:
                u = stack.pop()
                order.append(u)
                for v in adj[u]:
                    if marked[v] and parent[v] == -2:
                        parent[v] = u
                        stack.append(v)

    dp = [0] * n
    ans = 0

    for u in reversed(order):
        t0 = t1 = t2 = t3 = 0

        for v in adj[u]:
            if marked[v] and parent[v] == u:
                val = dp[v]
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

        dp[u] = 1 + t0 + t1 + t2
        best = 1 + t0 + t1 + t2 + t3
        if best > ans:
            ans = best

    print((3 * ans + 2) if ans > 0 else -1)

if __name__ == "__main__":
    main()
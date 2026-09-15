import sys

def solve():
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return
    n = int(line)

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * n
    parent[0] = -2
    order = [0]
    stack = [0]

    while stack:
        u = stack.pop()
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            stack.append(v)
            order.append(v)

    dp = [1] * n
    ans = -1

    for u in reversed(order):
        t1 = t2 = t3 = t4 = 0
        cnt = 0

        for v in g[u]:
            if v == parent[u]:
                continue
            cnt += 1
            x = dp[v]

            if x > t1:
                t4 = t3
                t3 = t2
                t2 = t1
                t1 = x
            elif x > t2:
                t4 = t3
                t3 = t2
                t2 = x
            elif x > t3:
                t4 = t3
                t3 = x
            elif x > t4:
                t4 = x

        if cnt >= 3:
            dp[u] = 1 + t1 + t2 + t3

        if cnt >= 4:
            cand = 1 + t1 + t2 + t3 + t4
            if cand > ans:
                ans = cand

        if t1 > 1:
            cand = 1 + t1
            if cand > ans:
                ans = cand

    print(ans)

if __name__ == "__main__":
    solve()
import sys


def solve():
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

    eligible = [False] * (n + 1)
    for i in range(1, n + 1):
        if deg[i] >= 4:
            eligible[i] = True

    parent = [0] * (n + 1)
    dp = [0] * (n + 1)
    max_s = 0

    for root in range(1, n + 1):
        if not eligible[root] or parent[root] != 0:
            continue

        parent[root] = -1
        stack = [root]
        order = []

        while stack:
            v = stack.pop()
            order.append(v)
            for to in adj[v]:
                if eligible[to] and parent[to] == 0:
                    parent[to] = v
                    stack.append(to)

        for v in reversed(order):
            t1 = t2 = t3 = t4 = 0

            for to in adj[v]:
                if parent[to] == v:
                    val = dp[to]
                    if val > t1:
                        t4 = t3
                        t3 = t2
                        t2 = t1
                        t1 = val
                    elif val > t2:
                        t4 = t3
                        t3 = t2
                        t2 = val
                    elif val > t3:
                        t4 = t3
                        t3 = val
                    elif val > t4:
                        t4 = val

            # f[v]: parent of v is selected, so v can take at most 3 child branches.
            dp[v] = 1 + t1 + t2 + t3

            # g[v]: parent of v is not selected, so v can take at most 4 child branches.
            closed = 1 + t1 + t2 + t3 + t4
            if closed > max_s:
                max_s = closed

    if max_s == 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write(str(3 * max_s + 2) + "\n")


if __name__ == "__main__":
    solve()
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        a = int(next(it)); b = int(next(it))
        adj[a].append(b)
        adj[b].append(a)

    NEG = -10**9

    # Root tree at 1, build parent and traversal order iteratively
    parent = [0] * (N + 1)
    parent[1] = -1
    order = []
    stack = [1]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)

    # dp[u][k][h]: max selected vertices in connected selected set inside u's
    # subtree that includes u, with exactly k selected children, where h=1 means
    # a degree-4 vertex already exists among u's selected descendants (not u).
    dp = [None] * (N + 1)
    ans = NEG

    for u in reversed(order):
        # knapsack merge over children: cur[m][h]
        cur = [[NEG, NEG] for _ in range(5)]
        cur[0][0] = 0
        for v in adj[u]:
            if v == parent[u]:
                continue
            d = dp[v]
            # child included => its parent (u) is selected, so child needs
            # selected-child-count 0 (degree 1) or 3 (degree 4)
            inc0 = d[0][0]                       # child degree 1, no deg-4 below
            inc1 = max(d[0][1], d[3][0], d[3][1])  # deg-4 at/below child
            nxt = [[NEG, NEG] for _ in range(5)]
            for m in range(5):
                for h in range(2):
                    val = cur[m][h]
                    if val == NEG:
                        continue
                    # exclude child
                    if val > nxt[m][h]:
                        nxt[m][h] = val
                    # include child
                    if m < 4:
                        if inc0 != NEG:
                            nv = val + inc0
                            if nv > nxt[m + 1][h]:
                                nxt[m + 1][h] = nv
                        if inc1 != NEG:
                            nv = val + inc1
                            if nv > nxt[m + 1][1]:
                                nxt[m + 1][1] = nv
            cur = nxt

        d = [[NEG, NEG] for _ in range(5)]
        for k in range(5):
            for h in range(2):
                if cur[k][h] != NEG:
                    d[k][h] = cur[k][h] + 1  # include u itself
        dp[u] = d

        # u as highest node of the alkane (parent not selected):
        # degree of u = k must be 1 or 4; need a degree-4 vertex somewhere.
        if d[1][1] > ans:
            ans = d[1][1]
        if d[4][0] > ans:
            ans = d[4][0]
        if d[4][1] > ans:
            ans = d[4][1]

    print(ans if ans != NEG else -1)

solve()
import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [int(x) - 1 for x in data[2:2 + n]]

    # in-degree peeling to find cycle nodes
    indeg = [0] * n
    for a in A:
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    removed = [False] * n
    while q:
        u = q.popleft()
        removed[u] = True
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    on_cycle = [not removed[i] for i in range(n)]

    # children lists: for non-cycle node u with parent A[u]
    children = [[] for _ in range(n)]
    for u in range(n):
        if not on_cycle[u]:
            children[A[u]].append(u)

    # compute f_u for every cycle node u (tree DP over its in-tree)
    f = [None] * n  # f[u] defined for cycle nodes
    for r in range(n):
        if not on_cycle[r]:
            continue
        order = []
        stack = [r]
        while stack:
            u = stack.pop()
            order.append(u)
            for c in children[u]:
                stack.append(c)
        dp = {}
        for u in reversed(order):
            fu = [1] * (m + 1)
            fu[0] = 0
            for c in children[u]:
                fc = dp[c]
                s = 0
                pref = [0] * (m + 1)
                for v in range(1, m + 1):
                    s = (s + fc[v]) % MOD
                    pref[v] = s
                for v in range(1, m + 1):
                    fu[v] = fu[v] * pref[v] % MOD
            dp[u] = fu
        f[r] = dp[r]

    # group cycles and combine
    visited = [False] * n
    total = 1
    for r in range(n):
        if not on_cycle[r] or visited[r]:
            continue
        # walk the cycle
        cyc = []
        u = r
        while not visited[u]:
            visited[u] = True
            cyc.append(u)
            u = A[u]
        # contribution: sum over v of product of f_u(v) over cycle nodes
        comp = 0
        for v in range(1, m + 1):
            prod = 1
            for u in cyc:
                prod = prod * f[u][v] % MOD
            comp = (comp + prod) % MOD
        total = total * comp % MOD

    print(total)

main()
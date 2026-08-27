import sys
sys.setrecursionlimit(1000000)
MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [int(x) - 1 for x in data[2:2 + n]]

    # Find nodes that lie on directed cycles via in-degree peeling
    indeg = [0] * n
    for a in A:
        indeg[a] += 1
    stack = [i for i in range(n) if indeg[i] == 0]
    removed = [False] * n
    while stack:
        v = stack.pop()
        removed[v] = True
        u = A[v]
        indeg[u] -= 1
        if indeg[u] == 0:
            stack.append(u)
    cyclic = [not removed[i] for i in range(n)]

    # Assign each node to a component representative (a cyclic node)
    comp = [-1] * n
    for i in range(n):
        if cyclic[i] and comp[i] == -1:
            j = i
            while comp[j] == -1:
                comp[j] = i
                j = A[j]
    for i in range(n):
        if comp[i] == -1:
            path = []
            j = i
            while comp[j] == -1:
                path.append(j)
                j = A[j]
            r = comp[j]
            for v in path:
                comp[v] = r

    # Build contracted forest
    children = [[] for _ in range(n)]
    roots = []
    for i in range(n):
        if cyclic[i]:
            if comp[i] == i:
                roots.append(i)
        else:
            p = A[i]
            parent = p if not cyclic[p] else comp[p]
            children[parent].append(i)

    # DP over each tree
    ans = 1
    for r in roots:
        order = []
        stack = [(r, False)]
        while stack:
            v, processed = stack.pop()
            if processed:
                order.append(v)
            else:
                stack.append((v, True))
                for u in children[v]:
                    stack.append((u, False))
        dp = {}
        for v in order:
            cur = [1] * (m + 1)
            for u in children[v]:
                pu = dp.pop(u)
                pref = 0
                for k in range(1, m + 1):
                    pref += pu[k]
                    if pref >= MOD:
                        pref -= MOD
                    cur[k] = cur[k] * pref % MOD
            dp[v] = cur
        total = sum(dp[r][1:]) % MOD
        ans = ans * total % MOD

    print(ans)

main()
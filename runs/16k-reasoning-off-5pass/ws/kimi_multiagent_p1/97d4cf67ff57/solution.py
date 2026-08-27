import sys

def main():
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

    if N < 5:
        print(-1)
        return

    # Iterative rooting from node 1
    parent = [0] * (N + 1)
    order = []          # preorder
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)

    NEG = -10**9
    # dp[u][d][f]: max size of connected chosen subtree inside subtree(u),
    # containing u, where u has exactly d chosen children (degree from children = d),
    # and f = 1 if some vertex in it has final degree 4.
    # Validity requirement for every included child v: v's total degree (incl. edge to u)
    # must be 1 or 4, i.e. v has 0 or 3 chosen children.
    dp = [[[NEG, NEG] for _ in range(5)] for _ in range(N + 1)]
    ans = -1

    for u in reversed(order):
        cur = [[NEG, NEG] for _ in range(5)]
        cur[0][0] = 1  # u alone, no children chosen yet
        for v in adj[u]:
            if v == parent[u]:
                continue
            dpv = dp[v]
            # best contribution when keeping edge (u,v): child v must end with
            # total degree 1 (0 children) or 4 (3 children, which forces f=1)
            best0 = dpv[0][0]                     # v degree 1, no deg-4 inside
            best1 = max(dpv[0][1], dpv[3][0], dpv[3][1])  # v degree 1 w/ deg-4 inside, or v degree 4
            nxt = [[NEG, NEG] for _ in range(5)]
            for d in range(5):
                for f in range(2):
                    c = cur[d][f]
                    if c == NEG:
                        continue
                    # cut edge
                    if c > nxt[d][f]:
                        nxt[d][f] = c
                    # keep edge
                    if d < 4:
                        if best0 != NEG:
                            val = c + best0
                            if val > nxt[d + 1][f]:
                                nxt[d + 1][f] = val
                        if best1 != NEG:
                            val = c + best1
                            if val > nxt[d + 1][1]:
                                nxt[d + 1][1] = val
            cur = nxt
        dpu = dp[u]
        for d in range(5):
            for f in range(2):
                dpu[d][f] = cur[d][f]
        # close component at u: u's total degree = d (no parent edge), must be 1 or 4,
        # and component must contain a degree-4 vertex (f=1 or d==4)
        for d in (1, 4):
            for f in range(2):
                if cur[d][f] != NEG and (f == 1 or d == 4):
                    if cur[d][f] > ans:
                        ans = cur[d][f]

    print(ans if ans >= 5 else -1)

main()
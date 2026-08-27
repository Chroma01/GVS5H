import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    N = int(input())
    if N == 0:
        print(-1)
        return
    adj = [[] for _ in range(N)]
    degree = [0] * N
    for _ in range(N - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)
        degree[a] += 1
        degree[b] += 1

    parent = [-1] * N
    order = []
    stack = [0]
    parent[0] = -2
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    # post-order
    for u in reversed(order):
        pass # order is preorder; we need postorder, so we'll process in reverse

    NEG_INF = -10**9
    none = [0] * N
    child1 = [1] * N  # always 1
    child4 = [NEG_INF] * N
    root1 = [NEG_INF] * N
    root4 = [NEG_INF] * N

    # Process in postorder (children before parent)
    for u in reversed(order):
        children = [v for v in adj[u] if parent[v] == u]
        # none[u]: sum of best of root1, root4, none for each child
        sum_none = 0
        for v in children:
            best = none[v]
            if root1[v] > best: best = root1[v]
            if root4[v] > best: best = root4[v]
            sum_none += best
        none[u] = sum_none

        # child4[u]
        if degree[u] >= 4:
            gains = []
            for v in children:
                # best attached value for child v (parent edge used)
                best_att = child1[v]  # child1 is always 1
                if child4[v] > best_att: best_att = child4[v]
                gain = best_att - none[v]
                gains.append(gain)
            gains.sort(reverse=True)
            top3 = gains[:3] if len(gains) >= 3 else gains
            child4[u] = 1 + sum_none + sum(top3)
        # else child4[u] remains NEG_INF

        # root1[u]: needs at least one child, and we must attach exactly one child as child4
        if children:
            best_gain = NEG_INF
            for v in children:
                if child4[v] > NEG_INF // 2:  # valid
                    gain = child4[v] - none[v]
                    if gain > best_gain:
                        best_gain = gain
            if best_gain > NEG_INF // 2:
                root1[u] = 1 + sum_none + best_gain
        # else root1[u] remains NEG_INF

        # root4[u]
        if degree[u] >= 4:
            gains = []
            for v in children:
                best_att = child1[v]
                if child4[v] > best_att: best_att = child4[v]
                gain = best_att - none[v]
                gains.append(gain)
            gains.sort(reverse=True)
            top4 = gains[:4] if len(gains) >= 4 else gains
            root4[u] = 1 + sum_none + sum(top4)
        # else root4[u] remains NEG_INF

    ans = NEG_INF
    for u in range(N):
        if root1[u] > ans: ans = root1[u]
        if root4[u] > ans: ans = root4[u]
    if ans < 1:
        print(-1)
    else:
        print(ans)

solve()
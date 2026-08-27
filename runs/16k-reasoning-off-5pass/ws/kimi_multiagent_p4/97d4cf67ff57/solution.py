import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        adj[a].append(b)
        adj[b].append(a)

    NEG = -10**18

    parent = [-1] * n
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

    A = [0] * n    # u kept, edge to parent kept; u has 0 or 3 kept children
    A4 = [NEG] * n # same, and the kept component contains a degree-4 vertex
    ans = NEG

    for u in reversed(order):
        kids = [v for v in adj[u] if v != parent[u]]
        m = len(kids)
        avals = [A[v] for v in kids]
        a4vals = [A4[v] for v in kids]

        # top-5 (value, index) by A descending
        idx = sorted(range(m), key=lambda i: -avals[i])[:5]
        top = [(avals[i], i) for i in idx]

        def sum_top(k):
            if m < k:
                return NEG
            s = 0
            for t in range(k):
                s += top[t][0]
            return s

        def sum_top_excl(k, j):
            # sum of k largest A values excluding child j
            s = 0
            cnt = 0
            for val, i in top:
                if i == j:
                    continue
                s += val
                cnt += 1
                if cnt == k:
                    return s
            return NEG

        def upgrade(k):
            # max over j with finite A4 of A4[j] + sum of top (k-1) A excluding j
            if k < 1:
                return NEG
            best = NEG
            for j in range(m):
                if a4vals[j] > NEG:
                    rest = sum_top_excl(k - 1, j) if k > 1 else 0
                    if rest > NEG:
                        cand = a4vals[j] + rest
                        if cand > best:
                            best = cand
            return best

        s3 = sum_top(3)
        # A[u]: k in {0, 3}
        best_a = 0
        if s3 > best_a:
            best_a = s3
        A[u] = 1 + best_a

        # A4[u]: k=3 (u itself degree 4) or k=3 with an upgraded child
        best_a4 = NEG
        if s3 > NEG:
            best_a4 = s3
        up3 = upgrade(3)
        if up3 > best_a4:
            best_a4 = up3
        if best_a4 > NEG:
            A4[u] = 1 + best_a4

        # C4[u]: u is top of alkane, k in {1, 4}; need a degree-4 vertex
        best_c4 = NEG
        s4 = sum_top(4)
        if s4 > NEG:  # u itself degree 4
            best_c4 = s4
        up1 = upgrade(1)
        if up1 > best_c4:
            best_c4 = up1
        up4 = upgrade(4)
        if up4 > best_c4:
            best_c4 = up4
        if best_c4 > NEG:
            cand = 1 + best_c4
            if cand > ans:
                ans = cand

    print(ans if ans > NEG else -1)

main()
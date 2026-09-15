import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n < 5:
        # The smallest alkane is K1,4 with 5 vertices.
        print(-1)
        return

    adj = [[] for _ in range(n + 1)]
    ptr = 1
    for _ in range(n - 1):
        a = int(data[ptr]); b = int(data[ptr + 1]); ptr += 2
        adj[a].append(b)
        adj[b].append(a)

    # If no vertex has degree at least 4, no alkane can exist.
    if max(len(adj[i]) for i in range(1, n + 1)) < 4:
        print(-1)
        return

    root = 1
    parent = [-1] * (n + 1)
    parent[root] = 0
    order = []
    dq = deque([root])
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            if parent[v] == -1:
                parent[v] = u
                dq.append(v)

    # down[u] = message from u to its parent: best branch hanging at u
    # (edge to parent included), where u has degree 1 or 4.
    down = [1] * (n + 1)
    for u in reversed(order):
        top1 = top2 = top3 = 0
        cnt = 0
        for v in adj[u]:
            if parent[v] == u:
                cnt += 1
                d = down[v]
                if d > top1:
                    top3 = top2
                    top2 = top1
                    top1 = d
                elif d > top2:
                    top3 = top2
                    top2 = d
                elif d > top3:
                    top3 = d
        if cnt >= 3:
            down[u] = 1 + top1 + top2 + top3

    # up[u] = message from parent[u] to u: branch at parent when edge to u is included.
    up = [0] * (n + 1)
    for u in order:
        L = []
        for v in adj[u]:
            if parent[v] == u:
                L.append((down[v], v))
        if u != root:
            L.append((up[u], -1))
        L.sort(reverse=True)
        if len(L) > 4:
            L = L[:4]
        for v in adj[u]:
            if parent[v] == u:
                s = 0
                cnt = 0
                for val, ci in L:
                    if ci == v:
                        continue
                    s += val
                    cnt += 1
                    if cnt == 3:
                        break
                if cnt == 3:
                    up[v] = 1 + s
                else:
                    up[v] = 1

    ans = -1
    for u in range(1, n + 1):
        L = []
        pu = parent[u]
        for v in adj[u]:
            if parent[v] == u:
                L.append(down[v])
            elif v == pu:
                L.append(up[u])
        if len(L) >= 4:
            L.sort(reverse=True)
            cand = 1 + L[0] + L[1] + L[2] + L[3]
            if cand > ans:
                ans = cand

    print(ans)

if __name__ == "__main__":
    main()
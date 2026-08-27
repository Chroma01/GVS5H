import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(next(it)); b = int(next(it))
        adj[a].append(b)
        adj[b].append(a)

    # Iterative post-order traversal rooted at 1 (avoids recursion limits)
    parent = [0] * (n + 1)
    order = []          # preorder; reversed gives post-order
    stack = [1]
    parent[1] = -1
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                stack.append(u)

    NEG = -10**18
    # state3[v]: best size of a partial subtree where v keeps its parent edge
    #            and exactly 3 child edges (so v has degree 4). NEG if <3 children.
    # A child u, if edge v-u is kept, contributes max(1 [u is a leaf], state3[u]).
    state3 = [NEG] * (n + 1)
    ans = NEG  # best completed alkane found so far

    for v in reversed(order):
        gains = []
        for u in adj[v]:
            if u == parent[v]:
                continue
            g = state3[u] if state3[u] > 1 else 1
            gains.append(g)
        gains.sort(reverse=True)
        if len(gains) >= 3:
            state3[v] = 1 + gains[0] + gains[1] + gains[2]
        if len(gains) >= 4:
            # Alkane whose topmost vertex is v with degree 4 (4 child edges kept)
            val = 1 + gains[0] + gains[1] + gains[2] + gains[3]
            if val > ans:
                ans = val

    # Alkane whose topmost vertex is a leaf: that leaf's unique neighbor v is a
    # degree-4 vertex using its parent edge plus exactly 3 children.
    # Size = 1 (the leaf) + state3[v], for any non-root v.
    for v in range(2, n + 1):
        if state3[v] != NEG:
            val = 1 + state3[v]
            if val > ans:
                ans = val

    print(ans if ans > 0 else -1)

main()
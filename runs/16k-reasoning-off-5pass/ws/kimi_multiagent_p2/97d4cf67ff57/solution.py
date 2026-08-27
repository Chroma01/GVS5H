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

    # Root the tree at 1 with iterative DFS, record parent and visit order.
    parent = [0] * (n + 1)
    order = []
    visited = bytearray(n + 1)
    stack = [1]
    visited[1] = 1
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if not visited[u]:
                visited[u] = 1
                parent[u] = v
                stack.append(u)

    NEG = -10**18
    # g[v]: max vertices of a valid partial alkane in v's subtree where v is
    # included AND uses its parent edge, so v must keep exactly 3 children
    # (each kept child also uses its parent edge). Invalid if < 3 children.
    g = [NEG] * (n + 1)
    ans = -1

    # Reverse pre-order guarantees children are processed before parents.
    for v in reversed(order):
        top = [0, 0, 0, 0]  # top-4 values of best[c] = max(1, g[c])
        cnt = 0
        for u in adj[v]:
            if u == parent[v]:
                continue
            cnt += 1
            val = g[u] if g[u] > 1 else 1  # child as internal node, or as leaf
            if val > top[0]:
                top[3] = top[2]; top[2] = top[1]; top[1] = top[0]; top[0] = val
            elif val > top[1]:
                top[3] = top[2]; top[2] = top[1]; top[1] = val
            elif val > top[2]:
                top[3] = top[2]; top[2] = val
            elif val > top[3]:
                top[3] = val
        if cnt >= 3:
            g[v] = 1 + top[0] + top[1] + top[2]
        if cnt >= 4:
            # v as the highest vertex of the alkane: degree 4, no parent used.
            cand = 1 + top[0] + top[1] + top[2] + top[3]
            if cand > ans:
                ans = cand

    sys.stdout.write(str(ans) + "\n")

main()
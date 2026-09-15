import sys


def solve() -> None:
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return

    n = int(line)
    adj = [[] for _ in range(n)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)

    # Only vertices with original degree at least 4 can become degree-4 vertices.
    eligible = [len(adj[i]) >= 4 for i in range(n)]

    # If there is no such vertex, no alkane exists.
    if not any(eligible):
        print(-1)
        return

    # Iterative rooting.
    parent = [-1] * n
    parent[0] = -2
    order = []
    stack = [0]

    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            stack.append(v)

    # down[u]:
    #   maximum number of eligible vertices in a connected subset inside u's
    #   rooted subtree, containing u, assuming the edge from u to its parent
    #   is selected. Then u may take at most 3 child branches.
    down = [0] * n
    best_internal = 0

    for u in reversed(order):
        if not eligible[u]:
            continue

        # Keep the four largest child branch sizes.
        t0 = t1 = t2 = t3 = 0

        for v in adj[u]:
            if parent[v] == u:
                val = down[v]
                if val > t0:
                    t3 = t2
                    t2 = t1
                    t1 = t0
                    t0 = val
                elif val > t1:
                    t3 = t2
                    t2 = t1
                    t1 = val
                elif val > t2:
                    t3 = t2
                    t2 = val
                elif val > t3:
                    t3 = val

        # If parent edge is selected, u can use at most 3 children.
        down[u] = 1 + t0 + t1 + t2

        # If u is the highest vertex of the internal set, it can use up to 4 children.
        cur = 1 + t0 + t1 + t2 + t3
        if cur > best_internal:
            best_internal = cur

    if best_internal == 0:
        print(-1)
    else:
        # For K degree-4 vertices, an alkane tree has 2K+2 leaves,
        # hence total vertices = K + (2K+2) = 3K+2.
        print(3 * best_internal + 2)


if __name__ == "__main__":
    solve()
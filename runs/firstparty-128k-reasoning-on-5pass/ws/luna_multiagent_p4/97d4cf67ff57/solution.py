import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    g = [[] for _ in range(n)]
    pos = 1
    for _ in range(n - 1):
        a = data[pos] - 1
        b = data[pos + 1] - 1
        pos += 2
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * n
    order = [0]
    parent[0] = n
    for u in order:
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    # down[u] = maximum valid arm rooted at u, using the edge u-parent[u].
    down = [1] * n
    for u in reversed(order):
        best = []
        for v in g[u]:
            if parent[v] == u:
                best.append(down[v])
        if len(best) >= 3:
            best.sort(reverse=True)
            down[u] = 1 + best[0] + best[1] + best[2]

    # up[u] = message from parent[u] to u.
    up = [1] * n
    answer = -1

    for u in order:
        # Incoming arm values from all neighbors of u.
        top = []
        if parent[u] != n:
            top.append((up[u], parent[u]))
        for v in g[u]:
            if parent[v] == u:
                top.append((down[v], v))

        top.sort(reverse=True)
        if len(top) > 4:
            top = top[:4]

        # u can be the degree-4 center, choosing its best four arms.
        if len(g[u]) >= 4:
            answer = max(answer, 1 + sum(value for value, _ in top[:4]))

        # Compute messages from u to each child.
        for child in g[u]:
            if parent[child] != u:
                continue

            selected = []
            for value, neighbor in top:
                if neighbor != child:
                    selected.append(value)
                    if len(selected) == 3:
                        break

            if len(selected) == 3:
                up[child] = 1 + selected[0] + selected[1] + selected[2]
            else:
                up[child] = 1

    print(answer)


if __name__ == "__main__":
    solve()
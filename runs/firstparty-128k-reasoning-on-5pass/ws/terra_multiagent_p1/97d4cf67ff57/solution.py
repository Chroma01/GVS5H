import sys

def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)

    eligible = [len(adj[v]) >= 4 for v in range(n)]
    if not any(eligible):
        print(-1)
        return

    parent = [-1] * n
    order = [0]
    for u in order:
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    # down[u] = directed message u -> parent[u]:
    # best skeleton size in u's side when u is connected to its parent.
    down = [0] * n

    for u in reversed(order):
        if not eligible[u]:
            continue

        best = []
        for v in adj[u]:
            if parent[v] == u and eligible[v]:
                x = down[v]
                best.append(x)
                i = len(best) - 1
                while i > 0 and best[i] > best[i - 1]:
                    best[i], best[i - 1] = best[i - 1], best[i]
                    i -= 1
                if len(best) > 3:
                    best.pop()

        down[u] = 1 + sum(best)

    # up[u] = directed message parent[u] -> u, if that endpoint is eligible.
    up = [0] * n
    best_internal_count = 1

    for u in order:
        if not eligible[u]:
            continue

        # At most four incoming branches may be selected at a top vertex.
        best4 = []

        p = parent[u]
        if p != -1 and eligible[p]:
            best4.append((up[u], p))

        for v in adj[u]:
            if parent[v] == u and eligible[v]:
                item = (down[v], v)
                best4.append(item)
                i = len(best4) - 1
                while i > 0 and best4[i][0] > best4[i - 1][0]:
                    best4[i], best4[i - 1] = best4[i - 1], best4[i]
                    i -= 1
                if len(best4) > 4:
                    best4.pop()

        best_internal_count = max(
            best_internal_count,
            1 + sum(value for value, _ in best4)
        )

        # Send messages u -> eligible child.
        for v in adj[u]:
            if parent[v] != u or not eligible[v]:
                continue

            total = 0
            taken = 0
            for value, neighbor in best4:
                if neighbor != v:
                    total += value
                    taken += 1
                    if taken == 3:
                        break
            up[v] = 1 + total

    print(3 * best_internal_count + 2)

if __name__ == "__main__":
    solve()
import sys


def solve() -> None:
    input = sys.stdin.buffer.readline
    n = int(input())
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * n
    order = [0]
    for u in order:
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    # down[u] = message u -> parent[u]
    # It is the maximum size of the selected branch on u's side
    # when edge (u, parent[u]) is selected.
    down = [1] * n
    for u in reversed(order):
        vals = [down[v] for v in g[u] if parent[v] == u]
        if len(vals) >= 3:
            vals.sort(reverse=True)
            down[u] = 1 + vals[0] + vals[1] + vals[2]

    # up[u] = message parent[u] -> u
    up = [0] * n
    ans = -1

    for u in order:
        incoming = []
        if parent[u] != -1:
            incoming.append((up[u], parent[u]))
        for v in g[u]:
            if parent[v] == u:
                incoming.append((down[v], v))

        incoming.sort(reverse=True)

        # Make u a degree-4 vertex: choose exactly four neighbor branches.
        if len(incoming) >= 4:
            total = 1 + sum(x for x, _ in incoming[:4])
            if total > ans:
                ans = total

        # Compute u -> child message by excluding that child direction.
        for v in g[u]:
            if parent[v] != u:
                continue
            total = 0
            count = 0
            for value, nei in incoming:
                if nei == v:
                    continue
                total += value
                count += 1
                if count == 3:
                    break
            up[v] = 1 + total if count == 3 else 1

    print(ans)


if __name__ == "__main__":
    solve()
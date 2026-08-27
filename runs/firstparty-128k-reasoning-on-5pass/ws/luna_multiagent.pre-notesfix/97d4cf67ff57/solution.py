import sys


def solve():
    input = sys.stdin.readline
    n = int(input())

    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)

    # Root the original tree iteratively.
    parent = [-1] * n
    order = [0]
    for v in order:
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            order.append(to)

    # Vertices usable as degree-4 vertices must have at least four
    # original neighbors.
    good = [len(adj[v]) >= 4 for v in range(n)]

    # down[v] is the best connected good-subtree contribution starting
    # at v and using the edge from v to its parent, so v can use at
    # most three child branches.
    down = [0] * n
    for v in reversed(order):
        if not good[v]:
            continue

        best = [0, 0, 0]
        for to in adj[v]:
            if parent[to] == v and good[to]:
                x = down[to]
                if x > best[0]:
                    best[2] = best[1]
                    best[1] = best[0]
                    best[0] = x
                elif x > best[1]:
                    best[2] = best[1]
                    best[1] = x
                elif x > best[2]:
                    best[2] = x
        down[v] = 1 + best[0] + best[1] + best[2]

    # up[v] is the analogous contribution from parent[v] into v.
    up = [0] * n
    answer_core = 0

    for v in order:
        if not good[v]:
            continue

        # Incoming branch values at v, tagged by the neighbor providing
        # the branch. Keep only the four largest; all values are positive.
        top = []

        if parent[v] != -1 and good[parent[v]]:
            top.append((up[v], parent[v]))

        for to in adj[v]:
            if parent[to] == v and good[to]:
                top.append((down[to], to))

        top.sort(reverse=True)
        if len(top) > 4:
            top = top[:4]

        # v is the center of a connected core; it may use up to four
        # incident core branches.
        core_size = 1 + sum(value for value, _ in top)
        if core_size > answer_core:
            answer_core = core_size

        # Send a message from v to each good child. Since that child
        # occupies one incident core edge, v may use at most three
        # other branches.
        for to in adj[v]:
            if parent[to] != v or not good[to]:
                continue

            total = 0
            used = 0
            for value, neighbor in top:
                if neighbor == to:
                    continue
                total += value
                used += 1
                if used == 3:
                    break
            up[to] = 1 + total

    if answer_core == 0:
        print(-1)
    else:
        # A core with k degree-4 vertices has exactly 2 + 2k leaves,
        # hence 3k + 2 total vertices.
        print(3 * answer_core + 2)


if __name__ == "__main__":
    solve()
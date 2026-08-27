import sys

NEG = -1


def add_top(top, value, idx, limit=4):
    if value < 0:
        return
    pos = 0
    while pos < len(top) and top[pos][0] >= value:
        pos += 1
    top.insert(pos, (value, idx))
    if len(top) > limit:
        top.pop()


def message_from_candidates(
    top, finite_count, total_count, excluded_id=None, excluded_is_finite=False
):
    """
    Return the best message for a vertex whose boundary edge is selected.

    The vertex must select exactly three additional incident edges, making
    its total selected degree four. Each selected neighboring branch can
    either be a leaf-only branch of value 1, or a finite message containing
    a degree-4 vertex.

    The returned structure always contains a degree-4 vertex: the endpoint
    of the boundary edge itself.
    """
    remaining_degree = total_count - (1 if excluded_id is not None else 0)
    finite = finite_count - (1 if excluded_is_finite else 0)

    if remaining_degree < 3:
        return NEG

    chosen = []
    for value, idx in top:
        if idx == excluded_id:
            continue
        chosen.append(value)
        if len(chosen) == 3:
            break

    take = min(3, finite)
    return 1 + sum(chosen[:take]) + (3 - take)


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # down[u]: message from u to parent[u].
    down = [NEG] * n

    for u in reversed(order):
        top = []
        finite_count = 0
        child_count = 0

        for v in graph[u]:
            if v == parent[u]:
                continue
            child_count += 1
            if down[v] >= 0:
                finite_count += 1
                add_top(top, down[v], v)

        down[u] = message_from_candidates(
            top, finite_count, child_count
        )

    # up[u]: message from parent[u] to u.
    up = [NEG] * n
    answer = -1

    for u in order:
        top = []
        finite_count = 0

        if parent[u] >= 0 and up[u] >= 0:
            finite_count += 1
            add_top(top, up[u], parent[u])

        for v in graph[u]:
            if v == parent[u]:
                continue
            if down[v] >= 0:
                finite_count += 1
                add_top(top, down[v], v)

        degree = len(graph[u])

        # u is a leaf of the selected alkane. Its selected neighbor's
        # message must already contain a degree-4 vertex.
        best_neighbor = NEG
        for v in graph[u]:
            value = up[u] if v == parent[u] else down[v]
            if value > best_neighbor:
                best_neighbor = value

        if best_neighbor >= 0:
            answer = max(answer, 1 + best_neighbor)

        # u is a degree-4 vertex. Select four incident branches. A branch
        # without a finite message is used as a leaf-only branch of value 1.
        if degree >= 4:
            selected = [value for value, _ in top[:4]]
            total = sum(selected)
            total += 4 - len(selected)
            answer = max(answer, 1 + total)

        # Compute messages from u to each child by excluding that child.
        for v in graph[u]:
            if v == parent[u]:
                continue

            up[v] = message_from_candidates(
                top,
                finite_count,
                degree,
                excluded_id=v,
                excluded_is_finite=(down[v] >= 0),
            )

    print(answer)


if __name__ == "__main__":
    solve()
import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    g = [[] for _ in range(n)]
    idx = 1
    for _ in range(n - 1):
        a = data[idx] - 1
        b = data[idx + 1] - 1
        idx += 2
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for v in order:
        for to in g[v]:
            if to != parent[v]:
                parent[to] = v
                order.append(to)

    # best_attached[v]:
    # maximum size of a valid branch rooted at v when v has a selected parent.
    # best_with4[v]:
    # same, but the branch contains at least one degree-4 vertex.
    best_attached = [1] * n
    best_with4 = [-1] * n

    answer = -1

    for v in reversed(order):
        count = 0
        b1 = b2 = b3 = b4 = 0
        max_with4_child = -1

        for to in g[v]:
            if parent[to] != v:
                continue

            value = best_attached[to]
            count += 1

            if value > b1:
                b4, b3, b2, b1 = b3, b2, b1, value
            elif value > b2:
                b4, b3, b2 = b3, b2, value
            elif value > b3:
                b4, b3 = b3, value
            elif value > b4:
                b4 = value

            if best_with4[to] > max_with4_child:
                max_with4_child = best_with4[to]

        # When attached to its parent, v has degree 1 or 4.
        # Degree 1 means no selected children and contains no degree-4 vertex.
        if count >= 3:
            best_with4[v] = 1 + b1 + b2 + b3
            best_attached[v] = best_with4[v]

        # v is the top vertex of the selected subtree, so it has degree 1 or 4.
        # Degree 1 requires exactly one child branch containing a degree-4 vertex.
        if max_with4_child != -1:
            candidate = 1 + max_with4_child
            if candidate > answer:
                answer = candidate

        # Degree 4 requires exactly four selected child branches.
        if count >= 4:
            candidate = 1 + b1 + b2 + b3 + b4
            if candidate > answer:
                answer = candidate

    print(answer)


if __name__ == "__main__":
    solve()
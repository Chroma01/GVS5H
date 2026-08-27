import sys

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

    parent = [-2] * n
    parent[0] = -1
    order = [0]

    for v in order:
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            order.append(to)

    # down[v] is the best component size on v's side when edge (v, parent[v])
    # is selected. Vertex v is then either a leaf, or has exactly 3 selected
    # edges further away from its parent.
    down = [1] * n

    for v in reversed(order):
        values = [down[to] for to in graph[v] if to != parent[v]]
        if len(values) >= 3:
            values.sort(reverse=True)
            down[v] = 1 + values[0] + values[1] + values[2]

    # up[v] is the analogous message from parent[v] to v:
    # the best component on the parent's side when edge (parent[v], v) is used.
    up = [1] * n
    answer = -1

    for v in order:
        incoming = []
        p = parent[v]

        if p != -1:
            incoming.append((up[v], p))

        for to in graph[v]:
            if to != p:
                incoming.append((down[to], to))

        incoming.sort(reverse=True)

        # Make v a degree-4 vertex: select four independently valid branches.
        if len(incoming) >= 4:
            answer = max(answer, 1 + sum(value for value, _ in incoming[:4]))

        # Send messages from v to each child. Excluding that child, v needs
        # exactly three other selected incident edges to be degree 4; otherwise
        # it can be a leaf.
        for to in graph[v]:
            if to == p:
                continue

            total = 0
            count = 0
            for value, neighbor in incoming[:4]:
                if neighbor == to:
                    continue
                total += value
                count += 1
                if count == 3:
                    break

            if count == 3:
                up[to] = 1 + total
            else:
                up[to] = 1

    print(answer)

if __name__ == "__main__":
    solve()
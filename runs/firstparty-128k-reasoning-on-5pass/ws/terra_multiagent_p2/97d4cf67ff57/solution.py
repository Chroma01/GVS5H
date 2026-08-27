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

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for v in order:
        for to in graph[v]:
            if parent[to] == -1:
                parent[to] = v
                order.append(to)

    # down[v] = message from v to parent[v]:
    # maximum size of a valid branch when edge (v, parent[v]) is selected.
    down = [1] * n

    for v in reversed(order):
        vals = []
        for to in graph[v]:
            if parent[to] == v:
                vals.append(down[to])

        if len(vals) >= 3:
            vals.sort(reverse=True)
            down[v] = max(1, 1 + vals[0] + vals[1] + vals[2])

    # up[v] = message from parent[v] to v.
    # It is unused for the root.
    up = [1] * n
    answer = -1

    for v in order:
        incoming = []

        if parent[v] >= 0:
            incoming.append((up[v], parent[v]))

        for to in graph[v]:
            if parent[to] == v:
                incoming.append((down[to], to))

        incoming.sort(reverse=True)

        # Use v as a degree-4 vertex of the final alkane.
        if len(incoming) >= 4:
            candidate = 1 + sum(value for value, _ in incoming[:4])
            if candidate > answer:
                answer = candidate

        # Compute messages from v to each child.
        for child in graph[v]:
            if parent[child] != v:
                continue

            total = 0
            count = 0
            for value, source in incoming:
                if source == child:
                    continue
                total += value
                count += 1
                if count == 3:
                    break

            if count == 3:
                up[child] = max(1, 1 + total)
            else:
                up[child] = 1

    print(answer)


if __name__ == "__main__":
    solve()
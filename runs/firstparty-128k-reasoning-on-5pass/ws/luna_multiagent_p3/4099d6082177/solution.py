import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    total = n * k
    adj = [[] for _ in range(total)]

    pos = 2
    for _ in range(total - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    # Every vertex is itself a path of one vertex.
    if k == 1:
        print("Yes")
        return

    parent = [-2] * total
    parent[0] = -1
    order = []
    stack = [0]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    # state[v] == 0: subtree of v is fully decomposed.
    # state[v] > 0: exactly one unfinished path remains, containing v,
    #                with state[v] vertices and exposed endpoint v.
    state = [0] * total

    for v in reversed(order):
        count = 0
        first = second = 0

        for to in adj[v]:
            if parent[to] != v:
                continue
            value = state[to]
            if value == 0:
                continue

            count += 1
            if count == 1:
                first = value
            elif count == 2:
                second = value
            else:
                print("No")
                return

        if count == 0:
            state[v] = 1
        elif count == 1:
            length = first + 1
            state[v] = 0 if length == k else length
        else:
            if first + second + 1 != k:
                print("No")
                return
            state[v] = 0

    print("Yes" if state[0] == 0 else "No")


if __name__ == "__main__":
    solve()
import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    total = n * k

    if k == 1:
        print("Yes")
        return

    graph = [[] for _ in range(total)]
    idx = 2
    for _ in range(total - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * total
    order = []
    stack = [0]
    parent[0] = -2

    while stack:
        v = stack.pop()
        order.append(v)
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    # state[v]:
    # 0: subtree of v is fully partitioned into K-vertex paths
    # x (1 <= x < K): exactly one unfinished x-vertex path ends at v
    state = [0] * total
    bad = False

    for v in reversed(order):
        dangling = []

        for to in graph[v]:
            if parent[to] != v:
                continue
            x = state[to]
            if x == -1:
                bad = True
                break
            if x != 0:
                dangling.append(x)

        if bad:
            break

        if len(dangling) > 2:
            bad = True
            break

        if len(dangling) == 0:
            # v must start the one segment exposed to its parent.
            state[v] = 1

        elif len(dangling) == 1:
            length = dangling[0] + 1
            if length == k:
                state[v] = 0
            elif length < k:
                state[v] = length
            else:
                bad = True
                break

        else:
            # Both child segments must be joined through v into one full path.
            if dangling[0] + dangling[1] + 1 == k:
                state[v] = 0
            else:
                bad = True
                break

    if not bad and state[0] == 0:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    solve()
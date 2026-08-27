import sys


def main():
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
    order = [0]
    parent[0] = -2

    for v in order:
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            order.append(to)

    # state[v]:
    #   0       -> subtree is fully decomposed into K-vertex paths
    #   1..K-1  -> one unfinished path fragment of this size, ending at v
    state = [0] * total

    for v in reversed(order):
        fragments = []

        for to in graph[v]:
            if parent[to] == v and state[to] != 0:
                fragments.append(state[to])

        if len(fragments) > 2:
            print("No")
            return

        if len(fragments) == 0:
            state[v] = 1

        elif len(fragments) == 1:
            length = fragments[0] + 1
            if length == k:
                state[v] = 0
            elif length < k:
                state[v] = length
            else:
                print("No")
                return

        else:
            if fragments[0] + fragments[1] + 1 != k:
                print("No")
                return
            state[v] = 0

    print("Yes" if state[0] == 0 else "No")


if __name__ == "__main__":
    main()
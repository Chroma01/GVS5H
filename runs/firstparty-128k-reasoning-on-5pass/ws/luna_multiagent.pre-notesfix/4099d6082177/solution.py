import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    V = N * K

    # For K = 1, every vertex forms a singleton path.
    if K == 1:
        print("Yes")
        return

    graph = [[] for _ in range(V)]
    idx = 2
    for _ in range(V - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at vertex 0 and obtain a traversal order.
    parent = [-2] * V
    parent[0] = -1
    order = [0]

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # open_len[u] is the length of the unique unfinished path
    # ending at u, or 0 if the subtree is fully decomposed.
    open_len = [0] * V
    possible = True

    for u in reversed(order):
        first = 0
        second = 0

        for v in graph[u]:
            if parent[v] != u:
                continue

            length = open_len[v]
            if length == 0:
                continue

            if first == 0:
                first = length
            elif second == 0:
                second = length
            else:
                possible = False
                break

        if not possible:
            break

        if first and second:
            # The two child paths and u must form one K-vertex path.
            if first + second != K - 1:
                possible = False
                break
            open_len[u] = 0
        elif first:
            # Extend the sole unfinished child path through u.
            if first + 1 == K:
                open_len[u] = 0
            else:
                open_len[u] = first + 1
        else:
            # u starts a new unfinished path.
            open_len[u] = 1

    print("Yes" if possible and open_len[0] == 0 else "No")


if __name__ == "__main__":
    solve()
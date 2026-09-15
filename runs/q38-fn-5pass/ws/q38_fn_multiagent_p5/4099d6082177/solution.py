import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    M = N * K

    # A path of one vertex is trivial for every vertex.
    if K == 1:
        print("Yes")
        return

    adj = [[] for _ in range(M)]
    idx = 2
    for _ in range(M - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    # Iterative DFS to root the tree at 0.
    parent = [-1] * M
    parent[0] = -2
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

    # sub[v] = size of the rooted subtree of v modulo K.
    sub = [1] * M
    for v in reversed(order):
        p = parent[v]
        if p >= 0:
            s = sub[p] + sub[v]
            if s >= K:
                s -= K
            sub[p] = s

    need = K - 1

    for v in range(M):
        cnt = 0
        total = 0

        for to in adj[v]:
            if parent[to] == v:
                # Component on the child side after removing v.
                rem = sub[to]
            else:
                # Component on the parent side after removing v.
                # Its size is M - subtree_size[v], and M is divisible by K.
                rem = 0 if sub[v] == 0 else K - sub[v]

            if rem:
                cnt += 1
                if cnt > 2:
                    print("No")
                    return
                total += rem

        if cnt == 1:
            if total != need:
                print("No")
                return
        elif cnt == 2:
            if total != need:
                print("No")
                return
        else:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()
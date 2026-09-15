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

    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    # Iterative DFS to get a parent array and a preorder.
    parent = [0] * (M + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    # rem[v] = 0 if subtree(v) can be fully decomposed.
    # Otherwise rem[v] is the length (number of vertices, 1..K-1)
    # of the unique unfinished path segment containing v.
    rem = [0] * (M + 1)
    bad = False

    for v in reversed(order):
        cnt = 0
        total = 0

        for to in adj[v]:
            if to == parent[v]:
                continue
            r = rem[to]
            if r > 0:
                cnt += 1
                total += r
                if cnt > 2:
                    bad = True
                    break

        if bad:
            break

        if cnt == 0:
            # Start a new unfinished segment at v and extend it upward.
            rem[v] = 1
        elif cnt == 1:
            s = total + 1
            if s == K:
                rem[v] = 0
            elif s < K:
                rem[v] = s
            else:
                bad = True
                break
        else:  # cnt == 2
            # The two child segments must be joined through v.
            # They cannot be extended to the parent.
            if total + 1 == K:
                rem[v] = 0
            else:
                bad = True
                break

    print("Yes" if (not bad and rem[1] == 0) else "No")


if __name__ == "__main__":
    solve()
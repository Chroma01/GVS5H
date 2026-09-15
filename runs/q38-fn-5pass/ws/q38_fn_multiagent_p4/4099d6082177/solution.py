import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    if len(data) < 2:
        return

    N = int(data[0])
    K = int(data[1])

    # A path of one vertex is always valid.
    if K == 1:
        print("Yes")
        return

    V = N * K

    # Robustness for malformed input; official input is always valid.
    if len(data) < 2 + 2 * (V - 1):
        print("No")
        return

    adj = [[] for _ in range(V + 1)]
    idx = 2
    for _ in range(V - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    # Iterative DFS to root the tree at 1 and get a preorder.
    parent = [0] * (V + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            if parent[to] != 0:
                continue
            parent[to] = v
            stack.append(to)

    if len(order) != V:
        print("No")
        return

    # state[v]:
    #   -1 : subtree of v cannot be handled
    #    0 : subtree of v is fully decomposed into K-vertex paths
    #    x>0 : subtree of v is fully decomposed except for one unfinished
    #          path of x vertices containing v as an endpoint; it must be
    #          extended through parent[v].
    state = [-1] * (V + 1)

    for v in reversed(order):
        cnt = 0
        a = 0
        b = 0
        ok = True

        for to in adj[v]:
            if parent[to] == v:
                st = state[to]
                if st < 0:
                    ok = False
                    break
                if st > 0:
                    cnt += 1
                    if cnt == 1:
                        a = st
                    elif cnt == 2:
                        b = st
                    else:
                        ok = False
                        break

        if not ok:
            state[v] = -1
        elif cnt == 0:
            # Start a new unfinished path at v.
            state[v] = 1
        elif cnt == 1:
            nxt = a + 1
            if nxt == K:
                state[v] = 0
            elif nxt < K:
                state[v] = nxt
            else:
                state[v] = -1
        else:  # cnt == 2
            # Two unfinished child paths can only be joined at v if they
            # form exactly one complete K-vertex path.
            if a + b + 1 == K:
                state[v] = 0
            else:
                state[v] = -1

    print("Yes" if state[1] == 0 else "No")


if __name__ == "__main__":
    solve()
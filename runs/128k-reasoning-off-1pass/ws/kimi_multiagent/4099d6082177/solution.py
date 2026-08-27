import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    V = N * K

    if K == 1:
        # Every vertex is its own path of length 1.
        sys.stdout.write("Yes\n")
        return

    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # Iterative post-order traversal from root 1.
    parent = [0] * (V + 1)
    order = []          # vertices in DFS pre-order
    stack = [1]
    parent[1] = -1
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                stack.append(u)

    # ret[v]: 0 if subtree of v fully decomposed,
    # otherwise length (1..K-1) of the single open chain ending at v
    # that must be extended upward through parent[v].
    ret = [0] * (V + 1)
    ok = True
    for v in reversed(order):
        chains = []
        for u in adj[v]:
            if u != parent[v] and ret[u] != 0:
                chains.append(ret[u])
        c = len(chains)
        if c > 2:
            ok = False
            break
        if c == 2:
            # The two open chains can only be joined through v,
            # forming a complete path of a + 1 + b vertices.
            if chains[0] + chains[1] + 1 == K:
                ret[v] = 0
            else:
                ok = False
                break
        elif c == 1:
            a = chains[0] + 1
            if a == K:
                ret[v] = 0      # path closes with v as endpoint
            else:
                ret[v] = a      # open chain extended upward
        else:
            ret[v] = 1          # v starts a fresh open chain

    if ok and ret[1] == 0:
        sys.stdout.write("Yes\n")
    else:
        sys.stdout.write("No\n")

solve()
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    V = N * K
    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # K == 1: every vertex is its own path of length 1 -> always Yes
    if K == 1:
        sys.stdout.write("Yes\n")
        return

    # Iterative DFS to get parent and post-order
    parent = [0] * (V + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if w != parent[u]:
                parent[w] = u
                stack.append(w)

    # dangling[u]: length (in vertices) of partial path ending at u going upward,
    # 0 means no dangling path; -1 means impossible
    dangling = [0] * (V + 1)
    ok = True
    for u in reversed(order):
        a = b = 0  # up to two nonzero child dangling lengths
        cnt = 0
        for w in adj[u]:
            if parent[w] == u:
                d = dangling[w]
                if d == -1:
                    ok = False
                    break
                if d != 0:
                    if cnt == 0:
                        a = d
                    elif cnt == 1:
                        b = d
                    cnt += 1
        if not ok:
            break
        if cnt >= 3:
            ok = False
            break
        elif cnt == 2:
            # pair both through u: a + b + 1 vertices must equal K
            if a + b + 1 == K:
                dangling[u] = 0
            else:
                ok = False
                break
        elif cnt == 1:
            if a + 1 == K:
                dangling[u] = 0
            else:  # a + 1 < K (a <= K-1 always)
                dangling[u] = a + 1
        else:
            dangling[u] = 1  # start a new path at u going up

    if ok and dangling[1] == 0:
        sys.stdout.write("Yes\n")
    else:
        sys.stdout.write("No\n")

solve()
import sys
sys.setrecursionlimit(100000)

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) - 1 for _ in range(N)]

    children = [[] for _ in range(N)]
    for i in range(N):
        children[A[i]].append(i)

    # Kahn peeling on functional graph to find cycle nodes.
    indeg = [len(c) for c in children]
    from collections import deque
    q = deque([u for u in range(N) if indeg[u] == 0])
    peeled = [False] * N
    peel_order = []
    while q:
        u = q.popleft()
        peeled[u] = True
        peel_order.append(u)
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    on_cycle = [not peeled[u] for u in range(N)]

    # subtree sizes over tree (non-cycle) children, for heavy-first ordering
    size = [1] * N
    for u in peel_order:
        s = 1
        for c in children[u]:
            if not on_cycle[c]:
                s += size[c]
        size[u] = s

    tree_children = [[] for _ in range(N)]
    for u in range(N):
        tc = [c for c in children[u] if not on_cycle[c]]
        tc.sort(key=lambda c: -size[c])
        tree_children[u] = tc

    def solve_tree(u):
        # h[v] = number of assignments to subtree of u with x_u <= v
        P = [1] * (M + 1)
        mod = MOD
        for c in tree_children[u]:
            h_c = solve_tree(c)
            for x in range(1, M + 1):
                P[x] = (P[x] * h_c[x]) % mod
            del h_c
        h = [0] * (M + 1)
        run = 0
        for x in range(1, M + 1):
            run += P[x]
            if run >= mod:
                run -= mod
            h[x] = run
        return h

    answer = 1
    visited_cycle = [False] * N
    mod = MOD
    for u in range(N):
        if on_cycle[u] and not visited_cycle[u]:
            cyc = []
            v = u
            while not visited_cycle[v]:
                visited_cycle[v] = True
                cyc.append(v)
                v = A[v]
            Cyc = [1] * (M + 1)
            for w in cyc:
                P = [1] * (M + 1)
                for c in tree_children[w]:
                    h_c = solve_tree(c)
                    for x in range(1, M + 1):
                        P[x] = (P[x] * h_c[x]) % mod
                    del h_c
                for x in range(1, M + 1):
                    Cyc[x] = (Cyc[x] * P[x]) % mod
            contrib = 0
            for x in range(1, M + 1):
                contrib += Cyc[x]
                if contrib >= mod:
                    contrib -= mod
            answer = (answer * contrib) % mod

    print(answer)

main()
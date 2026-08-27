import sys
from collections import deque
from array import array

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = [0] + data[2:2 + N]

    # A is a functional graph (outdegree 1): directed cycles with in-trees.
    # Constraint x_i <= x_{A_i} propagates toward the cycle, forcing all
    # nodes on a directed cycle to share one value c.

    # --- Kahn pruning: find cycle nodes; removal order is leaves -> cycle,
    # so every in-tree child is processed before its parent. ---
    indeg = [0] * (N + 1)
    for a in A[1:]:
        indeg[a] += 1

    in_cycle = [True] * (N + 1)
    q = deque(i for i in range(1, N + 1) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        in_cycle[u] = False
        order.append(u)
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    # Tree edges only (skip cycle->cycle edges; a cycle node's parent is
    # always on the same cycle, so the both-in-cycle test is exact).
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        p = A[i]
        if in_cycle[i] and in_cycle[p]:
            continue
        children[p].append(i)

    # pref[u][t] = P_u(t) = sum_{s<=t} f_u(s), where f_u(s) = #assignments
    # to u's in-subtree with x_u = s. Children w need x_w <= x_u, so
    # f_u(t) = prod_{w child of u} P_w(t).
    pref = [None] * (N + 1)
    R = range(1, M + 1)

    for u in order:
        ch = children[u]
        arr = array('i', [0]) * (M + 1)  # values < MOD < 2^31, fits int32
        if not ch:
            # Leaf: f_u(s) = 1 for every s, so P_u(t) = t.
            # (Covers M=1: P_u(1) = 1, the single all-1 assignment.)
            for t in R:
                arr[t] = t
        else:
            f = [1] * (M + 1)
            for w in ch:
                pw = pref[w]  # ready: w removed before u in Kahn order
                for t in R:
                    f[t] = (f[t] * pw[t]) % MOD
            run = 0
            for t in R:
                run += f[t]
                if run >= MOD:
                    run -= MOD
                arr[t] = run
        pref[u] = arr
        for w in ch:
            pref[w] = None  # free child tables; keeps memory O(M * frontier)

    # --- Per-cycle factor: all cycle nodes equal c, each attached tree
    # child w contributes P_w(c). Factor = sum_c prod P_w(c). ---
    seen = [False] * (N + 1)
    ans = 1
    for s in range(1, N + 1):
        if not in_cycle[s] or seen[s]:
            continue
        cyc = []
        v = s
        while not seen[v]:
            seen[v] = True
            cyc.append(v)
            v = A[v]

        comp = 0
        for c in R:
            prod = 1
            for v in cyc:
                for w in children[v]:
                    prod = (prod * pref[w][c]) % MOD
            comp += prod
            if comp >= MOD:
                comp -= MOD
        ans = (ans * comp) % MOD
        # Edge cases verified:
        #  * self-loop (N=1): no tree children, factor = sum_c 1 = M.
        #  * star into self-loop (sample 2): leaves give P_w(c)=c,
        #    factor = sum_c c^3 = 45^2 = 2025 for M=9.
        #  * M=1: every P_w(1)=1, factor=1, answer=1.

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
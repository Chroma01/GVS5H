import sys
from collections import deque

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) - 1 for _ in range(N)]          # 0‑based

    # children list and indegrees
    children = [[] for _ in range(N)]
    indeg = [0] * N
    for i, p in enumerate(A):
        children[p].append(i)
        indeg[p] += 1

    # ---- remove all vertices that are not on a directed cycle ----
    q = deque([i for i in range(N) if indeg[i] == 0])
    removed = []                     # order of removal (leaves → root)
    while q:
        v = q.popleft()
        removed.append(v)
        p = A[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    # vertices that still have indegree > 0 belong to cycles
    is_cycle = [indeg[i] > 0 for i in range(N)]

    # ---- group remaining vertices into cycles (components) ----
    visited = [False] * N
    comp_of = [-1] * N                # which component a cycle vertex belongs to
    comp_roots = []                   # list of list of tree‑roots for each component
    for i in range(N):
        if is_cycle[i] and not visited[i]:
            cur = i
            cycle_nodes = []
            while not visited[cur]:
                visited[cur] = True
                cycle_nodes.append(cur)
                cur = A[cur]
            cid = len(comp_roots)
            comp_roots.append([])
            for v in cycle_nodes:
                comp_of[v] = cid

    # ---- attach tree roots to their component ----
    for i in range(N):
        if is_cycle[i]:
            for ch in children[i]:
                if not is_cycle[ch]:          # ch is a root of a tree
                    comp_roots[comp_of[i]].append(ch)

    # ---- DP for all non‑cycle vertices (bottom‑up) ----
    pref = [None] * N                     # pref[v][k] only for non‑cycle v
    for v in removed:                     # children are already processed
        childs = children[v]              # all children are non‑cycle
        arr = [0] * (M + 1)
        cur = 0
        # for each possible maximal value k
        for k in range(1, M + 1):
            prod = 1
            for ch in childs:
                prod = (prod * pref[ch][k]) % MOD
            cur = (cur + prod) % MOD
            arr[k] = cur
        pref[v] = arr

    # ---- multiply contributions of all components ----
    answer = 1
    for roots in comp_roots:
        # product over all roots for each possible cycle value c
        comp_prod = [1] * (M + 1)          # index 0 unused
        for r in roots:
            pr = pref[r]
            for c in range(1, M + 1):
                comp_prod[c] = (comp_prod[c] * pr[c]) % MOD
        comp_sum = sum(comp_prod[1:]) % MOD
        answer = (answer * comp_sum) % MOD

    print(answer)


if __name__ == "__main__":
    solve()
import sys
sys.setrecursionlimit(10000)

def solve():
    MOD = 998244353
    N, M = map(int, input().split())
    A = [0] + list(map(int, input().split()))

    # Find cycles in the functional graph using DFS with coloring
    state = [0] * (N + 1)        # 0=unvisited, 1=visiting, 2=done
    in_cycle = [False] * (N + 1)
    cycles = []                  # list of cycles, each a list of node ids

    def dfs(u):
        if state[u] == 1:
            # Found a new cycle starting at u
            cycle = []
            v = u
            while True:
                cycle.append(v)
                v = A[v]
                if v == u:
                    break
            cycles.append(cycle)
            return
        if state[u] == 2:
            return
        state[u] = 1
        dfs(A[u])
        state[u] = 2

    for i in range(1, N + 1):
        if state[i] == 0:
            dfs(i)

    for cycle in cycles:
        for node in cycle:
            in_cycle[node] = True

    # Build tree children among non-cycle nodes
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        if not in_cycle[i] and not in_cycle[A[i]]:
            children[A[i]].append(i)

    # Compute f[u][v] for v = 0..M (f[u][v] = number of antitone maps of subtree
    # rooted at u to {1,...,v}; f[u][0] = 0 for non-empty subtree, 1 for empty)
    # f(leaf, v) = v
    # f(node, v) = sum_{r=1}^{v} prod_{c in children[node]} f(c, r)

    f_cache = [None] * (N + 1)

    def compute_f(u):
        if f_cache[u] is not None:
            return f_cache[u]
        if not children[u]:
            res = [0] + [v % MOD for v in range(1, M + 1)]
        else:
            child_fs = [compute_f(c) for c in children[u]]
            res = [0] * (M + 1)
            for v in range(1, M + 1):
                prod = 1
                for cf in child_fs:
                    prod = prod * cf[v] % MOD
                res[v] = (res[v - 1] + prod) % MOD
        f_cache[u] = res
        return res

    # For each cycle, compute its contribution
    answer = 1
    for cycle in cycles:
        comp_sum = 0
        for v in range(1, M + 1):
            prod = 1
            for cnode in cycle:
                # forest attached to cnode: direct tree-children (non-cycle)
                forest_prod = 1
                for child in children[cnode]:
                    forest_prod = forest_prod * compute_f(child)[v] % MOD
                prod = prod * forest_prod % MOD
            comp_sum = (comp_sum + prod) % MOD
        answer = answer * comp_sum % MOD

    print(answer)

solve()
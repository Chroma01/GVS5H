import sys
from collections import deque

MOD = 998244353

def solve():
    import sys
    sys.setrecursionlimit(10000)
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) - 1 for _ in range(N)]  # 0-indexed

    # Build reverse adjacency (children)
    children = [[] for _ in range(N)]
    for i, p in enumerate(A):
        children[p].append(i)

    # Find cycle nodes using topological removal
    indeg = [0] * N
    for p in A:
        indeg[p] += 1
    q = deque([i for i in range(N) if indeg[i] == 0])
    while q:
        u = q.popleft()
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)
    is_cycle = [False] * N
    for i in range(N):
        if indeg[i] > 0:
            is_cycle[i] = True

    # Build post-order list of all nodes (cycle nodes included)
    visited = [False] * N
    post_order = []
    for i in range(N):
        if is_cycle[i] and not visited[i]:
            stack = [(i, False)]
            while stack:
                u, processed = stack.pop()
                if processed:
                    post_order.append(u)
                    continue
                if visited[u]:
                    continue
                visited[u] = True
                stack.append((u, True))
                for v in children[u]:
                    if is_cycle[v]:
                        continue
                    if not visited[v]:
                        stack.append((v, False))

    # Compute dp arrays in post-order
    dp = [None] * N  # each entry will be a list of length M+1 (index 0 unused)
    for u in post_order:
        prod = [1] * (M + 1)
        for v in children[u]:
            if is_cycle[v]:
                continue
            dp_v = dp[v]
            s = 0
            # prefix sum of dp_v and multiply into prod
            for k in range(1, M + 1):
                s = (s + dp_v[k]) % MOD
                prod[k] = prod[k] * s % MOD
            # free child's dp to save memory
            dp[v] = None
        dp[u] = prod

    # Find cycles (each component's cycle)
    visited_cycle = [False] * N
    cycles = []
    for i in range(N):
        if is_cycle[i] and not visited_cycle[i]:
            cycle = []
            cur = i
            while not visited_cycle[cur]:
                visited_cycle[cur] = True
                cycle.append(cur)
                cur = A[cur]
            cycles.append(cycle)

    # Combine results per component
    ans = 1
    for cycle in cycles:
        comp = [1] * (M + 1)
        for node in cycle:
            dp_node = dp[node]
            for k in range(1, M + 1):
                comp[k] = comp[k] * dp_node[k] % MOD
        total = sum(comp[1:]) % MOD
        ans = ans * total % MOD

    print(ans)

if __name__ == "__main__":
    solve()
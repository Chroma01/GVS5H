import sys
from collections import deque

def solve():
    sys.setrecursionlimit(10000)
    MOD = 998244353
    input = sys.stdin.readline
    
    N, M = map(int, input().split())
    A = [0] + list(map(int, input().split()))
    
    # Step 1: Find cycle nodes using indegree elimination (Kahn's algorithm)
    indeg = [0] * (N + 1)
    for i in range(1, N + 1):
        indeg[A[i]] += 1
    
    is_cycle = [True] * (N + 1)
    q = deque()
    for i in range(1, N + 1):
        if indeg[i] == 0:
            q.append(i)
    
    while q:
        u = q.popleft()
        is_cycle[u] = False
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    
    # Step 2: Build reverse adjacency list (children)
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        children[A[i]].append(i)
    
    # Step 3: DFS to compute f for tree nodes (returns f array for the subtree)
    def dfs(u):
        # Compute f for all non-cycle children recursively
        child_fs = []
        for v in children[u]:
            if not is_cycle[v]:
                child_fs.append(dfs(v))
        
        if not child_fs:
            return [1] * M
        
        # Compute prefix sums for each child
        prefixes = []
        for cf in child_fs:
            pref = [0] * M
            s = 0
            for i in range(M):
                s = (s + cf[i]) % MOD
                pref[i] = s
            prefixes.append(pref)
        
        # Compute f_u: for each v, product of prefix values at v across all children
        f_u = [1] * M
        for i in range(M):
            prod = 1
            for pref in prefixes:
                prod = prod * pref[i] % MOD
            f_u[i] = prod
        return f_u
    
    # Step 4: Find cycles and compute answer
    visited_cycle = [False] * (N + 1)
    ans = 0
    
    for i in range(1, N + 1):
        if is_cycle[i] and not visited_cycle[i]:
            # Extract the cycle starting from i
            cycle = []
            cur = i
            while not visited_cycle[cur]:
                visited_cycle[cur] = True
                cycle.append(cur)
                cur = A[cur]
            
            # For each cycle node, compute f_c (considering only non-cycle children)
            # Then combine: all cycle nodes must have the same value
            prod = [1] * M
            for c in cycle:
                f_c = dfs(c)
                for v in range(M):
                    prod[v] = prod[v] * f_c[v] % MOD
            
            comp_ways = sum(prod) % MOD
            ans = (ans + comp_ways) % MOD
    
    print(ans)

solve()
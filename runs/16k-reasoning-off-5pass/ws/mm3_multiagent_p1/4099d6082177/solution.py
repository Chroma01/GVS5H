import sys
sys.setrecursionlimit(400000)

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    NK = N * K
    adj = [[] for _ in range(NK + 1)]
    for _ in range(NK - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)
    
    if K == 1:
        print("Yes")
        return
    
    def dfs(v, parent):
        total = 0
        for u in adj[v]:
            if u == parent:
                continue
            total += dfs(u, v)
        return (total + 1) % K
    
    root = 1
    if dfs(root, -1) == 0:
        print("Yes")
    else:
        print("No")

solve()
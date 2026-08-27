import sys

# Increase recursion depth to handle deep trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return
    
    num_vertices = N * K
    adj = [[] for _ in range(num_vertices + 1)]
    
    for _ in range(num_vertices - 1):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            adj[u].append(v)
            adj[v].append(u)
        except StopIteration:
            break
        
    # DFS function
    # Returns the length of the open path segment ending at u, or -1 if impossible
    # 0 means the subtree is fully covered by complete paths
    def dfs(u, p):
        children_with_open = []
        for v in adj[u]:
            if v == p:
                continue
            res = dfs(v, u)
            if res == -1:
                return -1
            if res > 0:
                children_with_open.append(res)
        
        # A node can be part of at most 2 paths (degree <= 2 in path decomposition)
        # If it connects to 2 children, it cannot connect to parent, so path must be closed
        # If it connects to 1 child, it can connect to parent (extend path)
        # If it connects to 0 children, it starts a new path
        
        if len(children_with_open) > 2:
            return -1
        
        if len(children_with_open) == 2:
            L1, L2 = children_with_open
            # Path through u is formed by two segments from children plus u itself
            if L1 + 1 + L2 == K:
                return 0
            else:
                return -1
        
        if len(children_with_open) == 1:
            L = children_with_open[0]
            new_L = L + 1
            if new_L == K:
                return 0
            elif new_L < K:
                return new_L
            else:
                return -1
        
        if len(children_with_open) == 0:
            if K == 1:
                return 0
            else:
                return 1

    result = dfs(1, -1)
    if result == 0:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
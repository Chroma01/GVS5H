import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 5:
        print(-1)
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at 1
    parent = [0] * (N + 1)
    order = []
    stack = [1]
    visited = [False] * (N + 1)
    visited[1] = True
    
    # Iterative DFS to determine order and parents
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process in reverse order (post-order)
    dp3 = [-1] * (N + 1)
    global_max = -1

    for u in reversed(order):
        child_vals = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            # val[v] = dp3[v] if dp3[v] != -1 else 1
            val = dp3[v] if dp3[v] != -1 else 1
            child_vals.append(val)
            
            # Check if u can be a leaf in an alkane
            # u connects to v, v becomes degree 4
            if dp3[v] != -1:
                size = 1 + dp3[v]
                if size > global_max:
                    global_max = size
        
        # Sort child_vals descending
        child_vals.sort(reverse=True)
        
        # Compute dp3[u] if possible
        if len(child_vals) >= 3:
            s = child_vals[0] + child_vals[1] + child_vals[2]
            dp3[u] = 1 + s
            
            # Check if u can be an internal node in an alkane (degree 4)
            if len(child_vals) >= 4:
                s4 = s + child_vals[3]
                size = 1 + s4
                if size > global_max:
                    global_max = size

    print(global_max)

if __name__ == '__main__':
    solve()
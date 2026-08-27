import sys

# Increase recursion depth to handle deep trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    total_vertices = N * K
    adj = [[] for _ in range(total_vertices + 1)]
    
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at vertex 1
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [1]
    visited = [False] * (total_vertices + 1)
    visited[1] = True
    
    # BFS/DFS to determine processing order (post-order)
    # We can use a simple stack for DFS to get an order, then reverse it for post-order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process in reverse order (bottom-up)
    # pending[u] will store the length of the pending path ending at u, or 0 if none
    pending = [0] * (total_vertices + 1)
    
    for u in reversed(order):
        # Collect pending lengths from children
        # Children are neighbors except parent
        child_pending = []
        for v in adj[u]:
            if v != parent[u]:
                if pending[v] > 0:
                    child_pending.append(pending[v])
        
        if not child_pending:
            # No pending paths from children, u starts a new path of length 1
            pending[u] = 1
        else:
            # Check conditions
            # M is the set of pending lengths that are NOT K-1
            # These cannot be completed at u unless extended
            m_values = [x for x in child_pending if x != K - 1]
            
            if len(m_values) > 1:
                # More than one path needs extension, but we can only extend one
                print("No")
                return
            elif len(m_values) == 0:
                # All children have pending paths of length K-1
                # We can extend one to complete it. The others are not extended,
                # so they remain length K-1 and cannot be completed.
                # This is only valid if there's exactly one child with a pending path.
                if len(child_pending) == 1:
                    # Extend the single child, path becomes K, completed
                    pending[u] = 0
                else:
                    # Multiple children with K-1, can only extend one, others fail
                    print("No")
                    return
            else:
                # Exactly one path needs extension (length < K-1)
                # We MUST extend this one. All other children (if any) must have length K-1
                # and will be completed.
                l = m_values[0]
                new_len = l + 1
                if new_len == K:
                    pending[u] = 0
                elif new_len < K:
                    pending[u] = new_len
                else:
                    # Should not happen if l < K-1
                    print("No")
                    return

    # After processing root, if pending[1] == 0, all paths are completed
    if pending[1] == 0:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
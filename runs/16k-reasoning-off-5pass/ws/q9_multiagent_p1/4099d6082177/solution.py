import sys

# Increase recursion depth just in case, though we will use iterative DFS
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

    total_nodes = N * K
    
    # If total nodes is not divisible by K, it's impossible (though problem constraints say NK vertices)
    # The problem states NK vertices, so total_nodes is always divisible by K.
    
    # Build adjacency list
    adj = [[] for _ in range(total_nodes + 1)]
    
    # There are total_nodes - 1 edges
    for _ in range(total_nodes - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        
    # Iterative DFS to compute subtree sizes and check the condition
    # We need a post-order traversal.
    # Stack will store (node, parent, state)
    # state 0: first visit (push children)
    # state 1: children processed (compute size)
    
    # To avoid recursion limit issues and manage state, we can use a specific stack structure.
    # Alternatively, we can generate a topological sort order (BFS from root reversed) or use a stack with explicit state.
    
    # Approach: 
    # 1. BFS to establish parent pointers and processing order (reverse BFS order is post-order).
    # 2. Iterate in reverse order to compute subtree sizes.
    
    parent = [0] * (total_nodes + 1)
    order = []
    stack = [1]
    visited = [False] * (total_nodes + 1)
    visited[1] = True
    
    # BFS to determine order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Reverse order gives us bottom-up (post-order)
    subtree_size = [1] * (total_nodes + 1)
    possible = True
    
    # Process nodes in reverse order (leaves to root)
    for u in reversed(order):
        # Check children condition
        # A child v has remainder != 0 if subtree_size[v] % K != 0
        # We need to count how many children have this property.
        # Note: In the reversed order, we process children before parents.
        # We can accumulate sizes.
        
        # However, we need to check the condition for the current node u based on its children.
        # The children of u are those v where parent[v] == u.
        # Since we are iterating in reverse order, we haven't necessarily processed all checks for u yet?
        # Actually, we process u now. We need to know the status of its children.
        # Since children appear earlier in 'reversed(order)' (later in 'order'), they are already processed.
        # But we need to count how many children have subtree_size % K != 0.
        
        # Let's optimize: instead of iterating children again, we can maintain a count or check during the loop.
        # But iterating children is O(degree), sum of degrees is O(N), so it's fine.
        
        count_non_zero = 0
        for v in adj[u]:
            if v != parent[u]:
                if subtree_size[v] % K != 0:
                    count_non_zero += 1
        
        if count_non_zero > 1:
            possible = False
            break
        
        # Add current node size to parent
        if u != 1:
            p = parent[u]
            subtree_size[p] += subtree_size[u]
            
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
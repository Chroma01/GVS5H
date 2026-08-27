import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # Total vertices
    total_vertices = N * K
    
    # If K is 1, any tree can be decomposed into N paths of length 1 (single vertices)
    if K == 1:
        print("Yes")
        return

    # Adjacency list
    adj = [[] for _ in range(total_vertices + 1)]
    
    # Read edges
    # There are total_vertices - 1 edges
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # To handle parent pointers and processing order (BFS)
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [1]
    visited = [False] * (total_vertices + 1)
    visited[1] = True
    
    # DFS to establish parent-child relationships and processing order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process in reverse order (bottom-up)
    # size[u] stores the number of vertices in the subtree rooted at u
    # rem[u] stores the length of the path segment extending from u to parent
    size = [1] * (total_vertices + 1)
    rem = [0] * (total_vertices + 1)
    
    possible = True
    
    # Iterate in reverse order (leaves to root)
    for i in range(len(order) - 1, -1, -1):
        u = order[i]
        
        if not possible:
            break
            
        # Identify children
        children = [v for v in adj[u] if v != parent[u]]
        
        # Calculate subtree size
        s = 1
        for v in children:
            s += size[v]
        
        size[u] = s
        
        r = s % K
        
        if r == 0:
            # Subtree is fully partitioned. All children must have rem == 0.
            for v in children:
                if rem[v] != 0:
                    possible = False
                    break
            if not possible:
                break
            rem[u] = 0
        else:
            # Subtree has a remainder r. We need to form a path of length r ending at u.
            if r == 1:
                # Path is just u. No child can contribute a dangling path.
                for v in children:
                    if rem[v] != 0:
                        possible = False
                        break
                if not possible:
                    break
                rem[u] = 1
            else:
                # r > 1
                # Find children with rem == r - 1
                count = 0
                child_with_rem = -1
                
                for v in children:
                    if rem[v] == r - 1:
                        count += 1
                        child_with_rem = v
                    elif rem[v] != 0:
                        # Any other child with non-zero rem is invalid
                        possible = False
                        break
                
                if not possible:
                    break
                
                if count != 1:
                    possible = False
                else:
                    rem[u] = r

    if possible and rem[1] == 0:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
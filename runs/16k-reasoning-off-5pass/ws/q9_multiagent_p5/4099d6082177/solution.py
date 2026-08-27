import sys

# Increase recursion depth to handle deep trees (up to 2*10^5 vertices)
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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
    
    # Edge case: If N*K is 0 (though constraints say >=1), handle gracefully
    if num_vertices == 0:
        print("No")
        return

    # Build adjacency list
    # Vertices are 1-indexed
    adj = [[] for _ in range(num_vertices + 1)]
    
    # Read edges
    # There are num_vertices - 1 edges
    for _ in range(num_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Global counter for paths found
    paths_found = 0
    
    # DFS function
    # Returns:
    #   -1 if invalid component detected (degree > 2 or size > K)
    #   size of the component rooted at u (if size < K)
    #   K if the component rooted at u is a valid path of size K (to be cut)
    def dfs(u, p):
        nonlocal paths_found
        current_sz = 1
        current_deg = 0
        
        for v in adj[u]:
            if v == p:
                continue
            
            res = dfs(v, u)
            
            if res == -1:
                return -1
            
            if res == K:
                # Child formed a valid path of size K. Cut it off.
                paths_found += 1
                # u does not connect to this component, so degree doesn't increase
                pass
            else:
                # res < K. Merge this component with u.
                current_sz += res
                current_deg += 1 # u connects to the root of the child component
                
                if current_sz > K:
                    return -1
                if current_deg > 2:
                    return -1
        
        # After processing all children
        if current_sz == K:
            # Check if it is a valid path
            # Condition: connected (guaranteed by construction) and max degree <= 2
            # We tracked current_deg for u. All child components were paths (max deg <= 2).
            # The connection points in child components became degree 2.
            # So if current_deg <= 2, the whole component has max degree <= 2.
            # Exception: K=1. sz=1, deg=0. Valid.
            
            if current_deg <= 2:
                paths_found += 1
                return K
            else:
                return -1
        elif current_sz < K:
            return current_sz
        else:
            # current_sz > K (should be caught inside loop, but safety check)
            return -1

    # Reset paths_found
    paths_found = 0
    
    # Start DFS from vertex 1
    root_res = dfs(1, -1)
    
    # Check results
    if root_res == -1:
        print("No")
    elif root_res == K:
        # We found N paths?
        # Total nodes = NK. Each path has K nodes.
        # If we successfully cut N-1 paths and the root forms the N-th, then paths_found should be N.
        if paths_found == N:
            print("Yes")
        else:
            # This case implies we found fewer than N paths but the root formed one?
            # Given NK vertices, if we found N-1 paths of size K, remaining is K.
            # If root forms a path of size K, total is N.
            # If paths_found != N, something is wrong with logic or input constraints.
            print("No")
    else:
        # root_res < K. Not all vertices covered by paths of size K.
        print("No")

if __name__ == '__main__':
    solve()
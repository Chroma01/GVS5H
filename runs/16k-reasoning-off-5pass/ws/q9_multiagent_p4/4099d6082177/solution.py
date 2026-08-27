import sys

# Increase recursion depth to handle deep trees (NK <= 2*10^5)
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
    
    # Edge case: If K=1, any tree with N vertices can be decomposed into N paths of length 1.
    if K == 1:
        print("Yes")
        return

    # Build adjacency list
    # Vertices are 1-indexed, so we use size total_vertices + 1
    adj = [[] for _ in range(total_vertices + 1)]
    
    # There are NK-1 edges
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # DFS function
    # Returns:
    #   -1: Impossible to decompose the subtree rooted at u
    #   L: Length of the longest path starting at u and going down into the subtree (1 <= L < K)
    #   0: The path starting at u is completed (length K)
    #
    # Logic:
    # We perform a post-order traversal. For each node u, we collect the lengths of 
    # "dangling" paths from its children. A child returns a length L < K if it has a 
    # valid path of length L starting at the child and going down, which hasn't been 
    # completed into a path of length K.
    #
    # A node u can be part of at most one path. In the path decomposition, u can have 
    # degree 1 (endpoint) or 2 (internal node).
    # - If u is an endpoint of a path going down, it connects to at most 1 child's dangling path.
    # - If u is an internal node of a path, it connects to exactly 2 children's dangling paths.
    # - If u is an endpoint of a path going up (to parent), it connects to 0 or 1 child's dangling path.
    #
    # Constraints at u:
    # 1. We cannot have more than 2 children returning dangling paths. If > 2, u would need 
    #    degree > 2 in the path graph, which is impossible.
    # 2. The total length of the path passing through u (or starting at u) must not exceed K.
    #    - If 0 children: length = 1.
    #    - If 1 child (len L): length = L + 1.
    #    - If 2 children (len L1, L2): length = L1 + 1 + L2.
    # 3. If the calculated length equals K, the path is completed. We return 0 to indicate 
    #    this to the parent (meaning u doesn't need to extend this path further).
    # 4. If the calculated length < K, we return the length. The parent will try to extend it.
    # 5. If the calculated length > K, it's impossible to form a path of length K.

    visited = [False] * (total_vertices + 1)

    def dfs(u, p):
        visited[u] = True
        dangling = []
        
        for v in adj[u]:
            if v == p:
                continue
            if visited[v]:
                continue
            
            res = dfs(v, u)
            
            if res == -1:
                return -1
            
            # If res == K, it means the path in the subtree of v is completed.
            # We don't need to connect u to v.
            if res == K:
                continue
            
            # If res < K, it's a dangling path of length res starting at v.
            # u can extend this path.
            dangling.append(res)
        
        # Logic for merging dangling paths at u
        if len(dangling) > 2:
            return -1
        
        current_len = 1 # Start with u itself
        
        if len(dangling) == 1:
            current_len = dangling[0] + 1
        elif len(dangling) == 2:
            current_len = dangling[0] + 1 + dangling[1]
        
        # Check if the path is completed
        if current_len == K:
            return 0 # Completed
        
        # If current_len > K, it's impossible to form a path of length K
        if current_len > K:
            return -1
        
        # If current_len < K, return the length
        return current_len

    # Run DFS from root (vertex 1)
    result = dfs(1, -1)
    
    # If result is 0, it means the path through root is completed (length K).
    # If result is a value < K, it means we have a dangling path of length result starting at root.
    # Since the root has no parent to extend it, this path is incomplete -> Invalid.
    # If result is -1, it's impossible.
    
    if result == 0:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()
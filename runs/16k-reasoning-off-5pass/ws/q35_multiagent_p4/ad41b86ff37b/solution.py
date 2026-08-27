import sys

def solve():
    # Increase recursion depth just in case, though we won't use deep recursion
    sys.setrecursionlimit(10**6)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N == 1:
        # A single node is a snowflake with x=0, y=0? 
        # Problem says x,y positive integers. 
        # But constraints say N >= 3. So this case is irrelevant.
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)
    
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Precompute LeafCount[u]: number of neighbors of u that are leaves in the original tree
    # A node is a leaf in the original tree if its degree is 1.
    LeafCount = [0] * (N + 1)
    for u in range(1, N + 1):
        if degree[u] == 1:
            # It's a leaf, so it contributes to LeafCount of its neighbors
            pass
    
    # Calculate LeafCount for each node
    for u in range(1, N + 1):
        count = 0
        for v in adj[u]:
            if degree[v] == 1:
                count += 1
        LeafCount[u] = count

    max_kept = 0

    # Iterate over each vertex as the potential center
    for center in range(1, N + 1):
        neighbors = adj[center]
        if not neighbors:
            # Isolated node, N=1 case handled, but N>=3 so this won't happen for center unless N=1
            continue
            
        # For each neighbor, calculate L(v, center)
        # L(v, center) is the number of leaf neighbors of v, excluding center.
        # L(v, center) = LeafCount[v] - (1 if center is a leaf neighbor of v else 0)
        # Center is a leaf neighbor of v if degree[center] == 1.
        
        is_center_leaf = (degree[center] == 1)
        
        L_values = []
        for v in neighbors:
            # If center is a leaf, it was counted in LeafCount[v], so subtract it
            val = LeafCount[v]
            if is_center_leaf:
                val -= 1
            L_values.append(val)
        
        # Sort L_values in descending order
        L_values.sort(reverse=True)
        
        m = len(L_values)
        # Check possible y values. 
        # If we pick k intermediates, we must have y <= L_values[k-1] (0-indexed).
        # To maximize 1 + k * (1 + y), we should pick y as large as possible, i.e., y = L_values[k-1].
        # We only need to check y = L_values[i] for each i from 0 to m-1.
        # Also, y must be at least 1. If L_values[i] < 1, we can't use it as an intermediate for y>=1.
        
        for i in range(m):
            y = L_values[i]
            if y < 1:
                # Since sorted descending, all subsequent are also < 1
                break
            
            # Number of intermediates we can support with this y is i + 1
            k = i + 1
            kept = 1 + k * (1 + y)
            if kept > max_kept:
                max_kept = kept

    # The answer is the minimum number of deleted vertices
    # which is N - max_kept.
    print(N - max_kept)

solve()
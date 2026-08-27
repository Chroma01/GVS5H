import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Handle edge case where N < 3 (though constraints say N >= 3)
    if N < 3:
        print(0)
        return

    # Build adjacency list
    adj = [[] for _ in range(N + 1)]
    
    # Read N-1 edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Precompute degrees
    degree = [0] * (N + 1)
    for i in range(1, N + 1):
        degree[i] = len(adj[i])

    max_kept = 0

    # Iterate over each vertex as a potential root of the Snowflake Tree
    for root in range(1, N + 1):
        # Get degrees of neighbors of the current root
        neighbor_degrees = []
        for v in adj[root]:
            neighbor_degrees.append(degree[v])
        
        # Sort in descending order to easily pick the top j neighbors
        neighbor_degrees.sort(reverse=True)
        
        num_neighbors = len(neighbor_degrees)
        
        # Try to form a Snowflake Tree with x = j intermediate nodes.
        # We select the j neighbors with the largest degrees to maximize potential leaves.
        # For a fixed j, the maximum valid number of leaves y is determined by the 
        # neighbor with the smallest degree among the selected j.
        # Constraint: y <= degree[v] - 1 for all selected v.
        # Since sorted descending, the minimum degree in the top j is neighbor_degrees[j-1].
        # So max y = neighbor_degrees[j-1] - 1.
        # We require y >= 1, so neighbor_degrees[j-1] must be >= 2.
        
        for j in range(1, num_neighbors + 1):
            d_val = neighbor_degrees[j-1]
            
            # If the degree of the j-th neighbor is less than 2, we cannot form 
            # a valid intermediate node with y >= 1 leaves.
            if d_val < 2:
                break
            
            # Calculate total kept nodes:
            # 1 (root) + j (intermediate nodes) + j * y (leaves)
            # Substituting y = d_val - 1:
            # Kept = 1 + j + j * (d_val - 1) = 1 + j * d_val
            kept = 1 + j * d_val
            if kept > max_kept:
                max_kept = kept

    # The answer is the total vertices minus the maximum vertices we can keep
    print(N - max_kept)

if __name__ == '__main__':
    solve()
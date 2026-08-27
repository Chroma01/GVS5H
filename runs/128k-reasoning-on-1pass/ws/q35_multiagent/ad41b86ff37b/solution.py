import sys

def solve():
    # Use fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
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

    max_snowflake_size = 0
    
    # Iterate over each vertex as the potential center of the Snowflake Tree
    for center in range(1, N + 1):
        # Collect available leaves for each neighbor (potential hub)
        # A neighbor v can be a hub if it has at least 1 other neighbor besides center
        # Number of leaves it can support is degree[v] - 1
        neighbor_avail_leaves = []
        for neighbor in adj[center]:
            avail = degree[neighbor] - 1
            if avail >= 1:
                neighbor_avail_leaves.append(avail)
        
        # Sort descending to pick hubs with most available leaves first
        neighbor_avail_leaves.sort(reverse=True)
        
        # Try all possible number of hubs x
        # x ranges from 1 to the number of valid neighbors
        for x in range(1, len(neighbor_avail_leaves) + 1):
            # The number of leaves y is limited by the hub with fewest available leaves
            # Since we sorted descending, the x-th hub (index x-1) has the minimum among top x
            y = neighbor_avail_leaves[x-1]
            
            # Total vertices in Snowflake: 1 (center) + x (hubs) + x * y (leaves)
            # Simplifies to 1 + x * (1 + y)
            current_size = 1 + x * (1 + y)
            
            if current_size > max_snowflake_size:
                max_snowflake_size = current_size

    # The minimum number of vertices to delete is N - max_snowflake_size
    print(N - max_snowflake_size)

if __name__ == '__main__':
    solve()
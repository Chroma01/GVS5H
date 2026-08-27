import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Constraints say 3 <= N, but handle small cases gracefully
    if N < 3:
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

    max_kept = 0

    # Iterate over each node as the potential root of the Snowflake Tree
    for r in range(1, N + 1):
        # Collect degrees of all neighbors of r
        neighbor_degrees = []
        for v in adj[r]:
            neighbor_degrees.append(degree[v])
        
        if not neighbor_degrees:
            continue
            
        # Sort neighbor degrees to efficiently count how many are >= y+1
        neighbor_degrees.sort()
        
        # We need to find max(1 + x + x*y)
        # where y = d - 1, and x is the count of neighbors with degree >= d.
        # d must be one of the values in neighbor_degrees.
        # y must be a positive integer, so d >= 2.
        
        n_neighbors = len(neighbor_degrees)
        
        # Iterate from the largest degree downwards
        for i in range(n_neighbors - 1, -1, -1):
            d = neighbor_degrees[i]
            
            # y must be >= 1, so d must be >= 2
            if d < 2:
                break
            
            # x is the number of neighbors with degree >= d
            # Since the list is sorted, all elements from index i to end are >= d
            x = n_neighbors - i
            
            y = d - 1
            
            # Calculate size of snowflake: 1 (root) + x (hubs) + x * y (leaves)
            current_size = 1 + x + x * y
            if current_size > max_kept:
                max_kept = current_size

    # The answer is the minimum number of vertices to delete.
    print(N - max_kept)

if __name__ == '__main__':
    solve()
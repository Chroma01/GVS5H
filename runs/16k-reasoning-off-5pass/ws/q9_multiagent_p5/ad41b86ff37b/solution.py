import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300005)

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

    if N == 0:
        print(0)
        return

    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)

    # Read N-1 edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    max_kept = 0

    # Iterate over each vertex as a potential center (root)
    for root in range(1, N + 1):
        # Collect degrees of neighbors minus 1 (since one edge connects to root)
        # A neighbor u can have at most degree[u] - 1 leaves attached to it in the subgraph.
        neighbor_leaves = []
        for u in adj[root]:
            neighbor_leaves.append(degree[u] - 1)
        
        # Sort descending to greedily pick the best branches
        neighbor_leaves.sort(reverse=True)
        
        # If no neighbors, we can't form a snowflake (requires x >= 1)
        if not neighbor_leaves:
            continue
            
        # Iterate over possible number of branches x
        # x corresponds to the number of neighbors we choose.
        # To maximize the snowflake size for a fixed x, we pick the x neighbors
        # with the highest available leaf counts.
        # Then y is determined by the minimum leaf count among these x neighbors.
        # Since we sorted descending, if we pick x neighbors (indices 0 to x-1),
        # the minimum is at index x-1.
        
        # We must ensure y >= 1. If neighbor_leaves[i] == 0, we cannot form a valid snowflake
        # with x = i+1 branches where the bottleneck is 0.
        
        for i in range(len(neighbor_leaves)):
            x = i + 1
            y = neighbor_leaves[i]
            
            if y < 1:
                # Since list is sorted descending, if current y is 0, all subsequent are 0.
                # We can stop early.
                break
            
            # Size of snowflake: 1 (root) + x (branches) + x*y (leaves)
            current_kept = 1 + x + x * y
            if current_kept > max_kept:
                max_kept = current_kept

    # The answer is the minimum number of vertices to delete
    print(N - max_kept)

if __name__ == '__main__':
    solve()
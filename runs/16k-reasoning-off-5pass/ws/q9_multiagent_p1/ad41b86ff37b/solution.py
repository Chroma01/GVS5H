import sys

# Increase recursion depth just in case, though we use an iterative approach
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

    # Constraints say N >= 3, but handle N=1 gracefully if needed
    if N == 1:
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    
    # Read edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Step 1: Identify leaves (degree 1)
    degree = [0] * (N + 1)
    for i in range(1, N + 1):
        degree[i] = len(adj[i])

    is_leaf = [False] * (N + 1)
    for i in range(1, N + 1):
        if degree[i] == 1:
            is_leaf[i] = True

    # Step 2: For each node u, compute L_v for each neighbor v.
    # L_v = number of leaf neighbors of v.
    leaf_counts = [0] * (N + 1)
    for v in range(1, N + 1):
        count = 0
        for neighbor in adj[v]:
            if is_leaf[neighbor]:
                count += 1
        leaf_counts[v] = count

    # Step 3: Iterate over each node as a potential root.
    # Collect leaf_counts of its neighbors, sort descending, and calculate max size.
    max_snowflake_size = 0

    for root in range(1, N + 1):
        # Collect leaf counts of neighbors
        neighbor_leaf_counts = []
        for neighbor in adj[root]:
            neighbor_leaf_counts.append(leaf_counts[neighbor])
        
        # Sort in descending order
        neighbor_leaf_counts.sort(reverse=True)
        
        # Filter out neighbors that don't have any leaves (since y must be >= 1)
        # Since the list is sorted descending, we can just take the prefix where count >= 1
        # However, filtering is safer for logic clarity.
        valid_counts = [c for c in neighbor_leaf_counts if c >= 1]
        
        if not valid_counts:
            continue
            
        # Iterate k from 1 to len(valid_counts)
        # We choose x = k neighbors.
        # To maximize size for a fixed k, we should pick the largest possible y.
        # Since we picked the top k neighbors with the largest leaf counts,
        # the limiting factor for y is the k-th largest count (index k-1).
        # So y = valid_counts[k-1].
        # The size is 1 + x + x*y.
        
        for k in range(1, len(valid_counts) + 1):
            x = k
            y = valid_counts[k-1]
            current_size = 1 + x + x * y
            if current_size > max_snowflake_size:
                max_snowflake_size = current_size

    # The answer is the minimum number of vertices to delete.
    print(N - max_snowflake_size)

if __name__ == '__main__':
    solve()
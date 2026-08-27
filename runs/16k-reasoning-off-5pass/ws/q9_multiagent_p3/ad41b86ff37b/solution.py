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

    if N == 1:
        # A single node is a snowflake tree with x=1, y=0? 
        # Problem says x, y are positive integers. 
        # However, constraints say N >= 3. So this case is not possible per constraints.
        # But if N=1 was possible, answer is 0.
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

    # Iterate over each node as a potential root
    for r in range(1, N + 1):
        # Collect degrees of neighbors
        neighbor_degrees = []
        for v in adj[r]:
            neighbor_degrees.append(degree[v])
        
        # Sort descending to easily pick top x neighbors
        neighbor_degrees.sort(reverse=True)
        
        num_neighbors = len(neighbor_degrees)
        
        # We need to choose x intermediates. 
        # If we choose x intermediates, we need y such that at least x neighbors have degree >= y+1.
        # To maximize 1 + x*(1+y), for a fixed x, we want the largest possible y.
        # The largest y satisfying the condition is y = neighbor_degrees[x-1] - 1.
        # We must have y >= 1, so neighbor_degrees[x-1] >= 2.
        
        # Iterate x from 1 to num_neighbors
        for x in range(1, num_neighbors + 1):
            # The x-th largest degree (0-indexed x-1)
            d_val = neighbor_degrees[x-1]
            
            # We need y >= 1. The constraint is degree >= y+1 => y <= degree - 1.
            # Max y = d_val - 1.
            if d_val >= 2:
                y = d_val - 1
                # Calculate kept nodes: 1 (root) + x (intermediates) + x*y (leaves)
                kept = 1 + x * (1 + y)
                if kept > max_kept:
                    max_kept = kept
            else:
                # If the x-th largest degree is < 2, then for any larger x, 
                # the degree will also be < 2 (since sorted descending).
                # So we can stop early.
                break

    # The answer is the minimum deletions
    print(N - max_kept)

if __name__ == '__main__':
    solve()
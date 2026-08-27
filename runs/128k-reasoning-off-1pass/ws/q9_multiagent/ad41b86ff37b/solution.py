import sys
import bisect

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

    # Constraints say N >= 3, but handle edge cases
    if N <= 1:
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

    max_snowflake_size = 0

    # Iterate over each vertex as the potential center
    for u in range(1, N + 1):
        # Collect degrees of neighbors
        neighbor_degrees = [degree[v] for v in adj[u]]
        
        # Sort ascending for binary search
        neighbor_degrees.sort()
        
        # We want to maximize 1 + x * (1 + y)
        # where x is the number of neighbors with degree >= y + 1.
        # y must be >= 1.
        # The optimal y for a fixed set of neighbors will always be of the form d-1
        # where d is the degree of one of the neighbors (specifically the smallest degree
        # among the selected x neighbors).
        # So we only need to check y = d - 1 for each unique degree d present in neighbor_degrees.
        # Condition: y >= 1 => d >= 2.
        
        # Get unique degrees >= 2
        unique_d = sorted(list(set(d for d in neighbor_degrees if d >= 2)))
        
        for d in unique_d:
            # If we choose y = d - 1, then we need neighbors with degree >= y + 1 = d.
            # x is the count of such neighbors.
            
            # Find the first index where degree >= d
            idx = bisect.bisect_left(neighbor_degrees, d)
            x = len(neighbor_degrees) - idx
            
            if x > 0:
                current_size = 1 + x * (1 + (d - 1))
                if current_size > max_snowflake_size:
                    max_snowflake_size = current_size

    # The answer is N - max_snowflake_size
    print(N - max_snowflake_size)

if __name__ == '__main__':
    solve()
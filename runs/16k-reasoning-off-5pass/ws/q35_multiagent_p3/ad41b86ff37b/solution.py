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

    if N < 3:
        # Constraints say N >= 3, but handle gracefully
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
    for c in range(1, N + 1):
        # Collect d_v = degree(v) - 1 for all neighbors v of c
        neighbor_caps = []
        for v in adj[c]:
            cap = degree[v] - 1
            if cap >= 1:
                neighbor_caps.append(cap)
        
        if not neighbor_caps:
            continue
            
        # Sort in descending order
        neighbor_caps.sort(reverse=True)
        
        # For each possible k (number of intermediate nodes),
        # the maximum y we can support is neighbor_caps[k-1]
        # because we need k neighbors each having at least y leaves.
        # The bottleneck is the k-th largest capacity.
        
        # We iterate k from 1 to len(neighbor_caps)
        # Size = 1 + k * (1 + y)
        # y = neighbor_caps[k-1]
        
        for k in range(1, len(neighbor_caps) + 1):
            y = neighbor_caps[k-1]
            # x = k
            size = 1 + k * (1 + y)
            if size > max_snowflake_size:
                max_snowflake_size = size

    # The answer is the number of deleted vertices
    ans = N - max_snowflake_size
    print(ans)

if __name__ == '__main__':
    solve()
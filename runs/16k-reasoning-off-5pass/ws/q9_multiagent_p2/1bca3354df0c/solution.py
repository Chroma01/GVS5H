import sys

# Increase recursion depth for deep DFS if necessary, though iterative BFS is safer
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Build adjacency list
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        
    # Count connected components using BFS
    visited = [False] * (N + 1)
    components = 0
    
    for i in range(1, N + 1):
        if not visited[i]:
            components += 1
            # Start BFS
            queue = [i]
            visited[i] = True
            while queue:
                u = queue.pop(0)
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        
    # Determine winner based on the number of components
    # Logic:
    # If components == 1 (2^0), Aoki wins (k=0 even)
    # If components == 2 (2^1), Takahashi wins (k=1 odd)
    # If components == 4 (2^2), Aoki wins (k=2 even)
    # If components is a power of 2 (2^k):
    #    If k is even -> Aoki
    #    If k is odd -> Takahashi
    # If components is NOT a power of 2 -> Aoki
    
    is_power_of_2 = (components > 0) and ((components & (components - 1)) == 0)
    
    if is_power_of_2:
        # Calculate k such that components = 2^k
        # Since components is power of 2, k = log2(components)
        # We can check parity of k by checking if components is divisible by 4?
        # No, 2^0=1 (k=0 even), 2^1=2 (k=1 odd), 2^2=4 (k=2 even), 2^3=8 (k=3 odd).
        # Pattern: 1, 2, 4, 8, 16...
        # k even: 1, 4, 16... (components % 4 == 1? No, 1%4=1, 4%4=0, 16%4=0)
        # k odd: 2, 8, 32... (components % 4 == 0? No, 2%4=2, 8%4=0)
        # Actually, simply count trailing zeros or use bit_length.
        # k = components.bit_length() - 1
        k = components.bit_length() - 1
        if k % 2 == 0:
            print("Aoki")
        else:
            print("Takahashi")
    else:
        print("Aoki")

if __name__ == '__main__':
    solve()
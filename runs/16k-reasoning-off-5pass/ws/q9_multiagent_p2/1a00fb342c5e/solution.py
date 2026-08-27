import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list: adj[u] = [(v, z), ...]
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        z = int(next(iterator))
        adj[u].append((v, z))
        adj[v].append((u, z))

    # Array to store the determined value for each node
    # Initialize with -1 to indicate unvisited
    A = [-1] * (N + 1)
    
    # Process each connected component
    for i in range(1, N + 1):
        if A[i] == -1:
            # Start a new component
            # We assign A[i] = 0 arbitrarily for the base calculation
            A[i] = 0
            
            # BFS to propagate values and check consistency
            queue = [i]
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                
                for v, z in adj[u]:
                    if A[v] == -1:
                        A[v] = A[u] ^ z
                        queue.append(v)
                    else:
                        # Check consistency
                        if A[v] != (A[u] ^ z):
                            print("-1")
                            return
            
    # Now compute optimal K for each component and update A
    # Max Z is 10^9, which is < 2^30. We check bits 0 to 29.
    # 10^9 fits in 30 bits (2^29 is approx 5.3e8, 2^30 is approx 1.07e9).
    
    for i in range(1, N + 1):
        if A[i] == -1:
            # This node was not visited, meaning it's an isolated node with no constraints
            # The value should be 0 to minimize sum.
            A[i] = 0
            continue
            
        # Collect nodes in the component starting from i
        # Since we didn't store components explicitly, we re-traverse or use a visited flag logic.
        # Actually, the previous loop visited everything. If A[i] != -1, it belongs to a component.
        # We need to identify the component to calculate K.
        # Let's use a simple BFS again to collect the component nodes.
        
        comp_nodes = []
        q = [i]
        visited_in_comp = {i}
        head = 0
        while head < len(q):
            u = q[head]
            head += 1
            comp_nodes.append(u)
            for v, z in adj[u]:
                if A[v] != -1 and v not in visited_in_comp:
                    visited_in_comp.add(v)
                    q.append(v)
        
        # Count set bits for each position across all nodes in the component
        bit_counts = [0] * 30
        
        for node in comp_nodes:
            val = A[node]
            for b in range(30):
                if (val >> b) & 1:
                    bit_counts[b] += 1
        
        # Determine K to minimize sum
        K = 0
        for b in range(30):
            count_ones = bit_counts[b]
            count_zeros = len(comp_nodes) - count_ones
            # If having bit 1 in K flips more 1s to 0s than 0s to 1s, choose 1
            # i.e., if count_ones > count_zeros, setting bit to 1 reduces total sum
            if count_ones > count_zeros:
                K |= (1 << b)
        
        # Apply K to all nodes in component
        for node in comp_nodes:
            A[node] ^= K

    # Output the result
    # A is 1-indexed, we need to print A[1]...A[N]
    print(*(A[1:]))

if __name__ == '__main__':
    solve()
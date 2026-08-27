import sys
from collections import deque

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

    # Build adjacency list
    # adj[u] = list of (v, z) meaning A[u] ^ A[v] = z
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        z = int(next(iterator))
        adj[u].append((v, z))
        adj[v].append((u, z))

    # Arrays to store relative XOR distances from the root of each component
    # dist[i] stores the XOR sum from the root of the component containing i to i
    dist = [-1] * (N + 1)
    # To store which component each node belongs to, or just process component by component
    # We'll use a visited array implicitly via dist != -1
    
    # Result array
    A = [0] * (N + 1)
    
    # Process each connected component
    for start_node in range(1, N + 1):
        if dist[start_node] != -1:
            continue
            
        # Start a new component
        component_nodes = []
        queue = deque([start_node])
        dist[start_node] = 0
        component_nodes.append(start_node)
        
        # BFS to traverse the component and check for consistency
        is_consistent = True
        head = 0
        while head < len(component_nodes):
            u = component_nodes[head]
            head += 1
            
            for v, z in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] ^ z
                    component_nodes.append(v)
                else:
                    # Check consistency
                    if dist[v] != (dist[u] ^ z):
                        print("-1")
                        return
        
        # Now determine the optimal root value for this component
        # For each bit position, count how many nodes have that bit set in their dist value
        # We want to choose root R such that sum(R ^ dist[v]) is minimized
        
        # Max possible Z is 10^9, which is less than 2^30. So check bits 0 to 29.
        # But A_i can be larger? No, we minimize sum, so we won't pick unnecessarily large bits.
        # Actually, since we can choose R freely, and bits are independent, we only need to check
        # up to the maximum bit present in any Z or implied by the structure.
        # 10^9 < 2^30, so 30 bits (0..29) are sufficient. Let's go up to 30 just to be safe.
        
        num_bits = 30
        component_size = len(component_nodes)
        
        # Count c0 and c1 for each bit position in the component's dist values
        # c1[b] = number of nodes in component where b-th bit of dist[v] is 1
        # c0[b] = component_size - c1[b]
        
        c1 = [0] * num_bits
        
        for v in component_nodes:
            d = dist[v]
            for b in range(num_bits):
                if (d >> b) & 1:
                    c1[b] += 1
        
        # Determine optimal R
        R = 0
        for b in range(num_bits):
            cnt1 = c1[b]
            cnt0 = component_size - cnt1
            # If we set b-th bit of R to 0: contribution is cnt1 * 2^b
            # If we set b-th bit of R to 1: contribution is cnt0 * 2^b
            # Choose 1 if cnt0 < cnt1, else 0. If equal, 0 is fine (minimizes value too).
            if cnt0 < cnt1:
                R |= (1 << b)
        
        # Assign final values to nodes in the component
        for v in component_nodes:
            A[v] = R ^ dist[v]

    # Output the result
    print(" ".join(str(A[i]) for i in range(1, N + 1)))

solve()
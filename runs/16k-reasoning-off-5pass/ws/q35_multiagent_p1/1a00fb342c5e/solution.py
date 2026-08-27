import sys

def solve():
    # Increase recursion depth just in case, though we will use iterative BFS/DFS
    sys.setrecursionlimit(300000)
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

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
        adj[v].append((u, w))

    # relative_val[i] stores the XOR sum from the root of the component to node i
    relative_val = [-1] * (N + 1)
    visited = [False] * (N + 1)
    
    # Components will be stored as lists of nodes
    components = []
    
    for i in range(1, N + 1):
        if not visited[i]:
            comp_nodes = []
            stack = [i]
            visited[i] = True
            relative_val[i] = 0
            comp_nodes.append(i)
            
            # BFS/DFS to traverse the component and check consistency
            # Using a stack for DFS
            idx = 0
            while idx < len(stack):
                u = stack[idx]
                idx += 1
                
                for v, w in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        relative_val[v] = relative_val[u] ^ w
                        stack.append(v)
                        comp_nodes.append(v)
                    else:
                        # Check consistency
                        if relative_val[v] != (relative_val[u] ^ w):
                            print("-1")
                            return
            
            components.append(comp_nodes)

    # Now determine the optimal root bit for each component and each bit position
    # We'll build the final answer array
    ans = [0] * (N + 1)
    
    # Max value of Z_i is 10^9, which is less than 2^30. So bits 0 to 29 are sufficient.
    # 2^29 = 536,870,912; 2^30 = 1,073,741,824. So 30 bits (0..29) cover up to ~10^9.
    # Let's use 31 bits to be safe (0..30).
    MAX_BIT = 31
    
    for comp in components:
        # For each bit position, count how many nodes have relative bit 0 and 1
        # If we set root bit to 0, nodes with relative bit 1 will have final bit 1.
        # If we set root bit to 1, nodes with relative bit 0 will have final bit 1.
        # We want to minimize the number of 1s at each bit position.
        
        # Count relative bits for this component
        # rel_bit_count[k][0] = count of nodes with k-th relative bit 0
        # rel_bit_count[k][1] = count of nodes with k-th relative bit 1
        # Since we process bit by bit, we can just compute counts on the fly or store them.
        # Given N up to 2*10^5 and 31 bits, storing counts is efficient.
        
        # Let's compute the counts for each bit
        bit_counts = [[0, 0] for _ in range(MAX_BIT)]
        
        for node in comp:
            val = relative_val[node]
            for k in range(MAX_BIT):
                if (val >> k) & 1:
                    bit_counts[k][1] += 1
                else:
                    bit_counts[k][0] += 1
        
        # Determine optimal root bit for each bit position
        # root_bit[k] = 0 or 1
        root_bits = [0] * MAX_BIT
        
        for k in range(MAX_BIT):
            c0 = bit_counts[k][0]
            c1 = bit_counts[k][1]
            # If root bit is 0, number of 1s is c1
            # If root bit is 1, number of 1s is c0
            # Choose root bit to minimize number of 1s
            if c1 <= c0:
                root_bits[k] = 0
            else:
                root_bits[k] = 1
        
        # Construct the final values for nodes in this component
        for node in comp:
            val = 0
            rel = relative_val[node]
            for k in range(MAX_BIT):
                rel_bit = (rel >> k) & 1
                final_bit = rel_bit ^ root_bits[k]
                if final_bit:
                    val |= (1 << k)
            ans[node] = val

    # Output the result
    print(" ".join(map(str, ans[1:])))

solve()
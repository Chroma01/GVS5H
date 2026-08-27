import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list for the graph
    # Nodes are 1-indexed, so size N + 1
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * (N + 1)
    val = [0] * (N + 1)
    result = [0] * (N + 1)
    
    possible = True
    
    # Process each connected component
    for i in range(1, N + 1):
        if visited[i]:
            continue
        
        # Start BFS for this component
        component_nodes = []
        q = [i]
        visited[i] = True
        val[i] = 0
        component_nodes.append(i)
        
        idx = 0
        while idx < len(q):
            u = q[idx]
            idx += 1
            
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    val[v] = val[u] ^ w
                    q.append(v)
                    component_nodes.append(v)
                else:
                    # Check consistency for back-edge or cross-edge
                    if val[u] ^ val[v] != w:
                        possible = False
                        break
            if not possible:
                break
        
        if not possible:
            break
        
        # If consistent, find optimal C for this component to minimize sum(val[u] ^ C)
        # We optimize each bit of C independently.
        # For bit k, if count of 0s > count of 1s in val[u], set C_k = 0.
        # Else set C_k = 1.
        
        # Max Z is 10^9 < 2^30, so we check bits 0 to 29
        bit_counts = [0] * 30
        
        for u in component_nodes:
            v_u = val[u]
            for k in range(30):
                if (v_u >> k) & 1:
                    bit_counts[k] += 1
        
        # Construct C
        C = 0
        for k in range(30):
            cnt_1 = bit_counts[k]
            cnt_0 = len(component_nodes) - cnt_1
            # We want to minimize (cnt_1 if C_k=0 else cnt_0) * 2^k
            # So choose C_k=1 if cnt_0 < cnt_1
            if cnt_0 < cnt_1:
                C |= (1 << k)
        
        # Apply C to all nodes in component
        for u in component_nodes:
            result[u] = val[u] ^ C

    if not possible:
        print("-1")
    else:
        # Output results for indices 1 to N
        print(*(result[1:]))

if __name__ == '__main__':
    solve()
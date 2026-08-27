import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator))
            adj[u].append((v, w))
            adj[v].append((u, w))
        except StopIteration:
            break

    D = [-1] * (N + 1)
    A = [0] * (N + 1)
    
    # Process each connected component
    for i in range(1, N + 1):
        if D[i] != -1:
            continue
        
        # BFS initialization
        queue = [i]
        D[i] = 0
        
        head = 0
        component_nodes = []
        
        while head < len(queue):
            u = queue[head]
            head += 1
            component_nodes.append(u)
            
            current_D_u = D[u]
            
            for v, w in adj[u]:
                if D[v] == -1:
                    D[v] = current_D_u ^ w
                    queue.append(v)
                else:
                    # Check consistency
                    if D[u] ^ D[v] != w:
                        print("-1")
                        return
        
        # Determine optimal base B for this component
        # We want to minimize sum of (B ^ D[u]) for u in component_nodes
        # Analyze bit by bit
        
        B = 0
        comp_size = len(component_nodes)
        
        # Count ones for each bit position in one pass
        # Max Z is 10^9, which is less than 2^30. 
        # We check up to 30 bits.
        bit_counts = [0] * 30
        for u in component_nodes:
            val = D[u]
            for b in range(30):
                if (val >> b) & 1:
                    bit_counts[b] += 1
        
        for b in range(30):
            # If more ones than zeros, we should flip bits (set B's bit to 1)
            # to minimize the total sum.
            # count_zeros = comp_size - bit_counts[b]
            # We choose B's bit to 1 if count_zeros < count_ones
            # <=> comp_size - bit_counts[b] < bit_counts[b]
            # <=> comp_size < 2 * bit_counts[b]
            if 2 * bit_counts[b] > comp_size:
                B |= (1 << b)
        
        # Assign final values
        for u in component_nodes:
            A[u] = B ^ D[u]

    # Output result
    print(' '.join(map(str, A[1:])))

if __name__ == '__main__':
    solve()
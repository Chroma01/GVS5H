import sys

def solve():
    # Increase recursion depth just in case, though we'll use iterative BFS/DFS
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
        
    # V[u] stores the relative value of node u with respect to the root of its component
    V = [-1] * (N + 1)
    # component_id[u] stores the component identifier for node u
    component_id = [-1] * (N + 1)
    
    # List to store nodes in each component
    components = []
    
    # To store the optimal C for each component
    # We'll map component index to C value
    comp_C = {}
    
    comp_idx = 0
    
    for i in range(1, N + 1):
        if V[i] != -1:
            continue
            
        # Start a new component
        nodes_in_comp = []
        queue = [i]
        V[i] = 0
        component_id[i] = comp_idx
        nodes_in_comp.append(i)
        
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            
            for v, w in adj[u]:
                if V[v] == -1:
                    V[v] = V[u] ^ w
                    component_id[v] = comp_idx
                    nodes_in_comp.append(v)
                    queue.append(v)
                else:
                    # Check consistency
                    if V[v] != (V[u] ^ w):
                        print("-1")
                        return
        
        components.append(nodes_in_comp)
        
        # Determine optimal C for this component
        # For each bit position, count how many nodes have that bit set in V
        # We need to check up to 30 bits since Z_i <= 10^9 < 2^30
        size = len(nodes_in_comp)
        C = 0
        
        for bit in range(30):
            cnt = 0
            for node in nodes_in_comp:
                if (V[node] >> bit) & 1:
                    cnt += 1
            
            # If more than half have the bit set, setting C's bit to 1 will flip them to 0
            # and the rest (size - cnt) will become 1.
            # We want to minimize the number of 1s at this bit position.
            # Number of 1s if C_bit = 0: cnt
            # Number of 1s if C_bit = 1: size - cnt
            if cnt > size - cnt:
                C |= (1 << bit)
                
        comp_C[comp_idx] = C
        comp_idx += 1
        
    # Construct the final answer
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        cid = component_id[i]
        C = comp_C[cid]
        A[i] = V[i] ^ C
        
    print(" ".join(map(str, A[1:])))

solve()
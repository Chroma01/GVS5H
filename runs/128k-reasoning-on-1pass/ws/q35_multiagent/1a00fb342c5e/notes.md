
## ideation
```python
import sys

# Increase recursion depth just in case, though we use iterative approach
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
        while head < len(queue):
            u = queue[head]
            head += 1
            
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
        # We want to minimize sum of (B ^ D[u]) for u in queue
        # Analyze bit by bit
        
        B = 0
        # Max Z is 10^9, which is less than 2^30. 
        # We check up to 30 bits.
        for bit in range(30):
            count_ones = 0
            for u in queue:
                if (D[u] >> bit) & 1:
                    count_ones += 1
            
            count_zeros = len(queue) - count_ones
            
            # If setting B's bit to 1 results in fewer 1s in the sum, choose 1.
            # B_bit = 1 => term is (1 ^ D_u_bit). 
            # If D_u_bit is 0, result is 1. If D_u_bit is 1, result is 0.
            # So number of 1s contributed by this bit position if B_bit=1 is count_zeros.
            # If B_bit=0, number of 1s is count_ones.
            
            if count_zeros < count_ones:
                B |= (1 << bit)
        
        # Assign final values
        for u in queue:
            A[u] = B ^ D[u]

    # Output result
    print(' '.join(map(str, A[1:])))

if __name__ == '__main__':
    solve()
```

## worker: finalize
The problem is modeled as a graph where vertices are indices $1 \ldots N$ and edges represent XOR constraints. Each connected component's values are determined relative to a base value $B$. We use BFS to assign relative values $D_u$ and check for consistency (cycle XOR sums must be 0). If inconsistent, output -1. For each component, we independently determine the optimal base $B$ by minimizing the sum of elements bit-by-bit. For each bit position, we count how many $D_u$'s have that bit set. If more than half have it set, we flip the bit in $B$ to minimize the total number of 1s in the resulting $A_u$'s, thus minimizing the sum. The algorithm runs in $O(N + M)$ time.

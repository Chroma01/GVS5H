import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

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

    # Read the grid
    # The input format gives N lines of strings
    adj = []
    for _ in range(N):
        row_str = next(iterator)
        adj.append(row_str)

    # Precompute adjacency lists for each character
    # in_adj[u][c] = list of x such that x -> u has char c
    # out_adj[v][c] = list of y such that v -> y has char c
    # To optimize, we will use bitsets (integers) for these lists
    # Since N <= 100, we can use Python's arbitrary precision integers as bitsets
    
    # in_adj[u][c] will be a bitmask where the k-th bit is 1 if node k+1 has an edge to u with char c
    # We use 0-indexed internally for nodes 0..N-1
    in_adj = [[0] * 26 for _ in range(N)]
    out_adj = [[0] * 26 for _ in range(N)]
    
    # Also store the graph as a list of lists for easy access if needed, but bitsets are better for the matrix mult
    # Actually, for the matrix multiplication approach:
    # We need R_c (adjacency matrix for char c)
    # R_c[x][y] = 1 if x -> y is c
    # Then Pre_c[u] corresponds to the column u of R_c (or row of R_c^T)
    # Succ_c[v] corresponds to the row v of R_c
    
    # Let's build R_c matrices as bitsets (rows)
    # R_c[u] is an integer where the v-th bit is 1 if u -> v is c
    R = [[0] * 26 for _ in range(26)] # R[c][u] is the bitset for row u of char c
    
    for u in range(N):
        for v in range(N):
            char = adj[u][v]
            if char != '-':
                idx = ord(char) - ord('a')
                # Set bit v in R[idx][u]
                R[idx][u] |= (1 << v)
                
    # We also need the transpose for the "predecessor" part
    # Pre_c[u] is the set of x such that x -> u is c.
    # This is the column u of R[c].
    # We can compute this on the fly or precompute.
    # Let's precompute Pre[c][u] as a bitset.
    Pre = [[0] * 26 for _ in range(N)]
    for c in range(26):
        for u in range(N):
            # Column u of R[c]
            # We can extract it by checking bits, but iterating is slow.
            # Better: Pre[c][u] = sum over v of (R[c][v] & (1<<u))? No.
            # Pre[c][u] is the set of x. x -> u is c.
            # So we look at column u of R[c].
            # We can compute this by iterating all x and checking if x->u is c.
            # But we can just use the R matrix.
            # Actually, let's just compute it directly.
            mask = 0
            for x in range(N):
                if (R[c][x] >> u) & 1:
                    mask |= (1 << x)
            Pre[c][u] = mask

    # Initialize distances
    # dist[u][v] stores the shortest palindrome length from u to v
    # Initialize with infinity
    INF = 10**9
    dist = [[INF] * N for _ in range(N)]
    
    # Base cases:
    # 1. Length 0: u -> u (empty path)
    for u in range(N):
        dist[u][u] = 0
        
    # 2. Length 1: u -> v with char c
    # We can push these into a queue or process them as layer 1
    # Let's use a queue for BFS: (u, v, length)
    # But to optimize, we process layer by layer.
    # Layer 0: all (u, u)
    # Layer 1: all (u, v) with edge
    
    # We will maintain a set of reachable pairs for the current layer
    # current_layer_pairs: set of (u, v)
    # But we need to know the length.
    # Let's use a list of sets: layers[L] = set of (u, v)
    # But L can be large.
    # Instead, we can just run BFS with a queue.
    # Queue stores (u, v, length).
    # To avoid re-processing, we use dist[u][v].
    # If dist[u][v] is already set, we skip.
    # Wait, if we process by length, the first time we visit (u, v) is the shortest.
    
    # Queue for BFS
    # We can store (u, v) and know the length from dist[u][v] when we pop?
    # No, because we might reach (u, v) with length L, and later with L+2.
    # But we only care about the first time.
    # So we can just use a queue of (u, v).
    # But we need to know the length to extend.
    # So we store (u, v, length) in the queue.
    
    # Initial queue
    queue = []
    
    # Add length 0
    for u in range(N):
        queue.append((u, u, 0))
        
    # Add length 1
    for u in range(N):
        for v in range(N):
            char = adj[u][v]
            if char != '-':
                idx = ord(char) - ord('a')
                if dist[u][v] == INF:
                    dist[u][v] = 1
                    queue.append((u, v, 1))
    
    # BFS
    # We process in increasing order of length.
    # Since we only push if dist is INF, and we start with 0 and 1,
    # the queue will naturally be sorted by length if we process carefully?
    # Not necessarily, because 0 -> 2, 1 -> 3.
    # But 0 < 1 < 2 < 3.
    # So if we process 0s, then 1s, then 2s...
    # We can group by length.
    
    # Let's use a list of lists for layers
    # layers[L] = list of (u, v)
    # But L can be large.
    # Instead, we can just use a queue and sort? No.
    # We can use two queues: current_layer and next_layer.
    # But lengths increase by 2.
    # So we can just use one queue and process.
    # But we need to ensure we process all length L before L+2.
    # Since we start with 0 and 1, and add 2, the lengths are 0, 1, 2, 3, 4, 5...
    # So if we just pop from the front, we might get 0, then 1, then 2...
    # Yes, because 0+2=2, 1+2=3.
    # So the queue will be sorted by length.
    
    # Optimization: Use bitsets for the transitions
    # For a state (u, v) with length L, we want to find (x, y) with length L+2
    # such that x -> u is c and v -> y is c.
    # This is equivalent to: x in Pre[c][u] and y in (R[c] row v)
    # We can iterate over c, then iterate over bits in Pre[c][u] and R[c][v].
    # This is O(26 * N^2) per state. Total O(N^4).
    # With N=100, N^4 = 10^8. 26 * 10^8 = 2.6 * 10^9. Too slow.
    
    # We need the matrix multiplication optimization.
    # Instead of iterating states, we iterate layers.
    # Let S_L be the set of pairs (u, v) with palindrome length L.
    # S_{L+2} = Union over c of (Pre[c] o S_L o R[c])
    # Where Pre[c] is the relation x->u with c, R[c] is u->v with c.
    # Composition: (A o B)[x][y] = OR_u (A[x][u] and B[u][y])
    # Here, Pre[c] is a matrix P_c where P_c[x][u] = 1 if x->u is c.
    # R[c] is a matrix M_c where M_c[u][v] = 1 if u->v is c.
    # We want P_c o S_L o M_c.
    # Let T = S_L o M_c. T[x][v] = OR_u (S_L[x][u] and M_c[u][v])
    # Then (P_c o T)[x][y] = OR_v (P_c[x][v] and T[v][y])
    # Wait, P_c[x][v] is 1 if x->v is c.
    # So we are computing P_c * S_L * M_c.
    # This is matrix multiplication over boolean semiring.
    # We can do this with bitsets.
    # S_L is a matrix of size N x N.
    # M_c is N x N.
    # P_c is N x N.
    # We can compute S_L * M_c first.
    # (S_L * M_c)[x][v] = OR_u (S_L[x][u] and M_c[u][v])
    # This is: for each row x of S_L, we OR the rows of M_c corresponding to set bits in S_L[x].
    # Since M_c is stored as bitsets (rows), this is fast.
    # Then P_c * (S_L * M_c).
    # (P_c * T)[x][y] = OR_v (P_c[x][v] and T[v][y])
    # This is: for each row x of P_c, we OR the rows of T corresponding to set bits in P_c[x].
    # P_c[x] is the set of v such that x->v is c.
    # Wait, P_c is defined as x->u is c. So P_c[x][u] = 1.
    # So P_c is the same as M_c?
    # No. M_c[u][v] = 1 if u->v is c.
    # P_c[x][u] = 1 if x->u is c.
    # So P_c is the transpose of M_c?
    # P_c[x][u] = M_c[u][x]. Yes, P_c = M_c^T.
    # So we want M_c^T * S_L * M_c.
    
    # Algorithm:
    # 1. Initialize S_0 = Identity matrix (dist[u][u]=0).
    # 2. Initialize S_1 = M_c for all c? No, S_1 is the set of pairs with length 1.
    #    S_1[u][v] = 1 if there is an edge u->v.
    #    This is OR over c of M_c.
    # 3. For L = 0, 2, 4...
    #    Compute S_{L+2} = OR over c of (M_c^T * S_L * M_c)
    #    Update dist matrix.
    #    If S_{L+2} is all zeros, stop.
    #    Also, we need to handle odd lengths.
    #    Base: S_0 (len 0), S_1 (len 1).
    #    Then S_2 from S_0, S_3 from S_1, S_4 from S_2, etc.
    
    # We can maintain two matrices: current_even (S_0, S_2, ...) and current_odd (S_1, S_3, ...)
    # But we need to update dist.
    # dist[u][v] = min length.
    # We can just maintain the current layer matrices and update dist.
    
    # Let's represent matrices as list of integers (bitsets).
    # mat[u] is an integer where v-th bit is 1 if (u, v) is in the set.
    
    # S_0: Identity
    S_even = [0] * N
    for u in range(N):
        S_even[u] = (1 << u)
        
    # S_1: Edges
    S_odd = [0] * N
    for u in range(N):
        for v in range(N):
            char = adj[u][v]
            if char != '-':
                S_odd[u] |= (1 << v)
                
    # We also need to track the current length
    # We process length 0, then 2, 4...
    # And length 1, then 3, 5...
    
    # We can run a loop for length L = 0, 1, 2, ...
    # But we need to separate even and odd.
    # Let's just run two loops.
    
    # Loop for even lengths: L = 0, 2, 4, ...
    # Current matrix: S_even (initially S_0)
    # Next matrix: S_next_even
    # We update dist with S_even.
    # Then compute S_next_even from S_even.
    # Repeat until S_next_even is all zeros.
    
    # Same for odd.
    
    # Function to compute next layer
    def compute_next_layer(current_layer, is_even):
        # current_layer is a list of N integers (bitsets)
        # We want to compute next_layer = OR over c of (M_c^T * current_layer * M_c)
        # M_c is the adjacency matrix for char c.
        # M_c[u] is the bitset of successors of u with char c.
        # M_c^T[u] is the bitset of predecessors of u with char c.
        # Let P_c[u] = M_c^T[u] (predecessors)
        # Let M_c[u] = successors
        
        next_layer = [0] * N
        
        for c in range(26):
            # Get P_c and M_c
            # P_c[u] is Pre[c][u]
            # M_c[u] is R[c][u]
            
            # We need to compute T = current_layer * M_c
            # T[u][v] = OR_k (current_layer[u][k] and M_c[k][v])
            # T[u] = OR over k where current_layer[u] has bit k set of M_c[k]
            
            # Then next_layer[u][y] = OR_v (P_c[u][v] and T[v][y])
            # next_layer[u] = OR over v where P_c[u] has bit v set of T[v]
            
            # Optimization:
            # T[v] depends on current_layer[v].
            # We can compute T for all v first.
            
            # Precompute T for this c
            T = [0] * N
            for u in range(N):
                # current_layer[u] is a bitset
                # We need to OR M_c[k] for all k in current_layer[u]
                # This is slow if we iterate bits.
                # But we can use the fact that M_c[k] are precomputed.
                # We can iterate k from 0 to N-1.
                # If (current_layer[u] >> k) & 1:
                #    T[u] |= M_c[k]
                # This is O(N^2) per c. Total O(26 * N^2).
                # Then next_layer[u] = OR over v in P_c[u] of T[v].
                # This is also O(N^2) per c.
                # Total O(26 * N^2).
                # This is fast enough!
                
                mask = current_layer[u]
                t_val = 0
                # Iterate over set bits in mask
                # Since N=100, we can just loop 0..N-1
                for k in range(N):
                    if (mask >> k) & 1:
                        t_val |= R[c][k]
                T[u] = t_val
                
            # Now compute next_layer[u]
            for u in range(N):
                mask = Pre[c][u]
                val = 0
                for v in range(N):
                    if (mask >> v) & 1:
                        val |= T[v]
                next_layer[u] |= val
                
        return next_layer

    # Process even lengths
    # We start with S_0 (len 0)
    # We update dist with S_0.
    # Then compute S_2, update dist, etc.
    
    # We need to keep track of the current length
    # Even loop: L = 0, 2, 4, ...
    # Odd loop: L = 1, 3, 5, ...
    
    # We can run them in parallel or sequentially.
    # Since we want the shortest, we should process L=0, then L=1, then L=2, etc.
    # But the dependency is S_{L+2} from S_L.
    # So we can just run two independent loops.
    # But we need to update dist with the minimum.
    # Since we process L=0, then L=2, then L=4...
    # And L=1, then L=3, then L=5...
    # We can just run the even loop and odd loop separately.
    # But we need to ensure we don't overwrite a shorter path with a longer one.
    # Since we process in increasing order of L, the first time we set dist[u][v] is the shortest.
    # So we can check if dist[u][v] is INF before updating.
    
    # Even loop
    current_even = S_even
    L = 0
    while True:
        # Update dist with current_even
        for u in range(N):
            mask = current_even[u]
            for v in range(N):
                if (mask >> v) & 1:
                    if dist[u][v] == INF:
                        dist[u][v] = L
        
        # Check if all zeros
        if all(x == 0 for x in current_even):
            break
            
        # Compute next
        current_even = compute_next_layer(current_even, True)
        L += 2
        
    # Odd loop
    current_odd = S_odd
    L = 1
    while True:
        # Update dist
        for u in range(N):
            mask = current_odd[u]
            for v in range(N):
                if (mask >> v) & 1:
                    if dist[u][v] == INF:
                        dist[u][v] = L
        
        if all(x == 0 for x in current_odd):
            break
            
        current_odd = compute_next_layer(current_odd, False)
        L += 2
        
    # Output
    for u in range(N):
        row = []
        for v in range(N):
            if dist[u][v] == INF:
                row.append("-1")
            else:
                row.append(str(dist[u][v]))
        print(" ".join(row))

solve()
import sys

def solve():
    # Increase recursion depth just in case, though not needed here
    sys.setrecursionlimit(200005)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    A = []
    for i in range(N):
        A.append(int(data[2 + i]))
        
    # Step 1: Compute initial inversion count for k=0 (B = A)
    # Using Fenwick Tree (BIT)
    # Since A_i < M, we can use values directly as indices in BIT (1-indexed)
    
    bit = [0] * (M + 1)
    
    def update(i, delta):
        while i <= M:
            bit[i] += delta
            i += i & (-i)
            
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
        
    inv_count = 0
    # Process from right to left or left to right.
    # Let's go left to right. For each element, count how many elements to the left are greater.
    # Or count how many elements to the right are smaller.
    # Standard: iterate left to right, for A[i], count elements already in BIT that are > A[i].
    # Elements in BIT are those to the left.
    # Count of elements > A[i] = (total elements so far) - (count of elements <= A[i])
    
    for x in A:
        # x is 0-indexed value, BIT is 1-indexed, so use x+1
        val = x + 1
        # Count elements <= x currently in BIT
        count_le = query(val)
        # Total elements processed so far
        count_processed = query(M) # This is just the loop index, but let's use a counter
        # Actually, simpler: inv_count += (i - query(val)) where i is 0-indexed count of previous elements
        
    # Let's rewrite the loop cleanly
    bit = [0] * (M + 1)
    inv_count = 0
    for i, x in enumerate(A):
        val = x + 1
        # Number of elements to the left that are greater than x
        # Total elements to left = i
        # Elements to left <= x = query(val)
        greater = i - query(val)
        inv_count += greater
        update(val, 1)
        
    # Step 2: Precompute deltas for each value v
    # When shifting from k to k+1, the value v = M - 1 - k wraps around.
    # Delta for value v:
    # Delta_v = P_left(v) - P_right(v)
    # P_left(v) = sum over positions p of v of (p - (number of v's to the left of p))
    # P_right(v) = sum over positions p of v of ((N - 1 - p) - (number of v's to the right of p))
    
    # Group positions by value
    pos = [[] for _ in range(M)]
    for i, x in enumerate(A):
        pos[x].append(i)
        
    deltas = [0] * M
    
    for v in range(M):
        positions = pos[v]
        c = len(positions)
        if c == 0:
            deltas[v] = 0
            continue
            
        p_left_sum = 0
        p_right_sum = 0
        
        for m, p in enumerate(positions):
            # m is 0-indexed index in the positions list
            # Number of v's to the left of this occurrence is m
            # Number of v's to the right of this occurrence is c - 1 - m
            
            # Non-wrapping elements to the left
            # Total elements to left = p
            # Non-wrapping to left = p - m
            p_left_sum += (p - m)
            
            # Non-wrapping elements to the right
            # Total elements to right = N - 1 - p
            # Non-wrapping to right = (N - 1 - p) - (c - 1 - m)
            p_right_sum += ((N - 1 - p) - (c - 1 - m))
            
        deltas[v] = p_left_sum - p_right_sum
        
    # Step 3: Apply deltas sequentially
    # For k=0, answer is inv_count
    # For k=1, answer is inv_count + delta[M-1] (since v = M-1-0 = M-1)
    # For k=2, answer is prev + delta[M-2]
    # ...
    # For k, answer is prev + delta[M-1-(k-1)] = delta[M-k]
    
    results = []
    current_inv = inv_count
    results.append(str(current_inv))
    
    for k in range(1, M):
        # Transition from k-1 to k
        # The value that wrapped in the previous step (k-1 -> k) was v = M - 1 - (k-1) = M - k
        # Wait, let's trace carefully.
        # k=0: initial state.
        # Transition k=0 -> k=1: value v = M - 1 - 0 = M - 1 wraps.
        # So delta to add is deltas[M-1].
        # Transition k=1 -> k=2: value v = M - 1 - 1 = M - 2 wraps.
        # So delta to add is deltas[M-2].
        # Transition k=i -> k=i+1: value v = M - 1 - i wraps.
        
        # We are computing answer for k=1, which is after transition 0->1.
        # So we add deltas[M-1].
        # For k=2, add deltas[M-2].
        # For general k (1 to M-1), we add deltas[M-k].
        
        v = M - k
        current_inv += deltas[v]
        results.append(str(current_inv))
        
    print('\n'.join(results))

solve()
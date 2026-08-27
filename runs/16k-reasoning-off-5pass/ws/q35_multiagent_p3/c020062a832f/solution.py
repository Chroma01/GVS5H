import sys

# Increase recursion depth just in case, though we won't use deep recursion
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # 1. Compute initial inversion count for k=0 (B = A)
    # Using Fenwick Tree (BIT) over values since values are in [0, M-1]
    # BIT size M+1 for 1-based indexing of values 1..M
    
    bit = [0] * (M + 2)
    
    def update(idx, val):
        """Add val to element at idx (1-based)"""
        while idx <= M + 1:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        """Return sum from 1 to idx (1-based)"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s

    initial_inv = 0
    # Process A from left to right
    # For each element A[i], count how many elements to its left are greater than A[i]
    # This is equivalent to: (total elements so far) - (elements <= A[i] so far)
    # Or: (elements so far) - query(A[i] + 1) if we store counts of values
    
    # Let's use BIT to store frequencies of values seen so far.
    # Values are 0..M-1. We map value v to index v+1 in BIT.
    
    for x in A:
        # Count elements already in BIT that are greater than x
        # Total elements so far is i (loop index)
        # Elements <= x is query(x + 1)
        # Elements > x is i - query(x + 1)
        
        # Note: i is 0-indexed here. Let's use a counter.
        pass

    # Re-doing initial inversion count properly
    bit = [0] * (M + 2)
    initial_inv = 0
    for i, x in enumerate(A):
        # Number of elements seen so far that are greater than x
        # Total seen = i
        # Seen <= x = query(x + 1)
        seen_le_x = query(x + 1)
        greater = i - seen_le_x
        initial_inv += greater
        update(x + 1, 1)

    # 2. Prepare data structures for transitions
    # Group indices by value
    indices_by_value = [[] for _ in range(M)]
    for i, x in enumerate(A):
        indices_by_value[x].append(i)
        
    # 3. Initialize BIT for range queries on indices
    # This BIT will track which indices have values < current_threshold
    # Size N+2 for 1-based indexing of indices 1..N
    idx_bit = [0] * (N + 2)
    
    def idx_update(idx, val):
        """Add val to element at idx (1-based) in index BIT"""
        while idx <= N + 1:
            idx_bit[idx] += val
            idx += idx & (-idx)
            
    def idx_query(idx):
        """Return sum from 1 to idx (1-based) in index BIT"""
        s = 0
        while idx > 0:
            s += idx_bit[idx]
            idx -= idx & (-idx)
        return s

    # Initialize the index BIT: mark all positions i where A[i] < M-1
    # Threshold starts at M-1. We want to mark A[i] < M-1.
    # So initially, all A[i] != M-1 are marked? No, A[i] < M-1.
    # Since A[i] are non-negative, this means all A[i] in [0, M-2].
    
    for i, x in enumerate(A):
        if x < M - 1:
            idx_update(i + 1, 1)
            
    current_inv = initial_inv
    results = []
    results.append(str(current_inv))
    
    # 4. Iterate k from 0 to M-2 to compute k+1 from k
    # For each k, the wrapping value is X = M - 1 - k
    # We compute the change to get to k+1, then update the BIT for the next step.
    
    for k in range(M - 1):
        X = M - 1 - k
        
        # Get all indices where A[i] == X
        pos_list = indices_by_value[X]
        
        loss = 0
        gain = 0
        
        for pos in pos_list:
            # pos is 0-based index in A
            # 1-based index for BIT is pos + 1
            
            # Loss: pairs (i, j) with i < j, A[i]=X, A[j] < X
            # Here i = pos. We need count of j > pos such that A[j] < X.
            # In our BIT, we have marked all indices j where A[j] < X.
            # So we query range [pos+2, N] (1-based: pos+2 to N)
            # Count = query(N) - query(pos+1)
            
            count_right = idx_query(N + 1) - idx_query(pos + 1)
            loss += count_right
            
            # Gain: pairs (i, j) with i < j, A[i] < X, A[j]=X
            # Here j = pos. We need count of i < pos such that A[i] < X.
            # Query range [1, pos-1] (1-based: 1 to pos-1)
            # Count = query(pos-1)
            
            count_left = idx_query(pos) # query(pos-1) in 1-based is query(pos-1)
            # Wait, if pos=0 (1-based index 1), query(0) returns 0. Correct.
            # If pos=1 (1-based index 2), query(1) returns count at index 1. Correct.
            gain += count_left
            
        current_inv = current_inv + gain - loss
        results.append(str(current_inv))
        
        # Update BIT for next step:
        # Next threshold will be X-1.
        # Currently BIT marks A[i] < X.
        # We need to unmark A[i] == X-1? No.
        # We need BIT to mark A[i] < X-1.
        # So we must remove indices where A[i] == X-1 from the BIT.
        # Wait, the current BIT marks A[i] < X.
        # The next step uses threshold X-1. We need BIT to mark A[i] < X-1.
        # So we need to remove indices where A[i] == X-1.
        
        # But wait, we are iterating k.
        # Step k=0: X = M-1. BIT marks A[i] < M-1.
        # We compute change for k=0 -> k=1.
        # Then we prepare BIT for k=1.
        # For k=1, X = M-2. BIT should mark A[i] < M-2.
        # So we need to remove indices where A[i] == M-2 from the BIT.
        
        # General step: After processing X, we need to remove indices where A[i] == X-1.
        # But X = M-1-k. So X-1 = M-2-k.
        # Let's verify.
        # k=0, X=M-1. Remove A[i] == M-2.
        # k=1, X=M-2. Remove A[i] == M-3.
        # ...
        # k=M-2, X=1. Remove A[i] == 0.
        
        # So we remove indices_by_value[X-1] from the BIT.
        
        if X - 1 >= 0:
            remove_list = indices_by_value[X - 1]
            for pos in remove_list:
                idx_update(pos + 1, -1)
                
    print('\n'.join(results))

solve()
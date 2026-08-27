import sys

def solve():
    # Increase recursion depth just in case, though we don't use recursion
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
    
    # Fenwick Tree (Binary Indexed Tree) implementation
    class FenwickTree:
        def __init__(self, size):
            self.tree = [0] * (size + 1)
            
        def update(self, i, delta):
            while i <= len(self.tree) - 1:
                self.tree[i] += delta
                i += i & (-i)
                
        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s
            
        def range_query(self, l, r):
            if l > r:
                return 0
            return self.query(r) - self.query(l - 1)

    # Step 1: Compute initial inversion number for k=0
    # B_i = A_i
    # We use a BIT to count inversions.
    # Iterate from left to right. For each element, count how many elements to its right are smaller.
    # Alternatively, iterate and count how many elements to its left are larger.
    # Let's use the standard method: iterate j from 0 to N-1, count elements already seen that are greater than A[j].
    # Or: count elements already seen that are smaller, and subtract from total seen so far.
    
    # Since A_i < M, we can use a BIT of size M.
    bit_val = FenwickTree(M)
    initial_inv = 0
    
    # To count inversions: for each j, count i < j such that A[i] > A[j].
    # This is equal to (number of elements seen so far) - (number of elements seen so far <= A[j]).
    # But wait, standard inversion counting:
    # Iterate j from 0 to N-1:
    #   inv += (j - bit_val.query(A[j] + 1)) # j elements seen, bit_val.query(A[j]+1) are <= A[j]
    #   bit_val.update(A[j] + 1, 1)
    
    for j in range(N):
        val = A[j]
        # Count elements already in BIT that are greater than val
        # Total elements so far: j
        # Elements <= val: bit_val.query(val + 1)
        # Elements > val: j - bit_val.query(val + 1)
        initial_inv += (j - bit_val.query(val + 1))
        bit_val.update(val + 1, 1)
        
    current_inv = initial_inv
    
    # Step 2: Prepare wrap events
    # Group indices by their original value A[i].
    # An element with original value v wraps when k = M - v.
    # We only care about v > 0, because if v=0, it wraps at k=M, which is outside our range [0, M-1].
    # wrappers[v] will store the list of indices (1-based) where A[i] == v.
    wrappers = [[] for _ in range(M)]
    for i in range(N):
        val = A[i]
        if val > 0:
            wrappers[val].append(i + 1) # 1-based index
            
    # Step 3: Transition from k to k+1
    # We maintain a BIT of active (non-wrapped) positions.
    # Initially, all positions are active.
    bit_pos = FenwickTree(N)
    for i in range(1, N + 1):
        bit_pos.update(i, 1)
        
    total_active = N
    
    results = []
    results.append(current_inv)
    
    # Iterate k from 0 to M-2 to compute answers for k=1 to M-1
    # At step k (0-indexed), we have computed answer for k.
    # We now transition to k+1.
    # The elements that wrap are those with current value M-1.
    # Current value of an element with original value v at step k is (v + k) % M.
    # It wraps when (v + k) % M == M-1 => v + k = M - 1 => v = M - 1 - k.
    
    for k in range(M - 1):
        v = M - 1 - k
        # Elements with original value v will wrap when moving from k to k+1
        wrap_indices = wrappers[v]
        
        if wrap_indices:
            delta = 0
            for idx in wrap_indices:
                # Count active elements to the left of idx
                left_active = bit_pos.query(idx - 1)
                # Count active elements to the right of idx
                right_active = total_active - bit_pos.query(idx)
                
                # Contribution to delta:
                # Pairs (i, j) with i in S (active), j in W (wrapping), i < j: gain 1 inversion
                #   This is exactly left_active for this j.
                # Pairs (i, j) with i in W (wrapping), j in S (active), i < j: lose 1 inversion
                #   This is exactly right_active for this i (which is j in the pair notation above).
                # So delta += left_active - right_active
                
                delta += left_active - right_active
                
            current_inv += delta
            
            # Remove wrapping elements from the active set
            for idx in wrap_indices:
                bit_pos.update(idx, -1)
                total_active -= 1
                
        results.append(current_inv)
        
    # Output results
    for res in results:
        print(res)

solve()
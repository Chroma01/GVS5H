import sys

# Increase recursion depth just in case, though not needed for this iterative solution
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
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # 1. Compute initial inversion count for k=0 (sequence A)
    # Using Fenwick Tree (Binary Indexed Tree)
    # Coordinate compression is not needed since 0 <= A_i < M
    
    # Fenwick Tree implementation
    bit = [0] * (M + 1)
    
    def update(i, delta):
        """Add delta to element at index i (1-based)"""
        while i <= M:
            bit[i] += delta
            i += i & (-i)
            
    def query(i):
        """Return sum from 1 to i (1-based)"""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    initial_inv = 0
    # Process from right to left or left to right.
    # Standard way: for each element, count how many elements to the right are smaller.
    # Or: for each element, count how many elements to the left are larger.
    # Let's do: iterate left to right. For A[i], count how many elements already seen are greater than A[i].
    # Total seen so far = i. Elements <= A[i] seen so far = query(A[i] + 1).
    # Elements > A[i] seen so far = i - query(A[i] + 1).
    
    for i in range(N):
        val = A[i]
        # Count elements strictly greater than val that have appeared before
        # Elements seen so far: i
        # Elements <= val seen so far: query(val + 1)
        greater = i - query(val + 1)
        initial_inv += greater
        update(val + 1, 1)
        
    current_inv = initial_inv
    
    # 2. Precompute deltas for each value v
    # Group indices by value
    pos_by_val = [[] for _ in range(M)]
    for idx, val in enumerate(A):
        pos_by_val[val].append(idx)
        
    # Precompute Add_v and Sub_v for each value v
    # Add_v = sum over j in Pos_v of (j - rank_of_j_in_Pos_v)
    # Sub_v = sum over i in Pos_v of ((N - 1 - i) - rank_of_i_in_Pos_v_from_end)
    # Note: rank_of_j_in_Pos_v is 0-based index in the list pos_by_val[v]
    
    delta_by_val = [0] * M
    
    for v in range(M):
        positions = pos_by_val[v]
        if not positions:
            continue
            
        add_v = 0
        sub_v = 0
        
        # positions is sorted by index because we iterated 0..N-1
        num_positions = len(positions)
        
        for rank, idx in enumerate(positions):
            # Term 1: j - rank
            add_v += (idx - rank)
            
            # Term 2: (N - 1 - idx) - (number of positions after idx)
            # Number of positions after idx is (num_positions - 1 - rank)
            sub_v += ((N - 1 - idx) - (num_positions - 1 - rank))
            
        delta_by_val[v] = add_v - sub_v
        
    # 3. Iterate k from 0 to M-1
    # Output for k=0
    results = []
    results.append(str(current_inv))
    
    # Transition from k to k+1
    # The elements that wrap when going from k to k+1 are those with A_i such that
    # (A_i + k) % M == M - 1  =>  A_i % M == (M - 1 - k) % M
    # Let target = (M - 1 - k) % M
    # The change is delta_by_val[target]
    
    for k in range(M - 1):
        target = (M - 1 - k) % M
        current_inv += delta_by_val[target]
        results.append(str(current_inv))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
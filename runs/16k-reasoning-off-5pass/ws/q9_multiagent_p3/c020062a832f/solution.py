import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Fast I/O setup
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Helper functions for Fenwick Tree (Binary Indexed Tree)
    # We will use 1-based indexing for the BIT internally
    
    def update_bit(bit, i, delta):
        """Adds delta to element at index i (0-based) in bit."""
        i += 1  # Convert to 1-based
        while i <= N:
            bit[i] += delta
            i += i & (-i)
            
    def query_bit(bit, i):
        """Returns sum of elements from index 0 to i (0-based) in bit."""
        i += 1  # Convert to 1-based
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    # 1. Calculate initial inversion count for k=0
    # Inversion: i < j and A[i] > A[j]
    # We iterate left to right. For current element x, inversions added = 
    # (number of elements seen so far) - (number of elements seen <= x)
    
    bit = [0] * (N + 1)
    initial_inversions = 0
    
    for i, x in enumerate(A):
        # Map value x to 1-based index for BIT: x+1
        idx = x + 1
        # Count elements already in BIT that are <= x
        count_le = query_bit(bit, idx)
        # Total elements processed so far is i
        count_gt = i - count_le
        initial_inversions += count_gt
        update_bit(bit, x, 1)
        
    # 2. Prepare data structures for incremental updates
    # We need to efficiently count pairs that change status as k increases.
    # Group indices by value.
    pos = [[] for _ in range(M)]
    for idx, x in enumerate(A):
        pos[x].append(idx)
        
    # 3. Simulate transitions from k to k+1 for k = 0 to M-2
    # We maintain a BIT (bit_w) that tracks the indices of elements that have "wrapped" so far.
    # An element with value v wraps when k reaches M - v.
    # Specifically, at step k (transitioning to k+1), elements with value V = M - 1 - k 
    # transition from "not wrapping" to "wrapping".
    
    bit_w = [0] * (N + 1)
    current_inversions = initial_inversions
    
    results = []
    results.append(str(current_inversions))
    
    # We need to output M lines. We have the first one (k=0).
    # We loop M-1 times to compute transitions for k=0->1, ..., k=M-2->M-1.
    for k in range(M - 1):
        # The value that starts wrapping at this transition is V = M - 1 - k
        V = M - 1 - k
        
        # If no elements have this value, no change occurs
        if V < 0 or V >= M:
            results.append(str(current_inversions))
            continue
            
        N_k = pos[V]
        if not N_k:
            results.append(str(current_inversions))
            continue
            
        len_Nk = len(N_k)
        
        # Calculate sizes of sets
        # W_k: set of indices of elements that have already wrapped (value >= M - k)
        # These are currently in bit_w.
        W_k_size = query_bit(bit_w, N - 1) # Sum of all elements in bit_w
        
        # Rest: set of indices of elements that have not wrapped yet (value < M - 1 - k)
        # Rest_size = Total - W_k_size - N_k_size
        Rest_size = N - W_k_size - len_Nk
        
        # We need to calculate the change in inversion count.
        # Change = |N_k|*|Rest| - 2*count(N_k, Rest, i<j) + |N_k|*|W_k| - 2*count(N_k, W_k, i<j)
        
        term1 = 0 # count(N_k, W_k, i<j)
        term2 = 0 # count(N_k, Rest, i<j)
        
        # Iterate through N_k (indices where A[i] == V)
        # N_k is naturally sorted by index because we appended in order of enumeration
        for idx, j in enumerate(N_k):
            # j is the index in A (0-based)
            
            # Count elements in W_k with index < j
            # query_bit(bit_w, j-1) gives sum of frequencies for indices 0 to j-1
            c_w = query_bit(bit_w, j - 1)
            term1 += c_w
            
            # Count elements in Rest with index < j
            # Total elements with index < j is j (since indices are 0..N-1)
            # Elements < j are composed of: (elements in W_k < j) + (elements in N_k < j) + (elements in Rest < j)
            # So, count(Rest < j) = j - c_w - (elements in N_k < j)
            # Since N_k is sorted, elements in N_k < j is simply the index of j in N_k (which is 'idx')
            count_rest_less = j - c_w - idx
            term2 += count_rest_less
            
        # Apply formula
        change = len_Nk * Rest_size - 2 * term2 + len_Nk * W_k_size - 2 * term1
        current_inversions += change
        
        # Update BIT to include N_k in W_k for the next step
        for j in N_k:
            update_bit(bit_w, j, 1)
            
        results.append(str(current_inversions))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
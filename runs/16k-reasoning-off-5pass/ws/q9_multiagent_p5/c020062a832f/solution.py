import sys

# Increase recursion depth just in case, though we use iterative BIT
sys.setrecursionlimit(200005)

class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)

    def update(self, i, delta):
        """Adds delta to element at index i (1-based)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        """Returns sum from index 1 to i (1-based)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

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

    # A is 0-indexed in our list, but problem uses 1-based indexing for logic.
    # We will map index i (0 to N-1) to BIT index i+1.

    # Group indices by their initial value
    # indices_by_val[v] contains list of indices i where A[i] == v
    indices_by_val = [[] for _ in range(M)]
    for i in range(N):
        indices_by_val[A[i]].append(i)

    # Initial Inversion Count for k=0
    # We can compute this using a standard BIT approach
    # Iterate from left to right, counting how many elements to the left are larger.
    
    bit_inv = FenwickTree(M) # Tracks values present so far
    current_inv = 0
    
    for i in range(N):
        val = A[i]
        # Count elements > val
        # Total elements added so far is i
        # Elements <= val is query(val)
        count_le = bit_inv.query(val)
        count_gt = i - count_le
        current_inv += count_gt
        bit_inv.update(val, 1)

    # We need two BITs to track positions for the update logic
    # bit_pos_gt0: At index p (1-based), stores 1 if B[p] > 0, else 0
    # bit_pos_ltM1: At index p (1-based), stores 1 if B[p] < M-1, else 0
    
    bit_pos_gt0 = FenwickTree(N)
    bit_pos_ltM1 = FenwickTree(N)
    
    # Initialize these BITs based on initial A
    for i in range(N):
        val = A[i]
        # Index in BIT is i+1
        idx = i + 1
        if val > 0:
            bit_pos_gt0.update(idx, 1)
        if val < M - 1:
            bit_pos_ltM1.update(idx, 1)

    # Prepare output list
    results = []

    # Loop k from 0 to M-1
    for k in range(M):
        results.append(str(current_inv))
        
        if k == M - 1:
            break
            
        # Identify indices that wrap around from M-1 to 0
        # Current value is (A[i] + k) % M
        # We want (A[i] + k) == M - 1 => A[i] == M - 1 - k
        target_val = M - 1 - k
        
        # Get indices where A[i] == target_val
        wrapping_indices = indices_by_val[target_val]
        
        if not wrapping_indices:
            continue
            
        # Calculate change in inversion count
        # For each wrapping index i:
        #   Loss: Pairs (i, j) with j > i and B[j] < M-1
        #   Gain: Pairs (j, i) with j < i and B[j] > 0
        
        total_gain = 0
        total_loss = 0
        
        for idx in wrapping_indices:
            # BIT is 1-based, so idx corresponds to idx+1
            bit_idx = idx + 1
            
            # Gain: count of j < idx with B[j] > 0
            # query(bit_idx - 1) gives sum from 1 to bit_idx-1
            total_gain += bit_pos_gt0.query(bit_idx - 1)
            
            # Loss: count of j > idx with B[j] < M-1
            # Total elements with B[j] < M-1 is bit_pos_ltM1.query(N)
            # Elements with j <= idx is bit_pos_ltM1.query(bit_idx)
            # So j > idx is total - query(bit_idx)
            total_loss += (bit_pos_ltM1.query(N) - bit_pos_ltM1.query(bit_idx))
            
        current_inv += (total_gain - total_loss)
        
        # Update BITs: The values at these indices change from M-1 to 0
        # For bit_pos_gt0: M-1 > 0 (was 1), 0 > 0 (is 0). Change -1.
        # For bit_pos_ltM1: M-1 < M-1 (is 0), 0 < M-1 (is 1). Change +1.
        
        for idx in wrapping_indices:
            bit_idx = idx + 1
            bit_pos_gt0.update(bit_idx, -1)
            bit_pos_ltM1.update(bit_idx, 1)

    print('\n'.join(results))

if __name__ == '__main__':
    solve()
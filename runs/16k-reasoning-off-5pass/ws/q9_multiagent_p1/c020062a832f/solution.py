import sys

# Increase recursion depth just in case, though we use iterative approaches
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

    # Fenwick Tree (Binary Indexed Tree) implementation
    # 1-based indexing internally
    class FenwickTree:
        def __init__(self, size):
            self.tree = [0] * (size + 1)

        def update(self, i, delta):
            while i < len(self.tree):
                self.tree[i] += delta
                i += i & (-i)

        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s

        def query_range(self, l, r):
            if l > r:
                return 0
            return self.query(r) - self.query(l - 1)

    # 1. Calculate initial inversion count for k=0
    # We need to count pairs (i, j) such that i < j and A[i] > A[j]
    # Since A[i] < M, we can use a BIT of size M.
    # Note: A[i] are 0-indexed values. BIT is 1-indexed.
    # Map value x to x+1.
    
    bit = FenwickTree(M)
    current_inv = 0
    cnt = 0
    
    # Traverse left to right
    # For each x, count how many elements seen so far are greater than x
    for x in A:
        val = x + 1
        # Elements greater than x seen so far = (total seen) - (elements <= x)
        greater = cnt - bit.query(val)
        current_inv += greater
        bit.update(val, 1)
        cnt += 1

    # 2. Precompute L[v] and R[v]
    # L[v]: pairs (i, j) with i < j, A[i] = v, A[j] < v
    # R[v]: pairs (i, j) with i < j, A[i] < v, A[j] = v
    
    # Compute R[v]:
    # Iterate left to right. When at j with A[j] = v, add count of i < j with A[i] < v.
    # We can use a BIT to store frequencies of values seen so far.
    # R[v] += query(v) (since values are 0..M-1, query(v) sums 0..v-1 if 1-based mapping is careful)
    # Let's use 1-based mapping for BIT: value x -> x+1.
    # Count of numbers < v is query(v) (sums indices 1 to v, which correspond to values 0 to v-1).
    
    R = [0] * M
    bit_R = FenwickTree(M)
    for x in A:
        val = x + 1
        # Count of numbers < x seen so far
        # Numbers < x correspond to values 0..x-1 -> indices 1..x
        count_less = bit_R.query(x)
        R[x] += count_less
        bit_R.update(val, 1)

    # Compute L[v]:
    # L[v] = sum over j where A[j] < v of (count of i < j where A[i] = v)
    # This is equivalent to: for each x in A, we need to add 1 to L[v] for all v > x.
    # We can use a difference array (or prefix sum array) approach.
    # Initialize diff array of size M+1.
    # For each x in A: diff[x+1] += 1.
    # Then L[v] = prefix_sum[v] of diff array?
    # Let's verify:
    # L[v] = sum_{j: A[j] < v} (count of i < j s.t. A[i] = v)
    # Let's iterate j from 0 to N-1. Let x = A[j].
    # We need to add 1 to L[v] for all v > x.
    # This is a range update on L: add 1 to [x+1, M-1].
    # Using difference array D: D[x+1] += 1, D[M] -= 1.
    # Then L[v] = sum(D[0]...D[v]).
    
    diff_L = [0] * (M + 2)
    for x in A:
        # Update range [x+1, M-1]
        # diff_L[x+1] += 1
        # diff_L[M] -= 1 (since we only care up to M-1, and array size is M+2)
        if x + 1 < M:
            diff_L[x + 1] += 1
        if M < len(diff_L):
            diff_L[M] -= 1
            
    # Compute prefix sums to get L
    L = [0] * M
    current_sum = 0
    for v in range(M):
        current_sum += diff_L[v]
        L[v] = current_sum

    # 3. Simulate transitions
    # We need to output for k = 0, 1, ..., M-1
    # Transition from k to k+1 involves elements with value v = M - 1 - k wrapping.
    # When k goes 0 -> 1, v = M-1 wraps.
    # When k goes 1 -> 2, v = M-2 wraps.
    # ...
    # When k goes M-2 -> M-1, v = 1 wraps.
    # Note: v=0 never wraps in this range (0 + (M-1) = M-1 < M).
    
    results = []
    results.append(current_inv)
    
    for k in range(M - 1):
        # Transition k -> k+1
        # Value v that wraps is M - 1 - k
        v = M - 1 - k
        
        # Update inversion count
        # Remove inversions where A[i] = v, A[j] < v (i < j) -> L[v]
        # Add inversions where A[i] < v, A[j] = v (i < j) -> R[v]
        
        current_inv -= L[v]
        current_inv += R[v]
        
        results.append(current_inv)
        
    # Print results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()
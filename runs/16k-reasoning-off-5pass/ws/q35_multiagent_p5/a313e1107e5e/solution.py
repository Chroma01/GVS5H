import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    
    A = []
    for i in range(N):
        A.append(int(data[idx])); idx += 1
        
    queries = []
    for i in range(Q):
        R = int(data[idx]); idx += 1
        X = int(data[idx]); idx += 1
        queries.append((R, X, i))
    
    # Coordinate compression for values in A
    sorted_unique_A = sorted(set(A))
    val_to_idx = {v: i+1 for i, v in enumerate(sorted_unique_A)}
    m = len(sorted_unique_A)
    
    # BIT for prefix maximum queries
    bit = [0] * (m + 1)
    
    def bit_update(i, val):
        """Update position i with val, keeping maximum."""
        while i <= m:
            if val > bit[i]:
                bit[i] = val
            i += i & (-i)
            
    def bit_query(i):
        """Query maximum in range [1, i]."""
        res = 0
        while i > 0:
            if bit[i] > res:
                res = bit[i]
            i -= i & (-i)
        return res
    
    # Sort queries by R
    queries.sort(key=lambda x: x[0])
    
    answers = [0] * Q
    
    # Process queries offline
    q_idx = 0
    for r in range(1, N + 1):
        # Add A[r-1] to the BIT
        val = A[r-1]
        c_val = val_to_idx[val]
        
        # Query max LIS length for values strictly less than val
        # That means we query up to c_val - 1
        prev_max = bit_query(c_val - 1)
        new_len = prev_max + 1
        
        # Update the BIT at c_val with new_len
        bit_update(c_val, new_len)
        
        # Answer all queries with R_i == r
        while q_idx < Q and queries[q_idx][0] == r:
            _, X, orig_idx = queries[q_idx]
            
            # Find the largest value in sorted_unique_A that is <= X
            # bisect_right returns the insertion point, so index-1 gives the last element <= X
            pos = bisect_right(sorted_unique_A, X)
            # pos is the count of elements <= X, which corresponds to index pos in 1-based BIT
            # If pos == 0, no elements <= X, answer is 0 (but problem guarantees X >= min, so pos >= 1)
            if pos > 0:
                ans = bit_query(pos)
            else:
                ans = 0
            answers[orig_idx] = ans
            q_idx += 1
    
    for ans in answers:
        print(ans)

solve()
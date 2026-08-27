import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    Q = int(data[1])
    
    A = []
    idx = 2
    for i in range(N):
        A.append(int(data[idx]))
        idx += 1
        
    queries = []
    for i in range(Q):
        R = int(data[idx])
        X = int(data[idx+1])
        idx += 2
        queries.append((R, X, i))
    
    # Coordinate compression for A values
    sorted_unique_A = sorted(set(A))
    val_to_rank = {val: i+1 for i, val in enumerate(sorted_unique_A)}
    num_unique = len(sorted_unique_A)
    
    # BIT for prefix maximum queries
    # tree[i] stores the max LIS length for values with rank <= i
    tree = [0] * (num_unique + 1)
    
    def update(i, val):
        """Update position i with val, taking maximum."""
        while i <= num_unique:
            if val > tree[i]:
                tree[i] = val
            i += i & (-i)
    
    def query(i):
        """Query maximum value in range [1, i]."""
        res = 0
        while i > 0:
            if tree[i] > res:
                res = tree[i]
            i -= i & (-i)
        return res
    
    # Sort queries by R_i
    queries.sort(key=lambda x: x[0])
    
    answers = [0] * Q
    current_idx = 0  # Number of elements from A processed so far
    
    for R, X, q_idx in queries:
        # Process elements A[0] to A[R-1] (0-indexed)
        while current_idx < R:
            val = A[current_idx]
            rank = val_to_rank[val]
            
            # Find max LIS length ending with value < val
            # This means we query for rank - 1
            if rank > 1:
                prev_max = query(rank - 1)
            else:
                prev_max = 0
            
            new_len = prev_max + 1
            
            # Update BIT at position rank with new_len
            update(rank, new_len)
            
            current_idx += 1
        
        # Answer the query: max LIS length with value <= X
        # Find the largest rank such that sorted_unique_A[rank-1] <= X
        # bisect_right returns the insertion point, so all elements before it are <= X
        pos = bisect_right(sorted_unique_A, X)
        # pos is the count of elements <= X, which corresponds to ranks 1..pos
        if pos > 0:
            ans = query(pos)
        else:
            ans = 0
        
        answers[q_idx] = ans
    
    for ans in answers:
        print(ans)

solve()
import sys

# Increase recursion depth to handle deep segment trees if necessary
sys.setrecursionlimit(1000000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    for i in range(1, M + 1):
        S[i] = int(next(iterator))
        T[i] = int(next(iterator))
    
    # Ensure S[i] < T[i] for consistent interval handling
    for i in range(1, M + 1):
        if S[i] > T[i]:
            S[i], T[i] = T[i], S[i]
    
    queries = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r, i))
    
    # Sort queries by R to process offline
    queries.sort(key=lambda x: x[1])
    
    # Segment Tree Implementation
    # Size needs to be power of 2 >= N to cover 1..N
    size = 1
    while size < N:
        size *= 2
    
    # Tree arrays
    # max_B[u]: maximum value of B (latest endpoint index) in the range covered by node u
    # max_D[u]: maximum value of min(A, B) in the range covered by node u
    # lazy_A[u]: lazy value for A updates (latest intermediate index) in the range covered by node u
    
    max_B = [0] * (2 * size)
    max_D = [0] * (2 * size)
    lazy_A = [0] * (2 * size)
    
    def push_up(node):
        max_B[node] = max(max_B[2 * node], max_B[2 * node + 1])
        max_D[node] = max(max_D[2 * node], max_D[2 * node + 1])
        
    def push_down(node):
        if lazy_A[node] != 0:
            val = lazy_A[node]
            # Left child
            lazy_A[2 * node] = max(lazy_A[2 * node], val)
            max_D[2 * node] = min(val, max_B[2 * node])
            
            # Right child
            lazy_A[2 * node + 1] = max(lazy_A[2 * node + 1], val)
            max_D[2 * node + 1] = min(val, max_B[2 * node + 1])
            
            lazy_A[node] = 0

    def update_range_A(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            lazy_A[node] = max(lazy_A[node], val)
            max_D[node] = min(val, max_B[node])
            return
        
        push_down(node)
        mid = (start + end) // 2
        update_range_A(2 * node, start, mid, l, r, val)
        update_range_A(2 * node + 1, mid + 1, end, l, r, val)
        push_up(node)

    def update_point_B(node, start, end, idx, val):
        if start == end:
            max_B[node] = val
            max_D[node] = min(lazy_A[node], val)
            return
        
        push_down(node)
        mid = (start + end) // 2
        if idx <= mid:
            update_point_B(2 * node, start, mid, idx, val)
        else:
            update_point_B(2 * node + 1, mid + 1, end, idx, val)
        push_up(node)

    # Process people and queries
    results = [False] * Q
    
    query_idx = 0
    num_queries = len(queries)
    
    for i in range(1, M + 1):
        s = S[i]
        t = T[i]
        
        # Update A for internal nodes (s+1 to t-1)
        # If s+1 > t-1, the interval is empty, so we skip
        if s + 1 <= t - 1:
            update_range_A(1, 1, size, s + 1, t - 1, i)
        
        # Update B for endpoints s and t
        update_point_B(1, 1, size, s, i)
        update_point_B(1, 1, size, t, i)
        
        # Answer queries ending at i
        while query_idx < num_queries and queries[query_idx][1] == i:
            l, r, q_idx = queries[query_idx]
            
            # We need max(min(A_u, B_u)) over all towns u in [1, N].
            # A conflict exists if there is any town u such that A_u >= l AND B_u >= l.
            # This is equivalent to min(A_u, B_u) >= l.
            # If max(min(A_u, B_u)) < l, then for all u, min(A_u, B_u) < l, so no conflict.
            
            ans = query_max_D(1, 1, size, 1, N)
            if ans < l:
                results[q_idx] = True
            else:
                results[q_idx] = False
            
            query_idx += 1
            
    # Output results
    output = []
    for res in results:
        output.append("Yes" if res else "No")
    
    print('\n'.join(output))

# Add the missing query function inside solve or define it globally
# Since the logic is inside solve, we need to define query_max_D before calling it or define it inside.
# Let's redefine the structure slightly to ensure query_max_D is available.

def solve_final():
    import sys
    sys.setrecursionlimit(1000000)
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    for i in range(1, M + 1):
        S[i] = int(next(iterator))
        T[i] = int(next(iterator))
    
    for i in range(1, M + 1):
        if S[i] > T[i]:
            S[i], T[i] = T[i], S[i]
    
    queries = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r, i))
    
    queries.sort(key=lambda x: x[1])
    
    size = 1
    while size < N:
        size *= 2
    
    max_B = [0] * (2 * size)
    max_D = [0] * (2 * size)
    lazy_A = [0] * (2 * size)
    
    def push_up(node):
        max_B[node] = max(max_B[2 * node], max_B[2 * node + 1])
        max_D[node] = max(max_D[2 * node], max_D[2 * node + 1])
        
    def push_down(node):
        if lazy_A[node] != 0:
            val = lazy_A[node]
            lazy_A[2 * node] = max(lazy_A[2 * node], val)
            max_D[2 * node] = min(val, max_B[2 * node])
            
            lazy_A[2 * node + 1] = max(lazy_A[2 * node + 1], val)
            max_D[2 * node + 1] = min(val, max_B[2 * node + 1])
            
            lazy_A[node] = 0

    def update_range_A(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            lazy_A[node] = max(lazy_A[node], val)
            max_D[node] = min(val, max_B[node])
            return
        
        push_down(node)
        mid = (start + end) // 2
        update_range_A(2 * node, start, mid, l, r, val)
        update_range_A(2 * node + 1, mid + 1, end, l, r, val)
        push_up(node)

    def update_point_B(node, start, end, idx, val):
        if start == end:
            max_B[node] = val
            max_D[node] = min(lazy_A[node], val)
            return
        
        push_down(node)
        mid = (start + end) // 2
        if idx <= mid:
            update_point_B(2 * node, start, mid, idx, val)
        else:
            update_point_B(2 * node + 1, mid + 1, end, idx, val)
        push_up(node)

    def query_max_D(node, start, end, l, r):
        if l > end or r < start:
            return -1
        if l <= start and end <= r:
            return max_D[node]
        
        push_down(node)
        mid = (start + end) // 2
        left_res = query_max_D(2 * node, start, mid, l, r)
        right_res = query_max_D(2 * node + 1, mid + 1, end, l, r)
        return max(left_res, right_res)

    results = [False] * Q
    query_idx = 0
    num_queries = len(queries)
    
    for i in range(1, M + 1):
        s = S[i]
        t = T[i]
        
        if s + 1 <= t - 1:
            update_range_A(1, 1, size, s + 1, t - 1, i)
        
        update_point_B(1, 1, size, s, i)
        update_point_B(1, 1, size, t, i)
        
        while query_idx < num_queries and queries[query_idx][1] == i:
            l, r, q_idx = queries[query_idx]
            
            ans = query_max_D(1, 1, size, 1, N)
            if ans < l:
                results[q_idx] = True
            else:
                results[q_idx] = False
            
            query_idx += 1
            
    output = []
    for res in results:
        output.append("Yes" if res else "No")
    
    print('\n'.join(output))

if __name__ == '__main__':
    solve_final()
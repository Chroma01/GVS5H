import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
        
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return
        
    A = [0] * N
    for i in range(N):
        A[i] = int(next(iterator))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    # Precompute next_p
    # next_p[i] is the smallest index j such that A[j] >= 2 * A[i]
    # Since A is sorted, we can use a two-pointer approach
    next_p = [N] * N
    j = 0
    for i in range(N):
        # Ensure j > i, though the condition A[j] >= 2*A[i] implies j > i for A[i] > 0
        if j <= i:
            j = i + 1
        while j < N and A[j] < 2 * A[i]:
            j += 1
        next_p[i] = j if j < N else N
        
    # Compute val[p] = next_p[p] - p
    # If next_p[p] == N, it means no such j exists, so val[p] is effectively infinity.
    # We set it to N, which is sufficient since max shift is N.
    val = [0] * N
    for i in range(N):
        if next_p[i] == N:
            val[i] = N
        else:
            val[i] = next_p[i] - i
            
    # Build Sparse Table for Range Maximum Query (RMQ)
    # st[k][i] stores the maximum value in val[i : i + 2^k]
    LOG = N.bit_length()
    st = [[0] * N for _ in range(LOG)]
    
    for i in range(N):
        st[0][i] = val[i]
        
    for k in range(1, LOG):
        length = 1 << (k - 1)
        limit = N - (1 << k) + 1
        for i in range(limit):
            st[k][i] = max(st[k-1][i], st[k-1][i + length])
            
    # Precompute logs for O(1) query
    logs = [0] * (N + 1)
    for i in range(2, N + 1):
        logs[i] = logs[i // 2] + 1
        
    def query_max(l, r):
        if l > r:
            return 0
        length = r - l + 1
        k = logs[length]
        return max(st[k][l], st[k][r - (1 << k) + 1])
        
    results = []
    for _ in range(Q):
        try:
            L = int(next(iterator))
            R = int(next(iterator))
        except StopIteration:
            break
            
        l = L - 1
        r = R - 1
        S = r - l + 1
        # We can form at most S // 2 pairs because each pair uses 2 distinct mochi
        max_K = S // 2
        
        low = 0
        high = max_K
        ans = 0
        
        # Binary search for the maximum K
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                ans = max(ans, mid)
                low = mid + 1
                continue
                
            # Check if K = mid is feasible
            # The condition is: mid + max(val[l : l+mid]) <= S
            # This ensures that for all chosen smaller elements, there exists a larger element
            # at least 'shift' positions away, where shift = S - mid.
            max_val = query_max(l, l + mid - 1)
            if mid + max_val <= S:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        results.append(str(ans))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
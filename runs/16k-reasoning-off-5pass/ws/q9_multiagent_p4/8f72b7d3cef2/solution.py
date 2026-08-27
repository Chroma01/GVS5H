import sys
import bisect

# Increase recursion depth to handle deep segment tree recursion if necessary
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Prefix sums P, where P[i] is sum of A[0]...A[i-1]
    # P[0] = 0
    # P[k] = sum(A[0]...A[k-1])
    P = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum += A[i]
        P[i+1] = current_sum

    # Q_vals[i] = P[i+1] + A[i] for i in 0..N-2
    # This value represents the threshold at index i to stop absorbing to the left.
    # Condition to stop at i (i not absorbed): Q_vals[i] >= P[K+1]
    Q_vals = []
    for i in range(N - 1):
        val = P[i+1] + A[i]
        Q_vals.append(val)
    
    # R_vals[j] = P[j] - A[j] for j in 1..N-1
    # This value represents the threshold at index j to stop absorbing to the right.
    # Condition to stop at j (j not absorbed): R_vals[j] <= P[K]
    R_vals = []
    for j in range(1, N):
        val = P[j] - A[j]
        R_vals.append(val)

    # Coordinate Compression for Q
    sorted_Q = sorted(list(set(Q_vals)))
    rank_Q = {v: i for i, v in enumerate(sorted_Q)}
    M_Q = len(sorted_Q)
    
    # Coordinate Compression for R
    sorted_R = sorted(list(set(R_vals)))
    rank_R = {v: i for i, v in enumerate(sorted_R)}
    M_R = len(sorted_R)

    # Segment Tree for Q: Stores max index for a range of ranks
    # Tree size 4 * M_Q
    tree_Q = [-1] * (4 * M_Q)
    
    def update_Q(node, start, end, idx, val):
        if start == end:
            tree_Q[node] = max(tree_Q[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            update_Q(2 * node, start, mid, idx, val)
        else:
            update_Q(2 * node + 1, mid + 1, end, idx, val)
        tree_Q[node] = max(tree_Q[2 * node], tree_Q[2 * node + 1])

    def query_Q(node, start, end, l_rank, r_rank):
        if r_rank < l_rank or start > end:
            return -1
        if l_rank <= start and end <= r_rank:
            return tree_Q[node]
        mid = (start + end) // 2
        q1 = query_Q(2 * node, start, mid, l_rank, r_rank)
        q2 = query_Q(2 * node + 1, mid + 1, end, l_rank, r_rank)
        return max(q1, q2)

    # Segment Tree for R: Stores min index for a range of ranks
    tree_R = [float('inf')] * (4 * M_R)

    def update_R(node, start, end, idx, val):
        if start == end:
            tree_R[node] = min(tree_R[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            update_R(2 * node, start, mid, idx, val)
        else:
            update_R(2 * node + 1, mid + 1, end, idx, val)
        tree_R[node] = min(tree_R[2 * node], tree_R[2 * node + 1])

    def query_R(node, start, end, l_rank, r_rank):
        if r_rank < l_rank or start > end:
            return float('inf')
        if l_rank <= start and end <= r_rank:
            return tree_R[node]
        mid = (start + end) // 2
        q1 = query_R(2 * node, start, mid, l_rank, r_rank)
        q2 = query_R(2 * node + 1, mid + 1, end, l_rank, r_rank)
        return min(q1, q2)

    # Calculate Left Boundaries
    left_stop_indices = [-1] * N
    
    # We iterate K from 0 to N-1.
    # For a specific K, we need max index i < K such that Q_vals[i] >= P[K+1].
    # We add Q_vals[K-1] to the tree before querying for K.
    
    for K in range(N):
        # Add left neighbor K-1 if it exists
        if K > 0:
            idx = K - 1
            val = Q_vals[idx]
            r = rank_Q[val]
            update_Q(1, 0, M_Q - 1, r, idx)
        
        # Query for P[K+1]
        target = P[K+1]
        # Find smallest rank with value >= target
        pos = bisect.bisect_left(sorted_Q, target)
        if pos < M_Q:
            r_min = pos
            res_idx = query_Q(1, 0, M_Q - 1, r_min, M_Q - 1)
            if res_idx != -1:
                left_stop_indices[K] = res_idx
            # else remains -1

    # Calculate Right Boundaries
    right_stop_indices = [float('inf')] * N
    
    # We iterate K from N-1 down to 0.
    # For a specific K, we need min index j > K such that R_vals[j] <= P[K].
    # We add R_vals[K+1] to the tree before querying for K.
    
    for K in range(N - 1, -1, -1):
        # Add right neighbor K+1 if it exists
        if K < N - 1:
            idx = K + 1
            val = R_vals[idx]
            r = rank_R[val]
            update_R(1, 0, M_R - 1, r, idx)
        
        # Query for P[K]
        target = P[K]
        # Find largest rank with value <= target
        pos = bisect.bisect_right(sorted_R, target) - 1
        if pos >= 0:
            r_max = pos
            res_idx = query_R(1, 0, M_R - 1, 0, r_max)
            if res_idx != float('inf'):
                right_stop_indices[K] = res_idx
            # else remains inf

    # Compute final answers
    ans = []
    for K in range(N):
        # Left part
        stop_L = left_stop_indices[K]
        if stop_L == -1:
            # Absorb everything to the left (indices 0 to K-1)
            left_sum = P[K+1]
        else:
            # Stop at stop_L. Absorb indices stop_L + 1 to K.
            left_sum = P[K+1] - P[stop_L + 1]
        
        # Right part
        stop_R = right_stop_indices[K]
        if stop_R == float('inf'):
            # Absorb everything to the right (indices K+1 to N-1)
            right_sum = P[N] - P[K]
        else:
            # Stop at stop_R. Absorb indices K to stop_R - 1.
            right_sum = P[stop_R] - P[K]
            
        total = left_sum + right_sum
        ans.append(total)

    print(*(ans))

if __name__ == '__main__':
    solve()
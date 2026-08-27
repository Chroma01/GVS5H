import sys

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    queries = []
    for _ in range(K):
        x, y = map(int, input().split())
        queries.append((x, y, _))
    
    # Precompute prefix sums of A and B
    prefixA = [0] * (N + 1)
    for i in range(N):
        prefixA[i+1] = prefixA[i] + A[i]
    prefixB = [0] * (N + 1)
    for i in range(N):
        prefixB[i+1] = prefixB[i] + B[i]
    
    # Segment tree over original indices
    size = 1
    while size < N:
        size *= 2
    # Initialize arrays
    sum_P = [0] * (2 * size)
    sum_S = [0] * (2 * size)
    min_A = [float('inf')] * (2 * size)
    max_A = [float('-inf')] * (2 * size)
    sum_A = [0] * (2 * size)
    count = [0] * (2 * size)
    lazy_P = [0] * (2 * size)  # number of times to add A_i to P_i
    lazy_S = [0] * (2 * size)  # total B_Y to add to S_i
    
    # Build leaves
    for i in range(N):
        sum_P[size + i] = 0
        sum_S[size + i] = 0
        min_A[size + i] = A[i]
        max_A[size + i] = A[i]
        sum_A[size + i] = A[i]
        count[size + i] = 1
    for i in range(N, size):
        min_A[size + i] = float('inf')
        max_A[size + i] = float('-inf')
        count[size + i] = 0
    # Build internal nodes
    for i in range(size - 1, 0, -1):
        left = 2 * i
        right = 2 * i + 1
        min_A[i] = min(min_A[left], min_A[right])
        max_A[i] = max(max_A[left], max_A[right])
        sum_A[i] = sum_A[left] + sum_A[right]
        count[i] = count[left] + count[right]
    
    def apply(i, p, s):
        # Apply lazy: add p * A_i to P_i, and s to S_i for all elements in node i
        sum_P[i] += p * sum_A[i]
        sum_S[i] += s * count[i]
        lazy_P[i] += p
        lazy_S[i] += s
    
    def push(i):
        if lazy_P[i] != 0 or lazy_S[i] != 0:
            apply(2 * i, lazy_P[i], lazy_S[i])
            apply(2 * i + 1, lazy_P[i], lazy_S[i])
            lazy_P[i] = 0
            lazy_S[i] = 0
    
    def update(i, l, r, B):
        # Update for all elements with A_i >= B in range [l, r)
        if max_A[i] < B:
            return
        if min_A[i] >= B:
            apply(i, 1, B)
            return
        push(i)
        mid = (l + r) // 2
        update(2 * i, l, mid, B)
        update(2 * i + 1, mid, r, B)
        sum_P[i] = sum_P[2 * i] + sum_P[2 * i + 1]
        sum_S[i] = sum_S[2 * i] + sum_S[2 * i + 1]
    
    def query(i, l, r, ql, qr):
        if ql >= r or qr <= l:
            return (0, 0)
        if ql <= l and r <= qr:
            return (sum_P[i], sum_S[i])
        push(i)
        mid = (l + r) // 2
        left = query(2 * i, l, mid, ql, qr)
        right = query(2 * i + 1, mid, r, ql, qr)
        return (left[0] + right[0], left[1] + right[1])
    
    # Sort queries by Y
    queries_sorted = sorted(queries, key=lambda x: x[1])
    answers = [0] * K
    current_Y = 0
    for x, y, idx in queries_sorted:
        while current_Y < y:
            current_Y += 1
            # Update for B[current_Y-1] (0-indexed)
            update(1, 0, size, B[current_Y-1])
        # Query for prefix 0..x
        sum_P_X, sum_S_X = query(1, 0, size, 0, x)
        S_Y = prefixB[y]
        sumA_X = prefixA[x]
        # Answer: 2 * sum_P_X - y * sumA_X - 2 * sum_S_X + x * S_Y
        ans = 2 * sum_P_X - y * sumA_X - 2 * sum_S_X + x * S_Y
        answers[idx] = ans
    
    for ans in answers:
        print(ans)

solve()
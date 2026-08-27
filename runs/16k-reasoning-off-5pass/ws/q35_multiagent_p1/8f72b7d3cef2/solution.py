import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    
    # For each index i, find the previous greater or equal element index
    # prev_ge[i] = index of the nearest j < i such that A[j] >= A[i], or -1 if none
    prev_ge = [-1] * N
    stack = []  # stack stores indices, maintaining decreasing order of A values
    
    for i in range(N):
        # We want the nearest previous element >= A[i]
        # So we pop elements from stack that are < A[i]
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            prev_ge[i] = stack[-1]
        stack.append(i)
    
    # For each index i, find the next greater or equal element index
    # next_ge[i] = index of the nearest j > i such that A[j] >= A[i], or N if none
    next_ge = [N] * N
    stack = []  # stack stores indices, maintaining decreasing order of A values
    
    for i in range(N-1, -1, -1):
        # We want the nearest next element >= A[i]
        # So we pop elements from stack that are < A[i]
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            next_ge[i] = stack[-1]
        stack.append(i)
    
    # Compute prefix sums for efficient range sum queries
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i+1] = prefix_sum[i] + A[i]
    
    def range_sum(l, r):
        """Sum of A[l..r] inclusive, 0-indexed"""
        if l > r:
            return 0
        return prefix_sum[r+1] - prefix_sum[l]
    
    # For each K (0-indexed), the answer is the sum of A[prev_ge[K]+1 .. next_ge[K]-1]
    results = []
    for k in range(N):
        l = prev_ge[k] + 1
        r = next_ge[k] - 1
        ans = range_sum(l, r)
        results.append(str(ans))
    
    print(' '.join(results))

solve()
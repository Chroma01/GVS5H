import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    
    # Precompute prefix sums for O(1) range sum queries
    # prefix[i] = sum(A[0]...A[i-1])
    prefix = [0] * (N + 1)
    for i in range(N):
        prefix[i+1] = prefix[i] + A[i]
        
    def range_sum(l, r):
        # Sum of A[l..r] inclusive (0-based)
        if l > r:
            return 0
        return prefix[r+1] - prefix[l]
    
    # Find previous greater or equal element index for each i
    # prev_ge[i] = index of nearest j < i such that A[j] >= A[i]
    # If no such j exists, prev_ge[i] = -1
    prev_ge = [-1] * N
    stack = []  # Stack stores indices
    
    for i in range(N):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            prev_ge[i] = stack[-1]
        stack.append(i)
        
    # Find next greater or equal element index for each i
    # next_ge[i] = index of nearest j > i such that A[j] >= A[i]
    # If no such j exists, next_ge[i] = N
    next_ge = [N] * N
    stack = []
    
    for i in range(N-1, -1, -1):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            next_ge[i] = stack[-1]
        stack.append(i)
        
    # For each K (0-based index), the range is (prev_ge[K]+1, next_ge[K]-1)
    results = []
    for i in range(N):
        l = prev_ge[i] + 1
        r = next_ge[i] - 1
        s = range_sum(l, r)
        results.append(str(s))
        
    print(' '.join(results))

if __name__ == '__main__':
    solve()
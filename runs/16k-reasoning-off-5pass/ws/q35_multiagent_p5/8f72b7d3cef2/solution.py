import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i+1] = prefix_sum[i] + A[i]
        
    def range_sum(l, r):
        if l > r:
            return 0
        return prefix_sum[r+1] - prefix_sum[l]

    left = [-1] * N
    stack = []
    for i in range(N):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
        
    right = [N] * N
    stack = []
    for i in range(N-1, -1, -1):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
        
    ans = [0] * N
    
    for K in range(N):
        L = left[K]
        R = right[K]
        S = A[K]
        
        current_sum = range_sum(L+1, R-1)
        S += current_sum
        
        while L >= 0 and A[L] < S:
            S += A[L]
            L -= 1
            
        while R < N and A[R] < S:
            S += A[R]
            R += 1
            
        ans[K] = S
        
    print(" ".join(map(str, ans)))

if __name__ == '__main__':
    solve()
import sys

def solve():
    # Increase recursion depth just in case, though we use iterative approach
    sys.setrecursionlimit(2000000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # We need to find for each index i:
    # L[i]: the index of the nearest element to the left such that A[L[i]] >= A[i]
    # R[i]: the index of the nearest element to the right such that A[R[i]] >= A[i]
    # If no such element exists, L[i] = -1 and R[i] = n
    
    # Using monotonic stack to find Previous Greater or Equal (PGE)
    # Stack will store indices. We want the nearest element >= current.
    # We maintain a stack of indices such that A[stack[j]] is decreasing?
    # No, for PGE (>=), we want to find the first element to the left that is >=.
    # Standard monotonic stack for Next Greater Element:
    # To find PGE: iterate left to right. Maintain stack of indices with decreasing values?
    # If we want the nearest >=, we pop elements that are < current.
    # The top of the stack after popping will be the PGE.
    
    pge = [-1] * n
    stack = []
    
    for i in range(n):
        # We want nearest to left >= A[i]
        # Pop elements that are strictly smaller than A[i]
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        
        if stack:
            pge[i] = stack[-1]
        else:
            pge[i] = -1
            
        stack.append(i)
        
    # To find NGE: iterate right to left.
    nge = [n] * n
    stack = []
    
    for i in range(n-1, -1, -1):
        # We want nearest to right >= A[i]
        # Pop elements that are strictly smaller than A[i]
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
            
        if stack:
            nge[i] = stack[-1]
        else:
            nge[i] = n
            
        stack.append(i)
        
    # Compute prefix sums for range sum queries
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + a[i]
        
    # Calculate answer for each K
    results = []
    for i in range(n):
        # The range of absorbable slimes is (pge[i], nge[i]) exclusive
        # i.e., from pge[i] + 1 to nge[i] - 1 inclusive
        left_idx = pge[i] + 1
        right_idx = nge[i] - 1
        
        if left_idx <= right_idx:
            total = prefix_sum[right_idx + 1] - prefix_sum[left_idx]
        else:
            total = 0
            
        results.append(str(total))
        
    print(" ".join(results))

if __name__ == '__main__':
    solve()
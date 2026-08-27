import sys

# Increase recursion depth just in case, though not using recursion here
sys.setrecursionlimit(2000)

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

    # Prefix sums for O(1) range sum queries
    # P[i] = sum(A[0]...A[i-1])
    # sum(A[l]...A[r]) = P[r+1] - P[l]
    P = [0] * (N + 1)
    for i in range(N):
        P[i+1] = P[i] + A[i]

    # Function to compute L array
    # L[i] is the nearest index j < i such that A[j] >= sum(j+1, i)
    # If no such j exists, L[i] = -1
    def compute_L(arr, P):
        n = len(arr)
        L = [-1] * n
        stack = [] # stores indices
        
        # We maintain a stack of indices j such that B[j] = arr[j] + P[j+1] is strictly decreasing.
        # For a current i, we want the largest j < i such that B[j] >= P[i+1].
        # Since B is decreasing in the stack, the largest j satisfying the condition is the top of the stack
        # IF B[top] >= P[i+1]. If B[top] < P[i+1], then no element in the stack satisfies it (since B is decreasing).
        
        for i in range(n):
            # Query
            # Check top of stack
            if stack:
                top_idx = stack[-1]
                if (arr[top_idx] + P[top_idx+1]) >= P[i+1]:
                    L[i] = top_idx
                else:
                    L[i] = -1
            else:
                L[i] = -1
            
            # Update
            # We want to maintain decreasing B. If current B_i <= B[top], then top is dominated by i?
            # No, if B[top] <= B[i], then for any future X, if B[top] >= X, then B[i] >= X.
            # And i is a larger index (better candidate for "nearest" if we were looking for max index, 
            # but here we are looking for max j < i for the current step, and for future steps i is a better candidate than top).
            # Wait, for future steps k > i, we want max j < k. i is larger than top.
            # So if B[i] >= B[top], then i is a better candidate than top for any X <= B[top].
            # So we can pop top.
            B_i = arr[i] + P[i+1]
            while stack and (arr[stack[-1]] + P[stack[-1]+1]) <= B_i:
                stack.pop()
            stack.append(i)
            
        return L

    # Compute L for original array
    L = compute_L(A, P)

    # Compute R using reversed array
    # R[i] is the nearest index j > i such that A[j] >= sum(i, j)
    # This is symmetric to L in the reversed array.
    # Let A_rev[k] = A[N-1-k].
    # Then R[i] = N - 1 - L_rev[N - 1 - i]
    
    A_rev = A[::-1]
    P_rev = [0] * (N + 1)
    for i in range(N):
        P_rev[i+1] = P_rev[i] + A_rev[i]
    
    L_rev = compute_L(A_rev, P_rev)
    
    R = [0] * N
    for i in range(N):
        idx = N - 1 - i
        if L_rev[idx] != -1:
            R[i] = N - 1 - L_rev[idx]
        else:
            R[i] = N

    # Compute answers
    ans = []
    for i in range(N):
        l_bound = L[i] + 1
        r_bound = R[i] - 1
        
        if l_bound > r_bound:
            ans.append(A[i])
        else:
            s = P[r_bound+1] - P[l_bound]
            ans.append(s)
            
    print(*(ans))

if __name__ == '__main__':
    solve()
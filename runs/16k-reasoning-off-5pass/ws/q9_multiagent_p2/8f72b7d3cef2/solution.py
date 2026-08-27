import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
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

    # Precompute prefix sums for O(1) range sum queries
    # prefix_sum[i] will store sum(A[0]...A[i-1])
    prefix_sum = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum += A[i]
        prefix_sum[i+1] = current_sum
    
    def get_range_sum(l, r):
        # Sum of A[l...r] inclusive (0-based indices)
        # Using prefix_sum: sum(l, r) = prefix_sum[r+1] - prefix_sum[l]
        return prefix_sum[r+1] - prefix_sum[l]

    # Compute L[i]: index of the nearest element to the left such that A[L[i]] >= A[i]
    # If no such element exists, L[i] = -1.
    # We use a monotonic stack to find the previous greater or equal element.
    # The stack will store indices. We maintain the property that values corresponding to 
    # indices in the stack are non-increasing.
    L = [-1] * N
    stack = []
    for i in range(N):
        # Pop elements that are strictly smaller than current A[i]
        # because they cannot be the "nearest greater or equal" for current or future elements
        # if A[i] is larger.
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        
        if stack:
            L[i] = stack[-1]
        else:
            L[i] = -1
        
        stack.append(i)

    # Compute R[i]: index of the nearest element to the right such that A[R[i]] >= A[i]
    # If no such element exists, R[i] = N.
    # We scan from right to left.
    R = [N] * N
    stack = []
    for i in range(N-1, -1, -1):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        
        if stack:
            R[i] = stack[-1]
        else:
            R[i] = N
        
        stack.append(i)

    # Calculate answers
    # For each starting position i, Takahashi can absorb all slimes in the range (L[i], R[i]).
    # The range is exclusive of L[i] and R[i].
    # The indices to sum are from L[i] + 1 to R[i] - 1.
    # Note: Since L[i] < i < R[i], the range always includes i itself.
    
    results = []
    for i in range(N):
        l_idx = L[i]
        r_idx = R[i]
        
        start = l_idx + 1
        end = r_idx - 1
        
        # Calculate sum of A[start...end]
        ans = get_range_sum(start, end)
        results.append(str(ans))

    print(" ".join(results))

if __name__ == '__main__':
    solve()
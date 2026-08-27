import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    # Collect positions of all '1's (0-indexed)
    ones = [i for i, c in enumerate(S) if c == '1']
    k = len(ones)
    
    # If there are 0 or 1 ones, they are already contiguous
    if k <= 1:
        print(0)
        return
    
    # Transform positions: q[i] = ones[i] - i
    # This transforms the problem into finding a target start position s
    # that minimizes sum(|q[i] - s|) for i in 0..k-1
    q = [ones[i] - i for i in range(k)]
    
    # Sort q to find the median
    q.sort()
    
    # The optimal s is the median of q
    # For even k, any value between the two middle elements works, 
    # but since we need an integer and the cost function is convex,
    # taking q[k//2] is sufficient.
    s_opt = q[k // 2]
    
    # The block of 1s must fit in [0, N-1], so s must be in [0, N-k]
    s_min = 0
    s_max = N - k
    
    # Clamp s_opt to the valid range [s_min, s_max]
    s = max(s_min, min(s_max, s_opt))
    
    # Calculate the total cost
    cost = sum(abs(qi - s) for qi in q)
    
    print(cost)

if __name__ == '__main__':
    solve()
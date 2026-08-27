import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Collect indices of all '1's
    ones_indices = [i for i, char in enumerate(s) if char == '1']
    k = len(ones_indices)

    # If there are no 1s, cost is 0 (though problem guarantees at least one 1)
    if k == 0:
        print(0)
        return

    # Transform the problem:
    # We want to move ones at positions p_0, p_1, ..., p_{k-1} to positions l, l+1, ..., l+k-1.
    # The cost is sum(|p_i - (l + i)|) for i from 0 to k-1.
    # This can be rewritten as sum(|(p_i - i) - l|).
    # Let q_i = p_i - i. We need to find an integer l that minimizes sum(|q_i - l|).
    # The value of l that minimizes the sum of absolute differences is the median of q.
    
    q = [p - i for i, p in enumerate(ones_indices)]
    q.sort()
    
    # The optimal unconstrained l is the median of q.
    # Since we need an integer l, and the function is convex, the integer median works.
    # For a list of length k, the median is at index k // 2.
    median_l = q[k // 2]
    
    # The valid range for l is [0, n - k] because the block of 1s must fit in the string.
    # The function f(l) = sum(|q_i - l|) is convex.
    # The minimum over the valid range [0, n-k] is at:
    # - median_l if 0 <= median_l <= n - k
    # - 0 if median_l < 0
    # - n - k if median_l > n - k
    
    optimal_l = median_l
    if optimal_l < 0:
        optimal_l = 0
    elif optimal_l > n - k:
        optimal_l = n - k
        
    # Calculate the cost for the optimal l
    # Cost = sum(|ones_indices[i] - (optimal_l + i)|)
    total_ops = 0
    for i, p in enumerate(ones_indices):
        target_pos = optimal_l + i
        total_ops += abs(p - target_pos)
        
    print(total_ops)

if __name__ == '__main__':
    solve()
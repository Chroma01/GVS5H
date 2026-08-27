import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Step 1: Find positions of all '1's (0-indexed)
    ones_positions = [i for i, char in enumerate(s) if char == '1']
    k = len(ones_positions)
    
    if k <= 1:
        # If there are 0 or 1 ones, they are already contiguous
        print(0)
        return
    
    # Step 2: Compute q_i = p_i - i
    # p_i is the position of the i-th '1'
    q = [ones_positions[i] - i for i in range(k)]
    
    # Step 3: Find the median of q
    # Sort q to find the median
    q.sort()
    
    # For minimizing sum of absolute differences, the median is optimal.
    # If k is odd, median is q[k//2].
    # If k is even, any value between q[k//2 - 1] and q[k//2] works.
    # We can pick q[k//2] as it's one of the medians.
    median = q[k // 2]
    
    # Step 4: Calculate total cost
    total_swaps = sum(abs(val - median) for val in q)
    
    print(total_swaps)

if __name__ == '__main__':
    solve()
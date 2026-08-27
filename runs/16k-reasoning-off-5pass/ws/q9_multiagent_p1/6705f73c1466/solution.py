import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Collect indices of all '1's (0-based)
    ones_indices = [i for i, char in enumerate(s) if char == '1']
    
    k = len(ones_indices)
    if k == 0:
        print(0)
        return

    # Transform indices: q_i = p_i - i
    # We want to minimize sum(|p_i - (target_start + i)|)
    # Let target_start = x. Then target position for i-th '1' is x + i.
    # Cost = sum(|p_i - (x + i)|) = sum(|(p_i - i) - x|)
    # Let q_i = p_i - i. We need to find x that minimizes sum(|q_i - x|).
    # The optimal x is the median of q_i.
    
    q = [p - i for i, p in enumerate(ones_indices)]
    
    # Sort q to find the median
    q.sort()
    
    # The median for an odd number of elements is the middle one.
    # For an even number, any value between the two middle elements (inclusive) works.
    # We can pick the element at index k // 2.
    median_x = q[k // 2]
    
    # Calculate the total cost
    total_ops = 0
    for val in q:
        total_ops += abs(val - median_x)
        
    print(total_ops)

if __name__ == '__main__':
    solve()
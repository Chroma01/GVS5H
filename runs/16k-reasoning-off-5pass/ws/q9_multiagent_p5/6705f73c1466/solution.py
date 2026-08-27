import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Count total number of '1's
    total_ones = s.count('1')
    
    # If there are no '1's or only one '1', they are already contiguous
    if total_ones <= 1:
        print(0)
        return

    # Collect indices of all '1's (0-indexed)
    ones_indices = [i for i, char in enumerate(s) if char == '1']
    
    # Compute q_i = p_i - i for each 1
    # p_i is the index in the original string (0-based)
    # i is the rank of the 1 (0-based, 0th 1, 1st 1, ...)
    # We use 0-based rank for calculation: rank = index in ones_indices
    # So q_i = ones_indices[rank] - rank
    q = [ones_indices[i] - i for i in range(len(ones_indices))]
    
    # Find the median of q
    # Since we want to minimize sum of absolute differences, the optimal l is the median
    # If the number of elements is odd, median is the middle element.
    # If even, any integer between the two middle elements (inclusive) works.
    # We can simply pick the element at index len(q) // 2.
    median = q[len(q) // 2]
    
    # Calculate the cost: sum of |q_i - median|
    # This corresponds to the minimum number of swaps required
    ans = sum(abs(val - median) for val in q)
    
    print(ans)

if __name__ == '__main__':
    solve()
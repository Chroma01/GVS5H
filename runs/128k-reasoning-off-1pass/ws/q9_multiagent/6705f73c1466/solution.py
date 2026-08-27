import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Collect indices of all '1's (0-indexed)
    ones_indices = [i for i, char in enumerate(s) if char == '1']
    k = len(ones_indices)

    # If there are no 1s or only one 1, cost is 0 (though problem guarantees at least one 1)
    if k <= 1:
        print(0)
        return

    # Calculate adjusted indices: q_i = p_i - i
    # This transforms the problem to finding a target position 'l' 
    # that minimizes sum(|q_i - l|)
    adjusted_indices = [ones_indices[i] - i for i in range(k)]

    # Find the median of adjusted_indices
    # Since we need to minimize sum of absolute differences, the median is the optimal l.
    # If k is odd, median is at index k//2.
    # If k is even, any integer between the two middle elements works; we pick the lower one (k//2).
    median_val = adjusted_indices[k // 2]

    # The target block of 1s must fit within the string [0, N-1].
    # The block starts at 'l' and ends at 'l + k - 1'.
    # Constraints: 0 <= l and l + k - 1 < N  =>  0 <= l <= N - k
    min_l = 0
    max_l = n - k

    # Clamp the optimal median to the valid range
    optimal_l = max(min_l, min(max_l, median_val))

    # Calculate the total cost (number of swaps)
    # Cost = sum(|ones_indices[i] - (optimal_l + i)|)
    #      = sum(|(ones_indices[i] - i) - optimal_l|)
    #      = sum(|adjusted_indices[i] - optimal_l|)
    total_cost = sum(abs(x - optimal_l) for x in adjusted_indices)

    print(total_cost)

if __name__ == '__main__':
    solve()
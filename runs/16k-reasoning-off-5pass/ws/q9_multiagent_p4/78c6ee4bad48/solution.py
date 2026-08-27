import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        X = []
        for _ in range(N):
            X.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem asks us to minimize the sum of coordinates of N pieces.
    # We can perform an operation on index i (1-based) which affects pieces i, i+1, i+2, i+3.
    # Specifically, pieces i+1 and i+2 are moved to be symmetric around the midpoint of i and i+3.
    # Let the coordinates be x_i, x_{i+1}, x_{i+2}, x_{i+3}.
    # The new coordinates for the middle two become:
    # x'_{i+1} = x_i + x_{i+3} - x_{i+2}
    # x'_{i+2} = x_i + x_{i+3} - x_{i+1}
    #
    # The sum of the middle two elements changes from S_mid = x_{i+1} + x_{i+2} to:
    # S'_mid = 2*(x_i + x_{i+3}) - (x_{i+1} + x_{i+2})
    #
    # The total sum decreases if S'_mid < S_mid, which implies:
    # 2*(x_i + x_{i+3}) < 2*(x_{i+1} + x_{i+2})  =>  x_i + x_{i+3} < x_{i+1} + x_{i+2}
    #
    # To achieve the global minimum, we should greedily apply this operation whenever the condition holds.
    # The crucial observation is the order of operations. The operation at index i modifies x_{i+1} and x_{i+2}.
    # These modified values serve as anchors (specifically x_{i+2}) for the operation at index i-1.
    # Therefore, to ensure that the operation at i-1 uses the most optimized possible value for its right anchor,
    # we must process the operations from right to left (from N-4 down to 0 in 0-based indexing).
    
    # In 0-based indexing:
    # The valid range for the starting index of the window (j) is 0 to N-4.
    # The window consists of indices j, j+1, j+2, j+3.
    # The pieces moved are j+1 and j+2.
    # The anchors are j and j+3.
    
    # Iterate from right to left
    for j in range(N - 4, -1, -1):
        # Check condition: sum of anchors < sum of middle
        if X[j] + X[j+3] < X[j+1] + X[j+2]:
            # Apply operation
            # We must use the OLD values of X[j+1] and X[j+2] to calculate the new ones.
            # If we update X[j+1] first, we lose the old value needed for X[j+2].
            
            sum_anchors = X[j] + X[j+3]
            old_x_j1 = X[j+1]
            old_x_j2 = X[j+2]
            
            # Calculate new positions
            new_x_j1 = sum_anchors - old_x_j2
            new_x_j2 = sum_anchors - old_x_j1
            
            # Update the list
            X[j+1] = new_x_j1
            X[j+2] = new_x_j2
            
    # Calculate final sum
    total_sum = sum(X)
    print(total_sum)

if __name__ == '__main__':
    solve()
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
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        C = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Identify mismatches and calculate initial sum
    # A and B are 0-indexed in our list
    initial_sum = 0
    deltas = []
    
    for i in range(N):
        val_a = A[i]
        val_b = B[i]
        cost_c = C[i]
        
        # Add to initial sum based on current A[i]
        initial_sum += val_a * cost_c
        
        if val_a != val_b:
            # We need to flip A[i] exactly once
            # If A[i] is 0, it becomes 1. Sum increases by C[i]. Delta = +C[i]
            # If A[i] is 1, it becomes 0. Sum decreases by C[i]. Delta = -C[i]
            if val_a == 0:
                deltas.append(cost_c)
            else:
                deltas.append(-cost_c)

    # Sort deltas in ascending order to minimize total cost.
    # Logic: Total Cost = sum(S_after_j) for j=1 to k.
    # S_after_j = S_0 + sum(deltas processed so far).
    # Expanding the sum, the contribution of a delta is delta * (number of operations remaining including current).
    # To minimize the sum, we want larger multipliers (k, k-1, ...) to be paired with smaller (more negative) deltas.
    # Smaller multipliers (1) should be paired with larger (positive) deltas.
    # Thus, sorting deltas in ascending order achieves this optimal pairing.
    deltas.sort()
    
    total_cost = 0
    current_sum = initial_sum
    
    for delta in deltas:
        current_sum += delta
        total_cost += current_sum
        
    print(total_cost)

if __name__ == '__main__':
    solve()
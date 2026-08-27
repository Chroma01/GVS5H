import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from standard input efficiently
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

    # Calculate the initial weighted sum S = sum(A[i] * C[i])
    # This represents the cost incurred if we were to stop immediately (though we must flip)
    # It serves as the base for calculating operation costs.
    current_sum = 0
    for i in range(N):
        if A[i] == 1:
            current_sum += C[i]
    
    total_cost = 0
    
    # Identify indices that need to be flipped.
    # We categorize them into two sets based on the transition required:
    # U: Indices where A[i] == 1 and B[i] == 0. We need to flip 1 -> 0.
    #    Flipping 1->0 reduces the current_sum by C[i].
    #    Cost of this operation is (current_sum - C[i]).
    # V: Indices where A[i] == 0 and B[i] == 1. We need to flip 0 -> 1.
    #    Flipping 0->1 increases the current_sum by C[i].
    #    Cost of this operation is (current_sum + C[i]).
    
    U = [] # Stores (C[i], i) for 1->0 transitions
    V = [] # Stores (C[i], i) for 0->1 transitions
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                U.append((C[i], i))
            else:
                V.append((C[i], i))
    
    # Optimal Strategy Analysis:
    # The total cost depends on the order of operations.
    # 1. For U (1->0): We want to subtract large C[i] values from current_sum as early as possible
    #    to minimize the base for subsequent operations. Hence, sort U by C[i] descending.
    # 2. For V (0->1): We want to add large C[i] values to current_sum as late as possible
    #    because adding to current_sum increases the cost of all subsequent operations.
    #    Hence, sort V by C[i] ascending.
    # 3. We should perform all U operations before all V operations.
    #    Performing a 0->1 operation increases current_sum, which makes subsequent 1->0 operations
    #    (which subtract from current_sum) less effective at reducing the base for future costs.
    #    Conversely, reducing current_sum via 1->0 operations before increasing it via 0->1
    #    operations minimizes the cumulative cost.
    
    U.sort(key=lambda x: x[0], reverse=True)
    V.sort(key=lambda x: x[0])
    
    # Execute operations in the optimal order: U followed by V
    ops = U + V
    
    for cost_val, idx in ops:
        if A[idx] == 1:
            # Flip 1 -> 0
            # Cost incurred is the current weighted sum minus the value of the bit being removed
            total_cost += current_sum - cost_val
            current_sum -= cost_val
        else:
            # Flip 0 -> 1
            # Cost incurred is the current weighted sum plus the value of the bit being added
            total_cost += current_sum + cost_val
            current_sum += cost_val
            
    print(total_cost)

if __name__ == '__main__':
    solve()
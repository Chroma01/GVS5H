import sys

def solve():
    # Read all input from stdin
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

    # Identify indices where A[i] != B[i]
    # These are the indices that need to be flipped.
    # We assume each such index is flipped exactly once.
    
    P = [] # Indices where A[i] == 1 and A[i] != B[i] (will flip 1 -> 0)
    Z = [] # Indices where A[i] == 0 and A[i] != B[i] (will flip 0 -> 1)
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                P.append((C[i], i))
            else:
                Z.append((C[i], i))
                
    # Sort P by C[i] descending
    P.sort(key=lambda x: x[0], reverse=True)
    
    # Sort Z by C[i] ascending
    Z.sort(key=lambda x: x[0])
    
    # Optimal order: P followed by Z
    order = P + Z
    
    # Calculate initial sum of C[k] for all k where A[k] == 1
    current_sum = 0
    for i in range(N):
        if A[i] == 1:
            current_sum += C[i]
            
    total_cost = 0
    
    # Simulate the flips in the optimal order
    for c_val, i in order:
        # Cost of this operation is the current sum of C[k] for all k where A[k] == 1
        total_cost += current_sum
        
        # Flip A[i]
        if A[i] == 1:
            # It was 1, becomes 0. The sum decreases by C[i].
            current_sum -= C[i]
            A[i] = 0
        else:
            # It was 0, becomes 1. The sum increases by C[i].
            current_sum += C[i]
            A[i] = 1
            
    print(total_cost)

if __name__ == '__main__':
    solve()
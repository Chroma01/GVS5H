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
    # We need to flip these indices.
    # Indices where A[i] == B[i] are static.
    
    # Static cost calculation:
    # For any index i where A[i] == B[i], A[i] never changes.
    # If A[i] == 1, it contributes C[i] to the cost of EVERY operation.
    # Total operations = number of mismatches (K).
    # So contribution is K * A[i] * C[i].
    
    # Dynamic cost calculation:
    # For indices where A[i] != B[i], we must flip them.
    # Let K be the total number of such indices.
    # We split them into two groups:
    # 1. S_10: A[i] == 1, B[i] == 0 (Flip 1 -> 0)
    # 2. S_01: A[i] == 0, B[i] == 1 (Flip 0 -> 1)
    
    # Optimal Strategy:
    # - Perform all S_10 flips first (to minimize their cost contribution).
    # - Perform all S_01 flips last (to minimize their cost contribution).
    # - Within S_10, sort by C[i] ascending (assign smaller t to smaller C).
    # - Within S_01, sort by C[i] descending (assign larger t to larger C).
    
    s_10 = [] # Stores C[i] for 1->0
    s_01 = [] # Stores C[i] for 0->1
    static_cost = 0
    
    K = 0
    
    for i in range(N):
        if A[i] != B[i]:
            K += 1
            if A[i] == 1:
                s_10.append(C[i])
            else:
                s_01.append(C[i])
        else:
            if A[i] == 1:
                static_cost += C[i]
    
    # Total cost from static indices
    total_cost = static_cost * K
    
    # Process S_10 (1 -> 0)
    # Cost contribution for index i flipped at step t (1-based):
    # A[i] starts at 1, becomes 0 at step t.
    # Value is 1 for steps 1 to t-1. Value is 0 for steps t to K.
    # Sum of values = (t-1) * 1 + (K - t + 1) * 0 = t - 1.
    # We want to minimize sum(C[i] * (t-1)).
    # Sort s_10 ascending. Assign t = 1, 2, ..., len(s_10).
    s_10.sort()
    k1 = len(s_10)
    for idx, val in enumerate(s_10):
        # t = idx + 1
        # term = val * (t - 1) = val * idx
        total_cost += val * idx
        
    # Process S_01 (0 -> 1)
    # Cost contribution for index i flipped at step t (1-based):
    # A[i] starts at 0, becomes 1 at step t.
    # Value is 0 for steps 1 to t-1. Value is 1 for steps t to K.
    # Sum of values = (t-1) * 0 + (K - t + 1) * 1 = K - t + 1.
    # We want to minimize sum(C[i] * (K - t + 1)).
    # This is equivalent to maximizing sum(C[i] * t).
    # Sort s_01 descending. Assign t = k1 + 1, k1 + 2, ..., K.
    s_01.sort(reverse=True)
    k2 = len(s_01)
    for idx, val in enumerate(s_01):
        # t = k1 + idx + 1
        # term = val * (K - t + 1) = val * (K - (k1 + idx + 1) + 1) = val * (K - k1 - idx)
        total_cost += val * (K - k1 - idx)
        
    print(total_cost)

if __name__ == '__main__':
    solve()
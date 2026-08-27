import sys

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

    # Identify indices to flip and their costs
    # S0: A[i] == 0, B[i] == 1 (needs 0 -> 1)
    # S1: A[i] == 1, B[i] == 0 (needs 1 -> 0)
    # Static: A[i] == B[i]
    
    S0 = [] # Stores costs for 0->1 flips
    S1 = [] # Stores costs for 1->0 flips
    
    for i in range(N):
        if A[i] == 0 and B[i] == 1:
            S0.append(C[i])
        elif A[i] == 1 and B[i] == 0:
            S1.append(C[i])
        elif A[i] == 1:
            # Static 1s contribute C[i] for every operation
            pass
        else:
            # Static 0s contribute 0
            pass

    # Sort descending by cost to optimize the order of operations
    # This is based on the rearrangement inequality to minimize the total cost
    S0.sort(reverse=True)
    S1.sort(reverse=True)

    T = len(S0) + len(S1)
    
    total_cost = 0
    
    # 1. Static 1s contribution: C[i] * T
    # Indices where A[i] == B[i] == 1 are always 1 during all T operations
    # because they never change.
    for i in range(N):
        if A[i] == 1 and B[i] == 1:
            total_cost += C[i] * T
            
    # 2. S1 contribution: sum(C[i] * (t_i - 1))
    # We perform all S1 operations first (times 1 to len(S1)).
    # An index flipped at time t contributes to costs of operations 1..t-1.
    # Multipliers are 0, 1, ..., len(S1)-1.
    # Since S1 is sorted descending, we pair largest C with smallest multiplier (0).
    for idx, cost in enumerate(S1):
        total_cost += cost * idx
        
    # 3. S0 contribution: sum(C[i] * (T - t_i + 1))
    # We perform all S0 operations last (times len(S1)+1 to T).
    # An index flipped at time t contributes to costs of operations t..T.
    # Multipliers are len(S0), len(S0)-1, ..., 1.
    # Since S0 is sorted descending, we pair largest C with largest multiplier (len(S0)).
    len_S0 = len(S0)
    for idx, cost in enumerate(S0):
        total_cost += cost * (len_S0 - idx)
        
    print(total_cost)

if __name__ == '__main__':
    solve()
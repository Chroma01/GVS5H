import sys

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

    # Identify indices where A[i] != B[i]
    # U: costs for indices where A[i] == 1 and B[i] == 0 (need to flip 1 -> 0)
    # V: costs for indices where A[i] == 0 and B[i] == 1 (need to flip 0 -> 1)
    U = []
    V = []
    
    for i in range(N):
        if A[i] == 1 and B[i] == 0:
            U.append(C[i])
        elif A[i] == 0 and B[i] == 1:
            V.append(C[i])
            
    # Strategy:
    # 1. Process flips that reduce the sum (1 -> 0) first.
    #    To minimize cost, we should reduce the largest costs first so the running sum drops quickly.
    #    Sort U in descending order.
    # 2. Process flips that increase the sum (0 -> 1) next.
    #    To minimize cost, we should add the smallest costs first so the running sum grows slowly.
    #    Sort V in ascending order.
    
    U.sort(reverse=True)
    V.sort()
    
    # Calculate initial weighted sum of A
    current_sum = sum(A[i] * C[i] for i in range(N))
    
    total_cost = 0
    
    # Process U (flip 1 -> 0)
    # When flipping A[i] from 1 to 0:
    # - The value of A[i] becomes 0.
    # - The new sum is current_sum - C[i].
    # - The cost paid is the new sum.
    for cost in U:
        total_cost += (current_sum - cost)
        current_sum -= cost
        
    # Process V (flip 0 -> 1)
    # When flipping A[i] from 0 to 1:
    # - The value of A[i] becomes 1.
    # - The new sum is current_sum + C[i].
    # - The cost paid is the new sum.
    for cost in V:
        total_cost += (current_sum + cost)
        current_sum += cost
        
    print(total_cost)

if __name__ == '__main__':
    solve()
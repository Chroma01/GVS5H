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

    # Identify mismatches
    # S1: indices where A[i] == 1 and B[i] == 0 (need to flip 1 -> 0)
    # S0: indices where A[i] == 0 and B[i] == 1 (need to flip 0 -> 1)
    S1 = []
    S0 = []
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                S1.append(C[i])
            else:
                S0.append(C[i])
    
    # If no mismatches, cost is 0
    if not S1 and not S0:
        print(0)
        return

    # Calculate initial sum of C[i] for all i where A[i] == 1
    current_sum = sum(C[i] for i in range(N) if A[i] == 1)
    
    total_cost = 0
    
    # Strategy:
    # 1. Perform all 1->0 flips first, sorted by C[i] descending.
    #    This reduces the current_sum as much as possible early on,
    #    which minimizes the cost for subsequent 0->1 flips.
    #    Within 1->0 flips, doing larger C[i] first minimizes the sum of resulting sums.
    #    Cost of flipping 1->0 with cost C_i is (current_sum - C_i).
    #    New current_sum becomes (current_sum - C_i).
    
    S1.sort(reverse=True)
    for c_val in S1:
        # Cost is the sum of 1s AFTER the flip
        cost = current_sum - c_val
        total_cost += cost
        current_sum -= c_val
        
    # 2. Perform all 0->1 flips, sorted by C[i] ascending.
    #    Cost of flipping 0->1 with cost C_i is (current_sum + C_i).
    #    New current_sum becomes (current_sum + C_i).
    #    Within 0->1 flips, doing smaller C[i] first minimizes the sum of resulting sums.
    
    S0.sort()
    for c_val in S0:
        # Cost is the sum of 1s AFTER the flip
        cost = current_sum + c_val
        total_cost += cost
        current_sum += c_val
        
    print(total_cost)

if __name__ == '__main__':
    solve()
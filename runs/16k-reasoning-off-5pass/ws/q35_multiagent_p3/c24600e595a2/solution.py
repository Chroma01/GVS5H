import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    B = list(map(int, data[N+1:2*N+1]))
    C = list(map(int, data[2*N+1:3*N+1]))
    
    # Identify indices where A[i] != B[i]
    # S0: indices where A[i] = 0 and B[i] = 1 (need to flip 0->1)
    # S1: indices where A[i] = 1 and B[i] = 0 (need to flip 1->0)
    S0 = []  # indices to flip from 0 to 1
    S1 = []  # indices to flip from 1 to 0
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 0:
                S0.append(i)
            else:
                S1.append(i)
    
    # If no flips needed, cost is 0
    if not S0 and not S1:
        print(0)
        return
    
    # Calculate initial weight sum W0 = sum of C[k] for all k where A[k] == 1
    W = sum(C[k] for k in range(N) if A[k] == 1)
    
    # Optimal strategy:
    # 1. Flip all indices in S1 (where A[i]=1, need to flip to 0) in increasing order of C[i]
    # 2. Flip all indices in S0 (where A[i]=0, need to flip to 1) in decreasing order of C[i]
    
    # Sort S1 by C[i] ascending
    S1_sorted = sorted(S1, key=lambda i: C[i])
    # Sort S0 by C[i] descending
    S0_sorted = sorted(S0, key=lambda i: C[i], reverse=True)
    
    total_cost = 0
    
    # Process S1 first (flip 1->0, which decreases W)
    for i in S1_sorted:
        # Cost of this operation is current W
        total_cost += W
        # After flipping, A[i] becomes 0, so W decreases by C[i]
        W -= C[i]
    
    # Process S0 next (flip 0->1, which increases W)
    for i in S0_sorted:
        # Cost of this operation is current W
        total_cost += W
        # After flipping, A[i] becomes 1, so W increases by C[i]
        W += C[i]
    
    print(total_cost)

solve()
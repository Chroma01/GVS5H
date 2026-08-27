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

    # P: indices where A[i]=1 and B[i]=0 (need to flip 1->0)
    # Q: indices where A[i]=0 and B[i]=1 (need to flip 0->1)
    P = []
    Q = []
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                P.append(i)
            else:
                Q.append(i)
    
    m = len(P) + len(Q)
    
    # Base cost: contribution from indices that are never flipped
    # For k not in P U Q, A[k] stays constant.
    # It contributes C[k] for every operation if A[k] == 1.
    base_cost = 0
    for i in range(N):
        if i not in P and i not in Q:
            if A[i] == 1:
                base_cost += m * C[i]
                
    # Constant offset from the expansion of (m - t_k + 1) and (t_k - 1)
    # Sum_{k in Q} (m + 1) C_k - Sum_{k in P} C_k
    sum_C_Q = sum(C[i] for i in Q)
    sum_C_P = sum(C[i] for i in P)
    
    offset = (m + 1) * sum_C_Q - sum_C_P
    
    # Variable part: minimize sum_{k in P U Q} t_k * V_k
    # V_k = C_k if k in P, -C_k if k in Q
    V = []
    for i in P:
        V.append(C[i])
    for i in Q:
        V.append(-C[i])
        
    # Sort V ascending
    V.sort()
    
    # Calculate min variable cost: sum_{j=1 to m} j * V_sorted[j-1]
    var_cost = 0
    for j in range(m):
        var_cost += (j + 1) * V[j]
        
    total_cost = base_cost + offset + var_cost
    print(total_cost)

if __name__ == '__main__':
    solve()
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
    # D0: A[i]=0, B[i]=1 (needs 0->1 flip)
    # D1: A[i]=1, B[i]=0 (needs 1->0 flip)
    D0 = []
    D1 = []
    
    # Constant part components
    # Sum of C[k] for k not in D where A[k] == 1
    sum_C_const = 0
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 0:
                # A[i]=0, B[i]=1
                D0.append(C[i])
            else:
                # A[i]=1, B[i]=0
                D1.append(C[i])
        else:
            # A[i] == B[i]
            if A[i] == 1:
                sum_C_const += C[i]
                
    m = len(D0) + len(D1)
    
    if m == 0:
        print(0)
        return

    # Constant term calculation:
    # Const = m * sum_C_const + (m+1) * sum(D0) - sum(D1)
    sum_D0 = sum(D0)
    sum_D1 = sum(D1)
    
    constant_part = m * sum_C_const + (m + 1) * sum_D0 - sum_D1
    
    # Variable part calculation:
    # Coefficients for indices in D:
    # For k in D1: coeff = +C[k]
    # For k in D0: coeff = -C[k]
    # We want to assign t_k = 1, 2, ..., m to these coefficients in descending order.
    # So we collect all coefficients, sort them descending, and compute sum(t * coeff).
    
    coeffs = []
    for c in D1:
        coeffs.append(c)
    for c in D0:
        coeffs.append(-c)
        
    # Sort coefficients in descending order
    coeffs.sort(reverse=True)
    
    variable_part = 0
    for t, val in enumerate(coeffs, 1):
        variable_part += t * val
        
    total_cost = constant_part + variable_part
    print(total_cost)

if __name__ == '__main__':
    solve()
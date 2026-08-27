import sys
import math

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        C = [int(next(iterator)) for _ in range(N)]
            
    except StopIteration:
        return

    # Sort A, B, C in descending order
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Determine M such that M^3 >= K.
    # We need M to be at least K^(1/3). 
    # Since K <= 5*10^5, M will be around 80.
    # We calculate M precisely.
    M = int(math.ceil(K ** (1/3)))
    
    # Ensure M does not exceed N
    if M > N:
        M = N
        
    # Extract the top M elements
    A_top = A[:M]
    B_top = B[:M]
    C_top = C[:M]
    
    # Generate all combinations
    # The expression is A[i]*B[j] + B[j]*C[k] + C[k]*A[i]
    # = B[j]*(A[i] + C[k]) + C[k]*A[i]
    
    values = []
    # Pre-calculate to avoid repeated lookups
    # Using explicit loops is generally faster than itertools.product for simple arithmetic in Python
    
    for i in range(M):
        ai = A_top[i]
        for j in range(M):
            bj = B_top[j]
            for k in range(M):
                ck = C_top[k]
                # val = ai * bj + bj * ck + ck * ai
                # Optimized: val = bj * (ai + ck) + ck * ai
                val = bj * (ai + ck) + ck * ai
                values.append(val)
                
    # Sort descending
    values.sort(reverse=True)
    
    # The K-th largest is at index K-1
    # Since M^3 >= K, the list 'values' has at least K elements.
    print(values[K-1])

if __name__ == '__main__':
    solve()
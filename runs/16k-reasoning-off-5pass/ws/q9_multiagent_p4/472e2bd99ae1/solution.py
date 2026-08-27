import sys

# Increase recursion depth just in case, though not needed here
sys.setrecursionlimit(2000)

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

    # Sort arrays in descending order
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Determine the number of top elements to consider (M)
    # We need M such that M^3 >= K.
    # Since K <= 5*10^5, M will be small (around 80).
    # We calculate M precisely.
    M = 1
    while M * M * M < K:
        M += 1
    
    # Ensure we don't exceed N
    if M > N:
        M = N
    
    # Extract top M elements
    A_top = A[:M]
    B_top = B[:M]
    C_top = C[:M]
    
    # Generate all combinations and compute values
    # The function f(i, j, k) = A[i]*B[j] + B[j]*C[k] + C[k]*A[i] is monotonic.
    # The top K values must come from the top M elements of each array where M^3 >= K.
    
    # We generate all M^3 values. Since M^3 >= K and K <= 5*10^5, 
    # the number of values is manageable (at most ~512,000 for K=500,000).
    
    # Using a list comprehension for speed
    values = [
        A_top[i] * B_top[j] + B_top[j] * C_top[k] + C_top[k] * A_top[i] 
        for i in range(M) 
        for j in range(M) 
        for k in range(M)
    ]
    
    # Sort values in descending order to find the K-th largest
    values.sort(reverse=True)
    
    # The K-th largest value is at index K-1
    print(values[K-1])

if __name__ == '__main__':
    solve()
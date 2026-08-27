import sys

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
            
        C = []
        for _ in range(N):
            C.append(int(next(iterator)))
            
    except StopIteration:
        return

    # Sort arrays in descending order to access largest elements first
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Determine the number of top elements to consider (M).
    # The function f(i, j, k) = A_i*B_j + B_j*C_k + C_k*A_i is monotonically increasing
    # with respect to each component (since A, B, C >= 1).
    # Therefore, the K largest values in the full set of N^3 combinations must be
    # contained within the combinations formed by the top M elements of each array,
    # where M is the smallest integer such that M^3 >= K.
    # Given K <= 5*10^5, M will be at most 80.
    
    M = 1
    while M * M * M < K:
        M += 1
    
    # Cap M at N (though K <= N^3 implies M <= N naturally)
    limit = min(N, M)
    
    # Extract top M elements
    A_top = A[:limit]
    B_top = B[:limit]
    C_top = C[:limit]
    
    # Generate all combinations of the top M elements
    # The number of combinations is limit^3, which is <= K <= 5*10^5
    values = []
    
    # Pre-calculate loops for efficiency
    for i in range(limit):
        a_val = A_top[i]
        for j in range(limit):
            b_val = B_top[j]
            # The term A_i * B_j is constant for fixed i, j
            # The term B_j * C_k + C_k * A_i = C_k * (B_j + A_i)
            base = a_val * b_val
            factor = b_val + a_val
            
            for k in range(limit):
                c_val = C_top[k]
                val = base + c_val * factor
                values.append(val)
    
    # Sort values in descending order to find the K-th largest
    values.sort(reverse=True)
    
    # The K-th largest value is at index K-1
    print(values[K-1])

if __name__ == '__main__':
    solve()
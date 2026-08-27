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
        n_str = next(iterator)
        N = int(n_str)
    except StopIteration:
        return

    # Constraints: S_i <= 10^6. 
    # We need an array to mark presence. Size 1000002 to handle 1-based indexing up to 10^6 safely.
    MAX_VAL = 1000002
    present = [False] * MAX_VAL
    
    # Read N integers
    count_read = 0
    for _ in range(N):
        try:
            val_str = next(iterator)
            val = int(val_str)
            if 1 <= val < MAX_VAL:
                present[val] = True
                count_read += 1
        except StopIteration:
            break
            
    ans = 0
    
    # Iterate over all possible common differences d.
    # We are looking for triplets (A, B, C) such that B = A + d, C = A + 2d.
    # Since C <= 10^6 (max value in S), we have A + 2d <= 10^6.
    # Since A >= 1, 2d <= 10^6 - 1 => d <= 499999.
    
    limit = 1000000 # Maximum possible value in S
    max_d = limit // 2
    
    # Pre-calculate the range for A to avoid repeated calculations inside the loop
    # For a given d, A can range from 1 to limit - 2*d
    
    for d in range(1, max_d + 1):
        # Determine the upper bound for A
        # A + 2*d <= limit  =>  A <= limit - 2*d
        end_A = limit - 2 * d
        
        # If end_A < 1, no such A exists (loop range handles this naturally, but explicit check is fine)
        if end_A < 1:
            break
            
        # Iterate through all possible starting points A
        # We check if A, A+d, and A+2d are all present in the set
        for A in range(1, end_A + 1):
            if present[A] and present[A + d] and present[A + 2 * d]:
                ans += 1
                
    print(ans)

if __name__ == '__main__':
    solve()
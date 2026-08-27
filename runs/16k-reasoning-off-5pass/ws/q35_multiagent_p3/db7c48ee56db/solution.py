import sys
from itertools import combinations

def solve():
    # Read all input from stdin
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
    except StopIteration:
        return
    
    # Compute total XOR of all elements
    total_xor = 0
    for x in A:
        total_xor ^= x
    
    # We want to choose K elements. 
    # Instead, we choose K' = min(K, N-K) elements.
    # If K <= N-K, we choose K elements directly.
    # If K > N-K, we choose N-K elements to exclude, and the answer is total_xor ^ xor_of_excluded.
    
    K_prime = min(K, N - K)
    
    max_xor = 0
    
    # If K_prime is 0, then we're choosing all elements (if K=N) or none (if K=0, but K>=1)
    # If K=0, not possible by constraints. If K=N, K_prime=0, combinations of size 0 is just empty set with xor 0.
    # If K=N, answer is total_xor.
    
    if K_prime == 0:
        # This happens when K == 0 or K == N.
        # K >= 1, so K == N.
        max_xor = total_xor
    else:
        # Generate all combinations of size K_prime
        # For each combination, compute its XOR sum
        # Then determine the candidate answer based on whether we're choosing or excluding
        
        # Precompute to speed up: we'll iterate through combinations
        # Using itertools.combinations is efficient enough given the constraint
        
        if K <= N - K:
            # We are choosing K elements directly (K_prime == K)
            for combo in combinations(A, K_prime):
                current_xor = 0
                for x in combo:
                    current_xor ^= x
                if current_xor > max_xor:
                    max_xor = current_xor
        else:
            # We are excluding N-K elements (K_prime == N-K)
            # The chosen K elements have XOR = total_xor ^ xor_of_excluded
            for combo in combinations(A, K_prime):
                current_xor = 0
                for x in combo:
                    current_xor ^= x
                candidate = total_xor ^ current_xor
                if candidate > max_xor:
                    max_xor = candidate
    
    print(max_xor)

if __name__ == '__main__':
    solve()
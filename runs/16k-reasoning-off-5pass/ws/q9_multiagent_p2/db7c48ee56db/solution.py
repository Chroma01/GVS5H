import sys
from itertools import combinations

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        k_str = next(iterator)
        N = int(n_str)
        K = int(k_str)
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem guarantees that binomial(N, K) <= 10^6.
    # This allows us to iterate through all possible combinations of K elements.
    # We need to find the maximum XOR sum of K distinct elements.
    
    max_xor = 0
    
    # Optimization: If K is 1, the answer is simply the maximum element.
    if K == 1:
        max_xor = max(A)
    else:
        # Iterate through all combinations of indices of length K
        # itertools.combinations yields tuples of indices, ensuring distinct elements
        indices = range(N)
        
        for combo in combinations(indices, K):
            current_xor = 0
            # Compute XOR sum for the current combination
            for idx in combo:
                current_xor ^= A[idx]
            
            if current_xor > max_xor:
                max_xor = current_xor

    print(max_xor)

if __name__ == '__main__':
    solve()
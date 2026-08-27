import sys
from itertools import combinations

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
    except StopIteration:
        return

    # Calculate total XOR of the array
    total_xor = 0
    for x in A:
        total_xor ^= x

    # The constraint C(N, K) <= 10^6 implies that the number of combinations is small.
    # However, calculating the XOR sum for each combination takes O(K) time.
    # If K is very large (close to N), O(K) per combination can be too slow (e.g., K ~ 2*10^5).
    # We optimize by choosing the smaller set to iterate over:
    # 1. If K <= N-K, we choose K elements to include.
    # 2. If K > N-K, we choose N-K elements to exclude.
    #    The XOR of the chosen K elements = (Total XOR of A) ^ (XOR of excluded N-K elements).
    # This ensures the inner loop runs min(K, N-K) times, which is bounded by a small constant
    # given the constraint C(N, K) <= 10^6.

    if K <= N - K:
        subset_size = K
        max_xor = -1
        
        for indices in combinations(range(N), subset_size):
            current_xor = 0
            for idx in indices:
                current_xor ^= A[idx]
            if current_xor > max_xor:
                max_xor = current_xor
    else:
        subset_size = N - K
        max_xor = -1
        
        for indices in combinations(range(N), subset_size):
            excluded_xor = 0
            for idx in indices:
                excluded_xor ^= A[idx]
            current_xor = total_xor ^ excluded_xor
            if current_xor > max_xor:
                max_xor = current_xor

    print(max_xor)

if __name__ == '__main__':
    solve()
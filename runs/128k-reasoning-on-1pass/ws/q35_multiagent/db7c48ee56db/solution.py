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
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Optimization: If K > N/2, it's more efficient to enumerate subsets of size N-K
    # to exclude. The XOR sum of the chosen K elements equals Total_XOR ^ XOR_sum_of_excluded.
    # This reduces the per-subset computation cost from O(K) to O(min(K, N-K)).
    use_complement = False
    if K > N // 2:
        K = N - K
        use_complement = True
        total_xor = 0
        for x in A:
            total_xor ^= x
            
    max_xor = 0
    
    # Enumerate all combinations of size K
    # The constraint binom(N, K) <= 10^6 guarantees this loop runs at most 10^6 times.
    # Combined with the complement optimization, the total operations are well within limits.
    for combo in combinations(A, K):
        current_xor = 0
        for x in combo:
            current_xor ^= x
        if use_complement:
            current_xor ^= total_xor
        if current_xor > max_xor:
            max_xor = current_xor
            
    print(max_xor)

if __name__ == '__main__':
    solve()
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

    # Since the number of combinations is at most 10^6, we can iterate through all of them.
    # We use itertools.combinations to generate all subsets of size K.
    # For each subset, we compute the XOR sum and track the maximum.
    
    max_xor = 0
    
    # Generate combinations of values directly.
    # The constraint binom(N, K) <= 10^6 ensures this loop runs efficiently.
    # The inner loop runs K times. The total complexity is roughly O(binom(N, K) * K).
    # Given the constraints, the worst-case operations count is well within the time limit.
    
    for combo in combinations(A, K):
        current_xor = 0
        for val in combo:
            current_xor ^= val
        
        if current_xor > max_xor:
            max_xor = current_xor
            
    print(max_xor)

if __name__ == '__main__':
    solve()
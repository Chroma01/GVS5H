import sys
from itertools import combinations
from functools import reduce
from operator import xor

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

    # Edge case: K=1, the answer is simply the maximum element
    if K == 1:
        print(max(A))
        return

    # Edge case: K=N, the answer is the XOR of all elements
    if K == N:
        print(reduce(xor, A))
        return

    # General case: Iterate over all combinations of K elements
    # The constraint binom(N, K) <= 10^6 ensures this loop is efficient enough.
    # We use reduce(xor, ...) which is implemented in C for speed.
    max_xor = 0
    
    # Since A_i are non-negative, max_xor initialized to 0 is safe.
    # However, if all possible XOR sums are 0, the result is 0.
    # We can initialize with the first combination's XOR to be strictly correct 
    # if we wanted to avoid the 0 initialization assumption, but 0 is the identity 
    # for XOR and since A_i >= 0, the max will be >= 0.
    
    for combo in combinations(A, K):
        current_xor = reduce(xor, combo)
        if current_xor > max_xor:
            max_xor = current_xor
            
    print(max_xor)

if __name__ == '__main__':
    solve()
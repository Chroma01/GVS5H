import sys
from itertools import combinations
from functools import reduce
import operator

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
    
    # If K is 0, the XOR sum is 0 (empty set)
    if K == 0:
        print(0)
        return
    
    # If K is 1, the answer is the maximum element
    if K == 1:
        print(max(A))
        return
    
    # If K is N, there's only one combination
    if K == N:
        result = 0
        for x in A:
            result ^= x
        print(result)
        return
    
    # For other cases, iterate through all combinations
    # The constraint binom(N, K) <= 10^6 ensures this is feasible
    max_xor = 0
    
    # Generate all combinations of K elements from A
    for combo in combinations(A, K):
        # Compute XOR sum of the combination
        current_xor = 0
        for x in combo:
            current_xor ^= x
        if current_xor > max_xor:
            max_xor = current_xor
    
    print(max_xor)

if __name__ == '__main__':
    solve()
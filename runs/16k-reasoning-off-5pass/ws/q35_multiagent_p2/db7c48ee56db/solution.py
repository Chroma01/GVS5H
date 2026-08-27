import sys
from itertools import combinations
from functools import reduce
from operator import xor

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
    
    # If K is 1, the answer is simply the maximum element
    if K == 1:
        print(max(A))
        return

    # Since binom(N, K) <= 10^6, we can iterate through all combinations
    max_xor = 0
    
    # Generate all combinations of K elements
    for combo in combinations(A, K):
        # Compute XOR sum of the combination
        current_xor = reduce(xor, combo)
        if current_xor > max_xor:
            max_xor = current_xor
            
    print(max_xor)

if __name__ == '__main__':
    solve()
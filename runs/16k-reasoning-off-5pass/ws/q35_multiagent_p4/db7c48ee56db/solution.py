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
    
    # If K is 0, the XOR sum is 0 (empty set)
    if K == 0:
        print(0)
        return
    
    # If K is 1, the answer is the maximum element
    if K == 1:
        print(max(A))
        return
    
    # Since binom(N, K) <= 10^6, we can iterate through all combinations
    # We want to find the maximum XOR sum of K distinct elements
    
    max_xor = 0
    
    # Generate all combinations of K elements
    # itertools.combinations returns tuples, we compute XOR for each
    for combo in combinations(A, K):
        current_xor = 0
        for x in combo:
            current_xor ^= x
        if current_xor > max_xor:
            max_xor = current_xor
            # Early exit if we hit the theoretical maximum (all bits set up to max possible)
            # But since values can be up to 2^60, we can't easily bound this.
            # However, we can check if max_xor is already very high, but it's not necessary.
    
    print(max_xor)

if __name__ == '__main__':
    solve()
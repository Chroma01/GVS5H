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

    # Calculate the total XOR of all elements in A
    total_xor = 0
    for x in A:
        total_xor ^= x

    # The problem guarantees that binom(N, K) <= 10^6.
    # We can iterate over all combinations. However, calculating the XOR sum for a combination
    # takes O(K) time. If K is large (close to N), this is inefficient.
    # Optimization: Choosing K elements to include is equivalent to choosing N-K elements to exclude.
    # The XOR sum of the included elements is total_xor ^ (XOR sum of excluded elements).
    # We choose to iterate over the smaller set (min(K, N-K)) to minimize the inner loop cost.
    
    if K <= N - K:
        # Iterate over combinations of K elements to include
        max_xor = 0
        for combo in combinations(A, K):
            current_xor = 0
            for x in combo:
                current_xor ^= x
            if current_xor > max_xor:
                max_xor = current_xor
    else:
        # Iterate over combinations of N-K elements to exclude
        exclude_count = N - K
        max_xor = 0
        for combo in combinations(A, exclude_count):
            current_xor = 0
            for x in combo:
                current_xor ^= x
            # XOR of the remaining K elements
            remaining_xor = total_xor ^ current_xor
            if remaining_xor > max_xor:
                max_xor = remaining_xor

    print(max_xor)

if __name__ == '__main__':
    solve()
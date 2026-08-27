import sys
from itertools import combinations

def solve():
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
    
    # If K is 0, the XOR sum is 0 (empty set)
    if K == 0:
        print(0)
        return
    
    # If K is 1, the answer is the maximum element
    if K == 1:
        print(max(A))
        return
    
    # Use the property that choosing K elements is equivalent to leaving out N-K elements.
    # XOR sum of chosen K elements = (XOR sum of all N elements) XOR (XOR sum of excluded N-K elements)
    # Let S = A[0] ^ A[1] ^ ... ^ A[N-1]
    # We want to maximize S ^ T, where T is the XOR sum of some subset of size N-K.
    # Since binom(N, K) == binom(N, N-K), we can iterate over subsets of size min(K, N-K)
    # to minimize the per-combination work.
    
    if K > N // 2:
        # It's more efficient to iterate over subsets of size N-K
        subset_size = N - K
        # Compute total XOR sum
        total_xor = 0
        for x in A:
            total_xor ^= x
        
        max_val = 0
        # Iterate over all combinations of N-K elements to exclude
        for comb in combinations(A, subset_size):
            t = 0
            for x in comb:
                t ^= x
            val = total_xor ^ t
            if val > max_val:
                max_val = val
        print(max_val)
    else:
        # Iterate over subsets of size K directly
        max_val = 0
        for comb in combinations(A, K):
            val = 0
            for x in comb:
                val ^= x
            if val > max_val:
                max_val = val
        print(max_val)

if __name__ == '__main__':
    solve()
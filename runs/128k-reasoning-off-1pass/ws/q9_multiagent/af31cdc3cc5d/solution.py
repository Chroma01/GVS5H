import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Sort the array to apply the greedy strategy
    A.sort()
    
    # Calculate k, the number of pairs we can form
    # If N is even, we use all elements. k = N/2.
    # If N is odd, we leave out the middle element. k = (N-1)/2.
    # In integer division, k = N // 2 works for both cases.
    k = N // 2
    
    # The maximum score is the sum of the largest k elements minus the sum of the smallest k elements.
    # The middle element (if N is odd) is effectively ignored (coefficient 0).
    # Indices for largest k: from N-k to N-1
    # Indices for smallest k: from 0 to k-1
    
    sum_large = sum(A[N-k:])
    sum_small = sum(A[:k])
    
    result = sum_large - sum_small
    print(result)

if __name__ == '__main__':
    solve()
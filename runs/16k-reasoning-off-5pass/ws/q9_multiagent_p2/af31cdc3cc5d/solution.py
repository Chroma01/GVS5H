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

    # Sort the array
    A.sort()

    # Calculate the maximum score
    # The strategy is to pair the smallest with the largest, 
    # second smallest with second largest, and so on.
    # We sum (A[N-1-i] - A[i]) for i from 0 to N//2 - 1.
    
    max_score = 0
    # We only need to iterate up to N // 2
    # If N is even, we pair all elements.
    # If N is odd, the middle element is left out (contributes 0).
    # The loop range(N // 2) handles both cases correctly.
    # For N=4 (indices 0,1,2,3): range(2) -> i=0, 1. Pairs (3,0) and (2,1).
    # For N=5 (indices 0,1,2,3,4): range(2) -> i=0, 1. Pairs (4,0) and (3,1). Index 2 is skipped.
    
    for i in range(N // 2):
        max_score += (A[N - 1 - i] - A[i])

    print(max_score)

if __name__ == '__main__':
    solve()
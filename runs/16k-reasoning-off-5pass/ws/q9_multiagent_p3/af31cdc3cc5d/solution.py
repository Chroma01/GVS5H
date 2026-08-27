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
    # The problem allows pairing any odd-indexed element with any even-indexed element
    # (1-based indices). This reduces to a maximum weight matching problem which is solved
    # by sorting the entire array and pairing the smallest with the largest, etc.
    A.sort()
    
    total_score = 0
    
    # We pair the smallest with the largest, 2nd smallest with 2nd largest, etc.
    # If N is even, we pair all elements.
    # If N is odd, the middle element is left out (it contributes 0 to the optimal sum).
    # The loop runs for i from 0 to (N // 2) - 1.
    # For each i, we take A[i] and A[N - 1 - i].
    
    limit = N // 2
    for i in range(limit):
        total_score += (A[N - 1 - i] - A[i])
        
    print(total_score)

if __name__ == '__main__':
    solve()
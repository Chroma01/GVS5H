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

    # Sort the array to easily access smallest and largest elements
    A.sort()
    
    # Calculate the maximum score
    # We pair the largest available with the smallest available
    # The number of pairs is floor(N / 2)
    total_score = 0
    num_pairs = N // 2
    
    for i in range(num_pairs):
        # Pair A[i] (smallest) with A[N - 1 - i] (largest)
        total_score += (A[N - 1 - i] - A[i])
        
    print(total_score)

if __name__ == '__main__':
    solve()
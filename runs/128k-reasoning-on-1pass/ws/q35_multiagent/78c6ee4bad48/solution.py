import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    X = list(map(int, input_data[1:]))
    
    # Compute gaps between adjacent pieces
    gaps = [X[i+1] - X[i] for i in range(N-1)]
    
    # Separate gaps into those at odd positions (1-based) and even positions (1-based)
    # In 0-based indexing, gaps[0], gaps[2], ... correspond to d1, d3, ...
    # gaps[1], gaps[3], ... correspond to d2, d4, ...
    odd_gaps = gaps[0::2]
    even_gaps = gaps[1::2]
    
    # Sort both lists in ascending order to assign smallest gaps to largest coefficients
    odd_gaps.sort()
    even_gaps.sort()
    
    # The sum of coordinates can be expressed as:
    # Sum = N * X[0] + sum((N - 1 - j) * d[j] for j in range(N-1))
    # Coefficients (N - 1 - j) are decreasing with j.
    total_sum = N * X[0]
    
    # Assign sorted odd-indexed gaps to positions j = 0, 2, 4, ...
    for i, d in enumerate(odd_gaps):
        total_sum += (N - 1 - 2 * i) * d
        
    # Assign sorted even-indexed gaps to positions j = 1, 3, 5, ...
    for i, d in enumerate(even_gaps):
        total_sum += (N - 2 - 2 * i) * d
        
    print(total_sum)

if __name__ == '__main__':
    solve()
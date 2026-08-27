import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        x = []
        for _ in range(n):
            x.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem asks to minimize the sum of coordinates after performing operations.
    # The operation on indices i, i+1, i+2, i+3 (sorted) transforms the middle two
    # elements A[i+1], A[i+2] into A[i] + A[i+3] - A[i+1], A[i] + A[i+3] - A[i+2].
    # This operation reduces the sum if A[i+1] + A[i+2] > A[i] + A[i+3].
    # It turns out that the minimum sum is achieved when the sequence of differences
    # d[i] = A[i+1] - A[i] satisfies d[i] <= d[i+2] for all valid i.
    # This implies that the odd-indexed differences (d[0], d[2], d[4]...) must be non-decreasing,
    # and the even-indexed differences (d[1], d[3], d[5]...) must be non-decreasing.
    # The first element A[0] is invariant under the operations.
    # To minimize the sum, we sort the odd-indexed differences and even-indexed differences
    # in ascending order and reconstruct the array.
    
    # Sort x just in case (though problem says X_1 < X_2 < ... < X_N)
    x.sort()
    
    if n < 4:
        # If N < 4, no operations can be performed.
        print(sum(x))
        return

    # Compute initial differences
    d = [x[i+1] - x[i] for i in range(n-1)]
    
    # Separate differences into odd and even indices
    # Note: In 0-based indexing, indices 0, 2, 4... are "even" positions in the difference array
    # and indices 1, 3, 5... are "odd" positions.
    # The condition d[i] <= d[i+2] means the subsequence at even indices must be sorted,
    # and the subsequence at odd indices must be sorted.
    
    even_pos_diffs = [] # Indices 0, 2, 4...
    odd_pos_diffs = []  # Indices 1, 3, 5...
    
    for i in range(n-1):
        if i % 2 == 0:
            even_pos_diffs.append(d[i])
        else:
            odd_pos_diffs.append(d[i])
            
    # Sort both lists in ascending order
    even_pos_diffs.sort()
    odd_pos_diffs.sort()
    
    # Reconstruct the new difference sequence
    new_d = [0] * (n-1)
    for i in range(0, n-1, 2):
        new_d[i] = even_pos_diffs[i // 2]
    for i in range(1, n-1, 2):
        new_d[i] = odd_pos_diffs[i // 2]
        
    # Reconstruct the array and compute the sum
    # x[0] remains the same (invariant)
    current_x = x[0]
    total_sum = current_x
    
    for i in range(n-1):
        current_x += new_d[i]
        total_sum += current_x
        
    print(total_sum)

if __name__ == '__main__':
    solve()
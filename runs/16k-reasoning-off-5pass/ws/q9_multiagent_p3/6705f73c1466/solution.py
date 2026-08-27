import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Extract indices of '1's (0-indexed)
    pos = [i for i, char in enumerate(s) if char == '1']
    k = len(pos)

    # If there are no 1s, cost is 0 (though problem guarantees at least one 1)
    if k == 0:
        print(0)
        return

    # Compute array A where A[i] = pos[i] - i
    # This transforms the problem to finding an integer l such that
    # sum(|A[i] - l|) is minimized, subject to 0 <= l <= n - k.
    a = [pos[i] - i for i in range(k)]

    # Find the median of A
    # Since k can be up to 5*10^5, sorting is O(N log N) which is acceptable.
    a.sort()
    median = a[k // 2]

    # The optimal l is the median, but it must be within [0, n - k]
    # because the contiguous block of 1s must fit within the string.
    min_l = 0
    max_l = n - k
    
    if median < min_l:
        l = min_l
    elif median > max_l:
        l = max_l
    else:
        l = median

    # Calculate the total cost
    # Cost = sum(|pos[i] - (l + i)|) = sum(|(pos[i] - i) - l|) = sum(|A[i] - l|)
    total_ops = 0
    for val in a:
        total_ops += abs(val - l)

    print(total_ops)

if __name__ == '__main__':
    solve()
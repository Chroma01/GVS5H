import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # We want to find the maximum number of pairs (top, bottom) such that top <= bottom / 2.
    # Since A is sorted, we use a greedy two-pointer approach.
    # i points to potential top mochi (starting from the smallest)
    # j points to potential bottom mochi (starting from the middle to ensure disjointness)
    
    i = 0
    j = N // 2
    count = 0
    
    while i < N // 2 and j < N:
        if 2 * A[i] <= A[j]:
            # Can form a pair
            count += 1
            i += 1
            j += 1
        else:
            # A[j] is too small for A[i], try a larger bottom
            j += 1
    
    print(count)

if __name__ == '__main__':
    solve()
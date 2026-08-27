import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # We want to maximize pairs (top, bottom) such that top <= bottom // 2
    # Since A is sorted, we use two pointers.
    # i points to potential top, j points to potential bottom.
    # We start j from N//2 because we can have at most N//2 pairs.
    
    i = 0
    j = N // 2
    count = 0
    
    while i < N // 2 and j < N:
        if A[i] <= A[j] // 2:
            # Form a pair
            count += 1
            i += 1
            j += 1
        else:
            # A[i] is too big for A[j], try a larger bottom
            j += 1
            
    print(count)

if __name__ == '__main__':
    solve()
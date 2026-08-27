import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # Two-pointer approach
    # i points to potential top mochi (smaller ones)
    # j points to potential bottom mochi (larger ones)
    # We start j at N//2 because we can have at most N//2 pairs,
    # and the bottoms must come from the upper half to be large enough.
    
    i = 0
    j = N // 2
    count = 0
    
    while i < N // 2 and j < N:
        if A[i] * 2 <= A[j]:
            # Can form a pair
            count += 1
            i += 1
            j += 1
        else:
            # Current bottom is too small for current top, try next larger bottom
            j += 1
            
    print(count)

if __name__ == '__main__':
    solve()
import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    # Two pointer approach
    # i points to the current top mochi candidate
    # j points to the current bottom mochi candidate
    i = 0
    j = 0
    count = 0
    
    while j < n:
        # We need i < j to ensure distinct mochi
        # And A[i] * 2 <= A[j] for the condition
        if i < j and a[i] * 2 <= a[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
            
    print(count)

if __name__ == '__main__':
    solve()
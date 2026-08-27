import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # A is already sorted in ascending order
    
    # We want to find maximum K pairs (top, bottom) such that top <= bottom / 2
    # Using two pointers: left for top candidates, right for bottom candidates
    # Top candidates are in the first half, bottom candidates in the second half
    
    left = 0
    right = N // 2
    count = 0
    
    while left < N // 2 and right < N:
        # Check if A[left] can be placed on top of A[right]
        # Condition: A[left] <= A[right] / 2, which is equivalent to 2 * A[left] <= A[right]
        if 2 * A[left] <= A[right]:
            count += 1
            left += 1
            right += 1
        else:
            # Current bottom is too small, try a larger bottom
            right += 1
    
    print(count)

if __name__ == '__main__':
    solve()
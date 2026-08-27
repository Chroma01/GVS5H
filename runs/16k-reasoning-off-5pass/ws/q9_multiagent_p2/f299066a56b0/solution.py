import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # The array 'a' is already sorted as per constraints.
    # We use a two-pointer approach to maximize pairs.
    # left pointer points to the candidate for the top mochi (smaller size)
    # right pointer points to the candidate for the bottom mochi (larger size)
    
    left = 0
    right = 1
    k = 0
    
    # We iterate while right is within bounds.
    # Note: left will never exceed right in a valid pairing logic here because
    # if left == right, the condition 2*a[left] <= a[right] becomes 2*a <= a => a <= 0,
    # which is impossible since A_i >= 1. So left < right is implicitly maintained 
    # when a pair is formed.
    while right < n:
        # Check if the mochi at 'right' can be placed under the mochi at 'left'
        # Condition: top_size <= bottom_size / 2  =>  2 * top_size <= bottom_size
        if 2 * a[left] <= a[right]:
            # Valid pair found
            k += 1
            left += 1
            right += 1
        else:
            # The current 'right' is too small to support 'left'.
            # Since the array is sorted, 'right' is also too small for any subsequent 'left' (which will be >= current 'left').
            # Therefore, 'right' cannot be used as a bottom piece for any remaining top piece.
            # We discard 'right' and move to the next potential bottom piece.
            right += 1
            
    print(k)

if __name__ == '__main__':
    solve()
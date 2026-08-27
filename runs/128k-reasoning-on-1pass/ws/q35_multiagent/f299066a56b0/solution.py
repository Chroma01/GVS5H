import sys

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # The first token is N
    n = int(input_data[0])
    
    # The rest of the tokens are the elements of A
    # A is guaranteed to be sorted in ascending order.
    a = [int(x) for x in input_data[1:]]
    
    # We want to find the maximum number of pairs (top, bottom) such that top <= bottom / 2.
    # Since the array is sorted, we can use a greedy two-pointer approach.
    # The maximum number of pairs is at most N // 2.
    # Therefore, we can restrict the "top" mochi to the first half of the array
    # and the "bottom" mochi to the second half.
    
    left = 0
    right = n // 2
    count = 0
    
    # Iterate while both pointers are within valid ranges.
    # 'left' points to a candidate for the top mochi.
    # 'right' points to a candidate for the bottom mochi.
    while left < n // 2 and right < n:
        # Check the condition: a[left] <= a[right] / 2
        # To avoid floating point issues, we use multiplication: 2 * a[left] <= a[right]
        if 2 * a[left] <= a[right]:
            # Valid pair found
            count += 1
            left += 1
            right += 1
        else:
            # If the current bottom mochi is too small, move the right pointer
            # to try a larger bottom mochi.
            right += 1
            
    print(count)

if __name__ == '__main__':
    solve()
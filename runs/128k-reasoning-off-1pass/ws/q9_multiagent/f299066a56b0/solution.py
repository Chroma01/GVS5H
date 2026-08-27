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

    # The array 'a' is already sorted in ascending order as per constraints.
    # We use a greedy two-pointer approach.
    # left pointer points to the candidate for the top mochi (smaller value).
    # right pointer points to the candidate for the bottom mochi (larger value).
    
    left = 0
    right = 1
    k = 0
    
    # We iterate while both pointers are within bounds.
    # We need at least two elements to form a pair.
    while left < n and right < n:
        # Condition: top mochi size <= bottom mochi size / 2
        # Equivalent to: 2 * top <= bottom to avoid floating point issues
        if 2 * a[left] <= a[right]:
            # Form a pair
            k += 1
            left += 1
            right += 1
        else:
            # The current 'right' is too small to support 'left'.
            # We need a larger 'right' mochi.
            right += 1
            
    print(k)

if __name__ == '__main__':
    solve()
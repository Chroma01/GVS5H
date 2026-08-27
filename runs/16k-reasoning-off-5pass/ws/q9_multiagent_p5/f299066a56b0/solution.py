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

    # The array 'a' is already sorted as per the problem statement.
    # We use a greedy two-pointer approach.
    # 'left' points to the candidate for the top mochi (smaller value).
    # 'right' points to the candidate for the bottom mochi (larger value).
    
    left = 0
    right = 0
    k = 0
    
    # We iterate while we have potential bottom candidates
    while right < n:
        # We cannot pair an element with itself, so if pointers are equal,
        # we must advance the right pointer to find a distinct base.
        if left == right:
            right += 1
            continue
        
        # Check the condition: top <= bottom / 2  <==>  top * 2 <= bottom
        # Using multiplication avoids floating point issues.
        if a[left] * 2 <= a[right]:
            # Valid pair found
            k += 1
            left += 1
            right += 1
        else:
            # The current 'right' is too small to support 'left'.
            # Since the array is sorted, 'right' cannot support any future 'left'
            # (which are >= current 'left'). Thus, 'right' is useless as a base.
            right += 1
            
    print(k)

if __name__ == '__main__':
    solve()
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

    # The array 'a' is already sorted as per problem constraints.
    # We use a greedy two-pointer approach.
    # 'left' points to the potential top mochi (smaller value).
    # 'right' points to the potential bottom mochi (larger value).
    # We want to find the smallest 'right' such that a[right] >= 2 * a[left].
    
    left = 0
    right = 1
    k = 0
    
    while right < n:
        # Check if the current 'right' mochi can support the 'left' mochi
        if a[right] >= 2 * a[left]:
            # Valid pair found
            k += 1
            left += 1
            right += 1
        else:
            # 'right' is too small to support 'left'.
            # Since the array is sorted, 'right' cannot support any subsequent 'left' (which are larger).
            # So we discard 'right' and look for a larger bottom mochi.
            right += 1
            
    print(k)

if __name__ == '__main__':
    solve()
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

    # Two-pointer approach
    # i points to the potential top mochi (smaller element)
    # j points to the potential bottom mochi (larger element)
    i = 0
    j = 1
    k = 0
    
    # We need to form pairs (a[i], a[j]) such that a[i] <= a[j] / 2
    # Since the array is sorted, we iterate j to find a valid base for a[i]
    while j < n:
        # Check condition: 2 * a[i] <= a[j] to avoid floating point issues
        if 2 * a[i] <= a[j]:
            # Valid pair found
            k += 1
            i += 1
            j += 1
        else:
            # Current base a[j] is too small for a[i]
            # We need a larger base, so move j forward
            j += 1
            
    print(k)

if __name__ == '__main__':
    solve()
import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # We want to find the maximum number of pairs (top, bottom) such that 2 * top <= bottom.
    # Greedy strategy:
    # - Use the smallest available mochi as potential 'top' (smaller one in the pair).
    # - Use the smallest available mochi that is large enough as 'bottom' (larger one in the pair).
    # - To maximize pairs, we should try to pair the smallest tops with the smallest valid bottoms.
    # - The maximum possible pairs is N // 2.
    # - We can use two pointers:
    #   i: pointer for top candidates, starting from 0.
    #   j: pointer for bottom candidates, starting from N // 2.
    #   Why N // 2 for j? Because in the best case, we pair the first K smallest with the last K largest.
    #   The bottoms must come from the upper half of the array to have a chance of being >= 2 * top.
    
    i = 0
    j = N // 2
    count = 0
    
    while i < N // 2 and j < N:
        if 2 * A[i] <= A[j]:
            # We can form a pair: A[i] on top of A[j]
            count += 1
            i += 1
            j += 1
        else:
            # A[j] is too small for A[i]. Since A is sorted, A[j] is also too small for any A[k] with k > i.
            # So A[j] cannot be used as a bottom for any remaining top candidate.
            # Try a larger bottom.
            j += 1
            
    print(count)

if __name__ == '__main__':
    solve()
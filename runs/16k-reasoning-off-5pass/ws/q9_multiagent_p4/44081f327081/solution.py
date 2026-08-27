import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Determine the maximum value in A to size our arrays
    # Constraints say A_i <= 10^6, but using max(A) is safer and adaptive
    if not A:
        return
        
    max_val = max(A)
    
    # Frequency array
    cnt = [0] * (max_val + 1)
    for x in A:
        cnt[x] += 1
    
    # total_multiples[g] will store the count of numbers in A divisible by g
    # We compute this using a sieve-like approach
    total_multiples = [0] * (max_val + 1)
    
    # Iterate g from 1 to max_val
    # Complexity: O(V log V) where V = max_val
    for g in range(1, max_val + 1):
        count = 0
        # Sum frequencies of multiples of g
        # range(g, max_val + 1, g) generates g, 2g, 3g, ...
        for multiple in range(g, max_val + 1, g):
            count += cnt[multiple]
        total_multiples[g] = count
    
    # ans[x] will store the maximum valid GCD for a number x
    # Initialize with 0
    ans = [0] * (max_val + 1)
    
    # Iterate g from 1 to max_val
    # If g is a valid GCD (count >= K), update all its multiples.
    # Since we iterate in increasing order, the last update for any multiple x
    # will be from the largest valid divisor of x.
    # Complexity: O(V log V) due to slice assignments
    for g in range(1, max_val + 1):
        if total_multiples[g] >= K:
            # Slice assignment is efficient in Python (implemented in C)
            # We set ans[m] = g for all m = g, 2g, 3g, ...
            # The length of the slice is (max_val - g) // g + 1
            length = (max_val - g) // g + 1
            # Create a list of g's and assign to the slice
            ans[g::g] = [g] * length
            
    # Prepare output
    results = []
    for x in A:
        results.append(str(ans[x]))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
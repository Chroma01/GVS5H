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
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Determine the maximum value in A to set the array size dynamically
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x
            
    # Frequency array for values present in A
    cnt = [0] * (max_val + 1)
    for x in A:
        cnt[x] += 1

    # Array to store the maximum GCD found for each value v
    # Initialize with 0. Since K >= 1, a valid GCD always exists (at least 1).
    # We will fill this array by iterating g from max_val down to 1.
    max_g = [0] * (max_val + 1)

    # Iterate g from max_val down to 1
    # If count of multiples of g is >= K, then g is a candidate for all multiples of g present in A.
    # Since we iterate downwards, the first time we set max_g[j], it is the largest possible.
    for g in range(max_val, 0, -1):
        # Count multiples of g in A
        count = 0
        # Iterate through multiples: g, 2g, 3g, ...
        for multiple in range(g, max_val + 1, g):
            count += cnt[multiple]
        
        if count >= K:
            # Update max_g for all multiples of g that are present in A
            # We only update if max_g is 0 to avoid redundant checks and assignments
            for multiple in range(g, max_val + 1, g):
                if cnt[multiple] > 0 and max_g[multiple] == 0:
                    max_g[multiple] = g

    # Prepare output
    # For each A[i], the answer is max_g[A[i]]
    results = [str(max_g[x]) for x in A]
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
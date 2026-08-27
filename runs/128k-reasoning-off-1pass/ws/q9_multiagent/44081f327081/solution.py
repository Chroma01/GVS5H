import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input at once for efficiency
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

    # Determine the maximum value in A to optimize array sizes
    # Constraints say A_i <= 10^6, but we can use the actual max for slight optimization
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x
            
    # Frequency array
    freq = [0] * (max_val + 1)
    for x in A:
        freq[x] += 1

    # cnt[g] will store the number of elements in A that are multiples of g
    cnt = [0] * (max_val + 1)
    
    # Sieve-like process to count multiples
    # Iterate g from 1 to max_val
    # Complexity: O(max_val * log(max_val))
    for g in range(1, max_val + 1):
        count = 0
        for multiple in range(g, max_val + 1, g):
            count += freq[multiple]
        cnt[g] = count

    # ans[x] will store the maximum GCD for a subset of size K containing x
    # Initialize with 0
    ans = [0] * (max_val + 1)

    # Iterate g downwards from max_val to 1
    # If cnt[g] >= K, then g is a candidate GCD for all multiples of g.
    # Since we go downwards, the first time we set ans[x], it is the maximum possible.
    # Complexity: O(max_val * log(max_val))
    for g in range(max_val, 0, -1):
        if cnt[g] >= K:
            # Mark all multiples of g
            for multiple in range(g, max_val + 1, g):
                if ans[multiple] == 0:
                    ans[multiple] = g

    # Output results
    results = []
    for x in A:
        results.append(str(ans[x]))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
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

    if N == 0:
        return

    # Determine the maximum value in A to size our arrays
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x

    # Frequency array to count occurrences of each number
    cnt = [0] * (max_val + 1)
    # Position list: pos[v] contains a list of indices i where A[i] == v
    pos = [[] for _ in range(max_val + 1)]

    for i in range(N):
        val = A[i]
        cnt[val] += 1
        pos[val].append(i)

    # total_multiples[g] will store the number of elements in A that are multiples of g
    total_multiples = [0] * (max_val + 1)

    # Compute total_multiples using a sieve-like approach
    # Iterate g from 1 to max_val
    for g in range(1, max_val + 1):
        count = 0
        for multiple in range(g, max_val + 1, g):
            count += cnt[multiple]
        total_multiples[g] = count

    # Initialize answers with 1 (minimum possible GCD)
    ans = [1] * N

    # We iterate g from max_val down to 1.
    # If total_multiples[g] >= K, then g is a valid GCD for any subset of size K.
    # Since we want the maximum GCD for each A[i], and we are iterating downwards,
    # the first time we encounter a valid g for a specific A[i], that is the maximum.
    # We only update indices i where A[i] is a multiple of g.
    
    for g in range(max_val, 0, -1):
        if total_multiples[g] < K:
            continue
        
        # Iterate through all multiples of g
        for v in range(g, max_val + 1, g):
            if cnt[v] == 0:
                continue
            
            # For each index i where A[i] == v, update answer if not already set
            for idx in pos[v]:
                if ans[idx] == 1:
                    ans[idx] = g
                # If ans[idx] is already > 1, it means we found a larger GCD earlier (since we iterate g downwards)
                # So we don't need to update.
    
    # Print results
    for x in ans:
        print(x)

if __name__ == '__main__':
    solve()
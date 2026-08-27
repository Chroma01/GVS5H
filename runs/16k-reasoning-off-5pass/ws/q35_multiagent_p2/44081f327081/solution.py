import sys

def solve():
    # Increase recursion depth just in case, though we don't use recursion
    sys.setrecursionlimit(2000)
    
    # Read all input from stdin
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

    # Find max value in A to determine the size of our arrays
    if not A:
        return
        
    max_val = 0
    for x in A:
        if x > max_val:
            max_val = x
            
    # Step 1: Frequency count
    freq = [0] * (max_val + 1)
    for x in A:
        freq[x] += 1
        
    # Step 2: Count multiples for each g
    # cnt[g] = number of elements in A divisible by g
    cnt = [0] * (max_val + 1)
    
    # Sieve-like approach: for each g, sum freq[j] for j = g, 2g, 3g, ...
    for g in range(1, max_val + 1):
        total = 0
        for j in range(g, max_val + 1, g):
            total += freq[j]
        cnt[g] = total
        
    # Step 3: Precompute the best valid GCD for each number up to max_val
    # best[g] will store the largest divisor d of g such that cnt[d] >= K
    # We initialize with 0 (meaning no valid GCD found yet, though 1 is always valid if K <= N)
    best = [0] * (max_val + 1)
    
    # Iterate g from max_val down to 1
    # If cnt[g] >= K, then g is a valid GCD candidate.
    # For all multiples j of g, if best[j] is not yet set, set it to g.
    # Since we iterate g from large to small, the first time we set best[j],
    # it is via the largest valid divisor of j.
    for g in range(max_val, 0, -1):
        if cnt[g] >= K:
            # Mark all multiples of g
            for j in range(g, max_val + 1, g):
                if best[j] == 0:
                    best[j] = g
                    
    # Step 4: Output the answer for each A_i
    results = []
    for x in A:
        results.append(str(best[x]))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
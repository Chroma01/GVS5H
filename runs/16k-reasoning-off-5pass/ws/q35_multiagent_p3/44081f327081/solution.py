import sys

def main():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    K = int(next(iterator))
    
    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
    
    # Find maximum value in A to determine the range
    MAX_VAL = 0
    for x in A:
        if x > MAX_VAL:
            MAX_VAL = x
    
    # Step 1: Compute frequency of each number in A
    freq = [0] * (MAX_VAL + 1)
    for x in A:
        freq[x] += 1
    
    # Step 2: Compute count[g] = number of elements in A divisible by g
    # Using sieve-like approach: for each g, sum freq[j] for all multiples j of g
    count = [0] * (MAX_VAL + 1)
    for g in range(1, MAX_VAL + 1):
        c = 0
        for j in range(g, MAX_VAL + 1, g):
            c += freq[j]
        count[g] = c
    
    # Step 3: For each A_i, find all divisors and pick the maximum d such that count[d] >= K
    # To efficiently find divisors, we can precompute divisors for all numbers up to MAX_VAL
    # But that might use too much memory. Instead, for each A_i, find divisors on the fly.
    # However, with N up to 1.2e6 and MAX_VAL up to 1e6, doing sqrt(A_i) for each might be slow.
    # Better: Precompute the largest valid divisor for each number up to MAX_VAL.
    
    # Let's compute ans[x] = largest divisor d of x such that count[d] >= K
    # We can do this by iterating g from MAX_VAL down to 1, and for each g with count[g] >= K,
    # set ans[x] = g for all multiples x of g that haven't been set yet.
    
    ans = [0] * (MAX_VAL + 1)
    # Initialize ans with 0 (or 1, since 1 always divides everything and count[1] = N >= K)
    # Actually, we want the maximum, so we iterate from large g to small g.
    
    # For each g from MAX_VAL down to 1, if count[g] >= K, then for all multiples x of g,
    # if ans[x] is not set, set ans[x] = g.
    for g in range(MAX_VAL, 0, -1):
        if count[g] >= K:
            for x in range(g, MAX_VAL + 1, g):
                if ans[x] == 0:
                    ans[x] = g
    
    # Now, for each A_i, the answer is ans[A_i]
    output = []
    for x in A:
        output.append(str(ans[x]))
    
    sys.stdout.write('\n'.join(output) + '\n')

if __name__ == '__main__':
    main()
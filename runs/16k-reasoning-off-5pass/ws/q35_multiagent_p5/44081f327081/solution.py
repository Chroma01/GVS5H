import sys

def main():
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
    except StopIteration:
        return
    
    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
    
    MAX_VAL = 1000000
    
    # Step 1: Compute frequency of each number in A
    freq = [0] * (MAX_VAL + 1)
    for x in A:
        freq[x] += 1
    
    # Step 2: For each g from 1 to MAX_VAL, count how many numbers in A are divisible by g
    # count[g] = sum(freq[m] for m in multiples of g)
    count = [0] * (MAX_VAL + 1)
    
    for g in range(1, MAX_VAL + 1):
        c = 0
        for m in range(g, MAX_VAL + 1, g):
            c += freq[m]
        count[g] = c
    
    # Step 3: For each value v from 1 to MAX_VAL, find the largest feasible divisor
    # A divisor g of v is feasible if count[g] >= K
    # best[v] = max feasible divisor of v
    
    best = [1] * (MAX_VAL + 1)
    
    # We iterate g from MAX_VAL down to 1.
    # If g is feasible, then for all multiples m of g, g is a feasible divisor of m.
    # Since we go from large to small, the first time we visit a multiple m,
    # we set best[m] to the largest feasible divisor found so far.
    # But wait, a number m might have multiple feasible divisors. We want the largest.
    # If we iterate g from MAX_VAL down to 1, and for each feasible g, we update best[m] = g
    # for all multiples m, then the first update for m will be the largest feasible divisor.
    # However, we need to be careful: we should only update if g > best[m].
    # Since we go from large to small, the first feasible g that divides m will be the largest.
    # So we can initialize best[v] = 0 or -1, and set it the first time we encounter a feasible divisor.
    
    # Let's re-initialize best to 0
    best = [0] * (MAX_VAL + 1)
    
    for g in range(MAX_VAL, 0, -1):
        if count[g] >= K:
            # g is feasible. Update all multiples of g.
            for m in range(g, MAX_VAL + 1, g):
                if best[m] == 0:
                    best[m] = g
    
    # For any v where best[v] is still 0, it means no feasible divisor was found.
    # But 1 is always feasible if K <= N (which is given), so best[v] should always be set.
    # Just in case, set best[v] = 1 for any remaining 0s.
    for v in range(1, MAX_VAL + 1):
        if best[v] == 0:
            best[v] = 1
    
    # Step 4: Output the answer for each A_i
    results = []
    for x in A:
        results.append(str(best[x]))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    main()
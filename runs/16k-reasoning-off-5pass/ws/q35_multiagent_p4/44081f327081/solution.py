import sys

def main():
    # Increase recursion depth just in case, though not needed here
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

    MAX_A = 1000000
    
    # Step 1: Frequency count of each number in A
    freq = [0] * (MAX_A + 1)
    for x in A:
        freq[x] += 1
        
    # Step 2: Count how many numbers in A are divisible by g for each g
    # count[g] = sum(freq[j*g] for j >= 1)
    count = [0] * (MAX_A + 1)
    
    for g in range(1, MAX_A + 1):
        c = 0
        for multiple in range(g, MAX_A + 1, g):
            c += freq[multiple]
        count[g] = c
        
    # Step 3: For each value v in [1, MAX_A], find the largest divisor g of v
    # such that count[g] >= K.
    # We can do this by iterating g from MAX_A down to 1.
    # If count[g] >= K, then for all multiples m of g, g is a candidate answer for m.
    # Since we iterate g from large to small, the first time we set ans[m], it is the largest valid divisor.
    
    ans = [0] * (MAX_A + 1)
    
    # We only need to process g where count[g] >= K
    # Iterate downwards
    for g in range(MAX_A, 0, -1):
        if count[g] >= K:
            # Mark all multiples of g that haven't been marked yet
            for m in range(g, MAX_A + 1, g):
                if ans[m] == 0:
                    ans[m] = g
                    
    # Step 4: Output the answer for each A_i
    results = []
    for x in A:
        results.append(str(ans[x]))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    main()
import sys

def solve():
    # Fast I/O
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

    if not A:
        return

    max_val = max(A)
    
    # Frequency array for values in A
    cnt = [0] * (max_val + 1)
    for x in A:
        cnt[x] += 1
        
    # res[x] will store the maximum valid GCD for value x
    res = [0] * (max_val + 1)
    
    # Iterate through all possible divisors g
    for g in range(1, max_val + 1):
        # Count how many elements in A are multiples of g
        # Using slice sum is highly optimized in Python
        if sum(cnt[g::g]) >= K:
            # Mark all multiples of g in res with g.
            # Processing in increasing order ensures larger valid g overwrites smaller ones.
            res[g::g] = [g] * (max_val // g)
            
    # Output results for each element in the original sequence
    sys.stdout.write('\n'.join(map(str, (res[x] for x in A))) + '\n')

if __name__ == '__main__':
    solve()
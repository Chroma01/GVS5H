import sys
import math

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        Q = int(next(iterator))
    except StopIteration:
        return

    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
        
    # Maximum possible value for sqrt(A) is 10^6 since A <= 10^12
    MAX_S = 1000000
    
    # cnt[i] will store the number of distinct prime factors of i
    cnt = [0] * (MAX_S + 1)
    
    # Sieve-like process to count distinct prime factors for all numbers up to MAX_S
    for i in range(2, MAX_S + 1):
        if cnt[i] == 0:  # i is prime
            for j in range(i, MAX_S + 1, i):
                cnt[j] += 1
                
    # last_valid[i] stores the largest integer M <= i such that M has exactly 2 distinct prime factors
    last_valid = [0] * (MAX_S + 1)
    current = 0
    for i in range(1, MAX_S + 1):
        if cnt[i] == 2:
            current = i
        last_valid[i] = current
        
    results = []
    for A in queries:
        # We need the largest M such that M^2 <= A, which means M <= floor(sqrt(A))
        S = math.isqrt(A)
        M = last_valid[S]
        results.append(str(M * M))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
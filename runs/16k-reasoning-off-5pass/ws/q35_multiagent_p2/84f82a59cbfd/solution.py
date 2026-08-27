import sys
from bisect import bisect_right

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
        
    # Max A is 10^12, so max k = sqrt(A) is 10^6
    MAX_K = 1000000
    
    # Sieve to count distinct prime factors for each number up to MAX_K
    # cnt[i] will store the number of distinct prime factors of i
    cnt = [0] * (MAX_K + 1)
    
    # For each prime p, increment count for all its multiples
    for i in range(2, MAX_K + 1):
        if cnt[i] == 0:  # i is prime
            for j in range(i, MAX_K + 1, i):
                cnt[j] += 1
                
    # Collect all k such that k has exactly 2 distinct prime factors
    # Then the 400 number is k^2
    valid_squares = []
    for k in range(2, MAX_K + 1):
        if cnt[k] == 2:
            valid_squares.append(k * k)
            
    # Sort the valid squares (they should already be mostly sorted, but let's ensure)
    valid_squares.sort()
    
    # Process each query
    results = []
    for A in queries:
        # Find the largest 400 number <= A
        # bisect_right returns the insertion point after all elements <= A
        # So the element at index pos-1 is the largest <= A
        pos = bisect_right(valid_squares, A)
        if pos > 0:
            results.append(str(valid_squares[pos - 1]))
        else:
            # This should not happen per constraints (A >= 36, and 36 is a 400 number)
            results.append("0")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
import sys
from bisect import bisect_right

def solve():
    # Maximum value for A is 10^12, so the base number x = sqrt(N) is at most 10^6.
    LIMIT = 1000000
    
    # Sieve to count distinct prime factors for each number up to LIMIT
    # omega[i] will store the number of distinct prime factors of i
    omega = [0] * (LIMIT + 1)
    
    # We can iterate through each prime and mark its multiples
    # This is effectively a sieve that counts distinct prime factors
    for i in range(2, LIMIT + 1):
        if omega[i] == 0:
            # i is prime
            for j in range(i, LIMIT + 1, i):
                omega[j] += 1
    
    # Collect all valid 400 numbers
    # A number N is a 400 number if N = x^2 and x has exactly 2 distinct prime factors.
    valid_numbers = []
    for x in range(2, LIMIT + 1):
        if omega[x] == 2:
            valid_numbers.append(x * x)
    
    # The list is naturally sorted because we iterate x in increasing order
    # But let's ensure it's sorted just in case (it is, but good practice)
    valid_numbers.sort()
    
    # Read input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        return

    results = []
    for _ in range(Q):
        try:
            A_str = next(iterator)
            A = int(A_str)
        except StopIteration:
            break
        
        # Find the largest number in valid_numbers <= A
        # bisect_right returns the insertion point i such that all e in valid_numbers[:i] have e <= A
        # So the answer is at index i-1
        idx = bisect_right(valid_numbers, A)
        
        if idx > 0:
            results.append(str(valid_numbers[idx - 1]))
        else:
            # According to problem constraints, a solution always exists for A >= 36
            # But if A < 36, no solution exists in our list (smallest is 36)
            results.append("0")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
import sys
from collections import Counter

# Increase recursion depth just in case, though iterative approach is used
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Precompute factorials and inverse factorials for multinomial coefficient
    # Max N is 5000
    max_val = n + 5
    fact = [1] * max_val
    finv = [1] * max_val

    for i in range(1, max_val):
        fact[i] = (fact[i-1] * i) % MOD

    finv[max_val-1] = pow(fact[max_val-1], MOD - 2, MOD)
    for i in range(max_val-2, -1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD

    # Decompose S into primitive components
    # A primitive component is a valid parenthesis sequence that cannot be split
    # into two non-empty valid sequences. This corresponds to the first time
    # the balance counter returns to 0.
    
    primitives = []
    balance = 0
    start_idx = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found a primitive component from start_idx to i
            primitives.append(s[start_idx : i+1])
            start_idx = i + 1

    # Count frequencies of each unique primitive component
    counts = Counter(primitives)
    
    # Calculate multinomial coefficient: N! / (prod(count_i!))
    # where N is the total number of components (len(primitives))
    total_components = len(primitives)
    
    numerator = fact[total_components]
    denominator = 1
    
    for count in counts.values():
        denominator = (denominator * finv[count]) % MOD
        
    ans = (numerator * denominator) % MOD
    print(ans)

if __name__ == '__main__':
    solve()
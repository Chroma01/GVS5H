import sys

# Set recursion limit just in case, though we will use iterative approach
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Step 1: Decompose S into top-level primitive components.
    # A primitive valid parenthesis sequence is one that cannot be split into two non-empty valid parenthesis sequences.
    # We can find these by tracking the balance.
    # A top-level primitive starts when balance goes from 0 to 1 and ends when balance returns to 0.
    
    primitives = []
    balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found a top-level primitive from start_index to i (inclusive)
            primitives.append(s[start_index:i+1])
            start_index = i + 1
            
    # Step 2: Count the frequency of each distinct primitive component.
    from collections import Counter
    counts = Counter(primitives)
    
    # Step 3: Calculate the number of distinct permutations.
    # Formula: k! / (count_1! * count_2! * ... * count_m!)
    # where k is the total number of primitives.
    
    MOD = 998244353
    k = len(primitives)
    
    # Precompute factorials
    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Calculate denominator: product of factorials of counts
    denom = 1
    for c in counts.values():
        denom = (denom * fact[c]) % MOD
        
    # Result is k! * modular_inverse(denom)
    # Modular inverse using Fermat's Little Theorem since MOD is prime
    def mod_inverse(a, m):
        return pow(a, m - 2, m)
        
    ans = (fact[k] * mod_inverse(denom, MOD)) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()
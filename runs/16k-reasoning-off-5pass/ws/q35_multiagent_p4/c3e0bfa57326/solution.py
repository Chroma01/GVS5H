import sys

# Increase recursion depth just in case, though we will use iterative approach
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Step 1: Decompose S into prime (indecomposable) valid parenthesis sequences.
    # A valid parenthesis sequence is prime if its balance (starting at 0, +1 for '(', -1 for ')')
    # never returns to 0 except at the very end of the sequence.
    
    prime_components = []
    balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found a prime component from start_index to i (inclusive)
            prime_components.append(s[start_index : i+1])
            start_index = i + 1
            
    # Step 2: Count the frequency of each unique prime component.
    from collections import Counter
    counts = Counter(prime_components)
    
    # Step 3: Calculate the number of distinct permutations of the multiset of prime components.
    # Formula: k! / (c1! * c2! * ... * cm!)
    # where k is the total number of components, and ci are the counts of each unique component.
    
    k = len(prime_components)
    
    # Precompute factorials and inverse factorials for efficient computation
    # Since k <= N <= 5000, we can precompute up to 5000.
    max_val = k
    fact = [1] * (max_val + 1)
    inv_fact = [1] * (max_val + 1)
    
    for i in range(1, max_val + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Fermat's Little Theorem for modular inverse: a^(MOD-2) % MOD
    inv_fact[max_val] = pow(fact[max_val], MOD - 2, MOD)
    for i in range(max_val - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Numerator: k!
    numerator = fact[k]
    
    # Denominator: product of ci! for each unique component count ci
    denominator = 1
    for count in counts.values():
        denominator = (denominator * fact[count]) % MOD
        
    # Result: numerator * modular_inverse(denominator)
    ans = (numerator * pow(denominator, MOD - 2, MOD)) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()
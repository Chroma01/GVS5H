import sys

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

    # Step 1: Decompose S into prime (irreducible) valid parenthesis sequences.
    # A prime valid sequence is one that cannot be split into two non-empty valid sequences.
    # We can find these by tracking the balance. A prime component starts when balance is 0
    # and ends when balance returns to 0 for the first time.
    
    components = []
    balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # We found a complete valid sequence from start_index to i
            # Since we reset balance to 0 only at the end of a component,
            # and we start at 0, this segment is a prime component.
            components.append(s[start_index : i+1])
            start_index = i + 1
            
    # Step 2: Count frequencies of each unique component
    from collections import Counter
    counts = Counter(components)
    
    # Step 3: Calculate the number of distinct permutations
    # Formula: (Total Length)! / (count1! * count2! * ... * countk!)
    # Here, total length of components is N.
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(2, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Calculate numerator: N!
    numerator = fact[n]
    
    # Calculate denominator: product of (count! for each count)
    denominator = 1
    for count in counts.values():
        denominator = (denominator * fact[count]) % MOD
        
    # Modular inverse for division
    # Using Fermat's Little Theorem: a^(MOD-2) % MOD
    def modInverse(a, m):
        return pow(a, m - 2, m)
        
    result = (numerator * modInverse(denominator, MOD)) % MOD
    
    print(result)

if __name__ == '__main__':
    solve()
import sys

# Set recursion depth just in case, though we won't use deep recursion
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Step 1: Decompose S into primitive valid parenthesis sequences
    # A primitive valid parenthesis sequence is one where the balance
    # returns to 0 only at the very end of the sequence.
    
    primitives = []
    balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        # When balance hits 0, we have completed a primitive component
        if balance == 0:
            # Extract the substring from start_index to i (inclusive)
            prim = s[start_index : i+1]
            primitives.append(prim)
            start_index = i + 1
            
    # Step 2: Count the frequency of each distinct primitive component
    from collections import Counter
    counts = Counter(primitives)
    
    k = len(primitives)
    
    # Step 3: Calculate the multinomial coefficient
    # Number of distinct permutations = k! / (c1! * c2! * ... * cm!)
    # where ci are the frequencies of each distinct primitive component.
    
    # Precompute factorials modulo MOD
    # Max factorial needed is k!
    max_fact = k
    fact = [1] * (max_fact + 1)
    for i in range(2, max_fact + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    numerator = fact[k]
    
    denominator = 1
    for count in counts.values():
        denominator = (denominator * fact[count]) % MOD
        
    # Compute modular inverse of denominator using Fermat's Little Theorem
    # Since MOD is prime, a^(MOD-2) = a^(-1) mod MOD
    denominator_inv = pow(denominator, MOD - 2, MOD)
    
    ans = (numerator * denominator_inv) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()
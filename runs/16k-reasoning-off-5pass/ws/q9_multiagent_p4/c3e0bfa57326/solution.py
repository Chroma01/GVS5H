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

    # We need to decompose the string S into primitive valid parenthesis sequences.
    # A primitive valid parenthesis sequence is one that cannot be split into two non-empty
    # valid parenthesis sequences. This corresponds to a sequence where the prefix sum
    # (mapping '(' to +1, ')' to -1) returns to 0 only at the very end.
    
    # We will iterate through the string, maintaining a current balance.
    # Whenever the balance returns to 0, we have found a primitive component.
    
    components = []
    current_balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            current_balance += 1
        else:
            current_balance -= 1
        
        if current_balance == 0:
            # Found a primitive component from start_index to i
            component = s[start_index : i+1]
            components.append(component)
            start_index = i + 1
            
    # Now we have a list of primitive components.
    # The problem reduces to finding the number of distinct permutations of these components.
    # If we have k components, and there are duplicates, we use the multinomial coefficient.
    # Count = k! / (count1! * count2! * ... * countm!)
    
    counts = Counter(components)
    k = len(components)
    
    MOD = 998244353
    
    # Precompute factorials
    fact = [1] * (k + 1)
    for i in range(2, k + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Calculate denominator
    denom = 1
    for count in counts.values():
        denom = (denom * fact[count]) % MOD
        
    # Result is k! * modInverse(denom) % MOD
    numerator = fact[k]
    
    # Modular inverse using Fermat's Little Theorem
    def modInverse(n):
        return pow(n, MOD - 2, MOD)
        
    ans = (numerator * modInverse(denom)) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()
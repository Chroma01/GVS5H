import sys
from collections import Counter

# Increase recursion depth just in case, though this solution is iterative.
sys.setrecursionlimit(20000)

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # The problem asks for the number of distinct strings obtainable by reversing valid parenthesis substrings.
    # Based on the properties of valid parenthesis sequences and the operation described:
    # 1. Any valid parenthesis sequence can be uniquely decomposed into a sequence of "primitive" 
    #    valid parenthesis sequences (those that cannot be split into two non-empty valid sequences).
    # 2. The operation of reversing a valid substring allows us to swap adjacent primitive components 
    #    and effectively permute them arbitrarily.
    # 3. Therefore, the problem reduces to finding the number of distinct permutations of the multiset 
    #    of primitive components.
    #
    # The number of distinct permutations of a multiset with counts c1, c2, ..., ck is given by:
    #   (Total Count)! / (c1! * c2! * ... * ck!)
    #
    # We need to compute this modulo 998244353.

    MOD = 998244353
    MAX_N = n + 1
    
    # Precompute factorials and inverse factorials
    fact = [1] * MAX_N
    inv = [1] * MAX_N
    
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Compute modular inverse of fact[MAX_N-1] using Fermat's Little Theorem
    inv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    
    # Compute inverse factorials backwards
    for i in range(MAX_N - 2, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    # Decompose S into primitive valid parenthesis components
    # We track the balance of parentheses. A primitive component ends when the balance returns to 0.
    components = []
    balance = 0
    start_index = 0
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found a primitive component from start_index to i
            components.append(s[start_index : i+1])
            start_index = i + 1
            
    # Count the frequency of each unique primitive component
    counts = Counter(components)
    
    # Calculate the multinomial coefficient: K! / (product of counts!)
    # This is equivalent to K! * product(inv[count!])
    K = len(components)
    ans = fact[K]
    
    for c in counts.values():
        ans = (ans * inv[c]) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()
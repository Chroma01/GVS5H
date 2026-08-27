```python
import sys
from collections import Counter

# Increase recursion depth just in case, though not strictly needed here
sys.setrecursionlimit(20000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    if len(input_data) < 2:
        return
        
    N = int(input_data[0])
    S = input_data[1]
    
    # Decompose S into primitive components
    # A primitive component is a valid parenthesis sequence that cannot be split into two non-empty valid sequences.
    # This corresponds to the path returning to balance 0 for the first time.
    components = []
    balance = 0
    start = 0
    for i, char in enumerate(S):
        if char == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found a primitive component
            comp = S[start : i+1]
            components.append(comp)
            start = i + 1
            
    m = len(components)
    
    # Count frequencies of each component
    counts = Counter(components)
    
    MOD = 998244353
    
    # Precompute factorials up to m
    fact = [1] * (m + 1)
    for i in range(2, m + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    def modInverse(n):
        return pow(n, MOD - 2, MOD)
    
    def get_fact(n):
        return fact[n]
    
    visited = set()
    numerator = get_fact(m)
    denominator = 1
    
    # Translation table for swapping '(' and ')'
    # This is used to compute phi(T), which is the reverse of T with parentheses swapped.
    trans = str.maketrans('()', ')(')
    
    unique_components = list(counts.keys())
    
    for T in unique_components:
        if T in visited:
            continue
        
        # Compute phi(T)
        # phi(T) is obtained by reversing T and swapping '(' and ')'
        rev_T = T[::-1]
        U = rev_T.translate(trans)
        
        cnt_T = counts[T]
        cnt_U = counts.get(U, 0)
        
        if T == U:
            # Symmetric orbit: T is invariant under phi.
            # We have cnt_T copies of T. They cannot be changed.
            # The contribution to the number of distinct permutations is 1 / cnt_T!
            # (relative to m!)
            denominator = (denominator * get_fact(cnt_T)) % MOD
        else:
            # Non-symmetric orbit: T and U are distinct and phi(T) = U.
            # We have cnt_T copies of T and cnt_U copies of U.
            # Total items in this orbit C = cnt_T + cnt_U.
            # Each item can be transformed to its phi-image independently.
            # So we have C items that can be either T or U.
            # The number of distinct sequences formed by these items (relative to m!)
            # is sum_{k=0}^{C} (1 / (k! * (C-k)!)) = 2^C / C!
            C = cnt_T + cnt_U
            numerator = (numerator * pow(2, C, MOD)) % MOD
            denominator = (denominator * get_fact(C)) % MOD
        
        visited.add(T)
        if U in counts:
            visited.add(U)
            
    # The result is numerator / denominator modulo MOD
    ans = (numerator * modInverse(denominator)) % MOD
    print(ans)

if __name__ == '__main__':
    solve()
```
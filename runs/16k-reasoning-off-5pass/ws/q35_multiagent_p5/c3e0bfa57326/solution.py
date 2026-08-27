import sys
from collections import Counter

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Step 1: Decompose the valid parenthesis sequence into primitive components.
    # A primitive component is a valid parenthesis sequence that cannot be split into two non-empty valid parenthesis sequences.
    # We can find these by tracking the balance.
    primitives = []
    current_primitive = []
    balance = 0
    
    for char in s:
        current_primitive.append(char)
        if char == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            primitives.append("".join(current_primitive))
            current_primitive = []
            
    # Step 2: Count the occurrences of each distinct primitive component.
    # Since all valid parenthesis sequences are fixed points under the reverse-swap operation,
    # the problem reduces to finding the number of distinct permutations of the multiset of primitive components.
    # The number of distinct permutations of a multiset is given by:
    # N! / (n1! * n2! * ... * nk!)
    # where N is the total number of items, and ni are the counts of each distinct item.
    
    counts = Counter(primitives)
    m = len(primitives)
    
    MOD = 998244353
    
    # Precompute factorials and inverse factorials for efficient computation
    # Since N <= 5000, we can precompute up to 5000.
    max_val = m
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

    # Calculate the multinomial coefficient: m! / (c1! * c2! * ... * ck!)
    # This is equivalent to: m! * (1/c1!) * (1/c2!) * ... * (1/ck!)
    
    ans = fact[m]
    for count in counts.values():
        ans = (ans * inv_fact[count]) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()
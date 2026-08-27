import sys

# Increase recursion depth just in case
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def get_inv_fact(n):
        return inv[n]

    # Function to decompose S into primitive components
    def decompose(S):
        n = len(S)
        components = []
        balance = 0
        start = 0
        for i in range(n):
            if S[i] == '(':
                balance += 1
            else:
                balance -= 1
            
            if balance == 0:
                components.append(S[start:i+1])
                start = i + 1
        return components

    # Function to compute the "reverse-swapped" version of a string
    def reverse_swap(s):
        res = []
        for char in reversed(s):
            if char == '(':
                res.append(')')
            else:
                res.append('(')
        return "".join(res)

    # Decompose S into primitive components
    components = decompose(S)
    
    # Separate into fixed and variable components
    # We group variable components by the pair of lengths (min_len, max_len)
    # because the actual string content doesn't matter for the polynomial degree,
    # only the lengths matter for the EGF.
    # Wait, the EGF depends on the string content? 
    # No, the EGF for a specific string S is x^|S|/|S|!.
    # If we have multiple distinct strings with the same length, they are distinct items in the multiset.
    # However, the problem asks for the number of distinct strings.
    # The generating function approach counts permutations of a multiset.
    # If we have two different strings A and B of the same length L, 
    # they contribute (x^L/L! + x^L/L!) = 2*x^L/L! to the EGF?
    # Yes, because they are distinct items.
    # So we only need to count how many pairs have length (a, b).
    # The actual content of the strings does not affect the count of permutations,
    # only the fact that they are distinct or identical matters.
    # But wait, if we have a pair (A, B) where A != B, and another pair (C, D) where C != D.
    # If A == C and B == D, then we have two identical pairs.
    # If A == C but B != D, then we have different pairs.
    # However, the EGF term for a pair (A, B) is (x^|A|/|A|! + x^|B|/|B|!).
    # This term depends ONLY on the lengths |A| and |B|.
    # So if we have multiple pairs with the same lengths (a, b), we can group them.
    # The number of such pairs is 'count'.
    # The contribution is (x^a/a! + x^b/b!)^count.
    # This is correct because the distinctness of the strings is handled by the fact that
    # we are permuting a multiset of items. If we choose A for one slot and B for another,
    # it's distinct from choosing B for the first and A for the second (if A != B).
    # The EGF multiplication naturally handles this.
    
    fixed_counts = {}
    variable_pair_counts = {}
    
    for comp in components:
        L = len(comp)
        comp_prime = reverse_swap(comp)
        if comp == comp_prime:
            fixed_counts[L] = fixed_counts.get(L, 0) + 1
        else:
            la, lb = L, len(comp_prime)
            if la > lb:
                la, lb = lb, la
            pair_key = (la, lb)
            variable_pair_counts[pair_key] = variable_pair_counts.get(pair_key, 0) + 1
            
    # Initialize polynomial
    current_poly = [0] * (N + 1)
    current_poly[0] = 1
    
    # Process fixed components
    for L, count in fixed_counts.items():
        shift = L * count
        coeff = pow(get_inv_fact(L), count, MOD)
        
        new_poly = [0] * (N + 1)
        for i in range(len(current_poly)):
            if current_poly[i] != 0:
                new_poly[i + shift] = (new_poly[i + shift] + current_poly[i] * coeff) % MOD
        current_poly = new_poly
        
    # Process variable pairs
    for (a, b), count in variable_pair_counts.items():
        deg_pg = (a + b) * count
        
        # Precompute powers of inv_fact
        inv_a = get_inv_fact(a)
        inv_b = get_inv_fact(b)
        
        # We need to compute (x^a/a! + x^b/b!)^count
        # This is sum_{j=0 to count} C(count, j) * (x^a/a!)^j * (x^b/b!)^(count-j)
        # = sum_{j=0 to count} C(count, j) * inv_a^j * inv_b^(count-j) * x^(a*j + b*(count-j))
        
        temp_poly = [0] * (deg_pg + 1)
        c_n_j = 1
        
        for j in range(count + 1):
            term_coeff = (c_n_j * pow(inv_a, j, MOD)) % MOD
            term_coeff = (term_coeff * pow(inv_b, count - j, MOD)) % MOD
            
            power_x = a * j + b * (count - j)
            if power_x <= N:
                temp_poly[power_x] = (temp_poly[power_x] + term_coeff) % MOD
            
            if j < count:
                c_n_j = (c_n_j * (count - j)) % MOD
                c_n_j = (c_n_j * pow(j + 1, MOD - 2, MOD)) % MOD
                
        # Multiply current_poly by temp_poly
        new_current_poly = [0] * (N + 1)
        
        for i in range(len(current_poly)):
            if current_poly[i] == 0:
                continue
            val_i = current_poly[i]
            for j in range(len(temp_poly)):
                if temp_poly[j] == 0:
                    continue
                val_j = temp_poly[j]
                new_current_poly[i + j] = (new_current_poly[i + j] + val_i * val_j) % MOD
        
        current_poly = new_current_poly

    ans = (fact[N] * current_poly[N]) % MOD
    print(ans)

if __name__ == '__main__':
    solve()
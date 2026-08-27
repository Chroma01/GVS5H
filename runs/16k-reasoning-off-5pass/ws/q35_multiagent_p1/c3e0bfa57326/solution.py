import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # Step 1: Decompose S into irreducible components
    # An irreducible component is a valid parenthesis sequence that cannot be split
    # into two non-empty valid parenthesis sequences.
    # We can find them by tracking the balance.
    # When balance drops to 0, we have completed an irreducible component.
    
    components = []
    balance = 0
    start = 0
    
    for i in range(N):
        if S[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Found an irreducible component from start to i (inclusive)
            comp = S[start:i+1]
            components.append(comp)
            start = i + 1
            
    # Step 2: For each component, check if it is symmetric
    # A component C is symmetric if C == R(C), where R(C) is the reverse of C with swapped parentheses.
    
    non_symmetric_count = 0
    
    for comp in components:
        # Compute R(comp)
        # Reverse the string
        rev_comp = comp[::-1]
        # Swap parentheses
        dual_rev = []
        for char in rev_comp:
            if char == '(':
                dual_rev.append(')')
            else:
                dual_rev.append('(')
        dual_rev_str = ''.join(dual_rev)
        
        if comp != dual_rev_str:
            non_symmetric_count += 1
            
    # Step 3: The answer is 2^non_symmetric_count % MOD
    ans = pow(2, non_symmetric_count, MOD)
    
    print(ans)

if __name__ == '__main__':
    solve()
import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # A is 1-indexed, size N+1
    # Store A[i] modulo MOD directly
    A = [0] * (N + 1)
    MOD = 998244353
    
    for i in range(2, N + 1):
        A[i] = int(next(iterator)) % MOD

    # Precompute modular inverses for 1 to N+1
    inv = [1] * (N + 2)
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # Precompute (N-1)!
    fact = 1
    for i in range(1, N):
        fact = (fact * i) % MOD

    # Prefix sums
    # S1[i] = sum_{x=2}^i A[x] * inv[x]
    # S2[i] = sum_{x=2}^i A[x] * 2 * (inv[x] - inv[x+1])
    S1 = [0] * (N + 1)
    S2 = [0] * (N + 1)
    
    curr_S1 = 0
    curr_S2 = 0
    
    for i in range(2, N + 1):
        val = A[i]
        
        # S1
        term1 = (val * inv[i]) % MOD
        curr_S1 = (curr_S1 + term1) % MOD
        S1[i] = curr_S1
        
        # S2
        # p_x = 2 / (x(x+1)) = 2 * (1/x - 1/(x+1))
        diff = (inv[i] - inv[i+1]) % MOD
        term2 = (val * 2 * diff) % MOD
        curr_S2 = (curr_S2 + term2) % MOD
        S2[i] = curr_S2

    results = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        if u > v:
            u, v = v, u
        
        a = u
        b = v
        
        ans = 0
        
        # 1. x < a: sum 2 * S2[a-1]
        if a > 2:
            ans = (ans + 2 * S2[a-1]) % MOD
        # if a == 2, S2[1] is 0, so nothing to add
        
        # 2. x = a: A[a] * (a-1)/a
        if a >= 2:
            term = (A[a] * (a - 1) * inv[a]) % MOD
            ans = (ans + term) % MOD
            
        # 3. a < x < b: S1[b-1] - S1[a]
        if b > a + 1:
            term = (S1[b-1] - S1[a]) % MOD
            ans = (ans + term) % MOD
            
        # 4. x = b: A[b]
        term = A[b]
        ans = (ans + term) % MOD
        
        # Multiply by (N-1)!
        ans = (ans * fact) % MOD
        
        results.append(str(ans))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()
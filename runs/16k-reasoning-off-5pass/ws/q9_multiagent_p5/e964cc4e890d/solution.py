import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

MOD = 998244353
G = 3

def power(a, b):
    res = 1
    while b:
        if b & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        b >>= 1
    return res

def inv(n):
    return power(n, MOD - 2)

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    
    length = 2
    while length <= n:
        ang = power(G, (MOD - 1) // length)
        if invert:
            ang = inv(ang)
        wlen = 1
        for i in range(0, n, length):
            w = 1
            for k in range(i, i + length // 2):
                u = a[k]
                v = (a[k + length // 2] * w) % MOD
                a[k] = (u + v) % MOD
                a[k + length // 2] = (u - v + MOD) % MOD
                w = (w * ang) % MOD
        length <<= 1

    if invert:
        n_inv = inv(n)
        for i in range(n):
            a[i] = (a[i] * n_inv) % MOD

def multiply(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = (fa[i] * fb[i]) % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def inverse_poly(a, n):
    # Computes inverse of polynomial a modulo x^n
    # a[0] must be 1
    res = [1]
    curr_len = 1
    while curr_len < n:
        curr_len <<= 1
        # res_new = res * (2 - a * res) mod x^{curr_len}
        # We need a truncated to curr_len
        a_trunc = a[:curr_len]
        prod = multiply(res, a_trunc)
        prod = prod[:curr_len]
        # 2 - prod
        term = [(2 - x + MOD) % MOD for x in prod]
        res = multiply(res, term)
        res = res[:curr_len]
    return res[:n]

def solve():
    input_data = sys.stdin.read
    data = input_data().split()
    if not data:
        return
    N = int(data[0])
    S = data[1]
    
    # Check balanced prefixes
    # S is 0-indexed in Python, but problem is 1-indexed
    # S[i] corresponds to vertex i+1
    # We check balance at indices 2, 4, ..., 2N
    # Balance = count(W) - count(B)
    # W is 'W', B is 'B'
    
    is_balanced = [False] * (N + 1)
    is_balanced[0] = True
    
    bal = 0
    for i in range(2 * N):
        if S[i] == 'W':
            bal += 1
        else:
            bal -= 1
        
        # After processing i+1 vertices (which is index i in 0-based string)
        # If i+1 is even, say 2k, check if bal == 0
        if (i + 1) % 2 == 0:
            k = (i + 1) // 2
            if bal == 0:
                is_balanced[k] = True
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Construct polynomial F(x) = sum_{i=0}^N i! x^i
    F = [0] * (N + 1)
    for i in range(N + 1):
        F[i] = fact[i]
    
    # Compute InvF = 1/F modulo x^{N+1}
    # F[0] = 0! = 1, so inverse exists
    InvF = inverse_poly(F, N + 1)
    
    # Compute Answer = sum_{k=0}^N (is_balanced[k] ? k! : 0) * InvF[N-k]
    ans = 0
    for k in range(N + 1):
        if is_balanced[k]:
            term = (fact[k] * InvF[N - k]) % MOD
            ans = (ans + term) % MOD
            
    print(ans)

if __name__ == '__main__':
    solve()
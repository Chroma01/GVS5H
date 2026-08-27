import sys

def solve():
    # Set recursion limit higher for deep divide-and-conquer if needed,
    # though iterative or shallow recursion is preferred.
    sys.setrecursionlimit(300000)
    
    MOD = 998244353
    
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    N = int(data[0])
    
    if N == 1:
        print(1 % MOD)
        return
        
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv_fact = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
        
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i + 1) % MOD
        
    # Compute B_i = 10^{len(i)} for i in 1..N
    # We can compute lengths efficiently
    B = [0] * (N + 1)
    
    # Precompute powers of 10
    pow10 = [1] * (N + 1)
    curr = 1
    for i in range(1, N + 1):
        curr = (curr * 10) % MOD
        pow10[i] = curr
        
    for i in range(1, N + 1):
        # Calculate number of digits in i
        # For i in [1, 9], len=1; [10, 99], len=2; etc.
        if i < 10:
            d = 1
        elif i < 100:
            d = 2
        elif i < 1000:
            d = 3
        elif i < 10000:
            d = 4
        elif i < 100000:
            d = 5
        elif i < 1000000:
            d = 6
        elif i < 10000000:
            d = 7
        elif i < 100000000:
            d = 8
        elif i < 1000000000:
            d = 9
        else:
            d = 10
            
        B[i] = pow10[d]
        
    # Compute P(x) = product_{i=1}^N (1 + B_i x)
    # Coefficients E_t for t=0..N
    # Use divide and conquer with iterative polynomial multiplication
    
    def poly_mult(A, B):
        n = len(A)
        m = len(B)
        res = [0] * (n + m - 1)
        for i in range(n):
            if A[i] == 0:
                continue
            val = A[i]
            for j in range(m):
                res[i+j] = (res[i+j] + val * B[j]) % MOD
        return res
    
    # To avoid recursion depth issues, we can use a queue-based approach
    # or just rely on the fact that log2(200000) is about 18, so recursion is fine.
    
    def compute_poly(left, right):
        if left == right:
            return [1, B[left]]
        mid = (left + right) // 2
        L = compute_poly(left, mid)
        R = compute_poly(mid + 1, right)
        return poly_mult(L, R)
        
    E = compute_poly(1, N)
    # E[t] is the t-th elementary symmetric polynomial
    
    # Compute W_T = sum_{k=1}^N k * E_T^{(k)}
    # E_T^{(k)} = e_T of {B_i}_{i!=k}
    # Recurrence: E_T^{(k)} = E_T - B_k * E_{T-1}^{(k)}
    
    W = [0] * N  # W[T] for T=0..N-1
    
    for k in range(1, N + 1):
        bk = B[k]
        # Compute E_T^{(k)} for T=0..N
        # E_0^{(k)} = 1
        # E_T^{(k)} = E[T] - bk * E_{T-1}^{(k)}
        
        # We only need up to T = N-1 for the final answer, but let's compute up to N
        # to be safe and consistent.
        
        E_k_prev = 1  # E_0^{(k)}
        # W[0] += k * E_0^{(k)}
        W[0] = (W[0] + k * E_k_prev) % MOD
        
        for t in range(1, N):
            # E_t^{(k)} = E[t] - bk * E_{t-1}^{(k)}
            E_k_curr = (E[t] - bk * E_k_prev) % MOD
            W[t] = (W[t] + k * E_k_curr) % MOD
            E_k_prev = E_k_curr
            
    # Total = sum_{T=0}^{N-1} T! (N-1-T)! * W[T]
    ans = 0
    for T in range(N):
        term = fact[T] * fact[N-1-T] % MOD * W[T] % MOD
        ans = (ans + term) % MOD
        
    print(ans)

solve()
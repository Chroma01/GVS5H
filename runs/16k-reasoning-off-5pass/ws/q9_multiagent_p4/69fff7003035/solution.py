import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

MOD = 998244353
G = 3

def power(a, b, m=MOD):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def modInverse(n):
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
        wlen = power(G, (MOD - 1) // length)
        if invert:
            wlen = modInverse(wlen)
        for i in range(0, n, length):
            w = 1
            for k in range(length // 2):
                u = a[i + k]
                v = (a[i + k + length // 2] * w) % MOD
                a[i + k] = (u + v) % MOD
                a[i + k + length // 2] = (u - v) % MOD
                w = (w * wlen) % MOD
        length <<= 1
    
    if invert:
        inv_n = modInverse(n)
        for i in range(n):
            a[i] = (a[i] * inv_n) % MOD

def multiply(a, b):
    n = len(a)
    m = len(b)
    size = 1
    while size < n + m:
        size *= 2
    
    fa = a + [0] * (size - n)
    fb = b + [0] * (size - m)
    
    ntt(fa, False)
    ntt(fb, False)
    
    for i in range(size):
        fa[i] = (fa[i] * fb[i]) % MOD
        
    ntt(fa, True)
    
    return fa[:n+m]

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])

    if N == 1:
        print(1)
        return

    # Precompute factorials and inverse factorials
    MAX_N = N + 5
    fact = [1] * MAX_N
    inv = [1] * MAX_N
    for i in range(2, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
    inv[MAX_N-1] = modInverse(fact[MAX_N-1])
    for i in range(MAX_N-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD
        
    # Count frequencies of lengths and sum of values for each length
    cnt = [0] * 7
    sum_vals = [0] * 7
    
    # Numbers 1 to N
    for i in range(1, N + 1):
        s = str(i)
        l = len(s)
        cnt[l] += 1
        sum_vals[l] = (sum_vals[l] + i) % MOD

    # Construct Poly(t) = product_{len=1..6} (1 + 10^len * t)^{cnt[len]}
    poly = [1]
    
    for l in range(1, 7):
        if cnt[l] == 0:
            continue
        
        val = 10**l
        k = cnt[l]
        
        # Create term: [C(k,0)*val^0, C(k,1)*val^1, ..., C(k,k)*val^k]
        term = []
        curr_val = 1
        curr_comb = 1 
        
        term.append(1) 
        
        for j in range(1, k + 1):
            curr_comb = (curr_comb * (k - j + 1)) % MOD
            curr_comb = (curr_comb * inv[j]) % MOD
            curr_val = (curr_val * val) % MOD
            term.append((curr_comb * curr_val) % MOD)
        
        poly = multiply(poly, term)
        
    # Construct H array: h_k = (N-1-k)! * k! for k in 0..N-1
    h = [0] * N
    for k in range(N):
        val = (fact[N-1-k] * fact[k]) % MOD
        h[k] = val
        
    # We need the coefficient of t^N in Poly(t) * H(t)
    # H(t) has degree N-1. Poly(t) has degree N.
    # We need sum_{k=0}^{N-1} h_k * p_{N-k}
    # Let's reverse H to use standard convolution if we wanted coeff of t^N in Poly(t)*H(t)
    # But direct summation is O(N) and simpler.
    
    # We need p_j for j from 1 to N.
    # p_N is the leading coefficient of Poly(t), which is 1.
    # p_{N-1} is the coefficient of t^{N-1}.
    # We can extract these from poly array.
    # poly array is ordered by powers of t: poly[0] is t^0, poly[N] is t^N.
    
    # We need sum_{k=0}^{N-1} h_k * poly[N-k]
    
    # Let's verify indices.
    # h has indices 0 to N-1.
    # poly has indices 0 to N.
    # We need poly[N], poly[N-1], ..., poly[1].
    
    # Note: poly[N] should be 1.
    
    # Calculate the weighted sum K_m = sum_{j=0}^{N-1-m} h_j * poly[N-m-j] ?
    # No, the formula derived was:
    # W(L) = sum_{m=0}^{N-1} (-1)^m * 10^{Lm} * K_m
    # where K_m = sum_{j=0}^{N-1-m} h_j * poly[N-m-j] ??
    # Let's re-verify the convolution logic.
    # We need [t^N] (Poly(t) * H(t)).
    # Let P(t) = sum p_i t^i, H(t) = sum h_j t^j.
    # Coeff of t^N is sum_{i+j=N} p_i h_j.
    # i ranges from 1 to N (since p_0=0? No, p_0 is constant term of Poly).
    # Actually, Poly(t) = product (1 + ...). Constant term is 1.
    # So p_0 = 1.
    # H(t) has terms up to t^{N-1}.
    # So j ranges from 0 to N-1.
    # i = N - j.
    # So we need sum_{j=0}^{N-1} h_j * p_{N-j}.
    # This matches the direct summation plan.
    
    # Let's compute K = sum_{j=0}^{N-1} h_j * poly[N-j]
    # This K is actually the value we need for the "unweighted" case?
    # No, W(L) depends on L.
    # W(L) = sum_{m=0}^{N-1} (-1)^m * 10^{Lm} * [t^{N-m}] (Poly(t) / (1 + 10^L t) * H(t) )?
    # Let's re-derive carefully.
    # We need W(L) = sum_{A subset S_rem} (N-1-|A|)! |A|! 10^{sum L_j}
    # = sum_{m} (N-1-m)! m! sum_{A, |A|=m} 10^{sum L_j}
    # = sum_{m} (N-1-m)! m! [t^m] ( Product_{j in S_rem} (1 + t 10^{L_j}) )
    # Let G_all(t) = Product_{all} (1 + t 10^{L_j}) = Poly(t).
    # Then Product_{S_rem} = G_all(t) / (1 + t 10^L).
    # So W(L) = sum_{m} (N-1-m)! m! [t^m] ( G_all(t) * (1 + t 10^L)^{-1} )
    # = sum_{m} (N-1-m)! m! [t^m] ( G_all(t) * sum_{k=0}^{\infty} (-1)^k (10^L t)^k )
    # = sum_{m} (N-1-m)! m! sum_{k=0}^{m} (-1)^k 10^{Lk} [t^{m-k}] G_all(t)
    # Let j = m-k. Then m = j+k.
    # = sum_{j=0}^{N-1} (N-1-(j+k))! (j+k)! [t^j] G_all(t) * (-1)^k 10^{Lk}
    # We need to sum over k such that j+k <= N-1.
    # Let's swap sums: sum_{k=0}^{N-1} (-1)^k 10^{Lk} sum_{j=0}^{N-1-k} (N-1-j-k)! (j+k)! [t^j] G_all(t)
    # Let h_{j+k} = (N-1-(j+k))! (j+k)!.
    # Then inner sum is sum_{j=0}^{N-1-k} h_{j+k} [t^j] G_all(t).
    # Let p_j = [t^j] G_all(t).
    # Inner sum = sum_{j=0}^{N-1-k} h_{j+k} p_j.
    # Let m = j+k. Then j = m-k.
    # Inner sum = sum_{m=k}^{N-1} h_m p_{m-k}.
    # This is the coefficient of t^k in (H(t) * G_all(1/t) * t^N)? No.
    # It is the coefficient of t^k in H(t) * G_all(t) if we reverse G?
    # Let's just compute it directly.
    # We need to compute S_k = sum_{j=0}^{N-1-k} h_{j+k} p_j for each k.
    # Then W(L) = sum_{k=0}^{N-1} (-1)^k 10^{Lk} S_k.
    
    # To compute S_k efficiently for all k:
    # S_k = sum_{j=0}^{N-1-k} h_{j+k} p_j.
    # This is a convolution of h and p, but with indices shifted.
    # Let H_rev[i] = h[N-1-i].
    # Then S_k = sum_{j=0}^{N-1-k} h_{j+k} p_j.
    # Let m = j+k. S_k = sum_{m=k}^{N-1} h_m p_{m-k}.
    # This is exactly the coefficient of t^k in the product of H(t) and P(t) where P is reversed?
    # Let's check:
    # H(t) = sum h_m t^m.
    # P_rev(t) = sum p_j t^{N-1-j}.
    # Product H(t) * P_rev(t) = sum_{m, j} h_m p_j t^{m + N - 1 - j}.
    # We want coeff of t^{N-1-k}.
    # m + N - 1 - j = N - 1 - k => m - j = -k => j = m + k.
    # Coeff = sum_{m, j: j=m+k} h_m p_j = sum_{m} h_m p_{m+k}.
    # This is sum_{m} h_m p_{m+k}.
    # Our S_k is sum_{m=k}^{N-1} h_m p_{m-k}.
    # This is different.
    
    # Let's try:
    # S_k = sum_{j=0}^{N-1-k} h_{j+k} p_j.
    # Let's reverse h: h_rev[i] = h[N-1-i].
    # Then h_{j+k} = h_rev[N-1-(j+k)].
    # S_k = sum_{j=0}^{N-1-k} h_rev[N-1-j-k] p_j.
    # Let u = N-1-j-k. Then j = N-1-k-u.
    # Range of j: 0 to N-1-k.
    # Range of u: N-1-k to 0.
    # S_k = sum_{u=0}^{N-1-k} h_rev[u] p_{N-1-k-u}.
    # This is the coefficient of t^{N-1-k} in (H_rev(t) * P(t)).
    # H_rev(t) = sum h_rev[u] t^u.
    # P(t) = sum p_j t^j.
    # Coeff of t^{N-1-k} is sum_{u} h_rev[u] p_{N-1-k-u}.
    # Yes!
    # So we need to compute the product Q(t) = H_rev(t) * P(t).
    # Then S_k = [t^{N-1-k}] Q(t).
    # Then W(L) = sum_{k=0}^{N-1} (-1)^k 10^{Lk} S_k.
    
    # Implementation:
    # 1. Compute P(t) = poly.
    # 2. Compute H_rev(t).
    # 3. Compute Q(t) = multiply(H_rev, poly).
    # 4. Extract S_k from Q.
    
    # H_rev construction:
    # h has length N. h[0]..h[N-1].
    # h_rev[i] = h[N-1-i].
    # H_rev(t) = sum_{i=0}^{N-1} h[N-1-i] t^i.
    
    h_rev = [0] * N
    for k in range(N):
        h_rev[k] = h[N-1-k]
        
    # Multiply H_rev and poly
    # poly has degree N. h_rev has degree N-1.
    # Result degree 2N-1.
    res_poly = multiply(h_rev, poly)
    
    total_ans = 0
    
    for l in range(1, 7):
        if cnt[l] == 0:
            continue
            
        v = 10**l
        w_l = 0
        curr_v = 1
        sign = 1
        
        # W(L) = sum_{k=0}^{N-1} (-1)^k * v^k * S_k
        # S_k = coeff of t^{N-1-k} in res_poly
        
        for k in range(N):
            idx = N - 1 - k
            if idx < 0 or idx >= len(res_poly):
                break
            s_k = res_poly[idx]
            if s_k == 0:
                continue
            
            term = (s_k * curr_v) % MOD
            if sign == -1:
                term = (MOD - term) % MOD
            w_l = (w_l + term) % MOD
            
            curr_v = (curr_v * v) % MOD
            sign = -sign
            
        contrib = (sum_vals[l] * w_l) % MOD
        total_ans = (total_ans + contrib) % MOD
        
    print(total_ans)

if __name__ == '__main__':
    solve()
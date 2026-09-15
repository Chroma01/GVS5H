import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    MOD = 998244353

    Lmax = len(str(N))

    # powers of 10 mod MOD
    pw = [1] * (Lmax + 1)
    for l in range(1, Lmax + 1):
        pw[l] = pw[l - 1] * 10 % MOD

    c = [0] * (Lmax + 1)       # count of x with digit length l
    sumx = [0] * (Lmax + 1)    # sum of x with digit length l (mod)
    w = [0] * (Lmax + 1)       # 10^l mod MOD

    lo = 1
    for l in range(1, Lmax + 1):
        hi = 10 ** l - 1
        if hi > N:
            hi = N
        if lo > N:
            break
        cnt = hi - lo + 1
        c[l] = cnt
        sumx[l] = ((lo + hi) * cnt // 2) % MOD
        w[l] = pw[l]
        lo = hi + 1

    Ls = [l for l in range(1, Lmax + 1) if c[l] > 0]

    # A = prod_{l in Ls} (1 + w_l t)                 (degree d)
    # B = sum_{l in Ls} c_l w_l prod_{m!=l}(1 + w_m t) (degree d-1)
    # These satisfy A * Q' = B * Q for Q = prod (1+w_l t)^{c_l}
    A = [1]
    for l in Ls:
        wl = w[l]
        newA = [0] * (len(A) + 1)
        for i, ai in enumerate(A):
            newA[i] = (newA[i] + ai) % MOD
            newA[i + 1] = (newA[i + 1] + ai * wl) % MOD
        A = newA

    B = [0] * (len(A) - 1)
    for l in Ls:
        prod = [1]
        for m in Ls:
            if m == l:
                continue
            wm = w[m]
            newp = [0] * (len(prod) + 1)
            for i, pi in enumerate(prod):
                newp[i] = (newp[i] + pi) % MOD
                newp[i + 1] = (newp[i + 1] + pi * wm) % MOD
            prod = newp
        factor = (c[l] % MOD) * w[l] % MOD
        for j in range(len(prod)):
            B[j] = (B[j] + factor * prod[j]) % MOD

    # modular inverses 1..N
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
        for i in range(2, N + 1):
            inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # pf[k] = k! * (N-1-k)!  (weight for a subset of size k after x)
    pf = [0] * N
    for k in range(N):
        pf[k] = fact[k] * fact[N - 1 - k] % MOD

    # q_k = [t^k] prod (1+w_l t)^{c_l}, via (m+1) q_{m+1}
    #      = sum_i B_i q_{m-i} - sum_{i>=1} A_i (m+1-i) q_{m+1-i}
    q = [0] * (N + 1)
    q[0] = 1
    lenB = len(B)
    lenA = len(A)
    for m in range(N):
        s = 0
        for i in range(lenB):
            j = m - i
            if j < 0:
                break
            s += B[i] * q[j]
        mm = m + 1
        for i in range(1, lenA):
            j = mm - i
            if j < 0:
                break
            s -= A[i] * j * q[j]
        q[mm] = (s % MOD) * inv[mm] % MOD

    # For each length L: h = q/(1+w_L t), M_L = sum h_k * k! * (N-1-k)!
    ans = 0
    for l in Ls:
        wl = w[l]
        h = 0
        M = 0
        for k in range(N):
            hk = (q[k] - wl * h) % MOD
            M = (M + hk * pf[k]) % MOD
            h = hk
        ans = (ans + sumx[l] * M) % MOD

    print(ans % MOD)

main()
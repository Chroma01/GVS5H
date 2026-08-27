import sys
import gc

MOD = 998244353
G = 3

root_ws = [None]
inv_ws = [None]
inv_pow2 = [1]
ntt_ready = 0


def ensure_ntt(log):
    global root_ws, inv_ws, inv_pow2, ntt_ready
    if log <= ntt_ready:
        return
    old = ntt_ready
    add = log - old
    root_ws.extend([None] * add)
    inv_ws.extend([None] * add)
    inv_pow2.extend([1] * add)

    inv2 = (MOD + 1) // 2
    for i in range(old + 1, log + 1):
        inv_pow2[i] = inv_pow2[i - 1] * inv2 % MOD

    for k in range(old + 1, log + 1):
        wlen = pow(G, (MOD - 1) // (1 << k), MOD)
        half = 1 << (k - 1)

        arr = [1] * half
        for i in range(1, half):
            arr[i] = arr[i - 1] * wlen % MOD
        root_ws[k] = arr

        iwlen = pow(wlen, MOD - 2, MOD)
        iarr = [1] * half
        for i in range(1, half):
            iarr[i] = iarr[i - 1] * iwlen % MOD
        inv_ws[k] = iarr

    ntt_ready = log


def ntt(a, invert):
    n = len(a)
    if n == 1:
        return
    mod = MOD

    if not invert:
        length = n
        k = n.bit_length() - 1
        while length > 1:
            half = length >> 1
            ws = root_ws[k]
            for i in range(0, n, length):
                for j in range(half):
                    idx = i + j
                    u = a[idx]
                    v = a[idx + half]
                    x = u + v
                    if x >= mod:
                        x -= mod
                    y = u - v
                    if y < 0:
                        y += mod
                    a[idx] = x
                    a[idx + half] = y * ws[j] % mod
            length = half
            k -= 1
    else:
        length = 2
        k = 1
        while length <= n:
            half = length >> 1
            ws = inv_ws[k]
            for i in range(0, n, length):
                for j in range(half):
                    idx = i + j
                    u = a[idx]
                    v = a[idx + half] * ws[j] % mod
                    x = u + v
                    if x >= mod:
                        x -= mod
                    y = u - v
                    if y < 0:
                        y += mod
                    a[idx] = x
                    a[idx + half] = y
            length <<= 1
            k += 1

        inv_n = inv_pow2[n.bit_length() - 1]
        for i in range(n):
            a[i] = a[i] * inv_n % mod


def convolution_direct(a, b):
    n = len(a)
    m = len(b)
    res = [0] * (n + m - 1)
    mod = MOD

    if n < m:
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    res[i + j] = (res[i + j] + ai * bj) % mod
    else:
        for j, bj in enumerate(b):
            if bj:
                for i, ai in enumerate(a):
                    res[i + j] = (res[i + j] + ai * bj) % mod
    return res


def convolution_ntt(a, b):
    n = len(a)
    m = len(b)
    L = n + m - 1
    size = 1 << ((L - 1).bit_length())
    ensure_ntt(size.bit_length() - 1)

    fa = a + [0] * (size - n)
    fb = b + [0] * (size - m)

    ntt(fa, False)
    ntt(fb, False)

    mod = MOD
    fa = [fa[i] * fb[i] % mod for i in range(size)]
    del fb

    ntt(fa, True)
    return fa


def convolution(a, b):
    n = len(a)
    m = len(b)
    L = n + m - 1
    if L == 1:
        return [a[0] * b[0] % MOD]
    if L <= 64 or min(n, m) <= 32:
        return convolution_direct(a, b)
    fa = convolution_ntt(a, b)
    return fa[:L]


def poly_inv(A, n):
    B = [1]
    m = 1
    while m < n:
        m2 = m << 1
        if m2 > n:
            m2 = n

        C = convolution(A[:m2], B)
        D = [0] * m2
        for i in range(m2):
            if i == 0:
                D[i] = (2 - C[i]) % MOD
            else:
                D[i] = (-C[i]) % MOD

        B = convolution(B, D)
        if len(B) > m2:
            B = B[:m2]
        m = m2
    return B[:n]


def precompute_fact(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    return fact, invfact


def solve_direct(a, r, fact, invfact):
    M = len(a)
    T = [0] * M
    mod = MOD

    for i in range(M):
        if i == 0:
            T[i] = 1
        else:
            si = 0
            ri = r[i]
            for j in range(i):
                si += T[j] * fact[ri - a[j]]
            si %= mod
            T[i] = (-si * invfact[ri - a[i]]) % mod

    return (-T[-1]) % mod


def solve(N, S):
    if S[0] != 'B' or S[-1] != 'W':
        return 0

    fact, invfact = precompute_fact(N)

    a = [0]
    r = [0]
    w = 0
    b = 0
    last = -1

    for ch in S:
        if ch == 'W':
            w += 1
        else:
            if b >= 1:
                rr = w
                if rr >= b and rr != last:
                    a.append(b)
                    r.append(rr)
                    last = rr
            b += 1

    a.append(N)
    r.append(N)
    M = len(a)

    if M == 2:
        return fact[N]

    if M <= 3000:
        return solve_direct(a, r, fact, invfact)

    # Fast path: proper states are 0,1,...,K and r_i = i + c for all proper i.
    K = M - 2
    if a[K] == K:
        if K == 0:
            return fact[N]

        c = r[1] - 1
        ok = True
        if c < 0 or c + K > N:
            ok = False
        else:
            for i in range(1, K + 1):
                if r[i] - i != c:
                    ok = False
                    break

        if ok:
            if c == 0:
                A = [1] + fact[1:K + 1]
            else:
                invfc = invfact[c]
                A = [1] + [invfc * fact[c + k] % MOD for k in range(1, K + 1)]

            T = poly_inv(A, K + 1)
            ans = 0
            mod = MOD
            for j in range(K + 1):
                ans = (ans + T[j] * fact[N - j]) % mod
            return ans

    # CDQ divide-and-conquer with NTT.
    T = [0] * M
    acc = [0] * M
    CDQ_THRESHOLD = 64
    CROSS_DIRECT_LIMIT = 20000
    mod = MOD

    def cdq(left, right):
        if right - left <= CDQ_THRESHOLD:
            acc_l = acc
            T_l = T
            a_l = a
            r_l = r
            fact_l = fact
            invfact_l = invfact

            for i in range(left, right):
                if i == 0:
                    T_l[i] = 1
                else:
                    si = acc_l[i]
                    ri = r_l[i]
                    for j in range(left, i):
                        si += T_l[j] * fact_l[ri - a_l[j]]
                    si %= mod
                    acc_l[i] = si
                    T_l[i] = (-si * invfact_l[ri - a_l[i]]) % mod
            return

        mid = (left + right) >> 1
        cdq(left, mid)

        sl = mid - left
        sr = right - mid

        if sl * sr <= CROSS_DIRECT_LIMIT:
            acc_l = acc
            T_l = T
            a_l = a
            r_l = r
            fact_l = fact

            for i in range(mid, right):
                val = acc_l[i]
                ri = r_l[i]
                for j in range(left, mid):
                    val += T_l[j] * fact_l[ri - a_l[j]]
                acc_l[i] = val % mod
        else:
            a_min = a[left]
            a_max = a[mid - 1]
            A_len = a_max - a_min + 1

            r_min = r[mid]
            r_max = r[right - 1]
            B_len = r_max - r_min + 1
            G_len = A_len + B_len - 1

            if a_max - a_min == sl - 1:
                A = T[left:mid]
            else:
                A = [0] * A_len
                for j in range(left, mid):
                    A[a[j] - a_min] = T[j]

            base = r_min - a_max
            G = fact[base:base + G_len]

            fa = convolution_ntt(A, G)
            offset = A_len - 1
            acc_l = acc

            for i in range(mid, right):
                val = acc_l[i] + fa[offset + r[i] - r_min]
                if val >= mod:
                    val -= mod
                acc_l[i] = val

        cdq(mid, right)

    cdq(0, M)
    return (-T[-1]) % mod


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    gc.disable()
    print(solve(N, S))


if __name__ == "__main__":
    main()
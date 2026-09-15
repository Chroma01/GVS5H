import sys

MOD = 998244353
_NB = 10          # 10-byte (80-bit) slots give exact big-int convolution
_NAIVE = 8000     # schoolbook threshold (product of operand lengths)
_DIRECT = 1500    # O(m^2) DP up to this many live indices
_THRESH = 4000    # naive CDQ cross when left_cnt*right_cnt <= this


def _pack(a):
    nb = _NB
    ba = bytearray(len(a) * nb)
    off = 0
    for v in a:
        ba[off:off + nb] = v.to_bytes(nb, 'little')
        off += nb
    return int.from_bytes(ba, 'little')


def convolution(A, B):
    la = len(A)
    lb = len(B)
    if la == 0 or lb == 0:
        return []
    if la == 1:
        a0 = A[0]
        return [a0 * b % MOD for b in B]
    if lb == 1:
        b0 = B[0]
        return [b0 * a % MOD for a in A]
    if la * lb <= _NAIVE:
        res = [0] * (la + lb - 1)
        for i in range(la):
            a = A[i]
            if a:
                for j in range(lb):
                    res[i + j] = (res[i + j] + a * B[j]) % MOD
        return res
    # Exact integer convolution. coeff < MOD ~ 2^30, so any output coeff
    # <= min(la,lb)*(MOD-1)^2 < 2^78 < 2^80: no slot carry.
    P = _pack(A) * _pack(B)
    count = la + lb - 1
    nb = _NB
    by = P.to_bytes(count * nb + nb, 'little')
    res = [0] * count
    for i in range(count):
        res[i] = int.from_bytes(by[i * nb:i * nb + nb], 'little') % MOD
    return res


def poly_inv(A, n):
    B = [pow(A[0], MOD - 2, MOD)]
    while len(B) < n:
        L = min(2 * len(B), n)
        AB = convolution(A[:L], B)[:L]
        for i in range(L):
            AB[i] = (-AB[i]) % MOD
        AB[0] = (AB[0] + 2) % MOD
        B = convolution(B, AB)[:L]
    return B


def solve(N, S):
    # Strong connectivity requires S[0]='B' and S[-1]='W'.
    if S[0] != 'B' or S[-1] != 'W':
        return 0

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # t[i] = number of W before the (i+1)-th B, for i = 1..N-1.
    t = [0] * (N + 1)
    wc = 0
    bc = 0
    for c in S:
        if c == 'W':
            wc += 1
        else:
            bc += 1
            if bc >= 2:
                t[bc - 1] = wc

    # Live indices: starts of maximal constant-t runs with value >= start.
    idx = [0]
    Tv = [0]
    i = 1
    while i < N:
        tv = t[i]
        st = i
        while i < N and t[i] == tv:
            i += 1
        if tv >= st:
            idx.append(st)
            Tv.append(tv)
    m = len(idx) - 1

    if m == 0:
        return fact[N] % MOD

    # Fast path: idx[k] = s*k and Tv[k]-idx[k] = d constant.
    # Then A(x)*K(x)=fact[d], K(x)=sum fact[d+s*k] x^k, A_k = W_k.
    s = idx[1]
    d = Tv[1] - idx[1]
    ok = True
    for k in range(1, m + 1):
        if idx[k] != s * k or Tv[k] - idx[k] != d:
            ok = False
            break
    if ok:
        K = [fact[d + s * k] for k in range(m + 1)]
        invK = poly_inv(K, m + 1)
        f0 = fact[d]
        ans = 0
        for k in range(m + 1):
            ans = (ans + f0 * invK[k] % MOD * fact[N - s * k]) % MOD
        return ans

    # Small m: direct O(m^2) DP.
    if m <= _DIRECT:
        W = [0] * (m + 1)
        W[0] = 1
        for k in range(1, m + 1):
            Tk = Tv[k]
            sm = 0
            for l in range(k):
                wl = W[l]
                if wl:
                    sm = (sm + wl * fact[Tk - idx[l]]) % MOD
            W[k] = (-inv_fact[Tk - idx[k]] * sm) % MOD
        ans = W[0] * fact[N] % MOD
        for k in range(1, m + 1):
            ans = (ans + W[k] * fact[N - idx[k]]) % MOD
        return ans

    # General case: CDQ divide & conquer.
    W = [0] * (m + 1)
    Sacc = [0] * (m + 1)

    def cdq(l, r):
        if l == r:
            if l == 0:
                W[0] = 1
            else:
                W[l] = (-inv_fact[Tv[l] - idx[l]]) * Sacc[l] % MOD
            return
        mid = (l + r) >> 1
        cdq(l, mid)
        if mid + 1 <= r:
            offset = idx[l]
            if (mid - l + 1) * (r - mid) <= _THRESH:
                for k in range(mid + 1, r + 1):
                    Tk = Tv[k]
                    sm = 0
                    for j in range(l, mid + 1):
                        wj = W[j]
                        if wj:
                            sm = (sm + wj * fact[Tk - idx[j]]) % MOD
                    Sacc[k] = (Sacc[k] + sm) % MOD
            else:
                base = Tv[mid + 1] - idx[mid]
                lenA = idx[mid] - offset + 1
                lenB = Tv[r] - offset - base + 1
                A = [0] * lenA
                for j in range(l, mid + 1):
                    wj = W[j]
                    if wj:
                        A[idx[j] - offset] = wj
                B = fact[base:base + lenB]
                C = convolution(A, B)
                for k in range(mid + 1, r + 1):
                    pos = Tv[k] - offset - base
                    Sacc[k] = (Sacc[k] + C[pos]) % MOD
        cdq(mid + 1, r)

    cdq(0, m)
    ans = W[0] * fact[N] % MOD
    for k in range(1, m + 1):
        ans = (ans + W[k] * fact[N - idx[k]]) % MOD
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()
    sys.stdout.write(str(solve(N, S) % MOD) + "\n")


if __name__ == '__main__':
    main()
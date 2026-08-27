import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    mod = 998244353

    # w[l] = 10^l mod mod, for digit length l = 1..6
    w = [0] * 7
    v = 1
    for i in range(1, 7):
        v = (v * 10) % mod
        w[i] = v

    # counts[l] = number of integers in [1, N] with l digits
    # sums[l]   = sum of those integers
    counts = [0] * 7
    sums = [0] * 7
    lo = 1
    hi10 = 10
    for l in range(1, 7):
        hi = N if N < hi10 else hi10 - 1
        if lo <= hi:
            c = hi - lo + 1
            counts[l] = c
            sums[l] = ((lo + hi) * c // 2) % mod
        lo = hi10
        hi10 *= 10

    active = [l for l in range(1, 7) if counts[l]]
    M = len(active)

    # D(z) = product over active l of (1 + 10^l z)
    d = [1]
    for l in active:
        ww = w[l]
        d.append(0)
        for j in range(len(d) - 1, 0, -1):
            d[j] = (d[j] + ww * d[j - 1]) % mod

    # B(z) = sum_l c_l * 10^l * D(z) / (1 + 10^l z)
    b = [0] * M
    for l in active:
        ww = w[l]
        factor = counts[l] * ww % mod
        b[0] = (b[0] + factor) % mod
        t_prev = 1
        for j in range(1, M):
            t_j = (d[j] - ww * t_prev) % mod
            b[j] = (b[j] + factor * t_j) % mod
            t_prev = t_j

    # modular inverses of 1..N
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = mod - (mod // i) * inv[mod % i] % mod

    # a[k] = k! * (N-1-k)! for k = 0..N-1
    a = [0] * N
    fact = 1
    for i in range(2, N):
        fact = fact * i % mod
    a[0] = fact
    for k in range(N - 1):
        a[k + 1] = a[k] * (k + 1) * inv[N - 1 - k] % mod

    # p[k] = coefficient of z^k in P(z) = product_l (1 + 10^l z)^{c_l}
    # Use P'(z) D(z) = P(z) B(z).
    p = [0] * (N + 1)
    p[0] = 1
    dd = d
    bb = b
    mm = M
    invv = inv
    pp = p

    for k in range(N):
        s1 = 0
        lim1 = mm - 1
        if lim1 > k:
            lim1 = k
        for r in range(lim1 + 1):
            s1 += bb[r] * pp[k - r]

        s2 = 0
        lim2 = mm
        if lim2 > k:
            lim2 = k
        for r in range(1, lim2 + 1):
            s2 += dd[r] * (k - r + 1) * pp[k - r + 1]

        pp[k + 1] = (s1 - s2) * invv[k + 1] % mod

    ans = 0
    aa = a
    for l in active:
        ww = w[l]
        q = 1
        F = aa[0]
        for k in range(1, N):
            q = (pp[k] - ww * q) % mod
            F = (F + aa[k] * q) % mod
        ans = (ans + sums[l] * F) % mod

    print(ans)


if __name__ == "__main__":
    solve()
import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    if N <= 0:
        print(0)
        return

    mod = MOD

    # Digit-length classes: q = 10^d, count, sum of values in this class.
    qs = []
    cs = []
    sums = []

    start = 1
    q_int = 10
    q_mod = 10
    while start <= N:
        end = q_int - 1
        if end > N:
            end = N
        cnt = end - start + 1
        if cnt > 0:
            sums.append(((start + end) * cnt // 2) % mod)
            qs.append(q_mod)
            cs.append(cnt % mod)
        start = q_int
        q_int *= 10
        q_mod = (q_mod * 10) % mod

    m = len(qs)

    # D(z) = product_d (1 + q_d z)
    D = [1]
    for q in qs:
        new = [0] * (len(D) + 1)
        for i, v in enumerate(D):
            new[i] = (new[i] + v) % mod
            new[i + 1] = (new[i + 1] + v * q) % mod
        D = new

    # Num(z) = sum_d c_d q_d D(z) / (1 + q_d z)
    num = [0] * m
    for idx in range(m):
        q = qs[idx]
        c = cs[idx]
        H = [0] * m
        H[0] = D[0]
        for r in range(1, m):
            H[r] = (D[r] - q * H[r - 1]) % mod
        factor = c * q % mod
        for r in range(m):
            num[r] = (num[r] + factor * H[r]) % mod

    # Factorials.
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    # Modular inverses of 1..N.
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = mod - (mod // i) * inv[mod % i] % mod

    # Coefficients a_k of F(z) = product_d (1 + q_d z)^{c_d}, up to k=N-1.
    # From F' * D = F * Num.
    a = [0] * N
    a[0] = 1

    Dcoef = D
    numcoef = num
    inv_local = inv
    m_local = m

    for n in range(N - 1):
        s = 0

        lim1 = m_local - 1
        if lim1 > n:
            lim1 = n
        for r in range(lim1 + 1):
            s += numcoef[r] * a[n - r]

        lim2 = m_local
        if lim2 > n:
            lim2 = n
        for r in range(1, lim2 + 1):
            s -= Dcoef[r] * (n - r + 1) * a[n - r + 1]

        a[n + 1] = (s % mod) * inv_local[n + 1] % mod

    # weight[k] = k! * (N-1-k)!
    n = N - 1
    weight = [0] * N
    for k in range(N):
        weight[k] = fact[k] * fact[n - k] % mod

    ans = 0
    a_local = a
    w_local = weight

    # For each digit class, divide F by (1 + q z) to exclude one number
    # of that length, then combine with factorial weights.
    for idx, q in enumerate(qs):
        g = 1
        W = w_local[0]
        for k in range(1, N):
            g = (a_local[k] - q * g) % mod
            W += g * w_local[k]
        ans = (ans + sums[idx] * (W % mod)) % mod

    print(ans)


if __name__ == "__main__":
    solve()
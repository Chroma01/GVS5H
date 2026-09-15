import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.readline().strip()
    if not data:
        return
    N = int(data)

    # w[d] = 10^d modulo MOD, for digit lengths 1..6
    w = [0] * 7
    wd = 1
    for d in range(1, 7):
        wd = wd * 10 % MOD
        w[d] = wd

    # Count numbers and sum their values for each digit length.
    cnt = [0] * 7
    val = [0] * 7
    lo = 1
    for d in range(1, 7):
        hi = min(N, lo * 10 - 1)
        if lo <= N:
            c = hi - lo + 1
            cnt[d] = c
            val[d] = ((lo + hi) * c // 2) % MOD
        lo *= 10

    active = [d for d in range(1, 7) if cnt[d] > 0]

    # Modular inverses of 1..N.
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # weights[k] = k! * (N-1-k)! modulo MOD.
    # Compute iteratively from weights[0] = (N-1)!.
    weights = [0] * N
    cur = 1
    for i in range(1, N):
        cur = cur * i % MOD
    weights[0] = cur
    for k in range(N - 1):
        cur = cur * (k + 1) % MOD * inv[N - 1 - k] % MOD
        weights[k + 1] = cur

    # R(t) = product_{d active} (1 + w[d] t)
    R = [1]
    for d in active:
        wd = w[d]
        R.append(0)
        for i in range(len(R) - 1, 0, -1):
            R[i] = (R[i] + wd * R[i - 1]) % MOD

    # B(t) = sum_d cnt[d] * w[d] * product_{e active, e != d} (1 + w[e] t)
    m = len(active)
    B = [0] * m
    for d in active:
        poly = [1]
        for f in active:
            if f == d:
                continue
            wf = w[f]
            poly.append(0)
            for i in range(len(poly) - 1, 0, -1):
                poly[i] = (poly[i] + wf * poly[i - 1]) % MOD
        term = cnt[d] * w[d] % MOD
        for i, coef in enumerate(poly):
            B[i] = (B[i] + term * coef) % MOD

    # Pad to fixed sizes for an unrolled recurrence.
    r = [0] * 7
    for i, coef in enumerate(R):
        r[i] = coef
    b = [0] * 6
    for i, coef in enumerate(B):
        b[i] = coef

    # Compute P(t) = product_d (1 + w[d] t)^{cnt[d]}
    # using R(t) P'(t) = B(t) P(t).
    p = [0] * (N + 1)
    p[0] = 1

    # First few coefficients, avoiding negative indices.
    limit = N if N < 6 else 6
    for n in range(limit):
        rhs = 0
        maxb = n if n < 6 else 5
        for i in range(maxb + 1):
            rhs += b[i] * p[n - i]
        maxr = n if n < 7 else 6
        for i in range(1, maxr + 1):
            rhs -= r[i] * (n - i + 1) * p[n - i + 1]
        p[n + 1] = (rhs % MOD) * inv[n + 1] % MOD

    r1, r2, r3, r4, r5, r6 = r[1], r[2], r[3], r[4], r[5], r[6]
    b0, b1, b2, b3, b4, b5 = b[0], b[1], b[2], b[3], b[4], b[5]
    mod = MOD

    for n in range(6, N):
        pn = p[n]
        pn1 = p[n - 1]
        pn2 = p[n - 2]
        pn3 = p[n - 3]
        pn4 = p[n - 4]
        pn5 = p[n - 5]
        rhs = (
            b0 * pn + b1 * pn1 + b2 * pn2 + b3 * pn3 + b4 * pn4 + b5 * pn5
            - r1 * n * pn
            - r2 * (n - 1) * pn1
            - r3 * (n - 2) * pn2
            - r4 * (n - 3) * pn3
            - r5 * (n - 4) * pn4
            - r6 * (n - 5) * pn5
        )
        p[n + 1] = (rhs % mod) * inv[n + 1] % mod

    # For each active digit length d, divide P by (1 + w[d] t)
    # and accumulate sum_k q_k * k! * (N-1-k)!.
    ans = 0
    pp = p
    ww = weights
    for d in active:
        wd = w[d]
        q = 1
        total = ww[0]
        for k in range(1, N):
            q = (pp[k] - wd * q) % mod
            total += q * ww[k]
        total %= mod
        ans = (ans + val[d] * total) % mod

    print(ans)


if __name__ == "__main__":
    main()
import sys

def solve():
    mod = 998244353
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    D = len(str(N))

    c = [0] * (D + 1)
    sum_val = [0] * (D + 1)
    a = [0] * (D + 1)

    p = 1
    pow10 = 1
    for d in range(1, D + 1):
        pow10 = (pow10 * 10) % mod
        a[d] = pow10

        start = p
        p *= 10
        end = min(N, p - 1)
        cnt = end - start + 1
        c[d] = cnt
        sum_val[d] = ((start + end) * cnt // 2) % mod

    n = N - 1

    fact_n = 1
    for i in range(2, n + 1):
        fact_n = fact_n * i % mod

    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
        for i in range(2, n + 1):
            inv[i] = mod - (mod // i) * inv[mod % i] % mod

    invC = [1] * (n + 1)
    for k in range(n):
        invC[k + 1] = invC[k] * (k + 1) % mod * inv[n - k] % mod

    active = [d for d in range(1, D + 1) if c[d] > 0]
    active_a = [a[d] for d in active]
    active_c = [c[d] for d in active]
    active_S = [sum_val[d] for d in active]
    Dact = len(active_a)

    # R(x) = product over active digit lengths of (1 + a_d x)
    r = [1]
    for aa in active_a:
        nr = [0] * (len(r) + 1)
        for i, coef in enumerate(r):
            nr[i] += coef
            nr[i + 1] += coef * aa
        for i in range(len(nr)):
            nr[i] %= mod
        r = nr

    # T(x) = sum_d c_d a_d * product_{e != d} (1 + a_e x)
    # s[Dact] is kept as 0 for the recurrence.
    s = [0] * (Dact + 1)
    for aa, cc in zip(active_a, active_c):
        q = [0] * Dact
        q[0] = 1
        for j in range(1, Dact):
            q[j] = (r[j] - aa * q[j - 1]) % mod
        factor = cc * aa % mod
        for j in range(Dact):
            s[j] = (s[j] + factor * q[j]) % mod

    # E[k] = [x^k] P(x), where P(x) = product_d (1 + 10^d x)^{c_d}
    E = [0] * (n + 1)
    E[0] = 1
    for k in range(n):
        val = s[0] * E[k]
        maxj = Dact if Dact < k else k
        for j in range(1, maxj + 1):
            val += s[j] * E[k - j]
            val -= r[j] * (k - j + 1) * E[k - j + 1]
        E[k + 1] = (val % mod) * inv[k + 1] % mod

    ans = 0
    n1 = n + 1
    for aa, SS in zip(active_a, active_S):
        h = 0
        F = 0
        for k in range(n1):
            h = (E[k] - aa * h) % mod
            F = (F + h * invC[k]) % mod
        ans = (ans + SS * F) % mod

    ans = ans * fact_n % mod
    print(ans)

if __name__ == "__main__":
    solve()
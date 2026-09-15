import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    # Group numbers 1..N by decimal length.
    active = []
    low = 1
    l = 1
    while low <= N:
        high = min(N, low * 10 - 1)
        c = high - low + 1
        s = ((low + high) * c // 2) % MOD
        a = pow(10, l, MOD)
        active.append((l, c, s, a))
        low *= 10
        l += 1

    # D(x) = product over active lengths of (1 + a_l x)
    D = [1]
    for _, _, _, a in active:
        new = [0] * (len(D) + 1)
        for i, val in enumerate(D):
            new[i] = (new[i] + val) % MOD
            new[i + 1] = (new[i + 1] + val * a) % MOD
        D = new

    # C(x) = sum_l c_l a_l * product_{m != l} (1 + a_m x)
    C = [0] * len(active)
    for idx, (_, c, _, a) in enumerate(active):
        coeff = (c % MOD) * a % MOD
        term = [1]
        for j, (_, _, _, a2) in enumerate(active):
            if j == idx:
                continue
            new = [0] * (len(term) + 1)
            for i, val in enumerate(term):
                new[i] = (new[i] + val) % MOD
                new[i + 1] = (new[i + 1] + val * a2) % MOD
            term = new
        for i, val in enumerate(term):
            C[i] = (C[i] + coeff * val) % MOD

    # factorials and modular inverses up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
        for i in range(2, N + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # P(x) = product (1 + a_l x)^{c_l}
    # From P'(x) D(x) = P(x) C(x):
    # (s+1)p_{s+1} = sum_j C[j]p_{s-j}
    #                - sum_{i>=1} D[i]*(s-i+1)*p_{s-i+1}
    p = [0] * (N + 1)
    p[0] = 1
    lenC = len(C)
    lenD = len(D)

    for s in range(N):
        total = 0
        maxj = min(lenC - 1, s)
        for j in range(maxj + 1):
            total += C[j] * p[s - j]

        maxi = min(lenD - 1, s + 1)
        for i in range(1, maxi + 1):
            total -= D[i] * (s - i + 1) * p[s - i + 1]

        p[s + 1] = (total % MOD) * inv[s + 1] % MOD

    # w_k = k! * (N-1-k)!
    w = [0] * N
    for k in range(N):
        w[k] = fact[k] * fact[N - 1 - k] % MOD

    ans = 0
    for _, _, s, a in active:
        # Q_l(x) = P(x) / (1 + a_l x)
        # q_k = p_k - a_l q_{k-1}
        q = 1
        dot = w[0]
        for k in range(1, N):
            q = (p[k] - a * q) % MOD
            dot = (dot + w[k] * q) % MOD
        ans = (ans + s * dot) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    main()
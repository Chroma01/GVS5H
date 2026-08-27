import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    mod = MOD

    D = len(str(N))
    w = [0] * D
    c = [0] * D
    S = [0] * D
    inv2 = (mod + 1) // 2

    for d in range(1, D + 1):
        w[d - 1] = pow(10, d, mod)
        L = 10 ** (d - 1)
        R = min(N, 10 ** d - 1)
        if L <= R:
            cnt = R - L + 1
            c[d - 1] = cnt
            S[d - 1] = ((L + R) % mod) * (cnt % mod) % mod * inv2 % mod

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = mod - (mod // i) * inv[mod % i] % mod

    h = [fact[k] * fact[N - 1 - k] % mod for k in range(N)]

    q = [0] * N
    q[0] = 1

    active = [d for d in range(D) if c[d] > 0]
    m = len(active)
    act_w = [w[d] for d in active]
    act_cw = [c[d] * w[d] % mod for d in active]
    A = [1] * m
    rm = range(m)

    for k in range(N - 1):
        s = 0
        for i in rm:
            s += act_cw[i] * A[i]
        q_next = (s % mod) * inv[k + 1] % mod
        q[k + 1] = q_next
        for i in rm:
            A[i] = (q_next - act_w[i] * A[i]) % mod

    ans = 0
    h0 = h[0]
    for d in active:
        wa = w[d]
        p = 1
        G = h0
        for k in range(1, N):
            p = (q[k] - wa * p) % mod
            G = (G + h[k] * p) % mod
        ans = (ans + S[d] * G) % mod

    print(ans)

if __name__ == "__main__":
    main()
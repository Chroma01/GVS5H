import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    # Counts and value sums for each decimal digit length.
    D = len(str(N))
    cnt = [0] * (D + 1)
    sumv = [0] * (D + 1)

    start = 1
    length = 1
    while start <= N:
        end = min(N, start * 10 - 1)
        c = end - start + 1
        cnt[length] = c
        sumv[length] = ((start + end) * c // 2) % MOD
        start *= 10
        length += 1

    # w[d] = 10^d mod MOD
    w = [0] * (D + 1)
    val = 1
    for d in range(1, D + 1):
        val = (val * 10) % MOD
        w[d] = val

    present = [d for d in range(1, D + 1) if cnt[d] > 0]
    p = len(present)

    w_present = [w[d] for d in present]
    coef = [(cnt[d] % MOD) * w[d] % MOD for d in present]

    # Modular inverses up to N.
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # W_0 = (N-1)!
    fact = 1
    for i in range(1, N):
        fact = fact * i % MOD

    # h[i] is the current coefficient h_{d,k} of P(t) / (1 + w_d t).
    # G[i] accumulates sum_k h_{d,k} * k! * (N-1-k)!.
    h = [1] * p
    G = [fact] * p
    weight = fact

    mod = MOD
    range_p = range(p)
    inv_list = inv
    coef_list = coef
    w_list = w_present
    h_list = h
    G_list = G

    for k in range(1, N):
        # k * a_k = sum_d cnt[d] * w_d * h_{d,k-1}
        total = 0
        for i in range_p:
            total += coef_list[i] * h_list[i]

        a = (total % mod) * inv_list[k] % mod

        # W_k = W_{k-1} * k / (N-k)
        weight = (weight * k % mod) * inv_list[N - k] % mod

        # h_{d,k} = a_k - w_d * h_{d,k-1}
        for i in range_p:
            hi = (a - w_list[i] * h_list[i]) % mod
            h_list[i] = hi
            G_list[i] += hi * weight

    ans = 0
    for i, d in enumerate(present):
        ans = (ans + sumv[d] * (G_list[i] % mod)) % mod

    print(ans)


if __name__ == "__main__":
    main()
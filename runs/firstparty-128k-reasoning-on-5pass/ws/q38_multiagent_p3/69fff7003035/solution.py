import sys

def main():
    mod = 998244353
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    a_list = []
    val_list = []
    cnt_list = []
    start = 1
    a = 10
    while start <= N:
        end = start * 10 - 1
        if end > N:
            end = N
        cnt = end - start + 1
        val = (start + end) * cnt // 2
        a_list.append(a)
        val_list.append(val % mod)
        cnt_list.append(cnt)
        start *= 10
        a = (a * 10) % mod

    K = len(a_list)

    # M(z) = product over digit groups of (1 + a_d z)
    m = [1]
    for a in a_list:
        new = [0] * (len(m) + 1)
        for i, mi in enumerate(m):
            new[i] += mi
            new[i + 1] += mi * a
        for i in range(len(new)):
            new[i] %= mod
        m = new

    # E(z) = sum_d cnt_d * a_d * M(z) / (1 + a_d z)
    e = [0] * K
    for idx, a in enumerate(a_list):
        factor = cnt_list[idx] * a % mod
        prev = 0
        for i in range(K):
            qi = (m[i] - a * prev) % mod
            e[i] = (e[i] + factor * qi) % mod
            prev = qi

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = mod - (mod // i) * inv[mod % i] % mod

    p = [0] * N
    p[0] = 1
    c = [0] * K
    ans = 0

    a_l = a_list
    val_l = val_list
    m_l = m
    e_l = e
    fact_l = fact
    inv_l = inv
    p_l = p
    c_l = c
    rngK = range(K)

    for s in range(N):
        ps = p_l[s]
        term = 0
        for d in rngK:
            cd = c_l[d]
            nd = (ps - a_l[d] * cd) % mod
            c_l[d] = nd
            term += val_l[d] * nd
        term %= mod
        ans = (ans + fact_l[s] * fact_l[N - s - 1] % mod * term) % mod

        if s < N - 1:
            sp1 = s + 1
            rhs = 0

            if s < K - 1:
                maxj = s
            else:
                maxj = K - 1
            for j in range(maxj + 1):
                rhs += e_l[j] * p_l[s - j]

            if sp1 <= K:
                maxi = sp1 - 1
            else:
                maxi = K
            for i in range(1, maxi + 1):
                rhs -= m_l[i] * (sp1 - i) * p_l[sp1 - i]

            p_l[sp1] = (rhs % mod) * inv_l[sp1] % mod

    print(ans % mod)

if __name__ == "__main__":
    main()
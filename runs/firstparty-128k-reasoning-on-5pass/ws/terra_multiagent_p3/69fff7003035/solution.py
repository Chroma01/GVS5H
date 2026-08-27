import sys

MOD = 998244353

def main():
    N = int(sys.stdin.readline())

    counts = []
    sums = []
    bs = []

    start = 1
    d = 1
    while start <= N:
        end = min(N, start * 10 - 1)
        c = end - start + 1
        counts.append(c)
        sums.append(((start + end) * c // 2) % MOD)
        bs.append((pow(10, d, MOD) - 1) % MOD)
        start *= 10
        d += 1

    m = len(counts)

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    fact = 1
    for i in range(2, N + 1):
        fact = fact * i % MOD

    # D(t) = product_i (1 + b_i t)
    D = [1]
    for b in bs:
        nd = [0] * (len(D) + 1)
        for j, v in enumerate(D):
            nd[j] = (nd[j] + v) % MOD
            nd[j + 1] = (nd[j + 1] + v * b) % MOD
        D = nd

    # A(t) = sum_i c_i * b_i * D(t) / (1 + b_i t)
    A = [0] * m
    for i, b in enumerate(bs):
        q = [0] * m
        q[0] = D[0]
        for j in range(1, m):
            q[j] = (D[j] - b * q[j - 1]) % MOD
        mul = counts[i] % MOD * b % MOD
        for j in range(m):
            A[j] = (A[j] + mul * q[j]) % MOD

    # P(t) = product_i (1 + b_i t)^c_i.
    # From D(t) P'(t) = A(t) P(t), compute coefficients in O(N*m).
    P = [0] * (N + 1)
    P[0] = 1
    for n in range(1, N + 1):
        val = 0

        for j in range(m):
            idx = n - 1 - j
            if idx >= 0:
                val += A[j] * P[idx]

        for j in range(1, m + 1):
            idx = n - j
            if idx >= 0:
                val -= D[j] * (n - j) * P[idx]

        P[n] = (val % MOD) * inv[n] % MOD

    total = 0

    # For every digit-length class i:
    # P(t)/(1+b_i t) is the product excluding one number in that class.
    for i, b in enumerate(bs):
        q_prev = P[0]
        integral = q_prev  # coefficient of t^0 divided by 1

        for k in range(1, N):
            q_cur = (P[k] - b * q_prev) % MOD
            integral = (integral + q_cur * inv[k + 1]) % MOD
            q_prev = q_cur

        total = (total + sums[i] * integral) % MOD

    print(total * fact % MOD)

if __name__ == "__main__":
    main()
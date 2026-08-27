import sys

MOD = 998244353

def main():
    N = int(sys.stdin.readline())
    
    counts = []
    sums = []
    start = 1
    d = 1
    while start <= N:
        end = min(N, start * 10 - 1)
        c = end - start + 1
        counts.append(c)
        sums.append(((start + end) * c // 2) % MOD)
        start *= 10
        d += 1

    g = len(counts)
    weights = [pow(10, i + 1, MOD) for i in range(g)]
    a = weights
    b = [(1 - x) % MOD for x in weights]

    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Q(t) = product of distinct linear factors a_j + b_j*t
    Q = [1]
    for j in range(g):
        nq = [0] * (len(Q) + 1)
        for k, v in enumerate(Q):
            nq[k] = (nq[k] + v * a[j]) % MOD
            nq[k + 1] = (nq[k + 1] + v * b[j]) % MOD
        Q = nq

    # R(t) = sum_j count_j * b_j * product_{h != j}(a_h + b_h*t)
    R = [0] * g
    for j in range(g):
        poly = [1]
        for h in range(g):
            if h == j:
                continue
            np = [0] * (len(poly) + 1)
            for k, v in enumerate(poly):
                np[k] = (np[k] + v * a[h]) % MOD
                np[k + 1] = (np[k + 1] + v * b[h]) % MOD
            poly = np
        mul = counts[j] % MOD * b[j] % MOD
        for k, v in enumerate(poly):
            R[k] = (R[k] + mul * v) % MOD

    # P(t) = product_j (a_j + b_j*t)^count_j.
    # From Q*P' = R*P, compute all coefficients in O(g*N).
    P = [0] * (N + 1)
    p0 = 1
    for j in range(g):
        p0 = p0 * pow(a[j], counts[j], MOD) % MOD
    P[0] = p0

    inv_q0 = pow(Q[0], MOD - 2, MOD)
    for k in range(N):
        rhs = 0
        upper_r = min(g - 1, k)
        for h in range(upper_r + 1):
            rhs += R[h] * P[k - h]
        upper_q = min(g, k)
        for h in range(1, upper_q + 1):
            rhs -= Q[h] * (k - h + 1) * P[k - h + 1]
        P[k + 1] = (rhs % MOD) * inv[k + 1] % MOD * inv_q0 % MOD

    fact = 1
    for x in range(2, N + 1):
        fact = fact * x % MOD

    ans = 0

    # For each digit group, divide P by its linear factor and integrate.
    for j in range(g):
        q = [0] * N
        inv_a = pow(a[j], MOD - 2, MOD)
        q[0] = P[0] * inv_a % MOD
        integral = q[0]

        for k in range(1, N):
            q[k] = (P[k] - b[j] * q[k - 1]) % MOD * inv_a % MOD
            integral = (integral + q[k] * inv[k + 1]) % MOD

        ans = (ans + sums[j] * fact % MOD * integral) % MOD

    print(ans)

if __name__ == "__main__":
    main()
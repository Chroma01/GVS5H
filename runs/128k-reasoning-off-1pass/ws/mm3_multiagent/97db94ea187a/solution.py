import sys
import numpy as np

def solve():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    A = N // 2
    M_max = N * (N - 1) // 2
    FFT_size = 1
    while FFT_size <= 2 * M_max:
        FFT_size *= 2

    # Binomial coefficients mod P
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P

    # 2^C(s, 2) mod P
    pow2 = [1] * (N + 1)
    for s in range(1, N + 1):
        pow2[s] = pow(2, s * (s - 1) // 2, P)

    # Precompute Q[b][s] = ((1+x)^b - 1)^s coefficients, truncated to degree M_max
    Q = np.zeros((N + 1, N + 1, M_max + 1), dtype=np.int64)
    for b in range(1, N + 1):
        R = np.zeros(M_max + 1, dtype=np.int64)
        for j in range(1, min(b, M_max) + 1):
            R[j] = C[b][j] % P
        power = np.zeros(M_max + 1, dtype=np.int64)
        power[0] = 1
        for s in range(1, N + 1):
            new_power = np.zeros(M_max + 1, dtype=np.int64)
            for i in range(M_max + 1):
                pi = power[i]
                if pi == 0:
                    continue
                max_j = min(M_max - i, b)
                for j in range(1, max_j + 1):
                    rj = R[j]
                    if rj == 0:
                        continue
                    new_power[i + j] = (new_power[i + j] + pi * rj) % P
            power = new_power
            Q[b][s] = power

    # Precompute rfft of Q[b][s] using float64
    Q_fft = np.zeros((N + 1, N + 1, FFT_size // 2 + 1), dtype=np.float64)
    for b in range(1, N + 1):
        for s in range(1, N + 1):
            Q_fft[b][s] = np.fft.rfft(Q[b][s].astype(np.float64), n=FFT_size)

    # DP: state (a, b, p) -> 2D array (A+1, M_max+1)
    dp = {}
    init = np.zeros((A + 1, M_max + 1), dtype=np.int64)
    init[1, 0] = 1
    dp[(1, 1, 0)] = init

    for a in range(1, N):
        for b in range(1, a + 1):
            for p in (0, 1):
                key = (a, b, p)
                if key not in dp:
                    continue
                P_arr = dp[key]
                if not np.any(P_arr):
                    del dp[key]
                    continue
                P_fft = np.fft.rfft(P_arr.astype(np.float64), n=FFT_size, axis=1)
                for s in range(1, N - a + 1):
                    tkey = (a + s, s, 1 - p)
                    if tkey not in dp:
                        dp[tkey] = np.zeros((A + 1, M_max + 1), dtype=np.int64)
                    target = dp[tkey]
                    res_fft = P_fft * Q_fft[b, s][None, :]
                    res = np.fft.irfft(res_fft, n=FFT_size, axis=1)
                    res = res[:, :M_max + 1]
                    res = np.rint(res).astype(np.int64) % P
                    factor = (C[N - a][s] * pow2[s]) % P
                    if factor != 1:
                        res = (res * factor) % P
                    if p == 0:
                        target[:A + 1, :] = (target[:A + 1, :] + res) % P
                    else:
                        if s <= A:
                            target[s:A + 1, :] = (target[s:A + 1, :] + res[:A + 1 - s, :]) % P
                del dp[key]

    # Collect answer
    ans = [0] * (M_max + 1)
    for b in range(1, N + 1):
        for p in (0, 1):
            key = (N, b, p)
            if key in dp:
                row = dp[key][A, :]
                for m in range(N - 1, M_max + 1):
                    ans[m] = (ans[m] + int(row[m])) % P

    print(' '.join(str(ans[m]) for m in range(N - 1, M_max + 1)))

solve()
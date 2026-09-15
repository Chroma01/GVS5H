import sys

def fwht_np(a):
    n = a.shape[0]
    length = 1
    while length < n:
        a = a.reshape(-1, 2 * length)
        u = a[:, :length].copy()
        v = a[:, length:].copy()
        a[:, :length] = u + v
        a[:, length:] = u - v
        a = a.reshape(-1)
        length <<= 1
    return a

def fwht_py(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            j = i
            end = i + h
            while j < end:
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
                j += 1
        h = step
    return a

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    n = 1 << W
    freq = [0] * n
    for s in rows:
        p = int(s, 2)
        freq[p] += 1

    # Precompute G[j] = WHT(g) for any mask with popcount j
    # g[m] = min(popcount(m), W - popcount(m))
    C = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    G = [0] * (W + 1)
    for j in range(W + 1):
        total = 0
        for a in range(j + 1):
            for b in range(W - j + 1):
                val = a + b
                if val > W - val:
                    val = W - val
                term = C[j][a] * C[W - j][b] * val
                if a & 1:
                    total -= term
                else:
                    total += term
        G[j] = total

    try:
        import numpy as np
        use_np = True
    except ImportError:
        use_np = False

    if use_np:
        idx = np.arange(n, dtype=np.int64)
        pop = np.zeros(n, dtype=np.int64)
        for i in range(W):
            pop += (idx >> i) & 1
        G_arr = np.array(G, dtype=np.int64)
        ghat = G_arr[pop]
        f = np.array(freq, dtype=np.int64)
        F = fwht_np(f)
        H_hat = F * ghat
        S = fwht_np(H_hat) // n
        ans = int(S.min())
        print(ans)
    else:
        pop = [0] * n
        for i in range(1, n):
            pop[i] = pop[i >> 1] + (i & 1)
        F = fwht_py(freq)
        H_hat = [0] * n
        for c in range(n):
            H_hat[c] = F[c] * G[pop[c]]
        S = fwht_py(H_hat)
        ans = min(S) // n
        print(ans)

if __name__ == "__main__":
    main()
import sys
from math import comb


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    n = 1 << W

    # Histogram of row masks
    freq = [0] * n
    for r in rows:
        m = 0
        for ch in r:
            m = (m << 1) | (ch - 48)
        freq[m] += 1

    # g(k) = min(k, W - k): min ones in a row whose XOR with column flips has popcount k
    g = [min(k, W - k) for k in range(W + 1)]

    # Walsh-Hadamard (XOR) transform of kernel k[d] = g(popcount(d)), computed
    # analytically via Krawtchouk polynomials:
    #   hat_k[s] = sum_j g(j) * K_j(popcount(s)),
    #   K_j(t) = sum_i (-1)^i * C(t, i) * C(W - t, j - i)
    hat_k_by_pop = [0] * (W + 1)
    for t in range(W + 1):
        total = 0
        for j in range(W + 1):
            kj = 0
            lo = max(0, j - (W - t))
            hi = min(j, t)
            for i in range(lo, hi + 1):
                term = comb(t, i) * comb(W - t, j - i)
                if i & 1:
                    kj -= term
                else:
                    kj += term
            total += g[j] * kj
        hat_k_by_pop[t] = total

    try:
        import numpy as np

        # popcounts of 0..n-1 via SWAR bit tricks (uint64)
        x = np.arange(n, dtype=np.uint64)
        x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
        x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
        x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
        pc = ((x * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int64)

        hk = np.array(hat_k_by_pop, dtype=np.int64)[pc]

        def fwt(v):
            # In-place-style iterative Walsh-Hadamard butterfly.
            # reshape(-1, 2, step): index = block*(2*step) + half*step + off,
            # pairing (block, off) positions i and i+step exactly as required.
            step = 1
            while step < n:
                v = v.reshape(-1, 2, step)
                u = v[:, 0, :].copy()
                w = v[:, 1, :].copy()
                v[:, 0, :] = u + w
                v[:, 1, :] = u - w
                v = v.reshape(-1)
                step <<= 1
            return v

        a = np.array(freq, dtype=np.int64)
        fa = fwt(a)
        prod = fa * hk
        h = fwt(prod) // n  # exact: FWT is self-inverse up to factor n
        ans = int(h.min())
    except ImportError:
        # Pure-Python fallback
        pc = [0] * n
        for i in range(1, n):
            pc[i] = pc[i >> 1] + (i & 1)
        hk = [hat_k_by_pop[pc[i]] for i in range(n)]

        def fwt_list(v):
            step = 1
            while step < n:
                for start in range(0, n, step * 2):
                    up = start + step
                    for i in range(start, up):
                        u = v[i]
                        w = v[i + step]
                        v[i] = u + w
                        v[i + step] = u - w
                step <<= 1

        fwt_list(freq)
        for i in range(n):
            freq[i] *= hk[i]
        fwt_list(freq)
        ans = min(v // n for v in freq)

    print(ans)


main()
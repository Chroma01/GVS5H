import sys
from math import comb
from operator import add, sub


def fwht(a, n):
    """In-place XOR Walsh-Hadamard transform (unnormalized, self-inverse up to factor n)."""
    step = 1
    while step < n:
        jump = step << 1
        for i in range(0, n, jump):
            lo = a[i:i + step]
            hi = a[i + step:i + jump]
            a[i:i + step] = list(map(add, lo, hi))
            a[i + step:i + jump] = list(map(sub, lo, hi))
        step = jump


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    n = 1 << W

    # Aggregate identical rows into counts over masks.
    cnt = [0] * n
    for i in range(H):
        cnt[int(data[2 + i], 2)] += 1

    # Transform of the row-count array.
    fwht(cnt, n)

    # Kernel f(t) = min(popcount(t), W - popcount(t)) depends only on popcount,
    # so its Walsh-Hadamard transform depends only on popcount(S):
    #   f_hat[S] = sum_k f(k) * K_k(popcount(S))
    # where K_k(s) = sum_j (-1)^j C(s,j) C(W-s, k-j)  (Krawtchouk).
    f = [0] * (W + 1)
    for k in range(W + 1):
        f[k] = k if k <= W - k else W - k

    fhat = [0] * (W + 1)
    for s in range(W + 1):
        total = 0
        ws = W - s
        for k in range(W + 1):
            fk = f[k]
            if fk == 0:
                continue
            lo_j = k - ws
            if lo_j < 0:
                lo_j = 0
            hi_j = k if k < s else s
            K = 0
            sign = -1 if (lo_j & 1) else 1
            for j in range(lo_j, hi_j + 1):
                K += sign * comb(s, j) * comb(ws, k - j)
                sign = -sign
            total += fk * K
        fhat[s] = total

    # Popcounts of all masks.
    pc = [0] * n
    for i in range(1, n):
        pc[i] = pc[i >> 1] + (i & 1)

    # Pointwise product in transform domain.
    p = [cnt[i] * fhat[pc[i]] for i in range(n)]

    # Inverse transform (same butterfly); result is n times the true convolution.
    fwht(p, n)

    # min(p[c]) = n * min(g[c]); division is exact.
    sys.stdout.write(str(min(p) // n) + "\n")


main()
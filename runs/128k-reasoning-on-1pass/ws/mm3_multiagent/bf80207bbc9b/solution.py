import sys

def fwht(a):
    """In‑place Fast Walsh–Hadamard Transform (XOR version)."""
    n = len(a)
    step = 1
    while step < n:
        for i in range(0, n, step << 1):
            for j in range(i, i + step):
                u = a[j]
                v = a[j + step]
                a[j] = u + v
                a[j + step] = u - v
        step <<= 1

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = 1 << W

    freq = [0] * N
    for _ in range(H):
        s = next(it).decode()
        mask = int(s, 2)
        freq[mask] += 1

    # f[mask] = min(popcount(mask), W - popcount(mask))
    f = [0] * N
    for mask in range(N):
        p = mask.bit_count()
        f[mask] = p if p <= W - p else W - p

    # XOR‑convolution of freq and f via FWHT
    a = freq[:]          # copy
    b = f[:]
    fwht(a)
    fwht(b)
    for i in range(N):
        a[i] = a[i] * b[i]
    fwht(a)              # inverse transform (same routine)
    n_inv = N
    for i in range(N):
        a[i] //= n_inv    # normalisation

    ans = min(a)
    print(ans)

if __name__ == "__main__":
    solve()
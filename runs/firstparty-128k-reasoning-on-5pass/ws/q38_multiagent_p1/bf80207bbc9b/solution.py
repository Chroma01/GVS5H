import sys

_T_cache = {}


def get_T(W):
    cached = _T_cache.get(W)
    if cached is not None:
        return cached

    C = [[0] * (W + 1) for _ in range(W + 1)]
    for n in range(W + 1):
        C[n][0] = 1
        C[n][n] = 1
        for k in range(1, n):
            C[n][k] = C[n - 1][k - 1] + C[n - 1][k]

    T = [0] * (W + 1)
    for t in range(W + 1):
        Ct = C[t]
        Cwt = C[W - t]
        wt = W - t
        total = 0
        for k in range(W + 1):
            g = k if k <= W - k else W - k
            if g == 0:
                continue
            lo = k - wt
            if lo < 0:
                lo = 0
            hi = t if t < k else k
            s = 0
            for j in range(lo, hi + 1):
                term = Ct[j] * Cwt[k - j]
                if j & 1:
                    s -= term
                else:
                    s += term
            total += g * s
        T[t] = total

    _T_cache[W] = T
    return T


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        if h == 1:
            for i in range(0, n, 2):
                i1 = i + 1
                x = a[i]
                y = a[i1]
                a[i] = x + y
                a[i1] = x - y
        elif h == 2:
            for i in range(0, n, 4):
                i2 = i + 2
                i3 = i + 3
                x = a[i]
                y = a[i2]
                a[i] = x + y
                a[i2] = x - y
                x = a[i + 1]
                y = a[i3]
                a[i + 1] = x + y
                a[i3] = x - y
        elif h == 4:
            for i in range(0, n, 8):
                i4 = i + 4
                i5 = i + 5
                i6 = i + 6
                i7 = i + 7
                x = a[i]
                y = a[i4]
                a[i] = x + y
                a[i4] = x - y
                x = a[i + 1]
                y = a[i5]
                a[i + 1] = x + y
                a[i5] = x - y
                x = a[i + 2]
                y = a[i6]
                a[i + 2] = x + y
                a[i6] = x - y
                x = a[i + 3]
                y = a[i7]
                a[i + 3] = x + y
                a[i7] = x - y
        elif h == 8:
            for i in range(0, n, 16):
                i8 = i + 8
                i9 = i + 9
                i10 = i + 10
                i11 = i + 11
                i12 = i + 12
                i13 = i + 13
                i14 = i + 14
                i15 = i + 15
                x = a[i]
                y = a[i8]
                a[i] = x + y
                a[i8] = x - y
                x = a[i + 1]
                y = a[i9]
                a[i + 1] = x + y
                a[i9] = x - y
                x = a[i + 2]
                y = a[i10]
                a[i + 2] = x + y
                a[i10] = x - y
                x = a[i + 3]
                y = a[i11]
                a[i + 3] = x + y
                a[i11] = x - y
                x = a[i + 4]
                y = a[i12]
                a[i + 4] = x + y
                a[i12] = x - y
                x = a[i + 5]
                y = a[i13]
                a[i + 5] = x + y
                a[i13] = x - y
                x = a[i + 6]
                y = a[i14]
                a[i + 6] = x + y
                a[i14] = x - y
                x = a[i + 7]
                y = a[i15]
                a[i + 7] = x + y
                a[i15] = x - y
        else:
            for i in range(0, n, step):
                for j in range(i, i + h, 4):
                    jh = j + h
                    x = a[j]
                    y = a[jh]
                    a[j] = x + y
                    a[jh] = x - y
                    x = a[j + 1]
                    y = a[jh + 1]
                    a[j + 1] = x + y
                    a[jh + 1] = x - y
                    x = a[j + 2]
                    y = a[jh + 2]
                    a[j + 2] = x + y
                    a[jh + 2] = x - y
                    x = a[j + 3]
                    y = a[jh + 3]
                    a[j + 3] = x + y
                    a[jh + 3] = x - y
        h = step


def solve_from_freq(H, W, freq):
    if H <= 1 or W <= 1:
        return 0

    N = 1 << W
    T = get_T(W)
    kernel_hat = [T[i.bit_count()] for i in range(N)]

    fwht(freq)
    freq = [x * y for x, y in zip(freq, kernel_hat)]
    del kernel_hat
    fwht(freq)

    return min(freq) // N


def solve_case(H, W, rows):
    if H <= 1 or W <= 1:
        return 0

    N = 1 << W
    freq = [0] * N
    for s in rows:
        freq[int(s, 2)] += 1
    return solve_from_freq(H, W, freq)


def brute_force(rows, H, W):
    masks = [int(s, 2) for s in rows]
    full = (1 << W) - 1
    best = H * W

    for cm in range(1 << W):
        for rm in range(1 << H):
            total = 0
            for i, m in enumerate(masks):
                v = m ^ cm
                if (rm >> i) & 1:
                    v ^= full
                total += v.bit_count()
                if total >= best:
                    break
            if total < best:
                best = total
    return best


def brute_fast(rows, H, W):
    masks = [int(s, 2) for s in rows]
    best = H * W

    for cm in range(1 << W):
        total = 0
        for m in masks:
            d = (m ^ cm).bit_count()
            total += d if d <= W - d else W - d
            if total >= best:
                break
        if total < best:
            best = total
    return best


def selftest():
    for W in range(1, 7):
        N = 1 << W
        K = [min(i.bit_count(), W - i.bit_count()) for i in range(N)]
        fwht(K)
        T = get_T(W)
        for m in range(N):
            if K[m] != T[m.bit_count()]:
                raise AssertionError(f"kernel transform mismatch W={W} m={m}")

    samples = [
        (3, 3, ["100", "010", "110"], 2),
        (3, 4, ["1111", "1111", "1111"], 0),
        (10, 5, ["10000", "00111", "11000", "01000", "10110",
                 "01110", "10101", "00100", "00100", "10001"], 13),
    ]
    for H, W, rows, ans in samples:
        got = solve_case(H, W, rows)
        if got != ans:
            raise AssertionError(f"sample failed: H={H} W={W} got={got} expected={ans}")

    import random
    random.seed(12345)

    for _ in range(300):
        W = random.randint(1, 5)
        H = random.randint(1, 5)
        rows = [''.join(random.choice('01') for _ in range(W)) for _ in range(H)]
        got = solve_case(H, W, rows)
        exp = brute_force(rows, H, W)
        if got != exp:
            raise AssertionError(f"random failed: H={H} W={W} rows={rows} got={got} exp={exp}")

    for _ in range(50):
        W = random.randint(6, 8)
        H = random.randint(1, 3)
        rows = [''.join(random.choice('01') for _ in range(W)) for _ in range(H)]
        got = solve_case(H, W, rows)
        exp = brute_force(rows, H, W)
        if got != exp:
            raise AssertionError(f"random failed: H={H} W={W} rows={rows} got={got} exp={exp}")

    W = 18
    H = 2
    rows = [''.join(random.choice('01') for _ in range(W)) for _ in range(H)]
    got = solve_case(H, W, rows)
    exp = brute_fast(rows, H, W)
    if got != exp:
        raise AssertionError(f"large random failed: H={H} W={W} got={got} exp={exp}")

    print("selftest ok")


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    H = int(next(it))
    W = int(next(it))

    if H <= 1 or W <= 1:
        print(0)
        return

    N = 1 << W
    freq = [0] * N
    for s in it:
        freq[int(s, 2)] += 1

    del data, it
    print(solve_from_freq(H, W, freq))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    else:
        main()
import sys

def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h = step

def main():
    data = sys.stdin.buffer.read().split()
    if not data: return
    W = int(data[1])
    n = 1 << W
    cnt = [0] * n
    for s in data[2:]: cnt[int(s, 2)] += 1
    C = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i): C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    fval = [s if s <= W - s else W - s for s in range(W + 1)]
    Fhat = [0] * (W + 1)
    for t in range(W + 1):
        total = 0
        Ct = C[t]
        Cw = C[W - t]
        wt = W - t
        for s, f in enumerate(fval):
            if f == 0: continue
            lo = s - wt
            if lo < 0: lo = 0
            hi = s if s < t else t
            inner = 0
            for j in range(lo, hi + 1):
                if j & 1: inner -= Ct[j] * Cw[s - j]
                else: inner += Ct[j] * Cw[s - j]
            total += f * inner
        Fhat[t] = total
    fwht(cnt)
    for i in range(n): cnt[i] *= Fhat[i.bit_count()]
    fwht(cnt)
    print(min(cnt) // n)

if __name__ == "__main__": main()
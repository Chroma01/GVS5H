import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    H = int(data[0]); W = int(data[1])
    rows = data[2:]
    masks = []
    for s in rows:
        m = 0
        for j, ch in enumerate(s):
            if ch == '1':
                m |= 1 << j
        masks.append(m)
    S = 1 << W
    freq = [0] * S
    for m in masks:
        freq[m] += 1

    def fwht(a):
        n = len(a)
        step = 1
        while step < n:
            for i in range(0, n, step * 2):
                for j in range(i, i + step):
                    u = a[j]
                    v = a[j + step]
                    a[j] = u + v
                    a[j + step] = u - v
            step <<= 1
        return a

    # popcounts
    pc = [0] * S
    for i in range(1, S):
        pc[i] = pc[i >> 1] + (i & 1)

    # weights
    w = [0] * (W + 1)
    for k in range(W + 1):
        w[k] = k if k <= W - k else W - k

    # combined transform of weighted indicator functions
    W_hat = [0] * S
    for k in range(W + 1):
        Gk = [0] * S
        for mask in range(S):
            if pc[mask] == k:
                Gk[mask] = 1
        Gk_hat = fwht(Gk)
        wk = w[k]
        for i in range(S):
            W_hat[i] += wk * Gk_hat[i]

    F_hat = fwht(freq[:])
    for i in range(S):
        F_hat[i] *= W_hat[i]
    ans_arr = fwht(F_hat)
    # divide by S to get true convolution result
    n = S
    # all values are integers, ans_arr[i] should be divisible by S
    min_val = ans_arr[0] // n
    for v in ans_arr[1:]:
        v //= n
        if v < min_val:
            min_val = v
    print(min_val)

if __name__ == "__main__":
    main()
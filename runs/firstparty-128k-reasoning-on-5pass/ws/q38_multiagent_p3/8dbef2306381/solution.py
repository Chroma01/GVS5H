import sys

def compose(a, b):
    c = [0] * len(a)
    for i, row in enumerate(a):
        m = 0
        while row:
            lsb = row & -row
            m |= b[lsb.bit_length() - 1]
            row ^= lsb
        c[i] = m
    return c

def apply_pow(pows, g, s):
    while g:
        lsb = g & -g
        k = lsb.bit_length() - 1
        r = 0
        bit = 1
        for row in pows[k]:
            if row & s:
                r |= bit
            bit <<= 1
        s = r
        if not s:
            return 0
        g ^= lsb
    return s

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M, A, B = data[:4]
    vals = data[4:]

    mask = (1 << B) - 1
    T = [0] * B
    T[0] = ((1 << (B - A + 1)) - 1) << (A - 1)
    for i in range(1, B):
        T[i] = 1 << (i - 1)

    pows = [T]
    while (1 << len(pows)) <= N:
        pows.append(compose(pows[-1], pows[-1]))

    pos = 1
    s = 1
    idx = 0

    for _ in range(M):
        L = vals[idx]
        R = vals[idx + 1]
        idx += 2

        g = L - 1 - pos
        if g:
            s = apply_pow(pows, g, s)
            if not s:
                print("No")
                return

        length = R - L + 1
        if length >= B:
            print("No")
            return

        s = (s << length) & mask
        if not s:
            print("No")
            return

        pos = R

    g = N - pos
    if g:
        s = apply_pow(pows, g, s)

    print("Yes" if s & 1 else "No")

if __name__ == "__main__":
    main()
import sys


def main():
    data = sys.stdin.buffer.read() + b' '
    d = data
    i = 0

    while d[i] <= 32:
        i += 1
    N = 0
    while d[i] > 32:
        N = N * 10 + (d[i] - 48)
        i += 1

    TH = 3000

    # Small N: direct endpoint enumeration, only within the same parity.
    if N <= TH:
        st = set()
        add = st.add
        evens = []
        odds = []
        ev = evens.append
        od = odds.append

        for _ in range(N):
            while d[i] <= 32:
                i += 1
            x = 0
            while d[i] > 32:
                x = x * 10 + (d[i] - 48)
                i += 1
            add(x)
            if x & 1:
                od(x)
            else:
                ev(x)

        del data, d

        contains = st.__contains__
        ans = 0
        for lst in (evens, odds):
            m = len(lst)
            for ai in range(m - 1):
                a = lst[ai]
                for bi in range(ai + 1, m):
                    if contains((a + lst[bi]) >> 1):
                        ans += 1

        sys.stdout.write(str(ans) + '\n')
        return

    # Main path: parity-split packed-integer convolution.
    MAXV = 1000000
    pres = bytearray(MAXV + 32)

    MAX_U = MAXV >> 1
    BUILD_LEN = (19 * MAX_U) // 8 + 4
    build0 = bytearray(BUILD_LEN)  # even values 2u
    build1 = bytearray(BUILD_LEN)  # odd values 2u+1
    BITS = (1, 2, 4, 8, 16, 32, 64, 128)

    maxS = 0
    for _ in range(N):
        while d[i] <= 32:
            i += 1
        x = 0
        while d[i] > 32:
            x = x * 10 + (d[i] - 48)
            i += 1

        pres[x] = 1
        if x > maxS:
            maxS = x

        u = x >> 1
        pos = 19 * u
        idx = pos >> 3
        bit = BITS[pos & 7]

        if x & 1:
            build1[idx] |= bit
        else:
            build0[idx] |= bit

    del data, d

    # 8 coefficients of 19 bits each occupy exactly 19 bytes.
    blocks = (maxS + 8) // 8
    L = 19 * blocks + 4

    x0 = int.from_bytes(build0, 'little')
    del build0
    x1 = int.from_bytes(build1, 'little')
    del build1

    y0 = x0 * x0
    del x0
    b0 = y0.to_bytes(L, 'little')
    del y0

    y1 = x1 * x1
    del x1
    b1 = y1.to_bytes(L, 'little')
    del y1

    m = 0x7FFFF  # (1 << 19) - 1
    total = 0
    p = pres
    fb = int.from_bytes

    t0 = 0
    stop = 19 * blocks
    for base in range(0, stop, 19):
        v0 = fb(b0[base:base + 19], 'little')
        v1 = fb(b1[base:base + 19], 'little')

        if p[t0]:
            total += v0 & m
        if p[t0 + 1]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 1]:
            total += v0 & m
        if p[t0 + 2]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 2]:
            total += v0 & m
        if p[t0 + 3]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 3]:
            total += v0 & m
        if p[t0 + 4]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 4]:
            total += v0 & m
        if p[t0 + 5]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 5]:
            total += v0 & m
        if p[t0 + 6]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 6]:
            total += v0 & m
        if p[t0 + 7]:
            total += v1 & m
        v0 >>= 19
        v1 >>= 19

        if p[t0 + 7]:
            total += v0 & m
        if p[t0 + 8]:
            total += v1 & m

        t0 += 8

    ans = (total - N) // 2
    sys.stdout.write(str(ans) + '\n')


if __name__ == '__main__':
    main()
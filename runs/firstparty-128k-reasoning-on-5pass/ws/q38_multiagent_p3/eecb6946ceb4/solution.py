import sys
from array import array
import gc


def main():
    gc.disable()

    data = sys.stdin.buffer.read()
    L = len(data)
    i = 0

    while i < L and data[i] <= 32:
        i += 1

    n = 0
    while i < L:
        c = data[i]
        if c <= 32:
            break
        n = n * 10 + (c - 48)
        i += 1

    if n < 3:
        sys.stdout.write("0\n")
        return

    tc = 'I'
    if array('I').itemsize < 4:
        tc = 'L'

    vals = array(tc, [0]) * n
    minv = 10**18
    maxv = 0

    for k in range(n):
        while i < L and data[i] <= 32:
            i += 1

        x = 0
        while i < L:
            c = data[i]
            if c <= 32:
                break
            x = x * 10 + (c - 48)
            i += 1

        vals[k] = x
        if x < minv:
            minv = x
        if x > maxv:
            maxv = x

    del data

    M = maxv - minv + 1

    if n <= 2000:
        sv = sorted(vals)
        s = set(sv)
        contains = s.__contains__
        ans = 0

        for idx in range(n):
            b = sv[idx]
            tb = b + b
            for j in range(idx):
                if contains(tb - sv[j]):
                    ans += 1

        sys.stdout.write(str(ans) + "\n")
        return

    # Pack indicator g[i] as bit 20*i.
    # For even i: byte floor(5*i/2), bit 0  -> byte value 1.
    # For odd  i: byte floor(5*i/2), bit 4  -> byte value 16.
    pack_len = (5 * (M - 1) // 2) + 1
    pack = bytearray(pack_len)
    mn = minv

    for x in vals:
        idx = x - mn
        if idx & 1:
            pack[(5 * idx) // 2] = 16
        else:
            pack[(5 * idx) // 2] = 1

    X = int.from_bytes(pack, 'little')
    del pack

    Y = X * X
    del X

    prod_len = ((2 * M + 1) * 20 + 7) // 8
    pb = Y.to_bytes(prod_len, 'little')
    del Y

    ans = 0
    for x in vals:
        j = (x - mn) * 5
        c = (pb[j] | (pb[j + 1] << 8) | (pb[j + 2] << 16)) & 0xfffff
        ans += (c - 1) >> 1

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
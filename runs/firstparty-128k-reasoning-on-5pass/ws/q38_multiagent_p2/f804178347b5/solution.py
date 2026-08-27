import sys


def main():
    data = sys.stdin.buffer.read()
    if not data:
        return

    # Parse N manually so that digits of N are not mistaken for bits.
    i = 0
    ndata = len(data)
    while i < ndata and data[i] <= 32:
        i += 1

    N = 0
    while i < ndata and 48 <= data[i] <= 57:
        N = N * 10 + (data[i] - 48)
        i += 1

    L = 3 ** N

    # Collect exactly L bits from the rest of the input.
    # This works for both "010..." and "0 1 0 ...".
    bits = bytearray(L)
    idx = 0
    for ch in data[i:]:
        if ch == 48 or ch == 49:
            bits[idx] = ch - 48
            idx += 1
            if idx == L:
                break

    # cost[x] = minimum flips in subtree x to change node x's bit.
    # Leaves need exactly one flip.
    cost = [1] * L

    m = L
    b = bits
    c = cost

    # Bottom-up reduction of triples.
    while m > 1:
        nm = m // 3
        j = 0
        for p in range(nm):
            b0 = b[j]
            b1 = b[j + 1]
            b2 = b[j + 2]
            s = b0 + b1 + b2

            c0 = c[j]
            c1 = c[j + 1]
            c2 = c[j + 2]

            if s == 1:
                # Majority bit is 0. Need to flip one of the two 0-children.
                if b0 == 0:
                    if b1 == 0:
                        pc = c0 if c0 < c1 else c1
                    else:
                        pc = c0 if c0 < c2 else c2
                else:
                    pc = c1 if c1 < c2 else c2
                pb = 0
            elif s == 2:
                # Majority bit is 1. Need to flip one of the two 1-children.
                if b0 == 1:
                    if b1 == 1:
                        pc = c0 if c0 < c1 else c1
                    else:
                        pc = c0 if c0 < c2 else c2
                else:
                    pc = c1 if c1 < c2 else c2
                pb = 1
            else:
                # All three child bits are equal. Need to flip two children.
                if s == 3:
                    pb = 1
                else:
                    pb = 0

                mx = c0
                if c1 > mx:
                    mx = c1
                if c2 > mx:
                    mx = c2
                pc = c0 + c1 + c2 - mx

            b[p] = pb
            c[p] = pc
            j += 3

        m = nm

    sys.stdout.write(str(c[0]))


if __name__ == "__main__":
    main()
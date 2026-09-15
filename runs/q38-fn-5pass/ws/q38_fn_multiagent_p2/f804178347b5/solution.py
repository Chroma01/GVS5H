import sys


def solve():
    raw = sys.stdin.buffer.read()
    if not raw:
        return

    # Parse N manually, then keep only the binary digits from the rest.
    # Deleting all bytes <= 32 supports both contiguous strings and spaced digits.
    L = len(raw)
    pos = 0
    while pos < L and raw[pos] <= 32:
        pos += 1

    n = 0
    while pos < L and raw[pos] > 32:
        n = n * 10 + (raw[pos] - 48)
        pos += 1

    delete = bytes(range(33))
    s = raw[pos:].translate(None, delete)

    expected = 3 ** n
    if len(s) > expected:
        s = s[:expected]

    m = len(s)
    if m <= 1:
        sys.stdout.write("1\n" if m == 1 else "0\n")
        return

    # bits stores current output bits. Leaves are ASCII '0'/'1'; internal nodes are 0/1.
    # costs stores the minimum flips needed to force the opposite of the current bit.
    bits = bytearray(s)
    del raw, s

    costs = [1] * m
    bts = bits
    cst = costs

    # Bottom-up ternary-tree DP, in place.
    while m > 1:
        new_m = m // 3
        i = 0
        j = 0

        for _ in range(new_m):
            b0 = bts[j] & 1
            b1 = bts[j + 1] & 1
            b2 = bts[j + 2] & 1

            c0 = cst[j]
            c1 = cst[j + 1]
            c2 = cst[j + 2]

            sm = b0 + b1 + b2

            if sm >= 2:
                pbit = 1
                target = 0
            else:
                pbit = 0
                target = 1

            # Cost for each child to output target:
            # 0 if it already outputs target, otherwise its cost to force opposite.
            if b0 == target:
                d0 = 0
            else:
                d0 = c0

            if b1 == target:
                d1 = 0
            else:
                d1 = c1

            if b2 == target:
                d2 = 0
            else:
                d2 = c2

            # Parent needs at least two children outputting target.
            # This is equivalent to enumerating the 8 child-flip subsets.
            if d0 <= d1:
                if d1 <= d2:
                    cost = d0 + d1
                elif d0 <= d2:
                    cost = d0 + d2
                else:
                    cost = d1 + d2
            else:
                if d0 <= d2:
                    cost = d1 + d0
                elif d1 <= d2:
                    cost = d1 + d2
                else:
                    cost = d0 + d2

            bts[i] = pbit
            cst[i] = cost

            i += 1
            j += 3

        m = new_m

    sys.stdout.write(str(cst[0]) + "\n")


if __name__ == "__main__":
    solve()
import sys

IDENTITY = bytes(range(256))
DELETE = bytes([c for c in range(256) if c != 48 and c != 49])
TABLE = bytes.maketrans(b'01', b'\x00\x01')

# m = b0 + 2*b1 + 4*b2, where b0,b1,b2 are the three child bits.
MAJ = bytes([0, 0, 0, 1, 0, 1, 1, 1])

# Flip-cost case:
# 0: sum of two smallest of c0,c1,c2
# 1: min(c1,c2)
# 2: min(c0,c2)
# 3: min(c0,c1)
TYP = bytes([0, 1, 2, 3, 3, 2, 1, 0])

# First level: leaves all have flip cost 1.
# Uniform triple costs 2 to flip, mixed triple costs 1.
FIRST = bytes([2, 1, 1, 1, 1, 1, 1, 2])


def solve():
    data = sys.stdin.buffer.read()
    n = len(data)

    # Parse N (robust against leading non-digits).
    i = 0
    while i < n and (data[i] < 48 or data[i] > 57):
        i += 1

    N = 0
    while i < n:
        ch = data[i]
        if 48 <= ch <= 57:
            N = N * 10 + (ch - 48)
            i += 1
        else:
            break

    L = 3 ** N

    # Keep only ASCII '0' and '1', then map them to raw 0/1 bytes.
    b_ascii = data[i:].translate(IDENTITY, DELETE)
    del data
    b = b_ascii.translate(TABLE)
    del b_ascii

    if len(b) > L:
        b = b[:L]
    elif len(b) < L:
        b = b + b'\x00' * (L - len(b))

    # Not needed for the official constraints (N >= 1), but harmless.
    if L == 1:
        print(1)
        return

    # Build the first internal level directly from leaves.
    size = L
    new_size = size // 3
    bits = [0] * new_size
    costs = [0] * new_size

    maj = MAJ
    first = FIRST
    j = 0
    for i in range(0, size, 3):
        m = b[i] + (b[i + 1] << 1) + (b[i + 2] << 2)
        bits[j] = maj[m]
        costs[j] = first[m]
        j += 1

    del b
    size = new_size

    typ = TYP

    # Bottom-up DP over the remaining internal levels.
    while size > 1:
        new_size = size // 3
        nb = [0] * new_size
        nc = [0] * new_size

        b = bits
        c = costs
        j = 0

        for i in range(0, size, 3):
            b0 = b[i]
            b1 = b[i + 1]
            b2 = b[i + 2]
            m = b0 + (b1 << 1) + (b2 << 2)

            nb[j] = maj[m]

            c0 = c[i]
            c1 = c[i + 1]
            c2 = c[i + 2]

            t = typ[m]
            if t == 0:
                mx = c0
                if c1 > mx:
                    mx = c1
                if c2 > mx:
                    mx = c2
                nc[j] = c0 + c1 + c2 - mx
            elif t == 1:
                nc[j] = c1 if c1 < c2 else c2
            elif t == 2:
                nc[j] = c0 if c0 < c2 else c2
            else:
                nc[j] = c0 if c0 < c1 else c1

            j += 1

        bits = nb
        costs = nc
        size = new_size

    print(costs[0])


if __name__ == "__main__":
    solve()
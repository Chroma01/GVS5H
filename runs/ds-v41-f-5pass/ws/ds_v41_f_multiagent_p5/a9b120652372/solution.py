import sys


def answer(A, B):
    ONE = 49  # ord('1')
    m = A.count(ONE)
    k = B.count(ONE)
    if m < k:
        return -1

    af = A.find(ONE)
    al = A.rfind(ONE)
    bf = B.find(ONE)
    bl = B.rfind(ONE)

    # the span of the occupied set can never increase
    if (al - af) < (bl - bf):
        return -1

    # gaps between consecutive pieces of A
    g = []
    p = af
    while True:
        q = A.find(ONE, p + 1)
        if q < 0:
            break
        g.append(q - p)
        p = q

    # gaps between consecutive pieces of B
    h = []
    p = bf
    while True:
        q = B.find(ONE, p + 1)
        if q < 0:
            break
        h.append(q - p)
        p = q

    D = (al - af) - (bl - bf)   # required total span reduction
    d1 = bf - af                # net move of the leftmost piece
    need = k - 1
    best = -1

    for u1 in (0, 1):           # u1 = number of ops centred at the first piece
        j = 0
        pg = 0                  # parity of A-gaps strictly before current gap
        ph = 0                  # parity of already matched h-gaps
        for gi in g:
            if j == need:
                break
            hj = h[j]
            if gi >= hj and (gi > hj or (pg ^ ph) == u1):
                j += 1
                ph ^= (hj & 1)
            pg ^= (gi & 1)
        if j == need:
            c = u1 + d1
            o = ((u1 + D) & 1) + D - d1
            if o > c:
                c = o
            if best < 0 or c < best:
                best = c

    return best


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        idx += 1                 # skip N (== len of A / B)
        A = data[idx]; idx += 1
        B = data[idx]; idx += 1
        out.append(str(answer(A, B)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
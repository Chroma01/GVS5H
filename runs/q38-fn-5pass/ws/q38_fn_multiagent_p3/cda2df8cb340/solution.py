import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Compress equal values.  For each distinct value v with frequency c,
    # a residue group needs:
    #   count += c
    #   sum   += v * c
    # Pack both into one integer: (sum << SHIFT) | count.
    freq = {}
    get = freq.get
    for i in range(1, n + 1):
        a = data[i]
        freq[a] = get(a, 0) + 1
    del data, get

    SHIFT = 19
    CMASK = (1 << SHIFT) - 1

    vals = []
    adds = []
    total = 0
    max_a = 0
    diag = 0

    for v, c in freq.items():
        vals.append(v)
        vc = v * c
        total += vc
        if v > max_a:
            max_a = v
        diag += c * (v // (v & -v))
        adds.append((vc << SHIFT) + c)
    del freq

    m_count = len(vals)

    # H_0: ordered sum of (a+b) over all ordered pairs.
    ordered = 2 * n * total
    max_sum = 2 * max_a

    # Use dense lists for small moduli, dictionaries for large sparse ones.
    list_limit = min(1 << 20, 8 * m_count)

    m = 2
    shift = SHIFT
    cmask = CMASK
    A = vals
    adds_local = adds

    while m <= max_sum:
        mask = m - 1

        if m <= list_limit:
            arr = [0] * m

            for a, add in zip(A, adds_local):
                arr[a & mask] += add

            num = 0
            half = m >> 1

            # Self-complementary residues: 0 and m/2.
            p = arr[0]
            if p:
                num += 2 * (p & cmask) * (p >> shift)

            p = arr[half]
            if p:
                num += 2 * (p & cmask) * (p >> shift)

            # Other complementary residue pairs: r and m-r.
            for r in range(1, half):
                p = arr[r]
                if p:
                    q = arr[m - r]
                    if q:
                        num += 2 * (
                            (p & cmask) * (q >> shift)
                            + (q & cmask) * (p >> shift)
                        )

            ordered -= num // m
            del arr

        else:
            d = {}
            get = d.get

            for a, add in zip(A, adds_local):
                r = a & mask
                d[r] = get(r, 0) + add

            num = 0
            get = d.get

            for r, p in d.items():
                comp = (-r) & mask
                if r > comp:
                    continue

                if r == comp:
                    num += 2 * (p & cmask) * (p >> shift)
                else:
                    q = get(comp)
                    if q is not None:
                        num += 2 * (
                            (p & cmask) * (q >> shift)
                            + (q & cmask) * (p >> shift)
                        )

            ordered -= num // m
            del d, get

        m <<= 1

    ans = (ordered + diag) // 2
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()
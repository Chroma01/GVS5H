import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    del data

    if n == 0:
        print(0)
        return

    total = (n + 1) * sum(a)
    ans = total

    max_a = max(a)
    limit = max_a * 2

    # Encode (count, sum) as count * SHIFT + sum.
    # Max possible sum in one residue class is N * max(A) <= 2e12 < 2^42.
    SHIFT_BITS = 42
    SHIFT = 1 << SHIFT_BITS
    SUM_MASK = SHIFT - 1

    # For small moduli, a direct list is faster than a dictionary.
    ARRAY_LIMIT = 1 << 18

    m = 2
    while m <= limit:
        mask = m - 1
        half = m >> 1
        corr = 0

        if m <= ARRAY_LIMIT:
            d = [0] * m
            base = SHIFT

            for x in a:
                d[x & mask] += base + x

            sh = SHIFT_BITS
            sm = SUM_MASK

            val = d[0]
            if val:
                c = val >> sh
                s = val & sm
                corr += ((c + 1) * s) // m

            for r in range(1, half):
                val = d[r]
                if val:
                    val2 = d[m - r]
                    if val2:
                        c = val >> sh
                        s = val & sm
                        c2 = val2 >> sh
                        s2 = val2 & sm
                        corr += (c2 * s + c * s2) // m

            val = d[half]
            if val:
                c = val >> sh
                s = val & sm
                corr += ((c + 1) * s) // m

        else:
            d = {}
            get = d.get
            base = SHIFT

            for x in a:
                r = x & mask
                d[r] = get(r, 0) + base + x

            sh = SHIFT_BITS
            sm = SUM_MASK

            for r, val in d.items():
                if r > half:
                    continue

                if r == 0 or r == half:
                    c = val >> sh
                    s = val & sm
                    corr += ((c + 1) * s) // m
                else:
                    val2 = get(m - r)
                    if val2 is not None:
                        c = val >> sh
                        s = val & sm
                        c2 = val2 >> sh
                        s2 = val2 & sm
                        corr += (c2 * s + c * s2) // m

        ans -= corr
        m <<= 1

    print(ans)


if __name__ == "__main__":
    solve()